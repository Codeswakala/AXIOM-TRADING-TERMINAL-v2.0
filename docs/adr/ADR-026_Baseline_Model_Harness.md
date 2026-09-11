# ADR-026 — Baseline Market-Agnostic Model Harness

| Field | Value |
|-------|-------|
| ID | ADR-026 |
| Title | Pure-Python majority-class baseline harness bound to approved experiments |
| Date | 2026-07-14 |
| Status | Accepted |
| Deciders | Development Authority under Build Order W2-U06 |
| Domain | ML Research / Model Harness / Governance |

---

## Context

W2-U06 is the first model-touching unit after the ML Research foundation gate opened. The unit must prove the training harness can only train via an approved, hash-pinned experiment and must not introduce target-platform package failures on Windows + Python 3.14.6.

## Decision

Implement the first baseline as a **pure-Python majority-class classifier** rather than introducing numpy/scikit-learn in this unit.

Rationale:

- W2-U06 proves harness governance, artifact registration, refusals, and reproducibility — not predictive skill.
- Pure-Python stdlib avoids wheel/ABI risk on Python 3.14.6.
- More sophisticated ML dependencies can be introduced later through a dedicated compatibility spike and ADR.

The harness:

- loads only approved experiments;
- verifies frozen dataset hash, split hash, and feature records;
- consumes temporal split manifests as-is;
- refuses non-temporal splits;
- refuses identity fields at model input;
- emits research-only `ModelArtifact` rows;
- produces deterministic artifact hash and honest baseline metrics.

## Alternatives Considered

| Option | Outcome | Rationale |
|--------|---------|-----------|
| scikit-learn LogisticRegression | Deferred | Requires target package compatibility proof; unnecessary for harness mechanics. |
| numpy-only baseline | Deferred | Still a new dependency; pure Python is enough. |
| Train without registry lookup | Rejected | Violates W2-U05 gate. |
| Tune for predictive skill | Rejected | Skill is not W2-U06 goal; honest weak baseline acceptable. |

## Consequences

- No new ML dependencies are required.
- Baseline metrics are humble by design and must be reported honestly.
- Future model units may replace/extend model family after compatibility proof.
- Model gate remains research-only; no live signals or execution.

## Compliance

Supports `07_ML_SPEC` Model Types, Training Framework, Model Registry, Deployment Policy (research-only), and Research Integrity. Preserves D-W2-001 by enforcing identity exclusion at model input.

---

**End ADR-026**
