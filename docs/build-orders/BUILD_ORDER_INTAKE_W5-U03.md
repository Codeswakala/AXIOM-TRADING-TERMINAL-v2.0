# BUILD ORDER INTAKE — W5-U03

| Field | Value |
|---|---|
| Build Order | W5-U03 — Human-AI Collaboration: Chart Research Annotations & Drawing Tools |
| Received by DA | 2026-07-17 |
| Source artifact | `docs/build-orders/BUILD_ORDER_W5-U03.md` |
| Prerequisite verdict | `docs/build-orders/ITRGA_REVIEW_W5-U02.md` — W5-U02 APPROVED CLEAN, platform v0.40.0 |
| DA disposition | ACCEPTED FOR IMPLEMENTATION |
| Target platform version | 0.41.0 |

## Authorized scope

- Add inert chart research annotation/drawing persistence in `chart_research_annotations`.
- Add Alembic migration, ORM model, committing repository, and authenticated API for reads plus audited operator-authored create.
- Add presentation-only chart UI rendering persisted annotations/drawings with disclaimer and source linkage.
- Prove browser-visible annotation rendering, disclaimer, no execution/order controls, and logged-out block through the operator evidence pack.
- Carry R5-4, R5-6, R5-7, and R5-8. No AI-assisted annotation path is implemented in this unit, so R5-3/R5-5 AI-specific evidence is N/A beyond preserving W5-U01/W5-U02 tests.

## Binding constraints acknowledged

- No external LLM/API.
- No new compiled/LLM/tokenizer dependency.
- No assistant action tools.
- No annotation/drawing order, sizing, account, broker, position, signal-emission, execution, or Gate-opening payload.
- No client-side authoritative inference/analytics/signal recomputation.
- No raw-score rendering and no guaranteed/predicted-outcome framing.
- DA does not self-approve and does not start W5-U04 without ITRGA approval plus a new Build Order.

## Initial implementation plan

1. Add `chart_research_annotations` ORM/migration/repository and inert validation contract.
2. Add authenticated list/detail/create API where create writes only the annotation store and audit event.
3. Add chart page annotation layer and operator-authored inert research markup form.
4. Add backend and frontend named tests for R5-4/R5-6/R5-7/presentation-only/API behavior.
5. Update ADR, evidence commands, delivery report, and governance/status registers.

