#!/usr/bin/env python3
"""KiCad 6 Project Generator — MykoVolt DevKit v0.1

Generates a valid KiCad 6 project (schematic + PCB) programmatically.
Uses simp_sexp.Sexp for robust S-expression generation and pcbnew for PCB layout.

Target format: version 20211014 (KiCad 6).

Usage:
    python3 hardware/kicad/generate_kicad.py

After generation:
  1. Open hardware/kicad/mykovolt_devkit.kicad_pro in KiCad
  2. Schematic opens automatically — all components wired via global labels
  3. Run Tools → Assign Footprints (auto-resolve library paths)
  4. Run Tools → Update PCB from Schematic to place all footprints
  5. Run Route → Route Tracks to connect traces
  6. Run Inspect → Design Rules Checker to verify
"""

import os
import sys
import json
import uuid
from datetime import datetime
from collections import defaultdict

# ── Try importing simp_sexp for robust S-expression generation ──
try:
    from simp_sexp import Sexp
    HAVE_SEXP = True
except ImportError:
    HAVE_SEXP = False
    print("WARNING: simp_sexp not available, falling back to string-based generation")

# ── Try importing pcbnew for PCB layout ──
try:
    import pcbnew
    HAVE_PCBNEW = True
except ImportError:
    HAVE_PCBNEW = False
    print("WARNING: pcbnew not available, using string-based PCB generation")

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BOARD_NAME = "mykovolt_devkit"
VERSION = "0.1"

# KiCad 6 format version
KICAD_VERSION = 20211014


def det_uuid(seed: str) -> str:
    """Generate a deterministic UUID from a seed string."""
    ns = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
    return str(uuid.uuid5(ns, f"mykovolt.{seed}"))


# ═══════════════════════════════════════════════════════════════
# Component Database
# ═══════════════════════════════════════════════════════════════

# (ref, value, footprint, datasheet, kicad_symbol)
# kicad_symbol follows KiCad's "LIB:SYMBOL" format, or a custom symbol name.
COMPONENTS = [
    # ── ICs ──
    (
        "U1",
        "STM32L011F4Px",
        "Package_SO:TSSOP-20_4.4x6.5mm_P0.65mm",
        "https://www.st.com/resource/en/datasheet/stm32l011k4.pdf",
        "MCU_ST_STM32L0:STM32L011F4Px",
    ),
    (
        "U2",
        "BQ25570",
        "Package_DFN_QFN:QFN-20-1EP_3.5x3.5mm_P0.5mm_EP2x2mm",
        "https://www.ti.com/lit/ds/symlink/bq25570.pdf",
        "Battery_Management:BQ25570",
    ),
    (
        "U3",
        "ST25DV04K",
        "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm",
        "https://www.st.com/resource/en/datasheet/st25dv04k.pdf",
        "ST25DV04K",  # Custom embedded symbol
    ),
    (
        "U4",
        "MB85RC16",
        "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm",
        "https://www.fujitsu.com/downloads/MICRO/fma/fram/MB85RC16.pdf",
        "Memory_EEPROM:24LC16",
    ),
    (
        "U5",
        "PCF8523T",
        "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm",
        "https://www.nxp.com/docs/en/data-sheet/PCF8523.pdf",
        "Timer_RTC:PCF8523T",
    ),
    (
        "U6",
        "FDC1004",
        "Package_SON:Texas_S-PWSON-N10",
        "https://www.ti.com/lit/ds/symlink/fdc1004.pdf",
        "FDC1004",  # Custom embedded symbol
    ),
    # ── Resistors ──
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
    # ── Capacitors ──
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
    ("C22", "100nF", "Capacitor_SMD:C_0603_1608Metric", "", "Device:C_Small"),
    ("C23", "100nF", "Capacitor_SMD:C_0603_1608Metric", "", "Device:C_Small"),
    ("C24", "100nF", "Capacitor_SMD:C_0603_1608Metric", "", "Device:C_Small"),
    # ── Inductors ──
    ("L1", "10µH", "Inductor_SMD:L_Vishay_IFSC-1515AH_4x4x1.8mm", "", "Device:L_Small"),
    ("L2", "47µH", "Inductor_SMD:L_Bourns-SRN4018", "", "Device:L_Small"),
    # ── Crystal ──
    ("X1", "32.768kHz", "Crystal:Crystal_SMD_3215-2Pin_3.2x1.5mm", "", "Device:Crystal"),
    # ── Transistor ──
    ("Q1", "SI1308EDL", "Package_TO_SOT_SMD:SOT-323_SC-70", "", "Device:Q_PMOS_SGD"),
    # ── LEDs ──
    ("LED1", "Green", "LED_SMD:LED_0603_1608Metric", "", "Device:LED"),
    ("LED2", "Yellow", "LED_SMD:LED_0603_1608Metric", "", "Device:LED"),
    # ── Connectors ──
    (
        "J1",
        "SWD_2x5",
        "Connector_PinHeader_1.27mm:PinHeader_2x05_P1.27mm_Vertical_SMD",
        "",
        "Connector_Generic:Conn_02x05_Counter_Clockwise",
    ),
    (
        "J2",
        "Pressling",
        "Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical",
        "",
        "Connector_Generic:Conn_01x02",
    ),
    (
        "J3",
        "Aux_I2C",
        "Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical",
        "",
        "Connector_Generic:Conn_01x02",
    ),
    (
        "J4",
        "Sensor_In",
        "Connector_PinHeader_1.27mm:PinHeader_2x03_P1.27mm_Vertical_SMD",
        "",
        "Connector_Generic:Conn_01x03",
    ),
    # ── Supercap ──
    (
        "SC1",
        "100mF",
        "Capacitor_THT:CP_Radial_D8.0mm_P3.50mm",
        "",
        "Device:C_Polarized_Small",
    ),
    # ── TVS Diodes ──
    (
        "D1",
        "USBLC6-2P6",
        "Package_TO_SOT_SMD:SOT-666",
        "https://www.st.com/resource/en/datasheet/usblc6-2p6.pdf",
        "Device:D_TVS",
    ),
    (
        "D2",
        "PESD5V0S1UB",
        "Diode_SMD:D_SOD-523",
        "https://www.nexperia.com/packaging/SOD-523.html",
        "Device:D_TVS",
    ),
]

# ═══════════════════════════════════════════════════════════════
# Netlist
# ═══════════════════════════════════════════════════════════════

