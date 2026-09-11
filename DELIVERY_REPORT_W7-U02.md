# DELIVERY REPORT — W7-U02

## Operator Workspace Customization

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Unit | W7-U02 — Operator Workspace Customization |
| Wave | 7 — Institutional Platform |
| Build Order | `docs/build-orders/BUILD_ORDER_W7-U02.md` |
| Prerequisite verdict | `docs/build-orders/ITRGA_VERDICT_W7-U01_FINAL.md` — W7-U01 APPROVED |
| Target platform version | `0.56.0` |
| Alembic head | `20260717_0034` |
| DA status | Implemented and locally validated |
| Approval status | Not self-approved; pending operator evidence / browser evidence / ITRGA review |

---

## 1. Executive summary

W7-U02 has been implemented as per-operator workspace customization.

The implementation adds `operator_workspace_preferences`, an operator-scoped, presentation-only preference table for layout configuration, visible modules, theme configuration, and metadata. Preferences are scoped to the authenticated AXIOM operator and cannot be read or updated by other operators.

Preference payloads reject action/order/account/execution/Gate fields and secret/PII markers recursively. A protected `/workspace` UI lets the current operator save and update presentation preferences only.

No execution/order/broker/account field or control, plugin execution, plugin execution audit table, API catalogue persistence, portfolio dashboard, research management collections/tags, external LLM/API, new dependency, live broker adapter, real order routing, real account state, real P&L, Gate-opening path, or W7-U03+ feature was added.

The Constitutional Governance Gate remains **CLOSED**.

---

## 2. Scope delivered

### A. Persistence

Created:

```text
backend/app/db/models/operator_workspace_preference.py
backend/alembic/versions/20260717_0034_w7_u02_operator_workspace_preferences.py
```

Table:

```text
operator_workspace_preferences
```

Fields:

```text
preference_id
created_at
updated_at
operator_id
workspace_key
layout_config
visible_modules
theme_config
research_status
metadata
audit_correlation_id
```

Relationship:

```text
operator_id -> operators.id
```

Rows are unique by `(operator_id, workspace_key)`.

### B. Preference service

Created:

```text
backend/app/institutional_platform/preferences.py
```

Key implementation:

```text
WorkspacePreferenceDraft
WorkspacePreferenceFactory
WorkspacePreferenceRepository
```

Validation rejects recursively:

- forbidden action/order/account/execution/Gate fields;
- secret markers such as token, jwt, password, secret, api key, private key;
- unknown fields;
- invalid visible modules.

### C. API

Extended:

```text
backend/app/api/routes/institutional_platform.py
backend/app/models/operator_workspace_preference.py
```

Endpoints:

```text
GET  /api/v1/institutional-platform/workspace-preferences
GET  /api/v1/institutional-platform/workspace-preferences/{preference_id}
POST /api/v1/institutional-platform/workspace-preferences
PUT  /api/v1/institutional-platform/workspace-preferences/{preference_id}
```

These endpoints are authenticated and operator-scoped.

### D. UI

Created:

```text
frontend/src/pages/WorkspaceCustomizationPage.tsx
frontend/src/pages/WorkspaceCustomizationPage.test.tsx
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
/workspace
```

The UI edits presentation preferences only:

- workspace key;
- layout config JSON;
- visible modules;
- theme config JSON;
- metadata JSON.

It displays a presentation-only disclaimer and no action/order/account/execution controls.

### E. Audit events

Create/update appends:

```text
operator_workspace_preference.created
operator_workspace_preference.updated
```

For created rows, no-orphan audit JOIN is required in operator evidence.

---

## 3. Guardrail compliance

| Requirement | Result |
|---|---|
| R7-3 per-operator scoping | Implemented. Repository/API filter by authenticated `operator.id`; two-operator tests prove B cannot read/update A's preference. |
| R7-7 / GR7-8 no secrets/PII | Implemented. Recursive marker rejection for config blobs and source/API checks. |
| No actuation | Implemented. Schema and validation reject action/order/account/execution/Gate fields; UI has no action controls. |
| GR7-9 persistence capture | Implemented. Evidence pack includes raw SELECT, no-orphan audit join, and operator join. |
| GR7-10 browser proof | Evidence pack requires served `/workspace` screenshots and logged-out block. |
| Gate CLOSED | Preserved and tested. |
| No dependency change | Preserved. No new package added. |

---

## 4. Files changed or added for W7-U02

