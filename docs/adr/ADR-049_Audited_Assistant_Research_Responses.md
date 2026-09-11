# ADR-049 — Audited Assistant Research Responses

| Field | Value |
|---|---|
| Status | Accepted for W5-U02 implementation by DA; pending operator evidence / ITRGA review |
| Date | 2026-07-17 |
| Unit | W5-U02 — Human-AI Collaboration: Audited Assistant Research Responses |
| Platform version | 0.40.0 |
| Builds on | ADR-048 Collaboration Safety Foundation |

---

## Context

W5-U01 established the non-actuating deterministic assistant boundary, grounding-or-refuse policy, injection/secret refusal handling, disclaimer, and inert plan/journal contracts. W5-U01 audited assistant responses/refusals through `audit_events` but intentionally added no collaboration persistence table.

W5-U02 is authorized to give the assistant an accountable memory: grounded research responses and refusals must be stored in a dedicated table, exposed read-only, and linked to immutable audit events. The assistant remains local/deterministic and non-actuating. No external LLM/API or action tool is authorized.

---

## Decision

Add `assistant_research_responses` as an inert, audited research artifact table.

Each row stores:

- `assistant_response_id` primary key;
- UTC `created_at`;
- `operator_id` and `request_id`;
- `request_text_hash` only — no raw request/prompt text column exists;
- assistant policy/provider/model-or-engine metadata;
- `source_artifact_ids` and redacted `grounding_summary`;
- `response_text`, `refused`, `refusal_reason`, `limitations`, `disclaimer`, `research_status`;
- `audit_correlation_id` and JSON `provenance`.

Creation is allowed only through `AssistantResearchResponseRepository.create_from_response()`, which inserts the row and appends the corresponding `audit_events` record in the same outer transaction:

- grounded response: `assistant.response_draft_created`;
- refusal: `assistant.refused`.

If audit append fails, the repository raises so the response row is rolled back instead of becoming orphaned.

Expose read-only authenticated API:

- `GET /api/v1/collaboration/assistant-responses`;
- `GET /api/v1/collaboration/assistant-responses/{response_id}`.

No POST/mutation endpoint is added.

---

## Safety and governance controls

- **R5-1 non-actuation:** the assistant tool registry remains read + own-audited-artifact-write only. No action tool exists.
- **R5-2 no LLM/dependency:** no external LLM/API, tokenizer, compiled dependency, or new runtime package is added.
- **R5-3 audited refusals:** order-instruction, Gate instruction, secret exfiltration, unbounded-tool, ungrounded, and disabled-assistant refusals persist with reason codes and audit events.
- **R5-5 grounding-or-refuse:** non-refused rows require source artifact ids; ungrounded requests persist only as refusals.
- **R5-6 disclaimer:** every stored record carries the W5 assistant disclaimer in both `disclaimer` and `response_text`.
- **R5-7 persistence capture:** the new table advances Alembic head to `20260717_0024`; evidence must include raw SELECT and no-orphan audit join.
- **R5-8 wave-wide grep/CI:** every W5 unit must prove no execution/order/broker/account/Gate path and CI exit 0 via documented Git Bash invocation.

---

## Consequences

### Positive

- Assistant outputs are accountable and queryable without exposing raw request text.
- Refusals become first-class persisted safety artifacts with reason codes.
- ITRGA can verify response/audit completeness through direct SQL.
- Future UI can read from an inert API instead of invoking assistant behavior directly.

### Deliberately not included

- No assistant UI panel in W5-U02.
- No external LLM/API/provider integration.
- No prompt-generation endpoint.
- No assistant action tool.
- No trade planning, journal persistence, chart annotation, scenario workspace, execution, broker, account, position, sizing, Gate-opening, auto-retraining, or auto-remediation path.

---

## Validation expectations

- Named W5-U02 persistence/refusal/API tests pass.
- Existing W5-U01 collaboration safety tests continue to pass.
- Alembic head is `20260717_0024`.
- Operator evidence includes raw PostgreSQL SELECT from `assistant_research_responses` and a no-orphan audit join with `orphan_count = 0`.

---

**End of ADR-049**
