# Wave 4 Engineering Design and Implementation Plan

| Field | Value |
|---|---|
| Wave | **4 — Institutional Intelligence** |
| Objective | Expand analytical capabilities while remaining advisory/research-first |
| Prepared by | AXIOM Development Authority |
| Prepared for | ITRGA review under `docs/build-orders/ITRGA_REQUEST_WAVE4_DESIGN_PLAN.md` |
| Date | 2026-07-16 |
| Status | **Submitted design plan — no construction authorized** |
| Precondition | W3-U08.1 approved; Wave 3 residual-free; Professional Advisor Platform Complete declared |

---

## 0. DA Non-Authorization Statement

This document is a **design plan only**. It does not authorize implementation of Wave 4.

The Development Authority will not build any Wave-4 unit until:

1. ITRGA reviews and accepts this plan; and
2. ITRGA issues a specific Wave-4 Build Order; and
3. the operator authorizes the unit.

The Constitutional Governance Gate remains **CLOSED**. No Wave-4 design element opens execution, broker interaction, order generation, paper trading, or autonomous remediation.

---

## 1. Wave-4 Purpose

Wave 4, **Institutional Intelligence**, expands AXIOM's analytical/research and operator decision-support capabilities beyond individual advisory signals. It introduces institutional-grade intelligence layers such as:

- cross-market correlation intelligence;
- market-regime detection;
- scenario simulation;
- portfolio/risk analytics;
- macro/sector/context overlays where data exists;
- professional signal validation and advisory analytics extensions;
- presentation-only institutional intelligence dashboards.

All Wave-4 outputs are research artifacts. They inform a human operator; they do not act.

---

## 2. Binding Guardrail Compliance — GR-1 through GR-8

| Guardrail | Design response |
|---|---|
| GR-1 Gate remains CLOSED | No Wave-4 component opens, weakens, or adds a code path to open the Constitutional Governance Gate. |
| GR-2 Advisory/research outputs only | Correlations, regimes, scenarios, risk metrics, and validation outputs are labelled research/advisory and must never be framed as trade instructions or guarantees. |
| GR-3 No execution/order/broker APIs | No order payloads, broker calls, execution routes, paper trading, or position controls are introduced. Wave-wide grep remains mandatory every unit. |
| GR-4 Explainable/auditable/reproducible/traceable | Every persisted intelligence artifact carries input lineage, method/config, uncertainty, output hash, version, and audit event. |
| GR-5 Evidence mandatory | Every unit requires operator-run Windows + PostgreSQL evidence; report claims alone cannot approve work. |
| GR-6 Standing controls | First compiled scientific dependency requires wheel-compat spike; new persisted artifacts require committing script + raw SELECT proof; all new UI requires R-3 grep/test/browser evidence. |
| GR-7 Statistical/economic honesty | Every estimate carries uncertainty/sample count; statistical and economic meaning remain separate; no cherry-picking or guaranteed-return framing. |
| GR-8 Presentation-only UX | Frontend dashboards display persisted/read-only artifacts and do not authoritatively recompute analytics client-side. |

---

## 3. Bounded Contexts and Ownership

### 3.1 New bounded context: Institutional Intelligence

Proposed backend package:

```text
backend/app/institutional_intelligence/
```

Responsibilities:

- cross-market analytics;
- correlation reports;
- regime reports;
- scenario reports;
- portfolio/risk research reports;
- professional signal validation reports;
- common intelligence artifact contracts;
- lineage and audit integration.

This context reads from existing Market, ML, and Trading Intelligence contexts. It does not own live feeds, order flow, broker abstractions, auth, or frontend rendering.

### 3.2 Existing context ownership retained

| Context | Retained responsibility | Wave-4 interaction |
|---|---|---|
| Market / Persistence | Candles, market metadata, live simulated seam | Provides historical/live persisted market data to intelligence services. |
| ML Research | Dataset snapshots, feature definitions, validation/calibration/economic/generalization artifacts | Provides validated model/report lineage and statistical methods precedent. |
| Trading Intelligence | Live inference, advisory signals, guardrails, alerts, analytics | Provides advisory signals and alert records for higher-level validation. |
| Frontend UX | Presentation-only operator surfaces | Displays intelligence artifacts via read-only APIs only. |
| External Integration | Hard-closed broker seam | Not used by Wave 4. Gate remains CLOSED. |

---

## 4. Data and Persistence Design

Wave 4 should use explicit persisted report/artifact tables rather than in-memory-only analytics when an artifact is intended to support operator review or ITRGA evidence.

### 4.1 Common artifact fields

Every new persisted intelligence artifact should include at least:

```text
id
created_at UTC
artifact_type
method_version
config
input_lineage
source_artifact_ids
market_scope
as_of_start / as_of_end
sample_count
uncertainty
results
limitations
report_hash
research_status
created_by / actor
audit_correlation_id
```

