# MykoVolt Platform — Vanishing Electronics

**A modular, compostable sensing platform for ephemeral deployments where retrieval is impossible.**

---

## Platform Vision

MykoVolt is not a product. It's a **platform architecture** for building sensors that:
- Deploy at **100× the density** of alternatives (target: €0.01/node)
- Work where **no other power source can go** (inside concrete, compost, tissue, landfill)
- **Leave no trace** after mission completion (compostable power + future compostable substrate)

The current DevKit is the **first instantiation** of this platform — a 30×20mm NFC data logger with a compostable battery. Future instantiations will swap in different sensors, radios, and form factors while sharing the same power, compute, and manufacturing architecture.

---

## Architecture Layers

```
┌────────────────────────────────────────────────────┐
│                    APPLICATION                      │
│  DevKit  │  Compost  │  Concrete  │  Research  ...  │
├────────────────────────────────────────────────────┤
│                   COMMUNICATION                     │
│  NFC (v0.1)  │  BLE (v0.2)  │  Passive RF (v1.0)  │
├────────────────────────────────────────────────────┤
│                     COMPUTE                         │
│  ARM Cortex-M0+  │  FRAM  │  RTC  │  Energy Mgr    │
├────────────────────────────────────────────────────┤
│                     SENSING                         │
│  Capacitive  │  Temp (future)  │  Chem (future)    │
├────────────────────────────────────────────────────┤
│                      POWER                          │
│  Fungal MFC  │  Mg-Air  │  Hybrid  │  Harvesting   │
├────────────────────────────────────────────────────┤
│                   MANUFACTURING                     │
│  PCB Generator  │  Design Rules  │  BOM  │  CI/CD   │
└────────────────────────────────────────────────────┘
```

---

## Layer Specifications

### Power

| Technology | TRL | Power | Lifetime | Compostable | Status |
|------------|-----|-------|----------|-------------|--------|
| Fungal MFC (T. pubescens) | 2 | 25 µW | 7 days | ✅ Yes | Simulated, needs lab validation |
| Mg-Air (fallback) | 3 | 50 µW | 14 days | ❌ No (Mg) | Parallel R&D path |
| Hybrid (MFC + supercap) | 2 | 25 µW burst | 30+ days | ✅ Yes | Future research |

**Key constraint:** Fungal MFC requires O₂ at cathode. Below 5cm soil depth, O₂ < 0.1%. Solutions:
- Air-Chimney (tube to surface) — TRL 2
- Mg-Air backup (O₂-free operation) — TRL 3
- Surface/deployed applications only (no burial) — ship now

### Sensing

| Modality | Principle | TRL | Application |
|----------|-----------|-----|-------------|
| Capacitive (CIN1) | Dielectric measurement | 9 | Soil moisture, concrete curing, material detection |
| Capacitive (CIN2) | Differential reference | 9 | Temperature compensation |
| Guard ring (SHLD1) | Driven shield | 9 | Noise rejection, proximity |

**Future:** Temperature (thermistor), conductivity, pH (ion-selective electrode) — all compatible with existing analog front-end.

### Compute

| Component | Specification | Purpose |
|-----------|---------------|---------|
| STM32L011 | Cortex-M0+, 16MHz, 16KB flash, 2KB RAM | Main processing |
| MB85RC16 | 16Kbit FRAM, I²C, 10¹³ cycles | Non-volatile data logging |
| PCF8523 | RTC, 150 nA sleep | Scheduled wake-up, timestamps |
| BQ25570 | Boost converter, 80 nA Iq, MPPT | Power management |

**Sleep power:** 1.8 µA total (RTC + BQ25570 idle). **Active power:** 3 mA @ 1 MHz for ~150 ms per measurement.

### Communication

| Protocol | Range | Data Rate | Power | TRL |
|----------|-------|-----------|-------|-----|
| NFC (ISO 15693) | 2-5 cm | 53 kbit/s | Passive (reader-powered) | 9 |
| BLE (future) | 10-100 m | 1 Mbit/s | Active (10 mA peak) | 1 |
| Passive RF backscatter (future) | 1-10 m | 100 kbit/s | Passive | 1 |

NFC is the ship-now option. BLE enables remote data collection. Passive RF backscatter is the long-term vision (zero-power communication).

### Manufacturing

| Component | Method | TRL | Cost at Scale |
|-----------|--------|-----|---------------|
| PCB | Standard FR-4, 4-layer, ENIG | 9 | ~€8 |
| Pressling (MFC) | Compression molding | 2 | ~€0.15 |
| Casing | PLA/hemp, injection molded | 3 | ~€0.05 |
| Biodegradable PCB | Cellulose substrate, carbon ink | 2-3 | ~€0.50 (projected) |

The platform includes automated PCB generation (`generate_kicad.py`), design rules (`design_rules.yaml`), and CI/CD validation — enabling rapid iteration of application-specific variants.

---

## Instantiations

### Current: DevKit (v0.1)
- **Role:** Research platform, first product
- **Form:** 30×20mm, 4-layer FR-4, NFC
- **Sensor:** Capacitive (FDC1004)
- **Power:** Fungal MFC or Mg-Air
- **Status:** HW complete, firmware compiles, ready for prototyping
- **Docs:** `applications/devkit/`

### Future: Compost Monitor (v0.2)
- **Role:** First industrial application
- **Form:** 50×30mm, biodegradable PCB (future), NFC
- **Sensor:** Capacitive + temperature
- **Power:** Fungal MFC (thrives in compost heat)
- **Status:** Concept — needs biodegradable PCB research
- **Docs:** `applications/compost_monitor/`

### Future: Concrete Embed (v0.3)
- **Role:** Infrastructure monitoring
- **Form:** 20×10mm, no casing (embedded in concrete)
- **Sensor:** Capacitive + vibration
- **Power:** Mg-Air (no O₂ needed)
- **Status:** Concept
- **Docs:** Pending

---

## Key Research Problems

| Problem | Severity | Effort | Status |
|---------|----------|--------|--------|
| O₂ starvation in soil | Critical — blocks burial | 3 months | Identified, dual-path solution |
| Power density < 50 µW | High — limits sample rate | 6 months | Simulated path to 260 µW/cm² |
| FR-4 not biodegradable | High — limits "leave behind" claim | 12+ months | Cellulose PCB research needed |
| NFC range 2-5cm | Medium — requires close access | 3 months | BLE add-on (more power) |
| Lifetime 7 days | Medium — limits applications | 6 months | Better MFC formulation + supercap |
