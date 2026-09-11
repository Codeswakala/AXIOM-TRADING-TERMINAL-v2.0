# DELIVERY REPORT — W6-U02

## Simulated Execution Runs & Fill Events

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Unit | W6-U02 — Simulated Execution Runs & Fill Events |
| Wave | 6 — Execution Research |
| Build Order | `docs/build-orders/BUILD_ORDER_W6-U02.md` |
| Amendment | `docs/build-orders/BUILD_ORDER_W6-U02_AMENDMENT_1.md` |
| Prerequisite verdict | `docs/build-orders/ITRGA_VERDICT_W6-U01_FINAL.md` — W6-U01 APPROVED |
| Target platform version | `0.48.0` |
| Alembic head | `20260717_0029` |
| DA status | Implemented and locally validated |
| Approval status | Not self-approved; pending operator evidence and ITRGA review |

---

## 1. Executive summary

W6-U02 has been implemented as the first Wave-6 persisted-artifact unit.

The implementation adds two `SIMULATED`, research-only persistence tables:

```text
simulated_execution_runs
simulated_fill_events
```

A deterministic fill model creates simulated fill events from persisted historical/replayed candles. The model is deterministic, uses no live broker or venue seam, and produces model outputs only. `simulated_units` is dimensionless and not an order quantity. `simulated_fill_price` is a model output, not a broker fill.

No UI, broker SDK, broker credentials, live venue endpoint, real order routing, account/position/balance/margin/capital state, real P&L, Gate-opening path, or W6-U03+ feature was added.

The Constitutional Governance Gate remains **CLOSED**.

---

## 2. Amendment 1 resolution

`BUILD_ORDER_W6-U02_AMENDMENT_1.md` authorized interpreting R6-2's `users` reference as AXIOM's canonical `operators` table.

Implemented relationship:

```text
simulated_execution_runs.operator_id -> operators.id
```

No `users` table, alias, or view was added.

Operator-attribution evidence query:

```sql
SELECT COUNT(*) AS orphan_operator_count
FROM simulated_execution_runs ser
LEFT JOIN operators o ON o.id = ser.operator_id
WHERE o.id IS NULL;
```

Expected result:

```text
orphan_operator_count = 0
```

---

## 3. Scope delivered

### A. Persistence

Created:

```text
backend/app/db/models/simulated_execution.py
backend/alembic/versions/20260717_0028_w6_u02_simulated_execution_runs.py
backend/alembic/versions/20260717_0029_w6_u02_simulated_fill_events.py
```

Tables:

```text
simulated_execution_runs
simulated_fill_events
```

`simulated_execution_runs` fields include:

```text
run_id
created_at
operator_id
simulation_mode
simulation_policy_version
input_artifact_ids
replay_scope
fill_model_name
fill_model_version
assumptions
limitations
research_status
simulation_disclaimer
audit_correlation_id
```

`simulated_fill_events` fields include:

```text
simulated_fill_id
run_id
created_at
simulation_mode
market_class
symbol
timeframe
as_of_time
simulated_research_direction
simulated_units
requested_reference_price
simulated_fill_price
simulated_slippage_bps
source_candle_ids
fill_model_name
fill_model_version
research_status
simulation_disclaimer
audit_correlation_id
```

### B. Deterministic fill model and service

Created:

```text
backend/app/execution_research/simulation.py
```

Key implementation:

```text
DeterministicSimulatedFillModel
SimulatedExecutionRunSpec
SimulatedExecutionService
```

Fill model identity:

```text
fill_model_name = deterministic_mid_close_slippage
fill_model_version = w6-u02.fill_model.v1
```

Simulation policy version:

```text
w6-u01.gate_closed_simulation_envelope.v1
```

### C. API

Created:

```text
backend/app/api/routes/execution_research.py
backend/app/models/simulated_execution.py
```

Registered endpoints:

```text
POST /api/v1/execution-research/simulated-runs
GET  /api/v1/execution-research/simulated-runs
GET  /api/v1/execution-research/simulated-runs/{run_id}
GET  /api/v1/execution-research/simulated-runs/{run_id}/fills
GET  /api/v1/execution-research/simulated-fills/{fill_id}
```

The create endpoint writes only simulated research artifacts and does not reach a broker/live seam.

### D. Audit events

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

### E. Evidence script

Created:

```text
scripts/w6_u02_seed_simulated_execution.py
```

The script:

- ensures an AXIOM operator exists;
- seeds replay candles;
- creates one simulated execution run;
- creates deterministic simulated fill events;
- commits audit rows.

---

## 4. Guardrail compliance

| Requirement | Result |
|---|---|
| GR6-2 simulation/research only | All records carry `simulation_mode='SIMULATED'`, `research_status='research_only'`, and simulation disclaimer. |
| R6-2 operator attribution | `operator_id` FK targets `operators.id`; not broker/account identity. |
| R6-3 no real P&L / not real quantity | `simulated_units` is dimensionless; `simulated_fill_price` is a model output; tests reject real-P&L/live-fill/guarantee framing. |
| R6-4 Gate-closed proof | W6-U01 Gate-closed test and standing broker tests remain in targeted regression. |
| R6-6 immutable versions | `simulation_policy_version` and `fill_model_version` are stored on records and in audit details; no update path exists. |
| R6-8 write-safe create | Create path writes only simulated persistence; grep proves no live broker/Gate path. |
| R6-9 persistence capture | Evidence pack includes raw SELECTs and no-orphan audit/operator joins. |
| No UI | Preserved. No W6-U02 frontend page added; only shell identity updated. |
| No dependency change | Preserved. No broker/exchange/LLM SDK added. |

