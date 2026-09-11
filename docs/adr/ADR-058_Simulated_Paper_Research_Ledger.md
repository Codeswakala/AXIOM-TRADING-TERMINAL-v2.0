# ADR-058 — Simulated Paper Research Ledger

| Field | Value |
|---|---|
| Status | Accepted for W6-U03 implementation by DA; pending operator evidence / ITRGA review |
| Date | 2026-07-17 |
| Unit | W6-U03 — Simulated Paper Research Ledger |
| Platform version | 0.49.0 |
| Alembic head | 20260717_0030 |
| Builds on | W6-U02 simulated execution runs and fill events |

---

## Context

W6-U02 created `SIMULATED` execution runs and deterministic simulated fill events. W6-U03 adds a simulated paper research ledger over those artifacts only. The central risk is that `simulated_return_estimate` could be mistaken for real P&L, so every ledger entry must remain explicitly simulated, research-only, uncertainty-bearing, and non-actuating.

---

## Decision

Add one persisted research artifact table:

```text
simulated_paper_ledger_entries
```

via migration:

```text
20260717_0030_w6_u03_simulated_paper_ledger.py
```

Each ledger entry references existing simulated artifacts only:

```text
simulated_paper_ledger_entries.run_id -> simulated_execution_runs.run_id
simulated_paper_ledger_entries.simulated_fill_id -> simulated_fill_events.simulated_fill_id
simulated_paper_ledger_entries.operator_id -> operators.id
```

No broker/account/position/order linkage is present.

Add service/API support:

```text
SimulatedPaperLedgerService
POST /api/v1/execution-research/simulated-ledger-entries
GET  /api/v1/execution-research/simulated-ledger-entries
GET  /api/v1/execution-research/simulated-ledger-entries/{ledger_entry_id}
```

The create endpoint writes only simulated ledger persistence and audit rows. No UI is added in W6-U03.

---

## Field semantics

| Field | Meaning |
|---|---|
| `simulated_units` | Dimensionless research amount inherited from simulated fill; not order quantity. |
| `simulated_entry_value` | Simulated model value from the fill event; not broker execution value. |
| `simulated_exit_value` | Operator/research supplied simulated comparison value; not broker exit. |
| `simulated_return_estimate` | Research estimate computed from simulated entry/exit values; not realized P&L. |
| `uncertainty` | Mandatory uncertainty band for the return estimate. |
| `limitations` | Must include simulated/research-only and not-real-profit-loss limitations. |

---

## Audit events

Each ledger entry appends:

```text
action = simulated_paper_ledger_entry.created
resource_type = simulated_paper_ledger_entry
resource_id = simulated_paper_ledger_entries.ledger_entry_id
correlation_id = simulated_paper_ledger_entries.audit_correlation_id
```

No-orphan audit joins are mandatory.

---

## Forbidden fields

The ledger table does not contain:

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
execution_status_as_live
```

---

## Consequences

### Positive

- Establishes a simulated paper research ledger over simulated fills only.
- Keeps return estimates uncertainty-bearing and research-framed.
- Provides audit, operator, run, and fill lineage proof.
- Maintains Gate CLOSED and no-live-broker posture.

### Deliberately not included

- No UI.
- No real P&L.
- No broker/account/position ledger.
- No execution/order path.
- No broker SDK or credentials.
- No analytics/performance report.
- No W6-U04+ feature.

---

**End of ADR-058**
