# ITRGA DETERMINATION — DATA-P01

**Reviewing body:** Independent Technical Review & Governance Authority
**Subject:** Extend the simulated feed to all eleven instruments — correlated walks, per-symbol seeding, watchlist sparklines
**Date:** 2026-08-17
**Base:** nine-element chain through SURF-P03
**Verification:** `/tmp/d1` — pristine clone → chain → DATA-P01 applied

| Artifact | sha256 | Size |
|---|---|---|
| `data_p01.patch.txt` | `2af54d600e736359` | 977 lines · 10 files |
| `DELIVERY_REPORT_DATA-P01.md` | `7c81db6901518203` | 206 lines |
| `DATA-P01_CAPTURE_VERIFICATION.json.txt` | `03375da8e4b92f57` | 101 lines |
| 5 PNGs | reconcile | 1920×1080 |

---

## 1. DETERMINATION

# CORRECTION REQUIRED

The provenance architecture is correct and the constitutional requirements are met. **One scale defect makes a simulated price implausible on its face: `USD/JPY` is generated on the crypto walk.**

Transport is clean — hash matches, `git apply --check` exit 0, nine-element chain declared. **Ninth consecutive hash-reconciled delivery.**

---

## 2. 🔴 `CA-DATA1-1` — USD/JPY GENERATED ON THE CRYPTO WALK

| Field | Content |
|---|---|
| **Finding ID** | `CA-DATA1-1` (correction required) |
| **Requirement** | Build Order S1/S3 — realistic per-class walks; M3 — simulated data must never be presentable as market data. |
| **Evidence** | `chart_seed_service.py:123` branches on **price magnitude, not market class**: `if price >= Decimal("100")`. `USD/JPY` has base `150.000`, so it takes the **crypto** branch: `rng.gauss(8, 35)` per bar, quantized to `0.01`. Capture 01 shows `USD/JPY 155.00000 +3.33%` while every other forex pair moves ±0.01–0.02%. |
| **Quantified** | The crypto step has mean **+8.00 per bar**. Simulating 100 bars from 150.000 on that branch yields **976.22** — USD/JPY at 976. The 80-bar seed in the capture had already carried it to 155.00 (+3.33%) in one session. |
| **Root cause** | `market_class` is computed at `:100` (`class_for`) and correctly drives the correlation factor and beta — `USDJPY` is treated as forex there, with `beta = -1.0`. **The walk branch ignores it** and re-derives class from price. |
| **Why it matters** | This is not cosmetic. A JPY pair drifting ~8 yen per minute is not a plausible market series, and the phase's governing constraint (§2 of the Build Order) is that generated values must never be mistakable for — or embarrassingly unlike — market observations. It also makes `USD/JPY`'s `beta = -1.0` correlation meaningless: a forex-scaled factor of ±0.00006 against a crypto-scaled idiosyncratic step of ±35 is numerically inert. |
| **Required Correction** | Branch on `market_class`, not `price >= 100`. Forex pairs — including JPY crosses — take the forex walk. **Note JPY pairs need their own tick scale**: 5-decimal quantization is wrong for a 150.000 pair; JPY convention is 3 decimals, and the pip step should be ~100× a EUR/USD pip. State the chosen scale. |
| **Closure Evidence** | Re-seed and capture: `USD/JPY` rendering at a JPY-plausible level with per-bar moves comparable in *relative* terms to the other majors; determinism test still green. |
| **Owner** | DA |

**The report's own §1 table lists `USDJPY | 150.000 | forex (existing)`** and §62 assigns it `beta = −1`. The intent was correct throughout; the walk branch is the single place the class is not consulted.

**This defect predates DATA-P01** — the `price >= 100` branch is original to `chart_seed_service.py`. It was latent because `USD/JPY` was one of only six seeded symbols and the watchlist showed `--`. **This phase made it visible by populating the watchlist.** That is surfacing working as intended, and I do not hold its existence against this delivery — only its persistence now that it renders.

---

## 3. WHAT IS CORRECT — AND SHOULD NOT BE RE-DONE

### M1 — Provenance ✓

```
chart_seed_service.py:157   source="seed:synthetic"
```

**One provenance value, unchanged.** No new marker introduced. `inference/service.py`, `ml/dataset/service.py` and the live adapter — all of which branch on this exact string — are untouched by the patch. The requirement that mattered most is met exactly.

### M4 — The fabricated fallback is gone ✓

```python
if s not in defaults:
    raise KeyError(f"no simulated base price for symbol {s} (seed:synthetic reference data)")
```

