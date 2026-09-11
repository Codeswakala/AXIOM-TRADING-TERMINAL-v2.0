# AXIOM BUILD ORDER — W2-U07

## ML Research: Statistical Validation Framework

**Build Order ID:** W2-U07
**Wave:** 2 — Machine Learning Research Framework · **Unit:** 07
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-14
**Authorized By:** ITRGA, following **W2-U06 APPROVED** (Platform v0.18.0; first model on rails) + operator
authorization ("authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → `08/09` frameworks (Tier 6) → Tier-7 registers → this Build Order (Tier 8).
**Binding decision:** `docs/ITRGA_WAVE2_GOVERNANCE_DECISION_LOG.md` (D-W2-001, market-agnostic).
**Builds on (honour, do not re-implement):** W2-U01 chronology guard · W2-U02 query port · W2-U03 causal
features · W2-U04 reproducible snapshot + temporal split/embargo · W2-U05 experiment registry · **W2-U06
model harness (pinned/approved-experiment training).**
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Deliver the **Statistical Validation Framework** — the layer that turns a trained baseline (W2-U06) into
**honest, *uncertain* numbers.** Per `07_ML_SPEC` §Statistical Validation, every experiment must include
**walk-forward validation, out-of-sample testing, cross-validation (time-series), bootstrap, confidence
intervals, effect size, and statistical significance** — and *"Results shall include uncertainty — not
only point estimates."* This unit makes uncertainty **mandatory** and leakage-free validation **structural**.

It validates *models produced by the pinned-experiment harness*; it **does not** add a new model family,
live signals, calibration (that is W2-U08), economic validation (W2-U09), or execution. It runs on
**realistically-sized** data so the numbers are meaningful (the W2-U06 degenerate small-sample metrics were
acceptable *only* because that unit proved machinery, not skill — validation must not repeat that).

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No leakage / look-ahead / non-temporal validation.** Walk-forward + OOS + CV must be **strictly
  temporal**, respecting the W2-U04 embargo/purge; folds must never let training see validation/test-period
  outcomes. A random/shuffled CV, or a fold that violates the embargo, is an automatic FAIL — proven refused
  by negative test. **The W2-U01/U03/U04 guards stay active during validation.**
- ❌ **No point-estimate-only reporting.** Every reported metric must carry **uncertainty** (confidence
  interval and/or bootstrap distribution). A bare point estimate with no uncertainty is non-conformant
  (`07_ML_SPEC` §Statistical Validation) — enforce it (a validation report missing uncertainty is rejected).
- ❌ **No p-hacking / selective reporting / post-hoc metric changes** (R18). The metrics + evaluation plan
  come from the **pre-registered experiment** (W2-U05); validation reports against that plan, not a
  retro-fitted one. No cherry-picking the best fold/seed.
- ❌ **No symbol identity leaking into validation partitions as a *feature*** (D-W2-001). Market/symbol may
  define evaluation *slices* (that is required — per-market eval), but never re-enter the model input.
- ❌ **No untested compiled dependency.** *If* this unit adopts `numpy`/`scipy`/`statsmodels` (likely for
  bootstrap/CI/effect-size), it **owes the wheel-compatibility spike** (install→import→smoke on Windows +
  Py3.14.6) as its own staged sub-gate (the W2-U06 standing note; plan §4.2). If it can be done in
  pure-Python/stdlib, that is acceptable and preferred for risk.
- ❌ **No execution / broker / live signal / credentials.** W1-U03 gate CLOSED; validation output is a
  **research report artifact**, never a tradeable signal. Live signals are Wave 3.
- ❌ **No secrets/PII in reports/logs/telemetry** (§77); **no DB reach-around** (§16).
- ❌ **No regression** (Wave-0/1 + W2-U01–U06). Full suite + prior guard/registry/harness tests + parity smoke.
- ✅ **Preserve:** advisory/research-first, tz-UTC, observability, the full dataset→feature→snapshot→split→
  experiment→model→validation chain, reproducibility (seeded), and all prior hardening.

---

## 3. Scope — Components A–G

### Component A — (Conditional) wheel-compatibility spike (staged sub-gate)
- If `numpy`/`scipy`/`statsmodels` (or any compiled lib) is adopted: deliver install→import→smoke on
  Windows + Py3.14.6, pin versions, record in ADR/delivery note. If pure-Python/stdlib suffices (e.g.
  hand-rolled bootstrap + normal/percentile CIs), state so and skip — **but never ship an import that fails
  on the operator's machine.** This spike is its own acceptance checkpoint.

### Component B — Walk-forward validation (the spine) (`07_ML_SPEC` §Statistical Validation)
- Rolling/expanding-window **walk-forward** over the temporal split, retraining the W2-U06 baseline per
  fold, evaluating on the subsequent out-of-sample window, **embargo respected** between train and eval.
- Deterministic/seeded; fold boundaries + counts recorded.

### Component C — Out-of-sample + time-series cross-validation
- **OOS** hold-out evaluation and **time-series CV** (e.g. forward-chaining / blocked CV) — **temporal
  only, never random.** A random-CV request is refused (`NON_TEMPORAL_CV` / reuse `SPLIT_LEAKAGE`).

### Component D — Uncertainty: bootstrap, confidence intervals, effect size, significance
- **Bootstrap** distribution of the metric(s); **confidence intervals** (report method + level, e.g. 95%
  percentile); **effect size** (vs. a stated null/baseline, e.g. the W2-U06 majority baseline); **statistical
  significance** (test + p-value, with the multiple-comparison caveat noted). **Every headline number ships
  with its uncertainty.**

### Component E — Validation report artifact (research-only, uncertainty-mandatory)
- A persisted **validation report** bound to the experiment_id + model artifact: per-fold and aggregate
  metrics **each with CI/bootstrap uncertainty**, effect size, significance, walk-forward config, embargo,
  per-market/timeframe slices where applicable (D-W2-001 slicing), and an explicit **"uncertainty included"**
  contract. **A report missing uncertainty is rejected** (negative test). Reproducible (seeded → same
  report hash, or documented bounded nondeterminism).

### Component F — Governance, registers, ADR
- **ADR:** *Statistical + Calibration Validation* (this unit covers statistical; calibration is W2-U08 —
  reference it).
- **Registers:** record leakage-in-validation risk (mitigated by temporal folds + embargo + negative test);
  overfitting/optimistic-metric risk; p-hacking risk (mitigated by pre-registered plan). Update
  `PROJECT_STATE`/`CHANGELOG`. Note deferrals (calibration W2-U08; economic W2-U09; generalization/drift
  W2-U10).
- **Re-confirm** the chain is not bypassable and validation cannot be run off a non-pre-registered plan.

### Component G — Verification & Delivery
- Full suite green (baseline **135** backend / **16** frontend) — 0 failed, no regression — **plus** new
  tests: walk-forward temporal correctness; **random-CV / embargo-violation REFUSED**; bootstrap + CI
  produced; effect size + significance produced; **report-without-uncertainty REJECTED**; reproducible
  validation (seeded → same); leakage guards still active; per-market slicing without identity-as-feature;
  no live signal / research-only report.
- Delivery Report per §5 (captured `-vv` named tests; committing-script method for any persisted-PG proof).

### Explicitly OUT of scope (defer)
Calibration (W2-U08); economic validation (W2-U09); multi-market generalization + drift + registry
maturation (W2-U10); new model families; live/operator-facing signals (Wave 3); execution (Wave 6).

---

## 4. Success Criteria (Definition of Done)

- [ ] (If compiled dep adopted) **wheel spike passes on Win/Py3.14.6**, versions pinned; else pure-Python +
      stated.
- [ ] **Walk-forward + OOS + time-series CV**, strictly temporal, embargo respected; **random/shuffled CV
      REFUSED** (negative test); guards active.
- [ ] **Uncertainty mandatory:** bootstrap + CIs + effect size + significance produced; **a report missing
      uncertainty is REJECTED**.
- [ ] Validation report artifact persisted, bound to experiment_id + model, per-fold/aggregate with
      uncertainty, research-only; **reproducible** (seeded).
- [ ] Runs on **realistically-sized** data (not the W2-U06 degenerate sample); metrics reported **honestly
      with uncertainty** (weak-but-honest is fine; suspiciously-strong triggers a leakage review).
- [ ] No leakage/look-ahead; no p-hacking (validates the pre-registered plan); no identity-as-feature; no
      live signal/execution; gate CLOSED; no secrets; no DB reach-around.
- [ ] ADR + registers synced; full suite green (135/16 + new tests); no regression; W2-U01–U06 tests still
      pass; conforms to `07_ML_SPEC` §Statistical Validation / §Research Integrity + 05 v2.0 (§16/§77) +
      D-W2-001.

---

## 5. Delivery Report & Evidence Requirements (MANDATORY — operator-run, target platform)

Operator-run, **Windows/PowerShell + PostgreSQL** evidence:
1. **(If applicable) wheel-spike evidence** (install/import/smoke on Py3.14.6, versions).
2. **Operator test console** (raw, `collected N`): backend `pytest` **≥135 + new tests, 0 failed**;
   frontend `vitest 16`; `ruff` clean; `tsc`/build clean.
3. **Migration evidence** (if schema added for validation reports): clean `alembic upgrade head` on
   `PostgresqlImpl`, new head shown. (If none, state so.)
4. **Walk-forward / temporal-CV evidence:** the run showing temporal folds + embargo respected; **random-CV
   / embargo-violation REFUSED** (reason code visible) — captured `-vv` by name.
5. **Uncertainty evidence:** a validation report/output showing metric(s) **with CI + bootstrap** + effect
   size + significance; and a **report-without-uncertainty REJECTED** test.
6. **Reproducibility evidence:** seeded validation re-run → same report/metrics (or documented determinism).
7. **Persisted-PG proof (committing-script method):** the validation-report row shown via raw `psql SELECT`
   returning ≥1 row (bound to experiment_id + model).
8. **Honesty + no-leakage evidence:** report the real numbers with uncertainty; shown grep/test that no
   identity-as-feature and no live-signal route added. **If metrics look strong, include the leakage/temporal
   -integrity checks that rule out look-ahead** (per the W2-U06 forward caution).
9. **CI green on PostgreSQL** (local acceptable; remote preferred), fail-closed.
10. **Parity smoke:** login → WS ticket 200 → live feed → candle fetch, unaffected.
11. Confidence **HIGH / MODERATE / LIMITED with justification — no fabricated percentages**; metrics stated
    **with uncertainty, honestly.**

---

## 6. Standards & Constraints
Clean architecture / bounded context (ML Research owns validation); **temporal, embargoed, leak-free
validation** (`07_ML_SPEC` §Statistical Validation; R18); **uncertainty mandatory** (CI/bootstrap — no bare
point estimates); **pre-registered plan governs** (no p-hacking/selective reporting); **no identity as
feature** (D-W2-001, slicing only); **reproducible** (seeded); **research-only** report (no signal/
execution); target-proven deps only; no secrets (§77); tz-UTC. Every change in the registers (R20).
Cross-platform (Windows + docker/PostgreSQL).

---

## 7. Process
Implement (spike first if needed) → internal verify (suite + walk-forward/CV + uncertainty + refusals +
reproducibility) → doc sync (PROJECT_STATE + registers + ADR) → Delivery Report with §5 evidence
(operator-run, green, leakage-refused, uncertainty-mandatory, honest metrics) → **submit to ITRGA** →
independent review → corrections if required → approval → next Build Order (W2-U08). The DA does not
self-approve, does not self-authorize the next unit, and does not open the broker gate or emit live signals.

---

## 8. Priority Guidance (if staged)
**A (wheel spike if needed) → B (walk-forward) → C (OOS + time-series CV; reject random) → D (bootstrap/CI/
effect-size/significance) → E (uncertainty-mandatory report + reject-if-missing) → F (ADR/registers) →
G (verify).** Highest-value/highest-risk: **temporal leakage in the folds** and **uncertainty enforcement**
— a validation framework that leaks, or that reports a point estimate with no CI, defeats its own purpose.
*Prove the leaky/random fold is refused and the uncertainty-less report is rejected.* Report honestly:
weak-with-uncertainty is a good result; **strong metrics get a mandatory leakage review before they're
believed.**

---

## 8b. Gate status
Research/advisory only — **no live signals (Wave 3), no execution (Wave 6), broker gate CLOSED.** Validation
produces research reports, never tradeable signals. W2-U08 (Calibration) is the recommended next unit and
needs its own Build Order.

---

*ITRGA — Turn the honest data into honest, uncertain numbers: walk forward through time with a moat between
train and test, bootstrap the metric, band it with a confidence interval, and refuse any report that hides
its uncertainty behind a single number. A weak result stated with error bars is worth more than a strong one
stated without them — and a strong one gets checked for leakage before we believe it. We don't guess. We
prove.*
