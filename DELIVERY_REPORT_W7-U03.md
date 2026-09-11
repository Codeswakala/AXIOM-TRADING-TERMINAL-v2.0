# DELIVERY REPORT — W7-U03

## Research Management Collections & Tags

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Unit | W7-U03 — Research Management Collections & Tags |
| Wave | 7 — Institutional Platform |
| Build Order | `docs/build-orders/BUILD_ORDER_W7-U03.md` |
| Prerequisite verdict | `docs/build-orders/ITRGA_VERDICT_W7-U02_FINAL.md` — W7-U02 APPROVED |
| Platform of record before unit | `0.56.0` |
| Target platform version | `0.57.0` candidate |
| Starting Alembic head | `20260717_0034` |
| Target Alembic head | `20260717_0037` |
| DA status | Implemented and locally validated; evidence-command fix issued after operator run issue |
| Approval status | Not self-approved; pending valid operator evidence / browser evidence / ITRGA review |

---

## 1. Executive summary

W7-U03 has been implemented as a **reference-only research management metadata layer**.

The implementation lets authenticated operators organize existing governed research artifacts into per-operator collections and apply per-operator tags. The design is deliberately non-invasive: collection members and tags reference source artifacts by `(artifact_type, artifact_id)` only and do **not** mutate, copy, own, cascade to, or materialize source artifact content.

The unit adds three tables:

```text
research_collections
research_collection_members
research_tags
```

It also adds an authenticated, operator-scoped API and a protected `/research-management` frontend surface for collection/tag management.

The central R7-5 guarantee is implemented and tested: tagging or collecting a real governed source artifact does not change the source artifact row and does not add mutation audit events to the source artifact's audit trail.

The W7-U02 OBS-1 authorization-ordering observation is also addressed: cross-operator mutation of collection membership performs ownership authorization before request-body validation, returning deterministic `403` even with an empty/invalid body.

No execution/order/broker/account field or control, source-content copy, source-artifact cascading FK, plugin execution, API ecosystem catalogue, portfolio dashboard, external LLM/API, new dependency, live broker adapter, real order routing, real account state, real P&L, Gate-opening path, or W7-U04+ feature was added.

The Constitutional Governance Gate remains **CLOSED**.

---

## 2. Scope delivered

### A. Persistence

Created:

```text
backend/app/db/models/research_management.py
backend/alembic/versions/20260717_0035_w7_u03_research_collections.py
backend/alembic/versions/20260717_0036_w7_u03_research_collection_members.py
backend/alembic/versions/20260717_0037_w7_u03_research_tags.py
```

#### Table: `research_collections`

Fields:

```text
collection_id
created_at
updated_at
operator_id
name
description
research_status
audit_correlation_id
```

Relationship:

```text
operator_id -> operators.id
```

Unique constraint:

```text
(operator_id, name)
```

#### Table: `research_collection_members`

Fields:

```text
member_id
created_at
operator_id
collection_id
artifact_type
artifact_id
audit_correlation_id
```

Relationships:

```text
operator_id -> operators.id
collection_id -> research_collections.collection_id
```

Reference-only source artifact identity:

```text
artifact_type
artifact_id
```

There is intentionally **no FK to the source artifact table**, no source-content column, and no cascading source relationship.

Unique constraint:

```text
(collection_id, artifact_type, artifact_id)
```

#### Table: `research_tags`

Fields:

```text
tag_id
created_at
operator_id
artifact_type
artifact_id
tag
audit_correlation_id
```

Relationship:

```text
operator_id -> operators.id
```

Reference-only source artifact identity:

```text
artifact_type
artifact_id
```

There is intentionally **no FK to the source artifact table**, no source-content column, and no cascading source relationship.

Unique constraint:

```text
(operator_id, artifact_type, artifact_id, tag)
```

### B. Research management service

Created:

```text
backend/app/institutional_platform/research_management.py
```

Key implementation:

```text
ResearchManagementFactory
ResearchManagementRepository
ResearchCollectionDraft
ResearchArtifactReference
ResearchTagDraft
```

Supported artifact references are validated by type and id using existing governed artifact tables. The implementation includes support for references such as:

```text
advisory_signal
correlation_report
regime_report
scenario_report
portfolio_risk_report
signal_validation_report
simulated_execution_run
simulated_fill_event
simulated_paper_ledger_entry
execution_risk_research_report
execution_research_experiment
simulated_execution_analytics_report
trade_plan_note
manual_trade_journal_entry
```

Validation rejects:

- forbidden action/order/account/execution/Gate fields;
- `source_artifact_content` / materialized source content fields;
- secret and PII markers in collection names/descriptions and tag values;
- unsupported artifact types;
- missing or invalid source artifact ids;
- duplicate collection/member/tag entries.

### C. API

Extended:

```text
backend/app/api/routes/institutional_platform.py
backend/app/models/research_management.py
```

Endpoints added:

