# Delivery Report — W1-U03

| Field | Value |
|-------|-------|
| Build Order | **W1-U03** External Integration: MT5 Integration Framework |
| Platform | **0.11.0** |
| Date | 2026-07-13 |
| Author | Development Authority |
| Status | **Implemented — submitted for ITRGA review** |
| Approval | **Not self-approved** |
| Prerequisite | W1-U02 **APPROVED WITH OBSERVATIONS** (`docs/build-orders/ITRGA_VERDICT_W1-U02_FINAL.md`) |
| Canonical architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` v2.0 |

---

## 1. Executive Summary

W1-U03 delivers the **MT5 integration framework** as a broker-neutral External Integration seam. It intentionally provides the **door and the lock**, not broker operation.

This unit adds:

- pure broker adapter port/interface;
- broker-neutral anti-corruption DTOs;
- disabled `NullBroker` reference adapter;
- hard-closed Constitutional Governance Gate;
- service/DI wiring;
- tests proving no I/O, no connection, no execution, and no broker-specific leakage outside External Integration.

It does **not** add a real MT5 package call, broker connection, broker login, broker credentials, broker quotes, orders, positions, paper trading, execution simulator, or any execution behavior.

---

## 2. Hypothesis / counter-hypotheses

### Hypothesis

AXIOM can define a future broker integration seam while remaining provably incapable of broker connection or execution today.

### Counter-hypotheses

| Counter | Result | Evidence |
|---------|--------|----------|
| The framework might accidentally enable broker connection | **Falsified at test level** | `NullBroker.connect()` routes through hard-closed gate and raises `GovernanceGateClosedError` |
| The framework might accidentally enable order execution | **Falsified at test level** | `place_order()` and `cancel_order()` route through closed gate and raise |
| The disabled adapter might open a socket/network path | **Falsified at test level** | `test_null_broker_opens_no_socket` monkeypatches connection creation and passes |
| MT5/broker-specific vocabulary might leak inward | **Falsified structurally** | Structural grep test excludes `MetaTrader5`, `mt5.`, broker-native symbols outside External Integration |
| Boundary DTOs might allow naive timestamps or secrets | **Falsified at test level** | DTO UTC validator rejects naive `OrderIntent.created_at`; serialization contains no secret/token fields |
| Prior Wave behavior might regress | **Falsified at automated level** | Backend 88 and frontend 16 pass |

---

## 3. Implementation Summary

### 3.1 External Integration bounded context

Created:

```text
backend/app/external_integration/
backend/app/external_integration/broker/
```

This isolates broker integration framework code inside the External Integration System.

### 3.2 Broker port/interface

Created:

```text
backend/app/external_integration/broker/port.py
```

`BrokerPort` defines the future adapter contract:

- `connect()`
- `disconnect()`
- `is_connected()`
- `describe_capabilities()`
- `get_instruments()`
- `get_account_info()`
- `get_quote(symbol)`
- `place_order(intent)`
- `cancel_order(order_id)`

The port is pure and imports no concrete broker/MT5 client.

### 3.3 Broker-neutral DTOs and errors

Created:

```text
backend/app/external_integration/broker/models.py
backend/app/external_integration/broker/errors.py
```

DTOs:

- `BrokerCapabilities`
- `Instrument`
- `BrokerAccount`
- `BrokerQuote`
- `OrderIntent`

Errors:

- `BrokerIntegrationError`
- `BrokerDisabledError`
- `BrokerNotConnectedError`
- `GovernanceGateClosedError`

`OrderIntent` is inert data only and has no dispatch path.

### 3.4 NullBroker disabled reference adapter

Created:

```text
backend/app/external_integration/broker/null_broker.py
```

Behavior:

| Method | Behavior |
|--------|----------|
| `connect()` | refused by governance gate |
| `disconnect()` | no-op |
| `is_connected()` | always `False` |
| `describe_capabilities()` | returns disabled capabilities with `execution_enabled=False` |
| read methods | raise `BrokerDisabledError` |
| execution methods | refused by governance gate |

No I/O, socket, broker package, or credentials are used.

### 3.5 Constitutional Governance Gate

Created:

```text
backend/app/external_integration/broker/governance_gate.py
```

Behavior:

- hard-coded closed;
- no ordinary config/environment override;
- refuses broker connection;
- refuses order placement/cancel paths;
- logs a `GOVERNANCE` warning with correlation support inherited from W1-U02;
- increments `observability.governance.gate_refusals_total`.

### 3.6 Service/DI wiring

Created:

```text
backend/app/external_integration/broker/service.py
```

Updated:

```text
backend/app/core/dependencies.py
```

`BrokerIntegrationService` exposes the disabled broker seam through DI while inner systems depend on the interface/neutral service, not concrete broker technology.

### 3.7 Observability metric integration

Updated:

```text
backend/app/services/observability_service.py
```

Added:

- `record_governance_gate_refusal(action=...)`
- `observability.governance.gate_refusals_total`
- `observability.governance.gate_refusals_by_action`

---

## 4. Governance / Documentation Updates

Added:

- `docs/build-orders/ITRGA_VERDICT_W1-U02_FINAL.md`
- `docs/build-orders/BUILD_ORDER_W1-U03.md`
- `docs/build-orders/BUILD_ORDER_INTAKE_W1-U03.md`
- `docs/adr/ADR-019_Broker_Integration_Framework.md`
- `docs/evidence/W1-U03_OPERATOR_EVIDENCE_COMMANDS.md`

Updated:

- `PROJECT_STATE.md`
- `CHANGELOG.md`
- `README.md`
- `docs/governance/RISK_REGISTER.md`
- `docs/governance/TECHNICAL_DEBT_REGISTER.md`
- `docs/governance/GOVERNANCE_AMENDMENTS.md`
- `docs/governance/04_PROJECT_ROADMAP.md`
- `backend/app/models/system.py`
- frontend unit label.

---

## 5. Evidence

### 5.1 Backend tests and Ruff

Commands run in DA sandbox using a temporary virtual environment outside the persisted workspace:

```bash
cd backend
ruff check .
AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_DATABASE_URL='sqlite+aiosqlite:///:memory:' \
AXIOM_DATABASE_AUTO_CREATE_SCHEMA=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
pytest
```

Result:

```text
All checks passed!
collected 88 items
88 passed, 1 warning
```

### 5.2 Frontend tests/type/build

Commands:

```bash
cd frontend
npm ci
npm test
npm run lint
npm run build
```

Result:

```text
Test Files  8 passed (8)
Tests       16 passed (16)
tsc         clean
vite build  successful
```

### 5.3 Schema

No schema migration was added by W1-U03. Current Alembic head remains:

```text
20260711_0004 (head)
```

Operator PostgreSQL evidence remains required by the Build Order.

---

## 6. Tests Added

New file:

```text
backend/tests/test_broker_integration.py
```

Coverage:

| Test | Purpose |
|------|---------|
| `test_null_broker_implements_port_and_disabled_capabilities` | Port conformance + disabled capabilities |
| `test_governance_gate_refuses_connect_and_execute` | Gate refuses connect/place_order and metric increments |
| `test_null_broker_read_paths_disabled` | Read-shaped broker calls disabled |
| `test_null_broker_opens_no_socket` | Proves disabled adapter opens no network connection |
| `test_order_intent_rejects_naive_datetime_and_serializes_without_secret` | DTO UTC + no secret fields |
| `test_no_broker_specific_symbols_outside_external_integration` | Structural anti-corruption containment |
| `test_no_broker_credential_literals_in_external_integration_code` | No broker credential literals in new code |

Backend baseline increased from **81** to **88**.

---

## 7. Explicit Negative Evidence

| Prohibited item | Status |
|-----------------|--------|
| Real `MetaTrader5` package/client invocation | Not implemented |
| Broker socket/network connection | Not implemented; no-I/O test added |
| Broker login/account credential use | Not implemented |
| Live broker quotes | Not implemented |
| Order placement/cancellation/modification | Gate-refused; no dispatch |
| Paper trading/execution simulator | Not implemented |
| Broker-specific symbol leakage inward | Structural test added |
| Dev/config override to open gate | Not implemented |

---

## 8. Operator Evidence Command Pack

Created:

```text
docs/evidence/W1-U03_OPERATOR_EVIDENCE_COMMANDS.md
```

This includes Windows/PowerShell + PostgreSQL commands for:

1. PostgreSQL Alembic proof;
2. full backend/frontend test console;
3. gate-closed proof via `pytest tests/test_broker_integration.py -vv`;
4. boundary-containment grep;
5. no-secret grep;
6. optional runtime metric check;
7. CI run/local equivalent;
8. parity smoke.

---

## 9. Carried Observations / Debt

| Item | Status |
|------|--------|
| OBS-2 green CI run | Still requires real pipeline evidence; local/manual gates pass |
| TD-012 npm audit critical/high | Risk-assessed as `R-FE-01`; scheduled for next frontend/tooling hardening unit |
| Real MT5 adapter | Deferred by governance |
| Broker live quotes/account info | Deferred by governance |
| Execution simulator/paper trading/order dispatch | Deferred to Wave 6 governance |

---

## 10. Risks and Unknowns

| Risk / Unknown | Status | Mitigation |
|----------------|--------|------------|
| Future broker execution accidentally enabled | Controlled | Hard-closed gate; no config override; tests |
| Broker vocabulary leak | Controlled | Bounded context + structural test |
| Broker credentials leak | Controlled | No credential code/config; grep evidence required |
| CI orchestration green run | Still pending | Operator/GitHub evidence required |
| npm audit critical/high | Open | Registered as risk and debt |

---

## 11. Confidence Statement

| Dimension | Rating | Justification |
|-----------|--------|---------------|
| Broker framework architecture | **HIGH** | Pure port, neutral DTOs, bounded context, ADR documented |
| Gate-closed safety | **HIGH in DA tests** | connect and place_order refused; metric increment asserted |
| No-I/O guarantee | **HIGH in DA tests** | `socket.create_connection` monkeypatch test passes; no broker package imported |
| Boundary containment | **HIGH in DA tests** | Structural grep test passes |
| Target-platform runtime correctness | **LIMITED until Operator evidence lands** | Windows + PostgreSQL evidence required by Build Order |
| Overall package | **MODERATE-HIGH for implementation; CONDITIONAL for approval evidence** | Mandatory operator evidence remains required |

No percentage confidence is asserted.

---

## 12. Readiness Statement

> W1-U03 is implemented, tested locally, documented, and submitted for independent ITRGA review.  
> The Constitutional Governance Gate remains closed.  
> DA does **not** self-approve.  
> Operator-run Windows + PostgreSQL evidence remains mandatory for approval.  
> The next unit must not begin until ITRGA disposition and subsequent Build Order authorization.

---

**End of Delivery Report W1-U03**
