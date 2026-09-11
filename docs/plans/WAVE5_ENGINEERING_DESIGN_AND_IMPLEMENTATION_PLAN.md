# Wave 5 Engineering Design and Implementation Plan

| Field | Value |
|---|---|
| Wave | **5 — Human-AI Collaboration** |
| Objective | Create an interactive AI-assisted research and decision-support workspace without execution or autonomy |
| Prepared by | AXIOM Development Authority |
| Prepared for | ITRGA review under `docs/build-orders/ITRGA_REQUEST_WAVE5_DESIGN_PLAN.md` |
| Date | 2026-07-16 |
| Status | **Submitted design plan — no construction authorized** |
| Preconditions | Wave 3 Professional Advisor Platform Complete; Wave 4 Institutional Intelligence Layer Complete; Governance Gate CLOSED |

---

## 0. DA Non-Authorization Statement

This document is a **design plan only**. It does not authorize implementation of Wave 5.

The Development Authority will not build any Wave-5 unit until:

1. ITRGA reviews and accepts this design plan;
2. ITRGA issues a specific Wave-5 Build Order; and
3. the operator authorizes the unit.

The Constitutional Governance Gate remains **CLOSED**. No Wave-5 design element opens execution, broker interaction, account/position integration, order generation, position sizing, paper trading, or autonomous remediation.

---

## 1. Wave-5 Purpose

Wave 5, **Human-AI Collaboration**, introduces interactive research collaboration surfaces:

- AI-assisted research explanation;
- chart assistant and chart annotations;
- drawing tools and operator research markups;
- scenario comparison;
- signal investigation;
- decision explanations;
- inert trade planning workspace;
- inert manual trade journal;
- interactive research assistant.

Wave 5 outputs are **operator decision-support artifacts only**. They may explain, summarize, compare, annotate, and help a human reason. They must never instruct, execute, size, place orders, open the Governance Gate, mutate models/config, or automate a decision.

---

## 2. Binding Guardrail Compliance — GR-1 through GR-11

| Guardrail | Design response |
|---|---|
| GR-1 Gate remains CLOSED | No Wave-5 component can open, weaken, or approach the Constitutional Governance Gate. Broker/execution contexts remain hard-closed and out of scope. |
| GR-2 Advisory/research/decision-support only | Assistant replies, plans, notes, annotations, and journal entries carry research-only framing and never use instruction/order language. |
| GR-3 No execution/order/sizing/broker/account/position linkage | Data models explicitly exclude order payloads, quantity, stop/target, broker account, real account id, live position id, and execution routing fields. |
| GR-4 Explainable/auditable/reproducible/traceable | Every persisted assistant response, annotation, plan, or journal entry stores provenance, source artifact ids, prompt/version metadata, actor, timestamp, and audit event. |
| GR-5 Evidence mandatory | Every implementation unit requires operator-run target evidence; UI units require browser screenshots; report claims do not approve work. |
| GR-6 Standing controls | Any new compiled or LLM/tokenizer dependency requires a wheel/API compatibility spike; every new persisted artifact requires first-submission raw SELECT + audit no-orphan proof. |
| GR-7 Statistical/economic honesty | Assistant and UI may summarize existing uncertainty but may not remove it, invent performance, cherry-pick, or present guaranteed/expected returns. |
| GR-8 Presentation-only UX | Client-side surfaces display persisted governed artifacts and drafts; they do not authoritatively recompute analytics or inference. |
| GR-9 Trade planning/journal research only | Trade plans and journals are inert operator research notes; they contain no order/sizing/execution fields and trigger nothing. |
| GR-10 Assistant bounded/grounded/non-actuating | Assistant has no mutating tools except writing its own audited research-note/annotation drafts when explicitly authorized; no prompt can cause an action, Gate change, order, or unaudited write. |
| GR-11 No secrets/PII/model-internals leakage | Assistant context excludes secrets/tokens/raw internals; sampled outputs are checked for secret markers; logs are redacted. |

---

## 3. Bounded Contexts and Ownership

### 3.1 New bounded context: Collaboration Intelligence

Proposed backend package:

```text
backend/app/collaboration/
```

Responsibilities:

- assistant session contract;
- assistant response records;
- assistant grounding/provenance records;
- chart annotation records;
- drawing/markup records;
- inert trade plan records;
- inert trade journal records;
- decision explanation records;
- collaboration audit policies.

