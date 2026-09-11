# AXIOM — BUILD ORDER BO-B-ML
## Substantive Machine Learning: Real Model, Research-Tier Validation, Governed Promotion

| Item | Value |
|------|-------|
| Build Order ID | `BO-B-ML` |
| Programme | Backend Operationalization — the substantive path, now unblocked by real data (R1) |
| Authorizing authority | **Operator** (directive of 2026-08-20: "authorized") |
| Predecessors | BO-B-00 · BO-B-01 · BO-B-02 · BO-B-DATA (all APPROVED WITH OBSERVATIONS) |
| Governing documents | `07_ML_SPEC.md` · `05_SYSTEM_ARCHITECTURE.md` v2.0 · `SUBSTANTIVE_THRESHOLD_FRAMEWORK.md` (B-02 binding) · `VALIDATION_TIER_SEPARATION.md` (B-01 binding) · `09_DEVELOPER_REASONING_FRAMEWORK.md` §12 (dependency reasoning) |
| Implementer | Development Authority (DA) |
| Reviewer | ITRGA |
| Status | **ISSUED — awaiting DA implementation** |
| Governance Gate | CLOSED (unchanged) · Production NOT CERTIFIED (unchanged) |

---

## 0. Purpose and honest framing (read first)

This is the first unit that can produce a **real, governed, potentially promotable model**, because real historical data now exists (BO-B-DATA). But the honest technical reality — verified by ITRGA in code — is:

1. The codebase contains **only** the majority-class baseline (`app/ml/models/baseline.py`), whose own docstring states it "proves harness mechanics, not predictive skill."
2. **No real ML algorithm or library exists** in the dependencies (no numpy/scipy/sklearn/xgboost/lightgbm/catboost/torch).
3. The majority-class baseline **can never pass** the B-02 threshold gate (its effect ≈ 0 by definition, below the `≥ 0.05` statistical floor). Re-running it on real data would always fail, so it cannot produce the model B-03 needs.

Therefore this unit's real work is: **(a) implement a genuine learning algorithm**, **(b) run the governed research lifecycle over real data**, and **(c) promote the model if and only if it genuinely passes every threshold** — with an honest, documented negative result being a fully acceptable outcome.

**Definition of success for this unit:** a genuine, reproducible, governed ML research program was executed over real data, and the true outcome was reported. Success is **not** "a model was promoted." If no model passes thresholds, that negative result is a valid, valuable deliverable (ML Spec: "Failed experiments shall be documented with the same rigor as successful ones").

---

## 1. Objective

1. Implement a real, deterministic, market-agnostic, explainable predictive model (not the majority-class baseline).
2. Execute the full research-tier lifecycle over the real crypto corpus: pre-registration → walk-forward statistical validation → calibration → economic validation → cross-instrument generalization → eligibility evaluation.
3. Promote to `advisory_approved` **only** on genuine threshold passage; otherwise record the honest negative result.

---

## 2. Scope

### Phase 1 — Real model implementation

- **P1.1 — Algorithm.** Implement a genuine learning algorithm. **ITRGA recommendation (not mandate):** a seeded, deterministic, **pure-Python** implementation (e.g. logistic regression via SGD, or a small ridge/GBM) to respect the project's compatibility-safe pure-Python discipline and avoid dependency risk. A real ML library may be proposed **only** with full dependency-reasoning justification (Doc 09 §12: why necessary, maintenance/security implications, portability) and is subject to ITRGA review. The choice and its justification **must** be stated in the Delivery Report.
- **P1.2 — Properties (binding).** The model must be: deterministic for identical inputs (seeded, fixed feature order); market-agnostic (no symbol/provider/market identity feature; consistent with `_assert_no_identity_output`); explainable (coefficients / feature importance surfaced for the operator); and it must emit **real calibrated probabilities** (needed by the calibration gate — the B-02 degenerate-prior workaround is not acceptable here).
- **P1.3 — Features.** Work with the builtin v1 feature set (return_1, range_pct, rolling_return_3) and/or register **additional** market-agnostic, price-normalized, causal features **only if** the Delivery Report justifies each new feature against the ML Spec (relevance, low leakage, cross-market compatibility). No feature may encode symbol identity. No scope explosion — every added feature must carry a stated reason.

