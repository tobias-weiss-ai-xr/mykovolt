# MykoVolt — MVP Design Document

**Datum:** 2025-06-26
**Status:** Entwurf
**Version:** 1.0

---

## 1. Übersicht & Architektur

### 1.1 Vision

MykoVolt entwickelt die erste kommerzielle, biologisch abbaubare Pilz-Biobatterie zur Stromversorgung von Bodenfeuchtesensoren in der Präzisionslandwirtschaft. Die Technologie nutzt mikrobiellen Brennstoffzellen (MFC) auf Basis von Weißfäulepilzen (*Trametes pubescens*, *Phanerochaete chrysosporium*), eingebettet in einen kompostierbaren Pressling.

### 1.2 Zwei-Phasen-Strategie

| Phase | Produkt | Zeitraum | Kommunikation | Pilzstamm | Zielgruppe |
|---|---|---|---|---|---|
| 1 | **DevKit** | Q4 2026 | NFC (ST25DV04K) | *T. pubescens* | Forschungslabore, Universitäten, Maker |
| 2 | **Feldpilot** | Q2 2027 | LoRa (SX1262) | *P. chrysosporium* | Landwirtschaftliche Betriebe |

### 1.3 Pilz-Strategie: Parallelansatz

```
T. pubescens (Phase 1)
  ├── Empa 2024 bestätigt: 12,5 µW/cm²
  ├── Sicher & gut charakterisiert
  ├── OCV 300-600 mV
  └── Ideal für BQ25570 Boost-Converter

P. chrysosporium (Phase 2 R&D)
  ├── Literatur: 1.900 µW/cm² (150× höher)
  ├── aktive Lignin-verwertende Enzyme
  ├── In Pressling-Form noch nicht validiert
  └── Parallel-Forschung parallel zu DevKit
```

### 1.4 Systemarchitektur

```
┌─────────────────────────────────────────────────┐
│                  Feld (Boden)                    │
│  ┌──────────────────────────────────────┐       │
│  │        Kompostierbares Gehäuse       │       │
│  │  ┌─────────────┐  ┌──────────────┐  │       │
│  │  │  Pressling   │  │  Elektronik  │  │       │
│  │  │ (Pilz-MFC)   │──│  Board       │  │       │
│  │  │  Ø 50 mm     │  │  (wiederver- │  │       │
│  │  │  h 8 mm      │  │  wendbar)    │  │       │
│  │  └─────────────┘  └──────────────┘  │       │
│  └──────────────────────────────────────┘       │
│                        │                        │
│                        ▼                        │
│  ┌──────────────────────────────────────┐       │
│  │       Kommunikation (Phase-abh.)     │       │
│  │  DevKit: NFC (passiv, Reader nötig)  │       │
│  │  Feldpilot: LoRa (868 MHz, 2+ km)    │       │
│  └──────────────────────────────────────┘       │
└─────────────────────────────────────────────────┘
```

### 1.5 Hybrid-Ansatz

- **Kompostierbar:** Pressling (Biobatterie) + Gehäuse (PLA/Stroh-Verbund)
- **Wiederverwendbar:** Elektronik-Board (100+ Zyklen, einfach umstecken)
- **Begründung:** Volle biologische Abbaubarkeit der Elektronik ist technisch noch TRL 3-4 (Zellulose-Leiterplatten in Forschung). Hybrid-Ansatz ermöglicht Markteintritt jetzt, während volle bio-degradable Elektronik parallel erforscht wird.

---

## 2. Phase 1: DevKit (Q4 2026)

### 2.1 DevKit-Komponenten

| Komponente | Beschreibung |
|---|---|
| **Pressling (3er-Pack)** | Pilz-MFC in Tablettenform, Ø 50 mm, h 8 mm, je 12,5 µW/cm² |
| **Sensor-Board** | STM32L011 + FDC1004 Kapazitiv-Sensor + FRAM + NFC |
| **Reader** | USB-NFC-Reader (ST25R3916) + Python-Tooling |
| **Gehäuse** | Kompostierbar (PLA/Stroh), wiederverwendbarer Deckel |
| **Dokumentation** | Datenblatt, Quickstart-Guide, Beispiel-Code, API-Referenz |

