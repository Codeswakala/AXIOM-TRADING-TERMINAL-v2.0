# Build Order Intake — W3-U07

| Field | Value |
|---|---|
| Build Order | W3-U07 — Performance Analytics + Confidence Visualization |
| Wave | 3 — Live Research Advisor |
| Intake date | 2026-07-16 |
| Authority | ITRGA Build Order after W3-U06 approval |
| Prior review | `docs/build-orders/ITRGA_REVIEW_W3-U06.md` |
| Source build order | `docs/build-orders/BUILD_ORDER_W3-U07.md` |

## DA Intake Confirmation

The Development Authority confirms receipt of W3-U06 ITRGA approval and W3-U07 Build Order.

W3-U07 authorizes advisory/research performance analytics and confidence visualization only. Analytics must be uncertainty-mandatory, advisory-not-guaranteed, presentation-only in the browser, read-only via authenticated API, and free of execution controls.

## Authorized Scope

1. Read-only advisory analytics endpoint over existing persisted advisory signal records.
2. Operator-facing analytics/confidence visualization UI.
3. Uncertainty shown on every metric; no false precision.
4. Calibrated confidence visualization with calibration-status/unreliability warning.
5. Advisory-not-guaranteed framing.
6. Tests, ADR/register/state/changelog updates, delivery report, and operator evidence command pack with mandatory browser screenshots.

## Explicit Boundaries

- No execution controls.
- No guaranteed-return framing.
- No client-side authoritative inference/signal/economic/statistical computation.
- No signal write/emit path.
- No persisted analytics artifact unless explicitly needed; W3-U07 implementation uses read-only aggregation over existing artifacts.
- No auto-action, broker, order, paper trading, or position behavior.

## DA Non-Approval Statement

DA may implement and validate W3-U07 but does not self-approve it. W3-U07 acceptance remains subject to operator evidence, mandatory browser screenshots, and independent ITRGA review.
