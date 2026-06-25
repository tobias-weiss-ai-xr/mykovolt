#!/usr/bin/env python3
"""
Fungal Bio-Battery — Electron Transport Graph Simulation

Modelliert die Elektronentransportkette einer pilzbasierten mikrobiellen
Brennstoffzelle (MFC) als gerichteten Graphen und identifiziert:
  - Rate-limiting steps (Bottlenecks)
  - Theoretische maximale Leistungsdichte
  - Strain-Vergleich (T. pubescens vs. P. chrysosporium)
  - Sensitivität: Welcher Hebel bringt am meisten?

Graph-Modell:
  Knoten = molekulare / redox-Zustände
  Kanten = Reaktionen (mit Ratenkonstanten)
  Fluss = Elektronenstrom (mol e⁻/s → A → W)
  Max-Flow / Min-Cut = Bottleneck-Analyse

Literatur-Referenzen:
  - Reyes et al. 2024 (Empa): 3D-gedruckte Pilz-MFC, 12.5 µW/cm²
  - Energies 2021: P. chrysosporium, 1.9 W/m²
  - Frontiers 2024 Review: Übersicht Pilz-MFC-Leistungen

Autor: Contextual Intelligence / Tobias Weiss
Stand: Juni 2026
"""

import networkx as nx
import numpy as np
from typing import Dict, Tuple, Optional
import math

# ─── Physikalische Konstanten ──────────────────────────────────────────────────
FARADAY = 96485.3329       # C/mol (Faraday-Konstante)
R = 8.314                   # J/(mol·K) (Gaskonstante)
T = 298.15                  # K (25°C)
RT_OVER_F = R * T / FARADAY # ~0.0257 V (thermal voltage)

# ─── Zell-Geometrie (Empa-Design) ──────────────────────────────────────────────
CELL_AREA = 1.0             # cm² (Standard-Testzelle)
CELL_VOLUME = 0.5           # mL (Elektrolytvolumen)
YEAST_CELLS = 1e8           # Zellen (7-Lagen-Druck)
ELECTRODE_DISTANCE = 0.5    # cm (Abstand Anode-Kathode)

# ─── Anode: Yeast Metabolism (S. cerevisiae) ──────────────────────────────────
# Glucose consumption rate (anaerobic, glucose-limited)
GLUCOSE_CONSUMPTION = 2.0e-12   # mol glucose / cell / h (approx.)
                                # = ~2 mmol/gDCW/h, ~1e8 cells ≈ 0.2 mg DCW
NADH_PER_GLUCOSE = 2.0          # mol NADH / mol glucose (anaerobic glycolysis)
NADH_ELECTRON_YIELD = 2.0       # mol e⁻ / mol NADH (via mediator)

# ─── Mediator: ABTS ────────────────────────────────────────────────────────────
ABTS_CONCENTRATION = 20.0e-3    # M (20 mM — Empa-Protokoll)
ABTS_DIFFUSIVITY = 5.0e-10     # m²/s (approx. in hydrogel)
ABTS_TURNOVER = 100.0           # s⁻¹ (with laccase, kcat/Km)

# ─── Cathode: Laccase (T. pubescens) ──────────────────────────────────────────
# Laccase kinetic parameters
LACCASE_KCAT_T_PUB = 200.0      # s⁻¹ (T. pubescens laccase)
LACCASE_KM_O2 = 50.0e-6        # M (O₂ affinity, typical for fungal laccases)
LACCASE_CONC = 10.0e-6          # M (10 µM, approx. in supernatant)
O2_CONCENTRATION = 250.0e-6     # M (dissolved O₂ in water at 25°C, air-sat)

# ─── Alternative: P. chrysosporium enzymes ────────────────────────────────────
LACCASE_KCAT_P_CHRY = 500.0     # s⁻¹ (lignin peroxidase, higher activity)
LACCASE_KM_O2_P_CHRY = 30.0e-6 # M (higher O₂ affinity)

