# Customer Segment Strategy — MykoVolt

> **Status**: Draft v1 | **TRL**: 2 (technology concept formulated) | **Stage**: Pre-seed / solo founder
> **Core product**: Biodegradable fungal bio-battery DevKit with NFC readout, ~€25–35/unit

---

## 1. Strategic Context

MykoVolt is developing the first biodegradable fungal battery evaluation platform. At TRL 2, no working hardware exists yet — the strategy below is therefore a **research and outreach roadmap**, not a sales plan. It identifies the earliest possible customers, the channels to reach them, and the milestones that unlock each subsequent segment.

The fundamental challenge: **biodegradable electronics is a solution in search of a market**. The technology's strongest selling point (it composts) is irrelevant or even undesirable in most commercial settings. The strategy must therefore:

1. Find **research customers who pay for novelty** — labs that want to study, characterise, or publish on fungal MFCs.
2. Build **credibility through co-authored publications** before attempting any commercial sale.
3. Navigate the **innovation diffusion gap** between lab curiosity and field deployment.

---

## 2. Phase 1: Research Laboratory DevKit (2026–2028)

### 2.1 Segment Definition

Primary customers are academic and institutional research groups working on:

- Microbial fuel cells (MFCs) and bio-electrochemical systems (BES)
- Living materials, biodegradable electronics, fungal biotechnology
- Environmental sensing, soil microbial ecology, plant-microbe interactions

These groups have **grant-funded consumables budgets**, a **publication imperative**, and tolerance for experimental hardware that commercial buyers lack.

### 2.2 Target Institutions (Specific Groups)

| Institution | Group / Lab | Relevance |
|---|---|---|
| **Empa** (Switzerland) | Cellulose & Wood Materials / Biofuels | Active fungal MFC research; published on fungal electricity generation |
| **JKU Linz** (Austria) | Institute of Polymer Chemistry | Printed biodegradable electronics; potential integration partner |
| **TU Delft** (Netherlands) | Dept. of Biotechnology | Long history in MFC reactor design; microbial electrochemistry |
| **Fraunhofer IZM** (Germany) | Environmental & Reliability Engineering | Biodegradable PCB and sensor research |
| **University of Cambridge** | Dept. of Plant Sciences / MFC groups | Multiple PI's active in soil MFC and plant-MFC area |
| **Wageningen University** (Netherlands) | Bioprocess Engineering / Soil Biology | Strong ag-tech angle; soil microbial ecology |
| **University of Marburg** (Germany) | Fungal Biotechnology / Dept. of Biology | Dedicated fungal biology groups |
| **UC Berkeley** | Joint BioEnergy Institute (JBEI) / Synthetic Biology | Bio-energy and synthetic biology crossover |

**Outreach priority**: Contact group leaders 6–8 weeks before major conferences (see §6) with a pre-print or technical note, not a sales deck.

### 2.3 Value Proposition for Research Labs

> A reproducible, documented, open-hardware fungal battery platform — so you spend your grant on experiments, not on re-building someone's ambiguous prototype from a methods section.

| Lab Pain Point | MykoVolt Response |
|---|---|
| "I can't reproduce published fungal MFC results because the setup is never described in enough detail" | Standardised DevKit with documented assembly, materials list, and test protocol |
| "I need a baseline platform to test my own electrode materials / fungi strains / circuit designs" | Open-hardware PCB with exposed test points; firmware source available |
| "Paper reviewers ask for power density comparisons but every lab measures differently" | NFC readout with standardised logging format; enables cross-lab comparison |
| "Setting up electrochemical measurements from scratch takes months" | Pre-assembled NFC readout; connect electrodes, start logging in 15 minutes |

### 2.4 Pricing

| Item | Price (€) | Notes |
|---|---|---|
| MykoVolt DevKit (single unit) | 35 | PCB, NFC tag, electrode set, starter culture, assembly guide |
| Electrode refill pack (5x) | 10 | Consumable — the fungal substrate is consumed |
| NFC reader (if needed) | 25 | Off-the-shelf NFC phone app may suffice for most |
| Bulk lab pack (10 units) | 250 | 10 × DevKit, 10 × refills, shared reader |

