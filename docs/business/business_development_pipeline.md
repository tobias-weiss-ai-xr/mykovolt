# MykoVolt Business Development Pipeline

> **Status:** Active v1 | **FRAME:** TRL 2 → TRL 3/4 | **Stage:** Pre-seed / Solo Founder
> **Context:** These are **four parallel pipelines** — not a linear sequence. Progress on one unlocks the others.
> **Owner:** Founder (until co-founder onboarded)

---

## 0. The Control Panel

A single-view summary of where each pipeline stands RIGHT NOW:

| Pipeline | Current Stage | Blockers | This Week's Action |
|----------|--------------|----------|-------------------|
| **👥 Co-Founder** | Outreach → Engagement | No response yet from first batch | Send 10 follow-ups + post LinkedIn thread |
| **💰 Funding** | Pre-application (EXIST Q4 2026) | No co-founder, no university agreement | Draft LOEWE-Exploration pitch deck for EMC |
| **🎁 Customer** | Pre-deployment (no hardware) | No prototype, no labs contacted | Identify 10 target lab PIs with contact info |
| **🔬 Product** | Simulation → Lab PoC | Need co-founder for wet lab | Finalize Phase 0 experiment design |
| **📄 Publication** | Pre-data | No experimental data yet | Review Empa paper for replication protocol |

**Rule:** Every week, each pipeline must advance at least one action. No pipeline goes dark for >14 days.

---

## 1. 👥 Co-Founder Pipeline

**Goal:** Hire a scientific co-founder (mycology, electrochemistry, or materials science) by Q4 2026.
**Constraint:** EXIST application, all serious grant applications, and wet-lab access require this person.
**Owner:** Founder — this is the #1 personal priority.

### Pipeline Stages

```
Identified → Contacted → Engaged → Screened → Trial → Decision → Onboarded
    |            |           |          |         |         |          |
   30+ names    10/week     5 active    3 deep    1 trial    Mutual    Signed
                             convos     convos    project   yes       agreement
```

### Stage 1: IDENTIFIED (pool: 30+ contacts)

**Criteria:** Person matches ≥2 of these profiles:
- **Profile A:** PhD in mycology / fungal biotechnology — understands *T. pubescens*, *P. chrysosporium*, enzyme secretion
- **Profile B:** PhD in electrochemistry / bioelectrochemistry — understands MFC design, potentiostat, power density measurement
- **Profile C:** PhD in materials science / biopolymers — understands cellulose electrodes, 3D-printed bioelectronics
- **Profile D:** Postdoc or research group leader looking to leave academia — wants startup experience

**Sources:**

| Source | Effort | Expected Yield |
|--------|--------|---------------|
| ResearchGate: search "fungal fuel cell" + "microbial fuel cell fungi" | 30 min | 10–15 names |
| Google Scholar: authors citing Reyes 2024, Sukri 2021 | 30 min | 8–12 names |
| LinkedIn: search "fungal biotechnology PhD" + "Giessen" + "Marburg" + "Frankfurt" | 20 min | 5–8 names |
| ISMET conference attendee list (2025/2026) | 15 min | 15–20 names |
| University websites: JLU Gießen (EMC), Uni Marburg (fungal biology), TU Darmstadt (materials) | 45 min | 10–15 names |
| Twitter/X: follow #fungalMFC #bioelectrochemistry #mycelium | 10 min/day passive | 3–5 names/month |

**Tool:** Spreadsheet with columns: Name, Affiliation, Email, Profile Match (A/B/C/D), Outreach Date, Response, Notes.

**Target states:** Aim for 30+ names before starting outreach. Quality over quantity — Profile A matches are worth 3× Profile D.

---

### Stage 2: CONTACTED (10+ per week at peak)

**Templates:** `docs/assets/cofounder_outreach_email.md`, `docs/assets/cofounder_linkedin_post.md`, `docs/assets/cofounder_twitter_thread.md`

**Subject line A/B test:** Track open rates.

| Variant | Subject Line | Target Open Rate |
|---------|-------------|-----------------|
| A | "Fungal bio-battery startup — looking for co-founder" | >50% |
| B | "Your paper on [their topic] — we're building something around it" | >65% |
| C | "TRL 2 → TRL 3: help validate the first fungal MFC product" | >55% |

**Pitch structure (keep to 3 paragraphs max):**
1. Who you are + what MykoVolt is building (2 sentences)
2. Why THEM (specific reference to their work — shows you read their paper)
3. Ask: 15-min call to explore co-founder fit, not a pitch

**Outreach cadence:**

| Week | Action | Target |
|------|--------|--------|
| Week 1 | Send first 10 emails | 10 contacted |
| Week 2 | Follow up with non-responders (Day 7) + send 10 more | 20 contacted |
| Week 3 | Follow up Week 1 + send 10 more | 30 contacted |
| Week 4 | LinkedIn DM to non-email responders + last batch | 40 contacted |

**Success metrics:**
- Response rate: >30% (≥12 responses from 40)
- Positive ("tell me more"): >10% (≥4)
- Neutral ("not interested but happy to chat"): >15% (≥6)

