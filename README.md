# Fungal Bio-Battery / Mushroom Battery — Research & Startup Dossier

> Stand: Juni 2026 | Forschungsgrundlage: Empa (CH) + internationale Literatur

---

## 1. Kernkonzept

Eine **mikrobielle Brennstoffzelle (MFC)** auf Basis lebender Pilze — keine klassische Batterie, sondern ein biologisches Kraftwerk im Mikromaßstab. Zwei Pilzarten arbeiten zusammen:

| Pol | Pilz | Funktion |
|-----|------|----------|
| **Anode (−)** | *Saccharomyces cerevisiae* (Hefe) | Stoffwechsel setzt Elektronen frei |
| **Kathode (+)** | *Trametes pubescens* (Weißfäulepilz) | Produziert **Laccase**-Enzym → fängt Elektronen ab |

Die Pilze werden in eine **cellulosebasierte 3D-Druck-Tinte** eingemischt, die elektrisch leitfähig (Carbon Black + Graphitflocken), biobaubar und für die Pilze nährstoffreich ist.

**Vorteile:** Trocken lagerbar → vor Ort mit Wasser + Zucker aktivierbar. Nach Gebrauch baut sich die Zelle durch Pilzverdauung selbst ab. Null toxische Rückstände.

---

## 2. Messbare Leistungsparameter

### 2.1 Empa-Baseline (Reyes et al., 2024)

| Parameter | Wert | Bedingungen |
|-----------|------|-------------|
| Max. Leistungsdichte | **12,5 µW/cm²** | bei 22 kΩ Last |
| Max. Stromdichte | **49,2 µA/cm²** | bei 22 kΩ Last |
| Spannung (OCV) | **300–600 mV** | über mehrere Tage |
| Strom (10–100 kΩ Last) | **3–20 µA** | |
| 4 Zellen parallel | **65 h** Sensorbetrieb | |

### 2.2 Vergleich aller bekannten Pilz-MFC-Studien

| Pilz | OCV | Leistung | Bemerkung | Quelle |
|------|-----|----------|-----------|--------|
| *Phanerochaete chrysosporium* | **1,2 V** | **1,9 W/m²** | Höchster Wert; 44 Tage @ 1 mA; 1056 mAh Kapazität | Energies 2021 |
| *Pleurotus pulmonarius* | **940 mV** | 13,2 mW/m² | Laccase 155 U/mL auf Sägespänen | PJOES 2023 |
| *Ganoderma gibbosum* | **810 mV** | 14,2 mW/m² | Laccase-produzierend | Microb. Cell Fact. 2023 |
| *Candida tropicalis* (Konsortium) | **534 mV** | 77,8 mW/m² | POME-Abbau 94,7 % | Asian JAB 2025 |
| *M. pseudolusitanicus* | — | 47,3 mW/m² | Filter-Mud aus Jaggery-Industrie | ECJ 2026 |
| *Paecilomyces* | **575 mV** | 0,062 mW/cm² | Plastikabbau 85,5 % COD | Sustainability 2024 |
| *Aspergillus niger* | **814 mV** | 0,097 mW/m² | Tannery-Abwasser | Appl. Sci. 2023 |
| *Trametes versicolor* | — | 1.200 mW/m³ | | Frontiers 2024 Review |
| *Ganoderma lucidum* | — | 207 mW/m² | | Frontiers 2024 Review |
| *Kluyveromyces marxianus* | — | 850.000 mW/m³ | | Frontiers 2024 Review |
| *Hansenula anomala* | — | 2.900 mW/m³ | | Frontiers 2024 Review |
| Mycelium-Skin-Batterie (JKU Linz) | **~1,9 V** (2 Zellen) | **3,8 mAh/cm²** Kapazität | Zink-Carbon mit Myzel-Separator; Bluetooth-Modul (13,5 mA) | MycelioTronics |

### 2.3 Zustand der Technik — drei Architekturklassen

