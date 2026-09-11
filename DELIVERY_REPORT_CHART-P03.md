# DELIVERY REPORT — CHART-P03 (Drawing tools & Market Structure)

**Delivered by:** AXIOM Development Authority
**To:** ITRGA
**Date:** 2026-08-18
**Build Order:** `BUILD_ORDER_CHART-P03.md` (sha256 `c114a7cd3eb4de90687f1b95fa8c6a282bc7a0bbf9e1dfdfb68c4f88ecf1804e`)
**Base:** 14-element chain (through `chart_p02`)

| Artifact | sha256 |
|---|---|
| `chart_p03.patch` (== `.txt`, `cmp`-identical) | `5b74fc6466a73b90cb551ea5bd0d39e6bb05a2080d7b472abcbc9ca6fc738b0a` |
| Patch format | 2,896 lines · 20 files · LF-only (CR bytes: 0) · terminating newline |
| Pristine apply | 15th element of the chain; `git apply --check` exit 0 in a fresh clone |

## 1. Baseline correction (stated per the Build Order's instruction to confirm)

The Build Order cites "458 BE + 844 FE ≈ 1,302 (confirm against your transcripts)". The DA's
transcripts record **462 BE + 844 FE = 1,306** after CHART-P02 — the order's 458 is four short
of the delivered suite. This phase lands at **473 BE + 853 FE = 1,326** (+11 BE / +9 FE), per
the fresh transcripts in §6.

## 2. Requirement mapping — M1–M10

| Req | Delivered | Where |
|---|---|---|
| M1 | ✅ Drawings persist **(price, time)** per handle — `content.geometry.handles` through the existing annotation artifact; pixels exist only momentarily at conversion time. **Proven across the 1m → 1h → 1m round-trip: the persisted handles are byte-identical after the trip** (JSON-recorded `anchor equality true`), and the rendered overlay is identical. | `drawingTools.ts` types, `ChartDrawingOverlay`, stage placement flow |
| M2 | ✅ Drawings track their anchors under viewport changes (converted at draw time on every render); **S2 stated**: drawings are per (symbol, timeframe) — during the 1h leg of the round-trip the 1m drawings were correctly ABSENT (machine-recorded 0), so nothing ever appears unannounced on another timeframe. Anchors outside the loaded window are clipped by the SVG viewport — never clamped to the chart edge. | overlay + per-timeframe annotation scoping |
| M3 | ✅ **F-CHART3-1 closed**: saved notes render on the chart at their (price, time) anchors (capture 04: marker visible, count consistent). Every NEW note is anchored — to the operator's price level or the last visible bar's close, both real. | stage note flow (geometry attached) |
| M4 | ✅ **Legacy handled honestly, stated rule**: (a) `x_percent/y_percent` rows → the LEGACY list below the chart, labelled UNANCHORED ("saved before price/time anchoring; their chart position is unknown and is not invented"); (b) price-only rows → a horizontal line at their REAL price, labelled "price-anchored note (time unknown)"; (c) nothing gets a fabricated anchor. Capture 05. | stage derivation + legacy list |
| M5 | ✅ Drawing labels inherit the actuation rejection (`entry`, `stop_loss`, `take_profit`, `position_size`, `lot`, `order` + `setup`/`risk_reward`) via the shared `drawingLabelRejection`; the BACKEND factory independently rejects forbidden fields on every create AND update (server-side enforcement, not only UI). Fibonacci renders its geometric levels only — no trade semantics. | `drawingTools.ts`, factory reuse |
| M6 | ✅ The existing contract reused; **one stated extension**: the contract's verb surface gained `PATCH`/`DELETE /collaboration/chart-annotations/{id}` (same `CurrentOperatorDep`, same factory validation, same audit trail with new `.updated`/`.deleted` audit actions) — because the contract exposed create/list/get only, and S1 requires move + delete. Extension of the ONE path, not a parallel one; RBAC untouched. | `collaboration.py`, repository |
| M7 | ✅ Six Market Structure detections enter through `INDICATOR_REGISTRY` exactly as CHART-P02's did (formula module + registry rows + UI mirror). **Rules declared precisely** (the Build Order asked for the exact rule, not the conventional one): SWINGS strict ±5 lookback/lookforward; STRUCT classification vs the previous same-kind swing; BOS strict close-break of the most recent CONFIRMED swing level (a swing bar cannot break itself); CHoCH = the FIRST opposite-direction BOS; FVG = 3-bar gap, fill-by-close, 50-bar cap; OB pattern = bearish predecessor + close beyond its high + range ≥ 1.5× median-of-20, fill-by-close. | `market_structure.py` |
| M8 | ✅ **Naming binding honoured**: the disclosure — *"Geometric pattern detection over simulated OHLC — not evidence of institutional activity or order placement."* — is carried on every structure registry entry AND rendered in the product whenever one is active (captures 06/07 machine-record it in the statuses). Conventional labels retained for recognisability only. | registry `disclosure` field (stated extension) + status strip |
| M9 | ✅ The typed `insufficient` discriminant reused unchanged; capture 08: BOS on 1D → "12 required, 5 available — no series rendered", zero lines. Full-definition requirements: SWINGS 11 · STRUCT 29 · BOS 12 · CHoCH 24 · FVG 3 · OB 21 (declared rationales in the module + pinned by test). |
| M10 | ✅ Anchor pinned; the forbidden list extends to the institutional-claim and directional-folk vocabulary (`institutional order`, `smart money`, `accumulation/distribution zone`, `entry zone`, `golden pocket`, the buy/sell/cross vocabulary). The terms live OUTSIDE the stage source (in `drawingTools.ts`) precisely so the source-residue guard remains meaningful; render-level assertions cover the active surface. Discrimination recorded: the vocabulary was under test nowhere pre-fix (0/8), 8/8 post-fix. |

