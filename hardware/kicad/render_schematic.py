#!/usr/bin/env python3
"""Render the MykoVolt DevKit schematic as a clean SVG/PDF.

Reads component data and netlist from the generator,
draws proper electronic schematic symbols with orthogonal wiring.
"""

import os, sys, math
from datetime import datetime
from xml.sax.saxutils import escape as xml_escape

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)
from generate_kicad import COMPONENTS, NETS, POS, VERSION

# ── Component classification ──
IC_REFS = {c[0] for c in COMPONENTS if c[0].startswith("U")}
RES_REFS = {c[0] for c in COMPONENTS if c[0].startswith("R")}
CAP_REFS = {c[0] for c in COMPONENTS if c[0].startswith("C")}
IND_REFS = {c[0] for c in COMPONENTS if c[0].startswith("L")}
CONN_REFS = {c[0] for c in COMPONENTS if c[0].startswith("J")}
LED_REFS = {c[0] for c in COMPONENTS if c[0].startswith("LED")}
XTAL_REFS = {c[0] for c in COMPONENTS if c[0].startswith("X")}
DIO_REFS = {c[0] for c in COMPONENTS if c[0].startswith("D")}
MOS_REFS = {c[0] for c in COMPONENTS if c[0].startswith("Q")}
SCAP_REFS = {c[0] for c in COMPONENTS if c[0].startswith("SC")}

def get_value(ref):
    for cr, cv, *_ in COMPONENTS:
        if cr == ref: return cv
    return ""

# ── Layout: component bounding box and anchor points ──
# Each component gets a bounding box and a list of pin connection points
# We'll place pin points on the edges of the component box

COMP_BOX = {}  # ref -> (cx, cy, w, h) in mm
COMP_PINS = {}  # ref -> [(pin_name, side, offset), ...]
                 # side: 'L','R','T','B', offset is normalized 0..1 along that side

# Define pin maps for each component based on netlist
for net_name, connections in NETS:
    for ref, pin in connections:
        if ref not in POS:
            continue
        if ref not in COMP_PINS:
            COMP_PINS[ref] = []
        COMP_PINS[ref].append((pin, net_name))

# Assign box sizes based on component type
for ref, (x, y) in POS.items():
    cat = "ic" if ref in IC_REFS else \
          "res" if ref in RES_REFS else \
          "cap" if ref in CAP_REFS else \
          "ind" if ref in IND_REFS else \
          "conn" if ref in CONN_REFS else \
          "led" if ref in LED_REFS else \
          "dio" if ref in DIO_REFS else \
          "mos" if ref in MOS_REFS else \
          "xtal" if ref in XTAL_REFS else \
          "scap" if ref in SCAP_REFS else \
          "other"
    
    if cat == "ic":
        w, h = 24, 16
    elif cat in ("res", "cap", "ind"):
        w, h = 10, 6
    elif cat == "conn":
        w, h = 12, 8
    elif cat == "led":
        w, h = 10, 8
    elif cat == "dio":
        w, h = 10, 6
    elif cat == "mos":
        w, h = 10, 8
    elif cat == "xtal":
        w, h = 10, 6
    elif cat == "scap":
        w, h = 10, 12
    else:
        w, h = 12, 8
    
    COMP_BOX[ref] = (x, y, w, h)

# Find bounding box
all_x = [x for x, y in POS.values()]
all_y = [y for x, y in POS.values()]
min_x, max_x = min(all_x) - 20, max(all_x) + 20
min_y, max_y = min(all_y) - 20, max(all_y) + 20

scale = 5.0  # px per mm
margin = 40

def to_svg(x_mm, y_mm):
    sx = (x_mm - min_x) * scale + margin
    sy = (max_y - y_mm) * scale + margin  # flip Y
    return sx, sy

