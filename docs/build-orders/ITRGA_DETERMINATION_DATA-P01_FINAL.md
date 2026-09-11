# ITRGA DETERMINATION — DATA-P01 (PHASE CLOSURE)

**Reviewing body:** Independent Technical Review & Governance Authority
**Subject:** DATA-P01 — simulated feed extended to all eleven instruments · correction cycle 3 (`CA-DATA1-3`)
**Date:** 2026-08-18
**Base:** nine-element chain → `data_p01.patch.txt` → `data_p01_correction.patch.txt` → `data_p01_correction2.patch.txt`
**This cycle:** evidence only — **no patch, zero product code changes**, as scoped

| Artifact | sha256 | Status |
|---|---|---|
| `DATA-P01_01_WATCHLIST_ALL_ELEVEN_POPULATED.png` | `8091714d06a748e0` | New — reconciles |
| `DATA-P01_03_CRYPTO_ROWS_PROVENANCE_SCROLLED.png` | `f99b8cddc8621e7e` | New — reconciles |
| `DATA-P01_CAPTURE_VERIFICATION.json.txt` | — | New |
| `DELIVERY_REPORT_DATA-P01_CORRECTION3.md` | `24a381ab…`→ new, 142+ lines | Supplied |
| Captures 02 / 04 / 05 | declared, unchanged from cycle 2 | Verified previously |

---

## 1. DETERMINATION

# APPROVED WITH OBSERVATIONS

**DATA-P01 is complete.** Every mandatory requirement is satisfied, every finding raised across three correction cycles is closed, and the closure evidence is legible in the shipped artifacts.

One observation carries forward: `OBS-DATA-P01-WATCHLIST-CLIP`.

---

## 2. ✅ `CA-DATA1-3` — CLOSED

### Capture 01 — the JPY convention is visible

**`USD/JPY 150.000`** — three decimals, fully legible. All eleven rows populated, every one carrying a price, a sparkline and a `LIVE:SIMUL…` provenance chip. `dashCount: 0`.

The DA correctly pushed back on my wording. I wrote that capture 01 *"must legibly show `USD/JPY 150.010`"* — but `150.010` was the value from an earlier feed position, and **the requirement is the three-decimal convention, not a specific number.** The capture shows `150.000`. That satisfies `OBS-DATA1-2` exactly. A generated feed's digits move; the convention is what was under review. **The correction is accepted, and the imprecision was mine.**

### Capture 03 — the proportionality fix is visible, not inferred

| | Price | Change |
|---|---|---|
| BTC/USD | 41,998.61 | **−0.05%** |
| ETH/USD | 2,500.00 | **−0.05%** |
| SOL/USD | 150.00 | **−0.05%** |

Three instruments spanning **280×** in price level, moving the identical relative step. Compare the round-2 capture that opened `CA-DATA1-2`: `BTC +0.01% · ETH +0.20% · SOL +3.33%`.

This is the single best piece of evidence in the phase. The fix is now demonstrated **in the image**, which is the standard I set.

---

## 3. THE LEGIBILITY INSTRUMENT — AND AN INDEPENDENT PIXEL CHECK

The DA built the instrument I have been asking for since `OBS-SURF1-2`: per element it records the layout box, the **ink rect**, a canvas-measured **painted-stroke extent**, vertical visibility, and a hit-test at the element's rightmost pixel — with a hard gate that fails the capture run if a required element is not fully legible. This measures **rendered extent, not geometry containment**, which is precisely the distinction the `GEOMETRY IS NOT LEGIBILITY` lesson exists to enforce.

### The disclosed 0.9 px deviation — verified independently

`change-btcusd`'s layout box reaches x 287.9, which is 0.9 px past the 287.0 clip. The DA did **not** claim it was inside. It disclosed the overshoot prominently, then asserted that the last painted glyph pixel is at x 286 and that nothing paints at or beyond 287 — the overshoot being empty glyph advance.

**I verified this against the shipped PNG rather than accepting it.** Scanning the BTC change-text band for glyph-coloured pixels:

```
rightmost glyph pixel   x = 286
x = 287, 288            (38,50,68) uniform — panel border, no text
```

**The DA's claim is exact.** `-0.05%` is painted complete. `boxFullyInside` is honestly recorded `false` for the two affected elements while the image shows the text intact — the instrument and the image agree, and the disagreement between *box* and *ink* is reported rather than smoothed over.

This is the correct handling of an inconvenient measurement: disclose it, explain the mechanism, and let the primary artifact settle it.

---

## 4. OBSERVATION CARRIED FORWARD

**`OBS-DATA-P01-WATCHLIST-CLIP`** — the watchlist's fixed 240 px slot with `overflow-x: hidden` clips the right edge of the metrics block when BTC's price and range strings are at their widest. Root cause **measured, not assumed** (rows container x 48 → 287, clientWidth 239).