```text
GET    /api/v1/institutional-platform/research-management
GET    /api/v1/institutional-platform/research-collections
POST   /api/v1/institutional-platform/research-collections
GET    /api/v1/institutional-platform/research-collections/{collection_id}
DELETE /api/v1/institutional-platform/research-collections/{collection_id}
GET    /api/v1/institutional-platform/research-collections/{collection_id}/members
POST   /api/v1/institutional-platform/research-collections/{collection_id}/members
DELETE /api/v1/institutional-platform/research-collections/{collection_id}/members/{member_id}
GET    /api/v1/institutional-platform/research-tags
POST   /api/v1/institutional-platform/research-tags
GET    /api/v1/institutional-platform/research-tags/{tag_id}
DELETE /api/v1/institutional-platform/research-tags/{tag_id}
```

All endpoints require authentication and are scoped to the current operator.

Cross-operator reads and mutations return `403` for existing objects owned by another operator.

For collection member mutation, the endpoint authorizes collection ownership before parsing/validating the request body, satisfying OBS-W7U02-AUTHZ-ORDER.

### D. UI

Created:

```text
frontend/src/pages/ResearchManagementPage.tsx
frontend/src/pages/ResearchManagementPage.test.tsx
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
/research-management
```

The UI supports:

- listing current-operator research collections;
- creating current-operator collections;
- adding reference-only artifact members;
- listing and creating current-operator tags;
- displaying existing governed scenario reports as read-only target artifacts;
- showing reference-only and per-operator scoping disclaimers.

The UI exposes no execution/order/account/broker/Gate/actuation controls.

### E. Audit events

Create/delete operations append audit rows:

```text
research_collection.created
research_collection.deleted
research_collection_member.created
research_collection_member.deleted
research_tag.created
research_tag.deleted
```

The operator evidence pack requires no-orphan audit joins for created rows across all three W7-U03 tables.

---

## 3. Guardrail compliance

| Requirement | Result |
|---|---|
| R7-5 source no-mutation | Implemented and tested. Collection/tag operations over a real `scenario_report` preserve before/after source row identity and do not add source audit events. |
| R7-3 per-operator scoping | Implemented and tested. API filters by authenticated `operator.id`; two-operator test proves B cannot read/list/mutate A's collections/tags. |
| OBS-W7U02-AUTHZ-ORDER | Implemented and tested. Cross-operator member mutation with empty body returns `403` before body validation. |
| R7-7 / GR7-8 no secrets/PII | Implemented and tested. Recursive/string marker rejection for collection/tag fields; operator evidence includes DB and payload grep checks. |
| GR7-9 persistence capture | Implemented. Evidence pack includes raw SELECT, no-orphan audit joins, no-orphan operator joins, and source reference sanity checks. |
| GR7-10 browser proof | Evidence pack requires served `/research-management` screenshots and logged-out block. |
| GR7-1 Gate CLOSED | Preserved and tested. |
| No dependency change | Preserved. No new package added. |
| No source content materialization | Implemented. Tables only store source references by `(artifact_type, artifact_id)`. |
| No actuation | Implemented. Schema, service, API, UI, tests, and grep preserve no execution/order/broker/account/Gate path. |

---

## 4. Files changed or added for W7-U03

### Backend created

```text
backend/app/db/models/research_management.py
backend/app/institutional_platform/research_management.py
backend/app/models/research_management.py
backend/alembic/versions/20260717_0035_w7_u03_research_collections.py
backend/alembic/versions/20260717_0036_w7_u03_research_collection_members.py
backend/alembic/versions/20260717_0037_w7_u03_research_tags.py
backend/tests/test_research_management.py
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
backend/tests/test_institutional_platform_security.py
backend/tests/test_system.py
```

### Frontend created/modified

```text
frontend/src/pages/ResearchManagementPage.tsx
frontend/src/pages/ResearchManagementPage.test.tsx
frontend/src/App.tsx
frontend/src/api/client.ts
frontend/src/layouts/TerminalLayout.tsx
frontend/src/styles/global.css
```

### Scripts/docs created or updated

```text
scripts/w7_u03_seed_research_management.py
docs/build-orders/ITRGA_VERDICT_W7-U02_FINAL.md
docs/build-orders/BUILD_ORDER_W7-U03.md
docs/build-orders/BUILD_ORDER_INTAKE_W7-U03.md
docs/adr/ADR-066_Research_Management_Collections_and_Tags.md
docs/evidence/W7-U03_OPERATOR_EVIDENCE_COMMANDS.md
docs/evidence/W7-U03_EVIDENCE_FIX_COMMANDS.md
DELIVERY_REPORT_W7-U03.md
DELIVERY_REPORT_W7-U03_EVIDENCE_FIX.md
README.md
PROJECT_STATE.md
CHANGELOG.md
```

---

## 5. Mandatory tests implemented

Backend tests in:

```text
backend/tests/test_research_management.py
```

Mandatory tests implemented:

```text
test_research_collection_persists_and_audit_no_orphan
test_research_collection_member_persists_and_audit_no_orphan
test_research_tag_persists_and_audit_no_orphan
test_tagging_or_collecting_does_not_mutate_source_artifact_or_its_audit
test_research_management_is_operator_scoped_two_operator_isolation
test_cross_operator_mutation_returns_403_before_body_validation
test_research_management_tables_have_no_forbidden_or_source_content_columns
test_research_management_has_no_secret_or_pii_markers
test_research_management_requires_auth
test_gate_remains_closed_for_wave7
```

