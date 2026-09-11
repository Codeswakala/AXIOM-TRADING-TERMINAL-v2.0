# ADR-036 — Monitoring and Drift Alert Policy

| Field | Value |
|---|---|
| Status | Accepted for implementation under W3-U06; pending ITRGA review |
| Date | 2026-07-15 |
| Deciders | Development Authority under Build Order W3-U06 |
| Related | W1-U02 observability, W2-U10 drift monitoring, W3-U01..W3-U05, `07_ML_SPEC` Drift Monitoring |

## Context

W3-U06 adds operator-facing monitoring alert records for market, health, and drift conditions. The critical governance boundary is that alerts may inform a human operator but must never trigger automated remediation, model mutation, retraining, order placement, or execution.

W2-U10 established that drift monitoring records are research/governance evidence and do not trigger automatic retraining. W3-U06 carries that rule into the live advisory layer.

## Decision

AXIOM implements an inert `monitoring_alerts` table and `MonitoringAlertService`.

The service can create alerts for:

- `MODEL_OUT_OF_DOMAIN`;
- `MODEL_CALIBRATION_WARNING`;
- `MODEL_ECONOMICALLY_UNUSABLE`;
- `DRIFT_DETECTED`;
- `LIVE_DATA_STALE`;
- `INFERENCE_HEALTH_DEGRADED`;
- `SIGNAL_WITHHELD`.

Every alert is persisted and audited. Alerts include type, severity, subject, evidence, lineage, acknowledgement/read-state, and audit correlation.

Acknowledgement is explicitly read-state only. It changes only alert fields (`acknowledged`, `acknowledged_at`, `acknowledged_by`) and writes an audit event. It does not mutate models, experiments, configs, signals, drift records, or execution state.

## Explicit non-decisions

W3-U06 does not implement:

- automatic retraining;
- model status changes from alerts;
- config changes from alerts;
- signal emission/withholding as an alert side-effect;
- broker/order/execution behavior;
- external notification provider integration;
- alert UI indicator.

## Consequences

### Positive

- Operators can query alert records through an authenticated API.
- Drift and degraded-health evidence is visible without crossing into automated action.
- Every alert is durable and auditable.
- No execution or remediation payload exists in the alert schema.

### Deferred

- Alert UI indicator is deferred unless explicitly authorized.
- Performance analytics and confidence visualization remain W3-U07.
- Wave-3 closeout/hardening remains W3-U08.
- Execution remains Wave 6 only.

## Review note

DA does not self-approve this ADR or W3-U06. Acceptance requires operator evidence and ITRGA review.
