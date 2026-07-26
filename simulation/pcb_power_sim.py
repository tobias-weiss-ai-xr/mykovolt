#!/usr/bin/env python3
"""
PCB Power & Energy Simulation — MykoVolt Sensor Board v0.1

Models the complete power system of the sensor board:
  • Fungal MFC pressling power output (temperature/age dependent)
  • BQ25570 boost converter efficiency (load-dependent)
  • STM32L011 sleep/wake/measurement cycle
  • FDC1004 capacitive measurement energy
  • NFC readout (passive — zero draw from pressling)
  • Supercap/battery buffer for cold-start and peak loads
  • Monte Carlo on component tolerances
  • Survival probability over time

Usage:
    python3 simulation/pcb_power_sim.py                         # Default run
    python3 simulation/pcb_power_sim.py --days 30               # 30-day simulation
    python3 simulation/pcb_power_sim.py --interval 5            # 5-min measurement interval
    python3 simulation/pcb_power_sim.py --monte-carlo 5000      # 5000 MC runs
    python3 simulation/pcb_power_sim.py --conservative          # Use worst-case values
    python3 simulation/pcb_power_sim.py --no-plots              # Suppress plots
    python3 simulation/pcb_power_sim.py --json                  # JSON output only
"""

import numpy as np
import argparse
import json
import sys
import os
from dataclasses import dataclass, field
from typing import List, Tuple, Optional

# ──────────────────────────────────────────────
# Try importing matplotlib — graceful fallback
# ──────────────────────────────────────────────
try:
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

# ──────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────
MILLI = 1e-3
MICRO = 1e-6
NANO = 1e-9
HOURS_PER_DAY = 24
SECONDS_PER_HOUR = 3600
SECONDS_PER_DAY = HOURS_PER_DAY * SECONDS_PER_HOUR

# ──────────────────────────────────────────────
# Component Parameters
# ──────────────────────────────────────────────

@dataclass
class PresslingParams:
    """Fungal MFC pressling — power output model"""
    # Electrical (typical values from Empa paper, Reyes et al. 2024)
    v_ocv_typ: float = 0.45      # V, open-circuit voltage
    v_ocv_min: float = 0.30      # V, minimum (cold, old)
    v_ocv_max: float = 0.60      # V, maximum (fresh, warm)
    
    p_max_typ: float = 25.0      # µW, max power point
    p_max_min: float = 10.0      # µW, worst case
    p_max_max: float = 50.0      # µW, best case (optimistic)
    
    # Temperature dependence: Q10 ≈ 2 for fungal metabolism
    temp_opt: float = 25.0       # °C, optimal temperature
    temp_min: float = 5.0        # °C, minimum active
    temp_max: float = 40.0       # °C, maximum active
    
    # Aging: exponential decay, ~50% power after 30 days
    half_life_days: float = 45.0 # days, power halves
    
    # Internal resistance
    r_internal_typ: float = 100   # Ω, typical
    r_internal_min: float = 50    # Ω, best case
    r_internal_max: float = 300   # Ω, worst case


@dataclass
class BoostConverterParams:
    """BQ25570 boost converter parameters"""
    # Startup
    v_cold_start_min: float = 0.30  # V, minimum cold-start voltage
    v_cold_start_typ: float = 0.38  # V, typical
    v_hold: float = 0.05            # V, voltage drop after startup
    
    # Efficiency (load-dependent, from datasheet curves)
    # Efficiency at 10 µW load
    eff_10uw: float = 0.45
    # Efficiency at 50 µW load
    eff_50uw: float = 0.70
    # Efficiency at 500 µW load
    eff_500uw: float = 0.85
    
    # Quiescent current
    iq_typ: float = 80.0   # nA
    iq_max: float = 150.0  # nA
    
    # Output
    v_out: float = 3.3      # V, regulated output
    v_out_ripple: float = 0.05  # V, ripple


@dataclass
class McuParams:
    """STM32L011K4 power parameters (from datasheet)"""
    # Sleep modes
    i_stop_rtc_typ: float = 1.8   # µA, STOP with RTC
    i_stop_rtc_max: float = 2.5   # µA
    i_sleep_typ: float = 0.9      # µA, STOP without RTC
    
    # Active
    i_active_typ: float = 1.5     # mA @ 2 MHz MSI
    i_active_max: float = 2.0     # mA
    t_startup: float = 5.0        # µs, wake from STOP
    
    # Flash programming
    i_flash_write: float = 3.0    # mA
    t_flash_write_per_byte: float = 50.0  # µs/byte (approx)
    
    # GPIO drive
    i_gpio_per_pin: float = 0.5   # µA per pin, typ


