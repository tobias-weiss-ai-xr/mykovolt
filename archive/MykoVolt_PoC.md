# Anlage: Proof-of-Concept-Plan — MykoVolt

> **Bezug:** Geschäftsmodellskizze StartMiUp BM Wettbewerb 2026
> **Stand:** Juni 2026

---

## 1. Ziel des PoC

Experimenteller Nachweis, dass ein Hochleistungs-Pilzstamm (*Phanerochaete chrysosporium*) in einer 3D-gedruckten Cellulose-Tinte lebt, Strom produziert und rehydrierbar ist. Aufbauend auf Reyes et al. 2024 (12,5 µW/cm² mit *T. pubescens*), aber mit Transfer auf den leistungsfähigeren Stamm.

---

## 2. Minimal-Experiment (TRL 2→3, 3 Monate, ~5 k€)

### Materialien

| Posten | Beschreibung | Kosten |
|--------|-------------|-------|
| Pilzstamm | *P. chrysosporium* DSM 1556 (DSMZ Braunschweig) | ~150 € |
| Referenzstamm | *T. pubescens* (Kontrollgruppe) | ~50 € |
| 3D-Biodrucker | CELLINK BIO X oder modifizierter FDM (Uni-Labor) | Nutzung |
| Tintenrohstoffe | Cellulose-Nanofibrillen, CNC, Biochar, Carnaubawachs, Nährmedium | ~200 € |
| Messequipment | Potentiostat/Galvanostat, Multimeter, Klimakammer | Nutzung |
| Verbrauchsmaterial | Petrischalen, Malzagar, Pipetten, steriles Wasser | ~300 € |

### Versuchsablauf

| Schritt | Beschreibung | Dauer |
|---------|-------------|-------|
| 1. Stammkultur | P. chrysosporium auf Malz-Agar anziehen, Myzel ernten | 7–10 Tage |
| 2. Tintenmischung | Cellulose + Biochar + Wachs + Myzel-Suspension mischen | 1 Tag |
| 3. 3D-Druck | Tinte in Dual-Chamber-Design drucken (Anode: Pilz, Kathode: Luft) | 2–3 h |
| 4. Aktivierung | Trocknen (24 h, RT), Rehydrierung mit steriler Nährlösung | 1 Tag |
| 5. Dauerbetrieb | Leerlaufspannung (OCV) + Polarisation | 14 Tage |

### Erfolgskriterien

| Metrik | Minimal-PoC | Erstrebenswert | Reyes 2024 |
|--------|------------|---------------|-----------|
| Leerlaufspannung | >400 mV | >600 mV | ~550 mV |
| Leistungsdichte | >10 µW/cm² | >50 µW/cm² | 12,5 µW/cm² |
| Betriebsdauer | >7 Tage | >14 Tage | ~14 Tage |
| Rehydrierbarkeit | 1× trocknen + reaktivieren | 3× Zyklen | 1× gezeigt |
| Trockenlagerung | 2 Wochen | 6 Monate | n. t. |

---

## 3. Erweiterter PoC — Boden-Konkurrenz (TRL 3→4, 2 Monate, ~3 k€)

**Fragestellung:** Überlebt die Pilz-MFC im echten Ackerboden gegenüber einheimischen Bakterien?

**Aufbau:** Sensor-Gehäuse (3D-gedruckt) + MykoVolt-Zelle in Ackererde eines Bio-Betriebs. 14 Tage Dauerbetrieb.

| Versuchsvariante | Erwartung |
|-----------------|-----------|
| Sterilisierte Erde (Kontrolle) | Volle Leistung über 14 d |
| Unbehandelte Ackererde | Leistungsabfall Tag 3–7 |
| Ackererde + Lignin als selektives Substrat | Verzögerter Abfall |

**Erfolgskriterium:** Leistung >50 % der Lab-Kontrolle nach 7 Tagen in unbehandelter Erde. Lignin-Einbau als Schutzstrategie (nur Weißfäule-Pilze verdauen Lignin; Bakterien können es nicht).

---

## 4. Proof-of-Sensor (TRL 4, 4 Monate, ~7 k€)

Integration der MykoVolt-Zelle in ein funktionsfähiges Sensor-Kit (Developer Kit):

**Aufbau:**
- MykoVolt-Zelle (10 cm² aktive Fläche)
- 100 µF Kondensator (Zwischenspeicher für gepulsten Betrieb)
- BLE/NFC-Modul + µC + Temperatur-/Feuchtesensor
- PCB + Gehäuse aus biodegradierbarem Material

| Bauteil | Kosten | Lieferant |
|---------|--------|----------|
| MykoVolt-Zelle | ~5 € | Eigenbau |
| Kondensator 100 µF | 0,30 € | Mouser |
| BLE/LoRa-Modul | 3–5 € | Espressif/ST |
| µC + Sensor | 2–3 € | STM32/MAX |
| PCB + Gehäuse | 2–4 € | JLCPCB/Drucker |
| **Gesamt PoC-Kit** | **~12–15 €** | |

**Demonstration:** Messung → alle 15 min Daten per NFC → 7 Tage Laufzeit mit einer Zelle.

---

## 5. Abgrenzung — was der PoC beweist und was offen bleibt

| ✅ Im PoC nachweisbar | ❌ Noch offen (Folgeforschung) |
|----------------------|-----------------------------|
| P. chrysosporium überlebt Druckprozess + Trocknung | Langzeit-Haltbarkeit >6 Monate |
| Leistungssteigerung >12,5 µW/cm² | Fungizid-Toleranz im konventionellen Ackerbau |
| Rehydrierung funktioniert nach Trockenlagerung | Sporenfreisetzung / Biosicherheit |
| Developer Kit sendet Sensor-Daten per NFC | Stückkosten <5 € bei Massenfertigung |
| Boden-Konkurrenz beherrschbar (Lignin-Taktik) | Frost-Toleranz (Winterbetrieb) |

---

## 6. Kosten- & Zeitplan

| Phase | Dauer | Kosten | Finanzierung |
|-------|-------|--------|-------------|
| PoC 1: Minimal-Experiment | 3 Monate | ~5 k€ | EXIST-Seed (Sachmittel) |
| PoC 2: Boden-Konkurrenz | 2 Monate | ~3 k€ | Uni-Labornutzung |
| PoC 3: Sensor-Kit | 4 Monate | ~7 k€ | EXIST-Seed / Eigenanteil |
| **Gesamt** | **6–9 Monate** | **~15 k€** | EXIST-Gründungsstipendium |

---

## 7. Lokale Kooperationsmöglichkeit: SYNMIKRO Marburg

SYNMIKRO (Zentrum für Synthetische Mikrobiologie, Uni Marburg + MPI Terrestrische Mikrobiologie) forscht **nicht** an Pilz-Batterien oder mikrobiellen Brennstoffzellen — MykoVolt wäre in Marburg kein Duplikat. SYNMIKRO verfügt aber über exzellente Infrastruktur in Pilzbiologie (Myzel-Kultivierung, Stammcharakterisierung, Bioreaktoren), die für den PoC genutzt werden könnte. Eine Kooperation wäre komplementär: SYNMIKRO bringt die Mikrobiologie, MykoVolt die elektrochemische und drucktechnische Anwendung.

---

## 8. Nächste Schritte

1. DSMZ-Katalog: *P. chrysosporium* DSM 1556 Verfügbarkeit prüfen
2. Uni-Labor: Biodrucker- und Potentiostat-Zugang klären
3. Reyes 2024 *Supporting Information*: Tintenrezeptur extrahieren
4. EXIST-Antrag vorbereiten (nächste Runde Herbst 2026)
