# AXIOM V2 BE-1 — Replacement DA Intake and Reconciliation

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BE-1-DA-INTAKE-001 |
| Author | Replacement Development Authority (DA) |
| Date | 2026-08-24 |
| Governing instruction | `AXIOM-V2-DA-ONBOARD-001` (§5 — intake and reconciliation only) |
| Build Order | BO-V2-BE-1-001 |
| Status | **SUBMITTED TO ITRGA — no code change performed** |
| Scope of this document | Intake, source inventory, hash manifest, claim reconciliation, corrective action mapping |

---

## 1. Mandatory Reading Confirmation

### A. Constitutional and security foundation — ALL READ

| # | Document | Status |
|---|---|---|
| 1 | `docs/governance/00_VISION_AND_PRINCIPLES.md` | Read |
| 2 | `docs/governance/03_AXIOM_SPEC.md` | Read |
| 3 | `docs/governance/05_SYSTEM_ARCHITECTURE.md` | Read |
| 4 | `docs/governance/10_CONSTITUTIONAL_HIERARCHY.md` | Read |
| 5 | `docs/governance/DOCUMENT_PRECEDENCE.md` | Read |
| 6 | `docs/governance/17_INSTITUTIONAL_SECURITY_STANDARD.md` | Read |
| 7 | `docs/governance/09_DEVELOPER_REASONING_FRAMEWORK.md` | Read |
| 8 | `docs/governance/09_ITRGA_REASONING_FRAMEWORK.md` | Read |
| 9 | `docs/governance/QUALITY_GATE_SPEC.md` | Read |

### B. V2 programme authority — ALL READ (workspace location noted)

| # | Document | Status | Location note |
|---|---|---|---|
| 10 | `V2_DOCUMENT_PRECEDENCE_ADOPTION_RECORD.md` | Read | Supplied in `uploads/` (not at cited `docs/governance/` path) |
| 11 | `V2_REPOSITORY_CUSTODY_AND_GIT_OPERATIONS_RECORD.md` | Read | `uploads/` |
| 12 | `V2_REPOSITORY_CUSTODY_AND_GIT_OPERATIONS_AMENDMENT_1.md` | Read | `uploads/` |
| 13 | `OPERATOR_DECISION_V2_BE-0_CLOSURE_AND_CHARTER_APPROVAL.md` | Read | `uploads/` |
| 14 | `V2_BACKEND_ROADMAP.md` | Read | `uploads/` |
| 15 | `V2_FRONTEND_ROADMAP.md` | Read | `uploads/` |
| 16 | `docs/governance/V2_PROGRAMME_CHARTER.md` | Read | Workspace |
| 17 | `docs/governance/V2_ARCHITECTURE_PRINCIPLES.md` | Read | Workspace |
| 18 | `docs/governance/V2_RISK_REGISTER.md` | Read | Workspace |
| 19 | `docs/governance/V2_TECHNICAL_DEBT_REGISTER.md` | Read | Workspace |
| 20 | `V2_CURRENT_STATE.md` | Read | Workspace |

### C. BE-1 implementation authority — ALL READ

| # | Document | Status | Location note |
|---|---|---|---|
| 21 | `ITRGA_REQUEST_V2_BE-1_DA_DESIGN_PLAN.md` | Read | `uploads/` |
| 22 | ITRGA design-plan approval | Read via `ITRGA_REVIEW_V2_BE-1_CORRECTED_PLAN.md` (REV-003) + `ITRGA_REVIEW_V2_BE-1_FINAL_MIGRATION_GATE.md` (REV-004); BO-V2-BE-1-001 cites plan determination `ITRGA-REV-V2-BE-1-005` — APPROVED WITH OBSERVATIONS. The literal REV-005 document itself is **not in the supplied corpus** (see §4, item R-9). |
| 23 | `BUILD_ORDER_V2_BE-1_CORE_DOMAIN_AUDIT_MODE.md` | Read | `uploads/` (two identical copies) |
| 24 | `ITRGA_DETERMINATION_V2_BE-1_POSTGRESQL_ENVIRONMENTAL_EXCEPTION.md` | **Not present / unknown** — the exception is referenced by PG-001/PG-002 and DELIVERY-002; the standalone determination document is not in the workspace or uploads. Its operative constraints are understood from the referencing reviews. |
| 25 | `ITRGA_CORRECTION_REQUEST_V2_BE-1_POSTGRESQL_TEMPORAL_MIGRATION.md` | Read | `uploads/` |

