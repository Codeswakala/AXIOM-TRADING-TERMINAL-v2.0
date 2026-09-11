# Build Order Intake — W4-U04

| Field | Value |
|---|---|
| Build Order | W4-U04 — Scenario Simulation Research Reports |
| Wave | 4 — Institutional Intelligence |
| Intake date | 2026-07-16 |
| Authority | ITRGA Build Order after W4-U03 approval and OBS-1 closure |
| Prior review | `docs/build-orders/ITRGA_REVIEW_W4-U03.md` |
| OBS closure | `docs/build-orders/ITRGA_VERDICT_W4-U03_OBS1_CLOSURE.md` |
| Source build order | `docs/build-orders/BUILD_ORDER_W4-U04.md` |

## DA Intake Confirmation

The Development Authority confirms receipt of W4-U03 approval/OBS closure and W4-U04 Build Order.

W4-U04 authorizes persisted, audited, hypothetical Scenario Simulation Research Reports only.

## Authorized Scope

1. Hypothetical/counterfactual scenario service under Institutional Intelligence.
2. New `scenario_reports` table and Alembic migration.
3. Audit event on report creation.
4. Authenticated read-only scenario reports API.
5. Tests for no-look-ahead, hypothetical framing, assumptions/uncertainty, economic usefulness, inert/no-sizing/no-action behavior, persistence/audit, and dependency discipline.
6. ADR/register/docs/evidence/delivery updates.

## Explicit Boundaries

- No UI in this unit.
- No portfolio/risk or signal-validation feature.
- No order/sizing/quantity/stop/target payload.
- No signal emission or signal conversion.
- No execution/order/broker/paper-trading path.
- No guaranteed/expected-return framing.
- No unspiked dependency.

## DA Non-Approval Statement

DA may implement and validate W4-U04 but does not self-approve it. W4-U04 acceptance remains subject to operator evidence and independent ITRGA review.