### 2.2 Board-Architektur (DevKit)

```
┌──────────────────────────────────────────┐
│          STM32L011K4 (TSSOP20)           │
│  ┌─────────┐  ┌──────────┐  ┌────────┐  │
│  │ FDC1004 │  │ FRAM     │  │ PCF8523│  │
│  │ (kap.   │  │ MB85RC16 │  │ RTC    │  │
│  │ Sensor) │  │ (16 KB)  │  │        │  │
│  └────┬────┘  └────┬─────┘  └────┬───┘  │
│       │            │            │       │
│  ┌────┴────────────┴────────────┴───┐   │
│  │        I²C Bus                   │   │
│  └──────────────────────────────────┘   │
│       │                                │
│  ┌────┴───────────────────────────┐    │
│  │  ST25DV04K (NFC Type 5)       │    │
│  │  • 4 KB EEPROM                │    │
│  │  • Passiv power-vom Reader    │    │
│  │  • I²C Interface zu MCU       │    │
│  └───────────────────────────────┘    │
│       │                                │
│  ┌────┴───────────────────────────┐    │
│  │  BQ25570 Boost-Converter      │    │
│  │  • Start ab 0,3V Eingang      │    │
│  │  • MPPT für MFC-Optimierung   │    │
│  │  • 1,8V Ausgang für STM32     │    │
│  └───────────────────────────────┘    │
└──────────────────────────────────────────┘
```

### 2.3 Energiebudget DevKit

| Komponente | Verbrauch | Täglicher Energiebedarf |
|---|---|---|
| STM32L011 (Sleep 1,8 µA) | 1,8 µA × 1,8 V | 0,078 µWh (idle) |
| FDC1004 (5 ms Messung) | 220 µA × 5 ms × 96/Tag | ~0,059 µWh |
| FRAM Schreiben (12 Bytes) | 100 µA × 1 ms × 96/Tag | ~0,005 µWh |
| PCF8523 RTC | 150 nA × 1,8 V | ~0,006 µWh |
| **Gesamt** | | **~0,14 mWh/Tag** |

| Pressling-Leistung (T. pubescens) | Energie | Lastauslastung |
|---|---|---|
| Minimal (12 µW) | 0,29 mWh/Tag | ~48 % |
| Typisch (100 µW) | 2,4 mWh/Tag | ~6 % |
| Maximal (260 µW) | 6,24 mWh/Tag | ~2 % |

> **Fazit:** Selbst im Minimal-Szenario (12 µW) ist die Energiebilanz positiv. Das System läuft zu ~48 % Auslastung — ausreichend für 15-Minuten-Messintervalle.

### 2.4 Kommunikationsablauf (NFC)

```
Reader ──→ Tag (NFC aktivieren)
         ←── Tag (Energie via RF)
         ──→ Request: "sende gespeicherte Daten"
Tag: MCU aufwachen → FRAM auslesen → NFC-EEPROM schreiben → Sleep
         ←── Reader: Daten aus NFC-EEPROM lesen
         ──→ Acknowledge → Tag löscht bestätigte Einträge
```

**Vorteil:** NFC-Readout ist *passiv powered* — der Reader liefert die Energie für die Datenübertragung. Der Pressling muss nur für Sensormessungen + RTC sorgen.

### 2.5 FRAM-Ringpuffer-Format

| Adresse | Inhalt | Größe |
|---|---|---|
| 0x000–0x0FF | Header (Magic, Version, Write-Pointer, Konfiguration) | 256 Bytes |
| 0x100–0x3FFF | Ringpuffer (1.365 Einträge à 12 Bytes) | 15.744 Bytes |

