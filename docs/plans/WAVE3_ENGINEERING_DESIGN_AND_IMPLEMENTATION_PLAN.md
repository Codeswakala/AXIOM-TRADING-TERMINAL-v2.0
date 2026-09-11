# AXIOM Wave 3 Engineering Design & Implementation Plan

| Item | Value |
|------|-------|
| Document | Wave 3 Engineering Design & Implementation Plan |
| Request | `docs/build-orders/ITRGA_REQUEST_WAVE3_DESIGN_PLAN.md` |
| Date | 2026-07-15 |
| Author | Development Authority |
| Status | **Plan submitted for ITRGA review — no construction authorized** |
| Wave | 3 — Live Research Advisor |
| Predecessor milestone | Wave 2 Research Framework Complete confirmed by ITRGA request |
| Governing architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` v2.0 |
| Governing ML spec | `docs/governance/07_ML_SPEC.md` |

---

## 0. Non-construction statement

This document is a **design and implementation plan only**.

The Development Authority will not implement live inference, signals, alerts, dashboards, APIs, persistence schema, WebSocket channels, frontend UI, monitoring loops, or operator-facing advisory behavior until ITRGA accepts this plan and issues `BUILD_ORDER_W3-U01`.

Wave 3 is the first wave where AXIOM will speak to the operator about live or near-real-time market conditions. Therefore, this plan treats advisory signal generation as a higher-risk activity than Wave 2 research artifacts.

---

## 1. Executive Summary

Wave 3 builds the **Live Research Advisor**. Its purpose is to transform the Wave-2 research framework into a governed, deterministic, operator-facing advisory system.

Wave 3 will allow AXIOM to generate research/advisory signals for a human operator, but it will not execute trades.

The bright line:

```text
Model + market data → governed inference → advisory signal → operator decision surface → STOP
```

The Constitutional Governance Gate remains closed. There is no broker connection, no order path, no positions, no paper trading, and no execution.

The recommended first Wave-3 unit is:

> **W3-U01 — Live Inference Engine + Governed Model Eligibility Gate**

W3-U01 should prove the safest possible slice first: deterministic scoring of a fully-governed model, no UI signal surface yet, and no execution path.

---

## 2. Constitutional Frame

### 2.1 Advisory-only commitment

Wave 3 outputs recommendations to humans only.

It may produce:

- advisory signal records;
- calibrated confidence;
- explanation/rationale;
- operating-domain warnings;
- drift/health alerts;
- signal history;
- governance dashboard data;
- performance analytics.

It must not produce:

- broker orders;
- execution requests;
- paper trades;
- positions;
- account mutations;
- broker credentials;
- live automated actions;
- unreviewed live signals;
- unpersisted signal outputs.

### 2.2 Constitutional flow

The only permitted flow remains:

```text
Professional Recommendation
  → Operator Decision
    → CLOSED Constitutional Governance Gate
      → Future Broker Integration (Wave 6 only)
```

Wave 3 ends at the recommendation/operator decision surface.

### 2.3 Ownership by bounded context

| Capability | Owning system | Rule |
|------------|---------------|------|
| Live inference | ML / AI / Trading Intelligence boundary | deterministic scoring only |
| Signal generation | Trading Intelligence System | advisory only |
| Signal persistence/audit | Audit/Governance + Persistence services | append-only signal history |
| Signal presentation | UX/Presentation | display only, no analytics |
| Chart display | Chart State / UX | presentation-only; no signal computation |
| Drift/health alerts | Observability + Trading Intelligence | alert operator, never act |
| Broker/execution | External Integration + Governance Gate | closed, not used |

---

## 3. Architecture and Bounded Context

### 3.1 Wave-3 platform placement

Wave 3 spans the following architectural subsystems:

```text
Market Data / Market Intelligence
  → Live Inference Engine
  → Trading Intelligence System
  → Advisory Signal Store / Audit Trail
  → Operator Dashboard / Signal Workspace
```

The signal path must be interface-based and dependency-inward. It must not reach directly into unrelated subsystem internals.

### 3.2 Live inference bounded context

Owned responsibilities:

- load governed model metadata;
- verify model eligibility;
- construct deterministic inference input from approved market data contract;
- score model deterministically;
- validate operating domain;
- attach calibrated confidence;
- produce inert advisory signal candidate.

Not owned:

- broker communication;
- execution;
- chart rendering;
- operator decisions;
- retraining;
- model mutation;
- data ingestion mutation.

### 3.3 Trading Intelligence signal bounded context

Owned responsibilities:

- transform model score into advisory signal record;
- attach risk/uncertainty/domain/economic context;
- ensure recommendation is explainable;
- persist signal history;
- expose advisory signal to operator surfaces;
- emit alerts for drift/health/domain issues.

Not owned:

- direct broker calls;
- position sizing as executable instruction;
- order generation;
- automated action.

### 3.4 UX/Chart boundary

UX and chart layers remain presentation-only.

They may display:

- signal direction/status;
- calibrated confidence;
- rationale;
- domain warning;
- validation lineage;
- economic verdict;
- drift/health indicators;
- signal history.

They must not compute:

- model inference;
- signal rules;
- economic validation;
- indicators as authoritative analytics;
- execution logic.

---

## 4. End-to-End Signal Flow

```text
Live / near-real-time market data
  │
  ├─ Market data contract / query seam
  │
  ├─ Live chronology/as-of validation
  │
  ▼
