# AXIOM V2 — Proposed Backend Roadmap

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BE-ROADMAP-001 |
| Status | **PROPOSED — planning only** |
| Source | `AXIOM V2 — PRODUCT & ARCHITECTURE SPECIFICATION` (proposed) |
| Relationship to V1 | Preserves V1 evidence and supported behavior; V1 remains the current operational baseline |
| Implementation authority | **None conferred by this document** |
| Approval required | Operator constitutional adoption/amendment, approved V2 architecture, Build Order, and ITRGA review for every implementation unit |

---

## 1. Purpose

This roadmap decomposes the proposed V2 backend into governable capability bands. It is intended to prevent V2 from becoming an uncontrolled collection of providers, models, accounts, trading controls, and AI integrations.

It does not authorize code changes, external accounts, credentials, providers, broker access, paper trading, execution, external AI, or production use.

## 2. Non-negotiable backend invariants

Every V2 backend unit must preserve these rules:

1. **V1 historical truth is immutable.** V1 Build Orders, Delivery Reports, ITRGA determinations, provenance, technical debt, and evidence are not rewritten.
2. **No fabricated domain state.** No fabricated prices, accounts, balances, positions, fills, provider status, performance, research results, or certification status.
3. **Authoritative domain work is server-side.** The terminal consumes governed APIs/read models; it does not calculate authoritative analytical, risk, execution, or account state.
4. **Frontend-to-broker communication is prohibited.** All execution must pass through a separately authorized risk and execution gateway.
5. **Mode isolation is technical, not decorative.** Research, Simulation, Paper, and Live must have enforceable separation.
6. **Execution is default-deny.** No order can exist without authenticated identity, permission, account eligibility, risk evaluation, audit identity, idempotency, and explicit mode.
7. **Provider and broker secrets remain isolated.** They are never exposed to frontend code, general logs, research artifacts, or assistant prompts.
8. **Unknown is an allowed state.** Provider, broker, fill, reconciliation, and model failures must expose a degraded/unknown state; they must not be converted into apparent success.
9. **Every material result is traceable.** Inputs, schema/service/model versions, time, source, owner, lineage, and applicable limitations must be recoverable.

## 3. Delivery model

Each unit shall follow:

```text
Operator direction
→ DA design plan
→ ITRGA plan review
→ Build Order
→ DA implementation
→ tests and direct evidence
→ Delivery Report
→ ITRGA determination
```

No subsequent band opens merely because a prior band is implemented. Each band has its own authorization and exit criteria.

---

# Band BE-0 — V2 Governance, Baseline, and Architecture Foundation

## Objective

Create the controlled V2 programme baseline before any new external, account, execution, provider, or AI capability is designed in code.

## Scope

- V1 parent baseline and V2 initialization-baseline record;
- V2 repository/provenance decision and migration inventory;
- V2 current-state model, risk register, technical-debt register, and decision-record convention;
- canonical V2 architecture decision: service/domain boundaries, ownership, persistence, events, APIs, observability, deployment, retirement;
- V1 regression baseline and test inventory;
- V2 feature/mode/capability maturity registry;
- environment classification and configuration separation design.

## Explicit exclusions

- No provider credentials or integration;
- no account or broker domain;
- no order, fill, position, portfolio account, or execution implementation;
- no external AI provider;
- no production environment claim.

## Exit evidence

- Operator-approved V2 adoption/governance instrument;
- V1/V2 provenance map;
- approved V2 architecture/design plan;
- V1 regression command baseline and results;
- open risks and debt explicitly registered.

---

# Band BE-1 — Core V2 Domain, Audit, and Mode Framework

## Objective

Establish the backend primitives that every later capability requires without introducing real external effects.

## Scope

