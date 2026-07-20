# MykoVolt — Master's Thesis Topics

## Strategy

Master's theses are a **cost-effective R&D engine** for early-stage startups:
- Students get real-world problems, publications, IP experience
- You get 6 months of focused research per topic (€0 direct cost if university-funded)
- Builds IP portfolio before grant applications
- De-risks technology for investors (peer-reviewed validation)

**Ideal timing:** Start thesis recruitment 3-6 months before grant deadlines. Thesis results feed directly into Hessen Ideen / EXIST applications as "preliminary data".

---

## Thesis Topics by Work Package

### WP1: Fungal Strain Optimization & Power Density

#### Topic 1.1: High-Performance Fungal Strains for MFCs
**Degree:** M.Sc. Biotechnology / Microbiology
**Duration:** 6 months
**Start:** Q1 2026 (results for EXIST application Q3 2026)

**Research Question:** Which fungal strains maximize power density in compression-molded MFCs?

**Tasks:**
- Screen 10-15 fungal strains (*Trametes*, *Phanerochaete*, *Pleurotus*, *Ganoderma*)
- Measure power density (µW/cm²), OCV, longevity
- Test strain combinations (anode yeast + cathode white-rot)
- Optimize inoculation density, nutrient composition

**Target Metrics:**
- Baseline: 12.5 µW/cm² (Empa *T. pubescens*)
- Target: 100-260 µW/cm² (literature maximum: 1.9 W/m² = 190 µW/cm²)

**Deliverables:**
- Strain ranking (power density, growth rate, stability)
- Optimized co-culture protocol
- 1 journal publication (Bioresour. Technol. / Bioelectrochemistry)
- Patent: Strain combination + formulation

**Grant Relevance:** EXIST (technology validation), Horizon Europe (bio-based materials)

---

#### Topic 1.2: Enzyme Engineering for Laccase Optimization
**Degree:** M.Sc. Biochemistry / Molecular Biology
**Duration:** 6 months
**Start:** Q2 2026

**Research Question:** Can laccase activity be enhanced through protein engineering or immobilization?

**Tasks:**
- Express recombinant laccase variants (site-directed mutagenesis)
- Test immobilization on carbon electrodes (covalent vs. adsorption)
- Measure electron transfer kinetics (cyclic voltammetry)
- Optimize pH, temperature, mediator concentration (ABTS vs. direct)

**Target Metrics:**
- 2-5× laccase activity vs. wild-type
- Stable enzyme lifetime >14 days

**Deliverables:**
- Engineered laccase variant (or immobilization protocol)
- Kinetic parameters (Km, Vmax, kcat)
- 1 journal publication (ACS Catalysis / Enzyme Microb. Technol.)

**Grant Relevance:** BMBF (bioeconomy), Horizon Europe (industrial biotechnology)

---

### WP2: Manufacturing Process & Materials

#### Topic 2.1: Compression-Molded Fungal MFC Pellets
**Degree:** M.Sc. Materials Science / Chemical Engineering
**Duration:** 6 months
**Start:** Q1 2026 (critical for Hessen Ideen application)

**Research Question:** What compression molding parameters maximize conductivity and fungal viability?

**Tasks:**
- Formulate cellulose-carbon-graphite composite (vary ratios)
- Optimize compression pressure (10-100 bar), temperature (20-80°C), time (1-60 min)
- Characterize conductivity, porosity, mechanical strength
- Test fungal viability post-compression (CFU counts, metabolic activity)

**Target Metrics:**
- Conductivity: >10 S/m (sufficient for µW-scale MFCs)
- Fungal viability: >80% survival post-compression
- Compressibility: 1.5 mm thickness, IP67 integrity

**Deliverables:**
- Optimized formulation (cellulose : carbon : graphite ratio)
- Process parameters (pressure, temp, time window)
- 1 journal publication (Green Chem. / ACS Sustainable Chem. Eng.)
- Patent: Compression-molded fungal MFC architecture

**Grant Relevance:** Hessen Ideen (core technology), EXIST (manufacturing IP)

---

#### Topic 2.2: Biodegradable Encapsulation for IP67 Protection
**Degree:** M.Sc. Materials Science / Polymer Chemistry
**Duration:** 6 months
**Start:** Q2 2026

**Research Question:** Can we formulate a compostable coating that provides IP67 protection for 7-30 days, then degrades?

**Tasks:**
- Test biodegradable polymers (PLA, PHA, starch blends, beeswax)
- Measure water ingress (gravimetric, impedance)
- Accelerated aging (humidity, temperature cycling)
- Compostability testing (EN 13432 protocol)

**Target Metrics:**
- IP67 integrity: 7 days (Phase 1), 30 days (Phase 2)
- Full biodegradation: 30-90 days in compost
- Cost: <€0.05/unit

