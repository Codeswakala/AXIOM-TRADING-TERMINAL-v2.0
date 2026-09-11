# ADR-037 — Performance Analytics and Confidence Visualization

| Field | Value |
|---|---|
| Status | Accepted for implementation under W3-U07; pending ITRGA review |
| Date | 2026-07-16 |
| Deciders | Development Authority under Build Order W3-U07 |
| Related | W2-U07 statistical validation, W2-U08 calibration, W3-U02/W3-U03 signals/guardrails, W3-U05 advisory UI |

## Context

W3-U07 adds operator-facing advisory analytics and confidence visualization. The central risk is operator overtrust: a bare metric or confidence number can imply certainty or guaranteed future performance.

W2-U07 established that statistical outputs require uncertainty. W2-U08 established that confidence must be calibrated. W3-U05 established advisory-not-instruction UI framing. W3-U07 carries these rules into analytics.

## Decision

AXIOM implements a read-only backend analytics endpoint and a protected frontend analytics view.

The backend endpoint:

```text
GET /api/v1/analytics/advisory-performance
```

aggregates existing `advisory_signals` records and returns:

- advisory metrics with sample count and Wilson score interval uncertainty;
- calibrated confidence bands;
- calibration status;
- confidence unreliability flag;
- economic context;
- advisory-not-guaranteed disclaimer;
- source notes.

The frontend `/analytics` route displays this payload without client-side authoritative recomputation.

## Non-decisions

W3-U07 does not add:

- persisted analytics snapshot artifacts;
- guaranteed or promised outcome analytics;
- client-side metric/CI/calibration/economic recomputation;
- signal write/emit routes;
- execution controls;
- broker/order/paper-trading behavior.

## Consequences

### Positive

- Every headline analytics metric has uncertainty and sample count.
- Confidence visualization is calibrated and warns when unreliable.
- Analytics are visibly advisory research, not guaranteed future results.
- The UI remains presentation-only.

### Deferred

- Persisted analytics snapshot archival is deferred unless a future Build Order requires it.
- Advanced outcome attribution requires a future governed outcome data contract.
- Wave-3 closeout/hardening remains W3-U08.

## Review note

DA does not self-approve this ADR or W3-U07. Acceptance requires operator evidence, browser screenshots, and ITRGA review.