@dataclass
class SensorParams:
    """FDC1004 capacitive sensor power"""
    i_active_typ: float = 650.0   # µA, during conversion
    i_active_max: float = 800.0   # µA
    t_measurement: float = 15.0   # ms, single conversion
    i_sleep: float = 1.0          # µA, sleep mode


@dataclass
class NfcParams:
    """ST25DV04K NFC tag — passive, no battery draw"""
    # NFC readout is powered by the reader's RF field
    # No current drawn from pressling during readout
    i_sleep: float = 0.5          # µA, sleep (quiescent)
    t_transfer_per_kb: float = 3.0  # ms/KB, I²C transfer to NFC EEPROM


@dataclass
class BufferParams:
    """Energy buffer (supercap + optional battery)"""
    # Supercap (main buffer)
    c_supercap: float = 100.0     # mF, typical
    c_supercap_min: float = 47.0  # mF, smallest viable
    c_supercap_max: float = 470.0 # mF, largest practical
    
    v_supercap_max: float = 3.6   # V, max voltage
    v_supercap_min: float = 2.0   # V, minimum for buck-boost to maintain 3.3V
    
    # Leakage
    i_leak_typ: float = 2.0       # µA, supercap self-discharge
    i_leak_max: float = 5.0       # µA
    
    # Optional LiPo backup (unpopulated by default)
    has_battery: bool = False
    batt_capacity: float = 50.0   # mAh, if populated


@dataclass
class SystemParams:
    """Overall system configuration"""
    measurement_interval_min: float = 15.0  # minutes between measurements
    nfc_readout_interval_min: float = 60.0  # minutes between NFC data syncs
    t_measurement: float = 150.0            # ms, total measurement burst
    
    # Load switch — controlled by MCU
    t_switch_on: float = 0.5               # ms, switch turn-on time
    t_switch_stabilize: float = 1.0        # ms, wait for rail to stabilize
    
    # Temperature profile
    temp_daily_min: float = 15.0           # °C, night soil temp
    temp_daily_max: float = 30.0           # °C, day soil temp
    temp_profile: str = 'sine'             # 'sine' or 'constant'
    
    # Monte Carlo
    mc_iterations: int = 1000              # default
    confidence_pct: float = 95.0           # percentile for bounds


# ──────────────────────────────────────────────
# Power Model Functions
# ──────────────────────────────────────────────

def pressling_power(temp: float, age_days: float, params: PresslingParams,
                    rng: Optional[np.random.Generator] = None) -> Tuple[float, float]:
    """
    Calculate pressling power output at given temperature and age.
    Returns (p_max_uw, v_ocv) — max power in µW and OCV in volts.
    """
    if rng is None:
        rng = np.random.default_rng()
    
    # Base power
    p_base = rng.triangular(params.p_max_min, params.p_max_typ, params.p_max_max)
    
    # Temperature factor: Gaussian-ish with Q10 ≈ 2
    t_diff = temp - params.temp_opt
    t_factor = np.exp(-0.5 * (t_diff / 12.0) ** 2)  # ~1 at optimum, ~0.6 at ±10°C
    t_factor = np.clip(t_factor, 0.1, 1.0)
    
    # Age factor: exponential decay
    age_factor = np.exp(-np.log(2) * age_days / params.half_life_days)
    
    p_out = p_base * t_factor * age_factor
    
    # OCV — varies with temperature and age
    v_ocv = rng.triangular(params.v_ocv_min, params.v_ocv_typ, params.v_ocv_max)
    v_ocv *= (0.8 + 0.2 * t_factor)  # lower temp → lower voltage
    
    return max(p_out, 0), max(v_ocv, 0.1)


def boost_efficiency(p_in_uw: float, params: BoostConverterParams) -> float:
    """
    BQ25570 efficiency curve based on input power.
    From datasheet: ~45% at 10µW, ~70% at 50µW, ~85% at 500µW.
    """
    if p_in_uw < 1.0:
        return 0.0  # can't boost
    
    # Interpolate from datasheet points
    p_points = np.array([5, 10, 50, 100, 500, 1000])
    eff_points = np.array([0.30, 0.45, 0.70, 0.80, 0.85, 0.82])
    
    if p_in_uw <= p_points[0]:
        return eff_points[0] * p_in_uw / p_points[0]
    elif p_in_uw >= p_points[-1]:
        return eff_points[-1]
    else:
        return float(np.interp(p_in_uw, p_points, eff_points))