**Deliverables:**
- Coating formulation (polymer + plasticizer + filler)
- Degradation kinetics model
- EN 13432 certification (preliminary data)
- 1 journal publication (Polym. Degrad. Stab.)

**Grant Relevance:** DBU (environmental innovation), Horizon Europe (circular economy)

---

### WP3: Electronics & Energy Management

#### Topic 3.1: Ultra-Low-Power MCU Firmware for Energy Harvesting
**Degree:** M.Sc. Electrical Engineering / Embedded Systems
**Duration:** 6 months
**Start:** Q1 2026

**Research Question:** How to maximize sensor lifetime under µW-scale energy budgets?

**Tasks:**
- STM32L0 firmware (sleep modes, interrupt-driven sensing)
- Energy profiling (MCU, sensor, comms)
- Adaptive sampling (adjust interval based on energy availability)
- Boost converter optimization (0.45V → 3.3V efficiency)

**Target Metrics:**
- Average power: <40 µW (7-day runtime @ 15-min intervals)
- Sleep current: <0.5 µA
- Boost efficiency: >85%

**Deliverables:**
- Open-source firmware (GitHub)
- Energy profiling tool (Python + INA219)
- 1 conference paper (SenSys / IPSN)
- Hardware design files (KiCad, open-source)

**Grant Relevance:** EXIST (functional prototype), Hessen Ideen (system integration)

---

#### Topic 3.2: Capacitive Soil Moisture Sensor Calibration
**Degree:** M.Sc. Environmental Engineering / Agri-Tech
**Duration:** 6 months
**Start:** Q2 2026

**Research Question:** Can low-cost capacitive sensors achieve ±1% volumetric water content accuracy across soil types?

**Tasks:**
- Design interdigitated electrode PCB (100 kHz excitation)
- Calibrate vs. soil type (sand, loam, clay, organic matter)
- Temperature compensation (NTC thermistor)
- Field validation (vs. reference: TDR, gravimetric)

**Target Metrics:**
- Accuracy: ±1% VWC (volumetric water content)
- Soil types: sand, loam, clay (3 calibration curves)
- Temperature range: 0-40°C

**Deliverables:**
- Calibration model (capacitance → VWC, soil-specific)
- Open-source calibration software (Python)
- 1 journal publication (Soil Sci. Soc. Am. J. / Sensors)
- Field dataset (100+ measurements)

**Grant Relevance:** EXIST (product validation), DBU (environmental monitoring)

---

### WP4: Environmental Impact & Lifecycle

#### Topic 4.1: Life Cycle Assessment (LCA) of Fungal MFCs
**Degree:** M.Sc. Environmental Engineering / Sustainability Science
**Duration:** 6 months
**Start:** Q1 2026

**Research Question:** What is the carbon footprint of fungal MFCs vs. Li-ion batteries for disposable sensors?

**Tasks:**
- Cradle-to-grave LCA (ISO 14040/44)
- Compare: fungal MFC (cellulose, carbon, fungi) vs. Li-ion CR2032
- Impact categories: GWP, eutrophication, resource depletion, e-waste
- Sensitivity analysis (scale-up scenarios: 1k → 1M units/year)

**Target Metrics:**
- GWP reduction: >50% vs. Li-ion (hypothesis)
- E-waste reduction: 90% (compostable pellet)

**Deliverables:**
- Full LCA report (SimaPro / OpenLCA)
- 1 journal publication (J. Cleaner Production / Int. J. LCA)
- Environmental product declaration (EPD, preliminary)

**Grant Relevance:** DBU (environmental benefit), Horizon Europe (circular economy), BMBF (climate tech)

---

#### Topic 4.2: Biodegradation Kinetics in Soil
**Degree:** M.Sc. Soil Science / Environmental Microbiology
**Duration:** 6 months
**Start:** Q2 2026

**Research Question:** How fast do fungal MFC pellets degrade under field conditions?

**Tasks:**
- Bury pellets in soil (field + lab mesocosms)
- Monitor mass loss, CO2 evolution (respirometry)
- Metagenomic analysis (succession of decomposer microbes)
- Model degradation kinetics (first-order, Arrhenius)

**Target Metrics:**
- 90% mass loss: 30-90 days (compost), 180 days (soil)
- No toxic residues (heavy metals, persistent organics)

**Deliverables:**
- Degradation rate constants (temperature, moisture, soil type)
- Metagenomic dataset (16S rRNA sequencing)
- 1 journal publication (Soil Biol. Biochem. / Environ. Sci. Technol.)
- OK Compost certification (preliminary data)

**Grant Relevance:** DBU (environmental safety), Horizon Europe (bio-based materials)

---

### WP5: Application-Specific Optimization

