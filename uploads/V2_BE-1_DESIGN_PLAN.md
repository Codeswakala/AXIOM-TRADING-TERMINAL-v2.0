# AXIOM V2 BE-1 — Core V2 Domain, Audit, and Mode Framework Design Plan

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BE-1-DA-PLAN-001 |
| Document Type | DA Engineering Design Plan |
| Status | **SUBMITTED FOR ITRGA REVIEW** |
| Version | 1.0.0 |
| Date | 2026-08-23 |
| Author | Development Authority (DA) |
| Source Request | `ITRGA-REQ-V2-BE-1-001` |
| Implementation Authority | **NONE — this is a design plan only** |

---

# Part A — Authority, Scope, and V1 Compatibility

## A.1 Source Authorities

| Document | Status | Authority |
|----------|--------|-----------|
| V1 Vision & Principles | Approved | Tier 1 |
| V1 AXIOM Specification | Active | Tier 2 |
| V2 Programme Charter | **APPROVED** (AXIOM-V2-OD-001) | V2 governing context |
| V2 Document Precedence Adoption Record | Active | V2 transition governance |
| V2 Architecture Principles | Active | Binding for Research/Simulation |
| V2 Backend Roadmap | Approved planning | Band BE-1 definition |
| ITRGA Request | Active | `ITRGA-REQ-V2-BE-1-001` |

## A.2 BE-1 Objective

BE-1 builds the **non-actuating core foundations** necessary for all later V2 work: identifiers, audit, lineage, mode enforcement, capability maturity, error taxonomy, temporal integrity, and RBAC extension.

BE-1 is the **first V2 runtime-code band**. It produces actual backend code, schemas, APIs, and tests.

## A.3 In-Scope

| # | Capability | Description |
|---|-----------|-------------|
| 1 | V2 Identifiers | Versioned domain IDs, correlation IDs, causation IDs, actor IDs |
| 2 | Audit Contract | Extended append-oriented audit with redaction/classification |
| 3 | Lineage Contract | Metadata for V2 research/simulation artifacts |
| 4 | Mode Framework | RESEARCH/SIMULATION server-side enforcement |
| 5 | Capability Maturity | Registry read model and feature-flag design |
| 6 | Error/Status Contract | Structured error taxonomy and domain status |
| 7 | Temporal Model | Timezone-aware clock, storage, validation |
| 8 | RBAC Extension | V2 permissions for non-actuating primitives |
| 9 | Schema/API/Migration | Additive strategy for above only |

## A.4 Out-of-Scope (Mandatory Exclusions)

| Item | Exclusion Reason |
|------|-----------------|
| PAPER mode | Requires BE-8 design and security review |
| LIVE mode | Requires BE-10 design and production certification |
| Providers/provider credentials | Requires BE-3 |
| Brokers/exchanges | Requires BE-9 |
| Accounts/balances/orders/fills/positions | Requires BE-8/BE-10 |
| Paper trading | Requires BE-8 |
| Execution | Requires BE-10 |
| External AI providers | Requires BE-11 |
| Frontend redesign | Separate FE bands |
| V1 behavior modification | Additive compatibility only |

## A.5 BE-0 Observations Carried Forward

| Observation | Impact on BE-1 | Treatment |
|-------------|----------------|-----------|
| V1 Ruff lint/format debt (33 errors, 46 files) | BE-1 new code must pass current Ruff standards | New code is clean; V1 debt not addressed |
| V1 model/migration drift (alembic check) | BE-1 migrations must not worsen drift | New tables use Alembic migrations; drift documented |
| Dev baseline ≠ production readiness | BE-1 tests are development evidence, not certification | Acknowledged in Delivery Report |

## A.6 V1 Compatibility Matrix

