#!/usr/bin/env python3
"""
Pressling Viability Simulation — stdlib only

Simulates the key unvalidated aspects of the pressed-pellet (Pressling) approach:

  1) PRESSING DAMAGE — compression effects on enzyme activity & porosity
  2) O2 STARVATION — oxygen diffusion into soil at burial depth
  3) MONTE CARLO — probabilistic viability under uncertainty

Usage:
  python3 pressling_viability.py           # full Monte Carlo run
  python3 pressling_viability.py --quick   # fast parameter sweep only
"""

import math
import random
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict, Callable
import argparse

# =========================================================================
# 1. PRESSING MODEL — compression effects on the pellet
# =========================================================================

PRESS_DIAMETER_MM = 50.0
PRESS_AREA_CM2 = math.pi * (PRESS_DIAMETER_MM / 2) ** 2 / 100


def press_force_to_mpa(force_kN: float) -> float:
    # 1 kN/cm² = 10 MPa
    return force_kN / PRESS_AREA_CM2 * 10


def porosity_vs_pressure(pressure_mpa: float, initial_porosity: float = 0.7) -> float:
    """Compression reduces porosity (exponential compaction model)."""
    k = 0.08
    return initial_porosity * math.exp(-k * pressure_mpa)


def enzyme_retention_vs_pressure(pressure_mpa: float) -> float:
    """Laccase activity retention after compression (sigmoid decay)."""
    p50 = 25.0
    k = 0.12
    return 1.0 / (1.0 + math.exp(k * (pressure_mpa - p50)))


def conductivity_vs_porosity(porosity: float, base_conductivity: float = 10.0) -> float:
    """Effective conductivity per Archie's law."""
    tau = 2.0
    return base_conductivity * (1.0 - porosity) ** tau


# =========================================================================
# 2. O2 DIFFUSION IN SOIL
# =========================================================================

SOIL_PROPS = {
    "sand":    {"porosity": 0.40, "field_capacity": 0.10},
    "loam":    {"porosity": 0.50, "field_capacity": 0.25},
    "clay":    {"porosity": 0.60, "field_capacity": 0.40},
    "compost": {"porosity": 0.70, "field_capacity": 0.35},
}

D_AIR = 0.205  # cm2/s


def o2_concentration_at_depth(depth_cm: float, soil_type: str = "loam",
                               moisture_pct: float = 25.0) -> float:
    """O2 volume % at depth via Millington-Quirk diffusivity model."""
    props = SOIL_PROPS.get(soil_type, SOIL_PROPS["loam"])
    epsilon = props["porosity"]
    theta = moisture_pct / 100.0

    if epsilon <= theta:
        d_eff = 1e-6
    else:
        d_eff = D_AIR * (epsilon - theta) ** (4 / 3) / epsilon ** 2

    o2 = 21.0 * math.exp(-depth_cm / (2 * math.sqrt(d_eff))) if d_eff > 0 else 0.01
    return max(o2, 0.01)


def o2_limited_power(o2_concentration_pct: float, max_power_uw: float,
                     km_o2: float = 50e-6) -> float:
    """Michaelis-Menten power limitation by O2 availability."""
    o2_M = o2_concentration_pct / 21.0 * 250e-6
    saturation = o2_M / (km_o2 + o2_M)
    return max_power_uw * saturation


# =========================================================================
# 3. COMBINED PRESSLING MODEL
# =========================================================================

@dataclass
class PresslingConfig:
    press_force_kN: float = 30.0
    diameter_mm: float = 50.0
    height_mm: float = 8.0
    initial_porosity: float = 0.70

    base_power_density_uw_cm2: float = 260.0
    empa_baseline_uw_cm2: float = 12.5
    laccase_km_o2_mM: float = 50e-6

    burial_depth_cm: float = 10.0
    soil_type: str = "loam"
    soil_moisture_pct: float = 25.0

    deg_per_day_pct: float = 2.0
    target_days: float = 7.0
    geometry_efficiency: float = 0.7

    @property
    def area_cm2(self) -> float:
        return math.pi * (self.diameter_mm / 10) ** 2 / 4

    @property
    def pressure_mpa(self) -> float:
        return press_force_to_mpa(self.press_force_kN)


