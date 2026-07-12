# Phase 0 Execution Plan — Dual-Path Validation

> **Zeitraum:** Juli 2026 – Juni 2027 (12 Monate)
> **Budget:** ~15–50 k€ (EXIST-Sachmittel oder Eigenmittel)
> **Team:** Gründer + Mykologie/Elektrochemie Co-Founder (Position #1)
> **Labor:** EMC JLU oder alternative Kooperation

---

## 1. Overview

Phase 0 hat zwei parallele Ziele:

| Pfad | Ziel | Erfolgskriterium | Deadline |
|------|------|------------------|----------|
| **A: Air-Chimney Pressling** | Empa 2024 reproduzieren + O2-Versorgung via Chimney validieren | Power > 12 µW bei 10 cm Tiefe | Monat 9 |
| **B: Mg-Air Battery** | Mg-Korrosionsrate messen + Leistung bei 10 cm validieren | Power > 50 µW bei 10 cm Tiefe | Monat 9 |

**Gate-Entscheidung (Monat 12):** Welcher Pfad geht in Phase 1?

---

## 2. Meilensteine

```
Monat 1  (Jul 2026): Laborzugang + Co-Founder an Bord
Monat 2  (Aug 2026): Erste Versuche (beide Pfade)
Monat 3  (Sep 2026): Datenlage beider Pfade bewertbar
Monat 6  (Dez 2026): Vorläufige Machbarkeit beider Pfade bekannt
                     EXIST-Einreichung (Deadline 2027-03)
Monat 9  (Mrz 2027): Entscheidungskriterien beider Pfade messbar
                     EXIST-Einreichung
Monat 12 (Jun 2027): Gate 1 — Pfad-Entscheidung
```

---

## 3. Wöchentlicher Plan (Monate 1–3)

### Monat 1: Setup

| Woche | Pfad A (Air-Chimney) | Pfad B (Mg-Air) | Admin |
|-------|---------------------|-----------------|-------|
| 1 | Labor beziehen, Sicherheitseinweisung | Gleiches Labor | Co-Founder Veträge |
| 2 | T. pubescens Kultur ansetzen (PDA-Platten) | Mg-Folie bestellen (99.9%, 0.5 mm) | EXIST-Formulare studieren |
| 3 | Flüssigkultur ansetzen (5× 100 mL) | CNF-Hydrogel-Rezeptur testen | Budget-Plan finalisieren |
| 4 | Erste OCV-Messung (Becherglas-MFC) | Mg in Wasser + Boden: Korrosions-Vortest | Laborbuch-Vorlage einrichten |

### Monat 2: Erste Experimente

| Woche | Pfad A | Pfad B |
|-------|--------|--------|
| 5 | MFC mit Kohlepapier-Elektroden aufbauen | Mg in 5 Bodenproben vergraben (Sand, Lehm, Ton, Kompost, pH 5/7/9) |
| 6 | Strom-Spannungs-Kennlinie aufnehmen (Potentiostat) | Wöchentliche Massenverlust-Messung |
| 7 | Laccase-Aktivitätstest (ABTS-Assay, 420 nm) | 1. Leistungsmessung: Mg + Carbon-Papier im Becherglas |
| 8 | Erste Presslinge pressen (nur Anode, 10 kN) | Elektrolyt-Variation (NaCl 0.01/0.1/1.0 M) |

### Monat 3: Pressling + Chimney

| Woche | Pfad A | Pfad B |
|-------|--------|--------|
| 9 | Pressling Anode + Kathode (10 kN, bilayer) | Mg-Air Vollzelle im Becherglas (BQ25570-Test) |
| 10 | Chimney-Prototyp: PTFE-Rohr Ø3 mm, O2-Messung im Boden | H2-Entwicklung messen (Wasserverdrängung) |
| 11 | Soil-Box-Test: Pressling mit/ohne Chimney bei 5/10/15 cm | Soil-Box-Test: Mg-Air bei 5/10/15 cm |
| 12 | Datenauswertung: Power-Vergleich mit/ohne Chimney | Datenauswertung: Power-Vergleich vs. Tiefe |

---

## 4. Laborausstattung

### Vorhanden (im Biolabor vorhanden)

| Gerät | Zweck | Pfad |
|-------|-------|------|
| Autoklav | Sterilisation | A |
| Sterilwerkbank | Pilzkultur | A |
| Brutschrank 25–30 °C | Inkubation | A |
| pH-Meter | Medien-Puffer | Beide |
| Feinwaage (0.1 mg) | Einwaage | Beide |
| Spektrometer (UV-Vis) | Laccase-Assay | A |
| Messzylinder/Pipetten | Medien | Beide |
| Kühlschrank + Gefrierer | Lagerung | Beide |

### Anzuschaffen (via EXIST oder Eigenmittel)

| Gerät | Kosten | Zweck | Pfad |
|-------|--------|-------|------|
| Handpresse + Matrize Ø 50 mm | ~800 € | Presslinge | A + B |
| Potentiostat/Galvanostat (gebraucht, z.B. Ivium PalmSens) | ~1.500 € | Elektrochemie | Beide |
| Multimeter mit Datenlogger (4×) | ~300 € | Langzeitmessung | Beide |
| Trockenschrank 40 °C | ~300 € | Pressling-Trocknung | A |
| Vakuumiergerät | ~200 € | Verpackung | A |
| Soil-Box (Plexiglas, 30×30×30 cm, 3 St.) | ~150 € | Bodentests | Beide |
| Temperaturfühler (DS18B20, 10×) | ~30 € | Boden-Temperatur | Beide |
| **Gesamt** | **~3.280 €** | | |

---

## 5. Materialbedarf (erste 3 Monate)

### Pfad A: Fungal Pressling

| Material | Menge | Kosten | Lieferant |
|----------|-------|--------|-----------|
| T. pubescens Stammkultur | 1 Stamm | ~50 € | DSMZ / CBS |
| PDA-Platten (fertig) | 20 St. | ~40 € | Carl Roth |
| Malt Extract Broth | 500 g | ~30 € | Sigma |
| CNF (Cellulose-Nanofibrillen, 2% Dispersion) | 1 L | ~80 € | NanoNovin / lokale Uni |
| Carbon Black (Super P) | 100 g | ~30 € | Alfa Aesar |
| Graphit Flakes (99%, < 50 µm) | 100 g | ~25 € | Sigma |
| ABTS (Tabletten) | 10 St. | ~60 € | Sigma |
| Laccase (aus T. versicolor, Ersatz) | 10 mg | ~120 € | Sigma |
| Glucose | 100 g | ~10 € | Sigma |
| Yeast Extract | 100 g | ~15 € | Sigma |
| PTFE-Schlauch Ø 3×5 mm | 10 m | ~15 € | Labshop |
| PLA-Filament (Chimney-Kappe) | 1 kg | ~25 € | Filamentworld |
| **Summe Pfad A** | | **~500 €** | |

### Pfad B: Mg-Air Battery

| Material | Menge | Kosten | Lieferant |
|----------|-------|--------|-----------|
| Mg-Folie (99.9%, 0.5 mm, 100×100 mm) | 5 St. | ~40 € | Alfa Aesar |
| Mg-Legierung AZ31 (Korrosionsvergleich) | 2 St. | ~30 € | Goodfellow |
| Kohlepapier (Sigracet 35BC) | 5 St. 5×5 cm | ~50 € | SGL Carbon / local |
| CNF (gleiche Charge wie Pfad A) | 200 mL | ~20 € | s.o. |
| NaCl (Reinst) | 100 g | ~10 € | Sigma |
| PTFE-Binder (60% Dispersion) | 50 mL | ~30 € | Sigma |
| **Summe Pfad B** | | **~180 €** | |

### Gemeinsam

| Material | Kosten |
|----------|--------|
| Bodenproben (Sand, Lehm, Ton, Kompost, je 20 kg) | ~40 € |
| Bechergläser, Kabel, Krokodilklemmen, Lötzubehör | ~50 € |
| Laborbuch (3 St.) | ~30 € |
| **Summe Gemeinsam** | **~120 €** |

**Gesamt Materialkosten (Monat 1–3): ~800 €**

---

## 6. Exit-Kriterien

Jeder Pfad kann vorzeitig beendet werden, wenn ein klares No-Go eintritt:

### Pfad A (Air-Chimney) — Abbruchkriterien

| Kriterium | Messung | Schwelle | Monat |
|-----------|---------|----------|-------|
| Keine MFC-Aktivität | OCV im Becherglas | < 50 mV nach 7 Tagen | 2 |
| Pressling tot | Power nach Pressen | < 1 µW (60% der ungepressten Kontrolle) | 4 |
| Chimney bringt kein O2 | O2-Sensor am Chimney-Ende | < 5% O2 bei 10 cm | 6 |
| Power unzureichend | 7-Tage-Test bei 10 cm | < 12 µW | 9 |

### Pfad B (Mg-Air) — Abbruchkriterien

| Kriterium | Messung | Schwelle | Monat |
|-----------|---------|----------|-------|
| Korrosion zu schnell | Massenverlust nach 7 Tagen | > 50% des Mg verbraucht | 2 |
| Korrosion zu langsam | Massenverlust nach 7 Tagen | < 0.1% (keine Reaktion) | 2 |
| Spannung zu niedrig | OCV unter Last | < 0.3 V (BQ25570 Startspannung) | 3 |
| H2-Entwicklung gefährlich | Gasvolumen/Tag | > 1 mL/Tag (Blasenbildung im Gehäuse) | 4 |
| Power unzureichend | 7-Tage-Test bei 10 cm | < 50 µW | 6 |

---

## 7. Entscheidungsbaum (Monat 12)

```
Gate 1 — TRL 3 erreicht (Juni 2027)
│
├── Nur Pfad A bestanden (Air-Chimney)
│   → Phase 1: DevKit mit Chimney-Pressling + passive NFC
│   → Mg-Air als Reserve für Phase 2 Feldpilot
│
├── Nur Pfad B bestanden (Mg-Air)
│   → Phase 1: DevKit mit Mg-Air + passive NFC
│   → Pressling als Forschungsthema weiterführen (Drittmittel)
│
├── Beide bestanden
│   → Phase 1 DevKit: BEIDE Optionen anbieten
│     - Chimney-Pressling (für Forschungslabore, "echte Pilzbatterie")
│     - Mg-Air (für Feldtests, höhere Leistung)
│   → Phase 2 Feldpilot: Mg-Air (zuverlässiger, O2-unabhängig)
│
├── Keiner bestanden
│   → Pivot auf passive NFC-only DevKit (KEINE Batterie)
│   → Bodenfeuchtesensor + NFC-Logging + austauschbare CR2032 (optional)
│   → Fungal MFC als reines Forschungsthema (Paper, nicht Produkt)
│
└── Co-Founder nicht gefunden
    → Phase 0 pausieren, Teilzeit-Gründung, Projekt-Status
    → Keine EXIST-Förderung ohne Co-Founder möglich
```

---

## 8. EXIST-Antrag (Deadline: März 2027)

Der EXIST-Gründungszuschuss ist der primäre Finanzierungspfad für Phase 0.

### Antragspaket

| Dokument | Verantwortlich | Deadline |
|----------|---------------|----------|
| Business Plan (20 S.) | GF | Dez 2026 |
| Technische Beschreibung (10 S.) | Co-Founder | Dez 2026 |
| Dual-Path-Strategie inkl. Risikoanalyse | GF + Co-Founder | Dez 2026 |
| Vorläufige Ergebnisse (beide Pfade) | Co-Founder | Feb 2027 |
| Stellungnahme der Hochschule | Prof. (EMC JLU) | Jan 2027 |
| Finanzplan | GF | Feb 2027 |

### EXIST-Budgetschätzung

| Posten | Monatlich | 12 Monate |
|--------|-----------|-----------|
| Gründungsstipendium GF | 2.500 € | 30.000 € |
| Gründungsstipendium Co-Founder | 2.500 € | 30.000 € |
| Sachmittel (Labor, Material, Geräte) | 2.000 € | 24.000 € |
| **Gesamt** | **7.000 €** | **84.000 €** |

Alternativ: EXIST-Forschungstransfer (mit Uni-Kooperation, bis 250 k€).

---

## 9. Template: Laborbuch-Eintrag

Jeder Versuchstag wird im Laborbuch dokumentiert (Markdown in `docs/testlog/`):

```markdown
# Testlog YYYY-MM-DD

## Pfad: A / B (Air-Chimney / Mg-Air)
## Versuch: [Kurzbeschreibung]

### Setup
- Charge/Batch: [ID]
- Temperatur: [°C]
- Boden: [Typ, Feuchte %]
- Tiefe: [cm]
- Elektronik: [Board-ID, Firmware-Version]

### Messungen
| Zeit | OCV [mV] | Strom [µA] | Leistung [µW] | pH | Temp [°C] | Bemerkung |
|------|----------|------------|---------------|----|-----------|-----------|
| 09:00 | 410 | 45 | 18.5 | 6.8 | 22 | Stabil |

### Beobachtungen
- [Anomalien, Auffälligkeiten, Farb-/Geruchsänderungen]

### Fazit
- Power: [µW] — über/unter Erwartung
- Nächster Schritt: [...]
```

---

## 10. Risikomanagement Phase 0

| # | Risiko | Eintritt | Impact | Mitigation |
|---|--------|----------|--------|------------|
| P0-1 | **Kein Laborzugang** (EMC JLU sagt nein) | Mittel | Kritisch | Alternative Unis anfragen (JLU Chemie, Uni Marburg, TU Darmstadt); Co-Working-Lab (e.g. BioLab) |
| P0-2 | **T. pubescens wächst nicht** | Niedrig | Hoch | Anderen Weißfäulepilz testen (P. chrysosporium, T. versicolor, P. ostreatus) |
| P0-3 | **Laccase-Aktivität nach Pressen = 0** | Hoch | Hoch | Niedrigere Presskraft (5 kN); Vorkultivierte Myzel-Platte statt Pulver; Pfad B forcieren |
| P0-4 | **EXIST abgelehnt** | Mittel | Hoch | BMBF KMU-innovativ Parallelantrag; Teilzeit-Gründung; EIC Pathfinder |
| P0-5 | **Mg korrodiert nicht in Lehm** | Niedrig | Mittel | Elektrolyt-Konzentration erhöhen; andere Legierung; Pfad A forcieren |
| P0-6 | **Mg korrodiert zu schnell (> 50 % in 7 d)** | Mittel | Niedrig | AZ31-Legierung (langsamer); Paraffin-Beschichtung; dünnere Folie verkleinert Problem nicht |

---

## 11. Erfolgskriterien für Gate 1

Am Ende von Phase 0 (Monat 12) muss mindestens EIN Pfad folgende Kriterien erfüllen:

| Kriterium | Pfad A (Air-Chimney) | Pfad B (Mg-Air) |
|-----------|---------------------|-----------------|
| Power @ 10 cm | > 12 µW | > 50 µW |
| Lifetime @ 15-min-Intervall | > 7 Tage | > 7 Tage |
| Bio-Abbau > 80 % | Nach EN 13432 Test | Nach EN 13432 Test |
| Kosten | < 1,00 €/Stück | < 0,50 €/Stück |
| Fertigungszeit | < 5 min/Stück | < 3 min/Stück |
| Reproduzierbarkeit | 3 von 3 Zellen > Kriterium | 3 von 3 Zellen > Kriterium |
| H₂-Risiko (nur B) | — | < 0,5 mL/Tag |
| Chimney-Integrität (nur A) | O2 > 5% bei 10 cm | — |

**Falls beide Pfade bestehen, entscheiden diese Faktoren:**
- Kosten (Mg-Air ist günstiger) → 30 %
- "Green Story" (Fungal ist einzigartiger) → 25 %
- TRL / Ausfallrisiko (Mg-Air ist robuster) → 25 %
- Fertigungskomplexität (Mg-Air ist einfacher) → 20 %
