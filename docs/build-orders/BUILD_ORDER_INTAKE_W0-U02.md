# Build Order Intake Assessment — W0-U02

| Item | Value |
|------|--------|
| Build Order ID | W0-U02 |
| Title | Core Persistence Layer Foundation |
| Wave / Unit | Wave 0 — Foundation / Unit 02 |
| Issued By | ITRGA |
| Date Issued | 2026-07-10 |
| Intake By | Development Authority |
| Intake Date | 2026-07-10 |
| Status | ACCEPTED — IMPLEMENTATION AUTHORIZED |
| Prerequisite | W0-U01 (cited as approved by ITRGA in this Build Order) |

---

## 1. Acknowledgement

The Development Authority acknowledges receipt of Build Order **W0-U02** and accepts authorization to implement the foundational persistence layer within the defined scope.

---

## 2. Objectives Understood

1. Production-grade persistence layer per architecture  
2. Repository + data access separation  
3. PostgreSQL integration + pooling  
4. Alembic migrations  
5. Initial domain entities (Candle, Feature, ModelMetadata, AuditLog)  
6. Real DB health/readiness  
7. CRUD + transactions  
8. EKMS ADRs + debt/decision updates  
9. Tests + observability  
10. Multi-market / time-series extensibility preserved  

---

## 3. Scope Boundaries

| In Scope | Out of Scope |
|----------|--------------|
| SQLAlchemy + async engine | Market data ingestion pipelines |
| Alembic initial migration | Trading / signal logic |
| Base + concrete repositories | Advanced partitioning |
| Candle, Feature, ModelMetadata, AuditLog | Auth user models |
| Health DB connectivity | Production seeding / large-scale tuning |
| Unit + integration tests | ML training/inference |
| Docs + Delivery Report | Broker / external feeds |

---

## 4. Architecture Alignment

```
API / Services
      ↓
Repositories (interfaces + concrete)
      ↓
SQLAlchemy ORM models + session/unit-of-work
      ↓
PostgreSQL (dev/prod) | SQLite async (test isolation fallback)
```

Presentation remains non-authoritative. ML package remains stub.

---

## 5. Key Engineering Decisions (pre-ADR)

| Topic | Preferred approach | Rationale |
|-------|--------------------|-----------|
| ORM | SQLAlchemy 2.0 | Industry standard, async support, Alembic native |
| Driver | asyncpg (Postgres); aiosqlite (tests) | Async preferred per BO |
| Migrations | Alembic | Explicit schema versioning |
| Pattern | Generic repository + entity repos | Replaceable data layer |
| Test DB | SQLite in-memory async when Postgres unavailable; Postgres when configured | Isolation + CI friendliness |

---

## 6. Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| No PostgreSQL daemon in sandbox | Medium | Dual-mode: Postgres URL or SQLite test mode; document |
| Async + Alembic complexity | Medium | Sync migration env with async runtime pattern (standard) |
| Over-modeling future domains | Medium | Minimal columns; extensible JSON/metadata fields |
| Enhanced Investigation Standards doc not in workspace | Medium | Apply BO-stated EVF/discipline analysis in Delivery Report |

---

## 7. Implementation Plan

1. Dependencies + settings (`DATABASE_URL`, pool)  
2. DB engine/session lifecycle  
3. ORM models + Alembic  
4. Repositories + service wiring  
5. Health/readiness real checks + pool stats  
6. Optional minimal API for sample CRUD evidence  
7. Tests  
8. Docs/EKMS/PROJECT_STATE/Delivery Report  

---

## 8. Engineering Decision Approval

| Gate | Status |
|------|--------|
| Requirements understood | ✓ |
| Architecture reviewed | ✓ |
| Dependencies known | ✓ |
| Risks documented | ✓ |
| Strategy complete | ✓ |

**Proceed to implementation.**

---

**End of Intake W0-U02**
