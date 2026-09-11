# Delivery Report — W2-U08

| Field | Value |
|-------|-------|
| Build Order | **W2-U08** ML Research: Calibration + Probability Quality Framework |
| Platform | **0.20.0** |
| Date | 2026-07-14 |
| Author | Development Authority |
| Status | **Implemented — submitted for ITRGA review** |
| Approval | **Not self-approved** |
| Builds on | W2-U01–W2-U07 chain |

---

## 1. Executive Summary

W2-U08 implements the Calibration + Probability Quality Framework. It answers whether model probabilities are trustworthy by producing reliability bins, Brier score, Expected Calibration Error, per-slice calibration, miscalibration warnings, and base-rate-aware significance.

This unit validates probability quality of model outputs as research artifacts only. It adds **no new model family, no live signals, no inference API, no prediction endpoint, no economic validation, no execution, and no broker/provider live connection**.

---

## 2. Compatibility

No compiled dependency was added.

| Candidate | Decision | Rationale |
|-----------|----------|-----------|
| scikit-learn calibration utilities | Deferred | Would require wheel compatibility spike; pure Python sufficient now |
| numpy/scipy/statsmodels | Deferred | Not necessary for foundational calibration metrics |
| pure Python stdlib | Selected | Supports reliability bins, Brier, ECE, base-rate null, deterministic hashes |

---

## 3. Implementation Summary

### 3.1 Calibration report schema

Added ORM model:

```text
backend/app/db/models/calibration_report.py
```

Added Alembic migration:

```text
backend/alembic/versions/20260714_0012_w2_u08_calibration_reports.py
```

New table:

```text
calibration_reports
```

Fields include:

- experiment id;
- model artifact id;
- validation report id;
- Brier score;
- Expected Calibration Error;
- bin scheme;
- bins;
- per-slice results;
- warnings;
- base rate;
- base-rate significance;
- config;
- report hash;
- research-only status.

### 3.2 Calibration service

Added package:

```text
backend/app/ml/calibration/
```

Key files:

```text
errors.py
service.py
__init__.py
```

Implemented:

- `CalibrationService`
- `CalibrationConfig`
- `ProbabilityObservation`
- `CalibrationReportInvalidError`
- `CalibrationPinError`

### 3.3 Calibration metrics

Implemented:

| Metric | Purpose |
|--------|---------|
| Reliability bins | predicted confidence vs observed frequency |
| Brier score | proper scoring rule for probabilities |
| Expected Calibration Error | weighted absolute confidence/reliability gap |
| Per-slice calibration | market class, timeframe, regime slices |
| Base-rate significance | no-information-rate null comparison |

### 3.4 Miscalibration warning

If ECE exceeds configured threshold, report includes:

```text
POORLY_CALIBRATED
```

### 3.5 Base-rate-aware null

Added no-information-rate significance:

```text
base_rate = max(positive_rate, negative_rate)
skill_over_base_rate = accuracy - base_rate
significant_skill = skill_over_base_rate > 0
```

This prevents majority baseline performance on imbalanced data from being reported as significant skill relative to a hard-coded 0.5 null.

---

## 4. Tests Added

New file:

```text
backend/tests/test_calibration.py
```

Tests:

| Test | Purpose |
|------|---------|
| `test_miscalibrated_fixture_flagged_and_well_calibrated_not_flagged` | miscalibrated fixture flagged, calibrated fixture not flagged |
| `test_calibration_curve_brier_ece_and_per_slice_shape` | reliability bins, Brier/ECE, slice shape |
| `test_base_rate_null_majority_baseline_not_significant_skill` | majority baseline not significant vs base rate |
| `test_calibration_report_without_bins_uncertainty_rejected` | point/partial calibration report rejected |
| `test_calibration_report_persisted_and_reproducible` | persisted report + deterministic hash |
| `test_no_identity_or_live_signal_added_by_calibration` | no identity pattern and no live signal route |

Backend baseline increased from **140** to **146**.

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
146 passed, 1 warning
```

### 5.2 Alembic local migration

Command:

```bash
cd backend
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w2u08.db' \
AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
alembic upgrade head
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w2u08.db' alembic current
```

Result:

```text
Running upgrade 20260714_0011 -> 20260714_0012
20260714_0012 (head)
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

## 6. Explicit Negative Evidence

| Bad condition | Proof |
|---------------|-------|
| miscalibrated confident predictions | flagged with `POORLY_CALIBRATED` |
| well-calibrated fixture | not flagged |
| report missing bins/uncertainty | rejected |
| majority baseline on imbalanced data | not significant skill vs base-rate null |
| identity pattern in calibration code | absent by structural test |
| live signal route | absent by structural test |

---

## 7. Governance / Documentation Updates

Added:

- `docs/build-orders/BUILD_ORDER_W2-U08.md`
- `docs/build-orders/BUILD_ORDER_INTAKE_W2-U08.md`
- `docs/adr/ADR-028_Calibration_Probability_Quality.md`
- `docs/evidence/W2-U08_OPERATOR_EVIDENCE_COMMANDS.md`

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
docs/evidence/W2-U08_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes commands for:

1. compatibility evidence;
2. PostgreSQL migration to `20260714_0012`;
3. full backend/frontend test console;
4. named calibration tests;
5. miscalibration detection evidence;
6. base-rate null evidence;
7. persisted calibration report proof;
8. no identity/no live signal grep;
9. CI/local equivalent;
10. parity smoke.

---

## 9. Out of Scope Confirmed

Not implemented in W2-U08:

- economic validation;
- multi-market generalization/drift maturation;
- new model families;
- live/operator-facing signals;
- inference/prediction endpoint;
- execution;
- broker/provider live connection;
- compiled statistical/ML dependencies.

---

## 10. Risks and Unknowns

| Risk / Unknown | Status | Mitigation |
|----------------|--------|------------|
| PostgreSQL migration not DA-run | Operator evidence required | command pack includes PG migration |
| Remote CI run | Still carried | command pack includes local/remote evidence |
| Economic validation absent | Deferred | W2-U09 |
| Advanced calibration methods | Deferred | current pure-Python foundation; future methods require compatibility spike |

---

## 11. Confidence Statement

| Dimension | Rating | Justification |
|-----------|--------|---------------|
| Calibration metrics | **HIGH in DA tests** | reliability bins, Brier/ECE, slices tested |
| Miscalibration detection | **HIGH in DA tests** | bad fixture flagged and good fixture not flagged |
| Base-rate null correction | **HIGH in DA tests** | majority baseline not significant vs no-information-rate |
| Persistence/reproducibility | **HIGH in DA tests** | report persisted and same hash reproduced |
| Target-platform correctness | **LIMITED until Operator evidence lands** | Windows + PostgreSQL evidence required by Build Order |
| Overall package | **MODERATE-HIGH for implementation; conditional for approval evidence** | mandatory operator evidence remains required |

No percentage confidence is asserted.

---

## 12. Readiness Statement

> W2-U08 is implemented, tested locally, documented, and submitted for independent ITRGA review.  
> Calibration reports are research-only and emit no live signal.  
> Economic validation remains future W2-U09.  
> DA does **not** self-approve.  
> Operator-run Windows + PostgreSQL evidence remains mandatory for approval.  
> W2-U09 must not begin until ITRGA approval and a new Build Order.

---

**End of Delivery Report W2-U08**
