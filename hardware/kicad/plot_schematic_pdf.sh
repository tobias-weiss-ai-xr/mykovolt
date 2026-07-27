#!/bin/bash
# Plot schematic to PDF using KiCad eeschema via xvfb + xdotool automation
set -e

SCHEMATIC="/home/weissto_local/git/mykovolt/hardware/kicad/mykovolt_devkit.kicad_sch"
OUTPUT_DIR="/home/weissto_local/git/mykovolt/hardware/kicad/"

echo "Starting eeschema with xvfb..."

xvfb-run -a -s "-screen 0 1280x1024x24" bash <<'SCRIPT'
  # Start eeschema
  eeschema "$SCHEMATIC" &
  PID=$!
  
  # Wait for window to appear
  sleep 3
  
  # Find the eeschema window
  WID=$(xdotool search --sync --name "Eeschema" 2>/dev/null | tail -1)
  echo "Window ID: $WID"
  
  if [ -z "$WID" ]; then
    echo "ERROR: Could not find eeschema window"
    kill $PID 2>/dev/null
    exit 1
  fi
  
  # Activate window
  xdotool windowactivate "$WID"
  sleep 1
  
  # File → Plot (Alt+F, then arrow down to Plot, or use menu accelerator)
  # In KiCad 6, the plot dialog can be opened via keyboard: Alt+F, P
  xdotool key --window "$WID" --delay 200 alt+f p
  sleep 2
  
  # Now in the Plot dialog
  # Find the plot dialog window
  PLOT_WID=$(xdotool search --sync --name "Plot" 2>/dev/null | tail -1)
  echo "Plot dialog: $PLOT_WID"
  
  if [ -z "$PLOT_WID" ]; then
    echo "ERROR: Could not find Plot dialog"
    kill $PID 2>/dev/null
    exit 1
  fi
  
  xdotool windowactivate "$PLOT_WID"
  sleep 1
  
  # Tab to output directory field and set it
  # Or just use the default and change it later
  
  # Select PDF format - in the Plot dialog, there's a dropdown for format
  # Tab to the format dropdown and select PDF
  # This is fragile, let's try pressing Alt+F to open format dropdown then typing PDF
  
  # Actually, let's try a different approach: use the "Plot" button directly
  # The Plot button should have keyboard accelerator
  xdotool key --window "$PLOT_WID" --delay 100 alt+p
  sleep 2
  
  # Press Enter to confirm any dialogs
  xdotool key --delay 100 Return
  sleep 2
  
  # Close eeschema
  kill $PID 2>/dev/null
  wait $PID 2>/dev/null
  echo "Done"
SCRIPT

# Check what was generated
echo "Output files in $OUTPUT_DIR:"
ls -la "$OUTPUT_DIR"/*.pdf 2>/dev/null || echo "No PDF files found"
