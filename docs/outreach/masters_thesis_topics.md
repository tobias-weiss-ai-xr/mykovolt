# MykoVolt — Master's Thesis Topics

> **11 topics · 5 work packages · Start: Q4 2026**
>
> Strategy doc: [`PARADIGM.md`](../strategy/PARADIGM.md) · Lab setup: [`SOHO_LAB_PIPELINE.md`](../lab/SOHO_LAB_PIPELINE.md)

---

## Why Master's Theses?

Master's students are a **zero-cost R&D engine** for pre-seed startups:

| MykoVolt gets | Student gets |
|----------------|--------------|
| 6 months focused research (€0 if uni-funded) | Real-world problem, not toy project |
| IP + publications for grant applications | Co-authorship on papers |
| Peer-reviewed validation for investors | Patent inventor credit |
| Pilot data for Hessen Ideen / EXIST | Industry network & startup experience |

**Timing:** Results feed directly into Hessen Ideen (Q1 2027) and EXIST (Q2 2027) applications as preliminary data.

**SOHO Lab:** Most topics can start on MykoVolt's in-house hardware (Pi 5 + Hailo-8 + Anycubic Kobra S1 + Ender 3). Students who need wet-lab access work at their university but validate against our prototypes.

---

## WP1: Fungal Bioelectrochemistry

### 1.1 — Strain Screening for Maximum Power Density
**Degree:** M.Sc. Biotechnology / Microbiology
**Start:** Q4 2026 · **SOHO Lab:** Soil MFC + 3D-Printed MFC (Phase 1)
**Papers:** #2 (sediment MFC), #5 (*Ganoderma* growth), #8 (optimal conditions), #10 (soil microbes), #14 (wastewater fungi), #33 (soil bioelectrogenesis)

**Research question:** Which fungal species produce the highest stable power output in a low-cost MFC, and can we beat the Empa baseline of 12.5 µW/cm²?

**Approach:**
- Build 10 identical MFC chambers (3D-printed, from our [lab pipeline](../lab/SOHO_LAB_PIPELINE.md))
- Screen 8-10 strains: *Trametes versicolor*, *Phanerochaete chrysosporium*, *Pleurotus ostreatus*, *Ganoderma lucidum*, *Neurospora crassa*, *Aspergillus niger*, plus 2-3 soil isolates
- Measure: OCV, power density (µW/cm²), polarization curves, longevity (>30 days)
- Test co-cultures (white-rot anode + yeast cathode) for synergistic effects

**Target:** 50 µW/cm² stable output (4× Empa baseline)

**Deliverables:**
- Open strain-performance dataset (published on GitHub → feeds Knowledgebase pillar)
- Optimized inoculation protocol
- 1 paper (*Bioelectrochemistry* / *Bioresour. Technol.*)
- Patent: top-performing strain combinations

---

### 1.2 — Laccase Immobilization on Carbon Electrodes
**Degree:** M.Sc. Biochemistry / Molecular Biology
**Start:** Q2 2027
**Papers:** #15 (mycelial electron transfer), #20 (electrode materials), #23 (electrode placement), #35 (power density improvements)

**Research question:** Can immobilized fungal laccase on carbon cloth electrodes sustain direct electron transfer without mediators, and for how long?

**Approach:**
- Extract laccase from *T. versicolor* (commercial or in-house)
- Immobilize on carbon cloth via: (a) physical adsorption, (b) covalent (glutaraldehyde), (c) entrapment (alginate)
- Cyclic voltammetry + chronoamperometry to characterize electron transfer kinetics
- Test stability: daily measurements over 21 days

**Target:** 2-5× current density vs. free enzyme; >14 days stable activity

**Deliverables:**
- Immobilization protocol (open, feeds Knowledgebase)
- Kinetic parameters (Km, Vmax, kcat)
- 1 paper (*ACS Applied Materials* / *Enzyme Microb. Technol.*)

---

## WP2: Manufacturing & Materials

### 2.1 — Compression-Molded MFC Pellets
**Degree:** M.Sc. Materials Science / Chemical Engineering
**Start:** Q4 2026 · **SOHO Lab:** 3D-Printed MFC → compression mold tooling (Ender 3 laser)
**Papers:** #8 (chamber geometry), #12 (substrate comparison), #35 (power density), #47 (monitoring protocols)
**Priority:** 🔴 **Critical** — core manufacturing IP for Hessen Ideen + EXIST

**Research question:** Can compression-molded cellulose-carbon-graphite pellets host living fungi and produce usable power? What formulation and process parameters maximize both conductivity and fungal viability?

