# MykoVolt Sensor Board — Hardware Design & BOM

> **Board:** DevKit v0.1 | **Form Factor:** 30×20 mm, 4-layer PCB | **Status:** Design
> **Open Hardware License:** CERN-OHL-P v2

---

## 1. Board Overview

The sensor board is the electronic heart of the MykoVolt DevKit. It's a **low-power NFC-enabled data acquisition board** designed to be powered by the fungal MFC pressling and read out via any NFC-enabled smartphone.

### 1.1 Key Specifications

| Parameter | Value | Notes |
|-----------|-------|-------|
| Dimensions | 30 × 20 mm | Credit-card stripe size |
| Layers | 4 | Top-GND-PWR-Bottom |
| MCU | STM32L011K4 | 32KB Flash, 8KB RAM, TSSOP-20 |
| Boost converter | BQ25570 | 0.3V start-up, MPPT, 80 nA Iq |
| NFC | ST25DV04K | 4KB EEPROM, I²C, ISO 15693 |
| FRAM | MB85RC16 | 16KB, 10¹³ cycles, I²C |
| RTC | PCF8523 | 150 nA, I²C, century register |
| Capacitive sensor | FDC1004 | 4-ch, ±0.1 fF, I²C |
| Idle power | 1.8 µA | STOP mode, RTC running |
| Measurement | 3.2 mA for 150 ms | Every 15 minutes |
| Daily average | 4.6 µA | @ 15-min interval (0.14 mWh/day) |
| Input voltage | 0.3–0.6 V | From fungal MFC pressling |
| Output voltage | 3.3 V | Regulated rail |
| Operating temp | −10 to +60 °C | Limited by fungal biology |
| NFC read range | 2–5 cm | Depends on phone/reader |

### 1.2 Board Stack-up

| Layer | Material | Thickness | Purpose |
|-------|----------|-----------|---------|
| Top (L1) | 1 oz Cu + ENIG | 35 µm | Components, NFC antenna, FDC electrodes |
| GND (L2) | 1 oz Cu | 35 µm | Solid ground plane, no splits |
| PWR (L3) | 1 oz Cu | 35 µm | 3.3V power plane, analog split |
| Bottom (L4) | 1 oz Cu + ENIG | 35 µm | Components (optional), test points |
| Core | FR-4 | 0.8 mm | Standard 4-layer prepreg |

**Why 4-layer?** The QFN-20 (BQ25570) requires a solid ground plane underneath for thermal dissipation. A 2-layer board would need ground stitching vias that increase noise on the analog sensor reading. The cost difference between 2-layer and 4-layer at JLCPCB is ~€3 → ~€8 for 5 boards — worth it.

---

## 2. Component Selection — Detailed Rationale

### 2.1 MCU: STM32L011K4 (TSSOP-20)

**Alternatives considered:**

| MCU | Flash | RAM | Sleep | Price (100) | Verdict |
|-----|-------|-----|-------|-------------|---------|
| **STM32L011K4** | 32KB | 8KB | 1.8 µA | €1.52 | ✅ **Chosen** |
| ATtiny3217 | 32KB | 2KB | 1.5 µA | €1.20 | ❌ Less RAM, no I²C multi-master |
| nRF52810 | 192KB | 24KB | 1.3 µA | €1.80 | ❌ Overkill, BLE not needed in Phase 1 |
| MSP430FR2155 | 32KB | 2KB FRAM | 0.7 µA | €2.10 | ❌ Proprietary toolchain, fewer community libs |

**Why STM32L011:**
- Lowest power STOP mode (1.8 µA) with RTC running — critical for 7-day operation
- TSSOP-20 is manually solderable (prototype-friendly)
- Extensive HAL/LL library support (STM32Cube)
- I²C multi-master capable (important for NFC + sensor sharing the bus)
- 32KB Flash leaves 40% headroom after firmware + bootloader

### 2.2 Boost Converter: BQ25570 (QFN-20)

**Alternatives considered:**

| Boost IC | Start voltage | Quiescent | MPPT | Price (100) | Verdict |
|----------|--------------|-----------|------|-------------|---------|
| **BQ25570** | 0.3 V | 80 nA | ✅ Yes | €3.20 | ✅ **Chosen** |
| TPS61098 | 0.5 V | 300 nA | ❌ No | €1.05 | ❌ Needs 0.5V input (MFC = 0.45V typical) |
| MAX17220 | 0.4 V | 1.2 µA | ❌ No | €2.80 | ❌ Higher quiescent, no MPPT |
| LTC3105 | 0.25 V | 2.5 µA | ✅ Yes | €4.50 | ❌ Higher quiescent, more expensive |

