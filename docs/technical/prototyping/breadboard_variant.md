# MykoVolt DevKit — Breadboard Prototype

> Validate the design on a solderless breadboard before committing to PCB fabrication.  
> **Complexity:** Medium (30–40 jumper wires, 2–3 adapter boards)  
> **Estimated cost:** ~€25–35 in parts  
> **Time:** 2–3 evenings

---

## Overview

The PCB DevKit uses tiny SMD packages (QFN, WSON, TSSOP). For breadboarding, we:

1. **Replace SMD ICs** with DIP adapter boards or eval modules
2. **Use through-hole passives** (resistors, capacitors, LEDs)
3. **Wire everything** with standard Dupont jumper wires
4. **Verify** I²C communication, NFC, and capacitance sensing work

```
┌─────────────────────────────────────────────────────────────────┐
│  ┌─────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐          │
│  │Nucleo│   │ BQ25570  │   │ ST25DV04K│   │ MB85RC16 │          │
│  │L011K4│   │ EVM      │   │ SOIC→DIP │   │ SOIC→DIP │          │
│  │(MCU) │   │ (POWER)  │   │ (NFC)    │   │ (FRAM)   │          │
│  └──┬───┘   └────┬─────┘   └────┬─────┘   └────┬─────┘          │
│     │            │              │              │                │
│     ├──── I²C Bus (SCL/SDA) ────┼──────────────┘                │
│     │            │              │                               │
│  ┌──┴───┐   ┌────┴─────┐   ┌───┴────┐                          │
│  │PCF8523│   │ FDC1004  │   │Pressling│                          │
│  │SOIC→DIP│   │WSON→DIP  │   │ (MFC)   │                          │
│  │ (RTC) │   │(CAP SENS)│   │ J2      │                          │
│  └───────┘   └──────────┘   └────────┘                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Substitution Guide

### ICs — SMD to Breadboard

| Ref | SMD Package | Breadboard Option | Source |
|-----|-------------|-------------------|--------|
| **U1** STM32L011F4 | TSSOP-20 | **[Nucleo-L011K4](https://www.st.com/en/evaluation-tools/nucleo-l011k4.html)** — dev board with built-in ST-Link | €10 |
| **U2** BQ25570 | QFN-20 | **[BQ25570EVM](https://www.ti.com/tool/BQ25570EVM)** — evaluation module *or* QFN→DIP adapter | €20 / €3 |
| **U3** ST25DV04K | SOIC-8 | **[SOIC-8 DIP adapter](https://www.adafruit.com/product/1212)** + SOIC-8 chip | €2 |
| **U4** MB85RC16 | SOIC-8 | SOIC-8 DIP adapter + SOIC-8 chip | €3 |
| **U5** PCF8523T | SOIC-8 | **[PCF8523 breakout](https://www.adafruit.com/product/3295)** *or* SOIC-8 adapter | €4 |
| **U6** FDC1004 | WSON-10 | **[WSON→DIP adapter](https://www.digikey.com/en/products/detail?keywords=WSON-10-adapter)** + WSON-10 chip | €5 |

> **Alternative for U1:** Use an **STM32L031K6T6** in TSSOP-20 (similar, more flash) on a TSSOP→DIP adapter if you prefer bare chip.

### Passives — SMD to Through-Hole

| SMD | Through-Hole Substitute |
|-----|------------------------|
| 0603 resistors (R1–R14) | Standard ¼W axial leads |
| 0603 capacitors (C1–C22) | Ceramic disc / MLCC radial |
| 0805 capacitors (C14, C15) | 10µF electrolytic / tantalum |
| CP_Radial supercap (SC1) | **Same** — already through-hole! |
| Inductors L1/L2 | Radial leaded inductors (10µH + 47µH) |
| Crystal X1 | **HC-49S** 32.768kHz through-hole crystal |
| D1 USBLC6-2P6 | Omit for breadboard (TVS not needed) |
| D2 PESD5V0S1UB | Omit for breadboard |
| Q1 SI1308EDL | **2N7000** or **BS170** N-channel MOSFET |

### Connectors

| Ref | PCB | Breadboard |
|-----|-----|------------|
| J1 | 2×5 1.27mm SMD | **2×5 2.54mm pin header** or 4-pin SWD cable |
| J2 | JST PH 2.0mm | **2-pin 2.54mm header** (for pressling MFC) |
| J3 | JST PH 2.0mm | **2-pin 2.54mm header** (aux I²C) |
| J4 | 2×3 1.27mm SMD | **2×3 2.54mm pin header** (sensor electrodes) |

---

## Wiring Diagram

### Power Distribution

```
Pressling MFC (0.3–0.8V)
    │
    ├─[Red]── J2 pin 1 ───────────── BQ25570 VIN_DC (pin 2)
    │
    │  BQ25570
    │  ┌─── VSTOR (pin 19) ─── SC1 (100mF supercap +) ── GND
    │  ├─── LBOOST ─── L1 (10µH) ── BAT
    │  ├─── LBUCK  ─── L2 (47µH) ── VOUT
    │  └─── VOUT (pin 14) ─── 3.3V rail (!)
    │
    3.3V rail (red distribution):
    ├── Nucleo L011K4 VIN pin
    ├── All I²C device VDD pins
    ├── LED1 anode (via Q1 load switch)
    └── Pull-up resistors R1, R2

    GND rail (black distribution):
    ├── All IC GND/VSS pins
    ├── BQ25570 GND
    ├── SC1 (-)
    ├── J2 pin 2
    └── LED cathodes
