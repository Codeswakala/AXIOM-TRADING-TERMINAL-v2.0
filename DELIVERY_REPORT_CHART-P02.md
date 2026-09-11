# DELIVERY REPORT — CHART-P02 (Indicator breadth at scale)

**Delivered by:** AXIOM Development Authority
**To:** ITRGA
**Date:** 2026-08-18
**Build Order:** `BUILD_ORDER_CHART-P02.md` (sha256 `121ecaa2d92bd470bafc8f9f0f4db08a658de2cf81953d2a39aa67ae70ee0173`)
**Base:** 13-element chain (through `chart_p01`)
**VWMA decision:** **(b) — omitted.** Stated reason: volume in this system is `gauss()` noise generated independently of price action; a volume-weighted indicator over noise volume is arithmetically correct and informationally empty. It awaits volume-generator work (DATA-P03). This is the recommendation the Build Order made, adopted.

| Artifact | sha256 |
|---|---|
| `chart_p02.patch` (== `.txt`, `cmp`-identical) | `084b03c333c9c7ccc8427c033fd724c8bfa52a2174a538c3f91d058de9f51f53` |
| Patch format | 3,285 lines · 16 files · LF-only (CR bytes: 0) · terminating newline |
| Pristine apply | 14th element of the chain; `git apply --check` exit 0 in a fresh clone |

## 1. Scope disposition — and the count stated plainly

The Build Order's table lists **17 indicator rows** under a header that says 15, and a total of
22. The DA counted: 17 rows − VWMA (omitted, §0) = **16 new indicators**; 16 + 7 = **23 total**.
The discrepancy is stated rather than papered over; every row in the table except VWMA was built.

## 2. Requirement mapping — M1–M9

