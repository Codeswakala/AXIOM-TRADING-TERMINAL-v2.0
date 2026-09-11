# ADR-001 — Monorepo Layout with Layered Backend Packages

| Field | Value |
|-------|--------|
| ID | ADR-001 |
| Title | Monorepo layout with layered backend packages |
| Date | 2026-07-10 |
| Status | Accepted |
| Deciders | Development Authority (under Build Order W0-U01) |
| Domain | Architecture |

---

## Context

W0-U01 requires a clean repository structure aligned with the merged System Architecture (v1.1.0): Presentation, Application, Business Services, ML/Research (stub), Data, and Infrastructure.

## Decision

Adopt a **single monorepo** at repository root with:

- `frontend/` — React + TypeScript presentation layer
- `backend/app/` — FastAPI backend with internal packages:
  - `api/` — routers only
  - `core/` — configuration, logging, DI (infrastructure)
  - `services/` — application / business services
  - `models/` — Pydantic DTOs
  - `repositories/` — data access boundary (stub in W0)
  - `ml/` — ML platform boundary (stub in W0)
- `docs/` — governance, ADR/EKMS, build orders

## Alternatives Considered

1. **Separate repositories** for frontend and backend — better independent versioning, worse atomic foundation delivery and dual review overhead for Wave 0.  
2. **Flat backend module list** without layer packages — faster to start, violates architecture layering and replaceability goals.  

## Consequences

- Clear mapping from architecture document to directories.  
- Future services can be extracted without rewriting the monorepo narrative.  
- Requires discipline to keep routers thin and avoid domain logic in presentation.  

## Compliance

- SYSTEM_ARCHITECTURE.md v1.1.0  
- Build Order W0-U01  
- Design Philosophy (modularity, clean architecture)

---

**End of ADR-001**
