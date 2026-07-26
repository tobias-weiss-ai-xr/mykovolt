#!/usr/bin/env python3
"""
Manufacturing BOM (Bill of Materials) — Bottom-Up Cost Model

Builds a detailed cost estimate for each MykoVolt product path:
  Path A: Air-Chimney Pressling (fungal MFC + chimney)
  Path B: Mg-Air Battery (biodegradable metal-air)
  Path C: Passive NFC DevKit (no battery, reader-powered)
  Hybrid: Reusable electronics board + replaceable bio-pellet

All costs in EUR, at three volume tiers:
  - Prototype (1-100 units)
  - Pilot (1k-10k units)  
  - Mass Production (100k+ units)

Usage:
  python3 manufacturing_bom.py                  # Full report
  python3 manufacturing_bom.py --path a         # Path A only
  python3 manufacturing_bom.py --json bom.json  # Export to JSON
  python3 manufacturing_bom.py --sensitivity    # Monte Carlo on cost assumptions
"""

import math
import random
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple
from enum import Enum


class VolumeTier(Enum):
    PROTOTYPE = "prototype"       # 1-100 units
    PILOT = "pilot"               # 1k-10k units
    MASS = "mass_production"      # 100k+ units


@dataclass
class LineItem:
    """A single line item in the BOM."""
    name: str
    description: str
    qty: float                    # Quantity per unit
    unit: str                     # g, mm, pcs, ml, etc.
    cost_prototype: float         # EUR per unit at prototype scale
    cost_pilot: float             # EUR per unit at pilot scale
    cost_mass: float              # EUR per unit at mass production
    is_reusable: bool = False     # Can be reused across cycles?
    reusable_cycles: int = 1      # How many reuse cycles?
    is_biodegradable: bool = True # Compostable?
    source: str = "TBD"           # Supplier / sourcing note
    
    def cost_at_tier(self, tier: VolumeTier) -> float:
        cost = {
            VolumeTier.PROTOTYPE: self.cost_prototype,
            VolumeTier.PILOT: self.cost_pilot,
            VolumeTier.MASS: self.cost_mass,
        }[tier]
        if self.is_reusable and self.reusable_cycles > 1:
            cost /= self.reusable_cycles
        return cost * self.qty


@dataclass
class BOM:
    """Complete bill of materials for a product path."""
    name: str
    description: str
    items: List[LineItem]
    assembly_cost_prototype: float = 0
    assembly_cost_pilot: float = 0
    assembly_cost_mass: float = 0
    testing_cost_prototype: float = 0
    testing_cost_pilot: float = 0
    testing_cost_mass: float = 0
    packaging_cost_prototype: float = 0
    packaging_cost_pilot: float = 0
    packaging_cost_mass: float = 0
    
    def total_at_tier(self, tier: VolumeTier) -> float:
        mat = sum(item.cost_at_tier(tier) for item in self.items)
        assembly = {
            VolumeTier.PROTOTYPE: self.assembly_cost_prototype,
            VolumeTier.PILOT: self.assembly_cost_pilot,
            VolumeTier.MASS: self.assembly_cost_mass,
        }[tier]
        testing = {
            VolumeTier.PROTOTYPE: self.testing_cost_prototype,
            VolumeTier.PILOT: self.testing_cost_pilot,
            VolumeTier.MASS: self.testing_cost_mass,
        }[tier]
        packaging = {
            VolumeTier.PROTOTYPE: self.packaging_cost_prototype,
            VolumeTier.PILOT: self.packaging_cost_pilot,
            VolumeTier.MASS: self.packaging_cost_mass,
        }[tier]
        return mat + assembly + testing + packaging
    
    def breakdown_at_tier(self, tier: VolumeTier) -> Dict:
        """Detailed cost breakdown."""
        items_detail = []
        for item in self.items:
            items_detail.append({
                "name": item.name,
                "qty": item.qty,
                "unit_cost": item.cost_at_tier(tier),
                "total": item.cost_at_tier(tier),
                "is_biodegradable": item.is_biodegradable,
                "is_reusable": item.is_reusable,
            })
        
        total = self.total_at_tier(tier)
        mat_cost = sum(item.cost_at_tier(tier) for item in self.items)
        assembly = {
            VolumeTier.PROTOTYPE: self.assembly_cost_prototype,
            VolumeTier.PILOT: self.assembly_cost_pilot,
            VolumeTier.MASS: self.assembly_cost_mass,
        }[tier]
        
        return {
            "items": items_detail,
            "materials_total": round(mat_cost, 4),
            "assembly": round(assembly, 4),
            "total": round(total, 4),
            "biodegradable_pct": round(
                sum(i.cost_at_tier(tier) for i in self.items if i.is_biodegradable) / mat_cost * 100
                if mat_cost > 0 else 0, 1),
            "reusable_pct": round(
                sum(i.cost_at_tier(tier) for i in self.items if i.is_reusable) / mat_cost * 100
                if mat_cost > 0 else 0, 1),
        }


