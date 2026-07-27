#!/usr/bin/env python3
"""Generate a professional-looking schematic SVG/PDF from the MykoVolt DevKit component data."""

import os, sys, math
from datetime import datetime
from xml.sax.saxutils import escape as xml_escape

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)
from generate_kicad import COMPONENTS, NETS, POS, VERSION

# Component categories for color coding
IC_REFS = {"U1", "U2", "U3", "U4", "U5", "U6"}
PASSIVE_REFS = {"R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "R11", "R12", "R13", "R14",
                "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "C11", "C12", "C13",
                "C14", "C15", "C16", "C17", "C18", "C19", "C20", "C21", "C22"}
CONNECTOR_REFS = {"J1", "J2", "J3"}
OTHER_REFS = {"X1", "Q1", "LED1", "LED2", "SC1", "D1", "D2", "L1", "L2"}

def get_component_value(ref):
    for cr, cv, fp, ds, sym in COMPONENTS:
        if cr == ref:
            return cv
    return ""

def get_component_category(ref):
    if ref in IC_REFS: return "ic"
    if ref in PASSIVE_REFS: return "passive"
    if ref in CONNECTOR_REFS: return "connector"
    return "other"

def generate_svg():
    # Find bounding box
    xs = [pos[0] for pos in POS.values()]
    ys = [pos[1] for pos in POS.values()]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    
    # Add padding (mm)
    pad = 30
    min_x -= pad
    max_x += pad
    min_y -= pad
    max_y += pad
    
    # SVG viewport - use a reasonable size
    svg_width = max_x - min_x
    svg_height = max_y - min_y
    
    # Scale to fit nicely
    # Use mm directly (1mm = 3.779px at 96dpi, but we'll use real mm)
    # SVG uses px by default, let's use mm for simplicity
    scale = 3.779  # px per mm (roughly 96dpi)
    
    w_px = svg_width * scale + 40
    h_px = svg_height * scale + 40
    
    def to_svg(x, y):
        """Convert schematic mm to SVG px (with y flipped)."""
        sx = (x - min_x) * scale + 20
        sy = (max_y - y) * scale + 20  # flip Y
        return sx, sy
    
    lines = []
    lines.append(f'<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg"'
                 f' width="{w_px:.0f}" height="{h_px:.0f}"'
                 f' viewBox="0 0 {w_px:.0f} {h_px:.0f}">')
    
    # Background
    lines.append(f'<rect width="100%" height="100%" fill="#ffffff"/>')
    
    # Title
    lines.append(f'<text x="{w_px/2:.0f}" y="15" text-anchor="middle" '
                 f'font-family="Arial, sans-serif" font-size="12" font-weight="bold">'
                 f'MykoVolt DevKit v{VERSION} — Schematic</text>')
    lines.append(f'<text x="{w_px/2:.0f}" y="28" text-anchor="middle" '
                 f'font-family="Arial, sans-serif" font-size="8" fill="#666">'
                 f'Generated {datetime.now().strftime("%Y-%m-%d %H:%M")}</text>')
    
    # Draw net connections
    used_nets = set()
    for net_name, connections in NETS:
        if net_name in ("GND", "3.3V"):
            continue  # Skip power nets for line drawing
        
        # Collect positions
        pts = []
        for ref, pin in connections:
            if ref in POS:
                x, y = POS[ref]
                # Offset by pin number to spread connections
                pin_num = int(pin) if pin.isdigit() else 0
                ox = (pin_num % 5 - 2) * 4
                oy = (pin_num % 3 - 1) * 4
                pts.append((x + ox, y + oy, ref, pin))
        
        if len(pts) >= 2:
            # Draw lines in a star-like pattern from first component
            sx, sy = to_svg(pts[0][0], pts[0][1])
            for i in range(1, len(pts)):
                ex, ey = to_svg(pts[i][0], pts[i][1])
                lines.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}"'
                             f' stroke="#4488cc" stroke-width="0.5" fill="none" opacity="0.6"/>')
            
            # Net label
            if net_name not in used_nets:
                used_nets.add(net_name)
                lines.append(f'<text x="{sx+2:.1f}" y="{sy+1:.1f}" '
                             f'font-family="monospace" font-size="3" fill="#4488cc">'
                             f'{xml_escape(net_name[:18])}</text>')
    
    # Draw power nets (GND and 3.3V) as labels near components
    for net_name, connections in NETS:
        color = "#cc3333" if net_name == "GND" else "#33aa33"
        label = "⊥" if net_name == "GND" else "+3.3V"
        
        drawn_refs = set()
        for ref, pin in connections:
            if ref in POS and ref not in drawn_refs:
                drawn_refs.add(ref)
                x, y = POS[ref]
                sx, sy = to_svg(x, y - 10)
                lines.append(f'<text x="{sx:.1f}" y="{sy:.1f}" '
                             f'font-family="Arial" font-size="3.5" fill="{color}" text-anchor="middle">'
                             f'{label}</text>')
    
    # Draw components
    for ref, (x, y) in sorted(POS.items(), key=lambda kv: kv[0]):
        sx, sy = to_svg(x, y)
        value = get_component_value(ref)
        cat = get_component_category(ref)
        
        # Component size
        box_w, box_h = 16, 10
        
        # Color based on category
        colors = {
            "ic": ("#e8f0fe", "#3a7bd5"),
            "passive": ("#fff3e0", "#e65100"),
            "connector": ("#e8f5e9", "#2e7d32"),
            "other": ("#f3e5f5", "#7b1fa2"),
        }
        fill, stroke = colors.get(cat, ("#f5f5f5", "#666"))
        
        # Draw component box
        lines.append(f'<rect x="{sx-box_w/2:.1f}" y="{sy-box_h/2:.1f}" '
                     f'width="{box_w:.1f}" height="{box_h:.1f}" '
                     f'rx="2" ry="2" fill="{fill}" stroke="{stroke}" stroke-width="0.8"/>')
        
        # Draw reference
        lines.append(f'<text x="{sx:.1f}" y="{sy+1.5:.1f}" text-anchor="middle" '
                     f'font-family="Arial, sans-serif" font-size="3.5" font-weight="bold" fill="{stroke}">'
                     f'{xml_escape(ref)}</text>')
        
        # Draw value
        if value:
            lines.append(f'<text x="{sx:.1f}" y="{sy+box_h/2-1:.1f}" text-anchor="middle" '
                         f'font-family="Arial, sans-serif" font-size="2.5" fill="#666">'
                         f'{xml_escape(value[:14])}</text>')
    
    lines.append('</svg>')
    return "\n".join(lines)

def main():
    svg_content = generate_svg()
    svg_path = os.path.join(PROJECT_DIR, "mykovolt_devkit_schematic.svg")
    with open(svg_path, "w") as f:
        f.write(svg_content)
    print(f"  Generated {svg_path} ({len(svg_content)} bytes)")
    
    # Convert SVG to PDF using CairoSVG
    try:
        import cairosvg
        pdf_path = os.path.join(PROJECT_DIR, "mykovolt_devkit_schematic.pdf")
        cairosvg.svg2pdf(bytestring=svg_content.encode('utf-8'), write_to=pdf_path)
        print(f"  Generated {pdf_path}")
    except ImportError:
        print("  cairosvg not available, skipping PDF conversion")
        try:
            import subprocess
            pdf_path = os.path.join(PROJECT_DIR, "mykovolt_devkit_schematic.pdf")
            subprocess.run(["inkscape", svg_path, "--export-type=pdf", 
                          f"--export-filename={pdf_path}"], 
                         capture_output=True, timeout=30)
            print(f"  Generated {pdf_path} (via inkscape)")
        except:
            print("  Could not convert SVG to PDF (no cairosvg or inkscape)")
    
    return svg_path

if __name__ == "__main__":
    import sys
    main()
