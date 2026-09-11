# AXIOM — BUILD ORDER B-02
## ML Research Machinery Executed + Substantive-Threshold Gate

| Item | Value |
|------|-------|
| Build Order ID | `BO-B-02` |
| Programme | Backend Operationalization (reconciled v2) |
| Authorizing authority | **Operator** (directive of 2026-08-19: "authorized") |
| Predecessors | `BO-B-00` APPROVED-WITH-OBS · `BO-B-01` APPROVED-WITH-OBS (CA-B01-1 binding here) |
| Governing documents | `BACKEND_ROADMAP_v2.md` §B-02 · `07_ML_SPEC.md` · `05_SYSTEM_ARCHITECTURE.md` v2.0 · `VALIDATION_TIER_SEPARATION.md` (B-01 binding rule) |
| Implementer | Development Authority (DA) |
| Reviewer | ITRGA |
| Status | **ISSUED — awaiting DA implementation** |
| Governance Gate | CLOSED (unchanged) · Production NOT CERTIFIED (unchanged) |

---

## 0. Purpose and honest framing (read before everything)

This is the pivotal phase — but its **honest** scope is narrower than the roadmap's aspirational label "ML Research Executed," and the difference is a constitutional matter, not a style choice.

Two verified facts constrain this order:

1. **The corpus is synthetic** (B-01, `source="synthetic"`, tier `pipeline_validation`). The binding tier rule (B-01.1a / `VALIDATION_TIER_SEPARATION.md`) states synthetic data may prove the pipeline but **may not substantiate research, economic, or generalization conclusions**.
2. **The only model is a majority-class baseline** (`app/ml/models/baseline.py`) whose own docstring states it "proves governance and harness mechanics, **not predictive skill**," and which **emits no probabilities** (calibration requires them). All ML tables are empty (0 experiments, 0 models, 0 reports).

Therefore **this order does NOT produce a valid predictive model, does NOT promote any model to `advisory_approved`, and does NOT claim any research conclusion.** It does two legitimate, necessary things:

1. **Executes the full governed ML lifecycle at `pipeline_validation` tier** — proving the machinery (pre-registration → approval → training → walk-forward → calibration → economic → generalization → eligibility evaluation) works end-to-end, with every report honestly labeled pipeline-tier.
2. **Installs the substantive-threshold gate** — the Operator's §5 correction: report *existence* must never equal scientific *acceptability*. Today `ModelEligibilityGate` checks only that reports exist; this order makes the gate enforce **numeric acceptance thresholds** so a threshold-failing model can never be promoted, by any caller, ever.

---

## 1. Objective

Make the ML research lifecycle *run* under governance, and make the promotion gate *honest*. The deliverables are: (a) an executed, evidence-bearing research pipeline run; (b) a documented, code-enforced substantive-threshold framework; (c) a governed generalization research question.

---

## 2. Scope (in scope)

### B-02.1 — Execute the governed research lifecycle (pipeline_validation tier)

Run, against the B-01 synthetic corpus, the full W2 machinery:

1. **Pre-register + approve** one experiment via `ExperimentRegistryService` (draft → pre_register → approve with approver identity), referencing a B-01 snapshot + split manifest + feature set.
2. **Train** via `BaselineModelHarness.train()` (majority-class baseline) → produce a `model_artifact`.
3. **Walk-forward statistical validation** via `StatisticalValidationService.validate()` → `validation_reports` row.
4. **Calibration** via `CalibrationService.calibrate()` → `calibration_reports` row.
5. **Economic validation** via `EconomicValidationService.validate()` over `HypotheticalTrade`s with a full cost model (spread, commission, slippage, latency, liquidity, transaction costs) → `economic_reports` row.
6. **Generalization** via `GeneralizationService.create_report()` over hold-out series → `generalization_reports` row (see B-02.3 for the governance treatment).
7. **Eligibility evaluation** via `ModelEligibilityGate.evaluate()` → record the honest decision.

**Every report, snapshot, and artifact must carry the `pipeline_validation` tier and a truthful data-class label.** No report may state or imply a research/economic/generalization conclusion.

