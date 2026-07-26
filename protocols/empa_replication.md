# Empa Fungal Battery — Replication Protocol v1.0

> **Target:** Reproduce Reyes et al. 2024 (ACS Sustainable Chem. Eng.)  
> **Goal:** Validate 12.5 µW/cm² baseline; establish wet-lab capability  
> **Status:** ⬜ Not started — requires lab access + co-founder  
> **Estimated timeline:** 8–12 weeks from lab access  
> **Reference:** [10.1021/acssuschemeng.4c05494](https://doi.org/10.1021/acssuschemeng.4c05494)

---

## 1. Objective

Replicate the 3D-printed fungal bio-battery with the following success criteria:

| Metric | Empa (Reyes 2024) | Our Target | Pass/Fail |
|--------|-------------------|------------|-----------|
| Power density | 12.5 µW/cm² | ≥10 µW/cm² | |
| Open-circuit voltage | 300–600 mV | ≥250 mV | |
| Active lifetime | 65 h (4 cells) | ≥48 h | |
| Voltage stability | <20% drop over 24h | <25% drop | |
| Biodegradability | 93% mass loss, 11 d | ≥80%, 14 d | |

---

## 2. Materials

### 2.1 Biological Materials

| Item | Specification | Supplier | Status |
|------|--------------|----------|--------|
| *Trametes versicolor* | DSMZ 11372 or equivalent | DSMZ (Braunschweig) | ⬜ To order |
| *Pleurotus ostreatus* | DSMZ 11176 or equivalent | DSMZ (Braunschweig) | ⬜ To order |
| *Saccharomyces cerevisiae* | Baker's yeast, commercial | Local supplier | ✅ Available |
| Malt extract agar (MEA) | Standard formulation | Carl Roth | ⬜ To order |
| Potato dextrose agar (PDA) | Standard formulation | Carl Roth | ⬜ To order |

### 2.2 Ink Formulation (per Reyes 2024)

| Component | Ratio (wt%) | Amount per 10 mL | Function |
|-----------|-------------|-------------------|----------|
| Cellulose nanocrystals (CNC) | 3–5% | 0.3–0.5 g | Structural matrix |
| Cellulose nanofibrils (CNF) | 1–2% | 0.1–0.2 g | Rheology modifier |
| Carbon black | 2–3% | 0.2–0.3 g | Electron conduction |
| Graphite flakes | 5–8% | 0.5–0.8 g | Current collection |
| Deionized water | Balance | ~9 mL | Solvent |
| Glycerol | 1–2% | 0.1–0.2 mL | Printability |

**Total solids:** 12–20 wt%  
**Viscosity target:** 10³–10⁴ Pa·s (at shear rate 1 s⁻¹)

### 2.3 Consumables

| Item | Qty | Purpose |
|------|-----|---------|
| Glass slides (25×75 mm) | 20 | Substrate for printed electrodes |
| Copper tape (conductive) | 5 m | Current collector connections |
| Beeswax | 100 g | Encapsulation (Empa method) |
| Cellulose dialysis membrane | 1 m² | Separator |
| Alligator clips + wires | 20 | Measurement connections |
| Silicone tubing (3 mm ID) | 2 m | Air chimney prototypes |
| Petri dishes (90 mm) | 50 | Fungal culture |
| Erlenmeyer flasks (250 mL) | 10 | Liquid culture |

---

## 3. Equipment

| Equipment | Purpose | Alternative | Status |
|-----------|---------|-------------|--------|
| 3D printer (extrusion-based) | Print electrodes | Manual casting | ⬜ Need access |
| Potentiostat (e.g., Gamry, BioLogic) | Electrochemical characterization | Arduino + shunt | ⬜ Need access |
| Multimeter (6.5 digit) | Voltage/current logging | 3.5 digit (basic) | ⬜ Need |
| Data logger (24+ channel) | Long-term monitoring | Raspberry Pi + ADC | ✅ Can build |
| Laminar flow hood | Fungal inoculation | Still-air box | ⬜ Need access |
| Incubator (25°C, 85% RH) | Fungal growth | Temperature-controlled room | ⬜ Need access |
| Autoclave | Sterilization | Pressure cooker | ⬜ Need access |
| Analytical balance (0.1 mg) | Ink formulation | 1 mg balance | ⬜ Need |
| Conductive probe station | MFC characterization | Custom fixture | ⬜ Build |
| Microscope (100×–400×) | Hyphal growth check | USB microscope | ✅ Have |

---

## 4. Protocol Steps

### Phase 1: Fungal Culture (Week 1–2)

```
Day 1:   Prepare MEA plates (10 plates)
         Streak T. versicolor from stock
         Incubate at 25°C, 85% RH, 7 days

Day 7:   Fungal growth visible (white mycelium)
         Prepare liquid culture: 2% malt extract broth
         Inoculate 5 × 50 mL liquid cultures
         Static incubation, 25°C, 14 days

Day 14:  Mycelial biomass ready for ink formulation
```

### Phase 2: Ink Preparation (Week 3)

```
Day 15:  Disperse CNC (0.5 g) in DI water (5 mL)
         Probe sonicate: 30 min, 40% amplitude
         Add CNF (0.15 g), stir 1 h at 500 rpm
         Add carbon black (0.25 g), stir 30 min
         Add graphite flakes (0.6 g), stir 30 min
         Add glycerol (0.15 mL) for rheology
         Final solids: ~15 wt%
         Degas: vacuum desiccator, 15 min
         Viscosity check: should be toothpaste-like
```

### Phase 3: Electrode Printing (Week 3–4)

```
Day 17:  Load ink into 3D printer syringe
         Print pattern: 10×10 mm square, 0.5 mm height
         Printing parameters:
           - Nozzle: 0.4 mm
           - Layer height: 0.2 mm
           - Speed: 10 mm/s
           - Bed temp: ambient
         Print 10 anode electrodes
         Print 10 cathode electrodes
         Air-dry 24 h at ambient conditions
```

### Phase 4: MFC Assembly (Week 4)

```
Day 18:  Hydrate cellulose membrane in DI water (30 min)
         Assemble MFC stack:
           1. Glass slide substrate
           2. Anode (printed) + copper tape contact
           3. Cellulose membrane (separator)
           4. Cathode (printed) + copper tape contact
           5. Liquid culture inoculum (2 mL)
           6. Beeswax seal around edges
         Wire connections: anode → red, cathode → black
```

### Phase 5: Electrical Characterization (Week 4–6)

```
Day 19:  Open-circuit voltage measurement (every 10 min)
         Data: V(t) for 72 h
         Criteria: OCV ≥ 250 mV within 24 h

Day 21:  Polarization curve (if OCV stabilized)
         Apply external loads: 10 kΩ, 22 kΩ, 47 kΩ, 100 kΩ, 220 kΩ
         Measure stabilized voltage after 5 min per load
         Calculate power: P = V²/R

Day 25:  Long-term constant load test
         Apply 47 kΩ load (matches simulation)
         Log V(t), I(t) every 10 min for 72 h
         Key metric: power density vs time

Day 28:  Temperature sensitivity (if time permits)
         Repeat at 15°C, 25°C, 35°C
```

### Phase 6: Data Analysis (Week 6)

```
Day 35:  Compile all measurements
         Compare with simulation predictions
         Calculate:
           - Peak power density (µW/cm²)
           - Voltage stability (% drop/24h)
           - Internal resistance (from polarization curve)
           - Coulombic efficiency
         Publish results / update simulation parameters
```

---

## 5. Success Criteria

| Tier | Condition | Next Step |
|------|-----------|-----------|
| ✅ **Full replication** | ≥10 µW/cm², ≥48 h | Paper #2 (experimental) |
| ✅ **Partial replication** | ≥5 µW/cm², ≥24 h | Optimize ink formulation |
| ⚠️ **Failed** | <5 µW/cm² | Root cause analysis |

---

## 6. Safety

| Hazard | Precaution |
|--------|-----------|
| Fungal spores (allergen) | Work in laminar flow hood, N95 mask |
| Carbon nanoparticles (inhalation) | Wet handling only, fume hood if dry |
| Electrical (short circuits) | Fuse-protected measurement setup |
| Beeswax (hot) | Use caution when melting (60°C water bath) |

---

## 7. Estimated Budget

| Category | Item | Cost (€) |
|----------|------|----------|
| Biologicals | Fungal strains, agar, media | 120 |
| Inks | CNC, CNF, carbon, graphite | 180 |
| Consumables | Slides, tape, wax, wires | 80 |
| Disposables | Petri dishes, gloves, filters | 60 |
| **Total materials** | | **440** |
| Equipment access | Lab rental (8 weeks) | — (depends) |
| **Grand total** | | **€440 + lab access** |

---

## 8. Timeline

```
Week 1-2  ████████░░░░░░░░░░░░  Fungal culture
Week 3    ░░░░░░░░████░░░░░░░░  Ink prep + printing
Week 4    ░░░░░░░░░░░░██████░░  Assembly + initial testing
Week 5-6  ░░░░░░░░░░░░░░░░████  Full characterization
Week 7-8  ░░░░░░░░░░░░░░░░░░░░  Data analysis + reporting
```

---

*Status: ⬜ Awaiting lab access and scientific co-founder.*  
*Last updated: July 2026*
