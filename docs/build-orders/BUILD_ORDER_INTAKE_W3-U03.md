# Build Order Intake — W3-U03

| Field | Value |
|---|---|
| Build Order | W3-U03 — Operating-Domain + Calibration/Economic Guardrails at Emit Time (+ signal staleness) |
| Wave | 3 — Live Research Advisor |
| Intake date | 2026-07-15 |
| Authority | ITRGA Build Order after W3-U02 approval |
| Source build order | `docs/build-orders/BUILD_ORDER_W3-U03.md` |

## DA Intake Confirmation

The Development Authority confirms receipt of `docs/build-orders/BUILD_ORDER_W3-U03.md`.

The Build Order states it is issued by ITRGA following W3-U02 approval and operator authorization. DA treats this Build Order as the controlling Tier-8 authorization for W3-U03 implementation.

## Authorized Scope

Implement emit-time guardrails for persisted advisory signals only:

1. operating-domain guardrail at emit time;
2. calibration guardrail at emit time;
3. economic-verdict guardrail at emit time;
4. signal freshness/staleness contract;
5. governance documentation/register updates and R-2 closure;
6. tests, validation, delivery report, and operator evidence command pack.

## Explicit Boundaries

- No execution, orders, broker, paper trading, or order payload.
- No operator-facing signal UI, alerts, or live WebSocket signal push.
- No live market inference adapter.
- No W3-U04/W3-U05/W3-U06/Wave-6 functionality.
- Signal-history API remains read-only and authenticated.

## DA Non-Approval Statement

DA may implement and validate W3-U03 but does not self-approve it. W3-U03 acceptance remains subject to operator evidence and independent ITRGA review.
