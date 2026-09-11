# DELIVERY REPORT — W7-U01

## Institutional Platform Security & API Foundation

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Unit | W7-U01 — Institutional Platform Security & API Foundation |
| Wave | 7 — Institutional Platform |
| Build Order | `docs/build-orders/BUILD_ORDER_W7-U01.md` |
| Design review | `docs/build-orders/ITRGA_REVIEW_WAVE7_DESIGN_PLAN.md` |
| Target platform version | `0.55.0` |
| Alembic head | `20260717_0033` unchanged; no W7-U01 migration |
| DA status | Implemented and locally validated |
| Approval status | Not self-approved; pending operator evidence and ITRGA review |

---

## 1. Executive summary

W7-U01 has been implemented as the Institutional Platform security and API foundation.

The implementation adds an institutional-platform bounded-context skeleton, default-deny RBAC policy constants, an institutional route inventory, authenticated institutional API routes, and per-operator scope endpoints. It proves the safety envelope before any Wave-7 feature: institutional routes require auth, unprivileged roles are denied by default, the permission vocabulary cannot encode Gate/execution/order/broker/account capabilities, and two-operator isolation is enforced.

No new table, migration, UI, plugin execution, plugin execution audit table, dependency, external LLM/API, live broker, execution/order/account endpoint, or Gate-opening path was added.

The Constitutional Governance Gate remains **CLOSED**.

---

## 2. Scope delivered

### A. Institutional Platform bounded-context skeleton

Created:

```text
backend/app/institutional_platform/__init__.py
backend/app/institutional_platform/rbac.py
```

Core contracts:

```text
InstitutionalPermission
INSTITUTIONAL_ROLE_PERMISSIONS
INSTITUTIONAL_ROUTE_INVENTORY
InstitutionalScopeRecord
require_institutional_permission()
assert_permission_vocabulary_safe()
```

### B. Authenticated institutional routes

Created:

```text
backend/app/api/routes/institutional_platform.py
```

Registered routes:

```text
GET /api/v1/institutional-platform/route-inventory
GET /api/v1/institutional-platform/rbac/permissions
GET /api/v1/institutional-platform/operator-scope-records
GET /api/v1/institutional-platform/operator-scope-records/{operator_id}
```

No POST/PUT/PATCH/DELETE institutional route is added.

### C. Default-deny RBAC

Policy is implemented in code, with no schema in W7-U01.

Roles:

```text
admin    -> route inventory, RBAC vocabulary, own operator scope
operator -> own operator scope only
unknown/unprivileged -> no permissions
```

The permission vocabulary excludes Gate, execution, order, broker, account, position, live, capital, and margin capabilities.

### D. Two-operator isolation seam

The operator-scope endpoints derive per-operator institutional scope records from existing `operators` rows.

Behavior:

- operator A can read A's own scope record;
- operator B cannot read A's scope record;
- operator B's scope list includes B only;
- mutation attempts are absent and return 404/405.

### E. Tests

Created:

```text
backend/tests/test_institutional_platform_security.py
```

Named tests:

```text
test_gate_remains_closed_for_wave7
test_no_execution_or_broker_endpoint_in_wave7_api
test_api_requires_auth_for_all_institutional_routes
test_rbac_default_denies_unprivileged_operator
test_rbac_permission_vocabulary_excludes_gate_execution_account_capability
test_two_operator_isolation_no_cross_operator_leakage
test_institutional_platform_has_no_secret_or_pii_markers
test_wave7_bright_line_grep_no_execution_path
```

---

## 3. Guardrail compliance

| Requirement | Result |
|---|---|
| GR7-1 Gate CLOSED | Implemented/tested; no Gate mutation or permission exists. |
| GR7-2 no execution surface | Institutional route inventory and absent endpoint tests prove no execute/order/broker/account route. |
| GR7-5 authenticated APIs | Institutional routes require auth; unauth returns 401. |
| R7-2 strong absence | Would-be execution/order/broker/account/Gate paths return 404/405. |
| R7-3 two-operator isolation | Real operators are used in tests; cross-operator scope read is 403 and list leakage count is zero. |
| R7-4 RBAC default-deny | Unprivileged role is denied; permission vocabulary excludes forbidden capabilities. |
| R7-7 / GR7-8 no secret/PII markers | Source/payload marker checks added. |
| R7-1 no plugin execution | No plugin execution or plugin execution audit table added. |
| No persistence | Preserved; no W7-U01 migration/table. |

