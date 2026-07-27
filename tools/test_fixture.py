#!/usr/bin/env python3
"""
Test Fixture Generator — MykoVolt Probe Card

Generates a companion PCB with test points for all critical nets,
allowing automated testing with pogo pins.

Usage:
    python3 tools/test_fixture.py                           # Generate fixture for main design
    python3 tools/test_fixture.py --output build/fixture/   # Custom output dir
    python3 tools/test_fixture.py --list-nets               # Just list test nets
    python3 tools/test_fixture.py --json                    # JSON output
"""

import os
import sys
import json
import argparse
from datetime import datetime

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HW_DIR = os.path.join(PROJECT_DIR, "hardware", "kicad")

# Critical nets to probe — these must be accessible on test points
TEST_NETS = [
    # Power
    ("3.3V", "Main regulated rail"),
    ("GND", "Ground reference"),
    ("V_PRESSLING", "Raw MFC input voltage"),
    ("VSTOR", "Supercap storage voltage"),
    ("VBAT_OK", "BQ25570 power-good indicator"),

    # I2C
    ("I2C1_SCL", "I2C clock"),
    ("I2C1_SDA", "I2C data"),

    # Sensor
    ("CIN1", "Capacitance sensor channel 1"),
    ("CIN2", "Capacitance sensor channel 2"),

    # NFC
    ("NFC_RF1", "NFC antenna feed 1"),
    ("NFC_RF2", "NFC antenna feed 2"),

    # Debug
    ("SWDIO", "SWD debug data"),
    ("SWCLK", "SWD debug clock"),
    ("NRST", "MCU reset"),
    ("UART_TX", "Serial debug TX"),
    ("UART_RX", "Serial debug RX"),

    # MCU
    ("MCU_LED_CTRL", "Status LED control"),
    ("LOAD_SW_GATE", "Load switch gate"),

    # Interrupts
    ("NFC_IRQ", "NFC interrupt"),
    ("RTC_INT", "RTC interrupt"),
    ("SENSOR_RDY", "Sensor ready"),
]

# Pogo pin header (2×10, 2.54mm pitch)
# Standard JTAG/SWD 2×10 pinout for compatibility
FIXTURE_HEADER = {
    "rows": 2,
    "cols": 10,
    "pitch_mm": 2.54,
    "type": "pin_header_2x10",
}


def generate_fixture_schematic(nets):
    """Generate a simple schematic for the test fixture board."""
    lines = []
    lines.append("(kicad_sch")
    lines.append("  (version 20240125)")
    lines.append("  (generator test_fixture_gen)")
    lines.append('  (generator_version "1.0")')
    lines.append('  (uuid "fixture-0000-0000-0000-000000000001")')
    lines.append('  (paper "A4")')
    lines.append("  (title_block")
    lines.append('    (title "MykoVolt Test Fixture")')
    lines.append(f'    (date "{datetime.now().strftime("%Y-%m-%d")}")')
    lines.append('    (rev "0.1")')
    lines.append("  )")
    lines.append("  (lib_symbols)")
    lines.append("  )")
    lines.append("")

    # Add connector symbol
    lines.append("  (symbol")
    lines.append('    (lib_id Connector_Generic:Conn_02x10_Counter_Clockwise)')
    lines.append("    (at 200 200 0)")
    lines.append("    (unit 1)")

    # Add label for each net
    for i, (net_name, description) in enumerate(nets):
        y = 300 + i * 40
        lines.append("")
        lines.append("  (symbol")
        lines.append(f'    (lib_id Connector_Generic:Conn_01x01)')
        lines.append(f"    (at 400 {y} 0)")
        lines.append("    (unit 1)")
        lines.append(f'    (reference "TP{i+1}")')
        lines.append(f'    (value "{net_name}")')
        lines.append("  )")

    lines.append("  (symbol_instances)")
    lines.append("  )")
    lines.append(")")

    return "\n".join(lines)


