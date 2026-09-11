# ITRGA Request — V2 BE-1 Plain-Text Source Review Transcript

| Field | Value |
|---|---|
| Request ID | ITRGA-REQ-V2-BE-1-SOURCE-001 |
| Date | 2026-08-24 |
| Issued by | Independent Technical Review & Governance Authority (ITRGA) |
| Purpose | Close the remaining direct-source evidence condition for BE-1 final determination without Git operations or compressed-file upload |
| Status | Active request — no new implementation scope |

---

## 1. Purpose

The DA has supplied hashes and PostgreSQL runtime evidence, but the compressed source archive cannot be uploaded through the review chat.

Submit the BE-1 source as plain Markdown transcript file(s) for direct ITRGA inspection. This is an evidence-format request only. It does not request a commit, tag, push, pull, branch, repository publication, code change, or new capability.

## 2. Required submission format

Submit either:

```text
V2_BE-1_SOURCE_REVIEW.md
```

or, if needed due to attachment size:

```text
V2_BE-1_SOURCE_REVIEW_PART_1.md
V2_BE-1_SOURCE_REVIEW_PART_2.md
```

Each transcript must use this exact structure for every included file:

````markdown
## File: `relative/path/to/file.py`

**SHA-256:** `lowercase-64-character-sha256`

```python
<literal current file content>
```
````

Use the appropriate fenced-code language (`python`, `sql`, `toml`, `text`) for each file. Include literal file contents—not summaries, snippets, pseudocode, or references to an archive.

## 3. Required file contents

The submission must include the following current BE-1 files.

### Part 1 — Migration, models, mode, and security core

```text
backend/alembic/versions/20260823_0038_v2_be1_core.py
backend/app/db/models/__init__.py
backend/app/db/models/v2_audit_event.py
backend/app/db/models/v2_lineage_record.py
backend/app/db/models/v2_capability_record.py
backend/app/db/models/v2_permission.py
backend/app/v2/identifiers.py
backend/app/v2/mode/contract.py
backend/app/v2/mode/dependency.py
backend/app/v2/temporal/validation.py
backend/app/v2/errors/contract.py
backend/app/v2/errors/handlers.py
backend/app/v2/audit/contract.py
backend/app/v2/audit/redaction.py
backend/app/v2/audit/repository.py
backend/app/v2/lineage/contract.py
backend/app/v2/lineage/repository.py
backend/app/v2/rbac/permissions.py
backend/app/v2/rbac/dependencies.py
backend/app/v2/capability/contract.py
backend/app/v2/capability/seed.py
```

### Part 2 — API integration and tests

```text
backend/app/v2/api/router.py
backend/app/v2/api/mode.py
backend/app/v2/api/capability.py
backend/app/v2/api/audit.py
backend/app/v2/api/lineage.py
backend/app/v2/models/mode.py
backend/app/v2/models/capability.py
backend/app/v2/models/audit.py
backend/app/v2/models/lineage.py
backend/app/v2/models/errors.py
backend/app/api/router.py
backend/app/main.py
backend/tests/test_v2_mode.py
backend/tests/test_v2_audit.py
backend/tests/test_v2_temporal.py
backend/tests/test_v2_rbac.py
backend/tests/test_v2_identifiers.py
backend/tests/test_v2_errors.py
```

Include `__init__.py` files only when they contain material imports/registration logic. Empty package initializers do not need to be copied.

## 4. Integrity requirements

1. Regenerate SHA-256 values from the current DA workspace after the final PostgreSQL correction.
2. Use the same source state that produced the successful PostgreSQL rerun with source-bundle SHA-256:

```text
D725895DE9EF76D94355B315FB608A52B6C116ED9092DA5F8E595785B97C6DF2
```

3. State the source-bundle hash at the beginning of the transcript.
4. If any listed file differs from the manifest, identify the difference and explain why.
5. Do not include credentials, database URLs, JWT secrets, tokens, personal data, or other secrets. Redact any accidental secret before submission and record the redaction location/reason.

## 5. ITRGA verification focus

The ITRGA will inspect the transcript for:

- timezone-aware BE-1 migration seed definitions;
- V2 model inclusion in Alembic target metadata;
- PostgreSQL/SQLite trigger creation and removal;
- no suppression of V2 Alembic drift;
- mode sourced only from `AXIOM_V2_MODE`;
- Paper/Live refusal and absence of out-of-scope capability;
- append-only audit/lineage enforcement;
- secret redaction/rejection;
- RBAC default-deny and operator-scoped reads;
- restricted admin `read_all` handling;
- V2 temporal naive-datetime rejection;
- test coverage consistency with submitted PostgreSQL evidence.

## 6. Next state

After transcript review, ITRGA will issue the final BE-1 delivery determination. No Git operation is required for this request. No new implementation work is authorized unless a specific source-level defect is found.
