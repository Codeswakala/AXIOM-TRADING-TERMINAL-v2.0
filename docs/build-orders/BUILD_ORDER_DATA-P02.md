# BUILD ORDER — DATA-P02

**Issued by:** Independent Technical Review & Governance Authority (authorized by Operator)
**Date:** 2026-08-18
**Phase:** DATA-P02 — Multi-timeframe aggregation & session context
**Base of record:** nine-element chain → `data_p01.patch.txt` → `data_p01_correction.patch.txt` → `data_p01_correction2.patch.txt` (11 elements, DATA-P01 APPROVED WITH OBSERVATIONS)
**Scope authority:** Operator accepted ITRGA recommendations on Q1 (trim), Q2 (no per-instrument volatility), Q3 (fold `F-DATA2-1` into DATA-P02 as central requirement)

---

## 1. SCOPE — AND WHAT IS EXCLUDED

Re-inventoried against the current tree, not the blueprint. Two of the blueprint's four items are already delivered.

| Blueprint item | Disposition |
|---|---|
| Multi-timeframe aggregation | **IN SCOPE — central** |
| `TD-029` resampling | **IN SCOPE** — as the aggregation fix only; the notice already exists |
| Session context | **IN SCOPE — greenfield** |
| Volatility state | **EXCLUDED — already built and surfaced** |

### Explicitly out of scope — do not build

- **Per-instrument volatility regime.** `realized_volatility` exists (`portfolio_risk.py:80`) and is surfaced in the Risk & Drawdown dock (`TerminalBottomDock.tsx:718–730`). Operator decision: not duplicating it. **Do not add a volatility label to watchlist rows.**
- **The watchlist clip** (`OBS-DATA-P01-WATCHLIST-CLIP`) — POLISH triage.
- **Bundle size** (`OBS-5`) — POLISH-P01.
- Any change to the DATA-P01 walk generators, seeding, correlation, provenance or labelling. **That work is closed. Do not revisit it.**

---

## 2. THE CENTRAL DEFECT — `F-DATA2-1`

The UI offers `1m · 5m · 15m · 1h · 4h · 1d`. The database stores **`M1` only**.

`TerminalChartStage.tsx:88–97` maps the UI timeframe to a backend code (`"1h" → "H1"`), requests it, receives nothing, and falls back at `:106` to fetching `M1`. Then at `:118`:

```ts
const parsedBars: CandleBar[] = rawCandles.map((c: ApiCandle) => ({
  time: …, open: Number(c.open), high: Number(c.high),
  low: Number(c.low), close: Number(c.close), …
}));
```

**One-to-one. No bucketing. No aggregation anywhere in the codebase.**

So `1h` renders 100 one-minute bars while the axis, the `TD-029` notice (*"Resampled from M1 stream"*) and the saved-annotation metadata (`:239`, `resolution: "resampled"`) all assert an hourly series.

**Under this programme's constitutional posture this is a fabricated interval.** The governing question is *"could a manufactured value be mistaken for a market observation?"* — and a timeframe label applied to unaggregated data is exactly that. Worse than a silent gap: the honesty notice describes a transformation that never happened, converting a visible defect into an invisible one.

Pre-existing. Not a DATA-P01 regression. **`TD-029` is not closed by the existence of a notice.**

---

## 3. MANDATORY REQUIREMENTS (M1–M8)

### M1 — Real server-side OHLC aggregation
Aggregate `M1` candles into `M5`, `M15`, `H1`, `H4`, `D1` with correct semantics per bucket:
**open** = first bar's open · **high** = max high · **low** = min low · **close** = last bar's close · **volume** = sum.

Build on `CandleRepository` (`backend/app/repositories/candle_repository.py`). Aggregation is **backend** work — not a client transform. Bucket boundaries must be aligned to wall-clock intervals (an `H1` bucket starts on the hour), not to "every 60th row in the result set".

