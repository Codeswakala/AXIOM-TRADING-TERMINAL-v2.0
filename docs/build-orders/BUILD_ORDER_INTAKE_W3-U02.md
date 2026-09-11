# Build Order Intake — W3-U02

| Field | Value |
|---|---|
| Build Order | W3-U02 — Advisory Signal Contract + Signal Persistence |
| Wave | 3 — Live Research Advisor |
| Intake date | 2026-07-15 |
| Authority | ITRGA Build Order after W3-U01 approval |
| Prior review | `docs/build-orders/ITRGA_REVIEW_W3-U01.md` |
| Source build order | `docs/build-orders/BUILD_ORDER_W3-U02.md` |

## DA Intake Confirmation

The Development Authority confirms receipt of W3-U01 ITRGA approval and W3-U02 Build Order.

W3-U02 authorizes only the backend/API advisory signal contract, persistence table, governed signal production service, read-only authenticated signal-history API, audit events, documentation, and evidence pack.

## Explicit Boundaries

- No execution, orders, positions, broker, or paper trading.
- No executable order payload in a signal record.
- No operator-facing signal UI, alert, or live WebSocket signal stream.
- No signal from an ineligible or ungoverned model.
- No opaque signal; missing rationale requires withhold.
- No raw-score-as-confidence; stored confidence must be calibrated.
- Every emitted or withheld signal must be persisted and audited.

## Authorized Implementation Scope

Implement W3-U02 Components A–F exactly as issued:

1. advisory signal DTO and PostgreSQL table;
2. governed emission/state machine using the W3-U01 eligibility gate;
3. calibrated confidence and rationale requirements;
4. read-only authenticated signal-history API;
5. inert/no-execution proof and governance documentation;
6. validation suite and operator evidence commands.

## DA Non-Approval Statement

DA may implement and validate W3-U02 but does not self-approve it. W3-U02 acceptance remains subject to operator evidence and independent ITRGA review.
