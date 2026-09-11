# ADR-006 — Data Validation & Deduplication Strategy

| Field | Value |
|-------|--------|
| ID | ADR-006 |
| Title | Row-level validation and natural-key upsert for candles |
| Date | 2026-07-10 |
| Status | Accepted |
| Deciders | Development Authority (W0-U03) |
| Domain | Data Engineering / Architecture |

---

## Problem Statement

Repeated historical loads and imperfect CSVs must not corrupt the candle store.

## Decision

1. **Validation (row-level):** required timestamp/OHLC; decimal parse; high≥low; high≥open/close; low≤open/close; non-negative prices/volume; invalid rows counted, not fatal if any valid rows exist.  
2. **Normalization:** symbols uppercased; market_class lowercased; timeframe uppercased; timestamps → UTC aware.  
3. **Deduplication:** upsert on natural key `(market_class, symbol, timeframe, open_time)`.  
   - missing → insert  
   - identical OHLCV → unchanged  
   - different OHLCV → update  
4. **Error policy:** `completed` | `completed_with_errors` | `failed` with sampled error messages on the run record.

## Alternatives

| Option | Why not |
|--------|---------|
| Fail entire file on first bad row | Too brittle for research CSVs |
| Blind insert ignore conflicts | Hides revisions to historical bars |
| Hash-only dedup without update | Cannot correct bad prior loads |

## Trade-offs Accepted

- No gap filling or resampling (explicit out of scope)  
- No multi-timeframe aggregation  

## Risks

- Timezone-naive CSVs assumed UTC (documented)  
- Partial updates may still require operator review of source quality  

## Future Implications

Calibration of stricter quality scores / quarantine tables can attach without changing the natural key.

---

**End of ADR-006**
