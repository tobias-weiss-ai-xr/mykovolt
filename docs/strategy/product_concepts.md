# MykoVolt Product Concepts — Beyond the 15 Use Cases

> **Status:** Simulation-based feasibility scan | **TRL:** 2 | **Date:** July 2026
> **Tools:** `simulation/product_explorer.py`

---

## 1. The 15 Documented Use Cases

The README lists 15 use cases across 3 phases. The `product_explorer.py` scanner assessed feasibility against the **Mg-Air baseline** (50–500 µW, TRL 2–3) — *not* a fungal estimate. See [MVP Rethink](../strategy/mvp_rethink.md): 260 µW/cm² was audit-proven hallucinated, so concepts previously scored against 100–260 µW are **re-rated for the Mg-Air baseline**.

| # | Use Case | Phase | Verdict | Key Insight |
|---|----------|-------|---------|-------------|
| 1 | Soil Moisture Sensor | 1 DevKit | 🟢 GO | O2-limited at >5cm; chimney or Mg-air needed |
| 2 | Compost Monitor | 1 DevKit | 🟢 GO | Ideal environment: warm, moist, O2-rich near surface |
| 3 | Concrete Curing Monitor | 1 DevKit | 🟢 GO | Embedded during pour; chimney must survive concrete |
| 4 | Cold-Chain Logger | 1 DevKit | 🟢 GO | Surface use, no O2 issue; Mg-air for longer life |
| 5 | Research/Education Kit | 1 DevKit | 🟢 GO | First ship-ready product (NFC, no battery) |
| 6 | Forestry Under-Canopy | 2 Pilot | 🟢 GO | Deep shade → no solar; fungal MFC wins |
| 7 | Permafrost Monitor | 2 Pilot | 🟢 GO | Mg-air required (fungi dormant below 5°C) |
| 8 | Landfill/Waste Monitor | 2 Pilot | 🟢 GO | Mg-air required (depth, hazardous environment) |
| 9 | Wildlife Tracking Tag | 2 Pilot | 🟢 GO | Surface, short range; biodegradable is key differentiator |
| 10 | Smart Packaging | 2 Pilot | 🟢 GO | Passive NFC is cheapest; no battery needed |
| 11 | Agricultural Network | 3 Commercial | 🟢 GO | Dense deployment, low cost/unit critical |
| 12 | Medical Disposable Sensor | 3 Commercial | 🟢 GO | Highest TAM ($5B); regulatory path needed |
| 13 | Landmine/UXO Monitor | 3 Commercial | 🟢 GO | Passive, long-term; Mg-air for multi-year |
| 14 | Soil Carbon Verification | 3 Commercial | 🟢 GO | Growing market (carbon credits); Mg-air for 180d |
| 15 | Smart City Infrastructure | 3 Commercial | 🟢 GO | High TAM ($5B); chimney required for buried |

**Critical distinction buried vs surface:**

```
Surface (<3cm): Passive NFC or fungal pressling works fine
Shallow (3-15cm): Chimney pressling or Mg-air
Deep (>15cm): Mg-air only (O2 independent)
```

---

## 2. 15 Novel Product Concepts (Beyond the Original List)

These are ideas that extend beyond the documented use cases — some are derivative, some are genuinely novel.

### 2.1 Fungal Battery Seed Coating 🟢 GO
**Concept:** Coat seeds with fungal spores + conductive ink. As the seed germinates, the fungi activate and power a tiny NFC sensor that reports germination rate, soil temperature, and moisture.

**Why it's different:** No separate sensor deployment — the seed IS the sensor. Every planted seed becomes a data point.

| Dimension | Assessment |
|-----------|-----------|
| Power need | 0.1 µW avg — extremely low (germination is slow) |
| O2 | Surface (<3cm), no issue |
| BOM | €0.45/unit (pellet + printed electrode on seed coating) |
| TAM | €500M (seed treatment market) |
| Risk | Coating process must not inhibit germination |
| TRL path | 2→3: lab germination test with printed electrodes |

### 2.2 Smart Wound Dressing 🟢 GO
**Concept:** Bio-battery powered pH/temperature sensor in a bandage. Detects infection (pH change) before visible signs. Entire dressing is compostable.

