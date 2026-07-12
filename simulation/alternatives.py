#!/usr/bin/env python3
"""
Alternatives to the Pressling Approach

Quantitatively compares 6 design alternatives that address the fundamental
O2-starvation issue identified by pressling_viability.py.

Alternatives:
  A) AIR-CHIMNEY PRESSLING  — same fungal MFC, cathode breathes via porous tube
  B) SPLIT MFC              — fungal anode at depth, laccase cathode at surface
  C) Mg-Air BIODEGRADABLE   — Mg anode + air cathode (well-researched transient battery)
  D) PASSIVE NFC ONLY       — no battery at all, reader powers sensor momentarily
  E) SHALLOW BURIAL (2 cm)  — same pressling, just deploy at 2 cm depth
  F) Zn-Air BIODEGRADABLE   — Zn anode + air cathode (classic primary cell)

Each is evaluated on: viability (7d target), power margin, cost, biodegradability,
TRL, and O2-independence.
"""

import math
import random
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
import argparse

# =========================================================================
# CONSTANTS
# =========================================================================

PRESS_DIAMETER_MM = 50.0
PRESS_AREA_CM2 = math.pi * (PRESS_DIAMETER_MM / 2) ** 2 / 100
SOIL_TYPES_LIST = ["sand", "loam", "clay", "compost"]

SOIL_PROPS = {
    "sand":    {"porosity": 0.40, "field_capacity": 0.10},
    "loam":    {"porosity": 0.50, "field_capacity": 0.25},
    "clay":    {"porosity": 0.60, "field_capacity": 0.40},
    "compost": {"porosity": 0.70, "field_capacity": 0.35},
}
D_AIR = 0.205

DAILY_DEMAND_UJ = 504_000.0  # 0.14 mWh/day from MVP design

# =========================================================================
# O2 model (shared)
# =========================================================================

def o2_at_depth(depth_cm: float, soil_type: str = "loam",
                moisture_pct: float = 25.0) -> float:
    props = SOIL_PROPS.get(soil_type, SOIL_PROPS["loam"])
    epsilon = props["porosity"]
    theta = moisture_pct / 100.0
    if epsilon <= theta:
        d_eff = 1e-6
    else:
        d_eff = D_AIR * (epsilon - theta) ** (4 / 3) / epsilon ** 2
    o2 = 21.0 * math.exp(-depth_cm / (2 * math.sqrt(d_eff))) if d_eff > 0 else 0.01
    return max(o2, 0.01)

def o2_saturation(o2_pct: float, km_o2: float = 50e-6) -> float:
    o2_M = o2_pct / 21.0 * 250e-6
    return o2_M / (km_o2 + o2_M)

# =========================================================================
# DEVICE MODELS
# =========================================================================

@dataclass
class DeviceResult:
    name: str
    viable_7d: bool
    lifetime_days: float
    power_uw: float
    energy_margin_pct: float
    cost_euro: float
    bio_content_pct: float       # biodegradable mass fraction
    trl: int                     # technology readiness level 1-9
    o2_independent: bool         # does it need atmospheric O2?
    depth_limit_cm: float        # max burial depth before failing
    complexity: str              # Low / Medium / High

    def brief(self) -> str:
        status = "OK" if self.viable_7d else "FAIL"
        return (f"[{status:4s}] {self.name:25s}  {self.lifetime_days:>5.1f}d  "
                f"{self.power_uw:>6.1f}uW  bio={self.bio_content_pct:.0%}  "
                f"TRL={self.trl}  O2free={'Y' if self.o2_independent else 'N'}  "
                f"maxDepth={self.depth_limit_cm:.0f}cm")


# ─── A) Air-Chimney Pressling ────────────────────────────────────────────

