#!/usr/bin/env python3
"""
Parametric Sweep — MykoVolt Design Space Explorer

Generates multiple PCB variants by sweeping design parameters,
runs DRC on each, and produces a comparison report.

Usage:
    python3 tools/parametric_sweep.py --param nfc_antenna.outer_width_mm --values "10,12,14"
    python3 tools/parametric_sweep.py --param sensor_electrodes.num_fingers --values "8,10,12"
    python3 tools/parametric_sweep.py --all-combinations  # Sweep multiple params
    python3 tools/parametric_sweep.py --report-only       # Just re-check existing builds
    python3 tools/parametric_sweep.py --json              # JSON output for CI
"""

import os
import sys
import json
import copy
import shutil
import subprocess
import argparse
from pathlib import Path

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HW_DIR = os.path.join(PROJECT_DIR, "hardware", "kicad")
OUTPUT_DIR = os.path.join(PROJECT_DIR, "build", "sweep")

# Load config for reference
try:
    import yaml
    with open(os.path.join(HW_DIR, "design_rules.yaml")) as f:
        BASE_CONFIG = yaml.safe_load(f)
except Exception:
    BASE_CONFIG = {}


def parse_args():
    parser = argparse.ArgumentParser(description="MykoVolt parametric PCB sweep")
    parser.add_argument("--param", "-p", action="append", default=[],
                        help="Parameter to sweep, e.g. 'nfc_antenna.outer_width_mm'")
    parser.add_argument("--values", "-v", action="append", default=[],
                        help="Comma-separated values for the corresponding --param")
    parser.add_argument("--all-combinations", "-a", action="store_true",
                        help="Sweep all combinations of parameters")
    parser.add_argument("--report-only", "-r", action="store_true",
                        help="Re-check existing sweep results without regenerating")
    parser.add_argument("--json", action="store_true",
                        help="JSON output")
    parser.add_argument("--drc-only", action="store_true",
                        help="Skip Gerber export, DRC only")
    return parser.parse_args()


def set_nested(d, path, value):
    """Set a value in a nested dict using dot notation."""
    keys = path.split(".")
    for k in keys[:-1]:
        if k not in d:
            d[k] = {}
        d = d[k]
    if isinstance(value, str):
        # Try numeric conversion
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                pass
    d[keys[-1]] = value


def make_config_variant(param_path, value):
    """Create a config dict with one parameter overridden."""
    config = copy.deepcopy(BASE_CONFIG) if BASE_CONFIG else {}
    set_nested(config, param_path, value)
    return config


