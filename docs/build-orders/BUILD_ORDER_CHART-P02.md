# BUILD ORDER — CHART-P02

**Issued by:** Independent Technical Review & Governance Authority (authorized by Operator)
**Date:** 2026-08-18
**Phase:** CHART-P02 — Indicator breadth at scale: Trend · Momentum · Volatility · Levels · Statistics
**Base of record:** 13-element chain (through `chart_p01.patch.txt`)
**Precondition met:** CHART-P01 APPROVED (unqualified). The registry architecture it established is the foundation this phase scales.

---

## 1. WHY THIS PHASE IS DIFFERENT

CHART-P01 proved seven formulae. **CHART-P02 is not "more formulae" — it is the first phase where the surface has to survive scale.**

The re-inventory found the architecture genuinely ready: `INDICATOR_REGISTRY` is a clean `id / label / pane / required_bars / compute` table, the endpoint accepts comma-separated registry ids, and the toolbar renders from `INDICATOR_UI.map(...)` — so **adding a registry row automatically surfaces a pill.** That is exactly the extensibility CHART-P01 promised.

**But two constraints bite before the formulae do**, and both were measured in the tree:

| Constraint | Measurement | Consequence |
|---|---|---|
| **Toolbar** | `.chart-overlays-group` is a flat `display: flex` row; 7 pills today | ~20 pills will overflow or crush the toolbar |
| **Pane stacking** | `IndicatorPane` fixed `height = 110px`, no cap on count | 5 pane-indicators = 550px + ~360px price = **910px** in a ~500px area |

Adding fifteen indicators without addressing these produces an unusable terminal that passes every formula test. **This phase must solve the surface, not only the maths.**

---

## 2. SCOPE

### Indicators to add (15)

| Engine | Add | Pane |
|---|---|---|
| **Trend** | VWMA 20 · HMA 20 · Supertrend (10, 3) · Ichimoku (9/26/52) | overlay |
| **Momentum** | Stochastic (14,3,3) · CCI 20 · ROC 12 · ADX/DMI 14 | pane |
| **Volatility** | Keltner (20, 2×ATR10) · Donchian 20 | overlay |
| **Levels** | Pivot Points (classic) · Camarilla · Previous H/L · Session Levels | overlay |
| **Statistics** | Z-Score 20 · Percentile Rank 20 · Linear Regression Channel 20 | overlay |

Total surface after this phase: **22 indicators**.

### 🔴 VWMA — a required judgement, not a free addition

VWMA is volume-weighted. **Volume in this system is `gauss()` noise generated independently of price action** (`OBS-DATA2-1` neighbourhood; documented in `ITRGA_ASSESSMENT_AXIOM_ANALYTICS_ENGINE.md`). A VWMA over noise volume is arithmetically correct and informationally empty.

**Required:** either
- **(a)** implement VWMA and **disclose in the UI** that its volume input is simulated and uncorrelated to price — the disclosure must be visible to the operator, not only in a docstring; or
- **(b)** omit VWMA from this phase and state that it awaits volume-generator work.

**(b) is the recommendation.** Do not ship a volume-weighted indicator over noise volume without the operator being told. State the choice in the delivery report.

### Explicitly out of scope

- **Volume engine** (OBV, VWAP, MFI, CMF, Relative Volume, Volume Profile) — blocked pending volume-generator work.
- **Order Flow (08)** and **liquidity pools/sweeps/stop runs (06)** — data does not exist; constitutionally barred.
- **Confluence engine (11)**, especially `Trade Eligibility` — awaiting Operator ruling. **No build.**
- **Market Structure (05)** — CHART-P03, with the naming caution.
- **Drawing tools** — CHART-P03.
- Any change to DATA-P01 generators, DATA-P02 aggregation, or the CHART-P01 formulae. **All closed.**

---

## 3. MANDATORY REQUIREMENTS (M1–M9)

### M1 — Extend by registry row, not by architecture change
Each indicator = a formula in `indicators.py` + a row in `INDICATOR_REGISTRY` + a mirrored `INDICATOR_UI` entry. **The endpoint and client architecture must not need modification.** If they do, say so explicitly and explain why — that would mean CHART-P01's extensibility claim was overstated, which is worth knowing.

