# DELIVERY REPORT — W6-U05

## Trade Replay & Execution Experiment Pre-Registration

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Unit | W6-U05 — Trade Replay & Execution Experiment Pre-Registration |
| Wave | 6 — Execution Research |
| Build Order | `docs/build-orders/BUILD_ORDER_W6-U05.md` |
| Prerequisite verdict | `docs/build-orders/ITRGA_VERDICT_W6-U04_FINAL.md` — W6-U04 APPROVED |
| Target platform version | `0.51.0` |
| Alembic head | `20260717_0032` |
| DA status | Implemented and locally validated |
| Approval status | Not self-approved; pending operator evidence and ITRGA review |

---

## 1. Executive summary

W6-U05 has been implemented as simulated trade replay and execution experiment pre-registration.

The implementation adds `execution_research_experiments`, a `SIMULATED`, research-only experiment table. Each experiment stores an immutable pre-registration plan, deterministic plan hash, as-of bounded replay window, replay input lineage, included scope summary, uncertainty, limitations, disclaimer, and audit correlation.

Replay input selection is bounded by `open_time <= as_of_time`, and persisted lineage includes included candle ids plus excluded future candle count. No UI, live feed, broker SDK, broker credentials, live venue endpoint, real order routing, real account/position/balance/margin/capital state, real P&L, Gate-opening path, analytics/performance comparison, or W6-U06+ feature was added.

The Constitutional Governance Gate remains **CLOSED**.

---

## 2. Scope delivered

### A. Persistence

Created:

```text
backend/app/db/models/execution_experiment.py
backend/alembic/versions/20260717_0032_w6_u05_execution_research_experiments.py
```

Table:

```text
execution_research_experiments
```

Fields:

```text
experiment_id
created_at
simulation_mode
operator_id
experiment_title
pre_registration_plan
plan_hash
as_of_time
as_of_window
replay_input_lineage
included_scope_summary
uncertainty
limitations
research_status
simulation_disclaimer
audit_correlation_id
```

Foreign-key relationship:

```text
operator_id -> operators.id
```

### B. Experiment service

Created:

```text
backend/app/execution_research/experiment.py
```

Key implementation:

```text
ExecutionResearchExperimentDraft
ExecutionResearchExperimentService
```

The service:

1. validates a pre-registration draft;
2. resolves existing simulated artifact ids;
3. selects replay candles with `open_time >= as_of_start` and `open_time <= as_of_time`;
4. counts candles with `open_time > as_of_time` as excluded future rows;
5. computes deterministic `plan_hash` over canonical `pre_registration_plan`;
6. stores included/excluded replay input lineage;
7. stores declared and executed replay scope summaries;
8. stores uncertainty and limitations;
9. appends `execution_research_experiment.created` audit event.

### C. API

Extended:

```text
backend/app/api/routes/execution_research.py
backend/app/models/execution_experiment.py
```

Endpoints:

```text
POST /api/v1/execution-research/execution-experiments
GET  /api/v1/execution-research/execution-experiments
GET  /api/v1/execution-research/execution-experiments/{experiment_id}
```

The create endpoint writes only experiment persistence and does not reach any live feed, broker, order, account, or Gate seam.

### D. Audit event

Each experiment appends:

```text
action = execution_research_experiment.created
resource_type = execution_research_experiment
resource_id = execution_research_experiments.experiment_id
correlation_id = execution_research_experiments.audit_correlation_id
```

### E. Tests

Created:

```text
backend/tests/test_execution_experiments.py
```

Named tests include:

```text
test_execution_research_experiment_persists_and_audit_no_orphan
test_experiment_plan_hash_is_immutable_and_matches_preregistration
test_replay_excludes_future_rows_beyond_as_of
test_replay_included_scope_equals_preregistered_scope_no_cherry_picking
test_registered_plan_mutation_is_refused
test_execution_experiment_has_no_forbidden_account_pnl_or_sizing_columns
test_execution_experiment_carries_uncertainty_and_limitations
test_execution_research_experiment_create_path_has_no_live_feed_broker_or_gate_path
test_governance_gate_remains_closed_for_wave6
test_execution_experiment_api_auth_create_list_detail
```

---

## 3. Guardrail compliance

