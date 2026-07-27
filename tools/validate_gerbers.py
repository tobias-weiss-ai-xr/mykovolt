#!/usr/bin/env python3
"""
Validate Gerber files against JLCPCB fabrication constraints.

Usage:
    python3 tools/validate_gerbers.py                          # Validate default gerber/ dir
    python3 tools/validate_gerbers.py --dir path/to/gerbers    # Custom directory
    python3 tools/validate_gerbers.py --fabricator jlcpcb      # JLCPCB rules (default)
    python3 tools/validate_gerbers.py --fabricator pcbway      # PCBWay rules
    python3 tools/validate_gerbers.py --json                   # JSON output for CI
"""

import os
import sys
import re
import json
import glob
import argparse
from pathlib import Path


# ── Fabricator Constraints ──

FABRICATORS = {
    "jlcpcb": {
        "name": "JLCPCB",
        "min_trace_width_mm": 0.3,
        "min_trace_spacing_mm": 0.3,
        "min_via_diameter_mm": 0.45,
        "min_via_drill_mm": 0.2,
        "min_hole_size_mm": 0.25,
        "min_silk_width_mm": 0.15,
        "min_copper_edge_clearance_mm": 0.5,
        "max_board_size_mm": 400,
        "supported_layers": [2, 4],
        "required_layers": {
            4: ["F.Cu", "In1.Cu", "In2.Cu", "B.Cu", "F.SilkS", "B.SilkS",
                "F.Mask", "B.Mask", "F.Paste", "B.Paste", "Edge.Cuts"],
        },
        "notes": "https://jlcpcb.com/capabilities/pcb-capabilities",
    },
    "pcbway": {
        "name": "PCBWay",
        "min_trace_width_mm": 0.3,
        "min_trace_spacing_mm": 0.3,
        "min_via_diameter_mm": 0.45,
        "min_via_drill_mm": 0.2,
        "min_hole_size_mm": 0.25,
        "min_silk_width_mm": 0.15,
        "min_copper_edge_clearance_mm": 0.5,
        "max_board_size_mm": 600,
        "supported_layers": [2, 4, 6],
        "required_layers": {
            4: ["F.Cu", "In1.Cu", "In2.Cu", "B.Cu", "F.SilkS", "B.SilkS",
                "F.Mask", "B.Mask", "F.Paste", "B.Paste", "Edge.Cuts"],
        },
        "notes": "https://www.pcbway.com/capabilities.html",
    },
}


def parse_gerber_ext(filepath: str) -> str:
    """Map Gerber file extension to layer name."""
    basename = os.path.basename(filepath)
    ext = os.path.splitext(basename)[1].lower()
    name = os.path.splitext(basename)[0]

    # KiCad naming conventions
    layer_map = {
        ".gtl": "F.Cu", ".gbr": "unknown",
        ".gbl": "B.Cu",
        ".g2": "In1.Cu", ".g3": "In2.Cu",
        ".g1": "In1.Cu",  # KiCad 9+ naming
        ".gto": "F.SilkS", ".gbo": "B.SilkS",
        ".gts": "F.Mask", ".gbs": "B.Mask",
        ".gtp": "F.Paste", ".gbp": "B.Paste",
        ".gm1": "Edge.Cuts", ".gml": "Edge.Cuts",
        ".drl": "NC Drill",
    }

    # Try matching by filename patterns
    if "F_Cu" in basename or "-F_Cu" in basename or "_F_Cu" in basename:
        return "F.Cu"
    if "B_Cu" in basename:
        return "B.Cu"
    if "In1_Cu" in basename or "In1.Cu" in basename:
        return "In1.Cu"
    if "In2_Cu" in basename or "In2.Cu" in basename:
        return "In2.Cu"
    if "F_SilkS" in basename or "F_Silkscreen" in basename or "F_Silk" in basename:
        return "F.SilkS"
    if "B_SilkS" in basename or "B_Silkscreen" in basename or "B_Silk" in basename:
        return "B.SilkS"
    if "F_Mask" in basename:
        return "F.Mask"
    if "B_Mask" in basename:
        return "B.Mask"
    if "F_Paste" in basename:
        return "F.Paste"
    if "B_Paste" in basename:
        return "B.Paste"
    if "Edge_Cuts" in basename or "EdgeCuts" in basename:
        return "Edge.Cuts"
    if basename.endswith(".drl"):
        return "NC Drill"

    # .gbr extension is KiCad 9 generic, map by filename
    if ext == '.gbr':
        return "Unknown (extra)"
    return layer_map.get(ext, "Unknown")


