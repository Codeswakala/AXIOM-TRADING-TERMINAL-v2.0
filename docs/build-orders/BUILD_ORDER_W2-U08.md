# AXIOM BUILD ORDER — W2-U08

## ML Research: Calibration + Probability Quality Framework

**Build Order ID:** W2-U08
**Wave:** 2 — Machine Learning Research Framework · **Unit:** 08
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-14
**Authorized By:** ITRGA, following **W2-U07 APPROVED** (Platform v0.19.0; statistical validation) +
operator direction to continue the Wave-2 sequence.

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → `08/09` frameworks (Tier 6) → Tier-7 registers → this Build Order (Tier 8).
**Binding decision:** `docs/ITRGA_WAVE2_GOVERNANCE_DECISION_LOG.md` (D-W2-001, market-agnostic).
**Builds on (honour, do not re-implement):** W2-U01 guard · W2-U02 query port · W2-U03 causal features ·
W2-U04 reproducible snapshot/split · W2-U05 experiment registry · W2-U06 model harness · **W2-U07
statistical validation (walk-forward, uncertainty-mandatory).**
**Carries forward:** the **base-rate-aware significance null** methodological correction from
`ITRGA_REVIEW_W2-U07.md` §4.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Deliver the **Calibration + Probability Quality Framework** — the layer that answers *"when the model says
70%, is it right 70% of the time?"* Per `07_ML_SPEC` §Statistical Validation (calibration) and plan §9.4,
calibration must be **a named validation layer, not an afterthought**: reliability/calibration curves, a
**Brier score** (or equivalent proper scoring rule), **confidence bins**, calibration **by market class /
timeframe / regime**, and an **explicit warning when confidence is poorly calibrated.**

The headline governance proof mirrors every prior guard/validation unit: **an intentionally-miscalibrated
fixture must be *detected*** (a model that claims 90% confidence but is right 50% of the time must be flagged
poorly-calibrated) — the calibration analogue of the W1-U03 gate refusal, the W2-U04 leaky-split refusal, and
the W2-U07 uncertainty-less-report rejection.

This unit also **discharges the W2-U07 carry-forward**: replace/augment the hard-coded `0.5` significance
null with a **base-rate-aware (No-Information-Rate) null**, so a majority baseline is never mistaken for skill.

This validates probability quality of model outputs; it adds **no new model family, no live signals, no
economic validation (W2-U09), no execution.**

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No miscalibration passing silently.** A poorly-calibrated model/output must produce an **explicit
  warning** (`07_ML_SPEC` §Statistical Validation) — an intentionally-miscalibrated fixture that is *not*
  flagged is an automatic FAIL. Prove detection by test.
- ❌ **No point-estimate-only calibration.** Consistent with W2-U07, calibration outputs (Brier, ECE/bin
  reliabilities) should carry appropriate uncertainty/bin counts; do not report a single reliability number
  with no bin support. (Reuse the W2-U07 uncertainty discipline.)
- ❌ **No leakage / non-temporal evaluation.** Calibration is computed on the **temporal validation/test
  outputs** from W2-U07 (embargo respected). No re-splitting, shuffling, or peeking. Guards stay active.
- ❌ **No base-rate-blind significance (carry-forward correction).** The significance null must be
  **configurable and default to the base rate (No-Information-Rate)**, not hard-coded 0.5; report skill
  **relative to the base rate.** A majority baseline evaluated against 0.5 (the W2-U07 artifact) must no
  longer read as "significant skill" — prove the corrected behaviour by test.
- ❌ **No symbol identity as a feature (D-W2-001).** Market/timeframe/regime define calibration *slices*
  (required), never re-enter the model input.
- ❌ **No p-hacking / cherry-picking bins or thresholds** (R18). Calibration reports against the
  pre-registered plan; bin scheme is declared, not tuned to flatter the curve.
- ❌ **No untested compiled dependency.** If numpy/scipy/sklearn is adopted (e.g. for calibration curves),
  it **owes the wheel-compat spike** on Windows + Py3.14.6 (standing note; plan §4.2). Pure-Python is
  acceptable and preferred for risk.
- ❌ **No execution / broker / live signal / credentials.** W1-U03 gate CLOSED; calibration output is a
  **research report artifact**, never a tradeable/operator-facing signal.