**Eintragsformat (12 Bytes):**

| Offset | Feld | Typ | Beschreibung |
|---|---|---|---|
| 0 | timestamp | uint32 | Unixzeit oder RTC-Counter |
| 4 | capacitance | uint16 | Rohwert FDC1004 (0-65535) |
| 6 | v_batt | uint16 | Pressling-Spannung in mV |
| 8 | temperature | uint16 | Temperatur in 0,1 °C |
| 10 | status | uint8 | Flags (error, calibration, etc.) |
| 11 | crc | uint8 | Checksumme |

**14 Tage Datenspeicher bei 15-Minuten-Intervallen** (1.365 Einträge).

---

## 3. Phase 2: Feldpilot (Q2 2027)

### 3.1 Upgrades gegenüber DevKit

| Bereich | DevKit | Feldpilot |
|---|---|---|
| Kommunikation | NFC (passiv, Reader nötig) | LoRa (868 MHz, aktiv, 2+ km) |
| Pilzstamm | *T. pubescens* | *P. chrysosporium* (erwartet 150× mehr Leistung) |
| Gehäuse | Labor-Design | IP67, Feld-tauglich |
| Datenübertragung | Manuelles Auslesen | Automatisch, Gateway-basiert |
| Stromverbrauch | 0,14 mWh/Tag | ~0,60 mWh/Tag (LoRa) |
| Pressling-Leistung nötig | 12 µW | ~200 µW (bei 12,5 % Last) |

### 3.2 LoRa-Energiebudget

| Betriebsart | Strom | Dauer | Täglicher Verbrauch |
|---|---|---|---|
| Sleep (STM32 + SX1262) | 2,5 µA @ 3,3 V | 23:58 h | ~0,20 mWh |
| Sensor-Messung | 220 µA | 5 ms × 96/Tag | ~0,01 mWh |
| LoRa TX (SF12, 14 dBm) | 45 mA | 1,2 s × 96/Tag | ~0,54 mWh |
| RTC | 150 nA @ 3,3 V | 24 h | ~0,01 mWh |
| **Gesamt (SF12)** | | | **~0,60 mWh/Tag** |

**Optimierung:** SF7 reduziert TX-Zeit auf 0,1 s → **0,09 mWh/Tag** (SF7-Verlust: Reichweite sinkt von ~5 km auf ~1 km).

### 3.3 Gateway-Architektur (Feldpilot)

```
Feldpilot Tag ──LoRa──→ Gateway ──MQTT──→ Cloud (ThingsBoard)
     ↑                    │
     │              ┌─────┴─────┐
     └──────────────│ LoRaWAN   │
                    │ Netzwerk  │
                    └───────────┘
```

- **Gateway:** ESP32 + SX1268, 868 MHz, Multikanal
- **Protokoll:** LoRaWAN 1.0.4 (Class A, OTAA)
- **Backend:** ThingsBoard (Open Source) für Visualisierung + Alarme
- **Payload:** 12 Bytes (identisch zu FRAM-Eintragsformat)

---

## 4. Fertigung & Pressling-Rezeptur

### 4.1 Materialzusammensetzung

| Komponente | Anode (%) | Kathode (%) | Funktion |
|---|---|---|---|
| CNF (Cellulose-Nanofibrillen) | 40 | 40 | Gerüst, biol. Abbaubarkeit |
| Carbon Black | 25 | 20 | Leitfähigkeit |
| Graphite (Flakes) | 15 | 10 | Elektronenleitung |
| Hefe (*S. cerevisiae*) | 10 | – | Elektronen-Donor |
| Laccase (aus *T. pubescens*) | – | 15 | Sauerstoff-Reduktion |
| ABTS | – | 5 | Elektronenvermittler (Mediator) |
| Glucose | 5 | – | Nährstoff für Hefe |
| Phosphatpuffer (pH 5,5) | 5 | 10 | pH-Stabilität |

### 4.2 Fertigungsprozess

