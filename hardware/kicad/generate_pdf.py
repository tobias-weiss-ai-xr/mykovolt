#!/usr/bin/env python3
"""Generate PDFs of the MykoVolt DevKit from the generated KiCad files."""

import os, sys, math
from datetime import datetime

# Add the project directory to path
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)

# Import the generator data
from generate_kicad import COMPONENTS, NETS, POS, PCB_POS, VERSION

# Try to use fpdf2 for PDF, fall back to reportlab
try:
    from fpdf import FPDF
    HAVE_FPDF = True
except ImportError:
    HAVE_FPDF = False

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    HAVE_REPORTLAB = True
except ImportError:
    HAVE_REPORTLAB = False

def generate_schematic_pdf_python():
    """Generate a schematic PDF using pure Python rendering via reportlab."""
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import mm
    from reportlab.lib.colors import HexColor, black, red, blue, green
    
    output_path = os.path.join(PROJECT_DIR, f"mykovolt_devkit_schematic.pdf")
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4  # 595.27 x 841.89 points
    
    # Title block
    c.setFont("Helvetica-Bold", 14)
    c.drawString(20 * mm, height - 15 * mm, f"MykoVolt DevKit v{VERSION} — Schematic")
    c.setFont("Helvetica", 8)
    c.drawString(20 * mm, height - 20 * mm, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Scale and offset to fit the schematic on the page
    # Convert mm coordinates (from POS) to points on A4
    # We'll place the schematic in a viewport with some margin
    margin = 20  # mm
    view_w = (210 - 2 * margin)  # mm available width
    view_h = (297 - 2 * margin)  # mm available height
    
    # Find bounding box of all components
    min_x, max_x = float('inf'), float('-inf')
    min_y, max_y = float('inf'), float('-inf')
    for ref, (x, y) in POS.items():
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)
    
    # Add padding
    pad = 20  # mm
    min_x -= pad
    max_x += pad
    min_y -= pad
    max_y += pad
    
    # Calculate scale to fit
    scale_x = view_w / (max_x - min_x) if max_x > min_x else 1
    scale_y = view_h / (max_y - min_y) if max_y > min_y else 1
    scale = min(scale_x, scale_y)
    
    # Center the schematic
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    
    def to_points(x_mm, y_mm):
        """Convert schematic mm coordinates to page points."""
        px = (x_mm - center_x) * scale + (width / 2)
        py = (height / 2) - (y_mm - center_y) * scale
        return px, py
    
    # Draw component symbols as boxes with labels
    c.setFont("Helvetica", 6)
    
    for ref, (x, y) in sorted(POS.items(), key=lambda kv: kv[0]):
        px, py = to_points(x, y)
        comp_size = 8 * scale
        
        # Find component value
        value = ""
        for cr, cv, fp, ds, sym in COMPONENTS:
            if cr == ref:
                value = cv
                break
        
        # Draw component box
        c.setStrokeColor(black)
        c.setFillColor(HexColor('#F0F0F0'))
        c.roundRect(px - comp_size, py - comp_size, comp_size * 2, comp_size * 2, 2, fill=1, stroke=1)
        
        # Draw reference
        c.setFont("Helvetica-Bold", 6)
        c.drawCentredString(px, py + 2, ref)
        
        # Draw value
        c.setFont("Helvetica", 5)
        c.drawCentredString(px, py - 4, value[:12])
    
    # Draw net connections (as lines between components)
    c.setStrokeColor(HexColor('#4040FF'))
    c.setLineWidth(0.3)
    
    for net_name, connections in NETS:
        if net_name in ("GND", "3.3V"):
            continue  # Skip power nets for clarity
        
        # Get positions for each connected pin
        points = []
        for ref, pin in connections:
            if ref in POS:
                x, y = POS[ref]
                # Offset pin position slightly based on pin number
                dx = (int(pin) % 4 - 1.5) * 3
                dy = (int(pin) % 3 - 1) * 3
                points.append((ref, x + dx, y + dy))
        
        # Draw lines between consecutive points
        if len(points) >= 2:
            for i in range(len(points) - 1):
                p1 = to_points(points[i][1], points[i][2])
                p2 = to_points(points[i+1][1], points[i+1][2])
                c.line(p1[0], p1[1], p2[0], p2[1])
        
        # Draw net label near the first point
        if points:
            p = to_points(points[0][1], points[0][2])
            c.setFont("Helvetica", 4)
            c.setFillColor(HexColor('#4040FF'))
            c.drawString(p[0] + 2, p[1] + 1, net_name[:15])
            c.setFillColor(black)
    
    # Draw power nets (GND and 3.3V) with symbols
    for net_name, connections in NETS:
        if net_name not in ("GND", "3.3V"):
            continue
        
        for ref, pin in connections:
            if ref in POS:
                x, y = POS[ref]
                px, py = to_points(x, y)
                c.setFont("Helvetica", 4)
                c.setFillColor(red if net_name == "GND" else green)
                if net_name == "GND":
                    c.line(px - 3, py - comp_size - 3, px + 3, py - comp_size - 3)
                    c.line(px, py - comp_size + 1, px, py - comp_size - 3)
                else:
                    c.drawString(px + 3, py + comp_size + 2, f"+{net_name}")
                c.setFillColor(black)
    
    c.save()
    print(f"  Generated {output_path}")
    return output_path

