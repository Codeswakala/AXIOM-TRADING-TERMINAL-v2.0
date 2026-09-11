# DELIVERY REPORT — W7-U04

## API Ecosystem Catalogue & Versioned Research API Hardening

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Unit | W7-U04 — API Ecosystem Catalogue & Versioned Research API Hardening |
| Wave | 7 — Institutional Platform |
| Build Order | `docs/build-orders/BUILD_ORDER_W7-U04.md` |
| Prerequisite verdict | `docs/build-orders/ITRGA_VERDICT_W7-U03_FINAL.md` — W7-U03 APPROVED |
| Platform of record before unit | `0.57.0` |
| Target platform version | `0.58.0` candidate |
| Alembic head | `20260717_0037` unchanged |
| DA status | Implemented and locally validated |
| Approval status | Not self-approved; pending operator evidence / ITRGA review |

---

## 1. Executive summary

W7-U04 has been implemented as an authenticated, generated, versioned API catalogue for existing research and institutional API routes, plus API-surface hardening tests.

The implementation adds:

```text
GET /api/v1/institutional-platform/api-catalogue
```

The catalogue is generated from FastAPI route metadata at request time. It exposes sanitized route descriptors including path, methods, permission descriptor, version, description, tags, authentication requirement, operator-scoped classification, and mutation classification.

The catalogue asserts:

```text
actuation_surface_present: false
governance_gate_capability_present: false
```

No catalogue table was persisted. No migration was added. Alembic head remains:

```text
20260717_0037
```

No frontend catalogue UI was added. Browser evidence is therefore not applicable for W7-U04.

No rate-limit dependency or storage was added. The catalogue response explicitly declares the abuse/rate guard as deferred for this catalogue unit while existing auth, role, and operator scoping remain active.

No execution/order/broker/account/open-gate endpoint, plugin execution, external LLM/API, new dependency, live broker adapter, real order routing, real account state, real P&L, Gate-opening path, or W7-U05+ feature was added.

The Constitutional Governance Gate remains **CLOSED**.

---

## 2. Scope delivered

### A. API catalogue generation

Created:

```text
backend/app/institutional_platform/api_catalogue.py
```

Key implementation:

```text
ApiCatalogueRoute
build_api_catalogue
CATALOGUE_VERSION = "w7-u04.research_api_catalogue.v1"
API_ROUTE_VERSION = "v1"
```

The generator walks registered FastAPI routes, including nested included routers, and selects `/api/v1` routes tagged as research/institutional surfaces:

```text
advisory-analytics
advisory-signals
collaboration
execution-research
institutional-intelligence
institutional-platform
monitoring-alerts
```

Each descriptor includes:

```text
path
methods
permission
version
description
tags
auth_required
operator_scoped
mutation
```

### B. API endpoint

Extended:

```text
backend/app/api/routes/institutional_platform.py
```

New endpoint:

```text
GET /api/v1/institutional-platform/api-catalogue
```

The endpoint is authenticated through institutional RBAC and available to authenticated operators with:

```text
institutional.api_catalogue.read
```

### C. RBAC / inventory

Extended:

```text
backend/app/institutional_platform/rbac.py
```

Added permission:

```text
institutional.api_catalogue.read
```

The permission vocabulary remains free of Gate/execution/order/account/broker capabilities.

Updated institutional route inventory to include:

```text
/api/v1/institutional-platform/api-catalogue
```

### D. Persistence choice

No catalogue table was added.

No migration was added.

No `api_contract_catalog` or `api_access_audit_summary` table exists.

Alembic head remains:

```text
20260717_0037
```

### E. Frontend choice

No frontend API catalogue/docs surface was added.

Only the shell unit label was updated to W7-U04.

Browser evidence is not applicable because W7-U04 is API-only.

---

## 3. Guardrail compliance

| Requirement | Result |
|---|---|
| R7-2 / GR7-5 no execution surface | Implemented and tested. Catalogue asserts no actuation/Gate capability; forbidden endpoint probes return 404/405. |
| Auth on every catalogued route | Implemented and tested. Catalogue endpoint and representative catalogued routes return 401 unauthenticated and non-401 authenticated. |
| R7-3 operator scoping preserved | Implemented and tested using valid two-operator tokens and W7-U03 research-collection scoping. |
| Authorize-before-validate | Preserved and tested. Cross-operator member mutation with empty body returns 403. |
| R7-7 / GR7-8 / §77 no secrets/PII | Implemented and tested. Catalogue response marker scan is clean. |
| Abuse guard | Explicitly declared deferred in catalogue response; no new dependency or storage introduced. |
| GR7-9 persistence capture | Not applicable. No W7-U04 table persisted. |
| GR7-10 browser proof | Not applicable. No W7-U04 UI surface added. |
| GR7-1 Gate CLOSED | Preserved and tested. |
| No dependency change | Preserved. No new package added. |

---

## 4. Files changed or added for W7-U04

### Backend created

```text
backend/app/institutional_platform/api_catalogue.py
backend/tests/test_api_catalogue.py
```

### Backend modified

