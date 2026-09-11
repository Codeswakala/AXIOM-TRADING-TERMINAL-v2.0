# Chart Workspace (W0-U07)

## Purpose
Institutional candlestick chart: historical series + live forming-candle updates. **Presentation only** — no indicators, AI, or execution.

## Access (auth-gated)

**Canonical route:** `/charts`  
**Alias:** `/chart` (same page; kept for BO wording)

1. Sign in at `/login`
2. Open **Chart Workspace** (`/charts`)
3. **Seed history** (optional) or **Start live feed** (seeds + streams)
4. Switch symbol (EURUSD / BTCUSD), timeframe (M1/M5/H1/D1), chart type (Candles/Line/Area)

Logged-out users are redirected to `/login` (same guard as `/live`).

### Data provenance (ITRGA C-2)
| `source` value | Meaning |
|----------------|---------|
| `seed:synthetic` | **Non-authoritative** synthetic bars for chart context only |
| `live:simulated` | Simulated live feed ticks (not a real broker) |
| CSV ingest labels | Operator-loaded historical files |

The chart toolbar shows a **Data provenance** banner listing bar counts by source.

## Architecture
```
ChartState (symbol, timeframe, chartType, viewport)
  → useChartData (fetch history + merge live WS)
  → PriceChart (lightweight-charts render only)
```

Live path reuses `useLiveMarket` → `POST /api/v1/auth/ws-ticket` → `/ws/market?ticket=…`; candle persistence APIs require Bearer authentication.

## APIs used
| Method | Path | Role |
|--------|------|------|
| GET | `/api/v1/persistence/candles?order=asc` | Historical series |
| POST | `/api/v1/market/live/seed-history` | Synthetic seed bars |
| POST | `/api/v1/market/live/start\|stop` | Simulated feed control |
| WS | `/ws/market` | Live candles |

## Windows PowerShell (single uvicorn)

```powershell
cd frontend
npm install
npm run build

cd ..\backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open http://localhost:8000/login → Chart Workspace.

## Operator browser evidence (Level-I for ITRGA)
Capture screenshots:
1. Historical candles rendered  
2. Two frames showing live candle update/append  
3. Symbol/timeframe switch  
4. Logged-out `/charts` and `/live` redirect to login  

## Performance note
Lightweight Charts is used for efficient `update` on the last bar. Aim for smooth interaction; heavy analytics remain server-side by design.
