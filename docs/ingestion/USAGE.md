# Market Data Ingestion — Usage Guide (W0-U03)

Historical **CSV only**. Live feeds are deferred.

## Sample data

| File | Market | Notes |
|------|--------|-------|
| `backend/sample_data/eurusd_h1_sample.csv` | forex / EURUSD / H1 | Standard headers |
| `backend/sample_data/btcusd_h1_sample.csv` | crypto / BTCUSD / H1 | Alias headers (`time,o,h,l,c,vol`) |

## API

Base: `/api/v1/ingestion` (also mounted without prefix on root router set).

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/v1/ingestion/sample` | Load built-in sample by filename |
| POST | `/api/v1/ingestion/csv` | Load from allowlisted path (`sample_data/` or `tests/fixtures/`) |
| GET | `/api/v1/ingestion/runs` | Recent runs |
| GET | `/api/v1/ingestion/runs/{id}` | Run detail |
| GET | `/api/v1/ingestion/stats` | Totals + last run |
| GET | `/api/v1/ingestion/candle-counts` | Filtered counts |

### Example

```bash
curl -s -X POST localhost:8000/api/v1/ingestion/sample \
  -H 'Content-Type: application/json' \
  -d '{"sample_name":"eurusd_h1_sample.csv","market_class":"forex","symbol":"EURUSD","timeframe":"H1"}'
```

## CSV requirements

Required logical columns (aliases supported):

- timestamp / time / datetime / date / open_time  
- open / o  
- high / h  
- low / l  
- close / c  
- volume / vol / v (optional)

Timestamps without timezone are treated as **UTC**.

## Migrations

```bash
cd backend
alembic upgrade head   # includes 20260710_0002 ingestion_runs
```

## Programmatic use

```python
from app.ingestion import IngestionService
# within an AsyncSession:
result = await IngestionService(session).ingest_csv(
    path="sample_data/eurusd_h1_sample.csv",
    market_class="forex",
    symbol="EURUSD",
    timeframe="H1",
)
```

## Operator verification (PostgreSQL)

See Build Order W0-U03 §7 and Delivery Report. Production must use `postgresql+asyncpg://…`.