- ❌ **No secrets/PII** in reports/logs (§77); **no DB reach-around** (§16).
- ❌ **No regression** (Wave-0/1 + W2-U01–U07). Full suite + prior guard/validation tests + parity smoke.
- ✅ **Preserve:** advisory/research-first, tz-UTC, observability, the full chain, reproducibility (seeded),
  all prior hardening.

---

## 3. Scope — Components A–G

### Component A — (Conditional) wheel-compatibility spike (staged sub-gate)
- If a compiled lib is adopted: install→import→smoke on Windows + Py3.14.6, versions pinned, ADR-noted. If
  pure-Python (hand-rolled reliability bins + Brier), state so and skip — never ship a failing import.

### Component B — Calibration curve + Brier score (`07_ML_SPEC` §Statistical Validation; plan §9.4)
- **Reliability/calibration curve** (predicted-probability bins vs. observed frequency); **Brier score** (or
  equivalent proper scoring rule); **Expected Calibration Error (ECE)** or equivalent summary. Declared,
  fixed **confidence bins** (e.g. 10 equal-width or equal-count — stated, not tuned).

### Component C — Miscalibration detection + explicit warning (the headline)
- An explicit **"poorly-calibrated" warning** raised when calibration error exceeds a declared threshold.
- **Negative test (headline):** an **intentionally-miscalibrated fixture** (e.g. confidently-wrong
  predictions) is **detected and flagged**; a well-calibrated fixture is **not** flagged (positive/negative
  pair). This is the calibration analogue of the prior units' refusals.

### Component D — Per-slice calibration (market / timeframe / regime)
- Calibration computed **per market class, per timeframe, per regime** (D-W2-001 slicing — metadata for
  slices, never a feature). Surface which slices are well/poorly calibrated.

### Component E — Base-rate-aware significance null (W2-U07 carry-forward correction)
- Make the W2-U07 significance null **configurable**, defaulting to the **base rate (No-Information-Rate)**;
  report accuracy/skill **relative to the base rate** (and/or a balanced metric). **Test:** a majority
  baseline on imbalanced data is **NOT reported as significant skill** against the base-rate null (contrast
  the W2-U07 `p vs 0.5` artifact). Update the W2-U07 report path or add a corrected significance option.

### Component F — Calibration report artifact + governance
- Persist a **calibration report** bound to experiment_id + model + (W2-U07) validation report: curve/bin
  data, Brier, ECE, per-slice results, the poorly-calibrated warning flag, config (bin scheme, threshold),
  **research-only** status, reproducible (seeded → same report hash).
- **ADR:** *Calibration + Probability Quality* (+ the base-rate-null amendment). Registers updated
  (calibration-risk mitigated; W2-U07 base-rate observation **closed**); `PROJECT_STATE`/`CHANGELOG`; note
  deferrals (economic W2-U09; generalization/drift W2-U10).

### Component G — Verification & Delivery
- Full suite green (baseline **140** backend / **16** frontend) — 0 failed, no regression — **plus** new
  tests: calibration curve + Brier produced; **miscalibrated-fixture DETECTED / well-calibrated NOT flagged**
  (pair); per-slice calibration; **base-rate-aware null — majority baseline not "significant skill"**;
  uncertainty/bin-support present; reproducible (seeded); no identity-as-feature; no live signal; guards active.
- Delivery Report per §5 (captured `-vv` named tests; committing-script method for persisted-PG proof).

### Explicitly OUT of scope (defer)
Economic validation (W2-U09); multi-market generalization + drift + registry maturation (W2-U10); new model
families; live/operator-facing signals (Wave 3); execution (Wave 6).

---

## 4. Success Criteria (Definition of Done)

- [ ] (If compiled dep adopted) wheel spike passes on Win/Py3.14.6; else pure-Python + stated.
- [ ] Reliability/calibration curve + **Brier score** + ECE (or equivalent) with declared confidence bins.
- [ ] **Miscalibrated fixture DETECTED with explicit warning; well-calibrated fixture NOT flagged** — proven
      by test pair.
- [ ] Per market/timeframe/regime calibration slices (identity as slice only, never feature).
- [ ] **Base-rate-aware significance null** implemented + default; **majority baseline not reported as
      significant skill** — proven by test (W2-U07 carry-forward closed).
- [ ] Calibration report persisted (research-only), reproducible (seeded → same hash); bound to
      experiment/model/validation.
- [ ] No leakage/non-temporal; no p-hacking; no identity-as-feature; no live signal/execution; gate CLOSED;
      no secrets; no DB reach-around.