| V1 Component | BE-1 Interaction | Breaking? |
|--------------|------------------|-----------|
| `audit_events` table | Extended with new columns (causation_id, actor_type, mode) | No — additive |
| `operators` table | Extended with V2 permission fields | No — additive |
| V1 API endpoints | Unchanged | No |
| V1 auth flow | Unchanged | No |
| V1 RBAC | Extended with V2 permissions | No — additive |
| V1 observability | Extended with V2 metrics | No — additive |
| V1 temporal (`core/time.py`) | Reused; no changes | No |

## A.7 Confirmation

This plan **does not introduce** Paper/Live/provider/broker/execution/AI capabilities. All BE-1 work is within the authorized RESEARCH and SIMULATION scope.

---

# Part B — Domain Model and Ownership

## B.1 Proposed Module Structure

```
backend/app/
├── v2/                          # NEW: V2 domain module
│   ├── __init__.py
│   ├── identifiers.py           # V2 ID generation and validation
│   ├── audit/                   # V2 audit extensions
│   │   ├── __init__.py
│   │   ├── contract.py          # Audit event contract
│   │   ├── redaction.py         # Sensitive field redaction
│   │   └── repository.py        # V2 audit repository
│   ├── lineage/                 # V2 lineage metadata
│   │   ├── __init__.py
│   │   ├── contract.py          # Lineage metadata contract
│   │   └── repository.py        # Lineage repository
│   ├── mode/                    # V2 mode framework
│   │   ├── __init__.py
│   │   ├── contract.py          # Mode definitions and enforcement
│   │   ├── dependency.py        # FastAPI dependency for mode check
│   │   └── middleware.py        # Mode propagation middleware
│   ├── capability/              # V2 capability maturity
│   │   ├── __init__.py
│   │   ├── contract.py          # Maturity states and registry
│   │   ├── feature_flags.py     # Feature flag design
│   │   └── repository.py        # Capability read model
│   ├── errors/                  # V2 error taxonomy
│   │   ├── __init__.py
│   │   ├── contract.py          # Error codes and status
│   │   └── handlers.py          # Error response builders
│   ├── temporal/                # V2 temporal model
│   │   ├── __init__.py
│   │   └── validation.py        # Temporal integrity checks
│   ├── rbac/                    # V2 RBAC extension
│   │   ├── __init__.py
│   │   ├── permissions.py       # V2 permission definitions
│   │   └── dependencies.py      # FastAPI permission dependencies
│   ├── api/                     # V2 API routes
│   │   ├── __init__.py
│   │   ├── router.py            # V2 aggregate router
│   │   ├── mode.py              # Mode status endpoint
│   │   ├── capability.py        # Capability registry endpoint
│   │   └── audit.py             # V2 audit read endpoint
│   └── models/                  # V2 Pydantic models
│       ├── __init__.py
│       ├── audit.py             # Audit request/response models
│       ├── lineage.py           # Lineage models
│       ├── mode.py              # Mode models
│       ├── capability.py        # Capability models
│       └── errors.py            # Error response models
├── db/models/                   # EXISTING: extended with V2 tables
│   ├── v2_audit_event.py        # NEW: V2 audit event table
│   ├── v2_lineage_record.py     # NEW: V2 lineage table
│   ├── v2_capability_record.py  # NEW: V2 capability registry table
│   └── v2_mode_config.py        # NEW: V2 mode configuration table
└── api/routes/                  # EXISTING: V2 router mounted here
    └── v2.py                    # NEW: V2 route mount
```

## B.2 Source of Truth Ownership

| Domain | Owner | Storage | Immutability |
|--------|-------|---------|--------------|
| Mode | `v2/mode/contract.py` + `v2_mode_config` table | DB + config | Immutable at runtime |
| Audit | `v2/audit/` + `v2_audit_event` table | DB | Append-only |
| Lineage | `v2/lineage/` + `v2_lineage_record` table | DB | Append-only |
| Capability | `v2/capability/` + `v2_capability_record` table | DB | Versioned |
| Identifiers | `v2/identifiers.py` | Stateless | N/A |
| Errors | `v2/errors/contract.py` | Stateless | N/A |
| Temporal | `v2/temporal/validation.py` + `core/time.py` | Stateless | N/A |
| RBAC | `v2/rbac/` + `operators` table extension | DB | Versioned |

