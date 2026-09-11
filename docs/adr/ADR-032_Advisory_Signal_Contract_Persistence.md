# ADR-032 — Advisory Signal Contract and Persistence

| Field | Value |
|---|---|
| Status | Accepted for implementation under W3-U02; pending ITRGA review |
| Date | 2026-07-15 |
| Deciders | Development Authority under Build Order W3-U02 |
| Related | W3-U01 eligibility gate, ADR-031, Wave-3 design plan §6–§10 |

## Context

W3-U01 proved that only a fully governed, explicitly `advisory_approved` model can pass live inference eligibility, and that no execution path exists. W3-U02 is the first Wave-3 unit authorized to create a governed advisory signal record.

The signal must be an inert, persisted, auditable research/advisory record. It must not be an order, broker command, alert, WebSocket push, or UI signal surface. The signal must include lineage, deterministic inference evidence, calibrated confidence, rationale/explainability, state, and audit correlation.

## Decision

AXIOM implements an `advisory_signals` table and a Trading Intelligence signal service.

The signal service:

- reuses the W3-U01 `GovernedModelEligibilityGate` and `LiveInferenceEngine`;
- persists every decision as an `AdvisorySignal` record;
- emits only when the model is eligible, rationale exists, and calibration is not warning-state;
- withholds ineligible, out-of-domain, research-only, future/identity-invalid, and no-rationale candidates;
- marks poor calibration as `warning` instead of `emitted` certainty;
- stores calibrated confidence from calibration report bins/base rate rather than treating raw score as confidence;
- writes an append-only audit event for every emitted/withheld/warning signal;
- exposes only a read-only authenticated signal-history API.

## Schema

The `advisory_signals` table includes:

- `signal_id`, `created_at`, `as_of_time`;
- market identity fields: `market_class`, `provider`, `symbol`, `timeframe`;
- model lineage: `model_artifact_id`, `model_version`, `feature_set_version`, `experiment_id`;
- report lineage: `statistical_report_id`, `calibration_report_id`, `economic_report_id`, `generalization_report_id`;
- inference evidence: `inference_input_hash`, `raw_score`, `calibrated_confidence`;
- advisory state: `signal_direction`, `signal_state`, `state_reason`, `eligibility_reasons`;
- context: `operating_domain_status`, `calibration_status`, `economic_verdict`, `risk_notes`;
- rationale and explainability: `rationale`, `explainability_summary`, `state_transition_history`;
- `audit_correlation_id`.

It deliberately has no order payload, order intent, broker account, quantity, stop loss, take profit, or dispatch field.

## Consequences

### Positive

- First governed signal record exists only after W3-U01 eligibility passes.
- Ineligible signals are evidence-bearing `withheld` records, not silent or in-memory refusals.
- Poor calibration is surfaced as `warning` and cannot be displayed as certainty.
- Signal history is auditable and queryable without creating an emission endpoint.
- Execution boundary remains closed.

### Negative / Deferred

- No operator signal UI is implemented in W3-U02.
- No alerting or live signal WebSocket stream is implemented in W3-U02.
- Deeper emit-time guardrails for domain/calibration/economic maturation are deferred to W3-U03 as ordered.
- Live market inference adapter is deferred to W3-U04.

## Compliance

- `05_SYSTEM_ARCHITECTURE` §6: Trading Intelligence owns signals.
- `05_SYSTEM_ARCHITECTURE` §15: flow stops at Operator Decision; execution gate remains closed.
- `05_SYSTEM_ARCHITECTURE` §16: persistence occurs through ORM/session seams.
- `05_SYSTEM_ARCHITECTURE` §77: no secrets/PII stored in signal records.
- `07_ML_SPEC`: model lineage, calibration, and reproducibility evidence are preserved.
- D-W2-001: market-agnostic model governance is preserved.

## Review note

DA does not self-approve this ADR or W3-U02. Acceptance requires operator evidence and ITRGA review.
