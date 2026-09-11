# ITRGA Review — AXIOM V2 BE-1 Source Delta

| Field | Value |
|---|---|
| Review ID | ITRGA-REV-V2-BE-1-SOURCE-DELTA-001 |
| Evidence reviewed | `V2_BE-1_SOURCE_REVIEW_DELTA.md` |
| Determination | **CORRECTION REQUIRED** |

---

## 1. Closed source defect

**V2-BE1-SRC-001 — artifact-specific lineage cross-operator disclosure: Closed in source.**

`get_artifact_lineage()` now passes `operator_id=operator.id`, and `read_by_artifact()` applies that server-side filter when an ordinary operator endpoint invokes it. This corrects the previously verified direct disclosure path.

## 2. Findings

### Finding V2-BE1-DELTA-001 — Claimed integration tests do not exercise the claimed database/API security paths

| Field | Detail |
|---|---|
| Severity | High — evidence/test coverage integrity |
| Observed condition | `test_v2_integration.py` labels itself as database persistence, triggers, cross-operator isolation, and error-handler integration. Its actual tests exercise environment patches, redaction utilities, static RBAC maps, exception objects, and `inspect.signature`. The two lineage “isolation” tests only verify that an optional `operator_id` parameter exists/defaults to `None`; they do not create two operators/records or execute a query/API request. |
| Missing coverage | No supplied test exercises database append; SQLite/PostgreSQL trigger refusal; audit/lineage update/delete attempts; cross-operator list/artifact API denial; admin read-all API; sensitive-read audit persistence; registered error handler response; or migration upgrade/downgrade. |
| Required correction | Replace/add actual async database/API integration tests using the configured test database. Tests must create distinct operator-owned records, invoke real repositories/endpoints, assert no cross-operator data disclosure, assert admin read-all behavior, assert audit record creation for sensitive reads, and assert trigger refusal on update/delete. PostgreSQL-specific tests must be run in the available PostgreSQL verification environment. |
| Closure criterion | Security assertions are demonstrated by executed database/API behavior, not by code signature or static mapping inspection. |

### Finding V2-BE1-DELTA-002 — V2 test command double-collects the integration file and inflates its test total

| Field | Detail |
|---|---|
| Severity | Medium — test accounting integrity |
| Observed condition | The command is `pytest tests/test_v2_* tests/test_v2_integration.py ...`. The glob `tests/test_v2_*` already includes `test_v2_integration.py`; passing it a second time yields the reported 111 results rather than the stated 81 distinct V2 tests. |
| Required correction | Use one non-duplicating command, for example `pytest tests/test_v2_*.py -v --tb=short`, and report distinct test-file/test-case totals. Update Delivery Report/evidence totals accordingly. |
| Closure criterion | Reported V2 test count matches a single, non-duplicated pytest collection and no test file is collected twice. |

### Finding V2-BE1-DELTA-003 — Classification access control is declared but not enforced before audit disclosure

| Field | Detail |
|---|---|
| Severity | High — SAL-3/4 confidentiality |
| Governing rule | Document 17 SAL-3 operator isolation and RBAC; the BE-1 audit contract declares classification-based access control. |
| Direct evidence | `can_access_classification()` exists in `v2/audit/contract.py`, but it is not invoked by `V2AuditRepository` or `v2/api/audit.py`. `_to_response()` returns `details` and `classification` for every event returned to an operator. |
| Impact | An operator’s own audit record classified `secret` or above the operator’s effective clearance can be returned without a classification decision. The source also has no defined clearance source. |
| Required correction | Define role/identity clearance, apply classification filtering/redaction in every audit read path, and test public/internal/confidential/secret response behavior. If secret material is prohibited from audit records, enforce rejection/downgrade at write time and remove unsupported secret-readable semantics. |
| Closure criterion | Every audit read has an explicit, tested classification decision before details are returned. |

### Finding V2-BE1-DELTA-004 — V2 permission-denial response exposes internal permission names

| Field | Detail |
|---|---|
| Severity | Medium — secure error handling |
| Direct evidence | `require_v2_permission()` returns `HTTPException(detail=f"V2 permission denied: {permission}")`; `PermissionError` similarly includes the permission name. Document 17 §10.14/§12.10 requires error responses not expose internal implementation details. |
| Required correction | Return a generic public denial message such as `Permission denied`; log the required permission, actor, route, correlation ID, and decision internally/audit it. Add a direct API test confirming a denial response does not expose permission vocabulary. |
| Closure criterion | Public authorization errors disclose no internal permission/authorization implementation detail. |

## 3. Determination

**CORRECTION REQUIRED.** The primary lineage isolation source fix is present, but the final BE-1 delivery cannot be approved because test evidence is inflated/non-integrated and the audit classification/permission-denial security paths are incomplete.

No new product scope is authorized. Required work remains limited to BE-1 audit, RBAC, API error, and test correctness.