Feature input assembly
  │
  ├─ same feature definitions/version used by governed model
  ├─ no symbol identity feature
  ├─ no future data
  ▼
Model eligibility gate
  │
  ├─ approved experiment? yes/no
  ├─ model registry status advisory-approved? yes/no
  ├─ dataset/split/report lineage complete? yes/no
  ├─ statistical report linked? yes/no
  ├─ calibration report linked? yes/no
  ├─ economic report linked? yes/no
  ├─ operating domain valid? yes/no
  └─ if any no → refuse/withhold/warn
  ▼
Deterministic inference
  │
  ├─ same input + model version + feature version → same score
  ▼
Signal validation
  │
  ├─ calibrated confidence
  ├─ domain guardrail
  ├─ economic verdict
  ├─ uncertainty/explainability
  ▼
Advisory signal record persisted
  │
  ├─ audit event
  ├─ signal history
  └─ operator-facing display
  ▼
Operator decision surface
  │
  ▼
STOP — Constitutional Governance Gate CLOSED
```

---

## 5. Live Inference Engine Design

### 5.1 Deterministic inference contract

A live inference result must be deterministic:

```text
same model_artifact_id
same model_version
same feature_set_version
same input record/as_of_time
same inference config
→ same score and signal candidate
```

Required mechanisms:

- canonical feature vector ordering;
- pinned feature definitions;
- model artifact hash/version;
- deterministic model scoring path;
- UTC `as_of_time`;
- no random sampling at signal time;
- no live mutable model state.

### 5.2 Governed model eligibility gate

A model may serve advisory inference only if all are true:

| Requirement | Source |
|-------------|--------|
| experiment approved | W2-U05 |
| model artifact research-approved/advisory-eligible | W2-U06/W3 gate |
| statistical report linked | W2-U07 |
| calibration report linked | W2-U08 |
| economic report linked | W2-U09 |
| generalization/operating domain linked | W2-U10 |
| drift status not blocking | W2-U10/W3 monitoring |
| model input excludes identity | W2-U03/W2-U06 |
| feature version matches artifact | W2-U03 |
| no execution capability | W1-U03 gate |

Negative controls:

- ineligible model refused;
- missing report link refused;
- non-advisory status refused;
- out-of-domain request withheld/warned;
- identity field in inference input refused.

### 5.3 Advisory deployment status

Wave 3 should introduce a research-to-advisory eligibility status, for example:

```text
research_only
advisory_candidate
advisory_approved
advisory_suspended
retired
```

Only `advisory_approved` may emit operator-facing signals. Adding this status requires its own unit, tests, and ITRGA evidence.

### 5.4 Inference input discipline

Live inference input must obey:

- UTC `as_of_time`;
- no future candle/feature data;
- no `seed:synthetic` authoritative input;
- no forward-dated `live:simulated` treated as real chronology;
- no random split logic;
- no label/target construction at inference;
- no symbol/provider identity as learned feature.

---

## 6. Signal Contract

### 6.1 Advisory signal fields

A signal record should include:

```text
signal_id
created_at UTC
as_of_time UTC
market_class
provider
symbol
timeframe
model_artifact_id
model_version
feature_set_version
experiment_id
statistical_report_id
calibration_report_id
economic_report_id
generalization_report_id
inference_input_hash
raw_score
calibrated_confidence
signal_direction / classification
signal_state: emitted | withheld | warning | expired
operating_domain_status
calibration_status
economic_verdict
risk_notes
rationale
explainability_summary
audit_correlation_id
```

### 6.2 Signal state machine

```text
candidate
  → eligible_checked
  → emitted | withheld | warning
  → expired | superseded
