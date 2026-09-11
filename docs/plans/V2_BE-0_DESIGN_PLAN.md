# AXIOM V2 BE-0 — Governance, Baseline and Architecture Foundation Design Plan

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BE-0-DA-PLAN-001 |
| Document Type | DA Engineering Design Plan |
| Status | **CORRECTED — RESUBMITTED FOR ITRGA REVIEW** |
| Version | 2.0.0 |
| Date | 2026-08-23 |
| Author | Development Authority (DA) |
| Source Request | `ITRGA-REQ-V2-BE-0-001` |
| Prior Version | 1.0.0 — returned with CORRECTION REQUIRED |
| Review Finding References | V2-BE0-PLAN-001 through V2-BE0-PLAN-005 |
| Related Specification | `AXIOM V2 — Product & Architecture Specification` |
| Related Roadmap | `V2_BACKEND_ROADMAP.md`, Band BE-0 |
| Implementation Authority | **NONE — this is a design plan only** |

---

# Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-08-23 | Initial submission |
| 2.0.0 | 2026-08-23 | Corrected per ITRGA findings V2-BE0-PLAN-001 through V2-BE0-PLAN-005 |

### Corrections Applied

| Finding | Severity | Correction Summary |
|---------|----------|-------------------|
| V2-BE0-PLAN-001 | High | Removed fractional Tier 2.5/3.5/4.5 hierarchy; replaced with active Operator precedence rule from `V2_DOCUMENT_PRECEDENCE_ADOPTION_RECORD.md` |
| V2-BE0-PLAN-002 | High | Recorded same-repository as Operator decision; cited existing precedence adoption record; removed duplicate V2 precedence deliverable; constrained BE-0 modes to RESEARCH and SIMULATION; Paper/Live recorded as future out-of-scope |
| V2-BE0-PLAN-003 | Medium | Replaced `Current HEAD` with full commit SHA; removed unverified test-case counts; distinguished file inventory from executed results; defined baseline tag as post-Build-Order artifact |
| V2-BE0-PLAN-004 | Medium | Separated binding BE-0 decisions from non-binding future candidates; removed future trade permissions and production-facing table/configuration specifics from BE-0 canonical set |
| V2-BE0-PLAN-005 | Medium | Added V2 Amendment Register artifact; defined charter drafting/approval/review/record workflow; clarified DA cannot self-adopt charter |

---

# Part A — Authority and Scope

## A.1 Source Authority

The V2 programme derives authority from:

1. **AXIOM V2 — Product & Architecture Specification** — the proposed V2 product and architecture definition (status: Proposed — Design Stage)
2. **V2 Backend Roadmap** (`V2_BACKEND_ROADMAP.md`) — the proposed 12-band backend decomposition (status: Proposed — planning only)
3. **V2 Frontend Roadmap** (`V2_FRONTEND_ROADMAP.md`) — the proposed 11-band frontend decomposition (status: Proposed — planning only)
4. **ITRGA Request** (`ITRGA-REQ-V2-BE-0-001`) — the formal request for this design plan
5. **V2 Document Precedence Adoption Record** (`V2_DOCUMENT_PRECEDENCE_ADOPTION_RECORD.md`) — active Operator decision on V1/V2 transition governance

**Current governing status:**

| Document | Status | Authority Level |
|----------|--------|-----------------|
| V1 Vision & Principles | Approved (Foundation) | Tier 1 |
| V1 AXIOM Specification | Active | Tier 2 |
| V1 Project Roadmap | Active (Waves 0–7 Complete) | Tier 3 |
| V1 System Architecture v2.0 | Active | Tier 4 |
| V2 Document Precedence Adoption Record | **Active Operator Decision** | Governs V2 transition |
| V2 Product & Architecture Spec | **Proposed — Design Stage** | Not yet adopted |
| V2 Backend Roadmap | **Proposed — planning only** | Not yet adopted |
| V2 Frontend Roadmap | **Proposed — planning only** | Not yet adopted |

**Critical note:** The V2 specification and roadmaps are **proposed documents**. They have not been constitutionally adopted. The active V1 constitutional hierarchy remains binding on V2 per the Operator's precedence decision.

## A.2 BE-0 Objective

Band BE-0 creates the **controlled V2 programme baseline** before any new external, account, execution, provider, or AI capability is designed in code.

BE-0 is a **governance and architecture band**, not a feature band. Its purpose is:

1. Record the V1→V2 provenance relationship
2. Define bounded V2 architecture principles (binding only for Research/Simulation scope)
3. Capture the V1 regression baseline
4. Initialize V2 governance artifacts (risk register, technical debt register, decision records, capability maturity registry, amendment register)
5. Draft a V2 Programme Charter for Operator approval

## A.3 In-Scope

| Item | Scope |
|------|-------|
| V2 Programme Charter (drafted by DA; approved by Operator) | ✅ In scope |
| V2 Amendment Register | ✅ In scope |
| V1 parent baseline recording | ✅ In scope |
| V2 initialization baseline establishment | ✅ In scope |
| V2 canonical architecture principles (binding: Research/Simulation only) | ✅ In scope |
| V2 domain boundary principles (non-binding future candidates for Paper/Live/Broker/Execution/AI) | ✅ In scope |
| V1 regression baseline and test inventory | ✅ In scope |
| V2 Current State document | ✅ In scope |
| V2 Risk Register | ✅ In scope |
| V2 Technical Debt Register | ✅ In scope |
| V2 decision/ADR convention | ✅ In scope |
| V2 capability maturity registry | ✅ In scope |
| Security and governance design baseline | ✅ In scope |