**Rationale**: At ~€35/unit this is competitive with a single electrochemical cell (e.g. CH Instruments electrode ~€50–100) and far cheaper than a potentiostat (€2k–15k). It is priced as a **consumable research tool**, not capital equipment.

### 2.5 Expected Order Volume (Year 1)

| Scenario | Units | Revenue (€) | Trigger |
|---|---|---|---|
| Pessimistic | 15–25 | 525–875 | 3–5 labs buy a single unit to evaluate |
| Moderate | 40–60 | 1,400–2,100 | Conference demo leads to 8–12 lab trial orders |
| Optimistic | 80–120 | 2,800–4,200 | Published paper drives follow-on orders; some bulk lab packs |

**Year 1–2 total revenue**: hundreds to low thousands of euros, not millions. This is a **relationship-building phase**, not a revenue phase.

---

## 3. Phase 1b: University Teaching Labs (2028–2030)

### 3.1 Segment

Teaching laboratories in:

- **Bioelectronics / bioengineering courses** — students build and measure bio-electrochemical systems
- **Embedded systems labs** — NFC readout firmware exercises, I²C/SPI sensor interfacing
- **Environmental science / microbiology practicals** — hands-on demonstration of microbial energy conversion
- **DIY biology / synthetic biology workshops** — accessible living-tech demonstration

### 3.2 Value Proposition

> Replace an abstract lecture slide on "microbial fuel cells" with a 90-minute practical where every student pairs measure a real fungal battery — for less than the cost of a textbook.

### 3.3 Pricing (Educational)

| Item | Price (€) | Condition |
|---|---|---|
| Teaching lab pack (30 units) | 600 | Lab manual + lecture slides included |
| Repeat order (per year) | 500 | Recurring consumable replenishment |
| Single unit (faculty demo) | 30 | For instructor evaluation |

**Channel**: Direct outreach to course directors at target institutions. Leverage conference contacts from Phase 1 to get introductions.

### 3.4 Constraints

- Teaching lab adoption requires a **curriculum integration window** — most courses plan 6–18 months ahead.
- Labs need **pre-validated protocols** that reliably work in a 90–180 minute session.
- Liability / safety documentation required for undergraduate use (MSDS for fungal cultures, electrode handling).

---

## 4. Phase 2 (Year 3–5): Ag-Tech Early Adopters (Beta / Field Trial)

### 4.1 Segment: Research Farms and Test Stations

Not commercial farms. The target for Phase 2 is:

- **University agricultural research stations** (e.g. Wageningen UR experimental farm, ETH Agroscope)
- **Government agricultural test centres** (e.g. Julius Kühn Institute, USDA ARS)
- **Ag-tech incubator cohorts** (e.g. StartLife, AgTech NEXT, EIT Food RisingFoodStars)
- **Precision agriculture R&D teams** within large agribusiness (e.g. John Deere Labs, Syngenta R&D, Yara Crop Nutrition)

These organisations **already run field trials** on experimental sensors and are accustomed to high-failure-rate prototypes. They need **data, not product reliability** — exactly what a TRL 4–5 system can provide.

### 4.2 Value Proposition

> A self-powered soil sensor that needs no battery replacement and composts at end of life — for field trials comparing biodegradable vs. conventional IoT in real growing conditions.

### 4.3 Beta Program Structure

- 10–20 units deployed across 3–5 test sites
- Co-designed data format with partner agronomists
- Monthly data reviews; quarterly site visits
- Participants receive **co-authorship on field trial publications** and **first access to production units**
- **No payment required** in beta phase — participants cover only shipping and installation

### 4.4 Expected Outcomes

| Metric | Target |
|---|---|
| Field trial sites | 3–5 by end of Year 3 |
| Units deployed | 10–20 |
| Data collection hours | >5,000 per site |
| Co-authored publications | 1–2 in agronomy / sensor journals |
| Conversion to paid orders | 50–70% of beta participants |

---

## 5. Phase 3 (2030+): Agricultural Market

### 5.1 Why Not Earlier

The agricultural market for MykoVolt technology is **not addressable before 2030** for several structural reasons:

