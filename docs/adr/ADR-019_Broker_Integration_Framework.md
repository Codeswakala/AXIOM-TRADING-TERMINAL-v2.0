# ADR-019 — Broker Integration Framework and Closed Governance Gate

| Field | Value |
|-------|-------|
| ID | ADR-019 |
| Title | Broker-neutral adapter port with hard-closed Constitutional Governance Gate |
| Date | 2026-07-13 |
| Status | Accepted |
| Deciders | Development Authority under Build Order W1-U03 |
| Domain | External Integration / Governance / Broker Architecture |

---

## Context

Wave 1 roadmap includes an MT5 integration framework as part of Core Platform. The constitutional boundary is strict: Wave 1 may define the broker interoperability seam, but real broker connection, account login, live broker data, order placement, paper trading, execution simulation, and position management are not authorized until later governance, primarily Wave 6 execution research.

`05_SYSTEM_ARCHITECTURE.md` v2.0 requires broker-specific logic to remain inside the External Integration System and execution to stay behind the Constitutional Governance Gate.

## Decision

Implement a contract-only broker integration framework inside `backend/app/external_integration/broker`:

- `BrokerPort` protocol as the pure broker-neutral interface;
- strict boundary DTOs (`Instrument`, `BrokerAccount`, `BrokerQuote`, `OrderIntent`, `BrokerCapabilities`);
- typed errors (`BrokerDisabledError`, `BrokerNotConnectedError`, `GovernanceGateClosedError`);
- `NullBroker` disabled reference adapter implementing the full port with zero I/O;
- `ConstitutionalGovernanceGate` hard closed for broker connection and execution;
- observability metric increment and redacted/correlated warning log on refusal;
- DI seam through `BrokerIntegrationService`.

No real broker package is imported. No MT5 client is invoked. No credentials are read or stored. `OrderIntent` is inert data and cannot be dispatched.

## Alternatives Considered

| Option | Outcome | Rationale |
|--------|---------|-----------|
| Add real MT5 adapter skeleton importing `MetaTrader5` | Rejected | Too close to a live connection path; Build Order forbids broker package calls. |
| Define DTOs only, no port/gate | Rejected | Would fail the governance-gate proof requirement. |
| Gate controlled by environment variable | Rejected | Build Order explicitly forbids ordinary config/dev override. |
| Omit execution-shaped methods entirely | Rejected | The gate must have concrete connect/execute surfaces to refuse now. |

## Consequences

- Future broker adapters have a stable port to implement.
- Current platform remains provably incapable of broker connection or execution.
- Inner systems can depend on neutral DTOs only.
- Future Wave 6 work must explicitly amend/extend the gate through governance.

## Compliance

- Aligns with `05_SYSTEM_ARCHITECTURE.md` v2.0 §8, §12, §13, §15, §16, §17, §77.
- Supports W1-U03 Components A–E.
- Preserves advisory-first posture and all prior hardening.

---

**End ADR-019**