### D. BE-1 findings — ALL SUPPLIED ITEMS READ

| # | Document | Status |
|---|---|---|
| 26 | `ITRGA_REVIEW_V2_BE-1_DELIVERY.md` (DEL-001…004) | Read |
| 27 | `ITRGA_REVIEW_V2_BE-1_DELIVERY_RESUBMISSION.md` | Read |
| 28 | `ITRGA_REVIEW_V2_BE-1_POSTGRESQL_FAILURE_EVIDENCE.md` (PG-001) | Read |
| 29 | `ITRGA_REVIEW_V2_BE-1_POSTGRESQL_RERUN.md` (PG-002) | Read |
| 30 | `ITRGA_SOURCE_REVIEW_V2_BE-1.md` (SRC-001…004) | Read |
| 31 | `ITRGA_REVIEW_V2_BE-1_SOURCE_DELTA.md` (DELTA-001…004) | Read |
| 32 | `ITRGA_REQUEST_V2_BE-1_PLAIN_TEXT_SOURCE_REVIEW.md` | Read |
| 33 | `ITRGA_REQUEST_V2_BE-1_CORRECTION_SOURCE_DELTA.md` | Read |
| 34 | `V2_BE-1_POSTGRESQL_VERIFICATION_COMMAND_PACK.md` | **Not present / unknown** — not in workspace or uploads. |

### E. Current evidence corpus — PARTIALLY AVAILABLE

| Document | Status |
|---|---|
| `DELIVERY_REPORT_V2_BE-1.md` (DR-003) | Read (workspace root) |
| `docs/plans/V2_BE-1_DESIGN_PLAN.md` (v3.1.0) | Read (workspace) |
| `V2_BE-1_EVIDENCE.md` | **Not present / unknown** |
| `V2_BE-1_SOURCE_REVIEW_PART_1.md` / `PART_2.md` | **Not present / unknown** |
| `V2_BE-1_SOURCE_REVIEW_DELTA.md` | **Not present / unknown** |
| PostgreSQL verification transcript / `OPERATOR RESULTS.md` | **Not present / unknown** |

Consequence: the transcript-to-workspace comparison mandated by §5(3) of the onboarding is performed against the **claims recorded in the ITRGA reviews** (which quote the transcript contents) rather than against the raw transcripts. Every conclusion below is drawn from **direct inspection of current workspace source** (Level-I file evidence), which the onboarding designates as controlling. Absence of the historical transcripts does not block remediation, because all deliverable transcripts must be regenerated from the current workspace regardless.

---

## 2. Current-Workspace Source Inventory and SHA-256 Manifest

Environment of generation: DA sandbox workspace `/home/user/axiom`, 2026-08-24. All 50 expected BE-1 files are present; none missing.

