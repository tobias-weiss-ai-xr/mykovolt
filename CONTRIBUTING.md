# Contributing to MykoVolt

MykoVolt is an open platform for vanishing electronics. Contributions of all kinds are welcome: hardware design, firmware, simulation, documentation, and use-case exploration.

## Getting Started

1. **Read the README** — understand the architecture and constraints
2. **Check the Issues** — look for `good first issue` labels
3. **Fork the repo** and create a feature branch off `main`

## Development Setup

```bash
# Python CLI tools
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Firmware (requires ARM GCC)
cd firmware && mkdir build && cd build
cmake .. -DCMAKE_TOOLCHAIN_FILE=../cmake/arm-gcc-toolchain.cmake
make -j4

# Run tests
python3 -m pytest tests/
```

## Before Submitting

- Run the full test suite: `python3 -m pytest tests/`
- For firmware changes: verify both targets compile: `cmake --build build`
- For PCB changes: `python3 hardware/kicad/generate_kicad.py && kicad-cli pcb drc hardware/kicad/mykovolt_devkit.kicad_pcb`

## License

By contributing, you agree that your contributions will be licensed under the same licenses as the project:
- Hardware: CERN-OHL-P v2
- Firmware & Software: MIT
- Documentation: CC-BY 4.0