def simulate_air_chimney(depth_cm: float = 10.0,
                          base_power_uw: float = 260.0,
                          chimney_radius_mm: float = 3.0) -> DeviceResult:
    """Pressling with a porous breathing tube to the surface.

    The chimney provides O2 to the cathode even at depth.
    O2 supply is limited by chimney diffusion resistance.
    """
    # O2 at cathode via chimney: diffusion through air in the tube
    # Diffusion rate: J = D * A * dC/dx  (Fick's first law)
    # We assume the chimney maintains ~18% O2 at the cathode
    # (slight drop from 21% due to consumption)
    o2_at_cathode = max(3.0, 21.0 - depth_cm * 0.3)  # simple gradient model
    o2_sat = o2_saturation(o2_at_cathode)

    # Enzyme retention for pressing (same as pressling)
    press_mpa = 30.0 / PRESS_AREA_CM2 * 10
    enzyme_ret = 1.0 / (1.0 + math.exp(0.12 * (press_mpa - 25.0)))
    geometry_eff = 0.7

    area_cm2 = PRESS_AREA_CM2
    raw_power = base_power_uw * area_cm2 * enzyme_ret * geometry_eff
    o2_limited = raw_power * o2_sat
    effective = min(raw_power, o2_limited)

    # Lifetime
    cum_supply = 0.0
    cum_demand = 0.0
    day = 0
    for day in range(1, 366):
        p = effective * (1 - 0.02) ** day
        cum_supply += p * 24 * 3600
        cum_demand += DAILY_DEMAND_UJ
        if cum_demand > cum_supply:
            break
    lifetime = float(day)
    margin = (cum_supply - cum_demand) / cum_demand * 100 if cum_demand > 0 else 0

    return DeviceResult(
        name="A) Air-Chimney Pressling",
        viable_7d=lifetime >= 7,
        lifetime_days=lifetime,
        power_uw=effective,
        energy_margin_pct=margin,
        cost_euro=0.60,    # pressling + chimney tube
        bio_content_pct=0.85,
        trl=2,             # concept only
        o2_independent=False,
        depth_limit_cm=30.0,  # chimney can go deep
        complexity="Medium",
    )


# ─── B) Split MFC (surface cathode + buried anode) ──────────────────────

def simulate_split_mfc(depth_cm: float = 10.0,
                        base_power_uw: float = 260.0) -> DeviceResult:
    """Fungal anode buried at depth, laccase air-cathode on surface.

    The anode (yeast + glucose) operates anaerobically -- no O2 needed.
    The cathode (laccase on carbon paper) sits at the surface, receiving
    full atmospheric O2. Connected by biodegradable carbon-fiber wire.

    This completely decouples the O2-requiring cathode from depth.
    """
    # Anode: no O2 limitation (yeast is anaerobic)
    # But pressing damage still applies
    press_mpa = 20.0 / PRESS_AREA_CM2 * 10  # lighter pressing for anode
    enzyme_ret = 1.0 / (1.0 + math.exp(0.12 * (press_mpa - 25.0)))

    # Cathode at surface: full O2 (21%)
    o2_sat = o2_saturation(21.0)

    area_cm2 = PRESS_AREA_CM2
    raw_power = base_power_uw * area_cm2 * enzyme_ret
    o2_limited = raw_power * o2_sat
    effective = raw_power  # no O2 limitation (cathode on surface)
    # But the cathode has its own area limitation: assume 2 cm² carbon paper
    cathode_power_limit = 500.0  # uW max for 2 cm² air-cathode
    effective = min(raw_power, cathode_power_limit)

    cum_supply = 0.0
    cum_demand = 0.0
    day = 0
    for day in range(1, 366):
        p = effective * (1 - 0.02) ** day
        cum_supply += p * 24 * 3600
        cum_demand += DAILY_DEMAND_UJ
        if cum_demand > cum_supply:
            break
    lifetime = float(day)
    margin = (cum_supply - cum_demand) / cum_demand * 100 if cum_demand > 0 else 0

    return DeviceResult(
        name="B) Split MFC (surface cathode)",
        viable_7d=lifetime >= 7,
        lifetime_days=lifetime,
        power_uw=effective,
        energy_margin_pct=margin,
        cost_euro=0.70,    # anode pellet + cathode paper + bio-wire
        bio_content_pct=0.90,
        trl=2,             # concept only, no bio-wire exists
        o2_independent=False,
        depth_limit_cm=50.0,  # anode can be deep, cathode is on surface
        complexity="High",
    )