### Phase 2 — Research-tier lifecycle on real data

- **P2.1 — Experiment.** Pre-register + approve (with approver identity) an experiment over the **real** corpus (`source="historical:real"`, tier `research_validation`), referencing a real-data snapshot + temporal split + feature set. Use forward-return labels (the existing `derive_candle_labels`, no look-ahead).
- **P2.2 — Walk-forward statistical validation.** Temporal folds over real data; report effect vs majority-class null, p-value, fold count, held-out sample — against the B-02 statistical thresholds.
- **P2.3 — Calibration.** Real probabilities; report ECE + Brier — against the B-02 calibration thresholds.
- **P2.4 — Economic validation.** Full six-class cost model with **realistic crypto costs** (spread, commission, slippage, latency, liquidity, transaction costs); report the `economically_usable` / `economically_unusable` verdict — against the B-02 economic threshold.
- **P2.5 — Cross-instrument generalization.** Train on a subset of instruments, hold out **unseen instruments** (e.g. train on OKX H1 {BTC,ETH,SOL}, test on {XRP,ADA,DOGE}, or a forex-style split); report hold-out accuracy + degradation — against the B-02 generalization thresholds. Per B-02.3: this is a distinct, independently-governed research question; it must not reopen prior closed work.

### Phase 3 — Governed promotion (only on genuine passage)

- **P3.1 — Eligibility.** Run `GovernedModelEligibilityGate.evaluate()` over the trained model.
- **P3.2 — Promotion or honest negative.**
  - If **all** thresholds pass AND lineage is complete: `promote_to_advisory_approved` with approver identity + reason.
  - If **any** threshold fails: record the honest negative result (decision + reasons) and **do not** promote. The unit remains complete (research executed); no promotion is a valid outcome.

---

## 3. Exclusions (out of scope — do NOT do)

- **No** promotion of a model that fails any threshold, by any means or caller.
- **No** relabeling synthetic data as real; no training on the B-01 synthetic corpus at research tier.
- **No** fabrication of probabilities, metrics, or features; no p-hacking, no post-hoc hypothesis changes, no selective reporting (ML Spec research-integrity prohibitions).
- **No** live data feed, broker, execution, actuation, or gate-opening. The model remains a **research artifact**; it does not emit signals (that is B-03).
- **No** new ML library dependency without justification (Phase 1 constraint).
- **No** frontend changes. **No** assistant (B-06) work. **No** intelligence/alerts (B-04/B-05).
- **No** modification of the governance hierarchy or constitutional documents.
- **No** repository publication (custody model).
- **No** reopening of previously closed experiments.

---

## 4. Exact deliverables

1. A real model implementation (new module under `app/ml/models/`) with deterministic, explainable, probability-emitting behavior.
2. One approved experiment + trained `model_artifact` (research-tier, real data).
3. `validation_reports`, `calibration_reports`, `economic_reports`, `generalization_reports` rows (research-tier, real data).
4. An eligibility evaluation with the honest decision (PROMOTED or NOT-PROMOTED-with-reasons).
5. A Delivery Report (§10) with transmission manifest, algorithm-choice justification, and feature justification.

---

## 5. Dependencies

- **Upstream:** BO-B-DATA (real corpus, `historical:real` → AUTHORITATIVE) · BO-B-02 (threshold gate, fail-closed) · BO-B-01 (snapshot/split/feature machinery, tier rule).
- **Downstream:** B-03 (signals) consumes a **promoted** model — B-03 therefore proceeds only if this unit's P3.2 promotes; otherwise B-03 remains gated and the negative result governs the programme's next steps.

---

## 6. Allowed files / components

- `backend/app/ml/models/**` (new model module; harness/baseline may be extended or a new module added).
- `backend/app/ml/validation/*`, `calibration/*`, `economic/*`, `generalization/*`, `experiments/*` (consume; no weakening).
- `backend/app/ml/features/*` (register new market-agnostic features only with justification).
- `backend/app/trading_intelligence/inference/service.py` (consume the gate; do not weaken thresholds).
- `backend/tests/**` (new/churn tests).
- `backend/docs/**` (any ADR for the algorithm/dependency decision).
- The Delivery Report.

Anything outside this list is **not authorized**.

