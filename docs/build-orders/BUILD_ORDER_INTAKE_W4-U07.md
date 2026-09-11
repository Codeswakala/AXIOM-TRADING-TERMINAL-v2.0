# Build Order Intake — W4-U07

| Field | Value |
|---|---|
| Build Order | W4-U07 — Institutional Intelligence Dashboard / Chart Context |
| Wave | 4 — Institutional Intelligence |
| Intake date | 2026-07-16 |
| Authority | ITRGA Build Order after W4-U06 approval |
| Prior review | `docs/build-orders/ITRGA_REVIEW_W4-U06.md` |
| Source build order | `docs/build-orders/BUILD_ORDER_W4-U07.md` |

## DA Intake Confirmation

The Development Authority confirms receipt of W4-U06 approval and W4-U07 Build Order.

W4-U07 authorizes the first Wave-4 operator-facing UI: a protected, presentation-only Institutional Intelligence Dashboard that reads existing W4 read-only APIs and displays persisted research reports with uncertainty and advisory framing.

## Authorized Scope

1. Protected frontend dashboard route for Institutional Intelligence.
2. Read-only consumption of existing W4 APIs: correlation, regime, scenario, portfolio/risk, and signal-validation reports.
3. Display of uncertainty and sample count for report metrics.
4. Research/not-guaranteed framing and no execution controls.
5. Frontend tests, grep evidence, browser screenshot command pack, docs/register updates, delivery report.

## Explicit Boundaries

- No backend analytical capability.
- No new persisted artifact or schema migration.
- No client-side authoritative recomputation.
- No execution/order/broker/account/position/sizing controls.
- No raw model score rendering.
- No Wave-4 closeout or Wave-5/6 work.

## DA Non-Approval Statement

DA may implement and validate W4-U07 but does not self-approve it. W4-U07 acceptance requires operator evidence, mandatory browser screenshots, and ITRGA review.
