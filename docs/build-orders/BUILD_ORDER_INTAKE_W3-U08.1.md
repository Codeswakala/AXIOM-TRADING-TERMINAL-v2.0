# Build Order Intake — W3-U08.1

| Field | Value |
|---|---|
| Build Order | W3-U08.1 — Wave-3 Residual Hardening |
| Wave | 3 — Live Research Advisor |
| Intake date | 2026-07-16 |
| Authority | ITRGA Build Order after W3-U08 approval with observations |
| Source build order | `docs/build-orders/BUILD_ORDER_W3-U08.1_HARDENING.md` |
| Prior verdict | `docs/build-orders/ITRGA_VERDICT_W3-U08_FINAL_AND_WAVE3_CLOSURE.md` |

## DA Intake Confirmation

The Development Authority confirms receipt of W3-U08.1 residual hardening Build Order.

The scope is limited to closing the two W3-U08 observations:

1. OBS-1 — harden the SQLite StaticPool test harness so local CI is deterministically green for the right reason.
2. OBS-2 — complete the Wave-3 browser E2E screenshot archive.

## Explicit Boundaries

- No new product feature.
- No new endpoint.
- No new schema or migration.
- No execution, broker, order, paper trading, or position behavior.
- No Governance Gate change.
- No Wave-4+ work.
- No assertion deletion, xfail, or weakened test to hide the SQLite race.

## DA Non-Approval Statement

DA may implement and validate W3-U08.1, but does not self-approve residual closure. ITRGA must review the evidence and mark Wave 3 residual-free.