# =========================================================================
# PATH A: AIR-CHIMNEY PRESSLING (Fungal MFC + breathing tube)
# =========================================================================

def bom_path_a() -> BOM:
    """Bill of Materials for Air-Chimney Pressling."""
    items = [
        LineItem("Fungal strain culture", "T. pubescens or P. chrysosporium, freeze-dried spores",
                 0.01, "mg", 5.00, 0.50, 0.05, is_biodegradable=True, source="DSMZ / in-house"),
        LineItem("Cellulose nanofibrils (CNF)", "Binder and structural matrix, 2% dispersion",
                 0.5, "ml", 0.80, 0.08, 0.01, is_biodegradable=True, source="NanoNovin / paper mills"),
        LineItem("Carbon black (Super P)", "Conductive filler for anode",
                 0.05, "g", 0.30, 0.03, 0.005, is_biodegradable=True, source="Alfa Aesar / Imerys"),
        LineItem("Graphite flakes", "High-conductivity filler (99%, <50µm)",
                 0.05, "g", 0.25, 0.025, 0.004, is_biodegradable=True, source="Sigma / Graphit Kropfmühl"),
        LineItem("Glucose", "Fuel for yeast anode",
                 0.1, "g", 0.05, 0.005, 0.001, is_biodegradable=True, source="Sigma / local"),
        LineItem("Yeast extract", "Nutrient for fungal growth",
                 0.02, "g", 0.08, 0.008, 0.001, is_biodegradable=True, source="Sigma / local"),
        LineItem("ABTS mediator", "Electron shuttle for laccase cathode",
                 0.001, "g", 2.00, 0.20, 0.02, is_biodegradable=True, source="Sigma"),
        LineItem("PTFE chimney tube", "Air breathing tube, OD 3mm, ID 2mm",
                 10, "cm", 0.15, 0.05, 0.02, is_biodegradable=False, source="Labshop / custom extrusion"),
        LineItem("Chimney cap (PLA)", "3D-printed cap to keep tube open",
                 1, "pcs", 0.50, 0.10, 0.03, is_biodegradable=True, source="3D-printed in-house"),
        LineItem("Compostable casing", "PLA/PHA pellet housing, IP67",
                 1, "pcs", 0.80, 0.20, 0.05, is_biodegradable=True, source="Injection molded"),
        LineItem("Pressing energy", "Electricity for tablet press",
                 0.001, "kWh", 0.03, 0.003, 0.001, is_biodegradable=True, source="Grid"),
        LineItem("Moisture barrier pouch", "Vacuum-sealed foil for shelf life",
                 1, "pcs", 0.10, 0.03, 0.01, is_biodegradable=False, source="Packaging supplier"),
    ]
    return BOM(
        name="Air-Chimney Pressling",
        description="Fungal MFC pellet with air-breathing chimney tube for buried operation",
        items=items,
        assembly_cost_prototype=2.00,
        assembly_cost_pilot=0.30,
        assembly_cost_mass=0.05,
        testing_cost_prototype=0.50,
        testing_cost_pilot=0.10,
        testing_cost_mass=0.01,
        packaging_cost_prototype=0.30,
        packaging_cost_pilot=0.08,
        packaging_cost_mass=0.02,
    )


# =========================================================================
# PATH B: Mg-Air BIODEGRADABLE BATTERY
# =========================================================================

