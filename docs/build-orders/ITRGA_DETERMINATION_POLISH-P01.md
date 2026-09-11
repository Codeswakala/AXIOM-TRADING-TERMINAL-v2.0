# ITRGA DETERMINATION — POLISH-P01

**Reviewing body:** Independent Technical Review & Governance Authority
**Subject:** POLISH-P01 — open observations, simulator realism, evidence confluence
**Date:** 2026-08-18
**Base:** 15-element chain (through `chart_p03`)
**Verification:** `/tmp/p2` — pristine clone → 15-element chain → POLISH-P01 applied

| Artifact | sha256 | Size |
|---|---|---|
| `polish_p01.patch.txt` | `598d2ac91142f403` | 1,480 lines · 20 files |
| `DELIVERY_REPORT_POLISH-P01.md` | `08ba3318495ac05a` | 88 lines |
| `POLISH-P01_CAPTURE_VERIFICATION.json.txt` | `70b4ceef94b54984` | 256 lines |
| 7 PNGs | all reconcile, no dupes | — |

Declared patch hash matches computed. `git apply --check` **exit 0**. **Seventeenth consecutive hash-reconciled delivery.**

---

## 1. DETERMINATION

# APPROVED

Every mandatory requirement M1–M7 satisfied, every constraint R1–R6 honoured. No new findings.

**All observations carried since the CONV programme are now closed.**

---

## 2. ✅ M1 — THE DRIFT IS GONE, AND THE GENERATOR FENCE HELD

The patch changes **exactly three lines** in `chart_seed_service.py`:

```
- rng.gauss(0.0004,  0.0083)   → rng.gauss(0, 0.0083)    crypto
- rng.gauss(0.004,   0.015)    → rng.gauss(0, 0.015)     JPY
- rng.gauss(0.00004, 0.00015)  → rng.gauss(0, 0.00015)   forex
```

Sigma unchanged, wicks unchanged, volume unchanged. **The mean term only** — precisely the narrow authorization R1 granted.

**Verified by simulation across 12 seeds:**

| | before | after |
|---|---|---|
| 1 day (1,440 bars) | +5.2% | **+0.05%** |
| 6 days (8,640 bars) | **+31.4%** | **+0.31%**, range `[1.0889, 1.1197]` |

Direction now varies by seed rather than climbing deterministically. Capture 01 confirms it visually: five D1 bars oscillating in a 1.08–1.10 band with mixed direction, against the CHART-P02 capture where EURUSD climbed 1.24 → 1.44.

**The tripwire I set was not triggered.** I checked the patch for edits to CHART test expected values — **none**. `test_live_market.py` is **untouched**, so the DATA-P01 determinism test was re-run rather than rewritten, exactly as required. That was the discipline most at risk in a phase that reopens closed code, and it held.

---

## 3. ✅ M2 — `OBS-5` DISCHARGED, AND RBAC PROVEN AT CHUNK LEVEL

**Initial chunk `748.05 → 626.51 kB` (−121.5 kB, −16.2%).** Six lazy chunks: Intelligence 45.21 · ResearchHub 37.72 · ExecutionResearch 20.67 · TradePlanning 10.16 · ManualJournal 9.44 · LiveMarket 6.15 kB. Total 755.86 kB — the ~9 kB chunk overhead reported plainly rather than hidden behind the initial-chunk win.

**The requirement I flagged as the live risk — a chunk fetched for an unauthorized route is an information leak even if the render is blocked — is proven, not asserted:**

```
capture06 (authorized):    chunks = [index-N7jYdIYC.js, InstitutionalIntelligencePage-vt6XKB-Z.js]
capture07 (unauthorized):  chunks = [index-N7jYdIYC.js, index-N7jYdIYC.js]
                           intelligenceChunkFetched: false
                           "ACCESS DENIED … This is an access restriction, not an empty result."
```

The page chunk is **never requested** for a denied role. The mechanism is structural — the gate renders the denial before the lazy component mounts, and mounting is what triggers the fetch — and it is backed by a unit test that mocks the page module and asserts it is never imported. Denial text still discriminates restriction from absence, the `SURF-P03 M3` discipline.

---

## 4. ✅ M5 — CONFLUENCE STAYED ON THE AUTHORIZED SIDE OF THE LINE

This was the surface I said could still fail the programme's own constitution. Machine-recorded:

```
score:      "5 of 5 active indicators aligned (UP) · score 100%"
band:       "uncertainty ±0.00 (Wilson 95%)"
nonAct:     "NON-ACTUATING — evidence aggregation only"
statement:  "Aggregates the operator's currently active indicators over
             simulated data — not a market opinion."
```