### M2 — Aggregation is exposed through the API
The frontend must obtain aggregated bars from the server. Existing consumer is `fetchCandles` (`client.ts:1526`) hitting `list_candles` (`persistence.py:55`). Either extend that path or add an endpoint; state which and why. Follow the established auth pattern — `CurrentOperatorDep`, `SessionDep`, as in `backend/app/api/routes/market.py:21`.

### M3 — The client 1:1 fallback is removed
`TerminalChartStage.tsx:106–114` must no longer pass unaggregated `M1` bars off as a higher timeframe. **Deleting the fallback without providing aggregation is not acceptable** — that trades a false series for an empty chart on five of six timeframes.

### M4 — Provenance must distinguish three states, on a typed result kind
A bar series is now one of:
- **native** — stored at the requested timeframe
- **aggregated** — computed from `M1` at request time
- **unavailable** — insufficient `M1` coverage to form the bucket

Carry this as a **typed discriminant on the response**, following the `SURF-P03 M3` pattern:

```ts
export type CandleSeriesResult =
  | { kind: "native"; bars: … }
  | { kind: "aggregated"; bars: …; sourceTimeframe: "M1" }
  | { kind: "unavailable"; detail: string };
```

**Never** infer the state by matching message strings. **Never** infer it from bar count.

### M5 — The `TD-029` notice must become true
The existing notice (`data-testid="timeframe-resampled-notice"`) must render from the M4 discriminant, not from `timeframe !== "1m"`. When a series is genuinely aggregated it says so; when native it does not appear; when unavailable the chart must show absence, not an improvised series.

Same correction for the annotation metadata at `:239` — `resolution` must reflect what actually happened.

### M6 — Partial buckets are disclosed, never silently padded
If an `H1` bucket has only 40 of 60 minutes, the bar is **incomplete**. Either exclude it or mark it explicitly. **A partial bucket presented as a complete bar is the `a wrong price is worse than no price` failure at bar granularity.** State the chosen rule in the delivery report.

### M7 — Session context
Greenfield. Tokyo / London / New York sessions with correct UTC boundaries and overlap periods, surfaced so the operator can see which session a bar or the current moment falls in.

**Bounded:** session context is **presentation and labelling over existing data**. It must **not** alter the DATA-P01 walk generators to add time-of-day volatility. Those generators took three correction cycles to stabilise; reopening them is out of scope. If you believe session-varying volatility is needed, raise it as a recommendation in the delivery report — do not build it.

### M8 — Frontend T-1 guard with non-vacuity anchors
Per standing lesson: assert the anchor sentence is **present**, `.replace()` it out, then assert forbidden terms are absent from the residue. Anchor the honesty text — the aggregation/provenance disclosure — so its removal fails the build. Pin at least one anchor that would break if M5's notice reverted to a hardcoded string.

---

## 4. SUPPORTING SCOPE (S1–S3)

- **S1** — Aggregation must be deterministic and order-independent: the same `M1` input yields identical aggregated output regardless of row ordering or repeat calls.
- **S2** — Timeframe mapping (`tfMap`, `TerminalChartStage.tsx:89`) must have a single source of truth shared with the backend's timeframe vocabulary. Two divergent maps is a defect waiting to happen.
- **S3** — Performance: state the aggregation cost for the largest supported window. If aggregation is computed per request, say so and give the measured latency.

---

## 5. CONSTRAINTS (R1–R6)

- **R1** — No change to `_base_price`, the walk generators, `symbol_seed`, `class_factor_seed`, betas, or provenance values. DATA-P01 is closed.
- **R2** — **RBAC unchanged.** 16 routes, `protectedWorkspace()` (`workspaceRegistry.tsx:168`). No registry, route or role changes. Assert independently verifiable.
- **R3** — Constitutional boundaries: no automated execution, no external LLMs, no dynamic plugins, no live trading. Simulated data must never be presentable as market data.
- **R4** — `source="seed:synthetic"` remains the single provenance value. Aggregated bars derive from synthetic bars and **must not** acquire a new or weaker provenance marker.
- **R5** — No new dependencies without justification in the delivery report.
- **R6** — Report the bundle delta against DATA-P01's `720.67 kB` (`OBS-5`).