## 3. Supporting scope — S1–S4

- **S1** — create/select/move/delete with visible tool state. **Real-browser interaction traces in the JSON**: every placement click, menu click and the deletion selection click were hit-tested (`elementFromPoint`) before landing. jsdom cannot hit-test — the overlay component is converter-driven so drags are unit-tested, and the real-browser captures prove the interaction. **Found and fixed during the phase:** lightweight-charts consumes bubble-phase clicks, so placement uses a CAPTURE-phase listener (stated in code) — the bubble-phase handler would have been dead in production.
- **S2** — stated above (per symbol/timeframe; the round-trip capture proves the scoping).
- **S3** — layering declared: price series < indicator overlay lines (registry palette) < drawing overlay SVG < menus; structure detections use the deterministic registry palette; drawings use a fixed drawing palette. 19 concurrent indicator lines + drawings remain legible in captures 06/07.
- **S4** — measured: **6 structure detections over the 2880-bar compute window ≈ 251.6 ms** median; **50 drawings (500 SVG nodes) re-render ≈ 33 ms** (measured in-browser via performance marks; the 50 fixtures were created and then deleted — audited — leaving only audit rows).

## 4. Constraints — R1–R7

R1 ✅ no generator/aggregation/23-formula file modified. R2 ✅ RBAC unchanged (registry untouched; the annotation verbs use the existing auth dependency; endpoint-auth breadth extended). R3 ✅ no recommendations/verdicts/entry-stop-target output; the backend factory rejects actuation fields server-side. R4 ✅ vocabulary unchanged. R5 ✅ zero new dependencies — drawings render via SVG + `lightweight-charts` coordinate APIs (`timeToCoordinate`/`priceToCoordinate`/`coordinateToTime`/`coordinateToPrice`); stated: the library has no rectangle/ray primitives, so the DA rendered them in SVG **using the library's own coordinate conversion** rather than importing anything. R6 ✅ **736.97 → 748.05 kB (+11.08 kB)** — the largest UI surface so far, stated plainly → OBS-5. R7 ✅ `PriceChart` still renders, never computes (the overlay converts and draws provided data; the docblock states the division).

## 5. Fail-first + hand-computed fixtures (acceptance 13)

```
pytest tests/test_chart_p03_market_structure.py  (PRE-FIX)  exit 2 — no module app.services.market_structure
vitest terminalChartDrawings.test.tsx             (PRE-FIX)  exit 1 — modules absent (drawingTools)
guard-extension (PRE-FIX) 0/8 vocabulary under test → FAILS; (POST-FIX) 8/8 → PASSES
```

Hand-computed fixtures (verifiable by inspection): single-peak swing high at exactly bar 7
(=20.0) with the k-window rule; HH=16 at bar 15 / LH=12 in the falling-peak case (first swing
unclassified); BOS-up at bar 11 with level 12.0 (close 13 breaking swing 12); CHoCH-down at bar
20 with level 4.0 (first direction flip — the initial BOS-up at 11 is NOT a CHoCH); FVG top
13.0/bottom 10.5 at bar 2, unfilled through bar 3, filled at bar 4 (close 9.0 ≤ 10.5 — fill
BEFORE emission, so bar 4 emits nothing); OB pattern at bar 21 with zone [10.2, 9.3] under the
declared impulse rule; the PATCH/DELETE verbs audited (`.updated`/`.deleted` audit rows
asserted).

## 6. Executed-test position (fresh transcripts, both trees)

| Run | DA tree | Pristine clone (chain + chart_p03) |
|---|---|---|
| pytest | **473 passed** (`pytest_chart_p03_r2.log`) | **473 passed** (`pytest_chart_p03_verify.log`) |
| vitest | **174 files · 853 passed** (`vitest_chart_p03_r3.log`) | **174 files · 853 passed** (`vitest_chart_p03_verify.log`) |
| tsc -b --force | 0 errors | 0 errors |
| npm run build | `index-BZFGwQey.js` 748.05 kB | identical hash `afc577bb…` |

Suite position: **1,326 (473 backend / 853 frontend)** — baseline 1,306 + **20** (+11 backend:
6 hand-computed + full-definition + registry/naming + verbs + M8 source; +9 frontend drawing
tests). Build JS sha256 identical in both trees.

## 7. Level-I captures (image primary; instruments corroborate)

