# BUILD ORDER INTAKE — W6-U01

| Field | Value |
|---|---|
| Build Order | W6-U01 — Execution Research Safety Foundation: Gate-Closed Simulation Envelope |
| Amendment | `docs/build-orders/BUILD_ORDER_W6-U01_AMENDMENT_1.md` — Option A authorized; refusal reason codes stored in `audit_events.details` JSON |
| Received by DA | 2026-07-17 |
| Source artifacts | `docs/build-orders/BUILD_ORDER_W6-U01.md`; `docs/build-orders/BUILD_ORDER_W6-U01_AMENDMENT_1.md` |
| Prerequisite review | `docs/build-orders/ITRGA_REVIEW_WAVE6_DESIGN_PLAN.md` — Wave 6 design accepted with R6-1…R6-8 |
| DA disposition | ACCEPTED FOR IMPLEMENTATION |
| Target platform version | 0.47.0 |
| Alembic posture | No migration; expected head remains `20260717_0027` |

## Authorized scope

- Add backend `execution_research` skeleton with simulation-only constants/contracts.
- Harden External Integration broker refusal seam so closed-Gate connect/execute refusals append audit rows using `audit_events.details->>'reason_code'`.
- Add named W6-U01 safety tests and evidence commands.
- No schema, no migration, no UI, no broker SDK, no dependency change, no simulated run/fill/ledger feature.

## Amendment 1 interpretation

W6-U01 refusal audit evidence shall use existing `audit_events.details` JSON:

```sql
SELECT details->>'reason_code' AS reason_code, COUNT(*) AS refusal_count
FROM audit_events
WHERE details->>'reason_code' IN (
  'GATE_CLOSED_CONNECT_REFUSED',
  'GATE_CLOSED_EXECUTE_REFUSED'
)
GROUP BY details->>'reason_code'
ORDER BY reason_code;
```

No top-level `audit_events.reason_code` column will be added.

## Binding constraints acknowledged

- Gate remains CLOSED.
- No live broker path by construction.
- Broker logic containment under External Integration.
- No new table/migration.
- No UI.
- No dependency change.
- No Wave-6 feature beyond safety envelope.
- DA does not self-approve, self-open the Gate, or proceed to W6-U02 without ITRGA approval and a new Build Order.

