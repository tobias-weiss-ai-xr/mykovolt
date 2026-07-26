#!/usr/bin/env python3
"""
Product Concept Explorer — Fungal Bio-Battery Application Viability Scanner

Scans product concepts against battery physics (power, energy, O2, form factor)
and outputs a feasibility ranking for each.

Usage:
  python3 product_explorer.py                    # Full scan
  python3 product_explorer.py --list             # List all concepts
  python3 product_explorer.py --concept "deep-sea"  # Deep-dive one concept
  python3 product_explorer.py --novel-only       # Only the novel (beyond 15) concepts
"""

import math
import json
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Tuple, Dict
from enum import Enum

# =========================================================================
# BATTERY PHYSICS — what the fungal bio-battery can actually deliver
# =========================================================================

@dataclass
class BatteryCapability:
    """What the battery can deliver, at different confidence levels."""
    # Demonstrated (Empa 2024, TRL 2)
    power_density_uw_cm2_empa: float = 12.5
    # Simulation target (Bayesian Optimization, TRL 2 unvalidated)
    power_density_uw_cm2_target: float = 260.0
    # Conservative estimate (50% of target, typical real-world derating)
    power_density_uw_cm2_conservative: float = 50.0
    
    area_cm2: float = 2.0       # Typical pellet area
    voltage_nominal: float = 0.45  # V
    voltage_boosted: float = 3.3   # V (via boost converter)
    
    # O2 requirements
    needs_oxygen: bool = True     # Fungal MFC needs O2 at cathode
    depth_limit_cm: float = 3.0   # Max depth without O2 mitigation (chimney/Mg-air)
    
    # Lifetime
    lifetime_days_empa: float = 2.0   # At Empa power
    lifetime_days_target: float = 7.0  # At target power
    degradation_per_day_pct: float = 2.0
    
    # Cost
    cost_pellet_only_euro: float = 0.15
    cost_pellet_with_chimney_euro: float = 0.30
    cost_mg_air_euro: float = 0.35
    cost_pcb_nfc_euro: float = 0.20
    
    @property
    def power_uw_empa(self) -> float:
        return self.power_density_uw_cm2_empa * self.area_cm2
    
    @property
    def power_uw_target(self) -> float:
        return self.power_density_uw_cm2_target * self.area_cm2
    
    @property
    def power_uw_conservative(self) -> float:
        return self.power_density_uw_cm2_conservative * self.area_cm2


# =========================================================================
# PRODUCT CONCEPT MODEL
# =========================================================================

class TechReadiness(Enum):
    CONCEPT = 1      # Just an idea
    PLAUSIBLE = 2    # Physics says it could work
    FEASIBLE = 3     # Simulated and passes energy budget
    VIABLE = 4       # All known constraints satisfied
    PROTOTYPE = 5    # Built and tested
    PRODUCT = 6      # Ready for market

class O2Strategy(Enum):
    SURFACE = "surface"           # Operates at/near surface (<3cm)
    CHIMNEY = "air_chimney"       # Air chimney for O2 delivery
    MG_AIR = "mg_air_backup"      # Mg-air battery (O2 independent)
    PASSIVE_NFC = "passive_nfc"   # No battery, reader-powered
    HYBRID = "hybrid"             # Uses fungal + Mg-air in combination
    ANAEROBIC = "anaerobic"       # Uses alternative electron acceptor


@dataclass
class ProductConcept:
    """A product concept that the fungal battery could power."""
    id: str
    name: str
    description: str
    category: str                  # agri, env, med, logistik, consumer, industrial
    
    # Power requirements
    avg_power_uw: float            # Average power draw in µW
    peak_power_uw: float           # Peak power draw in µW
    energy_per_day_uj: float       # Daily energy consumption in µJ
    target_lifetime_days: float    # Required operational days
    
    # Deployment constraints
    burial_depth_cm: float         # How deep it goes (0 = surface)
    soil_contact: bool             # Needs to be in soil?
    temperature_min_c: float = 5
    temperature_max_c: float = 40
    
    # O2 strategy
    o2_strategy: O2Strategy = O2Strategy.CHIMNEY
    
    # Market
    tam_euro: float = 0            # Total Addressable Market €
    maturity_years: int = 5        # Years to market
    competition_level: str = "medium"  # low/medium/high
    novelty: str = "existing"  # "existing" or "novel"
    
    # Simulation results (filled by scanner)
    feasible_empa: bool = False
    feasible_target: bool = False
    feasible_conservative: bool = False
    trl: TechReadiness = TechReadiness.CONCEPT
    score: float = 0.0
    notes: str = ""


# =========================================================================
# ALL PRODUCT CONCEPTS — including the 15 already listed + 15 novel ones
# =========================================================================