```text
34ec444d3a9e9b30324361845e62c45afd5e2937b8917d82b81a0c022d425cb6  backend/alembic/versions/20260823_0038_v2_be1_core.py
e01dc1510b10f13878d12aecb3d4508204f843ea01b94291c61f8f96849382f0  backend/app/db/models/__init__.py
2647d95f2ede381278ac7912fdf86cd29a3c46c06e72031c4aeeac63d49002d6  backend/app/db/models/v2_audit_event.py
ec49cdef90998aedcd9170096d1f7d0ff63780541efb4838c8de0ef1f13177d5  backend/app/db/models/v2_lineage_record.py
dca21488ab0188f32f860c058fc27b8d3ba7dcd0ad93ee4e505956474b2633ef  backend/app/db/models/v2_capability_record.py
d153bad6ae5a3c449edbfd30b807a5616e7b0f695f1fe12efa760229536d3cad  backend/app/db/models/v2_permission.py
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  backend/app/v2/__init__.py (empty)
a03d48b598fed491459154cee4424d2c372c1f013e37a7b758963a9d3261dfc5  backend/app/v2/identifiers.py
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  backend/app/v2/mode/__init__.py (empty)
50fc0f4fd153a1276e0ab1ab2ee33f5e7b448bc16aecaebad2703c780fb5b6c0  backend/app/v2/mode/contract.py
1314224f4322fa2ffb9e92778ffb9dbcd0aa62131cfeb2c6f0489ea50f769203  backend/app/v2/mode/dependency.py
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  backend/app/v2/temporal/__init__.py (empty)
5a9aa38259a35bb85b8d48deba9b88d60b2ccf5150c187b844f7e408facf042b  backend/app/v2/temporal/validation.py
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  backend/app/v2/errors/__init__.py (empty)
446b0b2ea52a08a31ae0cdb9997712400a8d1dde594074361fc1eb4950b40379  backend/app/v2/errors/contract.py
f4e7abf792f151123a0e4dad6159435cceab78c8c70a94f50bdea92d7ea269bf  backend/app/v2/errors/handlers.py
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  backend/app/v2/audit/__init__.py (empty)
90eb1125c7b9266e1f92f3f9ab27614158793b3074356f9951bf5d5882ab2fab  backend/app/v2/audit/contract.py
22141e51649539a1d70a3f6b268bdd23997b61fc86a48d27a7bf518092bbf081  backend/app/v2/audit/redaction.py
e21bc4cb73c13642a18a63b7f13de54afa3b4e9089ca98197b4bfc02460dfdc8  backend/app/v2/audit/repository.py
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  backend/app/v2/lineage/__init__.py (empty)
ead2d63b8e137221a28b1b4bf9e11d0de693c9a062c473e53c278a8113f73881  backend/app/v2/lineage/contract.py
b2681fca5e72bf7bbd756096fce61e063fec07d9ddfa316876701006981e37ef  backend/app/v2/lineage/repository.py
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  backend/app/v2/rbac/__init__.py (empty)
54379f89543a316408b35172c2dad543c3e3e4472d1694d7d66a6fa601bf9438  backend/app/v2/rbac/permissions.py
8268b3a5cf14134a8327e5e4bc7d6febc0c28311eb8058f6d0f7650743d5195d  backend/app/v2/rbac/dependencies.py
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  backend/app/v2/capability/__init__.py (empty)
c4a1d17f702e7418ec6eb9774345a9b7797589c3fc8a12ef47068711c9ac3259  backend/app/v2/capability/contract.py
3a2482fd8e907e05cb33f0b05a4b8739564bc57f1d90bcd8d043bdca879282ae  backend/app/v2/capability/seed.py
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  backend/app/v2/api/__init__.py (empty)
4581c6bd0ca54143b34ac6592dafc4b04af86ce478f541c12d5e9d953dd19b71  backend/app/v2/api/router.py
ab000471a7d53a8953883e4a7ac2da0bd54041fb48683e915ecf56e3319d24b8  backend/app/v2/api/mode.py
33061aa720a740fb0df7d160a9f708cfd657c757a8961f2a6daa7e0c14e86614  backend/app/v2/api/capability.py
13dd61fc006209886082b1935f87e4f426e983f4e4770b580cbd374ec2d2ddae  backend/app/v2/api/audit.py
ec229f83c4f218f0b263fc52f6fd08662eca83b7fc2b8a125c24e5c4571c8134  backend/app/v2/api/lineage.py
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  backend/app/v2/models/__init__.py (empty)
1d5122c1b271f73450f02bf50a824e69120f249f65a817fb64be237b38aec837  backend/app/v2/models/mode.py
2b306c4a9fe31847d8ce9aa2b0cd72cb98b894b0633c56f8668a6ea65a3b7f20  backend/app/v2/models/capability.py
2e922522320e7f16624ef34b71a5af44943da3e964dcfaf21108d8492f0b9755  backend/app/v2/models/audit.py
66675a6210041e2cba703046327c61850f77d4faad70d9583a71f41c40b9bf50  backend/app/v2/models/lineage.py
576871e1fcebf11336232e89d174e133d00cb93bbfe1b84db9b67d1b516c40f7  backend/app/v2/models/errors.py
da9f01b661eb8ea025d4d7de8f94e3d747712749895b6a8cc0f24fc24fdaaa7d  backend/app/api/routes/v2.py
82fef935ab806df1cf4c169b1516a348017af9437c6cd3a686b81ba063c23433  backend/app/api/router.py
406093d92a23fc21e16d77b3408fd177332df5c0060e8fa3e55de00ac4761c29  backend/app/main.py
f2857d5a1df489feabeb3af4d4c88006adce63f52c3f5dafdf1a8902f6a3533e  backend/tests/test_v2_mode.py
d90349ffd71f524a8345b81ea4034354801e896d1f8ac51df905db3e06fc8e66  backend/tests/test_v2_audit.py
d8894031e34a7a3989e1ef8cad700612b58e05a91a4ba43c67d57928c9b12040  backend/tests/test_v2_temporal.py
caef42edf3b67d99db3da89cf5ffdd9849a0a7fbdd5932338d52282ad0aff3bb  backend/tests/test_v2_rbac.py
0343e11849f6b1bc982677d7ccfb15ed7afb3599209d4dfda6e867101716430f  backend/tests/test_v2_identifiers.py
e11f7e0646ca29aed94db481ce13b35edf03f5f0c7fa9960ab23cf8e5bfd73d8  backend/tests/test_v2_errors.py
37d1d39180aa9cbcc020badb0f2d38dc62aa0fb4aff4c6d7bad62566decf5dfe  backend/tests/test_v2_integration.py
```

