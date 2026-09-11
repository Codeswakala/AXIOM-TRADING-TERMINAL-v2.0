# AXIOM V2 BE-1 — Core V2 Domain, Audit, and Mode Framework Design Plan

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BE-1-DA-PLAN-001 |
| Document Type | DA Engineering Design Plan |
| Status | **CORRECTED v3.1.0 — RESUBMITTED FOR ITRGA REVIEW** |
| Version | 3.1.0 |
| Date | 2026-08-23 |
| Author | Development Authority (DA) |
| Source Request | `ITRGA-REQ-V2-BE-1-001` |
| Prior Version | 2.0.0 — returned with CORRECTION REQUIRED |
| Review References | `ITRGA-REV-V2-BE-1-001`, `ITRGA-REV-V2-BE-1-002`, `ITRGA-REV-V2-BE-1-003` |
| Implementation Authority | **NONE — this is a design plan only** |

---

# Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-08-23 | Initial submission |
| 2.0.0 | 2026-08-23 | Corrected per ITRGA findings V2-BE1-001 through V2-BE1-SEC-004 |
| 3.0.0 | 2026-08-23 | Corrected per ITRGA findings V2-BE1-PLAN-007 through V2-BE1-PLAN-010 |
| 3.1.0 | 2026-08-23 | Corrected per ITRGA finding V2-BE1-PLAN-011: migration-drift gate now rejects any V2 schema drift; trigger verification is separate gate |

### Corrections Applied

| Finding | Severity | Correction Summary |
|---------|----------|-------------------|
| V2-BE1-001 | High | Single mode source: `AXIOM_V2_MODE` env var only; `v2_mode_config` table removed |
| V2-BE1-002 | High | Audit/lineage reads scoped by operator_id; admin cross-operator requires explicit permission |
| V2-BE1-003 | High | Audit append-only enforced via DB trigger (no UPDATE/DELETE grants) |
| V2-BE1-004 | Medium | V2 temporal: `require_utc()` only; no `coerce_external_utc()` on V2 paths |
| V2-BE1-005 | Medium | Migration drift bounded: documented baseline; V2 migration adds tables only |
| V2-BE1-006 | Medium | Capability registry is read-only seeded; no runtime mutation |
| V2-BE1-SEC-001 | High | SAL control matrix added with actual protection mechanisms |
| V2-BE1-SEC-002 | Medium | Retention lifecycle: 7-year minimum; archival policy; disposal review |
| V2-BE1-SEC-003 | High | Resource ownership matrix with SAL-aware authorization and sensitive-read audit |
| V2-BE1-SEC-004 | Medium | Capability registry is read-only seeded (option a) |
| V2-BE1-PLAN-007 | High | Dialect-aware immutability: PostgreSQL trigger + SQLite trigger + application-layer enforcement |
| V2-BE1-PLAN-008 | High | Deployment-owned controls reclassified as assumptions; BE-1 application obligations separated |
| V2-BE1-PLAN-009 | Medium | v2_permission read-only seeded; governance-record preservation; future mutation deferred |
| V2-BE1-PLAN-010 | Medium | Migration drift containment gate: baseline artifact + comparison protocol + acceptance rule |
| V2-BE1-PLAN-011 | High | Drift gate rejects any V2 schema drift; trigger verification is separate gate |

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
| **17_INSTITUTIONAL_SECURITY_STANDARD.md** | **Active — Constitutional** | **Mandatory security framework** |
| ITRGA Request | Active | `ITRGA-REQ-V2-BE-1-001` |

## A.1.1 Security Standard Compliance

The `17_INSTITUTIONAL_SECURITY_STANDARD.md` is a **constitutional governance document**. BE-1 complies with its provisions as detailed in the SAL Control Matrix (§D.8), Resource Ownership Matrix (§D.9), and Retention Lifecycle (§D.10).

**Key security principles applied:**

| Principle | BE-1 Implementation |
|-----------|---------------------|
| Security by Design | Security controls in architecture; not retrofitted |
| Zero Trust | Every V2 endpoint requires authentication; no implicit trust |
| Least Privilege | Minimum permissions per role; operator-scoped queries |
| Defence in Depth | Mode enforced at config → middleware → service |
| Secure by Default | Most secure configuration; no insecure defaults |
| Accountability | Every security-sensitive action generates audit record |
| Explainable Security | All controls documented and independently verifiable |

## A.2 BE-1 Objective

BE-1 builds the **non-actuating core foundations** necessary for all later V2 work: identifiers, audit, lineage, mode enforcement, capability maturity, error taxonomy, temporal integrity, and RBAC extension.

BE-1 is the **first V2 runtime-code band**. It produces actual backend code, schemas, APIs, and tests.

## A.3 In-Scope

| # | Capability | Description |
|---|-----------|-------------|
| 1 | V2 Identifiers | Versioned domain IDs, correlation IDs, causation IDs, actor IDs |
| 2 | Audit Contract | Append-only audit with redaction/classification and DB-enforced immutability |
| 3 | Lineage Contract | Metadata for V2 research/simulation artifacts |
| 4 | Mode Framework | RESEARCH/SIMULATION server-side enforcement (single source) |
| 5 | Capability Registry | Read-only seeded registry (no runtime mutation) |
| 6 | Error/Status Contract | Structured error taxonomy and domain status |
| 7 | Temporal Model | `require_utc()` only; no naive coercion on V2 paths |
| 8 | RBAC Extension | V2 permissions with SAL-aware authorization |
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
| Feature-flag mutation endpoints | Read-only registry; no runtime mutation |