1. **Reliability requirements**: A commercial farmer needs 99%+ uptime across a growing season (4–9 months). A biodegradable device that starts degrading on contact with soil cannot yet guarantee this.
2. **Cost parity**: At scale, a passive RFID tag costs €0.05–0.50. Even at bulk production, a fungal MFC sensor will cost €2–10 per unit at minimum — a 10–200× premium with no proven lifetime advantage.
3. **Certification**: Agricultural sensors sold into the EU require CE marking under the Radio Equipment Directive (RED) and likely RoHS compliance. Biodegradable electronics currently struggle with RoHS because the biodegradable substrate materials themselves contain substances not listed in the exemption annexes.
4. **Conservative buyer**: Agriculture is a thin-margin, risk-averse industry. A farmer will not replace a known €0.50 CR2032-powered soil sensor with a €8 biodegradable one unless the biodegradable one demonstrably outlasts or outperforms it.
5. **Sales infrastructure**: Selling to farms requires on-the-ground channel partners (ag-dealers, irrigation suppliers, co-ops) — a distribution network that a solo founder cannot build while still validating the technology.

**Phase 3 is aspirational, not actionable.** The strategy document will be revised when MykoVolt reaches TRL 5–6 and has at least 2 years of field trial data.

### 5.2 What Must Happen Before Phase 3

- [ ] >20,000 cumulative field-hours of operation across multiple soil types and climates
- [ ] CE (RED) and RoHS certification achieved
- [ ] Unit cost at batch-1000 scale demonstrated below €5
- [ ] At least 3 independent field trials published in peer-reviewed agronomy journals
- [ ] Distribution agreement with an agricultural channel partner
- [ ] At least 1 FTE dedicated to sales and support (cannot be solo founder)

---

## 6. Conference & Outreach Strategy

### 6.1 Primary Conferences

| Conference | Focus | Why MykoVolt Should Attend | Timing |
|---|---|---|---|
| **ISMET** (International Society for Microbial Electrochemistry and Technology) | MFCs, BES, electroactive biofilms | Core technical audience; where MFC researchers present | Annual, Sept–Oct |
| **E-MRS** (European Materials Research Society) Fall Meeting | Advanced materials, biodegradable electronics | Materials science angle; biodegradable substrate research | Annual, Sept |
| **Agritechnica** (Hanover) | Agricultural technology | Only relevant in Phase 2–3; attend as visitor first, exhibitor later | Biennial, Nov |

### 6.2 Secondary / Emerging

| Conference | Relevance |
|---|---|
| **Living Materials Summit** (Wyss Institute / Empa) | Fungal materials + living electronics — directly overlaps |
| **Open Hardware Summit** | Open-source community; potential early adopters |
| **Biopolymers / Bioplastics conferences** | Substrate material science community |
| **International Conference on Soil Sensors** | Ag-tech sensor community |

### 6.3 Conference Playbook

1. **Before**: Submit a poster or short talk abstract. Contact 5–8 target lab PIs. Offer a 1:1 demo.
2. **During**: Bring 3–5 working prototypes. Let people handle them. Collect email + research interest on a paper form (no CRM needed at this stage).
3. **After**: Follow up within 48 hours with a one-page technical note and an offer to send a free (your-lab-pays-shipping) DevKit.

---

## 7. Sales Funnel (Phase 1)

```
Conference poster / talk
        ↓
    1:1 demo at conference (or Zoom)
        ↓
    Send free-trial DevKit (lab pays ~€10 shipping)
        ↓
    Lab tests for 4–8 weeks → produces data
        ↓
    Offer co-authorship on methods paper
        ↓
    Paper submitted → credibility built
        ↓
    Repeat order (lab buys own DevKits)
        ↓
    Lab publishes using MykoVolt → drives inbound inquiries
```

**Funnel metrics (Phase 1)**:

| Stage | Conversion | Notes |
|---|---|---|
| Conference contacts → demo | ~30% | Depends on poster quality; <10 mins to convey value |
| Demo → trial DevKit sent | ~60% | Low friction — just shipping cost |
| Trial → repeat purchase | ~30–50% | Success depends on documentation quality and data output |
| Repeat → publication | ~20% | Only if platform is genuinely useful for their research |

**Time from first contact to first paid order**: 6–14 months.

---

## 8. Academic Paper Collaboration

This is MykoVolt's most important marketing channel in Phase 1.

### 8.1 Strategy

