# ADR-012 — State Management & UX for Real-Time Institutional Dashboards

| Field | Value |
|-------|--------|
| ID | ADR-012 |
| Title | Local hook state + table watchlist (no global store yet) |
| Date | 2026-07-10 |
| Status | Accepted |
| Domain | Frontend / UX |

## Decision
- Keep live quotes in hook-local React state (not Redux) for foundation simplicity
- Institutional dark table with flash up/down on last price
- Always-visible Feed Health bar: connection, last update, rate, lag, adapter status
- Explicit Start/Stop feed controls (operator authority)
- No charts (W0-U07)

## Alternatives
| Option | Outcome |
|--------|----------|
| Global Zustand/Redux now | Overkill for one page; deferred |
| Card grid only | Table denser for multi-symbol ops |
| Auto-start feed without control | Less operator authority |

## Consequences
- Easy to lift state to context later
- Operator must start feed unless auto_start enabled server-side