---

## 6. EVIDENCE REQUIRED

**Standing rule: for visual requirements the image is primary; instruments corroborate. Instruments must measure rendered extent, not proxies.**

### Captures (PNG, hashes declared in a verification JSON)
1. **`1m` native** — no resampled notice.
2. **`1h` aggregated** — notice present and accurate; **the bars must visibly differ from the `1m` view of the same window.** This is the proof the aggregation is real. Two identical-looking charts at different timeframe labels is the defect, not the fix.
3. **`1d` aggregated** — longest bucket; verifies boundary alignment.
4. **Insufficient coverage** — the `unavailable` state rendering honestly.
5. **Session context** surfaced.

### Instruments
- Per-capture legibility record in the style delivered for DATA-P01 cycle 3 — layout box, ink rect, painted-stroke extent, hit-test at the rightmost pixel, and a hard gate failing the run if a required element is not fully legible. **That instrument was correct; reuse it.**
- Hash every PNG; reconcile against the JSON.

### Named tests
- `test_data_p02_aggregation_ohlc_semantics_correct` — feed known `M1` bars, assert first-open / max-high / min-low / last-close / summed-volume exactly.
- `test_data_p02_aggregation_bucket_boundaries_wall_clock_aligned`
- `test_data_p02_aggregation_deterministic_and_order_independent`
- `test_data_p02_partial_bucket_disclosed_not_padded`
- `test_data_p02_series_kind_discriminates_native_aggregated_unavailable`
- Frontend T-1 guard per M8.

**Each test must fail against the current code.** Demonstrate it — the DATA-P01 crypto regression test was accepted because it failed at a 227.97 ratio and passed at 1.00. Same standard.

### Executed evidence
Full `pytest`, `vitest`, `tsc -b`, `npm run build` transcripts. Distinguish executed from asserted. Baseline: **421 BE + 819 FE = 1,240**.

---

## 7. ACCEPTANCE CRITERIA

1. `M1`–`M8` satisfied and independently verifiable.
2. `S1`–`S3` addressed; deviations disclosed.
3. `R1`–`R6` honoured.
4. Aggregation semantics proven by test against known input.
5. Capture 2 visibly demonstrates aggregated ≠ native for the same window.
6. `TD-029` notice accurate in all three states.
7. Partial-bucket rule stated and enforced.
8. Session context surfaced without touching the generators.
9. All five captures legible, hashed, reconciled.
10. Every named test fails on current code, passes after.
11. Full transcripts supplied.
12. Delivery report documents what changed, where, and every deviation — **including any failed attempt.** DATA-P01 cycle 3 disclosed a 500 error unprompted; that is the standard.
13. Patch applies clean on the 11-element chain; sha256 declared and matching.
14. Bundle delta reported.

---

## 8. DELIVERY PROTOCOL

Upload: patch · delivery report · capture verification JSON · PNGs. **The artifact of record is the verified patch, not a commit.** No commits, pushes or pulls — repository activity is Operator-timed.

Filenames collide with prior uploads; expect ITRGA to preserve them on arrival.

---

## 9. NOTES TO THE DA

`F-DATA2-1` is a pre-existing defect, not a mark against your work. It surfaced because DATA-P01 populated all eleven instruments and made the chart reachable across timeframes.

Two things from DATA-P01 that I want repeated: you fixed the **defect class** rather than the cited line — twice — and you disclosed a failed seed attempt that a clean retry would have buried. Both are exactly right. The legibility instrument you built in cycle 3 is now the standard for this programme.

One caution carried from cycle 2: verify claims about rendered values against **the artifact you are shipping**, not your own screen.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This Build Order authorizes implementation of DATA-P02 only. It is not authorization for CHART or POLISH. No implementation beyond this scope.

**We don't guess. We prove.**
