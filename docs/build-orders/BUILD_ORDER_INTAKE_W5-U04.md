# BUILD ORDER INTAKE — W5-U04

| Field | Value |
|---|---|
| Build Order | W5-U04 — Human-AI Collaboration: Signal Investigation Workspace |
| Received by DA | 2026-07-17 |
| Source artifact | `docs/build-orders/BUILD_ORDER_W5-U04.md` |
| Prerequisite verdict | `docs/build-orders/ITRGA_REVIEW_W5-U03.md` — W5-U03 APPROVED CLEAN, platform v0.41.0 |
| DA disposition | ACCEPTED FOR IMPLEMENTATION |
| Target platform version | 0.42.0 |

## Authorized scope

- Add a read-only signal investigation workspace that explains persisted advisory signal rationale, guardrails, calibrated confidence, lineage, and linked/recent intelligence reports.
- Use existing read-only APIs; add no signal mutation endpoint and no new persisted analytical artifact.
- Add mandatory UI/browser evidence commands for the served investigation view, research framing, calibrated confidence/no raw score, no action controls, and logged-out block.
- Carry no-signal-mutation keystone, R5-6, and R5-8. No assistant summary is implemented in this unit, so R5-1/R5-3/R5-5/R5-7 assistant-summary evidence is N/A beyond preserving W5-U01/W5-U02 regression tests.

## Binding constraints acknowledged

- No signal mutation, re-emission, re-grading, guardrail override, or signal write endpoint.
- No external LLM/API.
- No new compiled/LLM/tokenizer dependency.
- No execution, order, sizing, broker, account, position, or Gate-opening path.
- No raw model score rendering.
- No client-side authoritative inference/analytics/guardrail recomputation.
- No new migration expected; if no assistant summary is added, R5-7 persistence-capture is not triggered.
- DA does not self-approve and does not start W5-U05 without ITRGA approval plus a new Build Order.

## Initial implementation plan

1. Add `/investigate` frontend route and navigation item.
2. Build a presentation-only signal investigation workspace over existing signal and intelligence APIs.
3. Add frontend tests for rationale/guardrails/lineage/reports, calibrated confidence/no raw score, no action controls, and presentation-only language.
4. Add backend named test proving investigation reads mutate/trigger nothing and no signal-write endpoint exists.
5. Update ADR, evidence commands, delivery report, and governance/status registers.

