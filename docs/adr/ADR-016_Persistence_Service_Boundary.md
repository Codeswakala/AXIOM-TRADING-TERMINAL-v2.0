# ADR-016 — Persistence Application Service Boundary

| Field | Value |
|-------|-------|
| ID | ADR-016 |
| Title | Route-independent persistence application service |
| Date | 2026-07-12 |
| Status | Accepted |
| Deciders | Development Authority under Build Order W1-U01 |
| Domain | Backend / Application Services / Persistence |

---

## Context

Wave 0 exposed persistence APIs primarily as verification surfaces. Some route handlers directly assembled repository/database responses, which was acceptable for foundation evidence but weaker than the canonical service-layer architecture required for Wave 1.

W1-U01 Components A and D require routers to remain thin, business/application orchestration to live in services, and persistence details to stay behind repository/service boundaries.

## Decision

Introduce `PersistenceService` as an Application Services boundary for persistence API workflows:

- candle create/list/get;
- audit-event listing;
- database statistics.

Routers now authenticate the operator, validate HTTP inputs, and delegate to the service. The service coordinates `CandleService`, `AuditRepository`, `check_database`, and query counts while keeping ORM/database details out of route handlers.

## Alternatives Considered

| Option | Outcome | Rationale |
|--------|---------|-----------|
| Leave route handlers as-is | Rejected | Would not mature W0 verification endpoints into Wave-1 service architecture. |
| Create many tiny services per endpoint | Rejected | Unnecessary fragmentation for current foundation scope. |
| Replace repositories | Rejected | Existing repository pattern is approved; W1-U01 extends before replacing. |

## Consequences

- Persistence API behavior is preserved for authenticated operators.
- The service boundary gives Wave 1 a cleaner extension point for future persistence/API hardening.
- Tests prove route parity and authorization behavior.
- No schema change is required.

## Compliance

- Aligns with `05_SYSTEM_ARCHITECTURE.md` v2.0 §11.2 Application Services and §23 Data Persistence Service.
- Closes TD-010 pending ITRGA approval.

---

**End ADR-016**