## B.3 Schema Design

### Table: `v2_audit_event`

Extends V1 `audit_events` with V2-specific fields.

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `id` | UUID | No | Primary key |
| `correlation_id` | String(64) | No | Request correlation |
| `causation_id` | String(64) | Yes | Triggering event ID |
| `actor_id` | String(128) | No | Operator/system/job ID |
| `actor_type` | String(32) | No | `operator`, `system`, `job` |
| `domain` | String(64) | No | V2 domain (e.g., `market_data`) |
| `action` | String(128) | No | Event action |
| `resource_type` | String(64) | Yes | Resource type |
| `resource_id` | String(128) | Yes | Resource ID |
| `mode` | String(16) | No | `RESEARCH` or `SIMULATION` |
| `details` | JSON | Yes | Redacted event details |
| `classification` | String(32) | No | `public`, `internal`, `confidential`, `secret` |
| `created_at` | DateTime(tz) | No | Event timestamp |

**Indexes:** `(domain, created_at)`, `(actor_id)`, `(correlation_id)`, `(mode)`

### Table: `v2_lineage_record`

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `id` | UUID | No | Primary key |
| `artifact_type` | String(64) | No | Artifact type |
| `artifact_id` | String(128) | No | Artifact ID |
| `source_artifact_ids` | JSON | Yes | Source artifact ID list |
| `computation_version` | String(64) | Yes | Computation/model version |
| `input_snapshot_id` | String(128) | Yes | Input data snapshot ID |
| `operator_id` | String(128) | Yes | Creating operator |
| `mode` | String(16) | No | `RESEARCH` or `SIMULATION` |
| `created_at` | DateTime(tz) | No | Record timestamp |

**Indexes:** `(artifact_type, artifact_id)`, `(operator_id)`, `(mode)`

### Table: `v2_capability_record`

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `id` | UUID | No | Primary key |
| `capability_id` | String(128) | No | Unique capability ID |
| `domain` | String(64) | No | Domain |
| `band` | String(16) | No | Roadmap band |
| `maturity` | String(32) | No | Maturity state |
| `artifact_status` | String(32) | No | Document/code status |
| `enabled` | Boolean | No | Feature flag |
| `version` | String(16) | No | Registry version |
| `created_at` | DateTime(tz) | No | Record timestamp |
| `updated_at` | DateTime(tz) | No | Last update |

**Indexes:** `(capability_id)` unique, `(domain)`, `(band)`

### Table: `v2_mode_config`

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `id` | UUID | No | Primary key |
| `mode` | String(16) | No | `RESEARCH` or `SIMULATION` |
| `description` | String(256) | No | Mode description |
| `is_active` | Boolean | No | Whether mode is currently active |
| `activated_at` | DateTime(tz) | Yes | When activated |
| `created_at` | DateTime(tz) | No | Record timestamp |

**Indexes:** `(mode)` unique, `(is_active)`

## B.4 Retention, Immutability, Redaction, and PII/Secret Treatment

| Data Type | Retention | Immutability | Redaction |
|-----------|-----------|--------------|-----------|
| Audit events | Permanent | Append-only; no updates/deletes | `details` field redacted before storage |
| Lineage records | Permanent | Append-only; no updates/deletes | No secrets in lineage |
| Capability records | Permanent | Versioned; historical versions preserved | N/A |
| Mode config | Permanent | Immutable at runtime; changed only by authorized admin | N/A |

**Redaction rules (applied before audit storage):**
- JWT tokens → `[REDACTED]`
- Passwords → `[REDACTED]`
- API keys → `[REDACTED]`
- Database connection strings → `[REDACTED]`
- Broker credentials → `[REDACTED]`

## B.5 API Design

### V2 API Prefix

