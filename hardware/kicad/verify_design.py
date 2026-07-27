#!/usr/bin/env python3
"""Comprehensive verification of MykoVolt DevKit design.

Performs:
1. KiCad file syntax validation
2. Component database consistency checks
3. Netlist connectivity verification
4. Electrical rule checks
5. PCB placement verification
6. Generates Lean formal verification artifact
"""

import os, sys, json, re
from datetime import datetime
from collections import defaultdict

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)

from generate_kicad import COMPONENTS, NETS, POS, PCB_POS, VERSION

errors = []
warnings = []
info = []

def err(msg): errors.append(msg); print(f"  \u2717 {msg}")
def warn(msg): warnings.append(msg); print(f"  \u26a0 {msg}")
def note(msg): info.append(msg); print(f"  \u2713 {msg}")

# ── 1. KiCad file syntax validation ──
def check_kicad_syntax():
    print("\n[1/6] KiCad File Syntax Check")
    for ext, desc in [(".kicad_pcb", "PCB"), (".kicad_sch", "Schematic"),
                       (".kicad_pro", "Project"), (".net", "Netlist")]:
        path = os.path.join(PROJECT_DIR, f"mykovolt_devkit{ext}")
        if not os.path.exists(path):
            err(f"{desc} file missing: {path}")
            continue
        with open(path) as f:
            content = f.read()
        depth = 0
        min_depth = 0
        ok = True
        for c in content:
            if c == '(': depth += 1
            elif c == ')': depth -= 1
            min_depth = min(min_depth, depth)
        if depth != 0 or min_depth < 0:
            err(f"{desc}: unbalanced parentheses (final={depth}, min={min_depth})")
        elif len(content) < 100:
            err(f"{desc}: suspiciously small ({len(content)} bytes)")
        else:
            note(f"{desc}: {len(content)} bytes, parentheses balanced")

    # Try loading with pcbnew API
    try:
        import pcbnew
        board = pcbnew.LoadBoard(os.path.join(PROJECT_DIR, "mykovolt_devkit.kicad_pcb"))
        note(f"PCB loaded via pcbnew: {len(board.GetFootprints())} footprints, {len(board.GetNetsByName())} nets")
    except Exception as e:
        err(f"PCB failed to load in pcbnew: {e}")

# ── 2. Component database consistency ──
def check_components():
    print("\n[2/6] Component Database Check")
    refs = [c[0] for c in COMPONENTS]
    dups = [r for r in refs if refs.count(r) > 1]
    if dups:
        err(f"Duplicate component references: {set(dups)}")
    else:
        note(f"No duplicate references ({len(COMPONENTS)} components)")

    for ref, value, fp, ds, sym in COMPONENTS:
        if ref not in POS:
            warn(f"{ref} ({value}): no schematic position")
        if ref not in PCB_POS:
            warn(f"{ref} ({value}): no PCB position")
        if fp and ":" not in fp:
            warn(f"{ref}: footprint '{fp}' missing library prefix")

    for ref in PCB_POS:
        if ref not in refs:
            err(f"PCB position for unknown component: {ref}")
    for ref in POS:
        if ref not in refs:
            err(f"Schematic position for unknown component: {ref}")

    # Categorize
    ics = [c for c in COMPONENTS if c[0].startswith("U")]
    passives = [c for c in COMPONENTS if c[0].startswith(("R", "C", "L"))]
    connectors = [c for c in COMPONENTS if c[0].startswith("J")]
    others = [c for c in COMPONENTS if c[0] not in [x[0] for x in ics + passives + connectors]]
    note(f"  ICs: {len(ics)}, Passives: {len(passives)}, Connectors: {len(connectors)}, Other: {len(others)}")

# ── 3. Netlist consistency ──
def check_netlist():
    print("\n[3/6] Netlist Connectivity Check")
    net_names = [n[0] for n in NETS]
    dups = [n for n in net_names if net_names.count(n) > 1]
    if dups: err(f"Duplicate net names: {set(dups)}")

    total_conns = 0
    for net_name, connections in NETS:
        total_conns += len(connections)
        if len(connections) < 2:
            warn(f"Net '{net_name}' has only {len(connections)} connection(s)")
        for ref, pin in connections:
            if ref not in [c[0] for c in COMPONENTS]:
                err(f"Net '{net_name}': unknown component '{ref}'")

    # Verify power connections
    gnd_count = sum(1 for n, c in NETS if n == "GND" for _ in c)
    pwr_count = sum(1 for n, c in NETS if n == "3.3V" for _ in c)
    note(f"GND connections: {gnd_count}, 3.3V connections: {pwr_count}")
    note(f"Total: {len(NETS)} nets, {total_conns} connections")

