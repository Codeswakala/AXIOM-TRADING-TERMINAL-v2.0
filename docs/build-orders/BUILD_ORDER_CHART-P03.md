# BUILD ORDER — CHART-P03

**Issued by:** Independent Technical Review & Governance Authority (authorized by Operator)
**Date:** 2026-08-18
**Phase:** CHART-P03 — Drawing tools & Market Structure
**Base of record:** 14-element chain (through `chart_p02.patch.txt`)
**Precondition met:** CHART-P02 APPROVED. 23 indicators registered; registry extensibility proven.

---

## 1. WHAT THE RE-INVENTORY FOUND

Two findings of record, both discovered in the tree and both material to this phase.

### 🔴 `F-CHART3-1` — SAVED ANNOTATIONS NEVER APPEAR ON THE CHART

`TerminalChartStage.tsx:240` fetches research annotations. `:650` renders `+ Note ({annotations.length})`.

**That is the only thing it does with them.** Grep across the stage for `chart-annotation-marker`, `ChartResearchMarkerLayer`, `createPriceLine`, `setMarkers`: **zero occurrences.**

An operator writes a research note against a chart, saves it, and the button count increments from `(0)` to `(1)`. The note never appears on the chart. To read it back they must go elsewhere. **The capability is built, persisted, RBAC-protected and audit-correlated — and invisible at the point of use.**

This is the governing reframe exactly: *every already-built capability must be surfaced in the best possible way.* Annotation persistence is fully built. Its surfacing is a counter.

### 🔴 `F-CHART3-2` — ANNOTATION POSITIONS ARE CSS PERCENTAGES, NOT PRICE/TIME

The legacy marker layer positions annotations like this:

```ts
const x = numberValue(payload.x_percent, 16 + (index % 4) * 18);
const y = numberValue(payload.y_percent, 18 + (index % 3) * 18);
return { left: `${x}%`, top: `${y}%` };
```

Persisted as `x_percent` / `y_percent` (`ChartWorkspaceSurface.tsx:569–570`). **There is no price or time coordinate anywhere in the annotation payload.**

A percentage position is meaningless against a chart: change the timeframe, zoom, pan, or let one new bar arrive, and the marker points at different data while appearing precise. **A note anchored to "62% across, 40% down" is a note about nothing.** On a research terminal whose entire discipline is that displayed values must mean what they claim, a drifting annotation is the same class of defect as a fabricated interval — it asserts a relationship to data that does not hold.

**Drawing tools must not inherit this.** Every drawing and annotation must anchor to `(price, time)` and be converted to pixels at render.

### Also noted

`ChartWorkspaceSurface.tsx` — which owns the whole marker/annotation layer — is referenced **only by tests**. It is an orphan below the component level by the standing test (`grep -rl <fn> src | grep -v test`). Market Structure is greenfield: no swing, fractal, BOS, CHoCH, FVG or order-block code exists.

---

## 2. SCOPE

### In scope

**A. Drawing tools** — trendline · horizontal line · ray · rectangle · Fibonacci retracement · text note.
**B. Annotation surfacing** — `F-CHART3-1`: saved annotations rendered on the chart at their anchors.
**C. Price/time anchoring** — `F-CHART3-2`: all drawings and annotations anchored to `(price, time)`.
**D. Market Structure (05)** — Swing Points · HH/HL/LH/LL · BOS · CHoCH · FVG · Order Blocks, as registry indicators.

### Out of scope — do not build

- Volume engine, Order Flow (08), liquidity pools/sweeps/stop runs (06) — data absent or constitutionally barred.
- **Confluence engine (11), especially `Trade Eligibility`** — still awaiting Operator ruling. **No build.**
- Any change to DATA-P01 generators, DATA-P02 aggregation, or the 23 CHART-P01/P02 formulae. **All closed.**
- Migrating or deleting `ChartWorkspaceSurface.tsx`. Its orphan status is noted, not this phase's problem.

---

## 3. MANDATORY REQUIREMENTS (M1–M10)

### M1 — Drawings anchor to price and time
Every drawing persists `(price, time)` per handle — never pixels, never percentages. Rendering converts to coordinates at draw time.

**Proof required:** a drawing is placed, the timeframe is switched `1m → 1h` and back, and **the drawing returns to the same bars and prices.** A capture at one zoom level proves nothing.

### M2 — Drawings survive zoom, pan and timeframe change
Following M1, a drawing must track its anchors under every viewport change. If a drawing's anchors fall outside the loaded window it must be **absent or clipped honestly** — never clamped to the chart edge, which would misrepresent its position.

### M3 — `F-CHART3-1`: saved annotations render on the chart
Persisted annotations must appear at their anchors, legible, and identifiable as research annotations. The `+ Note (N)` count must correspond to what is visible — or the difference must be explained in the UI (e.g. *N total, 3 outside view*).

