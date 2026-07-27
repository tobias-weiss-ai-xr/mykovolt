# DevKit — MykoVolt Platform Instantiation v0.1

The first instantiation of the MykoVolt platform. A 30×20mm NFC data logger with a compostable battery, designed for researchers working on ephemeral sensing applications.

## Platform Layers

| Layer | Implementation | Location |
|-------|---------------|----------|
| Power | Fungal MFC / Mg-Air + BQ25570 boost | Hardware design |
| Sensing | FDC1004 capacitive → interdigital electrodes | Hardware design + firmware |
| Compute | STM32L011 + MB85RC16 FRAM + PCF8523 RTC | Firmware |
| Communication | ST25DV04K NFC (ISO 15693) | Hardware design + firmware |
| Manufacturing | PCB Generator + Design Rules + CI/CD | `hardware/kicad/` + `tools/` |

## Quick Links

- **PCB Design:** `../../hardware/kicad/` — KiCad project, Gerbers, design rules
- **Firmware:** `../../firmware/` — STM32L011 C code, ARM GCC build
- **Simulation:** `../../simulation/` — 11-level simulation pipeline
- **Tools:** `../../tools/` — CI/CD, validation, sweep, fixture
- **Platform Architecture:** `../../platform/architecture/overview.md`