def generate_pcb_pdf_pcbnew():
    """Generate PCB PDF using pcbnew's PLOT_CONTROLLER."""
    from pcbnew import LoadBoard, PLOT_CONTROLLER, PLOT_FORMAT_PDF
    from pcbnew import F_Cu, In1_Cu, In2_Cu, B_Cu
    from pcbnew import F_SilkS, B_SilkS, F_Mask, B_Mask, Edge_Cuts
    from pcbnew import F_Fab, B_Fab, F_CrtYd, B_CrtYd
    
    pcb_path = os.path.join(PROJECT_DIR, "mykovolt_devkit.kicad_pcb")
    board = LoadBoard(pcb_path)
    
    plotter = PLOT_CONTROLLER(board)
    opts = plotter.GetPlotOptions()
    opts.SetOutputDirectory(PROJECT_DIR)
    opts.SetPlotFrameRef(False)
    opts.SetPlotValue(True)
    opts.SetPlotReference(True)
    opts.SetPlotInvisibleText(False)
    opts.SetAutoScale(True)
    opts.SetScale(1)
    opts.SetUseAuxOrigin(True)
    opts.SetNegative(False)
    opts.SetSkipPlotNPTH_Pads(False)
    opts.SetExcludeEdgeLayer(False)
    opts.SetPlotMode(True)
    
    plotter.OpenPlotfile("mykovolt_devkit_pcb", PLOT_FORMAT_PDF, "MykoVolt DevKit v0.1")
    
    layers = [
        (F_Cu, "F.Cu"), (In1_Cu, "In1.Cu"), (In2_Cu, "In2.Cu"), (B_Cu, "B.Cu"),
        (F_SilkS, "F.SilkS"), (B_SilkS, "B.SilkS"),
        (F_Mask, "F.Mask"), (B_Mask, "B.Mask"),
        (Edge_Cuts, "Edge.Cuts"),
        (F_Fab, "F.Fab"), (B_Fab, "B.Fab"),
    ]
    
    for layer_id, name in layers:
        plotter.SetLayer(layer_id)
        try:
            plotter.PlotLayer()
        except:
            pass
    
    plotter.ClosePlot()
    
    # Rename to clean filename
    default_name = os.path.join(PROJECT_DIR, "mykovolt_devkit_pcb-mykovolt_devkit_pcb.pdf")
    clean_name = os.path.join(PROJECT_DIR, "mykovolt_devkit_pcb.pdf")
    if os.path.exists(default_name):
        os.rename(default_name, clean_name)
    
    print(f"  Generated {clean_name}")
    return clean_name


def main():
    print(f"=== MykoVolt DevKit v{VERSION} — PDF Generator ===\n")
    
    print("Generating PCB PDF (via pcbnew)...")
    try:
        pcb_pdf = generate_pcb_pdf_pcbnew()
        print(f"  OK: {pcb_pdf}")
    except Exception as e:
        print(f"  Error: {e}")
    
    print("\nGenerating Schematic PDF (via reportlab)...")
    try:
        sch_pdf = generate_schematic_pdf_python()
        print(f"  OK: {sch_pdf}")
    except Exception as e:
        print(f"  Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