| Req | Delivered | Where |
|---|---|---|
| M1 | ✅ Registry-row extension held: each indicator = formula + registry row + mirrored UI entry. **Two stated contract extensions** (the only endpoint/client architecture changes): (1) the registry gains an `engine` field (S1) and an optional `required_bars_fn` — day/session-derived LEVELS have timeframe-dependent full-definition requirements a static number cannot express; (2) the response gains ONE new variant, `shape:"multi"` (named line series) for multi-line indicators, alongside a backward-compatible optional `detail` on the insufficient variant. The endpoint's path, auth and error semantics are untouched — CHART-P01's extensibility claim held. |
| M2 | ✅ 16 new formulae, every convention declared in code and pinned by a hand-computable test (§5): HMA (WMA(2·WMA(n/2)−WMA(n)) over floor(√n); n/2 floor, √n floor) · Supertrend (ATR bands, band-locking: adopt basic when beyond the previous FINAL band or price closed beyond it; two band lines ONLY — no trend verdict) · Ichimoku (9/26/52; senkou displaced +26, chikou −26) · Stochastic (SLOW 14/3/3) · CCI (0.015 × mean absolute deviation — MAD, not σ) · ROC · ADX/DMI (Wilder; DX→ADX averaging) · Keltner (EMA centre, SMA-seeded; ATR period distinct) · Donchian · Pivots (classic, prior UTC day) · Camarilla (multipliers 1.1/12,/6,/4,/2) · Prev H/L (prior UTC day) · Session Levels (fixed UTC LONDON/NEW YORK windows, weekend-closed) · Z-Score (population σ) · Percentile Rank (midpoint: (less+0.5·equal)/n) · Regression Channel (least squares; width = MAX deviation). |
| M3 | ✅ Full-definition `required_bars`: HMA20 23 (n+√n−1) · SUPERTREND103 11 · **ICHIMOKU952652 78** (52+26) · STOCH1433 18 · CCI20 20 · ROC12 13 · **ADX14 28** (DX at n+1, ADX at 2n) · KELTNER20 20 · DONCHIAN20 20 · PIVOTCL/CAMARILLA/PREVHL floor(1440/tf)+1 (M1 1441 · H1 25 · D1 2) · SESSLVL 540/tf+1 where resolvable (tf ≤ 60 and 540 % tf == 0), **unresolvable otherwise** (typed insufficient with detail on H4/D1) · ZSCORE/PCTRANK/REGCHAN 20. Pinned by `test_chart_p02_required_bars_are_full_definition_not_earliest_drawable`. |
| M4 | ✅ The CHART-P01 discriminant reused unchanged (plus the optional detail noted in M1): zero points, no line, typed counts. Capture 08: Ichimoku on D1 → "insufficient history (78 required, 5 available) — no series rendered", 0 overlay lines machine-recorded. |
| M5 | ✅ Toolbar scales: SMA 20/50/EMA 20 remain direct pills (**same interaction count as today**); five data-driven engine menus (Trend/Momentum/Volatility/Levels/Statistics) expose every other registry indicator; **active** menu indicators surface as tray pills visible at a glance without opening a menu (click = remove). Machine-recorded: menu buttons all inside the stage clip, per-engine item counts 6/6/4/4/3, nothing clipped. |
| M6 | ✅ **Policy stated and enforced in pixels:** at most **3 concurrent pane charts** (90px each, in a scrollable region); the **price pane keeps a 280px minimum**; a 4th pane toggle is **refused explicitly** — status-strip refusal naming the indicator, pane count unchanged, item never activates. Capture 03: price pane measured at exactly 280px with 3 panes; capture 07: refusal text machine-recorded. **Ichimoku displacement:** no point is plotted beyond the last bar — the cloud ends AT the last bar (final 26 values are the live projection at existing positions); the chikou trails 26 bars. The price-pane time axis is never extended. |
| M7 | ✅ Pane time axes track the price pane: `PriceChart` publishes `subscribeVisibleTimeRangeChange` → stage state → every pane applies `setVisibleLogicalRange`. Crosshair sync is not implemented (recommended-only, per the order). **Proven after a zoom:** capture 04 wheel-zoomed the price pane (range narrowed 1787051880→1787052060) and every pane's applied range equals the new price range (`synced: true`, machine-recorded). |
| M8 | ✅ Provenance/series-kind inheritance unchanged — status strips state the displayed series' provenance and the aggregated/native computation basis; unavailable series yields no computation (DATA-P02 path untouched). |
| M9 | ✅ The anchor ("Indicators describe data, they never advise a trade.") stays pinned; the forbidden list now includes the directional folk vocabulary (`buy/sell signal`, `golden/death cross`, `crossover signal`, `bullish`, `bearish`, `oversold`, `overbought`) asserted BOTH in the source residue and at render with indicators active. The source/render split from CHART-P01 is preserved. Guard-extension discrimination recorded: the directional vocabulary was under test nowhere pre-fix; 9/9 terms asserted post-fix (`guard_chart_p02_prefail.log`). |

## 3. Supporting scope — S1–S4

- **S1** — `engine` on both registries; toolbar grouping is data-driven. Golden tests pin the mirror on both sides.
- **S2** — stated strategy: a fixed 24-entry (colour token × line style) palette assigned deterministically from (indicator id, line name); full collision-avoidance at 20+ concurrent lines is not achievable within the token palette — the deterministic assignment plus labelled status strips are the mitigation. Capture 05 renders 19 concurrent level lines legibly.
- **S3** — measured: **all 23 indicators over the standard 100-bar window ≈ 25 ms**; over the extended 2880-bar compute window (levels only) ≈ **801 ms** for all 23 — the endpoint computes only the REQUESTED indicators, so a single toggle is one indicator (10–120 ms; ichimoku 119 ms, session levels 31 ms after the optimisation in §7.3). The per-toggle separate-call strategy still holds (S4).
- **S4** — asserted by call count: toggling never refetches the candle series (existing CHART-P01 test still green; new scaling tests assert fetch counts across menu interactions).

## 4. Constraints — R1–R7

