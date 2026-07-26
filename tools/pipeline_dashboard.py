#!/usr/bin/env python3
"""
MykoVolt Pipeline Dashboard — CLI tool for business development tracking.

Usage:
    python3 tools/pipeline_dashboard.py          # Full dashboard
    python3 tools/pipeline_dashboard.py --week   # Weekly action items only
    python3 tools/pipeline_dashboard.py --check  # Check if any pipeline is stale (>14d)

Pipeline State File: ~/.mykovolt_pipeline.json (auto-created)
"""

import json
import os
import sys
from datetime import datetime, timedelta

STATE_FILE = os.path.expanduser("~/.mykovolt_pipeline.json")

DEFAULT_STATE = {
    "cofounder": {
        "identified": 3,       # 30 target
        "contacted": 0,        # 10/week
        "engaged": 0,          # 3-5 active
        "screened": 0,         # 1-3 deep
        "trial": 0,            # 1 trial project
        "onboarded": 0,        # 1 signed
        "last_action": None,
    },
    "funding": {
        "monitoring": 3,       # grants being watched
        "in_prep": 0,          # preparing application
        "submitted": 0,        # submitted, awaiting decision
        "in_review": 0,        # under review
        "funded": 0,           # awarded
        "total_secured_euro": 0,
        "last_action": None,
    },
    "customer": {
        "target_list": 10,     # 25 target
        "warm_contact": 1,     # 15 target
        "demo_given": 0,       # 10 target
        "trial_committed": 0,  # 5 target
        "paid": 0,             # 5 target
        "advocate": 0,         # 2 target
        "revenue_euro": 0,
        "last_action": None,
    },
    "product": {
        "simulation_complete": 6,  # 7 modules
        "experiment_design": 0,
        "lab_poc_data": False,
        "devkit_prototype": False,
        "beta_deployed": False,
        "trl": 2,
        "last_action": None,
    },
    "publication": {
        "data_collected": False,
        "analysis_done": False,
        "draft_started": False,
        "submitted": 0,
        "published": 0,
        "citations": 0,
        "last_action": None,
    },
}

PIPELINE_NAMES = {
    "cofounder": "👥 Co-Founder",
    "funding": "💰 Funding",
    "customer": "🎁 Customer",
    "product": "🔬 Product",
    "publication": "📄 Publication",
}

STAGE_TARGETS = {
    "cofounder": [
        ("identified", 30, "30+ names"),
        ("contacted", 40, "10+/week at peak"),
        ("engaged", 5, "3-5 active conversations"),
        ("screened", 3, "1-3 deep convos"),
        ("trial", 1, "1 trial project"),
        ("onboarded", 1, "1 signed"),
    ],
    "funding": [
        ("monitoring", None, "always active"),
        ("in_prep", 1, "≥1 in prep"),
        ("submitted", 1, "≥1 submitted"),
        ("funded", 1, "≥1 awarded"),
    ],
    "customer": [
        ("target_list", 25, "25+ labs"),
        ("warm_contact", 15, "15+ contacts"),
        ("demo_given", 10, "10+ demos"),
        ("trial_committed", 5, "5+ trials"),
        ("paid", 5, "5+ paying"),
        ("advocate", 2, "2+ advocates"),
    ],
    "product": [
        ("simulation_complete", 7, "7 modules done"),
        ("experiment_design", 1, "protocols written"),
    ],
}

WEEKLY_ACTIONS_TEMPLATE = """
┌─────────────────────────────────────────────────────────────┐
│  📋 THIS WEEK'S ACTIONS (Week of {date})                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  👥 Co-Founder                                             │
│  [ ] Send {cofounder_target} outreach emails               │
│  [ ] Follow up with {cofounder_followup} non-responders    │
│  [ ] 1 LinkedIn post about co-founder search               │
│                                                             │
│  💰 Funding                                                │
│  [ ] Check wissenschaft.hessen.de for new LOEWE calls      │
│  [ ] Draft 2-page LOEWE-Exploration concept for EMC        │
│  [ ] {funding_extra}                                       │
│                                                             │
│  🎁 Customer                                               │
│  [ ] Add {customer_target} new lab PIs to target list      │
│  [ ] Send 1 warm email to research group                   │
│  [ ] {customer_extra}                                      │
│                                                             │
│  🔬 Product                                                │
│  [ ] {product_action}                                       │
│                                                             │
│  📄 Publication                                            │
│  [ ] {publication_action}                                   │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  ⏱  Total estimated time: ~{total_hours}h this week         │
└─────────────────────────────────────────────────────────────┘
"""


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return dict(DEFAULT_STATE)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def fmt_bool(val):
    return "✅" if val else "⬜"


def fmt_pct(current, target):
    if target == 0:
        return "—"
    pct = min(100, int(current / target * 100))
    return f"{pct:3d}%"


def fmt_bar(current, target, width=20):
    if target == 0:
        return "░" * width
    filled = min(width, int(current / target * width))
    return "█" * filled + "░" * (width - filled)