# Each net: (net_name, [(ref, pin_number), ...])
NETS = [
    (
        "GND",
        [
            ("U1", "15"), ("U1", "8"),  # STM32 VSSA
            ("U2", "1"), ("U2", "9"), ("U2", "15"), ("U2", "17"),
            ("U2", "21"), ("U2", "5"), ("U2", "7"),
            ("U3", "3"), ("U3", "4"),
            ("U6", "5"), ("U6", "9"),
            ("U4", "4"),
            ("U5", "4"),
            ("C1", "2"), ("C2", "2"), ("C3", "2"), ("C4", "2"),
            ("C5", "2"), ("C6", "2"), ("C7", "2"), ("C8", "2"),
            ("C9", "2"), ("C10", "2"),
            ("C11", "2"), ("C12", "2"), ("C13", "2"),
            ("C14", "2"), ("C15", "2"),
            ("C16", "2"), ("C17", "2"),
            ("C18", "2"), ("C19", "2"),
            ("C21", "2"), ("C22", "2"),
            ("C23", "2"), ("C24", "2"),
            ("J1", "3"),
            ("J2", "2"),
            ("J3", "2"),
            ("J4", "1"), ("J4", "2"), ("J4", "3"),
            ("LED1", "2"), ("LED2", "2"),
            ("SC1", "2"),
            ("D1", "3"), ("D1", "4"), ("D1", "6"),
            ("D2", "2"),
            ("R4", "1"),
            ("R5", "2"), ("R6", "2"), ("R8", "2"), ("R10", "2"),
            ("U4", "1"), ("U4", "2"), ("U4", "3"), ("U4", "7"),
        ],
    ),
    (
        "3.3V",
        [
            ("U1", "5"), ("U1", "16"),
            ("U2", "14"),
            ("U3", "8"),
            ("U4", "8"),
            ("U5", "8"),
            ("U6", "10"),
            ("C1", "1"), ("C2", "1"), ("C3", "1"), ("C4", "1"),
            ("C5", "1"), ("C6", "1"), ("C7", "1"), ("C8", "1"),
            ("C9", "1"), ("C10", "1"),
            ("C11", "1"), ("C12", "1"), ("C13", "1"),
            ("C14", "1"), ("C15", "1"),
            ("C19", "1"),
            ("C23", "1"), ("C24", "1"),
            ("R1", "1"), ("R2", "1"),
            ("R13", "2"),
            ("D2", "1"),
            ("L2", "2"),
            ("Q1", "2"),
            ("J1", "1"),
        ],
    ),
    (
        "V_PRESSLING",
        [("U2", "2"), ("J2", "1"), ("C21", "1"), ("L1", "1"), ("R9", "1"), ("R3", "2")],
    ),
    (
        "I2C1_SCL",
        [("U1", "17"), ("U3", "5"), ("U4", "6"), ("U5", "6"), ("U6", "7"), ("R1", "2")],
    ),
    (
        "I2C1_SDA",
        [("U1", "18"), ("U3", "6"), ("U4", "5"), ("U5", "5"), ("U6", "8"), ("R2", "2")],
    ),
    ("V_SENSE", [("U1", "6"), ("R9", "2"), ("R10", "1")]),
    ("SWDIO", [("U1", "19"), ("J1", "4"), ("R11", "1"), ("R11", "2")]),
    ("SWCLK", [("U1", "20"), ("J1", "2"), ("R12", "1"), ("R12", "2")]),
    ("NRST", [("U1", "4"), ("J1", "10"), ("C18", "1")]),
    ("LOAD_SW_GATE", [("U1", "10"), ("Q1", "1")]),
    ("NFC_IRQ", [("U1", "11"), ("U3", "7")]),
    ("RTC_INT", [("U1", "12"), ("U5", "7")]),
    ("SENSOR_RDY", [("U1", "7"), ("U6", "6")]),
    ("NFC_RF1", [("U3", "1"), ("C20", "1"), ("D1", "1")]),
    ("NFC_RF2", [("U3", "2"), ("C20", "2"), ("D1", "2")]),
    ("XTAL_IN", [("U1", "2"), ("X1", "1"), ("C16", "1")]),
    ("XTAL_OUT", [("U1", "3"), ("X1", "2"), ("C17", "1")]),
    ("CIN1", [("U6", "1"), ("J4", "1")]),
    ("CIN2", [("U6", "2"), ("J4", "2")]),
    ("SHLD1", [("U6", "3"), ("J4", "3")]),
    ("VOC_SAMP", [("U2", "3"), ("R3", "1")]),
    ("VREF_SAMP", [("U2", "4"), ("R4", "2")]),
    ("OK_HYST", [("U2", "10"), ("R6", "1")]),
    ("OK_PROG", [("U2", "11"), ("R5", "1")]),
    ("VOUT_SET", [("U2", "12"), ("R7", "2"), ("R8", "1")]),
    ("VRDIV", [("U2", "8"), ("C22", "1")]),
    ("VBAT_OK", [("U2", "13"), ("U1", "14")]),
    ("LBOOST", [("U2", "20"), ("L1", "2")]),
    ("LBUCK", [("U2", "16"), ("L2", "1")]),
    ("VSTOR", [("U2", "19"), ("SC1", "1"), ("U2", "6"), ("U2", "18"), ("U5", "3")]),
    ("LED_PWR", [("LED1", "1"), ("R13", "1"), ("Q1", "3")]),
    ("LED_STAT", [("LED2", "1"), ("R14", "1")]),
    ("MCU_LED_CTRL", [("U1", "13"), ("R14", "2")]),
    ("UART_TX", [("U1", "8"), ("J1", "8")]),
    ("UART_RX", [("U1", "9"), ("J1", "6")]),
]

# ═══════════════════════════════════════════════════════════════
# Schematic Positions (x, y in mm)
# ═══════════════════════════════════════════════════════════════

POS = {
    # Power section (left)
    "U2": (150, 200),
    "L1": (110, 300),
    "L2": (190, 300),
    "C21": (150, 350),
    "J2": (150, 400),
    "J3": (150, 550),
    "J4": (800, 750),
    "Q1": (300, 200),
    "SC1": (100, 500),
    # MCU section (center)
    "U1": (500, 200),
    "X1": (500, 100),
    "C16": (450, 100),
    "C17": (550, 100),
    "R11": (450, 250),
    "R12": (550, 250),
    "C18": (480, 300),
    # NFC section (right)
    "U3": (800, 200),
    "C20": (800, 100),
    "D1": (750, 300),
    # I2C devices (center-right)
    "U4": (700, 450),
    "U5": (700, 550),
    # Capacitance sensor (right)
    "U6": (700, 650),
    "D2": (700, 750),
    # I2C pull-ups
    "R1": (600, 400),
    "R2": (600, 450),
    # Debug connector
    "J1": (350, 600),
    # LEDs
    "LED1": (500, 550),
    "LED2": (600, 550),
    "R13": (500, 600),
    "R14": (600, 600),
    # Decoupling caps around U1 (500, 200)
    "C1": (430, 150),
    "C2": (430, 180),
    "C3": (430, 210),
    "C4": (430, 240),
    "C5": (430, 270),
    "C6": (430, 300),
    "C7": (570, 150),
    "C8": (570, 180),
    "C9": (570, 210),
    "C10": (570, 240),
    "C11": (650, 150),
    "C12": (650, 180),
    "C13": (650, 210),
    "C14": (780, 450),
    "C15": (780, 480),
    "C19": (480, 350),
    # BQ25570 programming resistors
    "R3": (300, 100),
    "R4": (300, 130),
    "R5": (300, 350),
    "R6": (300, 380),
    "R7": (300, 450),
    "R8": (300, 480),
    "R9": (300, 500),
    "R10": (300, 530),
    "C22": (400, 350),
    # Decoupling for U3 (800,200) and U6 (700,650)
    "C23": (650, 550),
    "C24": (650, 600),
}

# ═══════════════════════════════════════════════════════════════
# PCB Positions (x, y in nanometers)
# ═══════════════════════════════════════════════════════════════

