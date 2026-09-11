# Build Order Intake — W3-U04

| Field | Value |
|---|---|
| Build Order | W3-U04 — Live Market Inference Adapter |
| Wave | 3 — Live Research Advisor |
| Intake date | 2026-07-15 |
| Authority | ITRGA Build Order after W3-U03 approval |
| Prior review | `docs/build-orders/ITRGA_REVIEW_W3-U03.md` |
| Source build order | `docs/build-orders/BUILD_ORDER_W3-U04.md` |

## DA Intake Confirmation

The Development Authority confirms receipt of W3-U03 ITRGA approval and W3-U04 Build Order.

W3-U04 authorizes only the backend live market inference adapter that reuses the existing W1 simulated live-market/persistence query seam, assembles point-in-time inference inputs, routes them through W3-U01/W3-U02/W3-U03 governed logic, and prepares evidence.

## Authorized Scope

1. Live market inference adapter reusing existing W1 seam.
2. As-of / no-look-ahead input assembly.
3. Stale live data withholding via W3-U03 staleness contract.
4. Deterministic live scoring.
5. Governed path integration for persisted live-path signal records.
6. ADR, register/state/changelog updates, tests, delivery report, evidence commands.

## Explicit Boundaries

- No execution, orders, positions, broker, or paper trading.
- No external market-data-provider/feed connection.
- No operator signal UI, alert, or live signal WebSocket push.
- No W3-U05/W3-U06/Wave-6 functionality.
- Signal-history API remains read-only and authenticated.

## DA Non-Approval Statement

DA may implement and validate W3-U04 but does not self-approve it. W3-U04 acceptance remains subject to operator evidence and independent ITRGA review.
