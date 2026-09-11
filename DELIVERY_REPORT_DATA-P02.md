# DELIVERY REPORT — DATA-P02 (Multi-timeframe aggregation & session context)

**Delivered by:** AXIOM Development Authority
**To:** ITRGA
**Date:** 2026-08-18
**Build Order:** `BUILD_ORDER_DATA-P02.md` (sha256 `7177e80c31dc4a3694ad28e85464fca96edf20cfd7165c57f0c98de8c9d8f53e`)
**Base:** 11-element chain (`34f4c62` → item3 → item5 → item6 → item4(Rev B) → surf_p01 → surf_p01_obs1-2 → surf_p02 → surf_p03 → data_p01 → data_p01_correction → data_p01_correction2)
**Central defect:** `F-DATA2-1` — the UI offered 1m/5m/15m/1h/4h/1d while the database stores M1 only; the client fell back to M1 and rendered it 1:1 under a higher-timeframe label, with a TD-029 notice describing a resampling that never happened.

| Artifact | sha256 |
|---|---|
| `data_p02.patch` (== `.txt`, `cmp`-identical) | `69509b49e2738518e1414d4a13169294bdc628a309b6de8249954bc4227e7e90` |
| Patch format | 2,877 lines · 33 files · LF-only (CR bytes: 0) · terminating newline |
| Pristine apply | 12th element of the chain; `git apply --check` exit 0 in a fresh clone |

---

## 1. Scope disposition

Re-inventoried against the tree as instructed: per-instrument volatility regime **excluded**
(already built and surfaced — Risk & Drawdown dock), watchlist clip and bundle size left to
POLISH, and **no DATA-P01 generator/seed/provenance code was touched** (R1: none of those
files appear in the patch). Session context is built as presentation and labelling only —
no time-of-day volatility was added to the walks, and none is recommended at this time.

## 2. Requirement mapping — M1–M8

| Req | Requirement | Delivered | Where |
|---|---|---|---|
| M1 | Server-side OHLC aggregation, wall-clock buckets | ✅ | `backend/app/services/ohlcv_aggregation.py` — `aggregate_m1_to_target`: per bucket **open = first constituent's open · high = max · low = min · close = LAST constituent's close · volume = sum**; `bucket_start_for` floors to UTC wall-clock boundaries (H1 starts on the hour, D1 at UTC midnight). Named tests assert the exact semantics on known input. |
| M2 | Aggregation exposed through the API | ✅ — **dedicated endpoint, stated choice below** | `GET /api/v1/persistence/candle-series` (`backend/app/api/routes/persistence.py`), same auth pattern as the raw listing (`CurrentOperatorDep` + session dependency). *Why a new endpoint rather than morphing `/candles`: the raw listing keeps its exact list contract for existing consumers (lifecycle tests, audit surfaces); the typed series envelope gets its own response model instead of a polymorphic overload of an established route.* |
| M3 | Client 1:1 fallback removed | ✅ | `TerminalChartStage.tsx` — the `rawCandles.length === 0 && timeframe !== "1m"` M1 fallback is deleted; the series state is the server's discriminant. Unavailable ≠ empty: no improvised series, and unaggregated M1 bars are never passed off as a higher timeframe again. Guard-pinned (M8) and test-pinned (`test_data_p02_no_m1_fallback_when_higher_timeframe_has_no_native_records`: exactly one request per switch, no M1 re-fetch). |
| M4 | Three-state typed provenance on the response | ✅ | `CandleSeriesEnvelope` (backend) / `CandleSeriesResult` (frontend): `native \| aggregated {sourceTimeframe: "M1", excludedPartialBuckets} \| unavailable {detail}`. The discriminant is carried on the wire; consumers never match message strings or bar counts. |
| M5 | TD-029 notice becomes true | ✅ | The notice renders **only** for `kind: "aggregated"` and states the facts: `Resampled from M1 stream · wall-clock aligned {N}-minute buckets` + `· {k} partial bucket(s) excluded` when k > 0. Native shows the existing "Native M1 Stream" tag; unavailable shows a distinct red tag and the absence state in the canvas. Annotation `resolution` now records `native \| aggregated \| unavailable` — what actually happened, never a hardcoded `"resampled"`. |
| M6 | Partial buckets disclosed, never padded | ✅ — **chosen rule stated**: a bucket with fewer than the full complement of constituent minutes is **excluded from the series and disclosed** via `excludedPartialBuckets` + the notice + the unavailable detail (which reports stored-bar and partial-bucket counts). This includes the trailing, still-forming bucket. No bar with missing constituents is ever rendered; no padding of any kind. |
| M7 | Session context | ✅ | `frontend/src/terminal/sessions.ts` + `SessionContextStrip` — Tokyo 00:00–09:00 / London 07:00–16:00 / New York 12:00–21:00 **fixed UTC windows**; overlap periods labelled (Tokyo∩London 07:00–09:00, London∩NY 12:00–16:00); weekends render MARKET CLOSED (WEEKEND). The strip shows the current UTC moment's session + overlap + clock, the series-span sessions, and — via a presentation-only crosshair callback (`PriceChart` `onBarHover`) — **the session of the bar under the crosshair**. Purely labelling over existing data; no generator touched. **Convention disclosed:** boundaries are pinned to fixed UTC windows (DST-agnostic); real-market DST shifts and the Sunday 21:00 Sydney open are outside this labelling model. |
| M8 | T-1 guard with non-vacuity anchors | ✅ | `test_data_p02_honesty_anchor_present_and_hardcoded_notice_trigger_absent` — anchors `"wall-clock aligned"`, `.replace()`s it out, then asserts the residue contains **no** `timeframe !== "1m"`, **no** `"native" : "resampled"`, **no** `rawCandles.length === 0`. Discrimination demonstrated on the record: against the pre-fix source all four assertions fail; against the delivered source all four pass (`guard_data_p02_prefail.log`). |