def all_concepts() -> List[ProductConcept]:
    """Define all product concepts with their power requirements."""
    concepts = []
    
    # ── EXISTING 15 USE CASES (from README) ──
    
    # Phase 1: DevKit
    concepts.append(ProductConcept(
        id="soil-moisture", name="Soil Moisture Sensor",
        description="Buried capacitive sensor for precision agriculture moisture monitoring",
        category="agri", avg_power_uw=5.8, peak_power_uw=3000,
        energy_per_day_uj=504000, target_lifetime_days=7,
        burial_depth_cm=10, soil_contact=True,
        o2_strategy=O2Strategy.CHIMNEY, tam_euro=1.2e9, maturity_years=3,
        competition_level="high", novelty="existing"))
    
    concepts.append(ProductConcept(
        id="compost-monitor", name="Compost Pile Monitor",
        description="Internal compost temperature/moisture sensor, works in hot moist environment",
        category="env", avg_power_uw=5.8, peak_power_uw=3000,
        energy_per_day_uj=504000, target_lifetime_days=14,
        burial_depth_cm=30, soil_contact=True,
        o2_strategy=O2Strategy.CHIMNEY, tam_euro=200e6, maturity_years=3,
        competition_level="low", novelty="existing"))
    
    concepts.append(ProductConcept(
        id="concrete-cure", name="Concrete Curing Monitor",
        description="Embedded during pouring, monitors temperature/humidity during curing",
        category="industrial", avg_power_uw=2.0, peak_power_uw=1500,
        energy_per_day_uj=180000, target_lifetime_days=28,
        burial_depth_cm=5, soil_contact=False,
        o2_strategy=O2Strategy.CHIMNEY, tam_euro=500e6, maturity_years=4,
        competition_level="medium", novelty="existing"))
    
    concepts.append(ProductConcept(
        id="cold-chain", name="Cold-Chain Logger",
        description="Temperature logger for food/pharma shipping, compostable after use",
        category="logistik", avg_power_uw=3.0, peak_power_uw=2000,
        energy_per_day_uj=260000, target_lifetime_days=14,
        burial_depth_cm=0, soil_contact=False,
        o2_strategy=O2Strategy.MG_AIR, tam_euro=800e6, maturity_years=3,
        competition_level="high", novelty="existing"))
    
    concepts.append(ProductConcept(
        id="edu-kit", name="Research/Education DevKit",
        description="Open-hardware fungal MFC platform for labs and teaching",
        category="consumer", avg_power_uw=0, peak_power_uw=0,
        energy_per_day_uj=0, target_lifetime_days=30,
        burial_depth_cm=0, soil_contact=False,
        o2_strategy=O2Strategy.PASSIVE_NFC, tam_euro=50e6, maturity_years=1,
        competition_level="low", novelty="existing"))
    
    # Phase 2: Field Pilot
    concepts.append(ProductConcept(
        id="forestry", name="Forestry Under-Canopy Sensor",
        description="Soil moisture/temperature in dense forest where solar fails",
        category="env", avg_power_uw=5.8, peak_power_uw=3000,
        energy_per_day_uj=504000, target_lifetime_days=30,
        burial_depth_cm=5, soil_contact=True,
        o2_strategy=O2Strategy.CHIMNEY, tam_euro=300e6, maturity_years=4,
        competition_level="medium", novelty="existing"))
    
    concepts.append(ProductConcept(
        id="permafrost", name="Permafrost Monitoring",
        description="Continuous year-round temperature monitoring in Arctic/polar regions",
        category="env", avg_power_uw=2.0, peak_power_uw=1000,
        energy_per_day_uj=180000, target_lifetime_days=365,
        burial_depth_cm=10, soil_contact=True,
        o2_strategy=O2Strategy.MG_AIR, tam_euro=150e6, maturity_years=5,
        competition_level="medium", novelty="existing"))
    
    concepts.append(ProductConcept(
        id="landfill", name="Landfill/Waste Monitor",
        description="Gas/temperature monitoring inside waste piles, no retrieval needed",
        category="env", avg_power_uw=5.8, peak_power_uw=3000,
        energy_per_day_uj=504000, target_lifetime_days=30,
        burial_depth_cm=50, soil_contact=True,
        o2_strategy=O2Strategy.MG_AIR, tam_euro=400e6, maturity_years=4,
        competition_level="low", novelty="existing"))
    
    concepts.append(ProductConcept(
        id="wildlife-tag", name="Wildlife Tracking Tag",
        description="Biodegradable GPS-less tag for ecological studies, safe if ingested",
        category="env", avg_power_uw=1.0, peak_power_uw=500,
        energy_per_day_uj=90000, target_lifetime_days=60,
        burial_depth_cm=0, soil_contact=False,
        o2_strategy=O2Strategy.MG_AIR, tam_euro=100e6, maturity_years=4,
        competition_level="medium", novelty="existing"))
    
    concepts.append(ProductConcept(
        id="smart-packaging", name="Smart Packaging",
        description="Temperature abuse indicator for food/pharma logistics",
        category="logistik", avg_power_uw=0.5, peak_power_uw=100,
        energy_per_day_uj=45000, target_lifetime_days=21,
        burial_depth_cm=0, soil_contact=False,
        o2_strategy=O2Strategy.PASSIVE_NFC, tam_euro=2e9, maturity_years=3,
        competition_level="high", novelty="existing"))
    
    # Phase 3: Commercial
    concepts.append(ProductConcept(
        id="agri-network", name="Agricultural Sensor Network",
        description="Dense deployment (100+/ha) for row crops, vineyards, orchards",
        category="agri", avg_power_uw=5.8, peak_power_uw=3000,
        energy_per_day_uj=504000, target_lifetime_days=7,
        burial_depth_cm=10, soil_contact=True,
        o2_strategy=O2Strategy.CHIMNEY, tam_euro=3e9, maturity_years=5,
        competition_level="high", novelty="existing"))
    
    concepts.append(ProductConcept(
        id="medical-disposable", name="Medical Disposable Sensor",
        description="Single-use wound dressing/diagnostics with biodegradable battery",
        category="med", avg_power_uw=10.0, peak_power_uw=5000,
        energy_per_day_uj=864000, target_lifetime_days=3,
        burial_depth_cm=0, soil_contact=False,
        o2_strategy=O2Strategy.MG_AIR, tam_euro=5e9, maturity_years=5,
        competition_level="medium", novelty="existing"))
    
    concepts.append(ProductConcept(
        id="landmine", name="Landmine/UXO Monitoring",
        description="Long-term passive monitoring of munitions sites, biodegradable (no cleanup)",
        category="env", avg_power_uw=1.0, peak_power_uw=500,
        energy_per_day_uj=90000, target_lifetime_days=365,
        burial_depth_cm=5, soil_contact=True,
        o2_strategy=O2Strategy.MG_AIR, tam_euro=2e9, maturity_years=6,
        competition_level="low", novelty="existing"))
    
    concepts.append(ProductConcept(
        id="soil-carbon", name="Soil Carbon Verification",
        description="Buried sensors verify carbon sequestration for carbon credits",
        category="agri", avg_power_uw=2.0, peak_power_uw=1500,
        energy_per_day_uj=180000, target_lifetime_days=180,
        burial_depth_cm=20, soil_contact=True,
        o2_strategy=O2Strategy.MG_AIR, tam_euro=10e9, maturity_years=5,
        competition_level="medium", novelty="existing"))
    
    concepts.append(ProductConcept(
        id="smart-city", name="Smart City Infrastructure",
        description="Embedded in soil/concrete for flood detection, utility monitoring",
        category="industrial", avg_power_uw=5.8, peak_power_uw=3000,
        energy_per_day_uj=504000, target_lifetime_days=30,
        burial_depth_cm=10, soil_contact=True,
        o2_strategy=O2Strategy.CHIMNEY, tam_euro=5e9, maturity_years=6,
        competition_level="high", novelty="existing"))
    
    # ═══════════════════════════════════════════════════════════════════
    # NOVEL PRODUCT CONCEPTS — beyond the 15 listed use cases
    # ═══════════════════════════════════════════════════════════════════
    
    concepts.append(ProductConcept(
        id="seed-coating", name="Fungal Battery Seed Coating",
        description="Coat seeds with fungal spores + conductive ink — as seed germinates, it powers an NFC sensor for germination rate monitoring",
        category="agri", avg_power_uw=0.1, peak_power_uw=50,
        energy_per_day_uj=9000, target_lifetime_days=14,
        burial_depth_cm=3, soil_contact=True,
        o2_strategy=O2Strategy.SURFACE, tam_euro=500e6, maturity_years=5,
        competition_level="low", novelty="novel"))
    
    concepts.append(ProductConcept(
        id="smart-bandage", name="Smart Wound Dressing",
        description="Bio-battery powered pH/temperature sensor in a bandage — detects infection before visible signs. Entire dressing compostable.",
        category="med", avg_power_uw=5.0, peak_power_uw=2000,
        energy_per_day_uj=432000, target_lifetime_days=5,
        burial_depth_cm=0, soil_contact=False,
        o2_strategy=O2Strategy.SURFACE, tam_euro=3e9, maturity_years=5,
        competition_level="medium", novelty="novel"))
    
    concepts.append(ProductConcept(
        id="food-spoilage", name="Food Spoilage Indicator",
        description="Fungal battery that activates when food spoils — uses spoilage gases (NH3, H2S) as fuel. Integrated into packaging.",
        category="logistik", avg_power_uw=0.5, peak_power_uw=100,
        energy_per_day_uj=45000, target_lifetime_days=30,
        burial_depth_cm=0, soil_contact=False,
        o2_strategy=O2Strategy.SURFACE, tam_euro=4e9, maturity_years=4,
        competition_level="low", novelty="novel"))
    
    concepts.append(ProductConcept(
        id="mycelium-structural", name="Mycelium Structural Battery",
        description="Load-bearing mycelium composite panel that also generates power. Building material = battery. Self-powered smart walls.",
        category="industrial", avg_power_uw=50.0, peak_power_uw=10000,
        energy_per_day_uj=4.3e6, target_lifetime_days=365,
        burial_depth_cm=0, soil_contact=False,
        o2_strategy=O2Strategy.SURFACE, tam_euro=2e9, maturity_years=7,
        competition_level="low", novelty="novel"))
    
    concepts.append(ProductConcept(
        id="marine-sensor", name="Marine Biodegradable Sensor",
        description="Ocean-deployed temperature/current sensor that composts after mission. No plastic pollution from sensor buoys.",
        category="env", avg_power_uw=2.0, peak_power_uw=1000,
        energy_per_day_uj=180000, target_lifetime_days=30,
        burial_depth_cm=0, soil_contact=False,
        o2_strategy=O2Strategy.MG_AIR, tam_euro=800e6, maturity_years=5,
        competition_level="medium", novelty="novel"))
    
    concepts.append(ProductConcept(
        id="disaster-drone", name="Drone-Dropped Disaster Sensor Network",
        description="Air-droppable biodegradable sensors for disaster zones. No retrieval needed, no cleanup. Maps fire/flood/quake conditions.",
        category="env", avg_power_uw=5.8, peak_power_uw=3000,
        energy_per_day_uj=504000, target_lifetime_days=14,
        burial_depth_cm=0, soil_contact=False,
        o2_strategy=O2Strategy.SURFACE, tam_euro=1e9, maturity_years=4,
        competition_level="medium", novelty="novel"))
    
    concepts.append(ProductConcept(
        id="living-wall", name="Living Building Material",
        description="Mycelium-based wall panel with embedded fungal MFC. Generates power from ambient moisture. Self-powered smart building.",
        category="industrial", avg_power_uw=20.0, peak_power_uw=5000,
        energy_per_day_uj=1.7e6, target_lifetime_days=365,
        burial_depth_cm=0, soil_contact=False,
        o2_strategy=O2Strategy.SURFACE, tam_euro=5e9, maturity_years=7,
        competition_level="low", novelty="novel"))
    
    concepts.append(ProductConcept(
        id="health-patch", name="Compostable Wearable Health Patch",
        description="Biodegradable fitness/health monitor patch. Tracks heart rate, temperature, sweat chemistry. Composts after use.",
        category="med", avg_power_uw=15.0, peak_power_uw=5000,
        energy_per_day_uj=1.3e6, target_lifetime_days=7,
        burial_depth_cm=0, soil_contact=False,
        o2_strategy=O2Strategy.SURFACE, tam_euro=10e9, maturity_years=6,
        competition_level="high", novelty="novel"))
    
    concepts.append(ProductConcept(
        id="space-habitat", name="Space Habitat Bio-Battery",
        description="Bioregenerative power system for space habitats. Uses human organic waste as fuel. Combines waste management + power generation.",
        category="industrial", avg_power_uw=100.0, peak_power_uw=50000,
        energy_per_day_uj=8.6e6, target_lifetime_days=365,
        burial_depth_cm=0, soil_contact=False,
        o2_strategy=O2Strategy.ANAEROBIC, tam_euro=50e6, maturity_years=10,
        competition_level="low", novelty="novel"))
    
    concepts.append(ProductConcept(
        id="smart-plantpot", name="Smart Plant Pot",
        description="Self-powered plant pot that monitors soil moisture, light, and temperature. NFC readout. No batteries to change.",
        category="consumer", avg_power_uw=2.0, peak_power_uw=1000,
        energy_per_day_uj=180000, target_lifetime_days=90,
        burial_depth_cm=5, soil_contact=True,
        o2_strategy=O2Strategy.CHIMNEY, tam_euro=200e6, maturity_years=3,
        competition_level="medium", novelty="novel"))
    
    concepts.append(ProductConcept(
        id="fungal-art", name="Living Art / Bio-Installation",
        description="Mycelium-based art installation with embedded fungal MFC powering LEDs. Changes color as fungi grow. Living, breathing art.",
        category="consumer", avg_power_uw=50.0, peak_power_uw=20000,
        energy_per_day_uj=4.3e6, target_lifetime_days=60,
        burial_depth_cm=0, soil_contact=False,
        o2_strategy=O2Strategy.SURFACE, tam_euro=50e6, maturity_years=2,
        competition_level="low", novelty="novel"))
    
    concepts.append(ProductConcept(
        id="agri-drone-seed", name="Drone Seed + Sensor Drop",
        description="Seed pod with integrated fungal sensor. Drone drops over fields. Seed germinates, sensor monitors soil, everything biodegrades.",
        category="agri", avg_power_uw=1.0, peak_power_uw=500,
        energy_per_day_uj=90000, target_lifetime_days=30,
        burial_depth_cm=3, soil_contact=True,
        o2_strategy=O2Strategy.SURFACE, tam_euro=800e6, maturity_years=5,
        competition_level="low", novelty="novel"))
    
    concepts.append(ProductConcept(
        id="game-tag", name="Biodegradable Game Tag",
        description="Wildlife management tag for hunting/ecology. Biodegradable — falls off naturally, no retrieval, no plastic in nature.",
        category="env", avg_power_uw=0.5, peak_power_uw=200,
        energy_per_day_uj=45000, target_lifetime_days=90,
        burial_depth_cm=0, soil_contact=False,
        o2_strategy=O2Strategy.SURFACE, tam_euro=100e6, maturity_years=4,
        competition_level="low", novelty="novel"))
    
    concepts.append(ProductConcept(
        id="compost-air", name="Compost Facility Air Quality Sensor",
        description="Monitors H2S, CH4, NH3 inside compost facilities. Self-powered from compost gases. No wiring in explosive environment.",
        category="env", avg_power_uw=3.0, peak_power_uw=1500,
        energy_per_day_uj=260000, target_lifetime_days=60,
        burial_depth_cm=0, soil_contact=False,
        o2_strategy=O2Strategy.SURFACE, tam_euro=300e6, maturity_years=4,
        competition_level="low", novelty="novel"))
    
    concepts.append(ProductConcept(
        id="pet-tag", name="Biodegradable Pet Tracker",
        description="Short-range pet location tag that biodegrades if lost. NFC readout, compostable. No toxic battery in environment.",
        category="consumer", avg_power_uw=1.0, peak_power_uw=500,
        energy_per_day_uj=90000, target_lifetime_days=30,
        burial_depth_cm=0, soil_contact=False,
        o2_strategy=O2Strategy.SURFACE, tam_euro=500e6, maturity_years=4,
        competition_level="high", novelty="novel"))
    
    return concepts


