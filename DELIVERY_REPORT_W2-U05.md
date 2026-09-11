# Delivery Report — W2-U05

| Field | Value |
|-------|-------|
| Build Order | **W2-U05** ML Research: Experiment Registry + Pre-Registration Workflow |
| Platform | **0.17.0** |
| Date | 2026-07-13 |
| Author | Development Authority |
| Status | **Implemented — submitted for ITRGA review** |
| Approval | **Not self-approved** |
| Builds on | W2-U01 dataset/chronology, W2-U02 query/metadata, W2-U03 features, W2-U04 snapshot/splits |

---

## 1. Executive Summary

W2-U05 implements the **Experiment Registry** and **Pre-Registration Workflow**, the final ML Research gate layer before any model unit becomes reviewable.

It makes scientific integrity structural by requiring every future experiment to be:

- documented with mandatory fields;
- pinned to a frozen dataset `content_hash`;
- pinned to a split manifest `split_hash`;
- pre-registered;
- explicitly approved;
- immutable after approval;
- audited through append-only audit events.

This unit introduces **no model, no training, no inference, no prediction, no execution, no broker/provider live connection, and no credentials**.

---

## 2. Hypothesis / counter-hypotheses

### Hypothesis

AXIOM can enforce experiment governance before model work by rejecting undocumented, unpinned, unreproducible, random-split, or unapproved experiments while accepting only pre-registered, pinned, approved plans.

### Counter-hypotheses

| Counter | Result | Evidence |
|---------|--------|----------|
| Undocumented experiments may be accepted | **Falsified** | `test_undocumented_experiment_rejected` |
| Draft/unfrozen/unhashed pins may be accepted | **Falsified** | `test_unpinned_unfrozen_or_unhashed_experiment_rejected` |
| Experiment may run before approval | **Falsified** | `test_approval_required_before_runnable` |
| Approved experiment may be mutated | **Falsified** | `test_approved_plan_immutable_new_version_created` |
| Random split evaluation plan may pass | **Falsified** | `test_random_split_evaluation_plan_rejected` |
| Audit trail may be missing | **Falsified** | `test_audit_events_written_for_workflow` |
| Model/training code may be introduced | **Falsified structurally** | `test_no_model_training_code_introduced_in_experiment_registry` |

---

## 3. Implementation Summary

### 3.1 Experiment registry schema

Added ORM model:

```text
backend/app/db/models/experiment.py
```

Added Alembic migration:

```text
backend/alembic/versions/20260713_0009_w2_u05_experiment_registry.py
```

New table:

```text
experiments
```

Fields include:

- `experiment_id`
- `version`
- `status`
- `purpose`
- `hypothesis`
- `dataset_snapshot_id`
- `dataset_content_hash`
- `split_manifest_id`
- `split_manifest_hash`
- `feature_set_version`
- `model_family`
- `model_spec`
- `evaluation_plan`
- `approval_timestamp`
- `approver`
- `plan_hash`
- `previous_experiment_id`
- `notes`

### 3.2 Experiment registry service

Added:

```text
backend/app/ml/experiments/
```

Key files:

```text
errors.py
service.py
__init__.py
```

Implemented:

- `ExperimentPlanInput`
- `ExperimentRegistryService`
- `IncompleteExperimentError`
- `UnreproducibleExperimentPinError`
- `ExperimentApprovalRequiredError`
- `ImmutableExperimentError`
- `InvalidEvaluationPlanError`

### 3.3 Workflow

Implemented workflow:

```text
create draft → pre-register → approve
```

Only approved experiments are runnable by later units.

Approval records:

- approver;
- UTC approval timestamp.

### 3.4 Pin validation

An experiment must pin:

```text
frozen dataset snapshot id
snapshot content hash
split manifest id
split manifest hash
feature set version
```

Rejected cases:

- missing mandatory field;
- draft/unfrozen snapshot;
- missing or mismatched snapshot content hash;
- missing or mismatched split manifest hash;
- split not tied to the frozen snapshot;
- feature set version mismatch when present in split manifest;
- random split evaluation plan.

### 3.5 Immutability and versioning

Approved experiment plans cannot be mutated.

Any change must create a new version referencing the prior experiment.

### 3.6 Audit trail

Experiment registry actions append audit events through the existing audit seam:

- `experiment.create`
- `experiment.pre_register`
- `experiment.approve`
- `experiment.new_version`

No secret or PII fields are introduced.

---

## 4. Governance / Documentation Updates

Added:

- `docs/build-orders/BUILD_ORDER_W2-U05.md`
- `docs/build-orders/BUILD_ORDER_INTAKE_W2-U05.md`
- `docs/adr/ADR-025_Experiment_Registry_PreRegistration.md`
- `docs/evidence/W2-U05_OPERATOR_EVIDENCE_COMMANDS.md`

Updated:

- `PROJECT_STATE.md`
- `CHANGELOG.md`
- `README.md`
- `docs/governance/RISK_REGISTER.md`
- `docs/governance/TECHNICAL_DEBT_REGISTER.md`
- `docs/governance/GOVERNANCE_AMENDMENTS.md`
- `docs/governance/04_PROJECT_ROADMAP.md`
- backend version/system metadata;
- frontend unit label.