### M2 — Correct, hand-verifiable formulae with declared conventions
Every indicator has convention choices. **State each, and pin it with a hand-computable test**, as CHART-P01 did:
- **HMA** — `WMA(2×WMA(n/2) − WMA(n))` over `√n`; state rounding of `n/2` and `√n`.
- **Supertrend** — ATR multiplier, and the band-locking rule on trend flips.
- **Ichimoku** — the 26-period forward displacement of the cloud and the 26-period lagging span. **Displacement means plotting beyond the last bar; state how future-dated points are handled** (see M6).
- **Stochastic** — fast vs slow; the %D smoothing period.
- **ADX/DMI** — Wilder's smoothing; the DX-to-ADX averaging step.
- **CCI** — the `0.015` constant and **mean absolute deviation, not standard deviation**.
- **Keltner** — EMA or SMA centre; ATR period distinct from the channel period.
- **Pivots/Camarilla** — which prior period (session/day) supplies H/L/C, and the exact multipliers.
- **Z-Score / Percentile** — population vs sample; percentile interpolation method.
- **Linear Regression Channel** — least-squares fit; channel width basis (σ or max deviation).

**A test asserting the implementation equals itself proves nothing.** Supply inputs whose expected outputs are verifiable by inspection.

### M3 — `required_bars` is the full-definition requirement
Following CHART-P01's MACD precedent (34, not 26): declare what the **complete** indicator needs, not the earliest bar at which something can be drawn. Ichimoku's senkou B needs 52 periods; ADX needs roughly `2n` for the DX average to seed. **Never emit a partially-formed indicator.**

### M4 — Insufficiency stays typed
Reuse the CHART-P01 discriminant unchanged: `{kind: "insufficient", required, available}`, zero points, no line. This is settled architecture — do not reinvent it.

### M5 — 🔴 TOOLBAR MUST SCALE
22 pills cannot sit in a flat flex row. Deliver a scalable presentation — grouping by engine (Trend / Momentum / Volatility / Levels / Statistics), a menu, or a searchable picker.

**Requirements:** every indicator reachable **without horizontal scrolling of the whole toolbar**; active indicators visible at a glance without opening a menu; and the existing seven must remain reachable in **no more interactions than today** for the three most-used (SMA 20 / SMA 50 / EMA 20).

**A capability that becomes harder to reach after a phase is a defect** — the governing reframe applies directly.

### M6 — 🔴 PANE BUDGET MUST BE BOUNDED
Measured: 5 pane-indicators at 110px each = 550px, plus ~360px of price pane, in a ~500px area. Deliver an explicit policy — a maximum concurrent pane count with honest refusal, dynamic pane heights, or a tabbed/collapsible pane region.

**Whatever the policy: the price pane must never be squeezed below a usable height, and a refusal must be explicit — never a silently dropped indicator.** State the policy and the numbers in the delivery report.

**Ichimoku's forward displacement** must not distort the price pane's time axis or imply data beyond the last bar. State the handling.

### M7 — Cross-pane time-axis synchronisation
CHART-P01 disclosed that panes fit independently and do not follow price-pane zoom/pan (`subscribeVisibleTimeRangeChange` count: **0**). With 8+ pane indicators this stops being cosmetic — unsynchronised axes make multi-pane reading actively misleading, because a feature at one x-position in the price pane is at a different x-position below it.

**Required this phase:** pane time axes track the price pane. Crosshair sync is **recommended**, not required.

### M8 — Provenance and series-kind inheritance unchanged
Every new indicator inherits CHART-P01's M5/M6 behaviour: derived-value provenance from the displayed series, no new markers, no computation over an `unavailable` series, aggregation disclosure inherited.

### M9 — T-1 guard extended
The existing anchor (*"Indicators describe data, they never advise a trade."*) must still be pinned. **Extend the forbidden-advisory list for the new surface** — Supertrend, ADX and Stochastic attract directional language (`bullish`, `bearish`, `oversold`, `overbought`, `buy signal`, `golden cross`, `crossover signal`).

Naming an indicator's own conventional levels is acceptable (`RSI 70/30`); **rendering a directional verdict is not.** Keep the source-residue / render-assertion split CHART-P01 justified.

---

## 4. SUPPORTING SCOPE (S1–S4)

- **S1** — Registry rows carry an **engine/category** field so grouping is data-driven, not a hardcoded UI list.
- **S2** — Multi-line indicators (Ichimoku 5 lines, Donchian 3, Keltner 3, Bollinger 3, regression channel 3) must remain legible together. State how overlay colours avoid collision at 20+ possible lines.
- **S3** — Performance: measure all 22 enabled over the largest served window. CHART-P01 baseline: 7 in **5.0 ms**. Report the new figure and whether the per-toggle separate-call strategy still holds.
- **S4** — Toggling must still never refetch the candle series (CHART-P01 S3). Assert by call count.

---

## 5. CONSTRAINTS (R1–R7)