def generate_fixture_pcb(nets, board_w=50, board_h=40):
    """Generate a PCB layout for the test fixture using pcbnew if available."""
    # Board size: 50×40mm — room for 2×10 header + 16 test points
    pcb_lines = []
    pcb_lines.append(f"(kicad_pcb (version 20211014) (generator test_fixture_gen)")
    pcb_lines.append("  (general")
    pcb_lines.append(f"    (thickness 1.6)")
    pcb_lines.append("  )")
    pcb_lines.append(f"  (paper \"A4\")")
    pcb_lines.append(f"  (title_block")
    pcb_lines.append(f'    (title "MykoVolt Test Fixture")')
    pcb_lines.append(f"  )")
    pcb_lines.append("")

    # Board outline
    pcb_lines.append(f"  (gr_rect (start 0 0) (end {board_w} {board_h})")
    pcb_lines.append(f'    (layer "Edge.Cuts") (width 0.1))')

    # Space for additional pogo pin layout
    pcb_lines.append("")

    pcb_lines.append(f"  (footprint \"Connector_PinHeader_2.54mm:PinHeader_2x10_P2.54mm_Vertical\"")
    pcb_lines.append(f"    (at 10 20 0)")
    pcb_lines.append(f'    (layer "F.Cu")')
    pcb_lines.append(f'    (fp_text reference "J1" (at 0 0) (layer "F.SilkS")')
    pcb_lines.append(f'      (effects (font (size 1 1))))')
    pcb_lines.append(f"  )")
    pcb_lines.append("")

    # Add test point footprints
    for i, (net_name, description) in enumerate(nets):
        x = 35
        y = 3 + i * 2.2
        if y > board_h - 3:
            x = 43
            y = 3 + (i - 15) * 2.2
        if y > board_h - 3:
            continue  # Skip if no room

        pcb_lines.append(f"  (footprint \"TestPoint:TestPoint_Pad_1.0x1.0mm\"")
        pcb_lines.append(f"    (at {x} {y} 0)")
        pcb_lines.append(f'    (layer "F.Cu")')
        pcb_lines.append(f'    (fp_text reference "TP{i+1}" (at 0 0) (layer "F.SilkS")')
        pcb_lines.append(f'      (effects (font (size 1 1))))')
        pcb_lines.append(f'    (fp_text value "{net_name}" (at 0 2) (layer "F.Fab")')
        pcb_lines.append(f'      (effects (font (size 0.5 0.5))))')
        pcb_lines.append(f"  )")
        pcb_lines.append("")

    pcb_lines.append(")")

    return "\n".join(pcb_lines)


def main():
    parser = argparse.ArgumentParser(description="MykoVolt test fixture generator")
    parser.add_argument("--output", "-o", default=os.path.join(PROJECT_DIR, "build", "fixture"),
                        help="Output directory")
    parser.add_argument("--list-nets", action="store_true",
                        help="List test nets and exit")
    parser.add_argument("--json", action="store_true",
                        help="JSON output")
    args = parser.parse_args()

    if args.list_nets:
        print(f"{'Net':<20} Description")
        print(f"{'─'*20} {'─'*30}")
        for net_name, desc in TEST_NETS:
            print(f"{net_name:<20} {desc}")
        print(f"\n{len(TEST_NETS)} test nets total")
        return

    os.makedirs(args.output, exist_ok=True)

    # Generate fixture schematic
    sch = generate_fixture_schematic(TEST_NETS)
    sch_path = os.path.join(args.output, "mykovolt_fixture.kicad_sch")
    with open(sch_path, "w") as f:
        f.write(sch)
    print(f"  ✓ {sch_path} ({len(sch)} bytes)")

    # Generate fixture PCB
    pcb = generate_fixture_pcb(TEST_NETS)
    pcb_path = os.path.join(args.output, "mykovolt_fixture.kicad_pcb")
    with open(pcb_path, "w") as f:
        f.write(pcb)
    print(f"  ✓ {pcb_path} ({len(pcb)} bytes)")

    # Generate probe map (net → test point number)
    probe_map = {}
    for i, (net_name, description) in enumerate(TEST_NETS):
        probe_map[net_name] = {
            "test_point": f"TP{i+1}",
            "position_mm": {"x": 35, "y": 3 + i * 2.2},
            "description": description,
        }

    probe_path = os.path.join(args.output, "probe_map.json")
    with open(probe_path, "w") as f:
        json.dump(probe_map, f, indent=2)
    print(f"  ✓ {probe_path}")

    print(f"\n  {len(TEST_NETS)} test points")
    print(f"  Output: {args.output}/")

    if args.json:
        print(json.dumps({"fixture": args.output, "test_points": len(TEST_NETS)}, indent=2))


if __name__ == "__main__":
    main()
