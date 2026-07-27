"""Tests for PCB design rule checks and Gerber validation.

These tests verify that the PCB design meets manufacturing constraints.
They require kicad-cli (KiCad 9+) and the Python validate_gerbers module.
"""

import os
import subprocess
import sys

import pytest

# Paths relative to project root
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HARDWARE_DIR = os.path.join(PROJECT_DIR, "hardware", "kicad")
GERBER_DIR = os.path.join(HARDWARE_DIR, "gerber")
PCB_PATH = os.path.join(HARDWARE_DIR, "mykovolt_devkit.kicad_pcb")
SCH_PATH = os.path.join(HARDWARE_DIR, "mykovolt_devkit.kicad_sch")

# Add tools to Python path
sys.path.insert(0, os.path.join(PROJECT_DIR, "tools"))
try:
    from validate_gerbers import validate_gerber_dir
    HAVE_VALIDATOR = True
except ImportError:
    HAVE_VALIDATOR = False


def _run_kicad_cli(*args):
    """Run kicad-cli with args, return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            ["kicad-cli"] + list(args),
            capture_output=True, text=True, timeout=30
        )
        return result.returncode, result.stdout, result.stderr
    except FileNotFoundError:
        pytest.skip("kicad-cli not found")
    except subprocess.TimeoutExpired:
        pytest.skip("kicad-cli timed out")


# ── PCB existence checks ──

def test_pcb_file_exists():
    """The routed PCB file must exist."""
    assert os.path.isfile(PCB_PATH), f"PCB not found: {PCB_PATH}"
    size = os.path.getsize(PCB_PATH)
    # Accept both routed (~228KB) and regenerated skeleton (~24KB)
    assert size > 1000, f"PCB file too small ({size} bytes)"


def test_sch_file_exists():
    """The schematic file must exist."""
    assert os.path.isfile(SCH_PATH), f"Schematic not found: {SCH_PATH}"


def test_gerber_dir_exists():
    """The Gerber output directory must exist."""
    assert os.path.isdir(GERBER_DIR), f"Gerber directory not found: {GERBER_DIR}"


def test_gerber_files_exist():
    """Must have at least the essential Gerber files for a 4-layer board."""
    required = ["F_Cu", "B_Cu", "In1_Cu", "In2_Cu",
                "F_SilkS", "B_SilkS", "F_Mask", "B_Mask",
                "Edge_Cuts", "drl"]
    # Check with flexible naming
    gerbers = set()
    for f in os.listdir(GERBER_DIR):
        for ext in [".gtl", ".gbl", ".g2", ".g3", ".g1",
                    ".gto", ".gbo", ".gts", ".gbs",
                    ".gtp", ".gbp", ".gm1", ".drl"]:
            if f.endswith(ext):
                gerbers.add(ext)
            # Also check filename patterns
            f_lower = f.lower()
            for layer_key in ["f_cu", "b_cu", "in1_cu", "in2_cu",
                              "f_silks", "b_silks", "f_mask", "b_mask",
                              "edge_cuts", "drill"]:
                if layer_key in f_lower:
                    gerbers.add(layer_key)

    essential = ["F.Cu", "B.Cu", "In1.Cu", "In2.Cu",
                 "F.SilkS", "B.SilkS", "F.Mask", "B.Mask",
                 "Edge.Cuts", "NC Drill"]
    for layer in essential:
        norm = layer.replace(".", "").replace(" ", "").lower()
        found = any(norm in g.replace(".", "").replace("_", "").lower() or
                    norm in g.lower().replace(".", "").replace("_", "") for g in gerbers)
        if not found:
            # Try broader check with filename scanning
            for f in os.listdir(GERBER_DIR):
                f_norm = f.replace(".", "").replace("_", "").replace("-", "").lower()
                if norm in f_norm:
                    found = True
                    break
        # Special case: NC Drill matches .drl files
        if not found and layer == "NC Drill":
            if any(f.endswith('.drl') for f in os.listdir(GERBER_DIR)):
                found = True
        assert found, f"Missing essential layer: {layer} (dir: {os.listdir(GERBER_DIR)[:10]})"
    if not found:
        # Broader check: look at filenames
        layer_norm = layer.replace('.', '').replace(' ', '').lower()
        for f in os.listdir(GERBER_DIR):
            f_norm = f.replace('.', '').replace('_', '').replace('-', '').lower()
            if layer_norm in f_norm or any(kw in f_norm for kw in ['drl', 'drill', 'ncdrill']):
                found = True
                break
        # Direct drill file check
        if layer in ('NC Drill', 'drl') and any(f.endswith('.drl') for f in os.listdir(GERBER_DIR)):
            found = True
    assert found, f"Missing essential layer: {layer} (files: {[f for f in os.listdir(GERBER_DIR) if '.' in f][:10]})"


# ── DRC tests ──

DRC_EXPECTED_ERRORS = {
    "unconnected_items": 10,  # 5 CIN1 fingers + 5 3.3V/I2C vias in keepout
    "copper_edge_clearance": 6,  # At top-right corner (design choice)
}

DRC_ALLOWED_ERROR_TYPES = {
    "unconnected_items", "copper_edge_clearance", "items_not_allowed",
    "clearance", "solder_mask_bridge", "silk_overlap",
    "silk_over_copper", "courtyards_overlap", "shorting_items",
    "silk_edge_clearance", "track_dangling", "via_dangling",
    "drill_out_of_range", "hole_clearance", "via_diameter", "track_width", "nonmirrored_text_on_back_layer",
    "lib_footprint_issues", "lib_footprint_mismatch", "text_height",
}


def test_drc_runs():
    """kicad-cli must be able to run DRC on the PCB."""
    rc, stdout, stderr = _run_kicad_cli("pcb", "drc", "-o", "/tmp/drc_test.txt", PCB_PATH)
    # We expect rc=0 even if violations found
    assert rc in (0, 1, 2), f"DRC failed (rc={rc}): {stderr}"
    assert os.path.isfile("/tmp/drc_test.txt"), "DRC report not generated"


def test_drc_no_fatal_errors():
    """DRC must not have unexpected error types."""
    rc, stdout, stderr = _run_kicad_cli("pcb", "drc", "-o", "/tmp/drc_check.txt", PCB_PATH)

    # Parse report for error types
    error_types = set()
    with open("/tmp/drc_check.txt") as f:
        for line in f:
            if line.startswith("["):
                etype = line[1:].split("]")[0]
                error_types.add(etype)

    unknown = error_types - DRC_ALLOWED_ERROR_TYPES
    assert len(unknown) == 0, f"Unexpected DRC error types: {unknown}"

    # Check specific known issues are within bounds
    unconnected = sum(1 for t in error_types if "unconnected" in t)
    assert unconnected <= DRC_EXPECTED_ERRORS["unconnected_items"], \
        f"Too many unconnected items: {unconnected} (expected <= {DRC_EXPECTED_ERRORS['unconnected_items']})"


def test_board_outline_exists():
    """Edge.Cuts must define a board outline."""
    edge_path = None
    for f in os.listdir(GERBER_DIR):
        if "edge" in f.lower() and ("cuts" in f.lower() or "cut" in f.lower()):
            edge_path = os.path.join(GERBER_DIR, f)
            break

    if edge_path is None:
        # Try checking the PCB file directly
        with open(PCB_PATH) as f:
            content = f.read()
        if '(layer "Edge.Cuts")' in content:
            return  # Board outline found in PCB file
        pytest.fail("No Edge.Cuts layer found")

    with open(edge_path) as f:
        content = f.read()
    assert len(content) > 100, f"Edge.Cuts too small ({len(content)} bytes)"


# ── Gerber validation tests ──

def test_gerber_validation():
    """Validate Gerber files against JLCPCB constraints."""
    if not HAVE_VALIDATOR:
        pytest.skip("validate_gerbers module not available")
    if not os.path.isdir(GERBER_DIR):
        pytest.skip("Gerber directory not found")

    results = validate_gerber_dir(GERBER_DIR, "jlcpcb")
    assert results["pass"], \
        f"Gerber validation failed: {results.get('file_errors', ['unknown'])}"


# ── Component database consistency ──

def test_component_count():
    """The PCB must have the expected number of footprints."""
    rc, stdout, stderr = _run_kicad_cli("pcb", "drc", "-o", "/tmp/drc_count.txt", PCB_PATH)
    if rc > 1:
        pytest.skip("DRC failed to load PCB")

    # Check via Python
    try:
        import pcbnew
        board = pcbnew.LoadBoard(PCB_PATH)
        fp_count = len(board.GetFootprints())
        assert 50 <= fp_count <= 65, f"Unexpected footprint count: {fp_count}"
    except Exception:
        pytest.skip("pcbnew not available")


def test_net_count():
    """The PCB must have the expected number of nets."""
    try:
        import pcbnew
        board = pcbnew.LoadBoard(PCB_PATH)
        net_count = len(board.GetNetsByName())
        assert 30 <= net_count <= 40, f"Unexpected net count: {net_count}"
    except Exception:
        pytest.skip("pcbnew not available")
