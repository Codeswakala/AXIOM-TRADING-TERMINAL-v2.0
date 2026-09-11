# AXIOM Build Order
## W0-U02 — Core Persistence Layer Foundation

**Build Order ID:** W0-U02  
**Wave:** 0 — Foundation  
**Unit:** 02  
**Version:** 1.0  
**Status:** ISSUED  
**Authority:** Independent Technical Review & Governance Authority (ITRGA)  
**Date Issued:** 2026-07-10  
**Authorized By:** ITRGA (following completion and approval of W0-U01)  
**Classification:** Official Build Order  
**Governing Documents:**  
- 03_AXIOM_SPEC_v1.1.md  
- 04_PROJECT_ROADMAP.md  
- GOVERNANCE_HIERARCHY.md  
- AXIOM_SYSTEM_ARCHITECTURE_MERGED.md (v1.1)  
- 02_DESIGN_PHILOSOPHY.md  
- 08_UI_UX_SPEC.md  
- 00_VISION_AND_PRINCIPLES.md  
- ITRGA_Enhanced_Investigation_Standards_v1.1.md (incorporated)

---

## 1. Purpose

This Build Order authorizes the Development Authority to implement the foundational persistence layer for AXIOM.

Building on the successful completion of W0-U01, this unit establishes a professional, maintainable, and governance-aligned data access foundation that will support all future market data, features, models, signals, experiments, and governance records.

---

## 2. Objectives

1. Introduce a clean, production-grade persistence layer using the approved architecture.
2. Implement repository and data access patterns with clear separation of concerns.
3. Add PostgreSQL database integration with proper configuration and connection management.
4. Establish Alembic (or equivalent) for schema migrations.
5. Create initial domain entities and repositories aligned with future roadmap needs (Market Data, Features, Models, etc.).
6. Enhance health/readiness probes to accurately reflect database state.
7. Implement basic CRUD patterns and transaction management.
8. Expand the Engineering Knowledge Management System with relevant ADRs and updates.
9. Maintain full compliance with institutional standards for testing, documentation, and observability.
10. Preserve future extensibility for multi-market, high-volume, and time-series data.

---

## 3. Scope

### In Scope
- Database configuration and connection pooling (async preferred where appropriate).
- SQLAlchemy (or equivalent ORM) setup with proper models.
- Alembic migration system (initial migration + migration workflow).
- Repository pattern implementation:
  - Base repository
  - Concrete repositories for initial entities
- Core domain models (minimal set):
  - MarketData / Candle (basic structure)
  - FeatureRecord (placeholder)
  - ModelArtifact (placeholder)
  - AuditEvent (governance)
- Health/readiness integration with real database connectivity checks.
- Unit and integration tests (including database test isolation).
- Structured logging for database operations.
- Documentation and EKMS updates.
- Delivery Report with evidence.

### Explicitly Out of Scope
- Full market data ingestion pipelines.
- Real trading or signal logic.
- Advanced time-series optimizations or partitioning.
- Authentication/authorization data models (deferred).
- Production data seeding or large-scale performance tuning.
- Any ML training or inference components.
- Broker or external data feed integration.

---

## 4. Deliverables

The Development Authority shall deliver the following as a complete unit:

1. **Database Integration**
   - PostgreSQL connection configuration (environment-aware).
   - Connection pooling and lifecycle management.
   - Async database support (recommended) or clear justification.

2. **Migration System**
   - Alembic (or equivalent) fully integrated.
   - Initial migration(s) for core tables.
   - Clear developer workflow documented for creating and applying migrations.

3. **Repository & Data Access Layer**
   - Abstract repository interface.
   - Concrete repository implementations.
   - Transaction and session management patterns.
   - Basic query helpers.

4. **Initial Domain Models**
   - At minimum:
     - `Candle` / basic OHLCV structure
     - `Feature` placeholder
     - `ModelMetadata`
     - `AuditLog` entry
   - Pydantic + ORM model mapping where appropriate.

5. **Observability Enhancements**
   - Database health checks that reflect actual connectivity and basic latency.
   - Structured logging for DB operations (queries, errors, connection events).
   - Basic metrics exposure (connection pool stats).

6. **Testing**
   - Unit tests for repositories (using test database or mocks where appropriate).
   - Integration tests with a real or containerized test database.
   - Test isolation strategy documented.

