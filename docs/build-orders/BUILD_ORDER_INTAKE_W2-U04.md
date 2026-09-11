# Build Order Intake — W2-U04

| Item | Value |
|------|-------|
| Build Order | W2-U04 — Reproducible Dataset Snapshot Builder + Temporal Split Engine |
| Date received | 2026-07-13 |
| Authority | ITRGA, following W2-U03 APPROVED + Operator authorization |
| DA status | ACCEPTED — implementation authorized by issued Build Order |
| Approval | Not self-approved; delivery requires ITRGA review |

---

## 1. Governance confirmation

The Development Authority confirms receipt of `docs/build-orders/BUILD_ORDER_W2-U04.md`.

The Build Order authorizes dataset snapshot builder and temporal split engine only. No model, training, inference, prediction, broker, or execution work is authorized.

## 2. Objective

Build reproducible dataset snapshot artifacts and deterministic temporal split manifests with label-horizon / embargo leakage refusal.

## 3. Scope interpretation

| Component | DA interpretation |
|-----------|-------------------|
| A Snapshot builder | Build frozen dataset snapshots from query-port/canonical records and pinned feature version; deterministic hashes. |
| B Temporal split engine | Time-only train/validation/test split; reject random/shuffle. |
| C Label horizon/embargo | Reject split where training label horizon overlaps validation/test boundary; accept properly embargoed split. |
| D Persistence/manifests | Add `dataset_split_manifests` table and manifest hash/lineage. |
| E Governance | Add ADR/register/state/changelog updates. |
| F Verification | Add tests for build-twice hash, split rejection, label leakage, no identity in training matrix, guard exclusions, no regression. |

## 4. Constraints

- No model/training/inference/prediction.
- No broker/execution/provider live connection.
- No random splits.
- No label horizon leakage.
- No synthetic/simulated authoritative training data.
- No symbol identity in training matrix.
- Preserve all previous hardening.

---

**End of intake**
