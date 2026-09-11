# ITRGA DETERMINATION — CHART-P03

**Reviewing body:** Independent Technical Review & Governance Authority
**Subject:** CHART-P03 — drawing tools, annotation surfacing, price/time anchoring, Market Structure
**Date:** 2026-08-18
**Base:** 14-element chain (through `chart_p02`)
**Verification:** `/tmp/c4` — pristine clone → 14-element chain → CHART-P03 applied

| Artifact | sha256 | Size |
|---|---|---|
| `chart_p03.patch.txt` | `5b74fc6466a73b90` | 2,896 lines · 20 files |
| `DELIVERY_REPORT_CHART-P03.md` | `72121d266c5bea96` | 139 lines |
| `CHART-P03_CAPTURE_VERIFICATION.json.txt` | `44e15b82e5d6e2f2` | 1,307 lines |
| 10 PNGs | all reconcile, no dupes | — |

Declared patch hash matches computed. `git apply --check` **exit 0**. **Sixteenth consecutive hash-reconciled delivery.**

**Transmission:** all 13 artifacts arrived together. The §8 pre-upload check worked — every declared sha256 resolves to an attached file except two that legitimately cannot (the Build Order, which is my file, and an optional gallery). **The `OBS-CONV3-9` pattern did not recur.**

---

## 1. DETERMINATION

# APPROVED

Both findings of record are **CLOSED**. Six Market Structure detections verified against their declared rules by direct execution. No new findings.

---

## 2. ✅ `F-CHART3-2` — ANCHORING IS REAL, AND THE ROUND-TRIP PROVES IT

The architecture is right: pixels exist **only** at input capture (`ChartDrawingOverlay.tsx:64`), immediately converted via `coordinateToTime` / `coordinateToPrice`, and `(price, time)` is what persists. Rendering converts the other way at draw time. No `x_percent` anywhere in new work.

**The M2 proof — `1m → 1h → 1m`, machine-recorded:**

```
drawings before: 15    after: 15
BYTE-IDENTICAL persisted geometry: True
differing drawings: NONE
rendered ids before: 24   after: 24   identical set: True
```

I compared the before/after geometry myself rather than accepting the `equal: true` flag. `json.dumps(before, sort_keys=True) == json.dumps(after, sort_keys=True)` → **True**. Fifteen drawings returned to identical prices and timestamps after a full timeframe round-trip.

**The `1h` leg recorded `drawingCount: 0`, and that is correct, not a gap.** S2 declares drawings are scoped per `(symbol, timeframe)`, so `1m` drawings must be absent on `1h`. The Build Order named the opposite failure — *"a trendline drawn on 1h appearing unannounced on 1m is a defect"*. The scoping is enforced and the capture demonstrates it.

---

## 3. ✅ `F-CHART3-1` — ANNOTATIONS NOW RENDER, AND M4 IS HANDLED HONESTLY

Saved annotations appear on the chart at their anchors (capture 04; `+ Note (25)` → `(26)` recorded across the save).

**The legacy handling is the part I want to commend.** Capture 05 renders:

> `LEGACY NOTES — UNANCHORED (1): saved before price/time anchoring; their chart position is unknown and is not invented.`

M4 offered three acceptable options and named one unacceptable: fabricating anchors. The DA chose the most honest available — a labelled off-chart strip that states the position is unknown **and that it was not invented**. On a programme whose governing risk is manufactured values passing as observations, that sentence is exactly right.

---

## 4. ✅ M7 — SIX DETECTIONS VERIFIED AGAINST DECLARED RULES

The Build Order set the standard: *"Declare your rule precisely; I will verify the implementation matches what you declared, not what I would have chosen."* The rules are declared in the module docstring. I planted unambiguous fixtures and executed.

| Test | Result |
|---|---|
| **SWINGS(k=5)** — one strict high 20.0 at index 10 | `swing_high: [('09:10', 20.0)]`, `swing_low: []` — **exact, no false positives** |
| **BOS** — close 20.5 breaks confirmed swing high 20.0 | `bos_up: [('09:17', 20.0)]` — **exact** |
| **BOS self-break guard** — swing bar's own close below its own high | **0 detections** — the declared "a swing bar cannot break itself" rule holds |
| **FVG** — `low[5]=12.0 > high[3]=10.0` | `fvg_top 12.0 / fvg_bottom 10.0` at `09:05` — **exact** |

`required_bars` are full-definition and derived, not guessed: SWINGS 11, BOS 12 (`2k+2`), CHoCH 24 (`4k+4`), STRUCT 29 (`5k+4`), FVG 3. Capture 08 shows the typed refusal in the product — *"BOS: insufficient history (12 required, 5 available) — no series rendered."*