- [ ] ADR + registers synced (W2-U07 base-rate obs **closed**); full suite green (140/16 + new tests); no
      regression; W2-U01–U07 tests still pass; conforms to `07_ML_SPEC` §Statistical Validation + R18 +
      05 v2.0 (§16/§77) + D-W2-001.

---

## 5. Delivery Report & Evidence Requirements (MANDATORY — operator-run, target platform)

Operator-run, **Windows/PowerShell + PostgreSQL** evidence:
1. **(If applicable) wheel-spike evidence.**
2. **Operator test console** (raw, `collected N`): backend `pytest` **≥140 + new tests, 0 failed**;
   frontend `vitest 16`; `ruff` clean; `tsc`/build clean.
3. **Migration evidence** (if schema added for calibration reports): clean `alembic upgrade head` on
   `PostgresqlImpl`, new head shown. (If none, state so.)
4. **Calibration evidence:** reliability curve + Brier + ECE with declared bins for a model output.
5. **Miscalibration-detection evidence (headline, captured `-vv`):** intentionally-miscalibrated fixture →
   **flagged poorly-calibrated**; well-calibrated fixture → **not flagged**.
6. **Base-rate-null evidence (carry-forward):** the majority baseline evaluated against the **base-rate
   null** is **not** reported as significant skill (contrast W2-U07 `p vs 0.5`) — captured `-vv`.
7. **Reproducibility evidence:** seeded calibration re-run → same report/hash.
8. **Persisted-PG proof (committing-script method):** the calibration-report row via raw `psql SELECT`
   returning ≥1 row (bound to experiment/model).
9. **No identity-as-feature / no live-signal grep** (R7: cmd + empty output).
10. **CI green on PostgreSQL** (local acceptable; remote preferred), fail-closed — **capture the completion
    marker** this time (the W2-U07 LOW note).
11. **Parity smoke:** login → WS ticket 200 → live feed → candle fetch, unaffected.
12. Confidence **HIGH / MODERATE / LIMITED with justification — no fabricated percentages.**

---

## 6. Standards & Constraints
Clean architecture / bounded context (ML Research owns calibration); **calibration as a named layer** with
proper scoring (`07_ML_SPEC` §Statistical Validation; plan §9.4); **miscalibration flagged, never silent**;
**base-rate-aware significance** (carry-forward); **temporal, leak-free** (guards active; R18); **no identity
as feature** (D-W2-001, slicing only); **reproducible** (seeded); **research-only** (no signal/execution);
target-proven deps only; no secrets (§77); tz-UTC. Every change in the registers (R20). Cross-platform.

---

## 7. Process
Implement (spike first if needed) → internal verify (suite + calibration + miscalibration-detection pair +
base-rate-null + reproducibility) → doc sync (PROJECT_STATE + registers + ADR; **close W2-U07 base-rate
observation**) → Delivery Report with §5 evidence (operator-run, green, miscalibration detected, base-rate
null corrected, honest) → **submit to ITRGA** → independent review → corrections if required → approval →
next Build Order (W2-U09). The DA does not self-approve, does not self-authorize the next unit, and does not
open the broker gate or emit live signals.

---

## 8. Priority Guidance (if staged)
**A (wheel spike if needed) → B (reliability curve + Brier) → C (miscalibration detection + warning — the
headline) → E (base-rate-aware null — the carry-forward) → D (per-slice) → F (report/ADR/registers) →
G (verify).** Highest-value/highest-risk: **miscalibration detection** (a probability layer that can't tell
a confidently-wrong model from a well-calibrated one is worthless) and the **base-rate null correction**
(so significance never flatters a majority baseline). *Prove the miscalibrated fixture is caught and the
majority baseline is not mistaken for skill.*

---

## 8b. Gate status
Research/advisory only — **no live signals (Wave 3), no execution (Wave 6), broker gate CLOSED.** Calibration
produces research reports, never signals. W2-U09 (Economic Validation) is the recommended next unit and needs
its own Build Order.

---

*ITRGA — Make the model's confidence honest: when it says seventy percent, hold it to being right seventy
percent of the time, and raise a flag the moment it isn't. Catch the confidently-wrong fixture, score it
with Brier, band it by market and regime — and finally measure skill against the base rate, not a coin flip,
so no majority guess ever masquerades as an edge. We don't guess. We prove.*