**If response rate <20% after 40 emails:** Revise subject line + first paragraph. Test variant B more aggressively.

---

### Stage 3: ENGAGED (aim for 3–5 active conversations)

**Definition:** They replied with interest and agreed to a 15-minute call.

**First call script outline:**

```
[5 min] Me: MykoVolt story — the problem (e-waste from IoT), the approach (fungal MFC), 
         where we are (TRL 2, simulation validated, need wet-lab validation)
[5 min] Them: What they work on, what excites them, what they're looking for next
[5 min] Fit check: Would they want to lead the mycology/electrochemistry work? 
         What would their ideal involvement look like?
```

**After the call:** Send a one-page summary of the opportunity + link to the simulation repo + invite a second call to discuss a trial project.

**Tracking:**

| Candidate | Call Date | Fit Score (1-5) | Interest Score (1-5) | Next Step | 
|-----------|-----------|-----------------|---------------------|-----------|
| — | — | — | — | — |

**Fit Score factors:**
- 5 = PhD in fungal MFC, wants to leave academia, available within 3 months
- 4 = Strong domain match, open to startup, needs 6-month runway
- 3 = Adjacent domain, intrigued but unsure
- 2 = Wrong domain, useful as advisor not co-founder
- 1 = No match

**Move to SCREENED if:** Fit ≥3 AND Interest ≥3.

---

### Stage 4: SCREENED (aim for 1–3 deep conversations)

**Criteria for moving from ENGAGED to SCREENED:**
- Second call completed (≥45 min)
- They've read the simulation code / business docs
- They can articulate what they'd build in Phase 0
- Mutual interest in a 2-week trial project

**Second call agenda:**
1. Walk through the simulation results (product_explorer, pressling_viability)
2. Ask: "If you had €3k and 3 months, what experiment would you run first?"
3. Discuss equity: typical co-founder split is 30–50% for a technical co-founder joining at TRL 2
4. Timeline: When could they start? Part-time or full-time?
5. Conflict check: Existing obligations (postdoc contract, IP assignment)

**Red flags (automatic NO):**
- Can't commit ≥20 hrs/week for the next 3 months
- Current institution claims IP on their work (standard German research contract issue)
- Wants salary before grant funding (not possible at TRL 2)
- Doesn't believe in fungal MFC potential (culture fit)

---

### Stage 5: TRIAL (2-week mini-project)

**Purpose:** Test working relationship before committing to co-founder status.
**Structure:** A defined, concrete project with deliverables.

**Example trial projects:**

| Project | Duration | Deliverable | Evaluation Criteria |
|---------|----------|-------------|-------------------|
| Replication protocol for Empa 2024 | 1 week | Step-by-step lab protocol + BOM for materials | Completeness, accuracy, feasibility |
| O2 diffusion model validation | 1 week | Literature review of O2 in soil + proposed experiment | Depth of analysis, testable hypothesis |
| Strain selection matrix | 2 weeks | Comparison of 10 candidate fungi on power density, O2 tolerance, compostability | Rigor, surprise findings |
| Mg-air corrosion baseline | 2 weeks | Proposed test setup + expected results from literature | Feasibility, cost estimate |

**During trial:**
- Daily 10-min standup (or async text)
- Shared GitHub repo for all work
- Use `docs/technical/phase0_execution_plan.md` as reference

**Trial outcome options:**
1. 🟢 **Hire** — Clear co-founder fit → negotiate terms → agree
2. 🟡 **Extend** — Good work but need more time → define second trial
3. 🔴 **No** — Wrong fit → honest conversation, offer advisory role or referral

---

### Stage 6: DECISION → ONBOARDED

**Decision framework (both parties say YES):**

| Topic | Standard Terms for TRL 2 Co-Founder |
|-------|-------------------------------------|
| Equity | 30–50% (vesting: 4-year, 1-year cliff) |
| Salary | None until EXIST or grant funding (typically 6–12 months) |
| Role | CTO / CSO (depending on their background) |
| IP | All IP assigned to company; they retain inventor credit |
| Commitment | Full-time after EXIST; part-time before |
| Probation | 6 months (German statutory) |

**Onboarding checklist:**

```
[ ] Sign co-founder agreement (lawyer-reviewed template)
[ ] Register company (GmbH or UG) — both founders as Gesellschafter
[ ] Open business bank account (DE)
[ ] Set up shared workspace (physical or virtual)
[ ] Transfer GitHub repo ownership to company
[ ] Apply for EXIST together (new: co-founder fills scientific gap)
[ ] First joint lab visit (JLU/EMC) to scope Phase 0
[ ] Joint press release / LinkedIn announcement
```

---

## 2. 💰 Funding Pipeline

**Goal:** Secure €365k+ non-dilutive funding by end of 2027 to reach TRL 4.
**Constraint:** Most applications require co-founder, company registration, or university partner.
**Owner:** Founder (co-founder supports on scientific writing).

### Pipeline Stages

```
Monitor → Prep → Submit → Review → Decision → Manage
   |        |       |        |         |         |
Always   4-8 wks   Deadline  2-6 mo   Funded   Reporting
active   before    met                         + renewal
```