```text
backend/app/__init__.py
backend/app/api/routes/institutional_platform.py
backend/app/core/config.py
backend/app/institutional_platform/__init__.py
backend/app/institutional_platform/rbac.py
backend/app/main.py
backend/app/models/system.py
backend/tests/test_system.py
```

### Frontend modified

```text
frontend/src/layouts/TerminalLayout.tsx
```

### Scripts/docs created or updated

```text
docs/build-orders/ITRGA_VERDICT_W7-U03_FINAL.md
docs/build-orders/BUILD_ORDER_W7-U04.md
docs/build-orders/BUILD_ORDER_INTAKE_W7-U04.md
docs/adr/ADR-067_API_Ecosystem_Catalogue_and_Research_API_Hardening.md
docs/evidence/W7-U04_OPERATOR_EVIDENCE_COMMANDS.md
docs/build-orders/ITRGA_REVIEW_W7-U04.md
docs/evidence/W7-U04_C1_CORRECTION_COMMANDS.md
DELIVERY_REPORT_W7-U04.md
DELIVERY_REPORT_W7-U04_C1_RESPONSE.md
README.md
PROJECT_STATE.md
CHANGELOG.md
```

---

## 5. Mandatory tests implemented

Backend tests in:

```text
backend/tests/test_api_catalogue.py
```

Mandatory tests implemented:

```text
test_api_catalogue_lists_versioned_research_routes
test_api_catalogue_and_research_api_have_no_execution_or_broker_or_gate_endpoint
test_all_catalogued_routes_require_auth
test_api_catalogue_response_has_no_secret_or_pii_markers
test_api_surface_preserves_operator_scoping_two_operator
test_gate_remains_closed_for_wave7
```

No rate/abuse guard test was added because no rate guard was added; the catalogue declares the guard deferred.

No persistence-capture/forbidden-column test was added for a W7-U04 table because no W7-U04 catalogue table was persisted.

No frontend API-catalogue tests were added because no W7-U04 UI surface was added.

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
pytest tests/test_api_catalogue.py tests/test_research_management.py tests/test_workspace_preferences.py tests/test_institutional_platform_security.py tests/test_broker_integration.py -q
```

Result:

```text
40 passed, 1 warning
```

### Backend full suite

```bash
cd /home/user/axiom/backend
pytest -q
```

Result:

```text
383 passed, 1 warning
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

No W7-U04 migration was created.

### Frontend validation

```bash
cd /home/user/axiom/frontend
npm ci
npm audit --audit-level=high
npm test
npm run lint
npm run build
```

Results:

```text
npm audit: found 0 vulnerabilities
Vitest: 20 files / 64 tests passed
TypeScript: clean
Build: successful
```

---

## 7. Operator evidence pack

Primary operator evidence command pack:

```text
docs/evidence/W7-U04_OPERATOR_EVIDENCE_COMMANDS.md
```

Initial operator evidence proved build identity, unchanged Alembic head, no catalogue table, authenticated catalogue retrieval, no-execution-surface probes, auth status table, no dependency / no UI declaration, full regression, CI, and Gate CLOSED.

ITRGA review found that three named standalone operator-run proofs were not present in the initial transcript even though they were covered by passing tests:

```text
two-operator scoping spot-check with valid tokens
authorize-before-validate 403 proof
no-secret/PII response marker check over catalogue/API responses
```

Focused C-1 correction command pack:

```text
docs/evidence/W7-U04_C1_CORRECTION_COMMANDS.md
```

That correction pack supersedes the initial §5(f)/(g) evidence-form gap and provides exact Windows PowerShell + PostgreSQL commands for:

1. two real distinct operators and collections;
2. valid A/B login status and non-empty token checks;
3. B reading A's collection -> `403`;
4. B list visibility for A rows -> `0`;
5. cross-operator mutation with empty body -> `403`;
6. raw `raw_b_rows_for_a_collection = 0`;
7. no secret/PII markers in catalogue/API response files.

---

## 8. Deferred / explicitly not implemented

The following remain out of scope and were not implemented:

- persisted API contract catalogue table;
- API access audit summary table;
- frontend API catalogue/docs UI;
- rate-limit dependency or rate-limit storage;
- execution/order/broker/account/open-gate endpoint;
- plugin execution;
- plugin execution audit table;
- external LLM/API;
- live broker adapter;
- broker SDK or credentials;
- real order routing;
- real account/position/balance/margin/capital state;
- real P&L;
- Gate opening;
- W7-U05 or later functionality.

---

## 9. DA disposition

W7-U04 is implemented and locally validated by the Development Authority.

This is **not** an approval. DA does not self-approve W7-U04, self-authorize W7-U05, open the Governance Gate, add live broker connectivity, add execution/order/account paths, or begin any W7-U05+ feature.

Next required step: operator runs `docs/evidence/W7-U04_OPERATOR_EVIDENCE_COMMANDS.md` on the target Windows/PostgreSQL environment and submits the transcript to ITRGA for independent review.

---

**End of DELIVERY_REPORT_W7-U04.md**