All V2 endpoints use `/api/v2/` prefix. V1 endpoints remain unchanged.

### Endpoints

| Method | Path | Permission | Description |
|--------|------|------------|-------------|
| GET | `/api/v2/mode` | `v2.mode.read` | Current mode status |
| GET | `/api/v2/capabilities` | `v2.capability.read` | Capability registry |
| GET | `/api/v2/capabilities/{id}` | `v2.capability.read` | Single capability |
| GET | `/api/v2/audit` | `v2.audit.read` | V2 audit events |
| GET | `/api/v2/lineage` | `v2.lineage.read` | Lineage records |
| GET | `/api/v2/lineage/{artifact_type}/{artifact_id}` | `v2.lineage.read` | Artifact lineage |
| GET | `/api/v2/errors` | `v2.error.read` | Error taxonomy reference |

### Response Schemas

All V2 responses include:
```json
{
  "mode": "RESEARCH",
  "correlation_id": "...",
  "timestamp": "2026-08-23T...",
  "data": { ... }
}
```

### Error Responses

```json
{
  "error_code": "auth.denied",
  "detail": "Permission denied",
  "correlation_id": "...",
  "timestamp": "2026-08-23T..."
}
```

---

# Part C — Mode Safety

## C.1 Mode Definitions

| Mode | Definition | BE-1 Status |
|------|------------|-------------|
| `RESEARCH` | Read-only analytical work; no external state mutation | **Active** |
| `SIMULATION` | Simulated execution research; no real broker/account state | **Active** |
| `PAPER` | Paper trading with simulated fills | **Deferred to BE-8** |
| `LIVE` | Real broker execution | **Deferred to BE-10** |

## C.2 Server-Side Enforcement

Mode is enforced at **three layers**:

1. **Configuration layer:** `AXIOM_V2_MODE` environment variable (immutable at runtime)
2. **Middleware layer:** Every request carries mode in request state
3. **Service layer:** Every service method checks mode before execution

```python
# Layer 1: Configuration
AXIOM_V2_MODE = "RESEARCH"  # or "SIMULATION"

# Layer 2: Middleware
@app.middleware("http")
async def mode_middleware(request, call_next):
    request.state.mode = get_configured_mode()
    response = await call_next(request)
    response.headers["X-AXIOM-Mode"] = request.state.mode
    return response

# Layer 3: Service
class V2Service:
    def __init__(self, mode: str):
        if mode not in ("RESEARCH", "SIMULATION"):
            raise ModeError(f"Mode {mode} not authorized")
        self._mode = mode
```

## C.3 Mode Cannot Be Changed by Browser

| Vector | Protection |
|--------|------------|
| API request header | Ignored; mode from config only |
| Query parameter | Ignored; mode from config only |
| Request body | Ignored; mode from config only |
| WebSocket message | Ignored; mode from config only |
| Cookie | Ignored; mode from config only |

**Proof:** Mode is read from `AXIOM_V2_MODE` environment variable at application startup. No API endpoint, middleware, or service accepts mode from client input.

## C.4 Unsupported Paper/Live Treatment

| Request Type | Response |
|--------------|----------|
| Paper mode request | `403 Forbidden` — `mode.not_authorized` |
| Live mode request | `403 Forbidden` — `mode.not_authorized` |
| Paper/Live in audit record | Refused; mode field restricted to RESEARCH/SIMULATION |

## C.5 Mode Propagation

| Location | Mode Value | Source |
|----------|------------|--------|
| API response header | `X-AXIOM-Mode` | Config |
| API response body | `mode` field | Config |
| Audit event | `mode` column | Config |
| Lineage record | `mode` column | Config |
| Log entries | `mode` field | Config |

---

# Part D — Audit, Lineage, and Security

## D.1 Audit Semantics

| Property | Value |
|----------|-------|
| Write model | Append-only |
| Update | Prohibited |
| Delete | Prohibited |
| Failure behavior | `AuditWriteFailureRecord` persisted (V1 pattern) |
| Retention | Permanent |

