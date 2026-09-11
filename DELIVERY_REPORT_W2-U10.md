# Delivery Report — W2-U10

| Field | Value |
|-------|-------|
| Build Order | **W2-U10** ML Research: Multi-Market Generalization + Model Registry / Drift Design |
| Platform | **0.22.0** |
| Date | 2026-07-15 |
| Author | Development Authority |
| Status | **Implemented — submitted for ITRGA review** |
| Approval | **Not self-approved** |
| Prerequisite | W2-U09 **APPROVED WITH OBSERVATIONS** |
| Milestone | Final Wave-2 unit; Research Framework Complete candidate pending ITRGA approval |

---

## 1. Executive Summary

W2-U10 implements the final layer of the Wave-2 ML Research Framework:

- multi-market generalization reports;
- trained-on-X / evaluated-on-Y holdout reporting;
- operating-domain guardrails and unsupported-domain warnings;
- model registry maturation linking statistical, calibration, and economic reports;
- drift monitoring design records;
- explicit no-auto-retrain enforcement.

This unit remains **research/advisory only**. It introduces no live inference loop, no live monitoring loop, no live signals, no auto-retrain, no execution, no broker/provider connection, and no Wave-3 behavior.

---

## 2. Hypothesis / Counter-Hypotheses

### Hypothesis

AXIOM can evaluate whether a model trained on one market set holds on another, record its validated operating domain, link its full statistical/calibration/economic evidence into the model registry, and record drift without triggering retraining automatically.

### Counter-hypotheses

| Counter | Result | Evidence |
|---------|--------|----------|
| Generalization may leak train market into evaluated market | **Falsified** | `test_market_holdout_overlap_refused` |
| Out-of-domain evaluation may pass silently | **Falsified** | `test_operating_domain_warning_pair` |
| Registry may omit U07/U08/U09 report links | **Falsified** | `test_model_registry_matured_with_report_links_and_domain` |
| Drift may trigger auto-retrain | **Falsified** | `test_drift_signal_does_not_auto_retrain` |
| Generalization report may be non-reproducible | **Falsified** | `test_generalization_report_reproducible_same_hash` |
| Live signal or identity paths may be introduced | **Falsified** | `test_no_identity_live_signal_or_auto_retrain_loop_added` |

---

## 3. Implementation Summary

### 3.1 Generalization and drift persistence

Added ORM models:

```text
backend/app/db/models/generalization.py
```

Added Alembic migration:

```text
backend/alembic/versions/20260715_0014_w2_u10_generalization_drift.py
```

New tables:

```text
generalization_reports
drift_monitoring_records
```

Extended existing table:

```text
model_artifacts
  statistical_report_id
  calibration_report_id
  economic_report_id
  operating_domain
  unsupported_domains
  approval_history
  rollback_version
```

### 3.2 Generalization service

Added package:

```text
backend/app/ml/generalization/
```

Files:

```text
errors.py
service.py
__init__.py
```

Implemented:

- `Domain`
- `GeneralizationInput`
- `GeneralizationService`
- `GeneralizationLeakageError`
- `AutoRetrainProhibitedError`
- `DomainUnsupportedWarning`

### 3.3 Trained-on-X / evaluated-on-Y reports

`GeneralizationService.create_report(...)` creates research-only generalization reports with:

- trained-on market/timeframe/regime domain;
- evaluated-on holdout markets/instruments;
- aggregate accuracy;
- operating domain;
- unsupported-domain warnings;
- deterministic report hash;
- audit event.

It refuses market holdout leakage when trained and evaluated market sets overlap.

### 3.4 Operating-domain guardrail

`GeneralizationService.domain_warning(...)` returns:

```text
UNSUPPORTED_DOMAIN
```

when a market/timeframe/regime is outside the validated operating domain.

### 3.5 Model registry maturation

`GeneralizationService.mature_registry_entry(...)` links a model artifact to:

- W2-U07 statistical validation report;
- W2-U08 calibration report;
- W2-U09 economic report;
- validated operating domain;
- approval history;
- research-only status.

This makes the research model registry answerable end-to-end: statistical, calibration, and economic evidence are linked from the model artifact.

### 3.6 Drift monitoring design

`GeneralizationService.record_drift_signal(...)` records drift evidence as a research artifact:

- drift kind;
- window start/end;
- signals;
- drift detected flag;
- auto-retrain requested flag;
- retrain triggered flag **always false**;
- governance required flag **true**;
- deterministic record hash;
- audit event when auto-retrain is requested/refused.

No live loop or auto-retrain path is introduced.

---

## 4. Governance / Documentation Updates

Added:

- `docs/build-orders/ITRGA_VERDICT_W2-U09_FINAL.md`
- `docs/build-orders/BUILD_ORDER_W2-U10.md`
- `docs/build-orders/BUILD_ORDER_INTAKE_W2-U10.md`
- `docs/adr/ADR-030_Generalization_Model_Registry_Drift.md`
- `docs/evidence/W2-U10_OPERATOR_EVIDENCE_COMMANDS.md`

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
159 passed, 1 warning
```

### 5.2 Alembic local migration

Command:

```bash
cd backend
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w2u10.db' \
AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
alembic upgrade head
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w2u10.db' alembic current
```

Result:

```text
Running upgrade 20260715_0013 -> 20260715_0014
20260715_0014 (head)
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
backend/tests/test_generalization_drift.py
```

Tests:

| Test | Purpose |
|------|---------|
| `test_trained_on_x_evaluated_on_y_generalization_report` | creates trained-on-X / evaluated-on-Y report |
| `test_market_holdout_overlap_refused` | refuses market holdout leakage |
| `test_operating_domain_warning_pair` | in-domain no warning; out-of-domain warning |
| `test_model_registry_matured_with_report_links_and_domain` | model artifact links U07/U08/U09 reports and operating domain |
| `test_drift_signal_does_not_auto_retrain` | drift record does not trigger retrain and requires governance |
| `test_generalization_report_reproducible_same_hash` | same report inputs yield same hash |
| `test_no_identity_live_signal_or_auto_retrain_loop_added` | no identity/live-signal/auto-retrain loop |

Backend baseline increased from **152** to **159**.

---

## 7. Explicit Negative Evidence

| Bad condition | Proof |
|---------------|-------|
| train and evaluation markets overlap | rejected with `MARKET_HOLDOUT_LEAKAGE` |
| out-of-domain evaluation | returns `UNSUPPORTED_DOMAIN` warning |
| drift auto-retrain requested | record created with `retrain_triggered=False`, `governance_required=True` |
| model registry missing report link | service validates report links exist before maturation |
| live signal / auto-retrain route | absent by structural test |
| identity pattern | absent by structural test |

---

## 8. Persisted Artifact Standing-Control Response

W2-U10 introduces new persisted artifact types:

- `generalization_reports`
- `drift_monitoring_records`
- matured `model_artifacts` registry links

The operator evidence command pack includes a committing-script proof that persists all three categories and queries them via PostgreSQL. This directly follows the W2-U09 standing control.

---

## 9. Operator Evidence Command Pack

Created:

```text
docs/evidence/W2-U10_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes commands for:

1. compatibility evidence;
2. PostgreSQL migration to `20260715_0014`;
3. full backend/frontend test console;
4. named W2-U10 tests;
5. persisted PostgreSQL proof for generalization report, drift record, and matured model artifact links;
6. no live signal / no auto-retrain / no identity grep;
7. CI/local equivalent;
8. parity smoke.

---

## 10. Out of Scope Confirmed

Not implemented in W2-U10:

- live inference loop;
- live monitoring loop;
- operator-facing predictions;
- live signals;
- auto-retraining;
- execution;
- broker/provider live connection;
- Wave-3 advisor behavior.

---

## 11. Risks and Unknowns

| Risk / Unknown | Status | Mitigation |
|----------------|--------|------------|
| PostgreSQL persistence not DA-run | Operator evidence required | command pack includes committing script and SELECTs |
| Remote CI run | Still carried/preferred | command pack includes local/remote evidence |
| Live drift monitoring | Out of scope | Wave 3+ |
| Auto-retraining | Prohibited | drift record requires governance; no retrain path |
| Wave-2 closure | ITRGA-only | DA records candidate only; ITRGA declares milestone |

---

## 12. Confidence Statement

| Dimension | Rating | Justification |
|-----------|--------|---------------|
| Generalization report | **HIGH in DA tests** | trained-on/evaluated-on and holdout leakage tests pass |
| Operating-domain guardrail | **HIGH in DA tests** | in-domain/out-of-domain warning pair passes |
| Registry maturation | **HIGH in DA tests** | U07/U08/U09 links and operating domain set |
| Drift no-auto-retrain | **HIGH in DA tests** | requested drift does not trigger retrain and requires governance |
| Target-platform correctness | **LIMITED until Operator evidence lands** | Windows + PostgreSQL evidence required |
| Wave-2 milestone readiness | **CONDITIONAL** | ITRGA must approve and declare Research Framework Complete |
| Overall package | **MODERATE-HIGH for implementation; conditional for approval evidence** | mandatory operator evidence remains required |

No percentage confidence is asserted.

---

## 13. Readiness Statement

> W2-U10 is implemented, tested locally, documented, and submitted for independent ITRGA review.  
> It is research-only and emits no live signal, no live monitoring loop, and no auto-retrain.  
> DA does **not** self-approve W2-U10 and does **not** declare Wave 2 complete.  
> Operator-run Windows + PostgreSQL evidence remains mandatory for approval.  
> The Research Framework Complete milestone must be declared by ITRGA, not DA.

---

**End of Delivery Report W2-U10**
