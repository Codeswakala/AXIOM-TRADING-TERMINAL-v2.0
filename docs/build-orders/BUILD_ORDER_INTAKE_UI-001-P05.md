# BUILD ORDER INTAKE — UI-001-P05

## Overlay Layer, Notification Service, Command Palette, Accessibility & Token Hardening

| Field | Value |
|---|---|
| Build Order | `docs/build-orders/BUILD_ORDER_UI-001-P05.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-001-P04.md` — APPROVED WITH OBSERVATIONS |
| Programme | Institutional UI Transformation |
| Workstream | UI-001 — Institutional Workspace Shell |
| Phase | P05 |
| Platform baseline | v0.62.0 |
| Alembic head | `20260717_0037` |
| Frontend baseline | 25 files / 89 tests |
| Governance Gate | CLOSED |
| DA decision | Accepted for implementation under one-phase scope |

## Authorized scope

Implement P05 overlay/accessibility/token hardening only:

- Region-F three-layer overlay family: Overlay, Global Dialog, Notification;
- centralized notification service with six types;
- full command palette shell commands limited to navigation/UI toggles;
- focus trap, ESC close, focus return, ARIA roles;
- reduced motion and light theme token seam;
- complete token categories and semantic roles;
- no-hardcoded-color proof in workstation source outside token definitions;
- tests and operator evidence pack.

## Explicit non-scope

Not authorized and not implemented:

- backend business logic changes;
- API/schema/Alembic changes;
- new table, endpoint, migration, or dependency;
- execution/order/broker/account/Gate controls;
- business/trading/research commands;
- P06 legacy `TerminalLayout` retirement;
- production certification.

---

**End of BUILD_ORDER_INTAKE_UI-001-P05**