```
1. Trockenmischung (alle Pulver, 5 min, Labormischer)
2. Feuchtigkeitskonditionierung (15-20 % deionisiertes Wasser)
3. Tablettierung (10-50 kN Presskraft, Pharma-Einzelpresse)
4. Trocknung (24 h, 40 °C, Umluft)
5. Qualitätskontrolle (Dicke, Gewicht, Leitfähigkeit, OCV)
6. Vakuumverpackung (Alu-Beutel, Feuchtigkeitsbarriere)
7. Chargenzertifikat
```

### 4.3 Pilot-Produktion (500 Presslinge)

| Posten | Kosten |
|---|---|
| Handpresse (Carver/Spek) + Matrize Ø 50 mm | ~800 € |
| Trockenschrank (gebraucht) | ~300 € |
| Vakuumiergerät | ~200 € |
| **Einmalkosten** | **~1.300 €** |
| Material 500 Presslinge (CNF, Carbon, Enzyme, etc.) | ~105 € |
| **Gesamt** | **~1.405 €** |

### 4.4 Skalierung (Phase 2)

- **Einzelpresse:** 10-20 Presslinge/h → 500 in 25-50 h
- **Rundläuferpresse (gebraucht ~50 k€):** 10.000 St./h
- **Direkt-Ink-Write (DIW) 3D-Druck:** 1 St./h, nicht geeignet für Produktion

---

## 5. Sensor-Board & Firmware

### 5.1 Bauteilauswahl

| Bauteil | Typ | Begründung |
|---|---|---|
| MCU | STM32L011K4 | 1,8 µA Sleep, TSSOP20 (manuell lötbar), ~1,50 € |
| Boost-Converter | BQ25570 | Booster ab 0,3V, MPPT, 1,8V Ausgang, ~3,50 € |
| NFC | ST25DV04K | 4 KB EEPROM, I²C, passiv power, ~1,20 € |
| FRAM | MB85RC16 | 16 KB, 10^13 Zyklen, I²C, ~1,80 € |
| RTC | PCF8523 | 150 nA, I²C, ~0,60 € |
| Sensor | FDC1004 | Kapazitiv, I²C, 4 Kanäle, ~3,00 € |
| **Gesamt Board BOM** | | **~13,55 €** |

### 5.2 Firmware-Architektur

```
main.c
├── init_hardware()
│   ├── init_clock()      // MSI 2.097 MHz
│   ├── init_i2c()         // 100 kHz
│   ├── init_rtc()         // PCF8523, 15-Min-Interrupt
│   ├── init_nfc()         // ST25DV04K I²C-Interface
│   └── init_sensor()     // FDC1004, Konfiguration
│
├── main_loop()
│   ├── sleep()            // STOP-Modus, ~1,8 µA
│   ├── wake_handler()     // RTC-Interrupt alle 15 Min
│   ├── measure()          // FDC1004 Lesen, Temperatur
│   ├── store()            // FRAM Ringbuffer Write
│   └── nfc_response()    // NFC-Readout vorbereiten
│
└── peripherals/
    ├── fdc1004.c          // Kapazitiv-Sensor Treiber
    ├── mb85rc16.c         // FRAM Treiber + Ringbuffer
    ├── pcf8523.c          // RTC Treiber
    ├── st25dv04k.c        // NFC-Interface
    └── bq25570.c          // Power Management
```

### 5.3 CLI-Tooling (Python)

```
mykovolt-cli/
├── mykovolt/
│   ├── __init__.py
│   ├── reader.py         # NFC-Reader Interface
│   ├── parser.py         # FRAM-Ringbuffer Parser
│   ├── calibrate.py      # Pressling-Kalibrierung (OCV, Leistungskurve)
│   ├── export.py         # CSV/JSON Export
│   └── plot.py           # Visualisierung (Verlauf, Spannung, Feuchte)
├── setup.py
└── README.md

# Beispiel-Nutzung:
$ mykovolt scan                   # NFC-Tag finden
$ mykovolt read                   # Alle Daten auslesen
$ mykovolt read --live            # Live-Messung + Anzeige
$ mykovolt export --csv data.csv  # Export
$ mykovolt calibrate              # Pressling-Kennlinie aufnehmen
$ mykovolt plot --voltage         # Spannungsverlauf anzeigen
```

