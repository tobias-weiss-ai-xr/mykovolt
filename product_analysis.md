# Fungal Bio-Battery — Forming Methods & Product Concepts

> Denkwerkzeug: Welche Herstellungsverfahren jenseits 3D-Druck? Welche Produkte sind end-to-end simulierbar?

---

## 1. Forming Methods

Das Empa-Design nutzt **Direct Ink Writing (DIW)** — aber das ist weder die einzige noch die skalierbarste Methode.

### Vergleichstabelle

| Verfahren | Auflösung | Durchsatz | Zell-Verträglichkeit | Skalierbarkeit | Kosten |
|-----------|-----------|-----------|---------------------|----------------|--------|
| **DIW (3D-Druck)** | 100-500 µm | Niedrig (1 cm²/min) | ✅ Sehr gut | ⚠️ Langsam | Mittel |
| **Gepresste Pellet** | mm | **Sehr hoch** (1000/min) | ✅ Gut (keine Scherkräfte) | ✅ Pharma-Standard | **€€** |
| **Siebdruck** | 50-200 µm | Hoch (10 m²/min) | ⚠️ Scherkräfte riskant | ✅ Roll-to-Roll | **€** |
| **Filmgießen** | 20-500 µm | Mittel (1 m²/min) | ✅ Sehr gut | ✅ Einfach skalierbar | **€€** |
| **Elektrospinnen** | 50 nm-5 µm | Niedrig | ⚠️ Hochspannung | ⚠️ Langsam | €€€ |
| **Spritzguss** | 10-100 µm | **Sehr hoch** | ❌ Hitze tötet Zellen | ✅ Ideal | **€** (nur Struktur) |
| **Tauchen / Dip Coating** | 1-100 µm | Mittel | ✅ Sanft | ⚠️ Batch | **€** |

### Die 3 vielversprechendsten Alternativen

**1. Gepresstes Pellet ("Battery Tablet")** ⭐⭐⭐⭐⭐
- Einfachste Methode: Pulver (Cellulose + Carbon + Graphit + getrocknete Hefe/Laccase) → Pressen → Tablette
- Aktivierung: Wasser + Zucker → 24-72h Betrieb
- Kompostierung: Pilz baut Cellulose ab
- **Vorteil:** Pharma-Produktion (EU-GMP) existiert. Tablette ist das verständlichste Produktformat.
- **Simulation:** 100% E2E (unsere Modelle decken Pressdichte → Leitfähigkeit → Leistung ab)

**2. Siebdruck auf Papier** ⭐⭐⭐⭐
- Papier als Substrat + Separator → bedruckt mit leitfähiger Pilz-Tinte
- Flexible, dünne, biologisch abbaubare Batterie
- Standard-Roll-to-Roll (drukker, printed electronics)
- **Problem:** Scherkräfte könnten Hefezellen beschädigen → Lösung: Hefe nach dem Druck aufsprühen

**3. Filmgießen + Laminieren** ⭐⭐⭐⭐
- Dünne Filme: Anode (Hefe + Carbon), Separator (Cellulose), Kathode (Laccase + Carbon)
- Gestapelt und laminiert wie eine Li-Ion-Zelle
- **Vorteil:** Höchste Energiedichte durch dünne Schichten, bekannte Fertigung

### 3D-Druck ist der falsche Fokus für Scale-Up

Aktuelle README-Position: "3D-Druck als Kerninnovation" — das ist wissenschaftlich interessant, aber **kommerziell der falsche Weg**.

| Aspekt | 3D-Druck | Pressling / Folie |
|--------|----------|-------------------|
| Kosten pro Zelle | ~€5-10 | **€0.01-0.10** |
| Durchsatz | 1 Zelle/Stunde | **10.000 Zellen/Stunde** |
| Materialausbeute | ~50% | **>99%** |
| Anlagenkosten | €10k-100k | **€50k (Tablettenpresse)** |
| Skalierbarkeit | Handwerklich | **Industriell** |

**Empfehlung:** 3D-Druck für R&D + Prototyping (flexibel, viele Iterationen). Pressling/Folie für Produktion (billig, schnell, skalierbar).

---

## 2. Produktkonzepte (E2E simulierbar)

Die folgende Bewertung: wie gut deckt unsere bestehende Simulations-Pipeline (Graph + AI) das Produkt ab?

### Produkt A: Bodenfeuchte-Sensor-Tag ⭐⭐⭐⭐⭐

| Aspekt | Beschreibung |
|--------|-------------|
| **Was** | Biologisch abbaubarer Sensor für Landwirtschaft |
| **Batterie** | Pilz-Pressling, 260 µW, 72h Dauerbetrieb |
| **Sensor** | kapazitiver Bodenfeuchte-Sensor (einfach, passiv) |
| **Kommunikation** | NFC (gepowert vom Lesegerät) + RTC (von Batterie) |
| **Lebensdauer** | 7 Tage aktiv → dann Kompost |
| **Markt** | Präzisionslandwirtschaft ($12 Mrd. bis 2030) |
| **Wettbewerb** | Solar-betrieben, Li-Ion — keiner ist kompostierbar |
| **Regulierung** | Keine (kein Medizinprodukt) |

