# ADR-054 — Manual Research Journal

| Field | Value |
|---|---|
| Status | Accepted for W5-U07 implementation by DA; pending operator evidence / ITRGA review |
| Date | 2026-07-17 |
| Unit | W5-U07 — Human-AI Collaboration: Manual Research Journal |
| Platform version | 0.45.0 |
| Builds on | W5-U01 inert contract pattern; W5-U06 trade plan notes; W3/W4 read-only artifacts |

---

## Context

W5-U07 authorizes a manual research journal: operator-authored reflection entries linked to plans/signals/reports. The keystone is that a journal is a research log, not a broker record. It must not import or reconcile broker/account/execution/fill data, claim P&L/realized returns, or become an execution/account surface.

---

## Decision

Add `manual_trade_journal_entries`, an inert persisted research-log table.

Allowed fields:

- `journal_id`
- `created_at`
- `operator_id`
- `title`
- `reflection_text`
- `linked_plan_id`
- `linked_signal_ids`
- `linked_report_ids`
- `emotion_tags`
- `process_tags`
- `lesson_notes`
- `research_disclaimer`
- `research_status`
- `audit_correlation_id`

No broker, account, execution, fill, order, sizing, position, P&L, or realized-return columns are present.

Creation and update are confined to `ManualJournalEntryRepository`, which validates inertness, writes only the journal store, and appends audit events:

- `manual_trade_journal_entry.created`
- `manual_trade_journal_entry.updated`

Expose API:

- `GET /api/v1/collaboration/journal-entries`
- `GET /api/v1/collaboration/journal-entries/{journal_id}`
- `POST /api/v1/collaboration/journal-entries`
- `PUT /api/v1/collaboration/journal-entries/{journal_id}`

No execution/order/signal endpoint is added.

Add a protected UI at:

```text
/journal
```

The UI renders and edits research reflection fields only, with visible not-a-trade-record disclaimer and no broker/account/execution/fill/P&L controls.

---

## Inertness controls

The journal factory rejects forbidden keys recursively, including:

- order/sizing fields from the W5-U01 collaboration forbidden set;
- `broker_import`, broker identifiers, execution identifiers/status;
- fill identifiers/prices/quantities/timestamps;
- P&L/realized-return fields;
- account-balance fields.

It also rejects P&L, broker-import, fill-price, realized-return, and guaranteed-return text markers.

---

## Assistant path decision

No AI-assisted journal drafting is implemented in W5-U07.

Therefore, W5-U07 does not trigger assistant-summary persistence capture. W5-U01/W5-U02 safety tests remain in regression, but R5-1/R5-3/R5-5 assistant-drafting evidence is not applicable for this unit.

---

## Consequences

### Positive

- Operators can persist research reflections linked to plan/signal/report ids.
- Entries are audited and no-orphan by construction.
- The UI makes research-only status explicit.
- Future closeout can validate Wave-5 inert collaboration surfaces.

### Deliberately not included

- No broker import or account linkage.
- No execution/fill/P&L/realized-return fields.
- No order/sizing/position fields.
- No execution/order/signal endpoint.
- No assistant drafting.
- No external LLM/API.
- No Gate opening.
- No W5-U08 closeout work.

---

## Validation expectations

- Backend tests pass for inert schema, recursive forbidden-field rejection, no-P&L/no-broker-import rejection, persistence/no-orphan audit, update audit, triggers-nothing, no execution/signal path reads, API auth/read/write behavior, and absent execute/submit endpoints.
- Frontend tests pass for reflection fields, disclaimer, linked ids/tags/lessons, no forbidden record labels, no import/action controls, and journal-store create/update callbacks.
- Alembic head advances to `20260717_0027`.
- Operator evidence includes raw PostgreSQL SELECT, no-orphan audit JOIN, and served-browser screenshots.

---

**End of ADR-054**