## A.5 BE-0 Observations Carried Forward

| Observation | Impact on BE-1 | Treatment |
|-------------|----------------|-----------|
| V1 Ruff lint/format debt | BE-1 new code must pass current Ruff standards | New code is clean |
| V1 model/migration drift | BE-1 migration adds tables only; drift documented | Drift baseline recorded |
| Dev baseline ≠ production readiness | BE-1 tests are development evidence | Acknowledged |

## A.6 V1 Compatibility Matrix

| V1 Component | BE-1 Interaction | Breaking? |
|--------------|------------------|-----------|
| `audit_events` table | Unchanged; V2 uses separate `v2_audit_events` | No |
| `operators` table | Unchanged; V2 permissions via separate table | No |
| V1 API endpoints | Unchanged | No |
| V1 auth flow | Unchanged | No |
| V1 RBAC | Extended via V2 permission table | No — additive |
| V1 observability | Extended with V2 metrics | No — additive |
| V1 temporal (`core/time.py`) | Reused; V2 uses `require_utc()` only | No |

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
│   │   └── repository.py        # V2 audit repository (append-only)
│   ├── lineage/                 # V2 lineage metadata
│   │   ├── __init__.py
│   │   ├── contract.py          # Lineage metadata contract
│   │   └── repository.py        # Lineage repository (append-only)
│   ├── mode/                    # V2 mode framework
│   │   ├── __init__.py
│   │   ├── contract.py          # Mode definitions (single source)
│   │   └── dependency.py        # FastAPI dependency for mode check
│   ├── capability/              # V2 capability registry (read-only)
│   │   ├── __init__.py
│   │   ├── contract.py          # Maturity states and registry
│   │   └── seed.py              # Seed data for registry
│   ├── errors/                  # V2 error taxonomy
│   │   ├── __init__.py
│   │   ├── contract.py          # Error codes and status
│   │   └── handlers.py          # Error response builders
│   ├── temporal/                # V2 temporal model
│   │   ├── __init__.py
│   │   └── validation.py        # require_utc() enforcement
│   ├── rbac/                    # V2 RBAC extension
│   │   ├── __init__.py
│   │   ├── permissions.py       # V2 permission definitions
│   │   └── dependencies.py      # FastAPI permission dependencies
│   ├── api/                     # V2 API routes
│   │   ├── __init__.py
│   │   ├── router.py            # V2 aggregate router
│   │   ├── mode.py              # Mode status endpoint (read-only)
│   │   ├── capability.py        # Capability registry endpoint (read-only)
│   │   └── audit.py             # V2 audit read endpoint (operator-scoped)
│   └── models/                  # V2 Pydantic models
│       ├── __init__.py
│       ├── audit.py             # Audit response models
│       ├── lineage.py           # Lineage models
│       ├── mode.py              # Mode models
│       ├── capability.py        # Capability models
│       └── errors.py            # Error response models
├── db/models/                   # EXISTING: V2 tables added
│   ├── v2_audit_event.py        # NEW: V2 audit event table
│   ├── v2_lineage_record.py     # NEW: V2 lineage table
│   ├── v2_capability_record.py  # NEW: V2 capability registry table
│   └── v2_permission.py         # NEW: V2 permission table
└── api/routes/                  # EXISTING: V2 router mounted
    └── v2.py                    # NEW: V2 route mount
```

## B.2 Source of Truth Ownership

| Domain | Owner | Storage | Immutability |
|--------|-------|---------|--------------|
| Mode | `AXIOM_V2_MODE` env var | Config only | Immutable at runtime |
| Audit | `v2/audit/` + `v2_audit_event` table | DB | Append-only (DB-enforced) |
| Lineage | `v2/lineage/` + `v2_lineage_record` table | DB | Append-only (DB-enforced) |
| Capability | `v2/capability/` + `v2_capability_record` table | DB | Read-only seeded |
| Identifiers | `v2/identifiers.py` | Stateless | N/A |
| Errors | `v2/errors/contract.py` | Stateless | N/A |
| Temporal | `v2/temporal/validation.py` + `core/time.py` | Stateless | N/A |
| RBAC | `v2/rbac/` + `v2_permission` table | DB | Versioned |

## B.3 Schema Design

### Table: `v2_audit_event`

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `id` | UUID | No | Primary key |
| `correlation_id` | String(64) | No | Request correlation |
| `causation_id` | String(64) | Yes | Triggering event ID |
| `actor_id` | String(128) | No | Operator/system/job ID |
| `actor_type` | String(32) | No | `operator`, `system`, `job` |
| `domain` | String(64) | No | V2 domain |
| `action` | String(128) | No | Event action |
| `resource_type` | String(64) | Yes | Resource type |
| `resource_id` | String(128) | Yes | Resource ID |
| `mode` | String(16) | No | `RESEARCH` or `SIMULATION` |
| `details` | JSON | Yes | Redacted event details |
| `classification` | String(32) | No | `public`, `internal`, `confidential`, `secret` |
| `operator_id` | String(128) | Yes | Owning operator (for scoping) |
| `created_at` | DateTime(tz) | No | Event timestamp |

**Indexes:** `(domain, created_at)`, `(actor_id)`, `(correlation_id)`, `(mode)`, `(operator_id)`

**Immutability enforcement:** Dialect-aware strategy:

**PostgreSQL (production):** DB trigger prevents UPDATE/DELETE on `v2_audit_event`:
```sql
CREATE OR REPLACE FUNCTION prevent_audit_mutation()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'V2 audit events are immutable; UPDATE/DELETE prohibited';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER v2_audit_immutable
    BEFORE UPDATE OR DELETE ON v2_audit_event
    FOR EACH ROW EXECUTE FUNCTION prevent_audit_mutation();