PCB_POS = {
    # Connectors
    "J1": (5e6, 15e6),
    "J2": (2e6, 2e6),
    "J3": (2e6, 5e6),
    "J4": (22e6, 17e6),
    # I2C pull-ups (top-right area)
    "R1": (20e6, 8e6),
    "R2": (21e6, 8e6),
    # BQ25570 programming resistors (left side)
    "R5": (4e6, 8e6),
    "R6": (5e6, 8e6),
    "R7": (6e6, 8e6),
    "R8": (7e6, 8e6),
    "R9": (4e6, 6e6),
    "R10": (5e6, 6e6),
    "R3": (4e6, 5e6),
    "R4": (5e6, 5e6),
    # Debug resistors
    "R11": (10e6, 15e6),
    "R12": (11e6, 15e6),
    "R13": (12e6, 2e6),
    "R14": (13e6, 2e6),
    # Decoupling caps around U1 (12,10)
    "C1": (10.5e6, 8.5e6),
    "C2": (11.5e6, 8.5e6),
    "C3": (12.5e6, 8.5e6),
    "C4": (13.5e6, 8.5e6),
    "C5": (14e6, 9.5e6),
    "C6": (14e6, 10.5e6),
    "C7": (10e6, 9e6),
    "C8": (10e6, 10e6),
    "C9": (10e6, 11e6),
    "C10": (14e6, 11.5e6),
    "C11": (11e6, 11.8e6),
    "C12": (13e6, 11.8e6),
    "C13": (14e6, 7.5e6),
    # Power caps
    "C21": (5e6, 9e6),
    "C14": (5e6, 4e6),
    "C15": (6e6, 4e6),
    "C16": (15e6, 14e6),
    "C17": (16e6, 14e6),
    "C18": (14e6, 13e6),
    "C19": (15e6, 13e6),
    "C20": (25e6, 10e6),
    "C22": (6e6, 6e6),
    # Decoupling for U3 (24,10) and U6 (22,14)
    "C23": (23e6, 11e6),
    "C24": (21e6, 15e6),
    # Inductors
    "L1": (3e6, 6e6),
    "L2": (4e6, 7e6),
    # Transistor
    "Q1": (8e6, 12e6),
    # LEDs
    "LED1": (12e6, 1e6),
    "LED2": (14e6, 1e6),
    # ICs
    "U1": (12e6, 10e6),
    "U2": (4e6, 10e6),
    "U3": (24e6, 10e6),
    "U4": (18e6, 12e6),
    "U5": (18e6, 8e6),
    "U6": (22e6, 14e6),
    # Crystal
    "X1": (14e6, 12e6),
    # Supercap
    "SC1": (8e6, 4e6),
    # TVS diodes
    "D1": (26e6, 10e6),
    "D2": (8e6, 14e6),
}

# ═══════════════════════════════════════════════════════════════
# Custom Symbol Definitions (KiCad 6 S-expression format)
# ═══════════════════════════════════════════════════════════════

CUSTOM_SYMBOLS = {
    "ST25DV04K": """(symbol "ST25DV04K" (pin_names (offset 0) hide) (in_bom yes) (on_board yes)
  (property "Reference" "U" (id 0) (at 7.62 2.54 0)
    (effects (font (size 1.27 1.27)) (justify left))
  )
  (property "Value" "ST25DV04K" (id 1) (at 7.62 0 0)
    (effects (font (size 1.27 1.27)) (justify left))
  )
  (symbol "ST25DV04K_0_1"
    (rectangle (start -6.35 -5.08) (end 6.35 5.08)
      (stroke (width 0.254) (type default) (color 0 0 0 0))
      (fill (type background))
    )
    (pin passive line (at -8.89 -2.54 0) (length 2.54)
      (name "RF_M" (effects (font (size 1.27 1.27))))
      (number "1" (effects (font (size 1.27 1.27))))
    )
    (pin passive line (at -8.89 0 0) (length 2.54)
      (name "RF_E1" (effects (font (size 1.27 1.27))))
      (number "2" (effects (font (size 1.27 1.27))))
    )
    (pin power_in line (at -8.89 2.54 0) (length 2.54)
      (name "VSS" (effects (font (size 1.27 1.27))))
      (number "3" (effects (font (size 1.27 1.27))))
    )
    (pin power_in line (at -8.89 5.08 0) (length 2.54)
      (name "VSS" (effects (font (size 1.27 1.27))))
      (number "4" (effects (font (size 1.27 1.27))))
    )
    (pin input line (at 8.89 -2.54 180) (length 2.54)
      (name "SCL" (effects (font (size 1.27 1.27))))
      (number "5" (effects (font (size 1.27 1.27))))
    )
    (pin bidirectional line (at 8.89 0 180) (length 2.54)
      (name "SDA" (effects (font (size 1.27 1.27))))
      (number "6" (effects (font (size 1.27 1.27))))
    )
    (pin open_collector line (at 8.89 2.54 180) (length 2.54)
      (name "IRQ" (effects (font (size 1.27 1.27))))
      (number "7" (effects (font (size 1.27 1.27))))
    )
    (pin power_in line (at 8.89 5.08 180) (length 2.54)
      (name "VDD" (effects (font (size 1.27 1.27))))
      (number "8" (effects (font (size 1.27 1.27))))
    )
  )
)""",
    "FDC1004": """(symbol "FDC1004" (pin_names (offset 0) hide) (in_bom yes) (on_board yes)
  (property "Reference" "U" (id 0) (at 7.62 2.54 0)
    (effects (font (size 1.27 1.27)) (justify left))
  )
  (property "Value" "FDC1004" (id 1) (at 7.62 0 0)
    (effects (font (size 1.27 1.27)) (justify left))
  )
  (symbol "FDC1004_0_1"
    (rectangle (start -6.35 -6.35) (end 6.35 6.35)
      (stroke (width 0.254) (type default) (color 0 0 0 0))
      (fill (type background))
    )
    (pin passive line (at -8.89 -5.08 0) (length 2.54)
      (name "CIN1" (effects (font (size 1.27 1.27))))
      (number "1" (effects (font (size 1.27 1.27))))
    )
    (pin passive line (at -8.89 -2.54 0) (length 2.54)
      (name "CIN2" (effects (font (size 1.27 1.27))))
      (number "2" (effects (font (size 1.27 1.27))))
    )
    (pin passive line (at -8.89 0 0) (length 2.54)
      (name "SHLD1" (effects (font (size 1.27 1.27))))
      (number "3" (effects (font (size 1.27 1.27))))
    )
    (pin passive line (at -8.89 2.54 0) (length 2.54)
      (name "CIN3" (effects (font (size 1.27 1.27))))
      (number "4" (effects (font (size 1.27 1.27))))
    )
    (pin power_in line (at -8.89 5.08 0) (length 2.54)
      (name "VSS" (effects (font (size 1.27 1.27))))
      (number "5" (effects (font (size 1.27 1.27))))
    )
    (pin open_collector line (at 8.89 -5.08 180) (length 2.54)
      (name "RDY" (effects (font (size 1.27 1.27))))
      (number "6" (effects (font (size 1.27 1.27))))
    )
    (pin input line (at 8.89 -2.54 180) (length 2.54)
      (name "SCL" (effects (font (size 1.27 1.27))))
      (number "7" (effects (font (size 1.27 1.27))))
    )
    (pin bidirectional line (at 8.89 0 180) (length 2.54)
      (name "SDA" (effects (font (size 1.27 1.27))))
      (number "8" (effects (font (size 1.27 1.27))))
    )
    (pin input line (at 8.89 2.54 180) (length 2.54)
      (name "ADDR" (effects (font (size 1.27 1.27))))
      (number "9" (effects (font (size 1.27 1.27))))
    )
    (pin power_in line (at 8.89 5.08 180) (length 2.54)
      (name "VDD" (effects (font (size 1.27 1.27))))
      (number "10" (effects (font (size 1.27 1.27))))
    )
  )
)""",
}

# ═══════════════════════════════════════════════════════════════
# Generation helpers
# ═══════════════════════════════════════════════════════════════

def _p(**kwargs):
    """Create a property list for an S-exp with key-value pairs.
    
    Usage: _p(at=[x, y, rot], name=value) -> [['at', x, y, rot], ['name', value]]
    """
    items = []
    for k, v in kwargs.items():
        if v is None:
            continue
        if isinstance(v, list):
            items.append([k.replace('_', '')] + v)
        else:
            items.append([k.replace('_', ''), v])
    return items