```

### I²C Bus (white/yellow wires)

```
SCL (Nucleo D15 / PA9):
    ├── ST25DV04K pin 5
    ├── MB85RC16 pin 6
    ├── PCF8523 pin 6
    ├── FDC1004 pin 7
    └── R1 (2.2kΩ) ──┐
                      ├── 3.3V
SDA (Nucleo D14 / PA10):        ┘
    ├── ST25DV04K pin 6
    ├── MB85RC16 pin 5
    ├── PCF8523 pin 5
    ├── FDC1004 pin 8
    └── R2 (2.2kΩ) ──┐
                      └── 3.3V
```

### Debug / SWD (Nucleo built-in)

Nucleo-L011K4 has an **integrated ST-Link** — just connect via USB.  
For bare-chip setups:

```
Nucleo SWD header (CN2)    DevKit SWD (J1)
    VCC     ─────────────────  1  (VCC)
    SWCLK   ─────────────────  2  (SWCLK)
    GND     ─────────────────  3  (GND)
    SWDIO   ─────────────────  4  (SWDIO)
    NRST    ─────────────────  10 (NRST)
```

### Sensor Electrodes (J4)

```
FDC1004 CIN1 (pin 1) ── J4-1 ── probe wire (soil moisture)
FDC1004 CIN2 (pin 2) ── J4-2 ── reference wire
FDC1004 SHLD1 (pin 3) ── J4-3 ── shield (insulated, driven guard)
```

---

## Breadboard Layout (Recommended)

```
                         ┌─────────────────────────┐
                         │     Nucleo-L011K4        │
                         │  ┌───────────────────┐  │
                         │  │ USB-ST-Link       │  │
                         │  └───────────────────┘  │
                         │  D13 D14 D15 3V3 GND    │
                         └──┬──┬──┬────┬───┬───────┘
                            │  │  │    │   │
                    ┌───────┘  │  │    │   └──────────┐
                    │   ┌──────┘  │    └──────────┐   │
                    │   │   ┌─────┘               │   │
                    ▼   ▼   ▼                     ▼   ▼
              ┌─────────────────────────────────────────┐
              │  Breadboard area                        │
              │                                         │
              │  ┌────────┐  ┌────────┐  ┌────────┐     │
              │  │BQ25570 │  │ST25DV04K│  │FDC1004 │     │
              │  │EVM/ADAP│  │SOIC→DIP │  │WSON→DIP│     │
              │  └────────┘  └────────┘  └────────┘     │
              │                                         │
              │  ┌────────┐  ┌────────┐  ┌────────┐     │
              │  │MB85RC16│  │PCF8523 │  │Pressling│     │
              │  │SOIC→DIP│  │SOIC→DIP│  │(J2)    │     │
              │  └────────┘  └────────┘  └────────┘     │
              │                                         │
              │  Resistors/Caps row                     │
              │  ┌─R1──R2──R3──C1──C2──...──C21┐        │
              │  └──────────────────────────────┘        │
              └─────────────────────────────────────────┘
```

---

## Step-by-Step Assembly

### Day 1: Power Supply

1. **Prepare the BQ25570** — solder the QFN-20 chip to a DIP adapter, or use the EVM
2. **Wire the power path:**
   - J2 pin 1 → BQ25570 VIN_DC (pin 2)
   - BQ25570 LBOOST (pin 20) → L1 (10µH) → BAT (GND return)
   - BQ25570 LBUCK (pin 16) → L2 (47µH) → VOUT → 3.3V rail
   - SC1 (100mF) → BQ25570 VSTOR (pin 19)
   - BQ25570 GND → common GND rail
3. **Configure programming resistors** (R3–R10 per schematic)
4. **Test:** Connect a 0.5V source to J2 — meter should show 3.3V on the output

### Day 2: I²C Bus

1. **Solder ICs to DIP adapters** — ST25DV04K, MB85RC16, PCF8523, FDC1004
2. **Wire the I²C bus** (SCL/SDA per diagram above)
3. **Add pull-ups** R1=2.2kΩ, R2=2.2kΩ to 3.3V
4. **Connect Nucleo-L011K4:**
   - D15 (PA9/SCL) → I²C SCL bus
   - D14 (PA10/SDA) → I²C SDA bus
   - 3.3V → I²C VDD (all devices)
   - GND → common GND
5. **Test:** Run `i2cdetect -y 0` from a Raspberry Pi or use the Nucleo firmware to scan addresses — should see `0x50 0x51 0x52 0x53`

### Day 3: Sensors + NFC

1. **Connect sensor electrodes** to J4:
   - J4-1 → probe wire (copper strip or screw in soil)
   - J4-2 → reference wire (same length, insulated tip)
   - J4-3 → shield (drain wire surrounding CIN1)
2. **NFC antenna** — solder a 3-turn 30×20mm rectangular coil (PCB trace substitute) to ST25DV04K RF1/RF2 via C20 (47pF)
3. **LED indicators** — wire LED1 + R13 (330Ω) to Q1 drain, LED2 + R14 to Nucleo D12
4. **Test NFC:** Hold a smartphone against the antenna — should detect the tag

### Day 4: Firmware Flash + Verify

```bash
# Build firmware
cd firmware
mkdir -p build && cd build
cmake .. -DCMAKE_TOOLCHAIN_FILE=../cmake/arm-gcc-toolchain.cmake
make -j4

