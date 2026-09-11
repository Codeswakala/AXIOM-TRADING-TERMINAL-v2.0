# ADR-027 — Statistical Validation Framework

| Field | Value |
|-------|-------|
| ID | ADR-027 |
| Title | Pure-Python statistical validation with uncertainty-mandatory reports |
| Date | 2026-07-14 |
| Status | Accepted |
| Deciders | Development Authority under Build Order W2-U07 |
| Domain | ML Research / Statistical Validation / Research Integrity |

---

## Context

W2-U07 must turn W2-U06 research-only model artifacts into honest validation reports. `07_ML_SPEC` requires walk-forward validation, out-of-sample/time-series validation, bootstrap, confidence intervals, effect size, statistical significance, and uncertainty — not just point estimates.

## Decision

Implement a pure-Python statistical validation framework:

- `ValidationConfig` for walk-forward/blocked time-series validation;
- `StatisticalValidationService` bound to approved experiments and model artifacts;
- temporal walk-forward folds with embargo;
- random/non-temporal validation refusal;
- bootstrap distribution and percentile confidence intervals;
- effect size vs. null accuracy;
- simple significance estimate vs. null baseline;
- `ValidationReport` persistence table with mandatory uncertainty contract;
- research-only status and audit event.

No compiled statistical dependency is introduced. Calibration and economic validation remain deferred to W2-U08/W2-U09.

## Alternatives Considered

| Option | Outcome | Rationale |
|--------|---------|-----------|
| Use scipy/statsmodels now | Deferred | Would require Windows/Python 3.14 wheel spike; pure Python is sufficient for foundation. |
| Report point estimates only | Rejected | Violates `07_ML_SPEC` Statistical Validation. |
| Random cross-validation | Rejected | Time-series leakage risk. |
| Add live signal endpoint | Rejected | Wave 3 only; W2 remains research-only. |

## Consequences

- Validation reports cannot omit uncertainty.
- W2-U07 remains dependency-light and target-platform safe.
- Statistical methods are intentionally foundational; deeper methods can be added in later validation units.
- Honest metrics with uncertainty become the default artifact.

## Compliance

Supports `07_ML_SPEC` Statistical Validation and Research Integrity. Preserves D-W2-001 and the W2-U01–W2-U06 governance chain.

---

**End ADR-027**