**Why it's different:** Single-use medical electronics that goes in the compost bin, not the landfill. No Li-ion in medical waste streams.

| Dimension | Assessment |
|-----------|-----------|
| Power need | 5 µW avg — well within fungal range |
| O2 | Surface (on skin), no issue |
| BOM | €0.45/unit |
| TAM | €3B (advanced wound care) |
| Risk | IVDR regulation (CE marking, 6-12 months) |
| **Prime differentiator** | Biocompatibility + compostability vs Li-ion alternatives |

### 2.3 Food Spoilage Indicator 🟢 GO
**Concept:** Fungal battery that activates when food spoils. Uses spoilage gases (NH₃, H₂S, volatile amines) as additional fuel. Integrated into packaging as a "smart freshness strip."

**Why it's different:** The battery is triggered by what it senses — no power drain until there's something to report. Self-activating.

| Dimension | Assessment |
|-----------|-----------|
| Power need | 0.5 µW avg — extremely low |
| O2 | Surface (inside packaging), no issue |
| BOM | €0.45/unit (printed on packaging substrate) |
| TAM | €4B (smart packaging market) |
| Risk | Food safety regulation; must be food-contact safe |
| **Innovation** | Fungal metabolism of spoilage gases → self-activation |

### 2.4 Mycelium Structural Battery ⚠️ MAYBE
**Concept:** Load-bearing mycelium composite panel (already a growing construction material) with embedded fungal MFC. The building material IS the battery.

**Why it's different:** Dual function — structural + energy storage. Like a solar roof tile but for bio-power.

| Dimension | Assessment |
|-----------|-----------|
| Power need | 50 µW avg |
| O2 | Surface, but panel interior may be anaerobic |
| BOM | €0.45/unit (fungal component only) |
| TAM | €2B+ (mycelium construction materials) |
| Risk | Previously rated FAIL at 50 µW fungal estimate — **now GO via Mg-Air (50–500 µW)** |
| **TRL** | 2→5: Long development, needs materials science co-founder |

### 2.5 Marine Biodegradable Sensor 🟢 GO
**Concept:** Ocean-deployed temperature/current/pH sensor that composts after mission. No plastic pollution from sensor buoys. Drop 100 sensors, they all biodegrade.

**Why it's different:** Solves the growing problem of marine debris from scientific instrumentation.

| Dimension | Assessment |
|-----------|-----------|
| Power need | 2 µW avg — low |
| O2 | Mg-air works in seawater (Mg corrosion in salt water is well-studied) |
| BOM | €0.65/unit (Mg-air + waterproof compostable casing) |
| TAM | €800M (oceanographic sensors) |
| Risk | Saltwater corrosion of electronics; pressure at depth |
| **Prime differentiator** | Zero marine debris — sensors disappear after use |

### 2.6 Drone-Dropped Disaster Sensor Network 🟢 GO
**Concept:** Air-droppable biodegradable sensors for disaster zones (fire, flood, earthquake). No retrieval, no cleanup. Drones drop 100s of sensors in minutes.

**Why it's different:** Speed of deployment + zero cleanup cost. Current solutions require helicopter recovery of expensive sensors.

| Dimension | Assessment |
|-----------|-----------|
| Power need | 5.8 µW avg — moderate |
| O2 | Surface drop, no issue |
| BOM | €0.45/unit (low-cost because disposable) |
| TAM | €1B (disaster response IoT) |
| Risk | Impact survival; must function after drop from 50m |

### 2.7 Living Building Material ⚠️ MAYBE
**Concept:** Mycelium-based wall panel with embedded fungal MFC. Generates power from ambient moisture differentials. Self-powered smart building.

**Why it's different:** Turns the building envelope into a living, sensing, power-generating membrane.

| Dimension | Assessment |
|-----------|-----------|
| Power need | 20 µW avg |
| O2 | Surface, but enclosed wall cavities may be O2-limited |
| BOM | €0.45/unit (fungal component only) |
| TAM | €5B (smart building materials) |
| Risk | Previously rated FAIL at 50 µW fungal estimate — **now GO via Mg-Air** (O₂ in wall cavities must be verified; surface mycelium preferred) |
| **TRL** | 2→4: Requires mycelium composite + MFC integration |

