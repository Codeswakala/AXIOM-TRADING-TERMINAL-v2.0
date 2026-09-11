# ITRGA DETERMINATION — DATA-P02

**Reviewing body:** Independent Technical Review & Governance Authority
**Subject:** DATA-P02 — server-side multi-timeframe aggregation, typed series discriminant, session context (`F-DATA2-1` fix)
**Date:** 2026-08-18
**Base:** 11-element chain (through `data_p01_correction2`)
**Verification:** `/tmp/d2` — pristine clone → 11-element chain → DATA-P02 applied

| Artifact | sha256 | Size |
|---|---|---|
| `data_p02.patch.txt` | `69509b49e2738518` | 2,877 lines · 33 files |
| `DELIVERY_REPORT_DATA-P02.md` | `24ac6089ef8f4642` | 159 lines |
| `DATA-P02_CAPTURE_VERIFICATION.json.txt` | `9341a53879b5fcdb` | 366 lines |
| 5 PNGs | all reconcile, no dupes | — |

Declared patch hash matches computed. `git apply --check` **exit 0**. **Thirteenth consecutive hash-reconciled delivery.**

---

## 1. DETERMINATION

# APPROVED WITH OBSERVATIONS

`F-DATA2-1` is **CLOSED**. The fabricated interval is gone: aggregation is real, server-side, wall-clock aligned, and proven by direct execution against known input. Every mandatory requirement M1–M8 is satisfied and every constraint R1–R6 honoured.

One observation is raised — `OBS-DATA2-1` — concerning what the six-day capture history reveals about the DATA-P01 walk. It is **not** a DATA-P02 defect and requires no rework in this phase.

---

## 2. ✅ M1 / M6 / S1 — AGGREGATION PROVEN BY EXECUTION, NOT INSPECTION

I did not accept the docstring. I loaded `ohlcv_aggregation.py` directly, fed it 60 M1 bars with **planted extremes at minute 37** and **deliberately shuffled input order**, and measured the output:

| Field | Result | Expected |
|---|---|---|
| `open` | `1.10` | first **by time** despite shuffle ✅ |
| `high` | `1.9999` | planted maximum ✅ |
| `low` | `0.0001` | planted minimum ✅ |
| `close` | `1.1060` | minute-59 close ✅ |
| `volume` | `6000` | summed ✅ |
| `complete` | `True`, 60 constituents | ✅ |

**Order independence (S1):** re-shuffled with a different seed → `out.bars == out2.bars` → **`True`**.

**Partial buckets (M6):** 40 of 60 minutes → **0 bars emitted, 1 excluded**. Not padded, not truncated, not silently rendered. The `AggregationOutcome` carries `excluded_partial` so the caller must disclose it — and the UI does, visibly: *"2 partial bucket(s) excluded"* in capture 02.

**Wall-clock alignment:** `09:37 → 09:00` (H1) and `09:37 → 00:00` (D1). Bucket keys are floored to real clock boundaries, not to result-set position. This is the specific defect the Build Order named — *"never every Nth row"* — and it is correctly avoided.

**Provenance join (R4):** `joined_provenance(["live:simulated","seed:synthetic","seed:synthetic"])` → `"seed:synthetic+live:simulated"`. Canonical order, deterministic, no invented marker. Backend-wide grep confirms the vocabulary is still exactly two values.

---

## 3. ✅ M2 / M3 / M4 / M5 — THE DISCRIMINANT IS REAL

**M4** — `CandleSeriesResult` is a genuine discriminated union (`client.ts:1533`), and critically the `kind` is a **server-side `Literal["native","aggregated","unavailable"]`** (`models/persistence.py:68`) decided in `persistence_service.py:92–173`. The client passes the payload through without re-deriving it. This is the SURF-P03 M3 pattern applied correctly: **state travels as a typed field, never reconstructed from message strings or bar counts.**

**M3** — the 1:1 fallback is deleted. The old `rawCandles.length === 0 && timeframe !== "1m"` M1 re-fetch no longer exists in `TerminalChartStage.tsx`. Pinned by a test asserting exactly one request per timeframe switch with no M1 re-fetch.

**M5** — the notice now renders from `seriesKind`, three ways:

```tsx
seriesKind === "native"     → "Native M1 Stream"
seriesKind === "aggregated" → "Resampled from M1 stream · wall-clock aligned {n}-minute buckets
                               · {k} partial bucket(s) excluded"
                            → "No {tf} series — insufficient coverage"
```

