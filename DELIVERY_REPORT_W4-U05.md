# Delivery Report — W4-U05

| Field | Value |
|---|---|
| Build Order | **W4-U05** Portfolio/Risk Research Analytics |
| Platform | **0.35.0** |
| Wave | **4 — Institutional Intelligence** |
| DA status | **Implemented and locally validated** |
| Approval status | **Not self-approved; pending operator evidence and ITRGA review** |
| Date | 2026-07-16 |

---

## 1. Executive Summary

W4-U05 implements persisted Portfolio/Risk Research Analytics as hypothetical market-series-level research artifacts. Reports are as-of-bounded, uncertainty-mandatory, assumption-explicit, persisted, audited, and read-only. The implementation explicitly avoids real account, broker, live position, order, execution, or sizing linkage.

Implemented outcomes:

- `portfolio_risk_reports` table and Alembic migration;
- `PortfolioRiskReportService` under Institutional Intelligence;
- as-of-bounded market-series risk windows with future-candle exclusion;
- max drawdown, realized volatility, and stress-loss-style metric;
- per-metric uncertainty and sample count;
- explicit assumptions and limitations;
- independent `economic_usefulness` field;
- audit event on report creation;
- authenticated read-only API;
- no UI in this unit;
- no account/broker/position/order/sizing path.

DA does not self-approve. Operator-run Windows + PostgreSQL evidence remains mandatory.

---

## 2. Authority and Traceability

| Artifact | Path |
|---|---|
| W4-U04 review | `docs/build-orders/ITRGA_REVIEW_W4-U04.md` |
| W4-U05 Build Order | `docs/build-orders/BUILD_ORDER_W4-U05.md` |
| W4-U05 Build Order Intake | `docs/build-orders/BUILD_ORDER_INTAKE_W4-U05.md` |
| W4-U05 ADR | `docs/adr/ADR-044_Portfolio_Risk_Research_Reports.md` |
| Operator evidence commands | `docs/evidence/W4-U05_OPERATOR_EVIDENCE_COMMANDS.md` |
| Migration | `backend/alembic/versions/20260716_0022_w4_u05_portfolio_risk_reports.py` |

---

## 3. Implementation Summary

### 3.1 Portfolio/risk report persistence

Added:

```text
backend/app/db/models/portfolio_risk_report.py
backend/alembic/versions/20260716_0022_w4_u05_portfolio_risk_reports.py
```

The table stores research artifact metadata, market-series metadata, as-of bounds, sample count, max drawdown, realized volatility, stress loss, metric payloads, uncertainty, assumptions, economic usefulness, lineage/config/results/limitations, report hash, research status, actor, and audit correlation id.

It intentionally contains no account, broker, live position, order, sizing, execution, remediation, or signal payload fields.

### 3.2 Portfolio/risk service

Added:

```text
backend/app/institutional_intelligence/portfolio_risk.py
```

Key objects:

```text
PortfolioRiskSeriesSpec
PortfolioRiskAssumptions
PortfolioRiskComputationResult
PortfolioRiskReportService
```

The service:

- reads persisted candles read-only;
- filters `open_time >= as_of_start` and `open_time <= as_of_end`;
- counts future candles beyond `as_of_end`;
- computes returns, max drawdown, realized volatility, and stress-loss-style value;
- attaches per-metric uncertainty/sample count;
- creates an `IntelligenceArtifactContract`;
- persists `PortfolioRiskReport`;
- writes `portfolio_risk_report.created` audit event.

### 3.3 R-8 linkage boundary

Reports are market-series research only. The schema has no account/broker/position linkage columns. The service does not read any broker/account/position source.

### 3.4 Read-only API

Added:

```text
GET /api/v1/intelligence/portfolio-risk-reports
GET /api/v1/intelligence/portfolio-risk-reports/{report_id}
```

No POST/emit/write route was added.

### 3.5 UI decision

W4-U05 adds no UI. The Build Order allows API + tests to suffice if no UI is added.

---

## 4. Files Created

```text
backend/app/db/models/portfolio_risk_report.py
backend/app/models/portfolio_risk_report.py
backend/app/institutional_intelligence/portfolio_risk.py
backend/alembic/versions/20260716_0022_w4_u05_portfolio_risk_reports.py
backend/tests/test_portfolio_risk_reports.py
docs/build-orders/ITRGA_REVIEW_W4-U04.md
docs/build-orders/BUILD_ORDER_W4-U05.md
docs/build-orders/BUILD_ORDER_INTAKE_W4-U05.md
docs/adr/ADR-044_Portfolio_Risk_Research_Reports.md
docs/evidence/W4-U05_OPERATOR_EVIDENCE_COMMANDS.md
DELIVERY_REPORT_W4-U05.md
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
| R-8 no account/broker/position linkage | Implemented and tested; schema inert |
| No guaranteed/expected-return framing | Implemented in limitations/tests |
| GR-7 + R-5 uncertainty/economic usefulness | Implemented and tested per metric |
| R-2 no look-ahead | Implemented and tested with future candle exclusion |
| R-6 non-signal/no mutation | Implemented and tested |
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

### Named W4-U05 tests

```text
$ pytest tests/test_portfolio_risk_reports.py -q
7 passed, 1 warning
```

### Backend full suite

```text
$ pytest -q
225 passed, 1 warning
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
Running upgrade 20260716_0021 -> 20260716_0022, W4-U05 portfolio risk research reports
20260716_0022 (head)
```

---

## 8. Security / Governance Review

| Area | Review |
|---|---|
| Authentication | API requires existing Bearer operator auth. |
| Authorization | No public portfolio/risk endpoint added. |
| Write surface | No portfolio/risk write API exposed. |
| Execution | No broker/order/execution path added. |
| Account/linkage boundary | No account/broker/position linkage fields or reads added. |
| Signal boundary | No advisory signal side-effect; report is not a signal. |
| Dependencies | Uses pure-Python arithmetic; no unspiked dependency. |
| D-W2-001 | No per-market specialized model or symbol-identity feature. |
| Persistence | New table via Alembic; audit event on create. |

---

## 9. Known Risks / Required Operator Evidence

| Risk | Status |
|---|---|
| PostgreSQL persistence proof not run in DA sandbox | Operator evidence pack includes committing script + raw SELECT + audit/no-orphan proof |
| No UI for portfolio/risk reports | Accepted; no UI in W4-U05 scope |
| Advanced portfolio methodology absent | Accepted; W4-U05 implements market-series research metrics only |
| Economic usefulness not assessed | Explicitly stored as `not_assessed`; no trading implication |

---

## 10. Operator Evidence Command Pack

Use:

```text
docs/evidence/W4-U05_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes exact commands for:

1. build identity;
2. PostgreSQL migration to `20260716_0022 (head)`;
3. named W4-U05 tests;
4. committed portfolio/risk report proof;
5. raw `portfolio_risk_reports` SELECT;
6. audit/no-orphan proof;
7. read-only API 401/200/405 proof;
8. dependency/no account-broker-position/gate proof;
9. full regression and CI through Git Bash;
10. explicit no-UI statement;
11. parity smoke.

---

## 11. DA Non-Approval Statement

W4-U05 is implemented and locally validated by the Development Authority. It is **not accepted or approved by DA declaration**.

Acceptance requires:

1. operator-run target evidence using `docs/evidence/W4-U05_OPERATOR_EVIDENCE_COMMANDS.md`;
2. PostgreSQL migration/persistence/audit proof;
3. ITRGA independent review;
4. ITRGA verdict.

DA will not begin W4-U06 or any subsequent work without ITRGA approval and a new Build Order.

---

**End of Delivery Report W4-U05**