### 4.2 Candidate artifact tables

| Artifact | Proposed table | Purpose | Persistence control applies? |
|---|---|---|---|
| Compatibility evidence | `scientific_dependency_spikes` or evidence-only file | Prove Windows/Python 3.14.6 install/import/smoke for compiled libs | If persisted table is added, yes; otherwise evidence file only |
| Correlation report | `correlation_reports` | Rolling/static correlation with uncertainty and sample count | Yes |
| Regime report | `regime_reports` | Market-regime classification research artifact | Yes |
| Scenario report | `scenario_reports` | Hypothetical scenario/counterfactual research outcomes | Yes |
| Portfolio/risk report | `portfolio_risk_reports` | Hypothetical exposure, drawdown, VaR/ES-style research metrics with uncertainty | Yes |
| Signal validation extension | `professional_signal_validation_reports` | Advisory signal outcome/quality research with uncertainty | Yes |
| UI annotations | likely no new table initially | Display existing persisted reports on charts/dashboard | Only if persisted annotations are added |

No artifact may contain an executable order payload or remediation directive.

---

## 5. Statistical and Economic Methodology

### 5.1 Correlation intelligence

Purpose: identify relationships between markets/timeframes as research context.

Controls:

- all correlation windows are time-bounded and as-of constrained;
- no future data beyond `as_of_end`;
- sample count mandatory;
- uncertainty interval mandatory;
- method/config stored;
- significance reported separately from economic usefulness;
- correlation never becomes a signal or instruction.

Candidate estimators:

- Pearson correlation for linear relation;
- Spearman/rank correlation if dependency stack is approved;
- bootstrap confidence intervals if computationally feasible;
- pure-Python fallback if compiled dependencies fail spike.

### 5.2 Regime detection

Purpose: classify market context such as trend/range/volatile/calm using explainable rules or validated statistical methods.

Controls:

- regime label has evidence and confidence/uncertainty;
- regime is not a trade instruction;
- no model retraining side effect;
- no hidden clustering model unless experiment-governed and dependency-spiked;
- no look-ahead in feature windows.

### 5.3 Scenario simulation

Purpose: hypothetical research scenario exploration.

Controls:

- prominently labelled hypothetical;
- no order sizing output intended for execution;
- no broker/order payload;
- uncertainty and limitations shown;
- scenario inputs and assumptions stored;
- no guaranteed-return language.

### 5.4 Portfolio/risk analytics

Purpose: research-level risk/exposure view for advisory context.

Controls:

- hypothetical/advisory labels;
- no account/broker/position linkage unless future governance authorizes;
- drawdown, volatility, and stress metrics include uncertainty/sample count;
- economic usefulness and statistical evidence remain separate.

### 5.5 Professional signal validation

Purpose: evaluate advisory signal quality over persisted records.

Controls:

- read persisted signals and outcomes only where outcome data is governed;
- no cherry-picked windows;
- uncertainty mandatory;
- raw score not treated as confidence;
- no guaranteed future performance.

---

## 6. Dependencies and Wheel-Compatibility Strategy

Wave 4 is likely to need scientific libraries. TD-065 requires a Windows + Python 3.14.6 wheel-compatibility spike before adopting any compiled dependency.

### 6.1 Candidate dependency sets

| Capability | Candidate dependency | Risk | Spike required? |
|---|---|---|---|
| Correlation/statistics | numpy, scipy, pandas | compiled wheels / Python 3.14.6 compatibility | Yes |
| Regime detection | numpy/scipy or scikit-learn | compiled wheels | Yes |
| Risk analytics | numpy/scipy/pandas | compiled wheels | Yes |
| Visualization | existing React/CSS first | low | No unless new chart lib introduced |

### 6.2 Recommended policy

W4-U01 should perform the compatibility spike before any Wave-4 unit depends on compiled scientific libraries. If the spike fails, W4-U01 should define a pure-Python fallback path and defer compiled adoption.

---

## 7. UX Surfaces

Wave-4 UX surfaces are presentation-only and authenticated.

Candidate surfaces:

- Institutional Intelligence overview dashboard;
- Correlation matrix/report view;
- Regime context panel;
- Scenario simulator view labelled hypothetical;
- Risk analytics view labelled research/not guarantee;
- Signal validation view with uncertainty and lineage;
- Chart annotations sourced from persisted reports only.

Each surface must show:

- advisory/research disclaimer;
- uncertainty/sample count;
- lineage/method/config where relevant;
- no buy/sell/order/broker controls;
- no guaranteed-return language.

---

## 8. Risk Register Plan

