# MykoVolt Competitive Intelligence

# Despite the .py extension, this is a markdown document.
# It was created as intelligence_dashboard.py to integrate with 
# the existing project structure. All content is markdown.

## Overview

MykoVolt operates at the intersection of:
- **Microbial fuel cells (MFC)** — scientific research → early commercialization
- **Soil moisture sensing** — established market with ~$500M TAM
- **Biodegradable electronics** — emerging field with ~$2B projected TAM by 2030

The competitive landscape spans direct substitutes (other soil-power technologies),
indirect alternatives (passive RFID, battery-powered sensors), and future threats
(emerging biodegradable battery research).

---

## 1. Direct Competitors

### 1.1 Bactery AB (Sweden)

| Aspect | Detail |
|---|---|
| **Technology** | Soil microbial fuel cell (bacteria-based, ceramic membrane) |
| **Product** | Soil-powered sensor node, ~£25/unit |
| **Lifetime** | Claims 25-30 years (bacteria self-replenish) |
| **TRL** | TRL 6-7 (field-tested since 2023) |
| **Funding** | €5M+ (Norrsken, EIC Accelerator, Swedish Energy Agency) |
| **Status** | Commercial pilot with farms in Sweden, UK |
| **Power** | ~10-50 µW (bacteria-based, similar class to T. pubescens) |

**MykoVolt vs Bactery:**

| Dimension | Bactery | MykoVolt |
|---|---|---|
| Power source | Soil bacteria (mixed consortia) | White-rot fungi (pure culture) |
| Lifetime | 25-30 years | 7-14 days (designed) |
| Biodegradability | Ceramic housing (not biodegradable) | 90% biodegradable (compostable pellet) |
| Cost | ~£25/unit | ~€35 (DevKit) / ~€0.15 (pellet only) |
| TRL | 6-7 | 2 |
| Target | Commercial farms | Research labs → farms |

**Threat level:** HIGH — Bactery is 3-4 years ahead and serving the same end market (farm soil sensors). MykoVolt's only differentiation is full biodegradability and lower ultimate pellet cost.

### 1.2 Microbial Fuel Cell Research Groups (Pipeline Competitors)

| Group | Focus | Key Results | Threat |
|---|---|---|---|
| **Empa** (Reyes et al., 2024) | 3D-printed cellulose fungal MFC | 12.5 µW/cm² (T. pubescens) | **Enabling** — core technology source |
| **Sukri et al.** (2021) | P. chrysosporium Zn/Air MFC | ~1,800 µW/cm² (~150× Empa) | **Reference** — different design (Zn/Air, membrane-less) |
| **JKU / MycelioTronics** | Fungal mycelium as electronic substrate | Mycelium skin for PCBs | **Complementary** — different application |
| **Sekrecka-Belniak et al.** (2018) | Fungal MFC with various white-rot fungi | OCV up to 450 mV | **Reference** — baseline data |
| **Umar et al.** (2024) | Fungal MFC optimization | Various strain comparisons | **Reference** |

**Note:** No research group has commercialized a fungal MFC. MykoVolt would be the first if successful.

---

## 2. Indirect Competitors (Current Alternatives)

### 2.1 Passive RFID Soil Moisture Sensors (CRITICAL THREAT)

| Aspect | Detail |
|---|---|
| **Technology** | Passive RFID tag with capacitive soil moisture sensing (e.g., StickNFind, Wireless Sensor Solutions) |
| **Power** | No battery — harvests energy from reader RF field |
| **Cost** | €0.50-3.00/tag (passive) |
| **Lifetime** | Unlimited (no battery) |
| **Read range** | ~0.1-1m (NFC/HF) or ~3-10m (UHF) |
| **Accuracy** | Medium (indirect moisture measurement via dielectric constant) |

**Why this matters:** Passive RFID solves the same problem (wireless soil moisture sensing without battery replacement) at **€0.50/unit** with **unlimited lifetime**. The trade-off against fungal MFC:

| Dimension | Passive RFID | Fungal MFC (MykoVolt) |
|---|---|---|
| Unit cost | €0.50-3.00 | €0.15-35.00 |
| Lifetime | Unlimited (no battery) | 7-14 days (designed) |
| Active sensing | No (reader-powered only) | Yes (15-min intervals) |
| Biodegradability | No (silicon + copper) | Yes (90%+) |
| Read range | 0.1-10m | 0.1-0.5m (NFC) |
| Data quality | Capacitive indirect | Electrochemical direct |

**MykoVolt's advantage:** Passive RFID can only sense when a reader is present. MykoVolt allows scheduled measurements and data logging — critical for precision agriculture where hourly/daily trends matter.

**MykoVolt's disadvantage:** Passive RFID costs 10-200× less and lasts forever. For simple "is the soil wet/dry?" applications, RFID wins.

### 2.2 CR2032-Powered Sensors (Status Quo)

| Aspect | Detail |
|---|---|
| **Examples** | TEROS 10/11 (METER), Sentek TriSCAN, Dragino LSN50 |
| **Battery** | CR2032 (1-3 year life depending on reporting interval) |
| **Cost** | €30-200/sensor + battery replacement labor |
| **Lifetime** | 1-3 years (limited by battery) |
| **Accuracy** | Very high (calibrated capacitance/frequency domain) |

**Why this matters:** CR2032 is the incumbent. It works, is reliable, and farmers accept the battery replacement cost (~€1-2/year in batteries + labor). MykoVolt needs to be cheaper over 5-year total cost of ownership.

**Total cost of ownership comparison (5 years):**

