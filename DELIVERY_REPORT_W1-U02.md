# Delivery Report — W1-U02

| Field | Value |
|-------|-------|
| Build Order | **W1-U02** Core Platform: Observability Service & CI Gate Consolidation |
| Platform | **0.10.0** |
| Date | 2026-07-13 |
| Author | Development Authority |
| Status | **Implemented — submitted for ITRGA review** |
| Approval | **Not self-approved** |
| Prerequisite | W1-U01 **APPROVED** per W1-U02 authorization statement |
| Canonical architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` v2.0 |

---

## 1. Executive Summary

W1-U02 establishes a first-class Observability Service and consolidates the automated CI gate. This is infrastructure/telemetry work only. It does **not** introduce execution, broker connectivity, ML/AI product behavior, chart feature expansion, or new markets.

### Components delivered

| Component | Status |
|-----------|--------|
| **A Observability Service** | Implemented — single-responsibility telemetry service, correlation IDs, structured redacted logs |
| **B Metrics + health/readiness** | Implemented — authenticated JSON `/metrics`; `/health` and `/ready` include latency/status detail |
| **C Runtime diagnostics** | Implemented — HTTP middleware logs request completion and unhandled exceptions with correlation IDs |
| **D CI gate consolidation** | Implemented — GitHub CI includes Alembic-on-PostgreSQL, Ruff, pytest, vitest, tsc/build; local CI equivalent added |
| **E Governance register sync** | Implemented — debt/risk/amendment/project state updated; simulated chronology risk documented |
| **F Verification** | Implemented locally — backend 81, frontend 16, Ruff clean, build clean |

---

## 2. Hypothesis / counter-hypotheses

### Hypothesis

A read-only Observability Service with redaction, correlation IDs, metrics, health/readiness maturation, and CI consolidation can improve diagnosability without leaking secrets, adding business logic, or regressing approved Wave-0/W1-U01 capabilities.

### Counter-hypotheses

| Counter | Result | Evidence |
|---------|--------|----------|
| Observability may log secrets/tokens/passwords | **Falsified at test level** | `test_redaction_removes_tokens_passwords_and_db_credentials`, JSON formatter test |
| Middleware may break request routing | **Falsified at automated level** | Backend 81 tests pass; health, auth, live, chart-support APIs preserved |
| Metrics endpoint may leak unauthenticated telemetry | **Falsified** | `/api/v1/metrics` returns 401 without token; test coverage added |
| Metrics/observability may contain business logic | **Falsified by design** | Observability service records/exposes telemetry only; no domain mutation |
| CI may still miss Ruff | **Falsified in config** | `.github/workflows/ci.yml` now runs `ruff check .` |

---

## 3. Implementation Summary

### 3.1 Observability Service

Added:

- `backend/app/services/observability_service.py`

Capabilities:

- read-only telemetry registry;
- process uptime and HTTP request metrics;
- request status/path/latency counters;
- correlation ID context management;
- redaction utility for strings and simple containers.

No business/domain decisions are made by this service.

### 3.2 Structured logging + correlation IDs

Changed:

- `backend/app/core/logging.py`
- `backend/app/main.py`
- `backend/app/api/routes/ws.py`

Behavior:

- HTTP middleware accepts `X-Correlation-ID` or generates a UUID.
- Response includes `X-Correlation-ID`.
- JSON logs include:
  - `timestamp`;
  - `level`;
  - `logger`;
  - `component`;
  - `category`;
  - `correlation_id`;
  - redacted `message`.
- Text logs include `cid=<correlation-id>` for local diagnostics.
- WebSocket status/market routes set per-connection correlation IDs where practical.

### 3.3 Redaction

Redaction covers:

- Authorization Bearer values;
- generic Bearer tokens;
- passwords;
- access/refresh tokens;
- WebSocket tickets;
- PostgreSQL URLs with embedded credentials.

Telemetry intentionally does not log request bodies or raw headers.

### 3.4 Metrics endpoint

Added:

- `backend/app/api/routes/observability.py`

Endpoint:

| Method | Path | Auth |
|--------|------|------|
| GET | `/api/v1/metrics` | Bearer |
| GET | `/metrics` | Bearer compatibility mount |

Metrics payload includes:

- service identity;
- process uptime/pid;
- HTTP request counters/status/path/latency/recent summaries;
- database status/backend/latency/pool detail;
- live market running/connected/message/persist/lag/subscriber data.

Payload is redacted before return.

### 3.5 Health/readiness maturation

Changed:

- `backend/app/models/health.py`
- `backend/app/services/health_service.py`

Updates:

- `HealthResponse` includes `latency_ms`.
- `ServiceStatus` includes `latency_ms`.
- `/ready` checks include latency for configuration, logging, database, ML stub, broker stub, market ingestion, authentication, and live market.
- No secrets or DB credentials are included.

### 3.6 CI gate consolidation

Changed:

- `.github/workflows/ci.yml`

Backend CI now runs:

1. PostgreSQL service container;
2. dependency install;
3. `alembic upgrade head` against PostgreSQL;
4. `ruff check .`;
5. `pytest -q`.

Frontend CI runs:

1. `npm ci`;
2. `npm test`;
3. `npx tsc -b --pretty false`;
4. `npm run build`.

Added local equivalent:

- `scripts/local_ci.sh`

### 3.7 Governance / documentation

Added:

- `docs/build-orders/BUILD_ORDER_W1-U02.md`
- `docs/build-orders/BUILD_ORDER_INTAKE_W1-U02.md`
- `docs/adr/ADR-017_Observability_Service.md`
- `docs/adr/ADR-018_CI_Gate_Consolidation.md`
- `docs/api/OBSERVABILITY_W1-U02.md`
- `docs/evidence/W1-U02_OPERATOR_EVIDENCE_CHECKLIST.md`

Updated:

- `PROJECT_STATE.md`
- `CHANGELOG.md`
- `README.md`
- `backend/README.md`
- `docs/api/ENDPOINT_AUTH_INVENTORY_W1-U01.md`
- `docs/governance/TECHNICAL_DEBT_REGISTER.md`
- `docs/governance/RISK_REGISTER.md`
- `docs/governance/GOVERNANCE_AMENDMENTS.md`
- frontend top-bar unit label.

---

## 4. Evidence

### 4.1 Backend tests and Ruff

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
collected 81 items
81 passed, 1 warning
```

