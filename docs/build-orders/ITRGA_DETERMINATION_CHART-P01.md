# ITRGA DETERMINATION — CHART-P01

**Reviewing body:** Independent Technical Review & Governance Authority
**Subject:** CHART-P01 — technical indicators: honest controls, server-side computation (`F-CHART-1` fix)
**Date:** 2026-08-18
**Base:** 12-element chain (through `data_p02`)
**Verification:** `/tmp/c1` — pristine clone → 12-element chain → CHART-P01 applied

| Artifact | sha256 | Size |
|---|---|---|
| `chart_p01.patch.txt` | `6e141e9ab7d27bf0` | 2,635 lines · 18 files |
| `DELIVERY_REPORT_CHART-P01.md` | `2c016e7fee8e02cb` | 161 lines |
| `CHART-P01_CAPTURE_VERIFICATION.json.txt` | `74a7a324b6738fc2` | 819 lines |
| 6 PNGs | all reconcile, no dupes | — |

Declared hash matches computed. `git apply --check` **exit 0**. **Fourteenth consecutive hash-reconciled delivery.**

---

## 1. DETERMINATION

# APPROVED

Unqualified. `F-CHART-1` is **CLOSED**. Every mandatory requirement M1–M8 is satisfied, every constraint R1–R7 honoured, and **all six formulae verified by independent execution against hand-computed values** — not accepted on the DA's test assertions.

No new findings. No observations raised against this phase.

---

## 2. ✅ M2 — EVERY FORMULA VERIFIED INDEPENDENTLY

I loaded `indicators.py` directly and computed each indicator by hand against known input. **This is the requirement the phase turned on, and it is the one I refuse to take on assertion.**

### SMA / EMA — and the discrimination test that matters

`SMA(5)` over closes `1..10` → `[3, 4, 5, 6, 7, 8]`. Exact.

A linear ramp is a **trap** for EMA verification: EMA and SMA coincide on it, so a wrong EMA would pass unnoticed. I re-ran on a deliberately non-linear series `[10,12,11,15,14,20,18,25,22,30]`:

| | values |
|---|---|
| SMA(5) | `12.4 · 14.4 · 15.6 · 18.4 · 19.8 · 23.0` |
| EMA(5) impl | `12.4 · 14.9333 · 15.9556 · 18.9704 · 19.9802 · 23.3202` |
| EMA(5) manual | `12.4 · 14.9333 · 15.9556 · 18.9704 · 19.9802 · 23.3202` |

**Identical to manual, and provably distinct from SMA.** `α = 2/(n+1)`, SMA-seeded — the declared rule is the implemented rule.

### RSI · ATR · Bollinger · MACD

- **RSI(14):** monotonic rise → `100.0`; monotonic fall → `0.0`. Wilder's smoothing behaves at the boundaries.
- **ATR(14):** constant true range of 2 → `2.0`. Exact.
- **Bollinger(20, 2):** I computed both conventions. Implementation upper `57.3156995`; **population** σ predicts `57.3157`, sample σ predicts `58.0357`. **Population — as declared.** The distinction is documented rather than left ambiguous.
- **MACD(12,26,9):** against my own EMA implementation — line `4.8616854` vs manual `4.8616854`; signal `4.90548842` vs `4.90548842`; histogram `−0.04380302` vs `−0.04380302`. Exact to eight decimals.

**Six formulae, six exact matches.**

---

## 3. ✅ M4 — INSUFFICIENCY IS TYPED, AND VISIBLE

Executed directly: `SMA(50)` over 5 D1 bars returns

```
kind: "insufficient"   required: 50   available: 5   points: 0
```

**Zero points. No padded value, no sentinel, no partial-window mean labelled 50.**

Capture 05 confirms it in the product: *"SMA 50: insufficient history (50 required, 5 available) — no series rendered"*, the pill showing `active` while **no line is drawn**. This is DATA-P02's partial-bucket rule correctly generalised to indicator granularity — the phase's most important honesty property, and it holds in both the computation and the render.

**M7** verified in the same run: shuffled input produced identical output.

---

## 4. ✅ `F-CHART-1` CLOSED — PROVEN IN PIXELS

Capture 01 shows both pills `active` with two lines. I measured the rendered artifact rather than reading the DOM claim:

```
SMA20 (blue)    x  289 → 1495    780 columns
SMA50 (orange)  x  727 → 1495    769 columns
blue starts 438 px LEFT of orange
```

**Both lines genuinely present, and the offset is the proof of correctness.** SMA 20 needs 20 bars, SMA 50 needs 50 — over one window the shorter-period line *must* begin earlier. A cosmetic fix would have drawn two lines starting together. The pixels encode the warm-up difference.

The control that changed nothing now changes something demonstrable.

---

## 5. ✅ M1 · M3 · M5 · M6 · M8 · S1–S4 · R1–R7

