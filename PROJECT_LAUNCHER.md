# AXIOM Project Launcher

| Item | Value |
|------|--------|
| Document | `PROJECT_LAUNCHER.md` |
| Audience | Operators / developers running AXIOM on their own machine |
| Primary OS | **Windows 10/11 + VS Code + PowerShell** |
| Platform version covered | 0.9.0 (Wave 1 W1-U01 service/API hardening) |
| Last updated | 2026-07-10 |

This guide walks you from a clean Windows machine to a running AXIOM terminal (API + UI), including login, historical CSV ingestion, and the simulated live market feed.

---

## 1. What you will run

AXIOM is a monorepo:

```
axiom/
  backend/     # FastAPI (Python)
  frontend/    # React + TypeScript (Vite)
  docs/        # Governance & guides
  scripts/     # Helpers (bash scripts are for Linux/macOS; use PowerShell steps below on Windows)
```

**Recommended on Windows (single process):**

1. Build the frontend once
2. Start **one** uvicorn server
3. Open **http://localhost:8000** (UI + API)

**Optional (two processes):** backend on port 8000 + `npm run dev` on port 5173 for hot UI reload.

---

## 2. Prerequisites (install once)

| Tool | Why | Check in PowerShell |
|------|-----|---------------------|
| **Python 3.11+** | Backend | `python --version` |
| **Node.js 18+ / 20+** and **npm** | Frontend build | `node --version` ; `npm --version` |
| **Git** (optional) | Clone/update repo | `git --version` |
| **PostgreSQL 14+** (recommended) | Production-like DB | `psql --version` |
| **VS Code** | Editor / integrated terminal | — |

### 2.1 Open PowerShell in the project

In VS Code:

1. **File → Open Folder…** → select the `axiom` folder
2. **Terminal → New Terminal**
3. Ensure the shell is **PowerShell** (not Git Bash, unless you prefer it)

```powershell
# Confirm you are in the project root (folder that contains backend\ and frontend\)
Get-Location
dir
```

You should see `backend`, `frontend`, `docs`, `PROJECT_LAUNCHER.md`, etc.

---

## 3. One-time backend setup

```powershell
cd backend

# Create virtual environment
python -m venv .venv

# Activate (PowerShell)
.\.venv\Scripts\Activate.ps1
```

If activation is blocked by execution policy:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create environment file:

```powershell
Copy-Item .env.example .env
notepad .env
# or: code .env
```

### 3.1 Database URL (choose A or B)

#### Option A — SQLite (fastest first run, no Postgres)

In `.env`:

```env
AXIOM_ENVIRONMENT=development
AXIOM_DATABASE_URL=sqlite+aiosqlite:///./axiom_dev.db
AXIOM_DATABASE_AUTO_CREATE_SCHEMA=true
```

#### Option B — PostgreSQL (recommended once installed)

1. Start PostgreSQL (Windows Services: **postgresql-x64-…** → Running).
2. Open **SQL Shell (psql)** or:

```powershell
# Adjust path/version if needed
& "C:\Program Files\PostgreSQL\16\bin\psql.exe" -U postgres
```

3. In `psql`:

```sql
CREATE USER axiom WITH PASSWORD 'axiom_dev_password';
CREATE DATABASE axiom OWNER axiom;
GRANT ALL PRIVILEGES ON DATABASE axiom TO axiom;
\q
```

4. In `.env`:

```env
AXIOM_ENVIRONMENT=development
AXIOM_DATABASE_URL=postgresql+asyncpg://axiom:axiom_dev_password@localhost:5432/axiom
AXIOM_DATABASE_AUTO_CREATE_SCHEMA=false
```

**Important:** URL must use `postgresql+asyncpg://` (not plain `postgresql://`).

If the password has special characters (`@`, `#`, `%`, …), URL-encode them (e.g. `@` → `%40`).

### 3.2 Auth secrets (W0-U08 hardened)

Also in `.env` (**required** for normal start):

```env
# Secret length >= 32 characters; do not use CHANGE-ME markers
AXIOM_JWT_SECRET_KEY=replace-with-a-long-random-secret-at-least-32-chars

# Local-only escape hatch (never production):
# AXIOM_ALLOW_INSECURE_DEV=true

# Bootstrap admin is OFF by default. Enable only with a strong password:
AXIOM_BOOTSTRAP_ADMIN_ENABLED=true
AXIOM_BOOTSTRAP_ADMIN_USERNAME=admin
AXIOM_BOOTSTRAP_ADMIN_PASSWORD=Choose-A-Strong-Local-Password-9
```