@dataclass
class PresslingResult:
    viable: bool
    lifetime_days: float
    porosity: float
    enzyme_retention: float
    conductivity_s_m: float
    o2_at_depth_pct: float
    o2_saturation: float
    o2_limited_power_uw: float
    raw_power_uw: float
    effective_power_uw: float
    safety_margin: float
    deg_days_to_50pct: int
    daily_demand_uj: float
    daily_supply_day1_uj: float
    energy_margin_pct: float

    def brief(self) -> str:
        status = "OK" if self.viable else "FAIL"
        return (f"[{status}] {self.lifetime_days:.1f}d | "
                f"{self.effective_power_uw:.1f}uW | "
                f"por={self.porosity:.2f} | "
                f"enz={self.enzyme_retention:.0%} | "
                f"O2={self.o2_at_depth_pct:.1f}% | "
                f"mgn={self.energy_margin_pct:+.0f}%")


def simulate_pressling(cfg: PresslingConfig) -> PresslingResult:
    pressure = cfg.pressure_mpa
    porosity = porosity_vs_pressure(pressure, cfg.initial_porosity)
    enzyme_ret = enzyme_retention_vs_pressure(pressure)
    conductivity = conductivity_vs_porosity(porosity)

    raw_power = cfg.base_power_density_uw_cm2 * cfg.area_cm2 * enzyme_ret * cfg.geometry_efficiency

    o2_pct = o2_concentration_at_depth(cfg.burial_depth_cm, cfg.soil_type, cfg.soil_moisture_pct)
    o2_limited = o2_limited_power(o2_pct, raw_power, cfg.laccase_km_o2_mM)
    o2_M = o2_pct / 21.0 * 250e-6
    o2_sat = o2_M / (cfg.laccase_km_o2_mM + o2_M)

    effective_power = min(raw_power, o2_limited)

    daily_demand_uj = 504_000.0  # 0.14 mWh/day from MVP design = 504 uWh = 504,000 uJ

    cum_supply = 0.0
    cum_demand = 0.0
    day = 0
    for day in range(1, 366):
        power_today = effective_power * (1 - cfg.deg_per_day_pct / 100) ** day
        cum_supply += power_today * 24 * 3600
        cum_demand += daily_demand_uj
        if cum_demand > cum_supply:
            break

    lifetime = float(day)
    energy_margin = (cum_supply - cum_demand) / cum_demand * 100 if cum_demand > 0 else 0
    safety = effective_power / (daily_demand_uj / 24 / 3600) if daily_demand_uj > 0 else 0
    half_life = math.log(0.5) / math.log(1 - cfg.deg_per_day_pct / 100)

    return PresslingResult(
        viable=lifetime >= cfg.target_days,
        lifetime_days=lifetime,
        porosity=porosity,
        enzyme_retention=enzyme_ret,
        conductivity_s_m=conductivity,
        o2_at_depth_pct=o2_pct,
        o2_saturation=o2_sat,
        o2_limited_power_uw=o2_limited,
        raw_power_uw=raw_power,
        effective_power_uw=effective_power,
        safety_margin=safety,
        deg_days_to_50pct=int(half_life),
        daily_demand_uj=daily_demand_uj,
        daily_supply_day1_uj=effective_power * 24 * 3600,
        energy_margin_pct=energy_margin,
    )


# =========================================================================
# 4. MONTE CARLO SIMULATION
# =========================================================================

SOIL_TYPES = ["sand", "loam", "clay", "compost"]


