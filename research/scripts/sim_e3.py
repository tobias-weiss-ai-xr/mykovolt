"""
!!! DRAFT / NOT PHYSICALLY VALIDATED — DO NOT QUOTE RESULTS !!!
=============================================================
Phase-E E3 Co-culture Amplifier Simulator (v2-draft)
Monte-Carlo ODE: Trametes versicolor + Pleurotus ostreatus on a Mg-air cell.

DEBUG 2026-09-03 — 3 STRUCTURAL BUG FIXES NEEDED BEFORE RESULTS ARE MEANINGFUL:
1. CIRCUIT BUG: model uses 15 Ohm R_INTERNAL vs a 200 Ohm LOAD → produces ~0.1V
   (54 uW) instead of the verified #56/#47 figure (~1.48V, 480 uW surface).
   FIX: replace divider with BQ25570 MPPT model (kΩ source impedance).
2. GROWTH BUG: logistic term saturates T,P to 1e9 within 24 h -> zero variance.
   FIX: realistic carrying capacity (~1e8) + lag phase (#48).
3. O2 BUG: dO2 scaled by dt/24 -> O2 frozen at 0.209 -> #47 starvation
   failure NEVER fires. FIX: O2 diffusion ~1/3600 (1/h) with depth sink.

CURRENT OUTPUT IS ARTIFACTUAL (54 uW, 100% success, P10==P90). Do not trust.

GATES (E1 pH-stable / E2 hypha>=150cpm / Mg-anode-bal) assumed passed.
Parameters referenced from papers.yaml but model NOT yet calibrated to them.
"""
import numpy as np

# ---- Verified constants (papers.yaml) ----
MU_T       = 0.35    # 1/h max growth T. versicolor  (#48)
MU_P       = 0.42    # 1/h max growth P. ostreatus   (#48)
K_O2       = 0.03    # O2 half-saturation (#48)
CORR_PAR   = 0.37    # g Mg/day open-circuit self-corrosion (#56)
CORR_BIO   = 0.12    # +12% bio-corrosion (#56/#88)
CORR_AH    = 0.084   # g Mg per Ah Coulomb-counted delivered charge
HYP_PERM   = 2.4     # O2 permeability gain (#47)
LAC_BOOST  = 0.16    # V cathode overpotential cut at uA regime (#45, Zn->Mg scaled)
LAC_COVG   = 0.56    # biofilm coverage fraction (#109)
PH_DIE     = 10.5    # laccase inactivation (#88)
PH_BUF     = 0.015   # pH units/h buffered by laccase (#12)
MG_START   = 0.50    # g Mg anode (DevKit)
PWR_DEMAND = 150e-6  # W steady load (STM32L0 idle)
V_OCV      = 1.48    # Mg-air OCV (solubility-limited)
R_INT      = 15.0    # Ohm internal resistance (#56 polarization)
DEPTHS_CM  = [2, 5, 10, 20]  # #47 scaling depths
O2_SURF    = 0.209


def single_hourly_state(h, T, P, Mg, O2, pH):
    dt = 1.0
    # growth (Monod)
    o2_lim = O2 / (K_O2 + O2)
    dT = MU_T * T * (1 - T/1e9) * o2_lim * (1 - 0.5*(T/1e9))   # logistic + mutual inhibit (#71)
    p_lim = min(1.0, Mg/MG_START) * (pH/9.0)
    dP = MU_P * P * (1 - P/1e9) * p_lim

    # Mg: Coulomb-counted + parasitic corrosion (#56/#88)
    i_base = PWR_DEMAND / max(0.8, V_OCV * R_INT/(R_INT+200.0))
    i_par  = CORR_PAR/24.0 / CORR_AH               # A parasitic
    i_bio  = (1.0 + CORR_BIO * (T/1e9 + P/1e9))    # bio factor
    dMg = -( (i_par + i_base) * CORR_AH * dt / 3600.0 ) * i_bio

    # O2 amplification (#47)
    dO2 = (0.05*(O2_SURF - O2) + 0.0008*HYP_PERM*(P/1e8)*O2_SURF) * dt/24.0

    # pH drift + laccase buffering (#12/#88)
    dph_cor = 0.18 * (Mg < 0.15)       # alkaline shift on passivation (#56)
    dph_buf = -PH_BUF * (T/1e7) * LAC_COVG
    dpH = (dph_cor + dph_buf) * dt

    # emergent cell voltage (load-line intersection at 200 Ohm + 150uW demand)
    lac = min(1.0, (T/1e7)) * LAC_COVG
    v_ocv = V_OCV + lac*LAC_BOOST
    v_ocv *= max(0.4, Mg/MG_START)      # passivation collapse (#56)
    v_ocv *= (0.55 + 0.45*(O2/O2_SURF))  # O2 cathode limit
    v_ocv = max(0.05, min(v_ocv, 1.7))
    v_cell = v_ocv * R_INT/(R_INT+200.0)
    cur = v_cell/200.0
    pwr = cur*1e6*v_cell            # emergent µW
    if O2 < O2_SURF*0.16:            # #47 survival threshold
        pwr *= 0.0                  # below cutoff
    return dT,dP,dMg,dO2,dpH,v_cell,pwr,lac


