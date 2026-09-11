# ADR-048 — Collaboration Safety Foundation

| Field | Value |
|---|---|
| Status | Accepted for implementation under W5-U01; pending ITRGA review |
| Date | 2026-07-16 |
| Deciders | Development Authority under Build Order W5-U01 |
| Related | Wave-5 Design Plan, R5-1…R5-8, GR-9…GR-11 |

## Context

Wave 5 introduces Human-AI Collaboration. The highest risks are a generative assistant that acts, leaks secrets, hallucinates ungrounded claims, or produces trade instructions, and trade plan/journal surfaces that drift into order tickets.

W5-U01 is the safety foundation before rich interaction or any external LLM.

## Decision

AXIOM implements a `collaboration` bounded context with:

- provider-neutral `AssistantPort`;
- deterministic `RuleBasedGroundedAssistant` and `NullAssistant`;
- `AssistantToolRegistry` with only read and own-audited-artifact-write tool modes;
- grounding-or-refuse policy;
- prompt-injection and secret-exfiltration refusals;
- assistant response/refusal audit events in existing `audit_events`;
- inert trade plan and manual journal contracts.

No external LLM/API, compiled dependency, collaboration table, UI, or product feature is introduced in W5-U01.

## Persistence decision

W5-U01 is contract-only for plan/journal and uses existing `audit_events` for assistant response/refusal audit. No new collaboration table is introduced; therefore no Alembic migration is added and R5-7 persistence-capture for new collaboration tables is not triggered in this unit.

Future units that persist assistant responses, annotations, trade plans, or journal entries must add Alembic migrations and first-submission raw SELECT + no-orphan audit proof.

## Non-actuation policy

No assistant tool may:

- place orders;
- size positions;
- call brokers;
- open the Governance Gate;
- mutate models/config/signals;
- fetch external data;
- write outside the assistant's own audited research artifact boundary.

## Review note

DA does not self-approve this ADR or W5-U01. Acceptance requires operator target evidence and ITRGA review.
