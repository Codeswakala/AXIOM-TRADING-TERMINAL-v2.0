# BUILD ORDER INTAKE — W5-U02

| Field | Value |
|---|---|
| Build Order | W5-U02 — Human-AI Collaboration: Audited Assistant Research Responses |
| Received by DA | 2026-07-17 |
| Source artifact | `docs/build-orders/BUILD_ORDER_W5-U02.md` |
| Prerequisite verdict | `docs/build-orders/ITRGA_REVIEW_W5-U01.md` — W5-U01 APPROVED CLEAN, platform v0.39.0 |
| DA disposition | ACCEPTED FOR IMPLEMENTATION |
| Target platform version | 0.40.0 |

## Authorized scope

- Persist assistant grounded research responses and refusals in `assistant_research_responses`.
- Add Alembic migration, ORM model, committing repository/script, and read-only authenticated list/detail API.
- Preserve W5-U01 non-actuating registry and grounding/refusal boundary.
- Store `request_text_hash` only; do not store raw request text.
- Carry disclaimer, source/provenance, refusal reason, research status, provider/policy metadata, and audit correlation.
- Prove no-orphan audit relationship between each response row and `audit_events`.
- No UI panel in this unit; therefore R5-6 is proven by backend/API tests and stored/displayable API payloads, with browser screenshot not applicable.

## Binding constraints acknowledged

- No external LLM/API.
- No new compiled/LLM/tokenizer dependency.
- No assistant action tools.
- No POST/mutation API.
- No execution, order, sizing, broker, account, position, Gate-opening, auto-retraining, or auto-remediation path.
- DA does not self-approve and does not start W5-U03 without ITRGA approval plus a new Build Order.

## Initial implementation plan

1. Add response persistence schema and Alembic revision `20260717_0024`.
2. Route all deterministic assistant responses/refusals through a repository that commits the response row and required audit event in one transaction.
3. Add read-only `/api/v1/collaboration/assistant-responses` list/detail endpoints.
4. Add W5-U02 named tests for R5-7, R5-3, R5-5, R5-1, R5-6, R5-2, API auth/read-only behavior, no raw prompt storage, and secret-marker exclusion.
5. Update ADR, evidence commands, delivery report, and governance/status registers.