| Klasse | Prinzip | Reifegrad | Referenz |
|--------|---------|-----------|----------|
| **3D-gedruckte Pilz-MFC** | Lebende Pilze in Cellulose-Tinte, komplett biologisch abbaubar | TRL 3–4 (Lab) | Reyes et al. 2024 (Empa) |
| **Myzel-Haut-Batterie** | Myzel als Separator/Gehäuse für Zink-Carbon-Zellen | TRL 4 (Demo: BLE-Sensor) | MycelioTronics (JKU Linz) |
| **Konventionelle Fungal MFC** | Pilze als Biokatalysator in Reaktoren (Wasser/Abwasser) | TRL 5–6 (Pilot) | diverse |

---

## 3. Technologie — die drei Dimensionen

### 3.1 Technologie-Dimension

**Material-Stack (Empa-Design):**
- Drucktinte: Cellulose-Nanokristalle (CNC) + Cellulose-Nanofibrillen (CNF) + Carbon Black + Graphitflocken
- Separator: maßgeschneiderte Cellulose-Protonenaustauschmembran
- Gehäuse: Bienenwachs (vollständig biologisch abbaubar)
- Anode: Hefe (*S. cerevisiae*), 7-Lagen-Druck, 1×10⁸ Zellen
- Kathode: Weißfäule (*T. pubescens*), 4 mL Laccase-Supernatant + 20 mM ABTS

**Optimierungshebel (Rangfolge nach Impact):**

| Hebel | Potenzial | Status |
|-------|-----------|--------|
| Bessere Pilzstämme (*P. chrysosporium* statt *T. pubescens*) | **~150× mehr Leistung** (1,9 W/m² vs. 12,5 µW/cm²) | Nur Einzelpilz, noch nicht in 3D-Druck demonstriert |
| Bakterien-Pilz-Konsortien | Mehrfache Steigerung belegt (*S. oneidensis–S. cerevisiae*) | Forschung |
| Anoden-Modifikation (Fe₃O₄/PANI-Nanokomposit) | **6× Steigerung** auf 424,5 mW/m² | PGE-Elektrode, Nature 2025 |
| Graphen-beschichtete Anoden | Hohe Steigerung, aber kostspielig (>$12.000/ha) | Lab |
| Single-Chamber statt Dual-Chamber | Niedrigerer Innenwiderstand | Bekannt, Standard |
| Laccase-Enzym-Engineering (ARTP-Mutagenese, Codon-Optimierung) | Höhere katalytische Effizienz | *Aspergillus* demonstriert |

**Critical Gap:** Die höchste Leistung (1,9 W/m²) wurde mit konventioneller Reaktorarchitektur erreicht, NICHT mit 3D-Druck. Die Kombination von Hochleistungsstämmen + 3D-Druck + Biologischer Abbaubarkeit ist **noch ungelöst** — das ist die Kerninnovation.

### 3.2 Nachhaltigkeits-Dimension

**LCA-Ergebnisse (MFC vs. Li-Ion):**

| Aspekt | Pilz-MFC | Li-Ion |
|--------|----------|--------|
| CO₂ bei Herstellung | Minimal (Cellulose, Bienenwachs, Wasser) | 100–200 kg CO₂/kWh (Herstellung dominiert) |
| Toxizität | Keine toxischen Materialien | Li, Co, Ni, Mn, elektrolytische Lösungsmittel |
| Rohstoffe | Cellulose (überall), Zucker, Pilze | Li (Bolivien/Chile), Co (Kongo), Graphit (China) |
| End-of-Life | **Kompostierbar** — Pilz verdaut sich selbst | Recycling komplex, <5 % werden wirklich recycelt |
| GWP-Dominanz | Reaktormaterial (Graphit/PET) → durch Cellulose lösbar | Kathodenproduktion (Pt/Ti oder NMC) |
| Wasserbelastung | Null Abwasser, null Lithium-Auswaschung | 4,69×10⁻⁴ kg Li ins Wasser beim Recycling |
| Betriebsdauer-Beitrag | **Vernachlässigbar** (LCA-bewertet) | signifikant |

**Schlüssel-Erkenntnis aus LCAs:** Der dominierende Umweltaspekt bei MFCs ist das **Reaktormaterial**, nicht der Betrieb. Das Empa-Design (Cellulose + Bienenwachs) eliminiert genau diesen Hotspot.

