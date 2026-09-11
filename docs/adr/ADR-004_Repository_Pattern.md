# ADR-004 — Repository Pattern and Session Boundaries

| Field | Value |
|-------|--------|
| ID | ADR-004 |
| Title | Generic async repository pattern with service orchestration |
| Date | 2026-07-10 |
| Status | Accepted |
| Deciders | Development Authority (Build Order W0-U02) |
| Domain | Architecture / Backend |

---

## Context

Clean Architecture requires isolation of persistence from API and domain services. Future waves will add many entities (signals, experiments, approvals). A consistent data-access pattern is required.

## Decision

1. Introduce `BaseRepository[ModelT]` with `get_by_id`, `list`, `count`, `add`, `add_many`, `delete`.  
2. Provide concrete repositories: `CandleRepository`, `FeatureRepository`, `ModelArtifactRepository`, `AuditRepository`.  
3. Application services (e.g. `CandleService`) orchestrate repositories and write audit events.  
4. Session lifecycle:
   - FastAPI dependency `get_db_session` commits on success / rolls back on error.  
   - `session_scope()` for non-HTTP use (tests, scripts).  
5. Routers remain thin; no SQL in route handlers beyond dependency injection.

## Alternatives Considered

1. **Active Record only (models with save methods)** — couples domain to ORM; harder to replace.  
2. **CQRS from day one** — overkill for foundation; deferred.  
3. **Unit of Work object separate from session** — valuable later; AsyncSession already acts as UoW for W0.

## Consequences

- New entities require: ORM model + repository (+ optional service/API).  
- Transactions span service operations sharing one session.  
- Repository layer is replaceable (e.g. future specialized time-series store) without changing API contracts.

## Compliance

- SYSTEM_ARCHITECTURE.md backend layering  
- DA Manual engineering standards  
- W0-U02 deliverables

---

**End of ADR-004**
