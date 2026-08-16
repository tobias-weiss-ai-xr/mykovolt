# SOHO Lab — Project Pipeline

> **Hardware:** Pi 5 + Hailo-8 AI Chip, Anycubic Kobra S1, Ender 3 (print+laser)  
> **Strategy:** Open Research as Competitive Advantage  
> **Paradigm:** ["We don't compete. We enable."](../product/PARADIGM.md)

---

## Pipeline Overview

Projects are organized into three phases. Each project feeds the
[three pillars](../product/PARADIGM.md#-the-three-pillars):
**Open Knowledgebase** (open data/papers),
**Agentic Harness** (AI tools), and
**Hardware Platform** (physical products).

```
Phase 1 (1-2 weeks)          Phase 2 (2-4 weeks)           Phase 3 (4-8+ weeks)
┌──────────────────┐        ┌──────────────────────┐      ┌──────────────────────┐
│ Soil MFC         │───────►│ Fungal Bioelectr.     │      │ MykoVolt DevKit      │
│ 3D-Printed MFC   │        │ Monitoring             │─────►│  (€299 product)      │
│ Edge AI Vision   │        │ MFC Electrode Opt.    │      │                      │
│                  │        │ Portable MFC Charger  │      │ Autonomous Fungal     │
│                  │        │ Fungal Net. Visual.   │─────►│  Farm (€999 system)  │
│                  │        │ Data Pipeline          │      │                      │
└──────────────────┘        └──────────────────────┘      │ Biohybrid Robot       │
                                                           │ Fungal Net. Mapping  │
                                                           └──────────────────────┘
```

---

## Phase 1 — Quick Wins (1-2 weeks, parallel)

### 1. Soil Microbial Fuel Cells ⭐ Score 3.6
> **Lowest barrier to entry — dirt + electrodes = working MFC**

- **Hardware:** Soil, carbon cloth, graphite, Pi 5, multimeter
- **Pillar:** Open Knowledgebase
- **Papers:** #2, #4, #10, #14, #33
- **Output:** First working MFC, open performance dataset
- **Repo:** `lab/soil-mfc/`

### 2. 3D-Printed MFC Prototypes ⭐ Score 4.7
> **Design and print fuel cell chambers from research**

- **Hardware:** Anycubic Kobra S1, PLA/PETG
- **Pillar:** Hardware Platform
- **Papers:** #8 (8mm electrode spacing), #12 (chamber geometry), #15, #47
- **Output:** OpenSCAD + STL files, assembly guide, functional prototype
- **Repo:** `lab/3d-printed-mfc/`

### 3. Edge AI Vision Testing ⭐ Score 2.4
> **Benchmark CV algorithms on Hailo-8, validate robotics-research**

- **Hardware:** Pi 5, Hailo-8, Camera
- **Pillar:** Open Knowledgebase
- **Papers:** [robotics-research](https://github.com/tobias-weiss-ai-xr/robotics-research) perception category
- **Output:** Benchmark dataset, Hailo optimization guides
- **Repo:** `lab/edge-ai-bench/`

---

## Phase 2 — Deepen Impact (2-4 weeks)

### 4. Fungal Bioelectricity Monitoring ⭐ Score 2.6
> **World's first open fungal bioelectricity dataset**

- **Hardware:** Pi 5, Hailo-8, Camera, Electrodes, ADC (MCP3008)
- **Pillar:** Open Knowledgebase + Agentic Harness
- **Papers:** #5, #8, #12, #15, #23, #47
- **Output:** Time-series dataset, monitoring software, research preprint
- **Repo:** `lab/fungal-monitor/`

### 5. MFC Electrode Optimization ⭐ Score 2.6
> **Test materials and configurations from literature**

- **Hardware:** Pi 5, multimeter, 3D-printed electrode holders
- **Pillar:** Open Knowledgebase
- **Papers:** #8, #15, #20, #23, #35
- **Output:** Comparative performance dataset, material recommendations
- **Repo:** `lab/electrode-opt/`

### 6. Portable MFC Charger ⭐ Score 2.6
> **First product prototype — trickle-charges small devices**

- **Hardware:** MFC array, BQ25570 boost, 3D-printed case, LiPo
- **Pillar:** Hardware Platform
- **Papers:** #5, #8, #12, #15, #20, #23, #35
- **Output:** Working charger, KiCad schematics, construction guide
- **Repo:** `lab/portable-charger/`

### 7. Fungal Network Visualization ⭐ Score 2.6
> **Real-time visualization of mycelial electrical signals**

- **Hardware:** Pi 5, Hailo-8, Electrodes, ADC, OLED/Web dashboard
- **Pillar:** Agentic Harness
- **Papers:** #15, #23, #47, #52
- **Output:** Open-source visualization tool, web dashboard
- **Repo:** `lab/net-visualizer/`

### 8. Automated Data Pipeline ⭐ Score 2.6
> **Automated collection, processing, sharing across all experiments**

- **Hardware:** Pi 5
- **Pillar:** Open Knowledgebase + Agentic Harness
- **Papers:** All 90 papers (enables research across corpus)
- **Output:** Data pipeline, automated reports, open data repo
- **Repo:** `lab/data-pipeline/`

---

## Phase 3 — Flagship Projects (4-8+ weeks)

### 9. MykoVolt DevKit ⭐ Score 4.3
> **The flagship product — complete development kit for fungal bioelectr.**

- **Hardware:** All (MFC + sensor board + Pi 5 integration)
- **Pillar:** All Three Pillars
- **Papers:** Multiple (#5, #8, #12, #15, #20, #23, #35, #47)
- **Output:** Product (€299), open-source software, documentation
- **Repo:** `applications/devkit/` (extends existing)

### 10. Autonomous Fungal Farm ⭐ Score 4.3
> **Automated fungal growth + bioelectricity monitoring system**

- **Hardware:** Pi 5, Hailo-8, 3D-printed structure, pumps, sensors
- **Pillar:** All Three Pillars
- **Papers:** #5, #8, #12, #18, #25, #31, #47
- **Output:** System (€999), optimization SaaS
- **Repo:** `lab/fungal-farm/`

### 11. Biohybrid Robot ⭐ Score 3.2
> **Fungal-powered robot with AI vision — media + investor demo**

- **Hardware:** Pi 5, Hailo-8, MFC array, motors, camera
- **Pillar:** All Three Pillars
- **Output:** Robot prototype, research paper, demo video
- **Repo:** `lab/biohybrid-robot/`

### 12. Fungal Electrical Network Mapping ⭐ Score 2.6
> **Map electrical networks in living fungal colonies**

- **Hardware:** Pi 5, Hailo-8, camera, multi-electrode array, 3D-printed arm
- **Pillar:** Open Knowledgebase
- **Papers:** #15, #23, #47, #52, #58
- **Output:** Mapping system, electrical network dataset, research paper
- **Repo:** `lab/net-mapper/`

### 13. Low-Cost SLAM Robot ⭐ Score 1.3
> **Validate SLAM algorithms from robotics-research on real hardware**

- **Hardware:** Pi 5, Hailo-8, camera, encoders, motors
- **Pillar:** Open Knowledgebase
- **Papers:** [robotics-research](https://github.com/tobias-weiss-ai-xr/robotics-research) SLAM category
- **Output:** Working robot, SLAM maps, benchmark data
- **Repo:** `lab/slam-robot/`

### 14. Fungal-Powered Sensor Node ⭐ Score 2.7
> **Small sensor robot powered by MFC — proof of concept**

- **Hardware:** MFC, ESP32, motors, wheels
- **Pillar:** Hardware Platform
- **Output:** Working prototype, construction guide, demo video
- **Repo:** `lab/fungal-sensor-node/`

### 15. 3D-Printed Robot End-Effectors ⭐ Score 2.0
> **Design grippers from manipulation papers**

- **Hardware:** Anycubic Kobra S1, servos
- **Pillar:** Open Knowledgebase
- **Papers:** [robotics-research](https://github.com/tobias-weiss-ai-xr/robotics-research) manipulation category
- **Output:** STL files, assembly guides, test results
- **Repo:** `lab/end-effectors/`

---

## How Projects Map to the Paradigm

| Project | Knowledgebase | Harness | Hardware | Revenue |
|---------|:---:|:---:|:---:|---------|
| Soil MFC | ✅ | | | Grants |
| 3D-Printed MFC | ✅ | | ✅ | Grants |
| Edge AI Bench | ✅ | | | Community |
| Monitoring | ✅ | ✅ | | Preprints |
| Electrode Opt. | ✅ | | | Preprints |
| Portable Charger | ⚠️ | | ✅ | **€99** |
| Net. Visualization | | ✅ | | Community |
| Data Pipeline | ✅ | ✅ | | Grants |
| DevKit | ⚠️ | ✅ | ✅ | **€299** |
| Fungal Farm | ⚠️ | ✅ | ✅ | **€999** |
| Biohybrid Robot | ✅ | | ✅ | Grants |
| Net. Mapping | ✅ | ✅ | | Preprints |
| SLAM Robot | ✅ | | | Community |
| Sensor Node | ⚠️ | | ✅ | Grants |
| End-Effectors | ✅ | | | Community |

✅ = fully open | ⚠️ = partial (open docs, proprietary product)

---

## Hardware Inventory

| Component | Available | Projects Using It |
|-----------|:---------:|-------------------|
| **Raspberry Pi 5 + SSD** | ✅ | All projects with Pi 5 |
| **Hailo-8 AI Chip** | ✅ | Monitoring, Edge AI, Farm, Robot |
| **Anycubic Kobra S1** | ✅ | MFC Prototypes, End-Effectors, Cases |
| **Ender 3 (print + laser)** | ✅ | PCB prototyping, detailed parts |
| **Camera (RPi or USB)** | ❌ buy | Monitoring, Edge AI, Farm, Robot |
| **Carbon cloth** | ❌ buy | Soil MFC, Electrodes, Monitoring |
| **Graphite sheets** | ❌ buy | Electrodes, Monitoring |
| **Agar + cultures** | ❌ buy | Monitoring, Farm |
| **ADC (MCP3008)** | ❌ buy | Monitoring, Net. Visualization |
| **Multimeter** | ❌ buy | All MFC projects |
| **Soldering station** | ❌ buy | Sensor board, Charger |

### Missing Materials Budget: ~€745

See [`BRAINSTORM.md`](PROJECT_BRAINSTORM.md) for full breakdown.

---

## Materials You May Already Have

From the existing [sensor board shopping list](../hardware/shopping_list.md):
- BQ25570 boost converter (useful for Portable Charger)
- STM32L011 MCU (useful for sensor nodes)
- ST25DV04K NFC (useful for DevKit)
- Resistors, capacitors, connectors (useful for all projects)

From existing [order checklist](../prototyping/order_checklist.md):
- Breadboard, jumper wires
- Hot air station, soldering iron
- ST-Link debugger

---

## Success Metrics

### Phase 1 Checkpoints (2 weeks)
- [ ] 3 working prototypes (soil MFC, 3D-printed chamber, Hailo benchmark)
- [ ] First open dataset published (GitHub)
- [ ] 5+ research papers validated experimentally
- [ ] First social media content (timelapses, benchmarks)

### Phase 2 Checkpoints (4 weeks)
- [ ] 6+ working systems
- [ ] World's first open fungal bioelectricity dataset
- [ ] First product prototype (Portable Charger)
- [ ] First preprint submitted

### Phase 3 Checkpoints (8 weeks)
- [ ] DevKit v0.2 with Pi 5 integration
- [ ] Autonomous Fungal Farm operational
- [ ] Biohybrid Robot demo video
- [ ] Strong open-source portfolio on GitHub

---

## Links

- [Paradigm](../product/PARADIGM.md) — Strategic foundation
- [Business Strategy](../product/business_strategy_refined.md) — Market + revenue model
- [Full Brainstorm](PROJECT_BRAINSTORM.md) — Market research + analysis
- [Sensor Board Design](../hardware/sensor_board_design.md) — Existing hardware
- [Shopping List](../hardware/shopping_list.md) — Existing components
- [Research Corpus](../../research/) — 90 curated papers
- [Robotics Research](https://github.com/tobias-weiss-ai-xr/robotics-research) — 1,637 papers for validation

---

*Created: 2026-08-16*
