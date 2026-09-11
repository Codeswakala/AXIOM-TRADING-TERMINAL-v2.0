# ITRGA Review — V2 BE-1 PostgreSQL Failure Evidence

| Field | Value |
|---|---|
| Review ID | ITRGA-REV-V2-BE-1-PG-001 |
| Evidence reviewed | Operator PostgreSQL result and AXIOM-V2-BE-1-EVIDENCE-003 |
| Determination | **CORRECTION REQUIRED** |

---

## 1. Verified PostgreSQL defect

The Operator PostgreSQL migration failed while seeding `v2_capability_record.created_at`.

The direct error shows a timezone-aware UTC Python value being bound to:

```text
TIMESTAMP WITHOUT TIME ZONE
```

and PostgreSQL/asyncpg rejected it with:

```text
can't subtract offset-naive and offset-aware datetimes
```

This confirms the defect recorded in `ITRGA-CR-V2-BE-1-PG-001`. It is a real BE-1 temporal/migration compatibility defect, not an environmental exception.

## 2. Evidence inconsistency

AXIOM-V2-BE-1-EVIDENCE-003 claims that the seed definition was corrected from `sa.DateTime` to `sa.DateTime(timezone=True)`.

However, its listed SHA-256 for:

```text
backend/alembic/versions/20260823_0038_v2_be1_core.py
```

is unchanged from the prior evidence manifest:

```text
caf44c16e4852fdef43f0dbd774faae7a78dd31330fbdb88989de01f10f4f21f
```

A changed migration file would produce a changed SHA-256 hash. Therefore, either:

- the corrected migration is not the file represented by the submitted manifest/archive; or
- the manifest was not regenerated after the correction.

The claimed correction is **Not Proven** and must not be used to close the PostgreSQL gate.

## 3. Required DA correction package

The DA must submit:

1. the corrected migration source file or updated source archive;
2. a newly generated SHA-256 manifest showing a changed migration-file hash;
3. direct proof that every seeded timestamp bind uses `sa.DateTime(timezone=True)` or an equally compliant timezone-aware column definition;
4. PostgreSQL rerun evidence after correction:
   - clean dedicated verification DB;
   - migration upgrade succeeds with exit code 0;
   - V2 tables/triggers exist;
   - PostgreSQL mutation-refusal test evidence;
   - drift comparison;
   - downgrade and trigger-removal evidence;
5. corrected Delivery Report/Evidence wording that does not claim PostgreSQL success until these outputs exist.

## 4. Status of PostgreSQL exception

The conditional PostgreSQL environmental exception does not cover a demonstrated migration failure on an available Operator PostgreSQL instance. The exception remains relevant only to unavailable DA workspace infrastructure; it does not waive correction or verification of the actual PostgreSQL defect.

## 5. Determination

**CORRECTION REQUIRED.** BE-1 remains unapproved. No repository publication/tagging, BE-2 planning, deployment, or PostgreSQL use is authorized on the basis of the current failed migration result.
