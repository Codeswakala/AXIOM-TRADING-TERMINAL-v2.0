# ADR-028 — Calibration and Probability Quality Framework

| Field | Value |
|-------|-------|
| ID | ADR-028 |
| Title | Pure-Python calibration reports with Brier/ECE and base-rate-aware significance |
| Date | 2026-07-14 |
| Status | Accepted |
| Deciders | Development Authority under Build Order W2-U08 |
| Domain | ML Research / Calibration / Probability Quality |

---

## Context

W2-U08 must answer whether model probabilities are trustworthy. `07_ML_SPEC` requires calibration analysis, confidence bins, proper scoring, and explicit warnings when confidence is poorly calibrated. W2-U07 also carried a methodological correction: significance must be base-rate-aware rather than hard-coded to a 0.5 null.

## Decision

Implement a pure-Python calibration framework:

- fixed equal-width reliability bins;
- Brier score;
- Expected Calibration Error;
- miscalibration warning when ECE exceeds a configured threshold;
- per-slice calibration by market class, timeframe, and regime;
- no-information-rate/base-rate significance;
- persisted research-only calibration reports with deterministic report hash.

No compiled dependencies are introduced.

## Alternatives Considered

| Option | Outcome | Rationale |
|--------|---------|-----------|
| Use sklearn calibration utilities | Deferred | Requires compiled dependency compatibility spike; pure Python suffices. |
| Report Brier only | Rejected | Build Order requires reliability bins and explicit calibration warning. |
| Keep hard-coded 0.5 null | Rejected | Majority baseline on imbalanced data can look falsely skillful. |
| Tune bins after seeing results | Rejected | P-hacking risk; bin scheme is declared in config. |

## Consequences

- Poor calibration is explicitly flagged.
- Probability quality reports remain research-only.
- Base-rate-aware significance prevents majority baseline overclaim.
- Calibration is foundational; economic validation remains W2-U09.

## Compliance

Supports `07_ML_SPEC` Statistical Validation / Calibration and Research Integrity. Preserves D-W2-001 by using metadata only for slices, not features.

---

**End ADR-028**