# ─── C) Mg-Air Biodegradable Battery ────────────────────────────────────

def simulate_mg_air(depth_cm: float = 10.0) -> DeviceResult:
    """Mg anode + air cathode.

    Chemistry: Mg -> Mg2+ + 2e-  (E0 = -2.37 V)
               O2 + 2H2O + 4e- -> 4OH-  (E0 = +0.40 V)
               Overall: 2Mg + O2 + 2H2O -> 2Mg(OH)2  (E0 ~ 2.8V, practical ~1.6V)

    Energy density: ~2.8 kWh/kg Mg (theoretical), ~0.5-1.0 kWh/kg practical
    Mg is abundant, cheap (~$2.50/kg), and Mg(OH)2 is soil-compatible.

    Key challenge: corrosion rate control (H2 evolution).
    """
    # Mg-air needs O2 for the cathode. With air cathode on surface: OK.
    # Buried: O2 limited.
    if depth_cm > 2:
        o2_pct = o2_at_depth(depth_cm)
        # Mg-air cathode needs O2. With air-cathode design, it can use
        # a gas-diffusion electrode. If buried >2cm, still limited by soil O2.
        # But Mg-air can also use water reduction as parasitic cathode:
        # 2H2O + 2e- -> H2 + 2OH- (water reduction at cathode)
        # This is less efficient but O2-independent
        if depth_cm <= 5:
            o2_limit = o2_saturation(o2_pct)
            power = 500.0 * o2_limit + 50.0  # O2 + water reduction
        else:
            # Deep burial: mostly water reduction (inefficient)
            power = 80.0  # uW from water reduction only
    else:
        power = 500.0  # uW with full air access

    # Lifetime: Mg mass limited
    mg_mass_g = 0.5  # g of Mg foil
    # Practical energy: 0.5 kWh/kg * 0.0005 kg = 0.25 Wh = 900 J
    # At 500 uW: 900 J / 500e-6 W = 1,800,000 s = 20.8 days
    # At 80 uW: 900 / 80e-6 = 11,250,000 s = 130 days
    energy_j = mg_mass_g * 0.5 * 3600  # 0.5 Wh/g practical
    lifetime_s = energy_j / (power * 1e-6) if power > 0 else 0
    lifetime_d = min(lifetime_s / 86400, 365.0)

    # Also check against energy demand
    supply_j = power * 1e-6 * lifetime_s
    demand_j = DAILY_DEMAND_UJ * 1e-6 * lifetime_d
    margin = (supply_j - demand_j) / demand_j * 100 if demand_j > 0 else 0

    viable = lifetime_d >= 7
    # Cost
    mg_cost = mg_mass_g * 0.0025  # $2.50/kg
    cathode_cost = 0.10
    packaging = 0.05
    total_cost = mg_cost + cathode_cost + packaging

    return DeviceResult(
        name="C) Mg-Air Battery",
        viable_7d=viable,
        lifetime_days=lifetime_d,
        power_uw=power,
        energy_margin_pct=margin,
        cost_euro=total_cost,
        bio_content_pct=0.95,  # Mg(OH)2 fully degradable
        trl=3,                 # demonstrated in labs for transient electronics
        o2_independent=bool(depth_cm > 5),  # water reduction works deep
        depth_limit_cm=50.0,
        complexity="Medium",
    )


# ─── D) Passive NFC Only ─────────────────────────────────────────────────