def run_once(seed=None):
    rng = np.random.default_rng(seed)
    T,P,Mg,O2,pH = 1e6, 1e6, MG_START, O2_SURF, 8.1
    pwr_hist=[]; ph_hist=[]
    H=336  # 14 days
    fail=None; failh=None
    for h in range(H):
        dT,dP,dMg,dO2,dpH,vc,pwr,lac = single_hourly_state(h,T,P,Mg,O2,pH)
        # noise (#48/#56 uncertainty)
        T  += dT*(1+0.05*rng.standard_normal()); T=max(0.0,T)
        P  += dP*(1+0.05*rng.standard_normal()); P=max(0.0,P)
        Mg += dMg*(1+0.10*rng.standard_normal()); Mg=max(0.0,Mg)
        O2 =  min(O2_SURF,max(0.02, O2+dO2*(1+0.05*rng.standard_normal())))
        pH =  min(PH_DIE+0.3, max(5.5, pH+dpH*(1+0.08*rng.standard_normal())))
        pwr_hist.append(pwr); ph_hist.append(pH)
        # failure gates (#56/#88/#47)
        if Mg<=0.0:
            fail,failh="Mg_exhausted",h
            break
        if pH>PH_DIE and lac>0.1*CORR_AH:
            fail,failh="pH_denaturation",h
            break
        if O2<O2_SURF*0.05:
            fail,failh="O2_depletion",h
            break
    ok = fail is None
    avg2 = np.mean(pwr_hist[-24:]) if pwr_hist else 0.0
    # depth scaling (#47): apply O2-frac scaling to get 20cm-equivalent
    o2_now = O2
    d20 = avg2*(o2_now/O2_SURF) if ok else pwr_hist[-1]*(o2_now/O2_SURF)
    # depth penalties: 2cm=1.0x, 5cm=0.9x, 10cm=0.63x, 20cm=0.25x (#47 measured)
    d20 *= 0.25
    return {"ok":ok,"fail":fail,"failh":failh,
            "pwr2cm":avg2,"pwr20cm":d20,
            "minpH":min(ph_hist),"maxpH":max(ph_hist),
            "final":{"T":T,"P":P,"Mg":Mg,"O2":O2,"pH":pH}
            if ok else {"Mg":Mg,"pH":pH,"O2":O2}}


def main(n=2000):
    print("="*64)
    print("Phase-E E3 CO-CULTURE SIMULATOR v2  (Mg Coulomb-counting + emergent V)")
    print("="*64)
    res=[run_once(seed=i) for i in range(n)]
    ok=[r for r in res if r["ok"]]
    fails={}
    for r in res:
        if not r["ok"]: fails[r["fail"]]=fails.get(r["fail"],0)+1
    succ=len(ok)*100.0/n
    print(f"Runs: {n}  |  Success: {len(ok)} ({succ:.1f}%)")
    for k,v in fails.items(): print(f"  • {k:<20} {v:>5} ({v*100/n:.1f}%)")
    if ok:
        p2=[r["pwr2cm"] for r in ok]; p20=[r["pwr20cm"] for r in ok]
        print(f"\nSurface(2cm): mean={np.mean(p2):.0f} µW  P50={np.percentile(p2,50):.0f}  P10={np.percentile(p2,10):.0f}  P90={np.percentile(p2,90):.0f}")
        print(f"Depth(20cm):  mean={np.mean(p20):.1f} µW  P50={np.percentile(p20,50):.1f}  P10={np.percentile(p20,10):.1f}  P90={np.percentile(p20,90):.1f}")
        print(f"\nMg-air control (#47): 480 µW (surface) | 12 µW (20cm)")
        g=np.mean(p20)/12.0; gs=np.mean(p2)/480.0
        print(f"→ gain @20cm: {g:.1f}x  |  @surface: {gs:.1f}x")
        verdict = "GO bench E3" if succ>70 else ("RISKY – buffer + E3b" if succ>20 else "NO-GO –Mg-air MVP")
        print(f"\nVERDICT: {verdict}")
    else:
        print("\nAll runs failed — revert to E1/E2 or Mg-air MVP.")
    print("="*64)

if __name__=="__main__":
    main(2000)
