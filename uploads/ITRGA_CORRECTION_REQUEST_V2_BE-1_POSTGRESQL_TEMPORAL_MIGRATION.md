# ITRGA Correction Request — V2 BE-1 PostgreSQL Temporal Migration Defect

| Field | Value |
|---|---|
| Request ID | ITRGA-CR-V2-BE-1-PG-001 |
| Date | 2026-08-24 |
| Authority | Independent Technical Review & Governance Authority (ITRGA) |
| Scope | Bounded correction within BO-V2-BE-1-001 |
| Status | Active — BE-1 delivery review paused pending correction evidence |

---

## 1. Verified condition

The Operator PostgreSQL verification produced a migration failure in:

```text
20260823_0038_v2_be1_core.py
```

The database adapter rejected the seeded `v2_capability_record.created_at` value:

```text
can't subtract offset-naive and offset-aware datetimes
```

The SQL shown in the error targets:

```text
created_at ... TIMESTAMP WITHOUT TIME ZONE
```

while the seeded Python value is timezone-aware UTC:

```text
datetime(..., tzinfo=datetime.timezone.utc)
```

This is direct Level-I/II PostgreSQL evidence of a BE-1 migration defect. It is not an environmental exception.

## 2. Governing impact

The approved BE-1 plan requires V2 timestamps to use timezone-aware UTC storage and serialization. Converting the seeded timestamp to naive time merely to make the migration pass is not an acceptable correction because it would contradict the approved V2 temporal model.

## 3. Required DA correction

The DA must make a bounded correction to the BE-1 migration and corresponding V2 model/seed definitions:

1. ensure all V2 timestamp columns that receive timezone-aware UTC values use the PostgreSQL-compatible timezone-aware timestamp type (for SQLAlchemy, the design intent is `DateTime(timezone=True)`);
2. ensure the migration and ORM model definitions agree exactly for each V2 timestamp column;
3. ensure seed values are timezone-aware UTC and originate from the approved V2 temporal utility/contract;
4. do not weaken `require_utc()` or introduce naive V2 timestamps;
5. do not modify V1 tables, V1 migrations, or any out-of-scope capability;
6. add/adjust tests proving timezone-aware seeded records migrate and persist on PostgreSQL-compatible and SQLite environments.

## 4. Safe operator actions before rerun

Do not manually alter `alembic_version`, delete migration history, or modify production/shared databases.

Because the log states PostgreSQL is using transactional DDL, the failed migration is expected to have rolled back. The Operator should nevertheless capture and supply the results of:

```powershell
& $Psql $env:POSTGRES_VERIFICATION_URL -c "SELECT version_num FROM alembic_version;"
& $Psql $env:POSTGRES_VERIFICATION_URL -c "
SELECT tablename FROM pg_tables
WHERE schemaname='public' AND tablename LIKE 'v2_%'
ORDER BY tablename;"
```

If the target is a disposable verification database, the preferred retest path after DA correction is a freshly recreated dedicated verification database.

## 5. Required correction evidence

The DA must submit:

- corrected non-Git source bundle/patch and updated source manifest;
- migration/model/seed diff limited to the temporal compatibility defect;
- PostgreSQL `alembic upgrade head` output with exit code 0;
- V2 table and trigger existence evidence;
- PostgreSQL test output including timestamp seed/persistence coverage;
- PostgreSQL drift and downgrade/trigger-removal evidence from the existing command pack;
- updated Delivery Report/evidence package accurately recording the defect and correction.

## 6. Status

The PostgreSQL environmental exception remains available only for genuinely unavailable infrastructure checks. It does not cover this demonstrated PostgreSQL migration incompatibility.

No BE-1 final approval can be issued until this correction and evidence are reviewed.
