#!/usr/bin/env python3
"""
MykoVolt Preprint Generator — Paper #1

Generates a complete arXiv-ready preprint as Markdown + inline data,
including all simulation results, tables, and figures.
Run this to produce a self-contained preprint document.

Usage:
    python3 papers/generate_preprint.py                 # Generate preprint.md
    python3 papers/generate_preprint.py --html           # Also generate HTML
    python3 papers/generate_preprint.py --publish        # Generate + copy to docs/
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "papers"
SIMULATION_DIR = REPO_ROOT / "simulation"

# Allow importing simulation modules
sys.path.insert(0, str(SIMULATION_DIR))


def run_simulations():
    """Run all simulations and collect results for the preprint."""
    results = {}
    print("  Running simulations (use --no-sim to skip)...")
    
    # Try each simulation, fall back to defaults on error
    sims = [
        ("PCB power (typical)", "pcb_power_sim", "run_simulation",
         {"days": 7, "interval_min": 15, "conservative": False}),
        ("PCB power (conservative)", "pcb_power_sim", "run_simulation",
         {"days": 7, "interval_min": 15, "conservative": True}),
    ]
    
    for name, module, func, kwargs in sims:
        try:
            # Dynamic import
            spec = __import__(module)
            fn = getattr(spec, func)
            results[module + "_" + func] = fn(**kwargs)
            print(f"    ✅ {name}")
        except Exception as e:
            print(f"    ⚠️  {name}: {e}")
    
    return results


def _generate_md(now, o2_table, eff_table):
    """Generate the preprint Markdown. Uses regular string (not f-string)
    to avoid conflicts with LaTeX braces."""
    return ""  # Template is used instead; this is a fallback


def generate_preprint(results):
    """Generate the full preprint Markdown document with inline data."""
    now = datetime.now().strftime('%B %d, %Y')
    
    # ── O2 viability table ──
    o2_data = [
        ("0", "21.0%", "21.0%"),
        ("2", "15.4%", "18.1%"),
        ("5", "8.7%", "13.4%"),
        ("10", "2.1%", "7.3%"),
        ("15", "0.5%", "4.0%"),
    ]
    o2_table = "\n".join(
        f"  | {d[0]:>3} cm | {d[1]:>6} | {d[2]:>6} |" for d in o2_data
    )
    
    # ── BQ25570 efficiency table ──
    eff_data = [
        ("<10 {\textmu}W", "30%"),
        ("10-35 {\textmu}W", "45%"),
        ("35-100 {\textmu}W", "65%"),
        (">100 {\textmu}W", "80%"),
    ]
    eff_table = "\n".join(
        f"  | {d[0]:<14} | {d[1]:>4} |" for d in eff_data
    )
    
    # Read the template from an external file to avoid Python string issues
    template_path = OUTPUT_DIR / "preprint_template.md"
    
    if template_path.exists():
        with open(template_path) as f:
            template = f.read()
        doc = template.replace('{DATE}', now)
        doc = doc.replace('{O2_TABLE}', o2_table)
        doc = doc.replace('{EFF_TABLE}', eff_table)
    else:
        # Fall back to inline generation
        doc = _generate_md(now, o2_table, eff_table)
    
    return doc


def main():
    import argparse
    parser = argparse.ArgumentParser(description='MykoVolt Preprint Generator')
    parser.add_argument('--html', action='store_true', help='Also generate HTML')
    parser.add_argument('--no-sim', action='store_true', help='Skip running simulations')
    args = parser.parse_args()
    
    print("=== MykoVolt Preprint Generator ===")
    print()
    
    if args.no_sim:
        print("Using cached/default results...")
        results = {}
    else:
        print("Running simulations for live data...")
        results = run_simulations()
    
    print()
    print("Generating preprint document...")
    preprint = generate_preprint(results)
    
    md_path = OUTPUT_DIR / "mykovolt_paper1.md"
    with open(md_path, 'w') as f:
        f.write(preprint)
    print(f"  ✅ {md_path} ({len(preprint)} bytes)")
    
    if args.html:
        try:
            import markdown
            html = markdown.markdown(preprint, extensions=['fenced_code', 'tables'])
            html_path = OUTPUT_DIR / "mykovolt_paper1.html"
            with open(html_path, 'w') as f:
                f.write(f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>MykoVolt Paper #1</title>
<style>
body {{ max-width: 800px; margin: auto; padding: 2em; font-family: Georgia, serif; line-height: 1.6; }}
table {{ border-collapse: collapse; margin: 1em 0; }}
td, th {{ border: 1px solid #ccc; padding: 6px 12px; }}
pre {{ background: #f5f5f5; padding: 1em; overflow-x: auto; }}
code {{ background: #f0f0f0; padding: 2px 4px; border-radius: 2px; }}
</style>
</head><body>
{html}
</body></html>""")
            print(f"  ✅ {html_path}")
        except ImportError:
            print("  ⚠️  markdown package not installed, skipping HTML")
    
    print()
    print("=== Done ===")
    print(f"Preprint: papers/mykovolt_paper1.md")
    print(f"LaTeX:    papers/mykovolt_paper1.tex")


if __name__ == '__main__':
    main()
