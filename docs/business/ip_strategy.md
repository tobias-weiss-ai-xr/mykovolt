# MykoVolt IP Strategy

## Executive Summary

MykoVolt's intellectual property strategy must balance the tension between:
- **Protecting** core innovations to build competitive moat and investor value
- **Openness** in the DevKit phase to drive academic adoption and community contributions
- **Budget reality** at TRL 2 with a solo founder and no funding yet

**Core principle:** File at least 1 priority patent *before* publishing any experimental results or launching the DevKit. After filing, use defensive publication selectively for non-core innovations.

**Immediate action item:** Freedom-to-Operate (FTO) analysis regarding Empa patent portfolio (Reyes et al., 2024). Their 3D-printed cellulose MFC may have IP that MykoVolt's pellet design builds upon.

---

## 1. Patentable Innovations (Ranked by Strategic Value)

### P1 — HIGH: Dry-Stable Fungal MFC Pellet Composition

| Aspect | Detail |
|---|---|
| **What** | A dry-compressed multi-layer pellet (anode + separator + cathode) containing lyophilized white-rot fungi, CNF/carbon black conductive matrix, and activatable enzyme (laccase). Activates on contact with water + sugar solution. |
| **Novelty** | No existing art (as of 2026) describes a *dry-stable*, *compressed*, *multi-layer fungal MFC pellet* that activates in-field by adding water. Prior fungal MFCs use wet-lab conditions. |
| **Claims** | Composition of matter; method of fabrication (dry pressing); method of activation (field hydration); multi-layer architecture |
| **Cost** | ~€3-5k German priority application (DPMA), ~€15-20k EP within 12 months |
| **Timeline** | File immediately upon first reproducible lab result |

### P2 — HIGH: NFC-Based Readout Protocol for Passive MFC Sensor

| Aspect | Detail |
|---|---|
| **What** | A communication protocol enabling an NFC reader (ST25R3916) to extract time-series sensor data (voltage, current, temperature) from a fungal MFC-powered tag (ST25DV04K) without an active battery on the tag side. Includes energy-aware scheduling: sensor sleeps until NFC field harvested, then takes measurement and transmits. |
| **Novelty** | Existing NFC sensors use external power or harvested energy from the reader. The innovation is the *co-optimization* of the biological power source's time-varying characteristics with the readout protocol's energy demands. |
| **Claims** | Method of operating a battery-less NFC tag with biological energy source; adaptive measurement scheduling based on MFC power state |
| **Cost** | ~€3-5k DPMA |
| **Timeline** | Q1 2028 (before DevKit launch) |

### P3 — MEDIUM: ML-Optimized Enzyme Formulation

| Aspect | Detail |
|---|---|
| **What** | A machine learning method (Bayesian optimization or similar) that predicts optimal laccase/mediator ratios for given fungal strain + substrate combinations, trained on a multi-dimensional dataset of MFC performance metrics. |
| **Novelty** | Applying ML to MFC enzyme formulation optimization specifically for fungal strains is novel. The *closed-loop* optimization (formulate → test → measure → feed back) for fungal MFCs is a distinct method. |
| **Claims** | Method of optimizing enzyme formulation via ML with feedback loop |
| **Cost** | ~€3-5k DPMA |
| **Timeline** | File when experimental dataset reaches n ≥ 50 data points |

### P4 — MEDIUM: Compostable Sensor Housing for Soil Deployment

| Aspect | Detail |
|---|---|
| **What** | A biodegradable multi-chamber housing design that separates fungal MFC (hydrated chamber) from electronics (dry chamber with NFC antenna) while allowing moisture exchange with surrounding soil. |
| **Novelty** | Biodegradable housings exist for medical devices, not for soil-deployed fungal battery systems with integrated electronics. |
| **Claims** | Multi-chamber biodegradable housing; moisture-exchange membrane |
| **Cost** | ~€3-5k DPMA |
| **Timeline** | Q3 2028 or defensive publication |

### P5 — LOW: LoRa-Based Long-Range Telemetry (Defensive Publication Candidate)

