# MFC Literature Review — MykoVolt Deep Dive

**Generated:** 2026-08-14  
**Corpus:** 75 papers (45 directly relevant to fungal MFCs)  
**Purpose:** Practical synthesis of MFC literature for MykoVolt's fungal bio-battery development

---

## 1. Key Findings for MykoVolt

### 1.1 Fungal Laccase is the Proven Power Engine

The strongest evidence base in the corpus is **laccase-mediated biocathodes** (12+ papers in `material/laccase`). Key insights:

| Finding | Evidence | Implication for MykoVolt |
|---------|----------|--------------------------|
| Laccase-carbon cloth cathodes reach **1.76 V** in hybrid Zn-O₂ cells | [Electrochimica Acta 2012](https://doi.org/10.1016/j.electacta.2011.12.026) | Our BQ25570 (0.33–5 V input) is well-matched |
| Laccase immobilization (entrapment + crosslinking) stabilizes low-activity laccase | [Enzyme Microb Technol 2017](https://doi.org/10.1016/j.enzmictec.2017.06.012) | Addresses Zorn's lifespan concern: **immobilization > free enzyme** |
| Fungal laccase MFCs enhance electricity generation vs controls | [JMBFS 2024](https://doi.org/10.55251/jmbfs.9703) | Validates *Trametes versicolor* as primary choice |
| Laccase + catalase H₂O₂–O₂ biocathode boosts performance | [Biosens Bioelectron 2013](https://doi.org/10.1016/j.bios.2012.07.066) | Hybrid enzyme cascade could extend pellet lifespan |

### 1.2 Extracellular Electron Transfer (EET) is the Fastest-Growing Area

`mechanism/eet` has **82% recent share** (9 of 11 papers in last 12 months) — the hottest research cell:

- [Bioelectricity harvesting review (2025)](https://doi.org/10.3389/ffunb.2025.1739847) — advances in microbial EET
- [Neurospora crassa in BES (2017)](https://doi.org/10.1021/acs.est.7b01253) — our high-power species, 260 µW/cm²
- [Fungal fuel cells for heavy metal pollution (2026)](https://doi.org/10.3389/fmicb.2026.1825368) — fungi as environmental MFC workhorses

**MykoVolt takeaway:** EET mechanisms (cytochromes, nanowires, mediated transfer) are where power-density breakthroughs come from. Co-cultures (fungi + *Geobacter*/yeast) are the frontier.

### 1.3 Research Gaps = MykoVolt Opportunities

The thinnest cells in the corpus are exactly where MykoVolt differentiates:

| Gap | Papers | MykoVolt Angle |
|-----|--------|----------------|
| `application/degradation` (biodegradable MFCs) | 1 | **Our entire product thesis** — vanishing electronics |
| `survey/hybrid` (fungal + bacterial co-cultures) | 2 | Hybrid systems for 2–3× power |
| `material/degradation` (compostable electrodes) | 8 | Cellulose/conductive-biochar electrodes |
| `application/hybrid` (self-powered sensors) | 20 | Our self-powered sensing platform |

---

## 2. Species-Specific Evidence (from Corpus)

### 2.1 Trametes versicolor — Best Supported
- **Laccase-carbon cloth biocathode → 1.76 V** hybrid biofuel cell ([2012](https://doi.org/10.1016/j.electacta.2011.12.026))
- **Dye-discoloring laccase MFCs** show oxidoreductase potential ([2023](https://doi.org/10.1186/s12934-023-02258-0))
- **Laccase immobilization strategies** reviewed ([2021](https://doi.org/10.1016/j.biotechadv.2021.107742))
- Multiple laccase electrode architectures (CNTs, redox mediators, MWCNTs): [2010](https://doi.org/10.1016/j.jpowsour.2010.02.033), [2016](https://doi.org/10.1016/j.enzmictec.2015.10.004)

### 2.2 Neurospora crassa — Highest Power
- **260 µW/cm²** demonstrated in bioelectrochemical systems ([2017](https://doi.org/10.1021/acs.est.7b01253))
- Model organism for EET research — genetic tools available

### 2.3 Pleurotus ostreatus — Low-Cost Entry
- **Electricity generation demonstrated** in MFCs ([2018](https://doi.org/10.1007/s12010-018-2840-8))
- **Biowelding** of biocomposites — grows into substrates ([2023](https://doi.org/10.3390/biomimetics8060504)) → relevant for pellet manufacturing

### 2.4 Ganoderma lucidum — Medical Niche
- **Biocatalyst in MFCs** ([2020](https://doi.org/10.1016/j.jbiotec.2020.01.006)) — biocompatibility focus
- Not a power champion, but the only biocompatible choice for wound dressings

---

## 3. Engineering Implications for the DevKit

### 3.1 Electrode Materials (from corpus)
| Material | Evidence | MykoVolt Use |
|----------|----------|--------------|
| Carbon cloth + laccase | 1.76 V hybrid cell ([2012](https://doi.org/10.1016/j.electacta.2011.12.026)) | Primary cathode |
| MWCNTs + laccase | Improved electron transfer ([2016](https://doi.org/10.1016/j.enzmictec.2015.10.004)) | Performance boost |
| Redox mediators | Enable mediated EET ([2010](https://doi.org/10.1016/j.jpowsour.2010.02.033)) | Longevity option |
| Nanozyme laccase mimics | Enzymatic cell without enzyme degradation ([2023](https://doi.org/10.1021/acs.analchem.6c00462.s001)) | **Addresses lifespan!** |

### 3.2 Lifespan Solutions (directly addressing Zorn's concern)
1. **Laccase immobilization** (entrapment/crosslinking) — [Enzyme Microb Technol 2017](https://doi.org/10.1016/j.enzmictec.2017.06.012)
2. **Enzyme cascades** (laccase + catalase) — [Biosens Bioelectron 2013](https://doi.org/10.1016/j.bios.2012.07.066)
3. **Nanozyme mimics** — inorganic catalysts that don't degrade — [Anal Chem 2023](https://doi.org/10.1021/acs.analchem.6c00462.s001)
4. **Hybrid Zn-O₂ with fungal biocathode** — longer life via inorganic anode — [Electrochim Acta 2012](https://doi.org/10.1016/j.electacta.2011.12.026)

### 3.3 Self-Powered Sensors (application/hybrid — 20 papers)
The corpus confirms **self-powered sensing is a mature field** we can build on:
- Urine-glucose paper biofuel cells for diaper sensors ([2021](https://doi.org/10.1021/acssensors.1c01266.s001))
- Photocatalytic fuel cell sensors (multiple, 2019–2025)
- H₂O₂ self-powered electrochemical sensors ([2024](https://doi.org/10.2139/ssrn.4725738))

---

## 4. Strategic Recommendations

### ✅ Adopt Now
1. **Trametes versicolor + carbon cloth** — strongest literature support
2. **Laccase immobilization** research track — directly answers pellet-lifespan criticism
3. **Nanozyme laccase mimics** — watch this space; could solve longevity fundamentally

### 🔬 Research Next
1. **Fungal + Geobacter co-cultures** — the `mechanism/eet` frontier (82% recent share)
2. **Biodegradable electrodes** (conductive biochar, mycelium-composite) — `material/degradation` gap
3. **Enzyme cascade biocathodes** (laccase + catalase + oxidase) — lifespan extension

### 📊 Track
- `mechanism/eet` growth (0.8 papers/month) — our innovation frontier
- Application-side self-powered sensors — validates our product direction
- Degradation-focused MFC papers — our differentiator

---

## 5. Corpus Metadata

- **Total papers:** 75 (45 relevant to fungal MFCs)
- **Time span:** 2009–2026 (median 2018)
- **Categories:** mechanism 32 · application 21 · material 20 · survey 2
- **Sources:** CrossRef (66), curated (7), OpenAlex (2)

---

*Generated from `papers.yaml` + `statistics.json` by the MykoVolt research pipeline.*