## A.4 Out-of-Scope (Explicit Exclusions)

| Item | Exclusion Reason |
|------|-----------------|
| Market-data provider integration | Requires BE-2/BE-3 |
| Provider credentials or secret storage | Requires BE-3 |
| Broker/exchange connectivity | Requires BE-9 |
| Account, balance, position, order, fill implementation | Requires BE-8/BE-10 |
| Paper trading implementation | Requires BE-8 |
| External AI provider integration | Requires BE-11 |
| Real market data claims | Requires BE-3 |
| Production certification | Separate governance |
| Frontend redesign | Separate FE-0 through FE-10 |
| New backend feature code | BE-0 is governance/architecture only |
| Database schema migrations for new V2 domains | Deferred to BE-1+ |
| Paper/Live mode design | Deferred to BE-8/BE-10 with specialist security review |
| Broker/execution architecture | Deferred to BE-9/BE-10 with specialist security review |

## A.5 Operator Decisions Already Recorded

The following decisions have been made by the Operator and are incorporated into this plan:

| Decision | Source | Status |
|----------|--------|--------|
| V2 continues in the same repository | Operator direction | **ACTIVE** |
| V1 governing documents remain binding on V2 | `V2_DOCUMENT_PRECEDENCE_ADOPTION_RECORD.md` | **ACTIVE** |
| V2 documents may amend V1 only through explicit governed amendment process | `V2_DOCUMENT_PRECEDENCE_ADOPTION_RECORD.md` | **ACTIVE** |
| V1 historical evidence remains immutable | `V2_DOCUMENT_PRECEDENCE_ADOPTION_RECORD.md` | **ACTIVE** |

## A.6 Remaining Dependencies

| Dependency | Owner | Status | Blocking |
|------------|-------|--------|----------|
| V2 Programme Charter adoption | Operator | **PENDING** | Yes — V2 programme not authorized until adopted |
| ITRGA review of this plan | ITRGA | **PENDING** | Yes — determines BE-0 Build Order scope |

## A.7 Confirmation

This plan **does not treat V2 as implementation-authorized**. The V2 specification is a proposed document. This design plan proposes the governance framework for BE-0. The DA drafts the V2 Programme Charter but **cannot self-adopt it** — Operator approval is required.

---

# Part B — V1 → V2 Constitutional and Provenance Relationship

## B.1 Applicable Precedence Rule

Per the active Operator decision in `V2_DOCUMENT_PRECEDENCE_ADOPTION_RECORD.md`:

> **All active V1 governing documents remain binding on AXIOM V2. A V2 governing document may amend a V1 requirement only where it explicitly identifies the affected V1 document/section, states the replacement rule and effective scope, is approved through the established AXIOM governance process, and is recorded in the V2 amendment register. Historical V1 evidence and determinations remain immutable.**

**This means:**

1. The V1 constitutional hierarchy (Tiers 1–10 as defined in `10_CONSTITUTIONAL_HIERARCHY.md`) remains the operative framework
2. V2 documents do **not** receive fractional tiers (no Tier 2.5, 3.5, or 4.5)
3. A V2 document that proposes to amend a V1 requirement must follow the explicit amendment process
4. The V2 Programme Charter, when adopted, becomes a governing document within the existing hierarchy — it does not reorder the tiers

## B.2 V2 Programme Charter — Drafting and Approval Workflow

The V2 Programme Charter is an Operator-owned governance instrument. The workflow is:

```text
DA drafts Charter
    ↓
DA submits Charter to Operator (via Delivery Report)
    ↓
Operator reviews
    ↓
Operator approves (or requests revision)
    ↓
Charter is published in docs/governance/
    ↓
Charter provisions that amend V1 requirements are entered in V2 Amendment Register
    ↓
ITRGA acknowledges Charter as governing context for V2 Build Orders
```

**Responsibilities:**

| Role | Responsibility |
|------|---------------|
| DA | Drafts the Charter; identifies affected V1 sections; proposes replacement rules |
| Operator | Reviews, approves, or rejects the Charter; owns the final document |
| ITRGA | Reviews Charter coherence; acknowledges it as governing context |

**The DA cannot self-adopt the Charter.** The Charter is not active until Operator-approved.

## B.3 V2 Amendment Register

Every V2 provision that amends a V1 requirement must be recorded in the **V2 Amendment Register**.

**Amendment Register entry format:**

| Field | Description |
|-------|-------------|
| Amendment ID | `V2-AMD-NNN` |
| Date | Date of approval |
| Affected V1 Document | Exact filename |
| Affected V1 Section(s) | Section number(s) |
| Prior Rule | The V1 rule being amended |
| Replacement Rule | The new rule |
| Effective Scope | What the amendment applies to |
| Approving Authority | Operator / ITRGA |
| Governing Process | Reference to the approval process used |
| Status | Active / Superseded / Retired |

**Location:** `docs/governance/V2_AMENDMENT_REGISTER.md`

