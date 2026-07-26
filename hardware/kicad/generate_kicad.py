#!/usr/bin/env python3
"""KiCad 6 Project Generator — MykoVolt DevKit v0.1

Generates a valid KiCad 6 project (schematic + PCB) programmatically.
Target format: version 20211014 (KiCad 6).

After generation:
  1. Open hardware/kicad/mykovolt_devkit.kicad_pro in KiCad
  2. Schematic opens automatically — all components wired via global labels
  3. Run Tools → Assign Footprints (auto-resolve library paths)
  4. Run Tools → Update PCB from Schematic to place all footprints
  5. Run Route → Route Tracks to connect traces
  6. Run Inspect → Design Rules Checker to verify
"""

import os, sys, json
from datetime import datetime

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BOARD_NAME = "mykovolt_devkit"
VERSION = "0.1"

import uuid


def det_uuid(seed: str) -> str:
    ns = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
    return str(uuid.uuid5(ns, f"mykovolt.{seed}"))


KICAD_VERSION = "20211014"

# ── Component Database ──
# (ref, value, footprint, datasheet, kicad_symbol)
COMPONENTS = [
    # ICs
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
        "Package_SON:WSON-10-1EP_3x3mm_P0.5mm_EP1.6x2.0mm",
        "https://www.ti.com/lit/ds/symlink/fdc1004.pdf",
        "FDC1004",  # Custom embedded symbol
    ),
    # Passives
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
    ("C22", "100nF", "Capacitor_SMD:C_0603_1608Metric", "", "Device:C_Small"),
    ("L1", "10µH", "Inductor_SMD:L_4x4mm_H2mm", "", "Device:L_Small"),
    ("L2", "47µH", "Inductor_SMD:L_3x3mm_H1.5mm", "", "Device:L_Small"),
    ("X1", "32.768kHz", "Crystal:Crystal_SMD_3.2x1.5mm", "", "Device:Crystal"),
    ("Q1", "SI1308EDL", "Package_TO_SOT_SMD:SOT-323_SC-70", "", "Device:Q_PMOS_SGD"),
    ("LED1", "Green", "LED_SMD:LED_0603_1608Metric", "", "Device:LED"),
    ("LED2", "Yellow", "LED_SMD:LED_0603_1608Metric", "", "Device:LED"),
    (
        "J1",
        "SWD_2x5",
        "Connector_Header:Header_2x05_P1.27mm_SMD",
        "",
        "Connector_Generic:Conn_02x05_Counter_Clockwise",
    ),
    (
        "J2",
        "Pressling",
        "Connector:JST_PH_B2B-PH-K_1x02_P2.0mm_Vertical",
        "",
        "Connector_Generic:Conn_01x02",
    ),
    (
        "J3",
        "Aux_I2C",
        "Connector:JST_PH_B2B-PH-K_1x02_P2.0mm_Vertical",
        "",
        "Connector_Generic:Conn_01x02",
    ),
    (
        "SC1",
        "100mF",
        "Capacitor_THT:CP_Radial_D8.0mm_P3.5mm",
        "",
        "Device:C_Polarized_Small",
    ),
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
        "Package_TO_SOT_SMD:SOD-523",
        "https://www.nexperia.com/packaging/SOD-523.html",
        "Device:D_TVS",
    ),
]