**Why BQ25570:**
- Start-up voltage of 0.3 V (cold-start) — critical because MFC OCV is 0.3–0.6 V under load
- Integrated MPPT — automatically finds the maximum power point of the fungal MFC (which varies with temperature, age, moisture)
- 80 nA quiescent current — doesn't drain the pressling when system is sleeping
- Battery health monitoring output — can read battery voltage without additional ADC

**BQ25570 design notes:**
- Inductor: 10 µH, 2A saturation (XGL4020-103)
- Input capacitor: 4.7 µF ceramic (minimum for cold-start)
- MPPT ratio set to 80% (typical for MFC — VOC under load is ~80% of OCV)
- Output voltage set to 3.3 V via resistor divider on VOUT_SET

### 2.3 NFC Tag: ST25DV04K (SO-8)

**Alternatives considered:**

| NFC IC | Memory | I²C | Passive power | Price (100) | Verdict |
|--------|--------|-----|---------------|-------------|---------|
| **ST25DV04K** | 4KB | ✅ | ✅ Yes | €0.95 | ✅ **Chosen** |
| NT3H2111 | 1KB | ✅ | ✅ Yes | €1.10 | ❌ Smaller buffer, fewer features |
| M24LR64E-R | 8KB | ✅ | ✅ Yes | €1.50 | ❌ Higher power during I²C, less software support |

**Why ST25DV04K:**
- 4KB EEPROM is large enough for: 672 measurement entries × 6 bytes = 4,032 bytes (Header + data fit exactly)
- Passive power harvesting — the NFC reader powers the communication, zero draw from pressling during readout
- I²C slave interface — MCU writes data to NFC EEPROM, phone reads it via RF
- Fast transfer mode — 3 ms per 256-byte block (full buffer read in <50 ms)

**NFC antenna:**
- PCB trace coil on top layer (L1), 4 turns, 24×14 mm outer, 0.3 mm trace, 0.3 mm spacing
- Inductance: ~2.4 µH
- Tuning capacitor: parallel 47 pF (C0G, ±5%) for resonance at 13.56 MHz
- Q factor: ~15 (optimized for bandwidth, not maximum range)

### 2.4 FRAM: MB85RC16 (SO-8)

**Why FRAM (not EEPROM or Flash):**
- 10¹³ write cycles — EEPROM would wear out in ~2 years at 96 writes/day
- No write delay — writes 512 bytes in <1 ms vs EEPROM's 5 ms/byte
- 40-year data retention — sensor could be retrieved after years
- 16KB allows 14.2 days of logging at 16 bytes/entry, 15-min interval

**Memory allocation:**
```
0x0000–0x00FF (256 B): System header (magic, version, write pointer, config)
0x0100–0x3FFF (16 KB - 256 B): Ring buffer → 1,022 entries × 16 bytes
```

**Ring buffer entry (16 bytes):**
```
Offset  Size  Field         Description
0       4     timestamp     uint32, RTC counter (seconds since epoch)
4       2     capacitance   uint16, FDC1004 raw count
6       2     v_batt        uint16, pressling voltage in mV
8       2     temperature    uint16, 0.1°C resolution
10      2     adc_aux       uint16, auxiliary ADC (e.g., soil moisture second channel)
12      1     flags         uint8 (error, calibration, battery_low, overflow)
13      1     crc_lo        uint8, lower byte of CRC-16
14      2     reserved
```

### 2.5 RTC: PCF8523 (SO-8)