---

## 5. Evidence

### 5.1 Backend tests and Ruff

Commands run in DA sandbox using a temporary virtual environment outside the persisted workspace:

```bash
cd backend
ruff check .
AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_DATABASE_URL='sqlite+aiosqlite:///:memory:' \
AXIOM_DATABASE_AUTO_CREATE_SCHEMA=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
pytest -q
```

Result:

```text
All checks passed!
127 passed, 1 warning
```

### 5.2 Alembic local migration

Command:

```bash
cd backend
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w2u05.db' \
AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
alembic upgrade head
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w2u05.db' alembic current
```

Result:

```text
Running upgrade 20260713_0008 -> 20260713_0009
20260713_0009 (head)
```

### 5.3 Frontend no-regression

Commands:

```bash
cd frontend
npm ci
npm audit --audit-level=high
npm test
npm run lint
npm run build
```

Result:

```text
found 0 vulnerabilities
Test Files  8 passed (8)
Tests       16 passed (16)
tsc         clean
vite build  successful
```

Operator target evidence remains mandatory.

---

## 6. Tests Added

New file:

```text
backend/tests/test_experiment_registry.py
```

Tests:

| Test | Purpose |
|------|---------|
| `test_undocumented_experiment_rejected` | missing mandatory field rejected |
| `test_unpinned_unfrozen_or_unhashed_experiment_rejected` | draft/unfrozen snapshot and unhashed split rejected |
| `test_pre_registered_and_approved_experiment_accepted` | valid pinned experiment accepted through workflow |
| `test_approval_required_before_runnable` | runnable check blocked before approval |
| `test_approved_plan_immutable_new_version_created` | approved mutation rejected; new version created |
| `test_random_split_evaluation_plan_rejected` | random split plan rejected |
| `test_audit_events_written_for_workflow` | audit events written for registry workflow |
| `test_no_model_training_code_introduced_in_experiment_registry` | no model/training code introduced |

Backend baseline increased from **119** to **127**.

---

## 7. Explicit Negative Evidence

| Bad condition | Proof |
|---------------|-------|
| undocumented experiment | rejected `UNDOCUMENTED_EXPERIMENT` |
| unfrozen snapshot pin | rejected `UNREPRODUCIBLE_EXPERIMENT_PIN` |
| unhashed/mismatched split pin | rejected `UNREPRODUCIBLE_EXPERIMENT_PIN` |
| random split evaluation plan | rejected `SPLIT_LEAKAGE` |
| runnable before approval | rejected |
| approved plan mutation | rejected; new version path required |
| model/training code | structural test confirms absent |

---

## 8. Operator Evidence Command Pack

Created:

```text
docs/evidence/W2-U05_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes Windows/PowerShell + PostgreSQL commands for:

1. PostgreSQL migration to `20260713_0009`;
2. full backend/frontend test console;
3. named W2-U05 tests;
4. rejection evidence focused commands;
5. acceptance/immutability/audit focused commands;
6. optional persisted experiment/audit SQL proof;
7. no model/training grep;
8. CI/local equivalent;
9. parity smoke.

---

## 9. Out of Scope Confirmed

Not implemented in W2-U05:

- model training;
- model evaluation execution;
- inference;
- prediction;
- calibration/economic/statistical validation runs;
- live signals;
- broker/provider live connection;
- credentials;
- execution.

`model_family` and `model_spec` are inert plan metadata only.

---

## 10. Risks and Unknowns

| Risk / Unknown | Status | Mitigation |
|----------------|--------|------------|
| PostgreSQL migration not DA-run | Operator evidence required | command pack includes PG migration |
| Remote CI run | Still carried | command pack includes local/remote evidence |
| First model package compatibility | Deferred | W2-U06 must include target-platform compatibility spike |
| Experiment execution | Deferred | W2-U06+ only after ITRGA approval |

---

## 11. Confidence Statement

| Dimension | Rating | Justification |
|-----------|--------|---------------|
| Registry schema/workflow | **HIGH** | mandatory fields, statuses, pins, approval fields, plan hash implemented |
| Rejection guarantees | **HIGH in DA tests** | undocumented/unpinned/random-split/runnable-before-approval rejected |
| Immutability/audit | **HIGH in DA tests** | approved mutation rejected; new version and audit events tested |
| Target-platform correctness | **LIMITED until Operator evidence lands** | Windows + PostgreSQL evidence required by Build Order |
| Model gate readiness | **CONDITIONAL** | W2-U05 approval required before W2-U06 becomes reviewable |
| Overall package | **MODERATE-HIGH for implementation; conditional for approval evidence** | mandatory operator evidence remains required |

No percentage confidence is asserted.

---

## 12. Readiness Statement

> W2-U05 is implemented, tested locally, documented, and submitted for independent ITRGA review.  
> No model, training, inference, prediction, execution, broker connection, provider live connection, or credentials have been introduced.  
> DA does **not** self-approve.  
> Operator-run Windows + PostgreSQL evidence remains mandatory for approval.  
> W2-U06 must not begin until ITRGA approves W2-U05 and issues the next Build Order.

---

**End of Delivery Report W2-U05**
