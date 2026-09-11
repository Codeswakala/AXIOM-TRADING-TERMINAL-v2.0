# ITRGA DETERMINATION — CHART-P02 (PHASE CLOSURE)

**Reviewing body:** Independent Technical Review & Governance Authority
**Subject:** CHART-P02 — indicator breadth at scale · re-submission against `CA-CHART2-1`
**Date:** 2026-08-18
**Base:** 13-element chain (through `chart_p01`)
**Verification:** `/tmp/c3` — pristine clone → 13-element chain → CHART-P02 applied

---

## 1. DETERMINATION

# APPROVED

`CA-CHART2-1` is **CLOSED**. All three missing artifacts arrived at **exactly the hashes previously declared** — the delivery was an attachment failure, not a substantive one, and the re-submission proves it.

Sixteen new indicators. **I hand-verified the conventions I flagged as most likely to be quietly wrong, and every one is correct.** No new findings.

---

## 2. ✅ `CA-CHART2-1` — CLOSED ON EXACT-HASH RE-SUBMISSION

| Artifact | Declared last cycle | Computed now |
|---|---|---|
| `chart_p02.patch.txt` | `084b03c333c9c7cc…` | **identical** |
| `CHART-P02_CAPTURE_VERIFICATION.json.txt` | `7da21fadd4c5b2b5…` | **identical** |
| `CHART-P02_08_INSUFFICIENT_ICHIMOKU_ON_D1.png` | `9622a0a56734d720…` | **identical** |

The DA did exactly as instructed: **re-sent, did not re-cut.** Had anything been regenerated the hashes would have moved and the reconciliation with the already-published report would have been destroyed. That restraint is what makes the declared-hash discipline worth having.

`git apply --check` **exit 0** on the 13-element chain; applied clean. 3,285 lines / 16 files. **All 8 captures now reconcile against the JSON — fifteenth fully reconciled delivery.**

---

## 3. ✅ M2 — CONVENTIONS VERIFIED BY EXECUTION

I loaded `indicators.py` and computed each against hand-derived values. These are the exact places a plausible implementation goes wrong.

### CCI — the headline check

```
impl last       122.91666667
MAD formula     122.91666667   ← correct
stdev formula   105.87218463   ← the common error
```

**CCI uses mean absolute deviation, not standard deviation.** The two differ by 16%, so a wrong implementation would look entirely reasonable on a chart. Correct.

### The rest

| Indicator | Result |
|---|---|
| **HMA 20** | `123.58528139` vs manual `123.58528139`. First value at bar **23** = `n + √n − 1`, matching the registry. |
| **ADX/DMI 14** | `+DI 17.42334966` · `−DI 19.79416917` · `ADX 10.65002068` — all three exact against Wilder's smoothing computed independently. |
| **ROC 12** | `21.63661581` exact. |
| **Ichimoku** | tenkan `104.38710885`, kijun `105.31299690` — both exact against `(nH+nL)/2`. |
| **Z-Score 20** | population σ (`−0.89596612`) not sample (`−0.87327976`) — declared convention is the implemented one. |

### A correction of my own

My first Stochastic check reported a mismatch: impl `66.03480174` against my manual `51.53158632`. **My manual was the raw %K.** The signature is `(14, 3, 3)` — slow stochastic, with `smooth_k=3` applied to raw %K. Recomputing: smoothed `66.03480174` — **exact**. And `%D` = SMA3 of smoothed %K, also exact. **The error was mine, and the implementation is right.**

---

## 4. ✅ M6 — ICHIMOKU DISPLACEMENT HANDLED HONESTLY

This was the subtlest requirement in the Build Order: forward displacement must not imply data beyond the last bar. Measured offsets from the final bar:

```
tenkan  +0    kijun  +0    senkou_a  +0    senkou_b  +0    chikou  −26 min
```

**Senkou spans are clamped to the last bar — no phantom future candles.** Chikou correctly lags 26 periods. A naive implementation plots the cloud 26 bars into the future, which on a simulated feed would be fabricated forward data. It does not.

Capture 08 confirms M4 in the product: *"Ichimoku: insufficient history (78 required, 5 available) — no series rendered"* — pill active, zero lines. `required_bars: 78` is the full definition (52 + 26 displacement), not the earliest drawable bar. The MACD precedent applied correctly.

---

## 5. ✅ M5 · M7 · M9 · R1–R7

