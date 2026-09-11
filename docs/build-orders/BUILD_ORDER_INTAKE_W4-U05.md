# Build Order Intake — W4-U05

| Field | Value |
|---|---|
| Build Order | W4-U05 — Portfolio/Risk Research Analytics |
| Wave | 4 — Institutional Intelligence |
| Intake date | 2026-07-16 |
| Authority | ITRGA Build Order after W4-U04 approval |
| Prior review | `docs/build-orders/ITRGA_REVIEW_W4-U04.md` |
| Source build order | `docs/build-orders/BUILD_ORDER_W4-U05.md` |

## DA Intake Confirmation

The Development Authority confirms receipt of W4-U04 approval and W4-U05 Build Order.

W4-U05 authorizes persisted, audited, hypothetical market-series Portfolio/Risk Research Analytics reports only.

## Authorized Scope

1. Hypothetical market-series risk service under Institutional Intelligence.
2. New `portfolio_risk_reports` table and Alembic migration.
3. Audit event on report creation.
4. Authenticated read-only portfolio/risk reports API.
5. Tests for no account/broker/position linkage, no-look-ahead, uncertainty/sample count, economic usefulness, non-signal/no-mutation, persistence/audit, and dependency discipline.
6. ADR/register/docs/evidence/delivery updates.

## Explicit Boundaries

- No UI in this unit.
- No account linkage, broker linkage, or live position data.
- No signal validation feature.
- No order/sizing/quantity/position payload.
- No signal emission or signal conversion.
- No execution/order/broker/paper-trading path.
- No guaranteed/expected-return framing.
- No unspiked dependency.

## DA Non-Approval Statement

DA may implement and validate W4-U05 but does not self-approve it. W4-U05 acceptance remains subject to operator evidence and independent ITRGA review.
