# BUILD ORDER INTAKE — W6-U02

| Field | Value |
|---|---|
| Build Order | W6-U02 — Simulated Execution Runs & Fill Events |
| Amendment | `docs/build-orders/BUILD_ORDER_W6-U02_AMENDMENT_1.md` — R6-2 identity target is `operators`, not `users` |
| Received by DA | 2026-07-17 |
| Source artifacts | `docs/build-orders/BUILD_ORDER_W6-U02.md`; `docs/build-orders/BUILD_ORDER_W6-U02_AMENDMENT_1.md` |
| Prerequisite verdict | `docs/build-orders/ITRGA_VERDICT_W6-U01_FINAL.md` — W6-U01 APPROVED, platform v0.47.0 |
| DA disposition | ACCEPTED FOR IMPLEMENTATION |
| Target platform version | 0.48.0 |
| Alembic target | `20260717_0029` |
| Governance Gate | **CLOSED** |

## Authorized scope

- Add `simulated_execution_runs` migration `20260717_0028`.
- Add `simulated_fill_events` migration `20260717_0029`.
- Add deterministic simulated fill model and committing service.
- Add authenticated create + read-only list/detail/fill APIs for simulated research artifacts.
- Persist and audit simulated run/fill artifacts with `SIMULATED` marker, disclaimer, immutable policy/model versions, and no real broker/account/order fields.
- Prove no-orphan audit joins for both tables and no-orphan `operator_id` join against `operators`.
- No UI, no broker SDK, no dependency change, no live broker/order/account path.

## Amendment 1 interpretation

Every W6-U02 reference to a `users` identity table is read as AXIOM's existing `operators` table.

Schema relationship:

```text
simulated_execution_runs.operator_id -> operators.id
```

Identity evidence:

```sql
SELECT COUNT(*) AS orphan_operator_count
FROM simulated_execution_runs ser
LEFT JOIN operators o ON o.id = ser.operator_id
WHERE o.id IS NULL;
```

No `users` table, alias, or view will be added.

## Binding constraints acknowledged

- Gate remains CLOSED.
- New artifacts are simulation/research only.
- `simulated_units` is dimensionless and not an order quantity.
- `simulated_fill_price` is a model output, not a broker fill.
- No real P&L / guaranteed-return / live-fill framing.
- `simulation_policy_version` and `fill_model_version` are immutable per record and included in raw SELECT + audit.
- No UI in W6-U02.
- DA does not self-approve and does not start W6-U03 without ITRGA approval plus a new Build Order.