Rather than selling DevKits, **offer them as research enablers** in exchange for co-authorship. This:

- Produces **independently verified data** (gold for a TRL 2 company)
- Generates **citations and visibility** in the target community
- Gets the platform name into the **methods section** of published papers (the most durable form of advertising)
- Builds a **publication record** that de-risks the technology for future funders (EXIST, Horizon Europe, EIC Accelerator)

### 8.2 Paper Types MykoVolt Can Co-Author

| Paper type | Target Journal | Timeline |
|---|---|---|
| Methods paper: "A reproducible open-hardware platform for evaluating fungal bio-battery performance" | HardwareX, PLOS ONE, J. Open Hardware | Year 1 |
| Comparative study: power density across 5 fungal strains using standardised platform | Bioresource Technology, Biosensors & Bioelectronics | Year 1–2 |
| Degradation study: lifetime vs. power output in controlled soil columns | Sensors and Actuators B, ACS Sustainable Chemistry | Year 2 |
| Field deployment: fungal MFCs in living soil sensors | Computers and Electronics in Agriculture, Sensors | Year 3+ |

### 8.3 Constraints

- MykoVolt must **contribute meaningfully** to writing and analysis, not just provide hardware — journal policies on ghost authorship apply.
- Data must be **reproducible**; the open-hardware nature of the platform should be a strength here.
- IP: ensure paper publication does not preclude patent filing on novel aspects (discuss with patent attorney before submitting).

---

## 9. Grant Consortium Building as Lead Generation

### 9.1 EXIST (German BMWK)

The EXIST Forschungstransfer programme (€150k–1M over 18–24 months) requires an academic partner. The application itself is a **lead generation exercise** — identifying a professor who agrees to be the academic PI means that professor and their group are automatically a pilot user.

| EXIST Stream | Applicability |
|---|---|
| EXIST Business Start-up Grant | Solo founder living stipend + materials budget (€25–30k) |
| EXIST Transfer of Research | Requires university partner; funds prototype development + validation by partner lab |

### 9.2 Horizon Europe

| Cluster | Call Topic | Relevance |
|---|---|---|
| Cluster 6 (Food, Bioeconomy, Natural Resources) | Soil health and sensors | HORIZON-CL6-2024-ZEROPOLLUTION-01 |
| EIC Pathfinder | Bioelectronics / living materials | Open to TRL 1–3 |
| EIC Transition | From lab to field prototype | TRL 3–4, requires experimental validation |

### 9.3 Consortium Building Playbook

1. Identify lead coordinator for a Horizon Europe call (often a university research office or a dedicated SME)
2. Offer to contribute the **MykoVolt platform as the sensing hardware foundation** for a soil-health sensor consortium
3. Consortium partners become **beta testers and validators** — each partner's lab gets DevKits as in-kind contribution
4. If funded, the consortium pays MykoVolt a sub-contract fee for hardware + data support

This is not a revenue stream — it is a **subsidy for R&D** that also builds network effects and validation.

---

## 10. Open-Source Hardware Distribution

### 10.1 Rationale

MykoVolt at TRL 2 cannot afford a sales team, a Shopify store with paid ads, or a distributor network. The open-source hardware ecosystem provides a **zero-cost distribution channel** with a built-in audience that is eager for novel, unconventional tech.

### 10.2 Platforms

| Platform | Format | Why It Fits |
|---|---|---|
| **Hackaday.io** | Project logs + build documentation | Largest community for open hardware projects; 100k+ active users |
| **CrowdSupply** | Crowdfunding + pre-orders | Open-hardware focused (vs. Kickstarter); handles fulfilment for a fee |
| **Tindie** | Direct sales of open hardware | Low barrier to listing; makers and researchers shop here |
| **GitHub** | KiCad files + firmware source | Not a sales channel, but essential for credibility in this segment |

### 10.3 Open-Source Approach

| Component | License | Rationale |
|---|---|---|
| PCB design files (KiCad) | CERN-OHL-P v2 | Standard for open hardware; permissive variant chosen to allow commercial use |
| Firmware source (Rust / C) | MIT or Apache 2.0 | Standard for embedded OSS |
| 3D-printable enclosure | CC-BY-SA 4.0 | Encourage remixing for different electrode geometries |
| Electrode chemistry / culture protocol | CC-BY 4.0 | Must be reproducible; no trade secret in biology protocols |