def simulate_passive_nfc() -> DeviceResult:
    """No battery at all. Sensor powered by NFC reader during readout.

    The ST25DV04K NFC chip is passive-powered by the reader's RF field.
    The MCU wakes, takes one measurement, and sends data back.
    No logging between reads -- the sensor is truly zero-power.

    From MVP design: NFC readout is passive powered. Reader supplies
    energy for data transfer. No battery needed for communication.
    But we still need energy for the sensor measurement itself.
    """
    # NFC can deliver ~15-30 mW to the tag at close range (2-5 cm)
    # Sensor measurement: FDC1004 + MCU = ~220 uA * 3.3V * 5ms = 3.6 uJ
    # NFC field provides enough for the measurement + data transfer
    # No battery needed at all

    # Lifetime: unlimited (no battery to deplete)
    # The sensor works only when reader is present
    # For DevKit (research labs): farmer brings reader, this is acceptable
    # For field pilot (unattended): this is NOT acceptable

    return DeviceResult(
        name="D) Passive NFC (no battery)",
        viable_7d=True,  # unlimited battery life
        lifetime_days=365.0,
        power_uw=0.0,    # no battery power needed
        energy_margin_pct=0.0,
        cost_euro=0.0,   # no battery cost
        bio_content_pct=0.0,  # no battery = no bio-content
        trl=9,            # NFC is fully mature technology
        o2_independent=True,
        depth_limit_cm=5.0,  # NFC range is ~2-5 cm through soil
        complexity="Low",
    )


# ─── E) Shallow Burial (2 cm) ────────────────────────────────────────────

def simulate_shallow_burial(base_power_uw: float = 260.0) -> DeviceResult:
    """Same pressling, deployed at 2 cm depth instead of 10 cm.

    At 2 cm, there's enough O2 for the cathode.
    """
    depth = 2.0
    o2_pct = o2_at_depth(depth, "loam", 25.0)
    o2_sat_val = o2_saturation(o2_pct)

    press_mpa = 30.0 / PRESS_AREA_CM2 * 10
    enzyme_ret = 1.0 / (1.0 + math.exp(0.12 * (press_mpa - 25.0)))

    area_cm2 = PRESS_AREA_CM2
    geometry_eff = 0.7
    raw_power = base_power_uw * area_cm2 * enzyme_ret * geometry_eff
    effective = raw_power * o2_sat_val

    cum_supply = 0.0
    cum_demand = 0.0
    day = 0
    for day in range(1, 366):
        p = effective * (1 - 0.02) ** day
        cum_supply += p * 24 * 3600
        cum_demand += DAILY_DEMAND_UJ
        if cum_demand > cum_supply:
            break
    lifetime = float(day)
    margin = (cum_supply - cum_demand) / cum_demand * 100 if cum_demand > 0 else 0

    return DeviceResult(
        name="E) Shallow Burial (2 cm)",
        viable_7d=lifetime >= 7,
        lifetime_days=lifetime,
        power_uw=effective,
        energy_margin_pct=margin,
        cost_euro=0.50,  # same pressling, no extra cost
        bio_content_pct=0.90,
        trl=2,
        o2_independent=False,
        depth_limit_cm=3.0,
        complexity="Low (just bury shallower)",
    )


# ─── F) Zn-Air Biodegradable Battery ────────────────────────────────────

def simulate_zn_air(depth_cm: float = 10.0) -> DeviceResult:
    """Zn anode + air cathode.

    Chemistry: Zn + 2OH- -> ZnO + H2O + 2e- (E0 = -1.25 V)
               O2 + 2H2O + 4e- -> 4OH- (E0 = +0.40 V)
               Overall: 2Zn + O2 -> 2ZnO (E0 ~ 1.65 V)

    Energy density: ~1.3 kWh/kg (theoretical), ~0.4 kWh/kg practical
    Very mature tech (hearing aid batteries). ZnO is soil-compatible
    as a micronutrient, but high concentrations can be toxic.

    Same O2 problem as Mg-air for the cathode.
    """
    if depth_cm > 2:
        o2_pct = o2_at_depth(depth_cm)
        if depth_cm <= 5:
            o2_limit = o2_saturation(o2_pct)
            power = 800.0 * o2_limit  # higher power density than Mg
        else:
            # Zn-air is more O2-dependent than Mg-air
            power = 20.0  # uW from residual O2
    else:
        power = 800.0  # uW with full air

    zn_mass_g = 0.8  # g of Zn powder
    energy_j = zn_mass_g * 0.4 * 3600  # 0.4 Wh/g practical
    lifetime_s = energy_j / (power * 1e-6) if power > 0 else 0
    lifetime_d = min(lifetime_s / 86400, 365.0)

    supply_j = power * 1e-6 * lifetime_s
    demand_j = DAILY_DEMAND_UJ * 1e-6 * lifetime_d
    margin = (supply_j - demand_j) / demand_j * 100 if demand_j > 0 else 0

    viable = lifetime_d >= 7
    zn_cost = zn_mass_g * 0.002
    cathode_cost = 0.10
    alkaline_elec = 0.05
    total_cost = zn_cost + cathode_cost + alkaline_elec

    return DeviceResult(
        name="F) Zn-Air Battery",
        viable_7d=viable,
        lifetime_days=lifetime_d,
        power_uw=power,
        energy_margin_pct=margin,
        cost_euro=total_cost,
        bio_content_pct=0.70,  # ZnO degrades but alkaline electrolyte is problematic
        trl=5,                 # hearing aid batteries are TRL 9, but biodegradable version is TRL 4-5
        o2_independent=False,
        depth_limit_cm=3.0,
        complexity="Low",
    )