This context owns collaboration artifacts only. It does **not** own market feeds, broker/execution abstractions, order placement, account data, model training, auth, or the Governance Gate.

### 3.2 Existing context interactions

| Existing context | Collaboration reads | Collaboration does not do |
|---|---|---|
| Market/Persistence | candles, chart context, metadata | no live feed ownership; no broker/provider connection |
| ML Research | validation, calibration, economic, generalization reports | no model training/retraining |
| Trading Intelligence | advisory signals, guardrails, alerts, analytics | no signal emission; no signal modification |
| Institutional Intelligence | correlation/regime/scenario/risk/signal-validation reports | no recomputation in UI; no mutation |
| Auth | current operator identity | no auth ownership |
| External Integration | no runtime dependency | no broker/account/order/position interaction |

---

## 4. AI/LLM Assistant Architecture

### 4.1 Provider strategy

Wave 5 should begin with a provider-neutral assistant boundary:

```text
AssistantPort
AssistantRequest
AssistantResponse
GroundingBundle
AssistantSafetyPolicy
```

Recommended W5-U01 provider implementation:

```text
RuleBasedGroundedAssistant / NullAssistant
```

Purpose:

- prove grounding, provenance, prompt-injection refusal, audit, and non-actuation before any external LLM or heavy local model is introduced;
- avoid external API secrets and unspiked dependencies in the first safety slice.

A future external LLM provider may be proposed only after:

- explicit Build Order authorization;
- secret-handling design under §77;
- provider terms/privacy review;
- prompt-injection tests;
- output redaction tests;
- no-action tool allowlist proof;
- dependency/API compatibility evidence.

### 4.2 Assistant tool/action allowlist

Initial assistant tools should be read-only or confined to its own collaboration artifact store:

| Tool | Type | Authorized in foundation? | Notes |
|---|---|---:|---|
| Read governed artifact summaries | Read-only | Yes | signals, alerts, intelligence reports, chart context |
| Create assistant draft response | Own artifact write | Yes | audited, research-only |
| Create chart annotation draft | Own artifact write | Later unit | inert annotation only |
| Create trade plan draft | Own artifact write | Later unit | no order/sizing fields |
| Create journal entry | Own artifact write | Later unit | manual research note only |
| Modify model/config/signal | Mutating | No | forbidden |
| Open Gate / broker action / order | Mutating | No | forbidden |
| Fetch external live data | External | No | future gated only |

### 4.3 Grounding strategy

Assistant responses must be grounded in persisted AXIOM artifacts:

- advisory signals;
- signal rationale and lineage;
- alerts;
- analytics/confidence visualization;
- Institutional Intelligence reports;
- chart/candle data;
- operator-selected context.

Every assistant response stores:

```text
assistant_response_id
created_at UTC
operator_id / actor
request_text_hash
assistant_policy_version
provider_name / provider_version
model_or_engine_version
source_artifact_ids
grounding_summary
response_text
limitations
disclaimer
audit_correlation_id
```

### 4.4 Prompt-injection and instruction escalation defenses

Design requirements:

- system safety policy is not overridable by user text;
- user prompt is data, not instruction to system/tool layer;
- no assistant output can call an action tool because no such tool exists;
- prompt-injection strings requesting order placement, Gate opening, secret disclosure, or model mutation must be refused;
- refusal must be audited.

Mandatory negative tests for the assistant safety foundation:

```text
assistant_refuses_order_instruction
assistant_refuses_gate_open_instruction
assistant_refuses_secret_exfiltration
assistant_refuses_unbounded_tool_request
assistant_response_has_grounding_or_refuses
assistant_write_limited_to_own_audited_artifact
```

### 4.5 AI output disclaimer

Every assistant response and assistant-derived annotation must visibly include or reference:

```text
AI-generated research assistance only. Not financial advice, not an instruction, may be wrong. Operator judgment required. AXIOM does not act.
```

---

## 5. Trade Planning Workspace and Journal Data Model

### 5.1 Inert trade plan record

A trade plan is a hypothetical operator-authored research note. It is not an order ticket.

Proposed table:

```text
trade_plan_notes
```

Allowed fields:

