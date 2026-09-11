# Observability & Metrics — W1-U02

| Item | Value |
|------|-------|
| Unit | W1-U02 |
| Service | Observability Service |
| Status | Implemented by DA; pending ITRGA review |

---

## 1. Purpose

W1-U02 establishes read-only operational telemetry for AXIOM without introducing business logic, execution, broker connectivity, ML, chart features, or new markets.

## 2. Correlation IDs

HTTP requests receive a correlation ID from `X-Correlation-ID` or a generated UUID. The value is:

- included in logs;
- returned as `X-Correlation-ID` response header;
- used by the in-process request metrics registry.

WebSocket status/market endpoints set a correlation ID per connection where practical.

## 3. Redaction

Telemetry redacts:

- Authorization Bearer values;
- access/refresh tokens;
- passwords;
- WebSocket tickets;
- PostgreSQL URLs with embedded credentials.

Tests prove raw token/password/DB credential strings do not appear in formatted logs.

## 4. Metrics endpoint

| Method | Path | Auth |
|--------|------|------|
| GET | `/api/v1/metrics` | Bearer operator auth |
| GET | `/metrics` | Bearer operator auth (compatibility mount) |

The endpoint returns JSON with:

- process uptime/pid;
- HTTP request counts, status counts, path counts, latency average/max, recent request summaries;
- database status/latency/backend/pool details;
- live-feed running/connected/message/persist/lag/subscriber metrics.

No request bodies, auth headers, tokens, passwords, or DB credentials are stored in metrics.

## 5. Health/readiness

`/health` returns liveness with timestamp and latency.

`/ready` returns per-check subsystem status and latency for:

- configuration;
- logging;
- database;
- ML stub;
- broker stub;
- market ingestion;
- authentication;
- live market.

## 6. Limitations / future work

- Metrics are process-local and reset on restart.
- Full OpenTelemetry/Grafana/distributed tracing is intentionally deferred.
- PostgreSQL API integration tier is future work; current CI validates Alembic-on-PostgreSQL and app tests in isolated SQLite.

---

**End of observability doc**