def run_monte_carlo(n_samples: int = 10000, seed: int = 42) -> Dict:
    rng = random.Random(seed)

    def uniform(a, b):
        return a + rng.random() * (b - a)

    def choice(seq):
        return seq[rng.randint(0, len(seq) - 1)]

    results = []
    for _ in range(n_samples):
        pf = uniform(10.0, 50.0)
        bp = uniform(12.5, 260.0)
        depth = uniform(5.0, 15.0)
        moisture = uniform(10.0, 40.0)
        soil = choice(SOIL_TYPES)
        deg = uniform(1.0, 5.0)
        geo = uniform(0.3, 1.0)
        km = uniform(20e-6, 150e-6)

        cfg = PresslingConfig(
            press_force_kN=pf,
            base_power_density_uw_cm2=bp,
            burial_depth_cm=depth,
            soil_moisture_pct=moisture,
            soil_type=soil,
            deg_per_day_pct=deg,
            laccase_km_o2_mM=km,
            geometry_efficiency=geo,
        )
        res = simulate_pressling(cfg)

        results.append({
            "viable": res.viable,
            "lifetime": res.lifetime_days,
            "power_uw": res.effective_power_uw,
            "porosity": res.porosity,
            "enzyme_ret": res.enzyme_retention,
            "o2_pct": res.o2_at_depth_pct,
            "margin": res.energy_margin_pct,
            "press_kN": pf,
            "base_power": bp,
            "depth": depth,
            "moisture": moisture,
            "soil": soil,
            "geo_eff": geo,
            "deg_rate": deg,
        })

    n = len(results)
    viable_count = sum(1 for r in results if r["viable"])
    lifetimes = [r["lifetime"] for r in results]
    powers = [r["power_uw"] for r in results]

    lifetimes_sorted = sorted(lifetimes)
    powers_sorted = sorted(powers)

    def percentile(data, p):
        idx = int(len(data) * p / 100)
        return data[min(idx, len(data) - 1)]

    # Sensitivity by soil type
    soil_breakdown = {}
    for st in SOIL_TYPES:
        sres = [r for r in results if r["soil"] == st]
        if sres:
            sv = sum(1 for r in sres if r["viable"])
            sl = [r["lifetime"] for r in sres]
            sp = [r["power_uw"] for r in sres]
            soil_breakdown[st] = {
                "p": sv / len(sres),
                "mean_life": sum(sl) / len(sl),
                "mean_power": sum(sp) / len(sp),
                "n": len(sres),
            }

    # Pearson correlation of each param with viability (point-biserial)
    def corr(xs, ys):
        n = len(xs)
        mx = sum(xs) / n
        my = sum(ys) / n
        num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
        dy = math.sqrt(sum((y - my) ** 2 for y in ys))
        return num / (dx * dy) if dx * dy > 0 else 0

    viable_float = [1.0 if r["viable"] else 0.0 for r in results]
    sensitivities = {}
    for param in ["press_kN", "base_power", "depth", "moisture", "geo_eff", "deg_rate"]:
        vals = [r[param] for r in results]
        c = corr(vals, viable_float)
        sensitivities[param] = c

    # Three deterministic scenarios
    scenarios = {}
    for label, params in [
        ("optimistic", {"base_power_density_uw_cm2": 260.0, "burial_depth_cm": 5.0,
                        "soil_moisture_pct": 10.0, "soil_type": "sand"}),
        ("realistic", {"base_power_density_uw_cm2": 50.0, "burial_depth_cm": 10.0,
                       "soil_moisture_pct": 25.0, "soil_type": "loam"}),
        ("pessimistic", {"base_power_density_uw_cm2": 12.5, "burial_depth_cm": 12.0,
                         "soil_moisture_pct": 35.0, "soil_type": "clay"}),
    ]:
        cfg = PresslingConfig(**params)
        res = simulate_pressling(cfg)
        scenarios[label] = {
            "viable": res.viable,
            "lifetime": res.lifetime_days,
            "power_uw": res.effective_power_uw,
        }

    return {
        "n": n,
        "prob_viable": viable_count / n,
        "mean_lifetime": sum(lifetimes) / n,
        "median_lifetime": lifetimes_sorted[n // 2],
        "p10_lifetime": percentile(lifetimes_sorted, 10),
        "p90_lifetime": percentile(lifetimes_sorted, 90),
        "mean_power": sum(powers) / n,
        "median_power": powers_sorted[n // 2],
        "sensitivities": sensitivities,
        "soil_breakdown": soil_breakdown,
        "scenarios": scenarios,
    }


# =========================================================================
# 5. PARAMETER SWEEP
# =========================================================================

def run_sweep() -> List[Dict]:
    results = []
    press_forces = [10, 20, 30, 40, 50]
    depths = [2, 5, 8, 10, 12, 15]

    for pf in press_forces:
        for depth in depths:
            for moisture in [15, 25, 35]:
                cfg = PresslingConfig(press_force_kN=pf, burial_depth_cm=depth,
                                      soil_moisture_pct=moisture)
                res = simulate_pressling(cfg)
                results.append({
                    "press": pf, "depth": depth, "moisture": moisture,
                    "viable": res.viable, "lifetime": res.lifetime_days,
                    "power": res.effective_power_uw, "porosity": res.porosity,
                    "enzyme": res.enzyme_retention, "o2": res.o2_at_depth_pct,
                    "margin": res.safety_margin,
                })
    return results


# =========================================================================
# 6. DISPLAY
# =========================================================================

def print_sweep_table(sweep: List[Dict]):
    print(f"\n{'=' * 90}")
    print("  PRESSLING VIABILITY SWEEP (T. pubescens base)")
    print(f"{'=' * 90}")
    hdr = f"{'kN':>5} {'Depth':>6} {'Moist':>6}  {'Status':>7}  {'Life':>7}  {'Power':>8}  {'Poros':>6}  {'Enz':>5}  {'O2%':>5}  {'Sfty':>6}"
    print(hdr)
    print("-" * 90)
    for r in sweep:
        status = "OK" if r["viable"] else "--"
        print(f"{r['press']:>5.0f} {r['depth']:>6.0f} {r['moisture']:>6.0f}  "
              f"{status:>7}  {r['lifetime']:>6.1f}d  "
              f"{r['power']:>7.1f}uW  "
              f"{r['porosity']:>5.2f}  "
              f"{r['enzyme']:>3.0%}  "
              f"{r['o2']:>4.1f}%  "
              f"{r['margin']:>+5.1f}x")


def print_mc_results(mc: Dict):
    print(f"\n{'=' * 90}")
    print(f"  MONTE CARLO PRESSLING VIABILITY ({mc['n']:,} samples)")
    print(f"{'=' * 90}")

    p = mc["prob_viable"]
    if p >= 0.8:
        verdict = "PROMISING -- pressling likely viable"
    elif p >= 0.5:
        verdict = "TENTATIVE -- plausible but high uncertainty"
    elif p >= 0.2:
        verdict = "RISKY -- significant challenges expected"
    else:
        verdict = "UNLIKELY -- fundamental issues with pressling approach"

    print(f"\n  VERDICT: {verdict}")
    print(f"  P(viable for 7 days): {p:.1%}")
    print(f"\n  LIFETIME")
    print(f"    Mean:   {mc['mean_lifetime']:.1f} days")
    print(f"    Median: {mc['median_lifetime']:.1f} days")
    print(f"    P10:    {mc['p10_lifetime']:.1f} days")
    print(f"    P90:    {mc['p90_lifetime']:.1f} days")
    print(f"    Mean power: {mc['mean_power']:.1f} uW")

    print(f"\n  SENSITIVITY (correlation with viability)")
    sorted_s = sorted(mc['sensitivities'].items(), key=lambda x: abs(x[1]), reverse=True)
    for name, c in sorted_s:
        d = "+" if c > 0 else "-"
        bar = "#" * int(abs(c) * 30)
        print(f"    {d} {name:15s}  r = {c:+.3f}  {bar}")

    print(f"\n  BY SOIL TYPE")
    for st, data in mc['soil_breakdown'].items():
        print(f"    {st:10s}: P(ok) = {data['p']:.1%},  "
              f"life = {data['mean_life']:.1f}d,  "
              f"power = {data['mean_power']:.1f} uW  (n={data['n']})")

    print(f"\n  SCENARIO ANALYSIS")
    for label, sc in mc['scenarios'].items():
        icon = "OK" if sc["viable"] else "--"
        print(f"    [{icon}] {label:12s}: {sc['lifetime']:.1f}d @ {sc['power_uw']:.1f} uW")


# =========================================================================
# 7. MAIN
# =========================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pressling Viability Simulation")
    parser.add_argument("--quick", action="store_true", help="skip Monte Carlo")
    parser.add_argument("--samples", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    print("#" * 90)
    print("#  PRESSLING VIABILITY ANALYSIS")
    print("#  pressed-pellet fungal bio-battery simulation")
    print("#" * 90)

    # 1. Baseline: MVP design assumptions
    base_cfg = PresslingConfig()
    base_res = simulate_pressling(base_cfg)

    print(f"\nBASELINE (MVP Design Assumptions)")
    print(f"  Press: {base_cfg.press_force_kN:.0f} kN ({base_cfg.pressure_mpa:.1f} MPa)")
    print(f"  Base power density: {base_cfg.base_power_density_uw_cm2} uW/cm2 (BO optimum)")
    print(f"  Burial: {base_cfg.burial_depth_cm} cm, {base_cfg.soil_type} @ {base_cfg.soil_moisture_pct}%")
    print(f"  Target: {base_cfg.target_days} days")
    print(f"  --> {base_res.brief()}")

    if not base_res.viable:
        print(f"  Constraints:")
        if base_res.enzyme_retention < 0.7:
            print(f"    * Enzyme retention ({base_res.enzyme_retention:.0%}) -- pressing denatures laccase")
        if base_res.o2_at_depth_pct < 10:
            print(f"    * O2 at depth ({base_res.o2_at_depth_pct:.1f}%) -- cathode starved")
        if base_res.effective_power_uw < base_res.raw_power_uw * 0.8:
            print(f"    * O2 limits power: {base_res.o2_limited_power_uw:.1f} vs {base_res.raw_power_uw:.1f} uW raw")

    # 2. Empa baseline (demonstrated)
    empa_cfg = PresslingConfig(base_power_density_uw_cm2=12.5)
    empa_res = simulate_pressling(empa_cfg)
    print(f"\nEMPA BASELINE (demonstrated 2024)")
    print(f"  Base: 12.5 uW/cm2 (real)")
    print(f"  --> {empa_res.brief()}")

    # 3. Sweep
    sweep = run_sweep()
    print_sweep_table(sweep)

    # Viable frontier
    ok_rows = [r for r in sweep if r["viable"]]
    if ok_rows:
        shallow = min(ok_rows, key=lambda r: r["depth"])
        dry = min(ok_rows, key=lambda r: r["moisture"])
        print(f"\n  Viable frontier: depth <= {shallow['depth']:.0f} cm, "
              f"moisture <= {dry['moisture']:.0f}% at {dry['press']:.0f} kN")
    else:
        print(f"\n  NO viable configuration in sweep range")

    # 4. Monte Carlo
    if not args.quick:
        mc = run_monte_carlo(n_samples=args.samples, seed=args.seed)
        print_mc_results(mc)

    # 5. Detailed press damage table
    print(f"\n  Pressing damage to laccase:")
    for pf in [10, 20, 30, 40, 50]:
        p = press_force_to_mpa(pf)
        ret = enzyme_retention_vs_pressure(p)
        por = porosity_vs_pressure(p)
        print(f"    {pf:2d} kN ({p:4.1f} MPa): enzyme={ret:.0%}, porosity={por:.2f}")

    print(f"\n  O2 at depth (loam, 25% moisture):")
    for d in [2, 5, 8, 10, 12, 15, 20]:
        o2 = o2_concentration_at_depth(d, "loam", 25)
        lim = o2_limited_power(o2, 100)
        print(f"    {d:2d} cm: {o2:.1f}% O2 -> {lim:.1f} uW (from 100 uW base)")

    # Bottom line
    print()