### Current State (July 2026)

| Grant | Stage | Deadline | Amount | Probability | Actions Needed |
|-------|-------|----------|--------|-------------|----------------|
| **MAFEX FLASH** 👁️ | Monitor | 15.8.2026 | €15k | Low (co-founder needed) | Note deadline; submit only if co-founder found by Aug 1 |
| **LOEWE-Exploration** | Prep | Q1 2027 (est.) | €200-300k | Medium-High | Draft pitch deck for EMC Gießen this month |
| **EXIST Gründung** | Pre-prep | Q4 2026 | €15-50k + stipend | Medium | NEED co-founder + university agreement → priority #1 |
| **EXIST Transfer** | Monitor | Rolling | €250k | Low (requires ongoing uni project) | Only after LOEWE-Exploration secured |
| **BMBF KMU-innovativ** | Monitor | Rolling 2027 | €150-400k | Low | Requires company registration + TRL 3 PoC |
| **LOEWE 3** | Monitor | Rolling 2027-28 | €100-500k | Low | Requires TRL 3 + company + Hesse partner |
| **EIC Pathfinder** | Monitor | 2027-28 | €2-3M (consortium) | Very Low | TRL 1-3 OK, but needs consortium lead |
| **EMC internal grant** | Prep | Ongoing | €5-15k | High | Ask EMC contact directly — quickest path to lab funds |

### Weekly Actions

| This Week | Action | Outcome Metric |
|-----------|--------|---------------|
| **Every Monday** | Check wissenschaft.hessen.de + BMWK + EIC portal for new calls | 0 new → no action; 1+ new → log in Grants Tracker |
| **Prep phase** | Draft 1-pager for target grant → share with advisor for feedback | Document version log |
| **Submit phase** | Finalize application → submit → log confirmation + expected decision date | Confirmation PDF saved |

### LOEWE-Exploration — Immediate Action Plan

**This is the quickest path to lab funding.** EMC (JLU Gießen) can apply now — no company needed.

| Week | Action | Owner |
|------|--------|-------|
| **Now** | Draft 2-page concept note for LOEWE-Exploration: "Experimental validation of fungal bio-batteries for biodegradable soil sensors" | Founder |
| **Week 1** | Email EMC contact: "We have a concept for LOEWE-Exploration — are you interested in leading the application?" | Founder |
| **Week 2** | Present concept to EMC team (15-min Zoom) | Founder + EMC |
| **Week 3** | Jointly draft Skizze (application outline) | Founder + EMC |
| **Week 4** | Submit if deadline aligned, or agree on next steps | EMC |

**Content of the concept note (2 pages max):**
1. **The hypothesis:** Fungal MFCs can power buried soil sensors for 7+ days if O2 is delivered via air-chimney
2. **The open question:** What is the real power density of *T. pubescens* in a 3D-printed cellulose MFC under realistic soil conditions?
3. **The experiment:** Replicate Empa 2024, then vary depth + O2 + strain (3×3 matrix, n=5 each = 45 cells)
4. **Budget:** ~€15k lab consumables + €30k student researcher stipend
5. **Why EMC:** Existing expertise in fungal biofilms + electrochemical characterization
6. **Why now:** EU Battery Regulation creates regulatory pull; first-mover advantage

### EXIST Application — Countdown

**Target: Q4 2026 submission**

| Days Out | Milestone | Status |
|----------|-----------|--------|
| T-120 | Co-founder identified | ⬜ |
| T-100 | University cooperation agreement (JLU) | ⬜ |
| T-90 | Business plan draft v1 | ⬜ |
| T-60 | Technische Beschreibung (mycology section) | ⬜ |
| T-30 | Application review with Gründungsberatung | ⬜ |
| T-7 | Final polish + format check | ⬜ |
| T-0 | SUBMIT | ⬜ |

### Grants Tracker Format

| Grant | Deadline | Submitter | Amount | Status | Probability | Last Action | Next Action |
|-------|----------|-----------|--------|--------|-------------|-------------|-------------|
| MAFEX FLASH | 15.8.2026 | MykoVolt (if co-founder) | €15k | 👁️ Monitor | 20% | → noted deadline | Check if co-founder found by Aug 1 |
| LOEWE-Exploration | Q1 2027 | EMC/JLU | €200-300k | 📝 Prep | 50% | → draft concept note | Present to EMC |
| EXIST Gründung | Q4 2026 | Founder + co-founder | €15-50k + stipend | 📝 Pre-prep | 35% | → waiting on co-founder | Finalize co-founder first |

---

## 3. 🎁 Customer Pipeline

**Goal:** First paid customer (research lab) by mid-2027 → 5 paying labs by end 2027.
**Constraint:** No hardware exists yet → this is a **relationship pipeline**, not a sales pipeline.
**Owner:** Founder, with scientific credibility from co-founder.

### Pipeline Stages

```
Target List → Warm Contact → Demo/Talk → Trial → Paid → Advocate
     |            |            |          |        |        |
  20-30 labs    Conference   15-min     Free      €35/    Co-author
  identified   + email       Zoom +    DevKit    unit     paper
               outreach      poster    sent               published
```