If JWT secret is missing/weak and `ALLOW_INSECURE_DEV` is false, the API **refuses to start**.

### 3.3 Live market defaults (optional)

```env
AXIOM_LIVE_MARKET_ENABLED=true
AXIOM_LIVE_MARKET_AUTO_START=false
AXIOM_LIVE_MARKET_CLASS=forex
AXIOM_LIVE_MARKET_SYMBOL=EURUSD
AXIOM_LIVE_MARKET_SYMBOLS=EURUSD,BTCUSD
AXIOM_LIVE_MARKET_TIMEFRAME=M1
AXIOM_LIVE_MARKET_INTERVAL_SECONDS=2.0
```

### 3.4 Apply database migrations

With venv **activated** and still in `backend`:

```powershell
# If using Postgres, ensure the same URL is visible to Alembic:
$env:AXIOM_DATABASE_URL = "postgresql+asyncpg://axiom:axiom_dev_password@localhost:5432/axiom"
# For SQLite you can skip setting it if .env already has the sqlite URL.

alembic upgrade head
```

Expected revisions include:

- `20260710_0001` — core tables
- `20260710_0002` — ingestion runs
- `20260710_0003` — operators

---

## 4. One-time frontend setup

Open a second PowerShell terminal in VS Code (**split terminal** is fine), or reuse after deactivating the venv.

```powershell
cd frontend
npm install
```

---

## 5. Recommended launch: single process (UI + API)

### 5.1 Build frontend

```powershell
cd frontend
npm run build
```

This creates `frontend\dist\`, which the backend serves.

### 5.2 Start backend (serves API + built UI)

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 5.3 Open in browser

| URL | Purpose |
|-----|---------|
| http://localhost:8000/login | Operator login |
| http://localhost:8000/ | Operations dashboard (after login) |
| http://localhost:8000/docs | Swagger API docs |
| http://localhost:8000/health | Liveness |
| http://localhost:8000/ready | Readiness (DB, auth, live market, …) |

### 5.4 Login (local bootstrap only)

Use the explicit bootstrap/operator credentials configured in `backend/.env`:

```env
AXIOM_BOOTSTRAP_ADMIN_ENABLED=true
AXIOM_BOOTSTRAP_ADMIN_USERNAME=admin
AXIOM_BOOTSTRAP_ADMIN_PASSWORD=Choose-A-Strong-Local-Password-9
```

The historical `admin/admin123` shortcut is blocked unless `AXIOM_ALLOW_INSECURE_DEV=true` is explicitly enabled for isolated local/test use.

---

## 6. Optional launch: two processes (hot UI reload)

**Terminal 1 — API**

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 — UI dev server**

```powershell
cd frontend
npm run dev
```

Open: **http://localhost:5173**
Vite proxies API calls to port 8000.

---

## 7. Smoke checks (PowerShell)

With the API running:

```powershell
# Health
Invoke-RestMethod http://localhost:8000/health | ConvertTo-Json

# Ready
Invoke-RestMethod http://localhost:8000/ready | ConvertTo-Json -Depth 6

# Login
$login = Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/v1/auth/login `
  -ContentType "application/json" `
  -Body '{"username":"admin","password":"<configured-bootstrap-password>"}'
$token = $login.tokens.access_token
$headers = @{ Authorization = "Bearer $token" }

# Who am I?
Invoke-RestMethod http://localhost:8000/api/v1/operator/me -Headers $headers | ConvertTo-Json

# Historical sample ingestion
Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/v1/ingestion/sample `
  -Headers $headers -ContentType "application/json" `
  -Body '{"sample_name":"eurusd_h1_sample.csv","market_class":"forex","symbol":"EURUSD","timeframe":"H1"}' `
  | ConvertTo-Json -Depth 6

# Start simulated live feed
Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/v1/market/live/start `
  -Headers $headers | ConvertTo-Json -Depth 6

Start-Sleep -Seconds 5

# Live stats
Invoke-RestMethod http://localhost:8000/api/v1/market/live/stats -Headers $headers | ConvertTo-Json -Depth 6