def mcu_sleep_current(stop_with_rtc: bool = True, 
                       params: McuParams = None,
                       rng: Optional[np.random.Generator] = None) -> float:
    """MCU sleep current in µA."""
    if params is None:
        params = McuParams()
    if rng is None:
        rng = np.random.default_rng()
    
    if stop_with_rtc:
        return rng.uniform(params.i_stop_rtc_typ, params.i_stop_rtc_max)
    else:
        return rng.uniform(params.i_sleep_typ, params.i_sleep_typ * 1.3)


def measurement_energy(sensor_params: SensorParams = None,
                       mcu_params: McuParams = None,
                       rng: Optional[np.random.Generator] = None) -> float:
    """
    Energy consumed during one measurement burst.
    Returns energy in µWh.
    """
    if sensor_params is None:
        sensor_params = SensorParams()
    if mcu_params is None:
        mcu_params = McuParams()
    if rng is None:
        rng = np.random.default_rng()
    
    # MCU startup + wake (5 µs at 1.5 mA)
    e_startup = (mcu_params.i_active_typ * MILLI) * (mcu_params.t_startup * MICRO) / SECONDS_PER_HOUR
    
    # MCU active during measurement (150 ms at 1.5 mA)
    e_mcu_active = (mcu_params.i_active_typ * MILLI) * 150e-3 / SECONDS_PER_HOUR
    
    # Sensor active (15 ms conversion + 10 ms settling = 25 ms at 650 µA)
    e_sensor = (sensor_params.i_active_typ * MICRO) * 25e-3 / SECONDS_PER_HOUR
    
    # FRAM write (16 bytes, 50 µs/byte at 3 mA)
    t_fram_write = 16 * 50e-6  # seconds
    e_fram = (3.0 * MILLI) * t_fram_write / SECONDS_PER_HOUR
    
    # I²C transfer to NFC (if syncing — 256 bytes at 100 kHz)
    t_i2c = 256 * 10e-6  # 10 µs per byte at 100 kHz I²C
    e_nfc_copy = (2.0 * MILLI) * t_i2c / SECONDS_PER_HOUR
    
    total_wh = e_startup + e_mcu_active + e_sensor + e_fram + e_nfc_copy
    return total_wh * 1e6  # convert to µWh


def standby_power(buffer_params: BufferParams = None) -> float:
    """Standby power (always-on components) in µW."""
    if buffer_params is None:
        buffer_params = BufferParams()
    
    # BQ25570 quiescent: 80 nA at 3.3V = 0.26 µW
    # PCF8523 RTC: 150 nA at 3.3V = 0.50 µW
    # Supercap leakage: 2 µA at 3.3V = 6.6 µW
    
    p_bq = BoostConverterParams.iq_typ * NANO * 3.3  # W
    p_rtc = 150e-9 * 3.3  # W
    p_leak = buffer_params.i_leak_typ * MICRO * 3.3  # W
    
    return (p_bq + p_rtc + p_leak) * 1e6  # µW


# ──────────────────────────────────────────────
# Simulation Engine
# ──────────────────────────────────────────────

@dataclass
class SimulationResult:
    """Results from one simulation run."""
    days: np.ndarray          # time in days
    p_pressling_uw: np.ndarray  # pressling power in µW
    p_available_uw: np.ndarray  # power after boost conversion in µW
    p_consumed_uw: np.ndarray   # power consumed by board in µW
    v_supercap: np.ndarray      # supercap voltage
    energy_balance_uw: np.ndarray  # cumulative energy balance in µWh
    survived: bool              # did the board survive the full period?
    failure_day: float          # day of failure (if any)
    avg_power_uw: float         # average power consumption
    min_supercap_v: float       # minimum supercap voltage reached


