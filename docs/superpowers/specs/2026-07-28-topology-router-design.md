# Topology-Driven Grid Autorouter — MykoVolt DevKit PCB

## Problem

`_route_critical_nets()` in `generate_kicad.py` is a 200-line function with ~2000 hand-coded nanometer coordinates. Every track start/end is hardcoded per component position. If any component moves, all routing breaks. The `route_L` helper exists but is only used for a few nets. The `pad_pos()` estimator is a crude heuristic that doesn't read actual footprint pad positions.

## Architecture

A dedicated `TopologyRouter` class in `hardware/kicad/topology_router.py`:

```
                      ┌──────────────────────┐
                      │  Component Positions  │
                      │  + Footprint Pads     │
                      └──────┬───────────────┘
                             │
                             ▼
                      ┌──────────────────────┐
                      │  Obstacle Grid        │
                      │  (300×200 @ 0.1mm)    │
                      └──────┬───────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  I2C Daisy-   │   │  Power Path   │   │  Signal P2P   │
│  Chain Router │   │  Router       │   │  Router       │
│  (trunk+drops)│   │  (wide trace) │   │  (A* maze)    │
└───────────────┘   └───────────────┘   └───────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             ▼
                      ┌──────────────────────┐
                      │  Track Segment Gen    │
                      │  → KiCad pcbnew API   │
                      └──────────────────────┘
```

## Components

### 1. Obstacle Grid (`GridMap`)

- 0.1mm resolution → 300×200 cells for 30×20mm board
- Each cell: FREE, OBSTACLE (component body), KEEPOUT (antenna zone), TRACK (already routed)
- Component obstacle = bounding box from footprint pads + 0.3mm clearance margin
- Board edge = obstacle on Edge.Cuts + 0.5mm margin

### 2. Net Class Strategies

| Net Class | Strategy | Trace Width | Layer | Notes |
|-----------|----------|-------------|-------|-------|
| `I2C_BUS` | Daisy-chain trunk + drops | 0.3mm | F.Cu | Trunk between extreme stops, vertical drops |
| `POWER_BUS` | Point-to-point wide | 0.5mm | F.Cu | VSTOR, LBOOST, LBUCK, V_PRESSLING |
| `POWER_SIG` | Point-to-point | 0.3mm | F.Cu | BQ25570 programming nets, V_SENSE |
| `SIGNAL` | A* maze route | 0.3mm | F.Cu | SWD, UART, control signals |
| `XTAL` | Short direct | 0.3mm | F.Cu | Crystal with guard trace |
| `NFC_ANTENNA` | Spiral coil generator | 0.3mm | F.Cu | Kept as existing `_add_nfc_antenna` |
| `SENSOR_ELEC` | Interdigital pattern | 0.3mm | B.Cu | Kept as existing `_add_sensor_electrodes` |

### 3. Daisy-Chain Router (for I2C)

1. Collect all stops (component + pin) in net
2. Sort stops by X coordinate
3. Draw horizontal trunk at median Y of all stops
4. For each stop, draw vertical drop from trunk to pin position
5. Pull-up resistors: tap into trunk with short stub

### 4. A* Maze Router (for signals)

- Heuristic: Manhattan distance
- Cost function: `g = length + 10 * via_count + 100 * obstacle_proximity`
- Neighbors: 4-directional (no diagonals to keep Manhattan routing)
- After routing, convert path to track segments (compress collinear points)

### 5. Net Routing Order (priority)

1. NFC antenna + sensor electrodes (geometry generators, untouched)
2. Power nets (VSTOR, LBOOST, LBUCK, V_PRESSLING) — wide traces
3. I2C bus (SCL, SDA) — daisy-chain
4. Crystal oscillator (XTAL_IN, XTAL_OUT) — short, direct
5. Control signals (NFC_IRQ, RTC_INT, SENSOR_RDY, VBAT_OK, etc.)
6. Debug (SWDIO, SWCLK, NRST, UART)
7. LEDs and remaining signals

After each net is routed, its tracks are added to the obstacle grid so subsequent nets route around them.

## Pad Position Resolution

Replace `pad_pos()` heuristic with actual footprint pad reading:

- For components loaded via `FootprintLoad`: iterate `fp.Pads()`, match by pad number
- For placeholder footprints: use estimated position from PCB_POS ± 1mm offset based on pin side (left: odd pins, right: even pins)

## Integration with `generate_kicad.py`

- `_route_critical_nets()` → delegate to `TopologyRouter.route_all(netcode_map)`
- `_add_nfc_antenna()` and `_add_sensor_electrodes()` remain unchanged (special geometry)
- `_add_power_vias()` remains unchanged
- New file: `topology_router.py`

## Testing

- Existing tests in `test_hardware_generation.py` and `test_pcb_drc.py` must pass
- New tests in `test_topology_router.py` for:
  - Grid obstacle construction from component positions
  - Daisy-chain trunk computation
  - A* finds path in open space
  - A* avoids obstacles
  - All nets route without overlapping tracks
  - Deterministic output (same inputs → same routing)