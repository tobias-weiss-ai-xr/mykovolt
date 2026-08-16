#!/usr/bin/env python3
"""Generate a visual SVG breadboard wiring diagram for the MykoVolt DevKit prototype.

Output: docs/technical/prototyping/breadboard_wiring.svg
"""

import os
from xml.sax.saxutils import escape as xml_escape

SVG_PATH = os.path.join(os.path.dirname(__file__), "breadboard_wiring.svg")

# ── Layout constants ──
W, H = 900, 650
MARGIN = 30
BREADBOARD_W = 640
BREADBOARD_H = 460
BREADBOARD_X = (W - BREADBOARD_W) // 2
BREADBOARD_Y = 100

# Component positions (center x, y)
COMPONENTS_LAYOUT = {
    "nucleo":  (BREADBOARD_X + 60, BREADBOARD_Y + 50),
    "bq25570": (BREADBOARD_X + 200, BREADBOARD_Y + 40),
    "sc1":     (BREADBOARD_X + 330, BREADBOARD_Y + 40),
    "st25dv04k": (BREADBOARD_X + 80, BREADBOARD_Y + 180),
    "mb85rc16": (BREADBOARD_X + 200, BREADBOARD_Y + 180),
    "pcf8523":  (BREADBOARD_X + 320, BREADBOARD_Y + 180),
    "fdc1004":  (BREADBOARD_X + 440, BREADBOARD_Y + 180),
    "j2":       (BREADBOARD_X + 500, BREADBOARD_Y + 40),
    "led1":     (BREADBOARD_X + 60, BREADBOARD_Y + 320),
    "led2":     (BREADBOARD_X + 180, BREADBOARD_Y + 320),
    "q1":       (BREADBOARD_X + 60, BREADBOARD_Y + 270),
    "j4":       (BREADBOARD_X + 440, BREADBOARD_Y + 320),
    "r1":       (BREADBOARD_X + 80, BREADBOARD_Y + 380),
    "r2":       (BREADBOARD_X + 200, BREADBOARD_Y + 380),
    "r3_r10":   (BREADBOARD_X + 320, BREADBOARD_Y + 380),
    "antenna":  (BREADBOARD_X + 500, BREADBOARD_Y + 280),
    "pressling": (BREADBOARD_X + 560, BREADBOARD_Y + 60),
}


def color(name):
    colors = {
        "3v3": "#d32f2f",
        "gnd": "#212121",
        "scl": "#f9a825",
        "sda": "#f9a825",
        "swd": "#1565c0",
        "sensor": "#2e7d32",
        "nfc": "#6a1b9a",
        "signal": "#00838f",
    }
    return colors.get(name, "#666")