# =========================================================================
# VIABILITY SCANNER
# =========================================================================

@dataclass
class ScanResult:
    concept_id: str
    concept_name: str
    category: str
    novelty: str
    
    # Feasibility flags
    power_feasible: bool         # Power supply meets demand
    energy_feasible: bool        # Energy budget works
    o2_feasible: bool            # O2 strategy works
    form_feasible: bool          # Form factor works
    temp_feasible: bool          # Temperature range works
    
    # Scores
    overall_score: float         # 0-1 combined feasibility
    market_score: float          # 0-1 market attractiveness
    differentiation_score: float # 0-1 uniqueness vs alternatives
    strategic_score: float       # 0-1 fits MykoVolt strategy
    
    # Economics
    bom_cost_euro: float         # Bill of materials cost
    potential_margin_pct: float  # Gross margin estimate
    
    # Verdict
    verdict: str                 # GO / MAYBE / NO-GO
    primary_risk: str            # Biggest risk
    recommended_path: str        # Which battery path
    notes: str


class ProductScanner:
    """Evaluates product concepts against battery physics and market criteria."""
    
    def __init__(self, battery: Optional[BatteryCapability] = None):
        self.battery = battery or BatteryCapability()
    
    def scan(self, concept: ProductConcept) -> ScanResult:
        """Evaluate one product concept."""
        b = self.battery
        
        # ── 1. Power feasibility ──
        # What power can we deliver at the concept's depth?
        if concept.burial_depth_cm > b.depth_limit_cm and b.needs_oxygen:
            # Deep burial with O2-sensitive battery
            if concept.o2_strategy == O2Strategy.MG_AIR:
                # Mg-air works at depth (O2 independent, uses water reduction)
                power_available = b.power_uw_conservative * 0.8  # derated for depth
            elif concept.o2_strategy in (O2Strategy.CHIMNEY, O2Strategy.HYBRID):
                power_available = b.power_uw_conservative * 0.5  # chimney derating
            elif concept.o2_strategy == O2Strategy.SURFACE:
                power_available = b.power_uw_conservative * 0.2  # surface only, deep is bad
            else:
                power_available = 0
        else:
            power_available = b.power_uw_conservative
        
        # Also check what power is available if concept has no soil contact
        if not concept.soil_contact:
            # Surface operation: no O2 limitation
            power_available = max(power_available, b.power_uw_conservative)
        
        # Passive NFC: no battery power needed at all
        if concept.o2_strategy == O2Strategy.PASSIVE_NFC:
            power_available = float('inf')  # reader-powered
        
        power_feasible = power_available >= concept.avg_power_uw * 1.2  # 20% margin
        
        # ── 2. Energy feasibility ──
        daily_supply_uj = power_available * 24 * 3600
        # Adjust for degradation
        total_supply = 0
        for d in range(int(concept.target_lifetime_days)):
            total_supply += daily_supply_uj * (1 - b.degradation_per_day_pct/100) ** d
        
        total_demand = concept.energy_per_day_uj * concept.target_lifetime_days
        energy_feasible = total_supply >= total_demand
        
        # ── 3. O2 feasibility ──
        if concept.burial_depth_cm > b.depth_limit_cm and b.needs_oxygen:
            if concept.o2_strategy in (O2Strategy.MG_AIR, O2Strategy.PASSIVE_NFC, O2Strategy.ANAEROBIC):
                o2_feasible = True
            elif concept.o2_strategy == O2Strategy.CHIMNEY:
                o2_feasible = concept.burial_depth_cm <= 30  # chimney works to ~30cm
            elif concept.o2_strategy == O2Strategy.HYBRID:
                o2_feasible = True
            else:
                o2_feasible = False
        else:
            o2_feasible = True
        
        # ── 4. Form factor feasibility ──
        # Passive concepts always work
        if concept.o2_strategy == O2Strategy.PASSIVE_NFC:
            form_feasible = True
        elif concept.burial_depth_cm <= b.depth_limit_cm or not concept.soil_contact:
            form_feasible = True
        elif concept.o2_strategy == O2Strategy.CHIMNEY:
            form_feasible = concept.burial_depth_cm <= 50  # very long chimneys impractical
        elif concept.o2_strategy == O2Strategy.MG_AIR:
            form_feasible = True  # Mg-air is compact
        else:
            form_feasible = False
        
        # ── 5. Temperature feasibility ──
        # Fungal MFC: optimal 20-30°C, works 10-40°C, dies <5°C or >45°C
        if concept.o2_strategy == O2Strategy.MG_AIR:
            temp_feasible = True  # Mg-air works across broader range
        elif concept.o2_strategy == O2Strategy.PASSIVE_NFC:
            temp_feasible = True  # no battery
        else:
            temp_feasible = (concept.temperature_min_c >= 5 and 
                            concept.temperature_max_c <= 40)
        
        # ── Overall score ──
        n_pass = sum([power_feasible, energy_feasible, o2_feasible, form_feasible, temp_feasible])
        overall_score = n_pass / 5.0
        
        # Market score
        tam_score = min(1.0, concept.tam_euro / 10e9)  # Normalize to €10B
        competition_penalty = {"low": 0.0, "medium": 0.15, "high": 0.30}[concept.competition_level]
        maturity_penalty = max(0, (concept.maturity_years - 3) / 10)  # Longer = riskier
        market_score = max(0, tam_score * 0.6 + (1 - competition_penalty) * 0.4) * (1 - maturity_penalty * 0.3)
        
        # Differentiation score: how unique is this application for MykoVolt?
        # Passive NFC concepts are less differentiated (many alternatives)
        if concept.o2_strategy == O2Strategy.PASSIVE_NFC:
            diff_score = 0.3
        elif concept.o2_strategy == O2Strategy.MG_AIR:
            diff_score = 0.6  # Good but Mg-air has prior art
        elif concept.novelty == "novel":
            diff_score = 0.85  # Novel concepts are more differentiated
        else:
            diff_score = 0.7  # Existing fungal concepts
        
        # Strategic fit
        # Concepts that leverage biodegradability + active sensing score highest
        strategic_score = (
            0.3 * (1 if concept.soil_contact else 0) +
            0.3 * (1 if concept.target_lifetime_days >= 7 else concept.target_lifetime_days / 7) +
            0.2 * (1 if concept.novelty == "novel" else 0.5) +
            0.2 * min(1, concept.tam_euro / 2e9)
        )
        
        # Combined score
        score = overall_score * 0.35 + market_score * 0.25 + diff_score * 0.20 + strategic_score * 0.20
        
        # ── Verdict ──
        if overall_score >= 0.8 and score >= 0.6:
            verdict = "GO"
        elif overall_score >= 0.4:
            verdict = "MAYBE"
        else:
            verdict = "NO-GO"
        
        # ── Primary risk ──
        risks = []
        if not power_feasible:
            risks.append(f"Power shortfall: needs {concept.avg_power_uw}µW, can deliver ~{power_available:.0f}µW")
        if not energy_feasible:
            risks.append(f"Energy budget fails by {total_supply/total_demand:.0%}")
        if not o2_feasible:
            risks.append(f"O2 starvation at {concept.burial_depth_cm}cm depth")
        if not temp_feasible:
            risks.append(f"Temperature range {concept.temperature_min_c}-{concept.temperature_max_c}°C exceeds fungal limits")
        primary_risk = risks[0] if risks else "Market adoption"
        
        # ── Recommended path ──
        if concept.o2_strategy == O2Strategy.PASSIVE_NFC:
            path = "Passive NFC (no battery needed)"
        elif concept.o2_strategy == O2Strategy.MG_AIR:
            path = "Mg-Air battery"
        elif concept.burial_depth_cm <= b.depth_limit_cm:
            path = "Surface fungal MFC"
        else:
            path = "Air-Chimney fungal MFC"
        
        # ── BOM cost ──
        if concept.o2_strategy == O2Strategy.PASSIVE_NFC:
            bom = b.cost_pcb_nfc_euro + 0.05  # just NFC tag + PCB
        elif concept.o2_strategy == O2Strategy.MG_AIR:
            bom = b.cost_mg_air_euro + b.cost_pcb_nfc_euro + 0.10  # Mg-air + PCB + sensor
        elif concept.burial_depth_cm <= b.depth_limit_cm:
            bom = b.cost_pellet_only_euro + b.cost_pcb_nfc_euro + 0.10
        else:
            bom = b.cost_pellet_with_chimney_euro + b.cost_pcb_nfc_euro + 0.10
        
        # Margin estimate (assuming €5-35 consumer price depending on complexity)
        est_price = 35.0 if concept.category in ("med", "industrial") else 15.0
        margin_pct = max(0, (est_price - bom) / est_price * 100)
        
        return ScanResult(
            concept_id=concept.id,
            concept_name=concept.name,
            category=concept.category,
            novelty=concept.novelty,
            power_feasible=power_feasible,
            energy_feasible=energy_feasible,
            o2_feasible=o2_feasible,
            form_feasible=form_feasible,
            temp_feasible=temp_feasible,
            overall_score=overall_score,
            market_score=market_score,
            differentiation_score=diff_score,
            strategic_score=strategic_score,
            bom_cost_euro=bom,
            potential_margin_pct=margin_pct,
            verdict=verdict,
            primary_risk=primary_risk,
            recommended_path=path,
            notes=f"{'✅' if power_feasible else '❌'} Power: {power_available:.0f}µW avail vs {concept.avg_power_uw}µW need"
        )
    
    def scan_all(self, concepts: List[ProductConcept]) -> List[ScanResult]:
        """Scan all concepts and return sorted results."""
        results = [self.scan(c) for c in concepts]
        results.sort(key=lambda r: (r.overall_score, r.market_score), reverse=True)
        return results


