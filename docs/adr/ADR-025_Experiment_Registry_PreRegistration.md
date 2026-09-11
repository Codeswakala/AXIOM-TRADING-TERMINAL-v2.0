# ADR-025 — Experiment Registry and Pre-Registration Workflow

| Field | Value |
|-------|-------|
| ID | ADR-025 |
| Title | Immutable pre-registered experiment plans pinned to dataset and split hashes |
| Date | 2026-07-13 |
| Status | Accepted |
| Deciders | Development Authority under Build Order W2-U05 |
| Domain | ML Research / Experiment Governance / Scientific Integrity |

---

## Context

W2-U05 is the final gate layer before any model unit becomes reviewable. `07_ML_SPEC` requires every experiment to be pre-registered and states that no undocumented experiment exists. Prior units established frozen dataset snapshots, temporal split manifests, and feature store artifacts. Experiments must pin those exact artifacts to prevent p-hacking, hidden experiments, and unreproducible results.

## Decision

Implement an experiment registry with:

- `experiments` table;
- immutable `experiment_id + version` identity;
- mandatory purpose, hypothesis, dataset, feature, model, evaluation plan, approval timestamp, version fields;
- pinned `dataset_content_hash`, `split_manifest_hash`, and `feature_set_version`;
- `plan_hash` over canonical experiment plan content;
- workflow: draft → pre_registered → approved;
- approval timestamp and approver;
- approved plan immutability; changes create a new version and supersede prior version;
- audit events for create, pre-register, approve, and new-version actions.

This unit records experiment plans only. It does not run models, training, inference, prediction, calibration, or evaluation.

## Alternatives Considered

| Option | Outcome | Rationale |
|--------|---------|-----------|
| Store experiments in free-form docs only | Rejected | Not queryable/enforceable enough for scientific integrity. |
| Allow draft experiments to be runnable | Rejected | Violates pre-registration and approval gate. |
| Allow post-approval mutation | Rejected | Enables p-hacking/post-hoc hypothesis changes. |
| Pin dataset id only | Rejected | Must pin exact content hash and split manifest hash for reproducibility. |

## Consequences

- W2-U06 model harness can only consume approved/pinned experiment plans.
- Undocumented or unpinned plans fail before model work.
- Approval and registration are reconstructable through audit events.
- Future experiment execution can verify the plan hash and artifact hashes before running.

## Compliance

Supports `07_ML_SPEC` Experiment Governance and Research Integrity, and preserves D-W2-001 by keeping model metadata inert until later model units.

---

**End ADR-025**
