# Wave 6 Engineering Design and Implementation Plan

## Execution Research — Simulation Only, Gate Closed

| Field | Value |
|---|---|
| Wave | **6 — Execution Research** |
| Prepared by | AXIOM Development Authority |
| Prepared for | ITRGA review under `docs/build-orders/ITRGA_REQUEST_WAVE6_DESIGN_PLAN.md` |
| Date | 2026-07-17 |
| Platform of record | **v0.46.0** |
| Alembic head | **20260717_0027** |
| Status | **Submitted design plan — no Wave-6 construction authorized** |
| Milestone predecessor | Human-AI Collaborative Workspace Complete — declared by ITRGA |
| Constitutional posture | Governance Gate **CLOSED**; execution remains roadmap/governance-gated |

---

## 0. DA Non-Authorization Statement

This document is a **design plan only**. It does not authorize implementation of any Wave-6 unit.

The Development Authority will not build any Wave-6 unit until:

1. ITRGA reviews and accepts this design plan;
2. ITRGA issues a specific Wave-6 Build Order; and
3. the operator authorizes that Build Order.

Wave 6 is the highest-risk wave. This plan treats **Execution Research** as **simulation/research only**. It does not open the Constitutional Governance Gate and does not authorize live broker connectivity, real order placement, real account linkage, real positions, real balances, real margin/capital state, or real-money workflows.

The Gate remains **CLOSED** for the entirety of this design. Any future Gate-state change would require explicit Operator authorization, ITRGA governance decision, and governance amendment. It is not a feature-unit code change.

---

## 1. Scope and Non-Scope

### 1.1 In-scope Wave-6 interpretation

Wave 6 may build an **Execution Research Environment** that supports:

- gate-closed execution-safety foundation;
- deterministic simulated execution runs over historical/replayed data;
- simulated fill records labelled `SIMULATED`;
- simulated paper research ledger artifacts labelled `SIMULATED`;
- advisory/hypothetical execution-risk research reports;
- pre-registered simulated execution experiments;
- execution replay and simulated execution analytics with uncertainty;
- operator UI surfaces that are research-framed, browser-proven, and non-actuating.

### 1.2 Explicitly out of scope for Wave 6

The following are not authorized by this design and must not appear in any Wave-6 Build Order unless a future constitutional amendment explicitly changes the scope:

- live broker adapter;
- broker SDK dependency;
- broker credentials;
- live venue endpoint;
- real order placement;
- order routing;
- real account id, broker account id, position id, balance, margin, capital, or portfolio account state;
- real P&L or realized trading performance claim;
- go-live switch;
- Gate opening;
- external LLM/API;
- unspiked compiled/LLM/tokenizer dependency;
- Wave-7 institutional platform work.

### 1.3 Smallest safe set

The plan proposes the smallest coherent Wave-6 set that can satisfy the roadmap while preserving the constitutional red line:

1. first prove the Gate-closed / simulation-only safety envelope;
2. introduce simulated execution artifacts with unambiguous `SIMULATED` labels;
3. build research ledgers/analytics only over those simulated artifacts;
4. add browser-proven research surfaces only after the persistence and refusal seams are proven;
5. close out the wave with full no-actuation proof.

---

## 2. Constitutional Fence Map

| Roadmap component | Wave-6 permitted interpretation | Construction fence | Hard prohibition proof |
|---|---|---|---|
| Execution simulator | Deterministic simulation over historical/replayed candles and advisory artifacts. Produces `SIMULATED` run/fill records. | Simulation engine has no broker client, no network egress, no credentials, and no External Integration dependency except refusal-proof tests. | Grep no broker SDK/endpoint; tests prove no live broker calls; simulated records labelled. |
| Risk engine | Advisory research report over hypothetical/simulated requests and simulated fills. | No account/capital/margin/balance fields; output is `research_only` with uncertainty and disclaimer. | Schema forbidden-column query; no account linkage tests. |
| Broker abstraction | External Integration owns the broker seam; only Null/Simulated refusal seam exists while Gate CLOSED. | Broker-specific code remains in `external_integration`; connect/execute refuse under closed Gate. | Extended `test_broker_integration.py`; containment grep. |
| Paper trading | Simulation ledger over `SIMULATED` fills only. | Ledger rows reference simulation runs/fills, not accounts or brokers; no real P&L claim. | Schema has no real account/broker columns; UI says simulated research only. |
| Execution analytics | Post-hoc analytics over simulated fills/ledger records. | Uncertainty mandatory; statistical result separated from economic interpretation. | Tests require uncertainty and no guaranteed/real-P&L language. |
| Position management research | Simulated position-state snapshots only, if needed, never real positions. | Use `simulated_position_state` terminology and `SIMULATED` marker; no `position_id`/account linkage. | Forbidden-column query and no real-position grep. |
| Trade replay | Replay historical/replayed data and existing governed artifacts. | Replay inputs are frozen/as-of bounded; no live feed dependency required. | No-look-ahead tests and future-row exclusion evidence. |
| Performance comparison | Compare simulated strategies/runs with uncertainty and limitations. | No real-money claims; no cherry-picking; pre-registered experiment scope. | Pre-registration hash and full-scope inclusion tests. |
| Execution experimentation | Pre-registered simulated execution experiments. | Experiment plan immutable; simulation-only input/output. | Audit, plan hash, no orphan, no live execution path. |

