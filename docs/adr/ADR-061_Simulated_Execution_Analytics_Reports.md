# ADR-061 — Simulated Execution Analytics & Performance Comparison Reports

| Field | Value |
|---|---|
| Status | Accepted for W6-U06 implementation by DA; pending operator evidence / ITRGA review |
| Date | 2026-07-17 |
| Unit | W6-U06 — Simulated Execution Analytics & Performance Comparison |
| Platform version | 0.52.0 |
| Alembic head | 20260717_0033 |
| Builds on | W6-U02 simulated fills, W6-U03 ledger, W6-U05 experiments |

---

## Context

W6-U06 implements simulated execution analytics and performance comparison over existing simulated artifacts. R6-7 is central: analytics must include uncertainty, sample count, full declared scope, deterministic report hash, no cherry-picking, and separation between statistical metrics and economic usefulness.

---

## Decision

Add one persisted simulated analytics report table:

```text
simulated_execution_analytics_reports
```

via migration:

```text
20260717_0033_w6_u06_simulated_execution_analytics_reports.py
```

The report stores:

- `simulation_mode = SIMULATED`
- `analytics_type`
- `included_scope`
- `sample_count`
- structured `metrics`
- `uncertainty`
- `limitations`
- separate `economic_usefulness`
- deterministic `report_hash`
- `source_artifact_ids`
- `research_status = research_only`
- `simulation_disclaimer`
- `audit_correlation_id`

No `operator_id` field is added in W6-U06, so no R6-2 operator join is triggered for this table.

---

## Full-scope / no-cherry-picking control

The service requires a declared `source_artifact_ids` set. Each id must resolve to one of:

- `simulated_fill_events`
- `simulated_paper_ledger_entries`
- `execution_research_experiments`

The persisted `included_scope` records:

```text
declared_source_artifact_ids
analyzed_source_artifact_ids
simulated_fill_ids
simulated_ledger_entry_ids
execution_experiment_ids
comparison_groups
full_scope_included = true
```

The service refuses unresolved ids and raises if analyzed ids do not exactly equal the declared source ids.

---

## Uncertainty and economics

Every metric has a corresponding uncertainty entry. If a metric has insufficient samples, the uncertainty record explicitly states `insufficient_sample_limitation` instead of fabricating a confidence interval.

`risk_metrics`/`metrics` remain statistical. `economic_usefulness` is a separate field with:

```text
verdict = not_assessed
```

No real P&L, guaranteed return, live-execution suitability, or economic success claim is asserted.

---

## Report hash

`report_hash` is SHA-256 over canonical JSON containing:

```text
analytics_type
included_scope
source_artifact_ids
method_version
```

This makes the report hash deterministic and recomputable from the persisted scope and inputs.

---

## Audit event

Each analytics report appends:

```text
action = simulated_execution_analytics_report.created
resource_type = simulated_execution_analytics_report
resource_id = simulated_execution_analytics_reports.report_id
correlation_id = simulated_execution_analytics_reports.audit_correlation_id
```

No-orphan audit join is mandatory.

---

## Forbidden fields

The analytics report table does not contain:

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
guaranteed_return
position_size
order_size
execution_status_as_live
```

---

## Consequences

### Positive

- Adds simulated analytics/performance comparison over already-governed simulated artifacts.
- Makes no-cherry-picking falsifiable through persisted scope equality.
- Makes uncertainty mandatory per metric.
- Keeps economic usefulness separate and not assessed.
- Preserves Gate CLOSED and no-live-broker posture.

### Deliberately not included

- No UI.
- No live broker or live account linkage.
- No real P&L.
- No order or sizing directive.
- No broker SDK or credentials.
- No Gate opening.
- No W6-U07 UI feature.

---

**End of ADR-061**