**The Amendment Register is a BE-0 artifact.** It is initialized empty (no amendments yet) and populated as V2 provisions amend V1 requirements.

## B.4 V1 Preservation Rules

| V1 Artifact | Treatment |
|-------------|-----------|
| Build Orders | Immutable historical record — never rewritten |
| Delivery Reports | Immutable historical record — never rewritten |
| ITRGA Determinations | Immutable historical record — never rewritten |
| Technical Debt Register | Preserved; V2 inherits relevant debt |
| Risk Register | Preserved; V2 inherits relevant risks |
| Provenance records | Preserved; V2 provenance builds on V1 |
| Git history | Preserved; V2 does not rewrite V1 commits |
| Alembic migrations | Preserved; V2 migrations extend, not replace |
| Test suite | Preserved; V1 regression baseline recorded |

## B.5 V1 Parent Baseline

| Item | Value |
|------|-------|
| V1 Platform Version | v0.62.0 |
| V1 Commit SHA | `9ab91e76b3ac5f6a42c3066f022700489c214a29` |
| V1 Alembic Head | `20260717_0037` |
| V1 Backend Test Files | 83 (file inventory — not executed count) |
| V1 Frontend Test Files | 188 (file inventory — not executed count) |
| V1 Governance Gate | CLOSED |
| V1 Production Status | NOT CERTIFIED |
| V1 Roadmap Status | Waves 0–7 Complete |

**Note on test counts:** The file inventory (83 backend, 188 frontend) is a count of test *files*, not executed test *cases*. The exact executed test-case count will be measured during BE-0 implementation by running the prescribed commands and capturing Level-II evidence. The current verified capability catalogue states 1,336 tests (476 backend + 860 frontend); this figure will be confirmed or corrected by actual execution.

## B.6 V2 Initialization Baseline

| Item | Value |
|------|-------|
| V2 Initial Version | v2.0.0-alpha.1 |
| V2 Parent Commit | `9ab91e76b3ac5f6a42c3066f022700489c214a29` |
| V2 Initial Baseline Tag | `AXIOM_V2_BE0_BASELINE` (created only after Build Order authorizes it; final SHA recorded at tag creation) |
| V2 Alembic Head | `20260717_0037` (unchanged — no new migrations in BE-0) |

**Baseline tag semantics:** The tag `AXIOM_V2_BE0_BASELINE` is an intended BE-0 artifact. It will be created only after the Build Order authorizes it, applied to the exact commit that completes BE-0, and its SHA recorded in the provenance record. It is not pre-created.

## B.7 Repository Decision

Per Operator direction: **V2 continues in the same repository.**

| Item | Decision |
|------|----------|
| Repository | Same as V1 |
| Rationale | Preserves Git history continuity; V1 provenance intact |
| V2 directories | Added alongside V1; no V1 code relocated |
| Git history | Unmodified; V2 commits are additive |

## B.8 Migration Inventory

| V1 Artifact | V2 Treatment |
|-------------|--------------|
| Backend source code (`app/`) | Preserved; V2 modules added alongside |
| Frontend source code (`frontend/src/`) | Preserved; V2 surfaces added alongside |
| Database models (`app/db/models/`) | Preserved; V2 models added in new modules |
| Alembic migrations | Preserved; V2 migrations extend the chain |
| Backend tests (`tests/`) | Preserved; V2 tests added alongside |
| Frontend tests | Preserved; V2 tests added alongside |
| Governance documents | Preserved; V2 governance documents added |
| Delivery Reports | Preserved as historical record |
| Technical Debt Register | V1 register preserved; V2 register initialized from V1 |
| Risk Register | V1 register preserved; V2 register initialized from V1 |
| Configuration (`.env.example`) | Preserved; V2 configuration variables added (in BE-1+) |

## B.9 Treatment of Historical V1 Records When V2 Evolves a Component

When V2 replaces or evolves a V1 component:

1. The V1 component is **deprecated**, not deleted
2. A deprecation notice is added to the V1 component
3. The V2 component is added alongside or in a new module
4. The V1→V2 mapping is recorded in the V2 architecture document
5. V1 regression tests continue to pass against the V1 component until V2 fully replaces it
6. The switchover is governed by a Build Order

---

# Part C — V2 Architecture Principles

## C.1 Binding BE-0 Architecture Decisions

The following architecture decisions are **binding** for BE-0 and the Research/Simulation scope:

### C.1.1 V1 Preservation

All V1 backend modules, APIs, tests, and database schema remain functional and unchanged during BE-0.

### C.1.2 Single Application Topology

V2 maintains the single FastAPI application topology from V1. New domains are added as Python modules within the existing application.

**Rationale:**
- V1's single-application architecture is proven and operationally simple
- Domain boundaries are enforced through module boundaries, not network boundaries
- Service extraction decisions are deferred to later bands where operational isolation requirements are known

### C.1.3 Additive API Strategy

V2 endpoints are additive to V1. V1 endpoints (`/api/v1/`) remain functional. V2 endpoints use a distinct prefix. The exact prefix strategy is an architecture decision for BE-1.

### C.1.4 Schema Ownership Principle

Each V2 domain owns its database tables. No cross-domain table mutations. V2 tables are distinguishable from V1 tables. V2 migrations extend the Alembic chain; they do not replace V1 migrations.