# Flash via Nucleo ST-Link
openocd -f interface/stlink.cfg -f target/stm32l0.cfg \
  -c "program mykovolt_firmware.hex verify reset exit"

# Verify I²C scan (via UART on Nucleo virtual COM port)
screen /dev/ttyACM0 115200
# Expected output:
#   FDC1004 ID: 0x1004
#   ST25DV04K IC ref: 0x24
#   Moisture: 12.34 pF
```

---

## Bill of Materials (Breadboard)

| Item | Qty | € Each | Total |
|------|-----|--------|-------|
| Nucleo-L011K4 | 1 | €10.00 | €10.00 |
| BQ25570EVM or QFN→DIP adapter | 1 | €20.00 / €3.00 | €3.00 |
| SOIC-8 DIP adapters (pack of 10) | 1 | €5.00 | €5.00 |
| WSON-10 DIP adapter | 1 | €3.00 | €3.00 |
| ST25DV04K (SOIC-8) | 1 | €1.50 | €1.50 |
| MB85RC16 (SOIC-8) | 1 | €2.00 | €2.00 |
| PCF8523T (SOIC-8) | 1 | €1.50 | €1.50 |
| FDC1004 (WSON-10) | 1 | €3.00 | €3.00 |
| ¼W resistors (assorted) | 14 | €0.10 | €1.40 |
| Ceramic caps (assorted) | 24 | €0.15 | €3.60 |
| 100mF supercap (SC1) | 1 | €2.00 | €2.00 |
| 10µH + 47µH inductors | 2 | €0.50 | €1.00 |
| 32.768kHz crystal HC-49S | 1 | €0.50 | €0.50 |
| LEDs + 2N7000 MOSFET | 3 | €0.30 | €0.90 |
| Pin headers + wires | 1 | €3.00 | €3.00 |
| Breadboard + jumper pack | 1 | €5.00 | €5.00 |
| **Total** | | | **€46.40** |

> **Saving tip:** If you already have a breadboard, jumper wires, and passives, the cost drops to **~€25** for just the ICs and adapters.

---

## Differences from PCB DevKit

| Feature | PCB DevKit | Breadboard Prototype |
|---------|------------|---------------------|
| MCU | STM32L011F4 (TSSOP-20) | Nucleo-L011K4 dev board |
| Debug | SWD header (J1) | Built-in ST-Link (USB) |
| Power | BQ25570 + SC1 | Same (on adapter) |
| NFC | PCB antenna coil | 3-turn hand-wound coil |
| Sensor | PCB interdigital electrodes | Wire probes |
| Capacitors | 0603 SMD | Through-hole ceramic |
| Size | 30×20mm PCB | ~200×150mm breadboard |
| Cost (qty=1) | ~€15 (PCB+assembly) | ~€25–46 |
| Time to build | 2–3 weeks (fab) | 2–3 evenings |
| Reconfigurable | No | Yes (move wires) |

---

## Verification Checklist

- [ ] **Power:** BQ25570 outputs stable 3.3V from pressling input (0.3–0.8V)
- [ ] **I²C scan:** All 4 devices respond at expected addresses
- [ ] **RTC:** PCF8523 reports correct time/date
- [ ] **FRAM:** MB85RC16 survives write/read cycle across power cycle
- [ ] **NFC:** Smartphone detects ST25DV04K tag, reads temperature/moisture
- [ ] **Cap sensor:** FDC1004 CIN1 capacitance changes when touching probe
- [ ] **LED1:** Lights when load switch (Q1) is enabled
- [ ] **LED2:** Blinks in sync with measurement cycle
- [ ] **Sleep:** Current drops to <10µA in STOP mode
- [ ] **UART:** Debug output on virtual COM port