```

Signals are inert advisory records. No signal may contain executable order payloads.

### 6.3 Explainability

Every emitted signal must explain:

- what model produced it;
- what input was scored;
- why the signal exists;
- confidence and calibration state;
- domain validity;
- economic verdict;
- limitations and uncertainty.

If the system cannot provide rationale, it should withhold rather than emit opaque advice.

---

## 7. Confidence and Probability Quality at Signal Time

### 7.1 Calibrated confidence

Displayed confidence must come from calibrated probability quality, not raw model score.

If calibration report indicates poor calibration:

- signal is withheld or marked warning;
- operator sees explicit calibration warning;
- confidence is not displayed as false certainty.

### 7.2 Confidence visualization

Operator UI should show:

- calibrated confidence;
- confidence band/uncertainty where available;
- calibration status;
- base-rate/economic context;
- explanatory warning when confidence is unreliable.

---

## 8. Operating-Domain Guardrail

A signal may only be emitted inside the model's validated operating domain:

```text
market class
provider/symbol where applicable
timeframe
regime
source authority
feature version
```

Out-of-domain behavior:

```text
withhold signal
or emit warning-only advisory record
never emit normal signal
```

Required negative test:

```text
out-of-domain live request → signal withheld / UNSUPPORTED_DOMAIN warning
```

---

## 9. Monitoring and Alerts

### 9.1 Market monitoring

Wave 3 may monitor:

- live feed status;
- candle freshness;
- market data lag;
- source authority;
- missing features;
- stale model/report links.

### 9.2 Health monitoring

Use W1-U02 observability:

- backend health;
- database latency;
- live adapter status;
- WebSocket status;
- inference service health;
- signal store health.

### 9.3 Drift monitoring

Wave 3 may surface W2-U10 drift signals as alerts.

Rules:

- drift alert never retrains;
- drift alert never changes model;
- drift alert never triggers order/action;
- operator sees warning and evidence.

### 9.4 Alerts

Alerts are information to human operators.

Examples:

```text
MODEL_OUT_OF_DOMAIN
MODEL_CALIBRATION_WARNING
MODEL_ECONOMICALLY_UNUSABLE
DRIFT_DETECTED
LIVE_DATA_STALE
INFERENCE_HEALTH_DEGRADED
SIGNAL_WITHHELD
```

---

## 10. Governance Dashboard and Operator Workspace

### 10.1 Governance dashboard

The governance dashboard should answer:

> Is this model allowed to advise me right now, and why?

Display:

- model status;
- advisory eligibility;
- experiment approval;
- dataset/split hashes;
- statistical validation summary;
- calibration status;
- economic verdict;
- generalization/operating domain;
- drift status;
- latest signal audit events;
- signal history.

### 10.2 Signal history

Every signal must be persisted and queryable by:

- signal id;
- model id;
- market/symbol/timeframe;
- signal state;
- time range;
- domain status;
- confidence range;
- economic verdict.

### 10.3 Research audit trail

Each emitted/withheld signal must write:

- signal record;
- audit event;
- correlation id;
- model lineage;
- input hash;
- reason for emit/withhold.

### 10.4 Operator workspace

The operator workspace shows advisory signals and rationale, not action buttons.

Forbidden UI elements:

- buy/sell execution button;
- order ticket;
- position manager;
- broker connect controls;
- paper trade execution.

---

## 11. Bright-Line Boundary

Wave 3 stops here:

```text
Advisory recommendation shown to operator
```

It does not cross into:

```text
order intent dispatch
broker connection
paper trading
execution simulation
position management
automated action
```

Negative controls required across Wave 3:

- no execution endpoint grep;
- no broker connect path;
- no order payload in signal record;
- governance gate remains closed;
- signal cannot call External Integration broker services;
- alerts cannot trigger retrain/action;
- UI contains no execution controls.

---

## 12. Target Platform and Dependencies

Target platform remains:

```text
Windows / PowerShell
PostgreSQL 18
Python 3.14.6
Node/npm frontend toolchain
```

### 12.1 Dependency rules

- Reuse existing FastAPI/WebSocket/React stack.
- Reuse W1 live market WebSocket seam; do not reinvent transport.
- Reuse W2 pure-Python model artifacts unless a later unit adopts a compiled model dependency.
- Any compiled serving/ML dependency requires Windows/Python 3.14.6 install/import/smoke spike.

### 12.2 Real-time path

Wave 3 should initially use the existing simulated live feed and ticket-based WebSockets.

No external broker/feed connection is introduced unless a future explicit Build Order authorizes data-provider work.

---

## 13. Proposed Wave-3 Unit Breakdown

### W3-U01 — Live Inference Engine + Governed Model Eligibility Gate

| Item | Detail |
|------|--------|
| Type | Backend infrastructure / safety gate |
| Scope | deterministic scoring path, model eligibility gate, input hash, advisory status check |
| No UI? | Yes, backend only initially |
| Evidence | ineligible model refused; deterministic same input/version same score; no execution grep; no signal surface yet |

### W3-U02 — Advisory Signal Contract + Signal Persistence

| Item | Detail |
|------|--------|
| Scope | signal DTO/table, emitted/withheld states, audit events, signal history API |
| Evidence | signal persisted with lineage; ineligible/out-of-domain signal withheld; committing proof first submission |

### W3-U03 — Operating-Domain + Calibration/Economic Guardrails at Emit Time

| Item | Detail |
|------|--------|
| Scope | domain checks, calibration warnings, economic verdict checks, confidence honesty |
| Evidence | out-of-domain withheld; poorly calibrated warning; economically unusable warning |

### W3-U04 — Live Market Inference Adapter

| Item | Detail |
| Scope | feed live/near-real-time market data into inference input through existing query/live seam |
| Evidence | no look-ahead as-of discipline; deterministic scoring; no broker connection |

### W3-U05 — Operator Advisory Dashboard / Signal Workspace

| Item | Detail |
| Scope | UI display for advisory signals, rationale, confidence, warnings, history |
| Evidence | browser screenshots; no execution controls; protected route; signal rationale visible |

### W3-U06 — Monitoring, Drift, Health Alerts

| Item | Detail |
| Scope | operator alerts for drift/health/stale data/model degradation |
| Evidence | drift alert does not retrain; alert persisted; no auto-action |

### W3-U07 — Performance Analytics + Confidence Visualization

| Item | Detail |
| Scope | advisory performance analytics, uncertainty display, confidence history |
| Evidence | no false precision, uncertainty shown, advisory labels |

### W3-U08 — Wave 3 Closeout & Hardening

| Item | Detail |
| Scope | security, evidence, docs, browser E2E, signal audit completeness, no-execution proof |
| Evidence | full suite, Playwright/browser evidence, persisted signal audit, no execution route grep |

---

## 14. Recommended W3-U01 Scope

The first Wave-3 Build Order should be the smallest safe slice:

> **W3-U01 — Live Inference Engine + Governed Model Eligibility Gate**

In scope:

- backend-only inference service;
- governed model eligibility gate;
- deterministic scoring of existing research-only baseline model;
- input hash and inference result DTO;
- refusal for ineligible model;
- no signal persistence/UI yet unless ITRGA chooses otherwise;
- no execution path.

Out of scope:

- dashboard;
- live WebSocket signal stream;
- operator-facing signal history;
- alerts;
- broker/provider connection;
- execution.

This sequencing proves the most important safety controls before any operator-facing signal appears.

---

## 15. Risks and Planned Register Entries

| Risk | Severity | Mitigation |
|------|----------|------------|
| Premature execution path | Critical | gate closed; no execution code; structural grep every unit |
| Ineligible model served | Critical | model eligibility gate, negative tests |
| Out-of-domain signal emitted | High | operating-domain guardrail, withhold/warn |
| Miscalibrated confidence shown as certainty | High | calibration status required at emit time |
| Drift triggers action/retrain | Critical | alert-only; no auto-retrain test |
| Signal not audited | High | signal persistence + audit event mandatory |
| Live data look-ahead/stale data | High | as-of discipline and freshness checks |
| UI implies trade instruction | High | advisory wording and no execution controls |
| Operator overtrusts signal | Medium-High | warnings, rationale, uncertainty, economic verdict displayed |

---

## 16. Planned ADRs

| ADR | Unit |
|-----|------|
| Live Inference Engine + Eligibility Gate | W3-U01 |
| Advisory Signal Contract and Persistence | W3-U02 |
| Signal Emit-Time Guardrails | W3-U03 |
| Live Market Inference Adapter | W3-U04 |
| Advisory Dashboard UX | W3-U05 |
| Monitoring/Drift Alert Policy | W3-U06 |
| Performance Analytics and Confidence Visualization | W3-U07 |

---

## 17. Plan Self-Check

| ITRGA criterion | Plan status |
|----------------|-------------|
| Advisory-only / no execution | Satisfied |
| Governed-model-only | Satisfied |
| Deterministic inference | Satisfied |
| Operating-domain guardrail | Satisfied |
| Calibrated confidence at emit time | Satisfied |
| No drift auto-action | Satisfied |
| Every signal audited/persisted | Satisfied |
| Trading Intelligence owns signals | Satisfied |
| UX presentation-only | Satisfied |
| Target-platform realism | Satisfied |
| Unit granularity | Satisfied |
| First unit safe slice | Satisfied |
| No construction started by this plan | Satisfied |

---

## 18. DA Readiness Statement

> The Development Authority submits this Wave-3 Engineering Design & Implementation Plan for ITRGA review.  
> No Wave-3 implementation, endpoint, signal, dashboard, live inference service, alert, schema, or UI has begun from this plan.  
> On ITRGA acceptance, DA will await `BUILD_ORDER_W3-U01` and will not self-authorize construction.

---

**End of Wave 3 Engineering Design & Implementation Plan**
