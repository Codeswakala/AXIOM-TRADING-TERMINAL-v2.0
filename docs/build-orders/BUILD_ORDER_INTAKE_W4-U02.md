# Build Order Intake — W4-U02

| Field | Value |
|---|---|
| Build Order | W4-U02 — Correlation Intelligence Reports |
| Wave | 4 — Institutional Intelligence |
| Intake date | 2026-07-16 |
| Authority | ITRGA Build Order after W4-U01 approval |
| Prior review | `docs/build-orders/ITRGA_REVIEW_W4-U01.md` |
| Source build order | `docs/build-orders/BUILD_ORDER_W4-U02.md` |

## DA Intake Confirmation

The Development Authority confirms receipt of W4-U01 ITRGA approval and W4-U02 Build Order.

W4-U02 authorizes the first Wave-4 analytical feature: persisted, audited, as-of-bounded Correlation Intelligence Reports with uncertainty and read-only API access.

## Authorized Scope

1. Backend correlation service under `institutional_intelligence`.
2. No-look-ahead as-of windowing over persisted candles.
3. Uncertainty-mandatory Pearson correlation reports.
4. New `correlation_reports` table and Alembic migration.
5. Audit event on report creation.
6. Read-only authenticated API for list/detail.
7. Tests, ADR/register/docs updates, delivery report, and evidence commands.

## Explicit Boundaries

- No UI in this unit.
- No signal emission or signal conversion.
- No execution/order/broker/paper-trading path.
- No guaranteed-return framing.
- No unspiked dependencies beyond W4-U01-approved numpy/pandas/scipy; DA chooses the committed pure-Python fallback for W4-U02 implementation to avoid runtime dependency adoption.
- No D-W2-001 breach or per-market specialized model.

## DA Non-Approval Statement

DA may implement and validate W4-U02 but does not self-approve it. W4-U02 acceptance remains subject to operator evidence and independent ITRGA review.