| Planned risk | Severity | Mitigation / proof |
|---|---|---|
| Correlation mistaken for causation | High | UI disclaimer, methodology note, uncertainty, no instruction language; screenshot proof |
| Scenario output treated as trade instruction | Critical | No order payload, hypothetical labels, no action controls; grep/test/screenshot |
| Compiled dependency incompatible with Windows/Python 3.14.6 | Medium-High | W4-U01 wheel-compat spike before dependency adoption |
| Regime detector leaks future data | Critical | As-of windows, future-data negative test, report lineage |
| Portfolio/risk analytics imply guaranteed returns | High | uncertainty and not-guaranteed language; UI test/browser proof |
| New persisted artifact unaudited | High | audit event and raw SELECT proof first submission |
| Client recomputes analytics authoritatively | High | read-only API, presentation-only grep/test |
| D-W2-001 market-agnostic discipline bypassed | High | no per-market specialized model unless governed amendment; structural tests |

---

## 9. Proposed Implementation Sequence

### W4-U01 — Scientific Dependency Compatibility + Intelligence Artifact Governance Foundation

Purpose: prove the Wave-4 safety/engineering foundation before analytical features.

Scope:

- Windows/Python 3.14.6 wheel-compat spike for proposed scientific dependencies;
- choose approved dependency set or pure-Python fallback;
- define Institutional Intelligence bounded context;
- common artifact/report base contracts;
- audit/persistence pattern;
- no-execution/no-guarantee policy tests;
- no operator-facing analytic feature yet unless needed for evidence.

Why first: it discharges TD-065 and prevents building analytics on an incompatible stack.

### W4-U02 — Correlation Intelligence Reports

- Persisted correlation reports;
- as-of windows;
- uncertainty/sample counts;
- no correlation-as-signal framing;
- read-only API;
- committing script + raw SELECT proof.

### W4-U03 — Regime Detection Reports

- Explainable regime classification reports;
- no-look-ahead feature windows;
- confidence/uncertainty;
- audit and lineage;
- no model retrain side effect.

### W4-U04 — Scenario Simulation Research Reports

- Hypothetical scenario reports;
- assumptions, lineage, uncertainty;
- no order payload or sizing directive;
- presentation-only API/UI if authorized.

### W4-U05 — Portfolio/Risk Research Analytics

- Hypothetical risk analytics;
- no account/broker position link;
- uncertainty and limitations;
- no guaranteed-return framing.

### W4-U06 — Professional Signal Validation Extension

- Extended advisory validation over persisted signals/outcomes;
- uncertainty mandatory;
- raw-score exclusion preserved;
- no cherry-picking.

### W4-U07 — Institutional Intelligence Dashboard / Chart Context

- Presentation-only UI over persisted intelligence reports;
- browser evidence mandatory;
- no action controls;
- no client-side authoritative recomputation.

### W4-U08 — Wave-4 Closeout & Hardening

- full-wave no-execution proof;
- artifact audit completeness;
- auth/read-only proof;
- docs/register reconciliation;
- milestone candidate: Institutional Intelligence Layer Complete.

---

## 10. Recommended W4-U01 Scope

Recommended first Build Order:

> **W4-U01 — Scientific Dependency Compatibility + Institutional Intelligence Artifact Foundation**

Acceptance criteria should include:

- no product analytics feature beyond foundation;
- wheel spike on Windows + Python 3.14.6 for candidate scientific dependencies;
- import/smoke evidence;
- fallback plan if dependencies fail;
- `institutional_intelligence` bounded-context skeleton;
- common report/artifact contract;
- no-execution/no-broker grep;
- no guaranteed-return language;
- audit/persistence pattern defined;
- no schema unless required; if schema added, Alembic + raw SELECT proof;
- full suite green and local CI exit 0.

---

## 11. Bright-Line Self-Check

| Capability | GR-1 Gate closed | GR-2 Advisory only | GR-3 No execution | GR-4 Traceable | GR-7 Uncertainty | GR-8 Presentation-only |
|---|---|---|---|---|---|---|
| Dependency/foundation | Yes | Yes | Yes | Yes | N/A / policy | Yes |
| Correlation | Yes | Yes | Yes | Yes | Yes | Yes |
| Regime | Yes | Yes | Yes | Yes | Yes | Yes |
| Scenario | Yes | Yes/hypothetical | Yes | Yes | Yes | Yes |
| Portfolio/risk | Yes | Yes/research | Yes | Yes | Yes | Yes |
| Signal validation | Yes | Yes | Yes | Yes | Yes | Yes |
| Dashboards | Yes | Yes | Yes | Displays lineage | Displays uncertainty | Yes |

---

## 12. ITRGA Review Request

The Development Authority submits this Wave-4 Design Plan for ITRGA review.

No Wave-4 implementation is authorized by this plan. DA awaits ITRGA review, refinements, and a future Build Order before beginning W4-U01.

---

**End of Wave 4 Engineering Design and Implementation Plan**
