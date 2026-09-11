# ADR-041 — Correlation Intelligence Reports

| Field | Value |
|---|---|
| Status | Accepted for implementation under W4-U02; pending ITRGA review |
| Date | 2026-07-16 |
| Deciders | Development Authority under Build Order W4-U02 |
| Related | W4-U01 artifact contract, TD-065, Wave-4 GR-1…GR-8, W2-U07 uncertainty discipline |

## Context

W4-U02 is the first Wave-4 analytical feature. It must produce correlation intelligence as research context only. A correlation report must not become a signal, action, order, remediation, or guaranteed tradable edge.

The critical controls are:

- no look-ahead: no candle after `as_of_end` can enter the result;
- uncertainty mandatory: no bare correlation coefficient;
- correlation is not causation, not a signal, and not economic usefulness;
- persistence and audit are mandatory for the new report type.

## Decision

AXIOM implements a persisted `correlation_reports` table and `CorrelationReportService` under the Institutional Intelligence bounded context.

The service:

- reads persisted candles read-only;
- builds an as-of-bounded aligned window using `open_time >= as_of_start` and `open_time <= as_of_end`;
- counts excluded future candles for evidence;
- computes Pearson correlation using the W4-U01 pure-Python fallback;
- emits an inert `correlation_report` artifact contract;
- includes uncertainty interval and sample count;
- stores statistical significance and economic usefulness as separate fields;
- stores limitations including `correlation_does_not_imply_causation` and `research_only_not_a_signal`;
- persists the report;
- writes an append-only audit event;
- exposes authenticated read-only list/detail APIs.

## Dependency decision

W4-U01 discharged TD-065 for numpy/pandas/scipy on the target, but W4-U02 uses the committed pure-Python fallback implementation. This avoids adding runtime compiled dependencies while preserving an approved path for future units.

No scikit-learn, statsmodels, or other unspiked dependency is used.

## API

```text
GET /api/v1/intelligence/correlation-reports
GET /api/v1/intelligence/correlation-reports/{report_id}
```

The API is read-only and authenticated.

## Persistence

W4-U02 adds Alembic revision:

```text
20260716_0019_w4_u02_correlation_reports.py
```

The persistence-capture control applies. Operator evidence must include:

- committing script;
- raw `psql SELECT >= 1 row` from `correlation_reports`;
- matching audit event;
- no-orphan proof.

## Non-decisions

W4-U02 does not add:

- UI;
- correlation dashboard;
- regime/scenario/risk analytics;
- signal emission;
- order/execution/broker behavior;
- guaranteed-return framing.

## Consequences

### Positive

- First Institutional Intelligence research artifact is persisted, audited, and inert.
- No-look-ahead control is tested with future-candle exclusion.
- Correlation values carry uncertainty and sample count.
- The API is read-only.

### Deferred

- Presentation UI for correlation reports is deferred to a later Build Order.
- Additional estimators such as Spearman are deferred.
- Economic usefulness assessment is not performed; it is explicitly recorded as `not_assessed`.

## Review note

DA does not self-approve this ADR or W4-U02. Acceptance requires operator target evidence and ITRGA review.