## 3. Supporting scope — S1–S3

- **S1 — determinism & order-independence:** constituents are sorted by open_time inside each bucket and bar ids derive from (symbol, target timeframe, bucket start), so output is identical regardless of input ordering or repeat calls. Pinned by `test_data_p02_aggregation_deterministic_and_order_independent` (forward vs reversed input, repeat calls — fingerprints equal).
- **S2 — single source of truth:** the backend owns the canonical vocabulary (`app/services/timeframes.py`: six codes, minutes per bucket, labels); the frontend mirrors the identical golden table (`frontend/src/api/timeframes.ts`) and both sides pin it with tests (`test_data_p02_timeframe_vocabulary_golden_table` / `test_data_p02_frontend_timeframe_table_matches_backend_golden`). Divergence cannot render silently: the API timeframe pattern rejects unknown codes with 422, which the client surfaces as an error state.
- **S3 — performance:** aggregation is computed per request and measured (raw transcript in this report's evidence set): **D1 over 8,640 M1 rows ≈ 25.3 ms median** (min 25.0 / max 27.1); H1 ≈ 40.3 ms. Negligible at the synthetic-data scale; stated for the record.

## 4. Constraints — R1–R6

| Constraint | State |
|---|---|
| R1 — DATA-P01 generators untouched | ✅ none of `chart_seed_service.py`, `adapters/simulated.py`, `config.py`, betas, seeds or provenance values appear in the patch |
| R2 — RBAC unchanged | ✅ `workspaceRegistry.tsx` is **not** in the patch; no registry/route/role change; the new endpoint follows the existing `CurrentOperatorDep` pattern and was added to the auth-breadth test (401 without bearer, 200 with) |
| R3 — constitutional boundaries | ✅ no actuation, no external LLM, no plugins; simulated data remains explicitly labelled at every surface |
| R4 — single provenance value | ✅ aggregated bars carry only the existing markers; mixed buckets join them canonically (`seed:synthetic+live:simulated`, seed first) — pinned by `test_data_p02_aggregation_provenance_never_weakened` (never null, never `resampled`) |
| R5 — no new dependencies | ✅ zero additions to either manifest |
| R6 — bundle delta | ✅ `720.67 → 724.50 kB` (**+3.83 kB**), `index-Dkwlfi1U.js` sha256 `8c17f7e14815d6e5e884de79e523acb26fbcd45232c18660d728757810107962` — rolls into OBS-5 |

## 5. Fail-first demonstration (acceptance 10)

Raw transcripts in `docs/evidence/uiconv/`:

```
pytest  tests/test_data_p02_aggregation.py  (PRE-FIX)  exit 2 — ModuleNotFoundError:
        No module named 'app.services.ohlcv_aggregation'  (all 6 backend tests uncollectable)
vitest  terminalChartTimeframes.test.tsx     (PRE-FIX)  exit 1 — missing modules (timeframes/sessions)
guard   (PRE-FIX source)  anchorPresent:false hardcodedNoticeTriggerAbsent:false
        hardcodedResolutionAbsent:false m1FallbackAbsent:false  => GUARD FAILS
        (POST-FIX source) all true                              => GUARD PASSES
```

## 6. Executed-test position (fresh transcripts, both trees)

| Run | DA tree | Pristine clone (chain + data_p02) |
|---|---|---|
| pytest | **429 passed**, 1 warning in 121.26s (`pytest_data_p02_r1.log`) | **429 passed** in 114.46s (`pytest_data_p02_verify.log`) |
| vitest | **171 files · 829 passed** (`vitest_data_p02_r1.log`) | **171 files · 829 passed** (`vitest_data_p02_verify.log`) |
| tsc -b --force | 0 errors (`tsc_data_p02_r1.log`) | 0 errors (`tsc_data_p02_verify.log`) |
| npm run build | `index-Dkwlfi1U.js` 724.50 kB (`vite_build_data_p02_r1.log`) | identical hash (`vite_build_data_p02_verify.log`) |

Suite position: **1,258 (429 backend / 829 frontend)** — baseline 1,240 + **18** (+8 backend
DATA-P02 named tests, +10 frontend DATA-P02 tests). Build JS sha256 identical in both trees
(`8c17f7e1…`) — byte-level reproducibility.

**New backend named tests** (all fail-first, all now green): `test_data_p02_aggregation_ohlc_semantics_correct`,
`test_data_p02_aggregation_bucket_boundaries_wall_clock_aligned`,
`test_data_p02_aggregation_deterministic_and_order_independent`,
`test_data_p02_partial_bucket_disclosed_not_padded`,
`test_data_p02_aggregated_kind_from_controlled_window`,
`test_data_p02_series_kind_discriminates_native_aggregated_unavailable`,
`test_data_p02_aggregation_provenance_never_weakened`,
`test_data_p02_timeframe_vocabulary_golden_table`.

## 7. Level-I captures (image primary; instrument corroborates)

Viewport 1920×1080, deviceScaleFactor 1, Chromium 151.0.7922.34 headless.
Environment machine-recorded in the JSON: feed stopped (platform's own control), watchlist
quotes from the retained `live:simulated` snapshot, persisted candles seed-only
(95,040 M1 rows / 6 days — fixture, §8).

| Capture | sha256 | Gate result |
|---|---|---|
| `DATA-P02_01_1M_NATIVE_NO_RESAMPLED_NOTICE.png` | `04a91476f66491ea87986bd859aecf802d3ab6615ef7900ae726420de506b48f` | native notice present, resampled count 0, ink fully inside the stage, hit-test self ✅ |
| `DATA-P02_02_1H_AGGREGATED_NOTICE_TRUE.png` | `d2224f8defcd719c658b962f7fe2f7643a9c79187876ab2b472edc36d8e52a3f` | notice `…wall-clock aligned 60-minute buckets · 2 partial bucket(s) excluded`; envelope 100 hour-aligned complete bars ✅ |
| `DATA-P02_03_1D_AGGREGATED_DAY_BOUNDARIES.png` | `640b0a470adf81f6612ef0ec9ca1a1a82917a2924731134587eb6ec1d020fb22` | envelope 5 bars, **all at UTC midnight** (`T00:00:00Z`), 1440/1440 constituents ✅ |
| `DATA-P02_04_UNAVAILABLE_STATE_HONEST_ABSENCE.png` | `7b0562d4e8e7185d031a83ab9980e8cb12ad31c7f63495ef6df8eb89616a72f4` | REAL backend `kind=unavailable` (no interception); absence state legible; no resampled/native notice ✅ |
| `DATA-P02_05_SESSION_CONTEXT_HOVER_READOUT.png` | `ad1339b339221ed5819b23881bf27f8cf89292c0d54f72fb2edac61c0e9c802b` | displayed session labels recomputed from the displayed clock/bar times and matched exactly; crosshair hit-tested before the hover ✅ |

Capture 02 vs capture 01 of the same window: 100 **hourly** OHLC bars (hour-aligned, 60/60
constituents each) versus 100 **minute** bars — the aggregation is visible in the image, not
inferred. The legibility instrument records layout box, ink rect (DOM Range), painted-stroke
extent (canvas), and a hit-test at each required element's rightmost pixel, with hard gates
that fail the run on any violation (the same instrument standard set by DATA-P01 cycle 3).

- `DATA-P02_CAPTURE_VERIFICATION.json` (Rev A) sha256 `9341a53879b5fcdb7f567ffb50741781c7392832dccf77dc3ccb0dc69dab1c4a` (`.txt` upload copy `cmp`-identical)
- `DATA-P02_CAPTURES.html` (self-contained gallery, per-image SHA-256, alt text stating measured values only) sha256 `9f053f1e5fff039d2f2aa4687b5ba483565c92c0c80efff4f75ba062af26a9ae`

## 8. Deviations disclosed unprompted (including failed attempts)

1. **Evidence fixtures (register row `TD-UI-DATA-P02-EVIDENCE-FIXTURE`):** six days of M1
   seed history (8,640 bars × 11 symbols = 95,040 rows) inserted into the LOCAL dev database
   via the existing `chart_seed_service.seed_chart_history` seam — the same service the
   authenticated `seed-history` endpoint uses, invoked with a larger bars argument. Capture 04
   removed USDCHF's M1 rows so the real backend aggregation path returned `kind=unavailable`;
   rows restored afterwards and verified at 8,640. Feed stopped at capture time; quotes from
   the retained snapshot. Database file local-only and gitignored.
2. **Register delta carried by the patch includes the two DATA-P01 cycle-3 rows**
   (`TD-UI-DATA-P01-EVIDENCE-ENVIRONMENT-FIXTURE`, `OBS-DATA-P01-WATCHLIST-CLIP`) which cycle 3
   declared in its correction report but could not ship in patch form (cycle 3 shipped no
   patch). They are now hash-reconciled as part of the artifact of record; their content is
   unchanged from the cycle-3 disclosure.
3. **Behavior change beyond the cited lines:** the live M1 tick merge in the chart stage is
   now restricted to `kind: "native"` series — a 1-minute live bar must never be merged into
   an H1/H4/D1 series (granularity honesty implied by M4/M6). Aggregated series re-fetch when
   a new M1 minute closes so the last completed bucket stays current.
4. **Test contract updates across 11 existing frontend test files** (mock envelopes for the
   new `fetchCandles` return type). No failing test was deleted or weakened to force green;
   every assertion change is the contract change M4 mandates.
5. **Failed attempts, on the record:** (a) first aggregation implementation had a
   bucket-flooring defect (hour kept + floored minutes added = +10h shift) — caught by the
   new boundary test before anything shipped; (b) the API-level aggregated test hit a
   fixture-ordering 401 (login performed against a pre-reinit engine) — fixed by inline
   login, the ordering hazard documented in the test; (c) the capture script's D1 gate
   initially read a field that existed only on its record object — fixed; (d) the seed script
   first failed with `ModuleNotFoundError: app` (script dir on sys.path) — fixed with
   `PYTHONPATH=.`; (e) Playwright's chromium binary and six apt libraries were absent after
   environment restore — reinstalled before any capture ran.

## 9. Acceptance criteria

1–14 addressed as mapped in §2–§8; criterion 13 (patch applies clean on the 11-element chain,
sha256 declared and matching) verified in a pristine clone; criterion 14 (bundle delta)
reported in §4. The artifact of record is the verified patch, not a commit — no commits,
pushes or pulls were performed.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This delivery implements DATA-P02 only; it is not authorization for CHART or POLISH.

**We don't guess. We prove.**