# =========================================================================
# DISPLAY
# =========================================================================

def print_results(results: List[ScanResult], title: str = "PRODUCT CONCEPT SCAN RESULTS"):
    """Print formatted scan results."""
    print(f"\n{'='*120}")
    print(f"  {title}")
    print(f"{'='*120}")
    
    hdr = (f"  {'Verdict':>6}  {'Score':>5}  {'Concept':30s}  {'Category':12s}  "
           f"{'Novelty':8s}  {'Power':>5}  {'Energy':>5}  {'O2':>5}  {'Form':>5}  "
           f"{'Temp':>5}  {'BOM €':>7}  {'Risk'}")
    print(hdr)
    print("  " + "-" * 112)
    
    for r in results:
        icon = {"GO": "🟢", "MAYBE": "🟡", "NO-GO": "🔴"}[r.verdict]
        p = "✅" if r.power_feasible else "❌"
        e = "✅" if r.energy_feasible else "❌"
        o = "✅" if r.o2_feasible else "❌"
        f = "✅" if r.form_feasible else "❌"
        t = "✅" if r.temp_feasible else "❌"
        
        name = r.concept_name[:28]
        risk_short = r.primary_risk[:28]
        
        print(f"  {icon}{r.verdict:>5}  {r.overall_score:.2f}  {name:28s}  "
              f"{r.category:12s}  {r.novelty:8s}  "
              f"{p:>5}  {e:>5}  {o:>5}  {f:>5}  {t:>5}  "
              f"€{r.bom_cost_euro:<5.2f}  {risk_short}")
    
    print(f"\n  Summary: {sum(1 for r in results if r.verdict=='GO')} GO | "
          f"{sum(1 for r in results if r.verdict=='MAYBE')} MAYBE | "
          f"{sum(1 for r in results if r.verdict=='NO-GO')} NO-GO "
          f"(of {len(results)} concepts)")


