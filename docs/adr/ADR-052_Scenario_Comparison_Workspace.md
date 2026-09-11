# ADR-052 — Scenario Comparison Workspace

| Field | Value |
|---|---|
| Status | Accepted for W5-U05 implementation by DA; pending operator evidence / ITRGA review |
| Date | 2026-07-17 |
| Unit | W5-U05 — Human-AI Collaboration: Scenario Comparison Workspace |
| Platform version | 0.43.0 |
| Builds on | W4-U04 scenario reports; W5-U01/U02 assistant safety/audit boundaries; W5-U04 UI no-mutation precedent |

---

## Context

W5-U05 authorizes a read-only operator surface to compare existing persisted W4-U04 `scenario_reports` side by side. The workspace must display assumptions, hypothetical result, uncertainty, provenance/source ids, limitations, economic usefulness, and research status while creating no new scenario and computing no new hypothetical outcome. Because this is a UI unit, browser evidence is mandatory.

---

## Decision

Implement a frontend-only Scenario Comparison Workspace at:

```text
/compare-scenarios
```

The workspace uses existing read-only APIs:

```text
GET /api/v1/intelligence/scenario-reports
GET /api/v1/intelligence/scenario-reports/{report_id}
```

No new backend table, migration, report type, scenario write/generate endpoint, or assistant summary persistence is added.

The UI displays at least two existing scenario reports side by side:

- scenario name;
- symbol/timeframe/as-of context;
- hypothetical return and counterfactual index as persisted values;
- assumptions;
- uncertainty interval/method/sample count;
- source artifact ids and input lineage policy;
- economic-usefulness verdict;
- limitations such as `not_a_prediction` and `not_a_trade_instruction`;
- research/not-guaranteed disclaimer.

---

## No-scenario-generation control

W5-U05 adds no scenario generation path. The workspace performs read-only fetches and presentation formatting only.

The named backend test `test_scenario_comparison_reads_existing_reports_and_creates_no_rows` reads the existing scenario list/detail repeatedly and asserts the `scenario_reports` row count is unchanged before/after comparison reads.

The implementation includes no route or UI action to create, compute, generate, re-run, or persist a new scenario.

---

## Presentation-only and no-guarantee control

The workspace does not recompute scenario results, uncertainty, economic usefulness, or analytics authoritatively in the browser. It formats already persisted fields for comparison.

Raw model score fields are filtered from compact value display and are not rendered. The visible framing is hypothetical research only: not a prediction, not guaranteed, not an instruction, and AXIOM does not act.

---

## Assistant path decision

No assistant comparison summary path is implemented in W5-U05.

Therefore, W5-U05 does not trigger new assistant persistence capture. W5-U01/W5-U02 safety tests remain in regression, but R5-1/R5-3/R5-5/R5-7 assistant-summary evidence is not applicable for this unit.

---

## Consequences

### Positive

- Operators can compare persisted scenario research artifacts without generating new scenarios.
- Assumptions, uncertainty, provenance, and limitations are visible side by side.
- The UI adds collaboration value while preserving W4-U04 scenario-report governance.
- Browser evidence can prove not-guaranteed framing and absence of action controls.

### Deliberately not included

- No new scenario generation/computation.
- No scenario write/generate endpoint.
- No new report type.
- No external LLM/API.
- No assistant summary.
- No new migration or persistence table.
- No execution/order/sizing/broker/account/position path.
- No Gate opening.
- No trade plan, journal, closeout, or W5-U06+ feature.

---

## Validation expectations

- Backend named tests pass for no-scenario-generation, read auth/detail, absent write/generate endpoints, no comparison migration, and generation-path grep.
- Frontend tests pass for side-by-side scenarios, assumptions/uncertainty/provenance/limitations, hypothetical/not-guaranteed framing, no raw score, no action controls, and presentation-only language.
- Alembic remains `20260717_0025 (head)` with no W5-U05 migration.
- Operator evidence includes served browser screenshots for scenario comparison view and logged-out block.

---

**End of ADR-052**