def run_simulation(days: float = 7.0,
                   interval_min: float = 15.0,
                   temp_profile: str = 'sine',
                   conservative: bool = False,
                   mc_run: int = 0,
                   rng: Optional[np.random.Generator] = None) -> SimulationResult:
    """
    Run one power simulation.
    
    Returns SimulationResult with time-series data.
    """
    if rng is None:
        rng = np.random.default_rng(mc_run)
    
    # Parameters (use conservative bounds if requested)
    pressling = PresslingParams()
    boost = BoostConverterParams()
    mcu = McuParams()
    sensor = SensorParams()
    nfc = NfcParams()
    buffer = BufferParams()
    system = SystemParams()
    system.measurement_interval_min = interval_min
    system.temp_profile = temp_profile
    
    if conservative:
        pressling.p_max_typ = pressling.p_max_min
        pressling.v_ocv_typ = pressling.v_ocv_min
        pressling.half_life_days = 30.0
        boost.iq_typ = boost.iq_max
        mcu.i_stop_rtc_typ = mcu.i_stop_rtc_max
        sensor.i_active_typ = sensor.i_active_max
        buffer.i_leak_typ = buffer.i_leak_max
        buffer.c_supercap = buffer.c_supercap_min
    
    # Time steps: 1 minute resolution
    dt_min = 1.0
    n_steps = int(days * HOURS_PER_DAY * 60 / dt_min)
    dt = dt_min / 60.0  # hours per step
    dt_days = dt / HOURS_PER_DAY
    
    # Arrays
    t_hours = np.arange(n_steps) * dt
    t_days = t_hours / HOURS_PER_DAY
    
    p_pressling = np.zeros(n_steps)
    p_available = np.zeros(n_steps)
    p_consumed = np.zeros(n_steps)
    v_supercap = np.full(n_steps, buffer.v_supercap_max)
    energy_balance = np.zeros(n_steps)  # cumulative µWh
    
    # State: track supercap energy explicitly
    cap_c_farads = buffer.c_supercap * MILLI  # mF → F
    v_max = buffer.v_supercap_max
    v_min = buffer.v_supercap_min
    e_full_wh = 0.5 * cap_c_farads * (v_max**2 - v_min**2) / SECONDS_PER_HOUR  # Wh
    e_full_uwh = e_full_wh * 1e6  # µWh
    
    e_sc_uwh = e_full_uwh  # µWh, usable energy stored in supercap
    cum_balance = 0.0  # µWh, cumulative net energy
    v_sc = v_max
    deficit_minutes = 0  # consecutive minutes of deficit when supercap empty
    
    # Measurement schedule
    measured_this_interval = False
    steps_since_measurement = 0
    measurement_step_interval = int(interval_min / dt_min)
    
    for i in range(n_steps):
        # Current temperature
        if temp_profile == 'sine':
            temp = system.temp_daily_min + (system.temp_daily_max - system.temp_daily_min) * \
                   0.5 * (1 + np.sin(2 * np.pi * t_hours[i] / 24.0 - np.pi/2))
        else:
            temp = (system.temp_daily_min + system.temp_daily_max) / 2.0
        
        # Age in days
        age = t_days[i]
        
        # Pressling power
        p_pw, v_ocv = pressling_power(temp, age, pressling, rng)
        p_pressling[i] = p_pw
        
        # Boost converter efficiency
        eff = boost_efficiency(p_pw, boost)
        p_avail = p_pw * eff
        p_available[i] = p_avail
        
        # Standby power (always-on RTC + BQ + leakage)
        p_standby = standby_power(buffer)
        
        # Measurement burst?
        doing_measurement = False
        p_burst = 0.0
        if i % measurement_step_interval == 0 and i > 0:
            doing_measurement = True
            # Energy for one measurement burst (µWh), convert to average power over this step
            e_meas_uwh = measurement_energy(sensor, mcu, rng)
            p_burst = e_meas_uwh / (dt_min / 60.0)  # µW averaged over the step
        
        # Load switch: power domains enabled during measurement
        if doing_measurement:
            # Peripherals powered (FRAM, NFC, Sensor) — add ~2 µA leakage
            p_consumed[i] = p_standby + p_burst + 2.0 * 3.3  # µW
        else:
            # Only always-on domain
            p_consumed[i] = p_standby
        
        # Energy balance
        p_net = p_avail - p_consumed[i]  # µW
        e_step_uwh = p_net * dt  # µWh over this step
        cum_balance += e_step_uwh
        energy_balance[i] = cum_balance
        
        # Supercap energy tracking (true state-of-charge)
        e_sc_uwh += e_step_uwh  # add net energy to supercap
        e_sc_uwh = np.clip(e_sc_uwh, 0, e_full_uwh)  # cannot go below 0 or above full
        
        # Voltage from energy content: E = 0.5*C*(V² - Vmin²)
        # V = sqrt(Vmin² + 2*E/C)
        if e_sc_uwh > 0:
            v_sc = np.sqrt(v_min**2 + 2 * e_sc_uwh * 1e-6 * SECONDS_PER_HOUR / cap_c_farads)
            v_sc = min(v_sc, v_max)
        else:
            v_sc = v_min  # exactly at minimum
        v_supercap[i] = v_sc
        
        # Check for brown-out
        if e_sc_uwh <= 0 and p_net < 0:
            deficit_minutes += 1
            # Need 60+ consecutive minutes of deficit to confirm failure
            # (avoids false positives from brief measurement peaks)
            if deficit_minutes >= 60:
                return SimulationResult(
                    days=t_days[:i+1],
                    p_pressling_uw=p_pressling[:i+1],
                    p_available_uw=p_available[:i+1],
                    p_consumed_uw=p_consumed[:i+1],
                    v_supercap=v_supercap[:i+1],
                    energy_balance_uw=energy_balance[:i+1],
                    survived=False,
                    failure_day=t_days[i],
                    avg_power_uw=np.mean(p_consumed[:i+1]),
                    min_supercap_v=np.min(v_supercap[:i+1])
                )
        else:
            deficit_minutes = 0
    
    return SimulationResult(
        days=t_days,
        p_pressling_uw=p_pressling,
        p_available_uw=p_available,
        p_consumed_uw=p_consumed,
        v_supercap=v_supercap,
        energy_balance_uw=energy_balance,
        survived=True,
        failure_day=999.0,
        avg_power_uw=np.mean(p_consumed),
        min_supercap_v=np.min(v_supercap)
    )