def bom_path_b() -> BOM:
    """Bill of Materials for Mg-Air Battery."""
    items = [
        LineItem("Mg foil (99.9%)", "Magnesium anode, 0.5mm thick, 5cm²",
                 0.5, "g", 4.00, 0.40, 0.04, is_biodegradable=True, source="Alfa Aesar / Goodfellow"),
        LineItem("Air cathode (carbon paper)", "Sigracet 35BC gas diffusion layer",
                 5, "cm²", 1.00, 0.15, 0.03, is_biodegradable=False, source="SGL Carbon"),
        LineItem("Cellulose separator", "CNF hydrogel between anode and cathode",
                 1, "pcs", 0.20, 0.03, 0.005, is_biodegradable=True, source="In-house casting"),
        LineItem("NaCl electrolyte", "0.1M NaCl in cellulose matrix",
                 0.1, "ml", 0.01, 0.001, 0.0002, is_biodegradable=True, source="Sigma"),
        LineItem("PTFE binder", "For cathode (60% dispersion)",
                 0.01, "ml", 0.06, 0.006, 0.001, is_biodegradable=False, source="Sigma"),
        LineItem("Compostable casing", "PHA housing with air vent for cathode",
                 1, "pcs", 0.80, 0.20, 0.05, is_biodegradable=True, source="Injection molded"),
        LineItem("Moisture barrier pouch", "Vacuum-sealed for shelf life",
                 1, "pcs", 0.10, 0.03, 0.01, is_biodegradable=False, source="Packaging supplier"),
        LineItem("Cu current collector tape", "Thin copper tape for electrode contact",
                 0.5, "cm", 0.10, 0.02, 0.005, is_biodegradable=False, source="3M / tesa"),
    ]
    return BOM(
        name="Mg-Air Biodegradable Battery",
        description="Mg anode + air cathode biodegradable primary cell, O2-independent operation",
        items=items,
        assembly_cost_prototype=1.50,
        assembly_cost_pilot=0.25,
        assembly_cost_mass=0.04,
        testing_cost_prototype=0.50,
        testing_cost_pilot=0.10,
        testing_cost_mass=0.01,
        packaging_cost_prototype=0.30,
        packaging_cost_pilot=0.08,
        packaging_cost_mass=0.02,
    )


# =========================================================================
# PATH C: PASSIVE NFC DEVKIT (No battery)
# =========================================================================

def bom_path_c() -> BOM:
    """Bill of Materials for Passive NFC DevKit (reader-powered, no battery)."""
    items = [
        LineItem("PCB (FR4, 2-layer)", "20×30mm sensor board with NFC antenna",
                 1, "pcs", 5.00, 1.50, 0.30, is_reusable=True, reusable_cycles=100,
                 is_biodegradable=False, source="PCBWay / JLCPCB"),
        LineItem("STM32L0 MCU", "Ultra-low-power Cortex-M0+",
                 1, "pcs", 3.00, 2.00, 0.80, is_reusable=True, reusable_cycles=100,
                 is_biodegradable=False, source="Mouser / Digikey"),
        LineItem("NFC tag IC (ST25DV04K)", "I²C NFC dynamic tag",
                 1, "pcs", 1.50, 1.00, 0.40, is_reusable=True, reusable_cycles=100,
                 is_biodegradable=False, source="Mouser / Digikey"),
        LineItem("FRAM (MB85RC256)", "32KB non-volatile FRAM",
                 1, "pcs", 2.00, 1.20, 0.50, is_reusable=True, reusable_cycles=100,
                 is_biodegradable=False, source="Mouser / Digikey"),
        LineItem("Capacitive sensor electrode", "Interdigitated copper on PCB (built-in)",
                 1, "pcs", 0.00, 0.00, 0.00, is_reusable=True, reusable_cycles=100,
                 is_biodegradable=False, source="Integrated in PCB"),
        LineItem("Boost converter (BQ25570)", "Ultra-low-power boost + MPPT",
                 1, "pcs", 2.50, 1.80, 0.70, is_reusable=True, reusable_cycles=100,
                 is_biodegradable=False, source="Mouser / Digikey"),
        LineItem("Passives (R, C, L)", "0402 resistors, capacitors, inductor",
                 15, "pcs", 0.75, 0.30, 0.08, is_reusable=True, reusable_cycles=100,
                 is_biodegradable=False, source="Mouser / Digikey"),
        LineItem("Temperature sensor (BME280)", "Temp/humidity/pressure sensor",
                 1, "pcs", 1.50, 1.00, 0.40, is_reusable=True, reusable_cycles=100,
                 is_biodegradable=False, source="Mouser / Digikey"),
        LineItem("Electrode contacts (spring)", "Pogo pins or spring contacts for pellet",
                 4, "pcs", 0.40, 0.20, 0.05, is_reusable=True, reusable_cycles=100,
                 is_biodegradable=False, source="Harwin / Mill-Max"),
        LineItem("Assembly (PCBA)", "SMT assembly including stencil, reflow",
                 1, "pcs", 8.00, 2.50, 0.60, is_reusable=True, reusable_cycles=100,
                 is_biodegradable=False, source="JLCPCB assembly / local EMS"),
    ]
    return BOM(
        name="Passive NFC DevKit (Reusable Electronics)",
        description="NFC-powered sensor board with capacitive moisture sensor, reusable over 100+ cycles",
        items=items,
        assembly_cost_prototype=0,
        assembly_cost_pilot=0,
        assembly_cost_mass=0,
        testing_cost_prototype=3.00,
        testing_cost_pilot=0.50,
        testing_cost_mass=0.10,
        packaging_cost_prototype=2.00,
        packaging_cost_pilot=0.50,
        packaging_cost_mass=0.15,
    )


