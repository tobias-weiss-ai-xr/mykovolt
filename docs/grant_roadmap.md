# MykoVolt — Grant Application Roadmap

## Executive Summary

**MykoVolt** develops the world's first biodegradable fungal bio-battery for disposable IoT sensors. Our technology enables a fundamentally new deployment pattern: **drop-and-forget sensor networks** that operate underground, in darkness, and compost away at end-of-life — zero e-waste, zero retrieval required.

---

## How the Battery Works

### Core Technology: Microbial Fuel Cell (MFC)

A fungal bio-battery is not a classical battery — it's a biological power plant at microscale. Two living fungal species work together:

| Component | Organism | Function |
|-----------|----------|----------|
| **Anode (−)** | *Saccharomyces cerevisiae* (yeast) | Metabolism releases electrons from organic substrate |
| **Cathode (+)** | *Trametes pubescens* (white-rot fungus) | Produces laccase enzyme → accepts electrons, reduces oxygen to water |
| **Electrolyte** | Cellulose matrix | Proton exchange membrane, biodegradable |
| **Housing** | Compostable pellet | IP67 protection, decomposes in 30-90 days |

### Electron Flow

```
Glucose → Yeast metabolism → NADH → Anode → External circuit → Cathode → Laccase → O₂ → H₂O
```

The fungi are embedded in a cellulose-based conductive ink (carbon black + graphite flakes), 3D-printed or compression-molded into a pellet. The system is dry-storable and activated on-site with water + nutrients.

### Performance (Current State)

| Metric | Value | Target (Phase 2) |
|--------|-------|------------------|
| Power density | 12.5 µW/cm² (Empa baseline) | ~260 µW/cm² (optimized) |
| Open circuit voltage | 0.45V (boost to 3.3V) | 0.6-0.8V |
| Runtime | 7 days @ 15-min intervals | 30+ days |
| Cost | €0.15/unit | €0.08/unit @ scale |
| Biodegradability | 90% compostable (pellet + electronics separate) | 100% (retrievable electronics) |

### Key Innovation

The highest documented fungal MFC performance (*Phanerochaete chrysosporium*: 1.9 W/m²) was achieved with conventional reactor architecture, **not** 3D-printing or compression-molded pellets. **MykoVolt's core IP** is combining high-performance fungal strains + scalable manufacturing (compression molding, not 3D printing) + full biodegradability. This combination is **unsolved** — that's the opportunity.

---

## The Pattern: Drop-and-Forget Sensor Networks

### What Makes This Different?

| Deployment Model | Classical Battery | Solar + Battery | MykoVolt |
|------------------|-------------------|-----------------|----------|
| **Surface required** | No | ✅ Yes (panel needs light) | No |
| **Retrieval required** | ✅ Yes (replace/recycle) | ✅ Yes (maintenance) | ❌ No (composts) |
| **E-waste** | ✅ Yes (Li-ion, toxic) | ✅ Yes (panel + battery) | ❌ No (90% biodegradable) |
| **Underground operation** | ✅ Yes | ❌ No (panel needs surface) | ✅ Yes |
| **Darkness operation** | ✅ Yes | ❌ No | ✅ Yes |
| **Unit cost** | €2-5 (battery + labor) | €15-30 (panel + install) | **€0.15** |
| **Installation** | Manual placement + retrieval | Surface mounting + wiring | **Drop and forget** |

### The Paradigm Shift

**Classical sensors** are assets you deploy, maintain, and eventually retrieve. They're expensive, require labor, and create e-waste.

**MykoVolt sensors** are consumables. You deploy them like seeds — hundreds per hectare, fully buried, no retrieval. At end-of-life, the battery and housing compost into the soil; only the electronics board (€0.50, 100+ reuse cycles) is retrieved.

This unlocks **dense, distributed sensor networks** at a cost and deployment model previously impossible.

---

## Application Roadmap

### Phase 1: DevKit (2025-Q3 to 2026-Q2)
**Goal:** Prove the technology with low-regulation, high-margin applications.

| Application | Market | Why MykoVolt Wins |
|-------------|--------|-------------------|
| **Soil moisture (agriculture)** | Precision ag, viticulture, turf management | Underground operation, €0.15/unit, compostable |
| **Compost monitoring** | Municipal composting, industrial biowaste | Works *inside* compost piles (dark, moist, perfect for fungal metabolism) |
| **Structural health (concrete curing)** | Construction, infrastructure | Embedded in concrete during pouring — no light, no retrieval |
| **Cold-chain loggers** | Food/pharma shipping | Disposable, compostable, no Li-ion in food containers |
| **Research/education kits** | Universities, schools | Safe, biodegradable, teaches synthetic biology + IoT |

