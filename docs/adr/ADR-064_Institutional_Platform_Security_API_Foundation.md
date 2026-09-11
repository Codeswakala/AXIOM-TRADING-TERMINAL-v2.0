# ADR-064 — Institutional Platform Security & API Foundation

| Field | Value |
|---|---|
| Status | Accepted for W7-U01 implementation by DA; pending operator evidence / ITRGA review |
| Date | 2026-07-18 |
| Unit | W7-U01 — Institutional Platform Security & API Foundation |
| Platform version | 0.55.0 |
| Alembic head | 20260717_0033 unchanged |
| Builds on | Wave-7 design review accepted with R7-1…R7-8 |

---

## Context

Wave 7 is the final roadmap wave and introduces the largest institutional attack surface: API ecosystem, plugin contracts, multi-user readiness, workspace preferences, research management, reporting, and scalability. W7-U01 is the safety/foundation unit: prove institutional routes are authenticated, RBAC is default-deny, operator scoping works, and no institutional route exposes execution/order/broker/account/Gate capability.

---

## Decision

Add an `institutional_platform` bounded-context skeleton with in-code policy contracts and tests, but no new database table.

Created backend package:

```text
backend/app/institutional_platform/
```

Core contracts:

- `InstitutionalPermission`
- `INSTITUTIONAL_ROLE_PERMISSIONS`
- `INSTITUTIONAL_ROUTE_INVENTORY`
- `InstitutionalScopeRecord`
- `require_institutional_permission()`
- `assert_permission_vocabulary_safe()`

Add authenticated institutional routes:

```text
GET /api/v1/institutional-platform/route-inventory
GET /api/v1/institutional-platform/rbac/permissions
GET /api/v1/institutional-platform/operator-scope-records
GET /api/v1/institutional-platform/operator-scope-records/{operator_id}
```

No POST/PUT/PATCH/DELETE institutional route is added.

---

## RBAC posture

RBAC is policy-constant based in W7-U01. No RBAC table is added.

Default-deny behavior:

- unknown/unprivileged roles get no permissions;
- `operator` role can read only its own institutional scope record;
- `admin` role can read route inventory and RBAC vocabulary.

The permission vocabulary contains no Gate, execution, order, broker, account, position, live, capital, or margin capability.

---

## Operator isolation posture

W7-U01 uses existing `operators` rows as the real identity source. The institutional scope endpoints derive a per-operator institutional scope record from the authenticated `Operator` row.

Isolation behavior:

- operator A can read A's own scope record;
- operator B cannot read A's scope record;
- operator B's list endpoint returns only B's scope record;
- mutation attempts are absent and return 404/405.

This satisfies the W7-U01 foundation goal without introducing a new table.

---

## Deliberately not included

- No new table.
- No migration.
- No UI.
- No plugin execution.
- No plugin execution audit table.
- No external LLM/API.
- No dependency.
- No execution/order/broker/account endpoint.
- No Gate-opening path.
- No workspace/portfolio/research-management feature.
- No Wave-7 feature beyond the security/API foundation.

---

## Validation expectations

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

Standing broker tests must remain green.

---

**End of ADR-064**