### 10.4 Risks of Open Source

- **Clones**: Competitors (or hobbyists) could manufacture and sell identical units. Mitigation: the fungal culture protocol and electrode surface treatment are non-trivial; the value is in the consumable ecosystem, not the PCB.
- **Brand dilution**: "MykoVolt" becomes a generic term. Mitigation: trademark the name and logo early (€300–1k in the EU); license the trademark for authorised manufacture.
- **No direct sales control**: Difficult to capture customer data. Mitigation: GitHub repository + discord/slack community as the coordination point; every user has to visit the repo to get firmware.

---

## 11. Developer Ecosystem

### 11.1 Why Build One

Platforms win when the ecosystem around them is more valuable than the platform itself (Arduino, Raspberry Pi). For MykoVolt, a developer ecosystem means:

- Third-party electrode designs optimised for different fungi
- Alternative firmware with different data-logging patterns (LoRa, BLE, CAN bus)
- Data analysis scripts in Python/R for publication-ready figures
- Classroom lab manuals written by educators who use the platform

### 11.2 Components

| Layer | What MykoVolt Provides | What Community Provides |
|---|---|---|
| **Firmware** | Rust embedded HAL + reference implementation (NFC readout, ADC, power management) | Alternative firmware ports (Arduino, CircuitPython), extended feature set |
| **Data format** | JSON schema for MFC time-series data (voltage, current, temperature, timestamps) with versioning | Analysis tools, visualisation dashboards, integration with lab data pipelines |
| **Hardware** | KiCad reference design, BOM, assembly instructions | Variant boards (different MCUs, additional sensors, different form factors) |
| **Biology** | Culture protocol for 3 reference fungal species | Protocols for new species, growth media optimisations |
| **Documentation** | Getting-started guide, API docs | Translation, tutorial videos, course materials |

### 11.3 Community Engagement

- **Monthly open call**: "MykoVolt community hangout" — 30-minute video call, GitHub issues triage, showcase community builds
- **Best build award**: Free DevKit pack to the best community contribution each quarter
- **Hackathon collaboration**: Partner with iGEM (synthetic biology competition), Hackaday Prize, or mHUB (monthly)

---

## 12. The Innovation Diffusion Challenge

### 12.1 The Problem

Biodegradable electronics faces a structural adoption barrier:

| Adopter Category | % of Market | Typical Response to MykoVolt |
|---|---|---|
| **Innovators** | 2.5% | "This is fascinating — I want to study it, not use it." (The Phase 1 audience) |
| **Early adopters** | 13.5% | "Show me published data and someone else's field trial first." (Phase 2 audience) |
| **Early majority** | 34% | "Make it work for 2 years straight without attention and cost less than a CR2032." (Phase 3 — 2030+) |
| **Late majority / laggards** | 50% | Will not adopt until biodegradable is regulation-mandated. |

The gap between innovators and early adopters — **"the chasm"** in Geoffrey Moore's Crossing the Chasm — is especially wide for biodegradable technology because:

1. **No reference installations**: Every early adopter wants to see a successful deployment in an operationally similar setting. But the first deployments are necessarily in non-identical lab settings.
2. **Risk of disappearance**: If MykoVolt goes under, the field-trial partner has orphaned hardware with no consumables supply.
3. **Data reproducibility**: Biodegradable systems have higher variance (fungi are biological). Early adopters accustomed to silicon sensors have lower tolerance for variance.

### 12.2 Mitigation

- **Publish early and often** — peer-reviewed data is the only trust currency for risk-averse adopters.
- **Design for backward compatibility** — ensure future production DevKits can use the same electrodes and firmware. Promise a 3-year consumables compatibility window.
- **Over-document** — every variance point in the biological system must be documented so users understand whether signal drift is real (fungus is running out of substrate) or a measurement artifact.

---

## 13. Certification Roadmap

Certification is not needed for Phase 1 research lab sales — university labs self-certify under their own risk assessment procedures. It **is** required for Phase 2 (paid commercial sales to non-research entities) and Phase 3.

