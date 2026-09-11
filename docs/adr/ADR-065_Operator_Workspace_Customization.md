# ADR-065 — Operator Workspace Customization

| Field | Value |
|---|---|
| Status | Accepted for W7-U02 implementation by DA; pending operator evidence / ITRGA review |
| Date | 2026-07-18 |
| Unit | W7-U02 — Operator Workspace Customization |
| Platform version | 0.56.0 |
| Alembic head | 20260717_0034 |
| Builds on | W7-U01 institutional platform security/API foundation |

---

## Context

W7-U02 is the first Wave-7 feature unit. It adds per-operator workspace preferences for layout, visible modules, and theme settings. Preferences are presentation-only and must not introduce action/order/account/execution fields or cross-operator leakage.

---

## Decision

Add a persisted table:

```text
operator_workspace_preferences
```

via migration:

```text
20260717_0034_w7_u02_operator_workspace_preferences.py
```

Each row stores:

- `preference_id`
- `created_at`
- `updated_at`
- `operator_id -> operators.id`
- `workspace_key`
- `layout_config`
- `visible_modules`
- `theme_config`
- `research_status`
- `metadata`
- `audit_correlation_id`

Preferences are unique per operator/workspace key.

---

## API decision

Add authenticated, operator-scoped API endpoints:

```text
GET  /api/v1/institutional-platform/workspace-preferences
GET  /api/v1/institutional-platform/workspace-preferences/{preference_id}
POST /api/v1/institutional-platform/workspace-preferences
PUT  /api/v1/institutional-platform/workspace-preferences/{preference_id}
```

An operator can list/read/update only their own preferences. Cross-operator reads/updates return not found/denied and list endpoints do not leak other operators' rows.

---

## UI decision

Add protected frontend route:

```text
/workspace
```

The page lets the current operator edit presentation preferences only:

- workspace key;
- layout config JSON;
- visible modules;
- theme config JSON;
- metadata JSON.

The page renders a presentation-only disclaimer and has no action/order/account/execution controls.

---

## Inertness / no-secret controls

Preference payloads reject forbidden fields recursively:

```text
order_payload
order_intent
broker_account_id
account_id
position_id
live_position_id
execution_status
real_pnl
pnl
balance
margin
capital
gate_state
open_gate
allow_execution
```

They also reject secret markers recursively:

```text
access_token
refresh_token
jwt
password
secret
api_key
private_key
```

---

## Audit event

Each create/update appends audit events:

```text
operator_workspace_preference.created
operator_workspace_preference.updated
```

For created rows, no-orphan audit JOIN is mandatory.

---

## Deliberately not included

- No execution/order/account/broker field.
- No Gate field.
- No institutional feature beyond preferences.
- No plugin execution.
- No external LLM/API.
- No new dependency.
- No live broker/order/account path.

---

**End of ADR-065**