---

## 3. Binding Wave-6 Guardrail Design Responses

| Guardrail | Design response |
|---|---|
| GR6-1 Gate stays CLOSED | W6-U01 proves closed Gate as the safety foundation. No unit may modify Gate state. Gate status evidence appears in every unit pack. |
| GR6-2 Simulation/research only | Simulation engine has no live broker dependency, no credentials, no external venue endpoint, and no real account/position/balance state. Simulated artifacts are labelled `SIMULATED`. |
| GR6-3 Broker logic containment | Broker-specific code remains only under External Integration. Execution Research reads simulation artifacts and uses no broker SDK/client. |
| GR6-4 Null/Simulated broker refuses | W6-U01 extends refusal tests for connect/execute and all new seams. Refusal event/metric is required where applicable. |
| GR6-5 No execution/actuation UI controls | UI labels all surfaces as `SIMULATED` and research-only. No buy/sell/submit/go-live/connect-broker affordance. Browser screenshots mandatory. |
| GR6-6 Simulated artifacts labelled and inert | Every simulated run/fill/ledger/report stores `simulation_mode='SIMULATED'`, `research_status='research_only'`, and disclaimer. |
| GR6-7 Uncertainty mandatory; stat ≠ economic | Any analytics/performance comparison report stores uncertainty, sample count, limitations, and separate economic-usefulness statement. |
| GR6-8 Option A / D-W2-001 | No symbol-identity learned feature; market metadata remains evaluation/governance context. Any specialization requires governance amendment. |
| GR6-9 Persistence-capture | Every new table requires Alembic, committing script, raw SELECT ≥1 row, and no-orphan audit JOIN in first submission. |
| GR6-10 UI judged in browser | Every UI unit requires served-browser screenshots, no unreachable pages, no action controls, logged-out block. |
| GR6-11 Git-Bash CI | Every unit evidence pack includes the documented Git-Bash local CI command and `LOCAL_CI_EXIT_CODE: 0`. |
| GR6-12 No unspiked dependency | No broker SDK, no live venue client, no new compiled dependency by default. Any other compiled dep requires spike; broker SDK barred. |
| GR6-13 External LLM future-gated | No external LLM/API in Wave 6 feature units. If proposed later, it requires separate hard-gated Build Order. |

---

## 4. Proposed Bounded Contexts

### 4.1 Execution Research bounded context

Proposed backend package, when authorized:

```text
backend/app/execution_research/
```

Responsibilities:

- simulation contracts;
- deterministic simulated fill model;
- simulated execution run/fill services;
- simulated paper ledger research artifacts;
- execution-risk research reports;
- replay experiment contracts;
- simulated execution analytics.

This context does **not** own broker connectivity, credentials, live order routing, real accounts, real positions, or the Governance Gate.

### 4.2 External Integration containment

Any broker seam hardening belongs only under:

```text
backend/app/external_integration/
```

Wave-6 permitted External Integration work is refusal/containment only:

- NullBroker / SimulatedBroker refusal behavior;
- Gate-closed refusal tests;
- no credentials;
- no live SDK;
- no endpoint.

### 4.3 Existing context reads

