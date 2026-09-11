# ADR-056 — Execution Research Safety Foundation

| Field | Value |
|---|---|
| Status | Accepted for W6-U01 implementation by DA; pending operator evidence / ITRGA review |
| Date | 2026-07-17 |
| Unit | W6-U01 — Execution Research Safety Foundation: Gate-Closed Simulation Envelope |
| Platform version | 0.47.0 |
| Builds on | Wave-6 design review accepted with R6-1…R6-8 |

---

## Context

Wave 6 is Execution Research, the highest-risk wave. ITRGA accepted the Wave-6 design plan with binding refinements. W6-U01 is the safety-foundation unit: prove the lock before the door.

W6-U01 must add no table, no migration, no UI, no dependency, no broker SDK, no simulated run/fill/ledger feature, and no live execution path. The Constitutional Governance Gate remains CLOSED.

---

## Decision

Add an `execution_research` bounded context skeleton containing simulation-only constants and a minimal immutable safety contract.

Core constants:

```text
SIMULATION_MODE = SIMULATED
RESEARCH_STATUS = research_only
EXECUTION_RESEARCH_POLICY_VERSION = w6-u01.gate_closed_simulation_envelope.v1
SIMULATED_EXECUTION_RESEARCH_DISCLAIMER = SIMULATED execution research only. Not a live order, not financial advice, not real P&L. AXIOM does not act. Governance Gate CLOSED.
```

Harden the existing `NullBroker` refusal seam so, when an `audit_session` is supplied, closed-Gate connect and execute refusals append audit rows to the existing `audit_events` table.

No `audit_events.reason_code` column is added. Per `BUILD_ORDER_W6-U01_AMENDMENT_1.md`, refusal reason codes are stored in the existing `audit_events.details` JSON field:

```text
details.reason_code = GATE_CLOSED_CONNECT_REFUSED
details.reason_code = GATE_CLOSED_EXECUTE_REFUSED
```

Stable audit discriminators:

```text
action = broker.connect.refused
resource_type = broker_integration
```

```text
action = broker.execute.refused
resource_type = broker_integration
```

Required audit details include:

```json
{
  "reason_code": "GATE_CLOSED_CONNECT_REFUSED",
  "gate_state": "CLOSED",
  "simulation_only": true,
  "adapter_name": "null-broker",
  "live_broker_connection_attempted": false,
  "live_order_attempted": false
}
```

and equivalent details for `GATE_CLOSED_EXECUTE_REFUSED`.

---

## Consequences

### Positive

- W6 starts with a provable closed-Gate safety envelope.
- Refusal evidence is auditable without schema changes.
- Broker-specific logic remains contained in External Integration.
- The execution research context contains no live execution path, no broker client, no secrets, and no network behavior.

### Deliberately not included

- No new table.
- No migration.
- No UI.
- No simulated execution runs/fills.
- No ledger.
- No analytics.
- No live broker adapter.
- No broker SDK or credentials.
- No execution/order/account/position path.
- No Gate opening.
- No external LLM/API.

---

## Validation expectations

Named tests must pass:

```text
test_governance_gate_remains_closed_for_wave6
test_null_or_simulated_broker_refuses_connect_when_gate_closed
test_null_or_simulated_broker_refuses_execute_when_gate_closed
test_broker_logic_contained_in_external_integration
test_execution_research_has_no_live_broker_sdk_or_credentials
test_wave6_bright_line_grep_no_live_execution_path
```

Standing broker tests must remain green.

Operator evidence must include raw PostgreSQL query over `audit_events.details->>'reason_code'`, showing at least one `GATE_CLOSED_CONNECT_REFUSED` and one `GATE_CLOSED_EXECUTE_REFUSED` row.

---

**End of ADR-056**
