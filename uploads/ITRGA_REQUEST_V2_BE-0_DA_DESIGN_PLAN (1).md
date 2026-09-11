# ITRGA Request — AXIOM V2 BE-0 DA Design Plan

| Field | Value |
|---|---|
| Request ID | ITRGA-REQ-V2-BE-0-001 |
| Issued by | Independent Technical Review & Governance Authority (ITRGA) |
| Date | 2026-08-23 |
| Status | Active request — **not a Build Order** |
| Related roadmap | `docs/plans/V2_BACKEND_ROADMAP.md`, Band BE-0 |
| Related specification | `AXIOM V2 — Product & Architecture Specification` |
| Required recipient | Development Authority (DA) |

---

## 1. Purpose

This request obtains the DA’s bounded engineering design plan for **V2 Backend Band BE-0 — V2 Governance, Baseline, and Architecture Foundation**.

This request does not authorize implementation, repository restructuring, external-provider work, credentials, data-provider access, paper trading, brokers, accounts, orders, positions, execution, external AI, or production deployment.

## 2. Required DA submission

Submit one self-contained document titled:

```text
AXIOM V2 BE-0 — Governance, Baseline and Architecture Foundation Design Plan
```

The plan must be evidence-based, traceable, and limited to BE-0.

## 3. Mandatory plan contents

### A. Authority and scope

- Source authority and current governing status of the V2 specification and approved roadmaps;
- BE-0 objective;
- explicit in-scope and out-of-scope boundaries;
- dependencies and blocking decisions;
- confirmation that the plan itself does not treat V2 as implementation-authorized.

### B. V1 → V2 constitutional and provenance relationship

- proposed V2 constitutional adoption/amendment package required from the Operator;
- document-precedence model during transition;
- V1 preservation rules and historical-record treatment;
- V1 parent baseline, current repository reference, and proposed V2 initialization baseline;
- repository/custody alternatives and recommendation;
- migration inventory for code, tests, docs, data, evidence, technical debt, risks, and prior determinations;
- treatment of historical V1 records when V2 replaces or evolves a component.

### C. Canonical V2 architecture proposal

Provide a clear, bounded architecture for planning purposes, including:

- domain boundaries and responsibility ownership;
- service/module topology;
- API boundary and versioning strategy;
- persistence and schema-ownership strategy;
- event, audit, correlation, and lineage model;
- observability, error taxonomy, and degraded-state strategy;
- configuration, feature-flag, capability-maturity, and environment-mode strategy;
- deployment and rollback assumptions;
- explicit list of architecture decisions that must be deferred to later bands.

Do not present speculative future broker/provider/AI components as implemented or authorized.

### D. BE-0 artifact inventory

List every BE-0 artifact proposed, its owner, purpose, location, authority level, required review, and completion criterion. At minimum consider:

- V2 Programme Charter / Constitutional Adoption Amendment;
- V2 Current State;
- V2 Risk Register;
- V2 Technical Debt Register;
- V2 decision/ADR convention;
- V2 repository/provenance record;
- V2 canonical architecture document;
- V1 regression baseline and test inventory;
- V2 capability maturity registry;
- mode/environment classification design.

### E. Security and governance design baseline

- existing V1 security controls to retain;
- initial threat model for V2 expansion;
- secret/credential isolation principles;
- RBAC/least-privilege implications;
- data classification and audit requirements;
- no-actuation boundary while BE-0 is active;
- explicit security risks deferred to data-provider, paper, execution, broker, and AI bands.

### F. V1 regression baseline

- exact baseline reference and method for recording it;
- existing backend/frontend test/build/type-check commands;
- expected test inventory and environmental prerequisites;
- approach for distinguishing inherited failures, new failures, unavailable environmental dependencies, and verified passes;
- plan for preserving V1 supported behavior during BE-0.

### G. Implementation plan and file scope

- implementation steps, ordered and independently testable;
- files/modules expected to be added, amended, or explicitly left untouched;
- schema/migration impact, if any;
- rollback/containment approach;
- no scope expansion statement.

### H. Test and evidence plan

- unit, integration, architecture, regression, security, and documentation tests applicable to BE-0;
- direct evidence required for completion;
- audit and provenance evidence;
- acceptance criteria mapped to proposed tests/evidence;
- expected Delivery Report contents.

### I. Risks, debt, and open decisions

- new risks introduced by V2 baseline establishment;
- inherited V1 debt/risk that materially affects BE-0;
- decisions requiring Operator action;
- decisions requiring later specialist/security review;
- unknowns stated explicitly, without invented resolution.

## 4. Mandatory exclusions

The plan and any subsequently proposed BE-0 Build Order must exclude:

- implementation of a market-data provider or storage of provider credentials;
- broker, exchange, account, balance, position, order, fill, or execution implementation;
- paper-trading implementation;
- external AI provider integration;
- real market data claim;
- production certification or production deployment;
- frontend redesign beyond evidence/architecture documentation required for planning;
- silent modification of V1 history or governing evidence.

## 5. ITRGA review standard

The ITRGA will review the submitted plan for:

1. constitutional coherence and authority boundary;
2. V1 historical/provenance preservation;
3. bounded scope and exclusions;
4. architecture completeness appropriate to BE-0;
5. security and mode-safety foundations;
6. V1 regression protection;
7. feasible evidence and acceptance criteria;
8. risk/debt disclosure;
9. absence of premature provider, paper, broker, execution, or AI authorization.

## 6. Next state

After a satisfactory DA plan and any required Operator constitutional-adoption decision are supplied, ITRGA may issue a bounded **BE-0 Build Order**. Until then, this request is the only active ITRGA action for the V2 backend workstream.
