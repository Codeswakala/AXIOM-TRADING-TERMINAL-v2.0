# ADR-060 — Trade Replay and Execution Experiment Pre-Registration

| Field | Value |
|---|---|
| Status | Accepted for W6-U05 implementation by DA; pending operator evidence / ITRGA review |
| Date | 2026-07-17 |
| Unit | W6-U05 — Trade Replay & Execution Experiment Pre-Registration |
| Platform version | 0.51.0 |
| Alembic head | 20260717_0032 |
| Builds on | W6-U02 simulated runs/fills, W6-U03 ledger, W6-U04 risk reports |

---

## Context

W6-U05 implements trade replay and execution experimentation as simulation-only research. The central requirements are no-look-ahead replay and immutable pre-registration. No candle after the declared `as_of_time` may enter a replay, and the experiment scope must not be narrowed after results.

---

## Decision

Add one persisted table:

```text
execution_research_experiments
```

via migration:

```text
20260717_0032_w6_u05_execution_research_experiments.py
```

Each experiment stores:

- `simulation_mode = SIMULATED`
- `operator_id -> operators.id`
- immutable `pre_registration_plan`
- deterministic `plan_hash`
- `as_of_time` and `as_of_window`
- `replay_input_lineage`
- `included_scope_summary`
- `uncertainty`
- `limitations`
- `research_status = research_only`
- `simulation_disclaimer`
- `audit_correlation_id`

---

## Pre-registration hash

`plan_hash` is SHA-256 over canonical JSON of `pre_registration_plan` using sorted keys and stable separators.

The service exposes no update method. API has no PUT/PATCH endpoint. Mutation attempts are expected to return 404/405.

---

## No-look-ahead replay

Replay inputs are selected using:

```text
Candle.open_time >= as_of_start
Candle.open_time <= as_of_time
```

The persisted `replay_input_lineage` stores included candle ids/open times and `excluded_future_candle_count`.

Operator evidence must include a bounding query and a negative check proving no included candle has `open_time > as_of_time`.

---

## Audit event

Each experiment appends:

```text
action = execution_research_experiment.created
resource_type = execution_research_experiment
resource_id = execution_research_experiments.experiment_id
correlation_id = execution_research_experiments.audit_correlation_id
```

---

## Forbidden fields

The experiment table does not contain:

```text
account_balance
real_account_balance
margin
capital
real_capital
broker_account_id
account_id
live_position_id
position_id
broker_endpoint
broker_credentials
order_payload
order_intent
real_pnl
pnl
realized_pnl
position_size
order_size
live_feed_url
execution_status_as_live
```

---

## Consequences

### Positive

- Adds immutable pre-registration and as-of bounded replay evidence.
- Makes no-look-ahead falsifiable through persisted lineage.
- Preserves operator attribution to AXIOM `operators` only.
- Preserves Gate CLOSED and no-live-feed/no-broker posture.

### Deliberately not included

- No UI.
- No live feed.
- No broker SDK or credentials.
- No live venue endpoint.
- No real order routing.
- No real account/position/balance/margin/capital state.
- No real P&L.
- No Gate opening.
- No W6-U06 analytics/performance comparison.

---

**End of ADR-060**