### Stage 0: Target List

**Source:** ResearchGate, Google Scholar (citing Reyes 2024, Sukri 2021), ISMET membership list.

**Target labs (top 10 priority):**

| # | Lab / Group | Institution | Interest Angle | Contact Status |
|---|-------------|-------------|----------------|----------------|
| 1 | Reyes et al. (Empa) | Empa, Switzerland | They built the closest thing to our product | Not yet |
| 2 | Sekrecka-Belniak | Poland | Fungal MFC characterization | Not yet |
| 3 | MFC group (any) | Wageningen UR | Soil MFC research | Not yet |
| 4 | Living Materials (Empa) | Empa, Switzerland | Adjacent fungal materials | Not yet |
| 5 | Printed Electronics IZM | Fraunhofer IZM, Berlin | Biodegradable PCB partners | Not yet |
| 6 | Biopolymers group | Uni Marburg | Fungal biology in Hesse | Not yet |
| 7 | EMC | JLU Gießen | Already have contact → potential partner | 🟢 Warm |
| 8 | Plant-Microbe | Uni Cologne | Soil sensor deployment | Not yet |
| 9 | Bioelectronics | JKU Linz | Printed bioelectronics | Not yet |
| 10 | Any MFC lab | TU Delft | Long history in MFCs | Not yet |

**Build this list to 25+ before any outreach.** Record in spreadsheet with: Lab name, PI name, email, recent publication (2023+), relevance score (1-5), contact status.

### Stage 1: WARM CONTACT

**Trigger:** Conference attendance OR paper citation.

**Playbook:**

| Event | Action | Goal |
|-------|--------|------|
| **You find their paper** | Email PI: "We built on your work — here's our simulation; would love your feedback" | Get on their radar |
| **They cite your work** (once published) | Email: "Thanks for citing us — would you like a DevKit?" | Trial lead |
| **Conference** | Attend talk → ask question → approach at poster → "Would love to show you our platform" | Face-to-face connection |
| **Gründungsberatung event** | Pitch → collect business cards → follow up | Local ecosystem connections |

**Email template for research labs:**

> **Subject:** Fungal MFC simulation — building on Reyes 2024
> 
> Dear Prof. [Name],
> 
> I'm building an open-hardware fungal bio-battery platform for soil sensing, as a follow-up to the Empa 2024 work by Reyes et al. (I see you cited their paper in your [year] paper on [topic]).
> 
> We've built a simulation suite that models pressling viability, O2 diffusion, and power density tradeoffs (MIT-licensed). I'd love to get your lab's perspective — would you have 15 minutes for a quick call? No pitch, just curiosity about whether our platform would be useful in your workflow.
> 
> Best,
> [Founder]
> MykoVolt
> [GitHub link]

### Stage 2: DEMO / TALK

**Format:** 15-minute video call OR conference poster session.

**The demo structure:**

```
[0-3 min] The problem: IoT e-waste, battery replacement labor, regulatory tailwind
[3-8 min] Our approach: Fungal MFC simulation results, product_explorer scan, 
          dual-path strategy (show the product concepts table)
[8-12 min] Their context: What are you working on? Where could a self-powered 
           biodegradable sensor fit?
[12-15 min] Ask: "Would you trial our DevKit when it's ready? No commitment, 
            just feedback."
```

**After demo — immediate follow-up (within 2 hours):**
- Send one-page summary PDF (pre-prepared)
- Link to GitHub + simulation README
- Offer to send free DevKit when batch 1 is produced (Q2 2027 target)
- Add to mailing list for DevKit launch update

**Conversion target:** 30% of demos → Trial commitment.

### Stage 3: TRIAL (Free DevKit)

**When:** Q2 2027 or whenever first 10 prototype DevKits exist.

**Trial structure:**
- Lab receives: Assembled DevKit + electrode pack + NFC phone app download link
- Lab pays: Only shipping (~€10 tracked)
- Lab provides: Feedback form within 60 days
- MykoVolt provides: Email support within 48 hours, firmware updates

**Trial feedback form (minimal):**

```
1. Did the DevKit work out of the box? (Y/N/Notes)
2. How long did you run it? (days)
3. What was the max power density you measured? (µW/cm²)
4. Would you use this for teaching? (Y/N)
5. Would you pay €35 for a DevKit? (Y/N/Maybe at €X)
6. What would you add/change? (free text)
```

**Trial → Paid conversion target:** 50% (5 of 10 trial labs buy at least 1 DevKit).

### Stage 4: PAID

**Pricing structure (Phase 1):**

| SKU | Items | Price (€) | Margin |
|-----|-------|-----------|--------|
| DEV-001 | DevKit + 1 electrode pack | 35 | ~50% |
| REF-001 | Electrode refill 5-pack | 15 | ~60% |
| LAB-010 | Lab pack: 10 DevKits + 10 refills + NFC reader | 300 | ~55% |
| EDU-030 | Teaching pack: 30 DevKits + 30 refills + manual | 600 | ~50% |

