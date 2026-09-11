# Build Order Intake — W0-U05

| Item | Value |
|------|--------|
| Build Order | W0-U05 Real-time Market Data Adapter Foundation |
| Prerequisite | W0-U04 approved (per BO) |
| Status | ACCEPTED |
| Date | 2026-07-10 |

## Hypothesis
A pluggable `MarketDataAdapter` with a simulated live feed, reusing `NormalizedCandleRow` + candle upsert and JWT-protected REST/WS channels, will deliver live market foundation without broker/HFT/execution scope.

## Alternatives
| Option | Decision |
|--------|----------|
| Simulated adapter (deterministic) | **Selected** — no paid APIs |
| External public WS (Binance etc.) | Optional later; network-dependent |
| Full MT5/FIX | Out of scope |

## Architecture
```
MarketDataAdapter (ABC)
  └── SimulatedCandleAdapter
LiveMarketService (lifecycle, fan-out)
  → normalize/upsert via CandleRepository
  → in-memory hub for WS subscribers
API: /market/live/* (auth)
WS: /ws/market (auth token query/header)
```

## Proceed to implementation.
