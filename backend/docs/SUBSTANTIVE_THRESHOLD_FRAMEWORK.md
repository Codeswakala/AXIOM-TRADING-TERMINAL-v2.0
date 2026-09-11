# AXIOM — Substantive-Threshold Framework
## Binding numeric acceptance criteria for model promotion (BO-B-02 §B-02.2)

| Item | Value |
|---|---|
| Instrument | `BO-B-02` §B-02.2 (Operator-authorized 2026-08-19; the §5 correction: *report existence ≠ scientific acceptability*) |
| Status | **BINDING** — enforced in code by `GovernedModelEligibilityGate` (`backend/app/trading_intelligence/inference/service.py`) |
| Precedent | `VALIDATION_TIER_SEPARATION.md` (BO-B-01 binding rule) — thresholds are evaluated on top of, and never instead of, the tier rule |

## R1 — The four gates and their numeric criteria (as proposed by the DA)

### Statistical gate
A model's validation report must satisfy ALL of:

| Criterion | Threshold | Source field |
|---|---|---|
| Out-of-sample accuracy above null | `effect_size.value ≥ 0.05` (accuracy minus majority-class null) | `validation_report.effect_size` |
| Statistical significance | `significance.p_value ≤ 0.05` | `validation_report.significance` |
| Walk-forward discipline | `len(fold_results) ≥ 3` folds | `validation_report.fold_results` |
| Minimum held-out sample | `sum(fold test_count) ≥ 300` rows | `validation_report.fold_results` |

### Calibration gate
| Criterion | Threshold | Source field |
|---|---|---|
| Expected calibration error | `ECE ≤ 0.10` (miscalibration warning stays at 0.15 — a warning is not a pass) | `calibration_report.expected_calibration_error` |
| Brier bound | `brier_score ≤ 0.20` (stricter than the balanced-class null of 0.25) | `calibration_report.brier_score` |

### Economic gate
| Criterion | Threshold | Source field |
|---|---|---|
| Usability verdict | `economic_conclusion.verdict == "economically_usable"` (net-positive after costs) | `economic_report.economic_conclusion` |
| Cost-model completeness | the base scenario lists all six cost classes (spread, commission, slippage, latency, liquidity, transaction_costs) with non-negative values | `economic_report.cost_model` |

### Generalization gate
| Criterion | Threshold | Source field |
|---|---|---|
| Hold-out degradation | `validation_accuracy − holdout_aggregate_accuracy ≤ 0.10` (within the stated degradation bound) | `validation_report.metrics.accuracy` vs `generalization_report.holdout_results.aggregate_accuracy` |
| Hold-out floor | `holdout_aggregate_accuracy ≥ 0.50` (no worse than the balanced-class null) | `generalization_report.holdout_results` |

## R2 — Rejection reasons

`GovernedModelEligibilityGate.evaluate()` returns one reason per failed gate (in addition to the existing lineage reasons):

```
STATISTICAL_THRESHOLD_NOT_MET
CALIBRATION_THRESHOLD_NOT_MET
ECONOMIC_NOT_USABLE
GENERALIZATION_THRESHOLD_NOT_MET
```

`promote_to_advisory_approved()` inherits every one of them as a blocking reason.

## R3 — Fail closed

- A missing report → `MISSING_*_REPORT` (unchanged).
- A present report whose values are **malformed, unparsable, or absent** → the corresponding `*_THRESHOLD_NOT_MET` reason. Unverifiable is unpassable. No silent bypass; no caller can promote without threshold passage.
- Threshold passage is **necessary, not sufficient** — the experiment-approval, lineage, and tier rules still apply.

## R4 — Tier relationship

These thresholds govern *promotion*. They do not relax the validation-tier rule: a
pipeline-validation-tier artifact (synthetic corpus) may never substantiate a
research conclusion, even if its numbers hypothetically passed every threshold.
The majority-class baseline trained on the BO-B-01 synthetic corpus is expected
to fail the statistical, calibration, and economic gates — and that honest
negative result is recorded, never overridden.

---

**End of Substantive-Threshold Framework (BO-B-02 §B-02.2)**
