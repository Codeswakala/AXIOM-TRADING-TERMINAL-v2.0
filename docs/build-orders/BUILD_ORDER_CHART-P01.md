# BUILD ORDER — CHART-P01

**Issued by:** Independent Technical Review & Governance Authority (authorized by Operator)
**Date:** 2026-08-18
**Phase:** CHART-P01 — Technical indicators: honest controls, server-side computation
**Base of record:** 12-element chain (through `data_p02.patch.txt`)
**Operator scope decisions:** build indicators for real · **server-side** computation · fix `F-CHART-1` + small indicator set

---

## 1. THE DEFECT THIS PHASE FIXES

`TerminalChartStage.tsx:362–391` renders `SMA 20`, `SMA 50`, `EMA 20`. Each toggles a boolean that is used **only** to set the pill's `active` class:

```tsx
onClick={() => setOverlays((prev) => ({ ...prev, sma20: !prev.sma20 }))}
className={`chart-overlay-pill ${overlays.sma20 ? "active" : ""}`}
```

`overlays` is never passed to the chart. The stage renders `<PriceChart bars chartType symbol height onBarHover />` — no overlay prop — and `PriceChart.tsx:3` declares *"Renders series data; does not compute indicators or analytics."* No SMA/EMA computation exists anywhere in the frontend or backend.

**Clicking SMA 20 highlights the button and changes nothing.** The control advertises a capability the system does not have — the inverse of the governing reframe, and the same class as `F-DATA2-1`: the UI asserting something the data does not support.

---

## 2. SCOPE

**In scope:** SMA 20 · SMA 50 · EMA 20 (making existing controls honest) · **RSI 14 · MACD (12/26/9) · Bollinger Bands (20, 2σ) · ATR 14**.

Seven indicators. Chosen because all are pure-OHLC, need no new data, and together exercise every architectural case: overlay-on-price (SMA/EMA/Bollinger), separate pane (RSI/MACD), and a volatility input other indicators later depend on (ATR).

### Explicitly out of scope — do not build

- **Volume indicators** (OBV, VWAP, MFI, CMF, Relative Volume, Volume Profile). Volume is generated as `gauss()` **independent of price action**; these would compute correctly and mean nothing. Deferred pending generator work.
- **Order Flow (Delta/CVD/Imbalance)** — requires per-trade buy/sell side, which does not exist and is constitutionally barred.
- **Liquidity pools / sweeps / stop runs** — order-book information the system must not claim.
- **Confluence engine, and `Trade Eligibility` in particular** — referred to Operator; may cross the non-actuating boundary. **No build under this order.**
- **Drawing tools** — CHART-P03.
- **Market Structure (BOS/CHoCH/FVG/Order Blocks)** — CHART-P02/P03, and see the naming caution.
- Any change to DATA-P01 generators or DATA-P02 aggregation. **Both are closed. R1 applies.**

---

## 3. MANDATORY REQUIREMENTS (M1–M8)

### M1 — Indicators computed server-side
Consistent with DATA-P02: derived series are **server** work. Compute over the same candle window the series endpoint already serves. Do not compute indicators in the browser.

### M2 — Correct, verifiable formulae
- **SMA(n)** — arithmetic mean of the last `n` closes.
- **EMA(n)** — `α = 2/(n+1)`; state and justify the seeding rule (SMA-seeded or first-value-seeded).
- **RSI(14)** — state whether Wilder's smoothing or simple averaging; Wilder's is standard.
- **MACD(12,26,9)** — MACD line, signal line, histogram.
- **Bollinger(20, 2)** — SMA ± 2 population standard deviations; state population vs sample.
- **ATR(14)** — true range with Wilder's smoothing.

**Each must be provable against hand-computable input** — see Evidence.

### M3 — The three existing controls become functional
`SMA 20`, `SMA 50`, `EMA 20` must render actual overlay series on the price chart. The `active` pill state must correspond to a visible line. **This is the `F-CHART-1` closure condition.**