R1 ✅ no generator/aggregation/CHART-P01-formula file modified (the seven CHART-P01 lambdas keep their exact semantics; the registry golden test asserts their positions and properties unchanged). R2 ✅ registry/RBAC untouched; endpoint auth breadth unchanged. R3 ✅ no directional verdict anywhere (M9-gated); Supertrend emits bands only. R4 ✅ vocabulary unchanged. R5 ✅ zero new dependencies — 16 formulae implemented explicitly. R6 ✅ **730.90 → 736.97 kB (+6.07 kB)**, `index-D0H_EgWa.js` sha256 `6336a689cbce5eabbb1994b9a33b47a846efe053d4d9b25a99eb4364421c8c41` → OBS-5. R7 ✅ `PriceChart` still renders, never computes.

## 5. Fail-first + hand-computed fixtures (acceptance 12)

```
pytest tests/test_chart_p02_indicators.py  (PRE-FIX)  exit 2 — no module app.services.indicators.hma…
vitest terminalChartIndicatorsScaling.test.tsx  (PRE-FIX)  exit 1 — 6/6 tests failed (modules absent)
guard-extension  (PRE-FIX) 0/9 directional terms under test → FAILS;  (POST-FIX) 9/9 → PASSES
```

Hand-computed fixtures (verifiable by inspection): HMA(4) on 1..8 → exactly 5,6,7,8; Supertrend
ATR=4 constant-drift band 122 **locked** (price never crossed) / lower 108 following; Ichimoku
tenkan(8)=5, kijun(25)=13.5, senkouB(77)=26.5, senkouA(77)=43.75, chikou(51)=78, nothing beyond
the last bar; Stochastic raw 18/23×100; CCI 126.666…; ROC 1200; ADX +DI 25/−DI 0/ADX 100
(constant drift) with ADX first defined at 2n; Keltner 14.5/10.5/6.5; Donchian 25/−4/10.5;
Pivots P=305/3 with the six R/S levels; Camarilla all eight 1.1-multiplier levels; session
levels 100/80 from a completed Monday London; Z-Score 9.5/√33.25; Percentile 97.5 and the tie
case 50.0; Regression [2,4,9] → 8.5 centre, ±1.0 channel.

## 6. Executed-test position (fresh transcripts, both trees)

| Run | DA tree | Pristine clone (chain + chart_p02) |
|---|---|---|
| pytest | **462 passed** (`pytest_chart_p02_r2.log`) | **462 passed** (`pytest_chart_p02_verify.log`) |
| vitest | **173 files · 844 passed** (`vitest_chart_p02_r2.log`) | **173 files · 844 passed** (`vitest_chart_p02_verify.log`) |
| tsc -b --force | 0 errors | 0 errors |
| npm run build | `index-D0H_EgWa.js` 736.97 kB | identical hash `6336a689…` |

Suite position: **1,306 (462 backend / 844 frontend)** — baseline 1,280 + **26** (+20 backend:
16 hand-computed + full-definition + registry/engine + long-period insufficiency + endpoint;
+6 frontend scaling tests). Build JS sha256 identical in both trees.

## 7. Deviations disclosed unprompted (including failed attempts)

1. **Compute-window extension (M1 note):** day/session LEVELS need a prior UTC day of bars —
   more than the 100-bar displayed window. The endpoint computes over an extended window
   (up to 2880 bars, reusing the native/aggregated series path) and TRIMS every output to the
   displayed window — computation-window extension only; the chart still receives exactly its
   displayed length. Implemented so the extended fetch happens ONLY when a level indicator is
   requested (common path cost unchanged).
2. **Performance defects found and fixed before shipping:** (a) `session_levels` recomputed
   per-session max/min for EVERY bar (quadratic; 1,158 ms) — fixed by precomputing per-session
   stats once (31 ms); (b) the indicator layer re-read ORM attributes per point (1.5M+ attribute
   loads) — fixed by materializing each bar to a plain float dict once at function entry
   (ichimoku 363→119 ms). Both caught by measuring S3, not by tests passing.
3. **HMA full-definition corrected during implementation:** the first fully-seeded HMA needs
   n+√n−1 bars (23 for HMA20), not n — the registry and the gate both state 23.
4. **`lines` shape mismatch caught by the capture gate:** the frontend type modelled
   `lines[name]` as `{points}` while the backend serializes a point list — capture 02 showed 0
   overlay lines and the contract was aligned to the backend. The capture gate did its job.