Additional supporting test:

```text
test_research_management_page_has_no_forbidden_controls
```

Frontend tests in:

```text
frontend/src/pages/ResearchManagementPage.test.tsx
```

Named coverage:

```text
ResearchManagementPage lists collections/tags over existing artifacts (read-only of others' data blocked)
ResearchManagementPage exposes no execution/order/account/actuation controls
ResearchManagementPage requires auth / blocks logged-out access
```

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
pytest tests/test_research_management.py tests/test_workspace_preferences.py tests/test_institutional_platform_security.py tests/test_broker_integration.py -q
```

Result:

```text
34 passed, 1 warning
```

### Backend full suite

```bash
cd /home/user/axiom/backend
pytest -q
```

Result:

```text
377 passed, 1 warning
```

Operator Windows run also reported:

```text
W7-U03 named backend tests: 11 passed
W7-U03 + W7 security + broker targeted suite: 34 passed
Backend full suite: 377 passed
Ruff: All checks passed
```

### Alembic migration smoke

```bash
cd /home/user/axiom/backend
AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w7u03_alembic.db' \
AXIOM_DATABASE_AUTO_CREATE_SCHEMA=false \
alembic upgrade head

AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w7u03_alembic.db' \
AXIOM_DATABASE_AUTO_CREATE_SCHEMA=false \
alembic current
```

Result:

```text
20260717_0037 (head)
```

Operator PostgreSQL migration run also reported:

```text
20260717_0037 (head)
```

### Frontend validation

```bash
cd /home/user/axiom/frontend
npm ci
npm audit --audit-level=high
npm test
npx tsc -b --pretty false
npm run build
```

Results:

```text
npm audit: found 0 vulnerabilities
Vitest: 20 files / 64 tests passed
TypeScript: clean
Build: successful
```

Operator Windows run also reported:

```text
ResearchManagementPage.test.tsx: 3 passed
Frontend full suite: 20 files / 64 tests passed
Build: successful
```

---

## 7. Evidence-command correction after operator run

The first operator evidence run surfaced two command-pack issues, both corrected by DA:

### E-1 — seed script import path

Observed:

```text
ModuleNotFoundError: No module named 'app'
```

Correction:

```text
scripts/w7_u03_seed_research_management.py
```

The script now inserts the backend package root into `sys.path` when run from repository root.

DA locally validated the fixed seed script from repository root, producing:

```text
W7_U03_RESEARCH_MANAGEMENT_SEED_COMPLETE
SOURCE_IDENTITY_UNCHANGED=True
SOURCE_AUDIT_UNCHANGED=True
```

### E-2 — PowerShell `Invoke-WebRequest` prompt

Observed:

```text
Security Warning: Script Execution Risk
```

Correction:

```text
docs/evidence/W7-U03_OPERATOR_EVIDENCE_COMMANDS.md
```

The login commands now use:

```powershell
Invoke-WebRequest -UseBasicParsing
```

A focused rerun pack was created:

```text
docs/evidence/W7-U03_EVIDENCE_FIX_COMMANDS.md
```

Evidence-fix report:

```text
DELIVERY_REPORT_W7-U03_EVIDENCE_FIX.md
```

These corrections do not add capability, do not alter governance scope, and do not self-approve W7-U03.

---

## 8. Operator evidence pack

Primary W7-U03 evidence command pack:

```text
docs/evidence/W7-U03_OPERATOR_EVIDENCE_COMMANDS.md
```

Focused evidence-fix rerun pack:

```text
docs/evidence/W7-U03_EVIDENCE_FIX_COMMANDS.md
```

The evidence pack includes exact Windows PowerShell + PostgreSQL + browser commands for:

1. build identity;
2. Alembic head advance to `20260717_0037`;
3. committing seed script;
4. raw SELECT for all three tables;
5. no-orphan audit/operator joins for all three tables;
6. source-reference sanity checks;
7. forbidden/source-content column proof;
8. named backend/frontend tests;
9. R7-5 source no-mutation proof;
10. two-operator API isolation with valid tokens;
11. authorize-before-validate `403` proof;
12. no-secret/PII marker checks;
13. browser evidence;
14. bright-line grep/no dependency change;
15. full regression and Git-Bash local CI.

---

## 9. Deferred / explicitly not implemented

The following remain out of scope and were not implemented:

- source artifact mutation;
- source content copy/materialization;
- source-artifact cascading FK;
- portfolio dashboard;
- API ecosystem catalogue;
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
- W7-U04 or later functionality.

---

## 10. DA disposition

W7-U03 is implemented and locally validated by the Development Authority.

This is **not** an approval. DA does not self-approve W7-U03, self-authorize W7-U04, open the Governance Gate, add live broker connectivity, add execution/order/account paths, mutate source artifacts through research management, or begin any W7-U04+ feature.

Next required step: operator completes the fixed W7-U03 evidence commands on the target Windows/PostgreSQL/browser environment and submits the transcript to ITRGA for independent review.

---

**End of DELIVERY_REPORT_W7-U03.md**
