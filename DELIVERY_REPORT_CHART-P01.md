# DELIVERY REPORT — CHART-P01 (Technical indicators: honest controls, server-side computation)

**Delivered by:** AXIOM Development Authority
**To:** ITRGA
**Date:** 2026-08-18
**Build Order:** `BUILD_ORDER_CHART-P01.md` (sha256 `d9c27aac083a85817def26d3613171fb19a903354844375d810b928658ddea52`; preceded by `ITRGA_INVENTORY_CHART_PRE-BUILD-ORDER.md` and `ITRGA_ASSESSMENT_AXIOM_ANALYTICS_ENGINE.md`, both ingested)
**Base:** 12-element chain (through `data_p02`)
**Central defect:** `F-CHART-1` — the SMA 20 / SMA 50 / EMA 20 pills toggled inert booleans used only for their own `active` class; no SMA/EMA computation existed anywhere, and `PriceChart` declared it computed none.

| Artifact | sha256 |
|---|---|
| `chart_p01.patch` (== `.txt`, `cmp`-identical) | `6e141e9ab7d27bf0d58f59dde87e8a28b0d4d15d85ca95ab54f148687cb143e1` |
| Patch format | 2,635 lines · 18 files · LF-only (CR bytes: 0) · terminating newline |
| Pristine apply | 13th element of the chain; `git apply --check` exit 0 in a fresh clone |

---

## 1. Scope disposition

Seven indicators built: **SMA 20 · SMA 50 · EMA 20** (making the existing controls honest)
plus **RSI 14 · MACD (12/26/9) · Bollinger (20, 2σ) · ATR 14**. Volume indicators,
order-flow, liquidity-pool claims, the Confluence engine and drawing tools were not
touched — out of scope per the Build Order and the assessment. **R1:** no DATA-P01
generator file and no DATA-P02 aggregation file appears in the patch.

## 2. Requirement mapping — M1–M8

| Req | Requirement | Delivered | Where |
|---|---|---|---|
| M1 | Server-side computation | ✅ | `backend/app/services/indicators.py` (pure functions) + `indicator_registry.py`; served by `GET /api/v1/persistence/indicator-series` (same `CurrentOperatorDep` auth pattern). Nothing is computed in the browser. |
| M2 | Correct, verifiable formulae | ✅ — **stated rules**: SMA = arithmetic mean of last n closes; **EMA seeding rule: SMA-seeded** (first EMA = SMA of the first n closes; α = 2/(n+1)) — the traditional charting convention, deterministic and self-consistent; **RSI: Wilder's smoothing** (first avgGain/avgLoss = plain means, then (prev·(n−1)+change)/n); MACD = EMA12−EMA26, signal = EMA9 of the line (SMA-seeded), histogram = MACD−signal (signal/histogram **null until seeded — absence, never 0**); **Bollinger: ±2 population standard deviations** (divide by n); ATR = true range with Wilder's smoothing. Each pinned by a hand-computable test (§5). |
| M3 | The three controls become functional | ✅ | The pills drive real fetches and real overlay series; `active` ⇔ visible line; Bollinger/RSI/MACD/ATR pills added per scope. **F-CHART-1 closed** (capture 01: two real lines, both pills active). |
| M4 | Insufficient history — typed, never padded | ✅ | `{shape:"insufficient", required, available}` per indicator; the endpoint gates on the registry's full-definition `required_bars` BEFORE computing; the client renders "insufficient history (50 required, 5 available) — no series rendered" and draws **no line** (capture 05, machine-recorded 0 overlay lines). Full-definition requirements: SMA20 20 · SMA50 50 · EMA20 20 · RSI14 15 (14 changes) · MACD 34 (26 for the line + 9 MACD values for a seeded signal) · Bollinger 20 · ATR 15 (14 true ranges). |
| M5 | Derived-value provenance | ✅ | Status strip states `derived from {provenance} OHLC` where `{provenance}` is the DISPLAYED series' provenance (seed:synthetic / live:simulated / the joined form) — never a new marker, never more authoritative than the bars beneath it. |
| M6 | Respects the DATA-P02 series kind | ✅ | The envelope carries `seriesKind` + `excludedPartialBuckets`; the status strip discloses `computed over aggregated H1 series (2 partial bucket(s) excluded)`; **an unavailable series yields no computation** (`seriesKind:"unavailable"`, empty `indicators`, detail stated — endpoint test + capture in the DATA-P02 style). |
| M7 | Determinism | ✅ | Inputs are sorted defensively inside every function; repeat calls and shuffled inputs produce identical points (pinned at function and wire level). |
| M8 | T-1 guard with non-vacuity anchors | ✅ | Anchor sentence **"Indicators describe data, they never advise a trade."** — `.replace()`d out, residue must be free of advisory vocabulary (`trade recommendation`, `eligibility`, `setup quality`, `risk/reward`); the actuation vocabulary (`buy`, `sell`, `execute`, `order_ticket`, `position`, … — the standing watchlist list) is asserted **at render** over the whole indicator surface with indicators active. Why the split is stated in the test: the annotation guard legitimately lists actuation terms as REJECTION tokens in source, so a source-residue check for those terms would be vacuous. Guard discrimination on the record: FAILS on the pre-fix source, PASSES on the delivered (`guard_chart_p01_prefail.log`). |

