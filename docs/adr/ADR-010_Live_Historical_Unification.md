# ADR-010 — Live vs Historical Data Unification Strategy

| Field | Value |
|-------|--------|
| ID | ADR-010 |
| Title | Shared NormalizedCandleRow + CandleRepository upsert |
| Date | 2026-07-10 |
| Status | Accepted |
| Domain | Data / Architecture |

## Decision
Live and historical data share:
1. `NormalizedCandleRow` type (W0-U03)
2. Natural-key upsert on `candles` (market_class, symbol, timeframe, open_time)
3. Source labels: `csv:*` vs `live:simulated` (future `live:broker`)

## Alternatives
| Option | Outcome |
|--------|---------|
| Separate live_ticks table only | Splits query model early; deferred |
| Overwrite without natural key | Breaks history integrity |

## Consequences
- Live bars appear via existing persistence candle queries
- Dedup/upsert semantics identical to historical reloads
- HFT tick storage remains future TD