# =========================================================================
# HYBRID: Reusable Electronics + Replaceable Bio-Pellet
# =========================================================================

def bom_hybrid() -> Tuple[BOM, BOM]:
    """Combined system: reusable electronics board + replaceable bio-pellet.
    
    Returns (electronics_bom, pellet_bom) as separate cost objects.
    """
    return bom_path_c(), bom_path_a()


# =========================================================================
# COMPARISON
# =========================================================================

def print_comparison(boms: Dict[str, BOM]):
    """Print side-by-side comparison of all BOMs."""
    tiers = [VolumeTier.PROTOTYPE, VolumeTier.PILOT, VolumeTier.MASS]
    tier_names = {VolumeTier.PROTOTYPE: "Prototype", VolumeTier.PILOT: "Pilot (1k)",
                  VolumeTier.MASS: "Mass (100k+)"}
    
    print(f"\n{'='*105}")
    print(f"  MANUFACTURING BOM — Bottom-Up Cost Comparison")
    print(f"{'='*105}")
    
    for tier in tiers:
        print(f"\n  📊 {tier_names[tier]} Scale")
        print(f"  {'-'*90}")
        print(f"  {'Product Path':35s}  {'Materials':>10}  {'Assembly':>10}  "
              f"{'Testing':>10}  {'Packaging':>10}  {'Total':>10}")
        print(f"  {'-'*90}")
        
        for name, bom in boms.items():
            bd = bom.breakdown_at_tier(tier)
            total = bom.total_at_tier(tier)
            print(f"  {name:35s}  €{bd['materials_total']:<8.4f}  "
                  f"€{bd['assembly']:<8.4f}  "
                  f"€{bom.testing_cost_prototype if tier==VolumeTier.PROTOTYPE else bom.testing_cost_pilot:<8.4f}  "
                  f"€{bom.packaging_cost_prototype if tier==VolumeTier.PROTOTYPE else bom.packaging_cost_pilot:<8.4f}  "
                  f"€{total:<8.4f}")
        
        # Cost per day
        print(f"  {'-'*90}")
        print(f"  {'Cost/day (7-day life)':35s}", end="")
        for name, bom in boms.items():
            total = bom.total_at_tier(tier)
            if "DevKit" in name:
                # DevKit is reusable, cost per day = total / 100 / 7
                cost_per_day = total / 100 / 7
            else:
                cost_per_day = total / 7
            print(f"  €{cost_per_day:<8.6f}", end="")
        print()
    
    # Biodegradable content comparison
    print(f"\n  ♻️  Biodegradable Content (Mass Production)")
    print(f"  {'-'*60}")
    for name, bom in boms.items():
        bd = bom.breakdown_at_tier(VolumeTier.MASS)
        bio = bd['biodegradable_pct']
        reusable = bd['reusable_pct']
        print(f"  {name:35s}  Bio: {bio:>5.1f}%  Reusable: {reusable:>5.1f}%")


