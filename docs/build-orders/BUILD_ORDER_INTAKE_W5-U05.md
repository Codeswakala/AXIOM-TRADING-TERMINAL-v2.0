# BUILD ORDER INTAKE — W5-U05

| Field | Value |
|---|---|
| Build Order | W5-U05 — Human-AI Collaboration: Scenario Comparison Workspace |
| Received by DA | 2026-07-17 |
| Source artifact | `docs/build-orders/BUILD_ORDER_W5-U05.md` |
| Prerequisite verdict | `docs/build-orders/ITRGA_REVIEW_W5-U04.md` — W5-U04 APPROVED CLEAN, platform v0.42.0 |
| DA disposition | ACCEPTED FOR IMPLEMENTATION |
| Target platform version | 0.43.0 |

## Authorized scope

- Add a read-only scenario comparison workspace for existing persisted W4-U04 `scenario_reports`.
- Use existing read-only scenario report APIs; add no scenario generation endpoint, no new report type, and no new persistence table.
- Display at least two persisted scenarios side by side with assumptions, hypothetical result, uncertainty, provenance/source ids, limitations, economic usefulness, and research status.
- Carry no-scenario-generation keystone, GR-7 uncertainty/no-guarantee, R5-6 browser proof, and R5-8 grep/CI.
- No assistant comparison summary is implemented in this unit, so R5-1/R5-3/R5-5/R5-7 assistant-summary evidence is N/A beyond preserving W5-U01/W5-U02 regression tests.

## Binding constraints acknowledged

- No scenario generation, computation, or new hypothetical outcome creation from this workspace.
- No scenario write/generate endpoint.
- No external LLM/API.
- No new compiled/LLM/tokenizer dependency.
- No execution, order, sizing, broker, account, position, or Gate-opening path.
- No raw model score rendering.
- No client-side authoritative scenario/analytics recomputation.
- No new migration expected; if no assistant summary is added, R5-7 persistence-capture is not triggered.
- DA does not self-approve and does not start W5-U06 without ITRGA approval plus a new Build Order.

## Initial implementation plan

1. Add `/compare-scenarios` frontend route and navigation item.
2. Build a presentation-only scenario comparison workspace over existing scenario report list/detail APIs.
3. Add frontend tests for side-by-side comparison, assumptions/uncertainty/provenance/limitations, no raw score/no guarantee/action controls, and presentation-only language.
4. Add backend named test proving scenario comparison reads create no new `scenario_reports` rows and no scenario write/generate endpoint exists.
5. Update ADR, evidence commands, delivery report, and governance/status registers.