**Target customers:** Research institutions, pilot farms, composting facilities, construction companies.

**Grant fit:** Hessen Ideen (early-stage R&D), EXIST (university spinoff).

---

### Phase 2: Feldpilot (2026-Q3 to 2027-Q2)
**Goal:** Field-ready product with LoRa telemetry, IP67 housing, 30+ day runtime.

| Application | Market | Why MykoVolt Wins |
|-------------|--------|-------------------|
| **Forestry / under-canopy sensing** | Carbon credits, wildfire detection, biodiversity monitoring | Zero light under canopy — solar is dead |
| **Permafrost monitoring** | Climate research, Arctic infrastructure | Solar is seasonal (polar night); fungal batteries work continuously |
| **Landfill / waste monitoring** | Environmental compliance, methane capture | Works inside waste piles; no retrieval in hazardous zones |
| **Wildlife tracking tags** | Conservation, ecology | €0.15 disposable tags — no retrieval, no harm if ingested |
| **Smart packaging** | Food/pharma logistics | Compostable temperature abuse indicators |

**Target customers:** Environmental agencies, forestry services, logistics companies, conservation NGOs.

**Grant fit:** Horizon Europe (Bio-based Industries), BMBF (climate tech), DBU (environmental innovation).

---

### Phase 3: Commercial Scale (2027-Q3+)
**Goal:** Mass production (10,000+ units/day), diversified product line.

| Application | Market | Why MykoVolt Wins |
|-------------|--------|-------------------|
| **Agricultural sensor networks** | Row crops, vineyards, orchards | Dense deployment (100+ sensors/ha), no retrieval labor |
| **Medical disposable sensors** | Wound dressings, pill bottles, diagnostics | Single-use, biocompatible, no Li-ion waste |
| **Unexploded ordnance / landmine monitoring** | Defense, humanitarian demining | Long-term passive monitoring, biodegradable (no cleanup) |
| **Soil carbon verification** | Carbon credits, regenerative agriculture | Buried sensors verify carbon sequestration — trusted data, zero maintenance |
| **Smart city infrastructure** | Underground utilities, flood detection | Embedded in soil/concrete, no battery replacement |

**Target customers:** Agribusiness, medical device companies, defense contractors, carbon credit verifiers, municipalities.

---

## Grant Strategy

### Hessen Ideen (2025-Q4)
**Focus:** Early-stage innovation, Hesse-based startups.

**Application angle:**
- University spinoff (if applicable) or Hesse-based R&D
- Biotechnology + IoT + sustainability (triple alignment with state priorities)
- Job creation potential (R&D lab, production facility)
- Proof-of-concept funding (€50k-150k range)

**Key metrics to highlight:**
- TRL 3-4 (lab prototype → functional prototype)
- 12.5 µW/cm² baseline → 260 µW/cm² target
- €0.15/unit cost structure
- 90% biodegradability

**Timeline:** Application deadline typically Q1/Q2, decision Q3.

---

### EXIST Forschungstransfer (2026-Q1)
**Focus:** University-to-market technology transfer.

**Application angle:**
- Technology transfer from Empa (CH) or partner university
- Founding team: technical + business co-founders
- 18-month runway to prototype + pilot customers
- Funding: €250k-500k (personnel + materials + coaching)

**Key metrics to highlight:**
- IP position (patent pending on compression-molded fungal MFC)
- Pilot customers (farms, composting facilities, research institutes)
- Team: fungal biology + electronics + business development
- Path to Series A (2027)

**Timeline:** Rolling applications, 8-12 week review.

---

### Horizon Europe — Bio-based Industries (2026-Q2)
**Focus:** Circular economy, bio-based materials, industrial biotechnology.

**Application angle:**
- Circular economy: compostable electronics
- Bio-based materials: cellulose matrix, fungal cultivation
- Industrial biotech: scaled fungal fermentation
- Cross-border consortium (DE + CH + FR partners)

**Key metrics to highlight:**
- GWP reduction vs. Li-ion (LCA analysis)
- Biodegradability certification (EN 13432, OK Compost)
- Scale-up pathway (lab → pilot → production)
- Consortium: universities, industry partners, end-users

**Funding:** €2-5M (multi-partner consortium).

**Timeline:** Annual calls (typically Q1), decision Q3-Q4.

---

### BMBF — Bioökonomie (2026-Q3)
**Focus:** Bioeconomy, sustainable production, climate tech.

