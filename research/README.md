<h1 align="center">
  <strong>MykoVolt MFC Research Corpus</strong>
</h1>
<h3 align="center">Microbial Fuel Cells — Fungal Bioelectrochemistry (literature review)</h3>

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

> 📚 **Data-driven literature corpus** for MykoVolt's fungal microbial fuel cell research.
> Curated via the same agentic pipeline as the `*-research` corpus repos: discover → validate → stats → reports.

## 📖 How it works

```
config/taxonomy.yaml ──► papers.yaml ──► validate_papers.py
                          │   ▲              │
                          ▼   └── fetch_* ───┘
                   generate_readme.py ──► README.md (auto)
                          │
                          ▼
                  standard_stats.py ──► statistics.json, papers.json
```

- **`papers.yaml`** is the source of truth (90 papers) — never edit README.md directly.
- The **taxonomy lives in one place** (`config/taxonomy.yaml`).
- New papers are discovered via `scripts/fetch/*` from **arXiv, CrossRef, EuropePMC, OpenAlex**.

## 🚀 Local pipeline

```bash
cd research

# Full pipeline (validate → README → stats)
python3 scripts/validate_papers.py && \
python3 scripts/generate_readme.py && \
python3 scripts/standard_stats.py

# Discover new papers
python3 scripts/fetch/fetch_other_sources.py      # CrossRef/EuropePMC/DBLP
python3 scripts/fetch/fetch_openalex_bulk.py      # OpenAlex bulk per category
python3 scripts/fetch/fetch_new_papers.py --local # arXiv (last N months)
```

## 🧭 Corpus overview

- **Total papers:** 75
- **Categories:** mechanism (32) · application (21) · material (20) · survey (2)
- **Subcategories:** laccase (24) · hybrid (22) · degradation (18) · eet (11)
- **Stats:** `statistics.json` (momentum, gaps, keyword bursts, venues, authors)

## 📚 Paper list

