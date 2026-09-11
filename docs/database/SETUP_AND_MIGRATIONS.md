# AXIOM Database Setup & Migrations

| Item | Value |
|------|--------|
| Unit | W0-U02 |
| ORM | SQLAlchemy 2.0 (async) |
| Migrations | Alembic |
| Production target | PostgreSQL + asyncpg |
| Dev/test fallback | SQLite + aiosqlite |

---

## 1. Configuration

Environment variables (prefix `AXIOM_`):

| Variable | Purpose | Example |
|----------|---------|---------|
| `AXIOM_DATABASE_URL` | Async SQLAlchemy URL | `postgresql+asyncpg://axiom:axiom@localhost:5432/axiom` |
| `AXIOM_DATABASE_ECHO` | Log SQL | `false` |
| `AXIOM_DATABASE_POOL_SIZE` | Pool size (Postgres) | `5` |
| `AXIOM_DATABASE_MAX_OVERFLOW` | Overflow | `10` |
| `AXIOM_DATABASE_POOL_TIMEOUT` | Seconds | `30` |
| `AXIOM_DATABASE_AUTO_CREATE_SCHEMA` | `create_all` on startup (non-prod) | `true` |

Copy `backend/.env.example` → `backend/.env`.

### URL schemes

| Mode | URL |
|------|-----|
| PostgreSQL (recommended) | `postgresql+asyncpg://USER:PASS@HOST:5432/DB` |
| SQLite file (local sandbox) | `sqlite+aiosqlite:///./axiom_dev.db` |
| SQLite memory (tests) | `sqlite+aiosqlite:///:memory:` |

---

## 2. PostgreSQL (recommended workflow)

```bash
# Create role/database (example)
createuser axiom
createdb -O axiom axiom

export AXIOM_DATABASE_URL=postgresql+asyncpg://axiom:axiom@localhost:5432/axiom
cd backend
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

Verify:

```bash
curl -s localhost:8000/ready | jq '.checks[] | select(.name=="database")'
```

---

## 3. Alembic workflow

```bash
cd backend
source .venv/bin/activate

# Apply all migrations
alembic upgrade head

# Show current revision
alembic current

# Generate a new revision after model changes (review carefully)
alembic revision --autogenerate -m "describe_change"

# Downgrade one step
alembic downgrade -1
```

Initial revision: `alembic/versions/20260710_0001_w0_u02_core_persistence.py`

Tables created:

- `candles`
- `feature_records`
- `model_artifacts`
- `audit_events`

---

## 4. Developer notes

- **Do not** rely solely on `AUTO_CREATE_SCHEMA` in production — set it `false` and use Alembic.  
- Repository code lives under `app/repositories/`.  
- ORM models live under `app/db/models/`.  
- Minimal verification API: `/api/v1/persistence/*` (not a market ingestion pipeline).  
- Test isolation: pytest uses in-memory SQLite via `AXIOM_DATABASE_URL` in `tests/conftest.py`.

---

## 5. Future extensibility (intentionally deferred)

- Hypertable / partitioning for high-volume ticks  
- Separate feature store backend  
- Object storage for large model binaries  
- Read replicas / connection routing  

Schema keys (`market_class`, `symbol`, `timeframe`, version fields) anticipate multi-market growth without redesign.

---

**End of Database Guide**