| Requirement | Result |
|---|---|
| R6-7 no-look-ahead | Implemented. Replay input query is bounded by `open_time <= as_of_time`; tests prove future rows are excluded. |
| Pre-registration immutability | Implemented. `plan_hash` is deterministic SHA-256 over canonical `pre_registration_plan`; no update route/service exists. |
| No cherry-picking | Implemented. Executed replay scope equals declared replay scope. |
| R6-2 operator attribution | Implemented. `operator_id -> operators.id`; no broker/account identity. |
| R6-4 Gate closed | Targeted tests include W6 gate-closed test and broker suite. |
| R6-8 write-safe create | Implemented. Grep/test prove no live feed, broker, order, account, or Gate path. |
| R6-9 persistence capture | Evidence pack includes raw SELECT, no-orphan audit, operator, and lineage joins. |
| No UI | Preserved. W6-U05 has no UI page. |
| No dependency change | Preserved. No broker/exchange/LLM SDK added. |

---

## 4. Files changed or added for W6-U05

### Backend created

```text
backend/app/db/models/execution_experiment.py
backend/app/execution_research/experiment.py
backend/app/models/execution_experiment.py
backend/alembic/versions/20260717_0032_w6_u05_execution_research_experiments.py
backend/tests/test_execution_experiments.py
```

### Backend modified

```text
backend/app/__init__.py
backend/app/api/routes/execution_research.py
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

No W6-U05 UI page was added.

### Scripts/docs created or updated

```text
scripts/w6_u05_seed_execution_experiment.py
docs/build-orders/ITRGA_VERDICT_W6-U04_FINAL.md
docs/build-orders/BUILD_ORDER_W6-U05.md
docs/build-orders/BUILD_ORDER_INTAKE_W6-U05.md
docs/adr/ADR-060_Trade_Replay_and_Execution_Experiment_PreRegistration.md
docs/evidence/W6-U05_OPERATOR_EVIDENCE_COMMANDS.md
DELIVERY_REPORT_W6-U05.md
README.md
PROJECT_STATE.md
CHANGELOG.md
docs/governance/RISK_REGISTER.md
docs/governance/TECHNICAL_DEBT_REGISTER.md
docs/governance/GOVERNANCE_AMENDMENTS.md
docs/governance/04_PROJECT_ROADMAP.md
```

---

## 5. Local validation performed by DA

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
pytest tests/test_execution_experiments.py tests/test_execution_risk_reports.py tests/test_simulated_paper_ledger.py tests/test_simulated_execution.py tests/test_execution_research_safety.py tests/test_broker_integration.py -q
```

Result:

```text
51 passed, 1 warning
```

### Backend full suite

```bash
cd /home/user/axiom/backend
pytest -q
```

Result:

```text
335 passed, 1 warning
```

### Alembic migration smoke

```bash
cd /home/user/axiom/backend
AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w6u05_alembic.db' \
AXIOM_DATABASE_AUTO_CREATE_SCHEMA=false \
alembic upgrade head

AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w6u05_alembic.db' \
AXIOM_DATABASE_AUTO_CREATE_SCHEMA=false \
alembic current
```

Result:

```text
20260717_0032 (head)
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

Experiment/live path grep:

```bash
grep -RInE "place_order|broker\.(connect|execute)|go_live|live_order|live_feed|real_account|account_balance|margin|position_size|order_size|real_pnl" backend/app/execution_research backend/app/api/routes/execution_research.py || true
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

## 6. Operator evidence pack

Operator evidence command pack is ready at:

```text
docs/evidence/W6-U05_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes exact Windows PowerShell + PostgreSQL commands for:

1. build identity;
2. Alembic head advance to `20260717_0032`;
3. committing seed script;
4. raw SELECT from `execution_research_experiments`;
5. no-orphan audit/operator/lineage joins;
6. forbidden-column proof;
7. no-look-ahead bounding and negative checks;
8. plan-hash recomputation and scope-match proof;
9. named tests;
10. API create/list/detail and mutation/execute absence;
11. bright-line grep and dependency proof;
12. frontend unchanged/no UI proof;
13. Git-Bash CI exit 0.

---

## 7. Deferred / explicitly not implemented

The following remain out of scope and were not implemented:

- UI;
- live feed;
- simulated execution analytics/performance comparison;
- broker SDK;
- broker credentials;
- live venue endpoint;
- real order routing;
- real account/position/balance/margin/capital state;
- real P&L;
- Gate opening;
- W6-U06 or later functionality.

---

## 8. DA disposition

W6-U05 is implemented and locally validated by the Development Authority.

This is **not** an approval. DA does not self-approve W6-U05, self-authorize W6-U06, open the Governance Gate, add live broker connectivity, add execution/order/account paths, or begin any W6-U06+ feature.

Next required step: operator runs `docs/evidence/W6-U05_OPERATOR_EVIDENCE_COMMANDS.md` on the target Windows/PostgreSQL environment and submits the transcript to ITRGA for independent review.

---

**End of DELIVERY_REPORT_W6-U05.md**