```

**SQLite (development/testing):** SQLite supports `BEFORE UPDATE` and `BEFORE DELETE` triggers:
```sql
CREATE TRIGGER v2_audit_immutable_update
    BEFORE UPDATE ON v2_audit_event
    BEGIN
        SELECT RAISE(ABORT, 'V2 audit events are immutable; UPDATE prohibited');
    END;

CREATE TRIGGER v2_audit_immutable_delete
    BEFORE DELETE ON v2_audit_event
    BEGIN
        SELECT RAISE(ABORT, 'V2 audit events are immutable; DELETE prohibited');
    END;
```

**Application-layer enforcement (both dialects):** The V2 audit repository class provides only `append()` method. No `update()` or `delete()` methods exist. SQLAlchemy ORM operations are restricted to `session.add()` only.

**Migration strategy:** The Alembic migration uses `op.execute()` with dialect detection:
```python
def upgrade():
    # Create table
    op.create_table('v2_audit_event', ...)
    
    # Dialect-aware trigger creation
    bind = op.get_bind()
    if bind.dialect.name == 'postgresql':
        op.execute("CREATE FUNCTION ... PL/pgSQL ...")
        op.execute("CREATE TRIGGER ... EXECUTE FUNCTION ...")
    elif bind.dialect.name == 'sqlite':
        op.execute("CREATE TRIGGER v2_audit_immutable_update ...")
        op.execute("CREATE TRIGGER v2_audit_immutable_delete ...")

def downgrade():
    bind = op.get_bind()
    if bind.dialect.name == 'postgresql':
        op.execute("DROP TRIGGER IF EXISTS v2_audit_immutable ON v2_audit_event")
        op.execute("DROP FUNCTION IF EXISTS prevent_audit_mutation()")
    elif bind.dialect.name == 'sqlite':
        op.execute("DROP TRIGGER IF EXISTS v2_audit_immutable_update")
        op.execute("DROP TRIGGER IF EXISTS v2_audit_immutable_delete")
    op.drop_table('v2_audit_event')
```

**Test strategy:** Identical `test_audit_update_blocked` and `test_audit_delete_blocked` tests run on both SQLite (CI) and PostgreSQL (production-equivalent) to verify dialect-equivalent behavior.

### Table: `v2_lineage_record`

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `id` | UUID | No | Primary key |
| `artifact_type` | String(64) | No | Artifact type |
| `artifact_id` | String(128) | No | Artifact ID |
| `source_artifact_ids` | JSON | Yes | Source artifact ID list |
| `computation_version` | String(64) | Yes | Computation/model version |
| `input_snapshot_id` | String(128) | Yes | Input data snapshot ID |
| `operator_id` | String(128) | No | Creating operator |
| `mode` | String(16) | No | `RESEARCH` or `SIMULATION` |
| `created_at` | DateTime(tz) | No | Record timestamp |

**Indexes:** `(artifact_type, artifact_id)`, `(operator_id)`, `(mode)`

**Immutability enforcement:** Same dialect-aware trigger pattern as audit (PostgreSQL trigger + SQLite trigger + application-layer enforcement).

### Table: `v2_capability_record`

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `id` | UUID | No | Primary key |
| `capability_id` | String(128) | No | Unique capability ID |
| `domain` | String(64) | No | Domain |
| `band` | String(16) | No | Roadmap band |
| `maturity` | String(32) | No | Maturity state |
| `artifact_status` | String(32) | No | Document/code status |
| `version` | String(16) | No | Registry version |
| `created_at` | DateTime(tz) | No | Record timestamp |

**Note:** No `enabled` column. Registry is read-only seeded. No runtime mutation.

**Indexes:** `(capability_id)` unique, `(domain)`, `(band)`

### Table: `v2_permission`

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `id` | UUID | No | Primary key |
| `role` | String(32) | No | Role name |
| `permission` | String(128) | No | Permission string |
| `sal` | String(16) | No | Security Assurance Level |
| `created_at` | DateTime(tz) | No | Record timestamp |

**Indexes:** `(role, permission)` unique

## B.4 Retention, Immutability, Redaction, and PII/Secret Treatment

| Data Type | Retention | Immutability | Redaction |
|-----------|-----------|--------------|-----------|
| Audit events | 7-year minimum; archival after; disposal review | DB trigger enforced | `details` field redacted before storage |
| Lineage records | 7-year minimum; archival after; disposal review | DB trigger enforced | No secrets in lineage |
| Capability records | Permanent (read-only reference) | No mutation | N/A |
| Permissions | Permanent (governance reference) | Versioned | N/A |

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

| Method | Path | Permission | SAL | Description |
|--------|------|------------|-----|-------------|
| GET | `/api/v2/mode` | `v2.mode.read` | SAL-2 | Current mode status |
| GET | `/api/v2/capabilities` | `v2.capability.read` | SAL-2 | Capability registry |
| GET | `/api/v2/capabilities/{id}` | `v2.capability.read` | SAL-2 | Single capability |
| GET | `/api/v2/audit` | `v2.audit.read` | SAL-3 | V2 audit events (operator-scoped) |
| GET | `/api/v2/lineage` | `v2.lineage.read` | SAL-3 | Lineage records (operator-scoped) |
| GET | `/api/v2/lineage/{artifact_type}/{artifact_id}` | `v2.lineage.read` | SAL-3 | Artifact lineage |
| GET | `/api/v2/errors` | `v2.error.read` | SAL-2 | Error taxonomy reference |

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

## C.2 Single Source of Truth

**Mode is determined by a single source: the `AXIOM_V2_MODE` environment variable.**

There is **no** `v2_mode_config` database table. Mode cannot be changed at runtime via API, database, or any client input.

```python
# v2/mode/contract.py
import os

