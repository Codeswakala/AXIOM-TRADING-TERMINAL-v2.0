# ADR-035 — Advisory Dashboard UX

| Field | Value |
|---|---|
| Status | Accepted for implementation under W3-U05; pending ITRGA review |
| Date | 2026-07-15 |
| Deciders | Development Authority under Build Order W3-U05 |
| Related | W3-U02 signal history API, W3-U03 guardrails/staleness, W3-U04 live inference adapter, design-plan R-3 |

## Context

W3-U05 is AXIOM's first operator-facing advisory signal UI. It is the first time governed advisory signal records are visible to a human operator. The primary governance risk is overtrust or action-framing: the UI must not present research as an instruction and must not contain execution controls.

## Decision

AXIOM adds a protected `AdvisorySignalsPage` under the existing authenticated terminal layout.

The page:

- reads the existing read-only signal-history API;
- displays signal list and detail views;
- shows signal state, calibrated confidence, rationale, guardrail status, economic verdict, freshness/expiry, and lineage;
- visibly distinguishes `warning`, `withheld`, `expired`, and `superseded` from clean advisory records;
- displays a visible research-advisory disclaimer;
- exposes filters for market, symbol, timeframe, and signal state;
- performs presentation and formatting only;
- does not recompute inference, signal, calibration, or economic logic;
- adds no signal write/emit endpoint;
- adds no alert or live signal push;
- adds no execution control.

## UX framing

The disclaimer text is intentionally visible near the top of the workspace:

```text
Research advisory only. This screen is not financial advice, not a trade instruction, and not an automated action surface. Operator judgment remains required.
```

The UI avoids action verbs and controls that could imply trading execution. The only buttons are read-only navigation/selection and refresh controls.

## Consequences

### Positive

- Operators can inspect governed advisory signals, warnings, withheld records, expired records, rationale, and lineage.
- R-3 advisory-not-instruction framing is implemented in the first operator-facing UI.
- Guardrail outcomes are visible and distinct.
- The read-only architecture is preserved.

### Deferred

- Alerts and live signal push remain W3-U06.
- Deeper analytics remain W3-U07.
- Execution remains Wave 6 and is not represented in this UI.

## Review note

DA does not self-approve this ADR or W3-U05. Acceptance requires operator-run tests, real browser screenshots, and ITRGA review.