The annotation `resolution` field is likewise derived from the discriminant, replacing the hardcoded `timeframe === "1m" ? "native" : "resampled"`. **The `TD-029` notice is now true.** I am satisfied to close `TD-029` on this basis — the disclosure and the behaviour finally agree.

**M2** — dedicated `/api/v1/persistence/candle-series` endpoint under `CurrentOperatorDep`, matching the established auth pattern.

---

## 4. ✅ THE DECISIVE CAPTURE — AGGREGATED ≠ NATIVE

The Build Order made this the test the phase turned on: *"two identical-looking charts at different timeframe labels is the defect, not the fix."*

- **Capture 01 (`1M` native):** dense minute bars across an ~80-minute window, axis `11:20 → 12:48`. Notice reads `Native M1 Stream`.
- **Capture 02 (`1H` aggregated):** ~65 hourly bars across **three days**, axis `06:00 → 18 06:00`. Notice reads *"Resampled from M1 stream · wall-clock aligned 60-minute buckets · 2 partial bucket(s) excluded"*.
- **Capture 03 (`1D`):** **five** wide daily bars on day-boundary gridlines (13–17), *"1440-minute buckets · 2 partial bucket(s) excluded"*.

Three genuinely different series, correct bar counts for their windows, each labelled honestly. The `1D` capture is particularly good evidence — five bars from six days of history is exactly what the M6 rule predicts once the two partial edge days are excluded.

**Capture 04 (unavailable)** is the best absence rendering delivered in this programme: *"No H1 Series for USD/CHF — insufficient M1 coverage to form a complete H1 bucket: stored M1 bars 0, partial buckets excluded 0. The chart renders absence, not an improvised series."* Provenance reads `NONE (0 live · 0 seed)`. No axis, no ghost series, and it names the remedy.

---

## 5. ✅ M7 / M8 / R1–R6

**M7 — session context.** `TOKYO 00:00–09:00 · LONDON 07:00–16:00 · NEW YORK 12:00–21:00 UTC`, with overlaps computed and **weekends returning no session** (`isWeekendUtc`) rather than a fabricated open market. Surfaced as a strip showing the active session and, in capture 02, the series' session span (`TOKYO + LONDON (overlap 07:00–09:00 UTC) → LONDON`).

**R1 honoured — and I want to record a correction of my own.** My first check used `git diff HEAD`, which compares against the base commit and therefore showed the DATA-P01 generator changes. That was **my** methodological error, not a DA violation. Checking the DATA-P02 patch itself: it touches **no** generator file — not `chart_seed_service.py`, not `adapters/simulated.py`, not `live_service.py`. The fence held. Session context was built as labelling over existing data exactly as scoped.

**M8** — the T-1 guard anchors `"wall-clock aligned"`, `.replace()`s it, then asserts the residue contains none of `timeframe !== "1m"`, `"native" : "resampled"`, `rawCandles.length === 0`, or `bars.length === 0 ? kind`. This is the SURF-P02 M4 pattern applied precisely, and the forbidden terms are **the exact regression mechanisms** this phase removed — so reintroducing the defect fails the build.

**R2** — 16 `protectedWorkspace({` / 16 `route:` entries; the registry is not in the patch. **R5** — no dependency files touched. **R6** — `720.67 → 724.50 kB (+3.83 kB)`, rolls into `OBS-5`.

---

## 6. EXECUTION EVIDENCE

**Pre-fix failure demonstrated**, as required: `pytest test_data_p02_aggregation.py` exit 2 and `vitest terminalChartTimeframes.test.tsx` exit 1 against the pre-patch tree. New tests genuinely could not pass before.

**429 BE + 829 FE = 1,258** (from 1,240; +18), `tsc -b` 0 errors, build reproduced with an identical bundle hash across two runs. Recorded as **asserted transcripts** — I did not re-run the suites. The aggregation core, which is the phase's substance, I verified by **direct execution** (§2), which is stronger than a transcript for those properties.

### Deviations — five failed attempts disclosed unprompted

Including a **bucket-flooring defect in the first implementation** (`hour kept + floored minutes added = +10h shift`), caught by the DA's own boundary test before shipping; a fixture-ordering 401; a capture-script field error; a `PYTHONPATH` failure; and a missing Playwright binary.