| Capture | sha256 | Gate result |
|---|---|---|
| 01 drawing palette | `83eff575349d1d97d920860d6294a8c01e2ce5831526068460ba355f8613cc4b` | 6 tools, active state visible, hit-tested ✅ |
| 02 trendline + fib | `cdc4e862ba92b322dc89694e41537a052c0444f951e0bde2704929a36cca1e16` | both placed by real clicks; 7 fib levels ✅ |
| 03a roundtrip BEFORE | `79f49817565832762ae494818e18343f84ae1054969a64957cd83a83a941b302` | API geometry recorded byte-for-byte ✅ |
| 03b roundtrip AFTER | `50422b836df6ff14b225b8429a83c83e7227cd9cdc61298ce884afe3744b3bdb` | **anchor equality TRUE; absent on 1h (scoped); identical on return** ✅ |
| 05 legacy honest | `59b96e5e7d0304e1d30386d51d9a5e64ccd586edcd6d3ced1eb97597bfd3ab21` | UNANCHORED list + price-anchored line; tool-armed strip ✅ |
| 04 saved note visible | `19789c91f4c5606c40d0141094384a6820adc4c592319d56fc5b98c17ef5623b` | F-CHART3-1: marker on chart, count consistent ✅ |
| 06 structure | `d7c2aaf02a560f2bb8f4e7df4bed00a9915c6fbcdafb23671f370046c75f6357` | swings+BOS+CHoCH; M8 disclosure in statuses ✅ |
| 07 FVG/OB zones | `fa1e90c349605c91232f88310671e88d3c9123e25d0b72c26f4279b331521695` | zones drawn; OB disclosure legible ✅ |
| 08 insufficient | `09d4419f17cabc14719397eaa4d6222dbd5f0a4bfcdf74b79321d06f6d1f538b` | 12/5 typed, zero lines ✅ |
| 09 deletion | `c3e5810b2a84eac3f4540610b72c18a59c3670aeaf345f55164f03ca135423c4` | selected by handle hit-test, deleted, clean ✅ |

- `CHART-P03_CAPTURE_VERIFICATION.json` (Rev A) sha256 `44e15b82e5d6e2f2678bce5e557c1d10f6e6ff8116f250c87ec9c1a0bef6c81a` (`.txt` `cmp`-identical)
- `CHART-P03_CAPTURES.html` (self-contained gallery) sha256 `70bd4e16382b891feeb51495682ffdd6374f7eb95915ac2cb5f01f37cb42ec2c`

## 8. Deviations disclosed unprompted (including failed attempts)

1. **Three defects found and fixed during the phase** (all would have shipped invisibly):
   (a) the stage's note/drawing saves sent `source_artifact_ids: []`, which the contract
   rejects (min 1 item) — every stage note save was 422-ing; the chart context is now the
   honest source (the convention ChartWorkspaceSurface already used). (b) drawings saved
   under the DISPLAY symbol ("EUR/USD") while the list endpoint filters the clean key
   ("EURUSD") — drawings vanished on reload; both save paths now use the same key. (c)
   lightweight-charts consumes bubble-phase clicks — the first placement implementation
   could never receive clicks in a real browser; placement now uses a capture-phase listener.
2. **The pending-anchor strip initially rendered inside the indicator status strip** (gated
   on active indicators) — invisible with none active; extracted to its own always-visible
   strip after the capture gate showed the pending state missing.
3. **Capture script defects caught by its own gates**: capture 03's DOM comparison was
   order-dependent (the refetch reorders by created_at desc) — replaced with byte-level
   persisted-anchor equality + sorted DOM sets; capture 09's counter counted handle circles —
   corrected to count drawing groups; captures 04/05 came out pixel-identical — reordered so
   each capture shows a distinct state; the capture-05 tool arm leaked into capture 09 (opening
   the note dialog on a handle click) — disarmed after use.
4. **Performance defects fixed before shipping**: none this phase in the indicator layer, but
   the level-indicator compute-window extension from CHART-P02 is reused and its structure
   cost measured (§S4).
5. **Fixture rows**: two legacy annotations (percent + price-only) inserted via the audited
   API to power capture 05 (register row `TD-UI-CHART-P03-EVIDENCE-FIXTURE`); 50 perf-fixture
   drawings created and then deleted (audited) for the S4 measurement.
6. **Registry/UI mirror contract widenings** (the established pattern): `engine` gains
   `MarketStructure`; the dataclass gains a `disclosure` field; the CHART-P01/P02 golden tests
   and the scaling test updated to the widened tables (their pinned positions unchanged).
7. **Playwright binary + apt graphics libraries** were absent after environment restore —
   reinstalled before any capture ran.

## 9. Acceptance criteria

1–17 addressed as mapped; criterion 16 (patch applies clean on the 14-element chain, sha256
declared and matching) verified in a pristine clone; criterion 17 (bundle delta) reported in
§4. The artifact of record is the verified patch, not a commit — no commits, pushes or pulls.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This delivery implements CHART-P03 only; it is not authorization for POLISH.

**We don't guess. We prove.**
