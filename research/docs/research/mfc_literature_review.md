# MFC Literature Review — MykoVolt Deep Dive

**Generated:** 2026-08-15 (rev. 2 — post evidence audit)  
**Corpus:** 96 papers (36 directly relevant to fungal MFCs; 100% DOI-verified)  
**Purpose:** Practical synthesis of MFC literature for MykoVolt's fungal bio-battery development  
> ⚠️ Rev. 2 removes 23 unverifiable entries found in the 2026-08 DOI audit (incl. the "Neurospora 260 µW/cm²" claim). See [gap_analysis.md](gap_analysis.md).

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
- [Trametes hirsuta laccase DET at electrodes (2013)](https://doi.org/10.1016/j.bioelechem.2012.11.001) — verified foundation for fungal EET
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

## 2. Species-Specific Evidence (verified corpus only)

### 2.1 Trametes — Best Supported
- **Laccase-carbon cloth biocathode → 1.76 V** hybrid biofuel cell ([2012](https://doi.org/10.1016/j.electacta.2011.12.026))
- **Direct electron transfer of T. hirsuta laccase at electrodes** ([Bioelectrochemistry 2013](https://doi.org/10.1016/j.bioelechem.2012.11.001); [Electroanalysis 2006](https://doi.org/10.1002/elan.200603600)) — the Shleev-line foundational work
- **Laccase MFCs enhance electricity generation** ([JMBFS 2024](https://doi.org/10.55251/jmbfs.9703))
- Multiple verified electrode architectures: [2010](https://doi.org/10.1016/j.jpowsour.2010.02.033), [2016](https://doi.org/10.1016/j.enzmictec.2015.10.004)
- ⚠️ Specific µW/cm² numbers for whole-cell *T. versicolor* MFCs remain to be measured by us (Phase E1)

### 2.2 Saccharomyces cerevisiae — Verified Model System (NEW)
- **Polypyrrole-modified yeast in MFCs** ([Biosensors 2025](https://doi.org/10.3390/bios15080519)) — real, current MFC demonstrations
- **Electrode size ↔ power generation** ([Ionics 2021](https://doi.org/10.1007/s11581-021-04162-2)) — directly transferable to our 2-cm² interdigital electrodes
- **Stable current + phytate degradation** yeast BFCs ([Yeast 2018](https://doi.org/10.1002/yea.3027))

### 2.3 Aspergillus niger — Qualitatively Verified
- **Bioelectricity generation + dye decolorization** ([JBR 2016](https://doi.org/10.4172/2155-6199.1000446)) — real demonstration, µW numbers still lacking

### 2.4 Pleurotus ostreatus — Substrate Integration (partial)
- **Biowelding of biocomposites** ([2023](https://doi.org/10.3390/biomimetics8060504)) → relevant for pellet manufacturing
- ⚠️ Direct electricity-generation evidence was retracted (unverifiable source)

### 2.5 Neurospora crassa — ❌ RETRACTED
- The claimed 260 µW/cm² rested on a hallucinated source. **No verifiable Neurospora electrochemistry literature exists** — this is genuine research whitespace, not established fact. Keep only as experimental candidate with explicit "first-mover" framing.

### 2.6 Ganoderma lucidum — ❌ RETRACTED (power claims)
- No verified MFC evidence; keep only as biocompatible-material candidate.

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
1. **Laccase immobilization** (covalent binding on electrodes) — [MSE:C 2004](https://doi.org/10.1016/j.msec.2003.09.036); enhanced stability/reusability — [Sci Rep 2026](https://doi.org/10.1038/s41598-026-40065-w)
2. **One-year-stable glucose/O₂ biofuel cell** — [Bioelectrochemistry 2015](https://doi.org/10.1016/j.bioelechem.2015.04.009) — the strongest single lifespan datapoint in the corpus
3. **Enzyme cascades** (laccase + catalase) — [Biosens Bioelectron 2013](https://doi.org/10.1016/j.bios.2012.07.066)
4. **Nanozyme mimics** — inorganic catalysts that don't degrade — [Anal Chem 2023](https://doi.org/10.1021/acs.analchem.6c00462.s001)
5. **Hybrid Zn-O₂ with fungal biocathode** — longer life via inorganic anode — [Electrochim Acta 2012](https://doi.org/10.1016/j.electacta.2011.12.026)
6. **Power management**: net-power-positive MPPT harvesting — [J Power Sources 2019](https://doi.org/10.1016/j.jpowsour.2019.02.042); comprehensive PMS evaluation — [Bioelectrochemistry 2024](https://doi.org/10.1016/j.bioelechem.2023.108597) — BQ25570-class architectures are literature-proven

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

- **Total papers:** 96 (100% DOI-verified; 36 fungal-relevant)
- **Time span:** 2004–2026
- **Categories:** mechanism 40 · material 30 · application 25 · survey 1
- **Sources:** CrossRef-fetched (29), inherited verified corpus (67)
- **Audit:** 23 entries retracted 2026-08 ([gap_analysis.md](gap_analysis.md))

---

*Generated from `papers.yaml` + `statistics.json` by the MykoVolt research pipeline.*