### M4 — Legacy percentage annotations handled honestly
Existing rows carry `x_percent`/`y_percent` and **no** price/time. They cannot be placed accurately. **Do not invent coordinates for them.**

Choose and state one: render them in a clearly-marked legacy affordance that does not claim chart position; or list them off-chart as unanchored; or migrate them **only if** a defensible mapping exists, and state the mapping. **Fabricating an anchor is the one unacceptable option** — that is `OBS-CONV2-1` at annotation granularity.

### M5 — Drawings are inert research artifacts
Drawings carry no execution semantics. The existing annotation guard rejects `entry`, `stop_loss`, `take_profit`, `position_size`, `lot`, `order` (`TerminalChartStage.tsx:450`). **Drawing labels and text must inherit this rejection.**

A Fibonacci retracement is a geometric construction, not a trade plan. **No entry/stop/target semantics, no risk/reward computation on a drawing, no "setup" vocabulary.**

### M6 — Drawing persistence uses the existing artifact contract
Reuse `chart_research_annotations` — `artifact_type`, `chart_context`, `content`, `provenance`, `uncertainty`, `disclaimer`, `research_status`, `audit_correlation_id` are all present and JSON-typed. Extend `content` for geometry. **Do not create a parallel persistence path** that bypasses the disclaimer and audit fields.

### M7 — Market Structure computed server-side as registry indicators
Swing Points, HH/HL/LH/LL, BOS, CHoCH, FVG, Order Blocks enter through `INDICATOR_REGISTRY` exactly as CHART-P02's sixteen did. Declare the swing-detection rule (lookback/lookforward) and each pattern's definition. `required_bars` is the **full-definition** requirement.

### M8 — 🔴 Market Structure naming must not claim institutional behaviour
Standing caution, now binding. **"Order Block" asserts a zone where institutions accumulated. On a `gauss()`-generated feed there are no institutions and no orders.** The pattern arithmetic is real; the microstructure interpretation is fabricated.

**Required:** name and describe these as **geometric pattern detections** over simulated OHLC, with the derived-value provenance every indicator already carries. If conventional labels are retained for recognisability, the surface must state plainly that they are pattern geometries detected on simulated data — not evidence of institutional activity.

### M9 — Insufficiency and provenance unchanged
Market Structure indicators use the established typed discriminant (`kind: "insufficient"`, `required`, `available`, zero points) and inherit series-kind and provenance behaviour. **Settled architecture — do not reinvent it.**

### M10 — T-1 guard extended
Keep the anchor (*"Indicators describe data, they never advise a trade."*) pinned. Extend the forbidden list for this surface: `institutional order`, `smart money`, `accumulation zone`, `distribution zone`, `entry zone`, `target`, `stop`, plus the directional vocabulary from CHART-P02.

Market Structure and Fibonacci carry the heaviest folk-trading vocabulary in technical analysis. **Detect the geometry; refuse the narrative.**

---

## 4. SUPPORTING SCOPE (S1–S4)

- **S1** — Drawing interaction must be usable: create, select, move, delete, with a visible tool state. **jsdom cannot hit-test** — supply an interaction trace or a real-browser hit-test, per standing lesson.
- **S2** — Drawings are per `(symbol, timeframe)` or explicitly cross-timeframe. State which; a trendline drawn on `1h` appearing unannounced on `1m` is a defect.
- **S3** — Market Structure detections must not collide visually with 23 indicators and user drawings. State the layering and colour strategy.
- **S4** — Performance: report drawing render cost with 50 drawings present, and Market Structure compute cost over the largest served window (CHART-P02 baseline: 23 indicators measured).

---

## 5. CONSTRAINTS (R1–R7)

- **R1** — No change to DATA-P01 generators, DATA-P02 aggregation, or the 23 existing formulae.
- **R2** — RBAC unchanged: 16 routes, `protectedWorkspace()`, registry untouched. Verify independently.
- **R3** — Constitutional: no automated execution, external LLMs, dynamic plugins, live trading. **No trade recommendations, eligibility verdicts, entry/stop/target output, or institutional-behaviour claims.**
- **R4** — Provenance vocabulary unchanged: `seed:synthetic`, `live:simulated`.
- **R5** — **No new dependencies.** 23 formulae were implemented explicitly; a drawing library must not appear now without justification. If `lightweight-charts` primitives are insufficient for a tool, say so rather than importing one.
- **R6** — Bundle delta against CHART-P02's **736.97 kB** (`OBS-5`). Drawing tools are the largest UI surface added so far — if the delta is significant, report it plainly.
- **R7** — `PriceChart` renders, does not compute. Contract holds.

