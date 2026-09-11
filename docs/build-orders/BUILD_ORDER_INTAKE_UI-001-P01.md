# BUILD ORDER INTAKE — UI-001-P01

## Institutional Workspace Shell — Skeleton, Workspace Registry, Region Scaffolding & Routing/State Seam

| Field | Value |
|---|---|
| Build Order | `docs/build-orders/BUILD_ORDER_UI-001-P01.md` |
| Programme | Institutional UI Transformation |
| Workstream | UI-001 — Institutional Workspace Shell |
| Phase | P01 |
| Platform baseline | v0.62.0 |
| Alembic head | `20260717_0037` |
| Baseline | backend 413 passed · frontend 21 files / 67 tests |
| Governance Gate | CLOSED |
| DA decision | Accepted for implementation under one-phase scope |

## Authorized scope

Implement P01 presentation infrastructure only:

- `InstitutionalWorkspaceShell` under `AuthProvider → ProtectedRoute`;
- Regions A–F scaffolded: Global Header, Navigation Dock, Primary Workspace, Context Panel, Activity Dock, Overlay Layer;
- canonical `WorkspaceRegistry` for all current protected routes;
- `WorkspaceHost` routing/state seam mounting existing page content;
- foundational semantic design tokens and typography tokens;
- P01 accessibility foundation: ARIA landmarks, keyboard focus transitions, logged-out block;
- replace active legacy `TerminalLayout` frame with the institutional shell.

## Explicit non-scope

Not authorized and not implemented:

- backend business logic changes;
- API contract changes;
- database/schema/Alembic changes;
- governance behavior changes;
- ML workflow changes;
- new trading/research capability;
- execution/order/broker/account/Gate controls;
- external AI/LLM;
- layout persistence to database;
- full navigation/docking/palette behavior beyond P01 scaffold;
- new dependency.

## Version posture

The platform remains v0.62.0 during P01 because this phase is UI-only and the Build Order prohibits backend application changes. The implementation is identified as `UI-001-P01` pending ITRGA determination on any UI-phase versioning convention.

---

**End of BUILD_ORDER_INTAKE_UI-001-P01**
