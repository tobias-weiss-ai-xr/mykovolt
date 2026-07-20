#!/usr/bin/env python3
"""
Dual-Path Analysis: Air-Chimney Pressling vs Mg-Air Battery
Under realistic field conditions (temperature, moisture, depth variation).

Outputs a comprehensive comparison table and saves to dual_path_results.txt
"""

import math
import random
from dataclasses import dataclass
from typing import List, Dict, Tuple

# =========================================================================
# Shared constants
# =========================================================================

D_AIR = 0.205               # O2 diffusivity in air (cm2/s)
PRESS_DIAMETER_MM = 50.0
PRESS_AREA_CM2 = math.pi * (PRESS_DIAMETER_MM / 2) ** 2 / 100
DAILY_DEMAND_UJ = 504_000.0  # 0.14 mWh/day

SOIL_PROPS = {
    "sand":    {"porosity": 0.40, "fc": 0.10},
    "loam":    {"porosity": 0.50, "fc": 0.25},
    "clay":    {"porosity": 0.60, "fc": 0.40},
    "compost": {"porosity": 0.70, "fc": 0.35},
}

# =========================================================================
# Physics models
# =========================================================================

def o2_at_depth(depth_cm, soil_type, moisture_pct, temp_C=20):
    props = SOIL_PROPS.get(soil_type, SOIL_PROPS["loam"])
    epsilon = props["porosity"]
    theta = moisture_pct / 100.0

    # Temperature dependence: D ∝ T^1.75 (kinetic gas theory)
    d_air_t = D_AIR * ((temp_C + 273.15) / 293.15) ** 1.75

    if epsilon <= theta:
        d_eff = 1e-6
    else:
        d_eff = d_air_t * (epsilon - theta) ** (4/3) / epsilon ** 2

    o2 = 21.0 * math.exp(-depth_cm / (2 * math.sqrt(d_eff))) if d_eff > 0 else 0.01
    return max(o2, 0.01)


def o2_limited_power(o2_pct, max_power, km_o2=50e-6):
    o2_M = o2_pct / 21.0 * 250e-6
    sat = o2_M / (km_o2 + o2_M)
    return max_power * sat


def enzyme_retention(pressure_mpa):
    return 1.0 / (1.0 + math.exp(0.12 * (pressure_mpa - 25.0)))


def mg_corrosion_rate(temp_C, soil_type, moisture_pct, pH=7.0):
    """Mg corrosion rate in mm/year.
    
    Baseline at 20°C, loam, 25% moisture, pH 7: ~1 mm/year
    Temperature: doubles per 10°C (Arrhenius)
    Moisture: linear from fc to saturation
    pH: slow in neutral, fast in acid (pH < 6) or alkaline (pH > 10)
    """
    props = SOIL_PROPS.get(soil_type, SOIL_PROPS["loam"])
    fc = props["fc"]
    
    # Arrhenius temperature factor
    t_factor = 2.0 ** ((temp_C - 20.0) / 10.0)
    
    # Soil moisture factor: corrosion needs water
    # Below field capacity: slow. Near saturation: fast.
    moisture_ratio = (moisture_pct / 100.0) / fc if fc > 0 else 1.0
    m_factor = min(max(moisture_ratio, 0.1), 3.0)
    
    # pH factor: minimum at neutral, increases at extremes
    ph_factor = 1.0 + 0.5 * (pH - 7.0) ** 2
    
    # Baseline: 1 mm/year at 20°C, loam, 25% moisture, pH 7
    baseline = 1.0
    return baseline * t_factor * m_factor * ph_factor


