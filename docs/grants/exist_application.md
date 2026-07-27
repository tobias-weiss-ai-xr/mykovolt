# EXIST-Gründungszuschuss — MykoVolt

> **Deadline:** März 2027 (Antragsstichtag)  
> **Förderzeitraum:** 12 Monate (Phase 0: Lab Validation)  
> **Team:** 2 Gründer (GF + Co-Founder Mykologie/Elektrochemie)  
> **Budgetrahmen:** ~84.000 €  
> **Status:** Entwurf — Stand Juli 2026

---

## 1. Executive Summary

**MykoVolt** entwickelt die erste kommerzielle, biologisch abbaubare Pilz-Biobatterie für IoT-Sensoren. Die Technologie nutzt mikrobielle Brennstoffzellen auf Basis von Weißfäulepilzen, eingebettet in einen kompostierbaren Pressling. Zielmarkt sind Bodenfeuchtesensoren in der Präzisionslandwirtschaft — ein Markt mit >15 Mio. Sensoren/Jahr, die heute mit Li-Ion-Batterien betrieben werden und E-Waste verursachen.

**Technology Readiness Level:** TRL 2 (Konzept + Simulation abgeschlossen)  
**Phase 0 Ziel:** TRL 3 (experimentelle Machbarkeit im Labor)  
**Laufzeit:** 12 Monate, Start Q3 2027

---

## 2. Team

### Gründer (GF)

| Rolle | Person | Expertise |
|-------|--------|-----------|
| CEO / Business Development | *[Name]* | KI-Simulation, Business Development, Produktmanagement |
| CTO / Mykologie | *[Co-Founder wird gesucht]* | Pilzkultur, MFC-Aufbau, Elektrochemie |

**Aktueller Status:** GF identifiziert, Co-Founder wird aktiv rekrutiert  
**Rekrutierungskanäle:** LinkedIn, Uni Marburg (FLASH), EMC JLU, Bioverfahrenstechnik-Netzwerke  
**Deadline Co-Founder:** Oktober 2026 (6 Monate vor EXIST-Einreichung)

---

## 3. Technische Beschreibung

### 3.1 Dual-Path-Strategie

Phase 0 untersucht zwei parallele Technologiepfade:

| Pfad | Technologie | Vorteil | Risiko | Erfolgskriterium |
|------|-------------|---------|--------|------------------|
| **A: Air-Chimney Pressling** | Pilz-MFC mit O2-Versorgung | Einzigartig, volle Bioabbaubarkeit | Power < 12 µW in 10 cm Tiefe | > 12 µW @ 10 cm |
| **B: Mg-Air Battery** | Mg-Folie + Kohlekathode | Höhere Power, robuster | Mg-Korrosion, H2-Entwicklung | > 50 µW @ 10 cm |

### 3.2 Stand der Technik

**Simuliert & validiert (TRL 2):**
- Elektronentransport-Graph-Modell: 91% Übereinstimmung mit Empa-Literatur
- Bayessche Optimierung der Tintenformulierung: 8 Parameter, 260 µW/cm² (simuliert)
- Degradationsmodell: Arrhenius + pH + Feuchte → Powerabfall
- Produktkostenmodell: €0.15/Stück im Scale-up
- PCB-Design: 30×20 mm, 4-Layer, 57 Komponenten, Gerber-Dateien generiert
- Firmware: STM32L011, FDC1004, NFC, I2C-Bus, 100% compilierbar

**Experimentell noch offen (Phase 0 Ziel):**
- Pilzkultur unter Laborbedingungen
- Pressling-Formulierung und -Verdichtung
- O2-Diffusion im Boden mit/ohne Chimney
- Mg-Korrosionsrate in Bodenproben
- BQ25570 Boost-Converter mit realer MFC

### 3.3 Arbeitsplan (12 Monate)

Siehe [Phase 0 Execution Plan](../technical/phase0_execution_plan.md) für detaillierten Wochenplan.

| Monat | Pfad A (Air-Chimney) | Pfad B (Mg-Air) | Meilenstein |
|-------|---------------------|-----------------|-------------|
| 1 | Labor einrichten, T. pubescens Kultur | Mg-Folie, Material bestellen | Co-Founder an Bord |
| 2 | Erste OCV-Messung | Mg-Korrosionstest | Erste Daten |
| 3 | Pressling-Formulierung | Mg-Air Vollzelle | Materialauswahl |
| 4-6 | Chimney-Prototyp + Bodentest | Soil-Box-Test | Vorläufige Machbarkeit |
| 7-9 | Optimierung + Reproduktion | Optimierung + Reproduktion | Entscheidungskriterien messbar |
| 10-12 | Gate-Entscheidung + EXIST-Evaluation | Gate-Entscheidung + EXIST-Evaluation | **Gate 1** |

