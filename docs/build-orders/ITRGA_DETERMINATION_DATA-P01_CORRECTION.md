# ITRGA DETERMINATION — DATA-P01 CORRECTION CYCLE (`CA-DATA1-1`)

**Reviewing body:** Independent Technical Review & Governance Authority
**Subject:** Correction submission against `CA-DATA1-1` (USD/JPY generated on the crypto walk)
**Date:** 2026-08-18
**Base:** nine-element chain → `data_p01.patch.txt` → `data_p01_correction.patch.txt`
**Verification:** `/tmp/d1` — pristine clone → full chain → correction applied

| Artifact | sha256 | Size | Status |
|---|---|---|---|
| `data_p01_correction.patch.txt` | `1bbaee09eb06f22f` | 86 lines · 2 files | New |
| `DATA-P01_CAPTURE_VERIFICATION.json.txt` | `e4273f49b4d7505a` | — | New (was `03375da8…`) |
| 5 PNGs (re-captured) | all 5 reconcile | — | New — see §5 |
| `DELIVERY_REPORT_DATA-P01.md` | `7c81db6901518203` | 206 lines | **Unchanged from round 1** — see §4 |

---

## 1. DETERMINATION

# CORRECTION REQUIRED (second cycle)

`CA-DATA1-1` is **CLOSED**. The fix is correct, and it went further than I asked — the DA found a **second** instance of the same defect that I missed.

But the same root cause survives in a third place. **`SOL/USD` renders at +3.33% against `BTC/USD`'s +0.01%** in capture 03 — the crypto branch applies one absolute step to every crypto regardless of base price. This is `CA-DATA1-1`'s pattern, not a new class of problem.

---

## 2. ✅ `CA-DATA1-1` — CLOSED

### Fixed, and more thoroughly than required

```python
is_crypto = market_class == "crypto"
is_jpy    = market_class == "forex" and symbol.endswith("JPY")
```

The `price >= Decimal("100")` proxy is gone. I grepped the entire backend: **no price-magnitude branch survives** in any executable line.

**The DA found a second site I did not flag.** `backend/app/market/adapters/simulated.py:129` carried the identical proxy on the live-tick path — USD/JPY was taking a ±5.00/tick crypto step there too. My finding cited only `chart_seed_service.py`. The DA corrected both. **That is the right response to a finding: fix the defect class, not the cited line.** Credit where due.

### The JPY scale is right

| | per-bar sigma | as % of base |
|---|---|---|
| EUR/USD | 0.00015 | 0.01364% |
| USD/JPY (corrected) | 0.015 | 0.01000% |
| USD/JPY (**before**) | 35.0 | 23.3% |

Three seeds over 100 bars: USD/JPY `+0.525% / +0.252% / +0.145%` against EUR/USD `+0.715% / +0.344% / +0.197%`. **Same order of magnitude — the objective.** Versus the old path, which reached **976.22 (+550%)**.

3-decimal quantization matches JPY convention, as required.

### The beta is no longer inert

`factor_scale = Decimal("100")` for JPY. Correlation weight against idiosyncratic sigma:

```
before:  0.00006 / 0.015 = 0.004   (numerically inert)
after:   0.00600 / 0.015 = 0.40    (equal to every other forex pair)
```

The DA's comment claims "0.4 of one idiosyncratic sigma." **I computed it independently: 0.40.** The claim is accurate. USD/JPY's `beta = -1.0` now actually expresses the USD correlation instead of being rounded into nothing.

---

## 3. 🔴 `CA-DATA1-2` — CRYPTO WALK IS MAGNITUDE-BLIND (SOL/USD AT +3.33%)

| Field | Content |
|---|---|
| **Finding ID** | `CA-DATA1-2` (correction required) |
| **Requirement** | Build Order S1/S3 — realistic per-class walks. Same requirement as `CA-DATA1-1`. |
| **Evidence** | **Capture 03 (image is primary):** `BTC/USD 42,005.00 +0.01%` · `ETH/USD 2,505.00 +0.20%` · **`SOL/USD 155.00 +3.33%`**. Three assets on one feed, three orders of magnitude apart in volatility. |
| **Root cause** | Both crypto paths apply an **absolute** step to every crypto irrespective of base. Adapter: `delta = Decimal("5")` — that is 0.012% of BTC but **3.33% of SOL**. Seeder: `rng.gauss(8, 35)` — 0.083% per-bar sigma on BTC, **23.3% on SOL**. |
| **Quantified** | Seeder, 100 bars from base: BTC `42,596 (+1.42%)` · ETH `3,096 (+23.85%)` · **SOL `746.37 (+397.58%)`**. |
| **Why it matters** | Identical in kind to `CA-DATA1-1`: a step calibrated for one price level applied to an instrument at another. SOL tripling within a session is not a plausible series, and the visible +3.33% against BTC's +0.01% is exactly the "would not survive an institutional reader's first glance" test that opened this cycle. `SOLUSD` at base `150.00` was **added by DATA-P01** — this is new surface, not inherited. |
| **Required Correction** | Make the crypto step **proportional to base price** rather than absolute — e.g. express idiosyncratic step and wicks as a percentage of the current price so BTC, ETH and SOL share a relative volatility profile. Apply to **both** `chart_seed_service.py` and `adapters/simulated.py`. |
| **Closure Evidence** | Fresh capture 03 showing all three crypto rows with comparable percentage changes; the printed per-bar sigma-as-%-of-base for all three within one order of magnitude. |
| **Owner** | DA |