# ─── Electrical Properties ─────────────────────────────────────────────────────
INK_CONDUCTIVITY = 10.0         # S/m (carbon black + graphite in cellulose)
INK_RESISTIVITY = 1 / INK_CONDUCTIVITY  # Ω·m
LOAD_RESISTANCE = 22.0e3        # Ω (Empa: max power at 22 kΩ)
INTERNAL_RESISTANCE = 10.0e3    # Ω (geschätzt aus Empa-Daten)

# ==============================================================================
class FungalMFCGraph:
    """Elektronentransport-Graph einer pilzbasierten mikrobiellen Brennstoffzelle."""

    def __init__(self, strain: str = "T_pubescens"):
        """
        strain: "T_pubescens" | "P_chrysosporium" | "custom"
        """
        self.strain = strain
        self.G = nx.DiGraph()
        self._build_graph()
        self._add_capacities()

    def _build_graph(self):
        """Erstellt den gerichteten Graphen der Elektronentransportkette."""

        # ── Knoten (Redox-Zustände) ──
        nodes = [
            # Substrate
            ("glucose", {"type": "substrate", "concentration": 100e-3, "unit": "M"}),  # 100 mM glucose
            ("o2", {"type": "substrate", "concentration": O2_CONCENTRATION, "unit": "M"}),

            # Yeast metabolism
            ("pyruvate", {"type": "metabolite"}),
            ("nadh", {"type": "electron_carrier", "concentration": None}),
            ("nad+", {"type": "electron_carrier"}),

            # Mediator (ABTS)
            ("abts_red", {"type": "mediator", "concentration": ABTS_CONCENTRATION, "unit": "M"}),
            ("abts_ox", {"type": "mediator"}),

            # Anode → External circuit
            ("anode", {"type": "electrode"}),
            ("circuit", {"type": "electrical"}),
            ("cathode", {"type": "electrode"}),

            # Laccase redox states
            ("laccase_ox", {"type": "enzyme", "concentration": LACCASE_CONC, "unit": "M"}),
            ("laccase_red", {"type": "enzyme", "concentration": 0.0, "unit": "M"}),

            # Products
            ("h2o", {"type": "product"}),
        ]

        self.G.add_nodes_from(nodes)

        # ── Kanten (Reaktionen) ──
        edges = [
            # Glycolysis: Glucose → 2 Pyruvate + 2 NADH
            ("glucose", "nadh", {
                "reaction": "glycolysis",
                "description": "Glucose → 2 Pyruvate + 2 NADH",
                "stoichiometry": NADH_ELECTRON_YIELD * NADH_PER_GLUCOSE,  # mol e⁻ per mol glucose
                "rate_type": "consumption",
            }),
            ("glucose", "pyruvate", {
                "reaction": "glycolysis",
                "description": "Glucose → 2 Pyruvate",
                "rate_type": "byproduct",
            }),

            # NADH → NAD⁺ via mediator (ABTS)
            ("nadh", "abts_red", {
                "reaction": "mediator_reduction",
                "description": "NADH reduces ABTS²⁻ → ABTS·⁻",
                "stoichiometry": NADH_ELECTRON_YIELD,  # 2 e⁻ per NADH
                "rate_type": "diffusion_limited",
            }),

            # ABTS_red → ABTS_ox (mediator re-oxidation at anode)
            ("abts_red", "abts_ox", {
                "reaction": "mediator_oxidation",
                "description": "ABTS·⁻ → ABTS²⁻ + e⁻ (at anode surface)",
                "stoichiometry": 1.0,
                "rate_type": "electron_transfer",
            }),

            # ABTS_ox → Anode (electron injected into external circuit)
            ("abts_ox", "anode", {
                "reaction": "electron_injection",
                "description": "e⁻ enters the external circuit from anode",
                "stoichiometry": 1.0,
                "rate_type": "ohmic",
            }),

            # Anode → External circuit (load resistor)
            ("anode", "circuit", {
                "reaction": "external_circuit",
                "description": "e⁻ flow through load resistor",
                "stoichiometry": 1.0,
                "rate_type": "ohmic",
            }),

            # Circuit → Cathode
            ("circuit", "cathode", {
                "reaction": "cathode_arrival",
                "description": "e⁻ arrives at cathode",
                "stoichiometry": 1.0,
                "rate_type": "ohmic",
            }),

            # Cathode → Laccase_red (electron reduces oxidized laccase)
            ("cathode", "laccase_red", {
                "reaction": "laccase_reduction",
                "description": "Laccase(ox) + e⁻ → Laccase(red) at cathode surface",
                "stoichiometry": 1.0,
                "rate_type": "enzyme_kinetics",
                "kcat": self._get_laccase_kcat(),
            }),

            # Laccase_red → Laccase_ox (enzyme re-oxidized by O₂)
            ("laccase_red", "laccase_ox", {
                "reaction": "laccase_reoxidation",
                "description": "Laccase(red) + O₂ → Laccase(ox) + H₂O",
                "stoichiometry": 4.0,  # each catalytic cycle transfers 4 e⁻ to O₂
                "rate_type": "enzyme_kinetics",
                "kcat": self._get_laccase_kcat(),
            }),

            # Laccase_ox → O₂ (electron transfer to terminal acceptor)
            ("laccase_ox", "o2", {
                "reaction": "oxygen_reduction",
                "description": "4 e⁻ reduce O₂ → 2H₂O via laccase",
                "stoichiometry": 4.0,
                "rate_type": "enzyme_kinetics",
                "kcat": self._get_laccase_kcat(),
            }),

            # O₂ → H₂O (overall ORR complete)
            ("o2", "h2o", {
                "reaction": "orr",
                "description": "O₂ + 4H⁺ + 4e⁻ → 2H₂O",
                "stoichiometry": 4.0,
                "rate_type": "overall",
            }),

            # NAD⁺ → Glucose (closed metabolic cycle — NAD⁺ recycled)
            # For the flow network this is a return edge but we keep flow directed
            ("nad+", "glucose", {
                "reaction": "metabolic_cycle",
                "description": "NAD⁺ recycling (metabolic cofactor)",
                "stoichiometry": 0.0,  # no net e⁻ flow
                "rate_type": "cycle",
            }),
        ]

        self.G.add_edges_from(edges)

    def _get_laccase_kcat(self) -> float:
        """Gibt die Enzym-Aktivität je nach Stamm zurück."""
        if self.strain == "T_pubescens":
            return LACCASE_KCAT_T_PUB
        elif self.strain == "P_chrysosporium":
            return LACCASE_KCAT_P_CHRY
        else:
            return LACCASE_KCAT_T_PUB

    def _add_capacities(self):
        """
        Berechnet die maximale Kapazität jeder Kante in mol e⁻/s.

        Die Kapazität = maximale Elektronenflussrate durch diesen Schritt.
        Umgerechnet in Strom: I = flow × FARADAY [A]
        """
        capacities = {}

        # 1) Glycolysis: Glucose consumption rate
        # Total glucose consumption = per-cell rate × number of cells
        total_glucose_mol_s = GLUCOSE_CONSUMPTION * YEAST_CELLS / 3600  # mol/s
        glycolysis_e_rate = total_glucose_mol_s * NADH_ELECTRON_YIELD * NADH_PER_GLUCOSE
        capacities[("glucose", "nadh")] = glycolysis_e_rate

        # 2) NADH → ABTS (mediator reduction)
        # Limited by ABTS concentration × diffusion × reaction rate
        abts_mol = ABTS_CONCENTRATION * CELL_VOLUME * 1e-3  # mol of ABTS in cell
        mediator_turnover_rate = abts_mol * ABTS_TURNOVER  # mol/s (if all ABTS is turning over)
        # But also limited by NADH availability
        nadh_mol_s = glycolysis_e_rate / NADH_ELECTRON_YIELD
        capacities[("nadh", "abts_red")] = min(glycolysis_e_rate, mediator_turnover_rate * 2)

        # 3) ABTS_red → ABTS_ox (mediator re-oxidation at anode)
        capacities[("abts_red", "abts_ox")] = mediator_turnover_rate * 2

        # 4) ABTS_ox → Anode (electron injection)
        capacities[("abts_ox", "anode")] = mediator_turnover_rate * 2

        # 5) Anode → Circuit (ohmic loss)
        v_oc = 0.45
        i_max_ohmic = v_oc / INTERNAL_RESISTANCE
        capacities[("anode", "circuit")] = i_max_ohmic / FARADAY

        # 6) Circuit → Cathode
        capacities[("circuit", "cathode")] = i_max_ohmic / FARADAY

        # 7) Cathode → Laccase_red (enzyme reduction)
        laccase_mol = LACCASE_CONC * CELL_VOLUME * 1e-3
        laccase_turnover_rate = laccase_mol * self._get_laccase_kcat()
        capacities[("cathode", "laccase_red")] = laccase_turnover_rate

        # 8) Laccase_red → Laccase_ox (enzyme re-oxidation, transfers 4e⁻ to O₂)
        capacities[("laccase_red", "laccase_ox")] = laccase_turnover_rate * 4

        # 9) Laccase_ox → O₂ (terminal e⁻ acceptor reduction)
        # Empa cathode is air-breathing with porous 3D-printed structure:
        #   - O₂ diffuses through AIR in pores (D_air ≈ 2e-5 m²/s)
        #   - Effective diffusion path: ~10 µm (thin printed electrode)
        #   - Effective surface area: factor ~100× geometric (porosity + roughness)
        o2_diffusivity_air = 2.0e-5  # m²/s (O₂ in air!)
        electrode_thickness = 10e-6  # m (10 µm — thin printed layer)
        surface_roughness = 100.0    # effective × geometric area
        o2_flux_mol_s = (o2_diffusivity_air * O2_CONCENTRATION / electrode_thickness) * (CELL_AREA * 1e-4 * surface_roughness)
        capacities[("laccase_ox", "o2")] = o2_flux_mol_s * 4  # 4 e⁻ per O₂

        # Set edge capacities
        for edge, cap in capacities.items():
            if self.G.has_edge(*edge):
                self.G[edge[0]][edge[1]]["capacity"] = cap
                self.G[edge[0]][edge[1]]["capacity_text"] = f"{cap:.3e} mol e⁻/s"
                self.G[edge[0]][edge[1]]["current_eq"] = f"{cap * FARADAY * 1e6:.1f} µA"

    def bottleneck_analysis(self) -> Dict:
        """
        Identifiziert den Flaschenhals (Min-Cut) im Elektronentransport.

        Returns:
            Dict mit bottleneck-Kante, Kapazität, max. Strom, max. Leistung
        """
        # Find min cut between source (glucose) and sink (h2o)
        try:
            flow_value, flow_dict = nx.maximum_flow(self.G, "glucose", "h2o", capacity="capacity")
        except Exception as e:
            return {"error": f"Max flow computation failed: {e}"}

        # Find minimum capacity edge on the critical path
        critical_path_edges = []
        min_capacity = float("inf")
        min_edge = None

        for u, v, data in self.G.edges(data=True):
            if "capacity" in data:
                cap = data["capacity"]
                if cap < min_capacity and cap > 0:
                    min_capacity = cap
                    min_edge = (u, v)
                critical_path_edges.append({
                    "edge": f"{u} → {v}",
                    "capacity_mol_s": cap,
                    "current_uA": cap * FARADAY * 1e6,
                    "reaction": data.get("description", ""),
                    "rate_type": data.get("rate_type", ""),
                })

        # Sort by capacity (ascending) = bottleneck ranking
        critical_path_edges.sort(key=lambda x: x["capacity_mol_s"])

        max_current_A = flow_value * FARADAY
        max_power_W = max_current_A ** 2 * LOAD_RESISTANCE  # P = I²R
        max_power_density_uW_cm2 = max_power_W / CELL_AREA * 1e6

        return {
            "max_flow_mol_s": flow_value,
            "max_current_A": max_current_A,
            "max_current_uA": max_current_A * 1e6,
            "max_power_W": max_power_W,
            "max_power_density_uW_cm2": max_power_density_uW_cm2,
            "bottleneck_edge": f"{min_edge[0]} → {min_edge[1]}" if min_edge else None,
            "bottleneck_capacity_mol_s": min_capacity,
            "bottleneck_current_uA": min_capacity * FARADAY * 1e6,
            "bottleneck_rate_type": self.G[min_edge[0]][min_edge[1]].get("rate_type", "") if min_edge else None,
            "bottleneck_reaction": self.G[min_edge[0]][min_edge[1]].get("description", "") if min_edge else None,
            "critical_path_ranking": critical_path_edges,
            "strain": self.strain,
        }

    def sensitivity_analysis(self, parameter: str, factor: float) -> Dict:
        """
        Führt eine Sensitivitätsanalyse durch: Was passiert, wenn ein Parameter
        um factor skaliert wird?

        Args:
            parameter: "glucose_consumption" | "laccase_activity" | "mediator" |
                      "o2_diffusion" | "conductivity" | "yeast_cells"
            factor: Multiplikator (z.B. 2.0 = Verdopplung)
        """
        # Save original values
        orig_glucose = GLUCOSE_CONSUMPTION
        orig_laccase = LACCASE_KCAT_T_PUB
        orig_o2 = O2_CONCENTRATION
        orig_abts = ABTS_TURNOVER
        orig_cells = YEAST_CELLS
        orig_conductivity = INK_CONDUCTIVITY

        # Apply modification
        if parameter == "glucose_consumption":
            globals()["GLUCOSE_CONSUMPTION"] = GLUCOSE_CONSUMPTION * factor
        elif parameter == "laccase_activity":
            globals()["LACCASE_KCAT_T_PUB"] = LACCASE_KCAT_T_PUB * factor
        elif parameter == "mediator":
            globals()["ABTS_TURNOVER"] = ABTS_TURNOVER * factor
        elif parameter == "o2_diffusion":
            globals()["O2_CONCENTRATION"] = O2_CONCENTRATION * factor
        elif parameter == "conductivity":
            globals()["INTERNAL_RESISTANCE"] = INTERNAL_RESISTANCE / factor
        elif parameter == "yeast_cells":
            globals()["YEAST_CELLS"] = YEAST_CELLS * factor

        # Rebuild graph and compute
        old_strain = self.strain
        new_graph = FungalMFCGraph(strain=old_strain)
        result = new_graph.bottleneck_analysis()

        # Restore
        globals()["GLUCOSE_CONSUMPTION"] = orig_glucose
        globals()["LACCASE_KCAT_T_PUB"] = orig_laccase
        globals()["O2_CONCENTRATION"] = orig_o2
        globals()["ABTS_TURNOVER"] = orig_abts
        globals()["YEAST_CELLS"] = orig_cells
        globals()["INTERNAL_RESISTANCE"] = 1 / orig_conductivity

        return result

    def multi_sensitivity(self) -> Dict:
        """Vergleicht alle Optimierungshebel bei Faktor 2x, 5x, 10x."""
        levers = [
            "glucose_consumption",
            "laccase_activity",
            "mediator",
            "o2_diffusion",
            "conductivity",
            "yeast_cells",
        ]
        factors = [2.0, 5.0, 10.0]

        baseline = self.bottleneck_analysis()
        baseline_power = baseline["max_power_density_uW_cm2"]

        results = {}
        for lever in levers:
            lever_results = {}
            for factor in factors:
                try:
                    r = self.sensitivity_analysis(lever, factor)
                    lever_results[f"{factor}x"] = {
                        "power_uW_cm2": r["max_power_density_uW_cm2"],
                        "improvement": r["max_power_density_uW_cm2"] / baseline_power if baseline_power > 0 else 0,
                        "new_bottleneck": r.get("bottleneck_rate_type", "unknown"),
                    }
                except Exception as e:
                    lever_results[f"{factor}x"] = {
                        "power_uW_cm2": 0,
                        "improvement": 0,
                        "error": str(e),
                    }
            results[lever] = lever_results

        ranking = []
        for lever in levers:
            entry = results[lever].get("5x", {})
            improvement = entry.get("improvement", 0.0)
            ranking.append({
                "lever": lever,
                "improvement_5x": improvement,
                "power_at_5x_uW_cm2": entry.get("power_uW_cm2", 0),
                "new_bottleneck_at_5x": entry.get("new_bottleneck", "unknown"),
            })

        ranking.sort(key=lambda x: x["improvement_5x"], reverse=True)

        return {
            "baseline_power_uW_cm2": baseline_power,
            "baseline_bottleneck": baseline["bottleneck_edge"],
            "strain": self.strain,
            "all_results": results,
            "ranking": ranking,
        }

    def print_summary(self):
        """Gibt eine formatierte Zusammenfassung aus."""
        result = self.bottleneck_analysis()

        print("=" * 60)
        print(f"  FUNGAL BIO-BATTERY — ELECTRON TRANSPORT GRAPH")
        print(f"  Strain: {self.strain}")
        print(f"  Cells: {YEAST_CELLS:.1e} | Area: {CELL_AREA} cm²")
        print("=" * 60)

        print(f"\n📊 MAX-FLOW ANALYSIS (glucose → h₂O):")
        print(f"   Max electron flow:  {result['max_flow_mol_s']:.3e} mol e⁻/s")
        print(f"   Max current:       {result['max_current_uA']:.1f} µA")
        print(f"   Max power density: {result['max_power_density_uW_cm2']:.3f} µW/cm²")
        print(f"   Empa baseline:     12.5 µW/cm²")
        print(f"   Achievable ratio:  {result['max_power_density_uW_cm2'] / 12.5:.2f}×")

        print(f"\n🔴 BOTTLENECK (rate-limiting step):")
        print(f"   Edge:     {result['bottleneck_edge']}")
        print(f"   Type:     {result['bottleneck_rate_type']}")
        print(f"   Reaction: {result['bottleneck_reaction']}")
        print(f"   Max:      {result['bottleneck_current_uA']:.1f} µA")

        print(f"\n📈 CRITICAL PATH RANKING (all edges):")
        for i, edge in enumerate(result["critical_path_ranking"][:8]):
            bar = "#" * max(1, int(edge["current_uA"] / max(1, result["critical_path_ranking"][-1]["current_uA"]) * 40))
            print(f"   {i+1}. {edge['edge']:35s} {edge['current_uA']:8.1f} µA  |{bar}")

        return result


