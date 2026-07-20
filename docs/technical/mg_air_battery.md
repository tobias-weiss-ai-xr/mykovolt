# Mg-Air Biodegradable Battery

> **Status:** Concept (TRL 2–3)
> **Cross-reference:** [alternatives.py](../simulation/alternatives.py) — comparative viability analysis
> **Literature:** Tsang et al. 2022 — transient Mg-air batteries; Yin et al. 2021 — biodegradable power sources

A Mg-air primary cell as the drop-in replacement for the fungal pressling in Phase 2 (field pilot). Higher TRL than the fungal MFC, O2-independent at depth via parasitic water reduction, and fully biodegradable (Mg(OH)2 is soil-compatible).

---

## 1. Chemistry

### 1.1 Half-Reactions

| Electrode | Reaction | E0 | Notes |
|-----------|----------|----|-------|
| Anode (Mg) | Mg → Mg²⁺ + 2e⁻ | −2.37 V | Corrosion potential |
| Cathode (O2) | O₂ + 2H₂O + 4e⁻ → 4OH⁻ | +0.40 V | Air cathode (preferred) |
| Parasitic (H₂O) | 2H₂O + 2e⁻ → H₂ + 2OH⁻ | −0.83 V | Kicks in when O₂ is scarce |
| **Overall (air)** | 2Mg + O₂ + 2H₂O → 2Mg(OH)₂ | **~1.6 V** | Practical |
| **Overall (water only)** | Mg + 2H₂O → Mg(OH)₂ + H₂ | **~0.8 V** | Deep burial mode |

### 1.2 Key Properties

| Property | Value | Source |
|----------|-------|--------|
| Theoretical energy density | 2.8 kWh/kg Mg | Standard electrochemistry |
| Practical energy density | 0.5–1.0 kWh/kg | Transient battery literature |
| Mg cost | ~€2.30/kg | LME, bulk |
| Degradation product | Mg(OH)₂ (brucite) | Soil pH buffer, non-toxic |
| Corrosion rate (in soil) | 0.3–3 mm/year | Tunable via alloying |
| H₂ evolution rate | ~0.5 mL/h per mA | Parasitic reaction |

### 1.3 Biodegradability

Mg(OH)₂ solubility in water: 6.4 mg/L at 25°C. In soil:
- Acts as a mild pH buffer (raises pH locally)
- Mg²⁺ is a plant macronutrient (0.5% of dry plant mass)
- 0.5 g Mg → 1.2 g Mg(OH)₂ → negligible in 1 m³ soil (raises Mg by ~0.3 ppm)
- EN 13432 compostability: passes (no organic toxins, fully mineralizes)

---

## 2. Cell Design

### 2.1 Architecture

```
Surface
  │  ┌───────────────────────────┐
  │  │  Air cathode (optional)    │  ← carbon paper + PTFE binder
  │  │  Ø 20 mm, 2 cm²           │     removed for deep burial
  │  └───────────┬───────────────┘
  │              │
Depth       ┌────┴────┐
  │         │ Reservoir │            ← cellulose sponge or hydrogel
  │         │ (electrolyte)│           soaked in 0.1 M NaCl or soil water
  │         ├─────────┤
  │         │ Separator│            ← cellulose paper
  │         ├─────────┤
  │         │ Mg anode │            ← foil, 0.5 mm × 20 mm × 30 mm
  │         │ (0.5 g)  │               embedded in CNF binder
  │         └─────────┘
  │
Soil ────────────────────────────

Optional: Air cathode on surface (for shallow deployment).
At depth (>5 cm): no cathode — water reduction at Mg surface is sufficient.
```

### 2.2 Operating Modes

| Mode | Condition | Voltage | Power | Lifetime (0.5 g Mg) |
|------|-----------|---------|-------|---------------------|
| Surface air | Cathode exposed to air | 1.4–1.6 V | ~500 µW | ~20 days |
| Shallow (2–5 cm) | Partial O₂ at cathode | 1.2–1.5 V | ~200 µW | ~40 days |
| Deep (>5 cm) | Water reduction only | 0.6–0.9 V | ~80 µW | ~130 days |
| Very deep (>20 cm) | Pure water reduction | 0.5–0.7 V | ~50 µW | ~200 days |

All modes exceed the 7-day MVP target with margin.

### 2.3 Cell Sizing for MVP

| Target | Mg mass | Cell volume | Lifetime at 10 cm | Cost |
|--------|---------|-------------|-------------------|------|
| 7-day minimum | 0.1 g | 2 × 2 × 0.5 cm | ~15 days | €0.005 |
| 30-day pilot | 0.5 g | 3 × 3 × 0.5 cm | ~130 days | €0.025 |
| 90-day field | 2.0 g | 5 × 4 × 0.5 cm | ~365 days | €0.08 |

Standard MVP cell: **0.5 g Mg** — fits existing casing envelope, 130+ day lifetime.

---

## 3. BOM

| Item | Spec | Cost | Supplier |
|------|------|------|----------|
| Mg foil (99.9%) | 0.5 mm × 30 mm × 30 mm | €0.015 | Alfa Aesar / local |
| Carbon paper cathode | Sigracet 35BC, 2 cm² | €0.05 | SGL Carbon |
| Cellulose separator | Filter paper, Ø 40 mm | €0.002 | Whatman |
| CNF binder/hydrogel | 2 g CNF + 10 mL water | €0.02 | Cellulose lab |
| NaCl electrolyte | 0.1 M, 1 mL | €0.001 | Sigma |
| Casing (PLA/straw) | Injection molded | €0.10 | Local molder |
| **Total** | | **€0.188** | vs €0.50 fungal pressling |

At scale (50k+): target **€0.08/unit** driven by Mg cost (€0.003) and casing (€0.05).

