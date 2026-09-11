# ITRGA Review — V2 BE-1 PostgreSQL Rerun Evidence

| Field | Value |
|---|---|
| Review ID | ITRGA-REV-V2-BE-1-PG-002 |
| Evidence | Operator PostgreSQL 18.4 rerun result dated 2026-08-24 |
| Determination | **CORRECTION REQUIRED** |

---

## 1. Verified facts

The rerun provides direct PostgreSQL evidence that:

- a fresh dedicated non-production PostgreSQL 18.4 database was used;
- migration `20260823_0038` now upgrades successfully after the timestamp correction;
- all four V2 tables exist after upgrade;
- PostgreSQL immutable triggers exist on V2 audit and lineage tables;
- the migration downgrades to `20260717_0037` and removes V2 tables;
- the migration can re-upgrade to `20260823_0038`.

This closes the original timezone-aware/naive timestamp binding defect.

## 2. Blocking defect: PostgreSQL Alembic drift contains new V2 operations

The post-upgrade PostgreSQL `alembic check` output reports removal of every BE-1 V2 table and its indexes, including:

```text
remove_table v2_audit_event
remove_table v2_lineage_record
remove_table v2_capability_record
remove_table v2_permission
```

and their `ix_v2_*` indexes.

Under the approved BE-1 migration-drift gate, any V2 table, column, index, or other V2 schema operation after upgrade is a **blocking BE-1 defect**.

### Likely condition

The database contains the V2 tables, but the Alembic target metadata does not include the imported V2 SQLAlchemy models when `alembic check` runs. This is a supported inference from the exact output; the actual source must be inspected to confirm root cause.

## 3. Required DA correction

The DA must make a bounded migration/metadata correction that:

1. ensures every BE-1 V2 SQLAlchemy model is imported/registered in Alembic `target_metadata` before autogenerate/check runs;
2. preserves the V2 migration and does not suppress, filter, or ignore V2 operations merely to make `alembic check` pass;
3. regenerates the source bundle and SHA-256 manifest after correction;
4. repeats the PostgreSQL verification from a fresh disposable database;
5. demonstrates that post-upgrade `alembic check` contains only the exact documented inherited V1 operations and **no V2 removals/additions/index operations**.

## 4. Remaining PostgreSQL evidence gaps

The supplied transcript does not show:

- trigger/function query output after downgrade;
- PostgreSQL trigger/function absence after downgrade;
- direct update/delete mutation-refusal output against PostgreSQL records;
- actual attached source archive for direct ITRGA inspection.

These remain required for final BE-1 delivery closure.

## 5. Determination

**CORRECTION REQUIRED.** PostgreSQL migration execution now succeeds, which is a meaningful correction. BE-1 remains unapproved because the actual PostgreSQL drift gate fails: V2 schema objects are reported as unrepresented/removable by Alembic metadata.