# ==============================================================================
def compare_strains():
    """Vergleicht T. pubescens (Empa) mit P. chrysosporium (High-Performance)."""
    print("\n" + "=" * 60)
    print("  STRAIN COMPARISON")
    print("=" * 60)

    strains = {
        "T_pubescens": "Trametes pubescens (Empa baseline)",
        "P_chrysosporium": "Phanerochaete chrysosporium (high-performance)",
    }

    results = {}
    for strain, name in strains.items():
        mfc = FungalMFCGraph(strain=strain)
        r = mfc.bottleneck_analysis()
        results[strain] = r
        print(f"\n  📊 {name}:")
        print(f"     Power density: {r['max_power_density_uW_cm2']:.3f} µW/cm²")
        print(f"     Bottleneck:    {r['bottleneck_edge']} ({r['bottleneck_reaction']})")
        print(f"     Current:       {r['max_current_uA']:.1f} µA")

    if len(results) == 2:
        ratio = results["P_chrysosporium"]["max_power_density_uW_cm2"] / results["T_pubescens"]["max_power_density_uW_cm2"]
        print(f"\n  🏆 Improvement P. chrysosporium vs T. pubescens: {ratio:.1f}×")

    return results


def run_sensitivity_ranking():
    """Führt die vollständige Sensitivitätsanalyse durch."""
    print("\n" + "=" * 60)
    print("  SENSITIVITY ANALYSIS — OPTIMIZATION LEVERS")
    print("=" * 60)

    mfc = FungalMFCGraph(strain="T_pubescens")
    baseline = mfc.bottleneck_analysis()["max_power_density_uW_cm2"]
    print(f"\n  Baseline (T. pubescens): {baseline:.3f} µW/cm² (= 1.0×)")

    sensitivity = mfc.multi_sensitivity()

    print(f"\n  RANKING (by impact at 5× improvement):")
    for i, item in enumerate(sensitivity["ranking"]):
        lever_name = {
            "laccase_activity": "🧬 Laccase activity (enzyme engineering)",
            "glucose_consumption": "🍬 Glucose uptake (strain engineering)",
            "o2_diffusion": "💨 O₂ diffusion (cathode design)",
            "conductivity": "⚡ Ink conductivity (material optimization)",
            "mediator": "🔬 Mediator turnover (ABTS chemistry)",
            "yeast_cells": "🦠 Yeast cell count (printing density)",
        }.get(item["lever"], item["lever"])

        print(f"   {i+1}. {lever_name:55s} {item['improvement_5x']:5.1f}× → {item['power_at_5x_uW_cm2']:.1f} µW/cm²")
        print(f"      New bottleneck: {item['new_bottleneck_at_5x']}")

    return sensitivity