Non-blocking: no value is fabricated, no value is hidden, and at present nothing is visually truncated. But the margin is under one pixel, and a wider value would clip. **Recommended** for POLISH triage. I explicitly instructed that layout code not be touched in this cycle, and it was not.

---

## 5. DEVIATIONS — DISCLOSED UNPROMPTED

Four, all volunteered:

1. Two untracked capture-tooling scripts in the working tree (DA tooling, not in any patch).
2. Governance register edit — two rows added.
3. Local dev DB manipulation before capture, **including a failed first attempt**: the `seed-history` endpoint returned 500 because live rows existed at insert time (natural-key collision); order corrected to delete-then-seed; 880 seed rows, 0 live at capture.
4. Capture 01 shows rows 1–9 plus BTC above the fold; ETH and SOL are recorded `verticallyInView: false` and **never claimed as visible** — capture 03 is the scrolled view.

Item 3 is the one I want on the record. **Reporting a failed attempt and its cause, unprompted, when a clean retry would have gone unnoticed, is the behaviour this review process exists to produce.** Item 4 is the `OBS-CONV3-1` discipline self-applied.

---

## 6. FINAL REQUIREMENT POSITION

| Req | Requirement | State | Basis |
|---|---|---|---|
| M1 | Single provenance value `seed:synthetic` | ✅ | grep — no new marker |
| M2 | Provenance derived from `source` | ✅ | helpers + 11 chips in image |
| M3 | No unqualified live/market/real-time | ✅ | T-1 guard + captures |
| M4 | No fabricated fallback price | ✅ | `KeyError` replaces `1.00000` |
| M5 | `--` absence rendering preserved | ✅ | capture 04, `dashCount: 0` when fed |
| M6 | Frontend T-1 guard | ✅ | 3 anchors incl. `tofixed(3)` |
| M7 | Determinism + order independence | ✅ | named test, verified |
| S1 | All 11 instruments | ✅ | 12 base prices |
| S2 | Per-symbol seeding | ✅ | `symbol_seed()` in loop |
| S3 | Correlated walks | ✅ | betas + fractional factor streams |
| S4/S5 | Sparklines from real series · degradation | ✅ | captures 01/05 |

**Findings across the phase:** `CA-DATA1-1` (USD/JPY on the crypto walk) · `CA-DATA1-2` (crypto walk magnitude-blind) · `CA-DATA1-3` (captures clipped) · `OBS-DATA1-1` (M6 guard) · `OBS-DATA1-2` (JPY display precision) — **all CLOSED.**

**Twelve consecutive hash-reconciled deliveries.**

**Execution evidence:** cycle-2 transcripts (421 BE + 819 FE = 1,240 tests, `tsc` 0, 720.67 kB) stand unchanged, as no code shipped this cycle. Recorded as **asserted transcripts**; the two decisive tests I verified independently by construction and simulation.

---

## 7. ASSESSMENT

Three scale defects were found and fixed across two generators. Each fix was generalised beyond the cited line — the DA found the `adapters/simulated.py` site I missed, and converted the crypto factor stream to fractional before I could raise it. Each closure is bound by a test that fails on the old code: I confirmed the crypto regression test fails at a 227.97 volatility ratio and passes at 1.00.

The phase's governing risk was that **a manufactured value might be mistaken for a market observation.** It is answered: the fabricated `1.00000` fallback is gone and raises instead, every rendered price carries an explicit simulated-provenance chip, and no price is presentable as market data. **A wrong price is worse than no price** — and the wrong prices are gone.

The blueprint's complaint was *"ten rows showing `--` is the single largest perceived-quality defect."* Eleven rows now carry realistic, correlated, per-symbol-seeded, honestly-labelled prices.

---

## 8. STATUS

| Item | State |
|---|---|
| **DATA-P01** | **APPROVED WITH OBSERVATIONS** |
| `CA-DATA1-1/2/3` · `OBS-DATA1-1/2` | **ALL CLOSED** |
| `OBS-DATA-P01-WATCHLIST-CLIP` | **OPEN** — non-blocking, POLISH triage |
| `OBS-5` bundle 720.67 kB | Open — POLISH-P01 |
| `OBS-SURF3-1` | Open — DA, non-blocking |
| `F-BRAND-1` | Open — GA-173 |

**Programme queue:** CONV ✅ · SURF ✅ · **DATA-P01 ✅** · DATA-P02 (not authorized) · CHART · POLISH.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This determination is **not** authorization for DATA-P02, CHART or POLISH. No implementation before the next Build Order.

**We don't guess. We prove.**