def gen_symbol_sexp(ref, value, footprint, datasheet, kicad_symbol):
    """Generate a symbol instance S-expression for the schematic."""
    uid = det_uuid(ref)
    if ":" in kicad_symbol:
        lib_id = kicad_symbol
    else:
        lib_id = kicad_symbol
    x, y = POS.get(ref, (500, 400))
    
    # Build symbol S-expression
    sym = Sexp([
        "symbol",
        ["lib_id", lib_id],
        ["at", x, y, 0],
        ["unit", 1],
        ["in_bom", "yes"],
        ["on_board", "yes"],
        ["uuid", uid],
    ])
    
    # Properties
    sym.append(Sexp([
        "property", "Reference", ref,
        ["at", x, y, 0],
        ["effects", ["font", ["size", 1.27, 1.27]], ["justify", "left"]],
    ]))
    sym.append(Sexp([
        "property", "Value", value,
        ["at", x, y - 2.54, 0],
        ["effects", ["font", ["size", 1.27, 1.27]], ["justify", "left"]],
    ]))
    sym.append(Sexp([
        "property", "Footprint", footprint,
        ["at", x, y - 5.08, 0],
        ["effects", ["font", ["size", 0.5, 0.5]], ["hide", "yes"]],
    ]))
    sym.append(Sexp([
        "property", "Datasheet", datasheet,
        ["at", x, y - 7.62, 0],
        ["effects", ["font", ["size", 0.5, 0.5]], ["hide", "yes"]],
    ]))
    
    return sym


def gen_power_symbol_sexp(text, x, y, ref_suffix=""):
    """Generate a power symbol instance (GND, +3.3V)."""
    uid = det_uuid(f"power_{text}_{x}_{y}_{ref_suffix}")
    pwr_ref = f"#PWR{abs(hash(uid)) % 1000:03d}"
    
    net_to_kicad = {
        "GND": "power:GND",
        "+3.3V": "power:+3.3V",
        "V_PRESSLING": "power:VCC",
    }
    lib_id = net_to_kicad.get(text, f"power:{text}")
    
    sym = Sexp([
        "symbol",
        ["lib_id", lib_id],
        ["at", x, y, 0],
        ["unit", 1],
        ["in_bom", "no"],
        ["on_board", "yes"],
        ["uuid", uid],
    ])
    
    sym.append(Sexp([
        "property", "Reference", pwr_ref,
        ["at", x, y, 0],
        ["effects", ["font", ["size", 1.27, 1.27]], ["hide", "yes"]],
    ]))
    sym.append(Sexp([
        "property", "Value", text,
        ["at", x, y - 2.54, 0],
        ["effects", ["font", ["size", 1.27, 1.27]]],
    ]))
    
    return sym


def gen_label_sexp(text, x, y):
    """Generate a global label for a net."""
    uid = det_uuid(f"glabel_{text}_{x}_{y}")
    return Sexp([
        "label", text,
        ["at", x, y, 0],
        ["effects", ["font", ["size", 1.27, 1.27]]],
        ["uuid", uid],
    ])


def gen_bus_entry_sexp(text, x, y):
    """Generate a bus entry (used for net connectivity symbols)."""
    uid = det_uuid(f"bentry_{text}_{x}_{y}")
    return Sexp([
        "symbol",
        ["lib_id", "Device:Conn_01x01"],
        ["at", x, y, 0],
        ["unit", 1],
        ["in_bom", "no"],
        ["on_board", "yes"],
        ["uuid", uid],
    ])


# ═══════════════════════════════════════════════════════════════
# Schematic Generation
# ═══════════════════════════════════════════════════════════════

def generate_schematic_sexp():
    """Generate the complete schematic as an Sexp tree."""
    
    root = Sexp([
        "kicad_sch",
        ["version", KICAD_VERSION],
        ["generator", "mykovolt_gen"],
    ])
    
    # ── Add all component symbols ──
    for comp in COMPONENTS:
        root.append(gen_symbol_sexp(*comp))
    
    # ── Add global labels for each net connection ──
    used = set()
    for net_name, connections in NETS:
        for ref, pin in connections:
            if ref not in POS:
                continue
            bx, by = POS[ref]
            # Offset labels to avoid overlap
            ly = int(by) + (int(pin) * 50) % 300 - 150
            lx = bx + 15
            key = f"{net_name}_{lx}_{ly}"
            if key not in used:
                used.add(key)
                root.append(gen_label_sexp(net_name, lx, ly))
    
    # ── Add power symbols near each component ──
    for ref, _, _, _, _ in COMPONENTS:
        if ref in POS:
            x, y = POS[ref]
            root.append(gen_power_symbol_sexp("GND", x, y + 15, ref))
            root.append(gen_power_symbol_sexp("+3.3V", x, y - 15, ref))
    
    # ── lib_symbols: embedded definitions for custom parts (ST25DV04K, FDC1004) ──
    # We build these as a string section and insert directly into the output
    # since simp_sexp cannot parse raw S-expression strings.
    lib_syms = []
    for kicad_symbol_name, sym_text in CUSTOM_SYMBOLS.items():
        lib_syms.append(sym_text)
    if lib_syms:
        lib_block = "    (lib_symbols\n"
        for ls in lib_syms:
            # Indent each line of the custom symbol definition
            for line in ls.strip().split('\n'):
                lib_block += f"      {line}\n"
        lib_block += "    )"
        root.append(lib_block)
    
    # ── Sheet instances and symbol instances (required by KiCad 6) ──
    root.append(Sexp(["sheet_instances"]))
    root.append(Sexp(["symbol_instances"]))
    
    return root