**M5 — toolbar (capture 01).** SMA 20 / SMA 50 / EMA 20 remain direct pills; five engine menus carry the rest; active indicators show as dismissible chips. **The three most-used are reachable in the same interaction count as before** — the governing-reframe condition held.

**M6 — pane budget (capture 07).** *"STOCH1433: pane budget reached — at most 3 pane indicators concurrently; the indicator was NOT enabled"* with `pane budget: 3/3 (policy: price pane keeps a 280px minimum)`. Explicit refusal, stated policy, nothing silently dropped.

**M7 — time-axis sync.** `subscribeVisibleLogicalRangeChange` / `setVisibleLogicalRange` now present (3 call sites; **was 0** in CHART-P01). The JSON records all three panes sharing one range after zoom — `syncedFrom 1787051880 / syncedTo 1787078760`, identical across panes. Capture 04 was taken **after** a zoom as required.

**M9 — no directional verdicts.** Grep across indicator service, registry, UI registry and pane component for `bullish|bearish|oversold|overbought|golden cross|buy signal|eligib`: **clean**. The guard's forbidden list was extended with exactly those terms. Supertrend emits bands only — no trend verdict, which is the discipline I asked for on an indicator usually taught as a trading system.

**R1** — no generator, aggregation or CHART-P01 formula file in the patch. **R2** — 16 routes, registry untouched. **R5** — zero new dependencies; 16 formulae implemented explicitly. **R6** — `730.90 → 736.97 kB (+6.07 kB)`, into `OBS-5`.

---

## 6. EXECUTION EVIDENCE AND DEVIATIONS

Transcripts asserted, not re-run by me: **+16 BE / +6 FE tests**, `tsc` 0, identical build hash across two trees. The sixteen formulae, the displacement handling and the insufficiency behaviour I verified by **direct execution**, which for those properties is stronger than a transcript.

Eight deviations disclosed. Three deserve the record:

- **The pane-height policy failed its own rule on first capture** — three panes squeezed the price pane to 217px against the stated 280px minimum, and **the capture gate refused it**. The instrument caught its own author violating a requirement written in this Build Order. CSS now enforces it; capture 03 shows exactly 280px.
- **Two performance defects found by measuring S3, not by tests passing:** quadratic `session_levels` (1,158 → 31 ms) and per-point ORM attribute re-reads (ichimoku 363 → 119 ms).
- **A frontend/backend `lines` contract mismatch** surfaced as 0 overlay lines in capture 02 and was corrected. The capture gate did its job twice.

**VWMA was omitted with a stated reason** — the recommended option. No volume-weighted indicator ships over `gauss()` volume.

---

## 7. STATUS

| Item | State |
|---|---|
| **CHART-P02** | **APPROVED** |
| `CA-CHART2-1` artifacts not transmitted | **CLOSED** — exact-hash re-submission |
| M1–M9 · S1–S4 · R1–R7 | **All satisfied** |
| Indicator surface | **23 registered** (7 + 16) |
| `OBS-SURF3-1` | **Open** — same declared-not-transmitted pattern, DA |
| `OBS-CHART-1` · `OBS-DATA2-1` · `OBS-DATA-P01-WATCHLIST-CLIP` · `OBS-5` (736.97 kB) | Open |

**Programme queue:** CONV ✅ · SURF ✅ · DATA-P01 ✅ · DATA-P02 ✅ · CHART-P01 ✅ · **CHART-P02 ✅** · CHART-P03 · POLISH — neither authorized.

---

## 8. ASSESSMENT

The registry architecture CHART-P01 established did what it promised: sixteen indicators arrived as formula modules plus registry rows, with the endpoint and client architecture untouched. That claim is now tested rather than asserted.

Two judgements stand out. Clamping Ichimoku's senkou spans to the last bar rather than projecting a cloud into empty space — on a synthetic feed, forward-plotted values would be fabricated data wearing an indicator's clothing. And declaring `required_bars: 78` for Ichimoku rather than the 52 that would let something draw.

I also want to record that my own Stochastic check was wrong before the implementation was. I published the mismatch in working notes and then found my manual had ignored `smooth_k`. **The standard applies to my arithmetic too**, and the phase should not carry a suspicion that originated in my error.

The programme now has 23 indicators that compute correctly, disclose insufficiency honestly, refuse to overflow the surface, and never advise.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
Not authorization for CHART-P03 or POLISH. No implementation before the next Build Order.

**We don't guess. We prove.**
