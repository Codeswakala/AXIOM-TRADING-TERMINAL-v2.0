# BUILD ORDER INTAKE — AXIOM V2 BE-1

| Field | Value |
|---|---|
| Build Order ID | BO-V2-BE-1-001 |
| Intake Date | 2026-08-23 |
| Intake By | Development Authority (DA) |
| Status | **INTAKE COMPLETE — READY FOR IMPLEMENTATION** |

---

## 1. Build Order Understanding

The Build Order authorizes BE-1 implementation of V2 non-actuating Research/Simulation core runtime primitives. This is the first V2 runtime-code band.

## 2. Objectives Extracted

| # | Objective | Deliverable |
|---|-----------|-------------|
| 1 | V2 module structure | `backend/app/v2/` package and submodules |
| 2 | V2 identifiers | `app/v2/identifiers.py` |
| 3 | V2 error taxonomy | `app/v2/errors/contract.py`, `handlers.py` |
| 4 | V2 temporal validation | `app/v2/temporal/validation.py` |
| 5 | V2 mode framework | `app/v2/mode/contract.py`, `dependency.py` |
| 6 | V2 audit contract | `app/v2/audit/contract.py`, `redaction.py`, `repository.py` |
| 7 | V2 lineage contract | `app/v2/lineage/contract.py`, `repository.py` |
| 8 | V2 capability registry | `app/v2/capability/contract.py`, `seed.py` |
| 9 | V2 RBAC extension | `app/v2/rbac/permissions.py`, `dependencies.py` |
| 10 | V2 database models | `app/db/models/v2_*.py` |
| 11 | Alembic migration | `alembic/versions/20260823_0038_v2_be1_core.py` |
| 12 | V2 API routes | `app/v2/api/router.py`, `mode.py`, `capability.py`, `audit.py` |
| 13 | V2 Pydantic models | `app/v2/models/*.py` |
| 14 | Tests | `tests/test_v2_*.py` |
| 15 | Documentation updates | V2 Current State, Risk Register, Debt Register, Capability Registry |
| 16 | Delivery Report | `DELIVERY_REPORT_V2_BE-1.md` |

## 3. Constraints Verified

| # | Constraint | Status |
|---|------------|--------|
| 1 | V1 additive/compatible | ✅ Confirmed |
| 2 | No Paper/Live | ✅ Confirmed |
| 3 | No provider/broker/execution/AI/frontend | ✅ Confirmed |
| 4 | Mode fails safely | ✅ Confirmed |
| 5 | Operator-scoped reads | ✅ Confirmed |
| 6 | No secrets in payloads | ✅ Confirmed |
| 7 | Read-only seeded registries | ✅ Confirmed |
| 8 | Reject naive datetimes | ✅ Confirmed |
| 9 | No V2 schema drift | ✅ Confirmed |
| 10 | No Git operations by DA | ✅ Confirmed |

## 4. Implementation Order

1. Create V2 module structure
2. Implement identifiers
3. Implement error taxonomy
4. Implement temporal validation
5. Implement mode framework
6. Implement audit contract (with redaction)
7. Implement lineage contract
8. Implement capability registry (read-only seeded)
9. Implement RBAC extension
10. Create database models
11. Create Alembic migration (with dialect-aware triggers)
12. Implement V2 API routes
13. Implement V2 Pydantic models
14. Seed capability and permission records
15. Write tests
16. Run V1 regression
17. Capture drift evidence
18. Update documentation
19. Prepare Delivery Report

## 5. Readiness Statement

> The DA has completed intake assessment of BO-V2-BE-1-001. All objectives, constraints, and exclusions are understood. The implementation plan is clear. The DA is ready to begin implementation.

---

**End of Build Order Intake**
