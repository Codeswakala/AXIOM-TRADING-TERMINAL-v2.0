# ADR-043 — Scenario Simulation Research Reports

| Field | Value |
|---|---|
| Status | Accepted for implementation under W4-U04; pending ITRGA review |
| Date | 2026-07-16 |
| Deciders | Development Authority under Build Order W4-U04 |
| Related | W4-U01 artifact contract, W4-U02/W4-U03 persistence/audit standards, GR-1…GR-8 |

## Context

W4-U04 introduces scenario simulation as hypothetical research context. The major risk is that a scenario could be interpreted as an order, sizing directive, prediction, or guaranteed return.

## Decision

AXIOM implements persisted `scenario_reports` and `ScenarioReportService`.

The service:

- reads persisted candles read-only;
- uses as-of-bounded windows with no future data;
- stores explicit hypothetical assumptions and inputs;
- computes a simple counterfactual result with uncertainty;
- stores an independent economic-usefulness verdict;
- labels outputs hypothetical / not prediction / not instruction;
- persists the report and writes a `scenario_report.created` audit event;
- exposes authenticated read-only list/detail APIs.

## Non-decisions

W4-U04 does not add UI, portfolio/risk analytics, order sizing, signal emission, execution, broker integration, or guaranteed-return framing.

## Persistence

Alembic revision:

```text
20260716_0021_w4_u04_scenario_reports.py
```

The persistence-capture control applies. Operator evidence must include raw `SELECT >= 1 row` from `scenario_reports`, matching audit event, and no-orphan proof.

## Review note

DA does not self-approve this ADR or W4-U04. Acceptance requires operator target evidence and ITRGA review.
