# BUILD ORDER INTAKE — W6-U05

| Field | Value |
|---|---|
| Build Order | W6-U05 — Trade Replay & Execution Experiment Pre-Registration |
| Received by DA | 2026-07-17 |
| Source artifact | `docs/build-orders/BUILD_ORDER_W6-U05.md` |
| Prerequisite verdict | `docs/build-orders/ITRGA_VERDICT_W6-U04_FINAL.md` — W6-U04 APPROVED, platform v0.50.0 |
| DA disposition | ACCEPTED FOR IMPLEMENTATION |
| Target platform version | 0.51.0 |
| Alembic target | `20260717_0032` |
| Governance Gate | **CLOSED** |

## Authorized scope

- Add `execution_research_experiments` migration `20260717_0032`.
- Add immutable pre-registration plan hash over declared replay scope.
- Add replay execution over frozen/as-of bounded inputs only.
- Add authenticated create/list/detail API.
- Persist and audit simulated experiment/replay records with `SIMULATED` marker, uncertainty, limitations, and no real P&L framing.
- Prove no-look-ahead using as-of/future-row-exclusion pattern.
- No UI, no broker SDK, no dependency change, no live feed, no live broker/order/account path.

## Binding constraints acknowledged

- Gate remains CLOSED.
- `operator_id -> operators.id`, research attribution only.
- No candle with `open_time > as_of_time` may enter replay lineage.
- `plan_hash` is immutable and recomputable from `pre_registration_plan`.
- Executed included scope must equal declared pre-registration scope.
- No live feed/broker/order/account/Gate seam.
- No UI in W6-U05.
- DA does not self-approve and does not start W6-U06 without ITRGA approval plus a new Build Order.