## D.2 Actor/Correlation/Causation Propagation

```
HTTP Request
    ↓
X-Correlation-ID header (or generated)
    ↓
Request state.correlation_id
    ↓
Service layer → Audit event (correlation_id)
    ↓
If event triggers another event:
    triggering event.id → new event.causation_id
```

## D.3 Audit Payload Schema

```python
class V2AuditEventCreate:
    domain: str           # e.g., "market_data", "simulation"
    action: str           # e.g., "data.ingested", "report.created"
    actor_id: str         # operator ID or "system"
    actor_type: str       # "operator", "system", "job"
    resource_type: str | None
    resource_id: str | None
    mode: str             # "RESEARCH" or "SIMULATION"
    details: dict | None  # Redacted before storage
    classification: str   # "public", "internal", "confidential", "secret"
```

## D.4 Sensitive Field Redaction

Applied to `details` before storage:

| Pattern | Replacement |
|---------|-------------|
| Bearer tokens | `[REDACTED]` |
| Passwords | `[REDACTED]` |
| API keys | `[REDACTED]` |
| DB connection strings | `[REDACTED]` |
| Broker credentials | `[REDACTED]` |

Uses existing `observability_service.redact()` pattern.

## D.5 Lineage Relation Model

```
Artifact (report, signal, scenario, etc.)
    ↓
Lineage Record
    ├── artifact_type
    ├── artifact_id
    ├── source_artifact_ids[]  → parent artifacts
    ├── computation_version
    ├── input_snapshot_id
    ├── operator_id
    └── mode
```

## D.6 RBAC Extension

### New V2 Permissions

| Permission | Description | Admin | Operator |
|------------|-------------|-------|----------|
| `v2.mode.read` | Read current mode | ✅ | ✅ |
| `v2.capability.read` | Read capability registry | ✅ | ✅ |
| `v2.audit.read` | Read V2 audit events | ✅ | ✅ |
| `v2.lineage.read` | Read lineage records | ✅ | ✅ |
| `v2.error.read` | Read error taxonomy | ✅ | ✅ |

### Permission Enforcement

```python
V2_ROLE_PERMISSIONS = {
    "admin": frozenset({
        "v2.mode.read", "v2.capability.read", "v2.audit.read",
        "v2.lineage.read", "v2.error.read",
    }),
    "operator": frozenset({
        "v2.mode.read", "v2.capability.read", "v2.audit.read",
        "v2.lineage.read", "v2.error.read",
    }),
}
```

## D.7 Threat Model

| Threat | Severity | Mitigation |
|--------|----------|------------|
| Mode bypass (client sets mode) | Critical | Mode from config only; no client input |
| Cross-operator data exposure | High | Operator-scoped queries; RBAC enforcement |
| Audit failure (silent loss) | High | `AuditWriteFailureRecord` (V1 pattern) |
| Log/secret leakage | High | Redaction before storage; sensitive patterns |
| Data tampering | High | Append-only audit; no update/delete |
| Replay attacks | Medium | Correlation ID dedup; idempotency keys |
| Privilege escalation | High | Default-deny RBAC; permission vocabulary check |

---

# Part E — Error/Status/Temporal Contracts

## E.1 Error Taxonomy

```python
class V2ErrorCode(str, Enum):
    # Data
    DATA_UNAVAILABLE = "data.unavailable"
    DATA_STALE = "data.stale"
    DATA_INSUFFICIENT = "data.insufficient"
    
    # Authorization
    AUTH_DENIED = "auth.denied"
    AUTH_EXPIRED = "auth.expired"
    AUTH_INSUFFICIENT_PERMISSION = "auth.insufficient_permission"
    
    # Mode
    MODE_MISMATCH = "mode.mismatch"
    MODE_NOT_AUTHORIZED = "mode.not_authorized"
    
    # Validation
    VALIDATION_FAILED = "validation.failed"
    TEMPORAL_VIOLATION = "temporal.violation"
    
    # General
    INTERNAL_ERROR = "internal.error"
    NOT_IMPLEMENTED = "not.implemented"
```