#### Topic 5.1: Precision Agriculture Sensor Networks
**Degree:** M.Sc. Agronomy / Precision Agriculture
**Duration:** 6 months
**Start:** Q2 2026

**Research Question:** What sensor density and deployment depth optimizes irrigation decisions in row crops?

**Tasks:**
- Deploy 50-100 MykoVolt sensors in field (corn, wheat, vineyard)
- Vary depth (10, 20, 30 cm), density (10, 50, 100 sensors/ha)
- Correlate soil moisture with crop yield, water use efficiency
- Economic analysis (water saved, yield gain vs. sensor cost)

**Target Metrics:**
- Water savings: >20% vs. farmer practice
- Yield gain: >5% (drought stress avoidance)
- ROI: <1 season (€0.15/sensor × 100/ha = €15/ha vs. €200/ha water savings)

**Deliverables:**
- Deployment guidelines (depth, density, crop-specific)
- Economic model (ROI calculator)
- 1 journal publication (Agric. Water Manage. / Precision Ag)
- Pilot customer testimonial (farm partner)

**Grant Relevance:** EXIST (market validation), DBU (resource efficiency)

---

#### Topic 5.2: Compost Process Monitoring
**Degree:** M.Sc. Waste Management / Bioprocess Engineering
**Duration:** 6 months
**Start:** Q2 2026

**Research Question:** Can distributed MykoVolt sensors optimize industrial composting (temperature, moisture, aeration)?

**Tasks:**
- Deploy sensors in compost windrows (municipal, industrial)
- Monitor temperature, moisture, O2 (multi-parameter nodes)
- Correlate with compost quality (C/N ratio, pathogen reduction, maturity)
- Optimize aeration schedule (energy savings)

**Target Metrics:**
- Composting time reduction: >20% (optimized aeration)
- Energy savings: >15% (turning, forced aeration)
- Compost quality: EN 13432 certification maintained

**Deliverables:**
- Process control algorithm (aeration based on sensor data)
- 1 journal publication (Waste Manage. / Bioresour. Technol.)
- Pilot customer (composting facility partner)

**Grant Relevance:** DBU (waste innovation), Horizon Europe (circular economy)

---

## Recruitment Timeline

| Thesis Start | Application Deadline | Results Ready For |
|--------------|----------------------|-------------------|
| **Q1 2026 (Jan-Mar)** | Hessen Ideen (Q2 2026) | EXIST (Q3 2026) |
| **Q2 2026 (Apr-Jun)** | EXIST (Q3 2026) | Horizon Europe (Q4 2026) |
| **Q3 2026 (Jul-Sep)** | Horizon Europe (Q4 2026) | DBU (Q1 2027) |

**Recruitment channels:**
- University job boards (TU Darmstadt, KIT, RWTH, ETH Zürich)
- Professor networks (fungal biology, materials science, embedded systems)
- LinkedIn, ResearchGate, Twitter (#AcademicChatter)
- Career fairs (BioTech, GreenTech, IoT)

**Funding options:**
- University-funded (professor's grant, departmental budget)
- Industry collaboration (MykoVolt provides stipend: €500-1000/month)
- DAAD (international students)
- Women in Tech / Diversity scholarships

---

## IP & Publication Strategy

| Aspect | Policy |
|--------|--------|
| **IP ownership** | MykoVolt retains IP; student is inventor (named in patents) |
| **Publication** | Allowed after patent filing (3-6 month delay) |
| **Thesis embargo** | Optional (1-2 years if sensitive) |
| **Authorship** | Student is first author on papers; MykoVolt team is co-author |
| **Open source** | Firmware, calibration software (GitHub, MIT license) |

**Patent pipeline:**
1. Compression-molded fungal MFC architecture (Q2 2026)
2. Strain combination + formulation (Q3 2026)
3. Biodegradable encapsulation (Q4 2026)
4. Ultra-low-power energy harvesting firmware (Q1 2027)

---

## Success Metrics

| Metric | Target (12 months) |
|--------|---------------------|
| Theses completed | 6-8 |
| Journal publications | 4-6 (peer-reviewed) |
| Patents filed | 2-3 |
| Pilot customers | 3-5 (farms, composting, construction) |
| Grant success rate | >50% (Hessen Ideen, EXIST) |

---

## Next Steps

1. **Identify supervising professors** (fungal biology, materials, electronics)
   - Empa (CH): Dr. Gustav Nyström (cellulose, 3D printing)
   - TU Darmstadt: Prof. Alexander Böker (materials)
   - KIT: Prof. Christoph Syldatk (industrial biotech)

2. **Draft thesis descriptions** (2-page PDF per topic)

3. **Post openings** (university portals, LinkedIn)

4. **Interview candidates** (Q4 2025)

5. **Onboard students** (Q1 2026)

---

*Last updated: 2026-07-20*