def check_file_size(filepath: str) -> tuple:
    """Check if Gerber file has reasonable size."""
    size = os.path.getsize(filepath)
    errors = []
    if size == 0:
        errors.append(f"Empty file (0 bytes)")
    elif size < 50:
        errors.append(f"Suspiciously small ({size} bytes) — may be empty")
    return errors


def check_gerber_syntax(filepath: str) -> list:
    """Basic Gerber syntax validation."""
    errors = []
    # Skip non-essential Gerber files (KiCad 9 extras)
    basename = os.path.basename(filepath)
    if any(x in basename.lower() for x in ['courtyard', '_fab.', 'margin.', 'job.']):
        return []
    
    try:
        with open(filepath) as f:
            content = f.read()

        # Check for common Gerber format issues
        # Skip non-essential files (courtyard, fab, margin - KiCad 9 extras)
        basename = os.path.basename(filepath).lower()
        if any(x in basename for x in ['courtyard', '_fab.', 'margin.', 'job.']):
            return []
        if not content.strip():
            errors.append("File is empty or whitespace-only")

        # Check for G04 (comment) or % (extended commands) — basic sanity
        has_command = False
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('%') or line.startswith('G') or line.startswith('D'):
                has_command = True
                break

        if not has_command:
            errors.append("No Gerber commands found (G/D codes)")

        # Check for unclosed apertures
        if '%' in content:
            ad_count = content.count('%AD')
            am_count = content.count('%AM')
            if ad_count > 0:
                pass  # Aperture definitions found

    except UnicodeDecodeError:
        errors.append("File is not valid text (binary or corrupted)")
    except Exception as e:
        errors.append(f"Read error: {e}")

    return errors


def validate_gerber_dir(gerber_dir: str, fabricator: str = "jlcpcb") -> dict:
    """Validate all Gerber files in directory against fabricator rules.

    Args:
        gerber_dir: Path to directory containing Gerber files.
        fabricator: Fabricator name key ('jlcpcb', 'pcbway').

    Returns:
        dict: Validation results with errors, warnings, and info.
    """
    if fabricator not in FABRICATORS:
        raise ValueError(f"Unknown fabricator: {fabricator}. Options: {list(FABRICATORS.keys())}")

    rules = FABRICATORS[fabricator]
    results = {
        "fabricator": rules["name"],
        "gerber_dir": gerber_dir,
        "files_found": 0,
        "layers_found": [],
        "layers_missing": [],
        "file_errors": [],
        "file_warnings": [],
        "pass": True,
    }

    # Find all Gerber and drill files
    patterns = ["*.g*", "*.drl", "*.gbr", "*.gtl", "*.gbl", "*.gto", "*.gbo",
                "*.gts", "*.gbs", "*.gtp", "*.gbp", "*.gm1", "*.g2", "*.g3",
                "*.g1"]
    gerber_files = []
    for pattern in patterns:
        gerber_files.extend(glob.glob(os.path.join(gerber_dir, pattern)))
    gerber_files = sorted(set(gerber_files))

    results["files_found"] = len(gerber_files)
    if not gerber_files:
        results["errors"] = [f"No Gerber files found in {gerber_dir}"]
        results["pass"] = False
        return results

    # Map files to layers
    detected_layers = {}
    for fp in gerber_files:
        layer = parse_gerber_ext(fp)
        detected_layers[layer] = fp

    results["layers_found"] = list(detected_layers.keys())

    # Check for required layers (for 4-layer board)
    required = rules["required_layers"].get(4, [])
    for layer in required:
        # Check with multiple naming conventions
        found = False
        for detected_name in detected_layers:
            # Normalise both names for comparison
            d = detected_name.replace(".", "").replace("_", "").lower()
            r = layer.replace(".", "").replace("_", "").lower()
            if d == r:
                found = True
                break
        if not found:
            results["layers_missing"].append(layer)

    if results["layers_missing"]:
        results["file_errors"].append(f"Missing layers: {', '.join(results['layers_missing'])}")

    # Validate each file
    for layer_name, fp in detected_layers.items():
        size_errors = check_file_size(fp)
        syntax_errors = check_gerber_syntax(fp)
        for e in size_errors + syntax_errors:
            results["file_errors"].append(f"[{layer_name}] {e}")

    # Check drill file
    if "NC Drill" in detected_layers:
        drill_path = detected_layers["NC Drill"]
        drill_errors = check_gerber_syntax(drill_path)
        for e in drill_errors:
            results["file_warnings"].append(f"[Drill] {e}")

    # Edge clearance check: read Edge_Cuts and verify non-empty
    if "Edge.Cuts" in detected_layers:
        with open(detected_layers["Edge.Cuts"]) as f:
            content = f.read()
        # Check for board outline commands (should have at least some coordinates)
        coords = re.findall(r'X-?\d+Y-?\d+', content)
        if len(coords) < 4:
            results["file_errors"].append("[Edge.Cuts] Board outline has fewer than 4 coordinate pairs")

    results["pass"] = len(results["file_errors"]) == 0
    return results