## E.2 Domain Status

```python
class V2DomainStatus(str, Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    STALE = "stale"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"
    DENIED = "denied"
```

## E.3 Public/Internal Detail Separation

| Response Type | Public Detail | Internal Detail |
|---------------|---------------|-----------------|
| 400 Bad Request | Validation error message | Field-level details |
| 401 Unauthorized | "Authentication required" | Token validation details |
| 403 Forbidden | "Permission denied" | Permission check details |
| 404 Not Found | "Resource not found" | Query details |
| 500 Internal Error | "Internal server error" | Exception details (logged, not returned) |

## E.4 Temporal Model

| Aspect | Strategy |
|--------|----------|
| Storage | All timestamps as `DateTime(timezone=True)` in UTC |
| Serialization | ISO-8601 with timezone offset |
| Input validation | `require_utc()` for trusted boundaries; `coerce_external_utc()` for external inputs |
| Naive datetime | Rejected at trusted boundaries; assumed UTC at external boundaries with warning |
| V1 compatibility | Reuses `app/core/time.py` unchanged |

---

# Part F — Implementation and Evidence Plan

## F.1 Implementation Steps

| Step | Description | Files |
|------|-------------|-------|
| 1 | Create V2 module structure | `app/v2/__init__.py` and subdirectories |
| 2 | Implement V2 identifiers | `app/v2/identifiers.py` |
| 3 | Implement V2 error taxonomy | `app/v2/errors/contract.py`, `handlers.py` |
| 4 | Implement V2 temporal validation | `app/v2/temporal/validation.py` |
| 5 | Implement V2 mode framework | `app/v2/mode/contract.py`, `dependency.py`, `middleware.py` |
| 6 | Implement V2 audit contract | `app/v2/audit/contract.py`, `redaction.py`, `repository.py` |
| 7 | Implement V2 lineage contract | `app/v2/lineage/contract.py`, `repository.py` |
| 8 | Implement V2 capability registry | `app/v2/capability/contract.py`, `feature_flags.py`, `repository.py` |
| 9 | Implement V2 RBAC extension | `app/v2/rbac/permissions.py`, `dependencies.py` |
| 10 | Create V2 database models | `app/db/models/v2_*.py` |
| 11 | Create Alembic migration | `alembic/versions/20260823_0038_v2_be1_core.py` |
| 12 | Implement V2 API routes | `app/v2/api/router.py`, `mode.py`, `capability.py`, `audit.py` |
| 13 | Mount V2 router in main app | `app/api/routes/v2.py`, `app/main.py` |
| 14 | Implement V2 Pydantic models | `app/v2/models/*.py` |
| 15 | Write unit tests | `tests/test_v2_*.py` |
| 16 | Write integration tests | `tests/test_v2_integration.py` |
| 17 | Run V1 regression | Verify all V1 tests still pass |
| 18 | Prepare Delivery Report | `DELIVERY_REPORT_V2_BE-1.md` |

## F.2 Schema/Migration Plan

| Item | Value |
|------|-------|
| New tables | 4 (`v2_audit_event`, `v2_lineage_record`, `v2_capability_record`, `v2_mode_config`) |
| New columns on V1 tables | 0 (V1 tables unchanged) |
| Migration file | `20260823_0038_v2_be1_core.py` |
| Rollback | Downgrade drops V2 tables only |

## F.3 Rollback/Containment

| Scenario | Action |
|----------|--------|
| BE-1 migration fails | `alembic downgrade -1` drops V2 tables |
| BE-1 code has defect | Disable V2 feature flag; V1 unaffected |
| V1 regression detected | Revert BE-1 commit; V1 restored |

## F.4 Test Plan