---

## 4. Files changed or added for W7-U01

### Backend created

```text
backend/app/institutional_platform/__init__.py
backend/app/institutional_platform/rbac.py
backend/app/api/routes/institutional_platform.py
backend/tests/test_institutional_platform_security.py
```

### Backend modified

```text
backend/app/__init__.py
backend/app/api/router.py
backend/app/core/config.py
backend/app/main.py
backend/app/models/system.py
backend/pyproject.toml
backend/tests/test_system.py
```

### Frontend modified

```text
frontend/src/layouts/TerminalLayout.tsx
```

No W7-U01 UI page was added.

### Docs created or updated

```text
docs/build-orders/ITRGA_REVIEW_WAVE7_DESIGN_PLAN.md
docs/build-orders/BUILD_ORDER_W7-U01.md
docs/build-orders/BUILD_ORDER_INTAKE_W7-U01.md
docs/adr/ADR-064_Institutional_Platform_Security_API_Foundation.md
docs/evidence/W7-U01_OPERATOR_EVIDENCE_COMMANDS.md
DELIVERY_REPORT_W7-U01.md
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

### W7-U01 targeted tests + broker suite

```bash
cd /home/user/axiom/backend
pytest tests/test_institutional_platform_security.py tests/test_broker_integration.py -q
```

Result:

```text
16 passed, 1 warning
```

### Backend full suite

```bash
cd /home/user/axiom/backend
pytest -q
```

Result:

```text
359 passed, 1 warning
```

### Alembic migration smoke

```bash
cd /home/user/axiom/backend
AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w7u01_alembic.db' \
AXIOM_DATABASE_AUTO_CREATE_SCHEMA=false \
alembic upgrade head

AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w7u01_alembic.db' \
AXIOM_DATABASE_AUTO_CREATE_SCHEMA=false \
alembic current
```

Result:

```text
20260717_0033 (head)
```

No W7-U01 migration was added.

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
Vitest: 18 files passed / 58 tests passed
TypeScript lint: clean
Build: successful
```

---

## 6. Operator evidence pack

Operator evidence command pack is ready at:

```text
docs/evidence/W7-U01_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes exact Windows PowerShell + PostgreSQL/API commands for:

1. build identity;
2. no migration/no table proof;
3. named tests;
4. seeding two real operators;
5. auth/route inventory proof;
6. absent execution/order/broker/account/Gate endpoints;
7. RBAC default-deny and vocabulary proof;
8. two-operator isolation proof;
9. no-secret/no-PII marker checks;
10. bright-line grep and broker containment;
11. full regression and CI.

---

## 7. Deferred / explicitly not implemented

The following remain out of scope and were not implemented:

- workspace customization;
- portfolio dashboard;
- research management collections/tags;
- API catalogue persistence;
- plugin execution;
- plugin execution audit table;
- advanced reporting/export;
- new table/migration;
- UI;
- external LLM/API;
- live broker adapter;
- broker SDK or credentials;
- real order routing;
- real account/position/balance/margin/capital state;
- real P&L;
- Gate opening;
- W7-U02 or later feature work.

---

## 8. DA disposition

W7-U01 is implemented and locally validated by the Development Authority.

This is **not** an approval. DA does not self-approve W7-U01, self-authorize W7-U02, open the Governance Gate, add live broker connectivity, add execution/order/account paths, or begin any W7-U02+ feature.

Next required step: operator runs `docs/evidence/W7-U01_OPERATOR_EVIDENCE_COMMANDS.md` on the target Windows/PostgreSQL environment and submits the transcript to ITRGA for independent review.

---

**End of DELIVERY_REPORT_W7-U01.md**