### M4 — Insufficient history is disclosed, never padded
An indicator needing `n` bars over a window with fewer than `n` **must not** emit a value. Reuse the DATA-P02 pattern — a typed discriminant, not a sentinel:

```ts
| { kind: "computed"; points: … }
| { kind: "insufficient"; required: number; available: number }
```

**Never** emit `0`, `null` rendered as a line, or a partial-window average presented as a full-period one. Concretely: **SMA 50 on D1 with 6 bars must render `insufficient`, not a 6-bar mean labelled 50.** This is `a wrong price is worse than no price` at indicator granularity, and the direct analogue of DATA-P02's partial-bucket rule.

### M5 — Derived-value provenance
Indicator output derives from `seed:synthetic` bars and must be labelled as derived from simulated data. **Do not introduce a new provenance marker** — the vocabulary is `seed:synthetic` and `live:simulated` (R4 of DATA-P02). An indicator must never appear more authoritative than the bars beneath it.

### M6 — Indicators respect the DATA-P02 series kind
An indicator computed over an **aggregated** series must be disclosed as such. An indicator must **never** be computed over a series whose kind is `unavailable`. If the underlying series is aggregated with excluded partial buckets, the indicator inherits that disclosure.

### M7 — Determinism
Same bars in, same indicator values out — across repeat calls and independent of request order. Aligns with DATA-P01 S2 and DATA-P02 S1.

### M8 — Frontend T-1 guard with non-vacuity anchors
Standing pattern: assert the anchor sentence **present**, `.replace()` it out, assert forbidden terms absent from the residue. Anchor the indicator provenance/insufficiency disclosure so its removal fails the build.

**Forbidden terms must include the actuation vocabulary** already enforced in `terminalWatchlistDepth.test.tsx:321–334` (`buy`, `sell`, `execute`, `order_ticket`, `position`, …). An indicator surface is where "signal → action" language creeps in. **No indicator may render a buy/sell recommendation, a trade signal, or an eligibility verdict.**

---

## 4. SUPPORTING SCOPE (S1–S4)

- **S1** — Indicator definitions in a **single registry** (name, period(s), required bars, pane placement) so CHART-P02 adds a formula and an entry, not an architecture.
- **S2** — Separate-pane indicators (RSI, MACD) must not distort the price pane's scale.
- **S3** — Toggling an indicator must not refetch or recompute the candle series unnecessarily. State the strategy — computed with the series, or a separate call.
- **S4** — State the computation cost for the largest supported window with all seven enabled.

---

## 5. CONSTRAINTS (R1–R7)

- **R1** — No change to DATA-P01 generators (`chart_seed_service.py`, `adapters/simulated.py`, `live_service.py`) or DATA-P02 aggregation (`ohlcv_aggregation.py`, `persistence_service.py` series logic). Both closed.
- **R2** — RBAC unchanged: 16 routes, `protectedWorkspace()`. Verify independently.
- **R3** — Constitutional: no automated execution, no external LLMs, no dynamic plugins, no live trading. **No trade recommendations, eligibility verdicts, or actionable entry/stop/target output.**
- **R4** — Provenance vocabulary unchanged: `seed:synthetic`, `live:simulated`.
- **R5** — **No new charting or math dependency without justification.** `lightweight-charts` is present; a TA library is not. Prefer explicit implementation — the formulae are short and must be test-provable.
- **R6** — Bundle delta reported against DATA-P02's **724.50 kB** (`OBS-5`).
- **R7** — `PriceChart.tsx`'s stated contract (*"does not compute indicators"*) must remain true — it may **render** provided series but must not **compute**. If the contract changes, update the docblock; do not silently violate it.

---

## 6. EVIDENCE REQUIRED

**Standing rule: the image is primary; instruments corroborate and must measure rendered extent.**

