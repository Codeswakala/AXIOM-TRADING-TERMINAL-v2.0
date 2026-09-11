# ITRGA Review — AXIOM V2 BE-1 Corrected Plan: Migration-Gate Clarification

| Field | Value |
|---|---|
| Review ID | ITRGA-REV-V2-BE-1-004 |
| Submission | `AXIOM-V2-BE-1-DA-PLAN-001`, v3.0.0 |
| Determination | **CORRECTION REQUIRED** |
| Scope | Final migration-drift acceptance-gate validation |

---

## 1. Assessment

The v3.0.0 plan substantively resolves the prior findings on mode source, cross-dialect triggers, operator scoping, SAL-control evidence boundaries, retention governance, read-only permission/capability seeding, temporal handling, and migration-drift comparison.

One migration-acceptance rule remains unsafe.

## 2. Finding

### Finding V2-BE1-PLAN-011 — BE-1 drift gate incorrectly permits BE-1 tables to remain reported as migration drift

| Field | Detail |
|---|---|
| Severity | High — schema/migration integrity |
| Observed condition | F.3.2 says post-BE-1 `alembic check` may contain the inherited V1 drift **plus the BE-1 V2 tables and triggers**. |
| Why this is incorrect | The approved BE-1 Alembic migration is intended to create the V2 tables. After `alembic upgrade head`, those table definitions must be represented by the migration chain. If `alembic check` reports a BE-1 V2 table as a new upgrade operation, that is new BE-1 model/migration drift, not an acceptable expected result. Database triggers may require separately documented dialect-specific verification because Alembic autogenerate may not compare them, but triggers cannot justify allowing V2 table drift. |
| Required correction | Replace the gate with: `post-BE-1 alembic check may contain only the exact documented inherited V1 drift baseline. Any V2 table, V2 column, V2 index, or other V2 schema operation in the post-BE-1 diff is a blocking BE-1 defect unless it is first added to and correctly represented by the approved BE-1 migration.` Add a separate trigger-verification gate: inspect/execute expected PostgreSQL and SQLite triggers after upgrade and verify their removal after downgrade. |
| Closure criterion | The implementation plan has a pass/fail gate that detects every new V2 schema drift rather than accepting it as expected. |

## 3. Determination

**CORRECTION REQUIRED.** This is a single bounded plan correction. No new feature, scope, or security design is requested. No BE-1 implementation may begin until the migration-drift rule is corrected.