## 3. Supporting scope — S1–S4

- **S1 — single registry:** `backend/app/services/indicator_registry.py` (id, label, pane, required_bars, compute) + frontend mirror `frontend/src/api/indicatorRegistry.ts` (labels, panes, testids, colors); both sides pinned by golden tests; unknown ids are a 422. CHART-P02 = formula module + registry row.
- **S2 — separate panes:** RSI/MACD/ATR render in their own stacked `lightweight-charts` instances BELOW the price pane (capture 03 measured: price pane y 251.6–611.3, panes 611.3–745.1 / 745.1–879; `stacked: true`). Note, not a deviation: crosshair/time-axis sync between panes is not implemented; panes independently fit their content.
- **S3 — strategy stated:** computed via a **separate call**, per toggle, for the toggled indicator only; the candle series is NEVER refetched by a toggle (asserted: `fetchCandles` call count unchanged across toggles). Results are cached per timeframe; a timeframe switch clears the cache and refetches the active set.
- **S4 — measured cost:** all seven indicators over the largest served window (100 bars): **5.0 ms median** (min 4.9 / max 5.2). Context: 546 ms over the full 8,640-bar seed — the endpoint never serves that window.

## 4. Constraints — R1–R7

| Constraint | State |
|---|---|
| R1 | ✅ no `chart_seed_service.py` / `adapters/simulated.py` / `live_service.py` / `ohlcv_aggregation.py` in the patch |
| R2 | ✅ RBAC unchanged — `workspaceRegistry.tsx` not in the patch; the endpoint was added to the auth-breadth test (401 without bearer, 200 with) |
| R3 | ✅ no actuation anywhere; no recommendation, eligibility or verdict output (M8-gated) |
| R4 | ✅ provenance vocabulary unchanged — indicators carry the displayed series' existing markers |
| R5 | ✅ zero new dependencies (both manifests untouched); formulae implemented explicitly |
| R6 | ✅ bundle `724.50 → 730.90 kB` (**+6.40 kB**), `index-DmzkpJL_.js` sha256 `574ef7c7f365ecccbdfd6f58026bf302efb80562c79b6bee80af1756fb031198` — rolls into OBS-5 |
| R7 | ✅ `PriceChart`'s contract ("does not compute indicators") remains true — it RENDERS precomputed `overlayLines`; the docblock was extended to state the CHART-P01 division of labour |

## 5. Fail-first demonstration (acceptance 11)

Raw transcripts in `docs/evidence/uiconv/`:

```
pytest  tests/test_chart_p01_indicators.py     (PRE-FIX)  exit 2 — ModuleNotFoundError:
        No module named 'app.services.indicators'   (all 13 tests uncollectable)
vitest  terminalChartIndicators.test.tsx       (PRE-FIX)  exit 1 — missing modules
guard   (PRE-FIX source)  anchorPresent:false  => GUARD FAILS
        (POST-FIX source) anchorPresent:true advisoryVocabularyAbsent:true => GUARD PASSES
```

Hand-computed fixtures (M2, verified by inspection): SMA [1..5] n=3 → 2,3,4; EMA same series
SMA-seeded → 2,3,4 with α=0.5; RSI Wilder: 14 gains of +1 → 100 at bar 14, then a −14 bar →
48.148… (100−1400/27); MACD spot value: 26 closes at 1000 then one at 1351 → MACD(26) = **28.0
exactly** (signal null until seeded); Bollinger [1..20]: mean 10.5, σ=√33.25, upper = 10.5+2σ;
ATR: 14 TRs of 1 then TR 15 → ATR = 1.0 then exactly 2.0.

## 6. Executed-test position (fresh transcripts, both trees)

| Run | DA tree | Pristine clone (chain + chart_p01) |
|---|---|---|
| pytest | **442 passed** (`pytest_chart_p01_r1.log`) | **442 passed** (`pytest_chart_p01_verify.log`) |
| vitest | **172 files · 838 passed** (`vitest_chart_p01_r1.log`) | **172 files · 838 passed** (`vitest_chart_p01_verify.log`) |
| tsc -b --force | 0 errors | 0 errors |
| npm run build | `index-DmzkpJL_.js` 730.90 kB | identical hash (`574ef7c7…`) |

Suite position: **1,280 (442 backend / 838 frontend)** — baseline 1,258 + **22** (+13 backend:
8 named + 2 endpoint + registry + insufficient/unavailable + determinism; +9 frontend). Build
JS sha256 identical in both trees — byte-level reproducibility.

## 7. Level-I captures (image primary; instruments corroborate)

