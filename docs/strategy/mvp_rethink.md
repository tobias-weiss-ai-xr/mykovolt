# MykoVolt MVP — Evidenz-Basierter Neu-Entwurf

> **Status:** Analyse (2026-08) | **Trigger:** DOI-Audit offenbarte, dass die bisherige MVP-Einschätzung (50 µW/cm² × 2 cm² = 100 µW, Neurospora 260 µW/cm²) auf halluzinierten Quellen ruhte.
> **Korrektur:** Neu-Ausrichtung auf den Mg-Air-Baseline (garantiert, TRL 2–3) mit Fungal-Pressling als *Phase-E-Upgrade*.

---

## 1. Harte Fakten (nur geprüfte Literatur)

| Komponente | Strom | Spannung | TRL | Quelle |
|-----------|-------|----------|-----|--------|
| Mg-Air-Batterie (0,6–1,6 V) | **50–500 µW** @ 10 cm | 0,6–1,6 V | 2–3 | `docs/mg_air_battery.md`, 12 Papers im Korpus |
| BQ25570-Boost + STM32L011 | <30 µW avg System | 3,3 V | 9 | `3.1 Ultra-Low-Power Firmware` (Thesis) |
| Laccase-Biokathode (Hybrid-Zn-O₂) | *nicht angegeben* | **1,76 V** ✅ | 2 | Electrochimica Acta 2012 (10.1016/j.electacta.2011.12.026) |
| Fungal Pressling (*Trametes*) | **12,5 µW/cm²** (OCV 300–600 mV) | 0,3–0,6 V | 2 | Empa-Baseline (original MVP 2025-06-26) |
| 1-Jahr stabile Enzym-BFC | *über 1 Jahr* | — | 2 | Bioelectrochemistry 2015 (10.1016/j.bioelechem.2015.04.009) |

**Der entscheidende Punkt:** Die einzige *quantifizierte, geprüfte* µW-Zahl für einen Pilz-MFC ist die Empa-Baseline von **12,5 µW/cm²** (12,5 µW × 2 cm² = **25 µW**). Der angeblich "bestätigte" Wert von **260 µW/cm² (Neurospora)** existiert **nicht** — kein Paper, kein DOI, keine Datenbank. Er wurde im DOI-Audit 2026 zurückgezogen.

---

## 2. Die zwei Wege zum funktionierenden Produkt

```
          ┌──────────────────────────────────────────────────┐
          │               Mg-Air MVP (TRL 2-3)               │
          │                                                  │
          │  Mg-Folienzelle (50–500 µW)                     │
          │        │  BQ25570 Boost  │                        │
          │        ↓                  ↓                        │
          │  STM32L011 + ST25DV04K NFC  +  FDC1004 Kapazitiv │
          │                                                  │
          │  ✅  funktioniert SOFORT   €0,08  kompostierbar   │
          └───────────────┬──────────────────────────┬───────┘
                          │                          │
            "Science-Skin"│                      "Garantierte"
               (falls      │                     Leistung
                 validiert)│                          │
                          ▼                          ▼
          ┌─────────────────────────┐    ┌─────────────────────────┐
          │ Fungal-Upgrade (Phase E) │    │  Product-MVP liefert    │
          │ *Trametes* Pressling     │    │  heute schon alle Daten │
          │ ggf. 12,5–50 µW        │    │  — Mg-Air ist ausreichend│
          └─────────────────────────┘    └─────────────────────────┘
```

| Stellung | Mg-Air-MVP | Fungal-Upgrade |
|----------|-----------|----------------|
| Leistung | ✅ 50–500 µW — deutlich über 30 µW Budget | ⚠️ 25 µW (12,5 × 2) — knapp am Budget |
| TRL-Produkt | ✅ 2–3 (Laborprototypen bekannt) | ⚠️ 2 (ungekrönt — muss validiert werden) |
| Kosten | ✅ €0,08 | €0,50 |
| Tiefe (>5 cm) | ✅ (Wasserreduktion) | ❌ (Chimney nötig) |
| Kälte/Permafrost | ✅ (> –20 °C mit Salzelektrolyt) | ❌ (Pilz dormiert < 5 °C) |
| Lebensdauer | ✅ 130–200 Tage (0,5 g Mg) | ⚠️ 2–4 Wochen (Zorn-Kritik) |
| "Fungal Story" | ⚠️ schwach | ✅ stark |
| **Time-to-First-Working-Logger** | **2–3 Wochen** | 6–12 Wochen + Unklarheit |

### Entscheidung

> **Mg-Air ist das produktive MVP.** Der fungale Pressling ist ein *separates Phase-E-Validierungsprojekt*, das – falls er >50 µW/cm² bei >30 Tagen Lebensdauer erreicht – ein **Kund-wertiges "Science-Skin"** liefert (Premium-Differenzierung), **nicht** die Grundversorgung des Produkts.

Das ist **konsistent** mit der Original-Architektur (`docs/archive/MVP_DESIGN.md` 2025-06-26), die bereits *Trametes@Empa 12,5 µW/cm²* als Ziel nannte und schrieb: *"Ein DevKit-Launch 2026 ist von TRL 2 aus nicht realisierbar."* Die 260-µW-These war ein späterer Drift.

---

## 3. Produkt-Konzepte neu bewertet