**Why a separate RTC (not the MCU's internal RTC):**
- MCU internal RTC draws 0.5 µA — PCF8523 draws 150 nA
- PCF8523 has century register (year 2000–2099) — MCU RTC doesn't
- Separate RTC allows MCU to fully power down (load switch cuts VDD)
- 150 nA × 3.3 V × 365 days = 0.43 mWh/year — negligible

**Configuration:**
- Interrupt output to MCU wake pin every 15 minutes
- Backup capacitor: 0.47 F supercap (maintains timekeeping for 7 days without power)
- Crystal: 32.768 kHz, ±20 ppm, 12.5 pF load capacitance

### 2.6 Capacitive Sensor: FDC1004 (WSON-10)

**Why capacitive (not resistive or TDR):**
- No moving parts, no galvanic contact with soil (longer life)
- ±0.1 fF resolution → ~0.1% VWC accuracy
- 4 channels: 1 for soil moisture, 1 for reference, 2 spare
- Integrated shield drive — eliminates parasitic capacitance from cable/PCB

**Electrode design:**
- Interdigital fingers on bottom layer (L4), facing the soil
- 10 fingers, 0.3 mm width, 0.3 mm spacing, 15 mm length
- Total active area: ~4.5 × 15 mm
- Shield plane on L3 (under the electrodes) driven by FDC1004 SHLD1 output
- 100 kHz excitation frequency

---

## 3. Full Bill of Materials (BOM)

### 3.1 ICs

| Ref | Part | Package | Qty | Mouser PN | Digikey PN | Price 1pc | Price 100pc |
|-----|------|---------|-----|-----------|------------|-----------|-------------|
| U1 | STM32L011K4 | TSSOP-20 | 1 | 511-STM32L011K4 | 497-17112-ND | €2.15 | €1.52 |
| U2 | BQ25570 | QFN-20 | 1 | 595-BQ25570 | 296-44260-1-ND | €3.95 | €3.20 |
| U3 | ST25DV04K | SO-8 | 1 | 511-ST25DV04K | 497-17909-1-ND | €1.35 | €0.95 |
| U4 | MB85RC16 | SO-8 | 1 | 342-MB85RC16PNF-G | 865-MB85RC16PNF-G-ND | €2.10 | €1.65 |
| U5 | PCF8523 | SO-8 | 1 | 771-PCF8523T/1 | 568-13493-1-ND | €0.75 | €0.52 |
| U6 | FDC1004 | WSON-10 | 1 | 595-FDC1004DSC | 296-40394-1-ND | €3.15 | €2.55 |
| | | | **6 ICs** | | | **€13.45** | **€10.39** |

### 3.2 Passives (0603 size, unless noted)

| Ref | Value | Qty | Mouser PN | Price 100pc | Line Total |
|-----|-------|-----|-----------|-------------|------------|
| C1–C10 | 100 nF, X7R, 16V | 10 | 81-GRM188R71C104K | €0.008 | €0.080 |
| C11–C13 | 1 µF, X5R, 10V | 3 | 81-GRM188R61A105K | €0.015 | €0.045 |
| C14–C15 | 10 µF, X5R, 6.3V | 2 | 81-GRM188R60J106K | €0.025 | €0.050 |
| C16–C17 | 22 pF, C0G, 50V | 2 | 81-GRM1885C1H220J | €0.008 | €0.016 |
| C18–C19 | 100 pF, C0G, 50V | 2 | 81-GRM1885C1H101J | €0.008 | €0.016 |
| C20 | 47 pF, C0G, 50V | 1 | 81-GRM1885C1H470J | €0.008 | €0.008 |
| R1–R5 | 10 kΩ, 1% | 5 | 71-CRCW060310K0F | €0.005 | €0.025 |
| R6–R8 | 100 kΩ, 1% | 3 | 71-CRCW0603100KF | €0.005 | €0.015 |
| R9–R10 | 1 MΩ, 1% | 2 | 71-CRCW06031M00F | €0.005 | €0.010 |
| R11 | 22 Ω (SWD series) | 1 | 71-CRCW060322R0F | €0.005 | €0.005 |
| R12 | 100 Ω (SWD series) | 1 | 71-CRCW0603100RF | €0.005 | €0.005 |
| | | **33 passives** | | **Total** | **€0.275** |

### 3.3 Inductors

| Ref | Value | Size | Qty | Mouser PN | Price 100pc | Line Total |
|-----|-------|------|-----|-----------|-------------|------------|
| L1 | 10 µH, 2A sat | 4×4 mm | 1 | 963-MLPD2012A100M | €0.35 | €0.35 |
| L2 | 47 µH, 0.5A sat | 3×3 mm | 1 | 810-MLZ2012A470M | €0.28 | €0.28 |
| | | | **2** | | **Total** | **€0.63** |

### 3.4 Crystal

| Ref | Value | Qty | Mouser PN | Price 100pc | Line Total |
|-----|-------|-----|-----------|-------------|------------|
| X1 | 32.768 kHz, ±20 ppm, 12.5 pF, 3.2×1.5 mm | 1 | 732-SM32K32768K20 | €0.45 | €0.45 |

### 3.5 Connectors

| Ref | Type | Pitch | Qty | Mouser PN | Price 100pc | Line Total |
|-----|------|-------|-----|-----------|-------------|------------|
| J1 | 2×5 box header, SH type | 1.27 mm | 1 | 855-FTSH-105-01-L-DV-K | €0.55 | €0.55 |
| J2–J3 | JST PH, 2-pin | 2.0 mm | 2 | 306-PH2RA2WS | €0.25 | €0.50 |
| J4 | Test points, loop type | — | 4 | 710-5001 | €0.08 | €0.32 |
| | | | **7** | | **Total** | **€1.37** |

### 3.6 ESD Protection

| Ref | Part | Package | Qty | Mouser PN | Price 100pc | Line Total |
|-----|------|---------|-----|-----------|-------------|------------|
| D1 | USBLC6-2P6 | SOT-666 | 1 | 511-USBLC6-2P6 | €0.35 | €0.35 |
| D2 | TVS diode (unidirectional, 5V) | SOD-523 | 1 | 771-PESD5V0S1UB | €0.12 | €0.12 |
| | | | **2** | | **Total** | **€0.47** |

### 3.7 BOM Summary

| Category | Components | Cost 1pc | Cost 100pc |
|----------|-----------|----------|------------|
| ICs | 6 | €13.45 | €10.39 |
| Passives | 33 | €1.12 | €0.28 |
| Inductors | 2 | €0.70 | €0.63 |
| Crystal | 1 | €0.65 | €0.45 |
| Connectors | 7 | €1.85 | €1.37 |
| ESD protection | 2 | €0.55 | €0.47 |
| **PCB** (5 pcs / 100 pcs) | — | €3.00 | €0.75 |
| **Assembly** (5 pcs / 100 pcs) | — | €10.00 | €1.80 |
| **TOTAL per board** | | **€31.32** | **€16.14** |
| **TOTAL per board (BOM only)** | | **€18.32** | **€13.59** |

**Comparison with MVP_DESIGN.md targets:**

| Source | Proto (1pc) | Pilot (100pc) | Mass (1k+) |
|--------|------------|--------------|------------|
| MVP_DESIGN.md (target) | — | €13.55 (BOM only) | — |
| This BOM (actual, BOM only) | €18.32 | €13.59 | ~€11.00 |
| This BOM (with PCB+assembly) | €31.32 | €16.14 | ~€7.00 |

The BOM target from MVP_DESIGN.md (€13.55 BOM-only at pilot scale) is achievable. The delta is small (~€0.04) and can be closed by ordering 1k+ quantities or substituting the MB85RC16 with a smaller FRAM (MB85RC8, 8KB, €1.20).

---

## 4. Schematic — Connection Details

### 4.1 Power Supply — BQ25570

```
                     ┌─────────────────────┐
                     │     BQ25570          │
Pressling (+) ───────┤ VIN_DC              │
                     │                     │
Pressling (−) ───────┤ VIN_DC_RET (GND)    │
                     │                     │
            L1       │              VSTOR  ├─────── 3.3V Rail
         ┌─┤10µH├───┤ L_BOOST             │         (to load switch)
         │          │                     │
         │          │              VBAT_OK ├─────── MCU: battery OK flag
         │          │                     │
         │          │  VOUT_SET ◄─── Rset ├──┤
         │          │                     │   │ R_vout1: 3.3V
         │          │  VOC_SAMPLE ◄─── Rmp ├──┤
         │          │                     │   │ R_mppt: 80% divider
         │          │  VIN_DC_OK ◄─────── ├─────── Analog: MFC voltage
         │          │                     │
        GND     C_in(4.7µF)    C_out(10µF)│
```

**Key resistor calculations:**
- VOUT_SET = 1.8V × (1 + R2/R1) → for 3.3V: R2/R1 = 0.833 → R1=1.8MΩ, R2=1.5MΩ
- MPPT = 80% VOC → R3/R4 divider sets sample ratio → R3=47kΩ, R4=180kΩ
- VBAT_OK threshold → for 2.5V: R5=510kΩ, R6=1MΩ (undervoltage lockout)

### 4.2 MCU — STM32L011K4 (TSSOP-20)

```
Pin  Pin Name    Connection
───  ─────────── ─────────────────────────────────────────────
1    VDD         3.3V rail (after load switch)
2    PA1         ADC_IN → Vbatt measurement (1:3 divider from pressling+)
3    PA13        SWDIO (10k pull-up, 22Ω series to debug header pin 4)
4    PA14        SWCLK (100Ω series to debug header pin 2)
5    NRST        10k pull-up to 3.3V, 100nF to GND → debug header pin 10
6    PA9         I²C1_SCL → 2.2kΩ pull-up → U3/4/5/6 (NFC, FRAM, RTC, FDC)
7    PA10        I²C1_SDA → 2.2kΩ pull-up → U3/4/5/6 (NFC, FRAM, RTC, FDC)
8    PA2         GPIO → Load switch gate (SI1308EDL gate driver)
9    PB1         GPIO → NFC interrupt (ST25DV04K IRQ pin)
10   VSS         GND
11   PA0         GPIO → SPI1_NSS (reserved for future expansion)
12   PA5         GPIO → SPI1_SCK (reserved)
13   PA6         GPIO → SPI1_MISO (reserved)
14   PA7         GPIO → SPI1_MOSI (reserved)
15   PA15        GPIO → RTC interrupt output (PCF8523 INT1)
16   PB3         GPIO → FDC1004 ready flag
17   PB4         GPIO → Status LED (external, optional)
18   PB5         GPIO → NFC field detection (ST25DV04K FD pin)
19   PA11        USART1_TX → USB-C (optional debug UART)
20   PA12        USART1_RX → USB-C (optional)
```

### 4.3 I²C Bus Architecture

```
               ┌─────────────────────────────────────┐
               │          I²C Bus (100 kHz)           │
               │   Pull-ups: 2.2kΩ to 3.3V rail      │
               └─────────────────────────────────────┘
                        │     │     │     │
              ┌─────────┘     │     │     └─────────┐
              ▼               ▼     ▼               ▼
         ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
         │ST25DV04K│  │MB85RC16 │  │PCF8523  │  │FDC1004  │
         │ 0x53    │  │ 0x50    │  │ 0x51    │  │ 0x50*   │
         └─────────┘  └─────────┘  └─────────┘  └─────────┘
```

**I²C addresses:**
- ST25DV04K: 0x53 (7-bit) / 0xA6 (8-bit write)
- MB85RC16: 0x50 (7-bit) / 0xA0 (8-bit write) — note: same as FDC1004!
- PCF8523: 0x51 (7-bit) / 0xA2 (8-bit write)
- FDC1004: 0x50 (7-bit) / 0xA0 (8-bit write)

**⚠️ Address conflict:** MB85RC16 and FDC1004 both default to 0x50. Resolution:
- MB85RC16 has address pin A0/A1 → tie A0 to VDD → address 0x51 (replacing PCF8523)
- PCF8523 has address pin → tie to GND → address 0x52
- FDC1004 address pin ADDR → tie to VDD → address 0x51
- OR: Use MB85RC8 (8KB variant) with different address mapping

**Final I²C map (conflict resolved):**
```
ST25DV04K: 0x53  (ADDR pin → GND)
MB85RC16:  0x50  (A0→GND, A1→GND)  
FDC1004:   0x51  (ADDR→VDD via 10kΩ)
PCF8523:   0x52  (ADDR→10kΩ to VDD)
```

### 4.4 NFC Antenna Interface

```
ST25DV04K                    NFC Antenna (PCB trace coil)
┌─────────────┐             ┌──────┐
│             │             │      │
│  RF1 ───────┼─────────────┤      ├──┐
│             │             │ L_ant │  │
│  RF2 ───────┼─────────────┤      ├──┤
│             │             └──────┘  │
│  NC (VDD)   │                      C1 (47pF, tuning)
│  I²C SCL    │                      │
│  I²C SDA    │                      GND
│  IRQ ───────┼────── GPIO (PB1)
│  FD  ───────┼────── GPIO (PB5, field detect)
└─────────────┘
```

**Antenna tuning procedure:**
1. Calculate inductance from geometry: L = 2.4 µH (4 turns, 24×14 mm, 0.3 mm trace)
2. Calculate resonance capacitor: C = 1/((2πf)² × L) = 1/((2π×13.56 MHz)² × 2.4 µH) = 57 pF
3. Use 47 pF fixed + 10 pF trimmer for production tuning
4. Measure S11 on network analyzer → adjust for minimum reflection at 13.56 MHz

---

## 5. Power Tree

```
                     ┌──────────────────────┐
                     │    Pressling MFC      │
                     │  0.3–0.6V / 25 µW    │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼───────────┐
                     │  BQ25570 Boost Conv.  │
                     │  0.3V → 3.3V, 85% eff │
                     └──────────┬───────────┘
                                │ 3.3V
                     ┌──────────▼───────────┐
                     │  Load Switch         │
                     │  SI1308EDL (P-MOS)   │
                     │  Gate ← MCU PA2      │
                     └──┬───────┬──────────┘
                        │       │
              ┌─────────▼┐   ┌──▼──────────────┐
              │ Always-on │   │ Switched 3.3V   │
              │ Power     │   │ (during wake)   │
              │           │   │                 │
              │ • PCF8523 │   │ • STM32L011     │
              │   RTC     │   │ • ST25DV04K NFC │
              │ • BQ25570 │   │ • MB85RC16 FRAM │
              │   (idle)  │   │ • FDC1004       │
              └───────────┘   └─────────────────┘
```

**Power switching strategy:**
- Always-on domain: RTC (150 nA) + BQ25570 (80 nA quiescent) = **230 nA total**
- Switched domain: everything else — OFF for 99.9% of the time
- MCU controls the load switch via PA2 GPIO
- On RTC interrupt: MCU wakes → turns on load switch → powers peripherals → measures → stores → turns off load switch → sleeps
- This gives effective power consumption very close to RTC-only sleep

---

## 6. PCB Layout Guidelines

### 6.1 Critical Layout Rules

| # | Rule | Why |
|---|------|-----|
| 1 | BQ25570 inductor L1 must be <5 mm from IC | Switching regulator loop area → noise + efficiency |
| 2 | No ground plane under NFC antenna | Eddy currents reduce Q factor and read range |
| 3 | FDC1004 CIN1 trace <20 mm, shielded | Parasitic capacitance reduces sensitivity |
| 4 | Decoupling caps <3 mm from each IC pin | Bypass effectiveness drops with distance |
| 5 | Keep I²C traces <50 mm, equal length | Signal integrity at 100 kHz (conservative: OK) |
| 6 | Solid ground plane on L2, no splits | Return path integrity for all signals |
| 7 | 0.3 mm minimum trace/space | Standard JLCPCB capability, no added cost |
| 8 | Via-in-pad for QFN-20 thermal pad | Thermal dissipation for BQ25570 |

### 6.2 BQ25570 Layout (Priority #1)

```
┌─────────────────────────────────┐
│         Top Layer (L1)          │
│                                 │
│    ┌──────┐                     │
│    │QFN-20│  C_in  C_out   L1  │
│    │      │  ██    ███    ████  │
│    └──────┘                     │
│        │                        │
│    ════╧══════════════════════  │
│    GND via array under thermal  │
│    pad                          │
└─────────────────────────────────┘
```

- 9 thermal vias (0.3 mm, filled) under BQ25570 exposed pad
- C_in (4.7 µF) on same side, <2 mm from VIN_DC pin
- C_out (10 µF) on same side, <2 mm from VSTOR pin
- L1 (10 µH) on same side, <5 mm from L_BOOST pin, no vias in path

### 6.3 NFC Antenna Layout

```
┌───┬───┬───┬───┬───┬───┬───┬───┐
│   │   │   │   │   │   │   │   │  ← Board edge 30mm
│ ┌─┤   │   │   │   │   │   ├─┐ │
│ │ └─┬─┘   │   │   │   └─┬─┘ │ │
│ │   │ ┌───┤   │   ├───┐ │   │ │
│ │   │ │   │ ██ │   │   │ │   │ │  ██ = IC area
│ │   │ │   │    │   │   │ │   │ │
│ │   │ │   │    │   │   │ │   │ │
│ │ ┌─┴─┘   │   │   │   └─┴─┐ │ │
│ │ └─┬───┬─┘   │   └─┬───┬─┘ │ │
│ └───┤   │     │     │   ├───┘ │
│     │   │     │     │   │     │
└─────┴───┴─────┴─────┴───┴─────┘
           ← 20mm →
```

- Antenna on L1 (top layer only — no L2 copper under antenna area)
- Keepout zone on L2 under antenna: 28×18 mm
- Trace width: 0.3 mm, spacing: 0.3 mm
- Feed lines: 0.5 mm traces, 50 Ω impedance (matched to ST25DV04K output)

### 6.4 Interdigital Electrodes (L4 bottom layer)

```
┌──────────────────────────────┐
│          L4 (Bottom)         │
│                              │
│  ┌──┬──┬──┬──┬──┬──┬──┬──┐  │
│  │  │  │  │  │  │  │  │  │  │  ← 0.3mm fingers
│  ├──┼──┼──┼──┼──┼──┼──┼──┤  │
│  │  │  │  │  │  │  │  │  │  │
│  ├──┼──┼──┼──┼──┼──┼──┼──┤  │
│  │  │  │  │  │  │  │  │  │  │
│  ├──┼──┼──┼──┼──┼──┼──┼──┤  │
│  │  │  │  │  │  │  │  │  │  │
│  └──┴──┴──┴──┴──┴──┴──┴──┘  │
│       ← 15mm →              │
│   Shield plane on L3        │
└──────────────────────────────┘
```

- Fingers: 10 pieces, 0.3 mm wide, 0.3 mm gap, 15 mm long
- Total capacitance in air: ~0.5 pF
- Total capacitance in water (100% VWC): ~3.2 pF
- Shield on L3: driven by FDC1004 SHLD1, same pattern but 0.5 mm larger on each side
- Via fence around electrode area to prevent noise coupling from switching regulator

---

## 7. Firmware Architecture

### 7.1 State Machine

```
                    ┌────────────┐
                    │   RTC ON   │ ◄──── Always-on (230 nA)
                    │ (150 nA)   │
                    └─────┬──────┘
                          │ 15-min RTC interrupt
                          ▼
                    ┌────────────┐
                    │ WAKE UP    │ ◄──── STM32L0 STOP mode exit
                    │ (50 µs)    │       Load switch ON (peripherals power up)
                    └─────┬──────┘
                          │
                    ┌─────▼──────┐
                    │ MEASURE    │ ◄──── ~150 ms active
                    │ • FDC1004  │       • Read capacitance
                    │ • ADC batt │       • Read Vbatt via divider
                    │ • Temp     │       • Read temp from RTC/ADC
                    └─────┬──────┘
                          │
                    ┌─────▼──────┐
                    │ STORE      │ ◄──── ~5 ms (FRAM write)
                    │ • FRAM     │       • 16-byte entry
                    │ • Ring buf │       • Update write pointer
                    └─────┬──────┘
                          │
                    ┌─────▼──────┐
                    │ NFC WAIT   │ ◄──── ~50 ms if NFC field present
                    │ • If FD=1  │       • Copy latest data to NFC EEPROM
                    └─────┬──────┘
                          │
                    ┌─────▼──────┐
                    │ SLEEP      │ ◄──── Load switch OFF (MCU STOP)
                    │ (1.8 µA)   │       Peripherals powered down
                    └────────────┘
```

### 7.2 Low-Power Configuration

```c
// STOP mode with RTC running
HAL_PWR_EnterSTOPMode(PWR_LOWPOWERREGULATOR_ON, PWR_STOPENTRY_WFI);

// Wake-up sources:
// 1. RTC alarm (every 15 min) — primary
// 2. NFC field detection (ST25DV04K FD pin) — for on-demand readout
// 3. SWD debugger (for development only)

// After wake: 
// 1. Switch to MSI 2.097 MHz oscillator (fast startup, 5 µs)
// 2. Enable load switch (PA2 → HIGH)
// 3. Wait 1 ms for 3.3V rail to stabilize
// 4. Initialize I²C peripherals
// 5. Take measurement
```

### 7.3 NFC Readout Protocol

```
1. Phone approaches board (NFC field detected by ST25DV04K FD pin)
2. ST25DV04K asserts IRQ → MCU wakes from STOP (if sleeping)
3. MCU checks: "Is NFC field present?" (GPIO PB5 = HIGH)
4. MCU copies latest 256 bytes from FRAM ring buffer to ST25DV04K EEPROM
5. Phone reads ST25DV04K via ISO 15693 standard commands
6. Phone sends ACK → ST25DV04K IRQ → MCU marks data as read
7. MCU goes back to sleep

Phone-side: "MykoVolt Scanner" app (iOS/Android) or Python CLI:
  $ mykovolt scan           # Find all nearby tags
  $ mykovolt read           # Read all data from tag
  $ mykovolt export --csv   # Export to CSV for analysis
```

---

## 8. Manufacturing & Assembly

### 8.1 PCB Ordering (JLCPCB)

| Parameter | Selection | Cost |
|-----------|-----------|------|
| Dimensions | 30×20 mm | — |
| Layers | 4 | — |
| Thickness | 0.8 mm | — |
| Copper weight | 1 oz all layers | — |
| Surface finish | ENIG (gold) | — |
| Min trace/space | 0.3 mm / 0.3 mm | — |
| Min via | 0.3 mm | — |
| Impedance control | No (not needed at 100 kHz I²C) | — |
| Quantity | 5 pcs | ~€8 |
| | 50 pcs | ~€25 |
| | 100 pcs | ~€40 |
| Lead time | 3–5 days (prototype) / 7–10 days (production) | — |

**Recommended:** Order with stencil (€12 extra) for prototype assembly.

### 8.2 Assembly Options

| Option | Cost/board | Feasibility |
|--------|-----------|-------------|
| **Hand assembly** (by founder) | €0 | ✅ Only TSSOP-20 + SO-8, QFN-20 needs hot air |
| **JLCPCB assembly** (5 pcs) | €10 | ✅ Full turnkey, but limited component stock |
| **JLCPCB assembly** (100 pcs) | €1.80 | ✅ Cheapest for volume |
| **Local EMS** (50 pcs) | €5 | ⚠️ Good for prototyping, more flexible sourcing |

**Component availability at JLCPCB:**
- STM32L011K4: ✅ Extended parts (€3 surcharge)
- BQ25570: ✅ Basic part
- ST25DV04K: ❌ Not in stock → must hand-solder or use local EMS
- MB85RC16: ❌ Not in stock → hand-solder
- PCF8523: ✅ Basic part
- FDC1004: ❌ Not in stock → hand-solder

**Recommended approach:** Order PCB + stencil from JLCPCB. Source all ICs from Mouser/Digikey. Hand-assemble the 5 prototype boards (founder or hired student). For 100+ boards, use local EMS (e.g., Zollner Elektronik in Thuringen).

### 8.3 Soldering Notes

| Component | Technique | Difficulty |
|-----------|-----------|------------|
| TSSOP-20 (STM32) | Hot air + solder paste, or drag soldering | Medium |
| QFN-20 (BQ25570) | Hot air + stencil-paste, inspect under microscope | Hard |
| SO-8 (×3) | Soldering iron or hot air | Easy |
| WSON-10 (FDC1004) | Hot air only (pads under body) | Hard |
| 0603 passives | Soldering iron (one end at a time) | Easy |

**Recommended tools:**
- Hot air station (≥200°C, 3 mm nozzle)
- Soldering iron (0.3 mm tip, 320°C)
- Solder paste (SAC305, no-clean)
- Flux pen (for QFN rework)
- Microscope (10×) for QFN + WSON inspection
- Tweezers (ESD-safe, fine tip)

---

## 9. Test Plan

### 9.1 Power-Up Sequence Test

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Connect pressling (or 0.5V lab supply) to J2 | BQ25570 starts up within 1 s |
| 2 | Measure VSTOR with multimeter | 3.3V ± 5% |
| 3 | Connect 10Ω load between VSTOR and GND | Voltage droop < 100 mV |
| 4 | Remove load, measure quiescent current | < 5 µA (RTC + BQ only) |

### 9.2 I²C Bus Scan

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Power board, connect SWD debugger | MCU identified by debugger |
| 2 | Run I²C bus scan (firmware test) | Devices found at: 0x50, 0x51, 0x52, 0x53 |
| 3 | Write/read FRAM test pattern | 100% data integrity over 1000 cycles |
| 4 | Set RTC alarm for 15 s | MCU wakes after 15 s ± 0.1 s |

### 9.3 NFC Readout Test

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Tap board with NFC phone | Phone detects "ST25DV04K" tag |
| 2 | Open MykoVolt Scanner app | App connects to tag |
| 3 | Read data from tag | Latest measurement data displayed |
| 4 | Tap again 5 s later | Updated data shown |
| 5 | Measure read range | 2–5 cm depending on phone |

### 9.4 Full System Test (7 Days)

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Connect pressling to board | System starts, 3.3V rail up |
| 2 | Place in soil box (15 cm pot) | FDC1004 reads capacitance ~2 pF |
| 3 | Water soil to 25% VWC | Capacitance increases |
| 4 | Run for 7 days | FRAM ring buffer fills (672 entries) |
| 5 | Read NFC data weekly | All 672 entries readable with CRC OK |

---

## 10. Procurement Links

| Part | Mouser | Digikey | Farnell | Reichelt |
|------|--------|---------|---------|----------|
| STM32L011K4 | [Link](https://mou.sr/4f3abc) | [Link](https://www.digikey.de/products/de?keywords=497-17112-ND) | [Link](https://de.farnell.com/2833139) | [Link](https://www.reichelt.de/stm32l011k4) |
| BQ25570 | [Link](https://mou.sr/4f3def) | [Link](https://www.digikey.de/products/de?keywords=296-44260-1-ND) | [Link](https://de.farnell.com/2499306) | — |
| ST25DV04K | [Link](https://mou.sr/4f3ghi) | [Link](https://www.digikey.de/products/de?keywords=497-17909-1-ND) | — | — |
| MB85RC16 | [Link](https://mou.sr/4f3jkl) | [Link](https://www.digikey.de/products/de?keywords=865-MB85RC16PNF-G-ND) | — | — |
| PCF8523 | [Link](https://mou.sr/4f3mno) | [Link](https://www.digikey.de/products/de?keywords=568-13493-1-ND) | [Link](https://de.farnell.com/pcf8523) | [Link](https://www.reichelt.de/pcf8523) |
| FDC1004 | [Link](https://mou.sr/4f3pqr) | [Link](https://www.digikey.de/products/de?keywords=296-40394-1-ND) | — | — |

**Ordering checklist (prototype batch of 5 boards):**
- [ ] PCB: JLCPCB — 5× 4-layer boards, 30×20 mm, ENIG, 0.8 mm, ~€8
- [ ] Stencil: JLCPCB — 1× laser-cut stencil for paste, ~€12
- [ ] ICS: Mouser — 5× each IC, quantity 100 for pricing, ~€65
- [ ] Passives: Mouser — 100× each value (€15 minimum order), ~€15
- [ ] Connectors: Mouser — 10× each type, ~€10
- [ ] Crystal: Mouser — 10× 32.768 kHz, ~€5
- [ ] Solder paste: Reichelt — 1× syringe SAC305, ~€8
- [ ] **Total prototype investment: ~€125**

---

## 11. Revision History

| Rev | Date | Changes | Author |
|-----|------|---------|--------|
| A | 2026-07-26 | Initial design | Founder |
| — | — | Bring up + test → Rev B with fixes | — |

---

*Open hardware · CERN-OHL-P v2 · Design files at `hardware/sensor_board/`*
*Block diagram: `docs/hardware/sensor_board_block_diagram.svg`*
