# ADR-003 — Database Technology and Async Access

| Field | Value |
|-------|--------|
| ID | ADR-003 |
| Title | PostgreSQL target with SQLAlchemy 2.0 async + Alembic |
| Date | 2026-07-10 |
| Status | Accepted |
| Deciders | Development Authority (Build Order W0-U02) |
| Domain | Architecture / Backend / Data |

---

## Context

W0-U02 requires a production-grade persistence foundation supporting multi-market time-series growth, governance audit records, and future feature/model registries. The architecture specifies PostgreSQL as the primary database.

## Decision

1. **Target RDBMS:** PostgreSQL (async driver `asyncpg`).  
2. **ORM:** SQLAlchemy 2.0 style mapped classes with `AsyncSession`.  
3. **Migrations:** Alembic with async `env.py`, initial revision `20260710_0001`.  
4. **Local/test fallback:** `sqlite+aiosqlite` when PostgreSQL is unavailable (dev sandbox / CI isolation).  
5. **Schema bootstrap:** Non-production may call `metadata.create_all` for convenience; **Alembic remains the evolution authority**.

## Alternatives Considered

1. **Sync SQLAlchemy only** — simpler, but blocks the async FastAPI event loop under load; rejected for long-term path.  
2. **Raw asyncpg without ORM** — maximum control, higher maintenance and weaker migration ergonomics for multi-entity foundation; rejected for W0.  
3. **NoSQL first (e.g. Mongo)** — poor fit for relational governance, FK integrity, and SQL analytics path; rejected.  
4. **Postgres-only with no SQLite fallback** — ideal purity, fails closed environments without a server; dual-mode chosen for engineering continuity.

## Consequences

- Production configuration must set `AXIOM_DATABASE_URL=postgresql+asyncpg://...`.  
- SQLite is acceptable for tests and constrained sandboxes but is **not** the production store.  
- JSON columns used for extensible payloads (features, metrics, audit details) pending specialized stores.  
- Pool stats introspection differs by dialect (documented as best-effort).

## Compliance

- SYSTEM_ARCHITECTURE.md v1.1.0 (PostgreSQL, repositories, observability)  
- Build Order W0-U02  
- Design Philosophy (modularity, replaceability)

---

**End of ADR-003**
