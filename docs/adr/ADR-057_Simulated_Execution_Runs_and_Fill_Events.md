# ADR-057 — Simulated Execution Runs and Fill Events

| Field | Value |
|---|---|
| Status | Accepted for W6-U02 implementation by DA; pending operator evidence / ITRGA review |
| Date | 2026-07-17 |
| Unit | W6-U02 — Simulated Execution Runs & Fill Events |
| Platform version | 0.48.0 |
| Alembic head | 20260717_0029 |
| Builds on | W6-U01 Gate-Closed Simulation Envelope |

---

## Context

W6-U01 proved the closed-Gate safety envelope. W6-U02 is the first Wave-6 persisted-artifact unit. It must create only `SIMULATED`, research-only artifacts and must not introduce live broker, real order, real account, real position, capital/margin, real P&L, UI, or Gate-opening paths.

ITRGA Amendment 1 clarified R6-2: `operator_id` references AXIOM's existing `operators` table, not a non-existent `users` table.

---

## Decision

Add two persisted research artifact tables:

```text
simulated_execution_runs
simulated_fill_events
```

with migrations:

```text
20260717_0028_w6_u02_simulated_execution_runs.py
20260717_0029_w6_u02_simulated_fill_events.py
```

`simulated_execution_runs.operator_id` is a research-attribution foreign key to:

```text
operators.id
```

`simulated_fill_events.run_id` is a lineage foreign key to:

```text
simulated_execution_runs.run_id
```

Add a deterministic fill model:

```text
deterministic_mid_close_slippage
w6-u02.fill_model.v1
```

The fill model reads historical/replayed candles and produces deterministic model outputs. `simulated_units` is dimensionless and not an order quantity. `simulated_fill_price` is a model output and not a broker fill.

---

## Audit events

Each run appends:

```text
action = simulated_execution_run.created
resource_type = simulated_execution_run
resource_id = simulated_execution_runs.run_id
correlation_id = simulated_execution_runs.audit_correlation_id
```

Each fill appends:

```text
action = simulated_fill_event.created
resource_type = simulated_fill_event
resource_id = simulated_fill_events.simulated_fill_id
correlation_id = simulated_fill_events.audit_correlation_id
```

No-orphan audit joins are mandatory for both tables.

---

## API decision

Add authenticated API endpoints:

```text
POST /api/v1/execution-research/simulated-runs
GET  /api/v1/execution-research/simulated-runs
GET  /api/v1/execution-research/simulated-runs/{run_id}
GET  /api/v1/execution-research/simulated-runs/{run_id}/fills
GET  /api/v1/execution-research/simulated-fills/{fill_id}
```

The create endpoint writes only simulated research artifacts. It does not call any broker seam, live execution path, account path, or Gate mutation.

No UI is added in W6-U02.

---

## Forbidden fields

The new tables do not contain:

```text
broker_account_id
account_id
real_account_balance
margin
capital
live_position_id
broker_endpoint
broker_credentials
order_payload
order_intent
execution_status_as_live
real_pnl
pnl
position_id
```

---

## Consequences

### Positive

- Establishes first persisted Wave-6 simulated research artifacts.
- Preserves Gate CLOSED posture.
- Provides deterministic, reproducible fill-model output.
- Provides audit and operator-attribution evidence.

### Deliberately not included

- No UI.
- No broker SDK.
- No broker credentials.
- No live venue endpoint.
- No real order routing.
- No real account/position/balance/margin/capital state.
- No real P&L claim.
- No Gate opening.
- No W6-U03 ledger or later feature.

---

**End of ADR-057**