**E2E Simulation:**
```
Humus-Gehalt → Sensor-Kapazität → Messzyklus → Leistungsbudget
    → Batterie-Dimensionierung → Pressdichte → Lebensdauer
    → Abbau-Rate im Boden → vollständige Kompostierung
```
✅ Unsere Modelle decken alles ab (Leistung + Geometrie + Optimierung)

### Produkt B: Einweg-Diagnostik-Stromquelle ⭐⭐⭐⭐⭐

| Aspekt | Beschreibung |
|--------|-------------|
| **Was** | Kompostierbare Batterie für IVD-Schnelltests |
| **Batterie** | Siebgedruckt auf Papier, 100-200 µW, 30 Min |
| **Anwendung** | Powered Readout für Lateral-Flow-Tests (quantitativ statt "ja/nein") |
| **Lebensdauer** | Einmalgebrauch, dann Kompost |
| **Markt** | IVD ($100 Mrd., CI-Zielgruppe) |
| **Regulierung** | IVDR 2017/746 (braucht CE-Kennzeichnung) |

**E2E Simulation:**
```
Test-Antigen-Konzentration → Signal-Stärke → Readout-Power → Batterie-Bedarf
    → Screen-Print-Geometrie → Papier-Substrat → Leistung
    → Kosten pro Test → Break-even vs. Li-Ion-Diagnostik
```
✅ Unsere Modelle decken alles ab + CI hat IVD-Know-how + Kontakte
✅ **Synergie mit CI:** Gleiche Zielkunden (IVD-Hersteller)

### Produkt C: Temperatur-Logger für Kühlkette ⭐⭐⭐⭐

| Aspekt | Beschreibung |
|--------|-------------|
| **Was** | Kompostierbarer Logger für verderbliche Waren |
| **Batterie** | Pilz-Folie, 100 µW, 14 Tage |
| **Sensor** | BME280 (Temperatur, Feuchte) + FRAM-Speicher |
| **Display** | E-Paper (keine Dauerleistung nötig) |
| **Markt** | Kühlkette ($8 Mrd.), Lebensmittelverschwendung ($1T) |

**E2E:** ✅ Leistung + Geometrie + Lebensdauer komplett simulierbar

### Produkt D: MykoVolt R&D Platform ⭐⭐⭐⭐

| Aspekt | Beschreibung |
|--------|-------------|
| **Was** | Verkaufe die Simulations-Plattform an Pilz-MFC-Labore |
| **Kunde** | Empa, JKU Linz, akademische MFC-Forschung |
| **Wert** | 50× schnellere R&D, 90% weniger Experimente |
| **Preis** | €5k-20k/Jahr pro Lab |
| **Markt** | ~200 MFC-Labore global |

**E2E:** ✅ Unsere Pipeline IST das Produkt

---

## 3. Die entscheidende Frage

### Welches Produkt ist der schnellste Weg zum ersten zahlenden Kunden?

| Kriterium | Bodenfeuchte | IVD Test | Kühlkette | R&D Plattform |
|-----------|-------------|----------|-----------|---------------|
| Tech-Reife (Simulation) | 100% | 95% | 90% | **100%** |
| Marktbedarf | Hoch | **Sehr hoch** | Hoch | Nische |
| Regulierung | **Keine** | IVDR (6-12 Mo) | Keine | Keine |
| Erster Kunde in | **3-6 Monate** | 12-18 Monate | 6-12 Monate | **Sofort** |
| Wettbewerbsvorteil | Nachhaltigkeit | Kompostierbarkeit | Kein Li-Ion-Verbot | Einzige Plattform |

### Meine Empfehlung: Zweigleisig fahren

**Gleis 1: Bodenfeuchte-Tag (Produkt A)**
- Schnellster Weg zum Produkt
- Keine Regulierung
- Unser 260 µW reichen
- Formgebung: Pressling (einfach, sofort produzierbar)
- Verkauf: an Agrarbetriebe via CI-Vertrieb

**Gleis 2: IVD Power Source (Produkt B)**
- Synergien mit CI-Business maximal
- Gleiche Zielkunden
- Höherer Preis (B2B, nicht B2C)
- Erfordert IVDR-Compliance → passt zu CI's Regulatory-Intelligence-Thema
- **KI-Connection:** Die Simulations-Pipeline wird zum Verkaufsargument ("Designed by AI")

---

## 4. Nächster konkreter Schritt

Baue eine **E2E-Simulation für Produkt A (Bodenfeuchte)**:

```
Input: Bodenart (Sand/Lehm/Ton) + Feuchte %
  → Kapazitiver Sensor: C = ε0·εr·A/d
    → Sensor-Messzyklus: 1 Hz, 10 µW
      → MCW-Aufwach-Zyklus: STM32L0, 20 mW für 10 ms
        → Leistungsbudget über 7 Tage
          → Batterie-Dimensionierung: 260 µW verfügbar
            → Zyklen-Lebensdauer: 6.720 Messungen
              → Abbau im Boden: Cellulose → 90 Tage
                → Ausgabe: "1 Pilz-Batterie = 1 Woche Bodensensor"
```

Das ist simulierbar, quantifizierbar und pitchen gegenüber einem Landwirt:

> "Einmal in den Boden stecken, eine Woche lang Feuchte messen, dann zersetzt sich der Sensor von selbst. Null Müll, null Wartung."

Soll ich diese E2E-Simulation bauen?