### C.1.5 Audit and Provenance Principle

Every material V2 state change must be attributable to an actor, a correlation, a mode, and a timestamp. V1's existing correlation-ID and audit infrastructure is the foundation.

### C.1.6 Mode Boundary Principle

BE-0 design scope is limited to **RESEARCH** and **SIMULATION** modes. These are the only modes that BE-0 artifacts may define, configure, or reference as active. Paper and Live modes are recognized as future V2 capabilities that require their own design, security review, and Build Orders.

### C.1.7 Degraded-State Principle

Every V2 API response representing domain state must distinguish: available, unavailable, stale, degraded, unknown, denied. Fabricated success states are prohibited.

### C.1.8 No-Actuation Boundary

BE-0 produces governance and architecture documentation only. No new API endpoints, no external connections, no state mutations.

## C.2 Non-Binding Future V2 Candidates

The following are **non-binding future candidates** — they are recorded as V2 direction but cannot be cited to justify later implementation without their own authorized design and Build Order:

| Candidate Domain | Future Band | Requires |
|------------------|-------------|----------|
| Market data provider abstraction | BE-2 | Provider selection; data governance design |
| Authorized provider adapters | BE-3 | Provider licensing; security review |
| Market context engine | BE-4 | Architecture design for context synthesis |
| ML research expansion | BE-5 | ML governance review |
| Portfolio and risk research | BE-6 | Risk methodology design |
| Backtesting and simulation | BE-7 | Simulation engine design |
| Paper trading | BE-8 | **Specialist security review; paper/live isolation proof** |
| Broker connectivity | BE-9 | **Broker selection; credential vault design; security review** |
| Live execution gateway | BE-10 | **Execution security review; risk gateway design; production certification** |
| External AI providers | BE-11 | **AI safety review; prompt injection defense; data governance** |

**These candidates are not approved architecture.** They represent the V2 product direction as described in the proposed specification and roadmaps. Each requires its own design plan, security review, Build Order, and ITRGA approval.

## C.3 Architecture Decisions Deferred to Later Bands

| Decision | Deferred To | Reason |
|----------|-------------|--------|
| API versioning prefix strategy | BE-1 | Requires V2 API design |
| V2 table naming convention specifics | BE-1 | Requires schema design |
| Provider adapter interface | BE-2/BE-3 | Requires provider selection |
| Broker adapter interface | BE-9 | Requires broker selection |
| Execution gateway protocol | BE-10 | Requires security review |
| AI provider adapter interface | BE-11 | Requires AI safety review |
| Message queue technology | BE-7 | Depends on research job requirements |
| Cache layer technology | BE-2+ | Depends on data volume |
| Service extraction boundaries | BE-10+ | May be needed for execution isolation |
| V2 permission model specifics | BE-1 | Requires RBAC design |
| Error taxonomy specifics | BE-1 | Requires domain design |
| Feature-flag implementation | BE-1 | Requires capability design |

---

# Part D — BE-0 Artifact Inventory

| # | Artifact | Owner | Purpose | Location | Authority | Review | Completion Criterion |
|---|----------|-------|---------|----------|-----------|--------|---------------------|
| D-1 | V2 Programme Charter | **Operator** (DA drafts) | Constitutional adoption of V2 | `docs/governance/V2_PROGRAMME_CHARTER.md` | Operator | ITRGA | Operator approved; published |
| D-2 | V2 Amendment Register | DA | Track V1 amendments | `docs/governance/V2_AMENDMENT_REGISTER.md` | DA | ITRGA | Initialized (empty); format defined |
| D-3 | V2 Current State | DA | V2 programme state tracking | `V2_CURRENT_STATE.md` | DA | ITRGA | Initialized with BE-0 baseline |
| D-4 | V2 Risk Register | DA | V2 risk tracking | `docs/governance/V2_RISK_REGISTER.md` | DA | ITRGA | Initialized from V1 + V2 risks |
| D-5 | V2 Technical Debt Register | DA | V2 debt tracking | `docs/governance/V2_TECHNICAL_DEBT_REGISTER.md` | DA | ITRGA | Initialized from V1 debt |
| D-6 | V2 ADR Convention | DA | Decision record standard | `docs/governance/V2_ADR_CONVENTION.md` | DA | ITRGA | Convention defined |
| D-7 | V2 Provenance Record | DA | Provenance tracking | `docs/governance/V2_PROVENANCE_RECORD.md` | DA | ITRGA | V1 baseline, V2 initialization recorded |
| D-8 | V2 Architecture Principles | DA | Architecture authority (binding: Research/Simulation only) | `docs/governance/V2_ARCHITECTURE_PRINCIPLES.md` | DA | ITRGA | Principles defined; binding/deferred separation clear |
| D-9 | V1 Regression Baseline | DA | V1 behavior preservation | `docs/evidence/V1_REGRESSION_BASELINE.md` | DA | ITRGA | Baseline captured; commands and results documented |
| D-10 | V2 Capability Maturity Registry | DA | Capability tracking | `docs/governance/V2_CAPABILITY_MATURITY.md` | DA | ITRGA | Registry initialized |
| D-11 | BE-0 Design Plan (this document) | DA | Engineering plan | `docs/plans/V2_BE-0_DESIGN_PLAN.md` | DA | ITRGA | Submitted (corrected) |