def draw_breadboard_svg():
    lines = []
    L = lines.append

    L('<?xml version="1.0" encoding="UTF-8"?>')
    L(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    L('<style>')
    L('  text { font-family: monospace; }')
    L('  .title { font-size: 16px; font-weight: bold; }')
    L('  .label { font-size: 10px; fill: #444; }')
    L('  .small { font-size: 8px; fill: #666; }')
    L('  .wire { fill: none; stroke-width: 1.5; }')
    L('  .wire-thick { fill: none; stroke-width: 3; }')
    L('</style>')

    # Background
    L(f'<rect width="{W}" height="{H}" fill="#fafafa" rx="8"/>')

    # Title
    L(f'<text x="{W//2}" y="25" text-anchor="middle" class="title">'
      'MykoVolt DevKit — Breadboard Wiring Diagram</text>')
    L(f'<text x="{W//2}" y="42" text-anchor="middle" class="small">'
      'Nucleo-L011K4  •  BQ25570 power  •  I²C bus 0x50–0x53  •  FDC1004 sensor</text>')

    # ── Breadboard outline ──
    bx, by = BREADBOARD_X, BREADBOARD_Y
    bw, bh = BREADBOARD_W, BREADBOARD_H
    L(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="none" stroke="#ccc" stroke-width="2" rx="4"/>')
    L(f'<text x="{bx + 5}" y="{by + 12}" class="small">Breadboard (830 tie points)</text>')

    # Power rails
    # Top rail: 3.3V (red)
    L(f'<rect x="{bx + 3}" y="{by + 3}" width="{bw - 6}" height="8" fill="#ffcdd2" rx="2"/>')
    L(f'<text x="{bx + 10}" y="{by + 9}" fill="#d32f2f" font-size="7" font-weight="bold">'
      '+3.3V RAIL</text>')
    # Bottom rail: GND (black)
    L(f'<rect x="{bx + 3}" y="{by + bh - 11}" width="{bw - 6}" height="8" fill="#e0e0e0" rx="2"/>')
    L(f'<text x="{bx + 10}" y="{by + bh - 5}" fill="#333" font-size="7" font-weight="bold">'
      'GND RAIL</text>')

    # ── Wires (draw before components so they appear underneath) ──

    # Power: 3.3V distribution
    wires_3v3 = [
        ("nucleo", "bq25570", -25, -15, 30, -10),
        ("bq25570", "sc1", 50, -5, 40, 0),
        ("bq25570", "st25dv04k", -20, 80, -20, 30),
        ("st25dv04k", "mb85rc16", 30, 20, 30, 10),
        ("mb85rc16", "pcf8523", 40, 20, 40, 10),
        ("pcf8523", "fdc1004", 40, 20, 40, 10),
    ]
    for src, dst, ox1, oy1, ox2, oy2 in wires_3v3:
        x1 = COMPONENTS_LAYOUT[src][0] + ox1
        y1 = COMPONENTS_LAYOUT[src][1] + oy1
        x2 = COMPONENTS_LAYOUT[dst][0] + ox2
        y2 = COMPONENTS_LAYOUT[dst][1] + oy2
        L(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="wire" stroke="{color("3v3")}"/>')

    # Power: GND distribution
    wires_gnd = [
        ("nucleo", "st25dv04k", -25, 25, -20, 60),
        ("st25dv04k", "mb85rc16", 20, 70, 20, 50),
        ("mb85rc16", "pcf8523", 40, 60, 40, 40),
        ("pcf8523", "fdc1004", 40, 60, 40, 40),
        ("bq25570", "j2", 80, 20, 80, -5),
    ]
    for src, dst, ox1, oy1, ox2, oy2 in wires_gnd:
        x1 = COMPONENTS_LAYOUT[src][0] + ox1
        y1 = COMPONENTS_LAYOUT[src][1] + oy1
        x2 = COMPONENTS_LAYOUT[dst][0] + ox2
        y2 = COMPONENTS_LAYOUT[dst][1] + oy2
        L(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="wire" stroke="{color("gnd")}"/>')

    # I2C bus (SCL)
    i2c_wires = [
        ("nucleo", "st25dv04k", -15, 5, 0, 20),
        ("st25dv04k", "mb85rc16", 40, 40, -10, 40),
        ("mb85rc16", "pcf8523", 40, 40, -10, 40),
        ("pcf8523", "fdc1004", 40, 40, -10, 40),
    ]
    for src, dst, ox1, oy1, ox2, oy2 in i2c_wires:
        x1 = COMPONENTS_LAYOUT[src][0] + ox1
        y1 = COMPONENTS_LAYOUT[src][1] + oy1
        x2 = COMPONENTS_LAYOUT[dst][0] + ox2
        y2 = COMPONENTS_LAYOUT[dst][1] + oy2
        L(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="wire" stroke="{color("scl")}" '
          f'stroke-dasharray="4,3"/>')

    # I2C bus (SDA) — slightly offset
    i2c_sda_wires = [
        ("nucleo", "st25dv04k", -15, 10, 0, 25),
        ("st25dv04k", "mb85rc16", 40, 45, -10, 45),
        ("mb85rc16", "pcf8523", 40, 45, -10, 45),
        ("pcf8523", "fdc1004", 40, 45, -10, 45),
    ]
    for src, dst, ox1, oy1, ox2, oy2 in i2c_sda_wires:
        x1 = COMPONENTS_LAYOUT[src][0] + ox1
        y1 = COMPONENTS_LAYOUT[src][1] + oy1
        x2 = COMPONENTS_LAYOUT[dst][0] + ox2
        y2 = COMPONENTS_LAYOUT[dst][1] + oy2
        L(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="wire" stroke="{color("sda")}" '
          f'stroke-dasharray="2,3"/>')

    # Sensor wires (CIN1, CIN2, SHLD1)
    sensor_wires = [
        ("fdc1004", "j4", 20, 50, -20, 40),
    ]
    for src, dst, ox1, oy1, ox2, oy2 in sensor_wires:
        x1 = COMPONENTS_LAYOUT[src][0] + ox1
        y1 = COMPONENTS_LAYOUT[src][1] + oy1
        x2 = COMPONENTS_LAYOUT[dst][0] + ox2
        y2 = COMPONENTS_LAYOUT[dst][1] + oy2
        L(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="wire-thick" stroke="{color("sensor")}"/>')

    # NFC antenna wires
    nfc_wires = [
        ("st25dv04k", "antenna", 60, 10, -40, 0),
    ]
    for src, dst, ox1, oy1, ox2, oy2 in nfc_wires:
        x1 = COMPONENTS_LAYOUT[src][0] + ox1
        y1 = COMPONENTS_LAYOUT[src][1] + oy1
        x2 = COMPONENTS_LAYOUT[dst][0] + ox2
        y2 = COMPONENTS_LAYOUT[dst][1] + oy2
        L(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="wire" stroke="{color("nfc")}"/>')

    # LED wires
    L(f'<line x1="{COMPONENTS_LAYOUT["q1"][0]}" y1="{COMPONENTS_LAYOUT["q1"][1]}" '
      f'x2="{COMPONENTS_LAYOUT["led1"][0]}" y2="{COMPONENTS_LAYOUT["led1"][1] - 20}" '
      f'class="wire" stroke="{color("signal")}"/>')
    L(f'<line x1="{COMPONENTS_LAYOUT["nucleo"][0] + 30}" y1="{COMPONENTS_LAYOUT["nucleo"][1] + 20}" '
      f'x2="{COMPONENTS_LAYOUT["led2"][0]}" y2="{COMPONENTS_LAYOUT["led2"][1] - 20}" '
      f'class="wire" stroke="{color("signal")}"/>')

    # ── Component boxes ──

    def draw_box(cx, cy, w, h, label, sublabel, fill="#e3f2fd", stroke="#1565c0"):
        L(f'<rect x="{cx - w//2}" y="{cy - h//2}" width="{w}" height="{h}" '
          f'fill="{fill}" stroke="{stroke}" stroke-width="1.5" rx="3"/>')
        L(f'<text x="{cx}" y="{cy - 2}" text-anchor="middle" class="label" font-weight="bold">'
          f'{xml_escape(label)}</text>')
        L(f'<text x="{cx}" y="{cy + 10}" text-anchor="middle" class="small">'
          f'{xml_escape(sublabel)}</text>')

    # Draw each component
    draw_box(*COMPONENTS_LAYOUT["nucleo"], 100, 40, "Nucleo-L011K4", "MCU (STM32L011)", "#e8f5e9", "#2e7d32")
    draw_box(*COMPONENTS_LAYOUT["bq25570"], 80, 36, "BQ25570", "Energy Harvester", "#fff3e0", "#e65100")
    draw_box(*COMPONENTS_LAYOUT["sc1"], 50, 30, "SC1", "100mF Supercap", "#fce4ec", "#c62828")
    draw_box(*COMPONENTS_LAYOUT["st25dv04k"], 70, 30, "ST25DV04K", "NFC Tag (0x53)", "#f3e5f5", "#7b1fa2")
    draw_box(*COMPONENTS_LAYOUT["mb85rc16"], 70, 30, "MB85RC16", "FRAM (0x50)", "#e0f7fa", "#00838f")
    draw_box(*COMPONENTS_LAYOUT["pcf8523"], 70, 30, "PCF8523", "RTC (0x52)", "#e0f2f1", "#00695c")
    draw_box(*COMPONENTS_LAYOUT["fdc1004"], 70, 30, "FDC1004", "Cap Sense (0x51)", "#fbe9e7", "#d84315")
    draw_box(*COMPONENTS_LAYOUT["j2"], 40, 25, "J2", "Pressling In", "#e8f0fe", "#3949ab")
    draw_box(*COMPONENTS_LAYOUT["j4"], 50, 30, "J4", "Sensor Electrodes", "#e8f5e9", "#2e7d32")
    draw_box(*COMPONENTS_LAYOUT["led1"], 40, 20, "LED1", "Green (PWR)", "#e8f5e9", "#2e7d32")
    draw_box(*COMPONENTS_LAYOUT["led2"], 40, 20, "LED2", "Yellow (STAT)", "#fff8e1", "#f9a825")
    draw_box(*COMPONENTS_LAYOUT["q1"], 40, 20, "Q1", "Load Switch", "#e0f2f1", "#004d40")
    draw_box(*COMPONENTS_LAYOUT["r1"], 40, 18, "R1", "I²C Pull-up SCL", "#f5f5f5", "#888")
    draw_box(*COMPONENTS_LAYOUT["r2"], 40, 18, "R2", "I²C Pull-up SDA", "#f5f5f5", "#888")
    draw_box(*COMPONENTS_LAYOUT["r3_r10"], 60, 20, "R3-R10", "BQ25570 Config", "#f5f5f5", "#888")

    # NFC antenna coil
    ax, ay = COMPONENTS_LAYOUT["antenna"]
    L(f'<ellipse cx="{ax}" cy="{ay}" rx="40" ry="15" fill="none" stroke="{color("nfc")}" '
      f'stroke-width="2" stroke-dasharray="2,2"/>')
    L(f'<text x="{ax}" y="{ay - 18}" text-anchor="middle" class="small" fill="{color("nfc")}">'
      'NFC Antenna (3 turns)</text>')

    # Pressling MFC symbol
    px, py = COMPONENTS_LAYOUT["pressling"]
    L(f'<polygon points="{px},{py-15} {px+15},{py+5} {px-15},{py+5}" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1.5"/>')
    L(f'<text x="{px}" y="{py + 18}" text-anchor="middle" class="small" fill="#2e7d32">'
      'Pressling MFC</text>')

    # ── Legend ──
    legend_x = bx + bw + 20
    legend_y = by + 20
    L(f'<rect x="{legend_x}" y="{legend_y}" width="120" height="130" fill="white" stroke="#ccc" rx="4"/>')
    L(f'<text x="{legend_x + 10}" y="{legend_y + 15}" font-size="9" font-weight="bold">Legend</text>')
    for i, (name, col, dash) in enumerate([
        ("+3.3V", color("3v3"), ""),
        ("GND", color("gnd"), ""),
        ("I²C SCL", color("scl"), "stroke-dasharray='4,3'"),
        ("I²C SDA", color("sda"), "stroke-dasharray='2,3'"),
        ("Sensor", color("sensor"), ""),
        ("NFC RF", color("nfc"), ""),
    ]):
        ly = legend_y + 35 + i * 16
        L(f'<line x1="{legend_x + 8}" y1="{ly}" x2="{legend_x + 38}" y2="{ly}" '
          f'stroke="{col}" stroke-width="2" {dash}/>')
        L(f'<text x="{legend_x + 45}" y="{ly + 3}" font-size="8" fill="#444">{name}</text>')

    L('</svg>')
    return "\n".join(lines)


def main():
    svg = draw_breadboard_svg()
    with open(SVG_PATH, "w") as f:
        f.write(svg)
    print(f"  ✓ Generated {SVG_PATH} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
