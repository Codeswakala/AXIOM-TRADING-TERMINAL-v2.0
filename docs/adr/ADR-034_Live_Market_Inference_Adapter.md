# ADR-034 — Live Market Inference Adapter

| Field | Value |
|---|---|
| Status | Accepted for implementation under W3-U04; pending ITRGA review |
| Date | 2026-07-15 |
| Deciders | Development Authority under Build Order W3-U04 |
| Related | W3-U01, W3-U02, W3-U03, W1 live-market seam, W2-U01 chronology guard, D-W2-001 |

## Context

W3-U04 connects AXIOM's existing simulated live-market seam to the governed inference/signal path. The critical risk is live look-ahead: an inference input must not include any candle whose `open_time` is later than the trusted as-of anchor.

This unit must not introduce a broker connection, external feed, operator signal UI, alert, or live signal push.

## Decision

AXIOM implements `LiveMarketInferenceAdapter` under `app/trading_intelligence/live_market`.

The adapter:

- uses persisted candles produced by the existing W1 simulated live-market seam and `CandleRepository` query boundary;
- builds a `LiveMarketInferenceWindow` containing only candles with `open_time <= requested_as_of_time`;
- excludes future candles and records `excluded_future_candle_count` for evidence;
- sets the inference input `as_of_time` to the freshest included candle's open time, not wall-clock query time;
- computes deterministic causal features (`return_1`, `range_pct`) from the point-in-time candle window;
- excludes identity fields from model features;
- refuses `seed:synthetic` as authoritative live inference input;
- supports deterministic scoring through the W3-U01 `LiveInferenceEngine`;
- can persist a governed live-path signal through W3-U02/W3-U03 `AdvisorySignalService`;
- adds no API route, no UI, no alert, no push channel, no broker path, and no external feed connection.

## Consequences

### Positive

- Live/near-real-time scoring now has an explicit as-of/no-look-ahead adapter.
- Future candles are structurally excluded from inference inputs.
- Stale data is naturally routed through W3-U03 `STALE_INPUT` guardrails because the input timestamp is the freshest included data timestamp.
- The live path remains governed by eligibility, signal persistence, guardrails, and staleness.
- The implementation reuses existing W1 infrastructure instead of opening a new egress surface.

### Deferred

- Operator dashboard/workspace remains W3-U05.
- Alerts/live signal stream remain W3-U06.
- External market-data-provider integration remains future gated work.
- Broker/execution remains Wave 6 only.

## Compliance

- `05_SYSTEM_ARCHITECTURE` §6: Trading Intelligence owns inference/signal logic.
- `05_SYSTEM_ARCHITECTURE` §15: no execution; operator decision/execution gate remains closed.
- `05_SYSTEM_ARCHITECTURE` §16: persistence/query through repository/session boundaries.
- `05_SYSTEM_ARCHITECTURE` §42: deterministic live scoring.
- `05_SYSTEM_ARCHITECTURE` §77: no secrets introduced.
- `07_ML_SPEC`: no look-ahead, feature traceability, and no identity-as-feature discipline preserved.

## Review note

DA does not self-approve this ADR or W3-U04. Acceptance requires operator evidence and ITRGA review.