# ──────────────────────────────────────────────
# Monte Carlo Ensemble
# ──────────────────────────────────────────────

@dataclass
class MonteCarloResult:
    survival_rate: float                    # fraction of runs that survived
    mean_survival_days: float               # mean days before failure (or full period)
    median_survival_days: float
    p10_survival_days: float                # 10th percentile
    p90_survival_days: float                # 90th percentile
    avg_power_uw_mean: float
    avg_power_uw_std: float
    avg_power_uw_p10: float
    avg_power_uw_p90: float
    min_supercap_v_mean: float
    min_supercap_v_p10: float
    failures_by_day: np.ndarray             # histogram of failure times
    failure_bins: np.ndarray
    n_runs: int


def run_monte_carlo(n_runs: int = 1000,
                    days: float = 7.0,
                    interval_min: float = 15.0,
                    temp_profile: str = 'sine',
                    conservative: bool = False,
                    seed: int = 42) -> MonteCarloResult:
    """Run Monte Carlo ensemble of PCB power simulations."""
    
    rng = np.random.default_rng(seed)
    results = []
    
    for run in range(n_runs):
        result = run_simulation(
            days=days,
            interval_min=interval_min,
            temp_profile=temp_profile,
            conservative=conservative,
            mc_run=run,
            rng=rng
        )
        results.append(result)
    
    survived = np.array([r.survived for r in results])
    survival_days = np.array([r.failure_day if not r.survived else days for r in results])
    avg_power = np.array([r.avg_power_uw for r in results])
    min_v = np.array([r.min_supercap_v for r in results])
    
    # Failure histogram
    if not conservative:
        n_bins = min(50, days * 2)
    else:
        n_bins = min(50, days * 4)
    fail_times = survival_days[~survived]
    hist, bins = np.histogram(fail_times if len(fail_times) > 0 else [days], 
                               bins=int(n_bins), range=(0, days))
    
    return MonteCarloResult(
        survival_rate=float(np.mean(survived)),
        mean_survival_days=float(np.mean(survival_days)),
        median_survival_days=float(np.median(survival_days)),
        p10_survival_days=float(np.percentile(survival_days, 10)),
        p90_survival_days=float(np.percentile(survival_days, 90)),
        avg_power_uw_mean=float(np.mean(avg_power)),
        avg_power_uw_std=float(np.std(avg_power)),
        avg_power_uw_p10=float(np.percentile(avg_power, 10)),
        avg_power_uw_p90=float(np.percentile(avg_power, 90)),
        min_supercap_v_mean=float(np.mean(min_v)),
        min_supercap_v_p10=float(np.percentile(min_v, 10)),
        min_supercap_v_p90=float(np.percentile(min_v, 90)),
        failures_by_day=hist,
        failure_bins=bins,
        n_runs=n_runs
    )


# ──────────────────────────────────────────────
# Plotting
# ──────────────────────────────────────────────

