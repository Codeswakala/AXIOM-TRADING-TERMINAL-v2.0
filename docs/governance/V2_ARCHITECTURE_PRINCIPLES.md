# AXIOM V2 — Architecture Principles

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-GOV-ARCH-001 |
| Status | Active |
| Date | 2026-08-23 |
| Author | Development Authority (DA) |
| Build Order | BO-V2-BE-0-001 |
| Scope | Binding for Research/Simulation; non-binding for future candidates |

---

## 1. Binding BE-0 Architecture Principles

These principles are **binding** for all V2 work within the Research/Simulation scope.

### 1.1 V1 Preservation

All V1 backend modules, APIs, tests, and database schema remain functional and unchanged. V2 is additive to V1.

### 1.2 Single Application Topology

V2 maintains the single FastAPI application topology from V1. New domains are added as Python modules within the existing application. Service extraction decisions are deferred to later bands.

### 1.3 Additive API Strategy

V2 endpoints are additive to V1. V1 endpoints (`/api/v1/`) remain functional. V2 endpoints use a distinct prefix (exact prefix decided in BE-1).

### 1.4 Schema Ownership

Each V2 domain owns its database tables. No cross-domain table mutations. V2 tables are distinguishable from V1 tables. V2 migrations extend the Alembic chain.

### 1.5 Audit and Provenance

Every material V2 state change must be attributable to an actor, a correlation, a mode, and a timestamp. V1's correlation-ID and audit infrastructure is the foundation.

### 1.6 Mode Boundary

BE-0 design scope is limited to **RESEARCH** and **SIMULATION** modes. Paper and Live modes are future capabilities requiring their own design, security review, and Build Orders.

### 1.7 Degraded-State Honesty

Every V2 API response representing domain state must distinguish: available, unavailable, stale, degraded, unknown, denied. Fabricated success states are prohibited.

### 1.8 No-Actuation Boundary

BE-0 produces governance and architecture documentation only. No new API endpoints, no external connections, no state mutations.

### 1.9 Secret Isolation

No secrets in source code, logs, API responses, frontend, research artifacts, or assistant prompts. All secrets via environment variables or vault.

### 1.10 Frontend-to-Broker Prohibition

Browser code must never communicate directly with broker/exchange APIs. All execution passes through a controlled backend gateway.

---

## 2. Non-Binding Future V2 Candidates

The following are **non-binding future candidates** — they represent V2 product direction but cannot be cited to justify implementation without their own authorized design and Build Order.

| Candidate Domain | Future Band | Requires |
|------------------|-------------|----------|
| Market data provider abstraction | BE-2 | Provider selection; data governance design |
| Authorized provider adapters | BE-3 | Provider licensing; security review |
| Market context engine | BE-4 | Architecture design for context synthesis |
| ML research expansion | BE-5 | ML governance review |
| Portfolio and risk research | BE-6 | Risk methodology design |
| Backtesting and simulation | BE-7 | Simulation engine design |
| Paper trading | BE-8 | Specialist security review; paper/live isolation proof |
| Broker connectivity | BE-9 | Broker selection; credential vault design; security review |
| Live execution gateway | BE-10 | Execution security review; risk gateway design; production certification |
| External AI providers | BE-11 | AI safety review; prompt injection defense; data governance |

---

## 3. Deferred Architecture Decisions

| Decision | Deferred To | Reason |
|----------|-------------|--------|
| API versioning prefix strategy | BE-1 | Requires V2 API design |
| V2 table naming convention | BE-1 | Requires schema design |
| Provider adapter interface | BE-2/BE-3 | Requires provider selection |
| Broker adapter interface | BE-9 | Requires broker selection |
| Execution gateway protocol | BE-10 | Requires security review |
| AI provider adapter interface | BE-11 | Requires AI safety review |
| Message queue technology | BE-7 | Depends on research job requirements |
| Service extraction boundaries | BE-10+ | May be needed for execution isolation |
| V2 permission model specifics | BE-1 | Requires RBAC design |
| Error taxonomy specifics | BE-1 | Requires domain design |

---

**End of Architecture Principles**
