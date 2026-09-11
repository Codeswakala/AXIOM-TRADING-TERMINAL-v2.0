# ADR-024 — Temporal Split Engine and Reproducible Snapshot Builder

| Field | Value |
|-------|-------|
| ID | ADR-024 |
| Title | Reproducible dataset snapshot builder with temporal split manifests |
| Date | 2026-07-13 |
| Status | Accepted |
| Deciders | Development Authority under Build Order W2-U04 |
| Domain | ML Research / Dataset Reproducibility / Statistical Integrity |

---

## Context

W2-U04 is the final dataset-layer unit before experiment registry. It must make two catastrophic ML failures impossible by construction: irreproducible datasets and split leakage. W2-U01 already defined dataset snapshots and chronology reason codes; W2-U03 already defined causal feature records. W2-U04 binds them into frozen dataset artifacts and temporal split manifests.

## Decision

Implement:

- `ReproducibleSnapshotBuilder` that builds frozen content-hashed snapshots from canonical records and pinned feature versions;
- deterministic feature matrix rows excluding symbol/provider/market identity;
- `TemporalSplitEngine` that allows only temporal splits;
- `DatasetSplitManifest` persistence table containing split boundaries, embargo, label horizon, counts, manifest JSON, and split hash;
- label-horizon/embargo rejection when training labels would overlap validation/test windows;
- deterministic split manifest hashing.

No model, training, inference, or prediction is introduced.

## Alternatives Considered

| Option | Outcome | Rationale |
|--------|---------|-----------|
| Random train/test split | Rejected | Violates time-series integrity and Build Order. |
| Keep split manifests only in memory | Rejected | Experiments must later pin reproducible split manifests. |
| Use dataframe stack now | Rejected | Existing stdlib/Pydantic/SQLAlchemy stack is sufficient for this layer and avoids Py3.14 dependency risk. |
| Build labels/model targets fully | Deferred | Labels are inert only for horizon tests; full target construction belongs later. |

## Consequences

- Snapshot and split artifacts become reproducible and auditable.
- Future experiments can pin exact dataset and split hashes.
- Leaky/random splits fail before model work begins.
- Feature matrix remains identity-free.

## Compliance

Supports `07_ML_SPEC` Dataset Governance, Statistical Validation, and Research Integrity. Preserves D-W2-001 and the Wave-2 hard gate before model training.

---

**End ADR-024**
