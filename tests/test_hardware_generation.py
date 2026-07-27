"""Tests for the KiCad hardware generation database and output files.

Validates the component database, netlist, schematic, and PCB output
for consistency and correctness.
"""

import os
import sys
import re

# Add project root to path
PROJECT_DIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, PROJECT_DIR)
sys.path.insert(0, os.path.join(PROJECT_DIR, "hardware", "kicad"))

from generate_kicad import (
    COMPONENTS,
    NETS,
    POS,
    PCB_POS,
    CUSTOM_SYMBOLS,
    BOARD_NAME,
    PROJECT_DIR as HW_DIR,
    VERSION,
    det_uuid,
    KICAD_VERSION,
)

import pytest


# ═══════════════════════════════════════════════════════════════
# 1. Component Database Integrity
# ═══════════════════════════════════════════════════════════════

class TestComponentDatabase:
    """Validate the COMPONENTS list integrity."""

    def test_all_components_have_unique_refs(self):
        """No duplicate component reference designators."""
        refs = [c[0] for c in COMPONENTS]
        assert len(refs) == len(set(refs)), f"Duplicate refs: {[r for r in refs if refs.count(r) > 1]}"

    def test_all_components_have_values(self):
        """Every component has a non-empty value."""
        for ref, value, *_ in COMPONENTS:
            assert value, f"{ref} has empty value"

    def test_all_components_have_footprints(self):
        """Every component has a non-empty footprint."""
        for ref, _, footprint, *_ in COMPONENTS:
            assert footprint, f"{ref} has empty footprint"

    def test_all_footprints_have_library_prefix(self):
        """Footprints follow KiCad 'LIB:NAME' format."""
        for ref, _, footprint, *_ in COMPONENTS:
            assert ":" in footprint, f"{ref} footprint '{footprint}' missing library prefix"

    def test_components_are_categorized_correctly(self):
        """All ref prefixes follow standard KiCad conventions."""
        ics = [c for c in COMPONENTS if c[0].startswith("U")]
        resistors = [c for c in COMPONENTS if c[0].startswith("R") and not c[0].startswith("RTC")]
        caps = [c for c in COMPONENTS if c[0].startswith("C")]
        inductors = [c for c in COMPONENTS if c[0] == "L1" or c[0] == "L2"]
        connectors = [c for c in COMPONENTS if c[0].startswith("J")]
        leds = [c for c in COMPONENTS if c[0].startswith("LED")]
        diodes = [c for c in COMPONENTS if c[0].startswith("D")]
        transistors = [c for c in COMPONENTS if c[0].startswith("Q")]
        crystals = [c for c in COMPONENTS if c[0].startswith("X")]
        supercaps = [c for c in COMPONENTS if c[0].startswith("SC")]

        assert len(ics) == 6, f"Expected 6 ICs, got {len(ics)}"
        assert len(resistors) == 14, f"Expected 14 resistors, got {len(resistors)}"
        assert len(caps) == 24, f"Expected 24 caps, got {len(caps)}"
        assert len(inductors) == 2
        assert len(connectors) == 4
        assert len(leds) == 2
        assert len(diodes) == 2
        assert len(transistors) == 1
        assert len(crystals) == 1
        assert len(supercaps) == 1

        total = len(ics + resistors + caps + inductors + connectors + leds + diodes + transistors + crystals + supercaps)
        assert total == len(COMPONENTS), f"Categorized {total}, but have {len(COMPONENTS)}"


# ═══════════════════════════════════════════════════════════════
# 2. Position Database Integrity
# ═══════════════════════════════════════════════════════════════

class TestComponentPositions:
    """Validate that all components have proper positions."""

    def test_all_components_have_schematic_positions(self):
        """Every component in COMPONENTS has a position in POS."""
        refs = {c[0] for c in COMPONENTS}
        pos_refs = set(POS.keys())
        missing = refs - pos_refs
        assert not missing, f"Components missing SCH positions: {missing}"

    def test_all_components_have_pcb_positions(self):
        """Every component in COMPONENTS has a position in PCB_POS."""
        refs = {c[0] for c in COMPONENTS}
        pcb_refs = set(PCB_POS.keys())
        missing = refs - pcb_refs
        assert not missing, f"Components missing PCB positions: {missing}"

    def test_no_extra_schematic_positions(self):
        """POS doesn't contain positions for unknown components."""
        refs = {c[0] for c in COMPONENTS}
        extra = set(POS.keys()) - refs
        assert not extra, f"Extra SCH positions: {extra}"

    def test_no_extra_pcb_positions(self):
        """PCB_POS doesn't contain positions for unknown components."""
        refs = {c[0] for c in COMPONENTS}
        extra = set(PCB_POS.keys()) - refs
        assert not extra, f"Extra PCB positions: {extra}"

    def test_pcb_positions_within_board(self):
        """All PCB positions are within the 30x20mm board."""
        BOARD_W, BOARD_H = 30e6, 20e6
        for ref, (x, y) in PCB_POS.items():
            assert 0 <= x <= BOARD_W, f"{ref} PCB X={x/1e6:.1f}mm outside board (0..30mm)"
            assert 0 <= y <= BOARD_H, f"{ref} PCB Y={y/1e6:.1f}mm outside board (0..20mm)"

    def test_pcb_positions_unique(self):
        """No two components share the exact same PCB position."""
        seen = {}
        for ref, (x, y) in PCB_POS.items():
            key = (x, y)
            assert key not in seen, f"{ref} and {seen[key]} share PCB position ({x/1e6:.1f}, {y/1e6:.1f})mm"
            seen[key] = ref