`defaults.get(s, Decimal("1.00000"))` is **replaced with a raise**. An unknown symbol now fails loudly instead of receiving a plausible-looking `1.00000`. The comment states the principle: *"a wrong price is worse than no price."*

This is the `OBS-CONV2-1` pattern eliminated at its source, and the base-price table is explicitly annotated as *"simulator inputs — plausible round levels per class — NOT market observations."*

### S1 — All eleven covered ✓

`AUDUSD 0.66000` · `USDCAD 1.36000` · `USDCHF 0.88000` · `NZDUSD 0.61000` · `EURGBP 0.86000` · `SOLUSD 150.00` added. All eleven `SUPPORTED_INSTRUMENTS` now resolve.

### S2 / M7 — Per-symbol seeding, proven ✓

```python
rng = random.Random(symbol_seed(symbol, timeframe))        # per symbol
factor_rng = random.Random(class_factor_seed(mc, timeframe))  # per class
```

The shared `Random(42)` is gone. `test_chart_seed_per_symbol_determinism_and_order_independence` asserts both same-input reproducibility (`first == second`) **and order independence** — seeding `["EURUSD","GBPUSD"]` then `["GBPUSD","EURUSD"]`. Proven, not asserted.

### S3 — Correlation, correctly bounded ✓

Per-class factor stream with betas: `EURUSD/GBPUSD/AUDUSD/NZDUSD = +1`, `USDJPY/USDCAD/USDCHF = −1`, `EURGBP = 0`, crypto `= +1`.

**The sign convention is right** — USD-base pairs move inversely to USD-quoted ones. `EURGBP = 0` as a cross is correct. No covariance model was built, exactly as scoped.

### M2 / M3 — Labelling ✓

```ts
if (hasSeed && hasLive) return "SEED:SYNTHETIC + LIVE:SIMULATED";
/** M2/M3: price provenance from the quote's source field. "LIVE" never appears alone */
```

Derived from the candles' `source` field rather than hardcoded. Capture 01 shows a `LIVE:SIMUL…` chip on **all eleven rows** (JSON: `chips: 11, sparklineTags: 11`).

### M5 — Absence path preserved ✓

Three `"--"` sites retained. Capture 04 confirms all eleven revert to `--` with the feed stopped and provenance reading `SEED:SYNTHETIC (0 live · 100 seed)`.

### R1 — Independent degradation ✓

Capture 05: `gbpSparklinePresent: false, gbpPrice: "1.27000", eurSparklinePresent: true, totalRows: 11`. One symbol's sparkline fails; its price still renders and the other ten are unaffected.

---

## 4. OBSERVATION — `OBS-DATA1-1`: M6 guard not delivered

Build Order M6 required a frontend T-1 guard over the watchlist/sparkline module, matching the three added in SURF-P01, P02 and P03. **The patch adds no such test.** `backend/tests/test_live_market.py` gains the determinism test but pins no frontend path.

Low severity — the watchlist renders prices, not actuation controls, and the domain risk is lower than execution research or alerts. But M6 was mandatory and three consecutive phases established the pattern. Fold it into the correction cycle.

---

## 5. EXECUTION EVIDENCE

Report cites the suites; I did not independently re-run them. Recorded as delivered:

```
frontend  vitest / tsc -b        backend  pytest
```

**Note:** the correction in §2 changes generated series, so `test_chart_seed_per_symbol_determinism_and_order_independence` and any golden-value assertions must be re-run after the fix. Supply fresh transcripts with the correction.

---

## 6. STATUS

| Item | State |
|---|---|
| **DATA-P01** | **CORRECTION REQUIRED** |
| `CA-DATA1-1` USD/JPY on crypto walk | **OPEN — blocker** |
| `OBS-DATA1-1` M6 guard absent | **OPEN** — fold into the correction |
| M1 provenance · M4 fallback · M5 absence | **Verified** |
| S1 eleven base prices · S2/M7 determinism · S3 correlation | **Verified** |
| M2/M3 labelling · R1 degradation | **Verified** |
| `OBS-5` bundle | Open — POLISH-P01 |
| `F-BRAND-1` | Open — GA-173 |

**Scope of correction: one branch condition and a JPY tick scale, plus the M6 guard.** Everything else in this delivery stands — do not rework the seeding, correlation, provenance or labelling.

The `--` defect is genuinely fixed: eleven instruments now populate with per-symbol sparklines and provenance chips. That was the phase's objective and it is met. This determination turns on one pair rendering at a scale that would not survive an institutional reader's first glance.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
Correction ≠ approval. This determination is not authorization for DATA-P02, CHART or POLISH.

**We don't guess. We prove.**