# =========================================================================
# COMPARISON
# =========================================================================

def run_all(depth_cm: float = 10.0) -> List[DeviceResult]:
    return [
        simulate_air_chimney(depth_cm),
        simulate_split_mfc(depth_cm),
        simulate_mg_air(depth_cm),
        simulate_passive_nfc(),
        simulate_shallow_burial(),
        simulate_zn_air(depth_cm),
    ]


def print_comparison(results: List[DeviceResult], depth: float):
    print(f"\n{'=' * 110}")
    print(f"  ALTERNATIVES COMPARISON @ {depth:.0f} cm burial depth")
    print(f"{'=' * 110}")

    hdr = (f"{'Status':>7}  {'Design':27s}  {'Life':>6}  {'Power':>7}  "
           f"{'Margin':>7}  {'Cost':>6}  {'Bio':>5}  {'TRL':>4}  "
           f"{'O2free':>7}  {'MaxD':>6}  {'Complexity':>10}")
    print(hdr)
    print("-" * 110)

    for r in sorted(results, key=lambda x: (not x.viable_7d, -x.lifetime_days, -x.bio_content_pct)):
        status = "OK" if r.viable_7d else "FAIL"
        print(f"{status:>7}  {r.name:27s}  {r.lifetime_days:>5.1f}d  "
              f"{r.power_uw:>6.1f}uW  {r.energy_margin_pct:>+6.0f}%  "
              f"{r.cost_euro:>5.2f}e  {r.bio_content_pct:>3.0%}  "
              f"{r.trl:>3d}  {'Y' if r.o2_independent else 'N':>7}  "
              f"{r.depth_limit_cm:>4.0f}cm  {r.complexity:>10}")


# =========================================================================
# DEPTH SWEEP
# =========================================================================

def depth_sweep() -> Dict[str, List]:
    """Show how each alternative performs across depths."""
    depths = [1, 2, 5, 8, 10, 15, 20, 30]
    all_results = {}

    for depth in depths:
        results = run_all(depth)
        all_results[depth] = {r.name.split(")")[1].strip(): r.viable_7d for r in results}

    print(f"\n{'=' * 90}")
    print("  VIABILITY ACROSS DEPTHS (shows where each alternative fails)")
    print(f"{'=' * 90}")
    print(f"{'Depth':>8}", end="")
    alt_names = list(all_results[depths[0]].keys())
    for name in alt_names:
        print(f"  {name:>24s}", end="")
    print()
    print("-" * 8 + "-" + "-" * 26 * len(alt_names))

    for depth in depths:
        print(f"{depth:>4} cm   ", end="")
        for name in alt_names:
            ok = all_results[depth][name]
            status = "   OK   " if ok else "  FAIL  "
            print(f"  {status:>24s}", end="")
        print()

    return all_results


# =========================================================================
# TRADE-OFF MATRIX
# =========================================================================

