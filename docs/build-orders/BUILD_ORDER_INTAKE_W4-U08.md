# Build Order Intake — W4-U08

| Field | Value |
|---|---|
| Build Order | W4-U08 — Wave-4 Closeout & Hardening |
| Wave | 4 — Institutional Intelligence |
| Intake date | 2026-07-16 |
| Authority | ITRGA Build Order after W4-U07 approval with observations |
| Prior verdict | `docs/build-orders/ITRGA_VERDICT_W4-U07_FINAL.md` |
| Source build order | `docs/build-orders/BUILD_ORDER_W4-U08.md` |

## DA Intake Confirmation

The Development Authority confirms receipt of W4-U07 final approval and W4-U08 closeout Build Order.

W4-U08 is a proof and hardening unit only. The sole functional hardening item is W4-U07 OBS-1: render numeric uncertainty interval bounds on the Institutional Intelligence dashboard when persisted report data contains them.

## Explicit Boundaries

- No new analytical capability.
- No new report type.
- No new backend endpoint.
- No schema migration unless justified; none is planned.
- No execution, order, broker, account, position, sizing, auto-retrain, or auto-remediation path.
- No Wave-5/6 work.
- DA does not declare the Institutional Intelligence Layer Complete milestone.

## Authorized Scope

1. Fix W4-U07 interval-bounds display.
2. Add/adjust frontend test for numeric interval rendering.
3. Produce Wave-4 closeout evidence index and ADR.
4. Reconcile docs/registers to v0.38.0.
5. Produce W4-U08 operator evidence commands and delivery report.