# Candles (includes live + historical)
Invoke-RestMethod "http://localhost:8000/api/v1/persistence/candles?symbol=EURUSD&timeframe=M1&limit=5" `
  | ConvertTo-Json -Depth 6

# Stop live feed
Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/v1/market/live/stop `
  -Headers $headers | ConvertTo-Json
```

---

## 8. Run tests (optional but recommended)

### Backend

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pytest -q
```

### Frontend

```powershell
cd frontend
npm test
npm run build
```

---

## 9. Daily “already set up” checklist

```powershell
# 1) Start Postgres if you use it (Services app), or rely on SQLite

# 2) Backend
cd backend
.\.venv\Scripts\Activate.ps1
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 3) If you changed frontend code and use single-process mode, rebuild:
# cd ..\frontend
# npm run build
# then restart uvicorn
```

Browser: http://localhost:8000/login

---

## 10. Feature map (what works in Wave 0)

| Capability | How |
|------------|-----|
| Login / session | UI `/login` or `POST /api/v1/auth/login` |
| Operations dashboard | UI after login |
| Historical CSV load | `POST /api/v1/ingestion/sample` (samples under `backend\sample_data\`) |
| Live simulated market | UI **Live Market** or `POST /api/v1/market/live/start` (auth) |
| Live WebSocket | `POST /api/v1/auth/ws-ticket` then `ws://localhost:8000/ws/market?ticket=<ticket>` |
| Live dashboard | http://localhost:8000/live (after login) |
| Chart workspace | http://localhost:8000/charts (after login) — candlestick + live |
| API docs | http://localhost:8000/docs |

**Not included yet:** real broker/MT5 connectors, full charting engine, ML training, live automated trading.

---

## 11. Troubleshooting (Windows)

| Problem | Fix |
|---------|-----|
| `Activate.ps1` cannot be loaded | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `python` not found | Install Python and tick “Add to PATH”; try `py -3 -m venv .venv` |
| `pip` / package errors | Ensure venv is activated (`(.venv)` in prompt) |
| Port 8000 in use | `uvicorn app.main:app --port 8001 --reload` (adjust URLs) |
| `Connection refused` (Postgres) | Start PostgreSQL service; check port 5432 |
| `password authentication failed` | Fix user/password in `AXIOM_DATABASE_URL` |
| `database "axiom" does not exist` | Create DB in `psql` (section 3.1 B) |
| Login works but UI blank | Run `npm run build` in `frontend` for single-process mode |
| Frontend “Unreachable” on 5173 | Start backend on 8000 first |
| JWT / secret warning in logs | Set a strong `AXIOM_JWT_SECRET_KEY` in `.env` |
| Live feed not running | Call `/market/live/start` or set `AXIOM_LIVE_MARKET_AUTO_START=true` |

Stop the server: focus the uvicorn terminal and press **Ctrl+C**.

---

## 12. Related documentation

| Doc | Purpose |
|-----|---------|
| `README.md` | Project overview |
| `docs/auth/SETUP.md` | Authentication details |
| `docs/database/SETUP_AND_MIGRATIONS.md` | DB & Alembic |
| `docs/ingestion/USAGE.md` | Historical CSV ingestion |
| `docs/market/LIVE_ADAPTER_USAGE.md` | Live simulated adapter |
| `PROJECT_STATE.md` | Current wave / unit status |
| `docs/governance/` | Vision, architecture, specs |

---

## 13. Security reminders for operators

1. Never commit `.env` or real passwords.
2. Use explicit strong bootstrap/operator credentials; never rely on historical demo defaults.
3. Set a long random `AXIOM_JWT_SECRET_KEY`.
4. Prefer PostgreSQL for serious verification; SQLite is for local demos.
5. Wave 0 live data is **simulated** unless a future unit adds real brokers.

---

## 14. Minimal “copy-paste” first launch (SQLite)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Ensure AXIOM_DATABASE_URL=sqlite+aiosqlite:///./axiom_dev.db in .env
alembic upgrade head

cd ..\frontend
npm install
npm run build

cd ..\backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Then open **http://localhost:8000/login** and sign in with the credentials configured in `backend/.env`.

---

**End of PROJECT_LAUNCHER.md**

*AXIOM Development Authority — operator runbook for Windows PowerShell / VS Code.*
