# ADR-009 — Live Market Data Adapter Architecture

| Field | Value |
|-------|--------|
| ID | ADR-009 |
| Title | Pluggable MarketDataAdapter with simulated foundation feed |
| Date | 2026-07-10 |
| Status | Accepted |
| Domain | Market Data / Architecture |

## Decision
- Abstract `MarketDataAdapter` with `start/stop/status`
- Concrete `SimulatedCandleAdapter` for foundation (no paid/network APIs)
- `LiveMarketService` owns lifecycle, persistence, and hub fan-out
- Auth-protected REST under `/api/v1/market/live/*`
- Auth-protected WebSocket `/ws/market?token=...`

## Alternatives
| Option | Outcome |
|--------|---------|
| Direct Binance public WS | Network/flaky in CI; deferred |
| MT5/FIX now | Out of scope |
| Tick-only store | Out of scope; candles unify with historical |

## Consequences
- Live path testable offline
- New brokers = new adapter implementations
- Auto-start optional via `AXIOM_LIVE_MARKET_AUTO_START`
