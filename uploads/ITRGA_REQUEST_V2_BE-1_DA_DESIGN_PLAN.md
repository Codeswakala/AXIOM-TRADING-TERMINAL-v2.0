# ITRGA Request — AXIOM V2 BE-1 DA Design Plan

| Field | Value |
|---|---|
| Request ID | ITRGA-REQ-V2-BE-1-001 |
| Date | 2026-08-23 |
| Issued by | Independent Technical Review & Governance Authority (ITRGA) |
| Status | Active request — **not a Build Order** |
| Related roadmap | `V2_BACKEND_ROADMAP.md`, Band BE-1 |
| Governing context | `AXIOM-V2-GOV-CHARTER-001` (approved), `AXIOM-V2-OD-001`, active V1 hierarchy and V2 precedence record |
| Required recipient | Development Authority (DA) |

---

## 1. Purpose

Submit a self-contained engineering design plan for **V2 Backend Band BE-1 — Core V2 Domain, Audit, and Mode Framework**.

BE-1 is the first V2 runtime-code planning band. It must build only the non-actuating core foundations necessary for later V2 work, within the currently authorized **RESEARCH** and **SIMULATION** scope.

This request does not authorize implementation. A separate ITRGA review and Build Order are required.

## 2. Authorized planning scope

The DA plan may design only the following capability families:

1. versioned V2 identifiers and correlation/causation/actor context;
2. append-oriented audit-event contract and redaction/classification rules;
3. lineage metadata contract for V2 research/simulation artifacts;
4. V2 Research/Simulation mode framework and server-side mode enforcement;
5. V2 capability-maturity registry/read model and feature-flag design;
6. structured error/refusal/status contract;
7. timezone-aware temporal model and temporal-integrity validation;
8. V2 RBAC/least-privilege extension necessary for the above non-actuating primitives;
9. additive schema/API/migration/testing/rollback strategy for the above only.

## 3. Mandatory exclusions

The plan and any later BE-1 Build Order must exclude:

- PAPER or LIVE mode implementation, configuration, selection, or APIs;
- providers, provider credentials, external market data, brokers, exchanges, accounts, balances, orders, fills, positions, execution, paper trading, or reconciliation;
- external AI providers, assistant tools, or assistant state mutation;
- frontend redesign or user-facing V2 trading/execution UI;
- schema work not essential to the approved BE-1 core primitives;
- modification of V1 behavior except explicitly additive compatibility seams approved through the normal governance process;
- new V1 amendment unless separately identified, justified, and submitted through the V2 Amendment Register process.

## 4. Required design-plan contents

### A. Authority, scope, and V1 compatibility

- source authorities and active Charter context;
- exact in/out scope;
- dependency on BE-0 observations: lint/format debt, Alembic model/migration drift, and development-only baseline limitations;
- V1 compatibility matrix and proposed additive/non-breaking changes;
- explicit confirmation that no Paper/Live/provider/broker/execution/AI capability is introduced.

### B. Domain model and ownership

- proposed bounded modules/services/repositories/models;
- source of truth and ownership for mode, capability, audit, lineage, actor, correlation, causation, and error state;
- schema ownership and migrations, including justification for every proposed new table/field/index;
- retention, immutability, redaction, and PII/secret treatment;
- API design, endpoint permissions, response schemas, versioning, and error/refusal behavior.

### C. Mode safety

- precise definition of `RESEARCH` and `SIMULATION` in BE-1;
- server-side enforcement points and default-deny behavior;
- proof approach that mode cannot be changed through a browser request or untrusted client value;
- treatment of unsupported Paper/Live requests: refusal, absence, or explicit not-authorized state;
- propagation rules for mode in API responses, audit records, and lineage.

### D. Audit, lineage, and security

- append/immutability semantics and failure behavior for audit events;
- actor/correlation/causation propagation;
- audit payload schema and sensitive-field redaction;
- lineage relation model and artifact metadata;
- RBAC extension and least-privilege matrix;
- threat model covering mode bypass, cross-operator data exposure, audit failure, log/secret leakage, data tampering, replay, and privilege escalation.

### E. Error/status/temporal contracts

- exact error taxonomy and public/internal detail separation;
- `available`, `unavailable`, `stale`, `degraded`, `unknown`, and `denied` semantics;
- timezone-aware clock strategy, storage/serialization rules, and prevention of naive datetime boundary warnings;
- migration/compatibility plan for V1 temporal fields where interaction is unavoidable.

### F. Implementation and evidence plan

- ordered implementation steps with limited file scope;
- schema/migration plan and rollback/containment;
- unit, integration, migration, authorization, security, regression, and failure-path tests;
- direct Level-I/II evidence required for delivery;
- baseline comparison and treatment of known V1 lint/format/Alembic-check observations;
- Delivery Report structure and technical-debt/risk update plan.

## 5. ITRGA review criteria

The plan will be reviewed for:

- compliance with active V1 governance and approved V2 Charter;
- Research/Simulation-only boundary;
- additive V1 compatibility and no silent V1 amendment;
- real server-side mode isolation and default deny;
- audit/lineage integrity and secrecy;
- correctly bounded schema/API scope;
- measurable acceptance criteria and feasible evidence;
- clear treatment of inherited V1 baseline observations;
- absence of premature execution/domain capability design.

## 6. Next state

Submit the plan for ITRGA review. No BE-1 implementation may begin until a separate BE-1 Build Order is issued.