That is a description of the operator's own indicator set with an uncertainty interval — the Advisory Signals precedent applied exactly. **No eligibility verdict, no risk/reward, no setup-quality judgement.** The forbidden vocabulary (`eligible`, `eligibility`, `risk/reward`, `setup quality`, `take the trade`) appears in the tree **only** inside the refusal list and the docblock stating what was constitutionally refused.

The distinction I drew in the Build Order — *"7 of 9 aligned" is description; "high-probability setup" is advice* — was respected without argument.

---

## 5. ✅ M3 · M4 · M6 · M7 · R1–R6

**M3** watchlist clip resolved (capture 02, with the gate corrected to scroll the rows and measure the horizontal clip axis). **M4** `ChartPlaceholderPage.tsx` deleted — confirmed absent. **M7** guard extended and pinned.

**M6** login and logo delivered — compass-with-epsilon monogram (capture 05), redesigned sign-in surface (capture 04). This discharges `F-BRAND-1` / `GA-173`, outstanding since turn 57 and the only programme item originating in an Operator design instruction rather than a review finding.

**R1** aggregation and all 29 formulae untouched · **R2** 16 routes · **R5** zero new dependencies, logo is inline SVG · **R6** reported both numbers.

**476 BE + 859 FE = 1,335 tests**, `tsc` 0, build hash reproduced identically.

---

## 6. 🔵 A CORRECTION OF MY OWN — MY M6 INVENTORY CLAIM WAS WRONG

Deviation 5 states the Build Order's claim that the login page had *"no 3D/gradient/perspective treatment"* did not match the tree. **The DA is right and I was wrong.**

My inventory grep ran against `LoginPage.tsx` only. The 3D treatment lives in **`LoginPage.css`** — 20 perspective/gradient/transform rules that I never looked at. I reported `0` and wrote a Build Order requirement on that basis.

The DA did not argue the point or quietly build to a false premise. It stated the discrepancy, strengthened the card's depth treatment, added the required logo, and moved on. **That is the correct handling of a reviewer's error**, and it is the second time this programme that I have had to record one of my own — the Stochastic `smooth_k` misreading in CHART-P02 was the first.

The standard has to apply to my evidence as well as the DA's. **A grep against one file is not an inventory of a component.**

---

## 7. DEVIATIONS

Seven disclosed. Three worth recording:

- **Capture 06 initially recorded zero chunks against the dev server** — a dev server serves no chunk files, so the instrument would have shown "no splitting" on working code. Moved to the production preview build. An instrument that measures the wrong environment is a false negative.
- **Capture 07's unprivileged context shared the admin cookies** and never reached the login surface — the standing multi-user capture lesson, hit for the third time and fixed with a fresh browser context per role.
- **A dev-harness audit error** (`no such savepoint`, the registered TD-031 SQLite-concurrency class) appeared in the capture window. Login succeeded, denial rendered, no shipped artifact depends on that row. Disclosed because the log line is visible in the evidence, which is the right instinct.

---

## 8. STATUS — ALL OBSERVATIONS CLOSED

| Finding | State |
|---|---|
| `OBS-5` bundle | **CLOSED** — 626.51 kB initial, −16.2% |
| `OBS-DATA2-1` walk drift | **CLOSED** — +31.4% → +0.31% |
| `OBS-DATA-P01-WATCHLIST-CLIP` | **CLOSED** |
| `OBS-CHART-1` orphan placeholder | **CLOSED** — deleted |
| `F-BRAND-1` / `GA-173` | **CLOSED** — compass + epsilon |
| Confluence engine (11) | **CLOSED** — evidence-only, as authorized |
| `OBS-SURF3-1` | **Open** — DA, non-blocking, sole survivor |

**Programme:** CONV ✅ · SURF ✅ · DATA-P01 ✅ · DATA-P02 ✅ · CHART-P01 ✅ · CHART-P02 ✅ · CHART-P03 ✅ · **POLISH-P01 ✅**

**All authorized phases are delivered and approved.**

---

## 9. ASSESSMENT

The riskiest thing in this Build Order was M1, because it reopened generators that three correction cycles had stabilised. The failure mode in a cleanup phase is scope creep into code that is finally being touched again. Three lines changed, one term each, and the determinism test came back green without being edited.

`OBS-5` deserves a note. It sat open across five phases as "the bundle is too big". The actual cause was that nothing was ever split — sixteen routes eagerly imported into one chunk. Naming the cause turned an accumulating complaint into a bounded fix with a measurable result.

And M5 held the line that matters most. This programme spent eight phases establishing that a displayed value must mean what it claims — that a simulated price is labelled simulated, an aggregated interval is labelled aggregated, an insufficient indicator draws nothing, and an order block is geometry rather than institutional evidence. Confluence was the first surface that could have quietly turned all of that into a recommendation. It counts the evidence and refuses the conclusion.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This determination closes POLISH-P01. **Programme closure is a separate determination** and is not granted here. No implementation before the next Build Order.

**We don't guess. We prove.**
