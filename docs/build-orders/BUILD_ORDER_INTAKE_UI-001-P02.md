# BUILD ORDER INTAKE — UI-001-P02

## Navigation Dock & Workflow Routing

| Field | Value |
|---|---|
| Build Order | `docs/build-orders/BUILD_ORDER_UI-001-P02.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-001-P01.md` — APPROVED WITH OBSERVATIONS |
| Programme | Institutional UI Transformation |
| Workstream | UI-001 — Institutional Workspace Shell |
| Phase | P02 |
| Platform baseline | v0.62.0 |
| Alembic head | `20260717_0037` |
| Frontend baseline | 22 files / 76 tests |
| Governance Gate | CLOSED |
| DA decision | Accepted for implementation under one-phase scope |

## Authorized scope

Implement P02 navigation infrastructure only:

- widen `WorkspaceRegistry` to 14-field canonical Workspace Registration Contract plus `requiresAuth` and `noActuation` guards;
- add registry-driven navigation generator;
- replace placeholder dock rendering with generated Navigation Dock;
- add expand/collapse, icons, active indicators, feature-flag and RBAC filtering seam;
- add deterministic workspace activation telemetry hook;
- preserve current route mounting and shell framing;
- close OBS-P01-1 and OBS-P01-2 in evidence.

## Explicit non-scope

Not authorized and not implemented:

- backend business logic changes;
- API/schema/Alembic changes;
- governance/ML changes;
- new trading/research capability;
- execution/order/broker/account/Gate controls;
- full panel docking/resize/layout manager;
- persistence to `operator_workspace_preferences`;
- Region-F three-layer overlay completion;
- full command palette behavior;
- new dependency.

## Version posture

The platform remains v0.62.0 during P02 because this phase is UI-only and the Build Order prohibits backend application changes. The implementation is identified as `UI-001-P02` pending ITRGA determination on any UI-phase versioning convention.

---

**End of BUILD_ORDER_INTAKE_UI-001-P02**