### 4.2 Frontend tests/type/build

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

### 4.3 Alembic local migration equivalent

Command:

```bash
cd backend
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w1u02_alembic.db' \
AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
alembic upgrade head
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w1u02_alembic.db' alembic current
```

Result:

```text
20260711_0004 (head)
```

True PostgreSQL/remote CI evidence must be provided by Operator/CI for ITRGA approval, per W1-U02 mandatory evidence.

---

## 5. Tests Added

New file:

- `backend/tests/test_observability.py`

New coverage:

| Test | Purpose |
|------|---------|
| `test_redaction_removes_tokens_passwords_and_db_credentials` | Proves raw token/password/DB password do not survive redaction |
| `test_json_formatter_has_required_fields_and_correlation_id` | Proves JSON log fields and correlation ID presence |
| `test_request_correlation_id_response_header` | Proves request correlation ID is returned to operator |
| `test_metrics_requires_auth_and_exposes_shape` | Proves metrics requires auth and exposes expected shape without secrets |
| `test_health_ready_include_latency_and_no_secrets` | Proves health/readiness latency fields and no DB password leakage |

Backend baseline increased from **76** to **81**.

---

## 6. Operator Evidence Checklist

Created:

`docs/evidence/W1-U02_OPERATOR_EVIDENCE_CHECKLIST.md`

It instructs the Operator to provide Windows + PostgreSQL evidence for:

1. PostgreSQL `alembic upgrade head` with `PostgresqlImpl`;
2. backend `pytest` raw output showing `collected 81 items` and `81 passed`;
3. `ruff check .`;
4. frontend `npm test`, `tsc`, build;
5. metrics/health/readiness runtime payloads;
6. redaction test output;
7. correlation ID evidence;
8. parity smoke: login → WS ticket 200 → live feed → candle fetch;
9. green GitHub Actions run or local equivalent.

---

## 7. Behavior Preservation

Preserved approved behavior:

- login/operator session;
- refresh rotation/reuse detection;
- WS ticket issue and `/ws/market` ticket auth;
- `/ws/status` ticket auth;
- authenticated operational endpoints;
- historical CSV ingestion;
- candle persistence/history;
- simulated live feed start/stop/status;
- chart data access after authenticated frontend session;
- data provenance markers;
- UTC strict trusted boundaries;
- single-uvicorn workflow.

Intentional additions:

- HTTP correlation ID header;
- request completion logs;
- authenticated metrics endpoint;
- per-check latency in health/readiness;
- CI Ruff gate.

No product trading/ML/chart-market behavior was added.

---

## 8. Technical Debt / Register Updates

Updated `TECHNICAL_DEBT_REGISTER.md`:

| Item | Status |
|------|--------|
| TD-033 no first-class observability/metrics | **Closed** W1-U02 |
| TD-034 CI missing Ruff/local equivalent gate | **Closed in code** W1-U02; target green-run evidence required |
| U07-OBS-2 logged-out screenshots | Closed per Wave-0 closure evidence |
| U07-OBS-5 default viewport | Closed; ~80-bar visible range recorded |
| OBS-1 simulated chronology | Documented as explicit ML/analytics risk |
| OBS-2 / W0-CI-C4b | CI code gate implemented; operator/remote green evidence required |
| OBS-3 UTC output | Code/tests implemented; operator `test_time_utc.py -vv` paste required |

Updated `RISK_REGISTER.md`:

- added/mitigated secret-leak telemetry risk;
- documented simulated chronology risk;
- documented runtime diagnostic risk mitigation;
- retained CI green-run evidence as open residual until Operator/CI evidence.

---

## 9. Risks and Unknowns

| Risk / Unknown | Status | Mitigation |
|----------------|--------|------------|
| Remote GitHub CI run not available in DA sandbox | Known unknown | CI workflow updated; local script added; Operator/CI evidence required |
| PostgreSQL runtime metrics not DA-verified | Known unknown | Operator evidence checklist includes PostgreSQL run |
| npm audit transitive vulnerabilities | Existing open debt | TD-012 remains open; not in W1-U02 scope to force breaking upgrades |
| Metrics are process-local | Accepted limitation | Full distributed telemetry deferred |
| OpenTelemetry/Grafana absent | Explicitly out of scope | ADR-017 documents future evolution |

---

## 10. Confidence Statement

| Dimension | Rating | Justification |
|-----------|--------|---------------|
| Observability design / architecture fit | **HIGH** | Single service, read-only telemetry, no business logic, ADR documented |
| Redaction implementation | **HIGH in DA tests** | Raw token/password/DB credential negative tests pass |
| DA-sandbox automated correctness | **HIGH** | Ruff clean; backend 81; frontend 16; tsc/build clean |
| Target-platform runtime correctness | **LIMITED until Operator evidence lands** | Windows + PostgreSQL + metrics/log samples required by Build Order |
| CI gate implementation | **MODERATE-HIGH** | Workflow and local script implemented; green remote/operator run still required |
| Overall package | **MODERATE-HIGH for implementation; CONDITIONAL for approval evidence** | Mandatory operator evidence remains required |

No percentage confidence is asserted.

---

## 11. Readiness Statement

> W1-U02 is implemented, tested locally, documented, and submitted for independent ITRGA review.  
> DA does **not** self-approve.  
> Operator-run Windows + PostgreSQL evidence remains mandatory for approval.  
> The next unit must not begin until ITRGA disposition and subsequent Build Order authorization.

---

**End of Delivery Report W1-U02**