**Payment terms:** Standard for research labs: purchase order (PO) via university procurement. Net 30 days. Accept credit card via Stripe (higher fee but lower friction).

### Stage 5: ADVOCATE

**A paid customer becomes an advocate when:**
- They publish using your DevKit → you co-author or get cited in methods
- They re-order refills → recurring revenue signal
- They recommend you to a colleague → referral source

**Advocate program:**
- Co-authorship on papers using MykoVolt hardware
- Free DevKit refresh (1 per year) for continuing labs
- Early access to new firmware/hardware versions
- Listing on MykoVolt website (with permission): "Used by [Lab Name]"

### Customer Pipeline Metrics

| Stage | Current Count | Target (End 2027) | Conversion |
|-------|--------------|-------------------|------------|
| Target List | 3 (EMC + 2 others) | 25+ | — |
| Warm Contact | 1 (EMC) | 15+ | 60% of list |
| Demo/Talk | 0 | 10+ | 67% of contacts |
| Trial Commitment | 0 | 5+ | 50% of demos |
| Paid | 0 | 5+ (labs) = ~€175-350 | 50% of trials |
| Advocate | 0 | 2+ | 40% of paid |

**Revenue forecast (conservative):**
- Year 1 (2027): 5-10 labs × €35-300 = €175-1,000
- Year 2 (2028): 15-30 labs × €100 avg = €1,500-3,000
- Year 3 (2029): 40-100 labs × €80 avg = €3,200-8,000

**Note:** Revenue is not the goal in Phase 1. **Publications and citations are the goal.** Revenue is a validation metric.

---

## 4. 🔬 Product Pipeline

**Goal:** From simulation → validated lab prototype → DevKit → field-tested product.
**Constraint:** Blocked on co-founder for wet-lab execution.
**Owner:** Founder (simulation, design) + Co-founder (wet lab, validation).

### Pipeline Stages

```
Simulation → Experiment Design → Lab PoC → DevKit → Beta → Product
     |              |               |         |       |        |
   Verified     Protocol +        TRL 3    TRL 4   TRL 5-6  TRL 7+
   physics      BOM ready         data     10 units field
```

### Stage 1: SIMULATION ✅ (Current State)

**Done:**
- `e2e_soil_sensor.py` — System-level energy budget with `--empa-baseline` flag
- `pressling_viability.py` — O2 diffusion + Monte Carlo viability
- `dual_path_analysis.py` — Air-chimney vs Mg-air comparison
- `alternatives.py` — Weighted decision matrix
- `product_explorer.py` — 30-concept product scan
- `manufacturing_bom.py` — Bottom-up cost model with sensitivity
- `degradation_model.py` — Physics-informed GP degradation

**Critical gap identified by simulation:**
> Pure pressling has **8.7% viability at >5 cm depth** due to O2 starvation.
> This is the single most important finding that needs experimental validation.

### Stage 2: EXPERIMENT DESIGN (Start now, even without co-founder)

**Parallel workstreams:**

| Workstream | Can Founder Do Alone? | Deliverable | Timeline |
|-----------|---------------------|-------------|----------|
| **Replication protocol** | ✅ Yes (literature review) | Step-by-step protocol for Empa 2024 replication with BOM | 1 week |
| **Materials sourcing list** | ✅ Yes (research + quote requests) | Spreadsheet of suppliers, part numbers, prices | 1 week |
| **O2 diffusion experiment design** | ⚠️ Partial (need co-founder for biology) | 3×3 factorial: depth × strain × chimney | 1 week shared |
| **Mg-air baseline protocol** | ✅ Yes (chemistry literature) | References + proposed test matrix | 1 week |
| **Phase 0 budget** | ✅ Yes | Itemized budget for 12-month Phase 0 | 2 days |

**Immediate deliverable:** Create a `protocols/` directory in the repo:

```
protocols/
├── empa_replication.md          # Step-by-step Empa 2024 replication
├── o2_diffusion_test.md          # O2 depth × strain experiment
├── mg_air_baseline.md            # Mg-air test protocol
├── materials_sourcing.csv        # Vendor, SKU, price, lead time
└── phase0_budget.md              # Total budget with contingency
```

### Stage 3: LAB PoC (TRL 3)

**Requires:** Co-founder + lab access (EMC collaboration or EXIST lab).

**Experiment 1: Empa Replication**

| Parameter | Value |
|-----------|-------|
| Strain | *T. pubescens* (as Empa) + *P. chrysosporium* (for comparison) |
| Anode | 3D-printed cellulose + carbon cloth |
| Cathode | *T. pubescens* (bio-cathode, as Empa) |
| Electrolyte | PBS + fungal growth medium |
| Cell count | n=5 per condition = 10 cells |
| Duration | 14 days continuous |
| Measurement | Voltage every 10 min via data logger |
| **Expected result** | 12.5 µW/cm² (reproduce Empa) OR different |

**Experiment 2: O2 Depth Series**

| Parameter | Value |
|-----------|-------|
| Strains | *T. pubescens*, *P. chrysosporium*, *P. ostreatus* |
| Depths | 0 cm (surface), 5 cm, 10 cm, 15 cm, 20 cm |
| O2 mitigation | Each depth with/without air-chimney (2×5×3 = 30 cells) |
| Duration | 7 days |
| **Expected result** | Power vs depth curve, validate pressling_viability.py |