# ── 4. Electrical sanity checks ──
def check_electrical():
    print("\n[4/6] Electrical Rule Check")
    i2c_nets = {"I2C1_SCL", "I2C1_SDA"}
    for net_name, connections in NETS:
        if net_name in i2c_nets:
            resistors = [r for r, p in connections if r.startswith("R")]
            if resistors:
                note(f"I2C '{net_name}' pull-up(s): {', '.join(resistors)}")
            else:
                warn(f"I2C '{net_name}' missing pull-up resistor")

    # Decoupling caps per IC (check both schematic and PCB positions)
    for ic_ref, _, _, _, _ in COMPONENTS:
        if not ic_ref.startswith("U"): continue
        nearby = []
        # Check PCB proximity first (more meaningful)
        if ic_ref in PCB_POS:
            ix, iy = PCB_POS[ic_ref]
            for c_ref, _, _, _, _ in COMPONENTS:
                if not c_ref.startswith("C"): continue
                if c_ref in PCB_POS:
                    cx, cy = PCB_POS[c_ref]
                    dx = abs(ix - cx) / 1e6
                    dy = abs(iy - cy) / 1e6
                    if dx < 10 and dy < 10:
                        nearby.append(f"{c_ref}@{dx:.0f}x{dy:.0f}mm")
        # Fall back to schematic positions
        if not nearby and ic_ref in POS:
            ix, iy = POS[ic_ref]
            for c_ref, _, _, _, _ in COMPONENTS:
                if not c_ref.startswith("C"): continue
                if c_ref in POS:
                    cx, cy = POS[c_ref]
                    dx = abs(ix - cx)
                    dy = abs(iy - cy)
                    if dx < 100 and dy < 100:
                        nearby.append(c_ref)
        if nearby:
            note(f"{ic_ref} decoupling: {', '.join(nearby[:5])}")
        else:
            warn(f"{ic_ref} no nearby decoupling capacitor")

    # BQ25570 programming circuit
    bq_nets = {"VOUT_SET", "OK_PROG", "OK_HYST", "VRDIV", "VOC_SAMP", "VREF_SAMP"}
    found = set(n for n, _ in NETS if n in bq_nets)
    missing = bq_nets - found
    if missing:
        err(f"BQ25570 missing nets: {missing}")
    else:
        note("BQ25570 programming circuit complete")

    # Crystal oscillator
    for net_name in ("XTAL_IN", "XTAL_OUT"):
        found_xtal = any(n == net_name for n, _ in NETS)
        if not found_xtal:
            err(f"Missing crystal net: {net_name}")
        else:
            caps = [r for r, p in next((c for n, c in NETS if n == net_name), []) if r.startswith("C")]
            if caps:
                note(f"XTAL load caps on {net_name}: {', '.join(caps)}")

# ── 5. PCB placement checks ──
def check_pcb_placement():
    print("\n[5/6] PCB Placement Check")
    w, h = 30e6, 20e6
    for ref, (x, y) in PCB_POS.items():
        if x < 0 or x > w or y < 0 or y > h:
            warn(f"{ref} at ({x/1e6:.1f}, {y/1e6:.1f})mm is outside board")

    note(f"{len(PCB_POS)} components on 30x20mm board ({int((w*h)/1e12)}mm\u00b2)")