def generate_schematic_string():
    """Fallback: generate schematic as a string (when simp_sexp not available)."""
    lines = [
        f'(kicad_sch (version {KICAD_VERSION}) (generator mykovolt_gen)'
    ]
    
    # Generate component symbols
    for ref, value, footprint, datasheet, kicad_symbol in COMPONENTS:
        uid = det_uuid(ref)
        if ":" in kicad_symbol:
            lib_id = kicad_symbol
        else:
            lib_id = kicad_symbol
        x, y = POS.get(ref, (500, 400))
        
        lines.append(f'  (symbol "{uid}" (in_bom yes) (on_board yes)')
        lines.append(f'    (property "Reference" "{ref}" (id 0) (at {x} {y} 0)')
        lines.append(f'      (effects (font (size 1.27 1.27)) (justify left))')
        lines.append(f'    )')
        lines.append(f'    (property "Value" "{value}" (id 1) (at {x} {y - 2.54} 0)')
        lines.append(f'      (effects (font (size 1.27 1.27)) (justify left))')
        lines.append(f'    )')
        lines.append(f'    (property "Footprint" "{footprint}" (id 2) (at {x} {y - 5.08} 0)')
        lines.append(f'      (effects (font (size 0.5 0.5)) hide)')
        lines.append(f'    )')
        lines.append(f'    (property "Datasheet" "{datasheet}" (id 3) (at {x} {y - 7.62} 0)')
        lines.append(f'      (effects (font (size 0.5 0.5)) hide)')
        lines.append(f'    )')
        if ":" not in kicad_symbol and kicad_symbol in CUSTOM_SYMBOLS:
            lines.append(f'    (lib_symbols')
            for cs_line in CUSTOM_SYMBOLS[kicad_symbol].split('\n'):
                lines.append(f'      {cs_line}')
            lines.append(f'    )')
        else:
            lines.append(f'    (lib_symbols)')
        lines.append(f'    (lib_id "{lib_id}")')
        lines.append(f'  )')
    
    # Generate global labels for net connections
    used = set()
    for net_name, connections in NETS:
        for ref, pin in connections:
            if ref not in POS:
                continue
            bx, by = POS[ref]
            ly = int(by) + (int(pin) * 50) % 300 - 150
            lx = bx + 15
            key = f"{net_name}_{lx}_{ly}"
            if key not in used:
                used.add(key)
                uid = det_uuid(f"glabel_{net_name}_{lx}_{ly}")
                lines.append(f'  (symbol "{uid}" (in_bom no) (on_board yes)')
                lines.append(f'    (property "Reference" "#FLG" (id 0) (at {lx} {ly} 0)')
                lines.append(f'      (effects (font (size 1.27 1.27)) hide)')
                lines.append(f'    )')
                lines.append(f'    (property "Value" "{net_name}" (id 1) (at {lx} {ly - 2.54} 0)')
                lines.append(f'      (effects (font (size 1.27 1.27)))')
                lines.append(f'    )')
                lines.append(f'    (property "Symbol" "label" (id 2) (at 0 0 0)')
                lines.append(f'      (effects (font (size 1.27 1.27)) hide)')
                lines.append(f'    )')
                lines.append(f'    (lib_symbols)')
                lines.append(f'    (lib_id "Device:L_Small")')
                lines.append(f'  )')
    
    # Power symbols near each component
    for ref, _, _, _, _ in COMPONENTS:
        if ref in POS:
            x, y = POS[ref]
            for pwr_name, dy in [("GND", 15), ("+3.3V", -15)]:
                uid = det_uuid(f"power_{pwr_name}_{x}_{y}_{ref}")
                pwr_ref = f"#PWR{abs(hash(uid)) % 1000:03d}"
                net_map = {"GND": "power:GND", "+3.3V": "power:+3.3V"}
                lib_id = net_map.get(pwr_name, f"power:{pwr_name}")
                lines.append(f'  (symbol "{uid}" (power (in_bom no) (on_board yes))')
                lines.append(f'    (property "Reference" "#PWR" (id 0) (at {x} {y} 0)')
                lines.append(f'      (effects (font (size 1.27 1.27)) hide)')
                lines.append(f'    )')
                lines.append(f'    (property "Value" "{pwr_name}" (id 1) (at {x} {y - 2.54} 0)')
                lines.append(f'      (effects (font (size 1.27 1.27)))')
                lines.append(f'    )')
                lines.append(f'    (lib_symbols)')
                lines.append(f'    (lib_id "{lib_id}")')
                lines.append(f'  )')
    
    lines.append("  (sheet_instances)")
    lines.append("  (symbol_instances)")
    lines.append(")")
    
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# PCB Generation
# ═══════════════════════════════════════════════════════════════

def generate_pcb_pcbnew():
    """Generate PCB using the pcbnew API (KiCad 6).
    
    Sets up a 4-layer board: F.Cu, In1.Cu (GND), In2.Cu (PWR), B.Cu.
    Falls back to string-based generation if pcbnew fails.
    """
    import pcbnew as pn
    board = pn.BOARD()
    
    # Board dimensions (nanometers)
    w, h = int(30e6), int(20e6)
    
    # ── Configure 4-layer stackup ──
    board.SetCopperLayerCount(4)
    
    # Enable all required layers
    enabled = pn.LSET()
    for layer in [pn.F_Cu, pn.In1_Cu, pn.In2_Cu, pn.B_Cu,
                   pn.F_SilkS, pn.B_SilkS,
                   pn.F_Mask, pn.B_Mask,
                   pn.F_Paste, pn.B_Paste,
                   pn.Edge_Cuts,
                   pn.F_Fab, pn.B_Fab,
                   pn.F_CrtYd, pn.B_CrtYd]:
        enabled.AddLayer(layer)
    board.SetEnabledLayers(enabled)
    
    # ── Create board outline from 4 edge segments on Edge.Cuts ──
    corners = [(0, 0), (w, 0), (w, h), (0, h)]
    for i in range(4):
        x1, y1 = corners[i]
        x2, y2 = corners[(i + 1) % 4]
        edge = pn.PCB_SHAPE(board)
        edge.SetShape(pn.SHAPE_T_SEGMENT)
        edge.SetLayer(pn.Edge_Cuts)
        edge.SetStart(pn.wxPoint(x1, y1))
        edge.SetEnd(pn.wxPoint(x2, y2))
        edge.SetWidth(100000)  # 0.1mm
        board.Add(edge)
    
    # ── Silkscreen text ──
    cx, cy = w // 2, h // 2
    
    text = pn.PCB_TEXT(board)
    text.SetText(f"MykoVolt DevKit v{VERSION}")
    text.SetLayer(pn.F_SilkS)
    text.SetPosition(pn.wxPoint(cx, cy + int(2e6)))
    text.SetTextSize(pn.wxSize(1000000, 1000000))
    text.SetTextThickness(150000)
    board.Add(text)
    
    text2 = pn.PCB_TEXT(board)
    text2.SetText("30x20mm 4L ENIG RevA")
    text2.SetLayer(pn.F_SilkS)
    text2.SetPosition(pn.wxPoint(cx, cy + int(3.5e6)))
    text2.SetTextSize(pn.wxSize(800000, 800000))
    text2.SetTextThickness(120000)
    board.Add(text2)
    
    # ── Create nets and build netcode map ──
    net_names = sorted(set(n[0] for n in NETS))
    netcode_map = {}  # net_name -> netcode
    for i, name in enumerate(net_names):
        netcode = i + 1
        net = pn.NETINFO_ITEM(board, name, netcode)
        board.Add(net)
        netcode_map[name] = netcode
    
    # ── Place footprints with pad net assignments ──
    # Build a lookup: ref -> { pin_num -> net_name }
    ref_nets = {}  # ref -> { pin -> net_name }
    for net_name, connections in NETS:
        for ref, pin in connections:
            if ref not in ref_nets:
                ref_nets[ref] = {}
            ref_nets[ref][pin] = net_name
    
    for ref, value, footprint, _, _ in COMPONENTS:
        if ref not in PCB_POS:
            continue
        x_nm, y_nm = PCB_POS[ref]
        
        # Parse footprint into library and name
        fp_path = "/usr/share/kicad/footprints"
        if ":" in footprint:
            lib, fp_name = footprint.split(":", 1)
            fp = pn.FootprintLoad(f"{fp_path}/{lib}.pretty", fp_name)
        else:
            fp = pn.FootprintLoad(fp_path, footprint)
        
        if fp is None:
            print(f"    ⚠ Cannot load '{footprint}', creating placeholder for {ref}")
            fp = pn.FOOTPRINT(board)
            fp.SetReference(ref)
            fp.SetValue(value)
            pad = pn.PAD(fp)
            pad.SetSize(pn.wxSize(500000, 500000))
            pad.SetPosition(pn.wxPoint(0, 0))
            pad.SetLayerSet(pn.LSET.AllCuMask())
            fp.Add(pad)
        else:
            fp.SetReference(ref)
            fp.SetValue(value)
        
        fp.SetPosition(pn.wxPoint(int(x_nm), int(y_nm)))
        fp.SetOrientation(0)
        fp.Reference().SetText(ref)
        fp.Value().SetText(value)
        
        # Assign nets to pads based on netlist
        if ref in ref_nets:
            pin_map = ref_nets[ref]
            for pad in fp.Pads():
                pad_num = pad.GetNumber()
                if pad_num in pin_map:
                    net_name = pin_map[pad_num]
                    if net_name in netcode_map:
                        pad.SetNetCode(netcode_map[net_name])
        
        board.Add(fp)
    
    # ── Add copper zones ──
    # Build zone outline from board edges (slightly inset)
    inset = int(0.3e6)  # 0.3mm clearance from edge
    zone_corners = [
        pn.wxPoint(inset, inset),
        pn.wxPoint(w - inset, inset),
        pn.wxPoint(w - inset, h - inset),
        pn.wxPoint(inset, h - inset),
    ]
    
    # Helper to create a zone (KiCad 6 API)
    def add_zone(layer, net_name, priority=0):
        zone = pn.ZONE(board)
        zone.SetLayer(layer)
        zone.SetNetCode(netcode_map.get(net_name, 0))
        zone.SetPriority(priority)
        zone.SetIslandRemovalMode(pn.ISLAND_REMOVAL_MODE_AREA)
        zone.SetMinIslandArea(100000000)  # 100mm²
        zone.SetCornerSmoothingType(pn.ZONE_SETTINGS.SMOOTHING_FILLET)
        zone.SetCornerRadius(500000)  # 0.5mm
        zone.SetFillMode(pn.ZONE_FILL_MODE_POLYGONS)
        
        # Build zone outline using AppendCorner (KiCad 6 compatible)
        for pt in zone_corners:
            zone.AppendCorner(pn.wxPoint(pt.x, pt.y), -1)  # -1 = no hole
        
        board.Add(zone)
        return zone
    
    # GND pour on In1.Cu (inner layer 1)
    if "GND" in netcode_map:
        add_zone(pn.In1_Cu, "GND", 0)
    
    # 3.3V pour on In2.Cu (inner layer 2)
    if "3.3V" in netcode_map:
        add_zone(pn.In2_Cu, "3.3V", 0)
    
    # ── NFC Antenna Coil (rectangular spiral on F.Cu) ──
    # 13.56 MHz, ~2.9 µH target, 4 turns, 0.3mm trace/space
    # Placed on right side of board near U3 (ST25DV04K)
    _add_nfc_antenna(board, pn, netcode_map)
    
    # ── GND keepout under antenna on In1.Cu ──
    # Prevent GND pour from coupling to antenna
    _add_antenna_keepout(board, pn)
    
    # ── Interdigital Sensor Electrodes (B.Cu) ──
    # Connected to FDC1004 CIN1 and CIN2 via J4
    _add_sensor_electrodes(board, pn, netcode_map)
    
    # ── Save ──
    pcb_path = os.path.join(PROJECT_DIR, f"{BOARD_NAME}.kicad_pcb")
    board.Save(pcb_path)
    return pcb_path