def print_itemized_bom(bom: BOM, tier: VolumeTier = VolumeTier.PILOT):
    """Print detailed itemized BOM for one path."""
    name = {VolumeTier.PROTOTYPE: "Prototype", VolumeTier.PILOT: "Pilot (1k)",
            VolumeTier.MASS: "Mass (100k+)"}[tier]
    
    print(f"\n  📋 {bom.name} — {name} Scale")
    print(f"  {'='*80}")
    print(f"  {bom.description}")
    print(f"  {'-'*80}")
    print(f"  {'Item':35s}  {'Qty':>6}  {'Unit':>6}  {'Cost':>10}  {'Bio':>4}  {'Reuse':>6}")
    print(f"  {'-'*80}")
    
    for item in bom.items:
        cost = item.cost_at_tier(tier)
        bio = "♻️" if item.is_biodegradable else " "
        reuse = f"{item.reusable_cycles}x" if item.is_reusable else ""
        print(f"  {item.name:35s}  {item.qty:>6.1f}  {item.unit:>6}  "
              f"€{cost:<8.4f}  {bio:>4}  {reuse:>6}")
    
    print(f"  {'-'*80}")
    bd = bom.breakdown_at_tier(tier)
    print(f"  {'TOTAL':63s}  €{bd['total']:<8.4f}")
    print(f"  {'Materials':63s}  €{bd['materials_total']:<8.4f}")
    print(f"  {'Assembly':63s}  €{bd['assembly']:<8.4f}")
    print(f"  {'Biodegradable':63s}  {bd['biodegradable_pct']}%")
    print(f"  {'Reusable value':63s}  {bd['reusable_pct']}%")


# =========================================================================
# SENSITIVITY ANALYSIS
# =========================================================================

def run_sensitivity(bom: BOM, n_samples: int = 10000, seed: int = 42) -> Dict:
    """Monte Carlo sensitivity on cost assumptions."""
    rng = random.Random(seed)
    
    costs_proto = []
    costs_pilot = []
    costs_mass = []
    
    for _ in range(n_samples):
        # Perturb each line item cost by ±50% (log-normal)
        proto_sum = 0
        pilot_sum = 0
        mass_sum = 0
        
        for item in bom.items:
            pert = math.exp(rng.gauss(0, 0.25))  # log-normal, ~±28% 1-sigma
            proto_sum += item.cost_prototype * pert
            pilot_sum += item.cost_pilot * pert
            mass_sum += item.cost_mass * pert
        
        # Perturb assembly, testing, packaging
        for base in [bom.assembly_cost_prototype, bom.testing_cost_prototype, bom.packaging_cost_prototype]:
            proto_sum += base * math.exp(rng.gauss(0, 0.25))
        for base in [bom.assembly_cost_pilot, bom.testing_cost_pilot, bom.packaging_cost_pilot]:
            pilot_sum += base * math.exp(rng.gauss(0, 0.25))
        for base in [bom.assembly_cost_mass, bom.testing_cost_mass, bom.packaging_cost_mass]:
            mass_sum += base * math.exp(rng.gauss(0, 0.25))
        
        costs_proto.append(proto_sum)
        costs_pilot.append(pilot_sum)
        costs_mass.append(mass_sum)
    
    def stats(arr):
        arr_sorted = sorted(arr)
        n = len(arr_sorted)
        return {
            "mean": round(sum(arr) / n, 4),
            "p5": round(arr_sorted[int(n * 0.05)], 4),
            "p25": round(arr_sorted[int(n * 0.25)], 4),
            "p50": round(arr_sorted[int(n * 0.50)], 4),
            "p75": round(arr_sorted[int(n * 0.75)], 4),
            "p95": round(arr_sorted[int(n * 0.95)], 4),
            "std": round(math.sqrt(sum((x - sum(arr)/n)**2 for x in arr) / n), 4),
        }
    
    return {
        "bom": bom.name,
        "n_samples": n_samples,
        "prototype": stats(costs_proto),
        "pilot": stats(costs_pilot),
        "mass": stats(costs_mass),
    }