### Captures
1. **SMA 20 + SMA 50 active on `1M`** — two visibly distinct lines tracking price; `SMA 50` visibly smoother than `SMA 20`. **Both pills `active` and both lines present** — the `F-CHART-1` proof.
2. **EMA 20 vs SMA 20 together** — visibly divergent at a turning point (EMA reacts faster). Two overlapping identical lines would indicate one formula is wrong.
3. **RSI + MACD in separate panes** — price pane scale undistorted.
4. **Bollinger Bands** — bands widening/narrowing with volatility.
5. **Insufficient history** — `SMA 50` on `1D` (6 bars) rendering the `insufficient` state honestly. **Must not show a line.**
6. **All indicators off** — chart returns to a clean candlestick view, no residue.

### Instruments
Reuse the DATA-P01 cycle-3 legibility instrument — layout box, ink rect, painted-stroke extent, hit-test at rightmost pixel, hard gate on illegibility. Hash every PNG; reconcile against the JSON.

### Named tests — each must fail against current code
- `test_chart_p01_sma_matches_hand_computed_values`
- `test_chart_p01_ema_seeding_rule_and_alpha_correct`
- `test_chart_p01_rsi_wilder_smoothing_matches_reference`
- `test_chart_p01_macd_line_signal_histogram_correct`
- `test_chart_p01_bollinger_bands_two_sigma_correct`
- `test_chart_p01_atr_true_range_wilder_correct`
- `test_chart_p01_insufficient_history_returns_typed_kind_not_padded_value`
- `test_chart_p01_indicator_deterministic_and_order_independent`
- `test_chart_p01_indicators_never_render_actuation_language` (M8 guard)

**Hand-computed fixtures are required for M2.** A test asserting the implementation equals itself proves nothing — supply input bars whose expected values can be verified by inspection, as the DATA-P02 aggregation test did.

### Executed evidence
Full `pytest`, `vitest`, `tsc -b`, `npm run build`. Distinguish executed from asserted. Baseline **429 BE + 829 FE = 1,258**.

---

## 7. ACCEPTANCE CRITERIA

1. M1–M8 satisfied and independently verifiable.
2. S1–S4 addressed; deviations disclosed.
3. R1–R7 honoured.
4. Every formula proven against hand-computed values.
5. `F-CHART-1` closed — the three existing pills render real series.
6. Capture 1 shows both SMA lines; capture 2 shows EMA/SMA divergence.
7. Insufficient history renders typed, never padded.
8. Indicator provenance never exceeds the underlying bars'.
9. No actuation language on any indicator surface.
10. All six captures legible, hashed, reconciled.
11. Every named test fails on current code, passes after.
12. Full transcripts supplied.
13. Delivery report documents changes and **all deviations, including failed attempts**.
14. Patch applies clean on the 12-element chain; sha256 declared and matching.
15. Bundle delta reported.

---

## 8. DELIVERY PROTOCOL

Upload: patch · delivery report · capture verification JSON · PNGs. **Artifact of record is the verified patch, not a commit.** No commits, pushes or pulls — repository activity is Operator-timed.

---

## 9. NOTES TO THE DA

**The lasting deliverable is the architecture, not seven indicators.** Roughly 45 of the ~70 items in the AXIOM Analytics Engine list are buildable on current data (see `ITRGA_ASSESSMENT_AXIOM_ANALYTICS_ENGINE.md`). If the registry, the typed insufficiency discriminant and the provenance rules are right here, each later indicator is a formula plus an entry. **Get the contract right on seven; it then scales to seventy.**

Two carried standards: fix the **defect class** rather than the cited line — if you find a fourth inert control, say so; and verify rendered-value claims against **the artifact you are shipping**.

One caution specific to this phase: an indicator surface is where advisory language turns into instruction. The precedent is Advisory Signals — calibrated probability, uncertainty interval, `NON-ACTUATING` label, and it stops short of recommending a trade. **Indicators display; they do not advise.**

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
Authorizes CHART-P01 only. Not authorization for CHART-P02/P03 or POLISH.

**We don't guess. We prove.**