Empty-file hash `e3b0c442…` marks empty `__init__.py` package files (no material imports/registration; per ITRGA transcript-format rules they need not be transcribed).

---

## 3. Comparison Against Prior Source Transcripts

The prior DA transcripts (`V2_BE-1_SOURCE_REVIEW_PART_1/2.md`, `_DELTA.md`) are **not in this workspace**; comparison is against the claims and hashes recorded in ITRGA reviews:

| Prior claim reference | Prior state | Current workspace state |
|---|---|---|
| PG-001 §2: migration SHA `caf44c16…` unchanged despite claimed temporal fix | Manifest inconsistency | Current migration SHA is `34ec444d…` — **different from the stale PG-001 hash**, and the file content contains `sa.DateTime(timezone=True)` on all four table definitions and both seed table constructs. The temporal correction is physically present. |
| SOURCE-001 / onboarding warning: `read_by_artifact` operator filter reverted in later transcripts | Uncorrected in submitted transcript | Current source **contains the filter** (see §4, DEF-BE1-01). The workspace does not match the reverted transcript state. |
| DELTA-002: 111 double-collected V2 tests / claimed 81 distinct | Inflated accounting | Static count of current test files: 89 distinct `def test_` cases across 7 files (10+8+5+38+8+10+10). DR-003 claims 89 — **consistent with a non-duplicated static count**, but no test execution has been performed by this replacement DA yet (see §7). |
| DELTA-001: integration file contains static/signature checks only | Defective evidence | **Unchanged in current workspace** — still static (see DEF-BE1-02). |

---

## 4. Claim Classification Table (DEF-BE1-01 … DEF-BE1-07)

Classification legend: **Verified in current workspace** (direct source inspection) / **Contradicted by current workspace** / **Not present / unknown**. Source verification ≠ runtime verification; runtime/test evidence for all items is produced in the remediation phase.

### DEF-BE1-01 — Cross-operator lineage isolation

| Required condition | Current source state | Classification |
|---|---|---|
| Operator lookup filters by `operator_id` at repository/query level | `V2LineageRepository.read_by_artifact()` accepts `operator_id` and applies `stmt.where(V2LineageRecord.operator_id == operator_id)` when provided; `read_by_operator()` always filters. `app/v2/api/lineage.py::get_artifact_lineage` passes `operator_id=operator.id`; list endpoint uses `read_by_operator(operator.id, …)` | **Verified in current workspace** (source) |
| Admin all-record access separately permission-protected and audited | `/lineage/all` guarded by `RequireV2LineageReadAll` (`v2.lineage.read_all`), sensitive read audited | **Verified in current workspace** (source) |
| Tests use real DB/API records for two different operators | `tests/test_v2_integration.py::TestV2LineageOperatorIsolation` contains only `inspect.signature` checks — no operators, no records, no query, no API call | **Contradicted by current workspace** — required test evidence absent |

**Net: source fix present; mandated two-operator DB/API test evidence missing → defect not closable yet.**

### DEF-BE1-02 — False "integration test" claims

| Required condition | Current source state | Classification |
|---|---|---|
| Genuine async DB/API integration tests | `test_v2_integration.py` (38 tests) contains zero `async def`, zero `AsyncSession`/`AsyncClient`/`httpx` usage; all tests are env-var patches, redaction utilities, static RBAC maps, exception objects, clearance maps, and signature inspection | **Contradicted by current workspace** — DELTA-001 condition persists unchanged |
| Required integration paths (audit append+redaction persistence, lineage append, trigger refusal, two-operator isolation, admin read_all, sensitive-read audit persistence, generic denial, safe exception response, PG behavior) | None exercised against DB/API in any V2 test file | **Contradicted by current workspace** |
| Non-duplicating collection command + distinct counts | No evidence artifact in workspace records the command used for DR-003's counts | **Not present / unknown** (static distinct count = 89, arithmetically consistent with DR-003) |