def print_top_go_results(results: List[ScanResult], n: int = 10):
    """Print detailed view of top GO concepts."""
    go = [r for r in results if r.verdict == "GO"][:n]
    if not go:
        print("\n  No GO concepts found.")
        return
    
    print(f"\n{'='*90}")
    print(f"  TOP {len(go)} GO CONCEPTS — Detailed")
    print(f"{'='*90}")
    
    for i, r in enumerate(go, 1):
        print(f"\n  {i}. {r.concept_name} ({r.category}, {r.novelty})")
        print(f"     Verdict:        🟢 GO (score: {r.overall_score:.2f})")
        print(f"     Market score:   {r.market_score:.2f}")
        print(f"     Differentiation:{r.differentiation_score:.2f}")
        print(f"     Strategic fit:  {r.strategic_score:.2f}")
        print(f"     BOM cost:       €{r.bom_cost_euro:.2f}")
        print(f"     Est. margin:    {r.potential_margin_pct:.0f}%")
        print(f"     Recommended:    {r.recommended_path}")
        print(f"     Primary risk:   {r.primary_risk}")
        print(f"     {r.notes}")


def print_concept_drilldown(concept: ProductConcept, result: ScanResult):
    """Deep-dive into a single concept."""
    print(f"\n{'='*70}")
    print(f"  DEEP DIVE: {concept.name}")
    print(f"{'='*70}")
    print(f"  ID:          {concept.id}")
    print(f"  Category:    {concept.category}")
    print(f"  Novelty:     {concept.novelty}")
    print(f"  Description: {concept.description}")
    print(f"\n  ⚡ Power Requirements:")
    print(f"     Avg power:     {concept.avg_power_uw} µW")
    print(f"     Peak power:    {concept.peak_power_uw} µW")
    print(f"     Daily energy:  {concept.energy_per_day_uj:,.0f} µJ")
    print(f"     Target life:   {concept.target_lifetime_days} days")
    print(f"\n  🌍 Deployment:")
    print(f"     Depth:         {concept.burial_depth_cm} cm")
    print(f"     Soil contact:  {concept.soil_contact}")
    print(f"     Temp range:    {concept.temperature_min_c}-{concept.temperature_max_c}°C")
    print(f"     O2 strategy:   {concept.o2_strategy.value}")
    print(f"\n  📊 Feasibility:")
    print(f"     Power:   {'✅' if result.power_feasible else '❌'} {result.notes.split('Power:')[1] if 'Power:' in result.notes else ''}")
    print(f"     Energy:  {'✅' if result.energy_feasible else '❌'}")
    print(f"     O2:      {'✅' if result.o2_feasible else '❌'}")
    print(f"     Form:    {'✅' if result.form_feasible else '❌'}")
    print(f"     Temp:    {'✅' if result.temp_feasible else '❌'}")
    print(f"\n  🏆 Score: {result.overall_score:.2f} | Verdict: {result.verdict}")
    print(f"  💰 BOM: €{result.bom_cost_euro:.2f} | Est. margin: {result.potential_margin_pct:.0f}%")
    print(f"  ⚠️  Primary risk: {result.primary_risk}")
    print(f"  🛤️  Recommended path: {result.recommended_path}")
    print(f"\n  📈 Market:")
    print(f"     TAM: €{concept.tam_euro:,.0f}")
    print(f"     Maturity: {concept.maturity_years} years")
    print(f"     Competition: {concept.competition_level}")


