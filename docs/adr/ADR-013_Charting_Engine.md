# ADR-013 — Charting Engine Choice

| Field | Value |
|-------|--------|
| ID | ADR-013 |
| Title | TradingView Lightweight Charts for institutional candlestick foundation |
| Date | 2026-07-11 |
| Status | Accepted |
| Domain | Frontend / Chart State (Architecture §30) |

## Context
W0-U07 requires professional candlestick rendering with live updates, dark theme, and no analytical computation in the presentation layer. `07_UI_UX_SPEC` / UI_UX corpus names TradingView Lightweight Charts as the primary engine.

## Decision
Adopt **lightweight-charts v4** in React via a thin presentation component (`PriceChart`) that only maps series data.

## Alternatives
| Option | Pros | Cons | Outcome |
|--------|------|------|---------|
| Lightweight Charts | Spec-aligned, performant, free for TV LC | Limited drawings vs Advanced Charts | **Selected** |
| TradingView Advanced Charts widget | Richer tools | License/weight; out of scope features | Deferred |
| Custom Canvas/D3 | Full control | Costly, reinvent series/time scale | Rejected |
| Chart.js | Familiar | Poor financial candle DX | Rejected |

## Consequences
- Fast institutional candle/line/area toggles
- Drawing tools / indicators deferred (scope)
- Client remains presentation-only (no signal calc)

## Related
Architecture v2.0 §30 Chart State; UI_UX chart philosophy; ADR-014