- **R1** — No change to DATA-P01 generators, DATA-P02 aggregation, or CHART-P01's seven formulae. All closed and verified.
- **R2** — RBAC unchanged: 16 routes, `protectedWorkspace()`, registry untouched. Verify independently.
- **R3** — Constitutional: no automated execution, external LLMs, dynamic plugins, live trading. **No trade recommendations, eligibility verdicts, entry/stop/target output, or directional verdicts.**
- **R4** — Provenance vocabulary unchanged: `seed:synthetic`, `live:simulated`.
- **R5** — **No new dependencies.** CHART-P01 implemented seven formulae explicitly with zero additions; a TA library must not appear now. Explicit implementation is what makes the formulae test-provable.
- **R6** — Bundle delta against CHART-P01's **730.90 kB** (`OBS-5`). This phase adds substantial surface — if the delta is large, say so plainly.
- **R7** — `PriceChart` renders, does not compute. Contract holds.

---

## 6. EVIDENCE REQUIRED

**Standing rule: the image is primary; instruments corroborate and must measure rendered extent.**

### Captures
1. **Toolbar at 22 indicators** — the M5 solution, nothing clipped, all groups reachable.
2. **Trend overlays** — Supertrend + Ichimoku on price; Ichimoku's cloud and displacement visibly correct.
3. **Momentum panes** — Stochastic + ADX/DMI + RSI stacked, **price pane still usable** (M6).
4. **Time-axis sync (M7)** — panes aligned with the price pane after a zoom or pan. A capture at default zoom proves nothing; **zoom or pan first.**
5. **Levels** — Pivots/Camarilla/Session Levels, with Session Levels composed from DATA-P02's session context.
6. **Statistics** — regression channel + Z-Score.
7. **Pane budget refusal** — the M6 policy engaging honestly when the limit is reached.
8. **Insufficient history** — a long-period indicator (Ichimoku 52) on `1D`, typed, no line.

### Instruments
Reuse the DATA-P01 cycle-3 legibility instrument with its hard gate. Hash every PNG; reconcile against the JSON.

### Named tests — each must fail against current code
One hand-computed test per indicator (`test_chart_p02_<id>_matches_hand_computed_values`), plus:
- `test_chart_p02_required_bars_are_full_definition_not_earliest_drawable`
- `test_chart_p02_pane_budget_refuses_explicitly_not_silently`
- `test_chart_p02_pane_time_axes_track_price_pane`
- `test_chart_p02_toolbar_exposes_every_registry_indicator`
- `test_chart_p02_no_directional_verdict_language` (M9)

### Executed evidence
Full `pytest`, `vitest`, `tsc -b`, `npm run build`. Distinguish executed from asserted. Baseline **442 BE + 838 FE = 1,280**.

---

## 7. ACCEPTANCE CRITERIA

1. M1–M9 satisfied and independently verifiable.
2. S1–S4 addressed; deviations disclosed.
3. R1–R7 honoured.
4. Every formula proven against hand-computed values with its convention declared.
5. `required_bars` is full-definition for every new indicator.
6. Toolbar scales; the three most-used indicators are no harder to reach than today.
7. Pane budget bounded, policy stated, refusal explicit.
8. Pane time axes track the price pane — proven **after a zoom or pan**.
9. VWMA either disclosed in-UI or omitted with a stated reason.
10. No directional verdict language anywhere.
11. All eight captures legible, hashed, reconciled.
12. Every named test fails on current code, passes after.
13. Full transcripts supplied.
14. Delivery report documents changes and **all deviations, including failed attempts**.
15. Patch applies clean on the 13-element chain; sha256 declared and matching.
16. Bundle delta reported.

---

## 8. DELIVERY PROTOCOL

Upload: patch · delivery report · capture verification JSON · PNGs. **Artifact of record is the verified patch, not a commit.** No commits, pushes or pulls — repository activity is Operator-timed.

---

## 9. NOTES TO THE DA

CHART-P01 was approved unqualified — I recomputed all six formulae independently and every one matched, including the EMA case where a linear test series would have hidden an error. That standard applies again here, across fifteen indicators with more convention ambiguity. **Declare your conventions; I will check them.**

**The hard part of this phase is not the maths.** It is that 22 indicators must remain usable on one screen. The toolbar and the pane budget are the requirements most likely to be under-served, and they are the ones I will look at first — in the captures, not the code.

Three carried standards: fix the **defect class** rather than the cited line (you did this three phases running — `overlays.volume` last time); verify rendered claims against **the artifact you ship**; and disclose failed attempts, which has been consistent and is valued.

One caution specific to breadth: Supertrend, ADX and Stochastic come with a folk vocabulary of buy and sell signals. Ichimoku especially is usually taught as a trading system. **Implement the mathematics; refuse the recommendations.** The precedent is Advisory Signals — calibrated numbers, uncertainty, `NON-ACTUATING`, no instruction.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
Authorizes CHART-P02 only. Not authorization for CHART-P03 or POLISH.

**We don't guess. We prove.**