**Approach:**
- Design compression mold (laser-cut acrylic from Ender 3, or 3D-printed on Kobra S1)
- Formulate composites: cellulose (30-60%) + carbon black (10-30%) + graphite (10-30%)
- Vary: pressure (10-100 bar), temperature (20-80°C), dwell time (1-60 min)
- Characterize: bulk conductivity (4-point probe), porosity (mercury intrusion), crush strength
- Test fungal viability post-compression: CFU counts, metabolic activity (CO₂ evolution)
- Head-to-head: 3D-printed (Empa-style) vs. compression-molded (MykoVolt-style)

**Target:** >10 S/m conductivity + >80% fungal survival + 50 µW/cm² output

**Deliverables:**
- Optimized formulation + process window (feeds Hardware Platform pillar)
- 1 paper (*Green Chemistry* / *ACS Sustainable Chem. Eng.*)
- Patent: compression-molded MFC architecture
- Preliminary data for Hessen Ideen application (Q1 2027)

---

### 2.2 — Biodegradable IP67 Encapsulation
**Degree:** M.Sc. Materials Science / Polymer Chemistry
**Start:** Q2 2027 · **SOHO Lab:** 3D-printed test fixtures for coating trials
**Papers:** #12 (substrate compatibility), regulatory context from compliance roadmap

**Research question:** Can a compostable coating provide IP67 water protection for 7-30 days, then fully degrade in soil?

**Approach:**
- Screen biopolymers: PLA, PHA, starch-PLA blends, shellac, beeswax
- Apply dip-coating and spray-coating on MFC pellets
- Water ingress: gravimetric (weight gain) + electrical (impedance change)
- Accelerated aging: 40°C/90% RH cycling
- Compostability: EN 13432 disintegration test (industrial compost, 12 weeks)

**Target:** 14-day IP67 @ <€0.05/unit; full degradation in 90 days (compost)

**Deliverables:**
- Coating formulation + application protocol
- 1 paper (*Polymer Degradation and Stability*)
- EN 13432 preliminary data (for DBU application)

---

## WP3: Electronics & Embedded Systems

### 3.1 — Ultra-Low-Power Firmware for µW-Scale Energy Harvesting
**Degree:** M.Sc. Electrical Engineering / Embedded Systems
**Start:** Q4 2026 · **SOHO Lab:** Existing sensor board design + Pi 5 for profiling
**Papers:** #47 (monitoring protocols) + KiCad design in `hardware/kicad/`

**Research question:** What is the minimum energy budget for a capacitive soil sensor reading + NFC transmission, and how close can we get STM32L0 firmware to the theoretical limit?

**Approach:**
- Start from existing [sensor board design](../technical/sensor_board_design.md) (STM32L0 + BQ25570 + FDC1004)
- Profile every subsystem: MCU (STOP/LPSLEEP), FDC1004 (single conversion), ST25DV (passive NFC), PCF8523 (RTC wakeup)
- Implement adaptive sampling: vary measurement interval based on harvested energy (BQ25570 VBAT_OK)
- Build energy budget model: µJ per measurement cycle, µJ per day, days to depletion
- Optimize: gate clock domains, minimize wake time, batch measurements

**Target:** <30 µW average (improves on current 4.6 µA @ 3.3V ≈ 15 µW by 2× duty cycle margin)

