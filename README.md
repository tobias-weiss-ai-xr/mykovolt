# MykoVolt — Vanishing Electronics Platform

**A modular, compostable sensing platform for environments where sensors can be placed but never retrieved.**

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
| `tests/` | 95 pytest tests (simulation, hardware, firmware, DRC, Gerber validation) |
| `tools/` | CI/CD, Gerber validation, parametric sweep, test fixture generator |
| `platform/architecture/` | Platform vision, layer specifications, research roadmap |
| `applications/` | Application-specific designs (DevKit → future products) |
| `docs/` | Business docs, grants, prototyping, technical specifications |

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

- **Hardware:** CERN-OHL-P v2
- **Firmware & Software:** MIT
- **Documentation:** CC-BY 4.0
