# ADR-033 — Signal Emit-Time Guardrails and Staleness

| Field | Value |
|---|---|
| Status | Accepted for implementation under W3-U03; pending ITRGA review |
| Date | 2026-07-15 |
| Deciders | Development Authority under Build Order W3-U03 |
| Related | ADR-031, ADR-032, W3-U01, W3-U02, Wave-3 plan R-2 |

## Context

W3-U01 proved deterministic inference and governed model eligibility. W3-U02 introduced an inert persisted advisory signal record and read-only signal-history API. W3-U03 matures the guardrails that decide whether an otherwise eligible model's specific signal may be cleanly emitted.

The risk is that an advisory-approved model could produce a signal that is out of its validated operating domain, poorly calibrated for the current context, economically unusable, or stale. Such a record must not be shown or stored as clean current advice.

## Decision

AXIOM adds emit-time guardrails to `AdvisorySignalService` and persists freshness metadata on `advisory_signals`.

A signal candidate is handled as follows:

- W3-U01 eligibility failures remain `withheld`.
- Additional emit-time operating-domain failures for provider, symbol, or source are `withheld` with `UNSUPPORTED_DOMAIN`.
- Input older than the configured max staleness is `withheld` with `STALE_INPUT`.
- Poor calibration from report warnings, aggregate ECE, or slice ECE becomes `warning` with `POORLY_CALIBRATED`.
- Economically unusable verdicts become `warning` with `ECONOMICALLY_UNUSABLE`.
- Signals whose validity window has elapsed become `expired` with `SIGNAL_EXPIRED`.
- The history API exposes a `current_only` read filter that returns only non-expired emitted/warning records still inside their validity window.

## Concrete freshness contract

Default values are configurable through settings:

```text
AXIOM_SIGNAL_MAX_INPUT_STALENESS_SECONDS = 300
AXIOM_SIGNAL_VALIDITY_SECONDS = 300
AXIOM_SIGNAL_CALIBRATION_WARNING_ECE_THRESHOLD = 0.15
```

The persisted signal stores:

- `input_staleness_seconds`;
- `signal_validity_seconds`;
- `expires_at`;
- `freshness_status`.

## Schema consequences

Alembic revision `20260715_0017` adds freshness fields to `advisory_signals`.

The fields are nullable for backward compatibility with W3-U02 rows, but W3-U03 service-created rows populate them.

## Boundary decisions

- The signal remains inert; no order payload or broker dispatch field is added.
- The API remains history/read-only; no signal creation endpoint is added.
- No UI, alerting, or live signal push is added.
- Expiration is implemented in the domain service and read filters; no scheduler is introduced in W3-U03.

## Consequences

### Positive

- R-2 signal staleness is closed in implementation.
- Calibrated confidence and economic verdict remain independent and visible.
- Economically unusable models cannot produce a clean `emitted` signal.
- Poor calibration cannot be hidden behind a positive score.
- Current-history reads cannot include expired records.

### Deferred

- Live market inference adapter remains W3-U04.
- Signal UI remains W3-U05.
- Alerts/live signal WebSocket stream remain W3-U06.
- Execution/broker/order behavior remains Wave 6 only.

## Review note

DA does not self-approve this ADR or W3-U03. Acceptance requires operator evidence and ITRGA review.
