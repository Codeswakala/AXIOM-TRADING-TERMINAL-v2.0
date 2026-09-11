# ADR-002 — Environment Configuration and Structured Observability

| Field | Value |
|-------|--------|
| ID | ADR-002 |
| Title | Environment-aware configuration and structured logging foundation |
| Date | 2026-07-10 |
| Status | Accepted |
| Deciders | Development Authority (under Build Order W0-U01) |
| Domain | Backend / Infrastructure |

---

## Context

The architecture requires externalized, environment-specific configuration and observability (structured logs, health checks). Secrets must never be hardcoded.

## Decision

1. Use **pydantic-settings** with `AXIOM_` environment prefix and optional `.env` file.  
2. Provide `/health` (liveness) and `/ready` (readiness with explicit subsystem stubs).  
3. Implement category-aware logging adapters (`SYSTEM`, `API`, …) with text or JSON formatters.  
4. Use FastAPI dependency injection for `Settings` and services.  

## Alternatives Considered

1. **Plain os.environ dict** — simple but weak validation and poor typing.  
2. **Full OpenTelemetry + metrics stack in W0** — valuable later, out of scope and premature for foundation unit.  

## Consequences

- Configuration is testable and validated.  
- Readiness honestly reports deferred subsystems as `stub` rather than faking “green” dependencies.  
- Observability can expand to OpenTelemetry in later waves without replacing the logging boundary.  

## Compliance

- SYSTEM_ARCHITECTURE.md (configuration, observability, security)  
- AXIOM_SPEC testing/security standards  
- Build Order W0-U01 success criteria  

---

**End of ADR-002**
