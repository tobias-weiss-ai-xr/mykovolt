# MykoVolt — Order & Build Checklist

> **Status:** All designs verified, firmware compiles. Ready to build.

---

## Phase A: Order PCBs (JLCPCB)

| Item | Status | Action |
|------|--------|--------|
| Gerber ZIP | ✅ Ready | `hardware/kicad/gerber/` — 12 files |
| JLCPCB order | ⬜ Todo | 4-layer, ENIG, 0.8mm, 5 pcs + stencil |
| Estimated cost | | ~€18 incl. shipping |

## Phase B: Order Components (Mouser + Reichelt)

| Category | Cost | Status |
|----------|------|--------|
| ICs (10× each) | €134.50 | ⬜ Mouser basket |
| Passives (100×) | €15.00 | ⬜ Mouser basket |
| Inductors + crystal | €10.80 | ⬜ Mouser basket |
| Supercap + ESD | €16.70 | ⬜ Mouser basket |
| MOSFET + LEDs | €4.10 | ⬜ Mouser basket |
| Connectors | €20.00 | ⬜ Mouser basket |
| **Subtotal** | **~€200** | **⬜ Order** |

## Phase C: Breadboard Prototype

| Item | Cost | Status |
|------|------|--------|
| Nucleo-L011K4 | €10 | ⬜ Order |
| BQ25570EVM or QFN adapter | €3-20 | ⬜ Order |
| DIP adapters (SOIC-8, WSON-10) | €8 | ⬜ Order |
| ICs (ST25DV04K, MB85RC16, etc.) | €8 | ⬜ Order (see Mouser above) |
| Passives + breadboard + wires | €15 | ⬜ Local shop |
| **Total** | **~€46** | **⬜ Order** |

## Phase D: Build & Test

| # | Task | Est. Time | Status |
|---|------|-----------|--------|
| D1 | Power: BQ25570 → 3.3V | 1 evening | ⬜ |
| D2 | I²C bus: scan 0x50–0x53 | 1 evening | ⬜ |
| D3 | RTC + FRAM: read/write | 1 evening | ⬜ |
| D4 | NFC: phone detects tag | 1 evening | ⬜ |
| D5 | Cap sensor: probe response | 1 evening | ⬜ |
| D6 | Firmware: flash + verify | 1 evening | ⬜ |
| D7 | Sleep: <10µA idle | 1 evening | ⬜ |
| D8 | **Full system test** | 2 evenings | ⬜ |

## Phase E: Fungal Bio-Battery Validation (Separate Track)

> **Status:** TRL 2 (literaturgestützt) | **Ziel:** Validierung der Pilz-Power-Ziele und Lebensdauer
> **Grundlage:** Der MVP (Phase A–D) nutzt **Mg-Air** als garantierte Stromquelle (`docs/mg_air_battery.md`). Phase E validiert, ob der **fungale Pressling** als Leistungs-Upgrade und für die "fungal story" genutzt werden kann — nicht als Leistungsbasis.

### E0 — Strom-Baseline (Empa, nicht 260 µW!)

| Spezies | Bestätigte Leistung | Quelle | Status |
|---------|---------------------|--------|--------|
| Trametes (Laccase-DET) | 12,5 µW/cm² (OCV 300–600 mV) | Empa-Baseline¹ | ✅ Replikations-Ziel |
| 1-Jahr stabile Enzym-BFC | >30 Tage Stabilität | Bioelectrochemistry 2015 (10.1016/j.bioelechem.2015.04.009) | ✅ Lebensdauer-Modell |
| Laccase-Biokathode (1,76 V) | 1,76 V Hybrid-Zn-O₂ | Electrochimica Acta 2012 | ✅ Spannung verlässlich (kein µW nötig) |

¹ *Keine Quelle existiert für "260 µW/cm²" (Neurospora) — dieser Claim wurde im DOI-Audit 2026 zurückgezogen (s. `research/docs/research/gap_analysis.md`). 50 µW/cm² ist ein Ziel, nicht eine bewährte Zahl.*

### E1 — Trametes-Presse-Replikation (2 Wochen)

| # | Task | Target | Status |
|---|------|--------|--------|
| E1 | Trametes-Pressling nach Empa-Protokoll bauen | OCV 300–600 mV, 12,5 µW/cm² | ⬜ |
| E1 | 30-Tage-Lebensdauer-Test | >70% Leistung nach 30 Tagen | ⬜ |
| E1 | Mg-Air-vs-Fungal-Leistungsvergleich | Fungal > Mg-air? | ⬜ |

**Erkenntis-Trigger:** Wenn der Pressling **>50 µW/cm²** liegt, wird er das Primary-Battery. Wenn **<12,5 µW/cm²** oder **<30 Tage Lebensdauer**, bleibt Mg-air das Product-MVP und der Pressling ein Phase-2 "Science-Spin".

### E2 — 8-Strains-Screening (4 Wochen)

| # | Task | Target | Status |
|---|------|--------|--------|
| E2 | Screening: Trametes, Pleurotus, Aspergillus, Ganoderma, Saccharomyces, Phanerochaete, Pestalotiopsis + 1 Boden-isolation | Beste Leistung > 12,5 µW/cm² | ⬜ |
| E2 | Co-Kultur-Test (weißer Fäule + Hefe) | Synergie-Effekt > Einzel-Stamm | ⬜ |
| E2 | Neurospora crassa — **nur als experimenteller Kandidat!** | Literatur fehlt → erst bei Positiv-Ergebnis publizieren | ⬜ |

### E3 — Lebensdauer-Battle (Parallel)

| # | Task | Target | Status |
|---|------|--------|--------|
| E3 | Laccase-Immobilisierung vs freies Enzym | 3–5× Lebensdauer | ⬜ |
| E3 | Langzeit-Stress (30–90 Tage, Temperatur-Zyklus) | >80% Leistung nach 30d | ⬜ |

---

## Budget Summary

| Item | Cost |
|------|------|
| PCB (JLCPCB) | €18 |
| Components (Mouser) | €200 |
| Breadboard parts | €46 |
| Tools (hot air, ST-Link, etc.) | €80 |
| **Total prototype investment** | **~€344** |
| Per-board at pilot (100 pcs) | ~€17 |
| Per-board at scale (1000 pcs) | ~€8.50 |