---

## 4. Manufacturing

```
Step 1: Cut Mg foil to size          → 30 × 30 mm
Step 2: Etch surface (10% HCl, 10 s) → remove oxide layer, activate
Step 3: Cast CNF hydrogel + NaCl     → mold 3 × 3 × 0.5 cm
Step 4: Embed Mg foil in hydrogel    → leave 5 mm tab for contact
Step 5: Place separator on top
Step 6: Attach cathode (if used)     → carbon paper + current collector
Step 7: Seal in casing               → PLA shell with vent holes (for air mode)
Step 8: Vacuum package               → same equipment as pressling
```

**Process time:** ~2 min/unit (simpler than pressling)

**Required new equipment:** None (uses same hand press + vacuum sealer as pressling)

---

## 5. Integration with Electronics Board

The Mg-air battery replaces the pressling at the connector level:

| Pin | Pressling | Mg-air | Compatible? |
|-----|-----------|--------|------------|
| V+ | 0.3–0.6 V (needs boost) | 0.6–1.6 V | ✅ Same BQ25570 boost |
| GND | Common | Common | ✅ |
| Signal | Optional temp sensor | None | ⚠️ No temp readout from battery |

The BQ25570 boost converter starts at 0.3 V and handles up to 3.5 V — directly compatible with Mg-air voltage range.

**Modification needed:** None for the electronics board. The Mg-air connects to the same power input header.

---

## 6. H₂ Management

The water reduction reaction produces H₂ gas:

Mg + 2H₂O → Mg(OH)₂ + H₂↑

At 80 µW deep-burial mode:
- Current: ~100 µA (at 0.8 V)
- H₂ production: ~1.9 µL/h = ~0.045 mL/day
- In a 3 cm³ casing: ~1.5% volume per day

| Approach | Method | Effectiveness |
|----------|--------|--------------|
| Vent | Tiny hole in casing | 100% (H₂ escapes into soil) |
| Catalytic recombination | Pt mesh inside casing | Converts to H₂O, adds €0.02 |
| Absorption | Palladium sponge | Too expensive (>€1) |

**Recommendation:** Small vent hole (0.1 mm) in the PLA casing. H₂ is non-toxic and escapes harmlessly into soil. At 0.045 mL/day, the bubble volume is negligible.

---

## 7. Comparison: Mg-air vs Fungal Pressling

| Criterion | Fungal Pressling | Mg-Air | Winner |
|-----------|-----------------|--------|--------|
| TRL | 2 (concept only) | 2–3 (lab prototypes exist) | **Mg-Air** |
| Power at 10 cm depth | 0.3–6.5 µW | 80 µW (water reduction) | **Mg-Air** |
| Biodegradable | 90% | 95% (Mg fully mineralizes) | **Mg-Air** |
| Depth limit | 2 cm (without chimney) | None (water reduction works) | **Mg-Air** |
| Story | "Fungal battery" novel | Less novel, but still green | **Fungal** |
| Manufacturing complexity | Pressling + biology | Foil + casting, simpler | **Mg-Air** |
| Cost (small volume) | €0.50 | €0.19 | **Mg-Air** |
| Cost (50k volume) | €0.15 | €0.08 | **Mg-Air** |
| H₂ safety issue | None | Minor (vented) | **Fungal** |
| Alloy risk | Mature compostable materials | Mg corrosion rate difficult to control | **Fungal** |

**Overall:** Mg-air wins on every quantitative metric except the "fungal story."

---

## 8. Validation Plan

| Step | What | How | Success criterion |
|------|------|-----|-------------------|
| 1 | Mg corrosion rate in soil | Bury Mg foil in loam at 25% moisture, measure mass loss/week | 0.3–3 mm/year (tunable) |
| 2 | Open-circuit voltage | Mg vs carbon paper in soil | >1.2 V at surface, >0.6 V at 10 cm |
| 3 | Power output | Connect to BQ25570 + dummy load at various depths | >50 µW sustained at 10 cm |
| 4 | 7-day soil test | Full cell + electronics in soil box, 15-min measurements | >80% data integrity |
| 5 | H₂ accumulation | Sealed cell with pressure sensor | Pressure < 1.1 atm over 7 days |
| 6 | Soil pH impact | Measure pH at 1/5/10 cm from cell after 30 days | pH change < 0.5 within 5 cm |

---

## 9. Open Research Questions

1. **Corrosion rate control** — Pure Mg corrodes too fast in acidic soil (pH < 6). AZ31 or WE43 alloys reduce rate but add cost and toxicity (Al, Zr, Y). Best approach: electrolyte formulation (0.1 M NaCl + pH buffer).
2. **Anode utilization** — Mg corrosion is non-uniform. At 50% utilization, effective capacity drops. Engineering the anode shape (thin foil vs. mesh) can improve this.
3. **Salt bridge to electronics** — Mg²⁺ ions migrating to the PCB could cause short circuits. A cellulose plug acts as a diffusion barrier.
4. **Freeze tolerance** — Electrolyte freezing stops the cell. Saline electrolyte (NaCl) lowers freezing point to −3°C. For colder climates, CaCl₂ (−20°C) or bury below frost line.

---

## 10. Go/No-Go Decision

Proceed with Mg-air battery if:
- Step 1 shows Mg corrosion rate is controllable (0.3–3 mm/year range)
- Step 3 shows >50 µW at 10 cm depth
- Step 5 shows safe H₂ management

Proceed with air-chimney pressling if:
- Fungal MFC in pressling form achieves >12 µW/cm² (Empa baseline)
- Chimney maintains O₂ at depth (Step 1 of chimney validation)

**Dual-path approach:** Pursue both in Phase 0. Gate decision at 12-month mark based on which yields a functional prototype first.
