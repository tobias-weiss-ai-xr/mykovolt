# MykoVolt DevKit — KiCad Project

> **Open with:** KiCad 8+  
> **Board:** 30×20 mm, 4-layer, ENIG  
> **Path:** `hardware/kicad/mykovolt_devkit.kicad_pro`

---

## Quick Start

```bash
kicad hardware/kicad/mykovolt_devkit.kicad_pro
```

## Project Structure

| File | Content |
|------|---------|
| `mykovolt_devkit.kicad_pro` | Project file — design rules, layer stack, net classes |
| `mykovolt_devkit.kicad_sch` | Schematic — 50 components placed, ready for wiring |
| `mykovolt_devkit.kicad_pcb` | PCB — board outline, layer stack, component footprints |
| `mykovolt_devkit.net` | Plain-text netlist — 34 nets, 126 connections |
| `generate_kicad.py` | Python generator — re-creates all project files |

## Schematic

Opens with 50 components placed in functional groups:

| Group | Components | Position |
|-------|-----------|----------|
| Power | BQ25570, L1, C21, R3–R8, Q1, J2 | Left |
| MCU | STM32L011, X1, C16, C17, R11, R12 | Center |
| I²C Bus | MB85RC16, PCF8523, FDC1004, R1, R2 | Center-right |
| NFC | ST25DV04K, C20 | Right |
| LEDs + Debug | LED1, LED2, R13, R14, J1 | Top/edges |

**What you need to do in KiCad:**
1. Wire components using the netlist as a guide (34 nets)
2. Add power symbols (GND, +3.3V) 
3. Annotate schematic (Tools → Annotate Schematic)
4. Assign footprints (Tools → Assign Footprints)
5. Run ERC (Electrical Rules Check)

## PCB Layout

The board outline (30×20 mm, Edge.Cuts layer) and stack-up are pre-configured.

| Layer | Type | Thickness | Notes |
|-------|------|-----------|-------|
| F.Cu | Signal | 0.035 mm | NFC antenna, components |
| In1.Cu | GND plane | 0.035 mm | Solid pour, cutout under antenna |
| In2.Cu | Power plane | 0.035 mm | 3.3V + analog shield split |
| B.Cu | Signal | 0.035 mm | Interdigital electrodes, test points |

### Design Rules (pre-configured in .kicad_pro)

| Rule | Value |
|------|-------|
| Min clearance | 0.3 mm |
| Min track width | 0.3 mm |
| Min via diameter | 0.6 mm |
| Min via drill | 0.3 mm |
| Default trace | 0.3 mm |
| Default clearance | 0.2 mm |

### PCB Layout Checklist

- [ ] Route I²C bus (SCL + SDA) — keep traces short, equal length
- [ ] Route BQ25570 switching path — L1 < 5mm from IC, no vias
- [ ] Route NFC antenna feed — keep 50 Ω impedance, no GND below
- [ ] Route FDC1004 CIN1 — trace < 20 mm, shield on L3
- [ ] Add GND copper pour on L2 (with antenna keep-out)
- [ ] Add 3.3V copper pour on L3
- [ ] Place 9 thermal vias under BQ25570 exposed pad
- [ ] Add via fence around sensor electrodes
- [ ] Run DRC (Design Rules Check)
- [ ] Generate Gerbers for JLCPCB (ENIG finish)

## Netlist Reference

Key nets (full list in `mykovolt_devkit.net`):

| Net | Connections |
|-----|-------------|
| GND | All ICs, capacitors, J2 pin 2, LEDs |
| 3.3V | All ICs VDD, pull-ups, Q1 drain |
| V_PRESSLING | J2 pin 1 → BQ25570 VIN_DC |
| I2C1_SCL | U1.6 → U3.5 → U4.6 → U5.6 → U6.7 |
| I2C1_SDA | U1.7 → U3.6 → U4.5 → U5.5 → U6.8 |
| SWDIO | U1.3 → J1.4, R11 series 22Ω |
| SWCLK | U1.4 → J1.2, R12 series 100Ω |
| NRST | U1.5 → J1.10, R5 pull-up, C18 |
| CIN1 | U6.1 → interdigital electrodes (L4) |
| NFC_RF1/RF2 | U3.2/U3.3 → NFC antenna, C20 |

## I²C Address Map

| Device | Address | Notes |
|--------|---------|-------|
| ST25DV04K | 0x53 | ADDR pin → GND |
| MB85RC16 | 0x50 | A0/A1 → GND |
| FDC1004 | 0x51 | ADDR → VDD via 10kΩ |
| PCF8523 | 0x52 | ADDR → 10kΩ to VDD |

## BOM Reference

Full BOM with Mouser SKUs and prices: `../../docs/hardware/shopping_list.md`

## Generating from Scratch

```bash
# Re-generate all KiCad files from Python
python3 hardware/kicad/generate_kicad.py

# This overwrites: .kicad_pro, .kicad_sch, .kicad_pcb, .net
```

---

*Layout SVG reference: `../../docs/hardware/sensor_board_layout.svg`*  
*Full design doc: `../../docs/hardware/sensor_board_design.md`*
