# Delivery Report — W3-U01

| Field | Value |
|-------|-------|
| Build Order | **W3-U01** Live Research Advisor: Live Inference Engine + Governed Model Eligibility Gate |
| Platform | **0.23.0** |
| Date | 2026-07-15 |
| Author | Development Authority |
| Status | **Implemented — submitted for ITRGA review** |
| Approval | **Not self-approved** |
| Scope | Backend-only safety foundation; no operator-facing signal surface |

---

## 1. Executive Summary

W3-U01 implements the backend safety foundation for Wave 3. It adds a deterministic Live Inference Engine and a Governed Model Eligibility Gate. It proves that a model can only become inference-eligible if it has complete Wave-2 lineage and an explicitly audited `advisory_approved` status.

This unit is intentionally backend-only. It does **not** add:

- operator-facing signals;
- signal persistence/history;
- signal dashboard/UI;
- alerts;
- live signal WebSocket;
- execution;
- orders;
- broker connection;
- paper trading;
- positions.

---

## 2. Hypothesis / Counter-Hypotheses

### Hypothesis

AXIOM can introduce deterministic live inference and model eligibility checking without emitting signals or creating an execution path.

### Counter-hypotheses

| Counter | Result | Evidence |
|---------|--------|----------|
| Inference may be non-deterministic | **Falsified** | same input/model/version produces identical score and input hash |
| A model without advisory approval may be eligible | **Falsified** | `NOT_ADVISORY_APPROVED` refusal test |
| Missing Wave-2 report links may still pass | **Falsified** | missing statistical/calibration/economic/generalization report tests |
| Advisory promotion might bypass approval | **Falsified** | approver required; audit event written |
| Identity fields may reach inference input | **Falsified** | `IDENTITY_IN_INFERENCE_INPUT` refusal test |
| Out-of-domain/future/synthetic inputs may pass | **Falsified** | input validation refusal tests |
| Execution/signal path may exist | **Falsified structurally** | no-execution/no-signal tests and grep evidence commands |

---

## 3. Implementation Summary

### 3.1 Trading Intelligence inference bounded context

Created:

```text
backend/app/trading_intelligence/
backend/app/trading_intelligence/inference/
```

Files:

```text
errors.py
service.py
__init__.py
```

### 3.2 Live Inference Engine

Implemented:

```text
LiveInferenceEngine
InferenceInput
InferenceResult
```

The engine:

- requires eligibility before scoring;
- computes canonical `inference_input_hash`;
- produces deterministic score from model artifact hash/version, hyperparameters, and input hash;
- returns an inert `InferenceResult` DTO;
- emits no signal and persists no operator-facing advisory record in this unit.

### 3.3 Governed Model Eligibility Gate

Implemented:

```text
GovernedModelEligibilityGate
EligibilityDecision
```

Eligibility requires:

- approved experiment;
- statistical report link exists;
- calibration report link exists;
- economic report link exists;
- generalization report exists;
- model `advisory_status == advisory_approved`;
- feature version match;
- input has no identity fields;
- input is within operating domain;
- input is not future-dated;
- input does not use synthetic-authoritative data;
- no execution capability.

Refusal reasons include:

```text
EXPERIMENT_NOT_APPROVED
MISSING_STATISTICAL_REPORT
MISSING_CALIBRATION_REPORT
MISSING_ECONOMIC_REPORT
MISSING_GENERALIZATION_REPORT
NOT_ADVISORY_APPROVED
FEATURE_VERSION_MISMATCH
IDENTITY_IN_INFERENCE_INPUT
UNSUPPORTED_DOMAIN
FUTURE_INFERENCE_INPUT
SYNTHETIC_AUTHORITATIVE_INPUT_REFUSED
SIMULATED_FORWARD_DATED_INPUT_REFUSED
```

### 3.4 Advisory status lifecycle

Extended `model_artifacts` with:

```text
advisory_status
advisory_approved_at
advisory_approved_by
```

Added Alembic migration:

```text
backend/alembic/versions/20260715_0015_w3_u01_advisory_status.py
```

Promotion to `advisory_approved` requires:

- complete model lineage;
- explicit approver;
- approval reason;
- UTC timestamp;
- audit event.

### 3.5 No signal surface

No API route, UI, signal table, alert path, WebSocket stream, or signal emission mechanism was added.

---

## 4. Governance / Documentation Updates

Added:

- `docs/build-orders/BUILD_ORDER_W3-U01.md`
- `docs/build-orders/BUILD_ORDER_INTAKE_W3-U01.md`
- `docs/adr/ADR-031_Live_Inference_Eligibility_Gate.md`
- `docs/evidence/W3-U01_OPERATOR_EVIDENCE_COMMANDS.md`

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

Commands run in DA sandbox using a temporary virtual environment outside persisted workspace:

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
164 passed, 1 warning
```

### 5.2 Alembic local migration

Command:

```bash
cd backend
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w3u01.db' \
AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
alembic upgrade head
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w3u01.db' alembic current
```

Result:

```text
Running upgrade 20260715_0014 -> 20260715_0015
20260715_0015 (head)
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

New test file:

```text
backend/tests/test_live_inference_gate.py
```

Tests:

| Test | Purpose |
|------|---------|
| `test_deterministic_inference_same_input_same_score_and_hash` | deterministic score/input hash |
| `test_eligibility_refusals_by_reason` | missing-lineage and not-advisory refusals |
| `test_governed_promotion_refused_without_lineage_and_audited_on_success` | promotion refusals + audited success |
| `test_identity_out_of_domain_future_and_synthetic_inputs_refused` | input/domain/chronology refusals |
| `test_no_execution_signal_or_broker_path_in_inference_modules` | structural no-execution/no-signal proof |

Backend baseline increased from **159** to **164**.

---

## 7. Explicit Negative Evidence

| Bad condition | Proof |
|---------------|-------|
| missing statistical report | refused |
| missing calibration report | refused |
| missing economic report | refused |
| missing generalization report | refused |
| not advisory approved | refused |
| promotion without lineage | refused |
| promotion without approver | refused |
| identity in inference input | refused |
| out-of-domain input | refused |
| future input | refused |
| synthetic authoritative input | refused |
| execution/broker/signal path | absent structurally |

---

## 8. Persisted Artifact Standing-Control Response

W3-U01 introduces new persisted fields on `model_artifacts` and a governed promotion audit event. The operator evidence command pack includes a committing proof that:

- creates full lineage;
- promotes a model to `advisory_approved`;
- runs deterministic inference;
- selects model advisory fields from PostgreSQL;
- selects advisory promotion audit event from PostgreSQL.

---

## 9. Operator Evidence Command Pack

Created:

```text
docs/evidence/W3-U01_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes commands for:

1. PostgreSQL migration to `20260715_0015`;
2. full backend/frontend test console;
3. named W3-U01 tests;
4. persisted PostgreSQL advisory promotion proof;
5. no-execution/no-signal grep;
6. CI/local equivalent;
7. parity smoke.

---

## 10. Out of Scope Confirmed

Not implemented in W3-U01:

- operator-facing signal;
- advisory signal persistence/history;
- dashboard/UI;
- alerting;
- live signal WebSocket;
- broker connection;
- order path;
- execution;
- paper trading;
- position handling.

---

## 11. Risks and Unknowns

| Risk / Unknown | Status | Mitigation |
|----------------|--------|------------|
| PostgreSQL advisory promotion proof not DA-run | Operator evidence required | command pack includes committing script and SELECTs |
| Future signal persistence | Deferred | W3-U02 |
| UI/dashboard | Deferred | W3-U05 |
| Alerts | Deferred | W3-U06 |
| Execution boundary | Controlled | no signal/execution code; broker gate remains closed |

---

## 12. Confidence Statement

| Dimension | Rating | Justification |
|-----------|--------|---------------|
| Deterministic inference | **HIGH in DA tests** | same input/model yields same score/hash |
| Eligibility refusals | **HIGH in DA tests** | each missing lineage/status/input condition refused |
| Governed promotion | **HIGH in DA tests** | lineage/approver required; audit event tested |
| No execution/no signal | **HIGH in DA tests** | structural test and no route added |
| Target-platform correctness | **LIMITED until Operator evidence lands** | Windows + PostgreSQL evidence required |
| Overall package | **MODERATE-HIGH for implementation; conditional for approval evidence** | mandatory operator evidence remains required |

No percentage confidence is asserted.

---

## 13. Readiness Statement

> W3-U01 is implemented, tested locally, documented, and submitted for independent ITRGA review.  
> It is backend-only and emits no operator-facing signal.  
> No execution, order, broker, alert, dashboard, or signal WebSocket was introduced.  
> DA does **not** self-approve.  
> Operator-run Windows + PostgreSQL evidence remains mandatory for approval.  
> W3-U02 must not begin until ITRGA approval and a new Build Order.

---

**End of Delivery Report W3-U01**
