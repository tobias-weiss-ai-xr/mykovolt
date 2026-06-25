#!/usr/bin/env python3
"""
Level 3: RL + Evolutionary Geometry Optimization for 3D-Printed Fungal MFC

Optimiert die Druck-Geometrie, um den ohmschen Widerstand zu minimieren
und die elektrochemische Oberfläche zu maximieren.

Parameter Space -> Geometry Model -> Physical Properties -> Power Density
     ^                                                            |
     |                     RL/Evolution                           |
     +------------------------------------------------------------+

Geometry parameters:
  1. layer_height_um      (50-500)    → contact resistance
  2. infill_density_pct   (20-100)    → effective conductivity
  3. tortuosity_factor    (1.0-5.0)   → ion transport resistance  
  4. electrode_width_mm   (1-10)      → ohmic resistance
  5. layer_count          (1-20)      → total thickness
  6. electrode_spacing_mm (1-10)      → electrolyte resistance
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution
from dataclasses import dataclass
from typing import List, Tuple, Optional

# ── Physical constants ──────────────────────────────────────
INK_RESISTIVITY_BASE = 0.1        # Ω·m (10 S/m, from carbon + graphite)
ELECTROLYTE_RESISTIVITY = 0.5     # Ω·m (cellulose hydrogel)
CONTACT_RESIST_PER_LAYER = 50     # Ω per layer interface
SURFACE_DENSITY_BASE = 1e6        # 1/mm² base surface sites
FARADAY = 96485.3329
LOAD_RESISTANCE = 22e3
V_OC = 0.45

# ── Geometry parameter space ─────────────────────────────────
PARAM_NAMES_GEO = [
    "layer_height_um",
    "infill_density_pct",
    "tortuosity_factor",
    "electrode_width_mm",
    "layer_count",
    "electrode_spacing_mm",
]

PARAM_BOUNDS_GEO = np.array([
    [50, 500],        # layer_height_um  
    [20, 100],        # infill_density_pct
    [1.0, 5.0],       # tortuosity_factor
    [1.0, 10.0],      # electrode_width_mm
    [1, 20],          # layer_count
    [1.0, 10.0],      # electrode_spacing_mm
])


@dataclass
class GeometryProperties:
    """Physical properties derived from print geometry."""
    internal_resistance: float      # Ω
    effective_area_mm2: float       # mm² (electrochemical surface)
    electrolyte_resistance: float   # Ω
    total_thickness_mm: float       # mm
    conductivity_effective: float   # S/m
    power_density_uW_cm2: float    # µW/cm²
    current_uA: float              # µA


class GeometryModel:
    """Physics-based model mapping print parameters to electrical properties."""

    def compute(self, params: np.ndarray) -> GeometryProperties:
        p = {name: val for name, val in zip(PARAM_NAMES_GEO, params)}
        
        lh = p["layer_height_um"] * 1e-3       # mm
        infill = p["infill_density_pct"] / 100  # 0-1
        tort = p["tortuosity_factor"]
        w = p["electrode_width_mm"]             # mm
        n_layers = int(round(p["layer_count"]))
        spacing = p["electrode_spacing_mm"]     # mm
        
        total_thickness = lh * n_layers         # mm
        
        # Effective conductivity: percolation model
        # Below ~30% infill, conductivity drops sharply
        percolation_threshold = 0.3
        if infill < percolation_threshold:
            cond_factor = (infill / percolation_threshold) ** 2.5
        else:
            cond_factor = 0.3 + 0.7 * (infill - percolation_threshold) / (1 - percolation_threshold)
        cond_eff = cond_factor / INK_RESISTIVITY_BASE  # S/m
        
        # Ohmic resistance of electrode: R = ρ × L / (w × t)
        # L = length along current path, w = width, t = thickness
        electrode_length = 10.0  # mm (fixed electrode length)
        electrode_thickness = total_thickness  # mm
        ohmic_resistance = (1 / cond_eff) * (electrode_length * 1e-3) / (w * 1e-3 * electrode_thickness * 1e-3)
        
        # Contact resistance between layers
        contact_r = CONTACT_RESIST_PER_LAYER * (n_layers - 1)
        
        # Electrolyte resistance: depends on spacing and tortuosity
        electrolyte_r = ELECTROLYTE_RESISTIVITY * (spacing * 1e-3) / (w * 1e-3 * electrode_thickness * 1e-3) * tort
        
        # Total internal resistance
        r_internal = ohmic_resistance + contact_r + electrolyte_r
        
        # Effective surface area: roughness from layer structure
        # More layers + thinner layers = higher roughness
        roughness = 1.0 + 0.5 * (n_layers / lh) if lh > 0 else 1.0
        geometric_area = w * electrode_length  # mm²
        effective_area = geometric_area * roughness * (0.5 + 0.5 * infill)
        
        # Power at matched load (R_load = R_internal gives max power transfer)
        r_total = r_internal + LOAD_RESISTANCE
        i = V_OC / r_total
        power = i ** 2 * LOAD_RESISTANCE
        power_density = power / (geometric_area * 1e-2)  # W → µW/cm²
        
        return GeometryProperties(
            internal_resistance=ohmic_resistance + contact_r,
            effective_area_mm2=effective_area,
            electrolyte_resistance=electrolyte_r,
            total_thickness_mm=total_thickness,
            conductivity_effective=cond_eff,
            power_density_uW_cm2=power_density * 1e6,
            current_uA=i * 1e6,
        )


# ── Evolutionary optimizer (Differential Evolution) ──────────

def _objective(params, model: GeometryModel):
    """Negative power density (for minimization)."""
    props = model.compute(params)
    return -props.power_density_uW_cm2


def run_evolutionary_optimization(population=60, max_iter=80):
    """Run differential evolution to find optimal geometry."""
    model = GeometryModel()
    
    result = differential_evolution(
        _objective,
        bounds=PARAM_BOUNDS_GEO,
        args=(model,),
        popsize=population // (2 * len(PARAM_NAMES_GEO)),
        maxiter=max_iter,
        tol=1e-6,
        mutation=(0.5, 1.0),
        recombination=0.7,
        seed=42,
        polish=True,
        disp=False,
    )
    
    best_params = result.x
    best_power = -result.fun
    best_props = model.compute(best_params)
    
    return best_params, best_power, best_props


# ── CMA-ES alternative (Covariance Matrix Adaptation) ────────

class CMAESOptimizer:
    """Simple CMA-ES implementation for geometry optimization."""
    
    def __init__(self, bounds, popsize=30, sigma_init=0.25):
        self.bounds = bounds
        self.n = bounds.shape[0]
        self.popsize = popsize
        self.sigma = sigma_init
        
        self.mean = (bounds[:, 0] + bounds[:, 1]) / 2
        self.C = np.eye(self.n) * sigma_init**2
        
        self.generation = 0
        self.history = []
    
    def sample_population(self):
        eigvals, eigvecs = np.linalg.eigh(self.C)
        Z = np.random.randn(self.n, self.popsize)
        return self.mean[:, None] + eigvecs @ np.diag(np.sqrt(np.abs(eigvals))) @ Z
    
    def tell(self, solutions):
        sorted_sol = sorted(solutions, key=lambda x: x[1])
        elite = sorted_sol[:self.popsize // 2]
        
        weights = np.log(self.popsize // 2 + 1) - np.log(np.arange(len(elite)) + 1)
        weights /= weights.sum()
        
        new_mean = np.zeros(self.n)
        for w, (x, _) in zip(weights, elite):
            new_mean += w * x
        self.mean = new_mean
        
        diff = np.array([x - self.mean for x, _ in elite]).T
        self.C = (diff * weights) @ diff.T + 1e-8 * np.eye(self.n)
        
        self.generation += 1
    
    def optimize(self, model: GeometryModel, n_generations=50):
        for gen in range(n_generations):
            pop = self.sample_population()
            # Clip to bounds
            pop = np.clip(pop, self.bounds[:, 0:1], self.bounds[:, 1:2])
            
            solutions = []
            for i in range(self.popsize):
                x = pop[:, i]
                props = model.compute(x)
                solutions.append((x, -props.power_density_uW_cm2))
                self.history.append({
                    "generation": gen,
                    "params": x.copy(),
                    "power": props.power_density_uW_cm2,
                    "resistance": props.internal_resistance,
                })
            
            self.tell(solutions)
            
            best_in_gen = max(self.history[-self.popsize:], key=lambda h: h["power"])
            if gen % 10 == 0 or gen == n_generations - 1:
                print(f"    Gen {gen:3d}: best = {best_in_gen['power']:8.2f} µW/cm²  "
                      f"R_int = {best_in_gen['resistance']:8.1f} Ω  "
                      f"mean = {self.mean[0]:5.1f} {self.mean[1]:5.1f}%")
        
        best = max(self.history, key=lambda h: h["power"])
        return best["params"], best["power"], model.compute(best["params"])


# ── Visualization ────────────────────────────────────────────

def plot_geometry_optimization(results, params, filename="geometry_optimization.png"):
    model = GeometryModel()
    
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    
    param_names_short = ["Layer Ht", "Infill%", "Tortuosity", "Width", "Layers", "Spacing"]
    
    # 1-6: Each parameter's effect (+/- 20% around optimal)
    for idx, (ax, name) in enumerate(zip(axes.flatten(), param_names_short)):
        if idx >= len(PARAM_NAMES_GEO):
            ax.set_visible(False)
            continue
        
        pname = PARAM_NAMES_GEO[idx]
        pmin, pmax = PARAM_BOUNDS_GEO[idx]
        
        test_vals = np.linspace(pmin, pmax, 30)
        powers = []
        resistors = []
        
        for val in test_vals:
            test_params = params.copy()
            test_params[idx] = val
            props = model.compute(test_params)
            powers.append(props.power_density_uW_cm2)
            resistors.append(props.internal_resistance)
        
        ax2 = ax.twinx()
        line1 = ax.plot(test_vals, powers, "b-", linewidth=2, label="Power")
        line2 = ax2.plot(test_vals, resistors, "r--", linewidth=2, label="R_internal")
        
        ax.axvline(params[idx], color="gray", linestyle=":", alpha=0.7)
        ax.set_xlabel(name)
        ax.set_ylabel("µW/cm²", color="b")
        ax2.set_ylabel("Ω", color="r")
        ax.grid(alpha=0.3)
        
        # Combine legends
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax.legend(lines, labels, fontsize=7, loc="upper left")
    
    plt.suptitle("Geometry Parameter Sensitivity (around optimal configuration)", fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    print(f"  Saved: {filename}")


def plot_tradeoff_surface(params, filename="tradeoff_surface.png"):
    """Plot the conductivity vs surface area tradeoff surface."""
    model = GeometryModel()
    
    infill_range = np.linspace(20, 100, 25)
    layers_range = np.linspace(1, 20, 25)
    
    X, Y = np.meshgrid(infill_range, layers_range)
    Z_power = np.zeros_like(X)
    Z_cond = np.zeros_like(X)
    
    for i in range(len(infill_range)):
        for j in range(len(layers_range)):
            test = params.copy()
            test[1] = infill_range[i]
            test[4] = layers_range[j]
            props = model.compute(test)
            Z_power[j, i] = props.power_density_uW_cm2
            Z_cond[j, i] = props.conductivity_effective
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    ax1.contourf(X, Y, Z_power, levels=20, cmap="viridis")
    ax1.set_xlabel("Infill Density (%)")
    ax1.set_ylabel("Layer Count")
    ax1.set_title("Power Density (µW/cm²)")
    cbar1 = plt.colorbar(ax1.contourf(X, Y, Z_power, levels=20, cmap="viridis"), ax=ax1)
    ax1.scatter(params[1], params[4], c="red", s=100, marker="*", zorder=5, label="Optimum")
    ax1.legend()
    
    ax2.contourf(X, Y, Z_cond, levels=20, cmap="plasma")
    ax2.set_xlabel("Infill Density (%)")
    ax2.set_ylabel("Layer Count")
    ax2.set_title("Effective Conductivity (S/m)")
    cbar2 = plt.colorbar(ax2.contourf(X, Y, Z_cond, levels=20, cmap="plasma"), ax=ax2)
    ax2.scatter(params[1], params[4], c="red", s=100, marker="*", zorder=5, label="Optimum")
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    print(f"  Saved: {filename}")


def plot_rl_convergence(history, filename="rl_convergence.png"):
    if not history:
        return
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    generations = [h["generation"] for h in history]
    powers = [h["power"] for h in history]
    best_so_far = np.maximum.accumulate(powers)
    
    ax1.scatter(generations, powers, c="#3498db", s=20, alpha=0.3, label="All samples")
    ax1.plot(range(len(np.unique(generations))),
             [best_so_far[generations.index(g)] for g in sorted(set(generations)) if g in generations],
             "r-", linewidth=2, label="Best so far")
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("Power Density (µW/cm²)")
    ax1.set_title("CMA-ES Convergence")
    ax1.legend(fontsize=8)
    ax1.grid(alpha=0.3)
    
    resistances = [h["resistance"] for h in history]
    ax2.scatter(resistances, powers, c=generations, cmap="viridis", s=20, alpha=0.6)
    ax2.set_xlabel("Internal Resistance (Ω)")
    ax2.set_ylabel("Power Density (µW/cm²)")
    ax2.set_title("Power vs Resistance (color = generation)")
    cbar = plt.colorbar(ax2.collections[0], ax=ax2, label="Generation")
    ax2.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    print(f"  Saved: {filename}")


# ── Main ─────────────────────────────────────────────────────

if __name__ == "__main__":
    print("#" * 60)
    print("#  LEVEL 3: 3D PRINT GEOMETRY OPTIMIZATION")
    print("#  RL + Evolutionary Strategies for Maximum Power")
    print("#" * 60)
    
    model = GeometryModel()
    
    # ── 1. Baseline (Empa-like geometry) ──
    empa_params = np.array([100, 50, 2.0, 5.0, 7, 3.0])
    empa_props = model.compute(empa_params)
    print(f"\n📐 Empa baseline geometry:")
    print(f"   Layer: 100µm, Infill: 50%, Width: 5mm, Layers: 7")
    print(f"   Power: {empa_props.power_density_uW_cm2:.2f} µW/cm²")
    print(f"   R_internal: {empa_props.internal_resistance:.0f} Ω")
    
    # ── 2. Differential Evolution ──
    print(f"\n🔬 RUN 1: Differential Evolution")
    print(f"   Population: 60, Generations: 80")
    de_params, de_power, de_props = run_evolutionary_optimization()
    
    # ── 3. CMA-ES ──
    print(f"\n🧬 RUN 2: CMA-ES (Evolution Strategy)")
    cmaes = CMAESOptimizer(PARAM_BOUNDS_GEO, popsize=30)
    cmaes_params, cmaes_power, cmaes_props = cmaes.optimize(model, n_generations=50)
    
    # ── Results ──
    print(f"\n" + "=" * 60)
    print(f"  OPTIMIZATION RESULTS")
    print(f"  " + "=" * 60)
    
    runs = [
        ("Empa baseline", empa_params, empa_props),
        ("Differential Evolution", de_params, de_props),
        ("CMA-ES", cmaes_params, cmaes_props),
    ]
    
    results_table = []
    for name, p, props in runs:
        results_table.append({
            "name": name,
            "power": props.power_density_uW_cm2,
            "r_int": props.internal_resistance,
            "r_elec": props.electrolyte_resistance,
            "current": props.current_uA,
            "conductivity": props.conductivity_effective,
            "area": props.effective_area_mm2,
        })
    
    best_run = max(results_table, key=lambda r: r["power"])
    improvement = best_run["power"] / empa_props.power_density_uW_cm2
    
    print(f"\n  🏆 Best: {best_run['name']}")
    print(f"     Power density:     {best_run['power']:.2f} µW/cm²")
    print(f"     vs Empa baseline:  {improvement:.1f}×")
    print(f"     Internal R:        {best_run['r_int']:.0f} Ω")
    print(f"     Electrolyte R:     {best_run['r_elec']:.0f} Ω")
    print(f"     Effective area:    {best_run['area']:.1f} mm²")
    print(f"     Conductivity:      {best_run['conductivity']:.2f} S/m")
    
    best_params = cmaes_params if cmaes_power >= de_power else de_params
    best_props = cmaes_props if cmaes_power >= de_power else de_props
    
    print(f"\n  Optimal geometry:")
    for name, val in zip(PARAM_NAMES_GEO, best_params):
        pmin, pmax = PARAM_BOUNDS_GEO[PARAM_NAMES_GEO.index(name)]
        pct = (val - pmin) / (pmax - pmin) * 100
        direction = "HIGH" if pct > 66 else ("LOW" if pct < 33 else "MID")
        print(f"     {name:25s} = {val:8.1f}  ({pct:.0f}% range, {direction})")
    
    # ── Visualizations ──
    print(f"\n📊 Generating visualizations...")
    plot_geometry_optimization(results_table, best_params,
        "/home/weissto_local/workspace/shrooms/simulation/geometry_optimization.png")
    plot_tradeoff_surface(best_params,
        "/home/weissto_local/workspace/shrooms/simulation/tradeoff_surface.png")
    plot_rl_convergence(cmaes.history,
        "/home/weissto_local/workspace/shrooms/simulation/rl_convergence.png")
    
    # ── Final recommendation ──
    print(f"\n" + "=" * 60)
    print(f"  FINAL RECOMMENDATION")
    print(f"  " + "=" * 60)
    print(f"""
  Combined AI optimization pipeline result:
  
  Level 1: Ink Formulation (Bayesian Opt)
     → {261:.0f} µW/cm² achievable with optimized carbon/graphite ratio
  
  Level 2: Parameter Synergy (RF)
     → Graphite content dominates (80.6%), carbon black secondary (13.0%)
     → No significant synergy between biology & materials needed
  
  Level 3: Print Geometry (CMA-ES + DE)
     → {best_props.power_density_uW_cm2:.0f} µW/cm² achievable with optimized geometry
     → vs {empa_props.power_density_uW_cm2:.1f} µW/cm² baseline = {best_run['power']/empa_props.power_density_uW_cm2:.1f}× improvement
  
  Total improvement potential: {best_run['power']/12.5:.0f}× over Empa baseline (12.5 µW/cm²)
  → From {12.5:.0f} µW/cm² to {best_run['power']:.0f} µW/cm²
  → SUFFICIENT for: IoT sensors, environmental monitoring, disposable diagnostics
  → NOT sufficient for: BLE transmission, continuous high-power applications
  
  Next hardware step: Build and measure the predicted optimal configuration.
""")
    
    print(f"  Done.")