| Certification | Scope | Estimated Cost | Timeline | Trigger |
|---|---|---|---|---|
| **CE (RED)** | NFC radio emissions (EU) | €5k–15k | 3–6 months | First paid commercial sale outside research |
| **CE (EMC)** | Electromagnetic compatibility | €3k–8k | 2–4 months | As above |
| **RoHS** | Restriction of hazardous substances | €1k–3k | 1–2 months (documentation review) | As above — but **biodegradable materials may face compliance challenges** |
| **FCC** | US radio emissions | €8k–15k | 3–6 months | First US customer or US-based field trial |
| **UKCA** | Post-Brexit UK market | €2k–5k | 1–3 months | UK customer |
| **REACH** | Chemical safety (EU) | €5k–20k | 6–12 months | If device is shown to release substances into soil |

> **RoHS challenge**: Biodegradable substrate materials (e.g. cellulose acetate, chitosan, mycelium composites) are not listed in RoHS exemption annexes. A strict reading would require documenting the absence of lead, mercury, cadmium, hexavalent chromium, PBB, and PBDE down to ppm levels in a biological material — which is technically possible but costly. This is a known issue for the entire biodegradable electronics field.

**Phase 1 gating**: None needed. Phase 2 gating: CE (RED) for any NFC-based paid product. Phase 3 gating: full compliance suite.

---

## 14. Competitive Landscape (Honest)

### 14.1 Direct: Bactery AB

- **What they do**: Soil microbial fuel cell for in-situ soil sensing (temperature, moisture, nutrient proxies)
- **Stage**: TRL 6–7 (field trials ongoing since 2022)
- **Funding**: ~€4M raised (EIC Accelerator, private)
- **Differentiation vs. MykoVolt**: Bactery is **ahead** — they have a working field-deployable product. But they target soil sensing, not fungal battery research. MykoVolt's DevKit is a **research tool for studying the MFC itself**, not a finished sensor.
- **Coexistence**: A lab studying soil MFCs could use Bactery's field sensors and MykoVolt's bench DevKit for different experiments.

### 14.2 Indirect: Passive RFID Soil Sensors

- **What they are**: Off-the-shelf RFID tags that power a temperature/humidity sensor from the reader's RF field
- **Price**: €0.50–5.00 per tag
- **Limitation**: No energy storage; cannot log data; reads are manual and intermittent
- **Verdict**: The cheapest alternative but not functionally equivalent — MykoVolt's device stores energy self-sufficiently

### 14.3 Indirect: CR2032-Powered Sensors

- **What they are**: The battery-sensor combination that powers 99% of today's IoT soil sensors
- **Price**: €0.50 (battery) + €1–10 (sensor module) per node
- **Limitation**: Battery must be replaced; creates toxic waste; battery fails at low temperatures
- **Verdict**: The **real** competition — not other MFCs, but the status quo. Every buyer will compare MykoVolt to "just use a coin cell."

### 14.4 MykoVolt's Real Competitive Advantage

Not performance — biodegradable is worse along every metric except one:

> **A MykoVolt-powered sensor can be buried in soil once and forgotten. A CR2032-powered sensor must be dug up, the battery replaced, and the hole re-sealed — every 6–18 months. For remote or large-scale deployments, the labour cost of battery replacement dwarfs the sensor cost.**

This advantage only matters if:
- The device's **lifetime matches or exceeds** the battery-powered alternative (gap open)
- The device is **cheap enough to be disposable** (gap narrowing at scale)
- The **deployment is large enough** that battery-replacement labour is material (true for precision ag above ~20 ha)

---

## 15. Revenue Projections (Honest)

### 15.1 Phase 1: DevKit Sales Only

| | Year 1 | Year 2 | Year 3 |
|---|---|---|---|
| **Units sold** | 25–80 | 60–200 | 150–500 |
| **Avg. unit price (€)** | 30 | 30 | 28 |
| **DevKit revenue (€)** | 750–2,400 | 1,800–6,000 | 4,200–14,000 |
| **Grant / consortium income (€)** | 0–30k (if EXIST funded) | 30k–80k (if Horizon) | 50k–150k (if EIC) |
| **Total revenue (€)** | **750–32,400** | **1,800–86,000** | **4,200–164,000** |