def pin_pos(ref, pin_idx, total_pins):
    """Calculate pin position on component edge."""
    if ref not in COMP_BOX:
        return (0, 0)
    cx, cy, w, h = COMP_BOX[ref]
    # Distribute pins on all 4 sides
    pins_per_side = max(1, math.ceil(total_pins / 4))
    side_idx = pin_idx // pins_per_side
    local_idx = pin_idx % pins_per_side
    frac = (local_idx + 0.5) / pins_per_side
    
    sides = ['L', 'T', 'R', 'B']
    side = sides[side_idx % 4]
    
    if side == 'L':
        return (cx - w/2, cy - h/2 + frac * h)
    elif side == 'R':
        return (cx + w/2, cy - h/2 + frac * h)
    elif side == 'T':
        return (cx - w/2 + frac * w, cy + h/2)
    else:  # B
        return (cx - w/2 + frac * w, cy - h/2)

def generate_svg():
    lines = []
    
    def L(s):
        lines.append(s)
    
    sw = (max_x - min_x) * scale + 2 * margin
    sh = (max_y - min_y) * scale + 2 * margin
    
    L('<?xml version="1.0" encoding="UTF-8"?>')
    L(f'<svg xmlns="http://www.w3.org/2000/svg"'
      f' width="{sw:.0f}" height="{sh:.0f}"'
      f' viewBox="0 0 {sw:.0f} {sh:.0f}">')
    L('<defs>')
    L('<marker id="dot" viewBox="0 0 6 6" refX="3" refY="3" markerWidth="4" markerHeight="4">')
    L('  <circle cx="3" cy="3" r="2" fill="#333"/>')
    L('</marker>')
    L('</defs>')
    
    L(f'<rect width="100%" height="100%" fill="#ffffff"/>')
    
    # Title
    L(f'<text x="{sw/2:.0f}" y="18" text-anchor="middle"'
      f' font-family="sans-serif" font-size="14" font-weight="bold">'
      f'MykoVolt DevKit v{VERSION} — Schematic Diagram</text>')
    L(f'<text x="{sw/2:.0f}" y="33" text-anchor="middle"'
      f' font-family="sans-serif" font-size="9" fill="#666">'
      f'Generated {datetime.now().strftime("%Y-%m-%d %H:%M")}  |  '
      f'{len(COMPONENTS)} components, {len(NETS)} nets</text>')
    
    # ── Draw net connections as orthogonal routes ──
    power_nets = {"GND", "3.3V"}
    
    # First, non-power nets
    for net_name, connections in NETS:
        if net_name in power_nets:
            continue
        
        # Get component positions for connected pins
        pts = []
        for ref, pin in connections:
            if ref in POS and ref in COMP_PINS:
                pins = COMP_PINS[ref]
                pin_idx = next((i for i, (p, n) in enumerate(pins) if p == pin), -1)
                if pin_idx >= 0:
                    px, py = pin_pos(ref, pin_idx, len(pins))
                    pts.append((px, py, ref, pin))
        
        if len(pts) < 2:
            continue
        
        # Draw connection lines - use orthogonal routing
        # Group by X position for vertical bus, then draw horizontal branches
        color = "#336699"
        
        # Draw a vertical bus line at the average X of first and last point
        bus_x = sum(p[0] for p in pts) / len(pts)
        
        # Find Y range
        ys = [p[1] for p in pts]
        min_y_bus, max_y_bus = min(ys), max(ys)
        if min_y_bus == max_y_bus:
            min_y_bus -= 5
            max_y_bus += 5
        
        # Draw vertical bus
        L(f'<line x1="{to_svg(bus_x, min_y_bus)[0]:.1f}" y1="{to_svg(bus_x, min_y_bus)[1]:.1f}"'
          f' x2="{to_svg(bus_x, max_y_bus)[0]:.1f}" y2="{to_svg(bus_x, max_y_bus)[1]:.1f}"'
          f' stroke="{color}" stroke-width="0.8" fill="none"/>')
        
        # Draw horizontal branches to each component
        for px, py, ref, pin in pts:
            sx, sy = to_svg(px, py)
            bx, by = to_svg(bus_x, py)
            L(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{bx:.1f}" y2="{by:.1f}"'
              f' stroke="{color}" stroke-width="0.6" fill="none"/>')
        
        # Net label on bus
        mid_y = (min_y_bus + max_y_bus) / 2
        lx, ly = to_svg(bus_x + 2, mid_y)
        L(f'<text x="{lx:.1f}" y="{ly:.1f}" font-family="monospace"'
          f' font-size="7" fill="{color}">{xml_escape(net_name[:18])}</text>')
    
    # Draw power nets as symbols
    for net_name, connections in NETS:
        if net_name not in power_nets:
            continue
        color = "#cc3333" if net_name == "GND" else "#339933"
        symbol = "⊥" if net_name == "GND" else "+3.3V"
        
        drawn = set()
        for ref, pin in connections:
            if ref in POS and ref not in drawn:
                drawn.add(ref)
                x, y = POS[ref]
                cx, cy, w, h = COMP_BOX.get(ref, (x, y, 12, 8))
                # Place power symbol near component bottom (GND) or top (3.3V)
                if net_name == "GND":
                    sx, sy = to_svg(cx, cy - h/2 - 6)
                else:
                    sx, sy = to_svg(cx, cy + h/2 + 6)
                L(f'<text x="{sx:.1f}" y="{sy:.1f}" text-anchor="middle"'
                  f' font-family="sans-serif" font-size="8" font-weight="bold" fill="{color}">'
                  f'{symbol}</text>')
    
    # ── Draw components ──
    for ref, (cx, cy, w, h) in COMP_BOX.items():
        x, y = to_svg(cx, cy)
        val = get_value(ref)
        cat = "ic" if ref in IC_REFS else \
              "res" if ref in RES_REFS else \
              "cap" if ref in CAP_REFS else \
              "ind" if ref in IND_REFS else \
              "conn" if ref in CONN_REFS else \
              "led" if ref in LED_REFS else \
              "dio" if ref in DIO_REFS else \
              "mos" if ref in MOS_REFS else \
              "xtal" if ref in XTAL_REFS else "other"
        
        sw_mm = w * scale / 2
        sh_mm = h * scale / 2
        
        # Colors by category
        colors = {
            "ic": ("#e8f0fe", "#2b5fbd", "#1a237e"),
            "res": ("#fff3e0", "#e65100", "#bf360c"),
            "cap": ("#e8f5e9", "#2e7d32", "#1b5e20"),
            "ind": ("#fce4ec", "#c62828", "#880e4f"),
            "conn": ("#f3e5f5", "#7b1fa2", "#4a148c"),
            "led": ("#fff8e1", "#f9a825", "#f57f17"),
            "dio": ("#e0f7fa", "#00838f", "#006064"),
            "mos": ("#e0f2f1", "#00695c", "#004d40"),
            "xtal": ("#fbe9e7", "#d84315", "#bf360c"),
            "other": ("#f5f5f5", "#616161", "#424242"),
        }
        fill, stroke, text_c = colors.get(cat, ("#f5f5f5", "#666", "#333"))
        
        # Draw component symbol
        if cat == "ic":
            # IC as rectangle with notched top-left (pin 1 indicator)
            L(f'<rect x="{x-sw_mm:.1f}" y="{y-sh_mm:.1f}" width="{2*sw_mm:.1f}" height="{2*sh_mm:.1f}"'
              f' rx="1" ry="1" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>')
            # Pin 1 notch
            L(f'<rect x="{x-sw_mm:.1f}" y="{y+sh_mm-6:.1f}" width="4" height="6"'
              f' fill="{fill}" stroke="{stroke}" stroke-width="0.8"/>')
        elif cat == "res":
            # Resistor as zigzag (or small rectangle)
            L(f'<rect x="{x-sw_mm:.1f}" y="{y-sh_mm:.1f}" width="{2*sw_mm:.1f}" height="{2*sh_mm:.1f}"'
              f' rx="1" ry="1" fill="{fill}" stroke="{stroke}" stroke-width="1"/>')
        elif cat == "cap":
            # Capacitor as two parallel plates
            L(f'<rect x="{x-sw_mm:.1f}" y="{y-sh_mm:.1f}" width="{2*sw_mm:.1f}" height="{2*sh_mm:.1f}"'
              f' rx="1" ry="1" fill="{fill}" stroke="{stroke}" stroke-width="1"/>')
        elif cat == "ind":
            # Inductor as rectangle with fill
            L(f'<rect x="{x-sw_mm:.1f}" y="{y-sh_mm:.1f}" width="{2*sw_mm:.1f}" height="{2*sh_mm:.1f}"'
              f' rx="1" ry="1" fill="{fill}" stroke="{stroke}" stroke-width="1"/>')
        elif cat == "led":
            # LED as rectangle
            L(f'<rect x="{x-sw_mm:.1f}" y="{y-sh_mm:.1f}" width="{2*sw_mm:.1f}" height="{2*sh_mm:.1f}"'
              f' rx="1" ry="1" fill="{fill}" stroke="{stroke}" stroke-width="1"/>')
        elif cat == "conn":
            # Connector as rounded rect
            L(f'<rect x="{x-sw_mm:.1f}" y="{y-sh_mm:.1f}" width="{2*sw_mm:.1f}" height="{2*sh_mm:.1f}"'
              f' rx="2" ry="2" fill="{fill}" stroke="{stroke}" stroke-width="1"/>')
        else:
            L(f'<rect x="{x-sw_mm:.1f}" y="{y-sh_mm:.1f}" width="{2*sw_mm:.1f}" height="{2*sh_mm:.1f}"'
              f' rx="1" ry="1" fill="{fill}" stroke="{stroke}" stroke-width="1"/>')
        
        # Reference label
        L(f'<text x="{x:.1f}" y="{y+3:.1f}" text-anchor="middle"'
          f' font-family="sans-serif" font-size="7" font-weight="bold" fill="{text_c}">'
          f'{xml_escape(ref)}</text>')
        
        # Value label (smaller, below reference)
        if val:
            L(f'<text x="{x:.1f}" y="{y-sh_mm+10:.1f}" text-anchor="middle"'
              f' font-family="sans-serif" font-size="5" fill="#666">'
              f'{xml_escape(val[:14])}</text>')
        
        # Pin labels for ICs
        if cat == "ic" and ref in COMP_PINS:
            pins = COMP_PINS[ref]
            n = len(pins)
            for i, (pin_num, net_name) in enumerate(pins):
                px, py = pin_pos(ref, i, n)
                sx, sy = to_svg(px, py)
                # Pin dot
                L(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="1.5" fill="{stroke}"/>')
                # Pin number
                L(f'<text x="{sx+3:.1f}" y="{sy+1:.1f}" font-family="monospace"'
                  f' font-size="4" fill="#555">{pin_num}</text>')
    
    L('</svg>')
    return "\n".join(lines)


def main():
    svg = generate_svg()
    svg_path = os.path.join(PROJECT_DIR, "mykovolt_devkit_schematic.svg")
    with open(svg_path, "w") as f:
        f.write(svg)
    print(f"Generated SVG: {svg_path} ({len(svg)} bytes)")
    
    # Convert to PDF
    try:
        import cairosvg
        pdf_path = os.path.join(PROJECT_DIR, "mykovolt_devkit_schematic.pdf")
        cairosvg.svg2pdf(bytestring=svg.encode('utf-8'), write_to=pdf_path)
        print(f"Generated PDF: {pdf_path}")
    except ImportError:
        print("cairosvg not available, trying inkscape...")
        try:
            import subprocess
            pdf_path = os.path.join(PROJECT_DIR, "mykovolt_devkit_schematic.pdf")
            subprocess.run(["inkscape", svg_path, "--export-type=pdf",
                          f"--export-filename={pdf_path}"],
                         capture_output=True, timeout=30)
            print(f"Generated PDF: {pdf_path} (via inkscape)")
        except:
            print("Could not convert to PDF")


if __name__ == "__main__":
    main()
