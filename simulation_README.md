# Fungal Bio-Battery — AI-Driven Graph Simulation Suite

> **Status:** Vollständige Simulations-Pipeline für eine pilzbasierte mikrobielle Brennstoffzelle
> **Basis:** Empa-Design (Reyes et al. 2024) — 3D-gedruckte Pilz-MFC mit *S. cerevisiae* (Anode) + *T. pubescens* (Kathode)
> **Simulationsziel (experimentell unbestätigt):** 15-20× Steigerung gegenüber Empa-Baseline (12.5 µW/cm² → ~260 µW/cm²)

---

## Überblick

Diese Simulations-Suite modelliert die pilzbasierte Bio-Batterie als **gerichteten Graph** und optimiert sie mit **KI-Methoden** (Bayesian Optimization, Evolutionäre Strategien, Reinforcement Learning).

```
Level 0: Graph-Modell des Elektronentransports (Max-Flow/Min-Cut Bottleneck-Analyse)
Level 1: Bayesian Optimization der Tinten-Formulierung (8 Parameter)
Level 2: Random Forest Synergy Analysis (Parameter-Interaktionen)
Level 3: Evolutionäre Optimierung der Druck-Geometrie (6 Parameter)
Level 4: E2E-Produktsimulation (Bodenfeuchte-Sensor-Tag)
Level 5: Multi-Objective Optimierung (Power/Cost/Lifetime/Compostability)
Level 6: Physics-Informed GP Degradationsmodell
Level 7: Uncertainty-Aware Digital Twin (Bootstrap-Ensembles)
```

## Dateien

| Datei | Level | Beschreibung |
|-------|-------|-------------|
| `electron_transport_graph.py` | 0 | Graph-Modell der e⁻-Transportkette (Max-Flow, Bottleneck, Maximalleistung) |
| `visualize.py` | 0 | Visualisiert den Transport-Graphen + Power-Kurve |
| `ai_optimizer.py` | 1+2 | Bayesian Optimization (GP + EI) + Random Forest Synergie-Analyse |
| `print_geometry_optimizer.py` | 3 | Differential Evolution + CMA-ES für Druck-Geometrie |
| `e2e_soil_sensor.py` | 4 | E2E-Produktsimulation: Bodenfeuchte-Tag (Boden → Leistungsbudget → Kompost) |
| `multi_objective_optimizer.py` | 5 | Multi-Objective BO (Pareto-Front: Power/Cost/Lifetime/Compostability) |
| `degradation_model.py` | 6 | Physics-Informed GP: Degradation (Arrhenius + pH + Moisture → Power/OCV/R_int) |
| `uncertainty_aware_twin.py` | 7 | Bootstrap-Ensemble Digital Twin (95% CI auf alle Vorhersagen) |
| `pressling_viability.py` | 8 | **Pressling-Viability:** O2-Diffusion im Boden, Pressschäden, Monte-Carlo (deckt O2-Problem auf) |
| `alternatives.py` | 9 | **Alternativen-Vergleich:** Air-Chimney, Mg-Air, Split-MFC, NFC-passiv, Tiefen-Sweep, Gewichtete Entscheidungsmatrix |
| `product_analysis.md` | — | Analyse alternativer Formgebungsverfahren + Produktkonzepte |

## Ergebnisse

### Level 0: Graph-Simulation

| Metrik | Simulation | Empa (Literatur) | Validierung |
|--------|-----------|-----------------|-------------|
| Max Strom | **45.0 µA** | 49.2 µA | ✅ 91% Übereinstimmung |
| Max Leistung | **44.6 µW/cm²** | 12.5 µW/cm² | 3.6× (optimierte Konfiguration) |
| Bottleneck | **Ohmscher Widerstand** | — | Physikalisch plausibel |

### Level 1: Tinten-Optimierung

| Ergebnis | Wert |
|----------|------|
| Beste Formulierung | **261 µW/cm²** (20.9× Empa) |
| Optimale Tinte | 11.8% Carbon Black, 24.5% Graphit |
| #1 Hebel | Graphit-Flocken (80.6% Impact) |
| #2 Hebel | Carbon Black (13.0% Impact) |

### Level 2: Synergie-Analyse

Parameter ranking by impact on power:
1. graphite_flake_pct         80.6%
2. carbon_black_pct           13.0%
3. layer_height_um             1.8%
4. mediator_conc_mM            1.4%
5-8. Rest                      3.2%

**Interpretation:** Biologische Parameter (Laccase, Hefe) sind NICHT limitierend. Der Engpass ist rein ohmsch.

### Level 3: Geometrie-Optimierung

| Ergebnis | Wert |
|----------|------|
| Beste Leistung | **86.3 µW/cm²** (5.5× Empa-Geometrie) |
| Optimale Geometrie | 500 µm Layer, 100% Infill, 1 mm Spacing |

**Interpretation:** Optimum liegt an den Grenzen des Parameterraums — maximale Leitfähigkeit durch minimale Abstände.

### Level 4: E2E Bodenfeuchte-Tag

