# Build Order Intake — W2-U05

| Item | Value |
|------|-------|
| Build Order | W2-U05 — Experiment Registry + Pre-Registration Workflow |
| Date received | 2026-07-13 |
| Authority | ITRGA, following W2-U04 APPROVED + Operator authorization |
| DA status | ACCEPTED — implementation authorized by issued Build Order |
| Approval | Not self-approved; delivery requires ITRGA review |

---

## 1. Governance confirmation

The Development Authority confirms receipt of `docs/build-orders/BUILD_ORDER_W2-U05.md`.

The Build Order authorizes the final pre-model gate layer: experiment registry and pre-registration workflow. No model, training, inference, prediction, broker, or execution work is authorized.

## 2. Objective

Implement a registry where experiments are pre-registered, immutable, approved through an explicit step, audited, and pinned to exact frozen dataset snapshot and split manifest hashes.

## 3. Scope interpretation

| Component | DA interpretation |
|-----------|-------------------|
| A Registry schema | Add experiment table with mandatory ML_SPEC fields plus snapshot/split/feature pins and plan hash. |
| B Workflow | create draft → pre-register → approve; approval required before runnable. |
| C Pin validation | reject missing/unfrozen/unhashed/mismatched snapshot or split pins and random split plans. |
| D Audit | append audit events for create/pre-register/approve/new version. |
| E Governance | ADR/register/state/changelog updates. |
| F Verification | Add tests for rejection, acceptance, immutability, audit, no model code, no regression. |

## 4. Constraints

- No model/training/inference/prediction.
- No broker/execution/provider live connection.
- No undocumented/unpinned experiments.
- No mutation of approved plan.
- No self-approval bypass.
- No secrets/PII in notes/logs.

---

**End of intake**