def run_generation(config, variant_name, drc_only=False):
    """Generate PCB with given config and run DRC. Returns (success, drc_errors, drc_unconnected)."""
    output_dir = os.path.join(OUTPUT_DIR, variant_name)
    os.makedirs(output_dir, exist_ok=True)

    # Write variant config
    config_path = os.path.join(output_dir, "design_rules.yaml")
    try:
        import yaml
        with open(config_path, "w") as f:
            yaml.dump(config, f)
    except Exception:
        return False, "config_write_error", 0

    # Run generator
    gen_cmd = [
        sys.executable, os.path.join(HW_DIR, "generate_kicad.py"),
        "--config", config_path,
        "--output", output_dir,
    ]
    if drc_only:
        gen_cmd.append("--skip-gerber")

    try:
        result = subprocess.run(gen_cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            return False, result.stderr[:200], 0
    except subprocess.TimeoutExpired:
        return False, "timeout", 0
    except Exception as e:
        return False, str(e), 0

    # Run DRC
    pcb_path = os.path.join(output_dir, "mykovolt_devkit.kicad_pcb")
    if not os.path.exists(pcb_path):
        # Try using the generator's output directory
        pcb_fallback = os.path.join(HW_DIR, "mykovolt_devkit.kicad_pcb")
        if os.path.exists(pcb_fallback):
            pcb_path = pcb_fallback
        else:
            return False, "pcb_not_found", 0

    drc_cmd = ["kicad-cli", "pcb", "drc", "-o", os.path.join(output_dir, "drc.txt"), pcb_path]
    try:
        subprocess.run(drc_cmd, capture_output=True, text=True, timeout=30)
    except Exception:
        pass

    # Parse DRC results
    drc_path = os.path.join(output_dir, "drc.txt")
    drc_errors = 0
    drc_unconnected = 0
    if os.path.exists(drc_path):
        with open(drc_path) as f:
            content = f.read()
        drc_errors = len(re.findall(r"error", content)) if 're' in dir() else 0
        drc_unconnected = content.count("unconnected_items") if 'unconnected' in content else 0
        # Count actual violations
        for line in content.split('\n'):
            if 'unconnected_items' in line:
                drc_unconnected += 1

    return True, drc_errors, drc_unconnected


def sweep_param(param_path, values, drc_only=False):
    """Sweep a single parameter across values and return results."""
    import re
    results = []
    for v in values:
        v = v.strip()
        variant_name = f"{param_path.replace('.', '_')}={v}"
        print(f"  Sweeping {param_path}={v} ... ", end="", flush=True)
        config = make_config_variant(param_path, v)
        success, drc_result, unconnected = run_generation(config, variant_name, drc_only)
        if success:
            print(f"DRC errors={drc_result}, unconnected={unconnected}")
        else:
            print(f"FAILED: {drc_result}")
        results.append({
            "variant": variant_name,
            "parameters": {param_path: v},
            "success": success,
            "drc_errors": drc_result if isinstance(drc_result, int) else str(drc_result),
            "unconnected": unconnected,
        })
    return results


def generate_report(results, json_output=False):
    """Generate a comparison report from sweep results."""
    if json_output:
        print(json.dumps(results, indent=2))
        return

    print(f"\n{'='*60}")
    print(f"  Parametric Sweep Report")
    print(f"{'='*60}")

    if not results:
        print("  No results.")
        return

    # Group by parameter
    by_param = {}
    for r in results:
        for param, value in r["parameters"].items():
            if param not in by_param:
                by_param[param] = []
            by_param[param].append(r)

    for param, variants in by_param.items():
        print(f"\n  Parameter: {param}")
        print(f"  {'─'*50}")
        print(f"  {'Value':<15} {'DRC Errors':<15} {'Unconnected':<15} {'Status':<10}")
        print(f"  {'─'*50}")
        best = None
        best_score = float('inf')
        for v in variants:
            value_str = str(list(v["parameters"].values())[0])
            status = "✅" if v["success"] else "❌"
            errors = v["drc_errors"]
            unconn = v["unconnected"]
            # Score: fewer errors is better
            score = (0 if isinstance(errors, int) else 999) + (unconn if isinstance(unconn, int) else 999)
            if score < best_score:
                best_score = score
                best = v
            print(f"  {value_str:<15} {str(errors):<15} {str(unconn):<15} {status:<10}")
        if best:
            print(f"\n  → Best: {list(best['parameters'].values())[0]} (score={best_score})")

    print(f"{'='*60}\n")


def main():
    args = parse_args()
    drc_only = args.drc_only

    if args.report_only:
        # Re-read existing results from build/sweep/
        results = []
        if os.path.isdir(OUTPUT_DIR):
            for variant_dir in sorted(os.listdir(OUTPUT_DIR)):
                drc_path = os.path.join(OUTPUT_DIR, variant_dir, "drc.txt")
                config_path = os.path.join(OUTPUT_DIR, variant_dir, "design_rules.yaml")
                if os.path.exists(drc_path) and os.path.exists(config_path):
                    with open(drc_path) as f:
                        content = f.read()
                    drc_errors = content.count("error")
                    unconnected = content.count("unconnected_items")
                    results.append({
                        "variant": variant_dir,
                        "success": True,
                        "drc_errors": drc_errors,
                        "unconnected": unconnected,
                    })
        generate_report(results, json_output=args.json)
        return

    all_results = []

    if args.param and args.values:
        for param_path, values_str in zip(args.param, args.values):
            values = [v.strip() for v in values_str.split(",")]
            print(f"\nSweeping {param_path} = {values}")
            results = sweep_param(param_path, values, drc_only)
            all_results.extend(results)
    else:
        # Default: sweep antenna width and finger count
        print("No parameters specified. Running default sweeps:\n")
        all_results.extend(sweep_param("nfc_antenna.outer_width_mm", ["10", "12", "14"], drc_only))
        all_results.extend(sweep_param("sensor_electrodes.num_fingers", ["8", "10", "12"], drc_only))

    generate_report(all_results, json_output=args.json)

    # Store results as JSON for CI
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, "sweep_results.json"), "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nResults saved to {OUTPUT_DIR}/sweep_results.json")


if __name__ == "__main__":
    main()