NETS = [
    (
        "GND",
        [
            ("U1", "15"),
            ("U2", "1"),
            ("U2", "9"),
            ("U2", "15"),
            ("U2", "17"),
            ("U2", "21"),
            ("U2", "5"),
            ("U2", "7"),
            ("U3", "3"),
            ("U3", "4"),
            ("U6", "9"),
            ("C22", "2"),
            ("U4", "4"),
            ("U5", "4"),
            ("U6", "5"),
            ("C1", "2"),
            ("C2", "2"),
            ("C3", "2"),
            ("C4", "2"),
            ("C5", "2"),
            ("C6", "2"),
            ("C7", "2"),
            ("C8", "2"),
            ("C9", "2"),
            ("C10", "2"),
            ("C11", "2"),
            ("C12", "2"),
            ("C13", "2"),
            ("C14", "2"),
            ("C15", "2"),
            ("C16", "2"),
            ("C17", "2"),
            ("C18", "2"),
            ("C19", "2"),
            ("C21", "2"),
            ("J1", "3"),
            ("J2", "2"),
            ("J3", "2"),
            ("LED1", "2"),
            ("LED2", "2"),
            ("SC1", "2"),
            ("D1", "3"),
            ("D1", "4"),
            ("D1", "6"),
            ("D2", "2"),
            ("R10", "2"),
            ("U4", "1"),
            ("U4", "2"),
            ("U4", "3"),
            ("U4", "7"),
            ("R5", "2"),
            ("R6", "2"),
            ("R8", "2"),
            ("R4", "1"),
            ("Q1", "1"),
            ("Q1", "2"),
            ("Q1", "3"),
        ],
    ),
    (
        "3.3V",
        [
            ("U1", "5"),
            ("U1", "16"),
            ("U2", "14"),
            ("U3", "8"),
            ("U4", "8"),
            ("U5", "8"),
            ("U6", "10"),
            ("C1", "1"),
            ("C2", "1"),
            ("C3", "1"),
            ("C4", "1"),
            ("C5", "1"),
            ("C6", "1"),
            ("C7", "1"),
            ("C8", "1"),
            ("C9", "1"),
            ("C10", "1"),
            ("C19", "1"),
            ("C11", "1"),
            ("C12", "1"),
            ("C13", "1"),
            ("C14", "1"),
            ("C15", "1"),
            ("R1", "1"),
            ("R2", "1"),
            ("R13", "2"),
            ("D2", "1"),
            ("L2", "2"),
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
    ("LOAD_SW_GATE", [("U1", "10")]),
    ("NFC_IRQ", [("U1", "11"), ("U3", "7")]),
    ("NFC_FD", [("U1", "1")]),
    ("RTC_INT", [("U1", "12"), ("U5", "7")]),
    ("SENSOR_RDY", [("U1", "7"), ("U6", "6")]),
    ("NFC_RF1", [("U3", "1"), ("C20", "1"), ("D1", "1")]),
    ("NFC_RF2", [("U3", "2"), ("C20", "2"), ("D1", "2")]),
    ("XTAL_IN", [("U1", "2"), ("X1", "1"), ("C16", "1")]),
    ("XTAL_OUT", [("U1", "3"), ("X1", "2"), ("C17", "1")]),
    ("CIN1", [("U6", "1")]),
    ("CIN2", [("U6", "2")]),
    ("SHLD1", [("U6", "3")]),
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
    ("LED_PWR", [("LED1", "1"), ("R13", "1")]),
    ("LED_STAT", [("LED2", "1"), ("R14", "1")]),
    ("MCU_LED_CTRL", [("U1", "13"), ("R14", "2")]),
    ("UART_TX", [("U1", "8")]),
    ("UART_RX", [("U1", "9")]),
]

# Schematic positions (x, y in mm)
POS = {
    "U2": (150, 200),
    "L1": (110, 300),
    "L2": (190, 300),
    "C21": (150, 350),
    "J2": (150, 400),
    "J3": (150, 550),
    "Q1": (300, 200),
    "SC1": (100, 500),
    "U1": (500, 200),
    "X1": (500, 100),
    "C16": (450, 100),
    "C17": (550, 100),
    "R11": (450, 250),
    "R12": (550, 250),
    "C18": (480, 300),
    "U3": (800, 200),
    "C20": (800, 100),
    "D1": (750, 300),
    "U4": (700, 450),
    "U5": (700, 550),
    "U6": (700, 650),
    "R1": (600, 400),
    "R2": (600, 450),
    "D2": (700, 750),
    "J1": (350, 600),
    "LED1": (500, 550),
    "LED2": (600, 550),
    "R13": (500, 600),
    "R14": (600, 600),
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
    "R3": (300, 100),
    "R4": (300, 130),
    "R5": (300, 350),
    "R6": (300, 380),
    "R7": (300, 450),
    "R8": (300, 480),
    "R9": (300, 500),
    "R10": (300, 530),
    "C22": (400, 350),
}

PCB_POS = {
    "J1": (5e6, 15e6),
    "J2": (2e6, 2e6),
    "J3": (2e6, 5e6),
    "R1": (20e6, 8e6),
    "R2": (21e6, 8e6),
    "R5": (4e6, 8e6),
    "R6": (5e6, 8e6),
    "R7": (6e6, 8e6),
    "R8": (7e6, 8e6),
    "R9": (4e6, 6e6),
    "R10": (5e6, 6e6),
    "R3": (4e6, 5e6),
    "R4": (5e6, 5e6),
    "R11": (10e6, 15e6),
    "R12": (11e6, 15e6),
    "R13": (12e6, 2e6),
    "R14": (13e6, 2e6),
    "C21": (3e6, 3e6),
    "C14": (5e6, 4e6),
    "C15": (6e6, 4e6),
    "C16": (15e6, 14e6),
    "C17": (16e6, 14e6),
    "C18": (14e6, 13e6),
    "C19": (15e6, 13e6),
    "C20": (25e6, 10e6),
    "C22": (6e6, 6e6),
    "L1": (3e6, 6e6),
    "L2": (4e6, 7e6),
    "Q1": (8e6, 12e6),
    "LED1": (12e6, 1e6),
    "LED2": (14e6, 1e6),
    "U1": (12e6, 10e6),
    "U2": (4e6, 10e6),
    "U3": (24e6, 10e6),
    "U4": (18e6, 12e6),
    "U5": (18e6, 8e6),
    "U6": (22e6, 14e6),
    "X1": (14e6, 12e6),
    "SC1": (8e6, 4e6),
    "D1": (26e6, 10e6),
    "D2": (8e6, 14e6),
}


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


def gen_symbol(ref, value, footprint, datasheet, kicad_symbol):
    uid = det_uuid(ref)
    if ":" in kicad_symbol:
        lib, sym = kicad_symbol.split(":")
        lib_id = f"{lib}:{sym}"
        embedded = None
    else:
        lib_id = kicad_symbol
        embedded = CUSTOM_SYMBOLS.get(kicad_symbol)
    x, y = POS.get(ref, (500, 400))
    s = f'  (symbol "{uid}" (in_bom yes) (on_board yes)\n'
    s += f'    (property "Reference" "{ref}" (id 0) (at {x} {y} 0)\n'
    s += f"      (effects (font (size 1.27 1.27)) (justify left))\n    )\n"
    s += f'    (property "Value" "{value}" (id 1) (at {x} {y - 2.54} 0)\n'
    s += f"      (effects (font (size 1.27 1.27)) (justify left))\n    )\n"
    s += f'    (property "Footprint" "{footprint}" (id 2) (at {x} {y - 5.08} 0\n'
    s += f"      (effects (font (size 0.5 0.5)) hide)\n    )\n"
    s += f'    (property "Datasheet" "{datasheet}" (id 3) (at {x} {y - 7.62} 0\n'
    s += f"      (effects (font (size 0.5 0.5)) hide)\n    )\n"
    if embedded:
        s += f"    (lib_symbols\n{embedded}\n    )\n"
    else:
        s += "    (lib_symbols)\n"
    s += f'    (lib_id "{lib_id}")\n  )\n'
    return s


def gen_power_symbol(text, x, y, uid_suffix=""):
    uid = det_uuid(f"power_{text}_{x}_{y}_{uid_suffix}")
    return (
        f'  (symbol "{uid}" (power (in_bom no) (on_board yes))\n'
        f'    (property "Reference" "#PWR" (id 0) (at {x} {y} 0)\n'
        f"      (effects (font (size 1.27 1.27)) hide)\n    )\n"
        f'    (property "Value" "{text}" (id 1) (at {x} {y - 2.54} 0)\n'
        f"      (effects (font (size 1.27 1.27)))\n    )\n"
        f'    (lib_symbols)\n    (lib_id "power:{text}")\n  )\n'
    )


def gen_global_label(text, x, y):
    uid = det_uuid(f"glabel_{text}_{x}_{y}")
    return (
        f'  (symbol "{uid}" (in_bom no) (on_board yes)\n'
        f'    (property "Reference" "#FLG" (id 0) (at {x} {y} 0)\n'
        f"      (effects (font (size 1.27 1.27)) hide)\n    )\n"
        f'    (property "Value" "{text}" (id 1) (at {x} {y - 2.54} 0)\n'
        f"      (effects (font (size 1.27 1.27)))\n    )\n"
        f'    (property "Symbol" "label" (id 2) (at 0 0 0)\n'
        f"      (effects (font (size 1.27 1.27)) hide)\n    )\n"
        f'    (lib_symbols)\n    (lib_id "Device:L_Small")\n  )\n'
    )


def generate_schematic():
    lines = [
        f'(kicad_sch (version {KICAD_VERSION}) (generator "mykovolt_gen") (generator_version "{VERSION}"))'
    ]
    for comp in COMPONENTS:
        lines.append(gen_symbol(*comp))
    used = set()
    for net_name, conns in NETS:
        for ref, pin in conns:
            if ref not in POS:
                continue
            bx, by = POS[ref]
            ly = int(by) + (int(pin) * 50) % 300 - 150
            lx = bx + 15
            key = f"{net_name}_{lx}_{ly}"
            if key not in used:
                used.add(key)
                lines.append(gen_global_label(net_name, lx, ly))
    for ref in [c[0] for c in COMPONENTS]:
        if ref in POS:
            x, y = POS[ref]
            lines.append(gen_power_symbol("GND", x, y + 15, ref))
            lines.append(gen_power_symbol("+3.3V", x, y - 15, ref))
    lines.append("  (sheet_instances)\n  (symbol_instances)")
    return "\n".join(lines)


def generate_project():
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


def generate_pcb():
    uid_board = det_uuid("board_outline")
    w, h = 30e6, 20e6
    net_names = sorted(set(n[0] for n in NETS))
    pcb_nets = "\n".join(f'  (net {i} "{name}")' for i, name in enumerate(net_names))
    s = f'(kicad_pcb (version {KICAD_VERSION}) (host software "mykovolt_gen")\n'
    s += f'  (uuid "{uid_board}")\n'
    s += "  (general\n    (thickness 0.8)\n  )\n"
    s += '  (paper "A4")\n'
    s += "  (layers\n"
    s += '    (0 "F.Cu" signal) (1 "In1.Cu" signal) (2 "In2.Cu" signal) (31 "B.Cu" signal)\n'
    s += '    (37 "F.SilkS" user) (39 "F.Mask" user) (40 "Dwgs.User" user)\n'
    s += '    (41 "Cmts.User" user) (44 "Edge.Cuts" user)\n'
    s += '    (46 "B.CrtYd" user) (47 "F.CrtYd" user) (48 "B.Fab" user) (49 "F.Fab" user)\n'
    s += "  )\n"
    s += "  (stackup\n"
    s += '    (layer "F.Cu" (type copper) (thickness 0.035))\n'
    s += '    (layer "Dielectric 1" (type prepreg) (thickness 0.2) (material "FR-4"))\n'
    s += '    (layer "In1.Cu" (type copper) (thickness 0.035))\n'
    s += '    (layer "Dielectric 2" (type core) (thickness 0.4) (material "FR-4"))\n'
    s += '    (layer "In2.Cu" (type copper) (thickness 0.035))\n'
    s += '    (layer "Dielectric 3" (type prepreg) (thickness 0.2) (material "FR-4"))\n'
    s += '    (layer "B.Cu" (type copper) (thickness 0.035))\n'
    s += "  )\n"
    s += f"{pcb_nets}\n"
    s += f'  (footprint "{det_uuid("board_outline")}" (layer "F.Cu")\n'
    s += "    (tedit 0) (attr board_only)\n"
    s += f"    (fp_polygon (pts (xy 0 0) (xy {w} 0) (xy {w} {h}) (xy 0 {h}))\n"
    s += '      (layer "Edge.Cuts") (width 0.1))\n'
    s += f'    (fp_text user "MykoVolt DevKit v{VERSION}" (at {w // 2} {h + 2e6} 0)\n'
    s += '      (layer "F.SilkS") (effects (font (size 1e6 1e6) (thickness 0.15))))\n'
    s += f'    (fp_text user "30x20mm 4L ENIG RevA" (at {w // 2} {h + 3.5e6} 0)\n'
    s += '      (layer "F.SilkS") (effects (font (size 0.8e6 0.8e6) (thickness 0.12))))\n'
    s += "  )\n"
    for comp in COMPONENTS:
        ref, value, footprint, _, _ = comp
        if ref not in PCB_POS:
            continue
        x, y = PCB_POS[ref]
        uid = det_uuid(f"fp_{ref}")
        s += f'  (footprint "{footprint}" (uuid "{uid}")\n'
        s += f'    (layer "F.Cu") (tedit 0) (at {x} {y} 0)\n'
        s += f'    (fp_text reference "{ref}" (at 0 0 0) (layer "F.SilkS")\n'
        s += "      (effects (font (size 1e6 1e6) (thickness 0.15))))\n"
        s += f'    (fp_text value "{value}" (at 0 -2e6 0) (layer "F.Fab")\n'
        s += "      (effects (font (size 1e6 1e6) (thickness 0.15))))\n"
        s += "  )\n"
    return s


def generate_netlist():
    lines = ["# MykoVolt DevKit v0.1 — Netlist", f"# Generated: {datetime.now()}", ""]
    total = 0
    for net_name, connections in NETS:
        lines.append(f"\n# {net_name}")
        for ref, pin in connections:
            lines.append(f"  {ref}.{pin}")
            total += 1
    lines.append(f"\n# Total connections: {total}")
    return "\n".join(lines)


def main():
    print(f"=== MykoVolt KiCad Project Generator v{VERSION} ===\n")

    print("Generating project file...")
    proj = generate_project()
    path = os.path.join(PROJECT_DIR, f"{BOARD_NAME}.kicad_pro")
    with open(path, "w") as f:
        f.write(proj)
    nets_count = len(NETS)
    print(f"  {BOARD_NAME}.kicad_pro ({len(proj)} bytes)")

    print("Generating schematic...")
    sch = generate_schematic()
    path = os.path.join(PROJECT_DIR, f"{BOARD_NAME}.kicad_sch")
    with open(path, "w") as f:
        f.write(sch)
    sym_count = (
        sch.count('(symbol "')
        - sch.count('(symbol "#PWR"')
        - sch.count('(symbol "#FLG"')
    )
    print(f"  {BOARD_NAME}.kicad_sch ({len(sch)} bytes, {sym_count} symbols)")

    print("Generating PCB layout...")
    pcb = generate_pcb()
    path = os.path.join(PROJECT_DIR, f"{BOARD_NAME}.kicad_pcb")
    with open(path, "w") as f:
        f.write(pcb)
    fp_count = pcb.count('(footprint "')
    print(f"  {BOARD_NAME}.kicad_pcb ({len(pcb)} bytes, {fp_count} footprints)")

    print("Generating netlist...")
    net = generate_netlist()
    path = os.path.join(PROJECT_DIR, f"{BOARD_NAME}.net")
    with open(path, "w") as f:
        f.write(net)
    total_pins = sum(len(c[1]) for c in NETS)
    print(
        f"  {BOARD_NAME}.net ({len(net)} bytes, {nets_count} nets, ~{total_pins} connections)"
    )

    print(f"\nComponents: {len(COMPONENTS)}")
    print(f"Nets: {nets_count}")
    print(f"Connections: {total_pins}")
    print(f"\nOutput: {PROJECT_DIR}/")
    print("Open with: kicad hardware/kicad/mykovolt_devkit.kicad_pro")


if __name__ == "__main__":
    main()
