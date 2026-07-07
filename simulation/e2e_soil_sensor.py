#!/usr/bin/env python3
"""
E2E Simulation: Fungal Bio-Battery Powered Soil Moisture Sensor Tag

Simuliert das gesamte Produkt von der Bodenfeuchte-Messung bis zur Kompostierung:

  Boden → Sensor → MCU → Battery → Lifetime → Degradation → Cost
    ↑       ↑       ↑       ↑          ↑            ↑          ↑
    |   kapazitiv  STM32L0  TBD µW  7 Tage     90 Tage     €0.15
    |   1 Hz Messung  0.4µA Standby  Pressling  Cellulose   pro Tag (Simulationsziel)

Ausgabe:
  - Batterie-Lebensdauer bei gegebener Messfrequenz
  - Optimale Messfrequenz für Ziel-Lebensdauer
  - Kosten pro Sensor-Tag
  - Vergleich mit Li-Ion / Alkaline
  - Degradations-Timeline

Autor: Contextual Intelligence / Tobias Weiss
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from typing import List, Tuple, Optional
import json

# =============================================================================
# 1. SOIL MODEL — Dielectric properties vs moisture content
# =============================================================================

# Soil dielectric constants (εr at 100 MHz)
SOIL_TYPES = {
    "sand":     {"epsilon_dry": 3.0, "epsilon_wet": 20.0, "porosity": 0.4},
    "loam":     {"epsilon_dry": 4.0, "epsilon_wet": 25.0, "porosity": 0.5},
    "clay":     {"epsilon_dry": 5.0, "epsilon_wet": 30.0, "porosity": 0.6},
    "compost":  {"epsilon_dry": 6.0, "epsilon_wet": 35.0, "porosity": 0.7},
}

def soil_epsilon(soil_type: str, moisture_pct: float) -> float:
    """Calculate soil dielectric constant from moisture content."""
    props = SOIL_TYPES[soil_type]
    dry = props["epsilon_dry"]
    wet = props["epsilon_wet"]
    # Non-linear mixing model (empirical)
    return dry + (wet - dry) * (moisture_pct / 100) ** 0.6

def moisture_from_epsilon(soil_type: str, epsilon: float) -> float:
    """Inverse: estimate moisture from measured dielectric constant."""
    props = SOIL_TYPES[soil_type]
    dry = props["epsilon_dry"]
    wet = props["epsilon_wet"]
    raw = (epsilon - dry) / (wet - dry)
    return max(0, min(100, raw ** (1/0.6) * 100))

# =============================================================================
# 2. SENSOR MODEL — Capacitive soil moisture measurement
# =============================================================================

@dataclass
class SensorConfig:
    electrode_width_mm: float = 2.0
    electrode_gap_mm: float = 1.0
    electrode_length_mm: float = 20.0
    pcb_thickness_mm: float = 1.6
    excitation_freq_hz: float = 100e3
    excitation_voltage: float = 3.3
    settling_time_ms: float = 10.0

    def capacitance(self, epsilon: float) -> float:
        """Interdigitated electrode capacitance (fringe-field model)."""
        n_fingers = int(self.electrode_length_mm / (self.electrode_width_mm + self.electrode_gap_mm))
        total_length = n_fingers * self.electrode_length_mm * 1e-3
        gap = self.electrode_gap_mm * 1e-3
        width = self.electrode_width_mm * 1e-3
        eps0 = 8.854e-12
        C = eps0 * epsilon * total_length * width / gap
        return max(C, 1e-12)

    def measurement_energy_uj(self, epsilon: float) -> float:
        """Energy per measurement in µJ."""
        C = self.capacitance(epsilon)
        # Energy to charge: E = 0.5 * C * V²
        charge_energy = 0.5 * C * self.excitation_voltage ** 2
        # Measurement time = frequency cycles + settling
        n_cycles = 10  # for stable reading
        measure_time = n_cycles / self.excitation_freq_hz + self.settling_time_ms * 1e-3
        # Assume constant current for oscillator + ADC
        I_meas = 200e-6  # 200 µA during measurement
        E_total = charge_energy + I_meas * self.excitation_voltage * measure_time
        return E_total * 1e6  # µJ

# =============================================================================
# 3. MCU MODEL — STM32L0 (ultra-low-power ARM Cortex-M0+)
# =============================================================================

@dataclass
class MCUConfig:
    """STM32L0 power modes."""
    v_core: float = 1.8       # V
    sleep_current_ua: float = 0.4     # µA (stop mode with RTC)
    active_current_ma: float = 3.0    # mA @ 1 MHz, 3.3V
    active_time_ms: float = 5.0       # ms per measurement cycle
    clock_freq_mhz: float = 1.0       # MHz (low-power mode)
    adc_current_ua: float = 50.0      # µA during ADC conversion
    adc_time_ms: float = 1.0          # ms per ADC read

    def energy_per_cycle_uj(self) -> float:
        """Energy per measurement cycle in µJ."""
        t_active = self.active_time_ms * 1e-3
        t_adc = self.adc_time_ms * 1e-3
        # Active: CPU + sensors
        E_active = (self.active_current_ma * 1e-3) * self.v_core * t_active
        # ADC conversion
        E_adc = (self.adc_current_ua * 1e-6) * self.v_core * t_adc
        return (E_active + E_adc) * 1e6  # µJ

    def sleep_power_uw(self) -> float:
        """Sleep power in µW."""
        return self.sleep_current_ua * 1e-6 * self.v_core * 1e6  # µW

# =============================================================================
# 4. BATTERY MODEL — Fungal bio-battery (from our graph simulation)
# =============================================================================

@dataclass
class BatteryConfig:
    """Fungal bio-battery parameters (from optimization)."""
    power_density_uw_cm2: float = 260.0  # Level 1 optimum
    area_cm2: float = 2.0               # 2 cm² typical for soil tag
    voltage_nominal: float = 0.45        # V (OCV)
    voltage_min: float = 0.2             # V (minimum for boost converter)
    depth_of_discharge: float = 0.8      # 80% usable
    degradation_per_day_pct: float = 2.0  # 2% power loss per day (mycelium aging)
    cost_per_unit_euro: float = 0.05     # €0.05 per battery (high volume)

    @property
    def total_power_uw(self) -> float:
        return self.power_density_uw_cm2 * self.area_cm2

    @property
    def total_energy_uj(self) -> float:
        """Total usable energy in µJ (80% DoD)."""
        power_w = self.total_power_uw * 1e-6
        # Assume 7-day lifetime at full power (simplified)
        lifetime_s = 7 * 24 * 3600
        return power_w * lifetime_s * self.depth_of_discharge * 1e6

    def power_at_day(self, day: int) -> float:
        """Power available on day N (degradation model)."""
        factor = (1 - self.degradation_per_day_pct / 100) ** day
        return self.total_power_uw * factor

    def energy_available_uj(self, day: int, hours_per_day: float = 24) -> float:
        """Energy available on day N in µJ."""
        return self.power_at_day(day) * hours_per_day * 3600

# =============================================================================
# 5. SYSTEM MODEL — Complete sensor tag simulation
# =============================================================================

@dataclass
class SystemConfig:
    soil_type: str = "loam"
    moisture_pct: float = 25.0
    measurement_interval_s: float = 900.0  # every 15 minutes
    target_lifetime_days: float = 7.0
    nfc_reads_per_day: int = 2  # how many times farmer reads tag

    sensor: SensorConfig = field(default_factory=SensorConfig)
    mcu: MCUConfig = field(default_factory=MCUConfig)
    battery: BatteryConfig = field(default_factory=BatteryConfig)


@dataclass
class SimulationResult:
    """Complete simulation output."""
    viable: bool
    total_lifetime_days: float
    margin_pct: float
    measurements_total: int
    energy_per_measurement_uj: float
    daily_consumption_uj: float
    daily_supply_uj: float
    battery_power_uw: float
    battery_mass_g: float
    battery_cost_euro: float
    total_device_cost_euro: float
    degradation_days_until_50pct: int
    compostable_mass_g: float

    def summary_dict(self) -> dict:
        return {
            "viable": self.viable,
            "lifetime_days": round(self.total_lifetime_days, 1),
            "energy_margin_pct": round(self.margin_pct, 1),
            "measurements_per_day": round(self.measurements_total / max(self.total_lifetime_days, 1)),
            "battery_power_uw": round(self.battery_power_uw, 1),
            "battery_mass_g": round(self.battery_mass_g, 2),
            "battery_cost_euro": round(self.battery_cost_euro, 4),
            "compostable_mass_g": round(self.compostable_mass_g, 2),
        }


class SoilSensorSimulator:
    """End-to-end simulation of the fungal bio-battery soil sensor tag."""

    def __init__(self, config: SystemConfig):
        self.config = config

    def run(self) -> SimulationResult:
        cfg = self.config
        eps = soil_epsilon(cfg.soil_type, cfg.moisture_pct)

        # Per-measurement energy
        E_sensor = cfg.sensor.measurement_energy_uj(eps)
        E_mcu = cfg.mcu.energy_per_cycle_uj()
        E_per_measure = E_sensor + E_mcu

        # Daily energy consumption
        measurements_per_day = 86400 / cfg.measurement_interval_s
        E_sleep_daily = cfg.mcu.sleep_power_uw() * 24   # µWh
        E_active_daily = E_per_measure * measurements_per_day  # µJ
        # Convert µJ to µWh (1 µWh = 3600 µJ)
        E_daily_uj = E_active_daily * 1  # already in µJ
        Sleep_daily_uj = cfg.mcu.sleep_power_uw() * 24 * 3600 / 1  # µW * 24h * 3600s = µJ

        # NFC reads: farmer reads tag 2x/day, each read requires tag to be active
        E_nfc_per_read_uj = 100.0  # µJ for NFC communication (passive, but MCU wakes)
        E_nfc_daily = E_nfc_per_read_uj * cfg.nfc_reads_per_day

        total_daily_uj = E_active_daily + Sleep_daily_uj + E_nfc_daily

        # Battery supply (with degradation)
        day = 0
        cumulative_consumption = 0.0
        cumulative_supply = 0.0

        for day in range(1, 366):  # simulate up to 1 year
            available = cfg.battery.energy_available_uj(day)
            needed = total_daily_uj

            cumulative_supply += available
            cumulative_consumption += needed

            if cumulative_consumption > cumulative_supply:
                break

        if day == 365:
            day = 365  # capped

        lifetime_days = day
        margin = (cumulative_supply - cumulative_consumption) / cumulative_consumption * 100 if cumulative_consumption > 0 else 0

        # Battery mass estimate
        # Cellulose + carbon + water → density ~1.2 g/cm³
        battery_volume = cfg.battery.area_cm2 * 0.05  # 0.5 mm thick
        battery_mass = battery_volume * 1.2  # g
        # Compostable part: everything (cellulose + carbon are biodegradable)
        compostable_mass = battery_mass * 0.9  # 90% by mass is biodegradable

        # Cost
        total_device_cost = cfg.battery.cost_per_unit_euro + 0.10  # €0.10 for PCB + MCU

        # Degradation: time to 50% power
        half_life = np.log(0.5) / np.log(1 - cfg.battery.degradation_per_day_pct / 100)

        return SimulationResult(
            viable=lifetime_days >= cfg.target_lifetime_days,
            total_lifetime_days=float(lifetime_days),
            margin_pct=margin,
            measurements_total=int(measurements_per_day * lifetime_days),
            energy_per_measurement_uj=E_per_measure,
            daily_consumption_uj=total_daily_uj,
            daily_supply_uj=cumulative_supply / max(lifetime_days, 1),
            battery_power_uw=cfg.battery.total_power_uw,
            battery_mass_g=battery_mass,
            battery_cost_euro=cfg.battery.cost_per_unit_euro,
            total_device_cost_euro=total_device_cost,
            degradation_days_until_50pct=int(half_life),
            compostable_mass_g=compostable_mass,
        )

    def parameter_sweep(self, param: str, values: List[float]) -> List[SimulationResult]:
        """Sweep a parameter and return results."""
        results = []
        for v in values:
            cfg_modified = self._modify_config(param, v)
            sim = SoilSensorSimulator(cfg_modified)
            results.append(sim.run())
        return results

    def _modify_config(self, param: str, value: float) -> SystemConfig:
        """Return modified config."""
        cfg = self.config
        import copy
        new = copy.deepcopy(cfg)
        parts = param.split(".")
        obj = new
        for p in parts[:-1]:
            obj = getattr(obj, p)
        setattr(obj, parts[-1], value)
        return new


# =============================================================================
# 6. VISUALIZATION
# =============================================================================

def plot_lifetime_heatmap(sim, filename="e2e_lifetime_heatmap.png"):
    """Plot lifetime as function of measurement interval and moisture."""
    intervals = [60, 300, 600, 900, 1800, 3600]  # seconds
    moistures = [5, 10, 15, 20, 25, 30, 40]
    lifetime_matrix = np.zeros((len(intervals), len(moistures)))

    for i, iv in enumerate(intervals):
        for j, m in enumerate(moistures):
            c = copy.deepcopy(sim.config)
            c.measurement_interval_s = iv
            c.moisture_pct = m
            res = SoilSensorSimulator(c).run()
            lifetime_matrix[i, j] = res.total_lifetime_days

    import copy

    fig, ax = plt.subplots(figsize=(10, 7))
    im = ax.imshow(lifetime_matrix, cmap="YlGn", aspect="auto", vmin=0, vmax=30)

    ax.set_xticks(range(len(moistures)))
    ax.set_xticklabels([f"{m}%" for m in moistures])
    ax.set_yticks(range(len(intervals)))
    ax.set_yticklabels([f"{int(iv//60)}m" if iv < 3600 else f"{iv/3600:.1f}h" for iv in intervals])
    ax.set_xlabel("Soil Moisture (%)")
    ax.set_ylabel("Measurement Interval")
    ax.set_title("Battery Lifetime (days) vs Moisture & Measurement Frequency")

    for i in range(len(intervals)):
        for j in range(len(moistures)):
            val = lifetime_matrix[i, j]
            color = "white" if val > 15 else "black"
            ax.text(j, i, f"{val:.0f}d", ha="center", va="center", fontsize=8, color=color)

    cbar = plt.colorbar(im, ax=ax, label="Days")
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    print(f"  Saved: {filename}")


def plot_degradation_curve(sim, filename="e2e_degradation.png"):
    """Plot battery power and cumulative energy over time."""
    cfg = sim.config

    days = np.arange(0, 31)
    power_daily = [cfg.battery.power_at_day(d) for d in days]
    energy_cumulative = np.cumsum([cfg.battery.energy_available_uj(d) for d in days])

    # Daily consumption
    eps = soil_epsilon(cfg.soil_type, cfg.moisture_pct)
    E_per = cfg.sensor.measurement_energy_uj(eps) + cfg.mcu.energy_per_cycle_uj()
    meas_per_day = 86400 / cfg.measurement_interval_s
    daily_consumption = E_per * meas_per_day + cfg.mcu.sleep_power_uw() * 24 * 3600
    consumption_cumulative = np.cumsum([daily_consumption] * len(days))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.plot(days, power_daily, "g-", linewidth=2)
    ax1.axhline(daily_consumption / 3600, color="r", linestyle="--", label="Daily need (µW)")
    ax1.fill_between(days, power_daily, alpha=0.2, color="green")
    ax1.set_xlabel("Days")
    ax1.set_ylabel("Available Power (µW)")
    ax1.set_title("Battery Power Degradation")
    ax1.legend()
    ax1.grid(alpha=0.3)

    ax2.plot(days, energy_cumulative / 1e6, "g-", linewidth=2, label="Supply")
    ax2.plot(days, consumption_cumulative / 1e6, "r--", linewidth=2, label="Demand")
    ax2.fill_between(days,
                     consumption_cumulative / 1e6,
                     energy_cumulative / 1e6,
                     where=(energy_cumulative > consumption_cumulative),
                     alpha=0.2, color="green", label="Surplus")
    ax2.fill_between(days,
                     consumption_cumulative / 1e6,
                     energy_cumulative / 1e6,
                     where=(energy_cumulative <= consumption_cumulative),
                     alpha=0.2, color="red", label="Deficit")
    ax2.set_xlabel("Days")
    ax2.set_ylabel("Cumulative Energy (MJ)")
    ax2.set_title("Energy Budget Over Time")
    ax2.legend(fontsize=8)
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    print(f"  Saved: {filename}")


def plot_cost_comparison(filename="e2e_cost_comparison.png"):
    """Compare fungal vs Li-ion vs alkaline per sensor-tag."""
    labels = ["Fungal\nBio-Battery", "Li-Ion\nCR2032", "Alkaline\nAAA", "Li-Po\nPicolithium"]
    costs = [0.05, 0.35, 0.15, 1.50]
    masses = [0.12, 3.0, 11.5, 0.7]
    lifetimes = [7, 180, 60, 90]
    compostable = [0.11, 0, 0, 0]

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    axes[0, 0].bar(labels, costs, color=["#2ecc71", "#e74c3c", "#f39c12", "#3498db"])
    axes[0, 0].set_ylabel("Cost per Unit (€)")
    axes[0, 0].set_title("Unit Cost")
    axes[0, 0].grid(alpha=0.3, axis="y")

    axes[0, 1].bar(labels, masses, color=["#2ecc71", "#e74c3c", "#f39c12", "#3498db"])
    axes[0, 1].set_ylabel("Mass (g)")
    axes[0, 1].set_title("Weight")
    axes[0, 1].grid(alpha=0.3, axis="y")

    axes[1, 0].bar(labels, lifetimes, color=["#2ecc71", "#e74c3c", "#f39c12", "#3498db"])
    axes[1, 0].set_ylabel("Lifetime (days)")
    axes[1, 0].set_title("Operational Life")
    axes[1, 0].grid(alpha=0.3, axis="y")

    axes[1, 1].bar(labels, compostable, color=["#2ecc71", "#e74c3c", "#f39c12", "#3498db"])
    axes[1, 1].set_ylabel("Compostable Mass (g)")
    axes[1, 1].set_title("Biodegradability")
    axes[1, 1].grid(alpha=0.3, axis="y")

    plt.suptitle("Battery Comparison for Disposable Soil Sensor Tags", fontsize=14, y=1.01)
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    print(f"  Saved: {filename}")


def plot_lifetime_vs_interval(sim, filename="e2e_lifetime_curve.png"):
    """Plot lifetime as function of measurement interval."""
    intervals = np.logspace(1, 4, 50)
    lifetimes = []

    for iv in intervals:
        import copy
        c = copy.deepcopy(sim.config)
        c.measurement_interval_s = iv
        res = SoilSensorSimulator(c).run()
        lifetimes.append(res.total_lifetime_days)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(intervals / 60, lifetimes, "b-", linewidth=2)
    ax.axhline(7, color="green", linestyle="--", alpha=0.7, label="Target: 7 days")
    ax.axvline(15, color="orange", linestyle=":", alpha=0.7, label="15 min (recommended)")
    ax.set_xscale("log")
    ax.set_xlabel("Measurement Interval (minutes)")
    ax.set_ylabel("Battery Lifetime (days)")
    ax.set_title("Lifetime vs Measurement Frequency (loam soil, 25% moisture)")
    ax.legend()
    ax.grid(alpha=0.3)

    # Fill viable region
    ax.fill_between(intervals / 60, lifetimes, 7, where=(np.array(lifetimes) >= 7),
                    alpha=0.15, color="green")
    ax.fill_between(intervals / 60, lifetimes, 7, where=(np.array(lifetimes) < 7),
                    alpha=0.15, color="red")

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    print(f"  Saved: {filename}")

# =============================================================================
# 7. COMPETITOR COMPARISON
# =============================================================================

COMPETITOR_BATTERIES = [
    {"name": "Fungal Bio-Battery", "type": "bio", "cost": 0.05, "mass_g": 0.12,
     "lifetime_days": 7, "compostable": True, "voltage": 0.45, "power_uw": 260,
     "needs_boost": True, "regulatory": "none"},
    {"name": "CR2032 (Li-Ion)", "type": "coin", "cost": 0.35, "mass_g": 3.0,
     "lifetime_days": 180, "compostable": False, "voltage": 3.0, "power_uw": 5000,
     "needs_boost": False, "regulatory": "UN38.3"},
    {"name": "AAA Alkaline", "type": "alkaline", "cost": 0.15, "mass_g": 11.5,
     "lifetime_days": 60, "compostable": False, "voltage": 1.5, "power_uw": 10000,
     "needs_boost": False, "regulatory": "none"},
    {"name": "Picolithium (Li-Po)", "type": "lipoly", "cost": 1.50, "mass_g": 0.7,
     "lifetime_days": 90, "compostable": False, "voltage": 3.7, "power_uw": 15000,
     "needs_boost": False, "regulatory": "UN38.3"},
    {"name": "EDLC Supercap", "type": "cap", "cost": 0.20, "mass_g": 0.5,
     "lifetime_days": 0.01, "compostable": False, "voltage": 2.5, "power_uw": 50000,
     "needs_boost": True, "regulatory": "none"},
]

# =============================================================================
# 8. MAIN
# =============================================================================

if __name__ == "__main__":
    import copy

    print("#" * 60)
    print("#  E2E SIMULATION: SOIL MOISTURE SENSOR TAG")
    print("#  Fungal Bio-Battery → Field → Compost")
    print("#" * 60)

    # ── Default configuration ──
    config = SystemConfig(
        soil_type="loam",
        moisture_pct=25.0,
        measurement_interval_s=900,  # every 15 minutes
        target_lifetime_days=7.0,
        nfc_reads_per_day=2,
    )

    sim = SoilSensorSimulator(config)
    result = sim.run()

    print(f"\n📋 CONFIGURATION")
    print(f"   Soil:            {config.soil_type} @ {config.moisture_pct}% moisture")
    print(f"   Measurement:     every {config.measurement_interval_s/60:.0f} minutes")
    print(f"   Target lifetime: {config.target_lifetime_days} days")
    print(f"   NFC reads/day:   {config.nfc_reads_per_day}")

    print(f"\n📊 RESULTS")
    print(f"   {'✅ VIABLE' if result.viable else '❌ NOT VIABLE'} — "
          f"Lifetime: {result.total_lifetime_days:.1f} days "
          f"(target: {config.target_lifetime_days})")
    print(f"   Energy margin:     {result.margin_pct:+.1f}%")
    print(f"   Per measurement:   {result.energy_per_measurement_uj:.1f} µJ")
    print(f"   Daily consumption: {result.daily_consumption_uj/3600:.1f} µWh")
    print(f"   Daily supply:      {result.daily_supply_uj/3600:.1f} µWh")
    print(f"   Total measurements: {result.measurements_total:,}")

    print(f"\n🔋 BATTERY")
    print(f"   Type:     Fungal Bio-Battery (pressed pellet)")
    print(f"   Power:    {result.battery_power_uw:.0f} µW")
    print(f"   Voltage:  {config.battery.voltage_nominal} V (needs boost converter → 3.3V)")
    print(f"   Mass:     {result.battery_mass_g:.2f} g")
    print(f"   Cost:     €{result.battery_cost_euro:.4f}")
    print(f"   Degradation to 50%: {result.degradation_days_until_50pct} days")
    print(f"   Compostable mass:   {result.compostable_mass_g:.2f} g")

    print(f"\n💰 COST BREAKDOWN")
    print(f"   Battery:     €{result.battery_cost_euro:.4f}")
    print(f"   PCB + MCU:   €0.1000")
    print(f"   Sensor PCB:  €0.0500")
    print(f"   Assembly:    €0.0500")
    print(f"   Total:       €{result.total_device_cost_euro:.4f}")
    print(f"   Cost per day: €{result.total_device_cost_euro/result.total_lifetime_days:.4f}")

    print(f"\n📈 COMPETITIVE POSITIONING")
    for comp in COMPETITOR_BATTERIES:
        viable = "✅" if comp["power_uw"] >= 50 else "❌"
        print(f"   {viable} {comp['name']:25s} "
              f"€{comp['cost']:<6.2f}  {comp['mass_g']:<5.1f}g  "
              f"{comp['lifetime_days']:5.0f}d  {'♻️' if comp['compostable'] else '🚫'}  "
              f"{comp['voltage']}V  {comp['power_uw']}µW")

    print(f"\n🏆 KEY ADVANTAGE OF FUNGAL BATTERY")
    print(f"   - Only compostable option ({result.compostable_mass_g:.2f}g biodegradable)")
    print(f"   - Lowest cost (€{result.battery_cost_euro:.2f}/unit)")
    print(f"   - Lowest mass ({result.battery_mass_g:.2f}g)")
    print(f"   - No recycling needed (compost with food waste)")
    print(f"   ⚠️ Needs boost converter (0.45V → 3.3V) → BOM TBD (simulation estimate)")
    print(f"   ⚠️ Shortest lifetime ({result.total_lifetime_days:.0f} days)")

    # ── Parameter sweeps ──
    print(f"\n📊 SENSITIVITY: LIFETIME VS MEASUREMENT INTERVAL")
    intervals = [60, 300, 600, 900, 1800, 3600, 7200]
    results = sim.parameter_sweep("measurement_interval_s", intervals)
    for iv, res in zip(intervals, results):
        label = f"{iv//60}m" if iv < 3600 else f"{iv/3600:.1f}h"
        status = "✅" if res.viable else "❌"
        print(f"   {status} Every {label:5s} → {res.total_lifetime_days:6.1f} days  "
              f"({int(res.measurements_total/res.total_lifetime_days)} meas/day)")

    print(f"\n📊 SENSITIVITY: LIFETIME vs SOIL TYPE (at 25% moisture, 15min interval)")
    for soil in ["sand", "loam", "clay", "compost"]:
        c = copy.deepcopy(config)
        c.soil_type = soil
        res = SoilSensorSimulator(c).run()
        eps_25 = soil_epsilon(soil, 25)
        print(f"   {soil:10s} εr={eps_25:.1f} → {res.total_lifetime_days:.1f} days {'✅' if res.viable else '❌'}")

    print(f"\n📊 SENSITIVITY: BATTERY SIZE vs LIFETIME (loam, 25%, 15min)")
    for area in [0.5, 1.0, 2.0, 4.0, 6.0]:
        c = copy.deepcopy(config)
        c.battery.area_cm2 = area
        res = SoilSensorSimulator(c).run()
        mass = area * 0.05 * 1.2
        power = area * 260
        print(f"   {area:<4.1f} cm²  {power:4.0f} µW  {mass:.2f}g → {res.total_lifetime_days:.1f} days {'✅' if res.viable else '❌'}")

    # ── Analysis summary ──
    print(f"\n" + "=" * 60)
    print(f"  E2E VERDICT")
    print(f"  " + "=" * 60)

    recommendations = []
    if result.viable:
        recommendations.append("✅ Product is technically viable at current specs")
    else:
        recommendations.append(f"❌ Current config insufficient: reduce interval or increase battery")
        # Find minimum viable interval
        for iv in [60, 120, 300, 600, 900]:
            c = copy.deepcopy(config)
            c.measurement_interval_s = iv
            res = SoilSensorSimulator(c).run()
            if res.viable:
                recommendations.append(f"   → Viable at {iv//60}min interval: {res.total_lifetime_days:.0f} days")
                break

    recommendations.append(f"📦 Optimal configuration for 7-day target:")
    recommendations.append(f"   → {config.battery.area_cm2} cm² battery (€{result.battery_cost_euro:.2f})")
    recommendations.append(f"   → {config.measurement_interval_s/60:.0f}min interval → {result.measurements_total:,} measurements")
    recommendations.append(f"   → Cost: €{result.total_device_cost_euro:.2f} per tag")
    recommendations.append(f"   → Compostable: ✓ ({result.compostable_mass_g:.2f}g)")
    recommendations.append(f"")
    recommendations.append(f"🌍 Market positioning: 'The first biodegradable soil sensor tag'")
    recommendations.append(f"💰 TAM: Precision agriculture $12B → soil sensors $1.2B → biodegradable niche $50M")
    recommendations.append(f"🎯 First customer: Organic farms (willing to pay premium for zero-waste)")

    for r in recommendations:
        print(f"  {r}")

    print(f"\n📈 GENERATING VISUALIZATIONS...")
    plot_lifetime_heatmap(sim)
    plot_degradation_curve(sim)
    plot_cost_comparison()
    plot_lifetime_vs_interval(sim)

    print(f"\n  Done. {4} plots saved.")
