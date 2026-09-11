# BUILD ORDER INTAKE — UI-001-P04

## Workspace Persistence via `operator_workspace_preferences`

| Field | Value |
|---|---|
| Build Order | `docs/build-orders/BUILD_ORDER_UI-001-P04.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-001-P03.md` — APPROVED WITH OBSERVATIONS |
| Programme | Institutional UI Transformation |
| Workstream | UI-001 — Institutional Workspace Shell |
| Phase | P04 |
| Platform baseline | v0.62.0 |
| Alembic head | `20260717_0037` |
| Frontend baseline | 24 files / 85 tests |
| Governance Gate | CLOSED |
| DA decision | Accepted for implementation under one-phase scope |

## Authorized scope

Implement P04 workspace persistence only:

- shell preference serialization under workspace key `institutional-shell-v1`;
- durable operator-scoped persistence through existing W7-U02 `operator_workspace_preferences` API/repository;
- restore last route, navigation collapsed state, and panel layout after login;
- safe default behavior for operators with no shell preference;
- operator-scoped isolation proof;
- persistence-capture evidence on the existing W7-U02 table.

## Explicit non-scope

Not authorized and not implemented:

- new table, migration, schema column, or endpoint;
- backend business logic beyond existing W7-U02 preference path;
- full P05 overlay/notification/command-palette completion;
- P06 legacy cleanup;
- new business/trading/research capability;
- execution/order/broker/account/Gate controls;
- new dependency.

---

**End of BUILD_ORDER_INTAKE_UI-001-P04**