- **M1/M3** — computation is server-side; pills drive real fetches and real overlay series.
- **M5** — status strip states `derived from {provenance} OHLC` using the **displayed series'** provenance. No new marker; backend vocabulary remains `seed:synthetic` / `live:simulated`.
- **M6** — the envelope carries `seriesKind` and `excludedPartialBuckets`; an `unavailable` series yields **no computation**. Indicators inherit the aggregation disclosure rather than laundering it.
- **M8** — anchor *"Indicators describe data, they never advise a trade."* present → `.replace()`d → residue asserted free of `trade recommendation`, `eligibility`, `setup quality`, `risk/reward`. **The DA also explained why actuation terms are asserted at render rather than in source: the annotation guard legitimately lists them as rejection tokens, so a source-residue check would be vacuous.** That is precisely the SURF-P02 M4 lesson understood rather than copied. Guard demonstrated failing pre-fix.
- **S1** — single registry backend + mirrored frontend, golden-tested; unknown ids `422`. CHART-P02 becomes formula + row.
- **S3/S4** — toggles never refetch the candle series (asserted by call count); 7 indicators over 100 bars in **5.0 ms median**.
- **R1** — no generator or aggregation file in the patch. **R2** — 16 routes, registry untouched. **R5** — zero new dependencies; formulae explicit. **R7** — `PriceChart` still renders and does not compute; docblock updated to state the division of labour rather than silently drifting.

**R6:** `724.50 → 730.90 kB` (+6.40 kB), into `OBS-5`.

---

## 6. EXECUTION EVIDENCE

Pre-fix failure demonstrated: `pytest` exit 2, `vitest` exit 1, guard `anchorPresent:false`. The new tests could not have passed before.

**442 BE + 838 FE = 1,280** (from 1,258), `tsc -b` 0, build hash reproduced identically across two runs. Recorded as **asserted transcripts** — I did not re-run the suites. The formulae, insufficiency and determinism I verified by **direct execution**, which is stronger than a transcript for those properties.

### The fourth inert control — found unprompted

The Build Order said: *"if you find a fourth inert control, say so."* The DA found one. `TechnicalOverlayState.volume` existed as state defaulting to `true` with **no pill and no consumer** — dead chrome in the same defect class as `F-CHART-1`. Removed, with a sweep confirming no others, and the misleading *"Presentation Only"* tooltips reworded to *"computed server-side from the displayed series; descriptive, never prescriptive."*

**Third consecutive phase in which the DA fixed the defect class rather than the cited line.** It also disclosed the MACD signal-availability subtlety — the line is computable at 26 bars but the signal is not seeded until 34, so the registry declares the full-definition requirement rather than emitting a half-formed indicator.

---

## 7. NOTE FOR THE NEXT PHASE — NOT A FINDING

`S2` discloses that **crosshair and time-axis synchronisation between panes is not implemented**; each pane fits independently. The DA flagged this itself and correctly did not call it a deviation, since the Build Order required only that separate panes not distort the price scale — which they do not (capture 03, measured rects).

For CHART-P02 this is worth scoping deliberately: unsynchronised time axes across stacked panes are a genuine analysis-ergonomics gap in a TradingView-class terminal. **Recommended, not required.**

---

## 8. STATUS

| Item | State |
|---|---|
| **CHART-P01** | **APPROVED** |
| `F-CHART-1` inert indicator controls | **CLOSED** — proven in pixels |
| M1–M8 · S1–S4 · R1–R7 | **All satisfied** |
| Fourth inert control (`overlays.volume`) | **CLOSED** — found and removed unprompted |
| `OBS-CHART-1` orphaned `ChartPlaceholderPage.tsx` | **OPEN** — non-blocking, POLISH |
| `OBS-DATA2-1` M1 walk drift | Open — Operator to route |
| `OBS-DATA-P01-WATCHLIST-CLIP` · `OBS-5` (730.90 kB) | Open — POLISH |
| `OBS-SURF3-1` · `F-BRAND-1` | Open — DA / GA-173 |

**Programme queue:** CONV ✅ · SURF ✅ · DATA-P01 ✅ · DATA-P02 ✅ · **CHART-P01 ✅** · CHART-P02 · CHART-P03 · POLISH — none authorized.

---

## 9. ASSESSMENT

This is the first unqualified APPROVED since SURF-P02, and it earns it on the hardest evidence standard the programme applies: I recomputed every formula independently and all six matched exactly, including the EMA case where a linear test series would have concealed an error.

The architectural goal mattered more than the seven indicators, and it was met. A registry with declared `required_bars`, a typed insufficiency discriminant, server-side computation, and provenance that inherits rather than launders — that contract is what makes roughly 45 of the ~70 AXIOM Analytics Engine items incremental rather than each a fresh argument.

Two judgements deserve particular credit. Declaring MACD's requirement as 34 bars — the full definition including a seeded signal — rather than the 26 that would let a half-formed indicator render. And explaining *why* the M8 guard splits source-residue from render assertions, rather than mechanically copying a pattern into vacuity.

The phase began with three buttons that lit up and did nothing. It ends with seven indicators that compute correctly, disclose honestly when they cannot, and never advise.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This determination is **not** authorization for CHART-P02, CHART-P03 or POLISH. No implementation before the next Build Order.

**We don't guess. We prove.**