### DEF-BE1-03 — Audit classification access enforcement

| Required condition | Current source state | Classification |
|---|---|---|
| Clearance source per role/identity | `ROLE_CLEARANCE` (admin=3/secret, operator=1/internal, unknown=0) + `get_role_clearance()` in `app/v2/audit/contract.py` | **Verified in current workspace** (source) |
| Classification decision before returning audit details | `app/v2/api/audit.py::_to_response(event, user_role)` invokes `filter_details_by_classification()` on every event; both call sites pass `operator.role` | **Verified in current workspace** (source) |
| Redact/withhold for insufficient clearance | Returns `{"_redacted": true, reason: …}` when clearance insufficient | **Verified in current workspace** (source) |
| Reject/handle secret-bearing audit material at write time | Write path applies pattern-based `redact()` to details, but there is **no write-time classification policy** (e.g., rejection or downgrade of `classification="secret"` events); DELTA-003 asked for defined semantics | **Contradicted by current workspace** — write-time secret-classification policy undefined |
| Tests of public/internal/confidential/secret behavior | Unit-level tests of the filter functions exist (static); **no API-level test** proving redaction in actual responses | **Contradicted by current workspace** — API-level test evidence absent |

### DEF-BE1-04 — Permission denial disclosure

| Required condition | Current source state | Classification |
|---|---|---|
| Public response generic `Permission denied` | `require_v2_permission()` raises `HTTPException(403, detail="Permission denied")`; `errors/contract.py::PermissionError` uses `detail="Permission denied"` | **Verified in current workspace** (source) |
| Permission, actor, route, correlation ID, decision retained internally | Log line records permission, role, username. **Route and correlation ID are not logged**, and the denial is not written to the V2 audit store | **Contradicted by current workspace** — internal record incomplete vs. required condition |
| Direct API test proving vocabulary absent from client output | Only a class-level unit test (`test_permission_error_hides_permission_from_detail`); no API request/response test | **Contradicted by current workspace** — API test absent |

### DEF-BE1-05 — V2 error handler registration and contract

| Required condition | Current source state | Classification |
|---|---|---|
| V2 exception handlers registered without changing V1 behavior | `app/main.py` registers `@application.exception_handler(...)` for `V2Error`, `ModeError`, `PermissionError`, `TemporalError`, all returning `v2_error_response()`; V1 handlers untouched | **Verified in current workspace** (source) |
| Safe structured code/detail/correlation/timestamp | `v2_error_response()` returns error_code, detail, correlation_id, timestamp; no stack traces | **Verified in current workspace** (source) |
| Internal-error path | `v2_internal_error_response()` is **defined but not registered** for any exception type; V2 internal errors would fall through to default/V1 handling | **Contradicted by current workspace** — internal-error contract unwired |
| Direct API tests for mode/permission/temporal/internal-error responses | None exist (no API-level error tests in any V2 test file) | **Contradicted by current workspace** — test evidence absent |

### DEF-BE1-06 — Response-envelope consistency

| Required condition | Current source state | Classification |
|---|---|---|
| Explicit Pydantic envelope for single-capability response | `GET /capabilities/{capability_id}` returns an **untyped raw dict** (`{"capability": …, "mode": …, "correlation_id": …, "timestamp": …}`) with **no `response_model`** on the route decorator | **Contradicted by current workspace** — fields present but explicit typed envelope model absent; required condition explicitly demands a Pydantic model, not a raw dictionary |
| All V2 endpoints include mode/correlation/timestamp | List endpoints (mode, capabilities, audit ×2, lineage ×3) use typed list-response models containing the context fields | **Verified in current workspace** (source), except the single-capability envelope above |
| Tests assert response schema | No API-level schema assertion tests exist | **Contradicted by current workspace** — test evidence absent |

### DEF-BE1-07 — PostgreSQL migration verification