### Backend created

```text
backend/app/db/models/operator_workspace_preference.py
backend/app/institutional_platform/preferences.py
backend/app/models/operator_workspace_preference.py
backend/alembic/versions/20260717_0034_w7_u02_operator_workspace_preferences.py
backend/tests/test_workspace_preferences.py
```

### Backend modified

```text
backend/app/__init__.py
backend/app/api/routes/institutional_platform.py
backend/app/core/config.py
backend/app/db/models/__init__.py
backend/app/institutional_platform/__init__.py
backend/app/institutional_platform/rbac.py
backend/app/main.py
backend/app/models/system.py
backend/pyproject.toml
backend/tests/test_institutional_platform_security.py
backend/tests/test_system.py
```

### Frontend created/modified

```text
frontend/src/pages/WorkspaceCustomizationPage.tsx
frontend/src/pages/WorkspaceCustomizationPage.test.tsx
frontend/src/App.tsx
frontend/src/api/client.ts
frontend/src/layouts/TerminalLayout.tsx
frontend/src/styles/global.css
```

### Scripts/docs created or updated

```text
scripts/w7_u02_seed_workspace_preferences.py
docs/build-orders/ITRGA_REVIEW_W7-U01.md
docs/build-orders/ITRGA_VERDICT_W7-U01_FINAL.md
docs/build-orders/BUILD_ORDER_W7-U02.md
docs/build-orders/BUILD_ORDER_INTAKE_W7-U02.md
docs/adr/ADR-065_Operator_Workspace_Customization.md
docs/evidence/W7-U02_OPERATOR_EVIDENCE_COMMANDS.md
DELIVERY_REPORT_W7-U02.md
README.md
PROJECT_STATE.md
CHANGELOG.md
docs/governance/RISK_REGISTER.md
docs/governance/TECHNICAL_DEBT_REGISTER.md
docs/governance/GOVERNANCE_AMENDMENTS.md
docs/governance/04_PROJECT_ROADMAP.md
```

---

## 5. Local validation performed by DA

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
pytest tests/test_workspace_preferences.py tests/test_institutional_platform_security.py tests/test_broker_integration.py -q
```

Result:

```text
23 passed, 1 warning
```

### Backend full suite

```bash
cd /home/user/axiom/backend
pytest -q
```

Result:

```text
366 passed, 1 warning
```

### Alembic migration smoke

```bash
cd /home/user/axiom/backend
AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w7u02_alembic.db' \
AXIOM_DATABASE_AUTO_CREATE_SCHEMA=false \
alembic upgrade head

AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w7u02_alembic.db' \
AXIOM_DATABASE_AUTO_CREATE_SCHEMA=false \
alembic current
```

Result:

```text
20260717_0034 (head)
```

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
Vitest: 19 files / 61 tests passed
TypeScript lint: clean
Build: successful
```

---

## 6. Operator evidence pack

Operator evidence command pack is ready at:

```text
docs/evidence/W7-U02_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes exact Windows PowerShell + PostgreSQL + browser commands for:

1. build identity;
2. Alembic head advance to `20260717_0034`;
3. seed script;
4. raw SELECT;
5. no-orphan audit/operator joins;
6. forbidden-column proof;
7. named tests;
8. two-operator isolation API proof;
9. no-secret/PII marker checks;
10. browser evidence;
11. bright-line grep;
12. full regression and CI.

---

## 7. Deferred / explicitly not implemented

The following remain out of scope and were not implemented:

- portfolio dashboard;
- research management collections/tags;
- API catalogue persistence;
- plugin execution;
- plugin execution audit table;
- advanced reporting/export;
- external LLM/API;
- live broker adapter;
- broker SDK or credentials;
- real order routing;
- real account/position/balance/margin/capital state;
- real P&L;
- Gate opening;
- W7-U03 or later functionality.

---

## 8. DA disposition

W7-U02 is implemented and locally validated by the Development Authority.

This is **not** an approval. DA does not self-approve W7-U02, self-authorize W7-U03, open the Governance Gate, add live broker connectivity, add execution/order/account paths, or begin any W7-U03+ feature.

Next required step: operator runs `docs/evidence/W7-U02_OPERATOR_EVIDENCE_COMMANDS.md` on the target Windows/PostgreSQL/browser environment and submits the transcript to ITRGA for independent review.

---

**End of DELIVERY_REPORT_W7-U02.md**