def _add_nfc_antenna(board, pn, netcode_map):
    """Add NFC antenna coil as a rectangular spiral on F.Cu.
    
    4-turn rectangular spiral, 0.3mm trace, 0.3mm spacing.
    Outer dimensions ~18×12mm, placed right of U3.
    Connected to NFC_RF1 and NFC_RF2 nets.
    """
    # Antenna center (right side of board, aligned with U3)
    cx, cy = int(25e6), int(10e6)  # 25mm, 10mm
    
    # Spiral parameters
    turns = 4
    trace_w = int(0.3e6)    # 0.3mm
    spacing = int(0.3e6)    # 0.3mm
    outer_w = int(14e6)     # 14mm outer width
    outer_h = int(10e6)     # 10mm outer height
    
    # Get netcodes
    rf1_net = netcode_map.get("NFC_RF1", 0)
    rf2_net = netcode_map.get("NFC_RF2", 0)
    
    # Build spiral segments going inward
    # Start from outer corner, spiral inward turn by turn
    x, y = cx - outer_w // 2, cy - outer_h // 2
    w, h = outer_w, outer_h
    
    segs = []  # (x1, y1, x2, y2, netcode)
    
    for turn in range(turns):
        # Top edge: left → right
        segs.append((x, y, x + w, y, 0))
        # Right edge: top → bottom
        segs.append((x + w, y, x + w, y + h, 0))
        # Bottom edge: right → left
        segs.append((x + w, y + h, x, y + h, 0))
        # Left edge: bottom → top (with inset for next turn)
        inset = (trace_w + spacing) * (turn + 1)
        segs.append((x, y + h, x, y + inset, 0))
        
        # Shrink for next turn
        x += trace_w + spacing
        y += trace_w + spacing
        w -= 2 * (trace_w + spacing)
        h -= 2 * (trace_w + spacing)
    
    # Create tracks for spiral
    # First segment is NFC_RF1, last is NFC_RF2
    if segs:
        # First segment = NFC_RF1
        x1, y1, x2, y2, _ = segs[0]
        _add_track(board, pn, x1, y1, x2, y2, trace_w, pn.F_Cu, rf1_net)
        
        # Middle segments = antenna (no net — they're the coil itself)
        for x1, y1, x2, y2, _ in segs[1:-1]:
            _add_track(board, pn, x1, y1, x2, y2, trace_w, pn.F_Cu, 0)
        
        # Last segment = NFC_RF2 (innermost turn's left edge from bottom to feed)
        if len(segs) > 1:
            x1, y1, x2, y2, _ = segs[-1]
            # Route to U3 feed point (near U3 pin 1/2 at right side)
            _add_track(board, pn, x1, y2, int(26.5e6), y2, trace_w, pn.F_Cu, 0)
    
    # ── Antenna matching: connect NFC_RF1 and NFC_RF2 to U3 via C20 position ──
    # Feed lines from spiral ends to U3 pins through C20
    c20_pos = PCB_POS.get("C20", (int(25e6), int(10e6)))
    d1_pos = PCB_POS.get("D1", (int(26e6), int(10e6)))
    
    # NFC_RF1: C20-1 → U3-1 (through D1-1 for ESD)
    _add_track(board, pn, c20_pos[0] - int(1e6), c20_pos[1], c20_pos[0], c20_pos[1],
               trace_w, pn.F_Cu, rf1_net)
    
    # Add silkscreen label
    lbl = pn.PCB_TEXT(board)
    lbl.SetText("NFC ANT")
    lbl.SetLayer(pn.F_SilkS)
    lbl.SetPosition(pn.wxPoint(cx, cy + int(7e6)))
    lbl.SetTextSize(pn.wxSize(600000, 600000))
    lbl.SetTextThickness(100000)
    board.Add(lbl)