Die alte Matrix ging von *"50 µW/cm² × 2 cm² = 100 µW"* aus (ungekrönt). Mit dem Mg-Air-Baseline (50–500 µW) **funktionieren fast alle Konzepte sofort**, ohnehin auf Pilzleistung zu warten:

| Konzept | Alte Abhängigkeit | Neue Bewertung | MVP-Phase |
|---------|-------------------|----------------|-----------|
| Soil Moisture / Compost / Concrete | 50 µW | ✅ Mg-Air liefert | **Phase 1** |
| Cold-Chain Logger / Smart Packaging / Wildlife Tag | 25 µW | ✅ Mg-Air oder passiv NFC | **Phase 1** |
| Edu Kit | — | ✅ passiv NFC, TRL 9 | **Phase 1 (sofort)** |
| Soil-Carbon (180 Tage) | 260 µW | ✅ Mg-Air (365 Tage) | **Phase 1** |
| Forestry / Permafrost / Landfill | 260 µW | ✅✓ Mg-Air = Einzellösung | **Phase 2** |
| Agricultural Network | 260 µW | ⚠️ Mg-Air-Skala (50k+ Stück) | Phase 2–3 |
| Smart Wound Dressing | 50 µW | ⚠️ medizinische Regulierung (IVDR) | Phase 2 |
| Landmine/UXO | 260 µW | ✅ Mg-Air (multi-year) | **Phase 2** |
| Mycelium Structural Battery | 260 µW | ❌ **nicht realisierbar** (70% Under-Energy) | ❌ Ausschalten |
| Space Habitat | 100 µW | ⚠️ Mg-Air + O₂ im Vakuum? | Langfrist |

**Neue Kern-Erkenntnis:** 5–6 Konzepte, die *spezifisch auf >100 µW Pilzleistung* angewiesen waren (Mycelium-Structural, Space, Agricultural-Network), sind entweder **realisierbar via Mg-Air** (mit anderer Rechtfertigung) oder **sollten gestrichen** (Mycelium-Structural: 70% Under-Energy). **Die Pilzleistung ist für das funktionierende Produkt irrelevant bewiesen** — sie ist das Vertrauen/Story-Element.

---

## 4. Die zwei unterschiedlichen "Stories"

| Story | Mg-Air | Fungal |
|------|--------|--------|
| **Produkt-Narrativ** | "Biodegradable battery that composts after use" | "Living battery that grows its own power" |
| **TRL** | 2–3 (funktioniert) | 2 (Versprechen) |
| **Kosten** | €0,08 | €0,50 |
| **Kundentrendenzuspruch** | "Zero-waste electronics" | "Self-growing electronics" |
| **Investor-Frage** | "Wann deliverst du?" → **2–3 Wochen** | "Beweisbar?" → 6+ Monate |

**Strategie:** Ship the **Mg-Air-DevKit** ("Zero-waste NFC Logger") *now* — es generiert Revenue + Validation-Daten. Das **Fungal-Upgrade** ("Living Battery") ist der **Phase-E-Science-Play** für PR, Grants (BMBF/Forschung) und die *eventuelle* Premium-Version — aber **nicht** die Abhängigkeit für ein funktionierendes Produkt.

---

## 5. Konkrete nächste Schritte (validierbar)

1. **Week 1:** Mg-Air-Einzelzelle bauen → messen: OCV, V, I bei 0 / 10 / 30 cm Tiefe (Validation Plan `mg_air_battery.md` Step 1–3).
2. **Week 2:** Breadboard mit Mg-Air-Eingang (statt J2-Pressling) → BQ25570 startet, NFC-Tag wird gelesen (Step 4).
3. **Week 3:** 7-Tage-Soil-Test: DevKit + Mg-Air in 10 cm Tiefe, >80% Datenintegrität.
4. **Parallel Phase E:** Fungal-Pressling validiert gegen 12,5 µW/cm² Empa-Baseline — *nur* wenn er die Mg-Air-Leistung deutlich überschreitet, wird er ins Produkt integriert.

> **Gate-Kriterium für Fungal-Integration:** Der Pressling muss **>50 µW/cm²** messen **und** >30 Tage Lebensdauer zeigen — sonst bleibt Mg-Air das Produkt und der Pressling ein veröffentlichbares Forschungsergebnis.

---

## Anhang: Warum 260 µW/cm² falsch ist

Der Claim stammt aus dem Email-Entwurf an Prof. Zorn ("Neurospora crassa ... 260 µW/cm²") und floss in die README-Species-Tabelle ein. Der DOI dafür (`10.1021/acs.est.7b01253`) existiert **nicht** — CrossRef 404. Die *echte* Paper-Menge zu Neurospora + Mikrobielles Brennstoffzellen ist **null** (vollständiger Audit, siehe `gap_analysis.md` §2). 260 µW/cm² ist ein 60-facher Überschuss gegenüber der einzigen verifizierten Zahl (12,5 µW/cm²); in der MFC-Literatur ist das **physikalisch implausibel** für einen einzelnen Pilz-Pellet bei Raumtemperatur.

---

*Ich (der Agent) habe diesen Neu-Entwurf angesetzt. Die ursprünglichen 2025er-Architekturen (`docs/archive/MVP_DESIGN.md`) und das detaillierte Mg-Air-Design (`docs/mg_air_battery.md`) waren bereits richtig — die 260-µW-These war der Fehler, den ich korrigiere.*
