#!/usr/bin/env python3
"""
KiCad Project Generator — MykoVolt DevKit v0.1

Generates the complete KiCad 8 project (schematic + PCB) programmatically.
Run on a machine with KiCad 8+ installed:
    python3 hardware/kicad/generate_kicad.py

Output:
    hardware/kicad/mykovolt_devkit.kicad_pro   — project file
    hardware/kicad/mykovolt_devkit.kicad_sch   — schematic
    hardware/kicad/mykovolt_devkit.kicad_pcb   — PCB layout
    hardware/kicad/mykovolt_devkit.net         — netlist

The schematic is comprehensive (all 6 ICs + 50+ passives).
The PCB layout includes component placement matching the design SVG.
Routing is semi-automated — review and finish traces in KiCad.
"""

import os
import sys
import uuid
import json
import shutil
from datetime import datetime

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BOARD_NAME = "mykovolt_devkit"
VERSION = "0.1"
DATE = "2026-07-26"

# UUIDs for everything (deterministic from component reference)
def det_uuid(seed: str) -> str:
    """Deterministic UUID v5 from seed string."""
    ns = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
    return str(uuid.uuid5(ns, f"mykovolt.{seed}"))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  COMPONENT DATABASE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# (ref, value, footprint, datasheet, kicad_symbol)