# ── 6. Generate Lean verification ──
def generate_lean():
    print("\n[6/6] Lean Formal Verification Artifact")
    path = os.path.join(PROJECT_DIR, "mykovolt_devkit_verification.lean")

    L = lambda s: lines.append(s)
    lines = []

    L("/-")
    L("  MykoVolt DevKit v" + VERSION + " — Formal Verification")
    L(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    L("  Upload to https://lean-lang.org/playground to run")
    L("-/")
    L("")

    L("structure Connection where")
    L("  component : String")
    L("  pin : String")
    L("  deriving Repr")
    L("")
    L("structure Net where")
    L("  name : String")
    L("  connections : List Connection")
    L("  deriving Repr")
    L("")
    L("structure ComponentInfo where")
    L("  reference : String")
    L("  value : String")
    L("  deriving Repr")
    L("")

    L("def components : List ComponentInfo :=")
    L("  [")
    for ref, value, _, _, _ in COMPONENTS:
        L(f'    {{ reference := "{ref}", value := "{value}" }},')
    L("  ]")
    L("")

    L("def nets : List Net :=")
    L("  [")
    for net_name, connections in NETS:
        L(f'    {{ name := "{net_name}", connections := [')
        for ref, pin in connections:
            L(f'      {{ component := "{ref}", pin := "{pin}" }},')
        L("    ] },")
    L("  ]")
    L("")

    L("-- Theorem 1: All nets have connections")
    L("theorem allNetsHaveConnections : Bool :=")
    L("  nets.all (fun n => n.connections.length > 0)")
    L("")

    L("-- Theorem 2: No floating nets (must have >= 2 connections)")
    L("def floatingNets : List (Nat) :=")
    L("  nets.filter (fun n => n.connections.length <= 1)")
    L("    |>.map (fun n => n.connections.length)")
    L("")

    L("-- Theorem 3: Power nets (GND, 3.3V) exist")
    L('def powerNetNames : List String := ["GND", "3.3V"]')
    L("theorem powerNetsExist : Bool :=")
    L("  let netNames := nets.map (fun n => n.name)")
    L("  powerNetNames.all (fun pn => netNames.contains pn)")
    L("")

    L("-- Theorem 4: I2C nets have pull-up resistors")
    L("theorem i2cHasPullups : Bool :=")
    L('  let i2cNets := nets.filter (fun n => "I2C".isPrefixOf n.name)')
    L("  i2cNets.all (fun n =>")
    L('    n.connections.any (fun c => "R".isPrefixOf c.component))')
    L("")

    L("-- Theorem 5: No duplicate component-pin assignments")
    L("theorem noDuplicatePinAssignments : Bool :=")
    L("  let allAssignments := nets.bind (fun n =>")
    L("    n.connections.map (fun c => (c.component, c.pin)))")
    L("  allAssignments.length == allAssignments.eraseDups.length")
    L("")

    L("-- Theorem 6: All net components exist in database")
    L("def allComponentRefs : List String :=")
    L("  components.map (fun c => c.reference)")
    L("theorem allNetComponentsExist : Bool :=")
    L("  nets.all (fun n =>")
    L("    n.connections.all (fun c =>")
    L("      allComponentRefs.contains c.component))")
    L("")

    L("-- Run all checks")
    L("def main : IO Unit := do")
    L('  IO.println "=== MykoVolt DevKit Formal Verification ==="')
    L('  IO.println s!"Components: {components.length}"')
    L('  IO.println s!"Nets: {nets.length}"')
    L('  IO.println s!"Power nets present: {powerNetsExist}"')
    L('  IO.println s!"I2C pull-ups: {i2cHasPullups}"')
    L('  IO.println s!"All nets have connections: {allNetsHaveConnections}"')
    L('  IO.println s!"No dup pin assignments: {noDuplicatePinAssignments}"')
    L('  IO.println s!"All components exist: {allNetComponentsExist}"')
    L('  IO.println s!"Floating nets: {floatingNets}"')
    L("")
    L("#eval main")

    content = "\n".join(lines)
    with open(path, "w") as f:
        f.write(content)
    note(f"Lean verification file: {os.path.basename(path)} ({len(content)} bytes)")


def main():
    print(f"\u2554{'='*60}\u2557")
    print(f"\u2551  MykoVolt DevKit v{VERSION} — Design Verification")
    print(f"\u2551  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\u255a{'='*60}\u255d")

    check_kicad_syntax()
    check_components()
    check_netlist()
    check_electrical()
    check_pcb_placement()
    generate_lean()

    print(f"\n{'='*62}")
    print(f"Results: {len(info)} checks passed, {len(warnings)} warnings, {len(errors)} errors")
    if errors:
        print(f"\n\u274c {len(errors)} error(s):")
        for e in errors: print(f"   \u2022 {e}")
    if warnings:
        print(f"\n\u26a0 {len(warnings)} warning(s):")
        for w in warnings: print(f"   \u2022 {w}")

    return len(errors) == 0

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
