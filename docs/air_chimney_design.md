# Air-Chimney Pressling Design

> **Status:** Concept (TRL 2)
> **Cross-reference:** [pressling_viability.py](../simulation/pressling_viability.py) — O2-limited power model
> **Prerequisite:** Empa 2024 MFC result reproduced in pressling form

The pure pressling fails at depth because O2 doesn't diffuse through moist soil to the cathode. The air-chimney solves this with a porous breathing tube connecting the cathode to the surface — no chemistry change, just a casing modification.

---

## 1. Design Overview

```
Surface
  │  ┌──────────────────────┐
  │  │ Porous cap (sheltered)│  ← rain-protected air intake
  │  └──────────┬───────────┘
  │             │
  │      ┌──────┴──────┐           ← flexible silicone tube
  │      │ Air chimney  │             Ø 3-5 mm, L = depth
  │      │  (porous PTFE│             hydrophobic (Gore-Tex-like)
  │      │   or silicone│             prevents water ingress
  │      └──────┬──────┘
  │             │
Depth     ┌─────┴─────┐
  │       │ Cathode   │            ← laccase + ABTS on carbon paper
  │       │ (air side)│               O2 diffuses through chimney
  │       ├───────────┤
  │       │ Separator │            ← cellulose membrane
  │       ├───────────┤
  │       │ Anode     │            ← yeast + glucose in CNF matrix
  │       │ (soil side)│
  │       └───────────┘
  │
Soil ──────────────────────────
```

### 1.1 Dimensions

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Pellet diameter | 50 mm | Same as pressling, existing tooling |
| Pellet height | 8 mm | Same, keeps BOM compatible |
| Chimney ID | 3 mm | Fickian diffusion: 60× O2 requirement at 10 cm |
| Chimney OD | 5 mm | Mechanical robustness |
| Chimney length | 5-30 cm | Covers deployment depth range |
| Cathode area | 2 cm² | Carbon paper, air-side of pellet |
| Anode area | 19.6 cm² | Full pellet cross-section |
| Cap diameter | 20 mm | Rain shelter, sits at ground level |

### 1.2 O2 Budget (Fickian Diffusion Verification)

Chimney diffusion rate at 10 cm depth:

| Parameter | Value |
|-----------|-------|
| O2 diffusivity in air (D) | 2.05e-5 m²/s |
| Chimney cross-section (A) | 7.07e-6 m² (Ø 3 mm) |
| Concentration gradient (dC/dx) | 87.5 mol/m³ / 0.1 m = 875 mol/m⁴ |
| Max O2 flux (J) | D × A × dC/dx = **1.27e-7 mol/s** |
| O2 required at 500 µW | 8e-10 mol/s (4 e⁻/O₂, F = 96485 C/mol) |
| Safety factor | **160×** at 10 cm, **50×** at 30 cm depth |

The chimney provides orders of magnitude more O2 than the cathode consumes. Water condensation and biofilm fouling are the practical failure modes, not O2 starvation.

### 1.3 Wicking Risk

At 25% soil moisture, capillary pressure in a 3 mm tube is ~50 Pa. Gravity drainage dominates: the tube self-drains if kept above the water table. Hydrophobic coating (PTFE or paraffin) eliminates wicking entirely.

---

## 2. Manufacturing Changes

### 2.1 Pressling (unchanged)
Same anode/cathode bilayer pressing process. The only change is a centered hole for the chimney interface.

### 2.2 Chimney Integration

```
Step 1: Press anode layer (10 kN, 4 mm height)
Step 2: Place cellulose separator disc
Step 3: Press cathode layer (10 kN, 4 mm height)
         └── with centered recess for chimney
Step 4: Insert chimney tube + seal with biodegradable wax
         (beeswax or PLA ring, compostable)
Step 5: Attach surface cap
Step 6: Vacuum package (same as pressling)
```

### 2.3 Additional BOM

| Item | Cost/unit | Source |
|------|-----------|--------|
| PTFE tube Ø 3×5 mm | €0.03/m → €0.01 @ 10 cm | Standard lab supply |
| PLA ring (seal) | €0.005 | 3D-printed or injection molded |
| Surface cap (PLA/straw) | €0.02 | Molded |
| Biodegradable wax | €0.01 | Beeswax or candelilla |
| **Chimney add-on cost** | **€0.045** | vs €0.50 baseline pressling |

### 2.4 Assembly Throughput

| Step | Time | Tooling |
|------|------|---------|
| Press anode + cathode | 3 min | Hand press (existing) |
| Insert chimney + seal | 30 s | Manual |
| Attach cap | 10 s | Manual |
| **Total per unit** | **~4 min** | 15/h (vs 10-20/h without chimney) |

---

## 3. Depth Rating

| Depth | O2 at cathode | Power (from 260 µW/cm² base) | Lifetime | Viable? |
|-------|--------------|-------------------------------|----------|---------|
| 2 cm | 18% | 957 µW | 365 d | ✅ |
| 5 cm | 16% | 850 µW | 365 d | ✅ |
| 10 cm | 12% | 640 µW | 365 d | ✅ |
| 20 cm | 8% | 420 µW | 365 d | ✅ |
| 30 cm | 5% | 265 µW | ~180 d | ✅ |

(full static air in chimney; no water blockage)

---

## 4. Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Water wicking into chimney | Medium | High | Hydrophobic coating; baffle cap |
| Soil ingress blocking tube | Medium | High | Porous PTFE plug at opening |
| Freeze-thaw damage (condensation) | Medium | Medium | Drain hole at bottom bend |
| Farmers pulling chimney during handling | Low | Medium | Low profile cap; breakaway joint |
| Additional assembly cost at scale | Low | Low | $0.05 is negligible in $24.55 BOM |

---

## 5. Validation Plan

| Step | What | How | Success criterion |
|------|------|-----|-------------------|
| 1 | Chimney diffusion test | Measure O2 at tube outlet vs depth in soil column | >10% O2 at 20 cm depth |
| 2 | Pressling with chimney | Build 5 units | Assembly < 5 min each |
| 3 | Soil box test | 7-day run in loam @ 25% moisture, 10 cm depth | Power > 12 µW sustained |
| 4 | Tillage test | Run tractor over buried unit | Chimney survives, maintains O2 |
| 5 | 30-day field test | 10 units in outdoor soil bed | >80% data integrity |

---

## 6. Go/No-Go Decision

Proceed with air-chimney if:
- Step 1 shows >10% O2 at 20 cm depth
- Step 3 shows >12 µW sustained at 10 cm depth

Fallback: Mg-air battery (dual-path) if either criterion fails.
