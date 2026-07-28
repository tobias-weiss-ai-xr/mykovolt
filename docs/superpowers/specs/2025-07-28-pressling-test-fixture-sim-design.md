# Pressling Test Fixture & Simulation Calibration Design

**Datum:** 2025-07-28
**Status:** Draft — awaiting user approval
**Scope:** Cell-agnostic pressling test PCB + simulation calibration loop

---

## 1. Overview

The pressling (fungal MFC) is an experimental power source — its viability as a real energy supply for MykoVolt is unproven. This design creates the tooling to **measure, compare, and iterate** on pressling power generation across many cell form factors, electrode materials, and environmental conditions.

### Two-Track Strategy

| Track | Role | Status |
|---|---|---|
| **Dev Kit** | Application PCB — FDC1004 soil moisture sensor, FRAM logging, NFC readout | Existing, unchanged |
| **Test Fixture** | Measurement PCB — characterizes any pressling/cell form, logs I/V data via NFC | New, this spec |

The test fixture answers: *Can a pressling deliver enough current to run the dev kit (or a future wireless node)?* If not, the fallback is a PHA 3D-printed biopolymer enclosure with a small primary cell (CR2032 or similar).

---

## 2. Test Fixture PCB Specification

### 2.1 Requirements

1. Accept **any cell form factor** via screw terminals (disc, cylinder, pouch, series stack, parallel array)
2. Measure **open-circuit voltage (V_OC)** and **current under programmable loads**
3. Log measurements to FRAM with RTC timestamps for long-duration unattended tests (days–weeks)
4. Provide NFC readout so data can be collected without opening the test chamber
5. Record environmental conditions (temperature, humidity) alongside power data
6. Be powered by USB during benchtop use, or by the pressling itself for in-soil tests

### 2.2 Hardware Components

| Component | Role | Package |
|---|---|---|
| STM32L011F4 | MCU (same as dev kit) | UFQFPN-20 |
| MB85RC16 | 2KB FRAM ring buffer (same as dev kit) | SOT-23-5 |
| ST25DV04K | NFC tag for data readout (same as dev kit) | SOIC-8 |
| PCF8523 | RTC for timestamps (same as dev kit) | SOIC-8 |
| INA219 | Current/voltage/power sensor (I2C) | SOT-23-8 |
| SHT30 | Temperature + humidity (I2C) | SOT-23-5 |
| BQ25570 | Boost converter (optional — bypassable via jumper) | VQFN-16 |
| 4× MOSFET + load resistors | Programmable load bank (4 steps) | SOT-23 |
| 4× screw terminals | Cell connection (anode, cathode, Vsense+, Vsense-) | 5mm pitch |
| USB-C | Bench power and debug | USB-C receptacle |

### 2.3 Screw Terminal Configuration

The 4 terminals are the core of the "accept anything" approach:

- **ANODE** — connects to cell anode
- **CATHODE** — connects to cell cathode
- **VSENSE+** — high-side current shunt input (INA219)
- **VSENSE−** — low-side current shunt input (INA219)

The user wires the cell terminals to ANODE/CATHODE for power. For precision current measurement, the cell also connects to VSENSE+/VSENSE− (4-wire measurement, eliminates contact resistance). Both configurations are supported.

### 2.4 Load Bank

Four MOSFET-switched load resistors provide programmable I/V curve sweeps:

| Load | Resistance | Current at 0.4V | Use |
|---|---|---|---|
| R1 (trickle) | 10 kΩ | 40 µA | Continuous light load |
| R2 (low) | 100 Ω | 4 mA | Light continuous load |
| R3 (medium) | 10 Ω | 40 mA | Moderate load |
| R4 (heavy) | 1 Ω | 400 mA | Heavy load / short-circuit test |

Loads are engaged individually or in parallel via GPIO-controlled MOSFETs. This allows the firmware to sweep an I/V curve by enabling each load step and recording the steady-state voltage and current via INA219.

### 2.5 Power Architecture

Two modes:

1. **USB powered (benchtop):** USB-C provides 5V. BQ25570 is bypassed via jumper. INA219 and MCU run from USB. Pressling connects only to screw terminals for measurement.

