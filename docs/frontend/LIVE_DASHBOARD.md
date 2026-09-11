# Frontend Live Dashboard

## Access

1. Sign in at `/login` with configured operator credentials.
2. Open **Live Market** in the sidebar (`/live`).
3. Click **Start feed** (starts multi-symbol simulated adapter).
4. Prices for **EURUSD** and **BTCUSD** update via authenticated WebSocket tickets.

Unauthenticated users are redirected to login; the live hook does not connect without an operator session.

## Architecture

```text
AuthProvider (JWT)
  → ProtectedRoute
    → LiveMarketPage
      → useLiveMarket
        → POST /api/v1/auth/ws-ticket
        → WS /ws/market?ticket=...
        → REST stats/start/stop with Bearer
      → FeedHealthBar
      → LivePriceTable
```

## Single-process run (Windows PowerShell)

```powershell
cd frontend
npm install
npm run build

cd ..\backend
.\.venv\Scripts\Activate.ps1
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open **http://localhost:8000/login** → Live Market.

## Config

`AXIOM_LIVE_MARKET_SYMBOLS=EURUSD,BTCUSD` (backend `.env`)

---

**End of live dashboard doc**
