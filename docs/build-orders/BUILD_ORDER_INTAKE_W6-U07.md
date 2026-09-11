# BUILD ORDER INTAKE — W6-U07

| Field | Value |
|---|---|
| Build Order | W6-U07 — Execution Research Workspace UI |
| Received by DA | 2026-07-17 |
| Source artifact | `docs/build-orders/BUILD_ORDER_W6-U07.md` |
| Prerequisite review | `docs/build-orders/ITRGA_REVIEW_W6-U06.md` — W6-U06 APPROVED CLEAN, platform v0.52.0 |
| DA disposition | ACCEPTED FOR IMPLEMENTATION |
| Target platform version | 0.53.0 |
| Alembic posture | No migration; expected head remains `20260717_0033` |
| Governance Gate | **CLOSED** |

## Authorized scope

- Add protected frontend route `/execution-research`.
- Display server-persisted simulated execution research artifacts from existing W6 read APIs.
- Show mandatory SIMULATED / not-live disclaimer and SIMULATED labels.
- Prove no execution/actuation controls and no client-side authoritative recomputation.
- No backend write path, no table, no migration, no dependency.

## Binding constraints acknowledged

- UI is display-only by default.
- No UI-triggered simulation write is implemented.
- No buy/sell/submit/execute/go-live/connect-broker/account controls.
- No client-side authoritative analytics recomputation.
- Browser evidence is mandatory.
- Gate remains CLOSED.
- DA does not self-approve and does not start W6-U08 without ITRGA approval plus a new Build Order.

