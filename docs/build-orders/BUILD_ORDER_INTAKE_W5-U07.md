# BUILD ORDER INTAKE — W5-U07

| Field | Value |
|---|---|
| Build Order | W5-U07 — Human-AI Collaboration: Manual Research Journal |
| Received by DA | 2026-07-17 |
| Source artifact | `docs/build-orders/BUILD_ORDER_W5-U07.md` |
| Prerequisite verdict | `docs/build-orders/ITRGA_VERDICT_W5-U06_FINAL.md` — W5-U06 APPROVED CLEAN, platform v0.44.0 |
| DA disposition | ACCEPTED FOR IMPLEMENTATION |
| Target platform version | 0.45.0 |

## Authorized scope

- Add persisted, operator-authored inert manual research journal entries in `manual_trade_journal_entries`.
- Add Alembic migration, ORM model, committing repository, authenticated read/list/detail and audited create/update API.
- Add presentation-only journal workspace UI with research/not-a-trade-record disclaimer and no broker/account/execution/fill/P&L controls.
- Carry R5-4/GR-9 inertness, R5-6 browser proof, R5-7 persistence capture, and R5-8 grep/CI.
- No AI-assisted journal drafting is implemented in this unit, so R5-1/R5-3/R5-5 AI-specific evidence is N/A beyond preserving W5-U01/W5-U02 regression tests.

## Binding constraints acknowledged

- No broker import, account linkage, execution reconciliation, fill records, P&L/realized-return claims, order/sizing/quantity/position fields, or Gate-opening path.
- No journal entry read by any execution path.
- No execution/order/signal endpoint.
- No external LLM/API.
- No new compiled/LLM/tokenizer dependency.
- No guaranteed/realized-return framing.
- DA does not self-approve and does not start W5-U08 without ITRGA approval plus a new Build Order.

## Initial implementation plan

1. Add `manual_trade_journal_entries` ORM/migration/repository and inert validation contract.
2. Add authenticated list/detail/create/update API where writes are confined to journal-store rows plus audit events.
3. Add `/journal` workspace UI over the journal-store API.
4. Add backend and frontend named tests for R5-4/R5-6/R5-7/API behavior/no-broker-record patterns.
5. Update ADR, evidence commands, delivery report, and governance/status registers.

