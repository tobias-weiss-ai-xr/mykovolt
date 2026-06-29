# MykoVolt — Biodegradable Fungal Battery for Precision Agriculture

<p align="center">
  <img src="docs/teaser.svg" alt="MykoVolt" width="100%">
</p>

<p align="center">
  <b>Die erste kompostierbare Bodenfeuchte-Sensor-Applikation.</b><br>
  7 Tage Laufzeit · 90% biologisch abbaubar · €0.15 pro Stück · Zero E-Waste
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
  - [Feldpilot (Phase 2)](#feldpilot-phase-2)
  - [Technology Stack](#technology-stack)
  - [Energy Budget](#energy-budget)
- [Product Roadmap](#product-roadmap)
- [Deployment Lifecycle](#deployment-lifecycle)
- [Competitive Positioning](#competitive-positioning)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Development Progress](#development-progress)
- [Contact](#contact)
- [License](#license)

---

## Overview

MykoVolt develops the first commercial, biodegradable Pilz-Biobatterie zur Stromversorgung von Bodenfeuchtesensoren in der Präzisionslandwirtschaft. Die Technologie nutzt mikrobiellen Brennstoffzellen (MFC) auf Basis von Weißfäulepilzen (*Trametes pubescens*, *Phanerochaete chrysosporium*), eingebettet in einen kompostierbaren Pressling.

### Key Innovation
- **Biologisch abbaubar**: Pilz-basierte Biobatterie + kompostierbares Gehäuse
- **Wiederverwendbar**: Elektronik-Board (100+ Zyklen)
- **Hybrider Ansatz**: Sofortiger Markteintritt mit vollständiger biologischer Abbaubarkeit als langfristiges Ziel

---

## MVP Design

<p align="center">
  <img src="docs/mvp_design.svg" alt="MykoVolt MVP Design" width="100%">
</p>

---

## System Architecture

### Signal Flow

```mermaid
flowchart TD
    subgraph ENV["🌍 Umwelt"]
        SOIL["Bodenfeuchte\n(Sand/Lehm/Ton)"]
        TEMP["Temperatur"]
    end

    subgraph SENSOR["📐 Sensor-Ebene"]
        ELEC["Kapazitiver Sensor\n100 kHz Exzitation"]
        ADC["ADC-Wandler\n12-Bit"]
    end

    subgraph MCU["🖥️ MCU — STM32L0"]
        SLEEP["Sleep Mode\n0.4 µA"]
        ACTIVE["Active Mode\n3 mA @ 1 MHz"]
        FRAM["FRAM 8 KB\nRing-Puffer"]
        CONTROL["Energie-Manager\n15 min Intervall"]
    end

    subgraph BATTERY["🔋 MFC Bio-Batterie"]
        FUNGUS["Trametes pubescens"]
        ANODE["Anode (−): Hefe"]
        CATHODE["Kathode (+): Enzym"]
        BOOST["Boost 0.45V → 3.3V"]
    end

    subgraph COMMS["📡 Kommunikation"]
        NFC["Phase 1: NFC (passiv)"]
        LORA["Phase 2: LoRa 868 MHz"]
    end

    subgraph CLOUD["☁️ Cloud"]
        GW["LoRa-Gateway / NFC-Reader"]
        DASH["Dashboard\nFeuchte-Karten"]
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
    subgraph L1["Schicht 1: Außen-Casing"]
        C1["Kompostierbarer Pressling\nIP67 · 1.5 mm"]
    end
    subgraph L2["Schicht 2: Antenne"]
        C2["NFC Spule / LoRa Modul"]
    end
    subgraph L3["Schicht 3: Sensor PCB"]
        C3["Kapazitiver Sensor"]
        C4["STM32L0 MCU"]
        C5["FRAM 8 KB"]
        C6["Boost Converter"]
        C3 --- C4 --- C5 --- C6
    end
    subgraph L4["Schicht 4: MFC Bio-Batterie"]
        C7["Anode: Hefe"]
        C8["Kathode: Trametes"]
        C9["Cellulose-Elektrolyt"]
    end
    subgraph L5["Schicht 5: Boden-Casing"]
        C10["Feuchtigkeits-Membran"]
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
    participant S as Boden
    participant SE as Sensor
    participant MCU as STM32L0
    participant F as FRAM
    participant B as Bio-Battery
    participant N as NFC/LoRa
    participant G as Gateway
    participant D as Dashboard

    Note over B: 520 µW @ 0.45V → 3.3V Boost
    B-->>MCU: Dauerhafte Stromversorgung

    loop Alle 15 Minuten
        S->>SE: Feuchte ändert Dielektrikum
        SE->>MCU: Kapazitätswert
        MCU->>MCU: ADC + Temperatur
        MCU->>F: 12-Byte Eintrag
        MCU->>MCU: Deep Sleep 0.4 µA
    end

    alt Phase 1: NFC
        G->>N: Feld aktivieren
        N->>G: 672 Einträge
    else Phase 2: LoRa
        N->>G: 12-Byte Packet
    end
    G->>D: JSON → Dashboard
```

---

## Technical Specifications

### DevKit (Phase 1)

| Parameter | Value |
|-----------|-------|
| Pilzstamm | *Trametes pubescens* (12,5 µW/cm²) |
| Kommunikation | NFC (passiv powered) |
| Energieverbrauch | ~0,14 mWh/Tag |
| Datenformat | 12-Byte-Einträge (timestamp, capacitance, voltage, temperature, status) |
| Dauer | 14 Tage bei 15-Minuten-Intervallen |

### Feldpilot (Phase 2)

| Parameter | Value |
|-----------|-------|
| Pilzstamm | *Phanerochaete chrysosporium* (erwartet 150× mehr Leistung) |
| Kommunikation | LoRa (868 MHz, 2+ km) |
| Energieverbrauch | ~0,60 mWh/Tag (SF12), ~0,09 mWh/Tag (SF7) |
| Gehäuse | IP67, feldtauglich |

### Technology Stack

| Layer | Component | Technology |
|-------|-----------|------------|
| MCU | STM32L0 (Cortex-M0+) | Sensor Datenverarbeitung und -speicherung |
| Memory | MB85RC256 FRAM (32 KB) | Hochzuverlässige Datenspeicherung |
| Communication | Passive NFC / SX1276 LoRa | Datenübertragung |
| Power | Trametes pubescens MFC | Energieerzeugung aus organischem Abfall |
| Casing | Kompostierbarer Pressling | Schutz und biologische Abbaubarkeit |
| Firmware | STM32 HAL C11 | Sensor Datenerfassung und -verarbeitung |
| Simulation | Python | Bodenfeuchte-Sensor-Simulation |

### Energy Budget

```mermaid
pie title Energieverbrauch pro Tag (~40.000 µJ)
    "Sleep (MCU)" : 75.6
    "ADC Messung" : 14.4
    "Sensor Exzitation" : 5.0
    "NFC Kommunikation" : 3.0
    "Boost Converter" : 2.0
```

```mermaid
xychart-beta
    title "Energiebilanz über 7 Tage (µJ)"
    x-axis ["Tag 1", "Tag 2", "Tag 3", "Tag 4", "Tag 5", "Tag 6", "Tag 7"]
    y-axis "µJ" 0 --> 50000
    bar [44928, 44029, 43148, 42285, 41440, 40611, 39800]
    line [40000, 40000, 40000, 40000, 40000, 40000, 40000]
```

---

## Product Roadmap

```mermaid
gantt
    title MykoVolt Entwicklungs-Roadmap
    dateFormat YYYY-MM-DD
    axisFormat %Y-%m

    section Phase 1: DevKit
        Pressling-Rezeptur           :done, p1a, 2025-04-01, 30d
        Board-Design Rev A          :done, p1b, 2025-05-01, 30d
        Prototyp (Funktionsmuster)  :done, p1c, 2025-06-01, 30d
        L2-Systemtest               :active, p1d, 2025-07-01, 60d
        EXIST-Einreichung           :p1e, 2025-09-01, 30d
        DevKit Produktion           :p1f, 2026-01-01, 90d
        DevKit Verkaufsstart        :p1g, 2026-04-01, 30d

    section Phase 2: Feldpilot
        Go/No-Go Entscheidung       :p2a, 2026-07-01, 30d
        LoRa-Integration            :p2b, 2026-08-01, 60d
        Feldpilot Feldtest          :p2c, 2026-10-01, 90d
        Skalierung Produktion       :p2d, 2027-01-01, 90d
        Markteinführung EU          :p2e, 2027-04-01, 60d
```

---

## Deployment Lifecycle

```mermaid
flowchart LR
    subgraph PROD["🏭 Produktion"]
        A1["Pilzzucht"] --> A2["Pressling"] --> A3["Elektronik"] --> A4["QA Test"]
    end
    subgraph DEPLOY["🌱 Feldeinsatz"]
        B1["Einsetzen\n8-12 cm tief"] --> B2["Aktivierung\nWasser + Nährstoffe"] --> B3["Betrieb\n7 Tage"] --> B4["NFC/LoRa TX"]
    end
    subgraph END["♻️ Lebensende"]
        C1["Batterie erschöpft"] --> C2["Pressling\nkompostiert\n30-90 Tage"]
        C1 --> C3["Electronik-Board\ngeborgen\n100+ Wiederverw."]
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
    title Wettbewerbspositionierung Bodensensor-Batterien
    x-axis "Niedrige Kosten" --> "Hohe Kosten"
    y-axis "Kurzlebig" --> "Langlebig"
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
│   ├── diagrams.html          # Full Mermaid diagram suite (12 diagrams)
│   ├── mvp_design.svg        # MVP exploded view & specifications
│   ├── teaser.svg             # Hero image
│   ├── manufacturing_process.md
│   └── supply_chain_analysis.md
├── simulation/
│   └── e2e_soil_sensor.py     # End-to-end sensor simulation
├── tests/
│   └── battery_validation.py
├── competitive/
│   └── intelligence_dashboard.py
├── compliance/
│   └── regulatory_roadmap.md
├── finance/
│   └── funding_strategy.md
├── marketing/
│   └── segment_strategies.md
├── ip/
│   └── ip_strategy.md
├── archive/                   # Historical documents
├── MykoVolt-mvp-design.md     # Full MVP design documentation
├── MykoVolt_Angebot_EMC.md     # EMC GmbH offer
├── MykoVolt_Pitch_Deck.html    # Interactive pitch deck
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.8+
- STM32CubeProgrammer (für NFC-Reader)
- LoRa-Stack (für Feldpilot)

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

## Development Progress

| Phase | Status | Completion |
|-------|--------|------------|
| DevKit Design | ✅ Complete | 100% |
| Prototyp | ✅ Complete | 100% |
| Simulation | ✅ Complete | 100% |
| Business Plan | ✅ Complete | 100% |
| Feldtest | ⏳ In Progress | 25% |
| Produktion | ⏳ Planned | 0% |

---

## Contact

- **GitHub**: [tobias-weiss-ai-xr/mykovolt](https://github.com/tobias-weiss-ai-xr/mykovolt)
- **Codeberg**: [graphwiz-ai/mykovolt](https://codeberg.org/graphwiz-ai/mykovolt)
- **Email**: tobias.weiss.ai.xr@gmail.com
- **LinkedIn**: [MykoVolt](https://www.linkedin.com/company/mykovolt)
- **Twitter**: [@MykoVolt](https://twitter.com/MykoVolt)

## License

This project is licensed under the MIT License.

---

*Letzte Aktualisierung: $(git log --format="%cd" --date=short -1)*