**Removed from v1.0.0:** D-11 (V2 Document Precedence) — superseded by the active Operator decision in `V2_DOCUMENT_PRECEDENCE_ADOPTION_RECORD.md`. No duplicate artifact is created.

**Added in v2.0.0:** D-2 (V2 Amendment Register) — required by the Operator's precedence decision for tracking V1 amendments.

---

# Part E — Security and Governance Design Baseline

## E.1 V1 Security Controls to Retain

| Control | V1 Status | V2 Treatment |
|---------|-----------|--------------|
| JWT authentication | ✅ Implemented | Retained; extended for V2 |
| RBAC (admin/operator roles) | ✅ Implemented | Extended with V2 permissions (BE-1) |
| Rate limiting | ✅ Implemented | Retained; extended for V2 endpoints |
| Security headers (CSP, HSTS, etc.) | ✅ Implemented | Retained |
| Credential validation | ✅ Implemented | Retained |
| Bootstrap admin controls | ✅ Implemented | Retained |
| Audit logging | ✅ Implemented | Extended with V2 event types |
| Correlation IDs | ✅ Implemented | Extended to all V2 domains |
| WebSocket ticket auth | ✅ Implemented | Retained |
| Input validation (Pydantic) | ✅ Implemented | Retained; extended for V2 models |

## E.2 Initial V2 Threat Model

| Threat | Severity | Mitigation | Band |
|--------|----------|------------|------|
| V2 mode bypass (research→paper/live) | Critical | Mode is server-side, immutable at runtime; BE-0 scope is Research/Simulation only | BE-1 |
| Provider credential exposure | Critical | Credential vault; never in API/logs/frontend | BE-3 |
| Broker credential exposure | Critical | Credential vault; never in API/logs/frontend | BE-9 |
| Execution without authorization | Critical | Default-deny; explicit authorization chain | BE-10 |
| Fabricated market data | High | Source provenance; data quality checks | BE-2 |
| Fabricated account state | High | Authoritative broker read; reconciliation | BE-9 |
| AI prompt injection | High | Input sanitization; output constraints; audit | BE-11 |
| Cross-mode data leakage | High | Mode-tagged queries; RBAC enforcement | BE-1 |
| Replay/duplicate orders | High | Idempotency keys; duplicate detection | BE-8/BE-10 |
| Stale data presented as live | Medium | Freshness indicators; staleness detection | BE-2 |

## E.3 Secret/Credential Isolation Principles

1. **No secrets in source code** — all secrets via environment variables or vault
2. **No secrets in logs** — structured logging with secret redaction
3. **No secrets in API responses** — credential fields never returned
4. **No secrets in frontend** — browser code never receives provider/broker credentials
5. **No secrets in research artifacts** — reports/analyses never contain credentials
6. **No secrets in assistant prompts** — AI context never includes raw credentials
7. **Credential rotation** — support for periodic secret rotation
8. **Credential scoping** — each credential has minimal required permissions

These principles are **binding** for all V2 bands.

## E.4 No-Actuation Boundary While BE-0 Is Active

While BE-0 is the active band:

1. No new API endpoints that modify external state
2. No provider connections
3. No broker connections
4. No order submission
5. No account mutations
6. No external AI calls
7. All new artifacts are governance, architecture, and provenance documentation only

## E.5 Security Risks Deferred to Later Bands

| Risk | Deferred To | Reason |
|------|-------------|--------|
| Provider credential management | BE-3 | Requires provider selection |
| Broker credential management | BE-9 | Requires broker selection |
| Execution security controls | BE-10 | Requires execution architecture |
| AI prompt injection defense | BE-11 | Requires AI provider selection |
| Paper/live mode isolation proof | BE-8 | Requires specialist security review |
| Reconciliation security | BE-9 | Requires broker integration |
| V2 RBAC permission specifics | BE-1 | Requires domain design |

---

# Part F — V1 Regression Baseline

## F.1 Baseline Reference

| Item | Value |
|------|-------|
| V1 Platform Version | v0.62.0 |
| V1 Commit SHA | `9ab91e76b3ac5f6a42c3066f022700489c214a29` |
| V1 Alembic Head | `20260717_0037` |
| V1 Backend Test Files | 83 (file inventory) |
| V1 Frontend Test Files | 188 (file inventory) |
| V1 Executed Test Count | **To be measured during BE-0** (capability catalogue states 476 backend + 860 frontend = 1,336; to be confirmed by execution) |

**Important:** Test-file count is not the same as executed test count. A single test file may contain multiple test functions. The executed count will be captured as Level-II evidence (actual `pytest`/`vitest` output) during BE-0 implementation.

## F.2 Backend Test/Build Commands

| Command | Purpose | Expected Result |
|---------|---------|-----------------|
| `cd backend && python -m pytest tests/ -v` | Run all backend tests; capture executed count | All pass; output captured |
| `cd backend && python -m pytest tests/ --tb=short -q` | Quick test run | All pass |
| `cd backend && python -m ruff check app/` | Lint check | No errors |
| `cd backend && python -m ruff format --check app/` | Format check | No differences |
| `cd backend && alembic upgrade head` | Schema migration | Success |
| `cd backend && alembic check` | Migration check | No pending |