- versioned domain identifiers, correlation IDs, causation IDs, actor IDs, and audit-event contract;
- durable artifact/lineage metadata contract;
- common status/failure model: `available`, `unavailable`, `stale`, `degraded`, `unknown`, `denied`;
- V2 environment/mode contract: `RESEARCH`, `SIMULATION`, `PAPER`, `LIVE`;
- permission and entitlement model extension, default-deny;
- feature flags/capability registry with maturity states: Designed → Implemented → Tested → Verified → Approved → Authorized → Production Certified;
- structured error and refusal contracts;
- timezone-aware temporal model and temporal-integrity validation.

## Controls

- Audit writes are append-oriented and attributable.
- Mode must be an explicit, immutable part of material state and API response contracts.
- No mode is inferred from a frontend toggle alone.
- Sensitive values are classified/redacted before logs and artifacts.

## Exit evidence

- schema/API contract tests;
- authorization tests for all new mode/capability endpoints;
- audit lineage tests;
- direct database/API evidence of status, mode, correlation, and refusal handling.

---

# Band BE-2 — Market Data Abstraction and Historical Data Integrity

## Objective

Create an internal normalized market-data model that supports V1 simulated data and future authorized sources without implying an external provider exists.

## Scope

- canonical instrument, venue/source, session, quote, bar, tick, depth, event, and dataset-snapshot contracts;
- symbol mapping and provider-neutral normalization;
- data-source state and provenance model;
- data-quality checks: ordering, duplicates, gaps, stale state, timezone, future-data prevention, source/snapshot version;
- immutable historical snapshot metadata;
- read-only data query APIs;
- V1 simulator adapter maintained as a clearly labelled source.

## Explicit exclusions

- No commercial data-provider integration until provider governance is approved;
- no unlicensed data ingestion;
- no representation of simulated data as live;
- no browser-side authoritative aggregation.

## Exit evidence

- adapter contract test harness;
- deterministic V1 simulator regression tests;
- snapshot/replay reproducibility tests;
- error/degraded-state tests;
- API evidence showing source, freshness, timezone, and availability.

---

# Band BE-3 — Authorized Provider Adapters and Market Data Operations

## Objective

Add one provider only after provider governance, licensing, entitlement, security, and operational acceptance are separately approved.

## Scope, per provider

- provider onboarding decision record;
- provider adapter implementation behind the BE-2 contract;
- credential-vault/secret-rotation integration;
- entitlement check and source status;
- rate-limit, retry, backoff, outage, and circuit-breaker behavior;
- source reconciliation and latency/freshness measurement;
- historical/live source state and source-specific audit records;
- provider contract and failure-path testing.

## Hard gates

A provider is not shown as **Integrated** merely because an adapter exists. The product must distinguish:

```text
Architecture candidate
→ Contract tested
→ Integrated
→ Authorized for a defined environment
→ Production certified
```

## Exit evidence

- license/authorization record;
- provider contract suite against approved test/sandbox environment;
- credential isolation evidence;
- source-health evidence;
- no-data/stale/disconnect behavior;
- provenance-visible API evidence.

---

# Band BE-4 — Market Context, Chart Intelligence, and Research Read Models

## Objective

Evolve V1 deterministic analysis into traceable V2 market-context and chart-intelligence read models.

## Scope

- deterministic structure/indicator reuse and versioning;
- multi-timeframe relationship model;
- market-context outputs: trend, structure, levels, session, volatility, momentum, liquidity-related observations;
- chart annotations and contextual explanations tied to input evidence;
- report/artifact model expansion for market context and chart intelligence;
- server-side computation and immutable inputs/versions.

## Controls

- Facts, derived observations, contextual interpretations, and predictions remain separately typed.
- Structural outputs do not imply institutional order flow or execution readiness.
- Insufficient data remains a typed outcome.

## Exit evidence

- deterministic/reproducibility tests;
- temporal-integrity tests;
- lineage from output to source snapshot and computation version;
- direct API and browser evidence of facts versus interpretation.

---

# Band BE-5 — Predictive ML, Signal, and Research Governance Expansion

## Objective

Expand predictive research while preserving V1’s evidence-gated, non-promotional ML discipline.

## Scope