| Aspect | Detail |
|---|---|
| **What** | The integration of an ultra-low-power LoRa radio (SX1262) with a fungal MFC power source, including energy-aware transmission scheduling (adaptive duty-cycling based on real-time MFC power output). |
| **Novelty** | Low—LoRa + energy harvesting is well-explored. The specific MFC co-optimization may be novel but is hard to enforce. |
| **Recommendation** | **Defensive publication only.** Publish on arXiv or as a design note. Don't spend patent budget here. |

---

## 2. Freedom to Operate (FTO) Analysis

**Search date:** July 2026. Searched FreePatentsOnline, Google Patents, WIPO PATENTSCOPE, Espacenet, Semantic Scholar.

### 2.1 Empa Patent Portfolio

The foundational technology (3D-printed cellulose-based fungal MFC by Reyes et al., 2024) was published in *ACS Sustainable Chemistry & Engineering* as open-access research.

- **Search result:** No patents found by Empa or Reyes related to microbial fuel cells, fungal batteries, or bio-batteries across all queried databases.
- **Assessment:** The 2024 paper was published as open science without apparent patent protection. Any Swiss national patent would have expired its 18-month non-publication window by mid-2026.
- **Remaining gap:** Swiss IPI and EPO Espacenet were not fully searchable (JS-rendered). A professional European search (~€500-1k) is recommended to confirm.
- **Risk:** **LOW** — no blocking patents found; dry-pressed pellet is methodologically distinct from 3D-printing.

### 2.2 MycelioTronics (JKU / Science Advances 2022)

- **What:** Fungal mycelium-based electronic substrates (not batteries)
- **Risk:** **Low** — different form factor, different application, different mechanism
- **Note:** MycelioTronics is enabling technology (mycelium as substrate), not competing IP

### 2.3 Bactery AB

- **What:** Soil microbial fuel cells (bacteria-based, not fungi) with proprietary ceramic membrane
- **Search result:** No patents found in US databases. Swedish/European patents may exist outside US coverage, or they may rely on trade secrets.
- **Risk:** **Low-Medium** — overlapping addressable market (soil-powered sensors) could lead to design-around claims
- **Action:** Monitor Bactery's patent filings; investigate via Swedish patent office (PRV)

### 2.4 Relevant Patents Found

| Patent | Title | Assignee | Year | Risk | Notes |
|--------|-------|----------|------|------|-------|
| US7160637 | Implantable miniaturized MFC | UC Berkeley | 2007 | **Low** | Yeast anode, but for implantable medical devices (MEMS), not IoT. Patent ~18yr old, likely expired. |
| US9257709 | Paper-based fuel cell | Univ. New Mexico | 2016 | **Low** | Enzymes (laccase, bilirubin oxidase), not living fungi. Paper lamination, not compression molding. "Microorganisms" in claims only specify bacteria (Shewanella, Geobacter). |
| US20250210680 | Terrestrial microbial fuel cell | — | 2025 | **Monitor** | Published application, claims not yet examined. Terrestrial deployment similar to Bactery's space. Monitor prosecution for fungal/biodegradable MFC claims. |
| US8552861 | Biodegradable smart sensor | — | 2013 | **Irrelevant** | Conventional battery chemistry, not biological. |

### 2.5 Key Finding: Fungal MFC Claim Space Is Unpatented

No patent anywhere claims a fungal cathode, fungal anode, or a fuel cell combining yeast and fungi. The fungal MFC claim space is a green field — MykoVolt should file first.

### FTO Checklist

| Item | Status | Result |
|---|---|---|
| Empa MFC method patents | ✅ Searched | **None found** (US, WIPO, Espacenet) |
| Generic MFC ink/pellet patents | ✅ Searched | **None fungal** (2 low-risk enzyme/paper patents) |
| Biodegradable sensor housing patents | ✅ Searched | **Irrelevant** (conventional chemistry only) |
| NFC energy harvesting + biological power source | ⬜ Search needed | — |
| Swiss IPI / EPO Espacenet (professional search) | ⬜ Recommended | ~€500-1k, before first patent filing |

---

## 3. Filing Strategy & Budget