## F.3 Frontend Test/Build Commands

| Command | Purpose | Expected Result |
|---------|---------|-----------------|
| `cd frontend && npm run test` | Run all frontend tests; capture executed count | All pass; output captured |
| `cd frontend && npx tsc -b` | TypeScript compilation | No errors |
| `cd frontend && npm run build` | Production build | Success |

## F.4 Environmental Prerequisites

| Prerequisite | Required For | Notes |
|--------------|-------------|-------|
| Python 3.11+ | Backend | Same as V1 |
| Node.js 18+ | Frontend | Same as V1 |
| PostgreSQL 14+ | Production backend | SQLite for dev/test |
| `AXIOM_JWT_SECRET_KEY` | Auth tests | Set or use `AXIOM_ALLOW_INSECURE_DEV=true` |
| `AXIOM_DATABASE_URL` | Database tests | Default: SQLite |

## F.5 Approach for Distinguishing Test Results

| Category | Definition | Action |
|----------|------------|--------|
| **Inherited failure** | Test existed in V1 and fails in V2 baseline | Record as V1 debt; do not fix in BE-0 |
| **New failure** | Test introduced by BE-0 and fails | Fix before BE-0 completion |
| **Environmental dependency** | Test fails due to missing env (DB, provider) | Record as environmental; mark as skipped |
| **Verified pass** | Test passes in BE-0 baseline | Record in regression baseline |

## F.6 Baseline Measurement Protocol

During BE-0 implementation, the DA will:

1. Run backend tests with verbose output; capture full output as evidence
2. Run frontend tests; capture full output as evidence
3. Record: commit SHA, Python version, Node version, OS, environment variables
4. Count: test files, test functions (from output), passed, failed, skipped, errors
5. Record TypeScript compilation result
6. Record production build result
7. Document all results in `docs/evidence/V1_REGRESSION_BASELINE.md`

The baseline tag `AXIOM_V2_BE0_BASELINE` is created **after** the regression baseline is captured and BE-0 artifacts are complete. Its SHA is recorded in the provenance record.

## F.7 V1 Behavior Preservation Plan

1. **No V1 code modification in BE-0** — BE-0 creates new files only
2. **No V1 API changes** — all V1 endpoints remain functional
3. **No V1 database schema changes** — no new Alembic migrations in BE-0
4. **V1 test suite passes unchanged** — regression verification

---

# Part G — Implementation Plan and File Scope

## G.1 Implementation Steps

BE-0 is a **documentation and architecture band**. Its deliverables are governance documents, not production code.

### Step 1: Record V1 Regression Baseline
- Run V1 backend test suite; capture output
- Run V1 frontend test suite; capture output
- Record environment details
- Document baseline in `docs/evidence/V1_REGRESSION_BASELINE.md`

### Step 2: Create V2 Provenance Record
- Record V1 parent baseline (commit SHA, Alembic head, test file inventory)
- Record V2 initialization baseline intent
- Document in `docs/governance/V2_PROVENANCE_RECORD.md`

### Step 3: Create V2 Amendment Register
- Initialize empty register with format definition
- Document in `docs/governance/V2_AMENDMENT_REGISTER.md`

### Step 4: Create V2 Architecture Principles
- Define binding principles (Research/Simulation scope)
- Define non-binding future candidates
- Document deferral mechanism
- Document in `docs/governance/V2_ARCHITECTURE_PRINCIPLES.md`

### Step 5: Create V2 Capability Maturity Registry
- Initialize registry with all V2 capabilities at DESIGNED state
- Document in `docs/governance/V2_CAPABILITY_MATURITY.md`

### Step 6: Create V2 Risk Register
- Initialize from V1 risks + V2-specific risks
- Document in `docs/governance/V2_RISK_REGISTER.md`

### Step 7: Create V2 Technical Debt Register
- Initialize from V1 debt + V2-specific debt
- Document in `docs/governance/V2_TECHNICAL_DEBT_REGISTER.md`

### Step 8: Create V2 ADR Convention
- Define Architecture Decision Record format and process
- Document in `docs/governance/V2_ADR_CONVENTION.md`

### Step 9: Create V2 Current State
- Initialize programme state tracking
- Document in `V2_CURRENT_STATE.md`

### Step 10: Draft V2 Programme Charter
- Draft charter for Operator approval
- Identify affected V1 sections
- Propose replacement rules where needed
- Document in `docs/governance/V2_PROGRAMME_CHARTER.md`
- **Note:** DA drafts; Operator approves. Charter is not active until approved.

### Step 11: Create BE-0 Baseline Tag
- After all artifacts are complete and regression baseline captured
- Tag the commit as `AXIOM_V2_BE0_BASELINE`
- Record tag SHA in provenance record

### Step 12: Prepare Delivery Report
- Compile all evidence
- Document known limitations
- Submit to ITRGA

## G.2 Files/Modules Expected to Be Added

