# MykoVolt Sensor Board — Shopping List

> **Qty:** 5 prototype boards + spares | **Budget:** ~€300 | **Last updated:** 2026-07-26

---

## How to Order

1. **Mouser** — one basket for all components (€200)
2. **JLCPCB** — 5× PCBs + stencil (€18)
3. **Reichelt/Amazon** — tools & consumables (€80)

---

## 1. ICs (buy 10× each)

| Ref | Part | Package | Qty | Mouser SKU | Price | Mouser | Conrad |
|-----|------|---------|:---:|------------|:-----:|--------|--------|
| U1 | STM32L011F4P6 | TSSOP-20 | 10 | 511-STM32L011F4P6 | €21.50 | [Mouser](https://www.mouser.de/ProductDetail/STMicroelectronics/STM32L011F4P6?qs=511-STM32L011F4P6) | [Conrad](https://www.conrad.de/de/search.html?search=STM32L011F4P6) |
| U2 | BQ25570 | QFN-20 | 10 | 595-BQ25570 | €39.50 | [Mouser](https://www.mouser.de/ProductDetail/Texas-Instruments/BQ25570RGER?qs=595-BQ25570) | [Conrad](https://www.conrad.de/de/search.html?search=BQ25570) |
| U3 | ST25DV04K | SO-8 | 10 | 511-ST25DV04K | €13.50 | [Mouser](https://www.mouser.de/ProductDetail/STMicroelectronics/ST25DV04K?qs=511-ST25DV04K) | [Conrad](https://www.conrad.de/de/search.html?search=ST25DV04K) |
| U4 | MB85RC16 | SO-8 | 10 | 342-MB85RC16PNF-G | €21.00 | [Mouser](https://www.mouser.de/ProductDetail/Fujitsu/MB85RC16PNF-G-JNE1?qs=342-MB85RC16PNF-G) | [Conrad](https://www.conrad.de/de/search.html?search=MB85RC16) |
| U5 | PCF8523T/1,118 | SO-8 | 10 | 771-PCF8523T/1,118 | €7.50 | [Mouser](https://www.mouser.de/ProductDetail/NXP-Semiconductors/PCF8523T-1-118?qs=771-PCF8523T-1-118) | [Conrad](https://www.conrad.de/de/search.html?search=PCF8523) |
| U6 | FDC1004DSCR | WSON-10 | 10 | 595-FDC1004DSC | €31.50 | [Mouser](https://www.mouser.de/ProductDetail/Texas-Instruments/FDC1004DSCR?qs=595-FDC1004DSC) | [Conrad](https://www.conrad.de/de/search.html?search=FDC1004) |

## 2. Resistors (0603, 1%, buy 100× each)

| Value | Used For | Mouser SKU | Price/100 | Mouser | Conrad |
|-------|----------|------------|:---------:|--------|--------|
| 2.2 kΩ | I²C pull-up | 71-CRCW06032K20F | €0.50 | [Mouser](https://www.mouser.de/ProductDetail/Vishay/CRCW06032K20F?qs=71-CRCW06032K20F) | [Conrad](https://www.conrad.de/de/search.html?search=2.2k+0603) |
| 47 kΩ | MPPT divider | 71-CRCW060347K0F | €0.50 | [Mouser](https://www.mouser.de/ProductDetail/Vishay/CRCW060347K0F?qs=71-CRCW060347K0F) | [Conrad](https://www.conrad.de/de/search.html?search=47k+0603) |
| 510 kΩ | VBAT_OK set | 71-CRCW0603510KF | €0.50 | [Mouser](https://www.mouser.de/ProductDetail/Vishay/CRCW0603510KF?qs=71-CRCW0603510KF) | [Conrad](https://www.conrad.de/de/search.html?search=510k+0603) |
| 1 MΩ | VOUT_SET | 71-CRCW06031M00F | €0.50 | [Mouser](https://www.mouser.de/ProductDetail/Vishay/CRCW06031M00F?qs=71-CRCW06031M00F) | [Conrad](https://www.conrad.de/de/search.html?search=1M+0603) |
| 100 kΩ | Vbatt div upper | 71-CRCW0603100KF | €0.50 | [Mouser](https://www.mouser.de/ProductDetail/Vishay/CRCW0603100KF?qs=71-CRCW0603100KF) | [Conrad](https://www.conrad.de/de/search.html?search=100k+0603) |
| 220 kΩ | Vbatt div lower | 71-CRCW0603220KF | €0.50 | [Mouser](https://www.mouser.de/ProductDetail/Vishay/CRCW0603220KF?qs=71-CRCW0603220KF) | [Conrad](https://www.conrad.de/de/search.html?search=220k+0603) |
| 22 Ω | SWDIO series | 71-CRCW060322R0F | €0.50 | [Mouser](https://www.mouser.de/ProductDetail/Vishay/CRCW060322R0F?qs=71-CRCW060322R0F) | [Conrad](https://www.conrad.de/de/search.html?search=22+0603) |
| 100 Ω | SWCLK series | 71-CRCW0603100RF | €0.50 | [Mouser](https://www.mouser.de/ProductDetail/Vishay/CRCW0603100RF?qs=71-CRCW0603100RF) | [Conrad](https://www.conrad.de/de/search.html?search=100+0603) |
| 330 Ω (R13, R14) | LED current limit | 71-CRCW0603330RF | €0.50 | [Mouser](https://www.mouser.de/ProductDetail/Vishay/CRCW0603330RF?qs=71-CRCW0603330RF) | [Conrad](https://www.conrad.de/de/search.html?search=330+0603) |

💡 **Or buy an 0603 resistor kit** (e.g. [YAGEO RC0603 kit](https://www.mouser.de/c/?q=0603+resistor+kit)) for ~€15 — covers all values.

## 3. Capacitors (buy 100× each)

| Value | Dielectric | Size | Used For | Mouser SKU | Price/100 | Mouser | Conrad |
|-------|-----------|:----:|----------|------------|:---------:|--------|--------|
| 100 nF | X7R 16V | 0603 | Decoupling | 81-GRM188R71C104K | €0.80 | [Mouser](https://www.mouser.de/ProductDetail/Murata/GRM188R71C104K?qs=81-GRM188R71C104K) | [Conrad](https://www.conrad.de/de/search.html?search=100nF+0603) |
| 1 µF | X5R 10V | 0603 | Decoupling | 81-GRM188R61A105K | €1.50 | [Mouser](https://www.mouser.de/ProductDetail/Murata/GRM188R61A105K?qs=81-GRM188R61A105K) | [Conrad](https://www.conrad.de/de/search.html?search=1%C2%B5F+0603) |
| 10 µF | X5R 6.3V | 0805 | BQ output | 81-GRM21BR60J106K | €2.50 | [Mouser](https://www.mouser.de/ProductDetail/Murata/GRM21BR60J106K?qs=81-GRM21BR60J106K) | [Conrad](https://www.conrad.de/de/search.html?search=10%C2%B5F+0805) |
| 22 pF | C0G 50V | 0603 | Xtal load | 81-GRM1885C1H220J | €0.80 | [Mouser](https://www.mouser.de/ProductDetail/Murata/GRM1885C1H220J?qs=81-GRM1885C1H220J) | [Conrad](https://www.conrad.de/de/search.html?search=22pF+0603) |
| 100 pF | C0G 50V | 0603 | Filter | 81-GRM1885C1H101J | €0.80 | [Mouser](https://www.mouser.de/ProductDetail/Murata/GRM1885C1H101J?qs=81-GRM1885C1H101J) | [Conrad](https://www.conrad.de/de/search.html?search=100pF+0603) |
| 47 pF | C0G 50V | 0603 | NFC tune | 81-GRM1885C1H470J | €0.80 | [Mouser](https://www.mouser.de/ProductDetail/Murata/GRM1885C1H470J?qs=81-GRM1885C1H470J) | [Conrad](https://www.conrad.de/de/search.html?search=47pF+0603) |
| 4.7 µF | X5R 10V | 0603 | BQ input | 81-GRM188R61A475K | €1.80 | [Mouser](https://www.mouser.de/ProductDetail/Murata/GRM188R61A475K?qs=81-GRM188R61A475K) | [Conrad](https://www.conrad.de/de/search.html?search=4.7%C2%B5F+0603) |

## 4. Inductors & Crystal (buy 10×)

| Ref | Value | Size | Mouser SKU | Price | Mouser | Conrad |
|-----|-------|------|------------|:-----:|--------|--------|
| L1 | 10 µH, 2A sat | 4×4×2 mm | 963-MLPD2012A100M | €3.50 | [Mouser](https://www.mouser.de/ProductDetail/TDK/MLPD2012A100M?qs=963-MLPD2012A100M) | [Conrad](https://www.conrad.de/de/search.html?search=10%C2%B5H+2A) |
| L2 | 47 µH, 0.5A sat | 3×3×1.5 mm | 810-MLZ2012A470M | €2.80 | [Mouser](https://www.mouser.de/ProductDetail/TDK/MLZ2012A470M?qs=810-MLZ2012A470M) | [Conrad](https://www.conrad.de/de/search.html?search=47%C2%B5H) |
| X1 | 32.768 kHz, ±20 ppm, 12.5 pF | 3.2×1.5 mm | 732-SM32K32768K20 | €4.50 | [Mouser](https://www.mouser.de/ProductDetail/Seiko/SM32K32768K20?qs=732-SM32K32768K20) | [Conrad](https://www.conrad.de/de/search.html?search=32.768kHz) |

**⚠️ L1 critical:** Must handle 2A saturation for BQ25570 cold-start. Do not substitute.

## 5. Supercap & ESD (buy 10×)

| Ref | Part | Mouser SKU | Price | Mouser | Conrad |
|-----|------|------------|:-----:|--------|--------|
| SC1 | 100 mF, 3.6 V, <5 µA leakage | 598-DGH336Q3R6 | €12.00 | [Mouser](https://www.mouser.de/ProductDetail/Illinois-Capacitor/DGH336Q3R6?qs=598-DGH336Q3R6) | [Conrad](https://www.conrad.de/de/search.html?search=100mF+Supercap) |
| D1 | USBLC6-2P6 (NFC ESD) | 511-USBLC6-2P6 | €3.50 | [Mouser](https://www.mouser.de/ProductDetail/STMicroelectronics/USBLC6-2P6?qs=511-USBLC6-2P6) | [Conrad](https://www.conrad.de/de/search.html?search=USBLC6-2P6) |
| D2 | PESD5V0S1UB (VDD TVS) | 771-PESD5V0S1UB | €1.20 | [Mouser](https://www.mouser.de/ProductDetail/Nexperia/PESD5V0S1UB?qs=771-PESD5V0S1UB) | [Conrad](https://www.conrad.de/de/search.html?search=PESD5V0S1UB) |

**Supercap selection note:** Leakage current is the dominant power drain in standby. The DGH series has <3 µA typical. For lower leakage (but smaller capacitance), consider Seiko CPH3225A (11 mF, <0.5 µA — Mouser [667-CPH3225A](https://www.mouser.de/c/?q=667-CPH3225A)).

## 6. Transistor & LEDs (buy 10×)

| Ref | Part | Mouser SKU | Price | Mouser | Conrad |
|-----|------|------------|:-----:|--------|--------|
| Q1 | SI1308EDL (P-MOS load switch) | 781-SI1308EDL-T1-GE3 | €2.50 | [Mouser](https://www.mouser.de/ProductDetail/Vishay/SI1308EDL-T1-GE3?qs=781-SI1308EDL-T1-GE3) | [Conrad](https://www.conrad.de/de/search.html?search=SI1308EDL) |
| LED1 | Green LED 0603 (power) | 78-VAOL-S6GT4 | €0.80 | [Mouser](https://www.mouser.de/ProductDetail/Vishay/VAOL-S6GT4?qs=78-VAOL-S6GT4) | [Conrad](https://www.conrad.de/de/search.html?search=0603+green+LED) |
| LED2 | Yellow LED 0603 (status) | 78-VAOL-S6YT4 | €0.80 | [Mouser](https://www.mouser.de/ProductDetail/Vishay/VAOL-S6YT4?qs=78-VAOL-S6YT4) | [Conrad](https://www.conrad.de/de/search.html?search=0603+yellow+LED) |

## 7. Connectors (buy 10×)

| Ref | Type | Mouser SKU | Price | Mouser | Conrad |
|-----|------|------------|:-----:|--------|--------|
| J1 | 2×5 box header SH, 1.27 mm (SWD) | 855-FTSH-105-01-L-DV-K | €5.50 | [Mouser](https://www.mouser.de/ProductDetail/Samtec/FTSH-105-01-L-DV-K?qs=855-FTSH-105-01-L-DV-K) | [Conrad](https://www.conrad.de/de/search.html?search=1.27mm+box+header) |
| J2, J3 | JST PH 2-pin header, 2.0 mm | 306-PH2RA2WS | €5.00 | [Mouser](https://www.mouser.de/ProductDetail/JST/PH2RA2WS?qs=306-PH2RA2WS) | [Conrad](https://www.conrad.de/de/search.html?search=JST+PH+2-pin) |
| — | JST PH housing (mating) | 306-PHR-2 | €0.50 | [Mouser](https://www.mouser.de/ProductDetail/JST/PHR-2?qs=306-PHR-2) | [Conrad](https://www.conrad.de/de/search.html?search=JST+PHR-2) |
| — | Crimp pins female | 306-BPH-002T-P0.5S | €0.60 | [Mouser](https://www.mouser.de/ProductDetail/JST/BPH-002T-P0.5S?qs=306-BPH-002T-P0.5S) | [Conrad](https://www.conrad.de/de/search.html?search=JST+crimp+pin) |
| J4 | Test point loop | 710-5001 | €1.60 | [Mouser](https://www.mouser.de/ProductDetail/Wurth-Elektronik/710-5001?qs=710-5001) | [Conrad](https://www.conrad.de/de/search.html?search=test+point+loop) |
| — | Silicone wire 24 AWG, 1 m | — | ~€3 | Local |

Also need: **2×5 ribbon cable 1.27 mm pitch** (~€3 from Reichelt).

## 8. PCB (JLCPCB)

| Parameter | Selection | Cost |
|-----------|-----------|:----:|
| Dimensions | 30×20 mm | — |
| Layers | 4 | — |
| Thickness | 0.8 mm | — |
| Copper | 1 oz all layers | — |
| Finish | **ENIG** | +€5 |
| Min trace/space | 0.3 mm / 0.3 mm | — |
| Qty | **5 pcs** | ~€8 |
| Stencil | Electropolished, 0.12 mm | +€4 |
| Shipping | DHL | ~€6 |
| **Total** | | **~€18** |

**⚠️ JLCPCB assembly:** Only BQ25570, PCF8523, and passives are in basic parts. ST25DV04K, MB85RC16, FDC1004 are not stocked — hand-solder these.

## 9. Tools & Consumables (one-time)

| Item | Use | Price | Where |
|------|-----|:-----:|-------|
| Hot air station (≥200°C, 3 mm nozzle) | QFN, WSON soldering | ~€80 | Reichelt / Amazon |
| Soldering iron (0.3 mm tip, 320°C) | TSSOP, SO-8, 0603 | ~€40 | Hakko FX-600 |
| DMM with µA resolution | Quiescent current | ~€30 | Uni-T UT61E |
| Digital microscope 10–20× | QFN inspection | ~€25 | Amazon USB |
| ST-Link/V2 debugger | SWD programming | ~€15 | Reichelt |
| SAC305 solder paste, syringe | Reflow | ~€8 | Reichelt |
| Flux pen | QFN rework | ~€5 | Reichelt |
| Solder wick 2 mm | Touch-up | ~€3 | Reichelt |
| ESD tweezers (straight + curved) | Placement | ~€10 | Reichelt |
| Isopropyl alcohol 99%, 250 ml | Cleaning | ~€5 | Pharmacy |
| Breadboard + jumper wires | Testing | ~€8 | Reichelt |
| **Total tools** | | **~€80** | |

## 10. Cost Summary

| Category | Cost |
|----------|:----:|
| ICs (10×) | €134.50 |
| Passives (100×) | ~€15.00 |
| Inductors + crystal (10×) | €10.80 |
| Supercap + ESD (10×) | €16.70 |
| MOSFET + LEDs (10×) | €4.10 |
| Connectors + wire (10×) | ~€20.00 |
| **Subtotal (components)** | **~€200** |
| PCB 5 pcs + stencil | €18.00 |
| **Subtotal (hardware)** | **~€218** |
| Tools & consumables (one-time) | ~€80 |
| **Total prototype investment** | **~€298** |

### Per-board at scale

| Scenario | Cost/board |
|----------|:----------:|
| Prototype (5 boards, full qty) | ~€43 |
| Pilot (100 boards, JLCPCB assembled) | **€16.99** |
| Mass (1000 boards, full SMT) | **~€8.50** |

## 11. Ordering Schedule

### Week 1 — Order
- [ ] JLCPCB: 5× 4-layer ENIG PCBs + stencil
- [ ] Mouser: all components in one basket
- [ ] Reichelt: ST-Link, solder paste, flux, wick, tweezers
- [ ] Amazon: hot air station (if needed)

### Week 2 — Build
- [ ] Receive PCBs + components
- [ ] Stencil paste → place parts → reflow (hot air + iron)
- [ ] Inspect under microscope → clean with IPA

### Week 3 — Test
- [ ] Power-up: 0.5 V supply → 3.3 V output ✓
- [ ] I²C scan: 0x50, 0x51, 0x52, 0x53 ✓
- [ ] NFC: phone tap → read tag ✓
- [ ] Quiescent: <5 µA sleep ✓
- [ ] Pressling: real fungal MFC → 3.3 V regulated ✓
- [ ] 7-day soil box test → NFC readout ✓

---

*Questions: mykovolt@pm.me*  
*Full design: `sensor_board_design.md`*  
*Simulation: `python3 ../simulation/pcb_power_sim.py`*