def print_tradeoff_matrix(results: List[DeviceResult]):
    """Weighted decision matrix across multiple criteria."""
    print(f"\n{'=' * 90}")
    print("  TRADE-OFF ANALYSIS (weighted score, higher = better)")
    print(f"{'=' * 90}")

    # Weights (can be tuned)
    w = {
        "viability": 0.25,     # must work for 7 days
        "lifetime": 0.10,       # longer is better
        "biodegradable": 0.20,  # core value prop
        "trl": 0.15,            # can we build it now?
        "o2_independent": 0.15, # freedom from depth constraint
        "cost": 0.10,           # cheaper is better
        "simplicity": 0.05,     # lower complexity is better
    }

    print(f"{'Design':30s}", end="")
    for k in w:
        print(f"  {k:>13s}", end="")
    print(f"  {'SCORE':>7s}")
    print("-" * 30 + "-" * 16 * len(w))

    # Normalize each criterion to 0-1
    max_life = max(r.lifetime_days for r in results)
    max_bio = max(r.bio_content_pct for r in results)
    max_trl = max(r.trl for r in results)
    max_cost = max(r.cost_euro for r in results)
    max_complex = 3  # Low=3, Med=2, High=1

    for r in results:
        # Score each criterion
        scores = {}
        scores["viability"] = 1.0 if r.viable_7d else 0.0
        scores["lifetime"] = min(r.lifetime_days / max_life, 1.0) if max_life > 0 else 0
        scores["biodegradable"] = r.bio_content_pct
        scores["trl"] = r.trl / max_trl if max_trl > 0 else 0
        scores["o2_independent"] = 1.0 if r.o2_independent else 0.0
        scores["cost"] = 1.0 - (r.cost_euro / max_cost) if max_cost > 0 else 1.0
        complexity_map = {"Low": 1.0, "Medium": 0.6, "High": 0.3}
        scores["simplicity"] = complexity_map.get(r.complexity, 0.5)

        total = sum(scores[k] * w[k] for k in w)

        print(f"{r.name:30s}", end="")
        for k in w:
            print(f"  {scores[k]:>10.2f}  ", end="")
        print(f"  {total:>7.3f}")


# =========================================================================
# MONTE CARLO FOR TOP CANDIDATES
# =========================================================================