| File | Purpose |
|------|---------|
| `docs/governance/V2_PROGRAMME_CHARTER.md` | Constitutional adoption (draft) |
| `docs/governance/V2_AMENDMENT_REGISTER.md` | V1 amendment tracking |
| `docs/governance/V2_PROVENANCE_RECORD.md` | Provenance tracking |
| `docs/governance/V2_ARCHITECTURE_PRINCIPLES.md` | Architecture authority |
| `docs/governance/V2_CAPABILITY_MATURITY.md` | Capability registry |
| `docs/governance/V2_RISK_REGISTER.md` | Risk tracking |
| `docs/governance/V2_TECHNICAL_DEBT_REGISTER.md` | Debt tracking |
| `docs/governance/V2_ADR_CONVENTION.md` | Decision records |
| `V2_CURRENT_STATE.md` | Programme state |
| `docs/evidence/V1_REGRESSION_BASELINE.md` | Regression baseline |
| `docs/plans/V2_BE-0_DESIGN_PLAN.md` | This document (corrected) |

## G.3 Files/Modules Explicitly Left Untouched

| File/Module | Reason |
|-------------|--------|
| `backend/app/` (all V1 code) | BE-0 is documentation only |
| `frontend/src/` (all V1 code) | BE-0 is documentation only |
| `backend/alembic/` | No new migrations in BE-0 |
| `backend/tests/` | No new tests in BE-0 (V1 tests run for baseline only) |
| `.env` / `.env.example` | No new configuration in BE-0 |

## G.4 Schema/Migration Impact

**None.** BE-0 creates no new database tables, columns, or migrations. The V1 Alembic head remains `20260717_0037`.

## G.5 Rollback/Containment Approach

Since BE-0 creates only documentation files:

1. **Rollback:** Delete the BE-0 documentation files; V1 is unchanged
2. **Containment:** BE-0 files are additive; they cannot break V1
3. **No code changes:** Zero risk to V1 functionality

## G.6 No Scope Expansion Statement

BE-0 is limited to:
- Governance documentation
- Architecture principles documentation
- Baseline recording
- Risk/debt initialization
- Charter drafting

It does not include:
- New backend code
- New frontend code
- Database migrations
- Configuration changes
- External integrations
- Paper/Live mode design
- Broker/execution architecture

---

# Part H — Test and Evidence Plan

## H.1 Tests Applicable to BE-0

| Test Type | Applicable | Evidence |
|-----------|------------|----------|
| Unit tests | No — no new code | N/A |
| Integration tests | No — no new code | N/A |
| Architecture tests | **Yes** — verify architecture document completeness | Document review |
| Regression tests | **Yes** — verify V1 baseline passes | Test output capture (Level II) |
| Security tests | **Yes** — verify no security regression | Test output capture (Level II) |
| Documentation tests | **Yes** — verify all artifacts exist and are complete | Document inventory |

## H.2 Direct Evidence Required for Completion

| Evidence | Source | Level | Format |
|----------|--------|-------|--------|
| V1 backend test baseline | `pytest` output | **Level II** | Captured text |
| V1 frontend test baseline | `vitest` output | **Level II** | Captured text |
| V1 TypeScript compilation | `tsc -b` output | **Level II** | Captured text |
| V1 commit SHA | `git rev-parse HEAD` | **Level I** | Recorded string |
| V1 Alembic head | `alembic heads` | **Level I** | Recorded string |
| BE-0 artifacts exist | File system | **Level I** | File paths |
| BE-0 artifacts complete | Document review | **Level III** | Content review |
| No V1 code modified | `git diff --name-only` | **Level I** | File list |

## H.3 Audit and Provenance Evidence

| Item | Evidence | Level |
|------|----------|-------|
| V1 parent baseline commit | Full SHA `9ab91e76b3ac5f6a42c3066f022700489c214a29` | Level I |
| V2 initialization baseline tag | Tag name + SHA (created during BE-0) | Level I |
| Document creation timestamps | File metadata | Level I |
| DA authorship | Document headers | Level III |

## H.4 Acceptance Criteria Mapped to Tests/Evidence

| Criterion | Verification Method |
|-----------|---------------------|
| V1 regression baseline captured | Test output files exist; results recorded with commit SHA |
| V2 Programme Charter drafted | Document exists; content complete; identifies affected V1 sections |
| V2 Amendment Register initialized | Document exists; format defined; initially empty |
| V2 architecture principles defined | Document exists; binding/deferred separation clear |
| V2 mode classification limited to Research/Simulation | Mode document references only RESEARCH and SIMULATION as BE-0 scope |
| V2 capability registry initialized | Registry document exists; all capabilities listed |
| V2 risk register initialized | Register document exists; risks enumerated |
| V2 debt register initialized | Register document exists; debt enumerated |
| V2 provenance recorded | Provenance document exists; commit SHA recorded |
| No V1 code modified | `git diff` shows only new files |
| No V1 tests broken | Regression baseline passes |
| Baseline tag created | Tag exists; SHA recorded |

## H.5 Expected Delivery Report Contents

1. Executive Summary
2. Objectives Completed
3. Artifacts Created (inventory)
4. V1 Regression Baseline Results (with executed test counts)
5. Architecture Principles Summary
6. Security Baseline Summary
7. Risks and Debt
8. Known Limitations
9. Recommendations for BE-1
10. Readiness Statement

---

# Part I — Risks, Debt, and Open Decisions

## I.1 New Risks Introduced by V2 Baseline Establishment