VALID_MODES = ("RESEARCH", "SIMULATION")

def get_mode() -> str:
    """Return the configured V2 mode. Immutable at runtime."""
    mode = os.environ.get("AXIOM_V2_MODE", "RESEARCH").upper()
    if mode not in VALID_MODES:
        raise ValueError(f"AXIOM_V2_MODE must be one of {VALID_MODES}, got: {mode}")
    return mode
```

## C.3 Server-Side Enforcement

Mode is enforced at **two layers**:

1. **Configuration layer:** `AXIOM_V2_MODE` environment variable (immutable at runtime)
2. **Dependency layer:** FastAPI dependency injects mode into every request

```python
# v2/mode/dependency.py
from fastapi import Depends, Request

def get_request_mode(request: Request) -> str:
    """FastAPI dependency: mode from config, not from client."""
    return request.app.state.v2_mode

def require_mode(*allowed: str):
    """Dependency factory: reject requests not in allowed modes."""
    def checker(mode: str = Depends(get_request_mode)):
        if mode not in allowed:
            from v2.errors.contract import V2ErrorCode
            raise ModeError(V2ErrorCode.MODE_NOT_AUTHORIZED, mode)
        return mode
    return checker
```

## C.4 Mode Cannot Be Changed by Browser

| Vector | Protection |
|--------|------------|
| API request header | Ignored; mode from config only |
| Query parameter | Ignored; mode from config only |
| Request body | Ignored; mode from config only |
| WebSocket message | Ignored; mode from config only |
| Cookie | Ignored; mode from config only |
| Database mutation | No mode table exists |

**Proof:** Mode is read from `AXIOM_V2_MODE` environment variable at application startup. No API endpoint, middleware, or service accepts mode from client input. No database table stores mode state.

## C.5 Unsupported Paper/Live Treatment

| Request Type | Response |
|--------------|----------|
| Paper mode request | `403 Forbidden` — `mode.not_authorized` |
| Live mode request | `403 Forbidden` — `mode.not_authorized` |
| Paper/Live in audit record | Refused; mode field restricted to RESEARCH/SIMULATION |

## C.6 Mode Propagation

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
| Update | **DB trigger prevents UPDATE** |
| Delete | **DB trigger prevents DELETE** |
| Failure behavior | `AuditWriteFailureRecord` persisted (V1 pattern) |
| Retention | 7-year minimum; archival after; disposal review |

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
    operator_id: str | None  # Owning operator (for scoping)
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

Per `17_INSTITUTIONAL_SECURITY_STANDARD.md` Part VI:
- **Default Deny:** Access denied unless explicitly authorized
- **Explicit Permission Grant:** Permissions assigned to roles
- **Least Privilege:** Minimum capabilities necessary
- **Complete Auditability:** All authorization events audited

### New V2 Permissions

| Permission | Description | Admin | Operator | SAL |
|------------|-------------|-------|----------|-----|
| `v2.mode.read` | Read current mode | ✅ | ✅ | SAL-2 |
| `v2.capability.read` | Read capability registry | ✅ | ✅ | SAL-2 |
| `v2.audit.read` | Read V2 audit events (own) | ✅ | ✅ | SAL-3 |
| `v2.audit.read_all` | Read all V2 audit events | ✅ | ❌ | SAL-4 |
| `v2.lineage.read` | Read lineage records (own) | ✅ | ✅ | SAL-3 |
| `v2.lineage.read_all` | Read all lineage records | ✅ | ❌ | SAL-4 |
| `v2.error.read` | Read error taxonomy | ✅ | ✅ | SAL-2 |

### Permission Enforcement

```python
V2_ROLE_PERMISSIONS = {
    "admin": frozenset({
        "v2.mode.read", "v2.capability.read",
        "v2.audit.read", "v2.audit.read_all",
        "v2.lineage.read", "v2.lineage.read_all",
        "v2.error.read",
    }),
    "operator": frozenset({
        "v2.mode.read", "v2.capability.read",
        "v2.audit.read", "v2.lineage.read",
        "v2.error.read",
    }),
}
```

### Forbidden Permission Markers

```python
V2_FORBIDDEN_PERMISSION_MARKERS = (
    "gate", "execution", "execute", "order", "broker",
    "account", "position", "live", "capital", "margin",
)
```

## D.7 Threat Model

Per `17_INSTITUTIONAL_SECURITY_STANDARD.md` Part XIX:

| Threat | Severity | SAL | Mitigation | Verification |
|--------|----------|-----|------------|--------------|
| Mode bypass (client sets mode) | Critical | SAL-4 | Mode from env var only; no DB table; no client input | Security test |
| Cross-operator data exposure | High | SAL-3 | Operator-scoped queries; `v2.audit.read_all` for admin only | Authorization test |
| Audit failure (silent loss) | High | SAL-3 | `AuditWriteFailureRecord` (V1 pattern) | Failure-path test |
| Log/secret leakage | High | SAL-4 | Redaction before storage | Security test |
| Data tampering | High | SAL-3 | DB trigger prevents UPDATE/DELETE | Integration test |
| Replay attacks | Medium | SAL-3 | Correlation ID dedup | Security test |
| Privilege escalation | High | SAL-4 | Default-deny RBAC; forbidden markers | Authorization test |
| Input validation bypass | Medium | SAL-3 | Pydantic validation | Security test |
| Temporal manipulation | Medium | SAL-3 | `require_utc()` only; no coercion | Temporal test |
| Feature flag tampering | N/A | N/A | No feature flags; read-only registry | N/A |

## D.8 SAL Control Matrix

Per `17_INSTITUTIONAL_SECURITY_STANDARD.md` §4.4:

| Asset | SAL | Storage Protection | Transmission | Backup | Monitoring | Access Control |
|-------|-----|-------------------|--------------|--------|------------|----------------|
| V2 audit events | SAL-3 | See §D.8.1 | See §D.8.1 | See §D.8.1 | Audit-write failure alerts (BE-1) | Operator-scoped; admin `read_all` |
| V2 lineage records | SAL-3 | See §D.8.1 | See §D.8.1 | See §D.8.1 | Lineage-write failure alerts (BE-1) | Operator-scoped; admin `read_all` |
| V2 capability registry | SAL-2 | See §D.8.1 | See §D.8.1 | See §D.8.1 | Standard | Read-only; all authenticated |
| V2 permissions | SAL-4 | See §D.8.1 | See §D.8.1 | See §D.8.1 | Permission-change alerts (BE-1) | Admin-only read |
| V2 mode config | SAL-4 | Env var (not in DB) | N/A (startup only) | Env var in deployment config | Mode-mismatch alerts (BE-1) | Immutable at runtime |
| V2 API endpoints | SAL-3 | N/A | JWT auth (BE-1) | N/A | Request logging (BE-1) | RBAC per endpoint |

### §D.8.1 Deployment-Owned Controls — Classification and Evidence Boundary

The following controls are **deployment-owned** and are NOT verified by BE-1 implementation evidence:

| Control | Owner | BE-1 Status | Evidence Required |
|---------|-------|-------------|-------------------|
| PostgreSQL encryption at rest | Deployment/Infrastructure | **Assumption — not verified** | Deployment configuration evidence; not BE-1 scope |
| HTTPS/TLS in transit | Deployment/Reverse Proxy | **Assumption — not verified** | Deployment configuration evidence; not BE-1 scope |
| Daily DB backup | Operations | **Assumption — not verified** | Operational procedure evidence; not BE-1 scope |
| Backup encryption | Operations | **Assumption — not verified** | Operational procedure evidence; not BE-1 scope |
| Monitoring/alerting infrastructure | Operations | **Assumption — not verified** | Monitoring system evidence; not BE-1 scope |

**BE-1 application obligations (verified by BE-1 evidence):**

| Control | Implementation | Evidence |
|---------|---------------|----------|
| JWT authentication | V1 `auth/security.py` (inherited, tested) | V1 test suite |
| RBAC enforcement | V2 permission table + dependency | BE-1 authorization tests |
| Audit-write failure detection | `AuditWriteFailureRecord` pattern | BE-1 failure-path tests |
| Sensitive field redaction | `v2/audit/redaction.py` | BE-1 security tests |
| Mode enforcement | `AXIOM_V2_MODE` env var + dependency | BE-1 mode tests |
| Operator-scoped queries | `operator_id` filter in repository | BE-1 authorization tests |
| Request logging | V1 observability middleware (inherited) | V1 test suite |

**BE-1 is NOT production/SAL certification evidence.** BE-1 produces development/test evidence. Production SAL certification requires separate deployment evidence for encryption, backup, monitoring, and infrastructure controls per Document 17 §4.8.

## D.9 Resource Ownership Matrix

Per `17_INSTITUTIONAL_SECURITY_STANDARD.md` §6.8, §8.5:

| Resource | Data Owner | SAL | Default Visibility | Operator Scope | Admin Exception | Sensitive-Read Audit | Retention Owner | Access Review |
|----------|------------|-----|-------------------|----------------|-----------------|---------------------|-----------------|---------------|
| `v2_audit_event` | Platform Governance | SAL-3 | Own events only | `operator_id` filter | `read_all` permission | Yes (logged) | Governance | Annual |
| `v2_lineage_record` | Platform Governance | SAL-3 | Own records only | `operator_id` filter | `read_all` permission | Yes (logged) | Governance | Annual |
| `v2_capability_record` | DA | SAL-2 | All authenticated | N/A | N/A | No | DA | Per release |
| `v2_permission` | Platform Governance | SAL-4 | Admin only | N/A | N/A | Yes (logged) | Governance | Quarterly |

## D.10 Retention Lifecycle

Per `17_INSTITUTIONAL_SECURITY_STANDARD.md` §8.11:

| Asset | Minimum Retention | Archive Policy | Disposal Policy | Review Cadence | Preservation Hold | Owner |
|-------|-------------------|----------------|-----------------|----------------|-------------------|-------|
| V2 audit events | 7 years | After 7 years: move to cold storage | After 10 years: secure disposal with audit | Annual | Litigation/regulatory hold overrides disposal | Platform Governance |
| V2 lineage records | 7 years | After 7 years: move to cold storage | After 10 years: secure disposal with audit | Annual | Litigation/regulatory hold overrides disposal | Platform Governance |
| V2 capability records | Governance-record preservation | No archive (reference data) | Superseded versions archived; current version retained | Per release | N/A | DA |
| V2 permissions | Governance-record preservation | No archive (governance reference) | Superseded versions archived; current version retained | Quarterly | N/A | Platform Governance |

**Governance-record preservation:** Capability and permission records are institutional governance records. They are retained as long as they remain operationally relevant. Superseded versions are archived (not disposed) to preserve governance history. Disposal requires explicit governance approval and audit.

**Disposal audit:** Every disposal event generates an audit record with: asset type, record count, disposal method, authorizing identity, timestamp.

### D.10.1 v2_permission Table — Read-Only Seeded in BE-1

The `v2_permission` table is **read-only seeded** in BE-1:

| Aspect | BE-1 Design |
|--------|-------------|
| Source | `app/v2/rbac/permissions.py` (Python constant `V2_ROLE_PERMISSIONS`) |
| Seed mechanism | Migration inserts rows from the constant |
| Runtime mutation | **None** — no API endpoint, service method, or ORM operation modifies `v2_permission` |
| Future mutation | Deferred to a future band with explicit SAL-4 controls (approval, audit, revocation, review) |
| Immutability | Application-layer enforced: repository provides `read_by_role()` only; no `update()` or `delete()` |

**Future mutation design (deferred):** If administrative permission mutation is needed, it requires:
- SAL-4 approval workflow
- Audit of all permission changes
- Revocation capability
- Periodic review
- Separate Build Order with security review

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

Per `17_INSTITUTIONAL_SECURITY_STANDARD.md` §10.14, §12.10:

| Response Type | Public Detail | Internal Detail | Logged |
|---------------|---------------|-----------------|--------|
| 400 Bad Request | Validation error message | Field-level details | Yes |
| 401 Unauthorized | "Authentication required" | Token validation details | Yes |
| 403 Forbidden | "Permission denied" | Permission check details | Yes |
| 404 Not Found | "Resource not found" | Query details | Yes |
| 500 Internal Error | "Internal server error" | Exception details | Yes (never returned) |

## E.4 Temporal Model

| Aspect | Strategy |
|--------|----------|
| Storage | All timestamps as `DateTime(timezone=True)` in UTC |
| Serialization | ISO-8601 with timezone offset |
| V2 input validation | `require_utc()` only — **no `coerce_external_utc()`** |
| Naive datetime at V2 boundary | **Rejected with ValueError** (not warned) |
| V1 compatibility | V1 `coerce_external_utc()` remains for V1 paths only |

**V2 temporal rule:** All V2 code paths use `require_utc()`. Naive datetimes are rejected, not coerced. This eliminates the warning path that could mask timezone defects.

---

# Part F — Implementation and Evidence Plan

## F.1 Implementation Steps

| Step | Description | Files |
|------|-------------|-------|
| 1 | Create V2 module structure | `app/v2/__init__.py` and subdirectories |
| 2 | Implement V2 identifiers | `app/v2/identifiers.py` |
| 3 | Implement V2 error taxonomy | `app/v2/errors/contract.py`, `handlers.py` |
| 4 | Implement V2 temporal validation | `app/v2/temporal/validation.py` |
| 5 | Implement V2 mode framework | `app/v2/mode/contract.py`, `dependency.py` |
| 6 | Implement V2 audit contract | `app/v2/audit/contract.py`, `redaction.py`, `repository.py` |
| 7 | Implement V2 lineage contract | `app/v2/lineage/contract.py`, `repository.py` |
| 8 | Implement V2 capability registry | `app/v2/capability/contract.py`, `seed.py` |
| 9 | Implement V2 RBAC extension | `app/v2/rbac/permissions.py`, `dependencies.py` |
| 10 | Create V2 database models | `app/db/models/v2_*.py` |
| 11 | Create Alembic migration | `alembic/versions/20260823_0038_v2_be1_core.py` |
| 12 | Create DB immutability triggers | In migration file |
| 13 | Implement V2 API routes | `app/v2/api/router.py`, `mode.py`, `capability.py`, `audit.py` |
| 14 | Mount V2 router in main app | `app/api/routes/v2.py`, `app/main.py` |
| 15 | Implement V2 Pydantic models | `app/v2/models/*.py` |
| 16 | Seed capability registry | `app/v2/capability/seed.py` |
| 17 | Write unit tests | `tests/test_v2_*.py` |
| 18 | Write integration tests | `tests/test_v2_integration.py` |
| 19 | Run V1 regression | Verify all V1 tests still pass |
| 20 | Prepare Delivery Report | `DELIVERY_REPORT_V2_BE-1.md` |

## F.2 Schema/Migration Plan

| Item | Value |
|------|-------|
| New tables | 4 (`v2_audit_event`, `v2_lineage_record`, `v2_capability_record`, `v2_permission`) |
| New columns on V1 tables | 0 (V1 tables unchanged) |
| DB triggers | 2 (audit immutability, lineage immutability) |
| Migration file | `20260823_0038_v2_be1_core.py` |
| Rollback | Downgrade drops V2 tables and triggers |

## F.3 Migration Drift Baseline and Containment Gate

### F.3.1 V1 Drift Baseline Artifact

The V1 drift baseline is captured at parent commit `9ab91e76b3ac5f6a42c3066f022700489c214a29`:

```
$ cd backend && AXIOM_ALLOW_INSECURE_DEV=true AXIOM_DATABASE_AUTO_CREATE_SCHEMA=true python -m alembic check
FAILED: New upgrade operations detected
```

**V1 drift operations (documented):**
- Added table: `audit_write_failure_records`
- Added index: `ix_audit_write_failures_category_action`
- Added index: `ix_audit_write_failures_created`
- Removed index: `ix_advisory_signals_expires_at`
- Removed index: `ix_advisory_signals_freshness_status`
- Removed index: `ix_ingestion_runs_symbol_started`
- Removed index: `ix_model_artifacts_advisory_status`
- Removed index: `ix_model_artifacts_artifact_hash`
- Removed index: `ix_model_artifacts_experiment_id`

### F.3.2 BE-1 Drift Containment Gate

**Acceptance rule:** After BE-1 migration upgrade, `alembic check` must report **only** the exact documented inherited V1 drift baseline. Any V2 table, V2 column, V2 index, or other V2 schema operation in the post-BE-1 diff is a **blocking BE-1 defect** unless it is first added to and correctly represented by the approved BE-1 migration.

**Pass/fail criteria:**

| Condition | Result |
|-----------|--------|
| Post-BE-1 `alembic check` shows only V1 drift (documented above) | ✅ PASS |
| Post-BE-1 `alembic check` shows V1 drift + any V2 table/column/index operation | ❌ BLOCKING DEFECT |
| Post-BE-1 `alembic check` shows any unexplained operation | ❌ BLOCKING DEFECT |

**Trigger verification (separate gate):** Alembic autogenerate may not compare triggers. Triggers are verified separately:

| Dialect | Verification Method |
|---------|---------------------|
| PostgreSQL | After upgrade: `SELECT tgname FROM pg_trigger WHERE tgname LIKE 'v2_%'` returns expected triggers. After downgrade: same query returns no V2 triggers. |
| SQLite | After upgrade: `SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%'` returns expected triggers. After downgrade: same query returns no V2 triggers. |
| Application-layer | Test: `session.execute(update(V2AuditEvent).where(...))` raises exception (both dialects). |

### F.3.3 Drift Comparison Protocol

```bash
# Step 1: Capture V1 baseline drift (at parent commit)
cd backend && AXIOM_ALLOW_INSECURE_DEV=true AXIOM_DATABASE_AUTO_CREATE_SCHEMA=true python -m alembic check 2>&1 | tee /tmp/v1_drift.txt
# Expected: FAILED with documented V1 drift operations only

# Step 2: Apply BE-1 migration
cd backend && AXIOM_ALLOW_INSECURE_DEV=true AXIOM_DATABASE_AUTO_CREATE_SCHEMA=true python -m alembic upgrade head

# Step 3: Capture post-BE-1 drift
cd backend && AXIOM_ALLOW_INSECURE_DEV=true AXIOM_DATABASE_AUTO_CREATE_SCHEMA=true python -m alembic check 2>&1 | tee /tmp/be1_drift.txt

# Step 4: Compare
# PASS: be1_drift contains ONLY the same V1 drift operations as v1_drift
# FAIL: be1_drift contains any V2 table/column/index operation (blocking defect)
# FAIL: be1_drift contains any unexplained operation (blocking defect)

# Step 5: Verify triggers (separate gate)
# SQLite:
sqlite3 axiom_dev.db "SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%';"
# Expected: v2_audit_immutable_update, v2_audit_immutable_delete, v2_lineage_immutable_update, v2_lineage_immutable_delete

# Step 6: Verify trigger removal after downgrade
cd backend && AXIOM_ALLOW_INSECURE_DEV=true AXIOM_DATABASE_AUTO_CREATE_SCHEMA=true python -m alembic downgrade -1
sqlite3 axiom_dev.db "SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%';"
# Expected: empty (no V2 triggers)
```

### F.3.4 Dialect Treatment

| Dialect | Drift Check | Notes |
|---------|-------------|-------|
| SQLite (dev/test) | `alembic check` with fresh SQLite | Primary CI verification |
| PostgreSQL (production) | `alembic check` with production-equivalent DB | Production verification (separate from BE-1) |

### F.3.5 Drift Evidence in Delivery Report

The Delivery Report will include:
- V1 baseline drift capture (exact output from `alembic check` at parent commit)
- Post-BE-1 migration drift capture (exact output from `alembic check` after upgrade)
- Comparison: post-BE-1 drift must contain ONLY the documented V1 drift operations
- Trigger verification: query output showing V2 triggers exist after upgrade
- Trigger removal: query output showing V2 triggers removed after downgrade
- Pass/fail determination with explicit criteria

## F.4 Rollback/Containment

| Scenario | Action |
|----------|--------|
| BE-1 migration fails | `alembic downgrade -1` drops V2 tables |
| BE-1 code has defect | V1 unaffected; V2 endpoints return errors |
| V1 regression detected | Revert BE-1 commit; V1 restored |

## F.5 Test Plan

Per `17_INSTITUTIONAL_SECURITY_STANDARD.md` Part XVIII:

| Test Type | Scope | Count (est.) |
|-----------|-------|--------------|
| Unit tests | Identifiers, errors, temporal, mode, audit, lineage, capability, RBAC | ~40 |
| Integration tests | API endpoints, mode enforcement, audit persistence | ~15 |
| Migration tests | Schema creation, rollback, trigger enforcement | ~5 |
| Authorization tests | Permission enforcement, default-deny, cross-operator isolation | ~12 |
| Security tests | Mode bypass, redaction, secret leakage, input validation | ~10 |
| Temporal tests | Naive datetime rejection, timezone validation | ~5 |
| Regression tests | V1 test suite unchanged | 552 backend |
| Failure path tests | Audit failure, mode rejection, temporal violation | ~8 |

**Estimated total: ~95 new tests + 552 V1 regression**

### Security-Specific Test Cases

| Test | Category | Description |
|------|----------|-------------|
| `test_mode_from_env_var_only` | Security | Mode read from `AXIOM_V2_MODE`; no other source |
| `test_mode_returns_403_for_paper` | Authorization | Paper mode request returns 403 |
| `test_mode_returns_403_for_live` | Authorization | Live mode request returns 403 |
| `test_audit_redacts_bearer_tokens` | Security | Bearer tokens redacted before storage |
| `test_audit_redacts_passwords` | Security | Passwords redacted before storage |
| `test_audit_redacts_db_strings` | Security | DB connection strings redacted |
| `test_audit_update_blocked_by_trigger` | Security | UPDATE on audit raises exception |
| `test_audit_delete_blocked_by_trigger` | Security | DELETE on audit raises exception |
| `test_lineage_update_blocked_by_trigger` | Security | UPDATE on lineage raises exception |
| `test_lineage_delete_blocked_by_trigger` | Security | DELETE on lineage raises exception |
| `test_cross_operator_audit_isolation` | Authorization | Operator cannot read other operator's audit |
| `test_admin_can_read_all_audit` | Authorization | Admin with `read_all` can read all audit |
| `test_default_deny_unknown_permission` | Authorization | Unknown permission denied |
| `test_forbidden_markers_rejected` | Security | Execution/broker/order permissions rejected |
| `test_naive_datetime_rejected` | Security | Naive datetime raises ValueError at V2 boundary |
| `test_sensitive_read_logged` | Security | SAL-3/4 read generates audit event |
| `test_error_no_internal_details` | Security | 500 errors don't expose stack traces |
| `test_capability_registry_read_only` | Security | No mutation endpoint exists |

---

# Part G — Risks, Debt, and Open Decisions

## G.1 New Risks

| ID | Risk | Severity | Mitigation |
|----|------|----------|------------|
| V2-R-18 | Mode bypass via env var manipulation | Critical | Env var set at deployment; no runtime change |
| V2-R-19 | Audit trigger failure | High | Trigger tested; failure creates `AuditWriteFailureRecord` |
| V2-R-20 | V2 migration breaks V1 | High | Additive-only; V1 tables unchanged |
| V2-R-21 | V2 RBAC conflicts with V1 | Medium | Separate permission table |
| V2-R-22 | Redaction misses new patterns | Medium | Extensible pattern list |

## G.2 Decisions Requiring Later Review

| Decision | Band | Reason |
|----------|------|--------|
| Paper mode enforcement | BE-8 | Requires specialist security review |
| Live mode enforcement | BE-10 | Requires production certification |
| Provider credential vault | BE-3 | Requires provider selection |
| Broker credential isolation | BE-9 | Requires broker selection |
| Retention policy refinement | BE-2+ | May need legal review |

## G.3 Unknowns

| Unknown | Resolution |
|---------|------------|
| Exact V2 permission granularity | Defined in this plan; may evolve |
| Archive/disposal infrastructure | Inherited from V1 ops; may need dedicated solution |
| Lineage graph depth | Single-hop for now; may add multi-hop later |

---

# Part H — Summary

## H.1 Plan Summary

BE-1 builds the non-actuating core foundations for V2:

1. **Identifiers** — Versioned domain IDs, correlation, causation, actor
2. **Audit** — Append-only with DB-enforced immutability, redaction, classification
3. **Lineage** — Artifact metadata and source tracking (append-only)
4. **Mode** — RESEARCH/SIMULATION from single env var source; no DB table
5. **Capability** — Read-only seeded registry; no runtime mutation
6. **Errors** — Structured error taxonomy and domain status
7. **Temporal** — `require_utc()` only; no naive coercion
8. **RBAC** — V2 permission extension with SAL-aware authorization

## H.2 Corrections Applied

All findings from `ITRGA-REV-V2-BE-1-001`, `ITRGA-REV-V2-BE-1-002`, and `ITRGA-REV-V2-BE-1-003` addressed:

| Finding | Correction |
|---------|------------|
| Competing mode sources | Single source: `AXIOM_V2_MODE` env var; no DB table |
| Broad audit/lineage reads | Operator-scoped; admin `read_all` permission |
| Audit not enforced immutable | Dialect-aware triggers (PostgreSQL + SQLite) + application-layer |
| Naive datetime coercion | V2 uses `require_utc()` only; no coercion |
| Migration drift | Baseline artifact + comparison protocol + acceptance gate |
| Feature-flag mutation | Read-only seeded registry; no mutation |
| SAL controls not designed | SAL Control Matrix with deployment/BE-1 separation |
| Permanent retention | Governance-record preservation; 7-year minimum for audit/lineage |
| Resource ownership undefined | Resource Ownership Matrix added |
| Feature-flag contradicts scope | Read-only registry (option a) |
| DB trigger PostgreSQL-specific | Dialect-aware triggers for PostgreSQL + SQLite |
| Inherited controls asserted | Deployment-owned controls reclassified as assumptions |
| Permission table mutable | Read-only seeded; future mutation deferred |
| Drift containment unmeasurable | Baseline artifact + comparison protocol + acceptance gate |

## H.3 Readiness Statement

> The Development Authority has corrected the BE-1 design plan per all findings. The plan demonstrates enforceable compliance with both V2 governance and the Institutional Security Standard.
>
> The plan requires ITRGA review and a separate Build Order before implementation.

---

**End of V2 BE-1 Design Plan (Corrected v2.0.0)**

**Development Authority · 2026-08-23**
