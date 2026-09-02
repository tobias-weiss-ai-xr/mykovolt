"""
!!! DRAFT / Under Calibration (E3.0 cycle) !!!
=============================================================
Phase-E E3 Co-culture Amplifier Simulator (v3-physics)
Models: Mg-air cell as voltage source + kOhm impedance, boosted by BQ25570
(MPP, 0.33V UVLO, 80% eff), Trametes laccase biocathode (+bias), Pleurotus
hyphal air-channel (O2 permeability). Calibrated to papers.yaml:
  #47  -> 480 µW surface, 12 µW @20cm (target)
  #56  -> 0.21 mA/cm^2 self-corrosion
  #109 -> 12.5 µW/cm^2 Trametes baseline
  #45  -> +0.16 V laccase cathode bias at uA regime (Zn->Mg scaled)

Run to produce E3.0c validation report: docs/simulation/e3_validation_report.md
STATUS: v3 implements the circuit-correct + diffusion model; _VALIDATED flips True
 once output reproduces #47 within ±20%.
"""
import numpy as np

# ---- Verified constants (papers.yaml) ----
MU_T       = 0.35    # 1/h max growth T. versicolor  (#48)
MU_P       = 0.42    # 1/h max growth P. ostreatus   (#48)
K_O2       = 0.03    # O2 half-saturation (#48)
MG_START   = 0.50    # g Mg anode (DevKit)
PWR_DEMAND = 150e-6  # W DevKit steady draw
V_OCV_BASE = 1.48    # Mg-air OCV (solubility-limited) (#56)
R_SOURCE   = 8_000.0 # Ohm source impedance (Mg-air, uA regime, #56 Tafel fit)
BOOST_EFF  = 0.80    # BQ25570 MPPT efficiency (#56: 0.33V start)
V_UVLO     = 0.33    # V  BQ25570 under-voltage lockout
LAC_BOOST  = 0.16    # V  laccase cathode bias (scaled #45, Zn->uA Mg)
LAC_COVG   = 0.56    # biofilm coverage (#109)
PH_DIE     = 10.5    # laccase denature (#88)
PH_BUF     = 0.015   # pH buffering by laccase (#12)
HYP_PERM   = 2.4     # O2 permeability gain (#47)
O2_DEPLETION = 0.16  # #47 survival threshold (surface frac)
O2_STARVE  = 0.05    # hard cutoff (#47)
CORR_PAR   = 0.37    # g Mg/day open-circuit (#56)
CORR_BIO   = 0.12    # bio-corrosion factor (#56/#88)
CORR_AH    = 0.084   # g Mg per Ah delivered (Faraday Mg -> Mg2+)
O2_SURF    = 0.209
DEPTHS_CM  = [2, 5, 10, 20]
_VALIDATED = False   # set True only after #47 within ±20% (E3.0c)
# Depth scaling DERIVED from O2 availability (papers.yaml #47):
# Mg-air-only (no hyphae) drops to 16% O2 at 20cm -> 12/480 = 0.025.
# Mycelium air-channel RAISES local pO2 -> relaxes the depth penalty.
O2_ONLY_FRAC = {2:1.00, 5:0.60, 10:0.25, 20:0.025}  # #47 Mg-air O2 fraction vs depth
def depth_factor(depth_cm, o2):
    """Hyphal permeability lifts local O2 above Mg-air-only profile (#47)."""
    o2_only = O2_ONLY_FRAC.get(depth_cm, 0.025)
    # gain factor: how much hyphae exceed bare-soil O2 at this depth
    gain = max(1.0, o2 / max(0.01, o2_only))
    # power scales ~sqrt(O2) (kinetic cathodic) * gain (air-channel)
    return min(1.0, (o2 / 0.209) ** 0.5) * min(2.4, gain)  # hyphal cap = HYP_PERM

def single_hourly_state(h, T, P, Mg, O2, pH, depth_cm):
    """Return derivatives + emergent power for current state."""
    dt = 1.0
    # --- growth (Monod, logistic, #48/#71) ---
    o2_lim = O2 / (K_O2 + O2)
    dT = MU_T * T * (1 - T/1e8) * o2_lim * (1 - 0.5*(T/1e8))
    p_lim = min(1.0, Mg/MG_START) * max(0.2, pH/9.0)
    dP = MU_P * P * (1 - P/1e8) * p_lim

    # --- Mg: Coulomb counting + parasitic corrosion (#56/#88) ---
    i_parasite = (CORR_PAR/24.0) / CORR_AH              # A  open-circuit loss
    # delivered current at MPP (if cell alive)
    v_ocv = V_OCV_BASE + min(1.0, (T/1e7))*LAC_COVG*LAC_BOOST
    v_ocv *= max(0.5, Mg/MG_START)                      # passivation (#56)
    v_ocv *= (0.55 + 0.45*(O2/O2_SURF))                 # O2 limit
    v_ocv = max(0.05, min(v_ocv, 1.7))
    if v_ocv > V_UVLO:
        v_mpp = v_ocv / 2.0
        i_deliv = v_mpp / max(R_SOURCE, 1.0)
        i_deliv = min(i_deliv, PWR_DEMAND / max(v_mpp, 0.1))
    else:
        v_mpp = 0.0; i_deliv = 0.0
    i_total = i_parasite + i_deliv
    bio = 1.0 + CORR_BIO*(T/1e9 + P/1e9)
    dMg = -(i_total * CORR_AH) * dt / 3600.0 * bio        # g Mg consumed

    # --- O2 diffusion + amplification (#47) ---
    k_diff = 0.06   # surface replenish 1/h
    dO2 = k_diff * (O2_SURF - O2) * dt
    dO2 += 0.02 * HYP_PERM * (P/1e8) * (O2_SURF - O2) * dt
    if O2 < O2_DEPLETION:
        dO2 -= 0.15 * dt

    # --- pH drift + laccase buffering (#12/#88) ---
    dph_cor = 0.18 * (Mg < 0.15)         # alkaline shift on passivation
    dph_buf = -PH_BUF * (T/1e7) * LAC_COVG
    dpH = (dph_cor + dph_buf) * dt

    # --- emergent power at this depth (#47 scaling) ---
    pwr_w = BOOST_EFF * v_mpp * i_deliv if v_mpp > V_UVLO else 0.0
    pwr = pwr_w * 1e6            # microWatts
    pwr *= depth_factor(depth_cm, O2)
    pwr = max(0.0, pwr)
    cur = i_deliv
    return dT, dP, dMg, dO2, dpH, v_mpp, pwr, cur, max(0, T/1e7)*LAC_COVG


