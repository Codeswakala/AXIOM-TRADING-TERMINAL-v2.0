# ITRGA DETERMINATION — UI TRANSFORMATION PROGRAMME CLOSURE

**Reviewing body:** Independent Technical Review & Governance Authority
**Subject:** Formal closure of the AXIOM UI transformation programme
**Date:** 2026-08-18
**Baseline:** `AXIOM-TRADING-TERMINAL-v1.0` @ `34f4c62`
**Final state:** 16-element verified patch chain

---

## 1. DETERMINATION

# PROGRAMME CLOSED — ALL AUTHORIZED PHASES APPROVED

Eight phases authorized, delivered, independently verified and approved. Every finding raised is closed but one, which is non-blocking and owned by the DA.

**This is not a production certification.** §8 states plainly what is and is not established.

---

## 2. THE ARTIFACT CHAIN OF RECORD

The artifact of record is the **verified patch, not the commit**. Repository state was never an acceptance criterion. Each element below applies clean, in this order, onto `34f4c62`, and each was applied by ITRGA in a pristine clone before its determination.

```
34f4c62 (baseline)
 1  item3.patch.txt                b7b4c4f74f3016cb
 2  item5.patch.txt                4c03910c76fdcbf2
 3  item6.patch.txt                f65da5c3ce8433ec
 4  item4.patch (1).txt            a516c2c144c1f2f6
 5  surf_p01.patch.txt             62c4d021e5b6f0a0
 6  surf_p01_obs1-2.patch.txt      69964afec17b9c0f
 7  surf_p02.patch.txt             e039c74bc9993640
 8  surf_p03.patch.txt             c18d5d05816de0cb
 9  data_p01.patch.txt             2af54d600e736359
10  data_p01_correction.patch.txt  1bbaee09eb06f22f
11  data_p01_correction2.patch.txt 34edc1762b8691f9
12  data_p02.patch.txt             69509b49e2738518
13  chart_p01.patch.txt            6e141e9ab7d27bf0
14  chart_p02.patch.txt            084b03c333c9c7cc
15  chart_p03.patch.txt            5b74fc6466a73b90
16  polish_p01.patch.txt           598d2ac91142f403
```

**Seventeen consecutive hash-reconciled deliveries.** Every declared hash was verified against transmitted bytes before any determination was written.

---

## 3. PHASE DETERMINATIONS

| Phase | Verdict | Substance |
|---|---|---|
| **UI-CONV-P03** | APPROVED WITH OBSERVATIONS | Workspace convergence; `OBS-CONV2-5` closed |
| **SURF-P01** | APPROVED WITH OBSERVATIONS | Execution Research dock surfaced; `OBS-SURF1-1/2` closed |
| **SURF-P02** | **APPROVED** (unqualified) | Alerts; `TD-061` closed; `unreadCount: number \| null` |
| **SURF-P03** | APPROVED WITH OBSERVATIONS | Governance surfacing; typed denial-vs-absence |
| **DATA-P01** | APPROVED WITH OBSERVATIONS (3 cycles) | Eleven instruments; `CA-DATA1-1/2/3` closed |
| **DATA-P02** | APPROVED WITH OBSERVATIONS | Real server-side aggregation; `F-DATA2-1`, `TD-029` closed |
| **CHART-P01** | **APPROVED** (unqualified) | 7 indicators; `F-CHART-1` closed |
| **CHART-P02** | **APPROVED** (after re-submission) | 16 indicators; `CA-CHART2-1` closed |
| **CHART-P03** | **APPROVED** | Drawings + Market Structure; `F-CHART3-1/2` closed |
| **POLISH-P01** | **APPROVED** | All carried observations closed |

Four unqualified approvals. One `RETURN FOR RE-SUBMISSION` (transmission, not merit). One phase requiring three correction cycles.

---

## 4. FINDINGS — FULL DISPOSITION

**Closed:** `OBS-CONV2-1` · `OBS-CONV2-4` · `OBS-CONV2-5` · `OBS-CONV3-1/5/9` · `OBS-SURF1-1` · `OBS-SURF1-2` · `TD-061` · `CA-DATA1-1` · `CA-DATA1-2` · `CA-DATA1-3` · `OBS-DATA1-1` · `OBS-DATA1-2` · `F-DATA2-1` · `TD-029` · `OBS-DATA2-1` · `OBS-DATA-P01-WATCHLIST-CLIP` · `F-CHART-1` · `CA-CHART2-1` · `F-CHART3-1` · `F-CHART3-2` · `OBS-CHART-1` · `OBS-5` · `F-BRAND-1`/`GA-173`

**Open — one:**

| `OBS-SURF3-1` | SURF-P03 capture 03 declared `f08ab63d…` but never transmitted. Owner: **DA**. Non-blocking; the requirement it evidenced was verified by other means. |

---

## 5. FINAL VERIFIED STATE