- model/feature/dataset registry evolution;
- model eligibility, calibration, freshness, economic validation, and rollback contracts;
- shadow/champion/challenger metadata;
- distinct structural and predictive signal contracts;
- signal lineage, limitations, uncertainty, and refusal/withholding states;
- research reports, model diagnostics, and evidence artifacts.

## Explicit exclusions

- No execution authority from a signal;
- no live strategy authorization;
- no performance claim without the correct data/mode/result classification;
- no model promotion by UI state or undocumented manual change.

## Exit evidence

- leakage, walk-forward, calibration, and economic-validation evidence;
- signal-family separation tests;
- traceability from signal to model/version/input snapshot;
- supported failure/withheld/expired state tests.

---

# Band BE-6 — Portfolio and Risk Research Domain

## Objective

Introduce portfolio and risk capabilities initially as governed research/read models, independent of live account access or execution.

## Scope

- hypothetical portfolios, allocations, exposures, concentration, factor/risk, scenario and stress-test read models;
- risk metric contracts with method, input, uncertainty, limitations, and time basis;
- report-preview/export contracts only where separately authorized;
- portfolio/risk artifact lineage.

## Explicit exclusions

- No real account state, broker balances, orders, positions, or live P&L in this band;
- no action-oriented risk recommendation that bypasses governance.

## Exit evidence

- numerical method tests and independent recomputation samples;
- uncertainty/assumption visibility;
- data-source and as-of validation;
- UI/API evidence distinguishing hypothetical research from account state.

---

# Band BE-7 — Backtesting, Simulation, Replay, and Governed Research Jobs

## Objective

Build reproducible, non-live strategy/simulation capabilities before any paper-order lifecycle.

## Scope

- historical replay with as-of boundaries;
- backtest input/version registration;
- transaction-cost, spread, slippage, latency, and risk-model configuration;
- temporal-leakage prevention;
- strategy-version lifecycle metadata;
- governed research job queue: owner, authorization, inputs, schedule, output, failure, audit;
- immutable research-result and replay artifacts.

## Controls

- Backtest, simulation, paper, and live results are different typed result classes.
- No scheduled job may silently mutate an institutional artifact or interact with an execution adapter.
- Job retries must be idempotent and audited.

## Exit evidence

- future-leakage tests;
- deterministic replay tests;
- queue/retry/cancel/failure evidence;
- result classification and lineage tests;
- no-live-effect source/API scan.

---

# Band BE-8 — Paper Trading, Paper Account, and Risk Gateway

## Objective

Introduce paper trading only as an isolated, governed environment after a dedicated paper-trading and execution-security design is approved.

## Scope

- paper account model;
- paper order intent and immutable order lifecycle;
- pre-trade risk gateway;
- paper execution simulator;
- simulated fills, positions, balances, margin, P&L, and account reconciliation;
- order status state machine;
- environment isolation and audit;
- operator permissions and confirmation requirements.

## Non-negotiable controls

- Paper credentials, accounts, routes, identifiers, secrets, and adapters are separated from Live.
- A paper order cannot reach a live broker adapter by configuration error, API substitution, or UI mutation.
- Every order carries mode, actor, account, correlation ID, idempotency key, risk decision, and audit lineage.
- Simulator fills are permanently identified as paper/simulated, never broker-confirmed.

## Exit evidence

- end-to-end paper lifecycle: draft → validation → risk decision → simulated fill → position → account → portfolio → audit;
- duplicate/replay/order-race tests;
- failed risk, rejected, partial-fill, timeout, and unknown-state tests;
- environment-isolation proof;
- security review and ITRGA determination.

---

# Band BE-9 — Broker/Exchange Connectivity and Account Visibility

## Objective

Integrate one authorized broker/account provider in a read-first, reconciliation-first posture.

## Scope

- broker adapter contract;
- encrypted credential vault and scoped service identity;
- account, balance, position, order, fill, and instrument-permission read models;
- read-side broker-to-AXIOM reconciliation;
- discrepancy record/state/ownership;
- provider/broker operational health;
- account RBAC and audit.