def _add_antenna_keepout(board, pn):
    """Add a GND keepout zone under the NFC antenna on In1.Cu.
    
    This prevents the GND pour from coupling to the antenna coil.
    """
    cx, cy = int(25e6), int(10e6)
    kw, kh = int(15e6), int(11e6)  # Slightly larger than antenna
    
    zone = pn.ZONE(board)
    zone.SetLayer(pn.In1_Cu)
    zone.SetNetCode(0)  # No net — keepout zone
    zone.SetIsRuleArea(True)  # This makes it a keepout
    zone.SetDoNotAllowCopperPour(True)
    zone.SetDoNotAllowTracks(True)
    zone.SetDoNotAllowVias(True)
    zone.SetDoNotAllowPads(True)
    zone.SetPriority(1)
    
    corners = [
        pn.wxPoint(cx - kw // 2, cy - kh // 2),
        pn.wxPoint(cx + kw // 2, cy - kh // 2),
        pn.wxPoint(cx + kw // 2, cy + kh // 2),
        pn.wxPoint(cx - kw // 2, cy + kh // 2),
    ]
    for pt in corners:
        zone.AppendCorner(pt, -1)
    
    board.Add(zone)


def _add_sensor_electrodes(board, pn, netcode_map):
    """Add interdigital sensor electrodes on B.Cu.
    
    Two interlocking comb patterns forming a capacitive sensor.
    CIN1 (measurement channel) and CIN2 (reference/compensation).
    SHLD1 guard ring surrounds the electrodes on B.Cu.
    
    Connected to FDC1004 via J4 connector.
    """
    # Electrode position: bottom-center of board (aligns with J4 at 22,17)
    ex, ey = int(15e6), int(17e6)
    
    # Electrode geometry
    finger_w = int(0.3e6)     # Finger width
    finger_gap = int(0.3e6)   # Gap between fingers
    finger_len = int(3e6)     # Finger length (3mm)
    num_fingers = 10           # Fingers per side
    total_w = num_fingers * (finger_w + finger_gap) + finger_w
    
    # Get netcodes
    cin1_net = netcode_map.get("CIN1", 0)
    cin2_net = netcode_map.get("CIN2", 0)
    shld_net = netcode_map.get("SHLD1", 0)
    
    # ── SHLD1 Guard Ring (rectangle around electrodes) ──
    guard_margin = int(0.5e6)
    guard_w = total_w + 2 * guard_margin
    guard_h = finger_len + 2 * guard_margin
    guard_x = ex - guard_w // 2
    guard_y = ey - guard_h // 2
    
    # Draw guard ring as 4 segments
    _add_track(board, pn, guard_x, guard_y, guard_x + guard_w, guard_y,
               int(0.2e6), pn.B_Cu, shld_net)
    _add_track(board, pn, guard_x + guard_w, guard_y, guard_x + guard_w, guard_y + guard_h,
               int(0.2e6), pn.B_Cu, shld_net)
    _add_track(board, pn, guard_x + guard_w, guard_y + guard_h, guard_x, guard_y + guard_h,
               int(0.2e6), pn.B_Cu, shld_net)
    _add_track(board, pn, guard_x, guard_y + guard_h, guard_x, guard_y,
               int(0.2e6), pn.B_Cu, shld_net)
    
    # ── CIN1 Fingers (left comb, connected to J4/CIN1) ──
    start_x = ex - total_w // 2
    for i in range(num_fingers):
        fx = start_x + i * (finger_w + finger_gap)
        fy_start = ey - finger_len // 2
        fy_end = ey
        _add_track(board, pn, fx, fy_start, fx, fy_end, finger_w, pn.B_Cu, cin1_net)
        # Bus bar at top
        if i == 0:
            _add_track(board, pn, fx, fy_start, fx + finger_w, fy_start, finger_w, pn.B_Cu, cin1_net)
    
    # ── CIN2 Fingers (right comb, interlocking, connected to J4/CIN2) ──
    for i in range(num_fingers):
        fx = start_x + i * (finger_w + finger_gap) + finger_w + finger_gap // 2
        if i == num_fingers - 1:
            break
        fy_start = ey
        fy_end = ey + finger_len // 2
        _add_track(board, pn, fx, fy_start, fx, fy_end, finger_w, pn.B_Cu, cin2_net)
        # Bus bar at bottom
        if i == num_fingers - 2:
            _add_track(board, pn, fx - finger_w - finger_gap, fy_end, fx + finger_w, fy_end,
                       finger_w, pn.B_Cu, cin2_net)
    
    # ── Route CIN1, CIN2, SHLD1 from electrodes to J4 ──
    j4_pos = PCB_POS.get("J4", (int(22e6), int(17e6)))
    _add_track(board, pn, ex, ey, j4_pos[0] - int(1e6), j4_pos[1],
               int(0.2e6), pn.B_Cu, cin1_net)
    _add_track(board, pn, ex + int(1e6), ey, j4_pos[0], j4_pos[1],
               int(0.2e6), pn.B_Cu, cin2_net)
    
    # Silkscreen label
    lbl = pn.PCB_TEXT(board)
    lbl.SetText("SENSOR")
    lbl.SetLayer(pn.B_SilkS)
    lbl.SetPosition(pn.wxPoint(ex, ey + int(4e6)))
    lbl.SetTextSize(pn.wxSize(600000, 600000))
    lbl.SetTextThickness(100000)
    board.Add(lbl)


def _add_track(board, pn, x1, y1, x2, y2, width, layer, netcode=0):
    """Helper to add a PCB track segment."""
    track = pn.PCB_TRACK(board)
    track.SetStart(pn.wxPoint(int(x1), int(y1)))
    track.SetEnd(pn.wxPoint(int(x2), int(y2)))
    track.SetWidth(int(width))
    track.SetLayer(layer)
    if netcode > 0:
        track.SetNetCode(netcode)
    board.Add(track)
    return track


def generate_pcb_string():
    """Fallback: generate PCB using S-expression string (when pcbnew not available)."""
    w, h = 30e6, 20e6
    uid_board = det_uuid("board_outline")
    net_names = sorted(set(n[0] for n in NETS))
    pcb_nets = "\n".join(f'  (net {i} "{name}")' for i, name in enumerate(net_names))
    
    s = f'(kicad_pcb (version {KICAD_VERSION}) (generator mykovolt_gen)\n'
    s += "  (general\n    (thickness 0.8)\n  )\n"
    s += '  (paper "A4")\n'
    s += "  (layers\n"
    s += '    (0 "F.Cu" signal) (1 "In1.Cu" signal) (2 "In2.Cu" signal) (31 "B.Cu" signal)\n'
    s += '    (32 "B.Adhes" user "B.Adhesive") (33 "F.Adhes" user "F.Adhesive")\n'
    s += '    (34 "B.Paste" user) (35 "F.Paste" user)\n'
    s += '    (36 "B.SilkS" user "B.Silkscreen") (37 "F.SilkS" user "F.Silkscreen")\n'
    s += '    (38 "B.Mask" user) (39 "F.Mask" user)\n'
    s += '    (40 "Dwgs.User" user "User.Drawings") (41 "Cmts.User" user "User.Comments")\n'
    s += '    (42 "Eco1.User" user "User.Eco1") (43 "Eco2.User" user "User.Eco2")\n'
    s += '    (44 "Edge.Cuts" user)\n'
    s += '    (45 "Margin" user)\n'
    s += '    (46 "B.CrtYd" user) (47 "F.CrtYd" user) (48 "B.Fab" user) (49 "F.Fab" user)\n'
    s += "  )\n"
    s += "  (setup\n"
    s += "    (stackup\n"
    s += '      (layer "F.SilkS" (type "Top Silk Screen") (color "White"))\n'
    s += '      (layer "F.Paste" (type "Top Solder Paste"))\n'
    s += '      (layer "F.Mask" (type "Top Solder Mask") (color "Green") (thickness 0.01))\n'
    s += '      (layer "F.Cu" (type "copper") (thickness 0.035))\n'
    s += '      (layer "dielectric 1" (type "prepreg") (thickness 0.2) (material "FR-4") (epsilon_r 4.5) (loss_tangent 0.02))\n'
    s += '      (layer "In1.Cu" (type "copper") (thickness 0.035))\n'
    s += '      (layer "dielectric 2" (type "core") (thickness 0.4) (material "FR-4") (epsilon_r 4.5) (loss_tangent 0.02))\n'
    s += '      (layer "In2.Cu" (type "copper") (thickness 0.035))\n'
    s += '      (layer "dielectric 3" (type "prepreg") (thickness 0.2) (material "FR-4") (epsilon_r 4.5) (loss_tangent 0.02))\n'
    s += '      (layer "B.Cu" (type "copper") (thickness 0.035))\n'
    s += '      (layer "B.Mask" (type "Bottom Solder Mask") (color "Green") (thickness 0.01))\n'
    s += '      (layer "B.Paste" (type "Bottom Solder Paste"))\n'
    s += '      (layer "B.SilkS" (type "Bottom Silk Screen") (color "White"))\n'
    s += '      (copper_finish "None")\n'
    s += '      (dielectric_constraints no)\n'
    s += "    )\n"
    s += "    (pad_to_mask_clearance 0)\n"
    s += "  )\n"
    s += f"{pcb_nets}\n"
    s += f'  (footprint "" (layer "F.Cu") (tedit 0) (tstamp "{uid_board}")\n'
    s += "    (at 0 0 0)\n"
    s += "    (attr board_only)\n"
    s += "    (fp_poly\n"
    s += f"      (pts (xy 0 0) (xy {w} 0) (xy {w} {h}) (xy 0 {h}))\n"
    s += '      (layer "Edge.Cuts") (width 0.1)\n'
    s += "    )\n"
    s += f'    (fp_text user "MykoVolt DevKit v{VERSION}" (at {w//2/1e6} {h//2/1e6 + 2} 0)\n'
    s += '      (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15)))\n'
    s += "    )\n"
    s += f'    (fp_text user "30x20mm 4L ENIG RevA" (at {w//2/1e6} {h//2/1e6 + 3.5} 0)\n'
    s += '      (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12)))\n'
    s += "    )\n"
    s += "  )\n"
    
    for ref, value, footprint, _, _ in COMPONENTS:
        if ref not in PCB_POS:
            continue
        x_nm, y_nm = PCB_POS[ref]
        x, y = x_nm / 1e6, y_nm / 1e6
        uid = det_uuid(f"fp_{ref}")
        s += f'  (footprint "{footprint}" (layer "F.Cu") (tedit 0) (tstamp "{uid}")\n'
        s += f'    (at {x} {y} 0)\n'
        s += f'    (fp_text reference "{ref}" (at 0 0 0) (layer "F.SilkS")\n'
        s += "      (effects (font (size 1 1) (thickness 0.15))))\n"
        s += f'    (fp_text value "{value}" (at 0 -2 0) (layer "F.Fab")\n'
        s += "      (effects (font (size 1 1) (thickness 0.15))))\n"
        s += "  )\n"
    
    s += ")\n"
    return s


# ═══════════════════════════════════════════════════════════════
# Project File Generation
# ═══════════════════════════════════════════════════════════════

def generate_project():
    """Generate the KiCad project file (.kicad_pro)."""
    net_names = sorted(set(n[0] for n in NETS))
    return json.dumps(
        {
            "board": {
                "design_settings": {
                    "rules": {
                        "min_clearance": 0.3,
                        "min_track_width": 0.3,
                        "min_via_diameter": 0.6,
                        "min_via_drill": 0.3,
                        "min_hole_to_hole": 0.3,
                        "min_silk_to_copper": 0.15,
                        "min_silk_to_silk": 0.15,
                        "allow_soldermask_bridges_in_footprints": False,
                    }
                }
            },
            "boards": [],
            "cvpcb": {},
            "erc": {},
            "libraries": {"pinned_footprint_libs": [], "pinned_symbol_libs": []},
            "meta": {"filename": f"{BOARD_NAME}.kicad_pro", "version": 2},
            "net_settings": {
                "classes": [
                    {
                        "name": "Default",
                        "clearance": 0.3,
                        "trace_width": 0.3,
                        "via_diameter": 0.6,
                        "via_drill": 0.3,
                        "uvia_diameter": 0.3,
                        "uvia_drill": 0.1,
                    }
                ],
                "meta": {"version": 2, "net_count": len(NETS)},
            },
            "pcbnew": {
                "last_paths": {"gerbers": "", "netlist": ""},
                "page_layout_descr_file": "",
            },
            "schematic": {
                "annotate_start_num": 0,
                "drawing": {"default_line_width": 0.15, "default_text_size": 1.27},
            },
            "sheets": [],
            "text_variables": {},
        },
        indent=2,
    )


def generate_netlist_string():
    """Generate a simple plain-text netlist."""
    lines = ["# MykoVolt DevKit v0.1 — Netlist", f"# Generated: {datetime.now()}", ""]
    total = 0
    for net_name, connections in NETS:
        lines.append(f"\n# {net_name}")
        for ref, pin in connections:
            lines.append(f"  {ref}.{pin}")
            total += 1
    lines.append(f"\n# Total connections: {total}")
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════

def main():
    print(f"=== MykoVolt KiCad Project Generator v{VERSION} ===\n")
    
    # ── 1. Generate Project File ──
    print("Generating project file...")
    proj = generate_project()
    path = os.path.join(PROJECT_DIR, f"{BOARD_NAME}.kicad_pro")
    with open(path, "w") as f:
        f.write(proj)
    print(f"  ✓ {BOARD_NAME}.kicad_pro ({len(proj)} bytes)")
    
    # ── 2. Generate Schematic ──
    print("Generating schematic...")
    if HAVE_SEXP:
        try:
            sch_sexp = generate_schematic_sexp()
            sch_str = sch_sexp.to_str()
        except Exception as e:
            print(f"  ⚠ Sexp generation failed ({e}), falling back to string-based")
            sch_str = generate_schematic_string()
    else:
        sch_str = generate_schematic_string()
    
    path = os.path.join(PROJECT_DIR, f"{BOARD_NAME}.kicad_sch")
    with open(path, "w") as f:
        f.write(sch_str)
    sym_count = len(COMPONENTS) * 2 + len(NETS)  # rough estimate
    print(f"  ✓ {BOARD_NAME}.kicad_sch ({len(sch_str)} bytes, ~{len(COMPONENTS)}+ symbols)")
    
    # ── 3. Generate PCB Layout ──
    print("Generating PCB layout...")
    if HAVE_PCBNEW:
        try:
            pcb_path = generate_pcb_pcbnew()
            with open(pcb_path, "r") as f:
                pcb_len = len(f.read())
            print(f"  ✓ {os.path.basename(pcb_path)} ({pcb_len} bytes, {len([c for c in COMPONENTS if c[0] in PCB_POS])} footprints) [pcbnew]")
        except Exception as e:
            print(f"  ⚠ pcbnew generation failed ({e}), falling back to string-based")
            pcb_str = generate_pcb_string()
            path = os.path.join(PROJECT_DIR, f"{BOARD_NAME}.kicad_pcb")
            with open(path, "w") as f:
                f.write(pcb_str)
            fp_count = len([c for c in COMPONENTS if c[0] in PCB_POS])
            print(f"  ✓ {BOARD_NAME}.kicad_pcb ({len(pcb_str)} bytes, {fp_count} footprints) [fallback]")
    else:
        pcb_str = generate_pcb_string()
        path = os.path.join(PROJECT_DIR, f"{BOARD_NAME}.kicad_pcb")
        with open(path, "w") as f:
            f.write(pcb_str)
        fp_count = len([c for c in COMPONENTS if c[0] in PCB_POS])
        print(f"  ✓ {BOARD_NAME}.kicad_pcb ({len(pcb_str)} bytes, {fp_count} footprints) [string]")
    
    # ── 4. Generate Netlist ──
    print("Generating netlist...")
    net = generate_netlist_string()
    path = os.path.join(PROJECT_DIR, f"{BOARD_NAME}.net")
    with open(path, "w") as f:
        f.write(net)
    total_pins = sum(len(c[1]) for c in NETS)
    print(f"  ✓ {BOARD_NAME}.net ({len(net)} bytes, {len(NETS)} nets, {total_pins} connections)")
    
    # ── Summary ──
    print(f"\n{'─' * 62}")
    print(f"  Components: {len(COMPONENTS)}")
    print(f"  Nets:       {len(NETS)}")
    print(f"  Connections: {total_pins}")
    print(f"  Library:    {'simp_sexp' if HAVE_SEXP else 'string-based'} S-expressions")
    print(f"  PCB:        {'pcbnew' if HAVE_PCBNEW else 'string-based'} [KiCad {pcbnew.Version() if HAVE_PCBNEW else 'N/A'}]")
    print(f"{'─' * 62}")
    print(f"\n  Output: {PROJECT_DIR}/")
    print(f"  Open with: kicad hardware/kicad/{BOARD_NAME}.kicad_pro")


if __name__ == "__main__":
    main()