def mc_alternatives(n_samples: int = 5000, seed: int = 42) -> Dict:
    """Monte Carlo for the two most promising non-trivial alternatives."""
    rng = random.Random(seed)

    def uniform(a, b):
        return a + rng.random() * (b - a)

    result = {}

    for label, sim_fn in [
        ("Air-Chimney Pressling", lambda d, bp: simulate_air_chimney(d, bp)),
        ("Split MFC", lambda d, bp: simulate_split_mfc(d, bp)),
    ]:
        viable_count = 0
        lifetimes = []
        for _ in range(n_samples):
            depth = uniform(5.0, 20.0)
            bp = uniform(12.5, 260.0)
            res = sim_fn(depth, bp)
            if res.viable_7d:
                viable_count += 1
            lifetimes.append(res.lifetime_days)
        lifetimes.sort()
        n = n_samples
        result[label] = {
            "p_viable": viable_count / n,
            "mean_life": sum(lifetimes) / n,
            "median_life": lifetimes[n // 2],
            "p10": lifetimes[int(n * 0.1)],
            "p90": lifetimes[int(n * 0.9)],
        }

    return result


def print_mc(mc: Dict):
    print(f"\n{'=' * 90}")
    print(f"  MONTE CARLO: Air-Chimney vs Split MFC")
    print(f"  (5-20 cm depth, 12.5-260 uW/cm2 base power, {list(mc.values())[0]['median_life']} samples)")
    print(f"{'=' * 90}")
    for label, data in mc.items():
        print(f"\n  {label}:")
        print(f"    P(viable 7d): {data['p_viable']:.1%}")
        print(f"    Lifetime: mean={data['mean_life']:.1f}d median={data['median_life']:.1f}d")
        print(f"    P10={data['p10']:.1f}d  P90={data['p90']:.1f}d")


# =========================================================================
# MAIN
# =========================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pressling alternatives comparison")
    parser.add_argument("--depth", type=float, default=10.0, help="Burial depth (cm)")
    parser.add_argument("--quick", action="store_true", help="Skip MC simulation")
    parser.add_argument("--samples", type=int, default=5000)
    args = parser.parse_args()

    print("#" * 110)
    print("#  PRESSLING ALTERNATIVES — comparative viability analysis")
    print("#" * 110)

    # 1. Full comparison at given depth
    results = run_all(args.depth)
    print_comparison(results, args.depth)

    # 2. Depth sweep
    depth_sweep()

    # 3. Trade-off matrix
    print_tradeoff_matrix(results)

    # 4. Key scoring analysis
    print(f"\n{'=' * 90}")
    print("  KEY INSIGHTS BY ALTERNATIVE")
    print(f"{'=' * 90}")

    for r in results:
        print(f"\n  {r.name}")
        if r.viable_7d:
            print(f"    OK: {r.lifetime_days:.0f}d life, {r.power_uw:.0f} uW, "
                  f"bio={r.bio_content_pct:.0%}, TRL={r.trl}")
            if r.name.startswith("D"):
                print(f"    Limitation: NFC range ~2-5 cm through soil, no unattended logging")
            elif r.name.startswith("E"):
                print(f"    Limitation: agricultural impracticality at 2 cm depth")
        else:
            failure_reason = []
            if r.lifetime_days < 7:
                failure_reason.append(f"lifetime={r.lifetime_days:.0f}d < 7d target")
            if not r.o2_independent:
                failure_reason.append("requires O2 at depth")
            print(f"    FAIL: {', '.join(failure_reason)}")

    # 5. Monte Carlo for top alternatives
    if not args.quick:
        mc = mc_alternatives(n_samples=args.samples)
        print_mc(mc)

    # 6. Recommendation
    print(f"\n{'=' * 90}")
    print("  RECOMMENDATION")
    print(f"{'=' * 90}")

    # Find best by weighted score
    w_score = {}
    for r in results:
        scores = {}
        scores["viability"] = 1.0 if r.viable_7d else 0.0
        scores["lifetime"] = min(r.lifetime_days / max(x.lifetime_days for x in results), 1.0)
        scores["biodegradable"] = r.bio_content_pct
        scores["trl"] = r.trl / max(x.trl for x in results)
        scores["o2_independent"] = 1.0 if r.o2_independent else 0.0
        scores["cost"] = 1.0 - (r.cost_euro / max(x.cost_euro for x in results))
        cmap = {"Low": 1.0, "Medium": 0.6, "High": 0.3}
        scores["simplicity"] = cmap.get(r.complexity, 0.5)
        w = {"viability": 0.25, "lifetime": 0.10, "biodegradable": 0.20,
             "trl": 0.15, "o2_independent": 0.15, "cost": 0.10, "simplicity": 0.05}
        w_score[r.name] = sum(scores[k] * w[k] for k in w)

    ranked = sorted(w_score.items(), key=lambda x: x[1], reverse=True)
    print(f"\n  Weighted ranking (higher = better overall fit):")
    for name, score in ranked:
        bar = "#" * int(score * 30)
        print(f"    {score:.3f}  {name:30s}  {bar}")

    print(f"\n  Bottom line:")
    print(f"    At {args.depth:.0f} cm burial depth, the pressling-only approaches fail due to O2 starvation.")
    print(f"    The most viable paths forward (in priority order):")
    print(f"")
    print(f"    1. Passive NFC (Phase 1 DevKit) — zero battery cost, TRL 9, no O2 problem.")
    print(f"       Good enough for research labs & development. No logging between reads.")
    print(f"")
    print(f"    2. Air-chimney pressling — modifies the casing, keeps the fungal story.")
    print(f"       Needs experimental validation of chimney + cathode integration.")
    print(f"       P(viable) = ~{(mc['Air-Chimney Pressling']['p_viable'] * 100) if not args.quick else '?'}% in MC")
    print(f"")
    print(f"    3. Mg-air biodegradable battery — higher TRL than fungal, O2-independent at depth")
    print(f"       via water reduction. Mg(OH)2 is soil-safe. Needs rate-control engineering.")
    print(f"")
    print(f"    (Avoid: split MFC — too complex, no bio-wire; Zn-air — same O2 problem, ZnO toxicity concern)")
    print()