def plot_single_run(result: SimulationResult, title: str = ""):
    """Plot time-series for a single simulation run."""
    if not HAS_MPL:
        return
    
    fig, axes = plt.subplots(4, 1, figsize=(10, 10), sharex=True)
    
    ax1, ax2, ax3, ax4 = axes
    
    # Power
    ax1.plot(result.days, result.p_pressling_uw, label='Pressling output', color='#2D6A4F', linewidth=1)
    ax1.plot(result.days, result.p_available_uw, label='After BQ25570 boost', color='#1565C0', linewidth=1)
    ax1.plot(result.days, result.p_consumed_uw, label='Board consumption', color='#E65100', linewidth=1)
    ax1.set_ylabel('Power (µW)')
    ax1.set_title(f'PCB Power Simulation {"— " + title if title else ""}')
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)
    
    # Cumulative energy
    ax2.plot(result.days, result.energy_balance_uw, color='#1B4332', linewidth=1.5)
    ax2.axhline(y=0, color='red', linestyle='--', alpha=0.3)
    ax2.set_ylabel('Cumulative Energy (µWh)')
    ax2.grid(True, alpha=0.3)
    ax2.fill_between(result.days, 0, result.energy_balance_uw, 
                     where=(result.energy_balance_uw >= 0), color='green', alpha=0.1)
    ax2.fill_between(result.days, 0, result.energy_balance_uw,
                     where=(result.energy_balance_uw < 0), color='red', alpha=0.1)
    
    # Supercap voltage
    ax3.plot(result.days, result.v_supercap, color='#6A1B9A', linewidth=1.5)
    ax3.axhline(y=2.0, color='red', linestyle=':', alpha=0.5, label='Brown-out threshold')
    ax3.set_ylabel('Supercap Voltage (V)')
    ax3.set_ylim(1.5, 3.8)
    ax3.legend(fontsize=8)
    ax3.grid(True, alpha=0.3)
    
    # Survival indicator
    ax4.set_xlabel('Time (days)')
    ax4.set_ylabel('Status')
    status = [1.0 if r.survived else 0.0 for r in [result]]
    colors = ['green' if result.survived else 'red']
    ax4.bar(0, 1, color=colors[0], alpha=0.6, width=result.days[-1] * 0.1)
    ax4.set_ylim(0, 2)
    ax4.set_yticks([])
    ax4.text(result.days[-1] * 0.3, 1.0, 
             f"SURVIVED ({result.days[-1]:.1f} days)" if result.survived 
             else f"FAILED day {result.failure_day:.2f}", 
             fontsize=12, fontweight='bold', 
             color=colors[0])
    ax4.grid(False)
    
    # Stats box
    stats_text = (
        f"Avg power: {result.avg_power_uw:.2f} µW\n"
        f"Min supercap: {result.min_supercap_v:.3f} V\n"
        f"Pressling: {np.mean(result.p_pressling_uw):.1f} µW → "
        f"{np.mean(result.p_available_uw):.1f} µW after boost"
    )
    ax4.text(result.days[-1] * 0.6, 0.3, stats_text, fontsize=9,
             bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    return fig


def plot_monte_carlo(mc_result: MonteCarloResult, days: float):
    """Plot Monte Carlo results."""
    if not HAS_MPL:
        return
    
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    
    ax1, ax2, ax3 = axes
    
    # Survival rate
    ax1.bar(['Survived', 'Failed'], 
            [mc_result.survival_rate * mc_result.n_runs, 
             (1 - mc_result.survival_rate) * mc_result.n_runs],
            color=['#2D6A4F', '#E65100'], alpha=0.7)
    ax1.set_ylabel('Runs')
    ax1.set_title(f'Survival Rate: {mc_result.survival_rate*100:.1f}% (n={mc_result.n_runs})')
    for i, v in enumerate([mc_result.survival_rate * mc_result.n_runs, 
                           (1 - mc_result.survival_rate) * mc_result.n_runs]):
        ax1.text(i, v + 5, f'{v:.0f}', ha='center', fontsize=10)
    
    # Failure histogram
    if np.sum(mc_result.failures_by_day) > 0:
        ax2.bar(mc_result.failure_bins[:-1], mc_result.failures_by_day, 
                width=mc_result.failure_bins[1] - mc_result.failure_bins[0],
                color='#E65100', alpha=0.6)
        ax2.set_xlabel('Days to failure')
        ax2.set_ylabel('Count')
        ax2.set_title(f'Failure Distribution (median: {mc_result.median_survival_days:.1f}d, '
                      f'P10: {mc_result.p10_survival_days:.1f}d)')
    else:
        ax2.text(0.5, 0.5, 'No failures in any run', 
                ha='center', va='center', transform=ax2.transAxes, fontsize=11)
        ax2.set_title('Failure Distribution')
    
    # Power statistics
    power_stats = [
        ('Mean', mc_result.avg_power_uw_mean),
        ('P10', mc_result.avg_power_uw_p10),
        ('P90', mc_result.avg_power_uw_p90),
    ]
    labels, values = zip(*power_stats)
    ax3.bar(labels, values, color=['#1565C0', '#90CAF9', '#0D47A1'], alpha=0.7)
    ax3.set_ylabel('Average Power (µW)')
    ax3.set_title(f'Power Consumption (±{mc_result.avg_power_uw_std:.2f} µW std)')
    for i, v in enumerate(values):
        ax3.text(i, v + 0.1, f'{v:.2f} µW', ha='center', fontsize=9)
    
    # Extra stats as text
    fig.suptitle(f'PCB Power Monte Carlo — {days:.0f}-day Simulation', fontsize=13, fontweight='bold')
    
    plt.tight_layout()
    return fig


def plot_interval_sweep(intervals: List[float], survival_rates: List[float], 
                         avg_powers: List[float]):
    """Plot measurement interval sweep."""
    if not HAS_MPL:
        return
    
    fig, ax1 = plt.subplots(figsize=(8, 5))
    
    color1 = '#2D6A4F'
    color2 = '#E65100'
    
    ax1.plot(intervals, survival_rates, 'o-', color=color1, linewidth=2, markersize=8)
    ax1.set_xlabel('Measurement Interval (minutes)')
    ax1.set_ylabel('Survival Rate', color=color1)
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.set_ylim(-0.05, 1.05)
    ax1.grid(True, alpha=0.3)
    
    ax2 = ax1.twinx()
    ax2.plot(intervals, avg_powers, 's--', color=color2, linewidth=2, markersize=8)
    ax2.set_ylabel('Average Power (µW)', color=color2)
    ax2.tick_params(axis='y', labelcolor=color2)
    
    # Annotate
    for i, (x, y_s, y_p) in enumerate(zip(intervals, survival_rates, avg_powers)):
        ax1.annotate(f'{y_s*100:.0f}%', (x, y_s), textcoords="offset points", 
                    xytext=(0, 10), ha='center', fontsize=9, color=color1)
        ax2.annotate(f'{y_p:.1f} µW', (x, y_p), textcoords="offset points",
                    xytext=(0, -15), ha='center', fontsize=9, color=color2)
    
    plt.title('Interval Sweep: Survival Rate vs Average Power')
    plt.tight_layout()
    return fig


# ──────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='PCB Power & Energy Simulation')
    parser.add_argument('--days', type=float, default=7.0,
                       help='Simulation duration in days (default: 7)')
    parser.add_argument('--interval', type=float, default=15.0,
                       help='Measurement interval in minutes (default: 15)')
    parser.add_argument('--temp-profile', choices=['sine', 'constant'], default='sine',
                       help='Temperature profile (default: sine)')
    parser.add_argument('--conservative', action='store_true',
                       help='Use worst-case values')
    parser.add_argument('--monte-carlo', type=int, default=1000,
                       help='Monte Carlo iterations (default: 1000, 0 = single run)')
    parser.add_argument('--interval-sweep', action='store_true',
                       help='Sweep measurement intervals and show survival rates')
    parser.add_argument('--no-plots', action='store_true',
                       help='Suppress plots')
    parser.add_argument('--json', action='store_true',
                       help='Output JSON only')
    parser.add_argument('--seed', type=int, default=42,
                       help='Random seed (default: 42)')
    
    args = parser.parse_args()
    
    show_plots = HAS_MPL and not args.no_plots and not args.json
    
    # ── Single run ──
    if args.monte_carlo == 0:
        result = run_simulation(
            days=args.days,
            interval_min=args.interval,
            temp_profile=args.temp_profile,
            conservative=args.conservative,
            mc_run=0
        )
        
        if args.json:
            print(json.dumps({
                'mode': 'single',
                'survived': result.survived,
                'failure_day': result.failure_day,
                'avg_power_uw': result.avg_power_uw,
                'min_supercap_v': result.min_supercap_v,
                'pressling_avg_uw': float(np.mean(result.p_pressling_uw)),
                'available_avg_uw': float(np.mean(result.p_available_uw)),
                'consumed_avg_uw': float(np.mean(result.p_consumed_uw)),
                'final_energy_balance_uw': float(result.energy_balance_uw[-1]),
                'n_steps': len(result.days)
            }, indent=2))
            return
        
        if show_plots:
            fig = plot_single_run(result, f'{args.days:.0f}d @ {args.interval:.0f}min')
            plt.show()
        
        print(f"\n{'='*60}")
        print(f"PCB POWER SIMULATION — Single Run")
        print(f"{'='*60}")
        print(f"  Duration:       {args.days:.0f} days @ {args.interval:.0f}min interval")
        print(f"  Temperature:    {args.temp_profile} profile")
        print(f"  Mode:           {'CONSERVATIVE' if args.conservative else 'TYPICAL'}")
        print(f"")
        print(f"  Pressling avg:  {np.mean(result.p_pressling_uw):.1f} µW")
        print(f"  After boost:    {np.mean(result.p_available_uw):.1f} µW")
        print(f"  Consumption:    {result.avg_power_uw:.2f} µW")
        print(f"  Energy margin:  {result.avg_power_uw / max(np.mean(result.p_available_uw), 0.001)*100:.1f}%")
        print(f"")
        print(f"  Status:         {'✅ SURVIVED' if result.survived else '❌ FAILED'}")
        print(f"  Failure day:    {result.failure_day:.2f}" if not result.survived else "")
        print(f"  Min supercap:   {result.min_supercap_v:.3f} V")
        print(f"  Final energy:   {result.energy_balance_uw[-1]:.1f} µWh")
        print(f"{'='*60}\n")
        return
    
    # ── Monte Carlo ──
    mc_result = run_monte_carlo(
        n_runs=args.monte_carlo,
        days=args.days,
        interval_min=args.interval,
        temp_profile=args.temp_profile,
        conservative=args.conservative,
        seed=args.seed
    )
    
    if args.json:
        print(json.dumps({
            'mode': 'monte_carlo',
            'n_runs': mc_result.n_runs,
            'days': args.days,
            'interval_min': args.interval,
            'conservative': args.conservative,
            'survival_rate': mc_result.survival_rate,
            'mean_survival_days': mc_result.mean_survival_days,
            'median_survival_days': mc_result.median_survival_days,
            'p10_survival_days': mc_result.p10_survival_days,
            'p90_survival_days': mc_result.p90_survival_days,
            'avg_power_uw': {
                'mean': mc_result.avg_power_uw_mean,
                'std': mc_result.avg_power_uw_std,
                'p10': mc_result.avg_power_uw_p10,
                'p90': mc_result.avg_power_uw_p90
            },
            'min_supercap_v': {
                'mean': mc_result.min_supercap_v_mean,
                'p10': mc_result.min_supercap_v_p10,
                'p90': mc_result.min_supercap_v_p90
            }
        }, indent=2))
        return
    
    # Print results
    print(f"\n{'='*60}")
    print(f"PCB POWER MONTE CARLO — {mc_result.n_runs} runs")
    print(f"{'='*60}")
    print(f"  Duration:       {args.days:.0f} days @ {args.interval:.0f}min interval")
    print(f"  Temperature:    {args.temp_profile} profile")
    print(f"  Mode:           {'CONSERVATIVE' if args.conservative else 'TYPICAL'}")
    print(f"")
    print(f"  ✅ Survival rate: {mc_result.survival_rate*100:.1f}%")
    print(f"  Mean survival:  {mc_result.mean_survival_days:.1f} days")
    print(f"  Median:         {mc_result.median_survival_days:.1f} days")
    print(f"  P10 / P90:      {mc_result.p10_survival_days:.1f} / {mc_result.p90_survival_days:.1f} days")
    print(f"")
    print(f"  Power consumption:")
    print(f"    Mean ± std:   {mc_result.avg_power_uw_mean:.2f} ± {mc_result.avg_power_uw_std:.2f} µW")
    print(f"    P10 / P90:    {mc_result.avg_power_uw_p10:.2f} / {mc_result.avg_power_uw_p90:.2f} µW")
    print(f"")
    print(f"  Supercap voltage:")
    print(f"    Min mean:     {mc_result.min_supercap_v_mean:.3f} V")
    print(f"    P10 / P90:    {mc_result.min_supercap_v_p10:.3f} / {mc_result.min_supercap_v_p90:.3f} V")
    print(f"{'='*60}\n")
    
    if show_plots:
        fig1 = plot_monte_carlo(mc_result, args.days)
        plt.show()
    
    # ── Interval sweep ──
    if args.interval_sweep:
        intervals = [1, 2, 5, 10, 15, 30, 60, 120]
        survival_rates = []
        avg_powers = []
        
        print(f"\n  Interval Sweep ({args.days:.0f} days, {args.monte_carlo} runs each):")
        print(f"  {'Interval':>10} {'Survival':>10} {'Avg Power':>10}")
        print(f"  {'─'*10} {'─'*10} {'─'*10}")
        
        for interval in intervals:
            sweep_mc = run_monte_carlo(
                n_runs=max(200, args.monte_carlo // 5),
                days=args.days,
                interval_min=interval,
                temp_profile=args.temp_profile,
                conservative=args.conservative,
                seed=args.seed + int(interval)
            )
            survival_rates.append(sweep_mc.survival_rate)
            avg_powers.append(sweep_mc.avg_power_uw_mean)
            print(f"  {interval:>5}min   {sweep_mc.survival_rate*100:>7.1f}%   {sweep_mc.avg_power_uw_mean:>8.2f} µW")
        
        if show_plots:
            fig2 = plot_interval_sweep(intervals, survival_rates, avg_powers)
            plt.show()


if __name__ == '__main__':
    main()