### B-02.2 — Substantive-threshold framework (the §5 correction)

- **Define**, as a documented, referenced instrument (ADR-style, under `backend/docs/`), the explicit numeric acceptance criteria for each gate:
  | Gate | Thresholds to define (examples — DA proposes exact values, subject to ITRGA review) |
  |------|----------------------------------------|
  | Statistical | minimum out-of-sample accuracy/effect above baseline; significance level; minimum sample; walk-forward folds |
  | Calibration | maximum ECE; Brier bound; miscalibration warning threshold (existing default 0.15); base-rate-aware significance |
  | Economic | cost model completeness; `economically_usable` verdict requires net-positive after costs across scenarios |
  | Generalization | hold-out performance within a stated degradation bound vs in-domain |
- **Enforce in code:** extend `ModelEligibilityGate` so `promote_to_advisory_approved` (and `evaluate`) reject a model whose reports fail the numeric thresholds — not merely missing reports. Add rejection reasons (e.g. `STATISTICAL_THRESHOLD_NOT_MET`, `CALIBRATION_THRESHOLD_NOT_MET`, `ECONOMIC_NOT_USABLE`, `GENERALIZATION_THRESHOLD_NOT_MET`).
- The majority-class baseline is **expected to fail** these thresholds. That failure must be recorded honestly (a valid, documented negative result), not hidden and not overridden.

### B-02.3 — Generalization as a distinct governed research question (the §6 correction)

- Cross-market/hold-out evaluation is a **new research question**, independently identified, governed, and evaluated.
- It must **not** retroactively reopen or alter the outcome of any previously closed experiment.
- The generalization report must record its own domain scope, its hold-out separation, and its independence from prior closed work.

---

## 3. Exclusions (out of scope — do NOT do)

- **No** promotion to `advisory_approved` of any model in this unit (the pipeline-tier baseline must not be promoted; the threshold gate must refuse it).
- **No** claim of predictive skill, statistical significance as a research conclusion, economic viability, or generalization validity — all results are pipeline-tier, synthetic-data-bound.
- **No** acquisition or fabrication of "real" data to satisfy the substantive path (see §8 — that is a separate Operator decision).
- **No** new ML model families, no real training algorithms, no hyperparameter search (harness mechanics only).
- **No** inference, signals, alerts, or intelligence (B-03/B-04/B-05).
- **No** assistant work (B-06). **No** frontend changes.
- **No** gate-opening, actuation, broker/account/trading/execution state.
- **No** modification of the governance hierarchy or constitutional documents (except the documented threshold ADR, which is new, not an amendment).
- **No** repository publication (custody model).
- **No** reopening of closed experiments.

---

## 4. Exact deliverables

1. One approved experiment + one trained `model_artifact` (pipeline-tier, honestly labeled).
2. `validation_reports`, `calibration_reports`, `economic_reports`, `generalization_reports` rows (pipeline-tier).
3. An eligibility evaluation with the honest (expected: NOT eligible) decision and reasons.
4. A documented **substantive-threshold framework** (ADR-style) with explicit numeric criteria per gate.
5. Code enforcement: `ModelEligibilityGate` extended to enforce thresholds (new rejection reasons).
6. A **Delivery Report** (§10) with transmission manifest (§9, CA-B01-1).

---

## 5. Dependencies

- **Upstream:** BO-B-01 (closed) — snapshots, split manifests, features, and the tier rule are inputs.
- **Downstream:** B-03 (signals) requires an `advisory_approved` eligible model, which this unit **does not and must not produce** from synthetic data. See §8.

---

## 6. Allowed files / components

- `backend/app/ml/models/*` (harness, baseline) — pipeline-tier execution and labeling only.
- `backend/app/ml/validation/*`, `calibration/*`, `economic/*`, `generalization/*`, `experiments/*`.
- `backend/app/trading_intelligence/inference/service.py` (the eligibility gate — threshold enforcement).
- `backend/app/ml/dataset/*`, `features/*` (read/consume only; no weakening of the tier rule or guards).
- `backend/tests/**` (new/churn tests).
- `backend/docs/**` (threshold-framework ADR).
- The Delivery Report.

