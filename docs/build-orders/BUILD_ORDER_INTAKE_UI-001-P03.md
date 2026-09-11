# BUILD ORDER INTAKE — UI-001-P03

## Panel Infrastructure & Layout Manager

| Field | Value |
|---|---|
| Build Order | `docs/build-orders/BUILD_ORDER_UI-001-P03.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-001-P02.md` — APPROVED WITH OBSERVATIONS |
| Programme | Institutional UI Transformation |
| Workstream | UI-001 — Institutional Workspace Shell |
| Phase | P03 |
| Platform baseline | v0.62.0 |
| Alembic head | `20260717_0037` |
| Frontend baseline | 23 files / 80 tests |
| Governance Gate | CLOSED |
| DA decision | Accepted for implementation under one-phase scope |

## Authorized scope

Implement P03 panel infrastructure only:

- canonical Panel Registration Contract;
- Panel Registry for existing shell context/activity panels;
- deterministic Docking Engine primitives;
- Layout Manager with serialize/restore/resize and in-memory/session seam;
- PanelHost renderer for registered panels in Regions D/E;
- Shell Event Bus seam for shell/panel coordination;
- responsive/focusable panel infrastructure;
- tests and operator evidence.

## Explicit non-scope

Not authorized and not implemented:

- backend business logic changes;
- API/schema/Alembic changes;
- persistence to `operator_workspace_preferences` or any backend table;
- new table or migration;
- full P04 database persistence;
- P05 overlay/notification three-layer split;
- full command palette behavior;
- legacy P06 cleanup;
- new business panel/capability;
- execution/order/broker/account/Gate controls;
- new dependency.

## Version posture

The platform remains v0.62.0 during P03 because this phase is UI-only and the Build Order prohibits backend application changes. The implementation is identified as `UI-001-P03` pending ITRGA determination on any UI-phase versioning convention.

---

**End of BUILD_ORDER_INTAKE_UI-001-P03**
