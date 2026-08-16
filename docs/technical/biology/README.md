# MykoVolt Biology Layer — Fungal Species for MFCs

> **Status:** Active Research | **Last Updated:** August 2026 | **Maintainer:** @weissto
> **Related:** [Product Concepts](../product/product_concepts.md) | [Breadboard Prototype](../prototyping/breadboard_variant.md) | [Order Checklist](../prototyping/order_checklist.md)

---

## 🧬 Overview

This document specifies the **fungal species** evaluated for use in MykoVolt's **microbial fuel cells (MFCs)**. The selection is optimized for:

1. **Power output** (compatibility with BQ25570 energy harvester: **0.33–5 V input**)
2. **Hardware integration** (FDC1004 capacitance sensor, ST25DV04K NFC, interdigital electrodes)
3. **Application suitability** (DevKit, sensors, medical, industrial)
4. **Scalability** (cost, availability, ease of cultivation)

> 📚 **Evidence base:** Species selection and cultivation parameters are grounded in the [MykoVolt MFC research corpus](../../research/docs/research/mfc_literature_review.md) — 75 papers on fungal bioelectrochemistry, auto-discovered via arXiv/CrossRef/OpenAlex.

---

## 🔬 Fungal Species Comparison Table

The following table ranks **6 fungal species** by their suitability for MykoVolt applications. All data is based on **literature reviews** (see [References](#references)) and **internal testing** with the DevKit hardware.

| Species | Scientific Name | Eignung für MykoVolt | **Primäre Anwendungen** | Stromausbeute | Lebensdauer | Substrat | Verfügbarkeit | Kosten (pro Kultur) | TRL | Notes |
|---------|------------------|----------------------|-------------------------|----------------|--------------|----------|--------------|---------------------|-----|-------|
| **Trametes versicolor** | *Trametes versicolor* | ⭐⭐⭐⭐⭐ | **DevKit, Soil Moisture Sensor, Compost Monitor, Smart Packaging, Forestry Under-Canopy** | **100–200 µW/cm²** | 3–4 Wochen | Lignin (Holzspäne, Agrarreste), Cellulose | **Hoch** (DSMZ, ATCC, Pilzzüchter) | €15–25 | 5 | **Best all-round choice** for most MykoVolt use cases. High laccase activity (10,000–20,000 U/L). Compatible with **BQ25570** and **interdigital electrodes**. |
| **Neurospora crassa** | *Neurospora crassa* | ⭐⭐⭐⭐⭐ | **High-Performance MFCs (Forschung, Medizin), Soil Carbon Verification, Agricultural Network** | **200–260 µW/cm²** | 2–3 Wochen | Glucose (Vogel’s Medium), Saccharose | Mittel (FGSC, DSMZ) | €20–30 | 4 | **Highest power density** of all tested species. Genetically well-characterized. Requires **specific medium (Vogel’s)**. |
| **Aspergillus niger** | *Aspergillus niger* | ⭐⭐⭐⭐ | **Mg-Air Hybrid Systems (Permafrost, Landfill), Smart City Infrastructure, Industrial Sensors** | 150–180 µW/cm² | 4–6 Wochen | Industrielle Abfälle (Pektin, Zellulose), Melasse | **Sehr hoch** | €10–20 | 5 | **Industrially robust**. Works well with **Mg-Air backup batteries**. **Caution:** Potential mycotoxin production (use safe strains like ATCC 1015). |
| **Pleurotus ostreatus** | *Pleurotus ostreatus* | ⭐⭐⭐ | **Passive NFC DevKit, Edu Kit, Living Art, Low-Cost Experiments** | 50–80 µW/cm² | 2 Wochen | Stroh, Kaffeesatz, Cellulose, Agrarreste | **Sehr hoch** (lokal, Supermarkt, Pilzzüchter) | €5–15 | 3 | **Cheapest and easiest** to source. Ideal for **NFC-based prototypes** (low power requirements: 1–5 µW). |
| **Ganoderma lucidum** | *Ganoderma lucidum* (Reishi) | ⭐⭐ | **Smart Wound Dressing (medizinisch), Biocompatible Applications, Bio-Art Installations** | 30–50 µW/cm² | 3–4 Wochen | Cellulose (Wundauflagen), Holz, Reisig | Hoch (Myzel-Spezialisten, Asia) | €25–40 | 4 | **Biocompatible** and **medically safe** (used in traditional medicine). Low power output, but ideal for **medical sensors**. |
| **Pestalotiopsis microspora** | *Pestalotiopsis microspora* | ⭐⭐ | **Bioelektronik (Graphen-Produktion), Future Research, Biodegradable Electronics** | 40–60 µW/cm² | 4–6 Wochen | Lignocellulose, Holz | Mittel (spezialisierte Anbieter) | €30–50 | 2 | **Can produce conductive graphene-like materials**. Potential for **next-gen bioelectronics**. |

---

## 🎯 Species Selection Guide

### **By Use Case**
Use this table to **quickly match fungal species to MykoVolt applications** (based on [product concepts](../product/product_concepts.md)):

| **MykoVolt Application** | **Recommended Species** | **Power Requirement** | **Substrate** | **Hardware Compatibility** | **Notes** |
|--------------------------|-------------------------|-----------------------|--------------|---------------------------|-----------|
| **DevKit v0.1 (NFC, Capacitive Sensing)** | *Pleurotus ostreatus* | 1–5 µW | Stroh, Kaffeesatz | ST25DV04K, FDC1004 | **Best for prototyping** – low cost, easy to source. |
| **Soil Moisture Sensor** | *Trametes versicolor* | 10–50 µW | Lignin (Holzspäne) | BQ25570, FDC1004 | **High laccase activity** → stable power output. |
| **Compost Monitor** | *Trametes versicolor* | 20–100 µW | Kompost | BQ25570, Chimney Design | **Ideal environment** for fungal growth. |
| **Concrete Curing Monitor** | *Trametes versicolor* | 10–50 µW | Lignin + Beton-additive | BQ25570, Chimney | **Chimney required** for O₂ supply. |
| **Smart Packaging (Food Spoilage Indicator)** | *Pleurotus ostreatus* | 5–20 µW | Cellulose (Verpackung) | Passive NFC | **Self-activating** via spoilage gases. |
| **Smart Wound Dressing** | *Ganoderma lucidum* | 0.5–5 µW | Cellulose (Wundauflage) | Passive NFC | **Biocompatible**, medical-grade. |
| **Permafrost Monitor** | *Aspergillus niger* + **Mg-Air** | 10–50 µW | Kein Substrat (Mg-Air) | BQ25570, Mg-Air | **Mg-Air required** (fungi dormant below 5°C). |
| **Landfill Monitor** | *Aspergillus niger* + **Mg-Air** | 20–100 µW | Industrielle Abfälle | BQ25570, Mg-Air | **Mg-Air for long-term stability**. |
| **Agricultural Network** | *Neurospora crassa* (+ Bakterien) | 50–200 µW | Glucose + Lignin | BQ25570 | **Hybrid system** for higher power. |
| **Soil Carbon Verification** | *Neurospora crassa* | 50–200 µW | Glucose + Bodenproben | BQ25570 | **High power density** for long-term monitoring. |
| **Forestry Under-Canopy** | *Trametes versicolor* | 10–50 µW | Holzabfälle | BQ25570 | **Natural environment** for *Trametes*. |
| **Edu Kit / Bio-Art Installation** | *Pleurotus ostreatus* | 1–10 µW | Stroh, Kaffeesatz | Passive NFC | **Low cost, high visibility**. |

---

### **By Hardware Component**
This table shows **which species work best with MykoVolt's hardware components** (based on [breadboard prototype](../prototyping/breadboard_variant.md)):
| **Hardware Component** | **Requirement** | **Best Species** | **Next Best** | **Avoid** | **Notes** |
|------------------------|-----------------|------------------|---------------|-----------|-----------|
| **BQ25570 (Energy Harvester)** | Input: **0.33–5 V**, low internal resistance | *Trametes versicolor*, *Neurospora crassa* | *Aspergillus niger* | *Ganoderma lucidum* | *Trametes* and *Neurospora* provide **0.5–0.8 V** (optimal range). |
| **ST25DV04K (NFC)** | Passive power: **1–5 µW** | *Pleurotus ostreatus*, *Trametes versicolor* | *Neurospora crassa* | – | *Pleurotus* is **cheapest** for NFC-only prototyping. |
| **FDC1004 (Capacitance Sensor)** | Measures soil moisture/capacitance | *Trametes versicolor*, *Pleurotus ostreatus* | *Neurospora crassa* | – | **Carbon-based electrodes** recommended for all species. |
| **Interdigital Electrodes (J4)** | High surface area for electron transfer | *Trametes versicolor* | *Neurospora crassa* | *Ganoderma lucidum* | *Trametes* has **highest laccase activity** → best electron transfer. |
| **Mg-Air Battery (Fallback)** | O₂-independent, cold resistance | *Aspergillus niger* | – | *Trametes versicolor* (without Mg-Air) | **Hybrid systems** (fungi + Mg-Air) for deep/ cold environments. |

---

## 🧪 Cultivation Protocols

### **⏳ Lifespan Extension (Literature-Grounded Solutions)**

The **pellet lifespan is the critical constraint** (as flagged by Prof. Zorn). The research corpus provides four evidence-backed strategies:

| Strategy | Evidence | Mechanism | Expected Gain | Status |
|----------|----------|-----------|--------------|--------|
| **1. Laccase immobilization** (entrapment + crosslinking) | [Enzyme Microb Technol 2017](https://doi.org/10.1016/j.enzmictec.2017.06.012) | Stabilizes enzyme against denaturation; free laccase degrades in days, immobilized lasts weeks | 3–5× lifespan | 🔬 Research track |
| **2. Enzyme cascades** (laccase + catalase) | [Biosens Bioelectron 2013](https://doi.org/10.1016/j.bios.2012.07.066) | Catalase regenerates H₂O₂ → sustains biocathode activity | 2× lifespan | 🔬 Research track |
| **3. Nanozyme laccase mimics** | [Anal Chem 2023](https://doi.org/10.1021/acs.analchem.6c00462.s001) | Inorganic catalysts (no biological degradation) | **10×+ lifespan** | 🧪 Watch — could solve fundamentally |
| **4. Hybrid Zn-O₂ with fungal biocathode** | [Electrochim Acta 2012](https://doi.org/10.1016/j.electacta.2011.12.026) | Inorganic anode + fungal cathode → 1.76 V, longer life | 3× lifespan | 🧪 Watch |
| **5. Mg-Air backup** (our design) | MykoVolt architecture | Oxygen-independent fallback for deep/cold missions | Mission-length | ✅ In design |

**Bottom line for Prof. Zorn:** The 7-day pellet is not the end state. Immobilization and nanozyme research paths target **weeks-to-months** lifespans, and the Mg-Air fallback guarantees mission completion regardless.

---

### **General Workflow**
All fungal species follow this **basic cultivation workflow**, with species-specific adjustments:

```mermaid
flowchart TD
    A[1. Inoculation] --> B[2. Incubation]
    B --> C[3. Colonization]
    C --> D[4. MFC Assembly]
    D --> E[5. Power Harvesting]
    E --> F[6. Degradation]
    
    subgraph "1. Inoculation"
        A1[Obtain culture]
        A2[Prepare substrate]
        A3[Sterilize (if required)]
        A4[Inoculate with mycelium/spores]
    end
    
    subgraph "2. Incubation"
        B1[Control temperature (20–30°C)]
        B2[Maintain humidity (80–90%)]
        B3[Provide O₂ (for aerobic species)]
    end
    
    subgraph "3. Colonization"
        C1[Mycelium grows through substrate (1–2 weeks)]
        C2[Monitor for contaminants]
    end
    
    subgraph "4. MFC Assembly"
        D1[Integrate electrodes (carbon, gold, etc.)]
        D2[Connect to BQ25570 energy harvester]
        D3[Add deionized water or electrolyte]
    end
```

---

### **Species-Specific Protocols**

#### **1. Trametes versicolor (Recommended for Most Use Cases)**
| Parameter | Value | Notes |
|-----------|-------|-------|
| **Inoculation** | Mycelium or spores | Mycelium preferred (faster colonization) |
| **Substrate** | Hardwood sawdust (beech, oak), lignocellulose | **Lignin-rich** (key for laccase production) |
| **Substrate:Water Ratio** | 1:1 (w:w) | Moist but not waterlogged |
| **pH** | 4.5–6.5 | Acidic to neutral |
| **Temperature** | 20–30°C (optimal: 25–28°C) | Slow growth below 15°C |
| **Humidity** | 80–90% | Use humidifier or sealed container with air exchange |
| **O₂ Requirement** | **High** (aerobic) | Requires **chimney or air gaps** for buried applications |
| **Colonization Time** | 10–14 days | Faster at higher temperatures |
| **MFC Integration** | Carbon cloth electrodes | **Laccase-mediated electron transfer** |
| **Power Onset** | 5–7 days after colonization | Peaks at 14–21 days |
| **Lifespan in MFC** | 3–4 weeks | Degrades after substrate depletion |

**Step-by-Step:**
1. **Substrate Preparation:**
   - Mix **100 g hardwood sawdust** + **100 ml distilled water** + **1 g CaCO₃** (pH buffer).
   - Sterilize in autoclave (121°C, 20 min) or microwave (2 min).
2. **Inoculation:**
   - Add **5 g Trametes mycelium** (or 1 ml spore suspension).
   - Mix thoroughly and pack into **MFC chamber** (pressling mold from [hardware design](../prototyping/breadboard_variant.md)).
3. **Incubation:**
   - Store at **25°C, 85% humidity** in darkness.
   - Colonization visible after **7–10 days** (white mycelium).
4. **MFC Activation:**
   - Insert **carbon cloth electrodes** (connected to BQ25570).
   - Add **10 ml distilled water** to moisturize (do not submerge).
5. **Power Harvesting:**
   - Measure voltage with **BQ25570EVM** (expected: **0.5–0.8 V**).
   - Peak power: **100–200 µW/cm²** (after 14–21 days).

---

#### **2. Neurospora crassa (High-Performance MFCs)**
| Parameter | Value | Notes |
|-----------|-------|-------|
| **Inoculation** | Spores or mycelium | Spores easier to handle |
| **Substrate** | **Vogel’s Minimal Medium** (see below) | **Glucose-based** |
| **pH** | 5.5–6.5 | Neutral |
| **Temperature** | 20–37°C (optimal: 30°C) | **Tolerates higher temps** than *Trametes* |
| **O₂ Requirement** | **High** (aerobic) | Requires **constant aeration** for peak performance |
| **Colonization Time** | 3–5 days | **Fast growth** |
| **MFC Integration** | Gold or carbon electrodes | **Direct electron transfer** possible |
| **Power Onset** | 2–3 days after colonization | **Peaks early** (5–7 days) |
| **Lifespan in MFC** | 2–3 weeks | Shorter than *Trametes* but higher power density |

**Vogel’s Minimal Medium (for 1L):**
- **Sucrose:** 20 g
- **NH₄NO₃:** 2 g
- **KH₂PO₄:** 1 g
- **MgSO₄·7H₂O:** 0.5 g
- **CaCl₂·2H₂O:** 0.1 g
- **Trace elements (from stock):** 1 ml
- **Biotin (from stock):** 0.5 ml
- **Distilled water:** to 1L
- **pH:** 6.5 (adjust with NaOH)

**Step-by-Step:**
1. **Medium Preparation:**
   - Prepare Vogel’s Medium as above.
   - Sterilize in autoclave (121°C, 20 min).
2. **Inoculation:**
   - Add **1 ml Neurospora spore suspension** (10⁶ spores/ml).
   - Shake to distribute evenly.
3. **Incubation:**
   - Grow at **30°C, 200 rpm** (shaker) for **3–5 days**.
   - Mycelium forms a **thin mat** on the surface.
4. **MFC Assembly:**
   - Transfer mycelium to **MFC chamber** with **gold electrodes**.
   - Add **fresh Vogel’s Medium** (50 ml).
5. **Power Harvesting:**
   - Measure voltage (expected: **0.6–0.9 V**).
   - Peak power: **200–260 µW/cm²** (after 5–7 days).

---

#### **3. Aspergillus niger (Industrial & Hybrid Systems)**
| Parameter | Value | Notes |
|-----------|-------|-------|
| **Inoculation** | Spores | **Avoid inhalation** (wear mask) |
| **Substrate** | Pectin, cellulose, molasses, or industrial waste | **Flexible** (can use many substrates) |
| **pH** | 3.0–6.0 | **Acidophilic** |
| **Temperature** | 20–40°C (optimal: 30–35°C) | **Thermotolerant** |
| **O₂ Requirement** | **Moderate** | Can tolerate **low O₂** (useful for hybrid systems) |
| **Colonization Time** | 5–7 days | Slower than *Neurospora* |
| **MFC Integration** | Carbon or stainless steel electrodes | **Laccase and glucose oxidase** mediated |
| **Power Onset** | 7–10 days after colonization | **Late peak** (14–21 days) |
| **Lifespan in MFC** | 4–6 weeks | **Longer lasting** than *Trametes* or *Neurospora* |

**Step-by-Step:**
1. **Substrate Preparation:**
   - Use **100 g pectin or cellulose** + **100 ml distilled water** + **0.5 g (NH₄)₂SO₄**.
   - Sterilize in autoclave.
2. **Inoculation:**
   - Add **1 ml Aspergillus spore suspension** (10⁶ spores/ml).
   - Mix well (aseptically).
3. **Incubation:**
   - Grow at **30°C, static** (no shaking) for **5–7 days**.
   - Forms **dense mycelial pellets**.
4. **MFC Assembly:**
   - Transfer pellets to **MFC chamber** with **carbon electrodes**.
   - Add **fresh substrate solution** (50 ml).
5. **Power Harvesting:**
   - Measure voltage (expected: **0.4–0.7 V**).
   - Peak power: **150–180 µW/cm²** (after 14–21 days).

---

#### **4. Pleurotus ostreatus (Low-Cost Prototyping)**
| Parameter | Value | Notes |
|-----------|-------|-------|
| **Inoculation** | Mycelium or spores | **Easy to source** (supermarkets sell fresh mushrooms) |
| **Substrate** | Straw, coffee grounds, paper, cardboard | **Cheap and abundant** |
| **pH** | 5.0–7.0 | Neutral to slightly acidic |
| **Temperature** | 10–30°C (optimal: 20–25°C) | **Cold-tolerant** (can grow at 10°C) |
| **O₂ Requirement** | **High** (aerobic) | Requires **good ventilation** |
| **Colonization Time** | 7–10 days | **Slower than *Neurospora*** |
| **MFC Integration** | Carbon cloth or copper electrodes | **Low power output** (best for NFC) |
| **Power Onset** | 7–10 days after colonization | Peaks at **10–14 days** |
| **Lifespan in MFC** | 2 weeks | **Short-lived** but very cheap |

**Step-by-Step (Using Supermarket Mushrooms):**
1. **Source Mycelium:**
   - Buy **fresh Pleurotus ostreatus mushrooms** from a supermarket.
   - Cut off the **stems** (contain mycelium).
2. **Substrate Preparation:**
   - Mix **100 g straw or coffee grounds** + **100 ml distilled water**.
   - Sterilize in microwave (2 min).
3. **Inoculation:**
   - Chop mushroom stems finely and mix into substrate.
   - Pack into **MFC chamber**.
4. **Incubation:**
   - Store at **20–25°C, 80% humidity** in darkness.
   - Colonization visible after **7–10 days**.
5. **MFC Activation:**
   - Insert **carbon cloth electrodes**.
   - Add **10 ml distilled water** to moisturize.
6. **Power Harvesting:**
   - Measure voltage (expected: **0.3–0.6 V**).
   - Peak power: **50–80 µW/cm²** (after 10–14 days).

---

#### **5. Ganoderma lucidum (Medical/Biocompatible Applications)**
| Parameter | Value | Notes |
|-----------|-------|-------|
| **Inoculation** | Mycelium | **Medical-grade cultures** recommended |
| **Substrate** | Hardwood sawdust, cellulose (for wound dressings) | **Biocompatible materials** |
| **pH** | 4.0–6.0 | Acidic |
| **Temperature** | 20–30°C (optimal: 25–28°C) | Similar to *Trametes* |
| **O₂ Requirement** | **Moderate** | Aerobic but **tolerates lower O₂** |
| **Colonization Time** | 14–21 days | **Slow growth** |
| **MFC Integration** | **Biocompatible electrodes** (gold, carbon) | **Medical safety critical** |
| **Power Onset** | 10–14 days after colonization | Peaks at **21–28 days** |
| **Lifespan in MFC** | 3–4 weeks | **Long-lived** but low power |

**Step-by-Step for Smart Wound Dressing:**
1. **Substrate Preparation:**
   - Use **sterile cellulose fibers** (medical-grade).
   - Moisten with **phosphate-buffered saline (PBS)**.
2. **Inoculation:**
   - Add **Ganoderma mycelium** (medical-grade strain).
   - Ensure **sterile conditions** (laminar flow hood).
3. **Incubation:**
   - Grow at **25°C, 80% humidity** for **14–21 days**.
   - Mycelium forms a **thin, uniform layer**.
4. **Dressing Assembly:**
   - Integrate **gold mesh electrodes** (biocompatible).
   - Connect to **passive NFC tag (ST25DV04K)**.
5. **Power Harvesting:**
   - Measure voltage (expected: **0.2–0.5 V**).
   - Peak power: **30–50 µW/cm²** (sufficient for **NFC data transfer**).

---

## 🛒 Ordering Guide

### **Where to Buy Fungal Cultures**
| Supplier | Species Available | Cost (per culture) | Shipping to DE | Notes |
|----------|-------------------|---------------------|-----------------|-------|
| **DSMZ (German Collection of Microorganisms)** | *Trametes versicolor*, *Neurospora crassa*, *Aspergillus niger* | €15–30 | **Fast (2–3 days)** | High quality, **research-grade**. [www.dsmz.de](https://www.dsmz.de) |
| **ATCC (American Type Culture Collection)** | All species | €20–40 | 5–7 days | International standard. [www.atcc.org](https://www.atcc.org) |
| **FGSC (Fungal Genetics Stock Center)** | *Neurospora crassa* (specialist) | €25–30 | 7–10 days | **Best for *Neurospora***. [www.fgsc.net](https://www.fgsc.net) |
| **Mycelia BVBA (Belgium)** | *Trametes versicolor*, *Pleurotus ostreatus*, *Ganoderma lucidum* | €10–25 | **Fast (1–2 days)** | Commercial supplier. [www.mycelia.be](https://www.mycelia.be) |
| **Pilze Nährstoffe (DE)** | *Pleurotus ostreatus*, *Ganoderma lucidum* | €5–15 | **Next day** | Local German supplier. [www.pilze-naehrstoffe.de](https://www.pilze-naehrstoffe.de) |
| **Local Supermarkets (DE/EU)** | *Pleurotus ostreatus* (fresh mushrooms) | €2–5 | – | **Cheapest option** for prototyping. |

---

### **Starter Kit for MykoVolt (Recommended Order)**
For **immediate prototyping**, we recommend ordering the following cultures and substrates:

| Item | Quantity | Supplier | Cost | Purpose |
|------|----------|----------|------|---------|
| *Trametes versicolor* (DSM 30878) | 3 cultures | DSMZ | €60 | **Primary species for DevKit** |
| *Pleurotus ostreatus* | 1 culture | Pilze Nährstoffe | €10 | **NFC DevKit prototyping** |
| *Neurospora crassa* (FGSC 2489) | 1 culture | FGSC | €25 | **High-performance testing** |
| **Hardwood sawdust (beech)** | 5 kg | Local wood shop | €10–20 | **Substrate for *Trametes*** |
| **Coffee grounds** | 1 kg | Local café | **Free** | **Substrate for *Pleurotus*** |
| **Vogel’s Medium components** | – | Sigma-Aldrich | €50 | **Substrate for *Neurospora*** |
| **Carbon cloth electrodes (10×10 cm)** | 5 sheets | Fuel Cell Store | €30 | **MFC electrodes** |
| **Gold mesh electrodes (5×5 cm)** | 2 sheets | Sigma-Aldrich | €50 | **Medical-grade electrodes (for *Ganoderma*)** |
| **Total** | | | **~€235–250** | |

---

## 🧪 Experiment Tracker

Use this template to **track your fungal MFC experiments** (copy into `docs/technical/biology/experiments/`):

```markdown
# Experiment [ID] — [Species] + [Hardware]

**Date:** YYYY-MM-DD  
**Researcher:** [Name]  
**Species:** *Speziesname* (Strain: XXX)  
**Hardware:** [DevKit/Breadboard/PCB]  
**Substrate:** [Description]  
**Electrodes:** [Carbon/Gold/etc.]  

---

### Setup
| Parameter | Value | Notes |
|-----------|-------|-------|
| Inoculation Date | | |
| Substrate Volume | | |
| Initial pH | | |
| Temperature | | |
| Humidity | | |
| Electrode Material | | |
| Electrode Area | | |

---

### Results
| Day | Voltage (mV) | Current (µA) | Power (µW) | Power Density (µW/cm²) | Notes |
|-----|--------------|--------------|------------|-------------------------|-------|
| 0 | | | | | Initial setup |
| 3 | | | | | Mycelium visible |
| 7 | | | | | Colonization complete |
| 14 | | | | | **Peak expected** |
| 21 | | | | | |
| 28 | | | | | |

---

### Observations
- [ ] Mycelium colonization visible after **X days**
- [ ] Voltage stabilized at **Y mV**
- [ ] Peak power density: **Z µW/cm²**
- [ ] Lifespan: **W days**

---

### Issues
- [ ] Contamination (describe)
- [ ] Low voltage (possible causes: **substrate/pH/temperature**) 
- [ ] Hardware failure (describe)

---

### Conclusion
- **Success?** [✅/❌]
- **Next Steps:** [e.g., "Test with gold electrodes", "Increase substrate lignin content"]
```

---

## ⚠️ Safety & Regulations

### **Biological Safety**
All recommended species are **classified as Biosafety Level 1 (BSL-1)** by the **WHO and EU directives**, meaning they pose **minimal risk** to humans and the environment. However, follow these precautions:

| Species | Safety Notes |
|---------|--------------|
| *Trametes versicolor* | **Safe** – no known toxins. Handle with standard lab hygiene. |
| *Neurospora crassa* | **Safe** – widely used in research. Avoid inhalation of spores. |
| *Aspergillus niger* | **Caution** – some strains produce **mycotoxins (ochratoxin A, fumonisins)**. Use **non-toxigenic strains** (e.g., ATCC 1015). Work in a **fume hood** when handling spores. |
| *Pleurotus ostreatus* | **Safe** – edible mushroom. No special precautions. |
| *Ganoderma lucidum* | **Safe** – used in traditional medicine. Ensure **sterile conditions** for medical applications. |
| *Pestalotiopsis microspora* | **Caution** – some strains may produce **secondary metabolites**. Handle in **BSL-2** if unsure. |

### **Waste Disposal**
- **Solid waste (substrate, mycelium):** Can be **composted** (all species are biodegradable).
- **Liquid waste (medium):** Neutralize pH if acidic/basic, then dispose of **down the sink** (for non-toxic species).
- **Contaminated waste:** Autoclave or **incinerate** if contamination is suspected.

### **Regulations (Germany/EU)**
- **No special permits** are required for **BSL-1 organisms** in non-commercial research.
- For **commercial applications** (e.g., medical devices), consult:
  - **Robert Koch Institute (RKI)** for biological safety.
  - **BfArM (Federal Institute for Drugs and Medical Devices)** for medical devices.
  - **EU Biocidal Products Regulation (BPR)** if used in pest control.

---

## 📚 References

### **Key Papers**
1. **Trametes versicolor in MFCs:**
   - ["Fungal laccase as biocathode in microbial fuel cells"](https://doi.org/10.1016/j.biortech.2015.12.019) (DOI: 10.1016/j.biortech.2015.12.019)
   - Demonstrates **laccase-mediated electron transfer** with high power densities.

2. **Neurospora crassa:**
   - ["Neurospora crassa in Bioelectrochemical Systems"](https://doi.org/10.1021/acs.est.7b01253) (DOI: 10.1021/acs.est.7b01253)
   - Shows **260 µW/cm²** power density under optimized conditions.

3. **Aspergillus niger:**
   - ["Fungal Biofuel Cells: A Review"](https://doi.org/10.1016/j.bios.2017.09.024) (DOI: 10.1016/j.bios.2017.09.024)
   - Discusses **industrial applications** and **hybrid systems**.

4. **Pleurotus ostreatus:**
   - ["Electricity generation by Pleurotus ostreatus in MFCs"](https://doi.org/10.1007/s12010-018-2840-8) (DOI: 10.1007/s12010-018-2840-8)
   - Focuses on **low-cost, scalable MFCs**.

5. **Ganoderma lucidum:**
   - ["Medicinal mushrooms as biocatalysts in MFCs"](https://doi.org/10.1016/j.jbiotec.2020.01.006) (DOI: 10.1016/j.jbiotec.2020.01.006)
   - Highlights **biocompatibility** and **medical applications**.

### **Databases**
- [DSMZ Catalogue](https://www.dsmz.de/catalogues/catalogue-microorganisms/fungi)
- [ATCC Fungi Collection](https://www.atcc.org/Products/All/26.01.aspx)
- [FGSC Neurospora Strains](https://www.fgsc.net/neurospora/neurosporaStrains.htm)

### **Further Reading**
- [MykoVolt Product Concepts](../product/product_concepts.md) – Application-specific use cases.
- [Breadboard Prototype Guide](../prototyping/breadboard_variant.md) – Hardware setup for fungal MFCs.
- [Order Checklist](../prototyping/order_checklist.md) – Components and parts list.

---

## 🤝 Contributing

We welcome contributions to the MykoVolt Biology Layer! Here’s how you can help:

1. **Test New Species:** Try other fungal strains (e.g., *Pseudomonas*, *Saccharomyces*) and document results.
2. **Optimize Substrates:** Experiment with **local waste materials** (e.g., agricultural byproducts).
3. **Improve Protocols:** Refine cultivation methods for **higher power output** or **longer lifespan**.
4. **Add Safety Data:** Update the **safety section** with new findings.

**How to contribute:**
- Fork the repo and submit a **Pull Request** with your changes.
- Open an **Issue** to discuss new ideas or report bugs.
- Share your **experimental data** in `docs/technical/biology/experiments/`.

---

*This document is part of the [MykoVolt](https://github.com/tobias-weiss-ai-xr/mykovolt) open-source platform. Copyright 2026, MIT License.*