```text
plan_id
created_at UTC
updated_at UTC
operator_id
title
market_context
hypothesis
linked_signal_ids
linked_report_ids
scenario_notes
risk_notes
invalidating_conditions_text
decision_status: draft | archived | reviewed
research_disclaimer
audit_correlation_id
```

Forbidden fields:

```text
order_payload
order_intent
side
quantity
lot_size
order_size
position_size
entry_price_order
stop_loss
take_profit
broker_account_id
account_id
position_id
execution_status
```

### 5.2 Manual journal record

A journal entry is an operator-authored reflection and research log. It does not import or reconcile broker trades.

Proposed table:

```text
manual_trade_journal_entries
```

Allowed fields:

```text
journal_id
created_at UTC
operator_id
title
reflection_text
linked_plan_id
linked_signal_ids
linked_report_ids
emotion_tags
process_tags
lesson_notes
research_disclaimer
audit_correlation_id
```

Forbidden:

- broker account identifiers;
- execution ids;
- fill prices as broker records;
- order quantity/position size;
- P&L claims unless future governed outcome/account data exists.

### 5.3 Persistence and audit

Both trade plan and journal records trigger persistence-capture control when implemented:

- Alembic migration;
- committing script;
- raw `psql SELECT >= 1 row` on correct table;
- audit event;
- no-orphan proof.

---

## 6. UX Surfaces

### 6.1 Assistant panel

- protected route or embedded panel;
- shows grounding sources;
- shows assistant disclaimer;
- shows refusal reasons when applicable;
- no execution controls;
- no order/sizing fields;
- no secret display.

### 6.2 Chart assistant and annotations

- presentation-only over chart context;
- annotations store research text, source ids, uncertainty/provenance where relevant;
- no predictive guarantee;
- no client-side authoritative analytics computation.

### 6.3 Trade planning workspace

- labelled hypothetical research plan;
- no order ticket design patterns;
- no buy/sell buttons;
- no quantity/SL/TP/position controls;
- operator may link persisted research artifacts and write notes.

### 6.4 Manual journal

- manual research note entry;
- no broker import;
- no account linkage;
- no execution reconciliation.

### 6.5 Signal investigation view

- reads existing signal/intelligence artifacts;
- explains lineage and guardrails;
- no action controls;
- no signal mutation.

---

## 7. Data and Persistence Design

Wave 5 introduces collaboration artifacts rather than analytics reports.

Candidate tables by unit:

| Artifact | Table | Persistence control applies? |
|---|---|---|
| Assistant safety/session response | `assistant_research_responses` | Yes |
| Grounding bundle references | JSON field or `assistant_grounding_sources` | If table added, yes |
| Chart annotation | `chart_research_annotations` | Yes |
| Drawing/markup | `chart_research_drawings` | Yes |
| Trade plan | `trade_plan_notes` | Yes |
| Manual journal | `manual_trade_journal_entries` | Yes |
| Decision explanation | `decision_explanation_records` | Yes |

Common fields:

```text
id
created_at UTC
operator_id / actor
artifact_type
source_artifact_ids
content
provenance
disclaimer
policy_version
research_status
audit_correlation_id
```

---

## 8. Dependencies

### 8.1 Initial dependency posture

W5-U01 should avoid new external LLM providers and new compiled dependencies. It can use existing Python/TypeScript stack and deterministic local assistant logic to prove safety first.

### 8.2 Future LLM dependency triggers

Any later unit proposing an external LLM/API or local model package must provide:

- dependency/API compatibility spike;
- secret handling plan;
- output redaction plan;
- prompt-injection tests;
- no-action tool boundary proof;
- latency/failure-mode behavior;
- data retention/privacy statement.

### 8.3 Explicit non-dependencies

Wave 5 does not require broker SDKs, trading APIs, external market data providers, account APIs, or order-routing packages.

---

## 9. Risk Register Plan

| Planned risk | Severity | Mitigation / proof |
|---|---|
| Assistant prompt-injected into action | Critical | no action tools; named injection refusal tests; grep; audit |
| Assistant leaks secrets/PII | Critical | redaction/context allowlist; sampled output tests; no secrets in prompts |
| Assistant hallucinates ungrounded signals | High | grounding-required policy; refusal if no sources; provenance shown |
| Trade plan interpreted as order ticket | Critical | inert schema; no order/sizing fields; UI no-action controls; screenshot |
| Journal becomes broker record | High | no broker/account fields; manual research-only disclaimer |
| Client recomputes analytics | High | presentation-only UI; grep/test |
| AI output lacks disclaimer | High | component tests and browser evidence |
| Persisted collaboration artifact unaudited | High | raw SELECT + audit no-orphan proof |

