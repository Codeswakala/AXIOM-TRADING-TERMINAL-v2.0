# ITRGA DETERMINATION — DATA-P01 CORRECTION CYCLE 2 (`CA-DATA1-2`)

**Reviewing body:** Independent Technical Review & Governance Authority
**Subject:** Correction submission against `CA-DATA1-2`, `OBS-DATA1-1`, `OBS-DATA1-2`
**Date:** 2026-08-18
**Base:** nine-element chain → `data_p01.patch.txt` → `data_p01_correction.patch.txt` → `data_p01_correction2.patch.txt`
**Verification:** `/tmp/d1` — pristine clone → 10-element chain → correction2 applied

| Artifact | sha256 | Size | Status |
|---|---|---|---|
| `data_p01_correction2.patch.txt` | `34edc1762b8691f9` | 222 lines · 5 files | New |
| `DELIVERY_REPORT_DATA-P01_CORRECTION2.md` | `24a381ab726f9964` | 142 lines | **New — supplied as required** |
| `DATA-P01_CAPTURE_VERIFICATION.json.txt` | — | 5 declared | New |
| 5 PNGs (re-captured) | all 5 reconcile | — | New |

---

## 1. DETERMINATION

# CORRECTION REQUIRED (third cycle) — evidence only

**Every code finding is closed.** `CA-DATA1-2`, `OBS-DATA1-1` and `OBS-DATA1-2` are all discharged in the tree, and I verified each independently rather than on assertion. The generator is now correct at every scale I can measure.

**The captures do not show what they are claimed to show.** The watchlist price column is clipped in every capture this cycle — `USD/JPY` renders as `15`, `BTC/USD` as `41,9`, `SOL/USD` as `1`. The report cites capture 01 as showing `USD/JPY 150.010`. **It does not.** Under the standing rule that for visual requirements the image is primary, the closure evidence for `OBS-DATA1-2` is not in hand — even though the code is right.

This is an evidence defect, not a code defect. No rework of the fix is required.

---

## 2. ✅ `CA-DATA1-2` — CLOSED

### Both paths now scale with price

```python
# seeder
idio_frac = Decimal(str(round(rng.gauss(0.0004, 0.0083), 5)))
step      = price * idio_frac + price * beta * factors[i]
# adapter
delta = (self._price * Decimal("0.0005")) * (…)
```

I ran both generators at all three base prices. **Same seed, 100 bars:**

| | BTC 42,000 | ETH 2,500 | SOL 150 |
|---|---|---|---|
| seed 7 | −1.15% | −1.15% | −1.15% |
| seed 21 | +10.33% | +10.33% | +10.33% |

**Exactly proportional.** Per-bar sigma is 0.830% for all three by construction, against the previous `BTC 0.083% / ETH 1.400% / SOL 23.333%`. The adapter tick is now 0.050% of price uniformly, against `0.012% / 0.200% / 3.333%`.

### The crypto factor stream was made fractional too

I did not ask for this and would have raised it if missed. Because the beta term is now `price * beta * factors[i]`, an absolute factor stream would have re-introduced the same distortion in the *correlation* term. The DA converted the crypto stream to fractional (`gauss(0, 0.002)`), giving a beta weight of **0.24** — same relative footing for every crypto. Forex and JPY remain at **0.40**, as verified last cycle.

**Second cycle running in which the DA generalised the fix correctly beyond the cited line.**

---

## 3. ✅ `OBS-DATA1-1` — CLOSED: the regression test is non-vacuous

`test_chart_seed_crypto_steps_are_relative_across_price_levels` seeds all three cryptos, reads **persisted rows** back, and asserts mean relative step `< 3%` with `max/min < 10`.

I checked it discriminates, per the standing non-vacuity requirement:

| | BTC | ETH | SOL | max/min | verdict |
|---|---|---|---|---|---|
| **Old absolute code** | 0.065% | 1.064% | **14.768%** | **227.97** | **FAILS** |
| **New proportional** | 0.640% | 0.640% | 0.640% | 1.00 | PASSES |

**It fails on the defect and passes on the fix.** It asserts a property, not a golden value, so it survives reseeding. This is the standard I have been asking for.

The T-1 guard was also extended with a third anchor (`assert "tofixed(3)" in text`), pinning the JPY precision routing so its removal breaks the build — the SURF-P03 M1 pattern applied correctly.

---

## 4. ✅ `OBS-DATA1-2` — code CLOSED, evidence NOT

```ts
const isJpy = sym.includes("JPY");
formattedPrice = isCrypto ? …2dp… : isJpy ? closeNum.toFixed(3) : closeNum.toFixed(5);
```