5. **Pane-height enforcement failed its own policy on first capture:** three panes squeezed the
   price pane to 217px, below the stated 280px minimum — the capture gate refused it; CSS now
   enforces the minimum and panes scroll in their own region (capture 03 shows exactly 280px).
6. **In-memory snapshot loss on backend restart:** the retained `latest_by_symbol` quote
   snapshot is in-memory and was lost when the backend restarted mid-phase with the new code;
   the feed start/stop cycle and the `live:simulated` row deletion were re-run before captures
   (register row TD-UI-CHART-P02-EVIDENCE-FIXTURE). Both restarts are in this report.
7. **Level indicator timeframes:** session levels are resolvable only where the 540-minute
   session divides evenly (M1/M5/M15/H1); H4/D1 return the typed insufficient result with the
   "not resolvable at this timeframe" detail — stated in the registry and tested.
8. **CHART-P01 test updates:** the four non-direct CHART-P01 pills moved into engine menus
   (M5 permits this — only the three most-used are interaction-pinned); the CHART-P01 tests'
   toggles were updated to the menu contract (test-contract update, not weakening — the same
   assertions run).
9. **Register rows carried by this patch:** `TD-UI-CHART-P02-EVIDENCE-FIXTURE` (new) and
   `OBS-CHART-1` (the CHART-P01 review-time observation, first hash-reconciled in patch form —
   the established pattern for review-time register edits).

## 8. Level-I captures (image primary; instruments corroborate)

| Capture | sha256 | Gate result |
|---|---|---|
| 01 toolbar 23 grouped | `fbe1e9085f8c11ff162d8410acf0bf84df2b81e907416265e2cd7172e428d64c` | 5 menus present, item counts 6/6/4/4/3, ink inside clip, hit-tests self ✅ |
| 02 trend overlays | `d8f0aa36db2af02fd3ce30bc1a1ccc988eac48c20a0897f3fd9bb07154897d76` | 7 overlay lines recorded; envelope multi shapes with named lines ✅ |
| 03 momentum panes | `7c613801ea13307f0b1f50b133da24c83ea142b8bce5aa40e1d91275beaec861` | 3 panes; price pane exactly 280px; stacked, no overlap ✅ |
| 04 time-axis sync after zoom | `34a0d823300c500db848ae0f52fd0f28d26553c5f83a9596b06ad3d96148dfc0` | zoom narrowed the range; every pane's applied range equals it (`synced: true`) ✅ |
| 05 levels 19 lines | `fecf915dfda2306d53543411679ff040eb139da3b0bd27048149cf3d1896261b` | 19 overlay lines recorded; statuses legible ✅ |
| 06 statistics | `54e7f255e19e6642142ace63dd12387d649ff0283931577a331f93bceef05def` | 4 overlay lines recorded ✅ |
| 07 pane budget refusal | `61339785326c538db855081d8ab6d1e9f030d395fb4359d4b44bd313300323ae` | refusal explicit, panes stay 3, item never active ✅ |
| 08 insufficient on 1D | `9622a0a56734d720dc95e34d6edb98bb3ef2b2288d18e8e8b5e4d75471e7c720` | 78/5 typed, 0 lines, status legible ✅ |

- `CHART-P02_CAPTURE_VERIFICATION.json` (Rev A) sha256 `7da21fadd4c5b2b5fc7d20ffd5a7dd9727b1ec6e48907f340f7d4683a857e029` (`.txt` `cmp`-identical)
- `CHART-P02_CAPTURES.html` (self-contained gallery) sha256 `a8bd8ba66ec7ecb46107b19d1261a3cf49faa65efcf51dd99efc42dc366e4e30`

## 9. Acceptance criteria

1–16 addressed as mapped; criterion 15 (patch applies clean on the 13-element chain, sha256
declared and matching) verified in a pristine clone; criterion 16 (bundle delta) reported in §4.
The artifact of record is the verified patch, not a commit — no commits, pushes or pulls.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This delivery implements CHART-P02 only; it is not authorization for CHART-P03 or POLISH.

**We don't guess. We prove.**
