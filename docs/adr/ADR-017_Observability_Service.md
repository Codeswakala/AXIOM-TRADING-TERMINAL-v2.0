# ADR-017 — Observability Service Foundation

| Field | Value |
|-------|-------|
| ID | ADR-017 |
| Title | Structured observability service with redaction and correlation IDs |
| Date | 2026-07-13 |
| Status | Accepted |
| Deciders | Development Authority under Build Order W1-U02 |
| Domain | Core Platform / Observability / Security |

---

## Context

W1-U02 requires Observability Service to become a first-class Core Platform Service under `05_SYSTEM_ARCHITECTURE.md` v2.0 §26/§69/§83. Observability must be read-only telemetry, independently testable, and must never leak credentials, tokens, passwords, PII, or DB credentials.

## Decision

Implement a lightweight in-process Observability Service foundation:

- request correlation IDs via `X-Correlation-ID` or generated UUID;
- context-local correlation propagation into log formatters;
- structured JSON logs with timestamp, level, logger, component/category, correlation ID, message;
- text logs also include correlation ID for local diagnostics;
- redaction utility shared by logging and metrics paths;
- request metrics captured by HTTP middleware;
- authenticated JSON `/metrics` endpoint exposing read-only HTTP/DB/live-feed/process telemetry.

OpenTelemetry/Grafana/distributed tracing are intentionally deferred.

## Alternatives Considered

| Option | Outcome | Rationale |
|--------|---------|-----------|
| Full OpenTelemetry stack now | Deferred | Valuable later, but too much infrastructure for W1-U02 foundation scope. |
| Prometheus text metrics only | Deferred | JSON is easier to validate and consume in the current operator terminal; Prometheus export can be added later. |
| Log all request headers/body for diagnostics | Rejected | Secret-leak risk violates §77. Current middleware logs method/path/status/duration only. |

## Consequences

- Operators can correlate request logs using `X-Correlation-ID` / response header.
- Logs and metrics avoid raw headers/bodies and redact common secret patterns.
- `/metrics` requires operator Bearer authentication per W1-U01 policy.
- Metrics are process-local and reset on restart; durable telemetry backend is future work.

## Compliance

- Aligns with `05_SYSTEM_ARCHITECTURE.md` v2.0 §26, §69, §77, §83.
- Supports W1-U02 Components A–C.
- No business logic or domain mutation occurs in observability service.

---

**End ADR-017**
