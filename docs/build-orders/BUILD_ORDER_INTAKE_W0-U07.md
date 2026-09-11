# Build Order Intake — W0-U07

| Item | Value |
|------|--------|
| Build Order | W0-U07 Live Chart Visualization Foundation |
| Date | 2026-07-11 |
| Status | ACCEPTED |
| Architecture | **05_SYSTEM_ARCHITECTURE.md v2.0** (canonical Tier 4) |
| Hierarchy | **10_CONSTITUTIONAL_HIERARCHY.md** adopted |

## Governance envelope
No trading/ML/AI on chart; presentation-only Chart State; reuse auth + WS + candle API; simulated feed only.

## Hypothesis
TradingView Lightweight Charts + ChartState (symbol/timeframe/type/viewport) + historical fetch + live WS forming-candle update will deliver institutional candlestick foundation without violating architecture §11.1/§30.

## Backend enablement (minimal)
- Ascending candle history for chart series; higher limit.
- Seed synthetic history on live feed start when series sparse (enables chart without manual CSV).

## Proceed to implementation.