def run_depth(depth_cm, seed=None):
    """Run 14-day sim at fixed depth; return result dict + trajectory."""
    rng = np.random.default_rng(seed)
    T, P = 1e5, 1e5          # lower inoculum (realistic lag, #48)
    Mg, O2, pH = MG_START, O2_SURF, 8.1
    pwr_hist = []; o2_hist = []; mg_hist = []
    fail = None; failh = None
    for h in range(336):
        dT, dP, dMg, dO2, dpH, vm, pmw, cur, lac = single_hourly_state(h, T, P, Mg, O2, pH, depth_cm)
        # stochastic noise (#48/#56 parameter uncertainty ±5-10%)
        T  = max(0.0, T  + dT  * (1 + 0.06*rng.standard_normal()))
        P  = max(0.0, P  + dP  * (1 + 0.06*rng.standard_normal()))
        Mg = max(0.0, Mg + dMg * (1 + 0.10*rng.standard_normal()))
        O2 = min(O2_SURF, max(0.01, O2 + dO2 * (1 + 0.06*rng.standard_normal())))
        pH = min(PH_DIE+0.3, max(5.0, pH + dpH * (1 + 0.08*rng.standard_normal())))
        pwr_hist.append(pmw); o2_hist.append(O2); mg_hist.append(Mg)
        # failure gates
        if Mg <= 0.0: fail,failh="Mg_exhausted",h; break
        if pH > PH_DIE and lac > 0.10: fail,failh="pH_denaturation",h; break
        if O2 < O2_STARVE: fail,failh="O2_depletion",h; break
    ok = fail is None
    avg = np.mean(pwr_hist[-24:]) if pwr_hist else 0.0
    return {"ok":ok,"fail":fail,"failh":failh,"pwr":avg,
            "minpH":min(pwr_hist) and min(pwr_hist), "final":{"Mg":Mg,"O2":O2,"pH":pH}}


def dt_with_noise(dT, frac, rng):
    return dT * (1 + frac*rng.standard_normal())


def main(n=2000):
    print("="*64)
    print("Phase-E E3 CO-CULTURE SIMULATOR v3 (circuit-correct + diffusion)")
    print("="*64)
    print("Calibration: papers.yaml #47 (480 uW surf / 12 uW @20cm)")
    v02 = run_depth(2,  seed=0)
    v20 = run_depth(20, seed=0)
    print(f"  surface(2cm): {v02['pwr']:.1f} uW  (target 480)")
    print(f"  depth(20cm):  {v20['pwr']:.1f} uW  (target 12)")
    print()
    allp = {d: [] for d in DEPTHS_CM}
    first_fail = {"Mg_exhausted":0,"pH_denaturation":0,"O2_depletion":0}
    succ = 0
    for i in range(n):
        rok=True; ff=None
        for d in DEPTHS_CM:
            r=run_depth(d, seed=i)
            allp[d].append(r["pwr"])
            if rok and not r["ok"]:
                rok=False; ff=r["fail"]
        if rok: succ+=1
        elif ff: first_fail[ff]=first_fail.get(ff,0)+1
    print(f"Monte-Carlo: {n} runs x {len(DEPTHS_CM)} depths. Success: {succ}/{n}")
    print("Depth x power (uW):")
    for d in DEPTHS_CM:
        a=np.array(allp[d])
        print(f"  {d:>3}cm: mean={a.mean():.1f}  P50={np.percentile(a,50):.1f}  P10={np.percentile(a,10):.1f}  P90={np.percentile(a,90):.1f}")
    p20=np.array(allp[20]); p2=np.array(allp[2])
    g20=p20.mean()/12.0; g2=p2.mean()/480.0
    print(f"Mg-air baseline (#47): surface 480 uW | depth 12 uW")
    print(f"  -> gain @20cm: {g20:.1f}x | @surface: {g2:.1f}x")
    print("First-failure (per run):")
    for k,v in first_fail.items():
        if v: print(f"  {k:<18} {v:>4} ({v*100/n:.1f}%)")
    ver = ("INVALID (calib off)" if not _VALIDATED else
           ("GO bench E3" if succ>70 and g20>1.5 else
            ("RISKY - buffer E3b" if succ>20 else "NO-GO - Mg-air MVP")))
    print(f"\nVERDICT: {ver}")
    print("="*64)

if __name__=="__main__":
    main(2000)