# =========================================================================
# MAIN
# =========================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="MykoVolt Manufacturing BOM")
    parser.add_argument("--path", type=str, choices=["a", "b", "c", "hybrid", "all"],
                        default="all", help="Product path to analyze")
    parser.add_argument("--json", type=str, help="Export to JSON file")
    parser.add_argument("--sensitivity", action="store_true", help="Run Monte Carlo sensitivity")
    parser.add_argument("--itemized", action="store_true", help="Show itemized BOM")
    args = parser.parse_args()
    
    boms = {}
    if args.path in ("a", "all", "hybrid"):
        boms["Path A: Air-Chimney Pressling"] = bom_path_a()
    if args.path in ("b", "all", "hybrid"):
        boms["Path B: Mg-Air Battery"] = bom_path_b()
    if args.path in ("c", "all", "hybrid"):
        boms["Path C: Passive NFC DevKit"] = bom_path_c()
    if args.path == "hybrid":
        # Hybrid = reusable electronics + replaceable pellet per cycle
        boms["Hybrid: DevKit + Pellet (1 cycle)"] = bom_path_c()
        # For hybrid, add one pellet cost
        pellet = bom_path_a()
        for item in pellet.items:
            boms["Hybrid: DevKit + Pellet (1 cycle)"].items.append(item)
        boms["Hybrid: DevKit + Pellet (1 cycle)"].assembly_cost_prototype += pellet.assembly_cost_prototype
        boms["Hybrid: DevKit + Pellet (1 cycle)"].assembly_cost_pilot += pellet.assembly_cost_pilot
        boms["Hybrid: DevKit + Pellet (1 cycle)"].assembly_cost_mass += pellet.assembly_cost_mass
    
    if args.path == "all":
        # Also add hybrid
        pellet = bom_path_a()
        devkit = bom_path_c()
        hybrid_items = list(devkit.items) + list(pellet.items)
        boms["Hybrid: DevKit + Pellet"] = BOM(
            name="Hybrid System (Reusable DevKit + Replaceable Pellet)",
            description="Reusable electronics board with replaceable fungal bio-pellet",
            items=hybrid_items,
            assembly_cost_prototype=devkit.assembly_cost_prototype + pellet.assembly_cost_prototype,
            assembly_cost_pilot=devkit.assembly_cost_pilot + pellet.assembly_cost_pilot,
            assembly_cost_mass=devkit.assembly_cost_mass + pellet.assembly_cost_mass,
            testing_cost_prototype=devkit.testing_cost_prototype,
            testing_cost_pilot=devkit.testing_cost_pilot,
            testing_cost_mass=devkit.testing_cost_mass,
            packaging_cost_prototype=devkit.packaging_cost_prototype,
            packaging_cost_pilot=devkit.packaging_cost_pilot,
            packaging_cost_mass=devkit.packaging_cost_mass,
        )
    
    if args.itemized:
        for name, bom in boms.items():
            print_itemized_bom(bom)
    else:
        print_comparison(boms)
    
    if args.sensitivity:
        print(f"\n\n{'='*90}")
        print(f"  COST SENSITIVITY (Monte Carlo, {10000} samples, ±50% perturbation)")
        print(f"{'='*90}")
        
        for name, bom in boms.items():
            sens = run_sensitivity(bom)
            print(f"\n  📊 {sens['bom']}")
            print(f"  {'Scale':15s}  {'Mean':>8}  {'P5':>8}  {'P25':>8}  "
                  f"{'P50':>8}  {'P75':>8}  {'P95':>8}  {'Std':>8}")
            print(f"  {'-'*70}")
            for scale in ["prototype", "pilot", "mass"]:
                s = sens[scale]
                print(f"  {scale:15s}  €{s['mean']:<7.4f}  €{s['p5']:<7.4f}  "
                      f"€{s['p25']:<7.4f}  €{s['p50']:<7.4f}  €{s['p75']:<7.4f}  "
                      f"€{s['p95']:<7.4f}  €{s['std']:<7.4f}")
    
    if args.json:
        import json
        data = {}
        for name, bom in boms.items():
            data[name] = {}
            for tier in VolumeTier:
                data[name][tier.value] = bom.breakdown_at_tier(tier)
        with open(args.json, "w") as f:
            json.dump(data, f, indent=2)
        print(f"\n  Results saved to {args.json}")
