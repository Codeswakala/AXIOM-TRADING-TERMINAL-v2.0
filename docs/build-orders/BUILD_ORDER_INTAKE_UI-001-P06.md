# BUILD ORDER INTAKE — UI-001-P06

## Legacy TerminalLayout Retirement · Migration Completion · UI-001 Completion Checkpoint

| Field | Value |
|---|---|
| Build Order | `docs/build-orders/BUILD_ORDER_UI-001-P06.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-001-P05.md` — APPROVED CLEAN |
| Programme | Institutional UI Transformation |
| Workstream | UI-001 — Institutional Workspace Shell |
| Phase | P06 — final UI-001 phase |
| Platform baseline | v0.62.0 |
| Alembic head | `20260717_0037` |
| Frontend baseline | 26 files / 94 tests |
| Governance Gate | CLOSED |
| DA decision | Accepted for implementation under one-phase scope |

## Authorized scope

Implement P06 closeout for UI-001 only:

- retire legacy `TerminalLayout` source;
- prove no reachable source path renders legacy frame;
- prove InstitutionalWorkspaceShell is the sole protected app frame;
- prove all current protected routes mount through `InstitutionalWorkspaceShell` / `WorkspaceHost`;
- update UI-001 completion evidence and delivery report;
- preserve all P01–P05 shell tests and platform regressions.

## Explicit non-scope

Not authorized and not implemented:

- new workspace/feature/business capability;
- backend business logic changes;
- API/schema/Alembic changes;
- new table/migration/dependency;
- execution/order/broker/account/Gate controls;
- production readiness certification;
- UI-002+ work.

## Version posture

The platform remains v0.62.0 during P06 because this phase is UI-only and the Build Order prohibits backend application changes. The implementation is identified as `UI-001-P06` pending ITRGA final UI-001 acceptance.

---

**End of BUILD_ORDER_INTAKE_UI-001-P06**