The self-break guard is the detail that persuades me the rule was thought through rather than transcribed. A naive BOS implementation lets the swing bar break its own level, producing a detection on every swing.

---

## 5. ✅ M8 — GEOMETRY, NOT INSTITUTIONAL CLAIMS

Capture 07's status line, machine-recorded and legible:

> `Order Blocks (Pattern): computed server-side · computed over native M1 series · derived from seed:synthetic + live:simulated OHLC · Geometric pattern detection over simulated OHLC — not evidence of institutional activity or order placement.`

Grep confirms `institutional`, `smart money`, `accumulation` and `distribution` appear **only inside disclaimer text** — never as a claim. The registry id is `OBPATTERN` and the label carries `(Pattern)`.

This was the requirement most exposed to drift, because the conventional vocabulary asserts market participants who do not exist on a `gauss()` feed. The naming discipline holds.

**M5/M10:** the drawing label derives from `annotationText`, which passes the forbidden-actuation guard before save, and the backend enforces `_assert_inert` / `_assert_no_guarantee_text` on the shared write path — **server-side rejection, not only client-side**. The guard vocabulary was extended with `institutional order`, `smart money`, `accumulation zone`, `entry zone`; discrimination recorded 0/8 pre-fix → 8/8 post-fix.

**R1** no closed file touched · **R2** 16 routes, registry untouched · **R5** zero new dependencies — rectangles and rays drawn in SVG using the library's own coordinate conversion rather than importing a drawing library, which is the right answer to a missing primitive · **R6** `736.97 → 748.05 kB (+11.08 kB)`, stated plainly as the largest UI surface so far.

---

## 6. EXECUTION EVIDENCE AND DEVIATIONS

Pre-fix failure demonstrated: `pytest` exit 2, `vitest` exit 1, guard 0/8. **473 BE + 853 FE = 1,326 tests.** Recorded as asserted transcripts; the six detections and the anchor round-trip I verified by direct execution.

**Three defects disclosed that would have shipped invisibly:**

1. Stage note saves sent `source_artifact_ids: []`, which the contract rejects — **every stage note save was 422-ing.** That is a live bug in existing behaviour, found and fixed.
2. Drawings saved under the display symbol `"EUR/USD"` while the list endpoint filters `"EURUSD"` — drawings vanished on reload.
3. **`lightweight-charts` consumes bubble-phase clicks, so the first placement implementation could never receive a click in a real browser.** jsdom would not have caught this; it is precisely the standing "jsdom cannot hit-test" lesson, found because the DA ran a real browser.

The capture script also caught three of its own defects — an order-dependent DOM comparison, a counter counting handle circles instead of drawing groups, and two captures coming out pixel-identical. The gate has now caught defects in four consecutive phases, including against its own author.

---

## 7. STATUS

| Item | State |
|---|---|
| **CHART-P03** | **APPROVED** |
| `F-CHART3-1` annotations invisible | **CLOSED** |
| `F-CHART3-2` percentage anchoring | **CLOSED** — byte-identical round-trip |
| M1–M10 · S1–S4 · R1–R7 | **All satisfied** |
| Indicator surface | **29 registered** (23 + 6 structure) |
| `OBS-CHART-1` orphan page · `OBS-DATA2-1` drift · `OBS-DATA-P01-WATCHLIST-CLIP` · `OBS-5` (748.05 kB) | Open — POLISH |
| `OBS-SURF3-1` | Open — DA |
| Confluence engine (11) / `Trade Eligibility` | **Awaiting Operator ruling** — unbuilt |

**Programme queue:** CONV ✅ · SURF ✅ · DATA-P01 ✅ · DATA-P02 ✅ · CHART-P01 ✅ · CHART-P02 ✅ · **CHART-P03 ✅** · POLISH — not authorized.

**The CHART programme is complete.**

---

## 8. ASSESSMENT

This phase closed two pre-existing defects that neither the blueprint nor the DA had listed, and it closed them at the root rather than at the symptom. Anchoring drawings to `(price, time)` is not a feature — it is the difference between a research artifact that means something and one that merely looks precise.

Three judgements stand out. The self-break guard in BOS, which a transcribed implementation would have missed. Refusing to invent anchors for legacy notes and saying so in the product. And solving the missing rectangle/ray primitive with SVG over the library's own coordinate conversion instead of importing a dependency — the constraint respected and the problem still solved.

The programme now carries 29 indicators, six drawing tools, honest insufficiency at every level, and a Market Structure surface that detects geometry while explicitly refusing the institutional narrative that normally travels with it.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
Not authorization for POLISH. No implementation before the next Build Order.

**We don't guess. We prove.**
