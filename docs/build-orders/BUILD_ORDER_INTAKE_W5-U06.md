# BUILD ORDER INTAKE — W5-U06

| Field | Value |
|---|---|
| Build Order | W5-U06 — Human-AI Collaboration: Inert Trade Planning Workspace |
| Received by DA | 2026-07-17 |
| Source artifact | `docs/build-orders/BUILD_ORDER_W5-U06.md` |
| Prerequisite verdict | `docs/build-orders/ITRGA_VERDICT_W5-U05_FINAL.md` — W5-U05 APPROVED CLEAN, platform v0.43.0 |
| DA disposition | ACCEPTED FOR IMPLEMENTATION |
| Target platform version | 0.44.0 |

## Authorized scope

- Add persisted, operator-authored inert trade plan research notes in `trade_plan_notes`.
- Add Alembic migration, ORM model, committing repository, authenticated read/list/detail and audited create/update API.
- Add presentation-only trade planning workspace UI with research/not-instruction disclaimer and no order-ticket controls.
- Carry R5-4/GR-9 inertness, R5-6 browser proof, R5-7 persistence capture, and R5-8 grep/CI.
- No AI-assisted plan drafting is implemented in this unit, so R5-1/R5-3/R5-5 AI-specific evidence is N/A beyond preserving W5-U01/W5-U02 regression tests.

## Binding constraints acknowledged

- No order, sizing, quantity, stop/target, broker, account, position, execution, or signal payload fields.
- No plan note read by any execution path.
- No execution/order/signal endpoint.
- No external LLM/API.
- No new compiled/LLM/tokenizer dependency.
- No guaranteed/expected-return framing.
- DA does not self-approve and does not start W5-U07 without ITRGA approval plus a new Build Order.

## Initial implementation plan

1. Add `trade_plan_notes` ORM/migration/repository and inert validation contract.
2. Add authenticated list/detail/create/update API where writes are confined to plan-store rows plus audit events.
3. Add `/trade-plans` planning UI over the plan-store API.
4. Add backend and frontend named tests for R5-4/R5-6/R5-7/API behavior/no-order-ticket patterns.
5. Update ADR, evidence commands, delivery report, and governance/status registers.