**Experiment 3: Mg-Air Baseline**

| Parameter | Value |
|-----------|-------|
| Anode | Mg foil (AZ31 or pure Mg) |
| Cathode | Air-cathode (gas diffusion layer + carbon) |
| Electrolyte | Soil moisture (0.1M NaCl + buffer) |
| Depths | 0 cm, 10 cm, 20 cm |
| Duration | 7 days continuous |
| **Expected result** | Power independent of depth; validate Mg-air path |

**Minimum viable PoC (for EXIST application):**
- Empa replication: ≥10 µW/cm² from *T. pubescens* in 3D-printed cellulose MFC
- O2 curve: Clear power drop with depth, partially mitigated by chimney
- Either result = valid scientific contribution (even "no power at depth" is publishable)

### Stage 4: DevKit (TRL 4)

**First hardware product:** NFC-based evaluation platform.

**Specifications (v1.0):**

| Component | Detail | Status |
|-----------|--------|--------|
| PCB | 4-layer, 30×20 mm, castellated edges | Design ready |
| MCU | nRF52832 (BLE + NFC) or STM32WB | Selecting |
| NFC | NT3H2111 (NXP) — passive readout | Selected (datasheet reviewed) |
| Sensor header | I²C + 2× analog (10-bit ADC) | Spec'd |
| Power input | JST 1.25mm for fungal MFC connector | Spec'd |
| Battery connector | Direct solder (replaceable pellet) | Spec'd |
| Enclosure | 3D-printed PLA + cellulose composite | Design phase |
| Firmware | Rust embedded (nrf-hal) | Select |

**DevKit block diagram (conceptual):**

```
Fungal MFC Pellet ──┬── Boost Converter (BQ25570) ──┬── nRF52 MCU ──┬── NFC Antenna
                    │                                │                │
                    ├── Voltage supervisor            ├── 512 Kbit FRAM (logging)
                    │                                │
                    └── Current sense (INA219)        └── I²C header → external sensors
```

**Cost target:** €35 BOM (prototype scale) → €12 (pilot scale, 1k) → €5 (mass, 100k+).

### Stage 5: BETA (TRL 5-6)

**10-20 DevKits deployed to research labs for field trials.**

Beta program details → see Customer Pipeline Stage 3.

### Stage 6: PRODUCT (TRL 7+)

**Transition from research tool to commercial product.**

| Product variant | Price | Target | Timeline |
|----------------|-------|--------|----------|
| DevKit v1.0 (NFC research tool) | €35 | Research labs | 2027 |
| DevKit v1.1 (BLE enabled) | €55 | Advanced labs + beta field trials | 2028 |
| FieldSensor v1 (Mg-air, LoRa) | €80 | Ag-tech research farms | 2029-30 |
| FieldSensor v2 (hybrid, multi-year) | TBD | Commercial farms | 2031+ |

---

## 5. 📄 Publication Pipeline

**Goal:** 2+ peer-reviewed papers by end 2027 using MykoVolt hardware/software.
**Constraint:** Requires experimental data from co-founder wet lab.
**Owner:** Co-founder (lead author) + Founder (co-author, computational).

### Pipeline Stages

```
Data → Analysis → Draft → Submit → Review → Published → Cited
  |       |         |        |        |        |         |
Raw     Plots +    Full      J.      Revise   Online   Others
output  stats     ms       submit    2-3x      first    build on
```

### Paper Plan

| # | Title | Target Journal | Timeline | Lead Author | Data Needed |
|---|-------|---------------|----------|-------------|-------------|
| 1 | "Simulation-guided design space exploration for fungal bio-batteries in buried soil sensor applications" | HardwareX OR PLOS ONE | H2 2027 | Founder | Simulation outputs (already have) |
| 2 | "Empa replication under soil conditions: oxygen starvation limits buried fungal MFC performance" | Sensors & Actuators B OR Bioresource Technology | H1 2028 | Co-founder | Experiment 2 data |
| 3 | "Comparative analysis of air-chimney and Mg-air biodegradable power sources for in-soil sensing" | ACS Sustainable Chemistry & Engineering | H2 2028 | Co-founder + Founder | Experiment 2+3 data |
| 4 | "Open-hardware platform for fungal bio-battery evaluation: reproducibility and community standards" | HardwareX OR JOSS | H1 2029 | Founder | DevKit validation data |

**Paper #1 — Priority: MAXIMUM.** This can be written RIGHT NOW with existing simulation data. No co-founder needed. This establishes MykoVolt's scientific credibility.