---

## 7. Security & integrity constraints (binding)

- No secrets/credentials. No new network surface (data already ingested; model training is local).
- The threshold gate, tier rule, and chronology guard must **not** be weakened. The fail-closed promotion semantics from B-02 remain binding.
- **Scientific integrity (ML Spec):** walk-forward only; out-of-sample only; no look-ahead; no data leakage; no post-hoc hypothesis changes; calibration and economic verdicts reported independently; negative results documented with full rigor.
- Any new dependency must be justified (Doc 09 §12) and must not introduce supply-chain risk beyond the existing severity/exception policy (BO-B-00.2).

---

## 8. Acceptance criteria

### Phase 1
- [ ] Real algorithm implemented; deterministic (seeded) and reproducible.
- [ ] Market-agnostic (no identity feature); explainable (coefficients/importance surfaced).
- [ ] Emits real calibrated probabilities (not degenerate priors).
- [ ] Algorithm choice + dependency justification stated in the Delivery Report.

### Phase 2
- [ ] Experiment approved over real data (`historical:real`, `research_validation`).
- [ ] Walk-forward validation report present, real data, with effect/p/folds/sample.
- [ ] Calibration report present, real probabilities, ECE + Brier.
- [ ] Economic report present, full six-class cost model, realistic crypto costs, verdict stated.
- [ ] Generalization report present, hold-out on **unseen instruments**, degradation stated, distinct research question recorded.

### Phase 3
- [ ] Eligibility evaluated via the gate.
- [ ] EITHER promoted (all thresholds passed, approver identity + reason recorded) OR honest negative result recorded with reasons. **No third outcome.**
- [ ] The Delivery Report states which outcome occurred and why, with full metrics.

---

## 9. Evidence requirements (custody model + transmission manifest)

**Binding (CA-B01-1 / CA-DATA-1):** the Delivery Report must include a transmission manifest that reflects **what the Operator can actually relay** (with per-file splitting for large artifacts, and the pre-emptive "public-endpoint reconstruction" path offered for any immutable corpus-derived evidence). A declared-but-untransmitted artifact is an automatic CORRECTION REQUIRED.

| Item | Class | Form |
|------|-------|------|
| Patch artifact + per-file SHAs + `git apply --check` transcript | Level I | patch + transcript |
| Executed test output (new/churn tests) | Level II | run transcript |
| Research-run evidence (model + report row counts + metrics + honest decision) | Level I | query/probe output |
| Algorithm/dependency justification (ADR or report section) | Level III | document |
| Feature justification (each new feature) | Level III | report section |
| Transmission manifest (relay-accurate) | — | table in Delivery Report |
| Delivery Report | Level III | §10 structure |

---

## 10. Delivery Report structure (required)

1. Claimed scope vs. this Build Order
2. What changed (files + SHAs + chain position)
3. **Algorithm choice + dependency reasoning** (Doc 09 §12), and why pure-Python or library
4. Model properties evidence (determinism, no-identity, explainability, real probabilities)
5. Feature justification (each new feature, with ML Spec basis)
6. Experiment + reports (tier + data-class labels, real data)
7. **Honest outcome: PROMOTED or NOT-PROMOTED, with full metrics and reasons**
8. Test evidence (executed)
9. Deviations register
10. **Transmission manifest** (relay-accurate, CA-DATA-1)
11. Known limitations / technical debt

---

## 11. Rollback / containment

- Model + reports are additive rows; no schema migration is authorized by default.
- A promotion is reversible via the registry (status/approval history); no data loss.
- If a library dependency was justified and added, it must be pinned and removable without affecting the rest of the platform.

---

## 12. Completion condition

Complete when: all §8 criteria met, evidence (§9) transmitted and verified, the Delivery Report submitted, **and ITRGA issues its independent determination**. The unit is complete whether the outcome is promotion or an honest negative result — but a DA declaration of completion is not evidence and does not close this unit.

**Next authorization state:** upon ITRGA approval of BO-B-ML:
- If a model was **promoted**, B-03 (signals) may be issued against it.
- If the outcome was an honest **negative**, the programme's next step is an Operator decision (retry with more/broader data or features; or accept that the current data does not support an eligible model).

---

**End of Build Order BO-B-ML**