| Existing context | Execution Research may read | Execution Research must not do |
|---|---|---|
| Persistence/Market | historical/replayed candles | no live external feed connection |
| Trading Intelligence | advisory signals and guardrail state | no signal emission or mutation |
| Institutional Intelligence | scenario/risk/signal-validation reports | no authoritative recomputation in UI unless server-side simulated report authorized |
| Collaboration | plan/journal ids as research links | no order ticket conversion |
| External Integration | refusal seam only | no live broker connection |

---

## 5. Data Model Plan

No data model is authorized until a Build Order. Candidate tables are pre-designed here for review.

### 5.1 W6-U01 safety foundation

Expected migration: none, unless ITRGA explicitly requests a refusal-event table. Prefer existing `audit_events` for refusal proof.

### 5.2 Simulated execution runs

Candidate table:

```text
simulated_execution_runs
```

Candidate fields:

```text
run_id
created_at UTC
operator_id
simulation_mode = SIMULATED
simulation_policy_version
input_artifact_ids
replay_scope
fill_model_name
fill_model_version
assumptions
limitations
research_status = research_only
simulation_disclaimer
audit_correlation_id
```

Forbidden fields:

```text
broker_account_id
account_id
real_account_balance
margin
capital
live_position_id
broker_endpoint
broker_credentials
order_payload
order_intent
execution_status_as_live
```

### 5.3 Simulated fill events

Candidate table:

```text
simulated_fill_events
```

Candidate fields:

```text
simulated_fill_id
run_id
created_at UTC
simulation_mode = SIMULATED
market_class
symbol
timeframe
as_of_time
simulated_research_direction
simulated_units
requested_reference_price
simulated_fill_price
simulated_slippage_bps
source_candle_ids
fill_model_name
research_status
simulation_disclaimer
audit_correlation_id
```

Design notes:

- `simulated_units` is a dimensionless research input, not an order quantity.
- `simulated_fill_price` is a simulated model output, not a broker fill.
- UI and API must label these fields `SIMULATED`.

### 5.4 Simulated paper ledger

Candidate table:

```text
simulated_paper_ledger_entries
```

Candidate fields:

```text
ledger_entry_id
created_at UTC
simulation_mode = SIMULATED
run_id
simulated_fill_id
operator_id
ledger_event_type
simulated_research_direction
simulated_units
simulated_entry_value
simulated_exit_value
simulated_return_estimate
uncertainty
limitations
research_status
audit_correlation_id
```

Forbidden:

- account balance;
- margin;
- real capital;
- broker account id;
- live position id;
- real P&L claim.

### 5.5 Execution risk research reports

Candidate table:

```text
execution_risk_research_reports
```

Candidate fields:

```text
report_id
created_at UTC
simulation_mode = SIMULATED
input_artifact_ids
simulated_request_summary
risk_metrics
uncertainty
limitations
economic_usefulness
research_status
audit_correlation_id
```

### 5.6 Execution experiment and analytics reports

Candidate tables:

```text
execution_research_experiments
simulated_execution_analytics_reports
```

Experiment records require pre-registration and immutable plan hash. Analytics reports require uncertainty, sample count, full-scope inclusion, and no real-P&L framing.

---

## 6. Refusal and Containment Test Plan

Mandatory tests across Wave 6:

```text
test_governance_gate_remains_closed_for_wave6
test_null_or_simulated_broker_refuses_connect_when_gate_closed
test_null_or_simulated_broker_refuses_execute_when_gate_closed
test_broker_logic_contained_in_external_integration
test_execution_research_has_no_live_broker_sdk_or_credentials
test_simulated_artifacts_are_labelled_simulated
test_simulation_creates_no_real_account_or_position_state
test_execution_research_ui_has_no_actuation_controls
test_wave6_bright_line_grep_no_live_execution_path
test_persistence_no_orphan_for_each_new_simulated_table
```

For each unit, evidence must include:

- direct test names and PASS lines;
- grep command and output;
- raw SQL SELECT for new tables;
- no-orphan audit JOIN;
- broker/Gate refusal proof;
- browser screenshots for UI units.

---

## 7. UI Plan

Wave-6 UI surfaces are research/simulation workspaces only.

### UI label requirements

Every Wave-6 execution-research UI must visibly include:

```text
SIMULATED execution research only. Not a live order, not financial advice, not real P&L. AXIOM does not act. Governance Gate CLOSED.
```

### UI controls allowed

Allowed:

- select replay scope;
- view simulated runs;
- view simulated fills;
- view simulated ledger entries;
- view uncertainty/limitations;
- create pre-registered simulated experiment plan if authorized;
- run deterministic simulated replay if a Build Order authorizes simulation writes.

Forbidden:

- buy/sell;
- submit order;
- execute;
- connect broker;
- go live;
- account selector;
- position management for real positions;
- broker credentials;
- real balance/margin/capital.

### Browser evidence

Each UI unit must provide screenshots showing:

- reachable served session;
- `SIMULATED` label;
- research/not-live disclaimer;
- no forbidden controls;
- logged-out block.

---

## 8. Analytics Method Plan

Execution analytics/performance comparison may only analyze simulated artifacts.

Required method properties:

- pre-registered scope;
- no cherry-picking;
- full included run/fill set listed;
- sample count;
- uncertainty interval or explicit insufficient-sample limitation;
- statistical finding separated from economic usefulness;
- simulated/not-real-P&L disclaimer;
- source artifact ids;
- deterministic report hash;
- audit event.

Potential metrics:

- simulated slippage distribution;
- simulated fill delay distribution;
- simulated missed-fill rate;
- simulated adverse excursion proxy;
- simulated return estimate with uncertainty;
- comparison across fill models or replay scopes.

Hard prohibition:

- no real P&L claim;
- no guaranteed return;
- no live execution recommendation;
- no conversion to order.

---

## 9. Dependency Declaration

Wave 6 starts with existing stack only:

```text
Python / FastAPI / SQLAlchemy / Alembic / Pydantic
React / TypeScript / Vite / Vitest
```

Explicit non-dependencies:

- no broker SDK;
- no exchange SDK;
- no external LLM/API;
- no tokenizer/model package;
- no live market provider SDK;
- no new compiled dependency by default.

If a non-broker compiled dependency is proposed later, it requires a separate compatibility spike and ITRGA review before adoption. A broker SDK is barred in Wave 6 regardless.

---

## 10. Risk Register and Falsification Plan

| Risk | Severity | Falsification / proof method |
|---|---|---|
| Gate accidentally opens | Critical | Gate-state test; broker connect/execute refusal; no Gate mutation code; governance amendments check. |
| Live broker path enters code | Critical | dependency grep; no SDK; no credentials; External Integration containment grep; refusal tests. |
| Simulation presented as live execution | Critical | `SIMULATED` schema marker; UI screenshot; disclaimer tests; no live account fields. |
| Simulated ledger becomes real account ledger | Critical | forbidden account/balance/margin columns 0 rows; no broker/account imports; UI no account controls. |
| Risk engine actuates sizing | Critical | no actuating output; no account/capital field; service writes report only; triggers-nothing test. |
| Analytics claims real P&L or guarantee | High | no-real-P&L text tests; uncertainty mandatory; limitations visible; browser screenshot. |
| Broker logic leaks outside External Integration | High | structural grep; import-boundary test. |
| New simulated artifact unaudited | High | raw SELECT + no-orphan audit JOIN for every table. |
| Browser evidence incomplete | Medium | served screenshots required; logged-out block mandatory. |
| External LLM/API sneaks in | High | dependency grep; no new env secrets; no provider import. |

---

## 11. Proposed Unit Decomposition

### W6-U01 — Execution Research Safety Foundation: Gate-Closed Simulation Envelope

Purpose: prove the lock before the door.

Scope:

- execution research bounded context skeleton;
- simulation-only contracts;
- Gate-closed proof extension;
- Null/Simulated broker refusal seam in External Integration only;
- no broker SDK/credentials;
- no schema unless ITRGA explicitly requests one;
- containment grep;
- browser not required unless UI is added.

Acceptance focus:

- GR6-1 through GR6-4;
- no live broker path by construction;
- broker refusal tests;
- full regression and Git-Bash CI.

### W6-U02 — Simulated Execution Runs and Fill Events

Purpose: persist deterministic simulated execution artifacts labelled `SIMULATED`.

Scope:

- `simulated_execution_runs`;
- `simulated_fill_events`;
- deterministic fill model over historical/replayed data;
- raw SELECT + no-orphan audit;
- no UI unless minimal evidence UI is authorized.

Acceptance focus:

- GR6-2, GR6-6, GR6-9;
- no real account/broker columns;
- no network/broker calls.

### W6-U03 — Simulated Paper Research Ledger

Purpose: build a simulation ledger over simulated fills only.

