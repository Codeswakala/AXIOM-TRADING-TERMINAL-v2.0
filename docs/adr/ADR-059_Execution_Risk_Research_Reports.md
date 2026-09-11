# ADR-059 — Execution Risk Research Reports

| Field | Value |
|---|---|
| Status | Accepted for W6-U04 implementation by DA; pending operator evidence / ITRGA review |
| Date | 2026-07-17 |
| Unit | W6-U04 — Execution Risk Research Reports |
| Platform version | 0.50.0 |
| Alembic head | 20260717_0031 |
| Builds on | W6-U02 simulated execution runs/fills and W6-U03 simulated paper ledger |

---

## Context

W6-U04 implements the roadmap's risk engine component under the constitutional interpretation accepted in the Wave-6 design plan: advisory research only over simulated/hypothetical artifacts. The central risks are that a risk report could actuate sizing, link to account/capital/margin, or present statistical metrics as economic success.

---

## Decision

Add one persisted simulated execution-risk research report table:

```text
execution_risk_research_reports
```

via migration:

```text
20260717_0031_w6_u04_execution_risk_reports.py
```

The report stores:

- `simulation_mode = SIMULATED`
- `input_artifact_ids`
- `simulated_request_summary`
- structured `risk_metrics`
- `uncertainty`
- `limitations`
- separate `economic_usefulness`
- `research_status = research_only`
- `simulation_disclaimer`
- `audit_correlation_id`

No `operator_id` field is added in W6-U04, so no R6-2 operator join is triggered for this table.

---

## Statistical/economic separation

`risk_metrics` are structured simulated research metrics only. `economic_usefulness` is a separate field and defaults to:

```text
verdict = not_assessed
```

The report does not assert economic success, real P&L, guaranteed returns, account suitability, or actuating sizing.

---

## Audit event

Each report appends:

```text
action = execution_risk_research_report.created
resource_type = execution_risk_research_report
resource_id = execution_risk_research_reports.report_id
correlation_id = execution_risk_research_reports.audit_correlation_id
```

No-orphan audit join is mandatory.

---

## API decision

Add authenticated API endpoints:

```text
POST /api/v1/execution-research/execution-risk-reports
GET  /api/v1/execution-research/execution-risk-reports
GET  /api/v1/execution-research/execution-risk-reports/{report_id}
```

The create endpoint writes only the report row and audit event. It does not call any broker seam, live execution path, account path, order path, or Gate mutation.

No UI is added in W6-U04.

---

## Forbidden fields

The report table does not contain:

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
recommended_size
sizing_directive
execution_status_as_live
```

---

## Consequences

### Positive

- Adds structured simulated execution-risk research reporting.
- Keeps uncertainty and limitations mandatory.
- Separates statistical risk metrics from economic usefulness.
- Preserves Gate CLOSED and no-actuation posture.

### Deliberately not included

- No UI.
- No sizing engine.
- No account/capital/margin linkage.
- No broker SDK or credentials.
- No live venue endpoint.
- No order routing.
- No real P&L claim.
- No analytics/performance comparison beyond this report.
- No W6-U05+ feature.

---

**End of ADR-059**