2. **Pressling powered (in-soil):** No USB. BQ25570 boosts pressling voltage to 3.3V for MCU, FRAM, NFC. INA219 runs directly from pressling rail (operates down to 0V Vbus). Load bank drains from pressling directly — this is the power being measured.

### 2.6 PCB Physical

- Same 4-layer FR-4 stack as dev kit (F.Cu, In1.Cu, In2.Cu, B.Cu)
- 30×20 mm (same footprint as dev kit)
- Same connector/antenna layout for NFC

### 2.7 Measurements Logged Per Entry

Each FRAM entry (12 bytes) stores:

| Field | Type | Bytes |
|---|---|---|
| timestamp (seconds since epoch) | uint32 | 4 |
| V_OC (mV) | uint16 | 2 |
| load_current (mA, signed) | int16 | 2 |
| load_resistor_index (0=none, 1-4=R1-R4) | uint8 | 1 |
| temperature (°C, signed) | int8 | 1 |
| humidity (% RH) | uint8 | 1 |
| status flags | uint8 | 1 |
| CRC | uint8 | 1 |
| **Total** | | **12 bytes** |

149 entries × 12 bytes = 1788 bytes in the 2048-byte FRAM (256 bytes reserved for header, same as dev kit).

### 2.8 Measurement Modes

The firmware supports three measurement modes, selectable via NFC command:

1. **V_OC tracking:** Every 60 seconds, measure open-circuit voltage (loads off). Minimal power draw. Good for multi-week lifetime tracking.

2. **I/V sweep:** Every 60 minutes, enable each load resistor for 5 seconds, record V and I at each step. This generates a full I/V curve 24 times per day. Moderate power draw from pressling.

3. **Load life test:** Continuously run at a fixed load (user selects via NFC). Record V and I every 60 seconds until voltage drops below cutoff. Determines mAh capacity at a given discharge rate.

---

## 3. Simulation Calibration Loop

### 3.1 Existing Simulation Infrastructure

`simulation/alternatives.py` already contains:
- `SimulateBioBattery()` with power density models
- Activation, ohmic, and concentration loss models
- Temperature effects
- Fuel depletion over time (exponential decay)
- O2 diffusion and saturation models

Current limitation: these models use **literature values** for power density and loss parameters. Real pressling behavior is unknown.

### 3.2 Calibration Workflow

```
1. Simulate (predict) →  alternatives.py produces power curves for a given cell design
2. Fabricate           →  build pressling per simulated parameters
3. Test                →  run on test fixture, collect I/V + environmental data
4. Extract            →  CLI `mykovolt parse` reads FRAM data via NFC
5. Compare            →  simulation/prediction vs. measurement
6. Fit                →  update model parameters (power density, loss coefficients)
7. Repeat             →  refined model → better prediction → next cell design
```

### 3.3 Parameters to Calibrate

| Parameter | Literature Value | Source | Calibrated By |
|---|---|---|---|
| Power density (µW/cm²) | 12.5 | Empa 2024 (T. pubescens) | I/V sweep at each size |
| Activation loss coefficient | Model-dependent | Nernst equation | V_OC vs. temperature curve |
| Ohmic loss (internal resistance) | ~50-200 Ω·cm² | Typical MFC | I/V slope under load |
| Fuel depletion rate (%/day) | 2% | Assumption | Load life test over 30+ days |
| O2 saturation coefficient | K_M = 50µM | Enzyme kinetics | Power vs. depth test |

### 3.4 Simulation Extensions

Extend `alternatives.py` with:

1. **Geometry sweep function:** Takes diameter (mm) and height (mm) as inputs, outputs predicted I/V curve. Replaces the fixed `PRESS_DIAMETER_MM = 50.0`.

2. **Multi-cell stacking model:** Predicts series and parallel cell behavior (voltage add, current add, mismatch losses).

3. **Environmental derating:** Maps temperature, moisture, soil type to power derating factors. Calibrated from SHT30 data on test fixture.

4. **Calibration loader:** Reads test fixture CSV exports and fits model parameters via least-squares regression.

---

## 4. Firmware Design