def mg_power_at_depth(depth_cm, soil_type, moisture_pct, temp_C=20, 
                       mg_mass_g=0.5, mg_area_cm2=5.0, pH=7.0):
    """Mg-air power at given conditions.
    
    Shallow (< 5 cm): mixed O2 + water reduction, ~500 uW possible
    Deep (> 5 cm): mostly water reduction, 50-200 uW depending on corrosion rate
    """
    o2_pct = o2_at_depth(depth_cm, soil_type, moisture_pct, temp_C)
    corr_rate = mg_corrosion_rate(temp_C, soil_type, moisture_pct, pH)

    if depth_cm <= 3:
        # Surface air mode: O2 cathode active, high power
        sat = o2_pct / 21.0
        power = 500.0 * sat
    elif depth_cm <= 8:
        # Transition: some O2 + water reduction
        sat = o2_pct / 21.0
        o2_part = 500.0 * sat
        water_part = 50.0 * (corr_rate / 1.0) * mg_area_cm2
        power = o2_part + water_part
    else:
        # Deep: mostly water reduction, proportional to corrosion rate
        power = 80.0 * (corr_rate / 1.0) * (mg_area_cm2 / 5.0)

    # Mg mass limited lifetime
    # Practical energy density: 0.5 Wh/g Mg
    # At low power: Mg lasts longer
    energy_wh = mg_mass_g * 0.5
    max_lifetime_h = energy_wh / (max(power, 1) * 1e-6) if power > 1 else 1
    lifetime_d = min(max_lifetime_h / 24, 365.0)

    return power, lifetime_d


def chimney_pressling_power(depth_cm, soil_type, moisture_pct, temp_C=20,
                              base_power_density=260.0, press_kN=20.0):
    """Air-chimney pressling: cathode gets O2 via breathing tube.
    
    Chimney model: O2 at cathode = 18% minus minor gradient loss.
    """
    # Chimney O2 delivery (Fickian)
    chimney_id_mm = 3.0
    chimney_area = math.pi * (chimney_id_mm / 2) ** 2 * 1e-2  # cm2
    d_air_t = D_AIR * ((temp_C + 273.15) / 293.15) ** 1.75
    o2_flux_mol_s = (d_air_t * chimney_area * 8.75 / depth_cm * 100) if depth_cm > 0 else 1e-6
    # O2 required for power: ~8e-10 mol/s per 500 uW
    max_power_from_chimney = (o2_flux_mol_s / 8e-10) * 500.0

    # Pressling power
    press_mpa = press_kN / PRESS_AREA_CM2 * 10
    enzyme_ret = enzyme_retention(press_mpa)
    
    area = PRESS_AREA_CM2
    raw_power = base_power_density * area * enzyme_ret * 0.7
    effective = min(raw_power, max_power_from_chimney)

    # Temperature effect on biology: optimal at 30°C, drops at extremes
    if temp_C < 5:
        temp_factor = 0.1
    elif temp_C < 15:
        temp_factor = 0.3 + 0.7 * (temp_C - 5) / 10
    elif temp_C <= 30:
        temp_factor = 1.0
    elif temp_C <= 40:
        temp_factor = 1.0 - 0.5 * (temp_C - 30) / 10
    else:
        temp_factor = 0.1
    effective *= temp_factor

    # Lifetime with degradation
    cum_supply = 0.0
    cum_demand = 0.0
    day = 0
    for day in range(1, 366):
        p = effective * (1 - 0.02) ** day
        cum_supply += p * 24 * 3600
        cum_demand += DAILY_DEMAND_UJ
        if cum_demand > cum_supply:
            break
    lifetime_d = float(day)

    return effective, lifetime_d


# =========================================================================
# Full comparison
# =========================================================================

def compare_paths(depth_cm=10, soil_type="loam", moisture_pct=25, temp_C=20):
    """Compare both paths under identical conditions."""
    a_power, a_life = chimney_pressling_power(depth_cm, soil_type, moisture_pct, temp_C)
    b_power, b_life = mg_power_at_depth(depth_cm, soil_type, moisture_pct, temp_C)

    o2_val = o2_at_depth(depth_cm, soil_type, moisture_pct, temp_C)
    corr = mg_corrosion_rate(temp_C, soil_type, moisture_pct)

    return {
        "depth": depth_cm,
        "soil": soil_type,
        "moisture": moisture_pct,
        "temp": temp_C,
        "o2_pct": o2_val,
        "mg_corr_rate": corr,
        "a_power": a_power,
        "a_life": a_life,
        "a_viable": a_life >= 7,
        "b_power": b_power,
        "b_life": b_life,
        "b_viable": b_life >= 7,
    }


