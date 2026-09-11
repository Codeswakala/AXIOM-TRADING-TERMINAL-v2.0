# Delivery Report — W2-U06

| Field | Value |
|-------|-------|
| Build Order | **W2-U06** ML Research: Baseline Market-Agnostic Model Harness |
| Platform | **0.18.0** |
| Date | 2026-07-14 |
| Author | Development Authority |
| Status | **Implemented — submitted for ITRGA review** |
| Approval | **Not self-approved** |
| Prerequisite | W2-U05 **APPROVED WITH OBSERVATIONS**; hard model gate open |
| Governing decision | D-W2-001 — generalized, market-agnostic model |

---

## 1. Executive Summary

W2-U06 delivers AXIOM's first model-touching unit: a **research-only baseline market-agnostic model harness**. The model is intentionally simple — a deterministic pure-Python majority-class baseline — because this unit proves governance and harness mechanics, not predictive skill.

The harness trains only through an approved, pre-registered, hash-pinned experiment. It verifies dataset/split/feature pins, consumes the W2-U04 temporal split manifest, refuses non-temporal/off-governance training, excludes symbol/provider/market identity at the model input boundary, and persists a research-only model artifact.

No live signals, inference API, prediction endpoint, execution, broker/provider live connection, or credentials are introduced.

---

## 2. Compatibility Spike

W2-U06 avoids new ML package risk by using a pure-Python stdlib baseline.

| Candidate | Decision | Rationale |
|-----------|----------|-----------|
| scikit-learn | Deferred | Requires Windows + Python 3.14.6 wheel compatibility proof; not needed for harness mechanics |
| numpy | Deferred | Still new dependency; not required for majority baseline |
| pure-Python majority baseline | Selected | No wheel/ABI risk; sufficient to prove training harness governance |

No `requirements.txt` ML dependency was added.

---

## 3. Implementation Summary

### 3.1 Baseline model

Added:

```text
backend/app/ml/models/baseline.py
```

Implements:

```text
MajorityClassBaseline
BaselinePredictionResult
```

The baseline:

- fits majority class on training labels;
- deterministic tie-breaks by lowest class;
- predicts same class for all rows;
- reports simple accuracy;
- exposes artifact payload with feature columns and seed.

### 3.2 Model harness

Added:

```text
backend/app/ml/models/harness.py
```

Implements:

```text
BaselineModelHarness.train(experiment_id, seed=42)
```

The harness:

1. loads an approved experiment;
2. verifies frozen dataset hash pin;
3. verifies split manifest hash pin;
4. refuses non-temporal splits;
5. loads feature records for pinned dataset and feature set;
6. builds identity-free matrices using manifest row ids;
7. fits majority baseline;
8. evaluates train/validation/test splits;
9. stores research-only `ModelArtifact`;
10. appends audit event.

### 3.3 Refusal errors

Added:

```text
backend/app/ml/models/errors.py
```

Errors:

- `ExperimentNotApprovedError`
- `UnresolvedExperimentPinError`
- `IdentityInModelInputError`
- `NonTemporalSplitError`

### 3.4 Model artifact registry fields

Extended:

```text
backend/app/db/models/model_artifact.py
```

Added Alembic migration:

```text
backend/alembic/versions/20260714_0010_w2_u06_model_artifact_registry.py
```

New fields:

- `experiment_id`
- `dataset_snapshot_id`
- `dataset_content_hash`
- `split_manifest_hash`
- `hyperparameters`
- `artifact_hash`
- `research_status`

Model artifact status is `research_only`.

---

## 4. Governance / Documentation Updates

Added:

- `docs/build-orders/ITRGA_VERDICT_W2-U05_FINAL.md`
- `docs/build-orders/BUILD_ORDER_W2-U06.md`
- `docs/build-orders/BUILD_ORDER_INTAKE_W2-U06.md`
- `docs/adr/ADR-026_Baseline_Model_Harness.md`
- `docs/evidence/W2-U06_OPERATOR_EVIDENCE_COMMANDS.md`

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

