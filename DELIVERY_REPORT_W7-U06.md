# DELIVERY REPORT — W7-U06

## Portfolio Research Dashboard / Advanced Reporting

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Unit | W7-U06 — Portfolio Research Dashboard / Advanced Reporting |
| Wave | 7 — Institutional Platform |
| Build Order | `docs/build-orders/BUILD_ORDER_W7-U06.md` |
| Prerequisite verdict | `docs/build-orders/ITRGA_REVIEW_W7-U05.md` — W7-U05 APPROVED CLEAN |
| Platform of record before unit | `0.59.0` |
| Target platform version | `0.60.0` candidate |
| Alembic head | `20260717_0037` unchanged |
| DA status | Implemented and locally validated |
| Approval status | Not self-approved; pending operator evidence / browser evidence / ITRGA review |

---

## 1. Executive summary

W7-U06 has been implemented as a **portfolio research dashboard and advanced reporting/export preview** over existing governed research artifacts.

The implementation is deliberately research-only and non-persistent. It reads current-operator governed artifacts, aggregates them into hypothetical research descriptors, and produces a generated report/export preview with source artifact ids, sample counts, uncertainty descriptors, limitations, full included scope, separate `economic_usefulness`, and a deterministic report hash.

The implementation adds:

```text
GET /api/v1/institutional-platform/portfolio-research/dashboard
GET /api/v1/institutional-platform/portfolio-research/report
```

and frontend route:

```text
/portfolio-research
```

No W7-U06 report table was persisted. No migration was added. Alembic head remains:

```text
20260717_0037
```

The UI is explicitly hypothetical/research framed and avoids real account, balance, and P&L labels. It exposes no execution/order/account/broker/Gate/actuation controls.

No execution/order/broker/account/open-gate endpoint, plugin execution, external LLM/API, new dependency, live broker adapter, real order routing, real account state, real P&L, Gate-opening path, or W7-U07+ feature was added.

The Constitutional Governance Gate remains **CLOSED**.

---

## 2. Scope delivered

### A. Portfolio research service

Created:

```text
backend/app/institutional_platform/portfolio_research.py
```

Key implementation:

```text
PortfolioResearchService
PortfolioResearchMetric
PortfolioResearchSnapshot
```

Static method version:

```text
w7-u06.portfolio_research.v1
```

The service reads existing current-operator governed artifacts including:

```text
simulated_execution_runs
execution_research_experiments
research_collections
research_tags
```

It returns aggregate descriptors with:

```text
source_artifact_ids
sample_count
uncertainty
limitations
economic_usefulness
included_scope
research_status
```

### B. Advanced report/export preview

The generated report endpoint returns:

```text
report_id
method_version
operator_id
research_status
disclaimer
included_scope
sections
source_artifact_ids
limitations
economic_usefulness
report_hash
export_preview_markdown
persisted: false
```

The report hash is deterministic over stable scope and aggregate data.

No report row is persisted.

### C. API schemas

Created:

```text
backend/app/models/portfolio_research.py
```

Schemas:

```text
PortfolioResearchMetricRead
PortfolioResearchDashboardRead
AdvancedResearchReportRead
```

### D. API routes

Extended:

```text
backend/app/api/routes/institutional_platform.py
backend/app/institutional_platform/rbac.py
backend/app/institutional_platform/api_catalogue.py
```

Endpoints:

```text
GET /api/v1/institutional-platform/portfolio-research/dashboard
GET /api/v1/institutional-platform/portfolio-research/report
```

Both endpoints require authentication and are scoped to the authenticated operator.

No mutation endpoint was added.

The W7-U04 API catalogue automatically includes the new routes as operator-scoped institutional routes.

### E. UI

Created:

```text
frontend/src/pages/PortfolioResearchPage.tsx
frontend/src/pages/PortfolioResearchPage.test.tsx
```

Modified:

```text
frontend/src/App.tsx
frontend/src/api/client.ts
frontend/src/layouts/TerminalLayout.tsx
frontend/src/styles/global.css
```

New protected route:

```text
/portfolio-research
```

The UI displays:

- hypothetical research disclaimer;
- aggregate research figures;
- sample counts;
- uncertainty method;
- separate economic usefulness verdict;
- report hash;
- generated export preview;
- included scope and limitations.

The UI exposes no execution/order/account/broker/Gate/actuation controls and no real P&L/balance/account labels.

### F. Evidence seed script

Created:

```text
scripts/w7_u06_seed_portfolio_research.py
```

It creates existing simulated research artifacts for admin and two real operators, then emits ids for operator-scoping evidence.

---

## 3. Guardrail compliance

| Requirement | Result |
|---|---|
| No real account/P&L | Implemented and tested. No forbidden fields/labels in service/UI; no report table persisted. |
| GR7-4 uncertainty + stat≠economic | Implemented and tested. Figures include uncertainty/sample_count; economic usefulness is separate and `not_assessed`. |
| No cherry-picking | Implemented and tested. Report includes full current-operator source scope. |
| Deterministic hash | Implemented and tested for generated report. |
| R7-3 operator scoping | Implemented and tested. Valid-token two-operator test proves B does not see A source artifact ids. |
| R7-7 / GR7-8 no secrets/PII | Implemented and tested. Dashboard/report response marker scan is clean. |
| GR7-9 persistence capture | Not applicable. No W7-U06 report table persisted. |
| GR7-10 browser proof | Evidence pack requires served `/portfolio-research` screenshots and logged-out block. |
| GR7-1 Gate CLOSED | Preserved and tested. |
| No dependency change | Preserved. No new package added. |

---

## 4. Files changed or added for W7-U06

### Backend created