Scope:

- `simulated_paper_ledger_entries`;
- optional simulated position-state snapshots if justified;
- simulation-only labels and disclaimers;
- no account/capital/margin/real P&L.

Acceptance focus:

- ledger references simulated runs/fills only;
- no real account/position path;
- no-orphan audit.

### W6-U04 — Execution Risk Research Reports

Purpose: evaluate simulated/hypothetical execution risk as research analytics.

Scope:

- execution risk research report artifact;
- uncertainty and limitations;
- no account/capital/margin state;
- no actuating sizing output.

Acceptance focus:

- GR6-7 uncertainty;
- triggers nothing;
- no account linkage.

### W6-U05 — Trade Replay and Execution Experiment Pre-Registration

Purpose: replay historical data and pre-register simulated execution experiments.

Scope:

- immutable simulated execution experiment plans;
- plan hash and scope declaration;
- replay input lineage;
- no live feed requirement;
- no cherry-picking.

Acceptance focus:

- pre-registration;
- no look-ahead;
- no broker/venue calls.

### W6-U06 — Simulated Execution Analytics and Performance Comparison

Purpose: compare simulated execution runs with uncertainty.

Scope:

- analytics reports over simulated fills/ledger entries;
- confidence intervals/sample count;
- stat/economic separation;
- no real P&L/guarantee.

Acceptance focus:

- GR6-7;
- no real-money framing;
- no-orphan audit.

### W6-U07 — Execution Research Workspace UI

Purpose: browser-proven UI for simulated execution research artifacts.

Scope:

- read/display simulated runs/fills/ledger/analytics;
- optional authorized simulated replay creation if prior artifacts are approved;
- visible `SIMULATED` labels;
- no buy/sell/submit/go-live/connect-broker/account controls.

Acceptance focus:

- GR6-5 and GR6-10 browser proof;
- auth/read-only/write-safe table;
- no action controls.

### W6-U08 — Wave-6 Closeout & Hardening

Purpose: prove the Execution Research Environment is simulation-only and non-actuating across the wave.

Scope:

- full-wave no-live-execution grep;
- Gate CLOSED proof;
- artifact no-orphan completeness;
- browser E2E;
- docs/register reconciliation;
- milestone candidate: Execution Research Environment Complete.

---

## 12. Recommended W6-U01 Scope

Recommended first Build Order:

> **W6-U01 — Execution Research Safety Foundation: Gate-Closed Simulation Envelope**

Acceptance criteria should include:

- no schema unless explicitly authorized;
- no UI unless minimal evidence UI is required;
- no external dependency;
- no broker SDK or credentials;
- External Integration refusal seam only;
- Gate CLOSED proof;
- connect/execute refusal tests;
- containment grep proving broker-specific logic lives only in External Integration;
- no execution/order/account/broker path in any new execution research context;
- full suite green;
- Git-Bash CI exit 0.

---

## 13. Bright-Line Self-Check

| Capability | Gate closed | Simulation-only | Broker contained | No real account | SIMULATED label | Uncertainty | Browser-proof if UI |
|---|---:|---:|---:|---:|---:|---:|---:|
| Safety foundation | Yes | Yes | Yes | Yes | N/A | N/A | N/A |
| Simulated runs/fills | Yes | Yes | Yes | Yes | Yes | Method dependent | If UI |
| Paper research ledger | Yes | Yes | Yes | Yes | Yes | Where metrics shown | If UI |
| Risk reports | Yes | Yes | Yes | Yes | Yes | Yes | If UI |
| Replay/experiments | Yes | Yes | Yes | Yes | Yes | Plan dependent | If UI |
| Analytics/comparison | Yes | Yes | Yes | Yes | Yes | Yes | If UI |
| Workspace UI | Yes | Yes | Yes | Yes | Yes | Visible | Yes |
| Closeout | Yes | Yes | Yes | Yes | Yes | Yes | Yes |

---

## 14. ITRGA Review Request

The Development Authority submits this Wave-6 Engineering Design and Implementation Plan for ITRGA review.

No Wave-6 implementation is authorized by this plan. DA awaits ITRGA review, binding refinements, a future W6-U01 Build Order, and operator authorization before beginning Wave-6 construction.

The Constitutional Governance Gate remains **CLOSED**.

---

**End of Wave 6 Engineering Design and Implementation Plan**