Commands run in DA sandbox using temporary virtual environment outside persisted workspace:

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
135 passed, 1 warning
```

### 5.2 Alembic local migration

Command:

```bash
cd backend
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w2u06.db' \
AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
alembic upgrade head
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w2u06.db' alembic current
```

Result:

```text
Running upgrade 20260713_0009 -> 20260714_0010
20260714_0010 (head)
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
backend/tests/test_model_harness.py
```

Tests:

| Test | Purpose |
|------|---------|
| `test_baseline_model_trains_approved_pinned_experiment` | approved pinned experiment trains and persists research-only artifact |
| `test_train_without_approved_experiment_refused` | rejects non-approved experiment |
| `test_unresolved_pin_refused` | rejects mismatched dataset pin |
| `test_identity_in_model_input_refused` | rejects symbol identity reaching model input |
| `test_non_temporal_split_refused` | rejects non-temporal split manifest |
| `test_reproducible_retrain_same_artifact_hash_and_metrics` | same experiment + seed yields same artifact hash and metrics |
| `test_pure_python_baseline_has_no_external_ml_dependency` | verifies no numpy/sklearn/pandas in baseline |
| `test_no_live_signal_or_model_api_endpoint_added` | verifies no live-signal/prediction endpoint added |

Backend baseline increased from **127** to **135**.

---

## 7. Explicit Negative Evidence

| Bad condition | Proof |
|---------------|-------|
| training without approved experiment | rejected `EXPERIMENT_NOT_APPROVED` |
| unresolved/mismatched dataset pin | rejected `UNRESOLVED_PIN` |
| identity in model input | rejected `IDENTITY_IN_MODEL_INPUT` |
| non-temporal split | rejected `NON_TEMPORAL_SPLIT` |
| external ML dependency import | not present |
| live signal / prediction API | not present |

---

## 8. Model Artifact Fields

The stored `ModelArtifact` includes:

- unique id;
- name/version;
- framework;
- feature set version;
- dataset snapshot id/hash;
- split manifest hash;
- experiment id;
- hyperparameters;
- metrics;
- artifact hash;
- research-only status.

The artifact is not deployed and cannot produce live signals.

---

## 9. Operator Evidence Command Pack

Created:

```text
docs/evidence/W2-U06_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes Windows/PowerShell + PostgreSQL commands for:

1. compatibility spike proof;
2. PostgreSQL migration to `20260714_0010`;
3. full backend/frontend test console;
4. refusal tests by name;
5. end-to-end train and reproducibility tests;
6. persisted PostgreSQL model artifact proof;
7. identity/no-live-signal grep;
8. CI/local equivalent;
9. parity smoke.

---

## 10. Out of Scope Confirmed

Not implemented in W2-U06:

- live signals;
- operator-facing predictions;
- prediction API;
- inference service;
- production model deployment;
- execution;
- broker/provider live connection;
- calibration framework;
- economic validation;
- advanced statistical validation;
- advanced model families.

---

## 11. Risks and Unknowns

| Risk / Unknown | Status | Mitigation |
|----------------|--------|------------|
| advanced model package compatibility | deferred | pure-Python baseline used now; future compatibility spike required |
| baseline predictive skill weak | accepted/expected | this unit proves machinery, not skill |
| statistical/calibration/economic validity absent | deferred | W2-U07/W2-U08/W2-U09 |
| target PostgreSQL evidence | operator required | command pack supplied |

---

## 12. Confidence Statement

| Dimension | Rating | Justification |
|-----------|--------|---------------|
| Harness governance binding | **HIGH in DA tests** | training only via approved experiment; refusals pass |
| Model input identity exclusion | **HIGH in DA tests** | identity-in-input rejected |
| Reproducibility | **HIGH in DA tests** | retrain same experiment/seed yields same artifact hash/metrics |
| Target platform correctness | **LIMITED until Operator evidence lands** | Windows + PostgreSQL evidence required by Build Order |
| Predictive skill | **LIMITED / not claimed** | baseline is intentionally simple; skill not W2-U06 objective |
| Overall package | **MODERATE-HIGH for implementation; conditional for approval evidence** | mandatory operator evidence remains required |

No percentage confidence is asserted.

---

## 13. Readiness Statement

> W2-U06 is implemented, tested locally, documented, and submitted for independent ITRGA review.  
> The harness is research-only and produces no live signal or execution path.  
> DA does **not** self-approve.  
> Operator-run Windows + PostgreSQL evidence remains mandatory for approval.  
> W2-U07 must not begin until ITRGA approval and a new Build Order.

---

**End of Delivery Report W2-U06**