# =========================================================================
# TOP PRODUCT CONCEPT RECOMMENDATIONS
# =========================================================================

def generate_strategy(results: List[ScanResult]) -> dict:
    """Generate strategic recommendations from scan results."""
    go = [r for r in results if r.verdict == "GO"]
    maybe = [r for r in results if r.verdict == "MAYBE"]
    no_go = [r for r in results if r.verdict == "NO-GO"]
    
    # Best by category
    by_category = {}
    for r in results:
        by_category.setdefault(r.category, []).append(r)
    
    best_per_category = {}
    for cat, cat_results in by_category.items():
        cat_results.sort(key=lambda r: r.overall_score, reverse=True)
        best_per_category[cat] = cat_results[0] if cat_results else None
    
    # Novel concepts that are GO
    novel_go = [r for r in go if r.novelty == "novel"]
    existing_go = [r for r in go if r.novelty == "existing"]
    
    return {
        "total": len(results),
        "n_go": len(go),
        "n_maybe": len(maybe),
        "n_no_go": len(no_go),
        "novel_go": len(novel_go),
        "existing_go": len(existing_go),
        "best_per_category": best_per_category,
        "top_novel": novel_go[:5] if novel_go else [],
        "top_existing": existing_go[:5] if existing_go else [],
        "immediate_actions": [
            f"Ship Passive NFC DevKit now (TRL 9, no battery needed) → edu-kit, smart-packaging",
            f"Validate fungal pressling at 12.5 µW/cm² (Empa baseline) → unblocks 8 concepts",
            f"If fungal hits 50 µW/cm² (conservative): {len(go)} concepts become feasible",
            f"If fungal hits 260 µW/cm² (target): all concepts become feasible",
        ]
    }


