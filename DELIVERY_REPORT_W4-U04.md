# Delivery Report — W4-U04

| Field | Value |
|---|---|
| Build Order | **W4-U04** Scenario Simulation Research Reports |
| Platform | **0.34.0** |
| Wave | **4 — Institutional Intelligence** |
| DA status | **Implemented and locally validated** |
| Approval status | **Not self-approved; pending operator evidence and ITRGA review** |
| Date | 2026-07-16 |

---

## 1. Executive Summary

W4-U04 implements persisted Scenario Simulation Research Reports as hypothetical, counterfactual research artifacts. Reports are as-of-bounded, uncertainty-mandatory, assumption-explicit, persisted, audited, and read-only. A scenario is not a prediction, not a guaranteed outcome, not a signal, and not a trade instruction.

Implemented outcomes:

- `scenario_reports` table and Alembic migration;
- `ScenarioReportService` under Institutional Intelligence;
- as-of-bounded candle windows with future-candle exclusion;
- explicit assumptions and inputs stored in the artifact;
- hypothetical result and uncertainty interval;
- independent `economic_usefulness` field;
- limitations including hypothetical/not prediction/not instruction;
- audit event on report creation;
- authenticated read-only API;
- no UI in this unit;
- no order/sizing/signal/action path.

DA does not self-approve. Operator-run Windows + PostgreSQL evidence remains mandatory.

---

## 2. Authority and Traceability

| Artifact | Path |
|---|---|
| W4-U03 review | `docs/build-orders/ITRGA_REVIEW_W4-U03.md` |
| W4-U03 OBS closure | `docs/build-orders/ITRGA_VERDICT_W4-U03_OBS1_CLOSURE.md` |
| W4-U04 Build Order | `docs/build-orders/BUILD_ORDER_W4-U04.md` |
| W4-U04 Build Order Intake | `docs/build-orders/BUILD_ORDER_INTAKE_W4-U04.md` |
| W4-U04 ADR | `docs/adr/ADR-043_Scenario_Simulation_Reports.md` |
| Operator evidence commands | `docs/evidence/W4-U04_OPERATOR_EVIDENCE_COMMANDS.md` |
| Migration | `backend/alembic/versions/20260716_0021_w4_u04_scenario_reports.py` |

---

## 3. Implementation Summary

### 3.1 Scenario report persistence

Added:

```text
backend/app/db/models/scenario_report.py
backend/alembic/versions/20260716_0021_w4_u04_scenario_reports.py
```

The table stores research artifact metadata, series metadata, as-of bounds, sample count, scenario name, hypothetical result, assumptions, inputs, uncertainty, economic usefulness, lineage/config/results/limitations, report hash, research status, actor, and audit correlation id.

It intentionally contains no order, sizing, execution, broker, remediation, or signal payload fields.

### 3.2 Scenario service

Added:

```text
backend/app/institutional_intelligence/scenario.py
```

Key objects:

```text
ScenarioSeriesSpec
ScenarioAssumptions
ScenarioComputationResult
ScenarioReportService
```

The service:

- reads persisted candles read-only;
- filters `open_time >= as_of_start` and `open_time <= as_of_end`;
- counts future candles beyond `as_of_end`;
- computes baseline returns and realized volatility;
- applies explicit hypothetical shock assumptions;
- computes a counterfactual index and uncertainty band;
- creates an `IntelligenceArtifactContract`;
- persists `ScenarioReport`;
- writes `scenario_report.created` audit event.

### 3.3 Hypothetical framing

Reports include limitations:

```text
hypothetical_counterfactual_research_only
not_a_prediction
not_a_trade_instruction
not_financial_advice
economic_usefulness_not_assessed
```

### 3.4 Read-only API

Added:

```text
GET /api/v1/intelligence/scenario-reports
GET /api/v1/intelligence/scenario-reports/{report_id}
```

No POST/emit/write route was added.

### 3.5 UI decision

W4-U04 adds no UI. The Build Order allows API + tests to suffice if no UI is added.

---

## 4. Files Created

```text
backend/app/db/models/scenario_report.py
backend/app/models/scenario_report.py
backend/app/institutional_intelligence/scenario.py
backend/alembic/versions/20260716_0021_w4_u04_scenario_reports.py
backend/tests/test_scenario_reports.py
docs/build-orders/ITRGA_REVIEW_W4-U03.md
docs/build-orders/ITRGA_VERDICT_W4-U03_OBS1_CLOSURE.md
docs/build-orders/BUILD_ORDER_W4-U04.md
docs/build-orders/BUILD_ORDER_INTAKE_W4-U04.md
docs/adr/ADR-043_Scenario_Simulation_Reports.md
docs/evidence/W4-U04_OPERATOR_EVIDENCE_COMMANDS.md
DELIVERY_REPORT_W4-U04.md
```