---

## 10. Proposed Implementation Sequence

### W5-U01 — Collaboration Safety Foundation: Assistant Boundary + Inert Planning/Journal Contracts

Purpose: prove the safety envelope before rich interaction.

Scope:

- `collaboration` bounded context skeleton;
- `AssistantPort` and deterministic `RuleBasedGroundedAssistant` / `NullAssistant`;
- assistant safety policy;
- grounding bundle contract;
- inert trade plan and journal schemas/contracts, or schema design if persistence deferred;
- no action tools;
- prompt-injection refusal tests;
- no secret leakage tests;
- no execution/no broker/no Gate grep;
- no external LLM provider yet.

### W5-U02 — Audited Assistant Research Responses

- persisted assistant response records;
- grounding source ids;
- audit events;
- read-only API;
- refusal events;
- browser evidence if UI panel added.

### W5-U03 — Chart Research Annotations and Drawing Tools

- inert annotations/drawings;
- source artifact linkage;
- no client-side analytics recompute;
- browser evidence;
- persistence/audit.

### W5-U04 — Signal Investigation Workspace

- operator surface for exploring signal rationale, guardrails, and linked intelligence reports;
- assistant may summarize only grounded artifacts;
- no signal mutation.

### W5-U05 — Scenario Comparison Workspace

- compares existing persisted scenario reports;
- no scenario generation beyond existing APIs unless separately authorized;
- no guaranteed outcomes;
- uncertainty/provenance visible.

### W5-U06 — Inert Trade Planning Workspace

- persisted research-only trade plan notes;
- no order/sizing/account fields;
- browser proof no order ticket patterns.

### W5-U07 — Manual Research Journal

- manual journal records;
- linked artifacts/plans;
- no broker import/account linkage;
- audit trail.

### W5-U08 — Wave-5 Closeout and Hardening

- full-wave no-execution/no-action proof;
- assistant prompt-injection proof index;
- collaboration artifact audit completeness;
- auth/read-only proof;
- browser E2E;
- milestone candidate: Human-AI Collaborative Workspace Complete.

---

## 11. Recommended W5-U01 Scope

Recommended first Build Order:

> **W5-U01 — Collaboration Safety Foundation: Assistant Boundary + Inert Planning/Journal Contracts**

Acceptance criteria should include:

- no external LLM provider yet;
- assistant boundary with no action tools;
- grounding-required policy;
- prompt-injection refusal tests;
- secret/PII leakage refusal tests;
- inert trade plan/journal contracts rejecting order/sizing/account fields;
- no execution/gate grep;
- no UI or minimal safety UI only if required for evidence;
- no schema unless explicitly authorized; if schema added, persistence-capture proof;
- full suite green and CI exit 0.

---

## 12. Bright-Line Self-Check

| Capability | GR-1 Gate closed | GR-3 No execution | GR-9 Plan/journal inert | GR-10 Assistant non-actuating | GR-11 No leakage | GR-8 Presentation-only |
|---|---|---|---|---|---|---|
| Assistant boundary | Yes | Yes | N/A | Yes | Yes | N/A |
| Assistant responses | Yes | Yes | N/A | Yes | Yes | Yes |
| Chart annotations | Yes | Yes | N/A | Yes where AI-assisted | Yes | Yes |
| Trade planning | Yes | Yes | Yes | Yes where AI-assisted | Yes | Yes |
| Journal | Yes | Yes | Yes | Yes where AI-assisted | Yes | Yes |
| Signal investigation | Yes | Yes | N/A | Yes | Yes | Yes |
| Scenario comparison | Yes | Yes | N/A | Yes | Yes | Yes |

---

## 13. ITRGA Review Request

The Development Authority submits this Wave-5 Design Plan for ITRGA review.

No Wave-5 implementation is authorized by this plan. DA awaits ITRGA review, refinements, and a future Build Order before beginning W5-U01.

---

**End of Wave 5 Engineering Design and Implementation Plan**