---

## 6. EVIDENCE REQUIRED

**The image is primary; instruments corroborate and must measure rendered extent.**

### Captures
1. **Drawing tools palette** — all six tools, visible tool state.
2. **Trendline + Fibonacci placed** on the price chart, anchored to visible bars.
3. **🔴 The M1/M2 proof** — same drawings after a timeframe switch `1m → 1h → 1m`, **returning to the same bars and prices.** Include the before/after pair. This is the capture the phase turns on.
4. **`F-CHART3-1` closed** — saved annotations visible on the chart at their anchors, count consistent with what is shown.
5. **Legacy percentage annotations** — the M4 handling, honest about being unanchored.
6. **Market Structure** — swings and BOS/CHoCH detected, with the M8 naming visible in the product.
7. **FVG / Order Blocks** — zones drawn, M8 disclosure legible.
8. **Insufficient history** — a Market Structure indicator on `1D`, typed, no series.
9. **Drawing deletion** — a drawing removed, chart clean, no residue.

### Instruments
Reuse the legibility instrument with its hard gate — it has now caught two real defects against its own author. Hash every PNG; reconcile against the JSON. **Interaction traces required for S1** (jsdom cannot hit-test).

### Named tests — each must fail against current code
- `test_chart_p03_drawing_anchors_persist_as_price_and_time_not_pixels`
- `test_chart_p03_drawing_returns_to_same_anchors_after_timeframe_change`
- `test_chart_p03_saved_annotations_render_on_chart`
- `test_chart_p03_legacy_percentage_annotations_not_given_fabricated_anchors`
- `test_chart_p03_drawing_labels_reject_actuation_terms`
- One hand-computed test per Market Structure detection
- `test_chart_p03_market_structure_required_bars_full_definition`
- `test_chart_p03_no_institutional_behaviour_claims` (M10)

### Executed evidence
Full `pytest`, `vitest`, `tsc -b`, `npm run build`. Distinguish executed from asserted. Baseline: **458 BE + 844 FE ≈ 1,302** (confirm against your transcripts).

---

## 7. ACCEPTANCE CRITERIA

1. M1–M10 satisfied and independently verifiable.
2. S1–S4 addressed; deviations disclosed.
3. R1–R7 honoured.
4. Drawings anchor to price/time — **proven across a timeframe round-trip**.
5. `F-CHART3-1` closed: saved annotations visible at their anchors.
6. `F-CHART3-2` closed: no pixel or percentage anchoring in new work.
7. Legacy annotations handled honestly; **no fabricated anchors**.
8. Market Structure named as geometry, not institutional behaviour.
9. Every Market Structure detection hand-verified with its rule declared.
10. `required_bars` full-definition throughout.
11. No actuation, directional-verdict or institutional-claim language.
12. All nine captures legible, hashed, reconciled.
13. Every named test fails on current code, passes after.
14. Full transcripts supplied.
15. Delivery report documents changes and **all deviations, including failed attempts**.
16. Patch applies clean on the 14-element chain; sha256 declared and matching.
17. Bundle delta reported.

---

## 8. DELIVERY PROTOCOL

Upload: patch · delivery report · capture verification JSON · PNGs. **Artifact of record is the verified patch, not a commit.** No commits, pushes or pulls — repository activity is Operator-timed.

**Before uploading, verify every sha256 declared in the report resolves to an attached file.** CHART-P02 cost a full review cycle to a missing patch; the check is mechanical and would have caught it. `OBS-SURF3-1` remains open for the same pattern.

---

## 9. NOTES TO THE DA

CHART-P02 was approved after I hand-verified the conventions most likely to be quietly wrong — CCI's mean absolute deviation, HMA's `n + √n − 1`, Ichimoku's clamped senkou spans. All were right. That standard applies again to Market Structure, where the definitions are **less standardised** than classical indicators: there is no single agreed BOS rule. **Declare your rule precisely; I will verify the implementation matches what you declared, not what I would have chosen.**

`F-CHART3-1` and `F-CHART3-2` are pre-existing defects, not marks against your work. They surfaced because this phase is the first to make chart-anchored artifacts a first-class concern.

Three carried standards: fix the **defect class**, not the cited line — you have done this four phases running; verify rendered claims against **the artifact you ship**; and disclose failed attempts, which has been consistent and valuable.

One caution specific to this phase. Fibonacci and Market Structure arrive with the densest folk-trading vocabulary in the field — golden pocket, smart money, institutional accumulation, entry zones. **Every one of those terms is a claim about market participants who do not exist on a `gauss()` feed.** Draw the geometry. Refuse the story.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
Authorizes CHART-P03 only. Not authorization for POLISH.

**We don't guess. We prove.**