7. **Engineering Knowledge Management Updates**
   - New Architecture Decision Records (at least 2):
     - Database technology choice and async vs sync rationale
     - Repository pattern design decisions
   - Updated Technical Debt Register
   - Updated Decision Log

8. **Documentation**
   - Updated `PROJECT_STATE.md`
   - Database setup and migration guide in `docs/`
   - Changes to architecture and configuration documentation

9. **Delivery Report**
   - Comprehensive `DELIVERY_REPORT_W0-U02.md` following all ITRGA standards, including application of the **Enhanced Investigation Standards v1.1**.

---

## 5. Success Criteria / Definition of Done

This unit is considered complete only when **all** of the following are satisfied:

- [ ] Database connects successfully in development and test environments
- [ ] Migrations can be created and applied cleanly
- [ ] Repository pattern is implemented and used for at least one real entity
- [ ] Health/readiness endpoints accurately report database status
- [ ] All tests pass (unit + integration with database)
- [ ] Structured logging and basic observability for DB operations implemented
- [ ] At least two new ADRs created with proper rationale
- [ ] Technical debt and decisions properly recorded
- [ ] `PROJECT_STATE.md` updated
- [ ] All governing documents synchronized where necessary
- [ ] Delivery Report includes evidence (connection logs, migration output, test results, sample queries)
- [ ] Implementation follows Clean Architecture and the merged System Architecture
- [ ] No violations of Vision, Design Philosophy, AXIOM_SPEC, or Governance Hierarchy
- [ ] Unit remains independently reviewable with clear structure and documentation

---

## 6. Constraints & Standards

The Development Authority **must** adhere to:

- **Architecture:** AXIOM_SYSTEM_ARCHITECTURE_MERGED.md (v1.1)
- **Enhanced Investigation Standards:** ITRGA_Enhanced_Investigation_Standards_v1.1.md (mandatory for this and all future units)
- **Engineering Philosophy:** 02_DESIGN_PHILOSOPHY.md
- **Project Constitution:** 03_AXIOM_SPEC_v1.1.md
- **Governance Hierarchy:** GOVERNANCE_HIERARCHY.md
- **Documentation as Governance:** Full synchronization required
- **Testing:** Both unit and integration tests with database isolation
- **Modularity:** Repository layer must be replaceable
- **Observability:** Database operations must be logged and health-checked
- **Future Compatibility:** Design must support multi-market and high-volume time-series data

All technical debt must be explicitly recorded.

---

## 7. References & Dependencies

- **Completed:** W0-U01 (approved)
- **Governing Documents** (current versions)
- **ITRGA Records:**
  - ITRGA-2026-07-10-001
  - ITRGA-2026-07-10-002
  - ITRR-W0-U01-001
  - ITRGA_Enhanced_Investigation_Standards_v1.1.md
- **Build Order W0-U01**

---

## 8. Delivery Report Requirements

The Delivery Report must follow the full structure defined in the ITRGA Operations Manual **and** explicitly demonstrate application of the Enhanced Investigation Standards (v1.1).

It must include:
- Discipline-by-discipline analysis (from Section 2 of the directive)
- Investigation of consequences and alternatives
- Future compatibility assessment
- Runtime investigation results (where available)
- **Review Confidence Assessment** (as defined in Section 8 of the directive)

---

## 9. Timeline & Process

- Development Authority implements this unit.
- Upon completion, submit the full unit + Delivery Report to the ITRGA.
- ITRGA will conduct a **full enhanced investigation** per Directive v1.1.
- Corrections (if required) → Re-submission → Final Approval.
- Only after ITRGA Approval will the next Build Order be issued.

**Estimated Effort:** Moderate foundation unit. Emphasis on clean design and long-term maintainability.

---

## 10. Authorization & Signature

**This Build Order is hereby issued by the Independent Technical Review & Governance Authority.**

**Issued By:** ITRGA  
**Date:** 2026-07-10  
**Reference:** Following successful approval of W0-U01 and formal incorporation of Enhanced Investigation Standards.

**Next Action Required from Development Authority:**
1. Acknowledge receipt of Build Order W0-U02.
2. Begin implementation with full adherence to the Enhanced Investigation Standards.
3. Produce complete Delivery Report with evidence of deep investigation mindset.
4. Submit for ITRGA independent review.

---

**End of Build Order W0-U02**

---

*ITRGA — Strengthening AXIOM through rigorous, multi-disciplinary, consequence-aware investigation.*