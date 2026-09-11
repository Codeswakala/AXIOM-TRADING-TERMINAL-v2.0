# ADR-011 — Frontend Live Data Consumption & WebSocket Integration

| Field | Value |
|-------|--------|
| ID | ADR-011 |
| Title | Authenticated browser WebSocket client with reconnection |
| Date | 2026-07-10 |
| Status | Accepted |
| Domain | Frontend / Market Data |

## Decision
- Hook `useLiveMarket` opens `ws://…/ws/market?token=<JWT>` when authenticated
- Exponential backoff reconnect on unexpected close
- Parse `live_candle` into per-symbol quote map; track rate / last update / lag hint
- REST start/stop/stats for adapter control; WS for streaming updates
- Live route `/live` behind existing `ProtectedRoute`

## Alternatives
| Option | Outcome |
|--------|---------|
| REST polling only | Rejected — BO requires WS live updates |
| Cookie-auth WS only | Browser WS lacks easy custom headers; query token retained (TD noted) |
| Third-party WS library | Deferred — native WebSocket sufficient |

## Consequences
- Token may appear in proxy logs (TD-022)
- Multi-symbol requires backend multi adapter (delivered)
