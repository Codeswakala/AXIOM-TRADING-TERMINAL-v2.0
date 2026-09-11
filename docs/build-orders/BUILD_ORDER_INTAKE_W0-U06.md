# Build Order Intake — W0-U06

| Item | Value |
|------|--------|
| Build Order | W0-U06 Frontend Live Data Integration |
| Prerequisite | W0-U05 Operator-verified (per BO) |
| Status | ACCEPTED |
| Date | 2026-07-10 |

## Hypothesis
An authenticated React WebSocket client to `/ws/market`, combined with a multi-symbol simulated feed and an institutional live dashboard (prices + feed health), will make live market intelligence usable to operators without charts or execution UI.

## Backend enablement (minimal, in scope)
W0-U05 single-symbol adapter cannot meet “≥2 concurrent symbols”. Extend LiveMarketService to run a multi-symbol simulated adapter (EURUSD + BTCUSD default) while reusing the same hub and upsert path.

## Alternatives
| Option | Decision |
|--------|----------|
| Poll REST only | Rejected — BO requires WS live updates |
| Single symbol UI | Fails DoD (≥2 symbols) |
| Multi-adapter composite | **Selected** |

## Proceed
Backend multi-symbol sim → FE hook/types → Live page → tests → ADRs → Delivery Report.
