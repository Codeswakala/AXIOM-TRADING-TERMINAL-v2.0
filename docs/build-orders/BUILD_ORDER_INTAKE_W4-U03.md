# Build Order Intake — W4-U03

| Field | Value |
|---|---|
| Build Order | W4-U03 — Regime Detection Reports |
| Wave | 4 — Institutional Intelligence |
| Intake date | 2026-07-16 |
| Authority | ITRGA Build Order after W4-U02 final approval |
| Prior verdict | `docs/build-orders/ITRGA_VERDICT_W4-U02_FINAL.md` |
| Source build order | `docs/build-orders/BUILD_ORDER_W4-U03.md` |

## DA Intake Confirmation

The Development Authority confirms receipt of W4-U02 final approval and W4-U03 Build Order.

W4-U03 authorizes persisted, audited, explainable, as-of-bounded, market-agnostic Regime Detection Reports only.

## Authorized Scope

1. Explainable rule-based regime detection over normalized backward-looking candle features.
2. New `regime_reports` table and Alembic migration.
3. Audit event on report creation.
4. Authenticated read-only regime reports API.
5. Tests for no-look-ahead, uncertainty, market-agnostic no-symbol-identity behavior, non-signal/no-mutation, persistence/audit, and dependency discipline.
6. ADR/register/docs/evidence/delivery updates.

## Explicit Boundaries

- No UI in this unit.
- No learned/clustering model.
- No per-market specialized model.
- No symbol identity as feature.
- No signal emission or signal conversion.
- No execution/order/broker/paper-trading path.
- No new unspiked dependency.
- No auto-retrain or model/advisory status mutation.

## DA Non-Approval Statement

DA may implement and validate W4-U03 but does not self-approve it. W4-U03 acceptance remains subject to operator evidence and independent ITRGA review.
