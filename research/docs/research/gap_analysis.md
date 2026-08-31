# 🔍 MFC Research Corpus — Quellen-Audit & Gap-Analyse

> **Stand:** 2026-08 · **Anlass:** Voll-Audit aller DOIs gegen CrossRef/OpenAlex
> **Ergebnis:** 26% des Korpus (23/90) waren nicht verifizierbar → entfernt; 29 verifizierte Papers nachgezogen; **Korpus jetzt 100% DOI-verifiziert** (96 Papers).

---

## 1. Executive Summary

| Metrik | Vor Audit | Nach Audit |
|--------|-----------|------------|
| Papers total | 90 | **96** |
| DOI-verifiziert | 67 (74%) | **96 (100%)** ✅ |
| Pilzbezogen (echt) | 43 (inkl. Halluzinationen) | **36** |
| Tote DOIs (404) | 15 | 0 |
| DOI→falsches Paper (Mismatch) | 7 | 0 |

**Zentrale Erkenntnis:** Zwei Sessions (Seed-Kuration + Web-Kuration) hatten unbemerkt **23 halluzinierte Einträge** eingebracht — darunter DOIs mit Signatur-Ziffern (`D4TA01234E`, `4c00123`), Titel-Mismatches (DOIs zeigten auf Lungenkrebs-/Algen-/Gassensor-Papers) und templathafte Titel ("X for enhanced electron transfer in microbial fuel cells"). **Die Spezies-Bewertung (Neurospora 260 µW/cm² u.a.) beruhte teilweise auf diesen Quellen und wurde zurückgezogen.**

---

## 2. Audit-Methodik

1. **Vollscan:** Alle DOIs gegen `api.crossref.org/works/{doi}` (User-Agent mit mailto, 0.35s Abstand)
2. **Titel-Match:** Wortüberlappung ≥50% (Stoppwörter entfernt) zwischen papers.yaml-Titel und CrossRef-Titel
3. **Reparatur-Versuch:** OpenAlex-Suche nach echten Papers für defekte Titel (≥60% Überlappung) → **0 Treffer** = alle 23 waren vollständig halluziniert
4. **Nachzug:** Gezielte CrossRef-Such-API-Queries pro Gap-Zelle, nur Einträge mit existierendem DOI, Venue-Pflicht, Vanity-Domain-Ausschluss (Research Square, Preprints.org), Typ-Filter (journal/proceedings/book-chapter)

---

## 3. Gap-Analyse (Dimensionen)

### 3.1 Spezies-Evidenz — NACH dem Audit

| Spezies | Verifizierte Papers | Status | Konsequenz für MykoVolt |
|---------|--------------------|--------|------------------------|
| *Trametes hirsuta/versicolor* | **2** (Shleev-Linie: DET, Bioelectrochemistry 2013; Electroanalysis 2006) | ✅ Fundament wiederhergestellt | **Primärspezies validiert** — Laccase-DET ist real, aber *Leistungszahlen* fehlen |
| *Saccharomyces cerevisiae* | **2** (PPy-modifiziert, Biosensors 2025; Elektroden-Größe, Ionics 2021) | ✅ Neu & stark | **Direkt hardware-relevant**: Elektroden-Geometrie ↔ Power für unsere 2-cm²-Designs |
| *Aspergillus niger* | **2** (Bioelectricity + Dye Decolorization, JBR 2016) | ✅ Qualitativ belegt | Bioelectricity-Demonstration real; µW-Zahlen aber unbelegt |
| *Pleurotus ostreatus* | 2 (Biowelding 2023; CABI ausgeschlossen) | ⚠️ Teilweise | **Biowelding/Substrat-Integration belegt, Stromerzeugung NICHT** |
| *Ganoderma lucidum* | 1 (Livestock-Feed-Noise entfernt → mycelium-electrical 2022?) | ⚠️ Dünn | Nur Material-Kandidat, keine MFC-Evidenz |
| *Neurospora crassa* | **0** | ❌ **Lücke ist real** | **Keine Elektrochemie-Literatur existiert** — 260 µW/cm² war halluziniert. Pursuing = genuine Forschungs-Lücke |
| *Pestalotiopsis microspora* | 0 | ❌ | PU-Abbau real, Graphen/Bioelektro chemie unbelegt |
| *Phanerochaete chrysosporium* | 0 | ❌ | Klassischer Weißfäule-Modellorganismus fehlt |

### 3.2 Themen-Abdeckung (verifiziert, Titel-basiert)