**Paper abstract (Paper #1 — draft):**

> We present a simulation framework for evaluating fungal bio-batteries in buried soil sensor applications. Our suite models oxygen diffusion, pressling compaction, power density tradeoffs, and degradation dynamics across multiple deployment scenarios. We identify oxygen starvation as the dominant failure mode for buried fungal MFCs: Monte Carlo simulations show only 8.7% of pure pressling configurations achieve viability at >5 cm depth. We further evaluate two mitigation strategies (air-chimney pressling and Mg-air hybrid) and quantify their performance envelopes. The framework is open-source (MIT license) and designed to guide experimental validation of fungal bio-battery technology for biodegradable IoT applications.

**Target length:** 4-6 pages (HardwareX) or 10-15 pages (PLOS ONE).

**Author list:** [Founder] (1st), [Co-founder if available] (2nd), possibly EMC collaborator (last).

### Paper Timeline (Paper #1)

| Week | Milestone | Owner |
|------|-----------|-------|
| W1 | Generate all figures (product_explorer, pressling_viability, e2e sensitivity) | Founder |
| W2 | Draft Methods section (simulation parameters) | Founder |
| W3 | Draft Results sections + figures | Founder |
| W4 | Introduction + Related Work | Founder |
| W5 | Discussion + Limitations | Founder |
| W6 | Full draft to co-founder/advisor for review | Founder |
| W7 | Revisions | Founder |
| W8 | Format for target journal | Founder |
| W9 | Submit to arXiv as preprint | Founder |
| W10 | Submit to journal | Founder |

**Key constraint:** This paper must NOT reveal patentable IP before filing. Review with patent attorney if budget allows. At minimum, keep Mg-air specific details vague if they constitute trade secret.

### Publication Metrics

| Metric | Current | Target End 2027 |
|--------|---------|-----------------|
| Preprints (arXiv) | 0 | 1 |
| Peer-reviewed papers | 0 | 1-2 |
| Citations | 0 | 5+ (from preprint) |
| Co-authored with customer labs | 0 | 1 |
| Conference presentations | 0 | 2 (ISMET + 1 other) |

---

## 6. Weekly Operating Rhythm

### Monday Morning — Pipeline Review (15 min)

Check each pipeline's status and set this week's one action:

| Pipeline | Last Week's Action | Outcome | This Week's Action |
|----------|-------------------|---------|-------------------|
| 👥 Co-Founder | — | — | — |
| 💰 Funding | — | — | — |
| 🎁 Customer | — | — | — |
| 🔬 Product | — | — | — |
| 📄 Publication | — | — | — |

**Rule:** Each pipeline must advance at least one row per week. No pipeline goes dark for >14 days.

### Friday Afternoon — Metrics Log (10 min)

Update the pipeline metrics:

| Metric | Value This Week | Change | Notes |
|--------|----------------|--------|-------|
| Co-founder pool (identified) | — | ±0 | — |
| Co-founder active conversations | — | ±0 | — |
| Grants in prep | — | ±0 | — |
| Grants submitted | — | ±0 | — |
| Target labs (customer) | — | ±0 | — |
| Warm contacts made | — | ±0 | — |
| Demos given | — | ±0 | — |
| Trials committed | — | ±0 | — |
| Paid customers | — | ±0 | — |
| Papers drafted | — | ±0 | — |
| Papers submitted | — | ±0 | — |

### Weekly Work Allocation (Target)

| Activity | Hours | Notes |
|----------|-------|-------|
| Co-founder outreach + conversations | 10 | #1 priority |
| Grant writing / funding prep | 5 | Use Founders' time when not doing outreach |
| Customer outreach + relationship building | 5 | Research lab contact, conference prep |
| Product development (simulation, design) | 10 | Paper writing, experiment design, code |
| Admin + learning | 5 | Regulatory reading, networking, accounting |
| **Total** | **35** | Sustainable solo founder pace |

**If total >40 hours/week for >3 consecutive weeks:** Drop publication pipeline hours to minimum (keep simulation data generation only).

---

## 7. Critical Path & Bottlenecks

### The Co-Founder Bottleneck

```
                   ┌─────────────────────┐
                   │   CO-FOUNDER FOUND   │
                   │         ↓            │
    ┌──────────────┼──────────────────────┼──────────────┐
    ↓              ↓                      ↓              ↓
Wet lab PoC    EXIST application     Customer demos    Publications
(TRL 3)        (€15-50k)             (credible labs)   (data-driven)
    ↓              ↓                      ↓              ↓
Product        LOEWE 3 / BMBF         Paid orders      Citations
DevKit         (€150-500k)            (revenue)        (credibility)
```

**Without co-founder:** Three of four pipelines are blocked (Funding, Product, Publication). Only Customer outreach can proceed (with simulation-only value proposition).

**Mitigation if co-founder not found by Q4 2026:**
1. Pivot to data-only offering (sell simulation tool + consulting to labs)
2. Apply for solo-founder-friendly grants (MAFEX FLASH, some BMWK programmes)
3. Contract a student researcher (HiWi) through EMC for specific lab tasks
4. Publish Paper #1 solo (simulation-only, no experimental validation needed)

### Key Decision: Publication vs Patent Timing

**Strategy:** Submit Paper #1 (simulation) as preprint NOW. File patent on any novel Mg-air integration or chimney design BEFORE submitting Paper #2-3 (experimental).

| Action | Timeline | Cost | Impact |
|--------|----------|------|--------|
| Paper #1 (simulation) arXiv preprint | Q3 2026 | €0 | Establishes priority |
| Provisional patent (chimney design + Mg-air hybrid) | Q4 2026 (before LOEWE-Exploration submission) | ~€2-5k (German attorney) | Protects core IP |
| Paper #2 (experimental) | H1 2028 | €0 (data from co-founder lab) | Builds on patent priority |

---

## 8. Templates & Assets Index

| Pipeline | Asset | Location |
|----------|-------|----------|
| 👥 Co-Founder | Outreach email template | `docs/assets/cofounder_outreach_email.md` |
| 👥 Co-Founder | LinkedIn post template | `docs/assets/cofounder_linkedin_post.md` |
| 👥 Co-Founder | Twitter thread template | `docs/assets/cofounder_twitter_thread.md` |
| 👥 Co-Founder | Masters student recruitment | `docs/assets/masters_students_recruitment.md` |
| 👥 Co-Founder | Co-founder search SVG (post image) | `docs/assets/cofounder_search.svg` |
| 💰 Funding | Grant roadmap | `docs/grants/grant_roadmap.md` |
| 💰 Funding | Finance & funding strategy | `docs/business/finance_funding_strategy.md` |
| 💰 Funding | Phase 0 execution plan | `docs/technical/phase0_execution_plan.md` |
| 🎁 Customer | Marketing segment strategies | `docs/business/marketing_segment_strategies.md` |
| 🎁 Customer | Competitive intelligence | `docs/business/competitive_intelligence_dashboard.py` |
| 🎁 Customer | Supply chain analysis | `docs/business/supply_chain_analysis.md` |
| 🎁 Customer | Compliance & regulatory roadmap | `docs/business/compliance_regulatory_roadmap.md` |
| 🔬 Product | Product concepts document | `docs/product/product_concepts.md` |
| 🔬 Product | IP strategy | `docs/business/ip_strategy.md` |
| 🔬 Product | Simulation README | `simulation/README.md` |
| 📄 Publication | Product analysis (archive) | `archive/product_analysis.md` |
| 📄 Publication | Superpowers plan (archive) | `archive/superpowers_plan.md` |

---

## 9. Templates (Ready-to-Use)

### Weekly Email to Advisor / Mentor

> **Subject:** MykoVolt weekly — [W/C DATE]
>
> Hi [Advisor],
>
> **Pipeline status this week:**
> - Co-Founder: [X active conversations, Y new contacts]
> - Funding: [Grant X in prep, deadline Z]
> - Customer: [X new target labs, Y contacts this week]
> - Product: [Simulation progress / experiment design]
> - Publication: [Paper X — Y% complete]
>
> **This week's wins:**
> - [1-2 bullet points]
>
> **Blocked on:**
> - [1-2 specific asks]
>
> **Request:** [Specific 5-min ask — feedback on an email, intro to someone, etc.]
>
> Best,
> [Founder]

### Pipeline Review Template (Monthly Board)

> **Date:** [DATE]
> **Solo Founder Check-in**
>
> **Pipeline Progress:**
> - Co-Founder: [🟢/🟡/🔴] — [1-line status]
> - Funding: [🟢/🟡/🔴] — [1-line status]
> - Customer: [🟢/🟡/🔴] — [1-line status]
> - Product: [🟢/🟡/🔴] — [1-line status]
> - Publication: [🟢/🟡/🔴] — [1-line status]
>
> **Burn rate:** €[X]/month personal
> **Runway:** [X] months
>
> **Key decision this month:**
> - [Decision with two options]
> - Decision: [Make a clear call]
>
> **If I only do ONE thing this month:**
> - [The single most impactful action]

---

## 10. Risk Register (Pipeline-Specific)

| Risk | Pipeline | Likelihood | Impact | Mitigation | Trigger |
|------|----------|-----------|--------|------------|---------|
| No co-founder found by Q4 2026 | All | Medium-High | Critical | Pivot to simulation-only offering; apply for solo founder grants; hire HiWi through EMC | <5 active conversations by Sept 2026 |
| EXIST application rejected | Funding | Medium (40% failure) | High | Apply again next round; pursue LOEWE-Exploration in parallel; bootstrap | Rejection letter |
| Empa replication fails (no measurable power) | Product | Medium | Critical | Publish negative result (valuable data); pivot to Mg-air focus; revisit strain selection | <1 µW/cm² after 14 days |
| First DevKit batch fails assembly | Product | Medium | Medium | Order from 2 PCB assemblers; test 5 units before shipping | >50% failure rate in QA |
| Lab declines trial DevKit | Customer | Low-Medium | Medium | Improve documentation; add I²C header for custom sensors; lower price | <30% trial conversion |
| Paper #1 rejected from all targets | Publication | Medium | Low | Submit to lower-tier journal; improve with reviewer feedback | 3 rejections |
| Patent filed too late (after publication) | Product | Medium-High | High | File provisional before any publication; use German "Gebrauchsmuster" for fast, cheap protection | First public disclosure |

---

*Generated from pipeline analysis of all existing MykoVolt business documents. Templates in `docs/assets/`. Simulation code in `simulation/`.*