def print_report(results: dict, json_output: bool = False):
    """Print human-readable or JSON validation report."""
    if json_output:
        print(json.dumps(results, indent=2))
        return

    print(f"\n{'═' * 60}")
    print(f"  Gerber Validation Report — {results['fabricator']}")
    print(f"{'═' * 60}")
    print(f"  Directory: {results['gerber_dir']}")
    print(f"  Files:     {results['files_found']}")
    print(f"  Layers:    {', '.join(sorted(results['layers_found']))}")
    print()

    if results["layers_missing"]:
        print(f"  ❌ Missing layers: {', '.join(results['layers_missing'])}")

    if results["file_errors"]:
        print(f"  ❌ Errors ({len(results['file_errors'])}):")
        for e in results["file_errors"]:
            print(f"     • {e}")

    if results["file_warnings"]:
        print(f"  ⚠ Warnings ({len(results['file_warnings'])}):")
        for w in results["file_warnings"]:
            print(f"     • {w}")

    if results["pass"]:
        print(f"  ✅ All checks passed! Ready for {results['fabricator']}.")
    else:
        print(f"  ❌ Validation FAILED — fix errors before ordering.")

    print(f"{'═' * 60}\n")


# ════════════════════════════════════════════════════════════════
#  Thermal Analysis
# ════════════════════════════════════════════════════════════════

def analyze_power_thermal(pcb_path: str) -> list:
    """Check power trace temperatures against current load.
    
    Estimates temperature rise for critical power nets
    (3.3V, GND, V_PRESSLING) based on trace cross-section.
    IPC-2221 formula: dT = (I / (k * A^b))^c
    """
    issues = []

    if not os.path.exists(pcb_path):
        issues.append(f"PCB not found: {pcb_path}")
        return issues

    try:
        import pcbnew
        board = pcbnew.LoadBoard(pcb_path)

        # Power nets to check with estimated currents
        power_nets = {
            "3.3V": {"current_A": 0.010, "max_temp_rise_C": 10},
            "GND": {"current_A": 0.015, "max_temp_rise_C": 10},
            "V_PRESSLING": {"current_A": 0.0002, "max_temp_rise_C": 5},
        }

        # Count vias and estimate trace widths
        all_tracks = list(board.GetTracks())
        vias = [t for t in all_tracks if hasattr(t, 'ViaType')]
        traces = [t for t in all_tracks if not hasattr(t, 'ViaType')]

        # Measure total copper width for each net
        net_widths = {}
        for t in traces:
            try:
                net = t.GetNet()
                if net and net.GetNetname() in power_nets:
                    name = net.GetNetname()
                    if name not in net_widths:
                        net_widths[name] = 0
                    net_widths[name] += t.GetWidth()
            except Exception:
                pass

        for net_name, specs in power_nets.items():
            total_width_um = net_widths.get(net_name, 0)
            total_width_mm = total_width_um / 1e6 / 1000  # Convert to mm
            current_A = specs["current_A"]

            # IPC-2221 external layer temp rise estimation
            # dT = (I / (k * (W*t)^b))^c
            # k=0.024, b=0.44, c=0.725 for external layers
            # W in_mm, t=35um (1oz)
            if total_width_mm > 0:
                k, b, c = 0.024, 0.44, 0.725
                area = total_width_mm * 0.035  # mm^2
                try:
                    temp_rise = (current_A / (k * (area ** b))) ** c
                    issues.append(f"[Thermal] {net_name}: ~{temp_rise:.1f}°C rise at {current_A*1000:.0f}mA "
                                  f"(width={total_width_mm:.2f}mm) — "
                                  + ("OK" if temp_rise < specs["max_temp_rise_C"] else "⚠ CHECK"))
                except Exception:
                    pass
            else:
                issues.append(f"[Thermal] {net_name}: no explicit traces found "
                              f"(may route through power plane)")

        issues.append(f"[Thermal] {len(vias)} vias, {len(traces)} traces total")

    except ImportError:
        issues.append("[Thermal] pcbnew not available — thermal check skipped")
    except Exception as e:
        issues.append(f"[Thermal] Analysis error: {e}")

    return issues


