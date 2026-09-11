# AXIOM Backend

FastAPI backend for AXIOM Wave 3 Live Research Advisor. Current DA implementation adds a live market inference adapter that reuses the existing simulated live-market seam with as-of/no-look-ahead discipline; execution and broker paths remain closed.

## Quick start

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Set a strong AXIOM_JWT_SECRET_KEY and explicit bootstrap credentials if needed.
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

See `../docs/database/SETUP_AND_MIGRATIONS.md` for PostgreSQL and migration workflow.

## Endpoint authorization

W1-U01 narrows the public surface. Public endpoints are limited to `/health`, `/ready`, `/api`, `/api/v1/auth/login`, and `/api/v1/auth/refresh` (refresh token credential). Operational endpoints require Bearer authentication.

See `../docs/api/ENDPOINT_AUTH_INVENTORY_W1-U01.md`.

## Selected endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/health` | Public | Liveness |
| GET | `/ready` | Public | Readiness |
| GET | `/system/info` | Bearer | Platform identity |
| GET | `/api/v1/metrics` | Bearer | Read-only observability metrics |
| GET | `/api/v1/persistence/stats` | Bearer | DB backend + counts |
| POST | `/api/v1/persistence/candles` | Bearer | Sample candle create |
| GET | `/api/v1/persistence/candles` | Bearer | List candles by symbol |
| GET | `/api/v1/persistence/audit-events` | Bearer | Recent audit events |
| GET | `/api/v1/signals/history` | Bearer | Read-only persisted advisory signal history; supports `current_only=true` |
| GET | `/api/v1/signals/history/{signal_id}` | Bearer | Read one persisted advisory signal |
| GET | `/api/v1/alerts` | Bearer | List inert monitoring alerts |
| GET | `/api/v1/alerts/{alert_id}` | Bearer | Read one monitoring alert |
| POST | `/api/v1/alerts/{alert_id}/ack` | Bearer | Acknowledge alert read-state only |
| GET | `/api/v1/analytics/advisory-performance` | Bearer | Read-only advisory analytics with uncertainty |
| GET | `/api/v1/intelligence/correlation-reports` | Bearer | Read-only correlation intelligence reports |
| GET | `/api/v1/intelligence/correlation-reports/{report_id}` | Bearer | Read one correlation report |
| GET | `/api/v1/intelligence/regime-reports` | Bearer | Read-only regime detection reports |
| GET | `/api/v1/intelligence/regime-reports/{report_id}` | Bearer | Read one regime report |
| GET | `/api/v1/intelligence/scenario-reports` | Bearer | Read-only scenario simulation reports |
| GET | `/api/v1/intelligence/scenario-reports/{report_id}` | Bearer | Read one scenario report |
| GET | `/api/v1/intelligence/portfolio-risk-reports` | Bearer | Read-only portfolio/risk research reports |
| GET | `/api/v1/intelligence/portfolio-risk-reports/{report_id}` | Bearer | Read one portfolio/risk report |
| GET | `/api/v1/intelligence/signal-validation-reports` | Bearer | Read-only professional signal validation reports |
| GET | `/api/v1/intelligence/signal-validation-reports/{report_id}` | Bearer | Read one signal validation report |
| GET | `/api/v1/intelligence/signal-validation-reports` | Bearer | Read-only professional signal validation reports |
| GET | `/api/v1/intelligence/signal-validation-reports/{report_id}` | Bearer | Read one signal validation report |
| POST | `/api/v1/ingestion/sample` | Bearer | Ingest built-in historical CSV sample |
| POST | `/api/v1/ingestion/csv` | Bearer | Ingest allowlisted CSV path |
| GET | `/api/v1/ingestion/runs` | Bearer | Recent ingestion runs |
| GET | `/api/v1/ingestion/stats` | Bearer | Ingestion + candle totals |
| POST | `/api/v1/auth/login` | Public | Operator login |
| POST | `/api/v1/auth/refresh` | Refresh credential | Rotate refresh/access tokens |
| POST | `/api/v1/auth/ws-ticket` | Bearer | Issue short-lived WS ticket |
| GET | `/api/v1/operator/me` | Bearer | Current operator |
| GET/POST | `/api/v1/market/live/*` | Bearer | Simulated live feed control/status |
| WS | `/ws/status?ticket=...` | WS ticket | Scoped status channel |
| WS | `/ws/market?ticket=...` | WS ticket | Live candles |

Interactive docs: `http://localhost:8000/docs` in non-production environments.

## Tests

```bash
cd backend
pytest -q
ruff check .
```

Tests use in-memory SQLite (`sqlite+aiosqlite:///:memory:`) for isolation. CI/Operator evidence should also exercise Alembic against PostgreSQL.

## Architecture notes

- Configuration: `app/core/config.py`
- UTC time utilities: `app/core/time.py`
- Logging: `app/core/logging.py`
- DI: `app/core/dependencies.py`
- DB engine/session: `app/db/session.py`
- ORM models: `app/db/models/`
- Repositories: `app/repositories/`
- Services hold application/domain logic; routers remain thin
- `app/services/persistence_service.py` is the W1-U01 persistence application-service boundary
- `app/ml` contains the governed Wave-2 research framework
- `app/trading_intelligence` contains W3 live inference, advisory signal, and live-market inference adapter services