Both the price and range columns route from the quote convention. The named test asserts `price-usdjpy` renders `150.010` and **never 4+ decimals** (`not.toMatch(/\.\d{4}/)`) while `price-eurusd` keeps `1.08450`. Correct construction.

**But see §5 — the capture cited as proof does not show it.**

---

## 5. 🔴 `CA-DATA1-3` — CAPTURES CLIP THE PRICE COLUMN; REPORT CLAIM NOT SUPPORTED

| Field | Content |
|---|---|
| **Finding ID** | `CA-DATA1-3` (correction required — evidence) |
| **Requirement** | Standing evidence rule: for visual requirements **the image is primary**. A capture must show the region it claims (`OBS-CONV3-1`, `OBS-CONV3-5`, `OBS-SURF1-1`, `OBS-SURF1-2`). |
| **Evidence** | Capture 01 renders `USD/JPY` as **`15`**, `BTC/USD` as **`42,0`**, `AUD/USD` as **`0.`**. Capture 03 renders `BTC/USD 41,9`, `ETH/USD 2,5`, `SOL/USD 1`. The price column is truncated mid-number in all five captures. |
| **Failure** | Report §2 states *"Capture 01 (Rev C) shows **USD/JPY 150.010**."* **It does not** — it shows `15`. The single visual artifact offered for `OBS-DATA1-2` closure cannot be read, and `CA-DATA1-2`'s headline proof — comparable crypto percentages — is equally unreadable. Round 2's captures showed full values (`42,005.00`, `SOL/USD 155.00 +3.33%`); this round's do not. |
| **Not a code regression** | I checked: `data_p01_correction2.patch.txt` touches **no CSS and no capture script**. The dock diff is precision routing only. The tree's layout is unchanged from round 2, so this is a capture-environment artifact (viewport/scroll/zoom), not a defect the patch introduced. **Do not modify layout code in response to this finding.** |
| **Required Correction** | Re-capture 01 and 03 with the watchlist price column fully visible. Capture 01 must legibly show `USD/JPY 150.010` at three decimals. Capture 03 must legibly show BTC, ETH and SOL prices **and** their percentage changes, so the proportional-volatility fix is visible rather than inferred. |
| **Closure Evidence** | Two re-captures, hashes declared in the JSON. |
| **Owner** | DA |

**A caution I want on the record.** The report asserted a specific rendered value that the image contradicts. I do not read this as misrepresentation — the value is correct in the code and in the passing test, so the DA almost certainly read it from a working screen and captured from a differently-sized one. But it is precisely the failure mode the image-is-primary rule exists to catch: **a claim about what renders must be verified against the artifact being shipped, not against the developer's own screen.** The instrument and the shipped evidence must agree.

---

## 6. EXECUTION EVIDENCE

Fresh transcripts supplied and, unlike cycle 1, **asserted as executed this cycle**:

```
pytest -q                        421 passed, 1 warning in 124.84s
pytest test_live_market.py …     14 passed
npx vitest run                   170 files · 819 passed
npx tsc -b --force               0 errors
npm run build                    index-Dejk2QKj.js 720.67 kB
```

**1,240 tests (421 BE + 819 FE), +2 named tests.** I did not re-run these; recorded as **asserted transcripts**, per the standing distinction. The two new tests I verified by construction and by independent simulation (§2, §3), which is stronger than a transcript for those two.

Bundle `720.62 → 720.67 kB` (+0.05 kB). Rolls into `OBS-5`.

---

## 7. STATUS

| Item | State |
|---|---|
| `CA-DATA1-1` USD/JPY on crypto walk | **CLOSED** (cycle 1) |
| `CA-DATA1-2` crypto walk magnitude-blind | **CLOSED** — verified proportional at 3 price levels |
| `OBS-DATA1-1` M6 guard | **CLOSED** — regression test proven non-vacuous |
| `OBS-DATA1-2` JPY display precision | **Code CLOSED · evidence OPEN** via `CA-DATA1-3` |
| `CA-DATA1-3` captures clip the price column | **OPEN — blocker (evidence only)** |
| **DATA-P01** | **CORRECTION REQUIRED (cycle 3)** |
| `OBS-5` bundle · `F-BRAND-1` | Open — POLISH-P01 / GA-173 |

**Cycle 3 scope: two re-captures. No code changes.** If the re-captures show what the code already does, DATA-P01 closes.

I want to be plain about where this stands. **The engineering is done and it is good** — three scale defects found and fixed across two generators, each fix generalised correctly beyond the cited line, each closed by a test that fails on the old code. What remains is that the photograph of the finished work is out of frame. That is a five-minute fix, and I am holding the phase open only because approving a visual requirement on an unreadable image is the one thing this role must never do.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
Correction ≠ approval. This determination is not authorization for DATA-P02, CHART or POLISH.

**We don't guess. We prove.**