| Required condition | Current source state | Classification |
|---|---|---|
| Timezone-aware seed and model definitions retained | Migration: all `created_at` columns `sa.DateTime(timezone=True)`; seed table constructs use `sa.DateTime(timezone=True)` with `datetime.now(timezone.utc)` values. All four V2 ORM models use `DateTime(timezone=True)` | **Verified in current workspace** (source) |
| V2 model imports retained in Alembic metadata | `app/db/models/__init__.py` imports all four V2 models with the explicit comment "must be imported so Alembic target_metadata includes them"; `alembic/env.py` imports `app.db.models` before `target_metadata = Base.metadata` | **Verified in current workspace** (source) |
| Dialect-aware triggers | Migration contains PostgreSQL (`CREATE OR REPLACE FUNCTION` + trigger) and SQLite (`CREATE TRIGGER … RAISE(ABORT, …)`) branches for audit and lineage tables | **Verified in current workspace** (source) |
| PostgreSQL re-run after any BE-1 correction touching migration/models/metadata; drift/trigger/mutation-refusal evidence | No PostgreSQL runtime evidence exists in this workspace; PostgreSQL execution occurs in the Operator verification environment | **Not present / unknown** — runtime evidence must be (re)produced during remediation; will be re-required if remediation touches migration/models/metadata |

---

## 5. Corrective Action List (mapped exactly to DEF-BE1-01 … 07)

No action below is implemented yet. Implementation begins only after ITRGA accepts this intake.

| # | Defect | Planned corrective action (bounded to BO-V2-BE-1-001) |
|---|---|---|
| CA-01 | DEF-BE1-01 | Retain the present source fix. Add genuine async two-operator DB tests (repository level) and API tests (list + artifact lookup) proving cross-operator lookups return no protected records and admin `read_all` requires `v2.lineage.read_all` and is audited. |
| CA-02 | DEF-BE1-02 | Replace/extend `test_v2_integration.py` with real async database/API integration tests using the configured test DB and `httpx.AsyncClient`, covering all ten required paths: audit append + persisted redaction; lineage append; audit/lineage UPDATE/DELETE trigger refusal; two-operator list isolation; two-operator artifact-lookup isolation; admin `read_all`; sensitive-read audit persistence; generic public permission denial; safe V2 exception response; SQLite (and PostgreSQL-where-available) migration/trigger behavior. Relabel any remaining static checks as unit tests. Adopt single non-duplicating collection (`pytest tests/test_v2_*.py`) and report distinct file/case counts. |
| CA-03 | DEF-BE1-03 | Define and enforce a write-time policy for secret-bearing audit material (reject or downgrade `classification="secret"` per plan semantics, in addition to existing pattern redaction). Add API-level tests proving response behavior for public/internal/confidential/secret events against operator and admin identities. Keep the existing read-path classification filtering. |
| CA-04 | DEF-BE1-04 | Extend the internal denial record to include route and correlation ID (log and/or V2 audit event) while keeping the public response generic. Add a direct API test asserting the denial body contains no permission vocabulary. |
| CA-05 | DEF-BE1-05 | Register the V2 internal-error path narrowly (scoped so V1 behavior is unchanged) so unhandled exceptions on V2 routes return `v2_internal_error_response()`. Add direct API tests for mode, permission, temporal, and internal-error responses asserting no stack trace/internal detail leakage. |
| CA-06 | DEF-BE1-06 | Introduce `V2CapabilityDetailResponse` (Pydantic envelope: capability, mode, correlation_id, timestamp), set it as `response_model` on the single-capability route, and add schema-assertion tests for every V2 endpoint response contract. |
| CA-07 | DEF-BE1-07 | Preserve temporal/metadata source state. After CA-01…06 are implemented: run SQLite migration upgrade/downgrade + trigger existence/removal + mutation-refusal + `alembic check` drift comparison in the DA workspace and capture literal output. Because remediation may touch models/tests (not intended to touch the migration), request Operator-run PostgreSQL re-verification per the existing command pack, with evidence returned through the review channel. |

Sequencing note: CA-03/04/05/06 are source changes; CA-01/02 are test construction; CA-07 is verification evidence. A consolidated plain-text source delta transcript with old→new SHA-256 manifest will accompany the corrected Delivery Report, per `ITRGA-REQ-V2-BE-1-DELTA-001` format.

---

## 6. No-Scope-Expansion Declaration

The replacement DA declares that remediation will be strictly limited to BE-1 corrective scope:

- No Paper/Live mode work; `AXIOM_V2_MODE` remains RESEARCH/SIMULATION only.
- No providers, brokers, exchanges, real market data, accounts, balances, positions, orders, fills, execution, paper trading, or reconciliation.
- No external AI providers or assistant actions.
- No frontend implementation.
- No production deployment or certification claims.
- No new tables, no new endpoints beyond the authorized read set (one typed response model for an existing endpoint is a contract correction, not a new capability).
- No V1 source/behavior changes beyond the already-authorized additive integration points; no modification of V1 historical governance or evidence.
- No refactoring outside defect scope.

---

## 7. Environment, Database Dialect, Migration Head, and Test-Command Inventory

| Item | Value |
|---|---|
| Workspace | `/home/user/axiom` (DA sandbox; filesystem rename of clone root to `axiom` — Operator-directed) |
| Python | 3.13.14 |
| Backend stack | FastAPI ≥0.115, SQLAlchemy[asyncio] ≥2.0.36, Alembic ≥1.14, Pydantic ≥2.9 |
| Dev/test dialect | SQLite via `aiosqlite` (V1 baseline convention) |
| Production-equivalent dialect | PostgreSQL via `asyncpg` — **not available in this DA workspace**; PostgreSQL verification is Operator-environment work (PostgreSQL 18.4 per PG-002) |
| Migration head (static file inspection) | `20260823_0038_v2_be1_core.py` (down_revision → `20260717_0037`) |
| V2 test inventory (static, distinct) | 7 files / 89 test cases: mode 8, audit 10, temporal 10, rbac 10, identifiers 5, errors 8, integration 38 |
| V1 test inventory (static) | 92 test files under `backend/tests/` (V1 baseline claim: 552 cases — **not re-executed by this DA yet**) |
| Canonical non-duplicating V2 command | `pytest tests/test_v2_*.py -v --tb=short` |
| Full-suite command | `pytest tests/ --tb=short -q` |
| Migration commands | `alembic upgrade head` / `alembic downgrade 20260717_0037` / `alembic check` |
| Execution status | **No test, migration, or server execution has been performed by the replacement DA in this intake phase.** All §4 findings are static Level-I source-inspection facts. Runtime results will be produced and reported in the remediation phase with literal output and exit codes. |

Known inherited (carried, not concealed): V1 Ruff lint (33 errors) + format debt; V1 model/migration drift on fresh SQLite `alembic check`; dev-baseline evidence ≠ production certification.

---

## 8. Git/GitHub Operation Confirmation

- **No Git/GitHub operation was performed as part of this intake** — no commit, tag, push, branch, merge, or history modification. All intake work was read-only source inspection and hash generation.
- Full session Git disclosure for the record: (a) the initial `git clone` was performed under direct Operator instruction before the custody boundary was communicated; (b) a **single Operator-authorized, one-time, read-only** `git fetch` + fast-forward (`edc1124 → 9c78afa`, Operator commit "DA UPLOADS") was performed solely to receive the Operator-supplied governance corpus, with explicit Operator authorization recorded in-session. No write operation to the remote has ever been performed by the DA.
- The Git boundary is re-sealed. This intake document itself is supplied as a workspace file through the review channel — the DA will not commit or push it.

---

## 9. Open Items Requiring ITRGA/Operator Input

| # | Item | Needed from |
|---|---|---|
| R-9.1 | `ITRGA-REV-V2-BE-1-005` (final plan approval document) — not in supplied corpus; understood only via Build Order citation | ITRGA (supply or confirm citation suffices) |
| R-9.2 | `ITRGA_DETERMINATION_V2_BE-1_POSTGRESQL_ENVIRONMENTAL_EXCEPTION.md` — operative constraints inferred from PG-001/PG-002 | ITRGA (supply or confirm inference) |
| R-9.3 | `V2_BE-1_POSTGRESQL_VERIFICATION_COMMAND_PACK.md` — required for CA-07 Operator rerun | Operator/ITRGA |
| R-9.4 | Write-time policy decision for `classification="secret"` audit events (reject vs. downgrade) if the approved plan v3.1.0 wording is deemed ambiguous | ITRGA (DA will propose rejection-with-audited-refusal as default) |

---

## 10. Submission Statement

This intake is a reconciliation record, not a Delivery Report and not a correction submission. No source file was modified. The replacement DA requests ITRGA acceptance of this intake and authorization to execute corrective actions CA-01 through CA-07 within BO-V2-BE-1-001.

**We don't guess. We prove.**

**End of Replacement DA Intake**