def show_dashboard(state):
    print()
    print("═" * 65)
    print("  MYKOVOLT PIPELINE DASHBOARD")
    print(f"  {'Last updated: ' + datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("═" * 65)
    print()

    # ── Co-Founder Pipeline ──
    cf = state["cofounder"]
    print("  👥 CO-FOUNDER PIPELINE")
    print("  ─────────────────────")
    stages = [("Identified", cf["identified"], 30),
              ("Contacted", cf["contacted"], 40),
              ("Engaged  ", cf["engaged"], 5),
              ("Screened ", cf["screened"], 3),
              ("Trial    ", cf["trial"], 1),
              ("Onboarded", cf["onboarded"], 1)]
    for name, cur, tgt in stages:
        bar = fmt_bar(cur, tgt, 15)
        print(f"    {name}: {cur:3d}/{tgt:<3d}  {bar}  {fmt_pct(cur, tgt)}")
    print(f"    Last action: {cf['last_action'] or '—'}")
    print()

    # ── Funding Pipeline ──
    fu = state["funding"]
    print("  💰 FUNDING PIPELINE")
    print("  ─────────────────")
    print(f"    Monitoring: {fu['monitoring']} grants  |  In prep: {fu['in_prep']}")
    print(f"    Submitted:  {fu['submitted']}          |  Funded:  {fu['funded']}")
    print(f"    Total secured: €{fu['total_secured_euro']:,}")
    print(f"    Last action: {fu['last_action'] or '—'}")
    print()

    # ── Customer Pipeline ──
    cu = state["customer"]
    print("  🎁 CUSTOMER PIPELINE")
    print("  ───────────────────")
    stages = [("Target List ", cu["target_list"], 25),
              ("Warm Contact", cu["warm_contact"], 15),
              ("Demo        ", cu["demo_given"], 10),
              ("Trial       ", cu["trial_committed"], 5),
              ("Paid        ", cu["paid"], 5),
              ("Advocate    ", cu["advocate"], 2)]
    for name, cur, tgt in stages:
        bar = fmt_bar(cur, tgt, 15)
        print(f"    {name}: {cur:3d}/{tgt:<3d}  {bar}  {fmt_pct(cur, tgt)}")
    print(f"    Revenue: €{cu['revenue_euro']:,}")
    print(f"    Last action: {cu['last_action'] or '—'}")
    print()

    # ── Product Pipeline ──
    pr = state["product"]
    print("  🔬 PRODUCT PIPELINE")
    print("  ──────────────────")
    print(f"    TRL: {pr['trl']}")
    print(f"    Simulation modules: {pr['simulation_complete']}/7 {fmt_bar(pr['simulation_complete'], 7, 10)}")
    print(f"    Experiment design: {fmt_bool(pr['experiment_design'])}")
    print(f"    Lab PoC:           {fmt_bool(pr['lab_poc_data'])}")
    print(f"    DevKit prototype:  {fmt_bool(pr['devkit_prototype'])}")
    print(f"    Beta deployed:     {fmt_bool(pr['beta_deployed'])}")
    print()

    # ── Publication Pipeline ──
    pb = state["publication"]
    print("  📄 PUBLICATION PIPELINE")
    print("  ──────────────────────")
    print(f"    Data:     {fmt_bool(pb['data_collected'])}")
    print(f"    Analysis: {fmt_bool(pb['analysis_done'])}")
    print(f"    Draft:    {fmt_bool(pb['draft_started'])}")
    print(f"    Submitted: {pb['submitted']}")
    print(f"    Published: {pb['published']}")
    print(f"    Citations: {pb['citations']}")
    print()

    # ── Overall Health ──
    health = []
    if cf["engaged"] == 0:
        health.append("🔴 Co-founder: No active conversations")
    elif cf["engaged"] < 3:
        health.append("🟡 Co-founder: Only {cf['engaged']} active conversations")
    else:
        health.append("🟢 Co-founder: Pipeline active")

    health.append(f"🟢 Funding: {fu['monitoring']} grants monitored")

    if cu["target_list"] < 10:
        health.append("🔴 Customer: Target list needs growth")
    else:
        health.append(f"🟢 Customer: {cu['target_list']} targets")

    health.append(f"🟢 Product: Simulation complete at TRL {pr['trl']}")
    health.append("🟡 Publication: No papers drafted yet" if not pb["draft_started"] else "🟢 Publication: Active")

    print("  📊 PIPELINE HEALTH")
    print("  ─────────────────")
    for h in health:
        print(f"    {h}")
    print()

    # ── Urgent items ──
    urgent = []
    if cf["engaged"] == 0:
        urgent.append("❗ Co-founder: No one is engaged. Outreach must restart.")
    if cu["target_list"] < 15:
        urgent.append("❗ Customer: Target lab list needs to reach 25.")
    if not pb["draft_started"]:
        urgent.append("❗ Publication: Paper #1 can be drafted NOW with existing simulation data.")
    if fu["funded"] == 0 and fu["submitted"] == 0:
        urgent.append("❗ Funding: No grants submitted. Target LOEWE-Exploration with EMC.")

    if urgent:
        print("  ⚠️  URGENT ITEMS")
        print("  ──────────────")
        for u in urgent:
            print(f"    {u}")
        print()

    print(f"  State file: {STATE_FILE}")
    print("  Use --update <pipeline> <field> <value> to update")
    print()


def show_weekly(state):
    cf = state["cofounder"]
    cu = state["customer"]
    pr = state["product"]
    pb = state["publication"]

    # Smart targets based on current state
    cofounder_target = max(0, min(10, 40 - cf["contacted"]))
    cofounder_followup = max(0, cf["contacted"] - cf["engaged"])
    customer_target = max(0, min(5, 25 - cu["target_list"]))

    # Determine product action
    if pr["experiment_design"] == 0:
        product_action = "Write Empa replication protocol (protocols/empa_replication.md)"
    elif not pr["lab_poc_data"]:
        product_action = "Source lab materials for PoC (see materials_sourcing.csv)"
    elif not pr["devkit_prototype"]:
        product_action = "Start PCB layout for DevKit v0.1"
    else:
        product_action = "Review beta program structure"

    # Publication action
    if not pb["draft_started"]:
        publication_action = "Generate figures for Paper #1 from simulation outputs"
    elif pb["submitted"] == 0:
        publication_action = "Write Methods section for Paper #1 (30 min/day)"
    else:
        publication_action = "Respond to reviewer comments"

    # Funding extra
    funding_extra = "Ask EMC if they're interested in LOEWE-Exploration lead"

    total_hours = (cofounder_target * 0.3 + cofounder_followup * 0.1 + 
                   customer_target * 0.2 + 3)  # base 3h for other actions

    print(WEEKLY_ACTIONS_TEMPLATE.format(
        date=datetime.now().strftime("%Y-%m-%d"),
        cofounder_target=cofounder_target,
        cofounder_followup=cofounder_followup,
        customer_target=customer_target,
        funding_extra=funding_extra,
        customer_extra="Review competitive intelligence for talking points",
        product_action=product_action,
        publication_action=publication_action,
        total_hours=int(total_hours),
    ))


def cmd_update(args):
    if len(args) < 3:
        print("Usage: pipeline_dashboard.py --update <pipeline> <field> <value>")
        print("  pipeline: cofounder, funding, customer, product, publication")
        print("  field: any field name in that section")
        print("  value: integer for numeric fields, 'true'/'false' for bools")
        return

    state = load_state()
    pipeline = args[0]
    field = args[1]
    value = args[2]

    if pipeline not in state:
        print(f"Unknown pipeline: {pipeline}. Options: {', '.join(state.keys())}")
        return

    if field not in state[pipeline]:
        print(f"Unknown field '{field}' in {pipeline}. Options: {', '.join(state[pipeline].keys())}")
        return

    # Parse value
    if value.lower() == "true":
        val = True
    elif value.lower() == "false":
        val = False
    else:
        try:
            val = int(value)
        except ValueError:
            try:
                val = float(value)
            except ValueError:
                val = value  # keep as string (e.g., dates)

    old = state[pipeline][field]
    state[pipeline][field] = val
    state[pipeline]["last_action"] = datetime.now().isoformat()
    save_state(state)
    print(f"✅ Updated {pipeline}.{field}: {old} → {val}")


def cmd_check(state):
    """Check for stale pipelines (>14 days since last action)."""
    now = datetime.now()
    stale = []
    for key, pipe in state.items():
        last = pipe.get("last_action")
        if last:
            try:
                dt = datetime.fromisoformat(last)
                days = (now - dt).days
                if days > 14:
                    stale.append((PIPELINE_NAMES.get(key, key), days))
            except (ValueError, TypeError):
                pass
        else:
            stale.append((PIPELINE_NAMES.get(key, key), "never"))

    if stale:
        print("\n  ⚠️  STALE PIPELINES (no action >14 days)")
        print("  ──────────────────────────────────────")
        for name, days in stale:
            print(f"    {name}: {days} days since last action")
        print()
        return 1
    else:
        print("\n  ✅ All pipelines active within 14 days\n")
        return 0


def main():
    state = load_state()

    if len(sys.argv) < 2:
        show_dashboard(state)
    elif sys.argv[1] == "--week":
        show_weekly(state)
    elif sys.argv[1] == "--check":
        return cmd_check(state)
    elif sys.argv[1] == "--update":
        cmd_update(sys.argv[2:])
    elif sys.argv[1] == "--init":
        save_state(DEFAULT_STATE)
        print("✅ Pipeline state initialized")
    elif sys.argv[1] == "--reset":
        save_state(DEFAULT_STATE)
        print("✅ Pipeline state reset to defaults")
    else:
        print(f"Unknown option: {sys.argv[1]}")
        print("Usage: pipeline_dashboard.py [--week|--check|--update|--init|--reset]")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