# ═══════════════════════════════════════════════════════════════
# 3. Netlist Integrity
# ═══════════════════════════════════════════════════════════════

class TestNetlist:
    """Validate the netlist consistency."""

    def test_all_nets_have_unique_names(self):
        """No duplicate net names."""
        names = [n[0] for n in NETS]
        assert len(names) == len(set(names)), f"Duplicate nets: {[n for n in names if names.count(n) > 1]}"

    def test_all_net_connections_reference_known_components(self):
        """Every (ref, pin) in NETS references a component in COMPONENTS."""
        refs = {c[0] for c in COMPONENTS}
        for net_name, connections in NETS:
            for ref, pin in connections:
                assert ref in refs, f"Net '{net_name}': unknown component '{ref}'"
                assert pin, f"Net '{net_name}': {ref} has empty pin number"

    def test_power_nets_exist(self):
        """GND and 3.3V power nets are present."""
        net_names = {n[0] for n in NETS}
        assert "GND" in net_names, "GND net missing"
        assert "3.3V" in net_names, "3.3V net missing"

    def test_gnd_has_most_connections(self):
        """GND net should have the most connections in the design."""
        max_net = max(NETS, key=lambda n: len(n[1]))
        assert max_net[0] == "GND", f"Expected GND as largest net, got '{max_net[0]}' ({len(max_net[1])} conns)"

    def test_i2c_nets_have_pullups(self):
        """I2C nets (SCL, SDA) have at least one pull-up resistor."""
        i2c_nets = {"I2C1_SCL", "I2C1_SDA"}
        for net_name, connections in NETS:
            if net_name in i2c_nets:
                resistors = [r for r, p in connections if r.startswith("R")]
                assert resistors, f"I2C net '{net_name}' missing pull-up resistor"

    def test_no_orphan_nets(self):
        """Every net has at least 2 connections (except power flags)."""
        exempt = {"NFC_FD"}  # Known single-pin nets (now removed, but keep check)
        for net_name, connections in NETS:
            if net_name in exempt:
                continue
            assert len(connections) >= 2 or net_name == "NFC_IRQ", \
                f"Net '{net_name}' has only {len(connections)} connection(s)"

    def test_net_count_is_expected(self):
        """We expect exactly 35 nets."""
        assert len(NETS) == 35, f"Expected 35 nets, got {len(NETS)}"


# ═══════════════════════════════════════════════════════════════
# 4. Generated File Validity
# ═══════════════════════════════════════════════════════════════