**Recommended, not required:** the same absolute-step reasoning should be swept across every remaining walk parameter. The fix pattern is now established twice; a third recurrence should not need a finding.

---

## 4. 🟠 `OBS-DATA1-2` — USD/JPY DISPLAYED AT 5 DECIMALS

`TerminalWatchlistDock.tsx:212–217` formats on a binary `isCrypto` test:

```ts
formattedPrice = isCrypto ? toLocaleString(…2dp…) : closeNum.toFixed(5);
```

Capture 01 shows **`USD/JPY 150.01000`**. The backend now correctly generates 3-decimal JPY ticks; the frontend pads them to five. A JPY pair is never quoted to five decimals.

Low severity — cosmetic, no fabricated value, the digits are real zeros. But it undercuts the correction's own purpose: the tick convention was fixed in the generator and lost at the render layer. **Recommended:** route display precision from the instrument's class/convention rather than a crypto boolean.

### `OBS-DATA1-1` — M6 guard: still not delivered

The correction adds **zero test files** and touches no frontend test. M6 remains undischarged from round 1. Restated, not escalated.

---

## 5. TRANSPORT AND EVIDENCE

**Correction patch:** sha256 `1bbaee09eb06f22f`, 86 lines, 2 files. `git apply --check` **exit 0** on the full chain; applied clean.

**All five PNGs were re-captured** (new hashes, none identical to round 1) and **all five reconcile against the new JSON**. Dupe check clean. **Tenth consecutive hash-reconciled delivery.**

**Round-1 evidence preserved** at `/home/user/uploads_data_p01/`; this round at `/home/user/uploads_data_p01_r2/`.

### ⚠️ The delivery report was not updated

The submission was described as a delivery report, but `DELIVERY_REPORT_DATA-P01.md` is **byte-identical to round 1** (`7c81db6901518203`). It therefore still describes `USDJPY | 150.000 | forex (existing)` as though nothing changed, and **documents neither the correction nor the second site the DA fixed in `adapters/simulated.py`.**

The patch is the artifact of record and it is sound, so this does not block. But the DA's best work this cycle — finding the second defect site — exists only in a code comment. **Required with the next submission:** a correction report stating what changed, where, and the executed-test position.

### Execution evidence

**None supplied this cycle, and none claimed.** The correction changes generated series, so the round-1 transcripts are stale: `test_chart_seed_per_symbol_determinism_and_order_independence` and any golden values must be re-run. I did not re-run them. Recorded as outstanding.

---

## 6. STATUS

| Item | State |
|---|---|
| `CA-DATA1-1` USD/JPY on crypto walk | **CLOSED** — verified, both sites |
| `CA-DATA1-2` crypto walk magnitude-blind (SOL +3.33%) | **OPEN — blocker** |
| `OBS-DATA1-1` M6 guard absent | **OPEN** — restated |
| `OBS-DATA1-2` JPY displayed at 5 decimals | **OPEN** — low severity |
| Test transcripts post-correction | **Outstanding** |
| **DATA-P01** | **CORRECTION REQUIRED (cycle 2)** |
| `OBS-5` bundle · `F-BRAND-1` | Open — POLISH-P01 / GA-173 |

**Scope of cycle 2: proportional crypto steps in two files, the M6 guard, the display-precision routing, and a correction report with fresh transcripts.** Everything verified in round 1 and everything in this correction stands — do not rework seeding, correlation, provenance, labelling, or the JPY walk.

The trajectory is good. Round 1 fixed the `--` defect; this cycle fixed a scale defect and found one I had missed. What remains is the same lesson applied one instrument-class further: **a step size calibrated for one price level is not a step size, it is a coincidence.**

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
Correction ≠ approval. This determination is not authorization for DATA-P02, CHART or POLISH.

**We don't guess. We prove.**
