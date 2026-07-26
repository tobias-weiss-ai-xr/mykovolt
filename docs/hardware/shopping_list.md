# MykoVolt Sensor Board — Shopping List & Procurement Guide

> **Board:** DevKit v0.1 | **Qty:** 5 prototype boards + 2 spare sets
> **Total Budget:** ~€155 | **Last Updated:** 2026-07-26

---

## How to Use This List

1. **Order PCB + stencil** from JLCPCB first (longest lead time: 5-7 days)
2. **Order all components** from Mouser + Digikey in one go (saves shipping)
3. **Order tools & consumables** from Reichelt (local, fast delivery)
4. **Assembly** — founder hand-solders prototypes (see skill-level notes below)

---

## Section 1: Integrated Circuits (ICs)

Order these from **Mouser** (best stock × price combo). Buy **10× each** to have spares.

| Ref | Part | Package | Qty | Mouser PN | Price 1pc | Line Total |
|-----|------|---------|:---:|-----------|----------:|----------:|
| U1 | **STM32L011K4** | TSSOP-20 | 10 | [511-STM32L011K4](https://mou.sr/4f3abc) | €2.15 | €21.50 |
| U2 | **BQ25570** | QFN-20 (3.5×3.5) | 10 | [595-BQ25570](https://mou.sr/4f3def) | €3.95 | €39.50 |
| U3 | **ST25DV04K** | SO-8 | 10 | [511-ST25DV04K](https://mou.sr/4f3ghi) | €1.35 | €13.50 |
| U4 | **MB85RC16** | SO-8 | 10 | [865-MB85RC16PNF-G](https://www.digikey.de/products/de?keywords=MB85RC16PNF-G) | €2.10 | €21.00 |
| U5 | **PCF8523** | SO-8 | 10 | [771-PCF8523T/1](https://mou.sr/4f3mno) | €0.75 | €7.50 |
| U6 | **FDC1004** | WSON-10 (3×3) | 10 | [595-FDC1004DSC](https://mou.sr/4f3pqr) | €3.15 | €31.50 |
| | | | **60** | | **Total ICs** | **€134.50** |

**⚠️ JLCPCB assembly note:** BQ25570 is a basic part at JLCPCB. ST25DV04K, MB85RC16, and FDC1004 are **not stocked** at JLCPCB — must hand-solder these.

**💡 Alternative for cost reduction (100+ qty):**
| Part | 100pc Price | Save vs 10pc |
|------|:----------:|:-----------:|
| STM32L011K4 | €1.52 | −29% |
| BQ25570 | €3.20 | −19% |
| ST25DV04K | €0.95 | −30% |
| MB85RC16 | €1.65 | −21% |
| PCF8523 | €0.52 | −31% |
| FDC1004 | €2.55 | −19% |

---

## Section 2: Passives — Resistors

**Size:** 0603 (1608 metric) — manually solderable, JLCPCB standard.  
**Tolerance:** 1% for all signal/divider resistors, 5% for pull-ups OK.  
**Order:** 100× each from **Mouser**.

| Ref | Value | Qty | Mouser PN | Price 100 | Line Total |
|-----|-------|:---:|-----------|----------:|----------:|
| R1, R2 | **2.2 kΩ** (I²C pull-up) | 100 | [71-CRCW06032K20F](https://mou.sr/) | €0.005 | €0.50 |
| R3, R4 | **47 kΩ** (BQ25570 MPPT div) | 100 | [71-CRCW060347K0F](https://mou.sr/) | €0.005 | €0.50 |
| R5, R6 | **510 kΩ** (BQ25570 VBAT_OK) | 100 | [71-CRCW0603510KF](https://mou.sr/) | €0.005 | €0.50 |
| R7, R8 | **1.0 MΩ** (BQ25570 VOUT_SET) | 100 | [71-CRCW06031M00F](https://mou.sr/) | €0.005 | €0.50 |
| R9 | **100 kΩ** (Vbatt divider upper) | 100 | [71-CRCW0603100KF](https://mou.sr/) | €0.005 | €0.50 |
| R10 | **220 kΩ** (Vbatt divider lower) | 100 | [71-CRCW0603220KF](https://mou.sr/) | €0.005 | €0.50 |
| R11 | **22 Ω** (SWDIO series) | 100 | [71-CRCW060322R0F](https://mou.sr/) | €0.005 | €0.50 |
| R12 | **100 Ω** (SWCLK series) | 100 | [71-CRCW0603100RF](https://mou.sr/) | €0.005 | €0.50 |
| | | **800** | | **Total** | **€4.00** |

**💡 Tip:** Buy an RC0603 assorted kit instead — [e.g. this 1600-piece kit from Mouser](https://mou.sr/) (~€15). Gives you all values plus extras for future boards.

---

## Section 3: Passives — Capacitors

**Dielectric:** X7R for decoupling (stable over temp), C0G/NP0 for timing/resonant circuits.  
**Voltage rating:** ≥10V (derated from 6.3V for ceramic — DC bias reduces capacitance).  
**Order:** 100× each from **Mouser**.

| Ref | Value | Dielectric | Size | Qty | Mouser PN | Price 100 | Line Total |
|-----|-------|-----------|:----:|:---:|-----------|----------:|----------:|
| C1–C10 | **100 nF** | X7R, 16V | 0603 | 100 | [81-GRM188R71C104K](https://mou.sr/) | €0.008 | €0.80 |
| C11–C13 | **1 µF** | X5R, 10V | 0603 | 100 | [81-GRM188R61A105K](https://mou.sr/) | €0.015 | €1.50 |
| C14, C15 | **10 µF** | X5R, 6.3V | 0805* | 100 | [81-GRM21BR60J106K](https://mou.sr/) | €0.025 | €2.50 |
| C16, C17 | **22 pF** | C0G, 50V | 0603 | 100 | [81-GRM1885C1H220J](https://mou.sr/) | €0.008 | €0.80 |
| C18, C19 | **100 pF** | C0G, 50V | 0603 | 100 | [81-GRM1885C1H101J](https://mou.sr/) | €0.008 | €0.80 |
| C20 | **47 pF** | C0G, 50V | 0603 | 100 | [81-GRM1885C1H470J](https://mou.sr/) | €0.008 | €0.80 |
| C21 | **4.7 µF** | X5R, 10V | 0603 | 100 | [81-GRM188R61A475K](https://mou.sr/) | €0.018 | €1.80 |
| | | | | **700** | | **Total Caps** | **€9.00** |

*\*C14, C15 (10 µF) in 0805 for lower DC bias derating at 3.3V — 0603 10 µF drops to ~4 µF at 3.3V.*

---

## Section 4: Inductors

| Ref | Value | Size | Qty | Mouser PN | Price 1pc | Line Total |
|-----|-------|:----:|:---:|-----------|----------:|----------:|
| L1 | **10 µH, 2A sat** | 4×4×2 mm | 10 | [963-MLPD2012A100M](https://mou.sr/) | €0.35 | €3.50 |
| L2 | **47 µH, 0.5A sat** | 3×3×1.5 mm | 10 | [810-MLZ2012A470M](https://mou.sr/) | €0.28 | €2.80 |
| | | | **20** | | **Total** | **€6.30** |

**L1 critical:** Must handle 2A saturation (BQ25570 has high peak inductor current during cold-start).  
**Do not substitute** with smaller inductor — system won't start.

---

## Section 5: Crystal

| Ref | Value | Package | Qty | Mouser PN | Price 1pc | Line Total |
|-----|-------|---------|:---:|-----------|----------:|----------:|
| X1 | **32.768 kHz, ±20 ppm, 12.5 pF** | 3.2×1.5 mm SMD | 10 | [732-SM32K32768K20](https://mou.sr/) | €0.45 | €4.50 |

**Alternative (cheaper):** [AB38T-32.768kHz-12.5pF](https://mou.sr/) — €0.28 each, cylinder package, easier to hand-solder.

---

## Section 6: Supercapacitor

| Ref | Value | Package | Qty | Mouser PN | Price 1pc | Line Total |
|-----|-------|---------|:---:|-----------|----------:|----------:|
| SC1 | **100 mF, 3.6V, <5 µA leakage** | 8×12 mm radial | 10 | [598-DGH336Q3R6](https://mou.sr/) | €1.20 | €12.00 |

**Selection rationale (based on simulation):**
- Leakage current is the #1 power drain in the conservative case (5 µA × 3.3V = 16.5 µW)
- The DGH series has **<3 µA leakage** at 3.6V (better than generic 5 µA)
- 100 mF provides: 0.5 × 0.1 × (3.3² − 2.0²) / 3600 = **18.7 µWh** of usable energy
- This buffers ~2.5 hours of operation without pressling power
- For 30-day deployment: **add optional LiPo backup** (see Section 12)

**⛔ Avoid:** Large can supercaps (≥1F) — their leakage is 10-50 µA and they're physically too big for the 30×20 mm board.

---

## Section 7: ESD Protection

| Ref | Part | Package | Qty | Mouser PN | Price 1pc | Line Total |
|-----|------|---------|:---:|-----------|----------:|----------:|
| D1 | **USBLC6-2P6** (NFC antenna ESD) | SOT-666 | 10 | [511-USBLC6-2P6](https://mou.sr/) | €0.35 | €3.50 |
| D2 | **PESD5V0S1UB** (VDD rail TVS) | SOD-523 | 10 | [771-PESD5V0S1UB](https://mou.sr/) | €0.12 | €1.20 |
| | | | **20** | | **Total** | **€4.70** |

---

## Section 8: Transistors

| Ref | Part | Package | Qty | Mouser PN | Price 1pc | Line Total |
|-----|------|---------|:---:|-----------|----------:|----------:|
| Q1 | **SI1308EDL** (P-MOSFET load switch) | SOT-323 (SC-70) | 10 | [781-SI1308EDL-T1-GE3](https://mou.sr/) | €0.25 | €2.50 |

**Why SI1308EDL:** Lowest Rds(on) (≈50 mΩ) at 1.8V Vgs — critical for 3.3V rail switching with minimal voltage drop.

---

## Section 9: LEDs (Optional — Debug Only)

| Ref | Color | Package | Qty | Mouser PN | Price 1pc | Line Total |
|-----|-------|---------|:---:|-----------|----------:|----------:|
| LED1 | **Green** (power indicator) | 0603 SMD | 10 | [78-VAOL-S6GT4](https://mou.sr/) | €0.08 | €0.80 |
| LED2 | **Yellow** (status/activity) | 0603 SMD | 10 | [78-VAOL-S6YT4](https://mou.sr/) | €0.08 | €0.80 |
| | **330 Ω current-limit resistors** | 0603 | 20 | [71-CRCW0603330RF](https://mou.sr/) | €0.005 | €0.10 |
| | | | **20** | | **Total** | **€1.70** |

**Production note:** Leave LEDs unpopulated for deployed units (saves ~3 µA total). Only needed for debugging.

---

## Section 10: Connectors

| Ref | Type | Pitch | Qty | Mouser PN | Price 1pc | Line Total |
|-----|------|:----:|:---:|-----------|----------:|----------:|
| J1 | **2×5 box header, SH type** (SWD debug) | 1.27 mm | 10 | [855-FTSH-105-01-L-DV-K](https://mou.sr/) | €0.55 | €5.50 |
| J2 | **JST PH 2-pin** (pressling input) | 2.0 mm | 10 | [306-PH2RA2WS](https://mou.sr/) | €0.25 | €2.50 |
| J3 | **JST PH 2-pin** (aux sensor, optional) | 2.0 mm | 10 | (same as J2) | €0.25 | €2.50 |
| J4 | **Test points, loop type** (Vbatt, 3.3V, GND) | — | 20 | [710-5001](https://mou.sr/) | €0.08 | €1.60 |
| | **Matching connector housings** (for pressling cable) | | 10 | [306-PHR-2](https://mou.sr/) | €0.05 | €0.50 |
| | **Crimp pins** (for pressling cable) | | 20 | [306-BPH-002T-P0.5S](https://mou.sr/) | €0.03 | €0.60 |
| | **24 AWG silicone wire, 1m** (pressling leads) | — | 2 | [602-160-1001-2-4-](https://mou.sr/) | €2.50 | €5.00 |
| | | | | | **Total** | **€18.20** |

**⚠️ SWD header:** Get a matching 2×5 ribbon cable with 1.27mm pitch connector and ST-Link/V2 programmer.

---

## Section 11: PCB & Assembly

### PCB Order — JLCPCB

| Parameter | Selection | 
|-----------|-----------|
| Dimensions | 30 × 20 mm |
| Layers | 4 |
| Thickness | 0.8 mm |
| Copper weight | 1 oz all layers |
| Surface finish | **ENIG** (gold) — required for NFC antenna and ENIG electrode durability |
| Min trace/space | 0.3 mm / 0.3 mm |
| Min via | 0.3 mm |
| Via process | Tented & filled (for QFN thermal pad) |
| Color | Green (default — cheapest) |
| Quantity | **5 pcs** |
| Stencil | **Included** (electropolished, for paste) |
| **Cost** | **~€18** (5 pcs + stencil + ENIG + shipping) |

**Ordering steps:**
1. Upload Gerber files (need to generate from KiCad/EDA)
2. Select "ENIG" surface finish (€5 surcharge for 5 pcs — worth it)
3. Select "Stencil" — electropolished, 0.12 mm thickness
4. Select "PCB Assembly" — BUT only BQ25570 + PCF8523 + passives are in basic parts
5. Uncheck assembly for ST25DV04K, MB85RC16, FDC1004 (not in JLCPCB stock)
6. **Recommended:** Order bare PCB + stencil, hand-solder everything

---

## Section 12: Optional — LiPo Backup Battery

For deployments >30 days or where pressling may dry out:

| Part | Qty | Supplier | Price | Line Total |
|------|:---:|----------|------:|----------:|
| **Lithium Polymer 50 mAh 3.7V** (10×15×4 mm) | 2 | [Adafruit 2750](https://www.adafruit.com/product/2750) | €4.95 | €9.90 |
| **MCP73831 LiPo charger** (SOT-23-5) | 5 | [Mouser 579-MCP73831T-2ACI/OT](https://mou.sr/) | €0.45 | €2.25 |
| **Schottky diode** (BAT54, OR-ing pressling/LiPo) | 10 | [Mouser 771-BAT54](https://mou.sr/) | €0.08 | €0.80 |
| **Total backup option** | | | | **€12.95** |

**When to add:** Only if customer requires >30-day unattended operation. Adds 10×10mm to board area.

---

## Section 13: Tools & Consumables

### Required Tools (if you don't have them)

| Tool | Use | Price | Supplier | 
|------|-----|------|----------|
| **Hot air station** (≥200°C, 3mm nozzle) | QFN-20, WSON-10 soldering | ~€80 | Reichelt / Amazon |
| **Soldering iron** (0.3mm tip, 320°C) | TSSOP-20, SO-8, 0603 | ~€40 | Hakko FX-600 |
| **Digital multimeter** (µA resolution) | Quiescent current measurement | ~€30 | Uni-T UT61E |
| **Oscilloscope** (2-ch, ≥20 MHz) | I²C debugging, power rail | ~€100 | Rigol DS1054Z (used) |

### Consumables (per prototype batch)

| Item | Qty | Price | Supplier |
|------|:---:|------|----------|
| **SAC305 solder paste** (syringe, no-clean) | 1 | €8.00 | Reichelt |
| **Flux pen** (for QFN rework) | 1 | €5.00 | Reichelt |
| **Solder wick** (2mm, for touch-up) | 1 | €3.00 | Reichelt |
| **Isopropyl alcohol 99%** (for cleaning) | 250 ml | €5.00 | Local pharmacy |
| **ESD tweezers** (fine tip, straight+curved) | 2 | €10.00 | Reichelt |
| **Microscope** (10-20×, for QFN inspection) | 1 | €25.00 | Amazon USB microscope |
| **ST-Link/V2** (SWD debugger) | 1 | €15.00 | Reichelt |
| **USB-micro cable** (for debugger) | 1 | €3.00 | Local |
| **Breadboard + jumper wires** (testing) | 1 | €8.00 | Reichelt |
| **Total consumables** | | **€82.00** | |

---

## Section 14: Price Summary

| Category | Cost |
|----------|:----:|
| ICs (10× each) | €134.50 |
| Resistors (100× each) | €4.00 |
| Capacitors (100× each) | €9.00 |
| Inductors (10× each) | €6.30 |
| Crystal (10×) | €4.50 |
| Supercap 100 mF (10×) | €12.00 |
| ESD protection (10×) | €4.70 |
| P-MOSFET load switch (10×) | €2.50 |
| LEDs + resistors (debug) | €1.70 |
| Connectors + wiring | €18.20 |
| PCB 5 pcs + stencil (JLCPCB) | €18.00 |
| **Subtotal (components + PCB)** | **€215.40** |
| Tools & consumables (one-time) | €82.00 |
| **Total prototype investment** | **€297.40** |

### Per-Board Cost Breakdown

| Scenario | Cost/Board |
|----------|:----------:|
| **Prototype** (5 boards, full component qty) | **€43.08** |
| **After tools amortized** (over 5 boards) | **€59.48** |
| **Pilot 100 pcs** (JLCPCB assembled, 100pc IC pricing) | **€13.22** |
| **Mass 1000 pcs** (full SMT, 1k IC pricing) | **~€8.50** |

### What's NOT Included (future spending)

| Item | Estimated Cost | When |
|------|:-------------:|:----:|
| NFC phone for testing (used Android with NFC) | €50 | Before testing |
| Environmental chamber (temp/humidity control) | €200 | For validation |
| Fungal pressling materials (mycelium + substrate) | €30 | For integration test |
| EMC pre-compliance scan | €500 | Before product launch |

---

## Section 15: Ordering Checklist

### Week 1 — Order Everything

- [ ] **JLCPCB** — 5× 30×20mm 4-layer ENIG PCBs + stencil — **~€18**
- [ ] **Mouser** — all ICs, passives, inductors, crystal, supercap, ESD, MOSFET, LEDs — **~€180**
- [ ] **Mouser** — connectors (JST PH, SWD header), test points, crimp pins — **~€20**
- [ ] **Mouser** — spare parts (10× each IC, 100× each passive) — included above
- [ ] **Reichelt** — ST-Link/V2 debugger, solder paste, flux, wick, tweezers — **~€40**
- [ ] **Local** — isopropyl alcohol, USB cables — **~€10**

### Week 2 — Build

- [ ] Receive PCBs from JLCPCB (5-7 day lead time)
- [ ] Receive components from Mouser (3-5 day shipping)
- [ ] Apply solder paste through stencil
- [ ] Place all components using tweezers + microscope
- [ ] Reflow: hot air for QFN/WSON, iron for TSSOP/SO-8
- [ ] Inspect under microscope — reflow any bridges
- [ ] Clean with isopropyl alcohol

### Week 3 — Test

- [ ] **Power-up test:** Connect 0.5V lab supply → measure 3.3V output
- [ ] **I²C scan:** Verify all 4 devices detected (0x50, 0x51, 0x52, 0x53)
- [ ] **NFC test:** Tap phone → read ST25DV04K
- [ ] **Quiescent current:** Measure <5 µA in sleep mode
- [ ] **Pressling test:** Connect real fungal pressling → verify 3.3V regulation
- [ ] **Capacitive sensor:** Place in soil → read FDC1004 values
- [ ] **Full system:** Run for 7 days, read NFC data at end

---

## Section 16: Simulation Validation

The PCB power simulation (see `simulation/pcb_power_sim.py`) predicts:

| Metric | Typical | Conservative |
|--------|:-------:|:------------:|
| Pressling output (avg) | 24.0 µW | 20.8 µW |
| After BQ25570 boost | 13.3 µW | 11.2 µW |
| Board consumption (avg) | **8.07 µW** | **17.97 µW** |
| Energy margin | **1.65×** | **0.62×** |
| 7-day survival rate | **100%** | **0%** |
| Supercap min voltage | 3.597 V | 2.000 V (brown-out) |
| Max deployment lifetime | ~37 days | <1 day |

**Critical finding:** The bottleneck is **supercap leakage**. In conservative mode, 5 µA leakage × 3.3V = 16.5 µW dominates the 17.97 µW consumption. The recommended supercap (DGH series, <3 µA leakage) improves this, but for robust deployment:

1. **Use typical parameters** — with 24 µW pressling output, the system has 1.65× margin
2. **Low-leakage supercap (<3 µA)** — halves the standby power
3. **Optional LiPo backup** (Section 12) for >30-day deployments
4. **Key metric to validate experimentally:** actual pressling power output at 15°C and 30°C

---

*Questions? Contact founder at mykovolt@pm.me*
*Simulation: `python3 simulation/pcb_power_sim.py --help`*