| ID | Risk | Severity | Mitigation |
|----|------|----------|------------|
| V2-R-01 | V2 scope creep beyond BE-0 | Medium | Strict exclusions; ITRGA review |
| V2-R-02 | V2 architecture principles too rigid for future changes | Low | Principles defer decisions; non-binding candidates clearly marked |
| V2-R-03 | V1 regression baseline incomplete | Medium | Capture both backend and frontend baselines with Level-II evidence |
| V2-R-04 | Operator delays V2 Programme Charter | Medium | DA cannot proceed without adoption; charter is DA-drafted but Operator-owned |
| V2-R-05 | V2 documentation becomes stale | Low | V2 Current State tracks programme state |

## I.2 Inherited V1 Debt/Risk Materially Affecting BE-0

| V1 Item | Impact on BE-0 | Treatment |
|---------|----------------|-----------|
| V1 frontend legacy CSS (global.css) | None — BE-0 is backend-focused | Record in V2 debt register |
| V1 TerminalChartStage god component | None — BE-0 is backend-focused | Record in V2 debt register |
| V1 monolithic API client | None — BE-0 is backend-focused | Record in V2 debt register |
| V1 production not certified | V2 cannot claim production status | Record in V2 risk register |
| V1 governance gate CLOSED | V2 must maintain gate closure | Record in V2 state |

## I.3 Decisions Requiring Operator Action

| Decision | Required For | Status |
|----------|-------------|--------|
| V2 Programme Charter approval | BE-0 completion | **PENDING** — DA will draft; Operator approves |

## I.4 Decisions Already Made by Operator

| Decision | Source | Status |
|----------|--------|--------|
| V2 continues in same repository | Operator direction | **ACTIVE** |
| V1 governing documents remain binding on V2 | `V2_DOCUMENT_PRECEDENCE_ADOPTION_RECORD.md` | **ACTIVE** |
| V2 documents may amend V1 only through explicit governed amendment process | `V2_DOCUMENT_PRECEDENCE_ADOPTION_RECORD.md` | **ACTIVE** |
| V1 historical evidence remains immutable | `V2_DOCUMENT_PRECEDENCE_ADOPTION_RECORD.md` | **ACTIVE** |

## I.5 Decisions Requiring Later Specialist/Security Review

| Decision | Required For | Band |
|----------|-------------|------|
| Provider adapter security review | Market data provider integration | BE-3 |
| Broker adapter security review | Broker connectivity | BE-9 |
| Execution gateway security review | Live execution | BE-10 |
| AI provider safety review | External AI integration | BE-11 |
| Paper/live mode isolation proof | Paper trading | BE-8 |

## I.6 Unknowns Stated Explicitly

| Unknown | Impact | Resolution |
|---------|--------|------------|
| Which market-data provider to integrate first | Affects BE-3 design | Operator decision; deferred |
| Which broker to integrate first | Affects BE-9 design | Operator decision; deferred |
| Whether external AI is desired | Affects BE-11 scope | Operator decision; deferred |
| V2 performance requirements | Affects architecture | Deferred to implementation bands |
| V2 scalability requirements | Affects architecture | Deferred to implementation bands |
| Exact V1 executed test count | Affects baseline accuracy | Measured during BE-0 implementation |

---

# Part J — Summary and Readiness Statement

## J.1 Plan Summary

This corrected design plan proposes BE-0 as a **governance and architecture band** that:

1. Records the V1→V2 provenance relationship with exact commit SHA
2. Defines bounded V2 architecture principles (binding only for Research/Simulation)
3. Captures the V1 regression baseline with Level-II evidence
4. Initializes V2 governance artifacts including the Amendment Register
5. Drafts a V2 Programme Charter for Operator approval
6. Incorporates all active Operator decisions (same repository, precedence rules)

BE-0 produces **documentation only** — no new code, no database migrations, no configuration changes, no external integrations.

## J.2 Corrections Applied

All five ITRGA findings have been addressed:

1. **V2-BE0-PLAN-001:** Fractional tiers removed; active Operator precedence rule adopted
2. **V2-BE0-PLAN-002:** Same-repository decision recorded; precedence adoption record cited; duplicate deliverable removed; modes constrained to Research/Simulation
3. **V2-BE0-PLAN-003:** Full commit SHA used; test counts marked as to-be-measured; file inventory distinguished from executed results; baseline tag defined as post-Build-Order artifact
4. **V2-BE0-PLAN-004:** Binding decisions separated from non-binding future candidates; future trade permissions removed from BE-0 canonical set
5. **V2-BE0-PLAN-005:** Amendment Register added; charter workflow defined; DA drafting vs Operator approval clarified

## J.3 Readiness Statement

> The Development Authority has corrected the BE-0 design plan per all five ITRGA findings. The plan is now aligned with the active Operator V2 transition-precedence decision, same-repository decision, and Research/Simulation-only BE-0 design scope.
>
> The plan does not authorize implementation of any V2 feature, provider, broker, execution, or AI capability.
>
> The plan requires Operator approval of the V2 Programme Charter before BE-0 Build Order implementation can proceed.
>
> The Development Authority is standing by for ITRGA closure review.

---

**End of V2 BE-0 Design Plan (Corrected)**

**Development Authority · 2026-08-23 · Version 2.0.0**