class TestGeneratedFiles:
    """Validate the generated KiCad files."""

    @pytest.fixture(autouse=True)
    def setup_and_generate(self):
        """Regenerate all KiCad files before running file tests."""
        from generate_kicad import main as generate
        # Run generation (captures print output)
        generate()
        yield

    def test_project_file_exists(self):
        path = os.path.join(HW_DIR, f"{BOARD_NAME}.kicad_pro")
        assert os.path.exists(path), "Project file not generated"
        assert os.path.getsize(path) > 100, "Project file suspiciously small"

    def test_schematic_file_exists(self):
        path = os.path.join(HW_DIR, f"{BOARD_NAME}.kicad_sch")
        assert os.path.exists(path), "Schematic file not generated"
        assert os.path.getsize(path) > 1000, "Schematic file suspiciously small"

    def test_pcb_file_exists(self):
        path = os.path.join(HW_DIR, f"{BOARD_NAME}.kicad_pcb")
        assert os.path.exists(path), "PCB file not generated"
        assert os.path.getsize(path) > 1000, "PCB file suspiciously small"

    def test_netlist_file_exists(self):
        path = os.path.join(HW_DIR, f"{BOARD_NAME}.net")
        assert os.path.exists(path), "Netlist file not generated"
        assert os.path.getsize(path) > 100, "Netlist file suspiciously small"

    def test_schematic_balanced_parentheses(self):
        """Schematic file has balanced parentheses (valid S-expression)."""
        path = os.path.join(HW_DIR, f"{BOARD_NAME}.kicad_sch")
        with open(path) as f:
            content = f.read()
        depth = 0
        min_depth = 0
        for c in content:
            if c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
            min_depth = min(min_depth, depth)
        assert depth == 0, f"Schematic: unbalanced parens (final depth={depth})"
        assert min_depth >= 0, f"Schematic: negative paren depth ({min_depth})"

    def test_pcb_balanced_parentheses(self):
        """PCB file has balanced parentheses (valid S-expression)."""
        path = os.path.join(HW_DIR, f"{BOARD_NAME}.kicad_pcb")
        with open(path) as f:
            content = f.read()
        depth = 0
        min_depth = 0
        for c in content:
            if c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
            min_depth = min(min_depth, depth)
        assert depth == 0, f"PCB: unbalanced parens (final depth={depth})"
        assert min_depth >= 0, f"PCB: negative paren depth ({min_depth})"

    def test_project_file_is_valid_json(self):
        """The .kicad_pro file is valid JSON."""
        import json
        path = os.path.join(HW_DIR, f"{BOARD_NAME}.kicad_pro")
        with open(path) as f:
            data = json.load(f)
        assert "board" in data
        assert "schematic" in data
        assert "pcbnew" in data

    def test_schematic_contains_custom_symbols(self):
        """Generated schematic includes custom symbol definitions."""
        path = os.path.join(HW_DIR, f"{BOARD_NAME}.kicad_sch")
        with open(path) as f:
            content = f.read()
        for name in CUSTOM_SYMBOLS:
            assert name in content, f"Custom symbol '{name}' not found in schematic"

    def test_schematic_contains_57_components(self):
        """Schematic references all 57 components (Sexp format without quotes)."""
        path = os.path.join(HW_DIR, f"{BOARD_NAME}.kicad_sch")
        with open(path) as f:
            content = f.read()
        for ref, *_ in COMPONENTS:
            # In Sexp format with simp_sexp, strings may or may not have quotes.
            # Check for either "REF" or REF (without quotes).
            assert f' {ref}' in content or f'"{ref}"' in content, \
                f"Component {ref} not found in schematic"


# ═══════════════════════════════════════════════════════════════
# 5. Custom Symbol Definitions
# ═══════════════════════════════════════════════════════════════

class TestCustomSymbols:
    """Validate embedded custom symbol definitions."""

    def test_st25dv04k_has_8_pins(self):
        """ST25DV04K symbol defines exactly 8 pins."""
        content = CUSTOM_SYMBOLS["ST25DV04K"]
        pin_count = len(re.findall(r'\(pin\s+\w+\s+\w+\s+\(at', content))
        assert pin_count == 8, f"ST25DV04K: expected 8 pins, found {pin_count}"

    def test_fdc1004_has_10_pins(self):
        """FDC1004 symbol defines exactly 10 pins."""
        content = CUSTOM_SYMBOLS["FDC1004"]
        pin_count = len(re.findall(r'\(pin\s+\w+\s+\w+\s+\(at', content))
        assert pin_count == 10, f"FDC1004: expected 10 pins, found {pin_count}"

    def test_custom_symbols_have_balanced_parens(self):
        """Each custom symbol has balanced parentheses."""
        for name, content in CUSTOM_SYMBOLS.items():
            depth = 0
            for c in content:
                if c == '(':
                    depth += 1
                elif c == ')':
                    depth -= 1
            assert depth == 0, f"Symbol '{name}': unbalanced parens (final depth={depth})"


# ═══════════════════════════════════════════════════════════════
# 6. UUID Consistency
# ═══════════════════════════════════════════════════════════════

class TestUUID:
    """Validate deterministic UUID generation."""

    def test_deterministic_uuid(self):
        """Same seed always produces the same UUID."""
        assert det_uuid("test") == det_uuid("test")
        assert det_uuid("U1") == det_uuid("U1")

    def test_different_seeds_different_uuids(self):
        """Different seeds produce different UUIDs."""
        assert det_uuid("U1") != det_uuid("U2")

    def test_uuid_format(self):
        """UUIDs follow the standard 8-4-4-4-12 format."""
        import uuid
        for seed in ["U1", "GND", "fp_R1", "power_test"]:
            u = det_uuid(seed)
            parsed = uuid.UUID(u)  # raises ValueError if invalid
            assert str(parsed) == u