**Deliverables:**
- Open-source firmware ([GitHub](https://github.com/tobias-weiss-ai-xr/mykovolt), MIT)
- Energy profiling toolkit (Python + INA219 scripts)
- 1 paper (*SenSys* / *IEEE Sensors Journal*)
- Hardware files (KiCad, CERN-OHL-P)

---

### 3.2 — AI-Optimized Fungal Growth Detection
**Degree:** M.Sc. Computer Science / AI & Vision
**Start:** Q1 2027 · **SOHO Lab:** Pi 5 + Hailo-8 + Camera → [Edge AI Vision](../lab/SOHO_LAB_PIPELINE.md)
**Papers:** #5 (*Ganoderma* growth patterns), #15 (electrical signaling), #47 (monitoring)
**NEW topic** — replaces generic soil calibration

**Research question:** Can a Hailo-8 neural network running on a Raspberry Pi 5 segment fungal growth from time-lapse images with >95% accuracy, enabling automated MFC monitoring?

**Approach:**
- Collect time-lapse dataset: daily photos of MFC chambers (10+ strains, 30+ days each)
- Annotate: fungal coverage (% area), growth stage, contamination
- Train MobileNetV2 / YOLOv8-nano on Hailo-8 (26 TOPS, <4W)
- Deploy on Pi 5 for real-time inference (target: 30 FPS)
- Integrate with voltage measurement (ADC) → correlate growth phase with bioelectricity output
- Publish open dataset (first of its kind → feeds Knowledgebase pillar)

**Target:** >95% segmentation accuracy; <10ms inference per frame; <5W total system power

**Deliverables:**
- Open fungal growth image dataset (feeds Knowledgebase pillar)
- Hailo-8 optimized model + Pi 5 deployment code
- 1 paper (*Computers and Electronics in Agriculture* / *Sensors*)
- Foundation for [Agentic Harness](../strategy/PARADIGM.md) offering

---

## WP4: Environment & Lifecycle

### 4.1 — Cradle-to-Grave LCA: Fungal MFC vs. Li-ion CR2032
**Degree:** M.Sc. Environmental Engineering / Sustainability
**Start:** Q1 2027 · **SOHO Lab:** Not needed — desk study + OpenLCA
**Papers:** All 90 papers inform boundary conditions and assumptions

**Research question:** Over its full lifecycle, does a fungal MFC sensor have a lower carbon footprint than a Li-ion-powered equivalent, and by how much?

**Approach:**
- Functional unit: 1 soil moisture measurement per day for 30 days
- Compare: (a) MykoVolt fungal MFC + NFC, (b) CR2032 Li-ion + BLE
- System boundaries: cradle-to-grave (raw materials → manufacturing → use → disposal/compost)
- Impact categories: GWP100, eutrophication, acidification, cumulative energy demand, e-waste
- Sensitivity analysis: scale (1K → 1M units/year), power density improvements, pellet formulation

**Target:** >50% GWP reduction vs. Li-ion; publish as open LCA dataset

**Deliverables:**
- Full LCA model (OpenLCA, open-source)
- Environmental product declaration (EPD, preliminary)
- 1 paper (*Journal of Cleaner Production*)

---

### 4.2 — Soil Biodegradation Kinetics of MFC Pellets
**Degree:** M.Sc. Soil Science / Environmental Microbiology
**Start:** Q1 2027 · **SOHO Lab:** 3D-printed test fixtures for field burial
**Papers:** #2 (sediment MFC), #12 (substrate), #14 (wastewater)

**Research question:** How fast do compression-molded MFC pellets degrade across soil types, temperatures, and moisture levels?

**Approach:**
- Bury pellets in 3 soil types (sand, loam, clay) at 2 depths (10 cm, 30 cm)
- Monitor: mass loss (weekly), CO₂ evolution (alkali trap), visual degradation
- Lab mesocosms for controlled temperature (10°C, 20°C, 30°C) and moisture (30%, 60%, 90% field capacity)
- Model: first-order + Arrhenius temperature dependence
- Analyze residual: heavy metals (ICP-MS), persistent organics (GC-MS)

**Target:** 90% mass loss in <90 days (compost), <180 days (soil); zero toxic residues

**Deliverables:**
- Degradation rate model (open-source Python)
- 1 paper (*Soil Biology & Biochemistry*)
- OK Compost preliminary data (for certification)

---

## WP5: Applications & Field Validation

### 5.1 — Precision Agriculture: Sensor Density Optimization
**Degree:** M.Sc. Agronomy / Precision Agriculture / Agri-Tech
**Start:** Q2 2027 · **SOHO Lab:** Prototypes for field deployment
**Papers:** #2 (sediment), #10 (soil), #33 (soil bioelectrogenesis)

**Research question:** What sensor density and deployment depth maximize irrigation water savings in row crops, using MykoVolt's compostable sensors?

**Approach:**
- Partner with 1-2 farms (Hessen region)
- Deploy MykoVolt sensors at 3 depths (10, 20, 30 cm) × 3 densities (10, 50, 100/ha)
- Reference measurement: TDR probe + gravimetric sampling
- Correlate soil moisture with crop stress indicators (NDVI from drone/satellite)
- Economic model: water saved × water price vs. sensor cost per hectare

**Target:** >20% irrigation savings; ROI <1 growing season

**Deliverables:**
- Deployment protocol (depth, density, crop-specific)
- ROI calculator (open-source spreadsheet)
- 1 paper (*Agricultural Water Management*)
- Pilot customer testimonial → EXIST validation

---

### 5.2 — Compost Process Monitoring with Disposable Sensors
**Degree:** M.Sc. Waste Management / Bioprocess Engineering
**Start:** Q2 2027 · **SOHO Lab:** Prototypes for industrial deployment
**Papers:** #2 (sediment MFC), #10 (soil microbes)

**Research question:** Can MykoVolt sensors embedded in compost windrows provide actionable temperature/moisture data for process optimization, then decompose with the compost?

**Approach:**
- Partner with municipal or industrial composting facility (Hessen region)
- Embed sensors in windrows at 3 positions (core, mid, surface)
- Monitor: temperature, moisture (capacitive), O₂ (if multi-parameter node)
- Correlate with compost quality: C/N ratio, pathogen reduction (E. coli, Salmonella), maturity (germination test)
- Compare: sensor-optimized aeration vs. standard schedule

**Target:** >15% reduction in composting time or energy use

**Deliverables:**
- Process control algorithm (open-source)
- 1 paper (*Waste Management* / *Bioresour. Technol.*)
- Pilot facility partnership → DBU validation

---

## Priority Matrix

Which topics to recruit first:

| Priority | Topic | Why | Grant Impact |
|:--------:|-------|-----|:------------:|
| 🔴 P0 | **2.1 Compression-Molded Pellets** | Core manufacturing IP | Hessen Ideen |
| 🔴 P0 | **3.1 Ultra-Low-Power Firmware** | Functional prototype | Hessen Ideen + EXIST |
| 🟡 P1 | **1.1 Strain Screening** | Power density data | EXIST |
| 🟡 P1 | **4.1 LCA** | Environmental narrative | All grants |
| 🟢 P2 | **3.2 AI Growth Detection** | Novel dataset + Agentic Harness | Horizon Europe |
| 🟢 P2 | **2.2 Biodegradable Encapsulation** | IP67 validation | DBU |
| 🟢 P2 | **1.2 Laccase Immobilization** | Electrode science | BMBF |
| ⚪ P3 | **4.2 Biodegradation Kinetics** | Certification data | DBU |
| ⚪ P3 | **5.1 Precision Agriculture** | Market validation | EXIST |
| ⚪ P3 | **5.2 Compost Monitoring** | Market validation | DBU |

**Recommendation:** Recruit 2 P0 students immediately (Q4 2026) + 1-2 P1 students (Q1 2027).

---

## How Topics Map to the Three Pillars

| Pillar | Topics | Output |
|--------|--------|--------|
| **Open Knowledgebase** | 1.1, 1.2, 3.2, 4.1 | Open datasets, strain rankings, growth images, LCA model |
| **Agentic Harness** | 3.2 | AI growth detection model → foundation for enterprise tool |
| **Hardware Platform** | 2.1, 2.2, 3.1 | Pellet formulation, coating, firmware, sensor board |

---

## IP & Publication Policy

| Aspect | Policy |
|--------|--------|
| **IP ownership** | MykoVolt retains IP; student is named inventor |
| **Publication** | Allowed after patent filing (3-month delay) |
| **Authorship** | Student = first author; MykoVolt = co-author |
| **Open source** | All code, data, firmware published on GitHub (MIT / CERN-OHL-P) |
| **Thesis access** | Public after grade awarded (no embargo) |

**Patent pipeline (from thesis work):**
1. Compression-molded MFC pellet formulation (from 2.1, Q2 2027)
2. Top-performing strain combinations (from 1.1, Q3 2027)
3. Biodegradable encapsulation coating (from 2.2, Q4 2027)
4. AI fungal growth detection method (from 3.2, Q1 2028)

---

## Recruitment

### Target Universities (Hessen region)
- **TU Darmstadt** — Materials science, embedded systems
- **Goethe Uni Frankfurt** — Biochemistry, microbiology
- **Uni Marburg** — Fungal biology (excellent mycology group)
- **JLU Giessen** — Agricultural science, soil science
- **Uni Kassel** — Environmental engineering
- **KIT Karlsruhe** (reachable) — Industrial biotech

### Supervision Model
Each student has:
- **Academic supervisor** (professor at their university — provides lab access + grading)
- **Industry mentor** (MykoVolt — provides problem definition, hardware, data, IP guidance)

### Funding
| Source | Amount | Covers |
|--------|--------|--------|
| University grant | €0-450/month | Standard thesis funding |
| MykoVolt stipend | €500/month | If uni-funded insufficient |
| HiWi (student assistant) | €13.50/hr | Up to 10 hrs/week |
| DAAD | varies | International students |

---

## 12-Month Targets

| Metric | Target |
|--------|--------|
| Active theses | 4 (2× P0 + 1× P1 + 1× P2) |
| Completed theses | 2-3 |
| Journal submissions | 3-4 |
| Patents filed | 1-2 |
| Open datasets published | 3-4 |
| Grant applications with thesis data | 2-3 (Hessen Ideen, EXIST, DBU) |

---

*Last updated: 2026-08-16 — [SOHO Lab](../lab/SOHO_LAB_PIPELINE.md) operational, recruiting P0 students for Q4 2026*