| Thema | Vorher | Nachher | Bewertung |
|-------|--------|---------|-----------|
| Laccase/Enzym-Elektroden | 20 (inkl. fake) | **22** | ✅ Stärkste Säule |
| MPPT/Power-Management | 0 | **7** | ✅ **Größter Zuwachs** — inkl. "Net power positive MPPT for MFC" (J Power Sources 2019) + PMS-Evaluierung (Bioelectrochemistry 2024) — direkt BQ25570-relevant |
| Mycel-Elektronik/Sensing | 0 | **5** | ✅ Adamatzky-Linie: lebende Myzel-Komposite unterscheiden Gewichte via elektrischer Signale (2022/2023) |
| Transiente/Biologisch abbaubare Elektronik | 2 | **5** | ✅ Kern-These gestärkt |
| Sediment/Plant-MFC (Kontext) | vorhanden | 4 | ✅ Application-Kontext |
| Cellulose-Elektroden | 0 | **3** | ✅ Material-Lücke für Biodeg-PCB |
| Lebensdauer/Stabilität | 6 (inkl. fake) | **3 echt** | ⚠️ Aber: **1-Jahr-stabile Glucose/O₂-BFC** (Bioelectrochemistry 2015) ist der stärkste Beleg |
| DET (Direct Electron Transfer) | 0 | **2** | ✅ Fundament |
| Mg-Air/Metall-Luft | 0 | **2** | ✅ Backup-Konzept untermauert |
| Implantierbar/Medizin | 0 | **2** | ✅ Future-Track |
| BOD-Sensor | 0 | **1** | ⚠️ dünn |
| **Co-Kulturen (Pilz+Bakterium)** | 1 (fake) | **0** | ❌ **Echte Lücke** — Frontier-Thema ohne verifizierte Basis |
| **NFC/RFID-Readout für BFC** | 0 | **0** | ❌ **Echte Lücke** — exakt unser DevKit-Feature |
| **Leistungsbenchmarks (µW/cm², fungal)** | 7 (inkl. fake) | ~5 | ⚠️ Systematische Messreihen fehlen |

### 3.3 Taxonomie-Zellen

```
                laccase  eet  hybrid  degradation
mechanism         ✓✓      ✓     ⚠️        ✓✓      (mechanism/hybrid dünn)
material          ✓✓      ✓     ⚠️        ✓✓      (material/hybrid dünn)
application       ✓       –     ✓✓        ❌       (application/degradation = 3, Kernlücke!)
survey            ❌      –     ⚠️        –        (survey/laccase = 0!)
```

**Kritisch:** `application/degradation` — unsere Vanishing-Electronics-These hat nur 3 direkte Papers. `survey/laccase` (0): kein aktueller Review der Laccase-BFC-Landschaft im Korpus.

### 3.4 Was definitiv FEHLT (echte Lücken mit Fetch-Potential)

1. **Fungal-Bacterial Co-Kulturen in MFCs** — Literatur existiert (z.B. Geobacter+Pilz-Kathoden), aber keine unserer Queries traf
2. **NFC-gespeiste Biosensorik / RF-Harvesting-Kopplung** — RFID-Sensor-Papers gibt es, Queries zu eng
3. *Phanerochaete* / *Pestalotiopsis* / *Yarrowia lipolytica* als MFC-Organismen (Yarrowia ist real als Zellfabrik; ECT-Arbeit existiert vereinzelt)
4. **Logan-Linie** (klassische MFC-Reviews) für survey-Basis
5. **Fungal MFC Compost/Soil-Anwendungen** (heavy-metals-Paper 2026 ist einziger Treffer)
6. **Langzeit-Experimente >30 Tage** für Lebensdauer-Kapitel

---

## 4. Durchgeführte Korrekturen

| Aktion | Detail |
|--------|--------|
| ❌ 23 Einträge entfernt | 15× DOI 404, 7× Mismatch, 1× kein DOI — inkl. aller 5 Seed-Papiere der E-Mail-Recherche |
| ✅ 29+11−5 verifizierte Papers nachgezogen | CrossRef-Suche mit Venue-Pflicht + Typ-Filter; Noise entfernt (CABI-Lexikon, Agribusiness, Livestock-Feed, Vanity-Preprints) |
| 📝 README-Spezies-Tabelle korrigiert | µW/cm²-Werte als unbelegt markiert; Footnote auf diese Analyse; *S. cerevisiae* als verifizierter High-Performance-Kandidat |
| 📝 `docs/technical/biology/README.md` | Evidence-Audit-Banner; 5 Halluzinations-DOIs ersetzt (Trametes-DET, A. niger, Biowelding, S. cerevisiae); Neurospora-Retraktion |
| 🔄 Pipeline regeneriert | validate ✅ (96) · README ✅ · stats ✅ · reports ✅ |

**⚠️ Offener Punkt:** Die E-Mail an Prof. Zorn enthielt ggf. die halluzinierten Zahlen (Neurospora 260 µW/cm², Spezies-Ranking). **Empfehlung: kurze Korrektur-Mail** mit dem verifizierten Stand — schadet der Glaubwürdigkeit weniger, als wenn ein Elektrochemiker die DOIs prüft.

---

## 5. Empfohlene nächste Schritte

1. **Korrektur-Mail an Zorn** (Quellen-Check transparent machen; wirkt wissenschaftlich seriöser, nicht schwächer)
2. **Gap-Queries nachziehen** (Co-Kultur, NFC-Sensor, Phanerochaete, Logan-Reviews) — Queries oben in §3.4 direkt in `config/other_sources_queries.yaml` übernehmbar
3. **Phase E1 messen statt zitieren:** *Trametes* + Carbon-Cloth + BQ25570 — wir brauchen EIGENE µW/cm²-Zahlen; alle Literatur-Werte sind Design-Hypothesen
4. **DOI-Audit als CI-Step** (`scripts/doi_audit.py`, 1×/Woche, 35 Requests/min) — Halluzinations-Schutz für alle künftigen Fetches
5. **Abstracts nachziehen** — aktuell titel-basierte Klassifikation; Abstracts verbessern Themen-Tiefe der Reports