### 4.1 Firmware = Dev Kit + Extra Drivers

The test fixture firmware reuses most of the dev kit firmware:

| Module | Dev Kit | Test Fixture | Notes |
|---|---|---|---|
| STM32L011 GPIO/clock init | Yes | Yes | Identical |
| I2C driver | Yes | Yes | Identical |
| FRAM driver (mb85rc16) | Yes | Yes | Identical |
| FRAM ring buffer | Yes | Yes | Same header, different entry struct |
| NFC driver (st25dv04k) | Yes | Yes | Identical |
| RTC driver (pcf8523) | Yes | Yes | Identical |
| FDC1004 driver | Yes | **No** | No sensor on test fixture |
| BQ25570 driver | Yes | Yes | Optional, bypassable |
| **INA219 driver** | No | **New** | V, I, P measurement |
| **SHT30 driver** | No | **New** | Temp + humidity |
| **Load bank control** | No | **New** | GPIO MOSFET switching |

### 4.2 New Drivers Required

**ina219.c/h:**
- `ina219_init()` — configure shunt resistor (0.1 Ω), 32V range, 12-bit ADC
- `ina219_read_voltage_mv()` — bus voltage
- `ina219_read_current_ma()` — shunt current
- `ina219_read_power_mw()` — computed power
- I2C address: 0x40 (configurable via A0/A1 pins)

**sht30.c/h:**
- `sht30_init()` — single-shot mode, high repeatability
- `sht30_read(&temp_c, &rh_pct)` — blocking read
- I2C address: 0x44

**load_bank.c/h (optional — can be inline in main.c):**
- `load_bank_set(mask)` — bitfield, 1=R1, 2=R2, 4=R3, 8=R4
- `load_bank_off()` — disconnect all loads

### 4.3 FRAM Entry Structure Change

The test fixture uses a different FRAM entry format than the dev kit. The CLI parser must detect which format based on a version field or magic byte in the header.

Dev kit entry: `{timestamp, capacitance_pf, v_batt_mv, v_sense_mv, status, crc_ok}`
Test fixture entry: `{timestamp, voc_mv, load_current_ma, load_resistor, temp_c, rh_pct, status, crc}`

Both are 12 bytes. Both use the same 256-byte header region and 0x4D56 magic. The header's version field distinguishes them (version=1 = dev kit, version=2 = test fixture).

---

## 5. CLI Extensions

### 5.1 New `mykovolt parse` Output Modes

The existing `mykovolt parse` command reads FRAM data and outputs structured records. Extend it to:

- Auto-detect entry format from FRAM header version field
- Parse test fixture entries (V_OC, current, load resistor, temp, humidity)
- Output as CSV, JSON, or Parquet (existing exporters)

### 5.2 New `mykovolt calibrate` Subcommand

Fit simulation model parameters to measured data:

```
mykovolt calibrate measurements.csv --output model_params.yaml
```

Input: CSV from `mykovolt parse`. Output: YAML with calibrated power density, loss coefficients, depletion rate.

---

## 6. Fallback: Biopolymer Enclosure + Primary Cell

If pressling testing shows insufficient power (less than ~100 µA sustained after 7 days), the fallback is:

- **Enclosure:** PHA (polyhydroxyalkanoate) 3D-printed puck, Ø60mm × 12mm. PHA is home-compostable (degrades in soil at ambient temperature, unlike PLA which needs industrial composting at 58°C+).
- **Power:** CR2032 coin cell (220 mAh) or similar. Powers dev kit for 1-2 years with sleep cycling.
- **Assembly:** PCB slides into printed housing. No pressling needed. Device is still biodegradable (PHA shell + soil-degrades-everything-else-approach).

This is higher confidence on power but less innovative. The test fixture determines which path to take.

---

## 7. Scope Exclusions

This spec does **not** cover:
- The dev kit sensor PCB (already designed, unchanged)
- Biodegradable sensor electrodes (deferred — pressling viability is the priority gate)
- LoRa radio integration (future — depends on pressling power results)
- Production tooling or BOM optimization (future — after pressling viability is proven)
- Multi-cell stacking hardware (future — after single-cell characterization is complete)
