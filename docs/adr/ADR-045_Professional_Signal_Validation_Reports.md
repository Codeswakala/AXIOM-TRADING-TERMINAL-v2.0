# ADR-045 — Professional Signal Validation Reports

| Field | Value |
|---|---|
| Status | Accepted for implementation under W4-U06; pending ITRGA review |
| Date | 2026-07-16 |
| Deciders | Development Authority under Build Order W4-U06 |
| Related | W3 advisory signals, W3 analytics raw-score exclusion, W4-U01 artifact contract, GR-1…GR-8 |

## Context

W4-U06 validates persisted advisory signal records as research context. The key risks are cherry-picking, raw-score leakage, and fabricated performance claims when governed forward outcome data is absent.

## Decision

AXIOM implements persisted `signal_validation_reports` and `SignalValidationReportService`.

The service:

- reads persisted advisory signals read-only;
- validates a declared as-of-bounded scope stored in the report config;
- includes all signals matching the declared scope and state filters;
- excludes future signals beyond `scope_end`;
- computes only metrics legitimately supported by existing signal records;
- excludes raw model score from output even when raw score exists upstream;
- reports outcome data status honestly as not available when governed forward outcomes do not exist;
- stores uncertainty and sample count on every metric;
- stores independent economic usefulness verdict;
- persists the report and writes `signal_validation_report.created` audit event;
- exposes authenticated read-only list/detail APIs.

## Metrics in W4-U06

W4-U06 computes research metrics that require no fabricated outcomes:

```text
clean_advisory_rate
guardrail_intervention_rate
calibrated_confidence_coverage
```

Each metric carries a Wilson score interval and sample count.

## Non-decisions

W4-U06 does not add UI, realized outcome/return attribution, raw-score confidence, signal emission, model mutation, execution, broker integration, or guaranteed-performance framing.

## Persistence

Alembic revision:

```text
20260716_0023_w4_u06_signal_validation_reports.py
```

The persistence-capture control applies. Operator evidence must include raw `SELECT >= 1 row` from `signal_validation_reports`, matching audit event, and no-orphan proof.

## Review note

DA does not self-approve this ADR or W4-U06. Acceptance requires operator target evidence and ITRGA review.