Anything outside this list is **not authorized**.

---

## 7. Security & integrity constraints (binding)

- No secrets/credentials. No new network surface. No weakening of `17_INSTITUTIONAL_SECURITY_STANDARD.md`.
- The tier rule and chronology guard must **not** be weakened; pipeline-tier reports must remain non-authoritative.
- The threshold gate must **fail closed**: any model that cannot be verified against thresholds is not promotable; no silent bypass; no caller can promote without threshold passage.
- Calibration requires probabilities; the majority-class baseline emits none. The DA must **disclose and address** this gap in the design plan (e.g. extend the baseline to emit degenerate calibrated probabilities for machinery proof, clearly labeled) — it may not silently skip calibration or fabricate probabilities.

---

## 8. Standing dependency — Operator decision required (not part of this unit)

The **substantive** ML path (a real model, real statistical/economic/generalization conclusions, and any `advisory_approved` promotion) requires **real historical market data**, which does not exist in this project. This is a programme-level decision for the Operator:

- **Option R1:** authorize acquisition of real historical data (a future, separately-governed unit), or
- **Option R2:** accept that the substantive research path — and therefore B-03 signal production with an eligible model — remains **blocked** until real data exists.

This unit is **not** authorized to resolve this by substituting synthetic data or by promoting a non-predictive baseline. The DA must note the standing dependency in the Delivery Report.

---

## 9. Evidence requirements (custody model + CA-B01-1 transmission manifest)

**Binding (CA-B01-1, carried from BO-B-01):** the Delivery Report **must** include a **transmission manifest** — a table mapping every declared artifact to its actual transmitted filename and hash. A declared-but-untransmitted artifact is an automatic **CORRECTION REQUIRED** on the delivery process, independent of whether ITRGA can independently reproduce the substance. This closes the twice-observed R3 gap.

| Item | Class | Form |
|------|-------|------|
| Patch artifact + per-file SHAs + `git apply --check` transcript | Level I | patch + transcript |
| Executed test output (new/changed tests) | Level II | run transcript |
| Research-run evidence (experiment/model/report row counts + honest NOT-eligible decision) | Level I | query/probe output |
| Threshold-framework ADR content | Level III | document |
| Transmission manifest (every declared artifact → filename + hash) | — | table in Delivery Report |
| Delivery Report | Level III | §10 structure |

---

## 10. Delivery Report structure (required)

1. Claimed scope vs. this Build Order
2. What changed (files + SHAs + chain position)
3. Experiment + model + reports produced (with tier labels and data-class labels)
4. Honest eligibility evaluation (decision + reasons — expected NOT eligible)
5. Substantive-threshold framework (the numeric criteria, as an ADR reference)
6. Gate-enforcement evidence (tests proving a threshold-failing model is refused)
7. Calibration-probability gap disclosure and how it was addressed
8. Generalization governance record (distinct research question, independence)
9. Standing-dependency note (real data — §8)
10. Test evidence (executed)
11. Deviations register
12. **Transmission manifest** (CA-B01-1)
13. Known limitations / technical debt

---

## 11. Rollback / containment

- Data artifacts are additive rows. No schema migration is authorized by default.
- The threshold-gate change is the riskiest edit: it must be proven to fail closed (tests for each new rejection reason) and must not break the existing eligibility tests.
- Revert: drop new rows, revert patch.

---

## 12. Completion condition

Complete when: all §2/§4 deliverables exist, acceptance criteria (§2 sub-bullets + threshold-gate tests) are met, evidence (§9) is transmitted and verified (transmission manifest complete), the Delivery Report is submitted, **and ITRGA issues its independent determination**. A DA declaration of completion is not evidence and does not close this unit.

**Next authorization state:** upon ITRGA approval of B-02, the next bounded Build Order may be issued — **subject to the §8 standing dependency**: B-03 (signals) cannot proceed to a *promoted-model* state without real data; the Operator's R1/R2 decision will determine the substantive path.

---

**End of Build Order B-02**
