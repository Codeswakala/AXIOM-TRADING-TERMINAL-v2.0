# BUILD ORDER — AXIOM V2 BE-1: Core Domain, Audit, and Mode Framework

| Field | Value |
|---|---|
| Build Order ID | BO-V2-BE-1-001 |
| Date | 2026-08-23 |
| Issued by | Independent Technical Review & Governance Authority (ITRGA) |
| Status | **AUTHORIZED FOR DA EXECUTION** |
| Governing plan | `AXIOM-V2-BE-1-DA-PLAN-001`, v3.1.0 |
| Plan determination | `ITRGA-REV-V2-BE-1-005` — APPROVED WITH OBSERVATIONS |
| Scope | V2 non-actuating Research/Simulation core runtime primitives only |

---

## 1. Objective

Implement the minimum additive V2 backend foundation for identifiers, audit, lineage, Research/Simulation mode enforcement, read-only capability/permission registry, secure error/status contracts, temporal validation, and restricted V2 read APIs.

## 2. In scope

- `backend/app/v2/` core package and bounded submodules for identifiers, audit, lineage, mode, capability, errors, temporal, RBAC, models, and API routes;
- additive `/api/v2/` authenticated read endpoints for mode, capabilities, audit, lineage, and error taxonomy;
- four new V2 tables only: audit events, lineage records, capability records, permission records;
- read-only seeded capability and permission records;
- `AXIOM_V2_MODE` as the sole effective runtime mode source, limited to `RESEARCH` and `SIMULATION`;
- cross-dialect SQLite/PostgreSQL update/delete prevention for V2 audit and lineage records;
- V2 audit redaction, actor/correlation/causation/mode propagation, and operator-scoped access enforcement;
- timezone-aware V2 validation that rejects naive values;
- one additive Alembic migration with upgrade/downgrade trigger handling;
- unit, integration, authorization, security, temporal, migration, trigger, drift-comparison, and V1 regression tests;
- documentation/state/risk/debt/Delivery Report updates required by the plan.

## 3. Mandatory constraints

1. V1 source/API/schema/behavior remains additive and compatible.
2. No Paper/Live configuration, request, state, API, table, or UI capability.
3. No provider, broker, exchange, account, balance, position, order, fill, paper-trading, execution, external-AI, frontend, deployment, or production work.
4. `AXIOM_V2_MODE` must fail safely for unsupported values; client headers/query/body/cookies/WebSockets/database state must not alter effective mode.
5. V2 audit/lineage read queries must enforce server-side operator scope. `read_all` is admin-only, SAL-4, and sensitive reads are audited.
6. No secret value may persist in V2 audit/lineage payloads. Reject/redact before storage.
7. V2 capability and permission records are read-only seeded; no mutation endpoint/service is allowed.
8. New V2 paths must reject naive datetimes and must not create the inherited V1 warning path.
9. New V2 schema drift is blocking. After migration, `alembic check` may show only the documented inherited V1 drift baseline; any V2 schema operation is a defect.
10. DA performs no Git/GitHub operation. Repository custody remains Operator post-approval work.

## 4. Required tests and evidence

- V2 test coverage for mode injection/bypass refusal, Paper/Live refusal, default deny, cross-operator isolation, admin read-all, sensitive-read audit, redaction, secret rejection, no public update/delete, SQLite/PostgreSQL trigger behavior, V2 temporal rejection, and read-only registry behavior;
- migration upgrade/downgrade on SQLite and PostgreSQL-equivalent environment;
- V1 regression/type/build results with inherited lint/format/migration-drift exceptions accurately classified;
- exact before/after `alembic check` drift evidence, plus trigger existence/removal query evidence;
- API/browser-independent direct endpoint evidence for authenticated, denied, scoped, stale/error, and mode status responses;
- updated V2 Current State, Risk Register, Technical Debt Register, Capability Registry, and Delivery Report.

## 5. Acceptance criteria

BE-1 is ready for ITRGA review only if:

- all in-scope code is implemented and tests pass;
- V1 behavior remains intact under the recorded baseline or exceptions are explicitly classified;
- mode has only the approved config source and refuses invalid/Paper/Live values;
- sensitive audit/lineage data is redacted, scoped, immutable, and authorization-audited;
- both supported dialects enforce update/delete refusal and clean downgrade trigger removal;
- no V2 operation appears in post-migration Alembic drift output;
- no unsupported domain vocabulary/API/permission is introduced;
- all planned governance/evidence artifacts are synchronized;
- no Git operation is attributed to the DA.

## 6. Delivery and next state

The DA must submit a Delivery Report and consolidated non-Git evidence package. ITRGA will review evidence independently. Completion does not authorize BE-2. Operator repository publication/tagging remains post-approval custody work.