Viewport 1920×1080, deviceScaleFactor 1, Chromium 151.0.7922.34 headless. Environment
machine-recorded: feed stopped (platform's own control), watchlist quotes from the retained
`live:simulated` snapshot, persisted candles seed-only (95,040 M1 rows / 6 days — the DATA-P02
fixture REUSED unchanged; register row `TD-UI-CHART-P01-EVIDENCE-FIXTURE`). Canvas line
presence is corroborated by machine-recorded DOM state (`data-active-overlay-lines`,
`data-active-indicator-panes`, `data-active-indicator-ids`), pane geometry, and API envelopes;
the images are primary for the lines themselves. The legibility instrument (box, ink rect,
stroke extent, hit-test) gated every capture's text elements.

| Capture | sha256 | Gate result |
|---|---|---|
| `CHART-P01_01_SMA20_SMA50_REAL_LINES.png` | `52ef65e588af9060997a185a6c5513a2ab1ccdec568f2d8e8152247c10ccdd44` | F-CHART-1 proof: both pills active, 2 overlay lines (DOM-recorded), statuses computed ✅ |
| `CHART-P01_02_EMA20_VS_SMA20_DIVERGENCE.png` | `ccbff2a11fadd1137cbda8b81ae3f8623da5ab719c868e2562dac491deda46b3` | two distinct lines, both pills active ✅ |
| `CHART-P01_03_RSI_MACD_SEPARATE_PANES.png` | `198a3e335a6cc2fe1f0adfb2b7fe854e249a5c53b699444a94b2aacc3f91ee6d` | 2 panes stacked below the price pane (`stacked: true`, rects measured) ✅ |
| `CHART-P01_04_BOLLINGER_BANDS.png` | `77803546300d7c57b8bc064c3f6e45016dd204938ab4c2388e0bca72d35edae7` | 3 overlay lines (upper/middle/lower), DOM-recorded ✅ |
| `CHART-P01_05_INSUFFICIENT_HISTORY_NO_LINE.png` | `f94f3d4379979d9347666436af67b91b99411ac4049068495fdcc1e75732dd90` | typed insufficient (50 required, 5 available), **0 lines** ✅ |
| `CHART-P01_06_ALL_INDICATORS_OFF_CLEAN.png` | `a73dbfc54abe3f5eaac8563303296bfbaba58981cf6ce05191a8ff5c3c1abf9b` | clean chart, no residue (status strip count 0) ✅ |

- `CHART-P01_CAPTURE_VERIFICATION.json` (Rev A) sha256 `74a7a324b6738fc272806909000e276c3b4eaef065f56c232799c802aa511677` (`.txt` upload copy `cmp`-identical)
- `CHART-P01_CAPTURES.html` (self-contained gallery, per-image SHA-256, alt text stating measured values only) sha256 `59a0e4ae467657d66f4f95a012f2194f94e711bdcff36f7503b4cec90654cd4e`

## 8. Deviations disclosed unprompted (including failed attempts)

1. **Fourth inert control found and removed:** the Build Order asked the DA to report a
   fourth inert control if found. `TechnicalOverlayState.volume` existed as state (default
   `true`) with **no pill and no consumer** — dead chrome inside the same defect class.
   Removed (state field, interface, barrel export); the honest tooltips on the remaining
   pills were reworded ("computed server-side from the displayed series; descriptive, never
   prescriptive") to replace the pre-fix "Presentation Only" acknowledgement of inertness.
   A sweep of the other terminal components found no further inert toggles.
2. **MACD signal-line availability:** with 26–33 bars the MACD LINE is computable but the
   signal is not seeded; the registry declares `required_bars: 34` (full definition) and the
   endpoint returns the typed insufficient result below that — a partially-seeded MACD is
   never presented as the full indicator.
3. **RSI/ATR history requirements:** both need n+1 bars (n changes / n true ranges). Stated
   in the registry (`RSI14: 15`, `ATR14: 15`) — a deliberate, documented asymmetry against
   the naive "period = bars" reading.
4. **Indicator boundary UTC handling aligned with the aggregation boundary:** the first
   implementation rejected SQLite-naive `open_time` values (`require_utc` raise) — caught by
   the S4 measurement harness, not by the endpoint tests (the service path passes
   tz-normalized `CandleRead`s). The boundary now assumes UTC for naive values (the storage
   invariant; the driver strips tzinfo on read), matching DATA-P02's `ohlcv_aggregation`.
5. **Status-derivation ordering bug caught by the new tests before shipping:** an
   `unavailable` envelope was checked AFTER the missing-result branch, so the status would
   have shown "loading…" forever. Reordered (unavailable first); the regression test now
   pins the behaviour.
6. **Capture artifact naming corrected mid-cycle:** capture 02 was initially written as
   `CHART-P02_02_…` (typo); the file was renamed to `CHART-P01_02_…` and the JSON record's
   file field corrected BEFORE the verification JSON was finalized — disclosed rather than
   silently fixed, per the standing standard.
7. **Environment restore:** the sandbox dropped the Playwright chromium binary and the apt
   graphics libraries between turns; both were reinstalled before any capture ran.
8. **Capture fixture reuse:** the CHART-P01 captures run on the same local six-day seed the
   DATA-P02 captures used (95,040 seed-only rows; feed-stopped snapshot cycle with
   `live:simulated` rows deleted). Register row `TD-UI-CHART-P01-EVIDENCE-FIXTURE` records
   the reuse and the D1 = 5-bars property capture 05 depends on.

## 9. Acceptance criteria

1–15 addressed as mapped above; criterion 14 (patch applies clean on the 12-element chain,
sha256 declared and matching) verified in a pristine clone; criterion 15 (bundle delta)
reported in §4. The artifact of record is the verified patch, not a commit — no commits,
pushes or pulls were performed.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This delivery implements CHART-P01 only; it is not authorization for CHART-P02/P03 or POLISH.

**We don't guess. We prove.**
