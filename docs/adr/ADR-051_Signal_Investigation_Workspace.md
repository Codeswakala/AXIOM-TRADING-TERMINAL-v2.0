# ADR-051 — Signal Investigation Workspace

| Field | Value |
|---|---|
| Status | Accepted for W5-U04 implementation by DA; pending operator evidence / ITRGA review |
| Date | 2026-07-17 |
| Unit | W5-U04 — Human-AI Collaboration: Signal Investigation Workspace |
| Platform version | 0.42.0 |
| Builds on | W3 advisory signals and guardrails; W4 institutional reports; W5-U01/U02 safety and audit boundaries; W5-U03 chart UI precedent |

---

## Context

W5-U04 authorizes a read-only operator surface for investigating existing advisory signal records. The workspace must explain signal rationale, guardrail states, calibrated confidence, lineage, and linked/recent intelligence reports without mutating the signal or creating an action path. Because this is a UI unit, browser evidence is mandatory.

---

## Decision

Implement a frontend-only Signal Investigation Workspace at:

```text
/investigate
```

The workspace uses existing read-only APIs:

```text
GET /api/v1/signals/history
GET /api/v1/signals/history/{signal_id}
GET /api/v1/intelligence/*-reports
```

No new backend table, migration, report type, signal write endpoint, or assistant summary persistence is added.

The UI displays:

- persisted signal selector;
- rationale;
- guardrail states: state reason, operating domain, calibration status, economic verdict, freshness, expiry;
- calibrated confidence only;
- lineage: signal id, model id/version, experiment id, feature-set version, inference input hash;
- linked validation/report ids;
- recent institutional intelligence report summaries;
- research/not-instruction disclaimer.

---

## No-signal-mutation control

W5-U04 adds no signal mutation route and no code path that changes advisory signal/model state. The named backend test `test_signal_investigation_triggers_and_mutates_nothing` reads signal list/detail repeatedly and asserts:

- advisory signal row count unchanged;
- model artifact row count unchanged;
- investigated signal snapshot unchanged;
- model `status` and `advisory_status` unchanged.

The UI uses reads only and does not call signal creation/regrade/override endpoints.

---

## Presentation-only control

The workspace formats and displays persisted data only. It does not recompute inference, guardrail states, signal scores, analytics, or economic conclusions authoritatively in the browser.

Raw model score is not rendered. The UI shows calibrated confidence only.

---

## Assistant path decision

No assistant summary path is implemented in W5-U04.

Therefore, W5-U04 does not trigger new assistant persistence capture. W5-U01/W5-U02 safety tests remain in regression, but R5-1/R5-3/R5-5/R5-7 assistant-summary evidence is not applicable for this unit.

---

## Consequences

### Positive

- Operators can investigate advisory evidence in a dedicated workspace without using any mutation or action surface.
- The workspace improves traceability by co-locating rationale, guardrails, lineage, and related intelligence reports.
- Mandatory browser evidence can prove research framing, calibrated-confidence-only presentation, no raw score, and no action controls.

### Deliberately not included

- No signal mutation, re-emission, re-grade, or guardrail override.
- No signal write endpoint.
- No new analytical report type.
- No external LLM/API.
- No assistant summary.
- No new migration or persistence table.
- No execution/order/sizing/broker/account/position path.
- No Gate opening.
- No scenario comparison, trade plan, journal, or W5-U05+ feature.

---

## Validation expectations

- Backend named tests pass for no-signal-mutation, read auth/detail, absent write endpoints, and mutation grep.
- Frontend tests pass for rationale/guardrails/lineage/reports, calibrated confidence/no raw score, research framing/no action controls, presentation-only copy, and persisted-signal selector behavior.
- Alembic remains `20260717_0025 (head)` with no W5-U04 migration.
- Operator evidence includes served browser screenshots for investigation view and logged-out block.

---

**End of ADR-051**
