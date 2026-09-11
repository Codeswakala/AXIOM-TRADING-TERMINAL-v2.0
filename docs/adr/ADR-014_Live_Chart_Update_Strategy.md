# ADR-014 — Live Chart Update Strategy

| Field | Value |
|-------|--------|
| ID | ADR-014 |
| Title | Forming-candle update + append; reuse U05/U06 WS contract |
| Date | 2026-07-11 |
| Status | Accepted |
| Domain | Frontend / Market Data |

## Context
Live feed emits `live_candle` messages with OHLCV + `open_time`. Charts need smooth updates without full re-fetch per tick.

## Decision
1. Historical load: `GET /persistence/candles?order=asc&limit=500`
2. Live: reuse `useLiveMarket` → filter symbol/timeframe → `mergeLiveBar`:
   - same `time` → **update** forming bar
   - greater `time` → **append**
   - older `time` → ignore (reload history for corrections)
3. Chart seed: `POST /market/live/seed-history` before stream for sparse series
4. Lightweight Charts `setData` on symbol/type switch; `update` on live ticks

## Alternatives
| Option | Outcome |
|--------|---------|
| Full re-fetch every tick | Rejected — janky / heavy |
| Separate live series overlay | Deferred complexity |
| Tick-only micro bars | Out of scope |

## Consequences
- Reuses WS auth contract (query token TD-022 remains)
- Seed is synthetic enablement, not vendor data
- Chart State holds only presentation fields

## Related
ADR-011 FE WS; ADR-010 live/historical unification; Architecture §30