---

## 5. Files changed or added for W6-U02

### Backend created

```text
backend/app/db/models/simulated_execution.py
backend/app/execution_research/simulation.py
backend/app/models/simulated_execution.py
backend/app/api/routes/execution_research.py
backend/alembic/versions/20260717_0028_w6_u02_simulated_execution_runs.py
backend/alembic/versions/20260717_0029_w6_u02_simulated_fill_events.py
backend/tests/test_simulated_execution.py
```

### Backend modified

```text
backend/app/__init__.py
backend/app/api/router.py
backend/app/core/config.py
backend/app/db/models/__init__.py
backend/app/execution_research/__init__.py
backend/app/main.py
backend/app/models/system.py
backend/pyproject.toml
backend/tests/test_system.py
```

### Frontend modified

```text
frontend/src/layouts/TerminalLayout.tsx
```

No W6-U02 UI page was added.

### Scripts/docs created or updated

```text
scripts/w6_u02_seed_simulated_execution.py
docs/build-orders/BUILD_ORDER_W6-U02_AMENDMENT_1.md
docs/build-orders/BUILD_ORDER_INTAKE_W6-U02.md
docs/adr/ADR-057_Simulated_Execution_Runs_and_Fill_Events.md
docs/evidence/W6-U02_OPERATOR_EVIDENCE_COMMANDS.md
DELIVERY_REPORT_W6-U02.md
README.md
PROJECT_STATE.md
CHANGELOG.md
docs/governance/RISK_REGISTER.md
docs/governance/TECHNICAL_DEBT_REGISTER.md
docs/governance/GOVERNANCE_AMENDMENTS.md
docs/governance/04_PROJECT_ROADMAP.md
```

---

## 6. Local validation performed by DA

### Backend Ruff

```bash
cd /home/user/axiom/backend
ruff check .
```

Result:

```text
All checks passed!
```

### Targeted W6 tests

```bash
cd /home/user/axiom/backend
pytest tests/test_simulated_execution.py tests/test_execution_research_safety.py tests/test_broker_integration.py -q
```

Result:

```text
23 passed, 1 warning
```

### Backend full suite

```bash
cd /home/user/axiom/backend
pytest -q
```

Result:

```text
307 passed, 1 warning
```

### Alembic migration smoke

```bash
cd /home/user/axiom/backend
AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w6u02_alembic.db' \
AXIOM_DATABASE_AUTO_CREATE_SCHEMA=false \
alembic upgrade head

AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w6u02_alembic.db' \
AXIOM_DATABASE_AUTO_CREATE_SCHEMA=false \
alembic current
```

Result:

```text
20260717_0029 (head)
```

### Frontend validation

```bash
cd /home/user/axiom/frontend
npm ci
npm audit --audit-level=high
npm test
npm run lint
npm run build
```

Results:

```text
npm audit: found 0 vulnerabilities
Vitest: 17 files passed / 53 tests passed
TypeScript lint: clean
Build: successful
```

### Grep checks

Execution Research live-path grep:

```bash
grep -RInE "place_order|cancel_order|go_live|live_order|real_account|account_balance|margin|broker\.(connect|execute)" backend/app/execution_research backend/app/api/routes/execution_research.py || true
```

Result:

```text
No output
```

Barred dependency grep:

```bash
grep -RInE "MetaTrader|mt5|ccxt|ib_insync|oandapy|alpaca|binance|openai|anthropic|transformers|langchain|llama|broker-sdk|exchange" backend/requirements.txt backend/pyproject.toml frontend/package.json || true
```

Result:

```text
No output
```

---

## 7. Operator evidence pack

Operator evidence command pack is ready at:

```text
docs/evidence/W6-U02_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes exact Windows PowerShell + PostgreSQL commands for:

1. build identity;
2. Alembic head advance to `20260717_0029`;
3. committing seed script;
4. raw SELECTs for runs and fills;
5. no-orphan audit joins for runs and fills;
6. no-orphan operator join against `operators`;
7. forbidden-column proof;
8. named tests and determinism proof;
9. API create/list/detail/fill evidence;
10. bright-line grep and barred dependency proof;
11. frontend unchanged/no UI proof;
12. full frontend regression;
13. Git-Bash CI exit 0.

---

## 8. Deferred / explicitly not implemented

The following remain out of scope and were not implemented:

- UI;
- simulated paper ledger;
- execution risk reports;
- replay experiment pre-registration;
- analytics/performance comparison;
- broker SDK;
- broker credentials;
- live venue endpoint;
- real order routing;
- real account/position/balance/margin/capital state;
- real P&L;
- Gate opening;
- W6-U03 or later functionality.

---

## 9. DA disposition

W6-U02 is implemented and locally validated by the Development Authority.

This is **not** an approval. DA does not self-approve W6-U02, self-authorize W6-U03, open the Governance Gate, add live broker connectivity, add execution/order/account paths, or begin any W6-U03+ feature.

Next required step: operator runs `docs/evidence/W6-U02_OPERATOR_EVIDENCE_COMMANDS.md` on the target Windows/PostgreSQL environment and submits the transcript to ITRGA for independent review.

---

**End of DELIVERY_REPORT_W6-U02.md**
