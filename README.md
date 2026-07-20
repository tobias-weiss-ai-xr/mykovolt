# MykoVolt — Biodegradable Fungal Battery for IoT & Beyond

<p align="center">
  <img src="docs/assets/teaser.png" alt="MykoVolt" width="100%">
</p>

<p align="center">
  <b>Compostable bio-batteries for 15+ applications across agriculture, construction, logistics & environment.</b><br>
  15 use cases · 90% biodegradable · pellets from €0.15 · Zero e-waste
</p>

## Table of Contents

- [Overview](#overview)
- [MVP Design](#mvp-design)
- [System Architecture](#system-architecture)
  - [Signal Flow](#signal-flow)
  - [Layer Stack](#layer-stack)
  - [Data Flow](#data-flow)
- [Technical Specifications](#technical-specifications)
  - [DevKit (Phase 1)](#devkit-phase-1)
  - [Field Pilot (Phase 2)](#field-pilot-phase-2)
  - [Technology Stack](#technology-stack)
  - [Energy Budget](#energy-budget)
- [Product Roadmap](#product-roadmap)
- [Deployment Lifecycle](#deployment-lifecycle)
- [Competitive Positioning](#competitive-positioning)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Grant Applications & Recruitment](#grant-applications--recruitment)
- [Development Progress](#development-progress)
- [Contact](#contact)
- [License](#license)

---

## Overview

MykoVolt develops the first commercial, biodegradable fungal bio-battery to power IoT sensors across 15+ applications. The technology uses microbial fuel cells (MFC) based on white-rot fungi (*Trametes pubescens*, *Phanerochaete chrysosporium*), embedded in a compostable pellet.

### Key Innovation
- **Biodegradable**: Fungus-based bio-battery + compostable casing
- **Reusable**: Electronics board (100+ cycles)
- **Dual-path strategy**: Fungal MFC (primary) + Mg-Air battery (fallback)

### Use Cases (3 Phases)

#### Phase 1: DevKit (Research Labs)
| Application | Market | Why MykoVolt Wins |
|-------------|--------|-------------------|
| Soil moisture | Precision ag, viticulture, turf | Underground operation, €0.15/unit, compostable |
| Compost monitoring | Municipal composting, biowaste | Works inside compost piles (dark, moist, perfect for fungi) |
| Structural health (concrete curing) | Construction, infrastructure | Embedded during pouring — no light, no retrieval |
| Cold-chain loggers | Food/pharma shipping | Disposable, compostable, no Li-ion in food containers |
| Research/education kits | Universities, schools | Safe, biodegradable, teaches synthetic biology + IoT |

#### Phase 2: Field Pilot
| Application | Market | Why MykoVolt Wins |
|-------------|--------|-------------------|
| Forestry / under-canopy sensing | Carbon credits, wildfire detection | Zero light under canopy — solar is dead |
| Permafrost monitoring | Climate research, Arctic | Solar seasonal (polar night); fungal batteries work continuously |
| Landfill / waste monitoring | Environmental compliance | Works inside waste piles; no retrieval in hazardous zones |
| Wildlife tracking tags | Conservation, ecology | €0.15 disposable tags — no retrieval, no harm if ingested |
| Smart packaging | Food/pharma logistics | Compostable temperature abuse indicators |

#### Phase 3: Commercial Scale
| Application | Market | Why MykoVolt Wins |
|-------------|--------|-------------------|
| Agricultural sensor networks | Row crops, vineyards, orchards | Dense deployment (100+ sensors/ha), no retrieval labor |
| Medical disposable sensors | Wound dressings, diagnostics | Single-use, biocompatible, no Li-ion waste |
| Landmine / UXO monitoring | Defense, humanitarian demining | Long-term passive monitoring, biodegradable (no cleanup) |
| Soil carbon verification | Carbon credits, regenerative ag | Buried sensors verify carbon sequestration — zero maintenance |
| Smart city infrastructure | Underground utilities, flood detection | Embedded in soil/concrete, no battery replacement |

### MVP Options (Phase 0 Gate Decision)

| Path | Technology | Advantage | Risk |
|------|-----------|-----------|------|
| **A: Fungal MFC** | *T. pubescens* + yeast co-culture | Fully biodegradable, novel IP | Power density unproven at scale |
| **B: Mg-Air** | Mg foil anode, carbon cathode | Proven chemistry, higher power | Mg foil not fully biodegradable |

Both paths developed in parallel during Phase 0. Gate decision after 12 months of lab validation. See [MVP_DESIGN.md](MVP_DESIGN.md#9-dual-path-strategie-phase-0) for details.

---

## MVP Design

<p align="center">
  <img src="docs/technical/mvp_design.svg" alt="MykoVolt MVP Design" width="100%">
</p>

---

## System Architecture

### Signal Flow

```mermaid
flowchart TD
    subgraph ENV["🌍 Environment"]
        SOIL["Soil Moisture\n(Sand/Loam/Clay)"]
        TEMP["Temperature"]
    end

    subgraph SENSOR["📐 Sensor Layer"]
        ELEC["Capacitive Sensor\n100 kHz Excitation"]
        ADC["ADC Converter\n12-Bit"]
    end

    subgraph MCU["🖥️ MCU — STM32L0"]
        SLEEP["Sleep Mode\n0.4 µA"]
        ACTIVE["Active Mode\n3 mA @ 1 MHz"]
        FRAM["FRAM 8 KB\nRing Buffer"]
        CONTROL["Energy Manager\n15 min Interval"]
    end

    subgraph BATTERY["🔋 MFC Bio-Battery"]
        FUNGUS["Trametes pubescens"]
        ANODE["Anode (−): Yeast"]
        CATHODE["Cathode (+): Enzyme"]
        BOOST["Boost 0.45V → 3.3V"]
    end

    subgraph COMMS["📡 Communication"]
        NFC["Phase 1: NFC (passive)"]
        LORA["Phase 2: LoRa 868 MHz"]
    end

    subgraph CLOUD["☁️ Cloud"]
        GW["LoRa Gateway / NFC Reader"]
        DASH["Dashboard\nMoisture Maps"]
    end

    SOIL --> ELEC --> ADC --> ACTIVE --> FRAM
    CONTROL --> ACTIVE
    FUNGUS --> ANODE & CATHODE --> BOOST --> MCU
    ACTIVE --> NFC & LORA --> GW --> DASH

    style ENV fill:#E8F5E9,stroke:#2D6A4F,stroke-width:2px
    style SENSOR fill:#FFF3E0,stroke:#E65100,stroke-width:2px
    style MCU fill:#E3F2FD,stroke:#1565C0,stroke-width:2px
    style BATTERY fill:#F1F8E9,stroke:#558B2F,stroke-width:2px
    style COMMS fill:#F3E5F5,stroke:#6A1B9A,stroke-width:2px
    style CLOUD fill:#ECEFF1,stroke:#455A64,stroke-width:2px
```

### Layer Stack

```mermaid
flowchart TB
    subgraph L1["Layer 1: Outer Casing"]
        C1["Compostable Pellet\nIP67 · 1.5 mm"]
    end
    subgraph L2["Layer 2: Antenna"]
        C2["NFC Coil / LoRa Module"]
    end
    subgraph L3["Layer 3: Sensor PCB"]
        C3["Capacitive Sensor"]
        C4["STM32L0 MCU"]
        C5["FRAM 8 KB"]
        C6["Boost Converter"]
        C3 --- C4 --- C5 --- C6
    end
    subgraph L4["Layer 4: MFC Bio-Battery"]
        C7["Anode: Yeast"]
        C8["Cathode: Trametes"]
        C9["Cellulose Electrolyte"]
    end
    subgraph L5["Layer 5: Soil Casing"]
        C10["Moisture Membrane"]
    end
    L1 --> L2 --> L3 --> L4 --> L5
    style L1 fill:#A1887F,stroke:#5D4037,color:#fff
    style L2 fill:#7B1FA2,stroke:#4A148C,color:#fff
    style L3 fill:#1565C0,stroke:#0D47A1,color:#fff
    style L4 fill:#558B2F,stroke:#33691E,color:#fff
    style L5 fill:#795548,stroke:#4E342E,color:#fff
```

### Data Flow

```mermaid
sequenceDiagram
    participant S as Soil
    participant SE as Sensor
    participant MCU as STM32L0
    participant F as FRAM
    participant B as Bio-Battery
    participant N as NFC/LoRa
    participant G as Gateway
    participant D as Dashboard

    Note over B: TRL 2 baseline: 25 µW @ 0.45V → 3.3V Boost
    B-->>MCU: Continuous power supply

    loop Every 15 minutes
        S->>SE: Moisture changes dielectric
        SE->>MCU: Capacitance value
        MCU->>MCU: ADC + Temperature
        MCU->>F: 12-byte entry
        MCU->>MCU: Deep Sleep 0.4 µA
    end

    alt Phase 1: NFC
        G->>N: Activate field
        N->>G: 672 entries
    else Phase 2: LoRa
        N->>G: 12-byte packet
    end
    G->>D: JSON → Dashboard
```

---

## Technical Specifications

### DevKit (Phase 1)

| Parameter | Value |
|-----------|-------|
| Fungal strain | *Trametes pubescens* (12.5 µW/cm²) |
| Communication | NFC (passive powered) |
| Energy consumption | ~0.14 mWh/day |
| Data format | 12-byte entries (timestamp, capacitance, voltage, temperature, status) |
| Duration | 14 days at 15-minute intervals |

### Field Pilot (Phase 2)

| Parameter | Value |
|-----------|-------|
| Fungal strain | *Phanerochaete chrysosporium* (expected 150× more power) |
| Communication | LoRa (868 MHz, 2+ km) |
| Energy consumption | ~0.60 mWh/day (SF12), ~0.09 mWh/day (SF7) |
| Casing | IP67, field-ready |

### Technology Stack

| Layer | Component | Technology |
|-------|-----------|------------|
| MCU | STM32L0 (Cortex-M0+) | Sensor data processing and storage |
| Memory | MB85RC256 FRAM (32 KB) | High-reliability data storage |
| Communication | Passive NFC / SX1276 LoRa | Data transmission |
| Power | Trametes pubescens MFC | Energy generation from organic waste |
| Casing | Compostable pellet | Protection and biodegradability |
| Firmware | STM32 HAL C11 | Sensor data acquisition and processing |
| Simulation | Python | Soil moisture sensor simulation |

### Energy Budget

```mermaid
pie title Energy consumption per day (~40 mJ)
    "Sleep (MCU)" : 75.6
    "ADC Measurement" : 14.4
    "Sensor Excitation" : 5.0
    "NFC Communication" : 3.0
    "Boost Converter" : 2.0
```

```mermaid
xychart-beta
    title "Supply (50 µW target) vs Demand (mJ/day)"
    x-axis ["Tag 1", "Tag 2", "Tag 3", "Tag 4", "Tag 5", "Tag 6", "Tag 7"]
    y-axis "mJ" 0 --> 5000
    bar [4320, 4234, 4149, 4066, 3985, 3905, 3827]
    line [40, 40, 40, 40, 40, 40, 40]
```

---

## Product Roadmap

```mermaid
gantt
    title MykoVolt Realistic Development Roadmap
    dateFormat YYYY-MM-DD
    axisFormat %Y-%m

    section Phase 0: Lab Validation
        Reproduce Empa 2024 Result  :active, p0a, 2026-07-01, 90d
        Pellet Formulation Dev      :p0b, 2026-08-01, 120d
        Electrochemical Testing     :p0c, 2026-10-01, 90d
        Scientific Co-Founder Search:p0d, 2026-07-01, 180d
        EXIST Grant Application     :p0e, 2026-09-01, 90d

    section Phase 1: DevKit (Research Labs)
        Board Design Rev A          :p1a, 2027-04-01, 60d
        Prototype (Functional)      :p1b, 2027-06-01, 90d
        L2 System Test              :p1c, 2027-09-01, 60d
        DevKit Production           :p1d, 2028-01-01, 90d
        DevKit Launch               :milestone, p1e, 2028-04-01, 1d

    section Phase 2: Field Pilot (Research)
        Go/No-Go Decision           :milestone, p2a, 2028-09-01, 1d
        P. chrysosporium Validation :p2b, 2028-07-01, 180d
        LoRa Integration            :p2c, 2028-10-01, 90d
        Field Pilot Field Test      :p2d, 2029-01-01, 180d
        Production Scaling Decision :milestone, p2e, 2029-07-01, 1d

    section Phase 3: Commercial
        Pilot Production Line       :p3a, 2029-07-01, 180d
        EU Market Entry             :p3b, 2030-01-01, 180d
```

---

## Deployment Lifecycle

```mermaid
flowchart LR
    subgraph PROD["🏭 Production"]
        A1["Fungal Cultivation"] --> A2["Pellet"] --> A3["Electronics"] --> A4["QA Test"]
    end
    subgraph DEPLOY["🌱 Field Deployment"]
        B1["Insert\n8-12 cm deep"] --> B2["Activation\nWater + Nutrients"] --> B3["Operation\n7 Days"] --> B4["NFC/LoRa TX"]
    end
    subgraph END["♻️ End of Life"]
        C1["Battery Depleted"] --> C2["Pellet\ncomposted\n30-90 Days"]
        C1 --> C3["Electronics Board\nretrieved\n100+ Reuses"]
    end
    A4 --> B1
    B4 --> C1
    style PROD fill:#E3F2FD,stroke:#1565C0
    style DEPLOY fill:#F1F8E9,stroke:#558B2F
    style END fill:#FFF3E0,stroke:#E65100
```

---

## Competitive Positioning

```mermaid
quadrantChart
    title Soil Sensor Battery Competitive Positioning
    x-axis "Low Cost" --> "High Cost"
    y-axis "Short-lived" --> "Long-lasting"
    "MykoVolt Bio-Battery": [0.15, 0.15]
    "CR2032 Li-Ion": [0.6, 0.85]
    "AAA Alkaline": [0.35, 0.45]
    "Li-Po Picolithium": [0.9, 0.65]
    "EDLC Supercap": [0.4, 0.02]
```

---

## Project Structure

```
mykovolt/
├── docs/
│   ├── assets/                # Images & diagrams
│   │   ├── teaser.png         # Hero image (PNG)
│   │   └── teaser.svg         # Hero image (SVG source)
│   ├── business/              # Business, IP, finance & marketing
│   │   ├── competitive_intelligence_dashboard.py
│   │   ├── compliance_regulatory_roadmap.md
│   │   ├── finance_funding_strategy.md
│   │   ├── ip_strategy.md
│   │   ├── marketing_segment_strategies.md
│   │   └── supply_chain_analysis.md
│   ├── grants/                # Grant applications
│   │   ├── flash_submission.md    # MAFEX FLASH submission (deadline 15.8.2026)
│   │   └── grant_roadmap.md       # Grant strategy (Hessen Ideen, EXIST, Horizon)
│   ├── team/                  # Recruiting & team
│   │   ├── join_us.md             # Co-founders, students, advisors
│   │   └── masters_thesis_topics.md # 10 Master's thesis topics
│   └── technical/             # Technical documentation
│       ├── air_chimney_design.md
│       ├── diagrams.html      # Full Mermaid diagram suite (12 diagrams)
│       ├── manufacturing_process.md
│       ├── mg_air_battery.md
│       ├── mvp_design.svg     # MVP exploded view & specifications
│       └── phase0_execution_plan.md
├── simulation/                # Simulation code & outputs
│   ├── ai_optimizer.py
│   ├── alternatives.py
│   ├── component_failure_modes.py
│   ├── degradation_model.py
│   ├── dual_path_analysis.py
│   ├── e2e_soil_sensor.py     # End-to-end sensor simulation
│   ├── electron_transport_graph.py
│   ├── geometry_optimization.py
│   ├── multi_objective_optimizer.py
│   ├── pressling_viability.py
│   ├── print_geometry_optimizer.py
│   ├── uncertainty_aware_twin.py
│   └── visualize.py
├── tests/                     # Test suite
│   ├── conftest.py
│   ├── test_degradation.py
│   ├── test_multi_objective.py
│   └── test_uncertainty.py
├── MVP_DESIGN.md              # Full MVP design documentation
├── PITCH_DECK.html            # Interactive pitch deck
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.8+
- STM32CubeProgrammer (for NFC reader)
- LoRa stack (for field pilot)

### Installation
```bash
git clone https://github.com/tobias-weiss-ai-xr/mykovolt.git
cd mykovolt
pip install -r requirements.txt
```

### Running Tests
```bash
pytest simulation/
```

---

## Grant Applications & Recruitment

**Current status (Q3 2026):** Design complete. **Recruiting team** to build first functional prototype.

### Grant Roadmap

| Grant | Amount | Timeline | Status |
|-------|--------|----------|--------|
| **MAFEX FLASH** | €500 | 15.8.2026 | Preparing |
| **Hessen Ideen** | €50k-150k | Q4 2026 / Q1 2027 | Preparing |
| **EXIST** | €250k-500k | Q1 2027 | Preparing |
| **Horizon Europe** | €2-5M | Q2 2027 | Consortium building |
| **BMBF Bioökonomie** | €500k-2M | Q3 2027 | — |
| **DBU Umweltinnovation** | €300k | Q4 2027 | — |

📄 **Details:** [`docs/grants/grant_roadmap.md`](docs/grants/grant_roadmap.md)

### Master's Thesis Topics

**10 thesis topics** across 5 work packages (fungal strains, materials, electronics, environmental impact, applications).

**Key priorities:**
- **WP2.1:** Compression-molded fungal MFC pellets (critical path)
- **WP3.1:** Ultra-low-power MCU firmware
- **WP1.1:** High-performance fungal strains

📄 **Details:** [`docs/team/masters_thesis_topics.md`](docs/team/masters_thesis_topics.md)

### Join Us

**Looking for:**
- **Co-Founder / CTO** (fungal biology, electrochemistry, materials science)
- **Co-Founder / CEO** (business development, fundraising, grant writing)
- **Co-Founder / CIO** (AI, simulation, business development) — Tobias
- **Business Development** — Marc (part-time)
- **Master's Thesis Students** (Q4 2026 / Q1 2027 start)
- **Advisors** (2-4 hours/week, flexible)

📄 **Apply:** [`docs/team/join_us.md`](docs/team/join_us.md)

---

## Development Progress

| Phase | Status | Completion | Notes |
|-------|--------|------------|-------|
| Desk Research | ✅ Complete | 100% | 92 papers curated, literature survey done |
| System Simulation | ✅ Complete | 100% | Energy budget, soil model, lifetime model |
| MVP System Design | ✅ Complete | 100% | Board architecture, firmware spec, test plan |
| Business Planning | ✅ Complete | 100% | Market analysis, regulatory roadmap, IP strategy |
| Lab Validation (TRL 2→3) | ⏳ Phase 0 | 0% | First experimental PoC pending — lab access needed |
| Pellet Formulation | 📝 Planned | 0% | Requires wet-lab collaboration |
| Board Prototype | 📝 Planned | 0% | Requires validated power specs first |
| Field Test | 📝 Planned | 0% | Dependent on Phases 0-1 completion |
| Production | 📝 Planned | 0% | Realistic target: 2029+ |

> ⚠️ **Feasibility Note (July 2026):** MykoVolt is currently at **TRL 2** (technology concept formulated). The simulation and design work is complete, but no experimental validation has been performed. All hardware-dependent milestones above require successful lab validation first. See [docs/business/finance_funding_strategy.md](docs/business/finance_funding_strategy.md) for the realistic funding pathway and [MVP_DESIGN.md](MVP_DESIGN.md) for the risk register.

---

## Contact

- **GitHub**: [tobias-weiss-ai-xr/mykovolt](https://github.com/tobias-weiss-ai-xr/mykovolt)
- **Email**: tobias@tobias-weiss.org

## License

This project is licensed under the MIT License.

---

*Last updated: $(git log --format="%cd" --date=short -1)*
