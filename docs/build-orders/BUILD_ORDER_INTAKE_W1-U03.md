# Build Order Intake — W1-U03

| Item | Value |
|------|-------|
| Build Order | W1-U03 — External Integration: MT5 Integration Framework |
| Date received | 2026-07-13 |
| Authority | ITRGA, following W1-U02 APPROVED WITH OBSERVATIONS + Operator authorization |
| DA status | ACCEPTED — implementation authorized by issued Build Order |
| Approval | Not self-approved; delivery requires ITRGA review |

---

## 1. Governance confirmation

The Development Authority confirms receipt of:

- `docs/build-orders/ITRGA_VERDICT_W1-U02_FINAL.md`
- `docs/build-orders/BUILD_ORDER_W1-U03.md`

W1-U02 is recorded by ITRGA as **APPROVED WITH OBSERVATIONS**. W1-U03 is **ISSUED**. Implementation may proceed within the Build Order scope.

## 2. Objective

Define the broker integration framework seam inside the External Integration System while making present broker connection/execution impossible. This is contract-only architecture: adapter port, broker-neutral DTOs, disabled `NullBroker`, and a hard-closed Constitutional Governance Gate.

## 3. Scope interpretation

| Component | DA interpretation |
|-----------|-------------------|
| A Broker port | Define pure broker-neutral `BrokerPort` protocol; no concrete broker imports. |
| B Boundary DTOs | Define strict Pydantic DTOs (`Instrument`, `BrokerAccount`, `BrokerQuote`, `OrderIntent`, `BrokerCapabilities`) and typed errors. |
| C NullBroker | Disabled adapter implementing the port with zero I/O and no connection/execution. |
| D Governance Gate | Hard-closed gate refuses connect/execute, logs warning, increments observability metric. |
| E Wiring/registers | Register disabled service through DI; add ADR/register updates; preserve no broker-specific leakage. |
| F Verification | Add tests for contract, DTO UTC, no I/O, gate refusals, metrics, structural containment; preserve prior suite. |

## 4. Constraints

- No real MT5 package/client call, no socket, no broker login, no credentials.
- No execution/order dispatch; `OrderIntent` is inert data only.
- No dev/config override can open the governance gate.
- No broker-specific symbols outside `backend/app/external_integration`.
- Preserve W0-U08/W1-U01/W1-U02 hardening.

## 5. Initial risk assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Accidental execution/connection path | Critical | Hard-closed gate + tests refusing connect/place_order + no I/O tests. |
| Broker vocabulary leaks inward | High | External Integration bounded context + structural grep test. |
| Credential leakage | High | No credential models/config; redaction/logging inherited; grep evidence. |
| Misinterpreting framework as live integration | Medium | Documentation and capability descriptor state disabled/no execution. |

## 6. Implementation authorization posture

Build Order accepted. DA will implement, verify, document, and submit a Delivery Report. DA does not self-approve W1-U03 or open the Governance Gate.

---

**End of intake**