- [📚 Bioelectrochemical Mechanisms](#bioelectrochemical-mechanisms)
  - [Laccase-Mediated](#laccase-mediated)
  - [Extracellular Electron Transfer](#extracellular-electron-transfer)
  - [Hybrid / Co-Culture](#hybrid-/-co-culture)
  - [Degradation & Lifespan](#degradation-&-lifespan)
- [📚 Electrode & Material Systems](#electrode-&-material-systems)
  - [Laccase-Mediated](#laccase-mediated)
  - [Extracellular Electron Transfer](#extracellular-electron-transfer)
  - [Hybrid / Co-Culture](#hybrid-/-co-culture)
  - [Degradation & Lifespan](#degradation-&-lifespan)
- [📚 Applications & Devices](#applications-&-devices)
  - [Laccase-Mediated](#laccase-mediated)
  - [Extracellular Electron Transfer](#extracellular-electron-transfer)
  - [Hybrid / Co-Culture](#hybrid-/-co-culture)
  - [Degradation & Lifespan](#degradation-&-lifespan)
- [📚 Surveys & Reviews](#surveys-&-reviews)
  - [Hybrid / Co-Culture](#hybrid-/-co-culture)

### Bioelectrochemical Mechanisms

#### Laccase-Mediated

##### 2025

- [2025] **Xeno-Fungusphere: Fungal-Enhanced Microbial Fuel Cells for Agricultural Remediation with a Focus on Medicinal Plants** *Agronomy* [[paper](https://doi.org/10.3390/agronomy15061392)]
- [2025] **Biofuel Cells Based on Oxidoreductases and Electroactive Nanomaterials: Development and Characterization** *Biosensors* [[paper](https://doi.org/10.3390/bios15040249)]

##### 2024

- [2024] **ENHANCING ELECTRICITY GENERATION USING FUNGAL LACCASE-BASED MICROBIAL FUEL CELL** *Journal of microbiology, biotechnology and food sciences* [[paper](https://doi.org/10.55251/jmbfs.9703)]
- [2024] **Enhancing extracellular electron transfer and power generation in microbial fuel cell using a ferrocene-based conjugated oligoelectrolyte** *Fuel* [[paper](https://doi.org/10.1016/j.fuel.2023.130271)]

##### 2023

- [2023] **Electricity generation and oxidoreductase potential during dye discoloration by laccase-producing Ganoderma gibbosum in fungal fuel cell** *Microbial Cell Factories* [[paper](https://doi.org/10.1186/s12934-023-02258-0)]
- [2023] **Enhanced Extracellular Electron Transfer of Comn2o4@Cnt as Microbial Fuel Cell Anode** *Journal of environmental chemical engineering* [[paper](https://doi.org/10.2139/ssrn.4563137)]
- [2023] **Fe/N Codoped Paper Carbon Fiber Foam Promoted Extracellular Electron Transfer for a High-Performance Microbial Fuel Cell** *ACS Applied Engineering Materials* [[paper](https://doi.org/10.1021/acsaenm.3c00445.s001)]

##### 2021

- [2021] **&lt;i&gt;In Situ&lt;/i&gt; Laccase Biocathode Performance Assessment in Dual-Chamber Microbial Fuel Cells** *SSRN Electronic Journal* [[paper](https://doi.org/10.2139/ssrn.3954809)]

##### 2020

- [2020] **Dye reduction-based electron-transfer activity monitoring assay for assessing microbial electron transfer activity of microbial fuel cell inocula** *Journal of Environmental Sciences* [[paper](https://doi.org/10.1016/j.jes.2020.04.037)]

##### 2018

- [2018] **Effect of Geobacter metallireducens nanowire on electron transfer efficiency in microbial fuel cell** *Renewable and Sustainable Energy Reviews* [[paper](https://doi.org/10.1101/2021.07.14.452433)]
- [2018] **Interfacial Electron Transfer from the Outer Membrane Cytochrome OmcA to Graphene Oxide in a Microbial Fuel Cell: Spectral and Electrochemical Insights** *ACS Energy Letters* [[paper](https://doi.org/10.1021/acsenergylett.8b01299.s001)]
- [2018] **Anodic Electron Transfer Mechanism in Bioelectrochemical Systems** *Microbial Fuel Cell* [[paper](https://doi.org/10.1007/978-3-319-66793-5_5)]

##### 2017

- [2017] **Understanding and improving the microbial fuel cell anodic electron transfer process** *Journal of Power Sources* [[paper](https://doi.org/10.32657/10356/48051)]
- [2017] **Decolourisation of Acid orange 7 in a microbial fuel cell with a laccase-based biocathode: Influence of mitigating pH changes in the cathode chamber** *Enzyme and Microbial Technology* [[paper](https://doi.org/10.1016/j.enzmictec.2016.10.012)]

##### 2014

- [2014] **Abiotic (Nonenzymatic) Implantable Biofuel Cells** *Implantable Bioelectronics* [[paper](https://doi.org/10.1002/9783527673148.ch14)]

##### 2011

- [2011] **Platinum Nanoparticles (PtNPs) - Laccase Assisted Biocathode Reduction of Oxygen for Biofuel Cells** *International Journal of Electrochemical Science* [[paper](https://doi.org/10.1016/s1452-3981(23)19689-1)]

##### 2009

- [2009] **Silica Encapsulated Laccase/CNT Catalysts for Enzymatic Fuel Cell Cathodes** *ECS Meeting Abstracts* [[paper](https://doi.org/10.1149/ma2009-01/43/1452)]

[⬆ Back to top](#paper-list)

#### Extracellular Electron Transfer

##### 2026

- [2026] **Fungal fuel cells: an environmentally friendly approach to addressing heavy metal pollution and electricity production.** *MED* [[paper](https://doi.org/10.3389/fmicb.2026.1825368)]
- [2026] **Microbial Fuel Cells for Biomass Valorization: Bridging Climate Action and Terrestrial Ecosystem Protection.** *MED* [[paper](https://doi.org/10.3390/polym18111354)]
- [2026] **Scanning Electrochemical Microscopy of Nystatin-Treated Yeast Used for Biofuel Cells.** *MED* [[paper](https://doi.org/10.3390/s26020605)]
- [2026] **Microorganisms from Antarctica: A Review of Their Potential in the Bioremediation of Hydrocarbon-Contaminated Soils.** *MED* [[paper](https://doi.org/10.3390/microorganisms14050948)]
- [2026] **Mechanistic advances in microbial nanobiotechnology and their applications in sustainable agriculture, environment and biomedicine.** *MED* [[paper](https://doi.org/10.1186/s11671-026-04509-6)]
- [2026] **Using dual chamber microbial fuel cells for coupled microplastic biodegradation and bioelectricity production: assessing the effect of substrate.** *MED* [[paper](https://doi.org/10.1186/s12934-026-02925-y)]
- [2026] **Multi-Year Biofilm Formation on Granitic Surfaces Reveals Dynamic Microbial Communities in Fennoscandian Shield Deep Groundwaters.** *MED* [[paper](https://doi.org/10.1007/s00248-026-02812-4)]
- [2026] **Synergies of Quorum Sensing and Biofilm Dynamics in the Bioremediation of Emerging Medical Organic Pollutants.** *MED* [[paper](https://doi.org/10.1155/tswj/5568616)]

##### 2025

- [2025] **Bioelectricity harvesting from microorganism: review of recent advancements in utilizing the bioelectric properties of fungi for powering small-scale robotic systems.** *MED* [[paper](https://doi.org/10.3389/ffunb.2025.1739847)]

##### 2024

- [2024] **Electron transfer in enzymatic biofuel cells** *Biofuel Cells* [[paper](https://doi.org/10.1016/b978-0-443-13835-5.00008-5)]

##### 2020

- [2020] **Performance Modelling of the Bioelectrochemical Glycerol Oxidation by a Co‐Culture of <i>Geobacter Sulfurreducens</i> and <i>Raoultella Electrica</i>** *ChemElectroChem* [[paper](https://doi.org/10.1002/celc.202000027)]

##### 2019

- [2019] **Assessment of Electron Transfer Mechanisms during a Long-Term Sediment Microbial Fuel Cell Operation** *Energies* [[paper](https://doi.org/10.3390/en12030481)]

[⬆ Back to top](#paper-list)

#### Hybrid / Co-Culture

##### 2025

- [2025] **Polypyrrole-Modified Saccharomyces cerevisiae Used in Microbial Fuel Cell** *Biosensors* [[paper](https://doi.org/10.3390/bios15080519)]

##### 2023

- [2023] **Sediment microbial fuel cell (SMFCs)** *Biological Fuel Cells* [[paper](https://doi.org/10.1016/b978-0-323-85711-6.00004-7)]

##### 2020

- [2020] **The endophytic fungi pestalotiopsis what’s for it and what’s on it?** *Pharmaceutics and Pharmacology Research* [[paper](https://doi.org/10.31579/2693-7247/032)]
- [2020] **Impact of cathodic electron acceptor on microbial fuel cell internal resistance** *Bioresource Technology* [[paper](https://doi.org/10.1016/j.biortech.2020.123919)]
- [2020] **Microbial synergistic interactions enhanced power generation in co-culture driven microbial fuel cell** *Science of The Total Environment* [[paper](https://doi.org/10.1016/j.scitotenv.2020.140138)]

##### 2019

- [2019] **Pleurotus ostreatus (oyster mushroom)** *CABI Compendium* [[paper](https://doi.org/10.1079/cabicompendium.42037)]
- [2019] **Characterization of electricity generation and microbial community structure over long-term operation of a microbial fuel cell** *Bioresource Technology* [[paper](https://doi.org/10.1016/j.biortech.2019.121395)]

##### 2018

- [2018] **Bioelectricity Generation and Dye Decolorization by Aspergillus niger and Trichoderma harzianum** *Journal of Bioremediation &amp; Biodegradation* [[paper](https://doi.org/10.4172/2155-6199.1000446)]
- [2018] **Yeast-Based Biofuel Cells** *Encyclopedia of Interfacial Chemistry* [[paper](https://doi.org/10.1016/b978-0-12-409547-2.13467-5)]

##### 2017

- [2017] **Sediment Microbial Fuel Cell and Constructed Wetland Assisted with It: Challenges and Future Prospects** *Microbial Fuel Cell* [[paper](https://doi.org/10.1007/978-3-319-66793-5_17)]
- [2017] **Self-sustaining, solar-driven bioelectricity generation in micro-sized microbial fuel cell using co-culture of heterotrophic and photosynthetic bacteria** *Journal of Power Sources* [[paper](https://doi.org/10.1016/j.jpowsour.2017.03.014)]

##### 2013

- [2013] **Fuel Cell Operating Conditions** *PEM Fuel Cells* [[paper](https://doi.org/10.1016/b978-0-12-387710-9.00005-9)]

##### 2012

- [2012] **Bioelectrochemical Systems, Energy Production and Electrosynthesis** *Journal of Microbial &amp; Biochemical Technology* [[paper](https://doi.org/10.4172/1948-5948.1000e112)]

##### 2011

- [2011] **Anode microbial communities produced by changing from microbial fuel cell to microbial electrolysis cell operation using two different wastewaters** *Bioresource Technology* [[paper](https://doi.org/10.1016/j.biortech.2010.05.019)]

[⬆ Back to top](#paper-list)

#### Degradation & Lifespan

##### 2026

- [2026] **Bioresorbable and Transient Bioelectronics** *Next-Generation Biodegradable and Bioactive Biomaterials* [[paper](https://doi.org/10.4018/979-8-2600-0060-1.ch012)]
- [2026] **Cellulose-based sensors for decentralized monitoring in precision agriculture.** *MED* [[paper](https://doi.org/10.1038/s41467-026-70730-7)]

##### 2025

- [2025] **Harnessing carbon potential of lignocellulosic biomass: advances in pretreatments, applications, and the transformative role of machine learning in biorefineries.** *MED* [[paper](https://doi.org/10.1186/s40643-025-00935-z)]
- [2025] **Biodegradation of azo dyes by Aspergillus flavus and its bioremediation potential using seed germination efficiency.** *MED* [[paper](https://doi.org/10.1186/s12866-024-03703-9)]
- [2025] **Solutions for Space Waste: Biodegradation of Polyurethane by Pestalotiopsis Microspora in Microgravity** *International Journal of Science and Research (IJSR)* [[paper](https://doi.org/10.21275/sr241230151350)]

##### 2024

- [2024] **Research Progress on Lignin Depolymerization Strategies: A Review.** *MED* [[paper](https://doi.org/10.3390/polym16172388)]

##### 2022

- [2022] **Fungal oxidoreductases and CAZymes effectively degrade lignocellulosic component of switchgrass for bioethanol production** *Fuel* [[paper](https://doi.org/10.1016/j.fuel.2022.125341)]
- [2022] **Azo dyes degradation by microorganisms - An efficient and sustainable approach.** *MED* [[paper](https://doi.org/10.1016/j.sjbs.2022.103437)]
- [2022] **Time-dependent electrochemical characteristics of a phenolic and non-phenolic compound in the presence of laccase/ABTS system.** *MED* [[paper](https://doi.org/10.1371/journal.pone.0275338)]
- [2022] **Review on the preparation of fuels and chemicals based on lignin.** *MED* [[paper](https://doi.org/10.1039/d2ra01341j)]
- [2022] **A Horseradish Peroxidase-Mediator System for Benzylic C-H Activation.** *MED* [[paper](https://doi.org/10.1021/acscatal.2c03424)]

##### 2021

- [2021] **Comprehensive in silico and gene expression profiles of MnP family genes in Phanerochaete chrysosporium towards lignin biodegradation** *International Biodeterioration &amp; Biodegradation* [[paper](https://doi.org/10.1016/j.ibiod.2020.105143)]

##### 2019

- [2019] **Pretreatment for biorefineries: a review of common methods for efficient utilisation of lignocellulosic materials.** *MED* [[paper](https://doi.org/10.1186/s13068-019-1634-1)]

##### 2018

- [2018] **PHBVTM Biodegradable Polyester** *Degradable Materials* [[paper](https://doi.org/10.1201/9781351071321-3)]

##### 2014

- [2014] **Stable current outputs and phytate degradation by yeast-based biofuel cell** *Yeast* [[paper](https://doi.org/10.1002/yea.3027)]

##### 2012

- [2012] **Selective removal of lignin in steam-exploded rice straw by Phanerochaete chrysosporium** *International Biodeterioration &amp; Biodegradation* [[paper](https://doi.org/10.1016/j.ibiod.2012.09.003)]

[⬆ Back to top](#paper-list)

### Electrode & Material Systems

#### Laccase-Mediated

##### 2026

- [2026] **Enhanced stability and reusability of metagenomic laccase via immobilization on functionalized mesoporous silica for antibiotic contaminant removal** *Scientific Reports* [[paper](https://doi.org/10.1038/s41598-026-40065-w)]

##### 2023

- [2023] **Glucose/O2 Enzymatic Biofuel Cell Constructed with a Laccase-Mimicking Nanozyme for Efficient Cathode Oxygen Reduction and Bacterial Surface-Displayed Cascade Enzymes for an Anode Biocatalyst** *Biosensors* [[paper](https://doi.org/10.1021/acs.analchem.6c00462.s001)]

##### 2020

- [2020] **A hydrogen/oxygen hybrid biofuel cell comprising an electrocatalytically active nanoflower/laccase-based biocathode** *Catalysis Science &amp; Technology* [[paper](https://doi.org/10.1039/d0cy00675k)]
- [2020] **Cellulose nanofiber-based electrode as a component of an enzyme-catalyzed biofuel cell** *RSC Advances* [[paper](https://doi.org/10.1039/d0ra03476b)]

##### 2019

- [2019] **A Novel and Enhanced Membrane-Free Performance of Glucose/O2 Biofuel Cell, Integrated With Biocompatible Laccase Nanoflower Biocathode and Glucose Dehydrogenase Bioanode** *IEEE Sensors Journal* [[paper](https://doi.org/10.1109/jsen.2019.2937814)]

##### 2017

- [2017] **Combination of physico-chemical entrapment and crosslinking of low activity laccase-based biocathode on carboxylated carbon nanotube for increasing biofuel cell performance** *Enzyme and Microbial Technology* [[paper](https://doi.org/10.1016/j.enzmictec.2017.06.012)]

##### 2016

- [2016] **Ethanol/O2 biofuel cell using a biocathode consisting of laccase/ HOOC-MWCNTs/polydiallyldimethylammonium chloride** *Enzyme and Microbial Technology* [[paper](https://doi.org/10.1016/j.enzmictec.2015.10.004)]

##### 2015

- [2015] **One-year stability for a glucose/oxygen biofuel cell combined with pH reactivation of the laccase/carbon nanotube biocathode** *Bioelectrochemistry* [[paper](https://doi.org/10.1016/j.bioelechem.2015.04.009)]

##### 2014

- [2014] **Biofuel cell for generating power from methanol substrate using alcohol oxidase bioanode and air-breathed laccase biocathode** *Biosensors and Bioelectronics* [[paper](https://doi.org/10.1016/j.bios.2014.03.016)]

##### 2013

- [2013] **Combination of laccase and catalase in construction of H2O2–O2 based biocathode for applications in glucose biofuel cells** *Biosensors and Bioelectronics* [[paper](https://doi.org/10.1016/j.bios.2012.07.066)]

##### 2012

- [2012] **Fully enzymatic mediatorless fuel cell with efficient naphthylated carbon nanotube–laccase composite cathodes** *Electrochemistry Communications* [[paper](https://doi.org/10.1016/j.elecom.2012.04.011)]
- [2012] **A 1.76V hybrid Zn-O2 biofuel cell with a fungal laccase-carbon cloth biocathode** *Electrochimica Acta* [[paper](https://doi.org/10.1016/j.electacta.2011.12.026)]

##### 2010

- [2010] **Laccase electrodes based on the combination of single-walled carbon nanotubes and redox layered double hydroxides: Towards the development of biocathode for biofuel cells** *Journal of Power Sources* [[paper](https://doi.org/10.1016/j.jpowsour.2010.02.033)]

##### 2009

- [2009] **Three-dimensional, gas phase fuel cell with a laccase biocathode** *Journal of Power Sources* [[paper](https://doi.org/10.1016/j.jpowsour.2008.11.110)]

##### 2004

- [2004] **Modification of electrode surface for covalent immobilization of laccase** *Materials Science and Engineering: C* [[paper](https://doi.org/10.1016/j.msec.2003.09.036)]

[⬆ Back to top](#paper-list)

#### Extracellular Electron Transfer

##### 2013

- [2013] **Direct electron transfer of Trametes hirsuta laccase adsorbed at unmodified nanoporous gold electrodes** *Bioelectrochemistry* [[paper](https://doi.org/10.1016/j.bioelechem.2012.11.001)]

##### 2006

- [2006] **Direct Heterogeneous Electron Transfer Reactions of <i>Trametes hirsuta</i> Laccase at Bare and Thiol‐Modified Gold Electrodes** *Electroanalysis* [[paper](https://doi.org/10.1002/elan.200603600)]

[⬆ Back to top](#paper-list)

#### Hybrid / Co-Culture

##### 2023

- [2023] **Living Mycelium Composites Discern Weights via Patterns of the Electrical Activity** *Emergence, Complexity and Computation* [[paper](https://doi.org/10.1007/978-3-031-38336-6_6)]

##### 2022

- [2022] **Living mycelium composites discern weights via patterns of electrical activity** *Journal of Bioresources and Bioproducts* [[paper](https://doi.org/10.1016/j.jobab.2021.09.003)]

##### 2021

- [2021] **Effects of electrode size on the power generation of the microbial fuel cell by Saccharomyces cerevisiae** *Ionics* [[paper](https://doi.org/10.1007/s11581-021-04162-2)]

##### 2018

- [2018] **Quantifying long-term electrode performance** *Neuroprosthetics* [[paper](https://doi.org/10.1201/b19640-9)]

##### 2014

- [2014] **Enhanced response of microbial fuel cell using sulfonated poly ether ether ketone membrane as a biochemical oxygen demand sensor** *Analytica Chimica Acta* [[paper](https://doi.org/10.1016/j.aca.2014.01.059)]

[⬆ Back to top](#paper-list)

#### Degradation & Lifespan

##### 2026

- [2026] **Biodegradable Transient Electronics: Sustainable Materials and Architectures for Circular IoT and Computing** [[paper](https://doi.org/10.62311/nesx/rb-978-81-999904-4-9)]

##### 2024

- [2024] **Photothermic Energy Harvesting in Reduced Graphene Oxide Nanosheets Intercalated with Vanadium Nitride as Pseudocapacitive Electrode** *ACS Applied Nano Materials* [[paper](https://doi.org/10.1021/acsanm.4c01118.s001)]

##### 2023

- [2023] **Biowelding 3D-Printed Biodigital Brick of Seashell-Based Biocomposite by Pleurotus ostreatus Mycelium** *Biomimetics* [[paper](https://doi.org/10.3390/biomimetics8060504)]

##### 2022

- [2022] **High-Performance Asymmetric Flow-Electrode Capacitive Mixing with MnO2Coated Activated Carbon Flow-Electrode for Energy Harvesting from Salinity Gradient Power** [[paper](https://doi.org/10.1021/acsmaterialslett.2c00154.s001)]
- [2022] **New membrane and electrode assembly concept to improve salinity energy harvesting.** *Energy Conversion and Management* [[paper](https://doi.org/10.1016/j.enconman.2022.115297)]

##### 2020

- [2020] **Electrosprayed ThylakoidAlginate Film on a Micro-Pillar Electrode for Scalable Photosynthetic Energy Harvesting** [[paper](https://doi.org/10.1021/acsami.0c15993.s001)]

##### 2018

- [2018] **New biodegradable nano-composites for transient electronics devices** *AIP Conference Proceedings* [[paper](https://doi.org/10.1063/1.5047766)]

##### 2017

- [2017] **Fabrication of Advanced Electrode Materials for Supercapacitors** *International Conference of Energy Harvesting, Storage, and Transfer* [[paper](https://doi.org/10.11159/ehst17.103)]
- [2017] **Self-Sterilized Flexible Single-Electrode Triboelectric Nanogenerator for Energy Harvesting and Dynamic Force Sensing** *ACS Nano* [[paper](https://doi.org/10.1021/acsnano.6b07389.s001)]

##### 2016

- [2016] **A New Approach to Manufacturing Biocomposite Sandwich Structures: Mycelium-Based Cores** *Volume 1: Processing* [[paper](https://doi.org/10.1115/msec2016-8864)]

[⬆ Back to top](#paper-list)

### Applications & Devices

#### Laccase-Mediated

##### 2024

- [2024] **Towards a Self-Powered Amperometric Glucose Biosensor Based on a Single-Enzyme Biofuel Cell** *Biosensors* [[paper](https://doi.org/10.3390/bios14030138)]

[⬆ Back to top](#paper-list)

#### Extracellular Electron Transfer

##### 2021

- [2021] **Competitive advantage of oxygen-tolerant bioanodes of Geobacter sulfurreducens in bioelectrochemical systems** *Biofilm* [[paper](https://doi.org/10.1016/j.bioflm.2021.100052)]

[⬆ Back to top](#paper-list)

#### Hybrid / Co-Culture

##### 2026

- [2026] **Sediment Microbial Fuel Cell for Bioelectricity Generation** *Sediment Transport and Depositional Processes [Working Title]* [[paper](https://doi.org/10.5772/intechopen.1016822)]

##### 2025

- [2025] **Signal Amplification Strategy-Assisted Dual Photoelectrode Fuel Cell Self-Powered Sensor for MecA Gene Detection** *Analytical Chemistry* [[paper](https://doi.org/10.1021/acs.analchem.5c01477.s001)]
- [2025] **Industrial applications of Yarrowia lipolytica** *Yarrowia Lipolytica Yeast* [[paper](https://doi.org/10.1016/b978-0-443-22092-0.00005-0)]

##### 2024

- [2024] **Evaluation of a comprehensive power management system with maximum power point tracking algorithm for multiple microbial fuel cell energy harvesting** *Bioelectrochemistry* [[paper](https://doi.org/10.1016/j.bioelechem.2023.108597)]
- [2024] **A Study on the Modification, Mechanism, and Properties of a Self-Powered H2o2 Electrochemical Sensor Based on a Fuel Cell Configuration with Fen4 and Graphene Cathode Catalyst Materials** *SSRN Electronic Journal* [[paper](https://doi.org/10.2139/ssrn.4725738)]

##### 2023

- [2023] **Dual-Photoelectrode Fuel Cell Based Self-Powered Sensor for a Picomole Level Pollutant: Using an In Situ Molecularly Imprinted pType Organic Photocathode** [[paper](https://doi.org/10.1021/acs.analchem.3c03066.s001)]
- [2023] **Bioelectricity Generation by Single Chamber Microbial Fuel Cell by Using Platinum Catalyst as Electrode** *Petroleum &amp; Petrochemical Engineering Journal* [[paper](https://doi.org/10.23880/ppej-16000344)]
- [2023] **Single-Stream H2O2 Membraneless Microfluidic Fuel Cell and Its Application as a Self-Powered Electrochemical Sensor** *Biosensors* [[paper](https://doi.org/10.1021/acs.iecr.0c02548.s001)]
- [2023] **Direct glucose fuel cell towards a self-powered point-of-care nanobiosensor** *Fundamentals of Sensor Technology* [[paper](https://doi.org/10.1016/b978-0-323-88431-0.00010-7)]

##### 2022

- [2022] **Cofe2o4 Embedded Bacterial Cellulose for Flexible, Biodegradable, and Self-Powered Electromagnetic Sensor** *Nano Energy* [[paper](https://doi.org/10.2139/ssrn.4136294)]
- [2022] **A Solar-Cell-Assisted, 99% Biofuel Cell Area Reduced, Biofuel-Cell-Powered Wireless Biosensing System in 65nm CMOS for Continuous Glucose Monitoring Contact Lenses** *IEICE Transactions on Electronics* [[paper](https://doi.org/10.1587/transele.2021cds0002)]

##### 2021

- [2021] **Microstructure and battery performance of Mg-Zn-Sn alloys as anodes for magnesium-air battery** *Journal of Magnesium and Alloys* [[paper](https://doi.org/10.1016/j.jma.2021.08.022)]
- [2021] **Photocatalytic Fuel Cell-Assisted Molecularly Imprinted Self-Powered Sensor: A Flexible and Sensitive Tool for Detecting Aflatoxin B1** *Analytical Chemistry* [[paper](https://doi.org/10.1021/acs.analchem.1c02074.s001)]
- [2021] **Self-Powered Diaper Sensor with Wireless Transmitter Powered by Paper-Based Biofuel Cell with Urine Glucose as Fuel** *ACS Sensors* [[paper](https://doi.org/10.1021/acssensors.1c01266.s001)]
- [2021] **Implantable Biofuel Cells for Biomedical Applications** *Biofuel Cells* [[paper](https://doi.org/10.1002/9781119725008.ch3)]

##### 2020

- [2020] **Bioelectricity generation in a microbial fuel cell using polypyrrole-molybdenum oxide composite as an effective cathode catalyst** *Fuel* [[paper](https://doi.org/10.1016/j.fuel.2020.117994)]

##### 2019

- [2019] **Ratiometric Self-Powered Sensor for 17-Estradiol Detection Based on a Dual-Channel Photocatalytic Fuel Cell** *Frontiers in Chemistry* [[paper](https://doi.org/10.1021/acs.analchem.0c01543.s001)]
- [2019] **NFC Hybrid Harvester for Battery-free Agricultural Sensor Nodes** *2019 IEEE International Conference on RFID Technology and Applications (RFID-TA)* [[paper](https://doi.org/10.1109/rfid-ta.2019.8892237)]
- [2019] **Net power positive maximum power point tracking energy harvesting system for microbial fuel cell** *Journal of Power Sources* [[paper](https://doi.org/10.1016/j.jpowsour.2019.02.042)]

##### 2018

- [2018] **Bioelectricity Generation in Soil Microbial Fuel Cells Using Organic Waste** *Microbial Fuel Cell Technology for Bioelectricity* [[paper](https://doi.org/10.1007/978-3-319-92904-0_7)]
- [2018] **Advances in Concurrent Bioelectricity Generation and Bioremediation Through Microbial Fuel Cells** *Microbial Fuel Cell Technology for Bioelectricity* [[paper](https://doi.org/10.1007/978-3-319-92904-0_11)]
- [2018] **Microbial Fuel Cell Technology for Bioelectricity** [[paper](https://doi.org/10.1007/978-3-319-92904-0)]
- [2018] **Rumen Fluid Microbes for Bioelectricity Production: A Novel Approach** *Microbial Fuel Cell Technology for Bioelectricity* [[paper](https://doi.org/10.1007/978-3-319-92904-0_10)]
- [2018] **Electricigens: Role and Prominence in Microbial Fuel Cell Performance** *Microbial Fuel Cell Technology for Bioelectricity* [[paper](https://doi.org/10.1007/978-3-319-92904-0_9)]
- [2018] **Plant Microbial Fuel Cell Technology: Developments and Limitations** *Microbial Fuel Cell Technology for Bioelectricity* [[paper](https://doi.org/10.1007/978-3-319-92904-0_3)]
- [2018] **Heavy Metal Sensor Research Based on Microbial Fuel Cell** *International Journal of Environmental Monitoring and Analysis* [[paper](https://doi.org/10.11648/j.ijema.20180602.13)]

##### 2017

- [2017] **Battery-Free and Energy-Effective RFID Sensor Tag for Health Monitoring in Smart Grid** *2017 Asia Modelling Symposium (AMS)* [[paper](https://doi.org/10.1109/ams.2017.35)]

##### 2016

- [2016] **Magnesium–Air Battery** *Metal-Air and Metal-Sulfur Batteries* [[paper](https://doi.org/10.1201/9781315372280-12)]

##### 2015

- [2015] **Bioelectricity Generation and Treatment of Sugar Mill Effluent Using a Microbial Fuel Cell** *Journal of Clean Energy Technologies* [[paper](https://doi.org/10.7763/jocet.2016.v4.291)]

##### 2012

- [2012] **A Self-Powered Acetaldehyde Sensor Based on Biofuel Cell** *Analytical Chemistry* [[paper](https://doi.org/10.1021/ac302414a)]

[⬆ Back to top](#paper-list)

#### Degradation & Lifespan

##### 2025

- [2025] **3D‐Printed Macroporous Resin Anode in Microbial Fuel Cell‐Based Biosensors for Efficient Biodegradable Organic Carbon Monitoring** *Advanced Sensor Research* [[paper](https://doi.org/10.1002/adsr.202500072)]

[⬆ Back to top](#paper-list)

### Surveys & Reviews

#### Hybrid / Co-Culture

##### 2021

- [2021] **Material Function of Mycelium-Based Bio-Composite: A Review** *Frontiers in Materials* [[paper](https://doi.org/10.3389/fmats.2021.737377)]

[⬆ Back to top](#paper-list)

## 📖 Citation

If you use this corpus for a project, please cite:

```bibtex
@misc{mykovolt-research,
  author = {Weiß, Tobias},
  title = {MykoVolt MFC Research Corpus: Fungal Bioelectrochemistry Literature},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/tobias-weiss-ai-xr/mykovolt/blob/main/research/README.md}
}
```

## 📄 License

MIT — see [LICENSE](../LICENSE).