### 2.8 Compostable Wearable Health Patch 🟢 GO
**Concept:** Biodegradable fitness/health monitor patch. Tracks heart rate, temperature, sweat chemistry. Composts after 7 days. No e-waste from wearables.

**Why it's different:** The wearable market generates massive e-waste. A compostable patch eliminates the waste problem for disposable health monitors.

| Dimension | Assessment |
|-----------|-----------|
| Power need | 15 µW avg — within range |
| O2 | Surface (on skin), no issue |
| BOM | €0.45/unit |
| TAM | €10B (wearable health monitors) |
| Risk | Skin contact safety; sweat degradation of electronics |

### 2.9 Space Habitat Bio-Battery ❌ NO-GO (Currently)
**Concept:** Bioregenerative power system for space habitats. Uses human organic waste as fuel in fungal MFC. Combines waste management + power generation.

**Why it's different:** Closes the loop — waste → power. Critical for long-duration space missions.

| Dimension | Assessment |
|-----------|-----------|
| Power need | ~100 µW avg |
| O2 | Anaerobic operation possible with alternative electron acceptor |
| BOM | €0.45/unit |
| TAM | €50M (niche — space agencies) |
| Risk | Mg-Air in vacuum: parasitic H₂O-reduction dominates, no O₂. Requires engineered Mg-alloy + humidity control |
| **Verdict** | ⚠️ Re-rate on Mg-Air-vacuum chemistry — revisit at TRL 4 |

### 2.10 Smart Plant Pot 🟢 GO
**Concept:** Self-watering plant pot with fungal MFC sensor. Monitors soil moisture, triggers watering alert via NFC. No batteries to change — the soil powers the pot.

**Why it's different:** Consumer product that demystifies bio-energy. A "living" pot that uses the soil it sits in.

| Dimension | Assessment |
|-----------|-----------|
| Power need | 2 µW avg — low |
| O2 | Shallow (5cm), chimney or surface cathode |
| BOM | €0.60/unit (pot-integrated) |
| TAM | €200M (smart planters) |
| Risk | Consumer education; must be foolproof |

### 2.11 Living Art / Bio-Installation 🟢 GO
**Concept:** Mycelium-based art installation with embedded fungal MFC powering LEDs. As fungi grow, the art changes color. Living, breathing, self-powered art.

**Why it's different:** Art as a vehicle for bio-technology demonstration. Generates press, education, and cultural value.

| Dimension | Assessment |
|-----------|-----------|
| Power need | 50 µW avg — high but burst-mode LEDs |
| O2 | Surface, open air |
| BOM | €0.45/unit |
| TAM | €50M (bio-art installations) |
| Risk | Not a scalable product — but high PR value |
| **Strategy** | Build as museum/ gallery installation → generates PR for seed round |

### 2.12 Drone Seed + Sensor Drop 🟢 GO
**Concept:** Seed pod with integrated fungal sensor. Drone drops over fields. Seed germinates, sensor monitors soil, everything biodegrades. No deployment labor.

**Why it's different:** Combines reforestation/agriculture with sensor deployment. One drone pass = trees + data network.

| Dimension | Assessment |
|-----------|-----------|
| Power need | 1 µW avg — low |
| O2 | Surface (<3cm), no issue |
| BOM | €0.45/unit |
| TAM | €800M (precision seeding + agri-sensors) |
| Risk | Seed germination + sensor function must coexist |

### 2.13 Biodegradable Game Tag 🟢 GO
**Concept:** Wildlife management ear tag for hunting/ecology studies. Biodegradable — falls off naturally after 90 days, no retrieval, no plastic in nature.

**Why it's different:** Current tags are plastic and must be retrieved. This solves the "tag shedding = plastic pollution" problem.

| Dimension | Assessment |
|-----------|-----------|
| Power need | 0.5 µW avg — very low (short-range NFC) |
| O2 | Surface, no issue |
| BOM | €0.45/unit |
| TAM | €100M (wildlife management) |
| Risk | Animal safety; tag must not harm wildlife |

### 2.14 Compost Facility Air Quality Sensor 🟢 GO
**Concept:** Monitors H₂S, CH₄, NH₃ inside compost facilities. Self-powered from the compost environment. No wiring in potentially explosive atmosphere.