Disclosing a caught-and-fixed correctness bug that nothing would have revealed is the standard set in DATA-P01 cycle 3, and it is now consistent behaviour. It also demonstrates the boundary test has real diagnostic power.

Deviation 3 is a genuine scope extension, correctly flagged: live M1 tick merging is now restricted to `kind: "native"`, so a 1-minute tick can never be merged into an H1 bar. **That is the right call** — it is the granularity corollary of M4/M6, and merging live minutes into an aggregated bucket would have re-introduced a subtler version of `F-DATA2-1`. Approved as delivered.

---

## 7. 🟠 `OBS-DATA2-1` — THE M1 WALK HAS A DIRECTIONAL DRIFT VISIBLE OVER LONG WINDOWS

| Field | Content |
|---|---|
| **Finding ID** | `OBS-DATA2-1` (observation — **not** a DATA-P02 defect) |
| **Evidence** | Capture 02 shows EUR/USD climbing near-monotonically `1.24 → 1.44` over three days; capture 03 shows five ascending D1 bars with almost no overlap. |
| **Cause** | The DATA-P01 forex walk uses `gauss(0.00004, 0.00015)` — a **positive mean**. Over `n` bars, drift `= 0.00004n` grows linearly while noise grows as `0.00015√n`. At one day (1,440 bars) the drift-to-noise ratio is **10.1×**; at five days, **22.6×**. Six days of seeding moves EUR/USD `+0.3456` (`+31%`). |
| **Why it did not surface before** | Every prior capture showed ≤100 M1 bars, where drift is `+0.004` — invisible. **DATA-P02 is the first phase to render long windows, so it is the first to expose it.** Same pattern as DATA-P01 exposing the `--` rows. |
| **Assessment** | The aggregation is faithful — it is correctly showing what the generator produced. A real FX pair does not trend one direction for six days at 31%. This is a **simulator realism** matter, in the class of `CA-DATA1-1`/`CA-DATA1-2` but lower severity: nothing is mislabelled, no interval is fabricated, and provenance is honest throughout. |
| **Recommended** | Consider a mean-reverting or zero-mean walk when the generators are next legitimately open. **Do not open them now** — R1 fenced them for good reason, and three correction cycles were spent stabilising them. |
| **Owner** | Operator to route — candidate for a future DATA phase or POLISH triage. |

Raised because a future phase will render longer windows again, and it should be a known quantity rather than a rediscovery.

---

## 8. STATUS

| Item | State |
|---|---|
| **DATA-P02** | **APPROVED WITH OBSERVATIONS** |
| `F-DATA2-1` fabricated interval | **CLOSED** — aggregation proven by execution |
| `TD-029` | **CLOSED** — disclosure and behaviour now agree |
| M1–M8 · S1–S3 · R1–R6 | **All satisfied** |
| `OBS-DATA2-1` M1 walk drift | **OPEN** — non-blocking, Operator to route |
| `OBS-DATA-P01-WATCHLIST-CLIP` | Open — POLISH triage |
| `OBS-5` bundle 724.50 kB | Open — POLISH-P01 |
| `OBS-SURF3-1` · `F-BRAND-1` | Open — DA / GA-173 |

**Programme queue:** CONV ✅ · SURF ✅ · DATA-P01 ✅ · **DATA-P02 ✅** · CHART (not authorized) · POLISH (not authorized).

---

## 9. ASSESSMENT

This is the strongest delivery of the programme. The central defect was subtle and consequential — a timeframe label applied to unaggregated data, with an honesty notice actively asserting a transformation that never occurred. The fix is architecturally correct rather than cosmetic: aggregation moved to the server, state carried as a typed discriminant from its origin, the client reduced to a consumer, and the three-way `native`/`aggregated`/`unavailable` distinction made visible in the product.

Two details raise my confidence. The partial-bucket rule was implemented as **exclusion with disclosure** rather than the easier option of rendering a short bar — the harder and more honest choice. And the live-tick merge restriction was volunteered, closing a granularity hole nobody had named.

DATA-P02 answers the phase's governing question. A manufactured value cannot be mistaken for a market observation here, and a manufactured *interval* can no longer be either.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This determination is **not** authorization for CHART or POLISH. No implementation before the next Build Order.

**We don't guess. We prove.**
