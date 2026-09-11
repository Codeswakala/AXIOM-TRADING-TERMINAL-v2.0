# Delivery Report — W2-U07

| Field | Value |
|-------|-------|
| Build Order | **W2-U07** ML Research: Statistical Validation Framework |
| Platform | **0.19.0** |
| Date | 2026-07-14 |
| Author | Development Authority |
| Status | **Implemented — submitted for ITRGA review** |
| Approval | **Not self-approved** |
| Builds on | W2-U01–W2-U06 chain |

---

## 1. Executive Summary

W2-U07 implements a research-only Statistical Validation Framework. It validates research model artifacts produced by the W2-U06 harness and makes uncertainty mandatory.

Delivered:

- pure-Python walk-forward statistical validation;
- temporal-only validation strategy guard;
- random/non-temporal CV refusal;
- bootstrap distribution;
- percentile confidence interval;
- effect size vs. null accuracy;
- simple significance estimate;
- persisted research-only validation report artifact;
- uncertainty-mandatory report contract.

This unit adds **no live signals, no prediction endpoint, no execution, no broker/provider live connection, no calibration framework, and no economic validation**.

---

## 2. Compatibility

No compiled statistical dependency was added.

| Candidate | Decision | Rationale |
|-----------|----------|-----------|
| numpy/scipy/statsmodels | Deferred | Pure-Python implementation sufficient for W2-U07 foundation; avoids Python 3.14 wheel risk |
| pure-Python stdlib | Selected | Supports deterministic bootstrap/CI/effect-size/significance foundation |

---

## 3. Implementation Summary

### 3.1 Validation report schema

Added ORM model:

```text
backend/app/db/models/validation_report.py
```

Added Alembic migration:

```text
backend/alembic/versions/20260714_0011_w2_u07_validation_reports.py
```

New table:

```text
validation_reports
```

Fields include:

- experiment id;
- model artifact id;
- validation kind;
- metrics;
- uncertainty;
- fold results;
- effect size;
- significance;
- config;
- report hash;
- research-only status.

### 3.2 Statistical validation service

Added:

```text
backend/app/ml/validation/
```

Key files:

```text
errors.py
service.py
__init__.py
```

Implements:

- `ValidationConfig`
- `StatisticalValidationService`
- `NonTemporalValidationError`
- `EmbargoViolationError`
- `MissingUncertaintyError`
- `ValidationPinError`

### 3.3 Walk-forward validation

The service performs deterministic walk-forward validation:

```text
train window → embargo → test window → step forward
```

It reuses the W2-U06 majority baseline per fold.

Random/non-temporal validation strategies are refused.

### 3.4 Uncertainty and statistical fields

Each report includes:

- aggregate metric (`accuracy`);
- bootstrap distribution;
- confidence interval;
- effect size (`accuracy_minus_null`);
- significance p-value estimate;
- fold-level results;
- report hash.

A report payload missing uncertainty is rejected.

---

## 4. Tests Added

New file:

```text
backend/tests/test_statistical_validation.py
```

Tests:

| Test | Purpose |
|------|---------|
| `test_walk_forward_validation_report_with_uncertainty_persisted` | report includes metrics, CI/bootstrap uncertainty, effect size, significance, folds |
| `test_random_cv_and_embargo_violation_refused` | random validation refused and insufficient/invalid fold setup rejected |
| `test_report_without_uncertainty_rejected` | uncertainty-less report rejected |
| `test_seeded_validation_reproducible_same_report_hash` | seeded validation produces same hash/metrics/uncertainty |
| `test_no_validation_live_signal_or_identity_feature_route_added` | no live signal route and no identity pattern in validation module |

Backend baseline increased from **135** to **140**.

---

## 5. Evidence

### Backend

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
140 passed, 1 warning
```

### Alembic local migration

```bash
cd backend
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w2u07.db' \
AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
alembic upgrade head
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w2u07.db' alembic current
```

Result:

```text
Running upgrade 20260714_0010 -> 20260714_0011
20260714_0011 (head)
```

### Frontend no-regression

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

---

## 6. Explicit Negative Evidence

| Bad condition | Proof |
|---------------|-------|
| random/non-temporal validation | rejected `NON_TEMPORAL_CV` |
| validation report without uncertainty | rejected `VALIDATION_UNCERTAINTY_MISSING` |
| invalid/insufficient walk-forward fold setup | rejected |
| validation live signal route | absent by structural test |
| symbol identity pattern in validation module | absent by structural test |

---

## 7. Governance / Documentation Updates

Added:

- `docs/build-orders/ITRGA_REVIEW_W2-U06.md`
- `docs/build-orders/BUILD_ORDER_W2-U07.md`
- `docs/build-orders/BUILD_ORDER_INTAKE_W2-U07.md`
- `docs/adr/ADR-027_Statistical_Validation_Framework.md`
- `docs/evidence/W2-U07_OPERATOR_EVIDENCE_COMMANDS.md`

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

## 8. Operator Evidence Command Pack

Created:

```text
docs/evidence/W2-U07_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes commands for:

1. compatibility evidence;
2. PostgreSQL migration to `20260714_0011`;
3. full backend/frontend test console;
4. named W2-U07 tests;
5. random/non-temporal validation refusal;
6. uncertainty-mandatory report proof;
7. reproducible seeded validation proof;
8. persisted PostgreSQL validation report proof;
9. no identity/no live signal grep;
10. CI/local equivalent;
11. parity smoke.

---

## 9. Out of Scope Confirmed

Not implemented in W2-U07:

- calibration framework;
- economic validation;
- model family upgrades;
- live/operator-facing signals;
- inference or prediction endpoint;
- execution;
- broker/provider live connection;
- compiled statistical/ML dependencies.

---

## 10. Confidence Statement

| Dimension | Rating | Justification |
|-----------|--------|---------------|
| Statistical validation foundation | **HIGH in DA tests** | walk-forward reports with uncertainty persist locally |
| Random/non-temporal refusal | **HIGH in DA tests** | negative test passes |
| Uncertainty enforcement | **HIGH in DA tests** | report without uncertainty rejected |
| Reproducibility | **HIGH in DA tests** | same seed/config yields same report hash/metrics/uncertainty |
| Target-platform correctness | **LIMITED until Operator evidence lands** | Windows + PostgreSQL evidence required by Build Order |
| Overall package | **MODERATE-HIGH for implementation; conditional for approval evidence** | mandatory operator evidence remains required |

No percentage confidence is asserted.

---

## 11. Readiness Statement

> W2-U07 is implemented, tested locally, documented, and submitted for independent ITRGA review.  
> Validation reports are research-only and emit no live signal.  
> Calibration and economic validation remain future units.  
> DA does **not** self-approve.  
> Operator-run Windows + PostgreSQL evidence remains mandatory for approval.  
> W2-U08 must not begin until ITRGA approval and a new Build Order.

---

**End of Delivery Report W2-U07**