**Vergleich der Nachhaltigkeits-Claims:**
- Li-Ion: GWP dominiert von Kathode + Produktion
- Graphit-MFC: gut, aber Graphit nicht biologisch abbaubar
- **Cellulose-Pilz-MFC (Empa):** vollständiger Kreislauf — bestmögliche Nachhaltigkeitsstory

### 3.3 Wirtschaftslichkeits-Dimension

**Marktvolumen (Bio-Batterien / Bio-based Batteries):**

| Quelle | Jahr | Marktvolumen | CAGR |
|--------|------|--------------|------|
| Roots Analysis | 2024 | **$96,1 Mrd.** | 8,21 % (→ $230 Mrd. 2035) |
| Grand View Research | 2025 | Wachstend, frühe Phase | — |
| IndexBox | 2026 | US-Markt $100–150 Mio. | Sustainability-Premium 30–50 % |

**Wettbewerber:**

| Unternehmen | Technologie | Status |
|-------------|-------------|--------|
| **BeFC** (FR) | Enzym-Papier-Batterie | Seed/Series A |
| **Bioo** (ES) | biologische Batterie (pflanzenbasiert) | Seed |
| **Bactery AB** (SE) | bakterielle MFC | Früh |
| Stora Enso (FI) | Bio-Materialien für Batterien | Scale-up |
| Northvolt (SE) | grüne Li-Ion (nicht bio) | Scale-up |
| MycelioTronics (AT) | Myzel-Skin-Elektronik | Universität JKU Linz |

**Kostenstruktur (aktuell geschätzt):**

| Kostenblock | Anteil | Hinweis |
|-------------|--------|---------|
| Feedstock / Spezialchemikalien | Hoch (niedriges Volumen) | Hochreine Bio-Precursoren, Enzyme |
| Materialsynthese & Reinigung | Hoch | Energieintensiv, ausbeutesensitiv |
| Fertigung (Niedrigvolumen) | Hoch | Maßgefertigte Linien, 3D-Druck |
| Systemintegration & Qualifizierung | Mittel | BMS, Packaging, applikationsspezifisches Testing |

**Preispositionierung:** Sustainability-Premium von **30–50 %** über konventionellen Zellen für Early Adopters → sinkt auf 15–25 % bis 2030.

**Revenue-Modell-Optionen:**

| Modell | Beschreibung | Risiko |
|--------|-------------|--------|
| **Sensor-as-a-Service** | Verkauf kompletter Biodegradierbarer Sensor-Knoten (inkl. Batterie) für Landwirtschaft/Forst | Mittel — Hardware + Software |
| **Battery-Component-Licensing** | Technologie-Lizenz an Sensor-Hersteller (OEM) | Hoch — IP muss stark sein |
| **Waste-to-Energy** | Pilz-MFC für Abwasser/Klärschlamm → Strom + Wasserreinigung | Geringer Tech-Risk, aber niedrige Margen |
| **Disposable Diagnostics** | Einweg-Biosensoren (Medizin/Lebensmittel) mit eingebauter Pilz-Stromquelle | Hoch ( regulatorisch) |

---

## 4. Paper & Quellen

### 4.1 Kernpaper (Empa — der Tagesschau-Artikel)

