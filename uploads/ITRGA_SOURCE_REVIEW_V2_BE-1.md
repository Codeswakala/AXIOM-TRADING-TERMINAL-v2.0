# ITRGA Source Review — AXIOM V2 BE-1 Source Transcript

| Field | Value |
|---|---|
| Review ID | ITRGA-REV-V2-BE-1-SOURCE-001 |
| Evidence reviewed | Plain-text BE-1 source transcript Parts 1 and 2; PostgreSQL rerun evidence |
| Determination | **CORRECTION REQUIRED** |

---

## 1. Directly verified positive controls

The supplied source directly verifies several BE-1 claims:

- the corrected migration uses `sa.DateTime(timezone=True)` for seeded V2 timestamps;
- V2 models are imported in `app.db.models.__init__`, explaining the resolved V2 Alembic metadata drift;
- PostgreSQL and SQLite immutable-trigger logic is present in the migration;
- V2 mode is sourced from `AXIOM_V2_MODE` only;
- Paper and Live modes are rejected by the V2 mode contract;
- V2 temporal helpers reject naive datetimes;
- V2 capability records have no `enabled` mutation field;
- V2 permission vocabulary excludes execution/broker/account/order/live-capability terms;
- PostgreSQL rerun evidence supports successful upgrade, V2 tables/triggers/functions, V1-only drift, downgrade, and post-downgrade trigger/function removal.

## 2. Findings

### Finding V2-BE1-SRC-001 — Artifact-specific lineage endpoint bypasses operator isolation

| Field | Detail |
|---|---|
| Severity | Critical — SAL-3 confidentiality / cross-operator disclosure |
| Governing rule | Document 17 §4.4 SAL-3 operator isolation; §6.8 resource ownership; approved BE-1 plan requires operator-scoped lineage reads. |
| Direct evidence | `backend/app/v2/api/lineage.py`: `get_artifact_lineage()` is protected only by `RequireV2LineageRead`, then calls `repo.read_by_artifact(artifact_type, artifact_id)`. `V2LineageRepository.read_by_artifact()` filters only `artifact_type` and `artifact_id`; it does not filter by `operator_id`. |
| Impact | Any ordinary operator who knows or guesses an artifact type/ID can retrieve another operator’s lineage record through `/api/v2/lineage/{artifact_type}/{artifact_id}`. |
| Required correction | Add server-side operator ownership filtering to the non-admin artifact-specific lineage read. Provide a separate admin-only `read_all` artifact lookup only if justified and audited. Add integration tests with two operators proving cross-operator artifact lookup returns an appropriate denied/not-found response without disclosure. |
| Closure criterion | A non-admin operator cannot retrieve another operator’s lineage record through list, single-artifact, correlation, or any future query path. |

### Finding V2-BE1-SRC-002 — Required security/integration tests are claimed but not implemented in supplied tests

| Field | Detail |
|---|---|
| Severity | High — evidence/test coverage integrity |
| Build Order requirement | BO-V2-BE-1-001 requires authorization, security, temporal, migration, trigger, drift, and failure-path tests, including cross-operator isolation, sensitive-read audit, update/delete refusal, and both supported dialects. |
| Direct evidence | Supplied `test_v2_audit.py` contains redaction tests only. It has no database persistence, update/delete-trigger, audit-write-failure, sensitive-read, or cross-operator test. `test_v2_rbac.py` tests static permission mappings only, not endpoint/resource isolation. The claimed PostgreSQL 30-test run therefore does not establish PostgreSQL trigger mutation refusal or cross-operator endpoint behavior. |
| Required correction | Implement and run actual database/API integration tests for: SQLite and PostgreSQL update/delete refusal; audit/lineage append; cross-operator list and artifact-specific denial; admin `read_all`; sensitive-read audit record persistence; handler response safety; migration upgrade/downgrade and trigger presence/removal. Report actual test names and results. |
| Closure criterion | Every BE-1 security acceptance criterion maps to a concrete implemented test that exercises the real persistence/API path. |

### Finding V2-BE1-SRC-003 — V2 secure error handlers are not registered with the FastAPI application

| Field | Detail |
|---|---|
| Severity | High — secure error handling |
| Governing rule | Document 17 §10.14 and §12.10; BE-1 plan requires structured safe V2 error/status contract. |
| Direct evidence | `app.v2.errors.handlers` defines `v2_error_response()` and `v2_internal_error_response()`, but the supplied `app.main.py` does not register exception handlers for `V2Error` or V2 internal exceptions. The API route modules also do not catch and translate V2 errors. |
| Impact | V2 error classes can propagate through FastAPI’s default error behavior rather than the claimed V2 structured/safe error contract. |
| Required correction | Register a narrowly scoped V2 exception handler in the application, ensure it returns safe structured V2 responses with correlation/timestamp, preserve existing V1 handler behavior, and test V2 mode/permission/temporal/internal error responses for no internal-detail leakage. |
| Closure criterion | Direct API tests prove V2 errors are returned through the approved safe contract and no stack trace/internal detail reaches a client. |

### Finding V2-BE1-SRC-004 — V2 API response contract is inconsistent

| Field | Detail |
|---|---|
| Severity | Medium — API contract integrity |
| Observed condition | The approved plan says all V2 responses include mode, correlation ID, timestamp, and data context. List endpoints return these fields; `GET /api/v2/capabilities/{capability_id}` returns `V2CapabilityResponse` only, without mode/correlation/timestamp. |
| Required correction | Define and implement a consistent response-envelope policy. At minimum, add mode/correlation/timestamp to the single-capability response or formally document an approved exception and update the plan/endpoint contract. |
| Closure criterion | All V2 endpoints meet their published response contract and tests assert it. |

## 3. Determination

**CORRECTION REQUIRED.** PostgreSQL migration/metadata verification is now substantially supported, but direct source inspection identified a critical operator-isolation defect and missing required integration/security/handler evidence. BE-1 remains unapproved until the bounded corrections above are implemented and independently evidenced.