def print_results(results: List[dict], title: str):
    print(f"\n{'=' * 105}")
    print(f"  {title}")
    print(f"{'=' * 105}")
    hdr = (f"{'Conditions':>35s}  {'O2%':>5}  {'Corr':>5}  "
           f"{'A-Power':>8}  {'A-Life':>7}  {'A?':>3}  "
           f"{'B-Power':>8}  {'B-Life':>7}  {'B?':>3}")
    print(hdr)
    print("-" * 105)

    for r in results:
        cond = f"{r['soil']:>8} {r['depth']:>3}cm {r['moisture']:>3}%H2O {r['temp']:>3}°C"
        o2 = f"{r['o2_pct']:>4.2f}" if r['o2_pct'] > 0.01 else "<.01"
        corr = f"{r['mg_corr_rate']:.2f}"
        a_p = f"{r['a_power']:.1f}"
        a_l = f"{r['a_life']:.1f}d"
        a_v = "Y" if r['a_viable'] else "N"
        b_p = f"{r['b_power']:.1f}"
        b_l = f"{r['b_life']:.1f}d"
        b_v = "Y" if r['b_viable'] else "N"
        print(f"  {cond:>35s}  {o2:>5}  {corr:>5}  "
              f"{a_p:>8}  {a_l:>7}  {a_v:>3}  "
              f"{b_p:>8}  {b_l:>7}  {b_v:>3}")


def depth_sweep_temp():
    """Depth × temperature sweep for both paths."""
    depths = [2, 5, 8, 10, 15, 20]
    temps = [5, 15, 25, 35]
    results = []
    for d in depths:
        for t in temps:
            results.append(compare_paths(depth_cm=d, temp_C=t))
    print_results(results, "DEPTH × TEMPERATURE SWEEP (loam, 25% moisture)")


def moisture_sweep():
    """Moisture × depth sweep."""
    moistures = [10, 20, 30, 40]
    depths = [5, 10, 15]
    results = []
    for m in moistures:
        for d in depths:
            results.append(compare_paths(depth_cm=d, moisture_pct=m))
    print_results(results, "MOISTURE × DEPTH SWEEP (loam, 20°C)")


def soil_type_sweep():
    """Soil type comparison."""
    results = []
    for soil in ["sand", "loam", "clay", "compost"]:
        results.append(compare_paths(soil_type=soil))
    print_results(results, "SOIL TYPE COMPARISON (10 cm, 25% moisture, 20°C)")


def winter_vs_summer():
    """Winter vs summer scenario."""
    results = []
    scenarios = [
        ("Winter (5°C, 35% H2O, clay)", "clay", 35, 5),
        ("Spring (15°C, 30% H2O, loam)", "loam", 30, 15),
        ("Summer (30°C, 15% H2O, sand)", "sand", 15, 30),
        ("Harvest (25°C, 25% H2O, loam)", "loam", 25, 25),
        ("Heavy rain (20°C, 45% H2O, clay)", "clay", 45, 20),
        ("Drought (35°C, 5% H2O, sand)", "sand", 5, 35),
    ]
    for label, soil, moist, temp in scenarios:
        r = compare_paths(soil_type=soil, moisture_pct=moist, temp_C=temp)
        r["label"] = label
        results.append(r)
    
    print(f"\n{'=' * 105}")
    print(f"  SEASONAL SCENARIOS (10 cm depth)")
    print(f"{'=' * 105}")
    print(f"{'Scenario':>35s}  {'O2%':>5}  {'Corr':>5}  "
          f"{'A-Power':>8}  {'A-Life':>7}  {'A?':>3}  "
          f"{'B-Power':>8}  {'B-Life':>7}  {'B?':>3}")
    print("-" * 105)
    for r in results:
        cond = r["label"]
        o2 = f"{r['o2_pct']:>4.2f}" if r['o2_pct'] > 0.01 else "<.01"
        corr = f"{r['mg_corr_rate']:.2f}"
        a_p = f"{r['a_power']:.1f}"
        a_l = f"{r['a_life']:.1f}d"
        a_v = "Y" if r['a_viable'] else "N"
        b_p = f"{r['b_power']:.1f}"
        b_l = f"{r['b_life']:.1f}d"
        b_v = "Y" if r['b_viable'] else "N"
        print(f"  {cond:>35s}  {o2:>5}  {corr:>5}  "
              f"{a_p:>8}  {a_l:>7}  {a_v:>3}  "
              f"{b_p:>8}  {b_l:>7}  {b_v:>3}")


