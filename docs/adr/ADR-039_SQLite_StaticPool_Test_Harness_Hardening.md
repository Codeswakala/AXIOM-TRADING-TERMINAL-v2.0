# ADR-039 — SQLite StaticPool Test Harness Hardening

| Field | Value |
|---|---|
| Status | Accepted for implementation under W3-U08.1; pending ITRGA residual-closure review |
| Date | 2026-07-16 |
| Deciders | Development Authority under Build Order W3-U08.1 |
| Related | W3-U08 OBS-1, `tests/test_live_market.py::test_live_start_stop_and_status`, `scripts/local_ci.sh` |

## Context

ITRGA approved W3-U08 and closed Wave 3, but carried OBS-1: `local_ci.sh` intermittently failed in the SQLite test harness with `aiosqlite` / `sqlite3` `no active connection` during `test_live_market.py::test_live_start_stop_and_status`.

The failure was proven unrelated to PostgreSQL target behavior and product logic. The root cause is the in-memory SQLite `StaticPool` harness sharing a single async connection between request-scoped writes and the background live-market adapter writer.

## Decision

AXIOM adds a SQLite-StaticPool-only serialization guard in `app.db.session` and uses the same guard around the live-market background writer.

The guard:

- activates only when the configured database is SQLite with `:memory:`;
- serializes request-scoped sessions, `session_scope`, and live-market background persistence against the same per-event-loop async lock;
- does not affect PostgreSQL;
- does not remove or weaken the affected test;
- does not xfail or skip the test;
- does not alter production/PostgreSQL persistence behavior.

## Files changed

```text
backend/app/db/session.py
backend/app/market/live_service.py
```

## Consequences

### Positive

- The SQLite `StaticPool` single-connection race is removed at the correct lifecycle boundary.
- The live-market endpoint test remains meaningful and continues to assert behavior.
- PostgreSQL behavior remains unchanged.
- `local_ci.sh` can become deterministically green rather than merely lucky.

### Tradeoff

- SQLite in-memory test DB work is serialized more strictly. This is acceptable because the serialization applies only to the single-connection test harness.

## Governance note

This is a test-harness / SQLite lifecycle hardening correction only. It adds no product capability, endpoint, schema, execution path, broker path, or Governance Gate change.