# =========================================================================
# MAIN
# =========================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="MykoVolt Product Concept Explorer")
    parser.add_argument("--list", action="store_true", help="List all concept IDs")
    parser.add_argument("--concept", type=str, help="Deep-dive one concept by ID")
    parser.add_argument("--novel-only", action="store_true", help="Only novel concepts")
    parser.add_argument("--go-only", action="store_true", help="Only GO concepts")
    parser.add_argument("--json", type=str, help="Export results to JSON file")
    args = parser.parse_args()
    
    battery = BatteryCapability()
    scanner = ProductScanner(battery)
    concepts = all_concepts()
    
    if args.list:
        print(f"\n{'ID':25s}  {'Name':30s}  {'Category':12s}  {'Novelty':8s}")
        print("-" * 80)
        for c in concepts:
            print(f"  {c.id:25s}  {c.name:30s}  {c.category:12s}  {c.novelty:8s}")
        print(f"\n  Total: {len(concepts)} concepts")
    
    elif args.concept:
        matches = [c for c in concepts if c.id == args.concept]
        if not matches:
            print(f"Concept '{args.concept}' not found. Use --list to see all IDs.")
        else:
            c = matches[0]
            r = scanner.scan(c)
            print_concept_drilldown(c, r)
    
    else:
        # Filter concepts
        if args.novel_only:
            concepts = [c for c in concepts if c.novelty == "novel"]
        
        results = scanner.scan_all(concepts)
        
        if args.go_only:
            results = [r for r in results if r.verdict == "GO"]
        
        print_results(results)
        print_top_go_results(results)
        
        strategy = generate_strategy(results)
        
        print(f"\n{'='*60}")
        print(f"  STRATEGIC SUMMARY")
        print(f"{'='*60}")
        print(f"  {strategy['n_go']} GO concepts (incl. {strategy['novel_go']} novel)")
        print(f"  {strategy['n_maybe']} MAYBE concepts")
        print(f"  {strategy['n_no_go']} NO-GO concepts")
        print(f"\n  Immediate actions:")
        for a in strategy["immediate_actions"]:
            print(f"    • {a}")
        
        if strategy["top_novel"]:
            print(f"\n  Top novel concepts to explore:")
            for r in strategy["top_novel"]:
                print(f"    🟢 {r.concept_name} (score: {r.overall_score:.2f}) — {r.primary_risk}")
        
        if args.json:
            import json
            with open(args.json, "w") as f:
                json.dump([asdict(r) for r in results], f, indent=2, default=str)
            print(f"\n  Results saved to {args.json}")