**Note**: The wide range reflects binary grant outcomes, not market uncertainty. Without grant funding, revenue stays below €15k/year.

### 15.2 Phase 2 (Year 3–5): Beta + Early Commercial

- Beta revenue: negligible (shipping-only, no unit price)
- First commercial sales (ag-tech research farms): €50–100/unit, 100–500 units/year
- Revenue range (Year 4–5): €5k–50k without grants; €100k–200k with active grant consortium

### 15.3 Phase 3 (2030+): Agricultural

- Do not project until field trial data exists.
- **Target unit price at scale**: €3–8/unit
- **Target market**: precision agricultural sensor market (€2.3B by 2030 per Mordor Intelligence)
- **MykoVolt addressable share at 2030**: unknown — dependent on certification, cost curve, and competition

---

## 16. Implementation Timeline

| Quarter | Action | Deliverable |
|---|---|---|
| **Y1 Q1–Q2** | Finalise DevKit PCB + firmware v0.1; order first prototype batch (50 units) | Working prototype |
| **Y1 Q2** | Open-source hardware release on GitHub, Hackaday.io | Project page live |
| **Y1 Q3** | Submit ISMET poster abstract; contact target lab PIs | 8–15 email contacts |
| **Y1 Q4** | Attend ISMET; demo prototypes; send 5–10 free trial units | Funnel started |
| **Y1 Q4** | Submit EXIST application (if eligible); begin Horizon Europe partner search | Grant pipeline |
| **Y2 Q1** | First trial feedback; revise firmware + documentation v1.0 | Updated DevKit |
| **Y2 Q2** | Publish methods paper (or submit); open teaching-lab pack | Publication |
| **Y2 Q3** | Attend E-MRS or ISMET again; follow-up with trial labs | Repeat orders |
| **Y2 Q4** | List on Tindie; CrowdSupply campaign (if sufficient demand) | Sales channel |
| **Y3–5** | Phase 1b teaching lab rollout; Phase 2 beta launch | Segments expand |

---

## 17. Key Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| No lab buys DevKit ("interesting but not useful") | Medium | Critical | Validate with 5 labs before committing to batch production |
| Grants not funded | High | High | Bootstrap; keep burn rate at solo-founder level |
| Fungal culture incompatible with target lab's equipment | Low | Medium | Provide 3 reference strains; document equipment requirements |
| Open-source clone undercuts price | Low–Medium | Low | Commodity hardware cannot be protected; differentiate on consumables + community |
| NFC readout range too short for lab use | Medium | Medium | Test with 3 different NFC phone models before v1.0; consider adding I²C/UART header for wired readout |
| Biodegradable materials fail RoHS | Medium | High (Phase 3) | Phase 1–2 exempt; monitor RoHS exemption updates; engage CEN workshop on biodegradable electronics standards |
| Solo founder bandwidth — cannot attend conferences AND ship DevKits AND write grants AND publish | High | Critical | Prioritise: Year 1 focus is conference attendance + grants. Ship DevKits from stock assembled by local maker space or JLCPCB. |

---

## 18. Summary

| Phase | Segment | Timeframe | Revenue | Key Activity |
|---|---|---|---|---|
| **1** | MFC research labs | 2026–2028 | €750–32k / yr | Conference demos → trial → publication → repeat |
| **1b** | University teaching labs | 2028–2030 | €500–6k / yr | Lab manual development → curriculum integration |
| **2** | Ag-tech research farms (beta) | 2030–2032 | €5–50k / yr | Field trials → certification → co-authored papers |
| **3** | Commercial agriculture | 2030+ | Unknown | Scale manufacturing → channel distribution |

**Guiding principles**:
1. **Researchers pay for novelty, farmers pay for reliability.** Do not confuse the two.
2. **Publications are harder to ignore than ads.** Every euro spent on co-authored papers is better spent than a euro on Google Ads.
3. **Open-source the hardware, sell the consumables.** The DevKit PCB is a loss leader for electrode refills; the research platform is a loss leader for the agricultural device.
4. **Grants are not revenue, but they pay for R&D that would otherwise be unfundable.** Pursue them aggressively in Phase 1–2.
5. **Do not scale what you have not validated.** A single repeat order from a lab that published using your platform is worth more than 100 cold emails.
