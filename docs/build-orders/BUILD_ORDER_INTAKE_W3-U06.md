# Build Order Intake — W3-U06

| Field | Value |
|---|---|
| Build Order | W3-U06 — Monitoring, Drift & Health Alerts |
| Wave | 3 — Live Research Advisor |
| Intake date | 2026-07-15 |
| Authority | ITRGA Build Order after W3-U05 approval |
| Prior review | `docs/build-orders/ITRGA_REVIEW_W3-U05.md` |
| Source build order | `docs/build-orders/BUILD_ORDER_W3-U06.md` |

## DA Intake Confirmation

The Development Authority confirms receipt of W3-U05 ITRGA approval and W3-U06 Build Order.

W3-U06 authorizes inert persisted monitoring alerts for market, health, and drift conditions, plus authenticated alert read/query/ack read-state API, audit, documentation, tests, and evidence.

## Authorized Scope

1. Market/health monitoring alerts using existing observability/live state.
2. Drift alerts surfaced from W2-U10 drift monitoring records.
3. Inert alert contract/table with audit events.
4. Authenticated alerts API for list/query and acknowledgement read-state only.
5. ADR/register/state/changelog updates.
6. Tests, delivery report, and operator evidence commands.

## Explicit Boundaries

- No automatic retraining.
- No model/config mutation from monitoring.
- No signal emission/withholding side effect from alerts.
- No remediation side effect.
- No execution, orders, broker, paper trading, or positions.
- No alert UI indicator unless separately authorized; W3-U06 implementation remains backend/API only.
- No external notification provider integration.

## DA Non-Approval Statement

DA may implement and validate W3-U06 but does not self-approve it. W3-U06 acceptance remains subject to operator evidence and independent ITRGA review.
