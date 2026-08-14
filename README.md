# MykoVolt — Vanishing Electronics Platform

**A modular, compostable sensing platform for environments where sensors can be placed but never retrieved.**

[![CI](https://github.com/tobias-weiss-ai-xr/mykovolt/actions/workflows/pcb-ci.yml/badge.svg)](https://github.com/tobias-weiss-ai-xr/mykovolt/actions/workflows/pcb-ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Hardware: CERN-OHL-P](https://img.shields.io/badge/Hardware-CERN--OHL--P-blue.svg)](LICENSE_HARDWARE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](pyproject.toml)

---

## The Idea

MykoVolt is an open platform for building **ephemeral sensors** — devices that:
- Deploy at **high density** (target: €0.01/node at scale)
- Operate where **Li-ion can't go** (inside compost, concrete, landfills, tissue)
- **Leave no trace** after mission completion (compostable power, future compostable substrate)

This repo contains the **DevKit v0.1** — the first instantiation of the platform: a 30×20mm NFC data logger with a fungal or Mg-Air battery. It's a tool for researchers to experiment with biodegradable sensing, understand the constraints, and build the next generation of vanishing electronics.

---

## Architecture

```
                    APPLICATIONS
  DevKit (now)  →  Compost Monitor  →  Concrete Embed  →  Your App?
                    COMMUNICATION
            NFC (v0.1) → BLE (future) → Passive RF (long-term)
                    COMPUTE
         ARM Cortex-M0+ + FRAM + RTC + Energy Manager
                    SENSING
         Capacitive (now) → Temp/Chem (future — you build it)
                    POWER
         Fungal MFC (primary) + Mg-Air (fallback)
                    MANUFACTURING
         PCB Generator + Design Rules + CI/CD
```

Each layer is documented in the [platform architecture](platform/architecture/overview.md).

---

## What's Here

| Directory | Content |
|-----------|---------|
| `hardware/kicad/` | PCB design (DevKit v0.1: 30×20mm, 4-layer, 57 components) |
| `firmware/` | STM32L011 firmware (C, ARM GCC, zero warnings) |
| `simulation/` | 11-level simulation pipeline (Bayesian optimization, degradation, BOM) |
| `tests/` | 175 pytest tests (simulation, hardware, firmware, DRC, CLI) |
| `mykovolt/` | Python CLI package (fetch, parse, calibrate, export, plot) |
| `tools/` | CI/CD, Gerber validation, parametric sweep, test fixture generator |
| `platform/architecture/` | Platform vision, layer specifications, research roadmap |
| `applications/` | Application-specific designs |
| `docs/` | Technical specifications, prototyping guides, product concepts |
| `docs/biology/` | Fungal species selection, cultivation protocols, ordering guide |
| `research/` | MFC literature corpus (75 papers, auto-updated via arXiv/CrossRef/OpenAlex) |

---

## The Honest Constraint

This platform exists because of a fundamental problem: **Li-ion batteries are disqualified from environments where biodegradability, biocompatibility, or food safety are required.** The fungal MFC solves that — but it comes with tradeoffs:

| Constraint | Current Limit | Path to Improvement |
|------------|---------------|---------------------|
| Power | 25 µW (7 days) | Better strain + formulation → 260 µW simulated |
| O₂ requirement | Can't bury >5cm without air chimney | Mg-Air fallback, surface deployment |
| NFC range | 2-5 cm | BLE add-on (more power budget needed) |
| Board substrate | FR-4 (not biodegradable) | Cellulose PCB research (TRL 2-3) |

**The DevKit works today within these constraints.** The platform is designed to evolve as each layer improves.

---

## 📚 Research Corpus

MykoVolt maintains an **auto-updated MFC literature corpus** in [`research/`](research/README.md):

- **75 papers** on fungal bioelectrochemistry, discovered via arXiv, CrossRef, EuropePMC, and OpenAlex
- **Auto-validated** pipeline (`research/scripts/validate_papers.py`)
- **Deep-dive review** for our species selection: [MFC Literature Review](research/docs/research/mfc_literature_review.md)
- **Update anytime:** `cd research && python3 scripts/fetch/fetch_other_sources.py`

---

## Fungal Species for MykoVolt MFCs

We've evaluated **6 fungal species** for compatibility with the DevKit's power requirements (BQ25570 energy harvester: **0.33–5 V input**, FDC1004 capacitance sensor, ST25DV04K NFC) and MykoVolt's use cases. The table below ranks them by **technical suitability, power output, and ease of integration** with the existing hardware design.

| Species | Eignung für MykoVolt | Primäre Anwendungen | Stromausbeute | Lebensdauer | Substrat | Verfügbarkeit | Kosten (pro Kultur) |
|---------|----------------------|---------------------|----------------|--------------|----------|--------------|---------------------|
| **Trametes versicolor** (Schmetterlingstramete) | ⭐⭐⭐⭐⭐ | **DevKit, Soil Moisture Sensor, Compost Monitor, Smart Packaging** | **100–200 µW/cm²** | 3–4 Wochen | Lignin (Holzspäne, Agrarreste) | **Hoch** (DSMZ, ATCC, Pilzzüchter) | €15–25 |
| **Neurospora crassa** | ⭐⭐⭐⭐⭐ | **High-Performance MFCs (Forschung, Medizin), Soil Carbon Verification** | **200–260 µW/cm²** | 2–3 Wochen | Glucose (Vogel’s Medium) | Mittel (FGSC, DSMZ) | €20–30 |
| **Aspergillus niger** | ⭐⭐⭐⭐ | **Mg-Air-Hybrid-Systeme (Permafrost, Landfill), Smart City Infrastructure** | 150–180 µW/cm² | 4–6 Wochen | Industrielle Abfälle (Pektin, Zellulose) | **Sehr hoch** | €10–20 |
| **Pleurotus ostreatus** (Austernpilz) | ⭐⭐⭐ | **Passive NFC DevKit, Edu Kit, Living Art (günstig & einfach)** | 50–80 µW/cm² | 2 Wochen | Stroh, Kaffeesatz, Cellulose | **Sehr hoch** (lokal, Supermarkt) | €5–15 |
| **Ganoderma lucidum** (Reishi) | ⭐⭐ | **Smart Wound Dressing (medizinisch, biocompatibel)** | 30–50 µW/cm² | 3–4 Wochen | Cellulose (Wundauflagen), Holz | Hoch | €25–40 |
| **Pestalotiopsis microspora** | ⭐⭐ | **Bioelektronik (Graphen-Produktion), Future Research** | 40–60 µW/cm² | 4–6 Wochen | Lignocellulose | Mittel | €30–50 |

### 🎯 Quick Start Recommendations
| Use Case | Recommended Species | Why |
|----------|---------------------|-----|
| **DevKit v0.1 (NFC, Capacitive Sensing)** | *Pleurotus ostreatus* | Low cost, easy to source, **sufficient for passive NFC** (1–5 µW) |
| **Soil Moisture Sensor, Compost Monitor** | *Trametes versicolor* | High laccase activity, **compatible with BQ25570**, lignin substrates available |
| **High-Performance Research (260 µW target)** | *Neurospora crassa* | **Highest power density**, genetically well-characterized |
| **Mg-Air Hybrid Systems (Permafrost, Landfill)** | *Aspergillus niger* | Industrial robustness, **works with metallic electrodes (Mg)** |
| **Medical/Biocompatible Applications** | *Ganoderma lucidum* | **Biocompatible**, low power needs (0.5–5 µW) |

---

## Getting Started

```bash
# Clone
git clone https://github.com/tobias-weiss-ai-xr/mykovolt
cd mykovolt

# Build firmware
cd firmware && mkdir build && cd build
cmake .. -DCMAKE_TOOLCHAIN_FILE=../cmake/arm-gcc-toolchain.cmake
make -j4

# Validate PCB
kicad-cli pcb drc hardware/kicad/mykovolt_devkit.kicad_pcb

# Run all tests
python3 -m pytest tests/

# Generate everything from scratch
python3 hardware/kicad/generate_kicad.py

# Validate Gerbers for JLCPCB
python3 tools/validate_gerbers.py --thermal --bom
```

---

## License

- **Hardware:** [CERN-OHL-P v2](LICENSE_HARDWARE)
- **Firmware & Software:** [MIT](LICENSE)
- **Documentation:** CC-BY 4.0

---

*Built with curiosity for a planet that doesn't need more toxic waste in the ground.*