---

## 4. Marktanalyse

### Zielmarkt: Bodenfeuchtesensoren in der Präzisionslandwirtschaft

| Kennzahl | Wert | Quelle |
|----------|------|--------|
| Globaler Agrar-IoT-Markt (2030) | $7.2 Mrd. | Grand View Research |
| Sensoren pro Hektar (Präzisionslandwirtschaft) | 100-500 | Branchenberichte |
| Aktuelle Batteriekosten pro Sensor/Jahr | €0.35-1.50 (CR2032) | Marktpreise |
| E-Waste durch Agrar-Sensoren (2030) | >500 Mio. Batterien/Jahr | Hochrechnung |
| **MykoVolt-Kosten pro Messung** | **€0.15 + 0 g E-Waste** | **Simulationsmodell** |

### Wettbewerbsvorteil

| Kriterium | Li-Ion | Solar + Akku | MykoVolt |
|-----------|--------|-------------|----------|
| Untergrund geeignet | ✅ | ❌ | ✅ |
| Kompostierbar | ❌ | ❌ | ✅ (90%) |
| Kosten pro Jahr (1×/h) | €0.70 | €2.50+ | €0.15 |
| Wartung | Wechsel nötig | Reinigung | **Null** |

---

## 5. Verwertungsplan

### Phase 1 (2028): DevKit
- NFC-basiertes Sensor-Board für Forschungslabore
- TRL 4-5, Stückzahl 100-500
- Preis: €49-99/Kit (3 Presslinge + Elektronik)
- Kunden: Universitäten, Forschungslabore, Maker

### Phase 2 (2029+): Feldpilot
- LoRa-basierter Sensor für Forschungsbetriebe
- TRL 6-7, Stückzahl 1.000-10.000
- Preis: €19-39/Sensor
- Kunden: Agrarforschung, Umweltmonitoring

### Phase 3 (2031+): Kommerziell
- Massenproduktion, Stückzahl >100.000
- Preis: €8-15/Sensor
- Kunden: Landwirtschaft, Logistik, Bau

---

## 6. Finanzplan

### Kosten (12 Monate)

| Position | Monatlich | Gesamt |
|----------|-----------|--------|
| Gründungsstipendium GF | €2.500 | €30.000 |
| Gründungsstipendium Co-Founder | €2.500 | €30.000 |
| Labormiete | €500 | €6.000 |
| Geräte (Potentiostat, Presse, etc.) | — | €3.280 |
| Material (Pilzkulturen, Chemikalien, etc.) | €200 | €2.400 |
| PCB-Prototypen (5x) | — | €300 |
| Reisekosten (Konferenzen, Netzwerk) | €200 | €2.400 |
| Rechtsberatung (IP, Gründung) | — | €2.000 |
| Sonstiges (Büro, Kommunikation) | €150 | €1.800 |
| **Gesamt** | **~€7.000/Monat** | **~€84.000** |

### Finanzierung
| Quelle | Betrag | Status |
|--------|--------|--------|
| EXIST-Gründungszuschuss | ~€84.000 | **Beantragung März 2027** |
| BMBF KMU-innovativ (Parallel) | ~€150.000 | Option bei EXIST-Ablehnung |
| EIC Pathfinder (EU) | ~€200.000 | Phase 2 Option |

---

## 7. Nächste Schritte

| Deadline | Aufgabe | Verantwortlich |
|----------|---------|---------------|
| **August 2026** | Co-Founder-Rekrutierung starten | GF |
| **September 2026** | Laborkooperation klären (EMC JLU, Uni Marburg, TU Darmstadt) | GF |
| **Oktober 2026** | EXIST-Formulare studieren, Grobgliederung | GF + Co-Founder |
| **November 2026** | Business Plan Entwurf (20 Seiten) | GF |
| **Dezember 2026** | Technische Beschreibung (10 Seiten) | Co-Founder |
| **Januar 2027** | Stellungnahme Hochschule einholen | Co-Founder |
| **Februar 2027** | Vorläufige Ergebnisse + Finanzplan final | Beide |
| **März 2027** | **Einreichung EXIST-Antrag** | Beide |
