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

### Performance (Target)

| Metric | Baseline (Empa literature) | Target (Phase 1) | Target (Phase 2) |
|--------|---------------------------|------------------|------------------|
| Power density | 12.5 µW/cm² | 50-100 µW/cm² | ~260 µW/cm² |
| Open circuit voltage | 0.45V | 0.5-0.6V | 0.6-0.8V |
| Runtime | — | 7 days @ 15-min intervals | 30+ days |
| Cost | — | €0.15/unit | €0.08/unit @ scale |
| Biodegradability | — | 90% compostable | 100% (retrievable electronics) |

**Current status (July 2026):** Design complete. **Recruiting team** to build first functional prototype.

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

### Phase 1: DevKit (2026-Q3 to 2027-Q2)
**Goal:** Build first functional prototype, prove the technology with low-regulation, high-margin applications.

| Application | Market | Why MykoVolt Wins |
|-------------|--------|-------------------|
| **Soil moisture (agriculture)** | Precision ag, viticulture, turf management | Underground operation, €0.15/unit, compostable |
| **Compost monitoring** | Municipal composting, industrial biowaste | Works *inside* compost piles (dark, moist, perfect for fungal metabolism) |
| **Structural health (concrete curing)** | Construction, infrastructure | Embedded in concrete during pouring — no light, no retrieval |
| **Cold-chain loggers** | Food/pharma shipping | Disposable, compostable, no Li-ion in food containers |
| **Research/education kits** | Universities, schools | Safe, biodegradable, teaches synthetic biology + IoT |

**Target customers:** Research institutions, pilot farms, composting facilities, construction companies.

**Grant fit:** Hessen Ideen (early-stage R&D), EXIST (university spinoff).

**Current status (July 2026):** **Recruiting team** (co-founders, Master's students) to build prototype. Hessen Ideen application Q4 2026 / Q1 2027.

---

### Phase 2: Feldpilot (2027-Q2 to 2027-Q4)
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

### Phase 3: Commercial Scale (2028-Q1+)
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

### Hessen Ideen (2026-Q4)
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

**Timeline:** Application deadline Q4 2026, decision Q1 2027.

**Status:** Preparing application (August-September 2026).

---

### EXIST Forschungstransfer (2027-Q1)
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
- Path to Series A (2028)

**Timeline:** Rolling applications, 8-12 week review.

**Status:** Prepare Q4 2026, submit Q1 2027.

---

### Horizon Europe — Bio-based Industries (2027-Q2)
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

**Status:** Build consortium Q4 2026 - Q1 2027, submit Q2 2027.

---

### BMBF — Bioökonomie (2027-Q3)
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

**Status:** Prepare Q1-Q2 2027, submit Q3 2027.

---

### DBU — Umweltinnovation (2027-Q4)
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

**Status:** Requires field pilot data (Q2-Q3 2027), submit Q4 2027.

---

## Technical Milestones

| Milestone | Target Date | Grant Dependency |
|-----------|-------------|------------------|
| **Pellet formulation (compression molding)** | 2026-Q3 | Hessen Ideen |
| **Board design Rev A (ultra-low-power)** | 2026-Q3 | EXIST |
| **Functional prototype (7-day runtime)** | 2026-Q4 | EXIST |
| **L2 system test (field validation)** | 2027-Q1 | EXIST |
| **LoRa integration** | 2027-Q2 | Horizon Europe |
| **Field pilot (100+ sensors)** | 2027-Q3 | DBU |
| **Production scaling (1,000 units/day)** | 2027-Q4 | BMBF |
| **EU market launch** | 2028-Q2 | — |

**Current status (July 2026):** **Design complete, recruiting team to build prototype.** Next: compression molding + fungal cultivation (Q4 2026 - Q1 2027).

---

## Team Requirements

| Role | Profile | When Needed | Status |
|------|---------|-------------|--------|
| **CEO / Co-founder** | Business development, grant writing, fundraising | Now | Marc (part-time) |
| **CTO / Co-founder** | Fungal biology, electrochemistry, materials science | Now | ❌ Open |
| **Electronics Engineer** | Ultra-low-power design, STM32, LoRa | 2027-Q1 |
| **Fungal Cultivation Tech** | Mycology lab work, strain optimization | 2027-Q1 |
| **Production Engineer** | Scale-up, compression molding, QA | 2027-Q3 |
| **Field Application Engineer** | Pilot deployments, customer support | 2027-Q3 |

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
| 2026 | €0 (R&D) | 0 | €15k/mo | Bootstrap, Hessen Ideen |
| 2027 | €50k (pilots) | 5,000 | €35k/mo | EXIST, Horizon Europe |
| 2028 | €500k (early commercial) | 50,000 | €60k/mo | Series A |
| 2029 | €5M (scale-up) | 500,000 | €150k/mo | Revenue + Series B |

**Unit economics:**
- COGS: €0.15 (battery) + €0.50 (electronics) = €0.65
- ASP: €2.50 (sensor node)
- Gross margin: 74%

---

## Next Steps (Q3-Q4 2026)

### Immediate Priorities (Q3 2026)

1. **Recruit co-founding team** (CEO + CTO) — *Critical path*
   - CTO profile: fungal biology / electrochemistry / materials science
   - CEO profile: business development, grant writing, fundraising

2. **Recruit Master's thesis students** (3-4 topics) — *Start Q4 2026 / Q1 2027*
   - WP2.1: Compression molding (critical for prototype)
   - WP3.1: Ultra-low-power firmware
   - WP1.1: Fungal strain screening

3. **File provisional patent** (compression-molded fungal MFC architecture) — *Before publications*

4. **Prepare Hessen Ideen application** — *Deadline Q4 2026 or Q1 2027*

5. **Build first prototype** (3D-printed, lab-scale) — *Q4 2026*
   - Validate Empa baseline (12.5 µW/cm²)
   - Test with yeast + Trametes co-culture

### Medium-Term (Q4 2026 - Q1 2027)

6. **Secure pilot customers** (LOIs, not revenue) — *2-3 partners for letters of intent*
   - Research institutions (easiest entry)
   - Pilot farms (viticulture, turf)
   - Composting facilities

7. **Apply for EXIST** — *Submit Q1 2027*

8. **Build consortium for Horizon Europe** — *Q1-Q2 2027*

---

## Contact

- **GitHub**: [tobias-weiss-ai-xr/mykovolt](https://github.com/tobias-weiss-ai-xr/mykovolt)
- **Email**: tobias.weiss.ai.xr@gmail.com
- **LinkedIn**: [MykoVolt](https://www.linkedin.com/company/mykovolt)

---

*Last updated: 2026-07-20 (Q3 2026) — Pre-prototype, recruiting team*