**Application angle:**
- Bio-based alternative to Li-ion batteries
- Climate tech: enables precision ag (reduced water/fertilizer) + carbon monitoring
- Sustainable production: fungal fermentation vs. mining
- German/European supply chain independence (no Li/Co from China/Congo)

**Key metrics to highlight:**
- Supply chain: European cellulose, German fungal strains
- Climate impact: reduced e-waste, improved ag efficiency
- Economic impact: German production facility, jobs

**Funding:** €500k-2M (national projects).

**Timeline:** Annual calls.

---

### DBU — Umweltinnovation (2026-Q4)
**Focus:** Environmental innovation, proven technologies.

**Application angle:**
- E-waste reduction (disposable sensors without Li-ion)
- Environmental monitoring (soil health, water quality, biodiversity)
- Circular economy: compostable at end-of-life
- DBU typically funds *demonstration* projects (not basic R&D)

**Key metrics to highlight:**
- Pilot deployment (100+ sensors in field)
- Measurable environmental benefit (e-waste avoided, water saved)
- Partnership with environmental organizations

**Funding:** Up to €300k (50% of eligible costs).

**Timeline:** Rolling applications.

---

## Technical Milestones

| Milestone | Target Date | Grant Dependency |
|-----------|-------------|------------------|
| **Pellet formulation (compression molding)** | 2025-Q3 | Hessen Ideen |
| **Board design Rev A (ultra-low-power)** | 2025-Q3 | EXIST |
| **Functional prototype (7-day runtime)** | 2025-Q4 | EXIST |
| **L2 system test (field validation)** | 2026-Q1 | EXIST |
| **LoRa integration** | 2026-Q3 | Horizon Europe |
| **Field pilot (100+ sensors)** | 2026-Q4 | DBU |
| **Production scaling (1,000 units/day)** | 2027-Q1 | BMBF |
| **EU market launch** | 2027-Q2 | — |

---

## Team Requirements

| Role | Profile | When Needed |
|------|---------|-------------|
| **CEO / Co-founder** | Business development, grant writing, fundraising | Now |
| **CTO / Co-founder** | Fungal biology, electrochemistry, materials science | Now |
| **Electronics Engineer** | Ultra-low-power design, STM32, LoRa | 2025-Q3 |
| **Fungal Cultivation Tech** | Mycology lab work, strain optimization | 2025-Q4 |
| **Production Engineer** | Scale-up, compression molding, QA | 2026-Q2 |
| **Field Application Engineer** | Pilot deployments, customer support | 2026-Q3 |

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| **Power density insufficient** | Hybrid approach: retrievable electronics (100+ cycles) + compostable battery (single-use) |
| **Scale-up challenges (3D printing → molding)** | Parallel development: 3D printing for prototypes, compression molding for production |
| **Regulatory hurdles (agri/bio)** | Start with low-regulation applications (research, composting, construction) |
| **Competition (Li-ion, solar)** | Focus on niches where competitors can't operate: underground, darkness, disposable |
| **IP position** | Patent pending on compression-molded fungal MFC architecture |

---

## Financial Projections

| Year | Revenue | Units Sold | Burn Rate | Funding Source |
|------|---------|------------|-----------|----------------|
| 2025 | €0 (R&D) | 0 | €20k/mo | Hessen Ideen, EXIST |
| 2026 | €50k (pilots) | 5,000 | €40k/mo | EXIST, Horizon Europe |
| 2027 | €500k (early commercial) | 50,000 | €60k/mo | Series A |
| 2028 | €5M (scale-up) | 500,000 | €150k/mo | Revenue + Series B |

**Unit economics:**
- COGS: €0.15 (battery) + €0.50 (electronics) = €0.65
- ASP: €2.50 (sensor node)
- Gross margin: 74%

---

## Next Steps

1. **Finalize pellet formulation** (compression molding vs. 3D printing decision)
2. **File provisional patent** (compression-molded fungal MFC architecture)
3. **Prepare Hessen Ideen application** (deadline: Q1 2026)
4. **Recruit co-founding team** (CEO + CTO)
5. **Secure pilot customers** (2-3 farms, 1 composting facility, 1 construction partner)
6. **Apply for EXIST** (rolling, submit Q1 2026)
7. **Build consortium for Horizon Europe** (DE + CH + FR partners)

---

## Contact

- **GitHub**: [tobias-weiss-ai-xr/mykovolt](https://github.com/tobias-weiss-ai-xr/mykovolt)
- **Email**: tobias.weiss.ai.xr@gmail.com
- **LinkedIn**: [MykoVolt](https://www.linkedin.com/company/mykovolt)

---

*Last updated: 2026-07-20*