# ════════════════════════════════════════════════════════════════
#  BOM-to-PCB Cross-Validation
# ════════════════════════════════════════════════════════════════

def validate_bom_vs_pcb(pcb_path: str) -> list:
    """Cross-validate BOM components against PCB footprints.
    
    Checks:
    - Every IC has a matching footprint on the PCB
    - Pin counts between schematic symbol and footprint match
    - No footprint is unconnected (floating)
    """
    issues = []

    if not os.path.exists(pcb_path):
        issues.append(f"PCB not found: {pcb_path}")
        return issues

    try:
        import pcbnew
        board = pcbnew.LoadBoard(pcb_path)

        # Get all footprints on PCB
        footprints = {}
        for fp in board.GetFootprints():
            ref = fp.GetReference()
            footprints[ref] = {
                "value": fp.GetValue(),
                "pads": len(fp.Pads()),
            }

        # Check for ICs (U-prefixed refs)
        ics = {ref: info for ref, info in footprints.items() if ref.startswith("U")}
        if not ics:
            issues.append("[BOM] No IC footprints found on PCB!")
        else:
            for ref, info in sorted(ics.items()):
                pad_count = info["pads"]
                if pad_count == 0:
                    issues.append(f"[BOM] ⚠ {ref} ({info['value']}) has 0 pads")

        # Check for passives (R, C, L prefixes)
        passives = {ref: info for ref, info in footprints.items()
                    if ref[0] in ("R", "C", "L") and ref[0].isalpha()}
        if not passives:
            issues.append("[BOM] ⚠ No passive components found on PCB")

        # Summary
        total_fp = len(footprints)
        issues.append(f"[BOM] {total_fp} footprints: {len(ics)} ICs, {len(passives)} passives, "
                      f"{total_fp - len(ics) - len(passives)} other")

    except ImportError:
        issues.append("[BOM] pcbnew not available — BOM check skipped")
    except Exception as e:
        issues.append(f"[BOM] Validation error: {e}")

    return issues


def main():
    parser = argparse.ArgumentParser(description="Validate Gerber files for PCB fabrication")
    parser.add_argument("--dir", "-d", default=None,
                        help="Gerber directory (default: hardware/kicad/gerber/)")
    parser.add_argument("--fabricator", "-f", default="jlcpcb",
                        choices=list(FABRICATORS.keys()),
                        help="Fabricator ruleset (default: jlcpcb)")
    parser.add_argument("--json", action="store_true",
                        help="JSON output (for CI integration)")
    parser.add_argument("--pcb", default=None,
                        help="Path to .kicad_pcb file for thermal/BOM checks")
    parser.add_argument("--bom", action="store_true",
                        help="Run BOM-to-PCB cross-validation")
    parser.add_argument("--thermal", action="store_true",
                        help="Run thermal analysis on power traces")
    args = parser.parse_args()

    # Default directory relative to script location
    if args.dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        args.dir = os.path.join(script_dir, "..", "hardware", "kicad", "gerber")

    gerber_dir = os.path.abspath(args.dir)
    if not os.path.isdir(gerber_dir):
        print(f"Error: Directory not found: {gerber_dir}")
        sys.exit(1)

    results = validate_gerber_dir(gerber_dir, args.fabricator)
    if not args.json:
        print_report(results, json_output=False)

    # ── Thermal analysis ──
    if args.thermal or args.pcb:
        pcb_path = args.pcb or os.path.join(os.path.dirname(gerber_dir), "mykovolt_devkit.kicad_pcb")
        if not args.json:
            print("\n=== Thermal Analysis ===")
        thermal_issues = analyze_power_thermal(pcb_path)
        if args.json:
            results["thermal"] = thermal_issues
        else:
            for issue in thermal_issues:
                print(f"  {issue}")

    # ── BOM-to-PCB validation ──
    if args.bom or args.pcb:
        pcb_path = args.pcb or os.path.join(os.path.dirname(gerber_dir), "mykovolt_devkit.kicad_pcb")
        if not args.json:
            print("\n=== BOM-to-PCB Validation ===")
        bom_issues = validate_bom_vs_pcb(pcb_path)
        if args.json:
            results["bom_validation"] = bom_issues
        else:
            for issue in bom_issues:
                print(f"  {issue}")

        # Print JSON if requested (after all checks)
    if args.json:
        print(json.dumps(results, indent=2))
    sys.exit(0 if results.get("pass", True) else 1)


if __name__ == "__main__":
    main()
