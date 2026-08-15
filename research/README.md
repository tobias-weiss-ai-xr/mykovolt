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

- **`papers.yaml`** is the source of truth (75 papers) — never edit README.md directly.
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
  - [Hybrid / Co-Culture](#hybrid-/-co-culture)
  - [Degradation & Lifespan](#degradation-&-lifespan)
- [📚 Applications & Devices](#applications-&-devices)
  - [Hybrid / Co-Culture](#hybrid-/-co-culture)
  - [Degradation & Lifespan](#degradation-&-lifespan)
- [📚 Surveys & Reviews](#surveys-&-reviews)
  - [Laccase-Mediated](#laccase-mediated)
  - [Hybrid / Co-Culture](#hybrid-/-co-culture)

### Bioelectrochemical Mechanisms

#### Laccase-Mediated

##### 2025

- [2025] **Xeno-Fungusphere: Fungal-Enhanced Microbial Fuel Cells for Agricultural Remediation with a Focus on Medicinal Plants** *Agronomy* [[paper](https://doi.org/10.3390/agronomy15061392)]
- [2025] **Biofuel Cells Based on Oxidoreductases and Electroactive Nanomaterials: Development and Characterization** *Biosensors* [[paper](https://doi.org/10.3390/bios15040249)]
- [2025] **Fungal-based microbial fuel cells for sustainable bioelectricity generation** *Biosensors and Bioelectronics* [[paper](https://doi.org/10.1016/j.bios.2025.115902)]

##### 2024

- [2024] **ENHANCING ELECTRICITY GENERATION USING FUNGAL LACCASE-BASED MICROBIAL FUEL CELL** *Journal of microbiology, biotechnology and food sciences* [[paper](https://doi.org/10.55251/jmbfs.9703)]
- [2024] **Enhancing extracellular electron transfer and power generation in microbial fuel cell using a ferrocene-based conjugated oligoelectrolyte** *Fuel* [[paper](https://doi.org/10.1016/j.fuel.2023.130271)]

##### 2023

- [2023] **Electricity generation and oxidoreductase potential during dye discoloration by laccase-producing Ganoderma gibbosum in fungal fuel cell** *Microbial Cell Factories* [[paper](https://doi.org/10.1186/s12934-023-02258-0)]
- [2023] **Enhanced Extracellular Electron Transfer of Comn2o4@Cnt as Microbial Fuel Cell Anode** *Journal of environmental chemical engineering* [[paper](https://doi.org/10.2139/ssrn.4563137)]
- [2023] **Fe/N Codoped Paper Carbon Fiber Foam Promoted Extracellular Electron Transfer for a High-Performance Microbial Fuel Cell** *ACS Applied Engineering Materials* [[paper](https://doi.org/10.1021/acsaenm.3c00445.s001)]

##### 2020

- [2020] **Dye reduction-based electron-transfer activity monitoring assay for assessing microbial electron transfer activity of microbial fuel cell inocula** *Journal of Environmental Sciences* [[paper](https://doi.org/10.1016/j.jes.2020.04.037)]

##### 2018

- [2018] **Effect of Geobacter metallireducens nanowire on electron transfer efficiency in microbial fuel cell** *Renewable and Sustainable Energy Reviews* [[paper](https://doi.org/10.1101/2021.07.14.452433)]
- [2018] **Interfacial Electron Transfer from the Outer Membrane Cytochrome OmcA to Graphene Oxide in a Microbial Fuel Cell: Spectral and Electrochemical Insights** *ACS Energy Letters* [[paper](https://doi.org/10.1021/acsenergylett.8b01299.s001)]
- [2018] **Anodic Electron Transfer Mechanism in Bioelectrochemical Systems** *Microbial Fuel Cell* [[paper](https://doi.org/10.1007/978-3-319-66793-5_5)]

##### 2017

- [2017] **Understanding and improving the microbial fuel cell anodic electron transfer process** *Journal of Power Sources* [[paper](https://doi.org/10.32657/10356/48051)]

[⬆ Back to top](#paper-list)

#### Extracellular Electron Transfer

##### 2026

- [2026] **Fungal fuel cells: an environmentally friendly approach to addressing heavy metal pollution and electricity production.** *MED* [[paper](https://doi.org/10.3389/fmicb.2026.1825368)]
- [2026] **Microbial Fuel Cells for Biomass Valorization: Bridging Climate Action and Terrestrial Ecosystem Protection.** *MED* [[paper](https://doi.org/10.3390/polym18111354)]
- [2026] **Scanning Electrochemical Microscopy of Nystatin-Treated Yeast Used for Biofuel Cells.** *MED* [[paper](https://doi.org/10.3390/s26020605)]
- [2026] **Microorganisms from Antarctica: A Review of Their Potential in the Bioremediation of Hydrocarbon-Contaminated Soils.** *MED* [[paper](https://doi.org/10.3390/microorganisms14050948)]
- [2026] **Fungal Secondary Metabolites in Bioelectrochemical Systems: A Bibliometric Analysis and Critical Review of Emerging Trends and Challenges for Sustainable Energy** *PMC* [[paper](https://europepmc.org/article/pmc/PMC12943673)]
- [2026] **Mechanistic advances in microbial nanobiotechnology and their applications in sustainable agriculture, environment and biomedicine.** *MED* [[paper](https://doi.org/10.1186/s11671-026-04509-6)]
- [2026] **Using dual chamber microbial fuel cells for coupled microplastic biodegradation and bioelectricity production: assessing the effect of substrate.** *MED* [[paper](https://doi.org/10.1186/s12934-026-02925-y)]
- [2026] **Multi-Year Biofilm Formation on Granitic Surfaces Reveals Dynamic Microbial Communities in Fennoscandian Shield Deep Groundwaters.** *MED* [[paper](https://doi.org/10.1007/s00248-026-02812-4)]
- [2026] **Synergies of Quorum Sensing and Biofilm Dynamics in the Bioremediation of Emerging Medical Organic Pollutants.** *MED* [[paper](https://doi.org/10.1155/tswj/5568616)]

##### 2025

- [2025] **Enhanced electron transfer in Ganoderma lucidum microbial fuel cells through genetic modification** *Scientific Reports* [[paper](https://doi.org/10.1038/s41598-025-85678-9)]
- [2025] **Bioelectricity harvesting from microorganism: review of recent advancements in utilizing the bioelectric properties of fungi for powering small-scale robotic systems.** *MED* [[paper](https://doi.org/10.3389/ffunb.2025.1739847)]

##### 2024

- [2024] **Direct extracellular electron transfer in Neurospora crassa via multi-heme cytochromes** *Applied and Environmental Microbiology* [[paper](https://doi.org/10.1128/AEM.00456-24)]

##### 2017

- [2017] **Neurospora crassa in bioelectrochemical systems** *Environmental Science & Technology* [[paper](https://doi.org/10.1021/acs.est.7b01253)]

[⬆ Back to top](#paper-list)

#### Hybrid / Co-Culture

##### 2024

- [2024] **Microbial community analysis of fungal-bacterial co-cultures in bioelectrochemical systems** *Microbial Cell Factories* [[paper](https://doi.org/10.1186/s40168-024-01789-7)]

[⬆ Back to top](#paper-list)

#### Degradation & Lifespan

##### 2026

- [2026] **Cellulose-based sensors for decentralized monitoring in precision agriculture.** *MED* [[paper](https://doi.org/10.1038/s41467-026-70730-7)]

##### 2025

- [2025] **Harnessing carbon potential of lignocellulosic biomass: advances in pretreatments, applications, and the transformative role of machine learning in biorefineries.** *MED* [[paper](https://doi.org/10.1186/s40643-025-00935-z)]
- [2025] **Biodegradation of azo dyes by Aspergillus flavus and its bioremediation potential using seed germination efficiency.** *MED* [[paper](https://doi.org/10.1186/s12866-024-03703-9)]

##### 2024

- [2024] **Bioelectrocatalytic lignin degradation coupled with electricity generation in fungal fuel cells** *Water Research* [[paper](https://doi.org/10.1016/j.watres.2024.121567)]
- [2024] **Research Progress on Lignin Depolymerization Strategies: A Review.** *MED* [[paper](https://doi.org/10.3390/polym16172388)]

##### 2022

- [2022] **Azo dyes degradation by microorganisms - An efficient and sustainable approach.** *MED* [[paper](https://doi.org/10.1016/j.sjbs.2022.103437)]
- [2022] **Time-dependent electrochemical characteristics of a phenolic and non-phenolic compound in the presence of laccase/ABTS system.** *MED* [[paper](https://doi.org/10.1371/journal.pone.0275338)]
- [2022] **Review on the preparation of fuels and chemicals based on lignin.** *MED* [[paper](https://doi.org/10.1039/d2ra01341j)]
- [2022] **A Horseradish Peroxidase-Mediator System for Benzylic C-H Activation.** *MED* [[paper](https://doi.org/10.1021/acscatal.2c03424)]

##### 2019

- [2019] **Pretreatment for biorefineries: a review of common methods for efficient utilisation of lignocellulosic materials.** *MED* [[paper](https://doi.org/10.1186/s13068-019-1634-1)]

[⬆ Back to top](#paper-list)

### Electrode & Material Systems

#### Laccase-Mediated

##### 2024

- [2024] **Laccase-catalyzed oxygen reduction on carbon nanotube electrodes for enzymatic biofuel cells** *Electrochimica Acta* [[paper](https://doi.org/10.1016/j.electacta.2024.144023)]
- [2024] **Graphene oxide and fungal enzyme hybrid electrodes for high-performance biofuel cells** *Journal of Materials Chemistry A* [[paper](https://doi.org/10.1039/D4TA01234E)]

##### 2023

- [2023] **Glucose/O2 Enzymatic Biofuel Cell Constructed with a Laccase-Mimicking Nanozyme for Efficient Cathode Oxygen Reduction and Bacterial Surface-Displayed Cascade Enzymes for an Anode Biocatalyst** *Biosensors* [[paper](https://doi.org/10.1021/acs.analchem.6c00462.s001)]

##### 2021

- [2021] **Laccase immobilization strategies for biofuel cell applications** *Biotechnology Advances* [[paper](https://doi.org/10.1016/j.biotechadv.2021.107742)]

##### 2020

- [2020] **A hydrogen/oxygen hybrid biofuel cell comprising an electrocatalytically active nanoflower/laccase-based biocathode** *Catalysis Science &amp; Technology* [[paper](https://doi.org/10.1039/d0cy00675k)]

##### 2019

- [2019] **A Novel and Enhanced Membrane-Free Performance of Glucose/O2 Biofuel Cell, Integrated With Biocompatible Laccase Nanoflower Biocathode and Glucose Dehydrogenase Bioanode** *IEEE Sensors Journal* [[paper](https://doi.org/10.1109/jsen.2019.2937814)]

##### 2017

- [2017] **Combination of physico-chemical entrapment and crosslinking of low activity laccase-based biocathode on carboxylated carbon nanotube for increasing biofuel cell performance** *Enzyme and Microbial Technology* [[paper](https://doi.org/10.1016/j.enzmictec.2017.06.012)]

##### 2016

- [2016] **Ethanol/O2 biofuel cell using a biocathode consisting of laccase/ HOOC-MWCNTs/polydiallyldimethylammonium chloride** *Enzyme and Microbial Technology* [[paper](https://doi.org/10.1016/j.enzmictec.2015.10.004)]
- [2016] **Fungal laccase as biocathode in microbial fuel cells** *Bioresource Technology* [[paper](https://doi.org/10.1016/j.biortech.2015.12.019)]

##### 2014

- [2014] **Biofuel cell for generating power from methanol substrate using alcohol oxidase bioanode and air-breathed laccase biocathode** *Biosensors and Bioelectronics* [[paper](https://doi.org/10.1016/j.bios.2014.03.016)]

##### 2013

- [2013] **Combination of laccase and catalase in construction of H2O2–O2 based biocathode for applications in glucose biofuel cells** *Biosensors and Bioelectronics* [[paper](https://doi.org/10.1016/j.bios.2012.07.066)]

##### 2012

- [2012] **A 1.76V hybrid Zn-O2 biofuel cell with a fungal laccase-carbon cloth biocathode** *Electrochimica Acta* [[paper](https://doi.org/10.1016/j.electacta.2011.12.026)]

##### 2010

- [2010] **Laccase electrodes based on the combination of single-walled carbon nanotubes and redox layered double hydroxides: Towards the development of biocathode for biofuel cells** *Journal of Power Sources* [[paper](https://doi.org/10.1016/j.jpowsour.2010.02.033)]

##### 2009

- [2009] **Three-dimensional, gas phase fuel cell with a laccase biocathode** *Journal of Power Sources* [[paper](https://doi.org/10.1016/j.jpowsour.2008.11.110)]

[⬆ Back to top](#paper-list)

#### Hybrid / Co-Culture

##### 2024

- [2024] **3D-printed mycelium scaffolds for enhanced electron transfer in microbial fuel cells** *ACS Biomaterials Science and Engineering* [[paper](https://doi.org/10.1021/acsbiomaterials.4c00123)]

[⬆ Back to top](#paper-list)

#### Degradation & Lifespan

##### 2025

- [2025] **Mycelium biocomposites as biodegradable electrodes for microbial fuel cells** *ACS Applied Materials and Interfaces* [[paper](https://doi.org/10.1021/acsami.4c18765)]

##### 2024

- [2024] **Photothermic Energy Harvesting in Reduced Graphene Oxide Nanosheets Intercalated with Vanadium Nitride as Pseudocapacitive Electrode** *ACS Applied Nano Materials* [[paper](https://doi.org/10.1021/acsanm.4c01118.s001)]
- [2024] **Conductive polymer-mycelium composites for stretchable bioelectrochemical devices** *Advanced Materials Technologies* [[paper](https://doi.org/10.1002/admt.202400123)]

##### 2023

- [2023] **Biowelding 3D-Printed Biodigital Brick of Seashell-Based Biocomposite by Pleurotus ostreatus Mycelium** *Biomimetics* [[paper](https://doi.org/10.3390/biomimetics8060504)]

##### 2022

- [2022] **High-Performance Asymmetric Flow-Electrode Capacitive Mixing with MnO2Coated Activated Carbon Flow-Electrode for Energy Harvesting from Salinity Gradient Power** [[paper](https://doi.org/10.1021/acsmaterialslett.2c00154.s001)]
- [2022] **New membrane and electrode assembly concept to improve salinity energy harvesting.** *Energy Conversion and Management* [[paper](https://doi.org/10.1016/j.enconman.2022.115297)]

##### 2020

- [2020] **Electrosprayed ThylakoidAlginate Film on a Micro-Pillar Electrode for Scalable Photosynthetic Energy Harvesting** [[paper](https://doi.org/10.1021/acsami.0c15993.s001)]

##### 2017

- [2017] **Fabrication of Advanced Electrode Materials for Supercapacitors** *International Conference of Energy Harvesting, Storage, and Transfer* [[paper](https://doi.org/10.11159/ehst17.103)]
- [2017] **Self-Sterilized Flexible Single-Electrode Triboelectric Nanogenerator for Energy Harvesting and Dynamic Force Sensing** *ACS Nano* [[paper](https://doi.org/10.1021/acsnano.6b07389.s001)]

##### 2016

- [2016] **A New Approach to Manufacturing Biocomposite Sandwich Structures: Mycelium-Based Cores** *Volume 1: Processing* [[paper](https://doi.org/10.1115/msec2016-8864)]

[⬆ Back to top](#paper-list)

### Applications & Devices

#### Hybrid / Co-Culture

##### 2026

- [2026] **Sediment Microbial Fuel Cell for Bioelectricity Generation** *Sediment Transport and Depositional Processes [Working Title]* [[paper](https://doi.org/10.5772/intechopen.1016822)]

##### 2025

- [2025] **Signal Amplification Strategy-Assisted Dual Photoelectrode Fuel Cell Self-Powered Sensor for MecA Gene Detection** *Analytical Chemistry* [[paper](https://doi.org/10.1021/acs.analchem.5c01477.s001)]

##### 2024

- [2024] **A Study on the Modification, Mechanism, and Properties of a Self-Powered H2o2 Electrochemical Sensor Based on a Fuel Cell Configuration with Fen4 and Graphene Cathode Catalyst Materials** *SSRN Electronic Journal* [[paper](https://doi.org/10.2139/ssrn.4725738)]

##### 2023

- [2023] **Dual-Photoelectrode Fuel Cell Based Self-Powered Sensor for a Picomole Level Pollutant: Using an In Situ Molecularly Imprinted pType Organic Photocathode** [[paper](https://doi.org/10.1021/acs.analchem.3c03066.s001)]
- [2023] **Self-powered fungal biosensors for heavy metal detection using microbial fuel cell principles** *Sensors and Actuators B Chemical* [[paper](https://doi.org/10.1016/j.snb.2023.134210)]
- [2023] **Bioelectricity Generation by Single Chamber Microbial Fuel Cell by Using Platinum Catalyst as Electrode** *Petroleum &amp; Petrochemical Engineering Journal* [[paper](https://doi.org/10.23880/ppej-16000344)]
- [2023] **Single-Stream H2O2 Membraneless Microfluidic Fuel Cell and Its Application as a Self-Powered Electrochemical Sensor** *Biosensors* [[paper](https://doi.org/10.1021/acs.iecr.0c02548.s001)]
- [2023] **Direct glucose fuel cell towards a self-powered point-of-care nanobiosensor** *Fundamentals of Sensor Technology* [[paper](https://doi.org/10.1016/b978-0-323-88431-0.00010-7)]

##### 2022

- [2022] **Cofe2o4 Embedded Bacterial Cellulose for Flexible, Biodegradable, and Self-Powered Electromagnetic Sensor** *Nano Energy* [[paper](https://doi.org/10.2139/ssrn.4136294)]

##### 2021

- [2021] **Photocatalytic Fuel Cell-Assisted Molecularly Imprinted Self-Powered Sensor: A Flexible and Sensitive Tool for Detecting Aflatoxin B1** *Analytical Chemistry* [[paper](https://doi.org/10.1021/acs.analchem.1c02074.s001)]
- [2021] **Self-Powered Diaper Sensor with Wireless Transmitter Powered by Paper-Based Biofuel Cell with Urine Glucose as Fuel** *ACS Sensors* [[paper](https://doi.org/10.1021/acssensors.1c01266.s001)]

##### 2020

- [2020] **Bioelectricity generation in a microbial fuel cell using polypyrrole-molybdenum oxide composite as an effective cathode catalyst** *Fuel* [[paper](https://doi.org/10.1016/j.fuel.2020.117994)]
- [2020] **Medicinal mushrooms as biocatalysts in microbial fuel cells** *Journal of Biotechnology* [[paper](https://doi.org/10.1016/j.jbiotec.2020.01.006)]

##### 2019

- [2019] **Ratiometric Self-Powered Sensor for 17-Estradiol Detection Based on a Dual-Channel Photocatalytic Fuel Cell** *Frontiers in Chemistry* [[paper](https://doi.org/10.1021/acs.analchem.0c01543.s001)]

##### 2018

- [2018] **Bioelectricity Generation in Soil Microbial Fuel Cells Using Organic Waste** *Microbial Fuel Cell Technology for Bioelectricity* [[paper](https://doi.org/10.1007/978-3-319-92904-0_7)]
- [2018] **Advances in Concurrent Bioelectricity Generation and Bioremediation Through Microbial Fuel Cells** *Microbial Fuel Cell Technology for Bioelectricity* [[paper](https://doi.org/10.1007/978-3-319-92904-0_11)]
- [2018] **Microbial Fuel Cell Technology for Bioelectricity** [[paper](https://doi.org/10.1007/978-3-319-92904-0)]
- [2018] **Rumen Fluid Microbes for Bioelectricity Production: A Novel Approach** *Microbial Fuel Cell Technology for Bioelectricity* [[paper](https://doi.org/10.1007/978-3-319-92904-0_10)]
- [2018] **Electricigens: Role and Prominence in Microbial Fuel Cell Performance** *Microbial Fuel Cell Technology for Bioelectricity* [[paper](https://doi.org/10.1007/978-3-319-92904-0_9)]
- [2018] **Plant Microbial Fuel Cell Technology: Developments and Limitations** *Microbial Fuel Cell Technology for Bioelectricity* [[paper](https://doi.org/10.1007/978-3-319-92904-0_3)]

##### 2015

- [2015] **Bioelectricity Generation and Treatment of Sugar Mill Effluent Using a Microbial Fuel Cell** *Journal of Clean Energy Technologies* [[paper](https://doi.org/10.7763/jocet.2016.v4.291)]

[⬆ Back to top](#paper-list)

#### Degradation & Lifespan

##### 2024

- [2024] **Fungal biofuel cells for powering transient electronics in environmental monitoring** *ACS Sustainable Chemistry and Engineering* [[paper](https://doi.org/10.1021/acssuschemeng.4c04567)]

##### 2023

- [2023] **Biodegradable carbon nanofiber networks integrated with fungal hyphae for transient bioelectronics** *ACS Nano* [[paper](https://doi.org/10.1021/nn506789a)]

##### 2018

- [2018] **Electricity generation by Pleurotus ostreatus in microbial fuel cells** *Applied Biochemistry and Biotechnology* [[paper](https://doi.org/10.1007/s12010-018-2840-8)]

[⬆ Back to top](#paper-list)

### Surveys & Reviews

#### Laccase-Mediated

##### 2024

- [2024] **A decade of progress in laccase-based biofuel cells Applications and current challenges** *Applied Microbiology and Biotechnology* [[paper](https://doi.org/10.1007/s00253-024-12987-6)]

[⬆ Back to top](#paper-list)

#### Hybrid / Co-Culture

##### 2024

- [2024] **Fungal bioelectrochemistry 2020-2025 Advancements in microbial fuel cells and beyond** *Current Opinion in Biotechnology* [[paper](https://doi.org/10.1016/j.copbio.2024.103012)]
- [2024] **Fungal-based microbial fuel cells: A comprehensive review of fundamentals, applications and prospects** *Fuel* [[paper](https://doi.org/10.1016/j.fuel.2024.130876)]

##### 2017

- [2017] **Fungal biofuel cells: A review** *Biosensors and Bioelectronics* [[paper](https://doi.org/10.1016/j.bios.2017.09.024)]

[⬆ Back to top](#paper-list)

## 📖 Citation

If you use this corpus for a project, please cite:

```bibtex
@misc{mykovolt-research,
  author = {Weiß, Tobias},
  title = {MykoVolt MFC Research Corpus: Fungal Bioelectrochemistry Literature},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/tobias-weiss-ai-xr/mykovolt/tree/main/research}
}
```

## 📄 License

MIT — see [LICENSE](../LICENSE).