## Explicit exclusions

- No order submission in this band;
- no frontend broker calls;
- no mixed paper/live accounts;
- no assistant access to broker credentials.

## Exit evidence

- sandbox or non-production broker contract evidence;
- read-side reconciliation evidence;
- stale, unavailable, mismatch, and partial-data handling;
- entitlement/least-privilege test evidence;
- security review.

---

# Band BE-10 — Signal-Against-Account Intelligence

## Objective

Project persisted signal vocabulary onto latest-complete broker-synced account state in state nouns only, per `ITRGA_REQ_V2_BE-10_001.md`; zero broker order types; zero action language; fail-closed staleness.

## Status

**OPERATING (fielded 2026-09-08_0050, suite 1,121/0; closeout ITRGA-CAMPAIGN-BE10-CLOSE-001).**

---

# Band BE-11 — Paper-Execution Bridge to Live Practice-Book Truth

## Objective

Paper orders sized by live practice-book basis (BE-9 projection), gateway decisions and ledger math in `PAPER` mode only; drift reconciliation vs broker truth; scope per `ITRGA_REQ_V2_BE-11_001.md` upon its adoption.

## Hard exclusions

Zero broker-write verbs; zero terminal contact; price basis only via operator-cited inputs or (deferred) lawful fill-sim basis.

---

# Band BE-12 — Controlled Live Execution Gateway

## Objective

Enable a narrowly authorized, human-confirmed execution path only after all prior execution-security, provider, paper, risk, reconciliation, and production-readiness gates have been independently passed.

## Scope

- immutable order intent;
- account/instrument/market-session eligibility;
- pre-trade risk evaluation;
- explicit human confirmation and step-up authorization as specified;
- execution gateway/provider adapter submission;
- idempotency, duplicate prevention, acknowledgement and fill processing;
- cancellation/modify handling as explicitly supported;
- unknown-state handling and reconciliation;
- kill switch and emergency controls;
- execution audit and incident workflows.

## Hard prohibitions

- No autonomous execution unless a separate constitutional decision authorizes it.
- No execution based solely on assistant text, model output, chart pattern, signal, or UI state.
- No successful execution display without authoritative confirmation.

## Exit evidence

- controlled end-to-end success and failure-path evidence;
- independent security, risk, operational, reconciliation, and incident-response evidence;
- production readiness certification under the governing production instrument;
- explicit Operator authorization for the defined provider, accounts, instruments, and mode.

---

# Band BE-13 — Governed External AI Provider Adapters

## Objective

Optionally support external AI only after a dedicated AI safety/data-governance standard is approved.

## Scope

- provider-neutral AI adapter;
- approved-provider configuration and secret isolation;
- data classification/minimization and redaction;
- model/version identity, prompts/responses/audit records;
- local fallback/refusal behavior;
- prompt-injection defenses and output constraints;
- assistant access policies for research, account, risk, and execution explanation.

## Explicit exclusions

- No assistant authority to place, alter, approve, cancel, or route orders;
- no broker credential exposure;
- no generic tool execution;
- no hidden provider introduction;
- no use of external AI before provider-specific approval.

## Exit evidence

- data-flow, retention, and provider authorization evidence;
- prompt-injection, authorization, and refusal tests;
- proof that natural language cannot bypass risk or execution controls;
- operator disclosure and audit evidence.

---

## 4. Cross-band quality gates

Every backend unit must provide, as applicable:

- requirements-to-acceptance traceability;
- architecture conformance;
- threat/risk assessment;
- unit, integration, regression, contract, and failure-path tests;
- schema/migration and rollback evidence;
- API versioning/error-state evidence;
- audit/lineage evidence;
- security and secret-handling evidence;
- documentation, project-state, risk, and technical-debt updates;
- Delivery Report and ITRGA review package.

## 5. Backend roadmap completion condition

V2 backend is not complete when APIs exist. It is complete only when each authorized capability has reached its approved maturity state with evidence, and any production-facing execution capability has separately passed production certification.