---

## 5. Files Modified

```text
backend/app/__init__.py
backend/app/api/routes/intelligence.py
backend/app/core/config.py
backend/app/db/models/__init__.py
backend/app/institutional_intelligence/__init__.py
backend/app/institutional_intelligence/contracts.py
backend/app/main.py
backend/app/models/system.py
backend/pyproject.toml
backend/tests/test_endpoint_auth.py
backend/tests/test_system.py
frontend/src/layouts/TerminalLayout.tsx
README.md
PROJECT_STATE.md
CHANGELOG.md
backend/README.md
docs/governance/RISK_REGISTER.md
docs/governance/TECHNICAL_DEBT_REGISTER.md
docs/governance/GOVERNANCE_AMENDMENTS.md
docs/governance/04_PROJECT_ROADMAP.md
```

---

## 6. Acceptance Criteria Mapping

| Requirement | DA Result |
|---|---|
| R-6 no order/sizing/signal payload | Implemented and tested; schema inert |
| R-6 changes nothing / triggers nothing | Implemented and tested |
| Hypothetical labelling | Implemented in limitations/notes/tests |
| R-2 no look-ahead | Implemented and tested with future candle exclusion |
| Uncertainty + assumptions | Implemented and tested |
| R-5 economic usefulness | Implemented as independent `not_assessed` field with reason |
| R-4 persisted report + audit | Implemented and tested; operator raw SELECT/no-orphan proof required |
| Read-only API | Implemented and tested 401/200/405 |
| Dependency discipline | Uses pure-Python fallback; no unspiked imports |
| No UI | Explicitly no UI this unit |
| No execution / Gate closed | Preserved; evidence pack includes grep and broker gate proof |

---

## 7. Local Validation Evidence Collected by DA

### Backend lint

```text
$ ruff check .
All checks passed!
```

### Named W4-U04 tests

```text
$ pytest tests/test_scenario_reports.py -q
7 passed, 1 warning
```

### Backend full suite

```text
$ pytest -q
218 passed, 1 warning
```

### Frontend validation

```text
$ npm audit --audit-level=high
found 0 vulnerabilities

$ npm test
Test Files 11 passed
Tests 25 passed

$ npm run lint
# TypeScript clean

$ npm run build
✓ built
```

### Alembic local migration smoke

```text
Running upgrade 20260716_0020 -> 20260716_0021, W4-U04 scenario simulation research reports
20260716_0021 (head)
```

---

## 8. Security / Governance Review

| Area | Review |
|---|---|
| Authentication | API requires existing Bearer operator auth. |
| Authorization | No public scenario report endpoint added. |
| Write surface | No scenario report write API exposed. |
| Execution | No broker/order/execution path added. |
| Sizing/order boundary | No order/sizing/quantity/stop/target fields in schema. |
| Signal boundary | No advisory signal side-effect; scenario is not a signal. |
| Dependencies | Uses pure-Python arithmetic; no unspiked dependency. |
| D-W2-001 | No per-market specialized model or symbol-identity feature. |
| Persistence | New table via Alembic; audit event on create. |

---

## 9. Known Risks / Required Operator Evidence

| Risk | Status |
|---|---|
| PostgreSQL persistence proof not run in DA sandbox | Operator evidence pack includes committing script + raw SELECT + audit/no-orphan proof |
| No UI for scenario reports | Accepted; no UI in W4-U04 scope |
| Advanced scenario methodology absent | Accepted; W4-U04 implements simple hypothetical shock scenario only |
| Economic usefulness not assessed | Explicitly stored as `not_assessed`; no trading implication |

---

## 10. Operator Evidence Command Pack

Use:

```text
docs/evidence/W4-U04_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes exact commands for:

1. build identity;
2. PostgreSQL migration to `20260716_0021 (head)`;
3. named W4-U04 tests;
4. committed scenario report proof;
5. raw `scenario_reports` SELECT;
6. audit/no-orphan proof;
7. read-only API 401/200/405 proof;
8. dependency/no-execution/gate proof;
9. full regression and CI through Git Bash;
10. explicit no-UI statement;
11. parity smoke.

---

## 11. DA Non-Approval Statement

W4-U04 is implemented and locally validated by the Development Authority. It is **not accepted or approved by DA declaration**.

Acceptance requires:

1. operator-run target evidence using `docs/evidence/W4-U04_OPERATOR_EVIDENCE_COMMANDS.md`;
2. PostgreSQL migration/persistence/audit proof;
3. ITRGA independent review;
4. ITRGA verdict.

DA will not begin W4-U05 or any subsequent work without ITRGA approval and a new Build Order.

---

**End of Delivery Report W4-U04**