- **Reyes, C. et al.** (2024): *3D Printed Cellulose-Based Fungal Battery*. ACS Sustainable Chemistry & Engineering.
  - DOI: [10.1021/acssuschemeng.4c05494](https://doi.org/10.1021/acssuschemeng.4c05494)
  - Erstmalige Kombination zweier Pilzarten in einer 3D-gedruckten MFC

### 4.2 Übersichts- & Review-Paper

- **Umar, A. et al.** (2024): *Harnessing fungal bio-electricity: a promising path to a cleaner environment*. Frontiers in Microbiology.
  - URL: [frontiersin.org/articles/10.3389/fmicb.2023.1291904](https://www.frontiersin.org/journals/microbiology/articles/10.3389/fmicb.2023.1291904/full)
  - Vollständige Übersicht aller Pilz-Leistungswerte (Trametes, Ganoderma, Aspergillus etc.)

- **Sekrecka-Belniak & Toczyłowska-Mamińska** (2018): *Fungi-Based Microbial Fuel Cells*. Energies 11(10), 2827.
  - DOI: [10.3390/en11102827](https://doi.org/10.3390/en11102827)
  - Die Standard-Referenz für Fungal-MFC-Reviews; höchste dokumentierte Leistung: 1,5 W/m²

- **Frontiers in Fungal Biology** (2026): *Bioelectricity harvesting from microorganism: review of recent advancements in utilizing the bioelectrical properties of fungi for powering small-scale robotic systems*.
  - URL: [frontiersin.org/articles/10.3389/ffunb.2025.1739847](https://www.frontiersin.org/journals/fungal-biology/articles/10.3389/ffunb.2025.1739847/full)

- **Frontiers in Microbiology** (2026): *Fungal fuel cells: an environmentally friendly approach to addressing heavy metal pollution and electricity production*.
  - URL: [frontiersin.org/articles/10.3389/fmicb.2026.1825368](https://www.frontiersin.org/journals/microbiology/articles/10.3389/fmicb.2026.1825368/full)

### 4.3 Höchstleistungs-Studien

- **Sustainability** (2021): *Self-Sustaining Bioelectrochemical Cell from Fungal Degradation of Lignin-Rich Agrowaste*. MDPI Energies 14(8), 2098.
  - DOI: [10.3390/en14082098](https://doi.org/10.3390/en14082098)
  - *P. chrysosporium*, **1,9 W/m²**, 44 Tage Entladung, 1056 mAh

- **Nature Scientific Reports** (2025): *Improving the power production efficiency of microbial fuel cell by using biosynthesized polyanaline coated Fe₃O₄*.
  - DOI: [10.1038/s41598-024-84311-5](https://doi.org/10.1038/s41598-024-84311-5)
  - Fe₃O₄/PANI-Anodenmodifikation → **6× höhere Leistung** (424,5 mW/m²)

### 4.4 MycelioTronics (Myzel als Batteriematerial)

- **JKU Linz** — *MycelioTronics: Fungal mycelium skin for flexible and biodegradable batteries*.
  - PDF: [epub.jku.at/obvulioa/download/pdf/9001930](https://epub.jku.at/obvulioa/download/pdf/9001930)
  - Myzel als Separator + Gehäuse; 3,8 mAh/cm²; Bluetooth-Betrieb

### 4.5 LCA & Umweltbewertung

- **RSC Environ. Sci.: Water Res. Technol.** (2024): *Evaluation of environmental performance and selection of the most suitable system for MFCs with different electron acceptors by life cycle assessment and PROMETHEE approach*.
  - DOI: [10.1039/d3ew00809f](https://doi.org/10.1039/d3ew00809f)

- **Int. J. Life Cycle Assess.** (2025): *Life cycle assessment of microalgae-assisted microbial fuel cells*.
  - DOI: [10.1007/s11367-025-02518-8](https://doi.org/10.1007/s11367-025-02518-8)

- **Batteries (MDPI)** (2024): *Life cycle assessment and life cycle costing of large-scale battery systems*.
  - URL: [discovery.ucl.ac.uk/id/eprint/10211311/1/batteries-10-00295.pdf](https://discovery.ucl.ac.uk/id/eprint/10211311/1/batteries-10-00295.pdf)

### 4.6 Anwendungen & Biohybride Systeme

- **MIND Device** (arXiv 2026): *Mycoponically Integrated Network Device for Multimodal Biosensing using Electrophysiological Mycelial Networks*.
  - URL: [arxiv.org/html/2604.22947](https://arxiv.org/html/2604.22947)
  - Pleurotus ostreatus Myzel-Sensornetzwerk über 11 Monate stabil

- **PLOS One** (2025): *Sustainable memristors from shiitake mycelium for high-frequency bioelectronics*.
  - DOI: [10.1371/journal.pone.0328965](https://doi.org/10.1371/journal.pone.0328965)
  - Shiitake-Memristor, 5,85 kHz, 90 % Genauigkeit; strahlungsresistent

- **MyceliClean** (CSO Ireland 2026): *Harnessing Fungal Bioelectricity for Off-Grid Water Sterilisation*.
  - PDF: [cso.ie/.../18_Myceliclean.pdf](https://www.cso.ie/en/media/csoie/competitionsandawards/johnhooper/2026/18_Myceliclean_Harnessing_Fungal_Bioelectricity_for_Off-Grid_Water_Sterilisation.pdf)

### 4.7 Marktberichte

- **Roots Analysis**: *Biobatteries Market Report, 2035*.
  - URL: [rootsanalysis.com/biobatteries-market](https://www.rootsanalysis.com/biobatteries-market)

- **Grand View Research**: *Bio-based Battery Market Size, Share | Industry Report, 2033*.
  - URL: [grandviewresearch.com/industry-analysis/bio-based-battery-market-report](https://www.grandviewresearch.com/industry-analysis/bio-based-battery-market-report)

- **IndexBox**: *Bio Based Battery Market in the World / United States*.
  - URL: [indexbox.io/store/world-bio-based-battery-market-analysis](https://www.indexbox.io/store/world-bio-based-battery-market-analysis-forecast-size-trends-and-insights/)

### 4.8 Weitere Studien

- **Microb. Cell Fact.** (2023): *Electricity generation and oxidoreductase potential during dye discoloration by laccase-producing Ganoderma gibbosum*.
  - DOI: [10.1186/s12934-023-02258-0](https://doi.org/10.1186/s12934-023-02258-0)

- **PJOES** (2023): *Improved Performance of a Novel-Model Laccase-based Microbial Fuel Cell*.
  - URL: [pjoes.com/pdf-147196-78069](https://www.pjoes.com/pdf-147196-78069)

- **MDPI Sustainability** (2024): *Electricity Generation and Plastic Waste Reduction Using the Fungus Paecilomyces*.
  - DOI: [10.3390/su162411137](https://doi.org/10.3390/su162411137)

- **Appl. Sci.** (2023): *Performance of the Dual-Chamber Fungal Fuel Cell in Treating Tannery Wastewater*. MDPI 13(19), 10710.
  - DOI: [10.3390/app131910710](https://doi.org/10.3390/app131910710)

- **Agriculture** (2025): *Xeno-Fungusphere: Fungal-Enhanced MFCs for Agricultural Remediation*. MDPI 15(6), 1392.
  - DOI: [10.3390/agriculture15061392](https://doi.org/10.3390/agriculture15061392)

- **Yeast bio-batteries** — Crespilho, F.N. (2024): RSC Environ. Sci.: Energy.
  - URL: [pubs.rsc.org/en/content/articlepdf/2024/se/d4se00903g](https://pubs.rsc.org/en/content/articlepdf/2024/se/d4se00903g)

---

## 5. Presse & Weiteres

- **Tagesschau** (Artikel, der dich inspiriert hat):
  [tagesschau.de/wissen/forschung/batterie-pilze-100](https://www.tagesschau.de/wissen/forschung/batterie-pilze-100.html)

- **Empa Pressemitteilung**:
  [empa.ch/web/s604/fungal-biobattery](https://www.empa.ch/web/s604/fungal-biobattery)

- **Euronews** (Jan 2025): *Swiss scientists have taught fungi to generate electricity*.
  [euronews.com/2025/01/11/...](https://www.euronews.com/2025/01/11/swiss-scientists-have-taught-fungi-to-generate-electricity-how-do-mushroom-batteries-work)

- **New Atlas** (Jan 2025): *3D-printed battery made from fungi feeds on sugars to power sensors*.
  [newatlas.com/energy/3d-printed-battery-fungi-sugars-empa/](https://newatlas.com/energy/3d-printed-battery-fungi-sugars-empa/)

- **R&D World** (Jan 2025): *Microbial, fungi-powered battery generates electricity, biodegrades*.
  [rdworldonline.com/...](https://www.rdworldonline.com/the-battery-that-eats-itself-fungal-power-with-a-built-in-cleanup-crew/)

- **Anadolu (AA)** (Jan 2025): *3D-printed fungi batteries: A path to a biodegradable tech future?*
  [aa.com.tr/en/...](https://www.aa.com.tr/en/science-technology/3d-printed-fungi-batteries-a-path-to-a-biodegradable-tech-future/3463854)

---

## 6. Empa-Kontaktpersonen

- **Dr. Carolina Reyes** — Erstautorin, Forscherin (Cellulose & Wood Materials)
- **Dr. Gustav Nyström** — Leiter Cellulose & Wood Materials Lab
- **Empa** — Swiss Federal Laboratories for Materials Science and Technology, Dübendorf
- Förderung: Gebert Rüf Stiftung (Microbials Program)

---

## 7. Nächste Schritte für ein Startup

1. **Technologie-Scouting:** *P. chrysosporium* (1,9 W/m²) im 3D-Druck-Design von Reyes reproduzieren → ist die 150×-Steigerung realisierbar?
2. **IP-Check:** Empa-Patente prüfen; ggf. Lizenz oder eigene Architektur entwickeln
3. **Pilot-Anwendung:** Landwirtschaftliche Boden-Sensoren (Feuchte + Temperatur) — niedrigste regulatorische Hürde
4. **Förderung:** BMBF, DBU,EXIST-Forschungstransfer; Horizon Europe (Bio-based Industries)
5. **Partner:** Empa (CH), JKU Linz (AT MycelioTronics), lokale Landwirtschaftsverbände

---

## 8. Wettbewerbsübersicht (Detailliert)

| Unternehmen | Land | Technologie | Leistung | Status |
|-------------|------|-------------|----------|--------|
| Empa (Reyes) | CH | 3D-Druck Pilz-MFC | 12,5 µW/cm² | Forschung |
| MycelioTronics | AT | Myzel-Haut Batterie | 3,8 mAh/cm² | Forschung |
| BeFC | FR | Enzym-Papier-Batterie | Enzymatisch | Series A |
| Bioo | ES | Pflanzen-Batterie | Bio-elektrochemisch | Seed |
| Bactery AB | SE | Bakterien-MFC | Bakteriell | Früh |

**Gap:** Kein kommerzieller Akteur kombiniert **3D-Druck + Biologische Abbaubarkeit + Hochleistungspilze**. Das ist das Startup-Fenster.

---

## 9. AI-Leverage — Wo Künstliche Intelligenz den Hebel ansetzt

KI ist kein Marketing-Buzzword, sondern der zentrale Beschleuniger entlang der gesamten Wertschöpfungskette. Vier Hebel, mit Proof-of-Concept aus der Literatur:

### 9.1 R&D: Stamm-Selektion & Enzym-Engineering

**Problem:** Von Millionen Pilzstämmen nur wenige sind elektrogen. Klassische Trial-and-Error-Suche dauert Jahre.

**KI-Lösung:**

| Ansatz | Beweis | Übertragbarkeit auf MykoVolt |
|--------|--------|------------------------------|
| **ML-basierte Laccase-pH-Optimum-Vorhersage** | Aus kleinem Datensatz (basidiomycete Laccasen) wurde pH-Optimum mit Regressionsmodellen vorhergesagt und in vitro an *Lepista nuda* validiert (Biotechnol. Biofuels 2024) | Direkt auf *Trametes pubescens* & *P. chrysosporium* anwendbar — selektiert alkaline Laccasen mit höherer Aktivität bei Bodensensor-Bedingungen |
| **Computational Enzyme Design (PROSS + FuncLib)** | Rational "stabilize-and-diversify"-Strategie für High-Redox-Potential-Laccasen; Bestehende *Trametes*-Enzyme wurden stabilisiert und in der Aktivität optimiert (ACS Catalysis 2022) | Engineering maßgeschneiderter Laccasen für höhere Elektronentransfer-Raten an der Kathode |
| **Strain Engineering ML (MaLPHAS)** | Vorhersage von Gen-Edits, die Proteinsekretion verdoppeln; getestet an *Komagataella phaffii* (Eden Bio, 2023) | Optimierung der Laccase-Produktion im Produktionsstamm → senkt Enzymkosten massiv |
| **Genom-Mining mit Deep Learning** | Metagenom-Daten nach Elektrogenitäts-Mustern durchsuchen (Redox-Aktivität, Membran-Cytochrome) | Identifikation neuer Hochleistungspilze jenseits der bekannten 6–7 Arten |

**Hebel:** Statt 5 Jahre Stamm-Screening → 6–12 Monate mit ML-geführter Auswahl. Geschätzte Beschleunigung: **5–10×**.

### 9.2 Formulation Discovery: Drucktinte & Elektrolyt

**Problem:** Die 3D-Druck-Tinte muss gleichzeitig druckbar, leitfähig, biokompatibel und biologisch abbaubar sein. Das ist ein hochdimensionaler Suchraum (Cellulose-Typ, Carbon-Black-Anteil, Graphitflocken, Feuchtigkeit, Pilzdichte, Nährstoffe…).

**KI-Lösung — Self-Driving Lab mit Bayesian Optimization:**

Bewiesene Ansätze (übertragbar):

- **Active Learning + Robotik für Elektrolyt-Formulierungen** (Nature Comm. 2024): Aus >2000 Lösemitteln wurden mit <10 % Tests die optimalen gefunden → 6,20 M Löslichkeit. Direkt übertragbar auf Tintenoptimierung.
- **ChatBattery (LLM-gesteuert)** (arXiv 2025): LLM generiert Hypothesen → Synthese → Charakterisierung in Monaten statt Jahren. Erste LLM-getriebene Batteriematerial-Entdeckung weltweit.
- **Random Forest / Deep Learning für Bioink-Printability** (PMC 2023): 88 % Genauigkeit bei Vorhersage der Druckbarkeit aus Formulierung; Druckbarkeits-Fenster-Karten generiert.
- **CNN für Print-Quality-Control** (PMC 2022): Deep-Learning-Klassifikator (good/under/over-extrusion) mit Closed-Loop-Parameter-Anpassung in nur 4 Iterationen.
- **Bayesian Optimization für Gel-Druck** (MDPI Gels 2025): Predictive Prozessoptimierung mit Computer-Vision-Feedback.

**Architektur für MykoVolt:**

```
[Formulierungs-Vorschlag] → [3D-Druck Test] → [Leistungsmessung]
         ↑                                              ↓
    [Bayesian Opt.] ← ← ← ← ← [Ergebnis-Datensatz] ← ← ←
```

Geschlossener Loop aus ML-Vorschlag → automatisierter Druck → elektrochemischer Messung → Model-Update. Reduziert die Anzahl teurer Experimente um **80–90 %**.

### 9.3 Produktion: KI-gesteuerte 3D-Druck-Qualitätssicherung

**Problem:** Bei Skalierung schwankt die Leistung von Charge zu Charge — biologische Systeme sind nicht deterministisch.

**KI-Lösung:** Echtzeit-Computer-Vision überwacht jeden Druck (CNN-basierte Defekterkennung) und passt Parameter automatisch an (Schichtdicke, Fließrate, Extrusionsmultiplikator). Bewiesene Genauigkeit: R²=0,986 für HD-Metrik (IOP 2025).

**Wirtschaftlicher Effekt:** Ausschussquote von geschätzt 20 % auf <3 % → Stückkosten um ~15 % gesenkt.

### 9.4 Produkt: Sensor-Daten-Analytics

**Problem:** Tausende Bio-Sensoren im Feld erzeugen Datenströme — aber wer werten sie aus?

**KI-Lösung:**

- Edge-ML auf dem Sensor (TinyML): Anomalie-Erkennung direkt am Knoten (z. B. Trockenstress, Krankheitsbefall) → spart Übertragungsenergie, die wichtig bei μW-Budgets
- Cloud-Analytics: Aggregation über Verbünde → Vorhersagemodelle für Ertrag, Krankheitsausbruch, Boden-gesundheit. **Das eigentliche Revenue-Add-on** — die Batterie ist der Entry, die Datenanalyse das wiederkehrende Geschäft.

### 9.5 Business-Operations: Standard-KI-Tooling

| Bereich | KI-Einsatz |
|---------|-----------|
| Patent-Recherche | LLM-basiertes Mining existierender Empa-IP undFreedom-to-operate-Analyse |
| Marktforschung | Automatisierte Analyse von Ausschreibungen, Sensor-Tenders, regulatorischen Texten |
| Kundengewinnung | Predictive Lead-Scoring für Agrarbetriebe mit hohem Bio-Sensor-Bedarf |
| Fördermittel | LLM-gestützte Antragschreibung für BMBF/EXIST/Horizon Europe |

### 9.6 Zusammenfassung: Wo KI den meisten Hebel hat

```
Wirkungsgrad-Rangfolge (ROI pro KI-Investition):

1. STAMM-SELEKTION (ML für Elektrogenität)          ★★★★★  → 5-10× schneller R&D
2. FORMULATIONS-OPTIMIERUNG (Bayesian Opt + Lab)    ★★★★★  → 80% weniger Experimente
3. PRODUKTIONS-QS (Computer Vision)                 ★★★★☆  → 15% Stückkostensenkung
4. SENSOR-DATEN-ANALYTICS (Cloud + TinyML)          ★★★★☆  → Wiederkehrendes Revenue
5. ENZYME-ENGINEERING (PROSS/FuncLib)               ★★★☆☆  → Höhere Kathodenleistung
6. BUSINESS-OPS (Standard-Tooling)                  ★★☆☆☆  → Effizienz, kein USP
```

**Strategische Empfehlung:** Die ersten drei Hebel sind **verteidigungsfähig** (Competitive Moat) — ein Wettbewerber ohne KI-Pipeline braucht Jahre länger für dieselben Optimierungen. Die KI-Fähigkeit im R&D-Lab ist der eigentliche IP-Vorteil, nicht die Batterie selbst.

### 9.7 Referenzen (KI-spezifisch)

- **ML für Laccase-pH-Optimum:** Biotechnol. Biofuels Bioprod. (2024). DOI: [10.1186/s13068-024-02566-6](https://doi.org/10.1186/s13068-024-02566-6)
- **PROSS + FuncLib Laccase-Design:** ACS Catal. (2022). PMID: [36366766](https://pubmed.ncbi.nlm.nih.gov/36366766/)
- **MaLPHAS Strain Engineering:** PMC (2023). URL: [pmc.ncbi.nlm.nih.gov/articles/PMC9995161](https://pmc.ncbi.nlm.nih.gov/articles/PMC9995161/)
- **Active Learning Elektrolyte:** Nature Comm. (2024). OSTI: [2471574](https://www.osti.gov/biblio/2471574)
- **ChatBattery (LLM):** arXiv (2025). URL: [arxiv.org/pdf/2507.16110](https://arxiv.org/pdf/2507.16110)
- **Foundation Models Batteries:** OpenReview (2025). URL: [openreview.net/pdf?id=6pjxodugzO](https://openreview.net/pdf?id=6pjxodugzO)
- **Bayesian Opt. Polymer-Elektrolyte:** ChemRxiv (2025). DOI: [10.26434/chemrxiv-2025-2cjbg](https://doi.org/10.26434/chemrxiv-2025-2cjbg)
- **ML Bioink Printability:** PMC (2023). URL: [pmc.ncbi.nlm.nih.gov/articles/PMC10353544](https://pmc.ncbi.nlm.nih.gov/articles/PMC10353544/)
- **DL Quality Control 3D-Druck:** PMC (2022). URL: [pmc.ncbi.nlm.nih.gov/articles/PMC9668573](https://pmc.ncbi.nlm.nih.gov/articles/PMC9668573/)
- **Hausdorff-Metrik Printability:** IOP Biofabr. (2025). DOI: [10.1088/1758-5090/ae288c](https://doi.org/10.1088/1758-5090/ae288c)
- **ML Battery Science Review:** npj Comput. Mater. (2025). DOI: [10.1038/s41524-025-01575-9](https://doi.org/10.1038/s41524-025-01575-9)
