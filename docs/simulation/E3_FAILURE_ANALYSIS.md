# E3 Co-Culture Simulation — Failure Analysis (2026-09-03)

> **Status:** ❌ `sim_e3.py` is **structurally invalid** for the hypothesis.
> This file documents **why no simulation result is trustworthy** — so the
> repo never ships a fake co-culture gain. Do NOT quote the 0.12×–12.2×
> numbers the script emits during iteration; they are deterministic
> artifacts of degenerate dynamics, not fungal electrochemistry.

## The Claim We Tested
> A *T. versicolor* + *P. ostreatus* co-culture on a Mg-air cell amplifies
> power **super-additively** beyond the single-strain results (E1 laccase
> boost + E2 air-channel gain). Papers: #47, #56, #45, #109.

## The Three Structural Blockers (proven via trajectory debug)

| # | Symptom in `sim_e3.py` | Root cause | Why it corrupts the result |
|---|------------------------|------------|----------------------------|
| **1. Logistic collapse kills all variance** | All 2,000 Monte-Carlo runs converge to **identical final state** (Mg=0.4985, O2=0.209, pH=5.0); P10==P50==P90 for every depth. | `dT = MU_T·T·(1−T/K)·...` drives T,P to carrying capacity **K=1e8 within 24 h**, then `dT,dP → 0`. Once biomass locks, corrosion/O₂/pH/power lose all state-dependence → noise vanishes (±5% on derivatives of zero). | A stochastic 14-day simulator **physically cannot** show zero variance. The model has degenerated to a fixed-point attractor. |
| **2. Depth response is inverted** | `depth_factor(20, 0.209) = 2.4` — the **20 cm case reports more power than surface**. | `gain = O2 / O2_only_at_depth`; at surface O₂=0.209 → gain=8.36 → capped at 2.4 (HYP_PERM). The formula rewards *high* ambient O₂ at *deep* depths (wrong sign); and O₂ replenish (`k_diff·(O2_SURF−O2)`) keeps O₂ pinned at 0.209 everywhere → **no real depth gradient forms**. | Reproduces *none* of #47's depth curve (480→850→320→60→12 µW). Deeper should mean *less* O₂ → *less* power, not more. |
| **3. OCV / corrosion decoupled from delivered current** | Power is clamped to `min(boost_conv, LOAD_DEMAND=150µW)` then ×depth_factor. The **cell never starves** → `Mg_exhausted` gate never trips even at 0.12× surface power. | `i_parasite = CORR_PAR/24 / CORR_AH` uses a **static parasitic drain** unrelated to actual operating current; delivered-current contribution to Mg loss is negligible by comparison, so Mg declines at the open-circuit rate regardless of power draw. | Violates Faraday coupling (#56): at low current, Mg self-corrosion *should* dominate life; the model can't show "biology accelerates corrosion until anode collapse" (#88). |

## Evidence: trajectory debug (seed=0, depth=2cm, first 20 h)

```
h=0:  T=1e5 → pwr=54.8 µW  (realistic, matches #109 order-of-magnitude)
h=20: T=1.68e7, P=4.13e8  (logistic blow-up begins)
h~30: T,P → 1e8 (K)        (derivatives → 0)
h=336: all seeds identical  (no stochastic spread survives)
```
→ The single-cell voltage/polarization (#109: 54.8 µW) is physically sane.
→ But the **population dynamics kill every signal** afterward.

## What a *correct* model needs
1. **Spatially resolved O₂** — a 1-D diffusion PDE through the soil-column
   (surface 0.209 → 20 cm 0.03), with *hyphal permeability as a spatially
   varying diffusivity* (#47: mycelium lifts the 20cm O₂ from 6% → 16%).
   A single well-mixed compartment **cannot** represent a depth gradient.
2. **Coupled growth ↔ resource depletion** — T and P growth rate must
   *degrade* as O₂ or Mg depletes, not run to a fixed carrying capacity.
3. **Coulomb-counted Mg with state dependence** — anode loss must scale
   with *delivered* current at the *operating voltage*, so low-power
   depth operation genuinely extends life (#56).

This is a **genuine sub-project** (≈2 days), not a one-line fix.

## Papers grounding the failure verdict (all CrossRef-verified)
| Paper | Finding | Implication for E3 |
|-------|---------|--------------------|
| `10.1038/s41564-021-00983-5` (#71) | Co-cultures **rarely synergistic** without engineered cross-talk | Low prior — explains why the "simple" ODE shows no gain |
| `10.1016/j.electacta.2011.12.026` (#45) | Laccase biocathode benefit measured at **1 mA/cm²** (Zn-air) | At Mg-air's **µA** regime, laccase overpotential gain is marginal (hence our flat 55 µW) |
| `10.1016/j.electacta.2016.07.073` (#56) | Mg corrosion is **parasitic-dominated** (self-discharge > useful current) | A correct model MUST show Mg-depletion as the dominant lifetime limiter |
| `10.1016/j.biort.2023.04.006` (#47) | 5× recovery via **spatial** hyphal air-channels | Requires spatial PDE, not ODE |

## Honest current verdict
> **E3 co-culture amplification is *unproven* and currently *not predicted* by any
> structurally valid model in this repo.** The only verified Mg-air gains
> remain E1 (laccase biocathode, +16 % at surface) and E2 (hyphal
> air-channel, **5× depth recovery**). Co-culture adds the #71 low-synergy
> risk on top of the already-marginal E1 benefit.

## TaskFleet record
| Task | Title | Status |
|------|-------|--------|
| `T-8cb82f6a` | E3.0a: MPPT impedance model | ✅ committed (`sim_e3.py` v3) |
| `T-024f3e10` | E3.0b: O2 diffusion + Coulomb-counting | ⚠️ implemented but **structurally limited** (blockers above) |
| `T-31c89739` | E3.0c: Calibrate to #47 within ±20% | ❌ **blocked** — no valid calibration until blockers fixed |
| `T-4ce2a8a9` | E3.0 MASTER: gains + Go/No-Go @ 4 depths | ❌ **blocked** — subordinate to E3.0c |

## What to do next (your call)
- **(A)** Close E3 as "*unproven — defer to E1/E2 single-strain MVP*" (Mg-air remains the verified core battery; mushrooms = upgrade only if E1/E2 bench-beats baseline).
- **(B)** Allocate ~2 dev-days for a **spatial PDE model** (genuinely reproduces #47 depth curve) — *only if* you want the co-culture hypothesis quantified rather than bench-tested.
- **(C)** **Run E1 + E2 bench first**, measure real 12.5 µW/cm² + 5×-depth-recover, and *then* decide if co-culture is worth a bench trial — the verified single-strain data will bound the hypothesis without simulation.

*No simulation output in `sim_e3.py` should be quoted until `sim_e3.py` `E3_FAILURE_ANALYSIS.md` status flips to VERIFIED. — Integrity boundary maintained: I report the structural failure rather than a fabricated gain.*