def theoretical_maximum():
    """
    Berechnet das theoretische absolute Maximum unter idealen Bedingungen.
    """
    print("\n" + "=" * 60)
    print("  THEORETICAL UPPER BOUND")
    print("=" * 60)

    # Absolute limits based on biology and physics:

    # 1) Glucose energy content
    # ΔH_comb glucose = -2805 kJ/mol
    # If all glucose energy → electricity (η=100%)
    glucose_mol = GLUCOSE_CONSUMPTION * YEAST_CELLS  # mol/h
    power_total = glucose_mol * 2805e3 / 3600  # W (total chemical power)
    # Power density = power_total / area
    # But we can't extract ALL energy — max efficiency of MFC ~50-60%
    # And only electrons that go through external circuit count

    # 2) Maximum electron flux
    # Each glucose yields 24 e⁻ if fully oxidized (complete oxidation to CO₂)
    # Current: I = n × F × rate = 24 × 96485 × glucose_mol / 3600
    i_max = 24 * FARADAY * (GLUCOSE_CONSUMPTION * YEAST_CELLS) / 3600
    # At maximum power transfer (R_load = R_internal):
    # P_max = V_oc² / (4 × R_internal) for matched load
    v_oc_max = 1.2  # V (highest reported in literature, P. chrysosporium)
    r_internal_min = 1000  # Ω (highly optimized)
    p_max_ideal = v_oc_max**2 / (4 * r_internal_min)

    # 3) O₂ diffusion limit
    o2_diff_max = (2.0e-9 * O2_CONCENTRATION / 100e-6) * (CELL_AREA * 1e-4)  # mol O₂/s
    i_o2_limited = o2_diff_max * 4 * FARADAY  # A (4 e⁻ per O₂)

    # 4) Laccase turnover limit
    laccase_mol = LACCASE_CONC * CELL_VOLUME * 1e-3
    i_laccase_limited = laccase_mol * LACCASE_KCAT_T_PUB * 4 * FARADAY * 10  # 10× for high-expression

    print(f"   Energy limit (100% glucose→electricity): {power_total / CELL_AREA * 1e6:.1f} µW/cm²")
    print(f"   O₂ diffusion limit:                     {i_o2_limited * 1e6:.1f} µA/cm²")
    print(f"   Laccase turnover limit (10× expr.):     {i_laccase_limited * 1e6:.1f} µA/cm²")
    print(f"   Theoretical max power (matched load):   {p_max_ideal * 1e6 / CELL_AREA:.1f} µW/cm²")
    print(f"   Best literature (P. chrysosporium):     {1.9e6 * 1e4 * 1e6 / 1e6:.1f} µW/cm² (= 1,900,000 µW/cm²)")
    print(f"   → Biological limits suggest ~5 mW/cm² achievable with optimization")
    print(f"   → 3D-printed biodegradable: trade-off reduces this to ~50-100 µW/cm²")


# ==============================================================================
if __name__ == "__main__":
    print("\n" + "#" * 60)
    print("#  FUNGAL BIO-BATTERY GRAPH SIMULATION")
    print("#  Electron Transport Network Analysis")
    print("#" * 60)

    # 1. Baseline: T. pubescens (Empa design)
    mfc_tpub = FungalMFCGraph(strain="T_pubescens")
    mfc_tpub.print_summary()

    # 2. Compare with P. chrysosporium
    compare_strains()

    # 3. Sensitivity ranking
    run_sensitivity_ranking()

    # 4. Theoretical maximum
    theoretical_maximum()

    print("\n" + "=" * 60)
    print("  DONE.")
    print("=" * 60)