| Test Type | Scope | Count (est.) |
|-----------|-------|--------------|
| Unit tests | Identifiers, errors, temporal, mode, audit, lineage, capability, RBAC | ~40 |
| Integration tests | API endpoints, mode enforcement, audit persistence | ~15 |
| Migration tests | Schema creation, rollback | ~3 |
| Authorization tests | Permission enforcement, default-deny | ~10 |
| Security tests | Mode bypass, redaction, secret leakage | ~8 |
| Regression tests | V1 test suite unchanged | 552 backend |
| Failure path tests | Audit failure, mode rejection, temporal violation | ~8 |

**Estimated total: ~84 new tests + 552 V1 regression**

## F.5 Baseline Comparison

| Check | V1 Baseline | BE-1 Expected |
|-------|-------------|---------------|
| Backend tests | 552 passed | 552 + ~84 = ~636 passed |
| Ruff check | 33 exceptions (inherited) | 33 exceptions (unchanged) |
| Ruff format | 46 exceptions (inherited) | 46 exceptions (unchanged) |
| Alembic head | `20260717_0037` | `20260823_0038` |
| Alembic check | Exception (model drift) | Exception (unchanged; V2 tables added) |

## F.6 Delivery Report Structure

1. Executive Summary
2. Objectives Completed
3. Files Created/Modified
4. Schema/Migration Evidence
5. Test Results (with exit codes)
6. V1 Regression Results
7. Security Evidence
8. Mode Safety Evidence
9. Risks and Debt
10. Known Limitations
11. Recommendations for BE-2

---

# Part G — Risks, Debt, and Open Decisions

## G.1 New Risks

| ID | Risk | Severity | Mitigation |
|----|------|----------|------------|
| V2-R-18 | Mode bypass via config manipulation | Critical | Config immutable at runtime; no API to change |
| V2-R-19 | Audit failure causes silent data loss | High | `AuditWriteFailureRecord` pattern from V1 |
| V2-R-20 | V2 migration breaks V1 | High | Additive-only; V1 tables unchanged |
| V2-R-21 | V2 RBAC conflicts with V1 | Medium | Separate permission namespace (`v2.*`) |
| V2-R-22 | Redaction misses new secret patterns | Medium | Extensible pattern list; security review |

## G.2 Decisions Requiring Later Review

| Decision | Band | Reason |
|----------|------|--------|
| Paper mode enforcement | BE-8 | Requires specialist security review |
| Live mode enforcement | BE-10 | Requires production certification |
| Provider credential vault | BE-3 | Requires provider selection |
| Broker credential isolation | BE-9 | Requires broker selection |

## G.3 Unknowns

| Unknown | Resolution |
|---------|------------|
| Exact V2 permission granularity | Defined in this plan; may evolve |
| Audit retention policy | Permanent for now; may add archival later |
| Lineage graph depth | Single-hop for now; may add multi-hop later |

---

# Part H — Summary

## H.1 Plan Summary

BE-1 builds the non-actuating core foundations for V2:

1. **Identifiers** — Versioned domain IDs, correlation, causation, actor
2. **Audit** — Extended append-only audit with redaction/classification
3. **Lineage** — Artifact metadata and source tracking
4. **Mode** — RESEARCH/SIMULATION server-side enforcement
5. **Capability** — Maturity registry and feature flags
6. **Errors** — Structured error taxonomy and domain status
7. **Temporal** — Timezone-aware clock and validation
8. **RBAC** — V2 permission extension

All work is within the authorized RESEARCH/SIMULATION scope. No Paper/Live/provider/broker/execution/AI capabilities are introduced.

## H.2 Readiness Statement

> The Development Authority has completed the BE-1 design plan. The plan is bounded to non-actuating core foundations within the authorized RESEARCH/SIMULATION scope. It does not introduce Paper/Live/provider/broker/execution/AI capabilities.
>
> The plan requires ITRGA review and a separate Build Order before implementation.

---

**End of V2 BE-1 Design Plan**

**Development Authority · 2026-08-23**
