# ADR-053 — Inert Trade Planning Workspace

| Field | Value |
|---|---|
| Status | Accepted for W5-U06 implementation by DA; pending operator evidence / ITRGA review |
| Date | 2026-07-17 |
| Unit | W5-U06 — Human-AI Collaboration: Inert Trade Planning Workspace |
| Platform version | 0.44.0 |
| Builds on | W5-U01 inert collaboration contracts; W5-U03 audited UI artifact precedent; W5-U05 final approval |

---

## Context

W5-U06 authorizes the GR-9 keystone surface: a trade planning workspace that must be structurally inert. The term "trade plan" can be confused with execution; therefore the platform must prove a plan note is a research note only and cannot become an order ticket.

---

## Decision

Add `trade_plan_notes`, an inert persisted research-note table for operator-authored planning notes.

Allowed fields:

- `plan_id`
- `created_at`
- `updated_at`
- `operator_id`
- `title`
- `market_context`
- `hypothesis`
- `linked_signal_ids`
- `linked_report_ids`
- `scenario_notes`
- `risk_notes`
- `invalidating_conditions_text`
- `decision_status`
- `research_disclaimer`
- `research_status`
- `audit_correlation_id`

No order, sizing, stop/target, broker, account, position, signal, or execution columns are present.

Creation and update are confined to `TradePlanNoteRepository`, which validates inertness, writes only the plan note store, and appends audit events:

- `trade_plan_note.created`
- `trade_plan_note.updated`

Expose API:

- `GET /api/v1/collaboration/trade-plans`
- `GET /api/v1/collaboration/trade-plans/{plan_id}`
- `POST /api/v1/collaboration/trade-plans`
- `PUT /api/v1/collaboration/trade-plans/{plan_id}`

No execution/order/signal endpoint is added.

Add a protected UI at:

```text
/trade-plans
```

The UI renders and edits research fields only, with visible not-instruction disclaimer and no order-ticket controls.

---

## Inertness controls

The trade plan factory rejects forbidden keys recursively using the W5-U01 forbidden field set:

- `order_payload`
- `order_intent`
- `side`
- `quantity`
- `lot_size`
- `order_size`
- `position_size`
- `entry_price_order`
- `stop_loss`
- `take_profit`
- `broker_account_id`
- `account_id`
- `position_id`
- `execution_status`
- `live_position`

It also rejects guaranteed-return/profit text markers and unknown payload fields.

---

## Assistant path decision

No AI-assisted trade plan drafting is implemented in W5-U06.

Therefore, W5-U06 does not trigger assistant-summary persistence capture. W5-U01/W5-U02 safety tests remain in regression, but R5-1/R5-3/R5-5 assistant-drafting evidence is not applicable for this unit.

---

## Consequences

### Positive

- Operators can keep research plan notes with linked signal/report ids.
- Notes are audited and no-orphan by construction.
- The UI makes research-only status explicit.
- Future journal/closeout units can reference plan notes without introducing execution semantics.

### Deliberately not included

- No order ticket.
- No order/sizing/stop/target/broker/account/position/execution fields.
- No execution/order/signal endpoint.
- No assistant drafting.
- No external LLM/API.
- No Gate opening.
- No journal or W5-U07+ feature.

---

## Validation expectations

- Backend tests pass for inert schema, recursive forbidden-field rejection, persistence/no-orphan audit, update audit, triggers-nothing, no execution/signal path reads, API auth/read/write behavior, and absent execute/submit endpoints.
- Frontend tests pass for research-note fields, disclaimer, linked ids, no order-ticket labels, no action controls, and plan-store create/update callbacks.
- Alembic head advances to `20260717_0026`.
- Operator evidence includes raw PostgreSQL SELECT, no-orphan audit JOIN, and served-browser screenshots.

---

**End of ADR-053**