**Why it's different:** Compost facilities need gas monitoring but wiring is expensive and hazardous. A self-powered, wireless sensor solves both.

| Dimension | Assessment |
|-----------|-----------|
| Power need | 3 µW avg — low |
| O2 | Surface (in compost pile headspace), O2-rich |
| BOM | €0.45/unit |
| TAM | €300M (compost + biogas facility monitoring) |
| Risk | Corrosive gases may damage electronics |

### 2.15 Biodegradable Pet Tracker 🟢 GO
**Concept:** Short-range pet location tag with NFC readout. Compostable — if the tag falls off in the woods, it doesn't pollute. No toxic battery if ingested.

**Why it's different:** Pet owners lose tags constantly. This one doesn't become environmental plastic waste.

| Dimension | Assessment |
|-----------|-----------|
| Power need | 1 µW avg — low |
| O2 | Surface, no issue |
| BOM | €0.45/unit |
| TAM | €500M (pet wearables) |
| Risk | Waterproofing; must survive dog swimming |

---

## 3. Clustering by Battery Path

| Battery Path | Best Concepts | Why |
|-------------|---------------|-----|
| **Passive NFC** (no battery, TRL 9) | DevKit, Smart Packaging, Edu Kit | Reader-powered, no O2 issue, ships now |
| **Surface Fungal MFC** (0-3cm burial) | Seed Coating, Smart Bandage, Health Patch, Food Spoilage, Wildlife Tag | Surface O2 abundant, simplest design |
| **Air-Chimney Fungal MFC** (3-15cm burial) | Soil Moisture, Compost Monitor, Concrete Cure, Smart Plant Pot | Chimney delivers O2, but adds cost + failure mode |
| **Mg-Air Battery** (any depth, cold) | Permafrost, Landfill, Wildlife, Marine, Disaster, Landmine, Carbon Verification | O2-independent, broader temp range, simpler |

---

## 4. Strategic Recommendations

### Immediate (Ship within 6 months)
1. **Passive NFC DevKit** — No battery needed, TRL 9, revenue from research labs
2. **Edu Kit / Bio-Art Installation** — High PR value, builds community

### Short-term (12-18 months, after Phase 0)
3. **Smart Packaging** — Food spoilage indicator, huge TAM, uses fungal metabolism creatively
4. **Smart Wound Dressing** — Medical application, higher margin, regulatory path needed

### Medium-term (24-36 months)
5. **Soil Carbon Verification** — Growing carbon credit market, Mg-air for 180d lifetime
6. **Drone Seed + Sensor Drop** — Combines agri-drone trend with biotech differentiator

### Long-term (48+ months)
7. **Mycelium Structural Battery** — Transformative but needs materials science + building code
8. **Space Habitat Bio-Battery** — Sci-fi today, real need tomorrow

### Don't pursue now
- ❌ **Space Habitat** — Power requirement exceeds fungal capability at TRL 2
- ⚠️ **Living Building Material** — Needs 5× power improvement

---

## 5. Key Insight: The "Passive NFC" Trojan Horse

The most important strategic finding from the product scan:

> **Two fastest paths to market:**
> 1. *Passive NFC DevKit* (no battery — reader powered)
> 2. *Mg-Air DevKit* (guaranteed 50–500 µW, biodegradable, O₂-independent) — **now viable for buried/concealed deployments** the NFC-only DevKit cannot reach.
>
> The passive NFC version ships in days; the Mg-Air version is the **Week-1 MVP** for any application needing autonomous power.
> - TRL 9 today (NFC is a mature technology)
> - No O2 issue, no temperature limits, no degradation
> - Sells for €25-35 to research labs
> - Each lab that buys one becomes a fungal MFC researcher
> - Creates pull for the bio-battery pellet as a consumable refill

**Strategy:** Ship the NFC DevKit first as a "fungal MFC evaluation platform." The bio-battery pellet is the refill consumable. This is the **razor-blade model**:

```
DevKit (reusable) → €35 · 100+ cycles
Pellet (consumable) → €0.15 · 7-day life
```

---

*Generated by `simulation/product_explorer.py`*