def mc_both_paths(n=5000, seed=42):
    """Monte Carlo for both paths simultaneously."""
    rng = random.Random(seed)

    def uniform(a, b):
        return a + rng.random() * (b - a)

    a_ok = 0
    b_ok = 0
    both_ok = 0
    neither_ok = 0

    for _ in range(n):
        depth = uniform(5, 20)
        moisture = uniform(10, 40)
        temp = uniform(5, 35)
        soil = rng.choice(["sand", "loam", "clay", "compost"])
        base_power = uniform(12.5, 260.0)

        a_p, a_l = chimney_pressling_power(depth, soil, moisture, temp, base_power)
        b_p, b_l = mg_power_at_depth(depth, soil, moisture, temp)

        a_v = a_l >= 7
        b_v = b_l >= 7
        if a_v: a_ok += 1
        if b_v: b_ok += 1
        if a_v and b_v: both_ok += 1
        if not a_v and not b_v: neither_ok += 1

    print(f"\n{'=' * 60}")
    print(f"  MONTE CARLO ({n:,} samples, random depth/soil/moisture/temp)")
    print(f"{'=' * 60}")
    print(f"  Pfad A (Air-Chimney Pressling): {a_ok/n:.1%} viable")
    print(f"  Pfad B (Mg-Air Battery):        {b_ok/n:.1%} viable")
    print(f"  Beide:                          {both_ok/n:.1%}")
    print(f"  Keiner:                         {neither_ok/n:.1%}")
    print()


# =========================================================================
# Main
# =========================================================================

if __name__ == "__main__":
    import sys
    out_path = "dual_path_results.txt" if len(sys.argv) < 2 else sys.argv[1]

    # Run and capture output
    import io
    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf

    print("#" * 105)
    print("#  DUAL-PATH ANALYSIS: Air-Chimney Pressling vs Mg-Air Battery")
    print("#  Simulated under realistic field conditions")
    print("#" * 105)

    # Single comparison at baseline
    bl = compare_paths()
    print(f"\nBASELINE (10 cm, loam, 25% moisture, 20°C):")
    print(f"  O2 at depth: {bl['o2_pct']:.2f}%")
    print(f"  Mg corrosion rate: {bl['mg_corr_rate']:.2f} mm/year")
    print(f"  Pfad A (Air-Chimney Pressling): power={bl['a_power']:.1f} uW, "
          f"lifetime={bl['a_life']:.1f}d, viable={'Y' if bl['a_viable'] else 'N'}")
    print(f"  Pfad B (Mg-Air Battery):        power={bl['b_power']:.1f} uW, "
          f"lifetime={bl['b_life']:.1f}d, viable={'Y' if bl['b_viable'] else 'N'}")

    depth_sweep_temp()
    moisture_sweep()
    soil_type_sweep()
    winter_vs_summer()
    mc_both_paths()

    # Summary
    print(f"\n{'=' * 105}")
    print(f"  SUMMARY")
    print(f"{'=' * 105}")
    print(f"""
  Air-Chimney Pressling (Pfad A)
    Braucht: funktionierenden MFC + Chimney-Integrität
    Stärken: "echte" Pilzbatterie, glaubwürdige Green Story
    Schwächen: temperaturempfindlich (< 10°C = 30% power), Chimney bruchanfällig
    Beste Bedingungen: > 15°C, Sand/Lehm, < 30% moisture
    Schlechteste: < 10°C, Ton, Nässe

  Mg-Air Battery (Pfad B)
    Braucht: kontrollierte Mg-Korrosion (1-3 mm/year)
    Stärken: O2-unabhängig, breiterer Temperaturbereich, einfacher
    Schwächen: H2-Entwicklung, Korrosionskontrolle schwierig
    Beste Bedingungen: neutraler pH, moderate Feuchte, 15-30°C
    Schlechteste: extrem sauer oder alkalisch (korrodiert zu schnell)

  Empfehlung
    Beide Pfad A und B entwickeln. Mg-Air ist der sicherere Pfad
    für Phase 2 (Feldpilot), weil O2-unabhängig.
    Air-Chimney ist der bessere Pfad für die Positionierung
    ("erste kompostierbare Pilzbatterie") — wenn die Chimney-Technik hält.
""")

    # Restore stdout and write to file
    sys.stdout = old_stdout
    output = buf.getvalue()
    
    # Print to console
    print(output)
    
    # Save to file
    with open(out_path, "w") as f:
        f.write(output)
    print(f"\n  Results saved to {out_path}")
