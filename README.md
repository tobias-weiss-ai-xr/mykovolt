# MykoVolt - Biodegradable Fungal Battery for Precision Agriculture

## Overview

MykoVolt develops the first commercial, biodegradable Pilz-Biobatterie zur Stromversorgung von Bodenfeuchtesensoren in der Präzisionslandwirtschaft. Die Technologie nutzt mikrobiellen Brennstoffzellen (MFC) auf Basis von Weißfäulepilzen (*Trametes pubescens*, *Phanerochaete chrysosporium*), eingebettet in einen kompostierbaren Pressling.

### Key Innovation
- **Biologisch abbaubar**: Pilz-basierte Biobatterie + kompostierbares Gehäuse
- **Wiederverwendbar**: Elektronik-Board (100+ Zyklen)
- **Hybrider Ansatz**: Sofortiger Markteintritt mit vollständiger biologischen Abbaubarkeit als langfristiges Ziel

## Project Structure

### Core Components
- **DevKit** (Phase 1, Q4 2026): NFC-basierte Entwicklerplattform für Labore und Maker
- **Feldpilot** (Phase 2, Q2 2027): LoRa-basierte Feldlösung für landwirtschaftliche Betriebe

### Main Directories
- `simulation/` - Simulationen und Tests für Bodenfeuchte-Sensoren
- `archive/` - Historische Dokumente und Angebote
- `docs/` - Dokumentation (zukünftig)

### Key Files
- `MykoVolt-mvp-design.md` - Umfassende MVP-Design-Dokumentation
- `MykoVolt_Angebot_EMC.md` - Angebot für EMC GmbH
- `MykoVolt_Pitch_Deck.html` - Pitch Deck (interaktiv)

## Technical Specifications

### DevKit (Phase 1)
- **Pilzstamm**: *Trametes pubescens* (12,5 µW/cm²)
- **Kommunikation**: NFC (passiv powered)
- **Energieverbrauch**: ~0,14 mWh/Tag
- **Datenformat**: 12-Byte-Einträge (timestamp, capacitance, voltage, temperature, status)
- **Dauer**: 14 Tage bei 15-Minuten-Intervallen

### Feldpilot (Phase 2)
- **Pilzstamm**: *Phanerochaete chrysosporium* (erwartet 150× mehr Leistung)
- **Kommunikation**: LoRa (868 MHz, 2+ km)
- **Energieverbrauch**: ~0,60 mWh/Tag (SF12), ~0,09 mWh/Tag (SF7)
- **Gehäuse**: IP67, feldtauglich

## Current Status

### Recent Changes
- Aktualisierte Remote-Repository-URLs zu `mykovolt` mit originalen Benutzernamen
- GitHub-Repository erstellt und gepusht
- Codeberg-Repository auf `shrooms` belassen (wie angefordert)

### Active Development
- Simulation von Bodenfeuchte-Sensoren
- Tests für MFC-Leistung und Energieeffizienz
- NFC-basierte Datenübertragung
- FRAM-Ringpuffer für Datenspeicherung

## Getting Started

### Prerequisites
- Python 3.8+
- STM32CubeProgrammer (für NFC-Reader)
- LoRa-Stack (für Feldpilot)

### Installation
```bash
# Clone the repository
git clone https://github.com/tobias-weiss-ai-xr/mykovolt.git

# Navigate to project directory
cd mykovolt

# Install Python dependencies
pip install -r requirements.txt

# Install STM32 tools (if needed)
# STM32CubeProgrammer: https://www.st.com/en/development-tools/stm32cube-programmer.html
```

### Running Tests
```bash
# Run simulation tests
pytest simulation/

# Run unit tests for firmware
# (requires STM32 development environment)
```

## Documentation

### Available Documents
- `MykoVolt-mvp-design.md` - Vollständige MVP-Design-Dokumentation (536 Zeilen)
- `MykoVolt_Angebot_EMC.md` - Angebot für EMC GmbH
- `MykoVolt_Pitch_Deck.html` - Interaktive Pitch Deck

### Future Documentation
- `docs/` - Technische Dokumentation
- `docs/api/` - API-Referenz
- `docs/tutorials/` - Tutorials und Anleitungen
- `docs/roadmap/` - Projektmeilensteine

## Contributing

### Development Guidelines
1. **Test-First**: Schreiben Sie Tests vor dem Implementieren von Code
2. **Energieeffizienz**: Optimieren Sie den Stromverbrauch für Langzeitbetrieb
3. **Biologische Abbaubarkeit**: Bevorzugen Sie kompostierbare Materialien
4. **Dokumentation**: Halten Sie README und Code-Dokumentation auf dem neuesten Stand

### Code Style
- Python: PEP 8
- C/C++: STM32-Coding-Standards
- Markdown: Konsistente Formatierung

## License

This project is licensed under the MIT License.

## Contact

### Project Team
- **Website**: [tobias-weiss-ai-xr.github.io/mykovolt](https://tobias-weiss-ai-xr.github.io/mykovolt)
- **Email**: tobias.weiss.ai.xr@gmail.com
- **GitHub**: [tobias-weiss-ai-xr/mykovolt](https://github.com/tobias-weiss-ai-xr/mykovolt)
- **Codeberg**: [graphwiz-ai/mykovolt](https://codeberg.org/graphwiz-ai/mykovolt)

### Social Media
- **LinkedIn**: [MykoVolt](https://www.linkedin.com/company/mykovolt)
- **Twitter**: [@MykoVolt](https://twitter.com/MykoVolt)

## Future Roadmap

### Phase 1: DevKit (Q4 2026)
- [x] Pressling-Rezeptur finalisiert
- [x] Board-Design Rev A getapet-out
- [x] Prototyp (Funktionsmuster)
- [ ] L2-Systemtest bestanden
- [ ] EXIST-Einreichung
- [ ] DevKit Produktion Start
- [ ] DevKit Verkaufsstart

### Phase 2: Feldpilot (Q2 2027)
- [ ] Go/No-Go Feldpilot
- [ ] Feldpilot Feldtest
- [ ] Skalierung der Produktion

## Acknowledgments

Wir danken allen Unterstützern, Partnern und der Forschungsgemeinschaft für die Entwicklung dieser innovativen Technologie.

---

*Letzte Aktualisierung: $(git log --format="%cd" --date=short -1)*