| Year | Filing | Cost (cumulative) | Funding source |
|---|---|---|---|
| 2026-2027 | FTO analysis + provisional application P1 | ~€500-1k | Bootstrapped (essential) |
| 2027-2028 | Priority application P1 (DPMA) + P2 (DPMA) | ~€8-10k | EXIST grant |
| 2028-2029 | EP extension P1 + P3 filing + PCT | ~€20-25k | DevKit revenue + EXIST |
| 2029-2030 | National phase entries (US, JP, BR) + P4 | ~€30-50k | Angel/Seed round |
| 2030+ | Portfolio maintenance + enforcement | ~€5-10k/year | Series A |

**Total patent cost (5-year horizon):** ~€60-85k — realistic for a deep-tech startup.

---

## 4. Trade Secrets vs. Patents

| Innovation | Protect as | Rationale |
|---|---|---|
| Yeast strain optimization protocol | **Trade secret** | Hard to reverse-engineer; no disclosure required; lasts indefinitely |
| Carbon black ink processing parameters | **Trade secret** | Process know-how; not derivable from end product |
| Supplier relationships for specialty materials | **Trade secret** | Supply chain moat |
| Pellet composition ratios | **Patent** | Will be discoverable from product anyway; patent gives exclusion rights |
| NFC protocol details | **Patent** | Easily reverse-engineered from DevKit firmware |
| ML training data and model weights | **Trade secret** | Core AI asset |

---

## 5. Open-Source Strategy (The "DevKit Paradox")

MykoVolt faces a structural tension:

| Open (DevKit) | Closed (Commercial) |
|---|---|
| DevKit firmware must be open-source for academic adoption | P2 (NFC protocol) must have priority claim |
| Board design files should be OSHW-compliant | Key optimizations (pellet integration, power management) stay proprietary |
| Data formats and API open for community tools | ML models and enzyme formulation remain secret |

**Resolution:** Implement a "core + open wrapper" model:
1. **Open:** DevKit firmware base, data sheet format, example code, hardware design files
2. **Proprietary:** Pellet composition, NFC readout protocol optimizations, ML model, production methods

---

## 6. Brand Protection

| Asset | Protect when | Cost |
|---|---|---|
| **MykoVolt** wordmark (DE) | Q1 2027 (before DevKit launch) | ~€300 |
| **MykoVolt** wordmark (EU) | Q4 2027 | ~€900 |
| **MykoVolt** domain (mykovolt.com) | ✅ Already secured | — |
| Logo / design mark | When visual identity finalized | ~€500 |
| **Trade name** registration (Gewerbe/HR) | On incorporation | Free |

---

## 7. University Collaboration IP Terms

When working with EMC JLU or other academic labs (critical for EXIST):

| Clause | MykoVolt's position | Standard academic position |
|---|---|---|
| Ownership of foreground IP | MykoVolt (startup) | Joint or university-owned |
| Right to license | Exclusive, worldwide | Non-exclusive, research only |
| Publication delay | Max 90 days for patent filing | Usually 30 days |
| Background IP | MykoVolt retains all pre-existing IP | University retains theirs |
| Revenue sharing | Single-digit % on licensed foreground | Usually 15-30% net |

**Recommendation:** Use EXIST "Gründungsstipendium" terms as template. Most German universities have standardized spin-off agreements. Do NOT accept university ownership of foreground IP — this is a dealbreaker for investors.

---

## 8. Critical Path & Immediate Actions

| Priority | Action | Deadline | Cost |
|---|---|---|---|
| 1 | ~~FTO search for Empa patents~~ | ~~Before first lab experiment~~ | ~~€500-1k~~ |
| 1 | **Professional EPO/Swiss IPI patent search** (close gap on EU/Swiss databases) | Before first patent filing | ~€500-1k |
| 2 | Provisional DPMA for P1 (pellet) | Same month as first reproducible result | ~€3-5k |
| 3 | Trademark "MykoVolt" DE | Before any public DevKit announcement | ~€300 |
| 4 | University IP agreement template | Before signing any collaboration agreement | Legal review ~€1k |
| 5 | NDA template for suppliers/partners | Before sharing formulation specs | Free (templates exist) |
| 6 | Monitor US20250210680 prosecution | Ongoing, quarterly | Free |

**Budget needed for remaining IP steps:** ~€5-8k (can be funded from EXIST Sachmittel).