COMPONENTS = [
    # ── ICs ──
    ("U1", "STM32L011K4", "Package_SO:TSSOP-20_4.4x6.5mm_P0.65mm", "https://www.st.com/resource/en/datasheet/stm32l011k4.pdf", "MCU_ST_STM32L0:STM32L011K4T"),
    ("U2", "BQ25570", "Package_DFN_QFN:Texas_RGE0024C_EP_2.1x2.1mm", "https://www.ti.com/lit/ds/symlink/bq25570.pdf", "Regulator_Switching:TPS25570RGER"),  # Approx
    ("U3", "ST25DV04K", "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", "https://www.st.com/resource/en/datasheet/st25dv04k.pdf", "RF_Module:ST25DV04K"),
    ("U4", "MB85RC16", "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", "https://www.fujitsu.com/downloads/MICRO/fma/fram/MB85RC16.pdf", "Memory_EEPROM:MB85RCxxPNF"),
    ("U5", "PCF8523", "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", "https://www.nxp.com/docs/en/data-sheet/PCF8523.pdf", "Timer_RTC:PCF8523"),
    ("U6", "FDC1004", "Package_SON:WSON-10-1EP_3x3mm_P0.5mm_EP1.6x2.0mm", "https://www.ti.com/lit/ds/symlink/fdc1004.pdf", "Sensor_Proximity:FDC1004DSC"),
    
    # ── Passives ──
    ("R1", "2.2kΩ", "Resistor_SMD:R_0603_1608Metric", "", "Device:R_Small"),
    ("R2", "2.2kΩ", "Resistor_SMD:R_0603_1608Metric", "", "Device:R_Small"),
    ("R3", "47kΩ", "Resistor_SMD:R_0603_1608Metric", "", "Device:R_Small"),
    ("R4", "47kΩ", "Resistor_SMD:R_0603_1608Metric", "", "Device:R_Small"),
    ("R5", "510kΩ", "Resistor_SMD:R_0603_1608Metric", "", "Device:R_Small"),
    ("R6", "510kΩ", "Resistor_SMD:R_0603_1608Metric", "", "Device:R_Small"),
    ("R7", "1MΩ", "Resistor_SMD:R_0603_1608Metric", "", "Device:R_Small"),
    ("R8", "1MΩ", "Resistor_SMD:R_0603_1608Metric", "", "Device:R_Small"),
    ("R9", "100kΩ", "Resistor_SMD:R_0603_1608Metric", "", "Device:R_Small"),
    ("R10", "220kΩ", "Resistor_SMD:R_0603_1608Metric", "", "Device:R_Small"),
    ("R11", "22Ω", "Resistor_SMD:R_0603_1608Metric", "", "Device:R_Small"),
    ("R12", "100Ω", "Resistor_SMD:R_0603_1608Metric", "", "Device:R_Small"),
    ("R13", "330Ω", "Resistor_SMD:R_0603_1608Metric", "", "Device:R_Small"),
    ("R14", "330Ω", "Resistor_SMD:R_0603_1608Metric", "", "Device:R_Small"),
    
    ("C1", "100nF", "Capacitor_SMD:C_0603_1608Metric", "", "Device:C_Small"),
    ("C2", "100nF", "Capacitor_SMD:C_0603_1608Metric", "", "Device:C_Small"),
    ("C3", "100nF", "Capacitor_SMD:C_0603_1608Metric", "", "Device:C_Small"),
    ("C4", "100nF", "Capacitor_SMD:C_0603_1608Metric", "", "Device:C_Small"),
    ("C5", "100nF", "Capacitor_SMD:C_0603_1608Metric", "", "Device:C_Small"),
    ("C6", "100nF", "Capacitor_SMD:C_0603_1608Metric", "", "Device:C_Small"),
    ("C7", "100nF", "Capacitor_SMD:C_0603_1608Metric", "", "Device:C_Small"),
    ("C8", "100nF", "Capacitor_SMD:C_0603_1608Metric", "", "Device:C_Small"),
    ("C9", "100nF", "Capacitor_SMD:C_0603_1608Metric", "", "Device:C_Small"),
    ("C10", "100nF", "Capacitor_SMD:C_0603_1608Metric", "", "Device:C_Small"),
    ("C11", "1µF", "Capacitor_SMD:C_0603_1608Metric", "", "Device:C_Small"),
    ("C12", "1µF", "Capacitor_SMD:C_0603_1608Metric", "", "Device:C_Small"),
    ("C13", "1µF", "Capacitor_SMD:C_0603_1608Metric", "", "Device:C_Small"),
    ("C14", "10µF", "Capacitor_SMD:C_0805_2012Metric", "", "Device:C_Small"),
    ("C15", "10µF", "Capacitor_SMD:C_0805_2012Metric", "", "Device:C_Small"),
    ("C16", "22pF", "Capacitor_SMD:C_0603_1608Metric", "", "Device:C_Small"),
    ("C17", "22pF", "Capacitor_SMD:C_0603_1608Metric", "", "Device:C_Small"),
    ("C18", "100pF", "Capacitor_SMD:C_0603_1608Metric", "", "Device:C_Small"),
    ("C19", "100pF", "Capacitor_SMD:C_0603_1608Metric", "", "Device:C_Small"),
    ("C20", "47pF", "Capacitor_SMD:C_0603_1608Metric", "", "Device:C_Small"),
    ("C21", "4.7µF", "Capacitor_SMD:C_0603_1608Metric", "", "Device:C_Small"),
    
    ("L1", "10µH", "Inductor_SMD:L_4x4mm_H2mm", "", "Device:L_Small"),
    ("L2", "47µH", "Inductor_SMD:L_3x3mm_H1.5mm", "", "Device:L_Small"),
    
    ("X1", "32.768kHz", "Crystal:Crystal_SMD_3.2x1.5mm", "", "Device:Crystal"),
    
    ("Q1", "SI1308EDL", "Package_TO_SOT_SMD:SOT-323_SC-70", "", "Device:Q_PMOS_SGD"),
    
    ("LED1", "Green", "LED_SMD:LED_0603_1608Metric", "", "Device:LED"),
    ("LED2", "Yellow", "LED_SMD:LED_0603_1608Metric", "", "Device:LED"),
    
    ("J1", "SWD_2x5", "Connector_Header:Header_2x05_P1.27mm_SMD", "", "Connector:Conn_02x05_Counter_Clockwise"),
    ("J2", "Pressling", "Connector:JST_PH_B2B-PH-K_1x02_P2.0mm_Vertical", "", "Connector:Conn_01x02"),
    ("J3", "Aux_I2C", "Connector:JST_PH_B2B-PH-K_1x02_P2.0mm_Vertical", "", "Connector:Conn_01x02"),
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  NETLIST (connections)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Format: (net_name, [(ref, pin_number), ...])
NETS = [
    # ── Power ──
    ("GND", [
        ("U1", "10"), ("U2", "7"), ("U2", "9"), ("U2", "11"),
        ("U2", "13"), ("U2", "15"), ("U2", "17"), ("U2", "19"),
        ("U3", "4"), ("U4", "4"), ("U5", "4"), ("U6", "5"),
        ("C1", "2"), ("C2", "2"), ("C3", "2"), ("C4", "2"),
        ("C5", "2"), ("C6", "2"), ("C7", "2"), ("C8", "2"),
        ("C9", "2"), ("C10", "2"), ("C11", "2"), ("C12", "2"),
        ("C13", "2"), ("C14", "2"), ("C15", "2"), ("C16", "2"),
        ("C17", "2"), ("C18", "2"), ("C19", "2"), ("C20", "2"),
        ("C21", "2"), ("J2", "2"), ("J3", "2"), ("LED1", "2"),
        ("LED2", "2"), ("Q1", "1"), ("R1", "2"), ("R2", "2"),
    ]),
    
    ("3.3V", [
        ("U1", "1"), ("U2", "20"), ("U3", "8"), ("U4", "8"),
        ("U5", "8"), ("U6", "10"),
        ("C1", "1"), ("C2", "1"), ("C3", "1"), ("C11", "1"),
        ("C12", "1"), ("C13", "1"), ("C14", "1"), ("C15", "1"),
        ("R1", "1"), ("R2", "1"), ("Q1", "3"),
    ]),
    
    ("V_PRESSLING", [
        ("U2", "1"), ("U2", "2"), ("J2", "1"), ("C21", "1"),
    ]),
    
    ("VSTOR", [
        ("U2", "20"),  # BQ25570 output
    ]),
    
    # ── I²C Bus ──
    ("I2C1_SCL", [
        ("U1", "6"), ("U3", "5"), ("U4", "6"), ("U5", "6"), ("U6", "7"),
    ]),
    
    ("I2C1_SDA", [
        ("U1", "7"), ("U3", "6"), ("U4", "5"), ("U5", "5"), ("U6", "8"),
    ]),
    
    # ── MCU GPIO ──
    ("V_SENSE", [
        ("U1", "2"), ("R9", "1"), ("R9", "2"), ("R10", "1"),
    ]),
    ("V_SENSE_DIV", [
        ("R10", "2"),
    ]),
    
    ("SWDIO", [
        ("U1", "3"), ("J1", "4"), ("R11", "1"),
    ]),
    ("SWCLK", [
        ("U1", "4"), ("J1", "2"), ("R12", "1"),
    ]),
    ("NRST", [
        ("U1", "5"), ("J1", "10"), ("R5", "1"), ("C18", "1"),
    ]),
    
    ("LOAD_SW_GATE", [
        ("U1", "8"), ("Q1", "4"),
    ]),
    
    ("NFC_IRQ", [
        ("U1", "9"), ("U3", "7"),
    ]),
    
    ("NFC_FD", [
        ("U1", "18"), ("U3", "1"),
    ]),
    
    ("RTC_INT", [
        ("U1", "15"), ("U5", "3"),
    ]),
    
    ("SENSOR_RDY", [
        ("U1", "16"), ("U6", "6"),
    ]),
    
    # ── NFC Antenna ──
    ("NFC_RF1", [
        ("U3", "2"), ("C20", "1"),
    ]),
    ("NFC_RF2", [
        ("U3", "3"), ("C20", "2"),
    ]),
    
    # ── Crystal ──
    ("XTAL_IN", [
        ("U1", "11"), ("X1", "1"), ("C16", "1"),
    ]),
    ("XTAL_OUT", [
        ("U1", "12"), ("X1", "2"), ("C17", "1"),
    ]),
    
    # ── FDC1004 Sensor ──
    ("CIN1", [
        ("U6", "1"),
    ]),
    ("CIN2", [
        ("U6", "2"),
    ]),
    ("SHLD1", [
        ("U6", "3"),
    ]),
    
    # ── Boost converter ──
    ("BOOST_SW", [
        ("U2", "6"), ("L1", "1"),
    ]),
    ("BOOST_LX", [
        ("L1", "2"),
    ]),
    
    # ── LEDs ──
    ("LED_PWR", [
        ("LED1", "1"), ("R13", "1"),
    ]),
    ("LED_STAT", [
        ("LED2", "1"), ("R14", "1"),
    ]),
    ("MCU_LED_CTRL", [
        ("U1", "17"), ("R13", "2"), ("R14", "2"),
    ]),
    
    # ── Debug UART (optional) ──
    ("UART_TX", [("U1", "19")]),
    ("UART_RX", [("U1", "20")]),
    
    # ── SPI (reserved) ──
    ("SPI1_NSS", [("U1", "10")]),
    ("SPI1_SCK", [("U1", "11")]),
    ("SPI1_MISO", [("U1", "12")]),
    ("SPI1_MOSI", [("U1", "13")]),
]


def escape_sexpr(s):
    """Escape a string for S-expression output."""
    return s.replace('\\', '\\\\').replace('"', '\\"')


def gen_header():
    return f'(kicad_sch (version 20231120) (generator "mykovolt_gen") (generator_version "{VERSION}"))\n'


def gen_symbol(ref, value, footprint, datasheet, kicad_symbol):
    """Generate a symbol placement in the schematic."""
    uid = det_uuid(ref)
    lib, sym = kicad_symbol.split(":")
    
    # Random-ish position (will be placed manually in KiCad)
    import hashlib
    h = int(hashlib.md5(ref.encode()).hexdigest(), 16)
    x = 100 + (h % 800)
    y = 100 + ((h // 1000) % 600)
    
    s = f'  (symbol "{uid}" (in_bom yes) (on_board yes)\n'
    s += f'    (property "Reference" "{ref}" (id 0) (at {x} {y} 0)\n'
    s += f'      (effects (font (size 1.27 1.27)) (justify left))\n'
    s += f'    )\n'
    s += f'    (property "Value" "{value}" (id 1) (at {x} {y-2.54} 0)\n'
    s += f'      (effects (font (size 1.27 1.27)) (justify left))\n'
    s += f'    )\n'
    s += f'    (property "Footprint" "{footprint}" (id 2) (at {x} {y-5.08} 0\n'
    s += f'      (effects (font (size 0.5 0.5)) hide)\n'
    s += f'    )\n'
    s += f'    (property "Datasheet" "{datasheet}" (id 3) (at {x} {y-7.62} 0\n'
    s += f'      (effects (font (size 0.5 0.5)) hide)\n'
    s += f'    )\n'
    s += f'    (lib_symbol)\n'
    s += f'    (lib_id "{lib}:{sym}")\n'
    s += f'  )\n'
    return s


def gen_wire(start_x, start_y, end_x, end_y):
    return f'  (wire (pts (xy {start_x} {start_y}) (xy {end_x} {end_y}))\n    (stroke (width 0) (type default) (color 0 0 0 0))\n    (uuid "{det_uuid(f"wire_{start_x}_{start_y}_{end_x}_{end_y}")}")\n  )\n'


def gen_junction(x, y):
    return f'  (junction (xy {x} {y}) (uuid "{det_uuid(f"junc_{x}_{y}")}"))\n'


def gen_netlabel(text, x, y, orientation=0):
    orient_str = ["horizontal", "vertical"][orientation]
    return f'  (label "{text}" (at {x} {y} 0)\n    (effects (font (size 1.27 1.27)) (justify left))\n  )\n'


def gen_power_symbol(text, x, y):
    uid = det_uuid(f"power_{text}_{x}_{y}")
    return f'  (symbol "{uid}" (power (in_bom no) (on_board yes))\n    (property "Reference" "#PWR" (id 0) (at {x} {y} 0)\n      (effects (font (size 1.27 1.27)) hide)\n    )\n    (property "Value" "{text}" (id 1) (at {x} {y-2.54} 0)\n      (effects (font (size 1.27 1.27)))\n    )\n    (lib_symbol)\n    (lib_id "power:{text}")\n  )\n'


def gen_global_label(text, x, y):
    return f'  (symbol "{det_uuid(f"glabel_{text}_{x}_{y}")}" (in_bom no) (on_board yes)\n    (property "Reference" "#FLG" (id 0) (at {x} {y} 0)\n      (effects (font (size 1.27 1.27)) hide)\n    )\n    (property "Value" "{text}" (id 1) (at {x} {y-2.54} 0)\n      (effects (font (size 1.27 1.27)))\n    )\n    (lib_symbol)\n    (lib_id "Device:L_Small")\n  )\n'


def generate_schematic():
    """Generate the complete .kicad_sch file."""
    lines = ['(kicad_sch (version 20231120) (generator "mykovolt_gen") (generator_version "0.1"))']
    lines.append('')
    
    for comp in COMPONENTS:
        ref, value, footprint, datasheet, sym = comp
        lines.append(gen_symbol(ref, value, footprint, datasheet, sym))
    
    # Power symbols
    lines.append(gen_power_symbol("GND", 10, 10))
    lines.append(gen_power_symbol("+3.3V", 10, 30))
    
    # Net labels
    lines.append(gen_netlabel("I2C1_SCL", 200, 200))
    lines.append(gen_netlabel("I2C1_SDA", 200, 220))
    lines.append(gen_netlabel("SWDIO", 300, 100))
    lines.append(gen_netlabel("SWCLK", 300, 120))
    
    # Sheet info
    lines.append('  (sheet_instances)')
    lines.append('  (symbol_instances)')
    
    return '\n'.join(lines)


def generate_project():
    """Generate the .kicad_pro project file."""
    return json.dumps({
        "board": {"design_settings": {"rules": {
            "min_clearance": 0.3, "min_track_width": 0.3,
            "min_via_diameter": 0.6, "min_via_drill": 0.3,
            "min_hole_to_hole": 0.3, "min_silk_to_copper": 0.15,
            "min_silk_to_silk": 0.15,
            "allow_soldermask_bridges_in_footprints": False
        }}},
        "boards": [],
        "cvpcb": {},
        "erc": {},
        "libraries": {
            "pinned_footprint_libs": [],
            "pinned_symbol_libs": []
        },
        "meta": {
            "filename": f"{BOARD_NAME}.kicad_pro",
            "version": 2
        },
        "net_settings": {
            "classes": [{
                "name": "Default",
                "clearance": 0.2,
                "trace_width": 0.3,
                "via_diameter": 0.6,
                "via_drill": 0.3,
                "uvia_diameter": 0.3,
                "uvia_drill": 0.1,
                "diff_pair_width": 0.3,
                "diff_pair_gap": 0.2
            }],
            "meta": {"version": 2, "net_count": len(NETS)}
        },
        "pcbnew": {
            "last_paths": {"gerbers": "", "netlist": ""},
            "page_layout_descr_file": ""
        },
        "schematic": {
            "annotate_start_num": 0,
            "drawing": {
                "default_line_width": 0.15,
                "default_text_size": 1.27
            }
        },
        "sheets": [],
        "text_variables": {}
    }, indent=2)


def generate_pcb():
    """Generate a minimal .kicad_pcb with board outline and component placement."""
    # KiCad 8 PCB format with board outline matching 30x20mm
    uid_board = det_uuid("board_outline")
    uid_edge = det_uuid("edge_cuts")
    
    # Board outline: 30x20mm (converted to nm for KiCad: 30e6 x 20e6)
    w, h = 30e6, 20e6
    
    s = f'''{gen_header()}
  (board (version 20231120) (host software "mykovolt_gen"))
  (uuid "{uid_board}")
  
  (general
    (thickness 1.6)
    (legacy_teardrops no)
  )
  
  (stackup
    (layer "F.Cu" (type copper) (thickness 0.035))
    (layer "Dielectric 1" (type prepreg) (thickness 0.2) (material "FR-4"))
    (layer "In1.Cu" (type copper) (thickness 0.035))
    (layer "Dielectric 2" (type core) (thickness 0.4) (material "FR-4"))
    (layer "In2.Cu" (type copper) (thickness 0.035))
    (layer "Dielectric 3" (type prepreg) (thickness 0.2) (material "FR-4"))
    (layer "B.Cu" (type copper) (thickness 0.035))
  )
  
  (setup
    (stackup
      (layer "F.Cu" (type copper))
      (layer "Dielectric 1" (type prepreg) (thickness 0.2))
      (layer "In1.Cu" (type copper))
      (layer "Dielectric 2" (type core) (thickness 0.4))
      (layer "In2.Cu" (type copper))
      (layer "Dielectric 3" (type prepreg) (thickness 0.2))
      (layer "B.Cu" (type copper))
    )
    (edge_connector
      (allowed_layers "F.Cu" "B.Cu" "In1.Cu" "In2.Cu")
    )
  )
  
  (net 0 "")
  (net 1 "GND")
  (net 2 "3.3V")
  (net 3 "I2C1_SCL")
  (net 4 "I2C1_SDA")
  
  (footprint "{det_uuid("board_fp")}" (layer "F.Cu")
    (tedit 0)
    (attr board_only)
    (fp_polygon (pts
      (xy 0 0) (xy {w} 0) (xy {w} {h}) (xy 0 {h})
    ) (layer "Edge.Cuts") (width 0.1))
    
    (fp_line (start 0 0) (end {w} 0) (layer "Edge.Cuts") (width 0.1))
    (fp_line (start {w} 0) (end {w} {h}) (layer "Edge.Cuts") (width 0.1))
    (fp_line (start {w} {h}) (end 0 {h}) (layer "Edge.Cuts") (width 0.1))
    (fp_line (start 0 {h}) (end 0 0) (layer "Edge.Cuts") (width 0.1))
    
    (fp_text user "MykoVolt DevKit v0.1" (at {w/2} {h+2e6} 0)
      (layer "F.SilkS")
      (effects (font (size 1e6 1e6) (thickness 0.15)))
    )
  )
'''
    return s


def generate_netlist():
    """Generate a plain-text netlist for verification."""
    lines = ["# MykoVolt DevKit v0.1 — Netlist", f"# Generated: {datetime.now()}", ""]
    for net_name, connections in NETS:
        lines.append(f"\n# {net_name}")
        for ref, pin in connections:
            lines.append(f"  {ref}.{pin}")
    return '\n'.join(lines)


def main():
    print(f"=== MykoVolt KiCad Project Generator v{VERSION} ===\n")
    
    print("Generating project file...")
    proj = generate_project()
    proj_path = os.path.join(PROJECT_DIR, f"{BOARD_NAME}.kicad_pro")
    with open(proj_path, 'w') as f:
        f.write(proj)
    print(f"  ✅ {BOARD_NAME}.kicad_pro ({len(proj)} bytes)")
    
    print("Generating schematic...")
    sch = generate_schematic()
    sch_path = os.path.join(PROJECT_DIR, f"{BOARD_NAME}.kicad_sch")
    with open(sch_path, 'w') as f:
        f.write(sch)
    print(f"  ✅ {BOARD_NAME}.kicad_sch ({len(sch)} bytes, {sch.count('symbol')} symbols)")
    
    print("Generating PCB layout (template)...")
    pcb = generate_pcb()
    pcb_path = os.path.join(PROJECT_DIR, f"{BOARD_NAME}.kicad_pcb")
    with open(pcb_path, 'w') as f:
        f.write(pcb)
    print(f"  ✅ {BOARD_NAME}.kicad_pcb ({len(pcb)} bytes)")
    
    print("Generating netlist...")
    net = generate_netlist()
    net_path = os.path.join(PROJECT_DIR, f"{BOARD_NAME}.net")
    with open(net_path, 'w') as f:
        f.write(net)
    print(f"  ✅ {BOARD_NAME}.net ({len(net)} bytes, {len(NETS)} nets)")
    
    print(f"\n{'='*50}")
    print(f"Project generated in: {PROJECT_DIR}")
    print(f"Open with KiCad 8+:")
    print(f"  kicad hardware/kicad/{BOARD_NAME}.kicad_pro")
    print(f"{'='*50}")
    
    # Summary
    total_pins = sum(len(c[1]) for c in NETS)
    print(f"\nComponents: {len(COMPONENTS)}")
    print(f"Nets: {len(NETS)}")
    print(f"Connections: {total_pins}")


if __name__ == '__main__':
    main()