---

## 6. Testplan & Validierungskriterien

### 6.1 Test-Level

| Level | Name | Beschreibung | Kriterium |
|---|---|---|---|
| L0 | **Component** | Einzeltests: Pressling-Leistung, Sensor-Genauigkeit, NFC-Reichweite | Spezifikation erfüllt |
| L1 | **Board** | Integration: Stromverbrauch, I²C-Kommunikation, Power-Up-Sequenz | Spezifikation erfüllt |
| L2 | **System** | Geschlossener Kreislauf: Pressling → Board → FRAM → NFC-Readout | Datenkonsistenz |
| L3 | **Field** | Labor-Simulator: Bodenfeuchte-Zyklus, Temperatur, Langzeit (4 Wochen) | >80 % Datenintegrität |

### 6.2 Go/No-Go-Gates

```
Gate 1 (L0 bestanden)
  ├── Pressling: OCV > 300 mV, Leistung > 12 µW
  ├── Sensor: ±2 % Genauigkeit bei 0-100 % VWC
  └── NFC: Reichweite > 2 cm, Readout > 95 % Erfolgsrate

Gate 2 (L1 bestanden)
  ├── Gesamtstrom < 2,0 µA im Sleep
  ├── I²C: Alle Peripherie erkannt, CRC-Fehler < 0,1 %
  └── Power-Up: BQ25570 startet bei Pressling > 0,3V

Gate 3 (L2 bestanden)
  ├── Schreiben → Lesen: 100 % Datenkonsistenz über 100 Zyklen
  ├── RTC: Abweichung < 5 s/Tag
  └── NFC: Vollständiger Readout in < 3 s

Gate 4 (L3 bestanden)
  ├── 4 Wochen Dauerbetrieb ohne Ausfall
  ├── Datenintegrität > 80 % (Verlust durch NFC-Fehllesungen)
  └── Pressling degradiert < 20 % Leistung über Testdauer
```

### 6.3 Test-Driven-Farming (TDF)

> "Kein Sensor kommt in den Boden, bevor er nicht 100 Stunden im Simulator bestanden hat."

**Test-Philosophie:**
1. Jeder Sensor durchläuft 168 h (7 Tage) Labor-Simulator vor Feld-Einsatz
2. Simulator fährt 3 Bodenfeuchte-Zyklen (trocken → feucht → trocken)
3. Bei <80 % Datenintegrität → Sensor zurück ins Labor
4. Daten werden mit Referenzsensor (TEROS 10/11) verglichen
5. Abweichung >5 % → Kalibrierung anpassen

### 6.4 Labornotizbuch-Struktur

Jeder Testtag in Markdown (siehe `docs/testlog/YYYY-MM-DD.md`):

```markdown
# Testlog 2025-11-15

## Setup
- Pressling Charge: PC-003
- Board ID: DK-007
- Temperatur: 22 °C ±1
- Boden: Einheitserde Typ P

## Messungen
| Zeit | V_mfc [mV] | I_mfc [µA] | Kapazität [pF] | VWC [%] | Status |
|---|---|---|---|---|---|
| 09:00 | 410 | 45 | 12.340 | 22,1 | ok |
| 09:15 | 408 | 43 | 12.350 | 22,3 | ok |

## Anomalien
- 11:30: Kurzer Spannungseinbruch auf 312 mV (30 s)
  - Ursache: vermutlich Luftblase im Pressling
  - Maßnahme: Pressling entlüftet, Spannung erholt auf 395 mV

## Fazit
- 96 % Datenintegrität (4/96 Einträge mit CRC-Fehler)
- Pressling stabil, leichte Degradation (2 % nach 7 Tagen)
- Nächster Schritt: L3-Feldtest mit Temperaturzyklus
```