| Scenario | CR2032 Sensor | MykoVolt DevKit | MykoVolt Pellet-only |
|---|---|---|---|
| Hardware | €80 | €35 | — |
| Batteries (5yr) | €10 + labor | — | — |
| Pellets (5yr, 7-day cycle) | — | — | €0.15 × 260 = €39 |
| **Total** | **€90** | **€35 + €39 = €74** | **€39** |

At scale with pellet-only (reusable electronics + replaceable pellets), MykoVolt beats CR2032 on cost. But the hardware investment for the base station/reader (~€35) is a barrier.

### 2.3 Traditional Soil Moisture Sensor Market

| Sensor | Price | Power | Interface |
|---|---|---|---|
| TEROS 10 (METER) | ~€120 | Passive (reader-powered) | SDI-12 |
| TEROS 11 (METER) | ~€200 | Passive | SDI-12 |
| Sentek TriSCAN | ~€180 | Passive | SDI-12/RS-485 |
| Davis 6327C | ~€150 | CR2032 | Wireless |
| Dragino LSN50 | ~€80 | CR2032 | LoRaWAN |

All require batteries or external power. MykoVolt's self-powered approach is the differentiator.

---

## 3. Emerging/Future Competitors

### 3.1 Biodegradable Batteries (Research → Commercial)

| Group | Technology | Status | ETA to market |
|---|---|---|---|
| **Paper batteries** (multiple) | Cellulose-based, paper-thin | TRL 3-4 | 2027+ |
| **Enzymatic fuel cells** | Glucose/ethanol enzymes as catalyst | TRL 3-4 | 2028+ |
| **Biodegradable Zn-ion** | Zinc-based with biodegradable casing | TRL 3-4 | 2027+ |
| **Microbial fuel cells** (other) | Various bacteria/fungi in MFC | TRL 2-5 | 2028+ |

**Threat:** These compete on the "biodegradable power source" narrative — but none combine biodegradability with in-soil deployment and active sensing.

### 3.2 EU Battery Regulation 2023/1069

Effective February 2024, this regulation:
- Requires batteries to be removable/replaceable (favoring MykoVolt's replaceable pellet)
- Mandates carbon footprint declarations
- Incentivizes biodegradability for single-use batteries
- Creates regulatory tailwind for biodegradable alternatives

**Impact:** POTENTIALLY VERY POSITIVE — MykoVolt's biodegradable pellet could qualify for exemptions or preferences under the regulation's environmental provisions.

---

## 4. Competitive Positioning Matrix

```
Technology Readiness
        ^
    TRL 9│     CR2032 Sensors
        │     TEROS/Dragino
    TRL 7│         Bactery AB
        │         (soil bacteria MFC)
    TRL 5│
        │                       Passive RFID
    TRL 3│     MykoVolt───────► (future)
        │     (current)
    TRL 1│
        └─────────────────────────────────────►
            Low Cost              High Cost
```

**Most threatening quadrant:** Bottom-right — Passive RFID already combines low cost with unlimited lifetime. MykoVolt must compete on data quality, not cost alone.

**MykoVolt's sweet spot:** Medium cost + unique feature combination (biodegradable + active sensing + no battery replacement).

---

## 5. SWOT Analysis

### Strengths
- Biodegradability (90%+) — unique differentiator
- Replaceable pellet = reusable electronics
- Low pellet cost at scale (€0.15/target)
- No heavy metals, no toxic electrolytes
- Regulatory tailwind (EU Battery Regulation)
- ML-based optimization potential for enzyme formulation

### Weaknesses
- **TRL 2** — no experimental validation yet
- **No hardware exists** — all claims are theoretical
- **Single founder** with CS/ML background (no mycology/chemistry)
- 7-day runtime (requires pellet replacement)
- NFC range (~0.5m) limits deployment scenarios
- P. chrysosporium 150× power claim from different cell design (Zn/Air, not pellet)

### Opportunities
- Research lab market for MFC education/evaluation
- Agritech demand for sustainable alternatives
- Open-source hardware community (Hackaday, CrowdSupply, Tindie)
- EU Horizon/EIC funding for green deep tech
- Academic co-authorship model for early adopters
- Co-development with precision agriculture software platforms

### Threats
- **Bactery AB** entering market 3-4 years earlier
- **Passive RFID** improving in accuracy and range
- **CR2032 status quo** inertia in agriculture
- **Biodegradable battery research** reaching market
- **Patent/IP barriers** from Empa or others
- **Certification costs** (CE, FCC, RoHS ~€30k) may exceed early budget
- **Funding winter** for deep-tech hardware

---

## 6. Patent Landscape Summary

| Area | Key Patents | MykoVolt Risk |
|---|---|---|
| Fungal MFC methods | Mostly open literature (Reyes, Sukri, Sekrecka-Belniak published OA) | LOW — no known blocking patents |
| Bacterial MFC | Multiple patents (water treatment focus) | LOW — different biology |
| Biodegradable electronics | MycelioTronics (2022, method) | LOW — different application |
| Soil moisture sensors | Many (capacitance, frequency domain) | LOW — MykoVolt doesn't sense moisture directly |
| NFC/RFID with energy harvesting | Many (very crowded space) | MEDIUM — need FTO analysis |

---

## 7. Competitive Strategy Implications

1. **Bactery AB is the benchmark** — everything MykoVolt achieves must be compared to Bactery's progress
2. **Passive RFID is the budget killer** — if farmers only need wet/dry, RFID wins at €0.50
3. **Research labs are the only Phase 1 beachhead** — no agricultural market access before 2030
4. **Differentiation must be on data quality + biodegradability** — not on cost alone
5. **P. chrysosporium risk must be managed explicitly** — if 150× doesn't reproduce in pellet form, MykoVolt has a power problem for LoRa
6. **Regulatory moat is real** — EU Battery Regulation favors biodegradable alternatives
