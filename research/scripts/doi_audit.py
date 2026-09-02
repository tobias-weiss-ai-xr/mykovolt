#!/usr/bin/env python3
"""DOI / title audit for papers.yaml.

Verifies every paper's DOI resolves via CrossRef *and* that the CrossRef
title actually matches the title in papers.yaml (word-overlap >= 50 %).

Why this exists:
  An earlier corpus accumulated 23 hallucinated entries (dead DOIs, or DOIs
  pointing to unrelated papers — e.g. a 'fungal fuel cell' DOI resolving to
  a lung-cancer-diagnosis paper). This script makes that impossible to merge
  unnoticed: run it in CI and it fails fast on corruption.

Usage:
    python3 scripts/doi_audit.py            # exit 0 if clean, 1 if any DOI bad
    python3 scripts/doi_audit.py --json       # machine-readable report
    python3 scripts/doi_audit.py --strict     # also fail on network/rate-limit

Design choices:
  - arXiv entries have no DOI: skipped with a note (the corpus is
    CrossRef/OpenAlex-based for quality).
  - CrossRef 429 (rate limit) => exponential backoff retry (up to 4).
  - 5xx / connection errors are retried then reported as NETWORK;
    by default they do NOT fail the build (network flakiness) — with
    --strict they do.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

import requests
import yaml

# allow both `python3 scripts/doi_audit.py` and `from scripts.doi_audit`
try:
    import research_config  # when cwd is research/
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import research_config

CROSSREF_URL = "https://api.crossref.org/works/{doi}"
MAILTO = "business@tobias-weiss.org"
UA = "MykoVolt-Research/1.0 (mailto:business@tobias-weiss.org)"
OVERLAP_THRESHOLD = 0.50
PACE_SECONDS = 0.35  # ~35 req/min (Crossref polite-pool tolerance)

STOPWORDS = {
    "a", "an", "the", "of", "for", "in", "and", "with", "using", "based",
    "on", "via", "to", "from", "by", "at", "is", "are", "&",
}


def _words(text: str) -> set:
    return {
        w for w in re.sub(r"[^a-z0-9 ]", " ", text.lower()).split()
        if w and w not in STOPWORDS and len(w) > 1
    }


def _overlap(a: str, b: str) -> float:
    wa, wb = _words(a), _words(b)
    if not wa and not wb:
        return 1.0
    return len(wa & wb) / max(len(wa | wb), 1)


def check_doi(doi: str) -> tuple:
    """Return (status, detail). status in {OK, NOT_FOUND, MISMATCH, NETWORK}."""
    for attempt in range(4):
        try:
            r = requests.get(CROSSREF_URL.format(doi=doi),
                             timeout=20, headers={"User-Agent": UA})
        except requests.RequestException:
            time.sleep(3 * (attempt + 1))
            continue
        if r.status_code == 429:
            time.sleep(10 * (attempt + 1)); continue
        if r.status_code >= 500:
            time.sleep(2 * (attempt + 1)); continue
        if r.status_code == 404:
            return "NOT_FOUND", doi
        if r.status_code == 200:
            titles = r.json().get("message", {}).get("title", [])
            return "OK", (titles[0] if titles else "")
        return "NETWORK", f"HTTP {r.status_code}"
    return "NETWORK", "rate-limited or unreachable"


def audit_papers(papers: list, strict: bool = False) -> list:
    """Return a list of problem dicts. Empty list == clean corpus."""
    problems = []
    for i, p in enumerate(papers):
        title = p.get("title", "")
        doi = (p.get("doi") or "").strip().lower()
        url = (p.get("url") or "")
        m = re.search(r"doi\.org/(10\.\S+)", url)
        if m and not doi:
            doi = m.group(1).lower()
        if not doi:
            problems.append({"idx": i, "title": title, "status": "NO_DOI", "detail": "no DOI"})
            continue

        status, detail = check_doi(doi)
        time.sleep(PACE_SECONDS)
        rec = {"idx": i, "doi": doi, "title": title, "status": status}

        if status == "NOT_FOUND":
            rec["detail"] = "doi does not resolve (404)"
            problems.append(rec)
        elif status == "OK" and detail:
            ov = _overlap(title, detail)
            rec["detail"] = f"overlap={ov:.2f}"
            if ov < OVERLAP_THRESHOLD:
                rec["status"] = "MISMATCH"
                rec["detail"] = f"title mismatch (overlap {ov:.2f}); CrossRef: '{detail[:90]}'"
                problems.append(rec)
        elif status == "NETWORK":
            rec["detail"] = detail
            if strict:
                problems.append(rec)
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit papers.yaml DOI/title integrity")
    ap.add_argument("--strict", action="store_true",
                    help="Fail also on network/rate-limit errors")
    ap.add_argument("--json", action="store_true", help="Emit JSON report")
    args = ap.parse_args()

    yaml_path = Path(__file__).resolve().parent.parent / "papers.yaml"
    data = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
    papers = data.get("papers", [])
    problems = audit_papers(papers, strict=args.strict)

    if args.json:
        print(json.dumps({"total": len(papers), "problems": problems}, indent=2))
    else:
        corrupt = [p for p in problems if p["status"] in ("NOT_FOUND", "MISMATCH", "NO_DOI")]
        print(f"DOI audit: {len(papers)} papers, {len(corrupt)} corrupt, "
              f"{len(problems) - len(corrupt)} network/notes")
        for pr in problems:
            tit = (pr.get("title") or "")[:60]
            print(f"  [{pr['status']}] #{pr['idx']} | {tit} | {pr.get('detail','')}")

    corrupt = [p for p in problems if p["status"] in ("NOT_FOUND", "MISMATCH", "NO_DOI")]
    return 1 if corrupt else 0


if __name__ == "__main__":
    sys.exit(main())
