# Delivery Report — W2-U09

| Field | Value |
|-------|-------|
| Build Order | **W2-U09** ML Research: Economic Validation Framework |
| Platform | **0.21.0** |
| Date | 2026-07-15 |
| Author | Development Authority |
| Status | **Implemented — submitted for ITRGA review** |
| Approval | **Not self-approved** |
| Governing decision | D-W2-001 — generalized, market-agnostic model |
| Builds on | W2-U01–W2-U08 ML research foundation |

---

## 1. Executive Summary

W2-U09 implements AXIOM's **Economic Validation Framework** as a research-only layer. It answers whether a model that may look statistically positive remains economically usable after trading frictions.

The unit implements:

- transaction-cost model covering spread, commission, slippage, latency, liquidity, and transaction costs;
- cost input provenance: measured, provider-published, assumed;
- required sensitivity ranges for assumed costs;
- optimistic/base/pessimistic scenario sensitivity;
- independent statistical and economic conclusions;
- explicit statistically-positive/economically-negative detection;
- persisted research-only economic report artifact;
- audit event for report creation.

This unit does **not** add execution, orders, broker connectivity, live signals, paper trading, execution simulation, new model families, or live provider connections.

---

## 2. Hypothesis / Counter-Hypotheses

### Hypothesis

AXIOM can evaluate a model's hypothetical economic viability separately from its statistical quality, applying declared cost assumptions with provenance and sensitivity, without creating any execution path.

### Counter-hypotheses

| Counter | Result | Evidence |
|---------|--------|----------|
| Economic validation might conflate statistical and economic conclusions | **Falsified** | `test_statistically_positive_but_economically_negative_reported_separately` |
| Assumed costs might be accepted without provenance/sensitivity | **Falsified** | `test_cost_model_requires_provenance_and_sensitivity` |
| Reports might accept undeclared costs or conflated conclusions | **Falsified** | `test_conflated_or_undeclared_cost_report_rejected` |
| Scenario sensitivity might be missing | **Falsified** | `test_scenario_sensitivity_and_per_slice` |
| Economic report persistence/reproducibility might be absent | **Falsified locally** | `test_economic_report_persisted_and_reproducible` |
| Economic validation might introduce execution/live signal paths | **Falsified structurally** | `test_no_execution_or_live_signal_added_by_economic_validation` |

---

## 3. Implementation Summary

### 3.1 Economic report schema

Added ORM model:

```text
backend/app/db/models/economic_report.py
```

Added Alembic migration:

```text
backend/alembic/versions/20260715_0013_w2_u09_economic_reports.py
```

New table:

```text
economic_reports
```

Fields include:

- `experiment_id`
- `model_artifact_id`
- `validation_report_id`
- `calibration_report_id`
- `cost_model`
- `scenario_results`
- `statistical_conclusion`
- `economic_conclusion`
- `sensitivity_summary`
- `per_slice`
- `report_hash`
- `research_status`
- `notes`
- `created_at`

### 3.2 Economic validation package

Added package:

```text
backend/app/ml/economic/
```

Files:

```text
errors.py
service.py
__init__.py
```

Implemented:

- `EconomicValidationService`
- `CostInput`
- `CostScenario`
- `HypotheticalTrade`
- `CostProvenance`
- `EconomicValidationError`
- `CostInputInvalidError`
- `EconomicReportInvalidError`
- `EconomicPinError`

### 3.3 Cost model

The cost model applies these cost inputs to hypothetical research P&L:

| Cost input | Supported |
|------------|-----------|
| spread | Yes |
| commission | Yes |
| slippage | Yes |
| latency | Yes |
| liquidity | Yes |
| transaction costs | Yes |

Each cost input must declare provenance:

```text
measured
provider_published
assumed
```

Assumed values require sensitivity bounds:

```text
low_bps
high_bps
```

### 3.4 Independent conclusions

Economic validation reports keep statistical and economic conclusions separate:

```text
statistical_conclusion
economic_conclusion
```

If the statistical conclusion is positive but the base economic scenario is net negative, the report emits:

```text
STATISTICALLY_POSITIVE_ECONOMICALLY_NEGATIVE
```

### 3.5 Scenario sensitivity

Economic validation supports declared scenarios, for example:

```text
optimistic
base
pessimistic
```

Each scenario reports:

- gross return bps;
- total cost bps per trade;
- net return bps;
- trade count.

The report also includes:

```text
min_net_return_bps
max_net_return_bps
```

### 3.6 Per-slice economic summary

Economic validation summarizes hypothetical net results by:

- market class;
- timeframe;
- regime.

These are evaluation slices only. They are not model-input features.

---

## 4. Governance / Documentation Updates

Added:

- `docs/build-orders/BUILD_ORDER_W2-U09.md`
- `docs/build-orders/BUILD_ORDER_INTAKE_W2-U09.md`
- `docs/adr/ADR-029_Economic_Validation_Framework.md`
- `docs/evidence/W2-U09_OPERATOR_EVIDENCE_COMMANDS.md`

Updated:

- `PROJECT_STATE.md`
- `CHANGELOG.md`
- `README.md`
- `docs/governance/RISK_REGISTER.md`
- `docs/governance/TECHNICAL_DEBT_REGISTER.md`
- `docs/governance/GOVERNANCE_AMENDMENTS.md`
- `docs/governance/04_PROJECT_ROADMAP.md`
- backend version/system metadata
- frontend unit label

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
152 passed, 1 warning
```

### 5.2 Alembic local migration

Command:

```bash
cd backend
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w2u09.db' \
AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
alembic upgrade head
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w2u09.db' alembic current
```

Result:

```text
Running upgrade 20260714_0012 -> 20260715_0013
20260715_0013 (head)
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
backend/tests/test_economic_validation.py
```

Tests:

| Test | Purpose |
|------|---------|
| `test_cost_model_requires_provenance_and_sensitivity` | assumed costs require provenance and ranges |
| `test_statistically_positive_but_economically_negative_reported_separately` | headline stat-positive/econ-negative condition |
| `test_conflated_or_undeclared_cost_report_rejected` | conflated conclusions and undeclared costs rejected |
| `test_scenario_sensitivity_and_per_slice` | optimistic/base/pessimistic scenario sensitivity and slices |
| `test_economic_report_persisted_and_reproducible` | report persistence and deterministic hash |
| `test_no_execution_or_live_signal_added_by_economic_validation` | no execution/live-signal path introduced |

Backend baseline increased from **146** to **152**.

---

## 7. Explicit Negative Evidence

| Bad condition | Proof |
|---------------|-------|
| assumed cost without sensitivity | rejected |
| undeclared cost provenance | rejected |
| conflated statistical/economic conclusions | rejected |
| statistically positive but economically negative case hidden | rejected by explicit headline condition |
| execution/order/broker/live signal path | absent by structural test |

---

## 8. Out of Scope Confirmed

Not implemented in W2-U09:

- order placement;
- broker connection;
- live signal;
- execution simulator;
- paper trading;
- positions;
- market impact modeling;
- new model family;
- prediction API;
- economic decision automation.

All P&L is hypothetical research P&L only.

---

## 9. Operator Evidence Command Pack

Created:

```text
docs/evidence/W2-U09_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes commands for:

1. compatibility evidence;
2. PostgreSQL migration to `20260715_0013`;
3. full backend/frontend test console;
4. named W2-U09 tests;
5. headline stat-positive/econ-negative evidence;
6. cost provenance/sensitivity proof;
7. persisted PostgreSQL economic report proof;
8. no execution/no live signal grep;
9. CI/local equivalent;
10. parity smoke.

---

## 10. Risks and Unknowns

| Risk / Unknown | Status | Mitigation |
|----------------|--------|------------|
| PostgreSQL persistence not DA-run | Operator evidence required | command pack includes PG migration and report query |
| Remote CI run | Still carried/preferred | command pack includes local/remote evidence |
| Market impact modeling absent | Deferred | recorded as technical debt/future research |
| Economic validation not execution | Controlled | no execution path, research-only report, structural tests |

---

## 11. Confidence Statement

| Dimension | Rating | Justification |
|-----------|--------|---------------|
| Cost model/provenance | **HIGH in DA tests** | cost completeness/provenance/sensitivity tests pass |
| Independent conclusions | **HIGH in DA tests** | stat-positive/econ-negative condition reported separately |
| Scenario sensitivity | **HIGH in DA tests** | optimistic/base/pessimistic sensitivity and per-slice output tested |
| Persistence/reproducibility | **HIGH in DA tests** | economic report persisted and same hash reproduced |
| Execution safety | **HIGH in DA tests** | no execution/live-signal path structural test passes |
| Target platform correctness | **LIMITED until Operator evidence lands** | Windows + PostgreSQL evidence required |
| Overall package | **MODERATE-HIGH for implementation; conditional for approval evidence** | mandatory operator evidence remains required |

No percentage confidence is asserted.

---

## 12. Readiness Statement

> W2-U09 is implemented, tested locally, documented, and submitted for independent ITRGA review.  
> Economic reports are research-only and hypothetical.  
> No execution, order, broker connection, paper trading, or live signal path has been introduced.  
> DA does **not** self-approve.  
> Operator-run Windows + PostgreSQL evidence remains mandatory for approval.  
> W2-U10 must not begin until ITRGA approval and a new Build Order.

---

**End of Delivery Report W2-U09**
