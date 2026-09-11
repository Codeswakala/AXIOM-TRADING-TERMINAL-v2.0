# Build Order Intake — W4-U06

| Field | Value |
|---|---|
| Build Order | W4-U06 — Professional Signal Validation Extension |
| Wave | 4 — Institutional Intelligence |
| Intake date | 2026-07-16 |
| Authority | ITRGA Build Order after W4-U05 approval |
| Prior review | `docs/build-orders/ITRGA_REVIEW_W4-U05.md` |
| Source build order | `docs/build-orders/BUILD_ORDER_W4-U06.md` |

## DA Intake Confirmation

The Development Authority confirms receipt of W4-U05 approval and W4-U06 Build Order.

W4-U06 authorizes persisted, audited Professional Signal Validation Reports over declared as-of-bounded scopes of persisted advisory signals.

## Authorized Scope

1. Signal-validation service under Institutional Intelligence.
2. New `signal_validation_reports` table and Alembic migration.
3. Audit event on report creation.
4. Authenticated read-only signal-validation reports API.
5. Tests for no cherry-picking, raw-score exclusion, no-look-ahead, uncertainty/sample count, outcome-data honesty, economic usefulness, no-signal/no-mutation, persistence/audit, and dependency discipline.
6. ADR/register/docs/evidence/delivery updates.

## Explicit Boundaries

- No UI in this unit.
- No fabricated outcome/performance/return data.
- No raw score in report output.
- No signal emission or signal conversion.
- No execution/order/broker/account/position path.
- No guaranteed/expected future-performance framing.
- No unspiked dependency.

## DA Non-Approval Statement

DA may implement and validate W4-U06 but does not self-approve it. W4-U06 acceptance remains subject to operator evidence and independent ITRGA review.