| | |
|---|---|
| RBAC routes | **16**, `protectedWorkspace()` — unchanged across all eight phases |
| Registered indicators | **29** |
| Drawing tools | **6**, price/time anchored |
| Backend test files | **70** |
| Frontend test files | **175** |
| Tests | **476 BE + 859 FE = 1,335** |
| Initial bundle | **626.51 kB** (from 748.05 kB, −16.2%) |
| Provenance vocabulary | exactly two: `seed:synthetic` · `live:simulated` |

The provenance line is the one I would point to first. Across eight phases that generated prices, aggregated intervals, computed 29 indicators and detected market structure, **the vocabulary describing where a value came from never grew.** No phase introduced a marker that made derived output look more authoritative than the bars beneath it.

---

## 6. WHAT THE PROGRAMME ACTUALLY ESTABLISHED

The governing reframe was *"every already-built capability must be surfaced in the best possible way."* The recurring defect was the inverse — surfaces asserting more than the data supported.

Five instances, each closed at the root:

- **A fabricated price.** `_base_price` fell through to `Decimal("1.00000")` for five instruments. Replaced with `raise KeyError`. *A wrong price is worse than no price.*
- **A fabricated interval.** Six timeframes offered, one stored; `1h` rendered 100 one-minute bars while the notice read *"Resampled from M1 stream."* Real wall-clock aggregation, typed `native`/`aggregated`/`unavailable`.
- **A fabricated capability.** Three indicator pills toggled state and computed nothing. Now 29 indicators computed server-side.
- **A fabricated anchor.** Annotations positioned by CSS percentage — precise-looking, meaningless. Now `(price, time)`, proven byte-identical across a timeframe round-trip. Legacy rows labelled *"position is unknown and is not invented."*
- **A fabricated narrative.** Order Blocks assert institutional accumulation. On a `gauss()` feed there are none. Shipped as geometric pattern detection with that stated in the product.

**The last authorized surface was the one most able to undo it.** Confluence aggregates interpretations rather than data, and the distance from *"7 of 9 aligned"* to *"high-probability setup"* is one adjective. It emits a score with a Wilson interval, a `NON-ACTUATING` label, and a statement that it is not a market opinion. `Trade Eligibility` and `Risk/Reward` were refused and remain unbuilt absent a constitutional amendment.

---

## 7. REVIEW METHOD — AND ITS FAILURES

Every determination was written against a pristine clone with the full chain applied. Thirty-five formulae and detections were **recomputed independently** rather than accepted from test assertions — including the cases where a plausible implementation is quietly wrong: CCI's mean absolute deviation (16% off from the stdev variant), HMA's `n + √n − 1`, Ichimoku's senkou spans clamped rather than projected, EMA checked on a non-linear series because a linear ramp hides the error.

**Two of my own errors are on the record**, both found by me and one confirmed by the DA:

- **CHART-P02:** I reported a Stochastic mismatch. My manual was the raw %K; the signature was `(14,3,3)` — slow stochastic. The implementation was right.
- **POLISH-P01:** I stated the login page had no 3D treatment. I had grepped `LoginPage.tsx` and never opened `LoginPage.css`, which holds 20 such rules. **A grep against one file is not an inventory of a component.**

The DA disclosed failed attempts unprompted in every phase — a bucket-flooring `+10h` shift, a bubble-phase click handler that jsdom could never have caught, a capture instrument measuring a dev server that serves no chunks, and a pane policy that violated its own stated minimum and was refused by its own gate. **Instruments that catch their author are worth more than instruments that confirm them.**

---

## 8. WHAT IS **NOT** ESTABLISHED

Stated plainly, because closure is routinely over-read:

- **Production is NOT CERTIFIED.** This programme reviewed a UI transformation against Build Orders. It was not a security audit, a performance qualification, a data-integrity audit of pre-existing subsystems, or a release readiness assessment.
- **Test transcripts were recorded as asserted, not re-executed by ITRGA.** Where substance mattered — formulae, aggregation semantics, anchor round-trips, drift — I verified by direct execution. The suite totals are the DA's.
- **The feed is simulated throughout.** Nothing in this programme connects to a market.
- **The gate remains CLOSED.** No automated execution, no external LLMs, no dynamic plugins, no live trading.
- **`OBS-SURF3-1` remains open.**
- Unbuilt and out of scope: Volume engine (blocked — volume is noise uncorrelated to price), Order Flow (data does not exist), liquidity pools/sweeps (order-book data, barred), Regime engine and Equal Highs/Lows (buildable, never authorized), `Trade Eligibility` (refused).

---

## 9. CLOSING

The programme began with a watchlist showing ten rows of `--` and ends with eleven instruments carrying correlated, per-symbol-seeded, honestly-labelled prices across six timeframes, 29 indicators, six anchored drawing tools, and a market-structure surface that detects geometry while refusing the story that normally travels with it.

What was actually built is narrower and more useful than a feature list: **a terminal where a displayed value means what it claims, and where the system says so when it cannot.**

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This determination closes the UI transformation programme. It is **not** authorization for any further phase. No implementation before a new Build Order.

**We don't guess. We prove.**