```text
backend/app/institutional_platform/portfolio_research.py
backend/app/models/portfolio_research.py
backend/tests/test_portfolio_research.py
```

### Backend modified

```text
backend/app/__init__.py
backend/app/api/routes/institutional_platform.py
backend/app/core/config.py
backend/app/institutional_platform/__init__.py
backend/app/institutional_platform/api_catalogue.py
backend/app/institutional_platform/rbac.py
backend/app/main.py
backend/app/models/system.py
backend/tests/test_system.py
```

### Frontend created/modified

```text
frontend/src/pages/PortfolioResearchPage.tsx
frontend/src/pages/PortfolioResearchPage.test.tsx
frontend/src/App.tsx
frontend/src/api/client.ts
frontend/src/layouts/TerminalLayout.tsx
frontend/src/styles/global.css
```

### Scripts/docs created or updated

```text
scripts/w7_u06_seed_portfolio_research.py
docs/build-orders/ITRGA_REVIEW_W7-U05.md
docs/build-orders/BUILD_ORDER_W7-U06.md
docs/build-orders/BUILD_ORDER_INTAKE_W7-U06.md
docs/adr/ADR-069_Portfolio_Research_Dashboard_and_Advanced_Reporting.md
docs/evidence/W7-U06_OPERATOR_EVIDENCE_COMMANDS.md
DELIVERY_REPORT_W7-U06.md
README.md
PROJECT_STATE.md
CHANGELOG.md
```

---

## 5. Mandatory tests implemented

Backend tests in:

```text
backend/tests/test_portfolio_research.py
```

Mandatory tests implemented:

```text
test_portfolio_dashboard_aggregates_existing_artifacts_read_only
test_portfolio_and_reports_have_no_real_account_or_pnl_field_or_label
test_reports_carry_uncertainty_limitations_and_separate_economic_usefulness
test_reports_have_no_real_pnl_or_guaranteed_return_language
test_report_full_scope_included_no_cherry_picking
test_portfolio_and_reports_are_operator_scoped_two_operator
test_portfolio_and_reports_have_no_secret_or_pii_markers
test_gate_remains_closed_for_wave7
```

Frontend tests in:

```text
frontend/src/pages/PortfolioResearchPage.test.tsx
```

Named coverage:

```text
PortfolioResearchPage renders hypothetical/uncertainty-framed aggregates over existing artifacts (read-only of others' data blocked)
PortfolioResearchPage/ReportBuilder exposes no execution/order/account/actuation controls and no real-P&L labels
PortfolioResearchPage requires auth / blocks logged-out access
```

No persistence-capture/forbidden-column tests were added for a W7-U06 report table because no report table was persisted.

---

## 6. Local validation performed by DA

### Backend Ruff

```bash
cd /home/user/axiom/backend
ruff check .
```

Result:

```text
All checks passed!
```

### Targeted backend tests

```bash
cd /home/user/axiom/backend
pytest tests/test_portfolio_research.py tests/test_plugin_contracts.py tests/test_api_catalogue.py tests/test_research_management.py tests/test_workspace_preferences.py tests/test_institutional_platform_security.py tests/test_broker_integration.py -q
```

Result:

```text
56 passed, 1 warning
```

### Backend full suite

```bash
cd /home/user/axiom/backend
pytest -q
```

Result:

```text
399 passed, 1 warning
```

### Alembic migration state

```bash
cd /home/user/axiom/backend
alembic upgrade head
alembic current
```

Result:

```text
20260717_0037 (head)
```

No W7-U06 migration was created.

### Frontend validation

```bash
cd /home/user/axiom/frontend
npm ci
npm audit --audit-level=high
npm test -- PortfolioResearchPage.test.tsx
npm test
npm run lint
npm run build
```

Results:

```text
npm audit: found 0 vulnerabilities
PortfolioResearchPage.test.tsx: 3 passed
Vitest: 21 files / 67 tests passed
TypeScript: clean
Build: successful
```

---

## 7. Operator evidence pack

Operator evidence command pack is ready at:

```text
docs/evidence/W7-U06_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes exact Windows PowerShell + PostgreSQL + browser commands for:

1. build identity;
2. unchanged Alembic head and no report table;
3. seed existing simulated artifacts;
4. dashboard/report API proof;
5. uncertainty/sample_count/economic_usefulness proof;
6. no real account/P&L marker proof over API/UI;
7. valid-token two-operator scoping proof;
8. mutation route absence proof;
9. no secret/PII marker proof;
10. mandatory browser evidence;
11. no dependency declaration;
12. full regression and Git-Bash local CI.

---

## 8. Deferred / explicitly not implemented

The following remain out of scope and were not implemented:

- persisted advanced research report table;
- persisted report export table;
- real account source;
- real account/position/balance/margin/capital fields;
- real P&L fields or labels;
- execution/order/broker/account/open-gate endpoint;
- plugin execution;
- external LLM/API;
- new dependency;
- live broker adapter;
- broker SDK or credentials;
- real order routing;
- Gate opening;
- W7-U07 or later functionality.

---

## 9. DA disposition

W7-U06 is implemented and locally validated by the Development Authority.

This is **not** an approval. DA does not self-approve W7-U06, self-authorize W7-U07, open the Governance Gate, add live broker connectivity, add execution/order/account paths, add real account/P&L surfaces, or begin any W7-U07+ feature.

Next required step: operator runs `docs/evidence/W7-U06_OPERATOR_EVIDENCE_COMMANDS.md` on the target Windows/PostgreSQL/browser environment and submits the transcript to ITRGA for independent review.

---

**End of DELIVERY_REPORT_W7-U06.md**
