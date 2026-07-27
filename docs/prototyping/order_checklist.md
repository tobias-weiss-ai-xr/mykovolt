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
