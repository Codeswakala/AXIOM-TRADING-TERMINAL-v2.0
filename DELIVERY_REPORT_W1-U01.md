# Delivery Report — W1-U01

| Field | Value |
|-------|-------|
| Build Order | **W1-U01** Core Platform: Service Architecture & API Hardening Foundation |
| Platform | **0.9.0** |
| Date | 2026-07-12 |
| Author | Development Authority |
| Status | **Implemented — submitted for ITRGA review** |
| Approval | **Not self-approved** |
| Prerequisite | Wave 0 **CLOSED** by ITRGA (`docs/build-orders/ITRGA_WAVE0_CLOSURE.md`) |
| Canonical architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` v2.0 |

---

## 1. Executive Summary

W1-U01 matures the closed Wave-0 foundation into the first Wave-1 Core Platform seam-hardening unit. It does **not** introduce execution, broker connectivity, ML/AI product behavior, chart feature expansion, or new markets.

### Components delivered

| Component | Status |
|-----------|--------|
| **A Application Services** | Implemented — persistence workflows now route through `PersistenceService`; controllers stay thin |
| **B API authorization breadth** | Implemented — operational REST endpoints require Bearer; `/ws/status` now ticket-authenticated |
| **C Time & data correctness** | Implemented — UTC normalization utility + schema/service validators + regression tests |
| **D Persistence service maturation** | Implemented — repository → service → API layering for persistence surface |
| **E CI/local gate + register sync** | Implemented locally — backend/frontend/Alembic/Ruff gates passed; registers synced |
| **F Verification & delivery** | Implemented — backend 74, frontend 16, tsc/build clean; report submitted |

---

## 2. Hypothesis / counter-hypotheses

### Hypothesis

Hardening endpoint authorization, maturing persistence service layering, and enforcing UTC-aware API boundaries can be completed without regressing approved Wave-0 capabilities.

### Counter-hypotheses

| Counter | Result | Evidence |
|---------|--------|----------|
| Auth-locking operational endpoints breaks frontend chart/live flows | **Falsified** | Frontend API client now sends Bearer for system/persistence; frontend suite/build green |
| `/ws/status` auth breaks dashboard status socket | **Falsified** | `useStatusSocket` now obtains WS ticket; backend WS status tests pass |
| UTC normalization causes timestamp regressions | **Falsified** | `test_time_utc.py` validates auth/candle/audit/ingestion API timestamps |
| Persistence service refactor changes API behavior | **Falsified** | Persistence lifecycle tests pass through new service boundary |
| Hardening regresses Wave-0 live/chart/auth behavior | **Falsified at automated level** | Backend 74 and frontend 16 pass; WS ticket tests preserved |

---

## 3. Implementation Summary

### 3.1 Application Services layer

Added:

- `backend/app/services/persistence_service.py`

Changed persistence routes to delegate to this service:

- create/list/get candles;
- list audit events;
- database stats.

This keeps HTTP controllers focused on input/auth/response handling and keeps persistence orchestration in the application-service layer.

### 3.2 Endpoint authorization breadth

Added endpoint classification:

- `docs/api/ENDPOINT_AUTH_INVENTORY_W1-U01.md`

Operational APIs now require `CurrentOperatorDep`, including:

- `/system/info`
- `/api/v1/persistence/*`
- `/api/v1/ingestion/*`
- existing `/api/v1/market/live/*`

`/ws/status` now requires a short-lived one-time ticket, matching the W0-U08 `/ws/market` ticket pattern.

Public endpoints retained:

- `/health`
- `/ready`
- `/api`
- `/api/v1/auth/login`
- `/api/v1/auth/refresh` using refresh-token credential semantics.

### 3.3 UTC-aware time correctness

Added:

- `backend/app/core/time.py`

Key behavior:

- `utc_now()` returns timezone-aware UTC.
- `ensure_utc()` treats naive datetimes as UTC for compatibility and normalizes aware datetimes to UTC.
- Pydantic response/input models normalize API-facing datetimes.
- Candle repository/service boundaries normalize candle `open_time`.

### 3.4 Frontend compatibility updates

Changed:

- `fetchSystemInfo()` now sends Bearer auth.
- `fetchCandles()` now sends Bearer auth.
- `useStatusSocket()` now obtains a WS ticket before connecting to `/ws/status`.
- Login page no longer pre-fills historical insecure `admin/admin123` credentials.
- UI text updated from W0-U06/deferred language to W1-U01/current capability language.

### 3.5 Documentation / governance updates

Added:

- `docs/build-orders/ITRGA_WAVE0_CLOSURE.md`
- `docs/build-orders/BUILD_ORDER_W1-U01.md`
- `docs/build-orders/BUILD_ORDER_INTAKE_W1-U01.md`
- `docs/api/ENDPOINT_AUTH_INVENTORY_W1-U01.md`
- `docs/adr/ADR-015_API_Authorization_Breadth.md`
- `docs/adr/ADR-016_Persistence_Service_Boundary.md`

Updated:

- `PROJECT_STATE.md`
- `CHANGELOG.md`
- `README.md`
- `backend/README.md`
- `frontend/README.md`
- `docs/auth/SETUP.md`
- `docs/market/LIVE_ADAPTER_USAGE.md`
- `docs/frontend/LIVE_DASHBOARD.md`
- `docs/frontend/CHART_WORKSPACE.md`
- `TECHNICAL_DEBT_REGISTER.md`
- `RISK_REGISTER.md`
- `GOVERNANCE_AMENDMENTS.md`
- `scripts/run_dev.sh` now fails fast on Alembic errors and no longer prints insecure default credentials.

---

## 4. Endpoint Authorization Inventory

Full inventory is in:

`docs/api/ENDPOINT_AUTH_INVENTORY_W1-U01.md`

Summary:

| Surface | Status |
|---------|--------|
| `/health`, `/ready`, `/api` | Public, non-sensitive |
| `/auth/login` | Public credential-establishment |
| `/auth/refresh` | Refresh token credential; rotates/revokes |
| `/auth/logout`, `/auth/ws-ticket`, `/operator/me` | Bearer |
| `/system/info` | Bearer |
| `/persistence/*` | Bearer |
| `/ingestion/*` | Bearer |
| `/market/live/*` | Bearer |
| `/ws/status` | WS ticket / authorized Bearer-capable client |
| `/ws/market` | WS ticket preferred; legacy query JWT disabled by default |

---

## 5. Evidence

### 5.1 Backend tests

Command:

```bash
cd backend
AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_DATABASE_URL='sqlite+aiosqlite:///:memory:' \
AXIOM_DATABASE_AUTO_CREATE_SCHEMA=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
python3 -m pytest
```

Result:

```text
collected 74 items
...
======================== 74 passed, 1 warning in 22.19s ========================
```

### 5.2 Backend Ruff

Command:

```bash
cd backend
ruff check .
```

Result:

```text
All checks passed!
```

### 5.3 Alembic local migration equivalent

Command:

```bash
cd backend
rm -f /tmp/axiom_w1u01_alembic.db
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w1u01_alembic.db' \
AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
python3 -m alembic upgrade head
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w1u01_alembic.db' \
python3 -m alembic current
```

Result:

```text
20260711_0004 (head)
```

Note: true PostgreSQL/GitHub CI evidence cannot be produced in the DA sandbox because Docker, `psql`, and GitHub runner access are unavailable here. W1-U01 Build Order allows a documented local equivalent if GitHub is unavailable. Operator may attach remote CI/PG evidence if ITRGA requests it.

### 5.4 Frontend tests/type/build

Command:

```bash
cd frontend
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

### 5.5 Endpoint-auth tests added

New test coverage includes:

- `tests/test_endpoint_auth.py`
- `tests/test_websocket.py` updated for authenticated `/ws/status`
- persistence/ingestion tests updated to verify `401` without token and success with Bearer.

### 5.6 UTC tests added

New test coverage:

- `tests/test_time_utc.py`

Proves timezone-aware UTC API responses across:

- operator auth path;
- candle create/read path;
- audit event path;
- ingestion run path.

---

## 6. Behavior Preservation

Preserved Wave-0 capabilities:

- login/operator session;
- refresh rotation/reuse rejection;
- WS ticket issue and `/ws/market` ticket auth;
- historical CSV ingestion after authentication;
- candle persistence/history after authentication;
- simulated live feed start/stop/status after authentication;
- chart data fetch and live update through authenticated frontend session;
- data provenance banner and `seed:synthetic` marker;
- single-uvicorn workflow.

Intentional behavior change:

- formerly public operational endpoints now return `401` without Bearer authentication.
- `/ws/status` now rejects unauthenticated clients.
- login form no longer pre-fills insecure historical credentials.

These changes are authorized by W1-U01 Component B and W0-U08 hardening posture.

---

## 7. Technical Debt / Register Updates

Updated `TECHNICAL_DEBT_REGISTER.md`:

| Item | Status |
|------|--------|
| TD-003 `/ws/status` unauthenticated | Closed W1-U01 |
| TD-010 minimal persistence API | Closed W1-U01 |
| TD-014 naive UTC timestamps | Closed W1-U01 |
| TD-015 many public endpoints | Closed W1-U01 |
| U07-OBS-1 EURUSD frame | Closed per ITRGA Wave-0 closure |
| U07-OBS-5 viewport | Remains closed; ~80-bar default window already present |
| W0-CI-C4b | Closed locally via local equivalent; remote GitHub run can be attached if required |

Still open/deferred:

- TD-005 design tokens;
- TD-008 Playwright E2E;
- TD-012 npm audit transitive dependency chain;
- TD-013 row-by-row upsert;
- TD-021 simulated-only live feed;
- TD-029 multi-timeframe UI vs M1 sim;
- TD-019 IdP/MFA horizon.

---

## 8. Risks and Unknowns

| Risk / Unknown | Status | Mitigation |
|----------------|--------|------------|
| True remote GitHub CI run not available in DA sandbox | Known unknown | Local equivalent executed; Operator/GitHub evidence may be attached |
| PostgreSQL runtime/service tests still mostly SQLite-based | Known limitation | Alembic PG is CI-configured; future Wave 1 can add PG API integration tier |
| npm audit vulnerabilities remain | Known debt | TD-012 remains open; avoid forced breaking upgrade without build order/review |
| Full RBAC/MFA absent | Deferred | Out of W1-U01 scope; future auth/security unit |
| Browser E2E not automated | Open debt | TD-008 Playwright E2E remains Wave-1 target |

---

## 9. Files Created / Major Files Modified

### Created

- `backend/app/core/time.py`
- `backend/app/services/persistence_service.py`
- `backend/tests/test_endpoint_auth.py`
- `backend/tests/test_time_utc.py`
- `docs/api/ENDPOINT_AUTH_INVENTORY_W1-U01.md`
- `docs/adr/ADR-015_API_Authorization_Breadth.md`
- `docs/adr/ADR-016_Persistence_Service_Boundary.md`
- `docs/build-orders/BUILD_ORDER_INTAKE_W1-U01.md`
- `docs/build-orders/BUILD_ORDER_W1-U01.md`
- `docs/build-orders/ITRGA_WAVE0_CLOSURE.md`

### Major modified areas

- `backend/app/api/routes/*`
- `backend/app/models/*`
- `backend/app/repositories/candle_repository.py`
- `backend/app/services/candle_service.py`
- `frontend/src/api/client.ts`
- `frontend/src/hooks/useStatusSocket.ts`
- governance docs and operator docs.

---

## 10. Confidence Statement

| Dimension | Rating | Justification |
|-----------|--------|---------------|
| Backend automated correctness | **HIGH** | 74 tests pass, including new endpoint-auth and UTC coverage |
| Frontend compatibility | **HIGH** | 16 tests pass, tsc clean, production build successful |
| Architecture fit | **HIGH** | Service boundary and ADRs align with 05 v2.0 Application Services / Persistence rules |
| Security hardening | **HIGH** | Operational endpoints and `/ws/status` now require auth; W0-U08 ticket posture preserved |
| PostgreSQL/remote CI evidence | **MODERATE** | Local equivalent proven; true remote CI/PG run unavailable in DA sandbox |
| Overall | **HIGH for implementation; MODERATE-HIGH for full ITRGA evidence package** | Remaining uncertainty is external evidence, not local failing functionality |

No percentage confidence is asserted.

---

## 11. Readiness Statement

> W1-U01 is implemented, tested, documented, and submitted for independent ITRGA review.  
> DA does **not** self-approve.  
> The next unit must not begin until ITRGA disposition and subsequent Build Order authorization.

---

**End of Delivery Report W1-U01**