---

## 7. Unit Economics & Go-to-Market

### 7.1 Kostenstruktur (Entwicklung)

| Phase | Posten | Kosten |
|---|---|---|
| R&D (vor DevKit) | Pressling-Rezeptur, Board-Design, Firmware | ~10 k€ |
| DevKit-Tooling | Handpresse + Matrizen + Trockenschrank | ~1.300 € |
| DevKit-Produktion (500 St.) | Material + Board + Zusammenbau | ~7.800 € |
| Feldpilot (50 St.) | SX1262 + robustes Gehäuse + Feldtest | ~3.500 € |
| **Gesamt MVP** | | **~22.600 €** |

### 7.2 Unit Economics — DevKit

| Position | Pro Kit (500 St.) |
|---|---|
| Pressling (3er-Pack) | 1,50 € |
| Sensor-Board (BOM) | 13,55 € |
| Reader (ST25R3916) | 8,00 € |
| Gehäuse | 1,50 € |
| Verpackung + Versand | 3,00 € |
| **COGS gesamt** | **24,55 €** |
| **Verkaufspreis** | **35 €** |
| **Deckungsbeitrag** | **10,45 €** |
| **Marge** | **~30 %** |
| **Umsatz 500 Kits** | **17.500 €** |
| **Gesamtdeckung** | **5.225 €** |

### 7.3 Unit Economics — Feldpilot

| Position | Feldpilot (5.000 St./J.) | Pressling-Nachsetzer (50.000 St.) |
|---|---|---|
| Pressling | 0,50 € | 0,15 € |
| Board (LoRa) | 5,50 € | – |
| Gehäuse | 0,50 € | 0,10 € |
| Zusammenbau | 1,00 € | – |
| **COGS** | **7,50 €** | **0,25 €** |
| Verpackung + Versand | 1,50 € | 1,00 € |
| **Verkaufspreis** | **15 €** | **5 €** |
| **Deckungsbeitrag** | **6,00 €** | **3,75 €** |

**Geschäftslogik:** Der Feldpilot (komplette Einheit) ist das Hauptprodukt. Pressling-Nachsetzer (nur die Batterie) generieren Wiederholkäufe und binden Kunden ans System. Nach ~4 Nachsetzern ist der Kunde profitabel.

### 7.4 Go-to-Market

#### Phase 1: DevKit (Q4 2026)

| Kanal | Zielgruppe | Volumen | Preis |
|---|---|---|---|
| Direktvertrieb | MFC-Forschungslabore (Empa, JKU, TU Delft, Fraunhofer) | 100 | 35 € |
| Agri-Tech-Konferenzen | Agritechnica, Sensor+Test | 200 | 30 € |
| Open-Source-Devices | Hackaday, CrowdSupply | 150 | 25 € |
| Universitäten | Biotech + Embedded Lehre | 50 | 20 € (Edu) |

**Value Prop DevKit:** *"First biodegradable fungal battery evaluation platform. Includes reference sensor, NFC readout, Python tooling. Data-sheet-grade characterization in hours, not months."*

#### Phase 2: Feldpilot (Q2 2027)

| Weg | Beschreibung | Aufwand |
|---|---|---|
| B2B Pilot | 3-5 Bio-Betriebe, 10 Sensoren/Betrieb, 14 Tage kostenlos | Niedrig |
| CAP-gefördert | Über Maschinenringe / Agrarberatung, 50 % Zuschuss | Mittel |
| Forschungskooperation | SYNMIKRO + Uni Marburg: Gemeinsame Publikation | Mittel |

### 7.5 Finanzierungspfad