| Metrik | Fungal Bio-Battery | Li-Ion (CR2032) | AAA Alkaline |
|--------|-------------------|-----------------|--------------|
| Kosten | **€0.15**¹ | €0.35 | €0.15 |
| Masse | **0.12 g** | 3.0 g | 11.5 g |
| Lebensdauer | 7 Tage | 180 Tage | 60 Tage |
| Kompostierbar | **✅ 0.11 g** | ❌ 0 g | ❌ 0 g |
| Leistung | 260 µW¹ | 5000 µW | 10 mW |
| Spannung | 0.45V (boost nötig) | 3.0V | 1.5V |

> ¹ Massenproduktions-Schätzung des reinen Presslings (Material + Verarbeitung), konsistent mit der Analyse in [MykoVolt-mvp-design.md](../MykoVolt-mvp-design.md#77-bom-preis-lücke). Die frühere Schätzung von €0,05 basierte auf optimistischeren Materialkosten vor dem aktuellen Feasibility-Review.
>
> ² Simulationsziel aus Bayesian Optimization (260 µW = 20× Empa-Baseline). Experimentell bislang nur 12.5 µW/cm² (Empa 2024) bestätigt. Der tatsächlich erreichbare Wert hängt von Tintenformulierung und Zellgeometrie ab.

## Physikalisches Modell

### Elektronentransport-Graph

```
glucose → nadh → abts_red → abts_ox → anode → circuit → cathode → laccase_red → laccase_ox → o2 → h2o
```

Jede Kante hat eine Kapazität in mol e⁻/s, berechnet aus Michaelis-Menten-Kinetik, Diffusion, Ohm'schem Gesetz und Stoffwechselrate.

### Eingesetzte KI-Verfahren

| Verfahren | Bibliothek | Zweck |
|-----------|-----------|-------|
| Gaussian Process Regression | scikit-learn | Surrogat-Modell für BO |
| Expected Improvement | scipy | Nächste Experimente vorschlagen |
| Differential Evolution | scipy | Globaler Geometrie-Optimierer |
| CMA-ES | Eigenbau | Evolutionäre Strategie |
| Random Forest | scikit-learn | Feature-Importance + Synergien |
| Latin Hypercube Sampling | scipy.stats.qmc | Initial-Stichprobe |
| Max-Flow/Min-Cut | networkx | Bottleneck-Analyse |

## Kritischer Befund: O2-Starvation (pressling_viability.py)

Die Pressling-Simulation hat einen fundamentalen Fehler im ursprünglichen Design aufgedeckt:

> **Die Laccase-Kathode braucht O2. In 10 cm Bodentiefe gibt es praktisch keins.**
> Millington-Quirk-Diffusionsmodell: O2 < 0.1% in feuchtem Lehm ab 5 cm Tiefe.

### Ergebnisse der Monte-Carlo-Simulation (10.000 Samples)

| Metrik | Wert |
|--------|------|
| P(viable für 7 Tage) | **8.7 %** |
| Mittlere Lebensdauer | 6.0 Tage |
| Median | 1.0 Tag |
| Mittlere Leistung | 2.8 µW |

**Konsequenz:** Dual-Path-Strategie beschlossen (siehe MykoVolt-mvp-design.md Section 9).

## Alternativen-Vergleich (alternatives.py)

| Rang | Ansatz | Score | TRL | O2-unabhängig | Bemerkung |
|------|--------|-------|-----|---------------|-----------|
| 1 | **Passive NFC** (kein Akku) | 0.800 | 9 | ✅ | DevKit-Start, kein Logging |
| 2 | **Mg-Air Battery** | 0.784 | 3 | ✅ (Wasserreduktion) | Backup-Pfad, höchste Bio-Abaurate |
| 3 | Zn-Air Battery | 0.702 | 5 | ❌ | Gleiches O2-Problem |
| 4 | Shallow Burial (2 cm) | 0.617 | 2 | ❌ | Landwirtschaftlich unpraktisch |
| 5 | Air-Chimney Pressling | 0.598 | 2 | ❌ (braucht Röhre) | Hauptpfad, Chimney nötig |
| 6 | Split MFC (Oberflächen-Kathode) | 0.578 | 2 | ❌ | Zu komplex, kein Bio-Draht |

## Erkenntnisse für die R&D-Strategie

1. **Ohmscher Widerstand ist der Flaschenhals** — Tintenleitfähigkeit optimieren, nicht Enzyme
2. **3D-Druck ist für Scale-Up falsch** — Presslinge/Folien sind 100-1000× schneller
3. **O2-Starvation ist der Killer** — Pressling braucht Air-Chimney oder Mg-Air-Backup
4. **Simulationsziel 260 µW/cm²² reicht für IoT-Sensoren** — aber nur wenn O2-Problem gelöst
5. **Erstes Produkt: DevKit mit NFC-passiv** — kein Akku nötig, TRL 9, sofort lieferbar
6. **Zweites Produkt: Feldpilot mit Mg-Air** — höhere Erfolgswahrscheinlichkeit als Pressling

## Ausführung

```bash
pip install --break-system-packages networkx matplotlib scipy scikit-learn pytest
cd simulation
python3 electron_transport_graph.py  # Level 0
python3 ai_optimizer.py              # Level 1+2
python3 print_geometry_optimizer.py  # Level 3
python3 e2e_soil_sensor.py           # Level 4
python3 pressling_viability.py       # Level 8: O2-Starvationsanalyse + Monte-Carlo
python3 alternatives.py              # Level 9: Dual-Path-Vergleich
python3 visualize.py                 # Plots
pytest tests/                        # Run all 35 tests
```

