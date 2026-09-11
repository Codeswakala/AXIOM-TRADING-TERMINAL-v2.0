# BUILD ORDER INTAKE — W6-U03

| Field | Value |
|---|---|
| Build Order | W6-U03 — Simulated Paper Research Ledger |
| Received by DA | 2026-07-17 |
| Source artifact | `docs/build-orders/BUILD_ORDER_W6-U03.md` |
| Prerequisite verdict | `docs/build-orders/ITRGA_REVIEW_W6-U02.md` — W6-U02 APPROVED CLEAN, platform v0.48.0 |
| DA disposition | ACCEPTED FOR IMPLEMENTATION |
| Target platform version | 0.49.0 |
| Alembic target | `20260717_0030` |
| Governance Gate | **CLOSED** |

## Authorized scope

- Add `simulated_paper_ledger_entries` migration `20260717_0030`.
- Add simulated paper research ledger service and API create/list/detail.
- Ledger entries reference existing simulated execution runs and simulated fill events only.
- Persist and audit simulated ledger artifacts with `SIMULATED` marker, disclaimer, uncertainty, limitations, and no real P&L framing.
- Prove no-orphan audit, operator attribution, and run/fill lineage joins.
- No UI, no broker SDK, no dependency change, no live broker/order/account path.

## Binding constraints acknowledged

- Gate remains CLOSED.
- `operator_id -> operators.id`, research attribution only.
- `simulated_return_estimate` is a research estimate with uncertainty, not realized P&L.
- `simulated_units` remains dimensionless.
- No real account/broker/position/capital/margin/P&L fields.
- No UI in W6-U03.
- DA does not self-approve and does not start W6-U04 without ITRGA approval plus a new Build Order.