```
Q3 2026     Q4 2026         Q1 2027         Q2 2027
│           │               │               │
Pressling   DevKit          DevKit-         Feldpilot
Rezeptur    Production      Feedback        Feldtest
Board-      → 500 Kits      → Auswertung    → Pilotproduktion
Design      Verkauf         Gate-Entscheid  → 3 Bio-Betriebe
            starten         Go/No-Go        → CAP-Anträge
│           │               │               │
├──── EXIST Einreichung ────┤
├─────────── Horizon Europe CL6 Antrag ─────────────┤
```

1. **EXIST-Gründungsstipendium** (Sachmittel ~15 k€) → PoC + DevKit
2. **DevKit-Verkaufserlös** (~5 k€ Deckung) → Feldpilot-Vorbereitung
3. **Horizon Europe CL6-2027-FARM2FORK** (€12 Mio. Call) → Feldpilot-Skalierung
4. **GAP/ELER-Förderung** → Subventionierter Sensorkauf für Landwirte

---

## 8. Meilensteine & Risiken

### 8.1 Meilensteine

| Datum | Meilenstein | Verantwortlich |
|---|---|---|
| 2025-08 | Pressling-Rezeptur finalisiert | Labor |
| 2025-10 | Board-Design Rev A getaped-out | Elektronik |
| 2025-12 | Prototyp (Funktionsmuster) | Team |
| 2026-03 | L2-Systemtest bestanden | QA |
| 2026-06 | EXIST-Einreichung | Geschäftsführung |
| 2026-09 | DevKit Produktion Start | Fertigung |
| 2026-11 | DevKit Verkaufsstart | Vertrieb |
| 2027-01 | DevKit-Feedback-Auswertung | Produkt |
| 2027-03 | Go/No-Go Feldpilot | Team |
| 2027-06 | Feldpilot Feldtest | Feld |

### 8.2 Risiken & Mitigation

| Risiko | Eintrittswahrsch. | Auswirkung | Mitigation |
|---|---|---|---|
| Pressling-Leistung < 12 µW | Mittel | Hoch | T. pubescens + P. chrysosporium parallel entwickeln |
| FRAM-Datenverlust durch NFC | Gering | Mittel | CRC-Prüfung, Reader-Bestätigung vor Löschen |
| LoRa-Reichweite < 1 km | Mittel | Mittel | SF12 als Default, SF7-Optimierung optional |
| EU Battery Regulation Verbot | Gering | Sehr hoch | Frühzeitig Ausnahmeregelung beantragen |
| Bactery AB Markteintritt vor uns | Mittel | Hoch | DevKit als Entwickler-Plattform positionieren (kein Wettbewerb) |
| Enzym (Laccase) Degradation | Mittel | Mittel | Vakuumverpackung, Kühlkette bis Auslieferung |

---

## 9. Anhang

### 9.1 Referenzen

- Empa 2024 — *Trametes pubescens* MFC Charakterisierung (12,5 µW/cm²)
- Bactery AB — Soil MFC mit 25-30 Jahren Lebensdauer (~£25)
- EU Battery Regulation 2023/1542 — Phase-out single-use batteries
- STM32L011 Datasheet — 1,8 µA STOP-Modus
- BQ25570 Datasheet — Boost ab 0,3V, MPPT
- FDC1004 Datasheet — Kapazitiver Sensor, I²C, 4-Kanal

### 9.2 Begriffe

| Begriff | Definition |
|---|---|
| MFC | Mikrobielle Brennstoffzelle |
| Pressling | In Tablettenform gepresste Pilz-Biobatterie |
| DevKit | Entwickler-Kit für Laboranwendung |
| Feldpilot | Feldtauglicher Prototyp für landwirtschaftliche Tests |
| FRAM | Ferroelectric RAM, nichtflüchtig, extrem hohe Schreibzyklen |
| OCV | Open Circuit Voltage (Leerlaufspannung) |
| MPPT | Maximum Power Point Tracking |
| VWC | Volumetric Water Content (volumetrischer Wassergehalt) |
