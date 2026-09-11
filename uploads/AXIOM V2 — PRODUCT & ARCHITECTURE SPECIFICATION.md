# AXIOM V2 — PRODUCT & ARCHITECTURE SPECIFICATION

## Institutional Trading, Research, Intelligence, Portfolio, Risk, Simulation & Governed Execution Platform

| Field | Value |
|---|---|
| Product | **AXIOM** |
| Generation | **Version 2** |
| Document Type | **Product & Architecture Specification** |
| Relationship to V1 | **V2 extends V1; V1 remains the foundational baseline** |
| Governance Status | **Proposed — Design Stage** |
| Current V1 Governance Gate | **CLOSED** |
| V1 Production Status | **NOT CERTIFIED** |
| V2 Implementation Authorization | **NONE** |
| Primary Authorities | **Operator · Development Authority (DA) · ITRGA** |
| Intended Audience | Operator, DA, ITRGA, architects, engineers, security, QA, research and product stakeholders |

---

# 1. DOCUMENT PURPOSE

This document defines the proposed **AXIOM Version 2** product and architecture.

AXIOM V2 is not a replacement for AXIOM V1.

It is a deliberate expansion of the V1 foundation into a broader institutional trading and research platform capable of supporting:

- real market data;
- historical market data;
- multiple market-data providers;
- deterministic market-structure analysis;
- predictive machine learning;
- advanced chart intelligence;
- institutional research and intelligence;
- portfolio management;
- account visibility;
- risk management;
- paper trading;
- broker connectivity;
- exchange connectivity where authorized;
- order management;
- position management;
- governed execution;
- backtesting;
- simulation and replay;
- research automation;
- contextual AI assistance;
- evidence and artifact lineage;
- audit and governance.

This document is a **product and architecture specification**.

It is not:

- a Build Order;
- an implementation authorization;
- an ITRGA determination;
- a broker-connection authorization;
- a live-trading authorization;
- a production-readiness certification.

All implementation must proceed through the established AXIOM governance lifecycle.

---

# 2. WHY AXIOM V2 EXISTS

AXIOM V1 established the research, analysis, intelligence, evidence, governance and terminal foundation.

AXIOM V2 expands that foundation into a fuller institutional operating environment.

The purpose of V2 is therefore not:

> **Restart AXIOM.**

The purpose is:

> **Extend AXIOM into the complete product capability envisioned for the next generation while preserving the validated V1 foundation.**

The V2 programme must therefore:

1. preserve V1 historical truth;
2. preserve useful V1 capabilities;
3. reuse functioning V1 infrastructure where appropriate;
4. introduce new capabilities through explicit architectural boundaries;
5. add execution only through a dedicated governed execution architecture;
6. maintain the evidence and governance discipline established in V1.

---

# 3. V1 → V2 RELATIONSHIP

The intended relationship is:

```text
                         AXIOM V1
                            │
        ┌───────────────────┼────────────────────┐
        │                   │                    │
      MARKET             INTELLIGENCE         RESEARCH
      ANALYSIS           + ML Research        + EVIDENCE
        │                   │                    │
     Charts             Signals               Reports
     Structure           Risk                  Lineage
     Indicators         Scenarios              Audit
        │                   │                    │
        └───────────────────┼────────────────────┘
                            │
                       V1 FOUNDATION
                            │
                            ▼
                         AXIOM V2
                            │
      ┌─────────────────────┼─────────────────────┐
      │                     │                     │
 REAL / HISTORICAL      ADVANCED            EXECUTION
 MARKET DATA           INTELLIGENCE          PLATFORM
      │                     │                     │
 Providers              Context Engine        Brokers
 Vendors                Chart Intelligence    Orders
 Streaming              Advanced ML           Positions
 Historical             Research              Accounts
      │                     │                     │
      └─────────────────────┼─────────────────────┘
                            │
                       PORTFOLIO / RISK
                            │
                     PAPER / SIMULATION
                            │
                       RESEARCH AUTOMATION
                            │
                      GOVERNED AI / ASSISTANT
                            │
                         TERMINAL
                            │
                       HUMAN OPERATOR
```

V1 remains historical truth.

V2 must not silently rewrite V1:

- implementation history;
- Build Orders;
- Delivery Reports;
- ITRGA determinations;
- research conclusions;
- technical-debt history;
- provenance records.

---

# 4. V2 PRODUCT MISSION

AXIOM V2 is intended to provide one professional institutional workstation for:

> **observing markets, understanding market structure, researching intelligence, evaluating portfolio and risk conditions, testing trading hypotheses, simulating trading workflows, managing governed paper and live trading workflows, and making informed human decisions from one coherent terminal.**

Where live execution is authorized, V2 shall provide controlled execution infrastructure rather than allowing arbitrary UI-to-broker access.

---

# 5. V2 PRODUCT IDENTITY

AXIOM V2 should feel like:

> **A professional institutional trading terminal with an integrated research and intelligence platform.**

It should not become merely:

- a generic dashboard;
- a chatbot with charts;
- a broker wrapper with a research page;
- an autonomous trading bot;
- a collection of unrelated applications.

The terminal must retain one coherent operating context.

---

# 6. CORE V2 ARCHITECTURE

The high-level architecture is:

```text
                         AXIOM V2
                            │
        ┌───────────────────┼─────────────────────┐
        │                   │                     │
     MARKET DATA        INTELLIGENCE          EXECUTION
        │                   │                     │
   Live/Historical      Structure              Broker
   Provider Layer       Context                Exchange
   Vendor Adapters      Chart AI               Orders
   Data Quality         ML Research            Positions
                       Research                 Accounts
                       Scenarios                Fills
                       Risk
        │                   │                     │
        └───────────────────┼─────────────────────┘
                            │
                     MARKET CONTEXT
                            │
              ┌─────────────┼──────────────┐
              │             │              │
           SIGNALS        RESEARCH         RISK
              │             │              │
              └─────────────┼──────────────┘
                            │
                       ASSISTANT
                            │
                       AXIOM TERMINAL
                            │
                     HUMAN OPERATOR
```

---

# 7. ARCHITECTURAL PRINCIPLES

AXIOM V2 shall follow the following principles.

## 7.1 Separation of concerns

The following responsibilities remain distinct:

- market-data ingestion;
- data normalization;
- deterministic market analysis;
- market context;
- predictive ML;
- trading intelligence;
- research;
- portfolio;
- risk;
- execution;
- assistant;
- presentation;
- governance.

## 7.2 Provider abstraction

External providers must be accessed through controlled adapters.

The AXIOM core must not become tightly coupled to a single vendor.

## 7.3 Execution isolation

Broker/exchange execution must occur through an isolated execution gateway.

Frontend components must never call broker APIs directly.

## 7.4 Evidence-first operation

Important analytical, research, portfolio and execution states should produce traceable evidence.

## 7.5 Human control

V2 may support live execution, but authority remains explicit.

## 7.6 Safe failure

Failures must produce explicit degraded states rather than fabricated successful states.

## 7.7 No fabricated state

AXIOM must never fabricate:

- prices;
- market data;
- balances;
- positions;
- fills;
- broker confirmations;
- vendor data;
- model performance;
- research results;
- certification status.

---

# 8. V2 DATA PROVIDER ARCHITECTURE

## 8.1 Provider Abstraction

AXIOM shall use an internal normalized data interface.

```text
                    AXIOM DATA API
                         │
            ┌────────────┼────────────┐
            │            │            │
        Provider A   Provider B   Provider C
            │            │            │
        Historical      Live      Alternative
            │            │            │
            └────────────┼────────────┘
                         ▼
                    NORMALIZATION
                         ▼
                     AXIOM DATA
```

Provider adapters may expose:

- historical OHLCV;
- ticks;
- spreads;
- depth/order book;
- sessions;
- instrument metadata;
- corporate events;
- macroeconomic data;
- other authorized datasets.

---

# 9. REAL AND LIVE MARKET DATA

V2 may support real/live market data.

Potential capabilities include:

- live prices;
- streaming candles;
- real-time indicators;
- live market structure;
- live signals;
- live alerts;
- market-depth data where supported;
- session state;
- market status.

Every live stream must expose an explicit data state:

```text
LIVE
DELAYED
STALE
DISCONNECTED
UNAVAILABLE
SIMULATED
```

The terminal must not allow stale or simulated information to appear indistinguishable from live information.

---

# 10. HISTORICAL MARKET DATA

V2 shall support reproducible historical datasets.

Potential datasets include:

- OHLCV;
- ticks;
- spreads;
- market depth;
- instrument metadata;
- economic events;
- corporate/fundamental events.

Historical research should identify:

- dataset;
- version/snapshot;
- source;
- date range;
- timeframe;
- timezone;
- applicable assumptions.

---

# 11. EXTERNAL MARKET-DATA PROVIDERS

V2 may support authorized commercial or institutional providers such as:

- Bloomberg;
- Refinitiv/LSEG;
- FactSet;
- exchange-native feeds;
- specialist alternative-data providers.

However:

> **AXIOM must never claim a provider integration until the integration actually exists, is authorized, and has evidence supporting the claim.**

The product must distinguish:

```text
Provider Integrated
vs.
Provider Available in Architecture
vs.
Provider Not Integrated
```

---

# 12. DATA QUALITY & TEMPORAL INTEGRITY

V2 shall enforce:

- chronological ordering;
- future-data prevention;
- duplicate detection;
- missing-data handling;
- stale-data detection;
- timestamp integrity;
- timezone consistency;
- snapshot/version identification;
- reproducible research inputs.

Historical research and backtesting must never use future information accidentally.

---

# 13. DETERMINISTIC MARKET STRUCTURE & TECHNICAL INTELLIGENCE

V2 retains and extends the deterministic V1 market-analysis foundation.

This capability family includes:

- Break of Structure;
- Change of Character;
- Fair Value Gaps;
- market structure;
- swing highs/lows;
- Order Blocks;
- liquidity-related structures;
- trendlines;
- support/resistance;
- pivots;
- session levels;
- traditional technical indicators.

These outputs are descriptive and analytical.

They do not require a promoted predictive ML model.

---

# 14. MARKET CONTEXT ENGINE

V2 shall add a synthesis layer above the individual deterministic indicators.

```text
Trend
+
Structure
+
Swings
+
Liquidity
+
Levels
+
Session
+
Volatility
+
Momentum
+
Timeframe
+
Market Data
        ↓
MARKET CONTEXT
```

The engine may produce structured context such as:

- prevailing trend;
- structural state;
- protected swing;
- structural break;
- liquidity context;
- key levels;
- session context;
- volatility state;
- momentum state;
- timeframe relationships.

All generated context must remain traceable to contributing observations.

---

# 15. MULTI-TIMEFRAME REASONING

V2 may reason across multiple timeframes.

A representative relationship is:

```text
Higher Timeframe
      ↓
Market Context
      ↓
Intermediate Timeframe
      ↓
Local Structure
      ↓
Setup / Signal
```

The system must distinguish:

- directly observed information;
- derived relationships;
- contextual interpretation;
- statistical prediction.

It must not imply unsupported cross-timeframe conclusions.

---

# 16. CHART INTELLIGENCE ENGINE

V2 shall develop a higher-level Chart Intelligence Engine above deterministic market-structure detection.

Conceptual pipeline:

```text
Chart / Market Data
       ↓
Deterministic Detection
       ↓
Market Context
       ↓
Chart Intelligence
       ↓
Annotations + Interpretation
```

Potential capabilities:

- automatic structural annotations;
- contextual trend interpretation;
- liquidity visualization;
- multi-timeframe interpretation;
- contextual setup descriptions;
- chart-focused research;
- natural-language chart explanation.

The engine must clearly distinguish facts from interpretations and predictions.

---

# 17. PREDICTIVE MACHINE LEARNING

Predictive ML remains a separate evidence-gated subsystem.

V2 may expand the ML capability through:

- multiple model families;
- feature engineering;
- multi-horizon prediction;
- regime-conditioned models;
- ensembles;
- probability calibration;
- uncertainty estimation;
- walk-forward validation;
- economic validation;
- cross-market generalization;
- shadow models;
- champion/challenger testing;
- model registry;
- model promotion;
- rollback.

A failed predictive model remains a valid research result.

The absence of a promotable model must not disable unrelated deterministic intelligence.

---

# 18. SIGNAL ARCHITECTURE

V2 shall explicitly distinguish signal families.

## 18.1 Structural / Deterministic Signals

Derived from deterministic analysis:

- BoS;
- CHoCH;
- FVG;
- structural breaks;
- level breaks;
- liquidity events.

These can function independently of predictive ML.

## 18.2 Predictive Advisory Signals

Derived from an eligible predictive ML model.

Predictive signals should identify:

- model;
- model version;
- probability;
- confidence/calibration;
- freshness;
- limitations;
- evidence/lineage.

The terminal must never display structural and predictive signals as though they were the same thing.

---

# 19. TRADING INTELLIGENCE

Trading Intelligence may combine:

- market structure;
- deterministic indicators;
- predictive ML;
- market context;
- research;
- scenarios;
- portfolio state;
- risk.

```text
STRUCTURAL EVIDENCE
        +
PREDICTIVE EVIDENCE
        +
RESEARCH
        +
RISK
        +
PORTFOLIO CONTEXT
        ↓
TRADING INTELLIGENCE
        ↓
DECISION SUPPORT
```

The system must distinguish:

- observation;
- calculation;
- prediction;
- interpretation;
- recommendation;
- execution.

---

# 20. RESEARCH & INTELLIGENCE REPORTS

V2 may generate and persist institutional reports covering:

- correlation;
- market regime;
- scenario analysis;
- portfolio/risk;
- signal validation;
- market structure;
- model diagnostics;
- execution analytics.

Reports should contain where applicable:

- source data;
- computation version;
- as-of timestamp;
- assumptions;
- uncertainty;
- limitations;
- lineage;
- reproducibility information.

---

# 21. SCENARIO ENGINE

V2 may support:

- scenario definitions;
- parameterized scenarios;
- scenario comparison;
- historical replay scenarios;
- stress tests;
- what-if analysis;
- scenario reporting.

Scenario operations must be governed.

The following are not permitted as unrestricted generic behavior:

- arbitrary mutation of institutional artifacts;
- hidden scenario changes;
- unaudited report modification;
- unrestricted scheduling.

---

# 22. RESEARCH AUTOMATION

V2 may introduce a governed research-job system.

Possible jobs:

- scheduled reports;
- recurring intelligence;
- batch scenarios;
- model evaluation;
- daily/weekly research packages;
- monitoring jobs.

Conceptual flow:

```text
Authorized Job
      ↓
Job Queue
      ↓
Research Service
      ↓
Research Artifact
      ↓
Lineage
      ↓
Audit
```

Every scheduled job must have:

- owner;
- authorization;
- schedule;
- inputs;
- output;
- status;
- audit record;
- failure handling.

---

# 23. RESEARCH ARTIFACT MODEL

Research artifacts may include:

- reports;
- scenario results;
- model evaluations;
- signal investigations;
- market studies;
- portfolio studies;
- execution analyses;
- operator research notes.

Each artifact should support:

- identity;
- type;
- version;
- creation time;
- source;
- producing service/user;
- status;
- lineage;
- limitations;
- relationships.

---

# 24. PORTFOLIO MANAGEMENT

V2 may provide:

- portfolios;
- multi-account views;
- allocations;
- exposure;
- concentration;
- performance;
- P&L;
- attribution;
- benchmarks;
- risk-adjusted metrics;
- stress testing;
- portfolio research.

Portfolio analytics should remain useful even when execution is disabled.

---

# 25. ACCOUNT MANAGEMENT

V2 may provide controlled account-state visibility.

Potential attributes:

- account identity;
- currency;
- balance;
- equity;
- available funds;
- margin;
- free margin;
- leverage;
- buying power;
- realized P&L;
- unrealized P&L;
- account status.

Sensitive information must be protected through authentication, RBAC, least privilege and audit.

---

# 26. POSITION MANAGEMENT

V2 may support:

- current positions;
- historical positions;
- entry price;
- mark price;
- size;
- side;
- realized P&L;
- unrealized P&L;
- exposure;
- margin usage;
- lifecycle state.

The position model should support both:

- paper environments;
- authorized live environments.

---

# 27. ORDER MANAGEMENT

V2 may support:

- order creation;
- order validation;
- submission;
- modification;
- cancellation;
- order status;
- history;
- execution/fill history.

Potential order types include:

- market;
- limit;
- stop;
- stop-limit;
- provider-specific types where appropriate.

Every order must have an explicit lifecycle and unique correlation/client identifier.

---

# 28. EXECUTION GATEWAY

Execution must be isolated:

```text
AXIOM Terminal
       ↓
Order Intent
       ↓
Risk Gateway
       ↓
Execution Gateway
       ↓
Broker Adapter
       ↓
Broker / Exchange
       ↓
Execution Result
       ↓
Audit / State Reconciliation
```

The frontend must never directly communicate with broker APIs.

The execution gateway must enforce:

- authorization;
- account selection;
- instrument permissions;
- order validation;
- risk checks;
- idempotency;
- duplicate-order prevention;
- audit;
- provider error handling;
- execution confirmation.

---

# 29. BROKER / EXCHANGE ADAPTER LAYER

V2 shall support provider-specific adapters:

```text
                   EXECUTION GATEWAY
                          │
          ┌───────────────┼───────────────┐
          │               │               │
       Broker A        Broker B        Broker C
          │               │               │
       Adapter          Adapter         Adapter
```

The internal AXIOM order model should remain provider-neutral wherever practical.

---

# 30. PAPER TRADING ENGINE

Paper trading is a legitimate V2 capability.

Conceptual flow:

```text
Order Intent
      ↓
Risk Gateway
      ↓
Paper Execution Simulator
      ↓
Paper Account
      ↓
Fills
      ↓
Positions
      ↓
Balance / Margin
      ↓
P&L
```

The simulator may model:

- spreads;
- slippage;
- commissions;
- latency;
- partial fills;
- rejected orders;
- margin;
- order lifecycle;
- position lifecycle.

Paper mode must be visually unmistakable:

> **PAPER / SIMULATED**

Paper results must never be presented as live financial results.

---

# 31. LIVE TRADING

V2 may support authorized live trading after the execution architecture satisfies the relevant security, risk, governance, operational and production requirements.

Live mode requires:

- authenticated operator;
- authorized account;
- authorized provider;
- risk validation;
- explicit environment state;
- execution audit;
- broker acknowledgement;
- failure/reconciliation handling.

Early V2 live execution should default to explicit human confirmation.

Autonomous execution, if ever introduced, requires an additional explicit governance decision.

---

# 32. RISK ENGINE

V2 shall expand the risk capability.

Potential capabilities:

- position sizing;
- exposure;
- concentration;
- leverage;
- margin;
- drawdown;
- portfolio risk;
- stress testing;
- correlation risk;
- transaction-cost analysis;
- liquidity risk;
- execution risk;
- model risk.

The Risk Engine should serve:

- portfolio;
- paper trading;
- live execution;
- backtesting;
- strategy research.

---

# 33. PRE-TRADE RISK CONTROLS

Before live submission, the system should evaluate:

- account permissions;
- instrument permissions;
- position limits;
- order limits;
- exposure limits;
- margin;
- concentration;
- trading-session rules;
- duplicate orders;
- applicable risk policies.

A failed risk condition must produce a clear rejection/refusal state.

---

# 34. BACKTESTING ENGINE

V2 may include a strategy/backtest engine supporting:

- historical data;
- deterministic signals;
- eligible predictive signals;
- transaction costs;
- spread;
- slippage;
- latency;
- portfolio rules;
- risk constraints.

Potential metrics:

- return;
- drawdown;
- Sharpe;
- Sortino;
- expectancy;
- hit rate;
- profit factor;
- turnover;
- cost impact;
- exposure;
- time in market.

Backtest results are not live results.

---

# 35. SIMULATION & HISTORICAL REPLAY

V2 may support:

- historical replay;
- candle-by-candle playback;
- signal replay;
- strategy simulation;
- paper execution;
- risk simulation;
- strategy comparison.

Replay must preserve temporal integrity.

The engine must prevent future-information leakage.

---

# 36. NEWS / FUNDAMENTAL / MACRO INTELLIGENCE

V2 may integrate:

- economic calendar;
- macroeconomic indicators;
- news;
- sentiment;
- fundamentals;
- earnings;
- central-bank events;
- alternative data.

These become contextual inputs into the intelligence system.

They are not automatically trading instructions.

---

# 37. ASSISTANT V2

The assistant may become context-aware of:

- selected instrument;
- timeframe;
- market structure;
- technical indicators;
- signals;
- research;
- scenarios;
- portfolio;
- risk;
- orders;
- positions;
- execution status.

Potential interactions:

- explain the current market structure;
- explain a signal;
- summarize research;
- explain risk exposure;
- explain an order rejection;
- compare scenarios;
- explain execution state.

The assistant must distinguish:

```text
OBSERVATION
PREDICTION
INTERPRETATION
RECOMMENDATION
ACTION
```

---

# 38. EXTERNAL AI PROVIDER ADAPTERS

V2 may optionally support external LLM providers.

```text
AXIOM ASSISTANT
       ↓
AI PROVIDER INTERFACE
       │
 ┌─────┼──────┐
 │     │      │
Local  LLM  Provider B
Model   A
```

Every external provider requires:

- explicit authorization;
- configuration;
- security controls;
- data-sharing rules;
- model identity;
- request/response logging;
- secret management;
- refusal policy;
- failure/fallback behavior.

No provider may be silently introduced.

---

# 39. AI EXECUTION BOUNDARY

Natural-language requests must never bypass execution controls.

```text
Natural Language
      ↓
Intent
      ↓
Authorization
      ↓
Risk
      ↓
Execution Policy
      ↓
Human / Authorized Automation
      ↓
Execution Gateway
```

Access to account context does not imply execution authority.

---

# 40. TERMINAL V2

V2 should evolve the V1 terminal instead of restarting the shell.

The terminal should ultimately provide:

- global header;
- instrument search;
- watchlists;
- chart stage;
- market-structure context;
- signals;
- intelligence;
- research;
- portfolio;
- risk;
- orders;
- positions;
- alerts;
- journal;
- assistant;
- evidence/governance;
- controlled execution controls.

---

# 41. V2 WORKSPACES

Potential workspaces:

### Trading Workspace

Watchlist + Chart + Signals + Order Ticket + Positions

### Research Workspace

Chart + Research + Intelligence + Evidence

### Risk Workspace

Portfolio + Exposure + Risk + Positions + Scenarios

### Investigation Workspace

Instrument + Chart + Signal + Evidence + Research

### Execution Workspace

Account + Order Ticket + Risk + Positions + Execution Status

### Intelligence Workspace

Market + Structure + Intelligence + Research + Assistant

---

# 42. ORDER TICKET UX

The order ticket should display:

- account;
- instrument;
- side;
- quantity;
- order type;
- price;
- stop-loss;
- take-profit;
- estimated cost;
- estimated margin;
- risk metrics;
- validation status;
- execution mode.

Paper and live states must be unmistakable.

---

# 43. EXECUTION STATUS UX

The system should distinguish:

```text
DRAFT
VALIDATING
RISK BLOCKED
READY
SUBMITTED
ACKNOWLEDGED
PARTIALLY FILLED
FILLED
CANCELLED
REJECTED
FAILED
UNKNOWN
```

The UI must never display successful execution without authoritative execution evidence.

---

# 44. PORTFOLIO / EXECUTION STATE CONSISTENCY

V2 must preserve consistency across:

```text
Order
 ↓
Fill
 ↓
Position
 ↓
Account
 ↓
Portfolio
 ↓
Risk
 ↓
Audit
```

Partial failures must be detectable.

---

# 45. RECONCILIATION ENGINE

V2 should reconcile:

- broker vs AXIOM positions;
- broker vs AXIOM orders;
- broker vs AXIOM balances;
- provider vs AXIOM market state.

Differences must create a visible discrepancy state containing:

- severity;
- timestamp;
- correlation;
- affected object;
- resolution state.

---

# 46. ENVIRONMENT MODES

V2 should explicitly support:

```text
RESEARCH
SIMULATION
PAPER
LIVE
```

The active mode must remain visible throughout:

- market data;
- account state;
- orders;
- positions;
- execution;
- reports;
- assistant behavior.

Accidental transitions from paper to live must be prevented.

---

# 47. LIVE TRADING SAFEGUARDS

Live mode should require:

- obvious LIVE indicator;
- account confirmation;
- provider/broker confirmation;
- risk confirmation;
- order preview;
- explicit authorization;
- audit;
- kill switch;
- session controls.

---

# 48. EMERGENCY CONTROLS

V2 may support:

- disable live execution;
- disconnect broker;
- prevent new orders;
- cancel eligible orders where safely supported;
- freeze automated jobs;
- preserve audit state.

Emergency controls must themselves be authenticated and audited.

---

# 49. STRATEGY LAYER

V2 may introduce a governed strategy model containing:

- entry rules;
- exit rules;
- filters;
- instruments;
- timeframes;
- risk rules;
- position sizing;
- execution rules.

Strategies must be:

- versioned;
- testable;
- auditable;
- permission controlled.

---

# 50. STRATEGY / MODEL LIFECYCLE

A possible governed lifecycle is:

```text
DRAFT
 ↓
BACKTESTED
 ↓
VALIDATED
 ↓
PAPER
 ↓
APPROVED
 ↓
AUTHORIZED
 ↓
LIVE
 ↓
RETIRED
```

The exact lifecycle and gates require separate governance before implementation.

---

# 51. RESEARCH-TO-EXECUTION TRACEABILITY

Where appropriate, V2 should preserve:

```text
Research Artifact
      ↓
Scenario
      ↓
Signal / Strategy
      ↓
Order Intent
      ↓
Risk Decision
      ↓
Execution
      ↓
Fill
```

This provides traceability without claiming causation when the evidence does not establish it.

---

# 52. PERFORMANCE-CLAIM DISCIPLINE

V2 must distinguish:

- backtest results;
- simulation results;
- paper results;
- live results;
- model research;
- hypothetical scenarios.

Never describe:

- backtest as live;
- paper P&L as real P&L;
- simulated fills as broker fills;
- an unpromoted model as proven predictive edge.

Production readiness must never be claimed without the required certification.

---

# 53. VERSIONING

Where useful, independently version:

- data schemas;
- provider adapters;
- indicator engine;
- Market Context Engine;
- Chart Intelligence Engine;
- models;
- strategies;
- research reports;
- broker adapters;
- execution gateway.

Versions should be visible in evidence and audit records.

---

# 54. V2 MIGRATION STRATEGY

V2 should evolve incrementally.

A conceptual capability progression is:

```text
V1 Baseline
   ↓
V2 Data Abstraction
   ↓
Historical + Live Data
   ↓
Market Context / Structure
   ↓
Chart Intelligence
   ↓
Portfolio / Account
   ↓
Paper Trading
   ↓
Broker / Execution Gateway
   ↓
Orders / Positions
   ↓
Advanced Risk
   ↓
Backtesting / Simulation
   ↓
Research Automation
   ↓
Assistant / AI Providers
   ↓
Unified V2 Terminal
   ↓
End-to-End Verification
```

This is a **conceptual dependency model only**.

It is not implementation authorization or a mandatory roadmap.

The final phase structure must be decided through the normal Operator/DA/ITRGA process.

---

# 55. V2 REPOSITORY & PROVENANCE

The V2 programme must identify:

- V1 parent baseline;
- V2 initialization baseline;
- V2 architecture version;
- migration notes;
- current V2 state;
- retired legacy repository references where applicable.

If V2 uses a new repository, its history must accurately represent its ancestry.

A deleted repository must not be falsely represented as the Git ancestor of the new repository.

Historical V1 evidence is preserved independently where necessary.

---

# 56. V2 CAPABILITY MATURITY

Every V2 capability shall be classified as:

```text
DESIGNED
   ↓
IMPLEMENTED
   ↓
TESTED
   ↓
VERIFIED
   ↓
APPROVED
   ↓
AUTHORIZED
   ↓
PRODUCTION CERTIFIED
```

No capability may advance between states without appropriate evidence.

---

# 57. PRODUCTION CERTIFICATION

Production certification remains separate from development.

It should evaluate:

- security;
- reliability;
- observability;
- data integrity;
- execution safety;
- risk controls;
- reconciliation;
- performance;
- accessibility;
- governance;
- recovery;
- operational readiness.

Passing engineering tests does not equal production certification.

---

# 58. V2 END-TO-END WORKFLOW

The complete intended V2 workflow is:

```text
Discover Market
      ↓
Receive Historical / Live Data
      ↓
Analyze Chart
      ↓
Interpret Market Structure
      ↓
Generate Market Context
      ↓
Evaluate Signals
      ↓
Review Research / Intelligence
      ↓
Evaluate Portfolio / Risk
      ↓
Backtest / Simulate
      ↓
Paper Trade
      ↓
Risk Validate
      ↓
Human Authorize
      ↓
Execute through Broker
      ↓
Confirm Fill
      ↓
Update Position
      ↓
Update Portfolio
      ↓
Record Audit / Lineage
      ↓
Research / Review
```

Each transition must be independently testable.

---

# 59. FAILURE & RECOVERY

V2 must safely handle:

- market-provider failure;
- stale market data;
- broker downtime;
- order rejection;
- partial fill;
- execution timeout;
- unknown execution state;
- provider mismatch;
- account synchronization failure;
- risk rejection;
- model failure;
- research-job failure;
- assistant failure.

Unknown execution state must never be represented as successful execution.

---

# 60. SECURITY ARCHITECTURE

V2 security shall include:

- authentication;
- RBAC;
- least privilege;
- service authorization;
- secret management;
- secure token handling;
- encryption where required;
- input validation;
- output sanitization;
- provider isolation;
- broker credential isolation;
- audit logging.

Broker credentials must never be exposed to frontend code.

They must also never be inserted into general-purpose assistant prompts or research artifacts.

---

# 61. OBSERVABILITY

V2 should expose:

- service health;
- market-feed health;
- provider status;
- broker status;
- execution gateway status;
- research-job status;
- model service state;
- queue state;
- market-data latency;
- execution latency;
- error rates.

Operational health is not equivalent to domain truth.

---

# 62. TESTING MODEL

V2 shall use multiple verification layers.

## Unit Testing

Individual functions, services, algorithms and components.

## Integration Testing

Service-to-service workflows.

## Provider Contract Testing

Market-data and broker adapter contracts.

## Simulation Testing

Paper execution and historical replay.

## Security Testing

Authentication, authorization, credential isolation and execution boundaries.

## Regression Testing

Existing V1 behavior.

## End-to-End Testing

Complete operator workflows.

---

# 63. V1 REGRESSION REQUIREMENT

V2 must preserve supported V1 functionality unless an explicit breaking change is approved.

Major V2 milestones should verify:

```text
V1 Regression Baseline
+
V2 New Capability Tests
=
Current Supported Test Baseline
```

---

# 64. GOVERNANCE V2

Governed domains include:

- data providers;
- models;
- strategies;
- scenarios;
- research jobs;
- accounts;
- brokers;
- orders;
- positions;
- execution;
- AI providers.

Important state distinctions remain:

```text
IMPLEMENTED
VERIFIED
APPROVED
AUTHORIZED
PRODUCTION CERTIFIED
```

V2 does not eliminate the V1 governance discipline.

It expands the domains to which that discipline applies.

---

# 65. V2 AUTHORITY SEPARATION

## Operator

Responsible for:

- product direction;
- capability authorization;
- repository/custody publication;
- major activation decisions;
- escalations.

## Development Authority

Responsible for:

- engineering design;
- implementation;
- testing;
- evidence;
- Delivery Reports.

## ITRGA

Responsible for:

- independent review;
- evidence assessment;
- governance findings;
- determinations;
- approvals/corrections according to the governing framework.

V2 does not change these authority boundaries.

---

# 66. V2 GOVERNANCE LIFECYCLE

Each major V2 capability should follow:

```text
Operator Direction
      ↓
Product / Architecture Definition
      ↓
DA Engineering Plan
      ↓
ITRGA Review
      ↓
Build Order
      ↓
DA Implementation
      ↓
Testing / Evidence
      ↓
Delivery Report
      ↓
ITRGA Review
      ↓
Approval / Correction
      ↓
Next Capability
```

No V2 capability should bypass this process because implementation appears straightforward.

---

# 67. V2 RISK THEMES

The programme must actively manage:

### Data Risk
Incorrect, stale, incomplete or inconsistent information.

### Model Risk
Poor prediction or misleading model interpretation.

### Execution Risk
Incorrect, duplicated, delayed or unintended execution.

### Broker Risk
Provider failure or inconsistent broker state.

### Security Risk
Credential compromise, privilege escalation or unauthorized execution.

### Reconciliation Risk
AXIOM state diverging from broker/provider state.

### Governance Risk
New capability introduced without authorization.

### Provider Risk
Dependence on external services.

### Product Complexity Risk
V2 becoming too large to verify coherently.

---

# 68. COMPLEXITY CONTROL

Every major subsystem should have:

- clear responsibility;
- owner;
- interface;
- test strategy;
- security classification;
- governance requirements;
- evidence requirements;
- failure handling;
- retirement/deprecation strategy.

V2 must not become an uncontrolled feature collection.

---

# 69. V2 EXPANSION FEATURES

The following are legitimate V2 expansion areas and are **not retroactive V1 requirements**:

- real/live market data;
- historical market datasets;
- external market-data providers;
- vendor adapters;
- account management;
- balances;
- margin;
- broker connectivity;
- exchange connectivity;
- order management;
- position management;
- paper trading;
- live execution;
- advanced portfolio management;
- advanced risk;
- backtesting;
- simulation/replay;
- research automation;
- scheduled research;
- governed scenario operations;
- governed artifact mutation;
- external AI provider adapters;
- advanced Chart Intelligence.

---

# 70. V2 BOUNDARIES

The existence of V2 does not automatically authorize:

- unrestricted autonomous trading;
- hidden broker access;
- arbitrary account mutation;
- uncontrolled AI actions;
- secret exposure;
- fabricated market/vendor data;
- fabricated performance;
- false certification;
- bypassing risk controls;
- bypassing authorization;
- bypassing audit.

V2 expands capability.

It does not remove governance.

---

# 71. V2 COMPLETION / END-TO-END VERIFICATION GATE

Before V2 can be considered complete, the programme must verify an end-to-end chain such as:

```text
Data Provider
      ↓
Market Data
      ↓
Market Structure
      ↓
Market Context
      ↓
Signal
      ↓
Research / Intelligence
      ↓
Risk
      ↓
Strategy / Simulation
      ↓
Paper Trading
      ↓
Execution Gateway
      ↓
Broker
      ↓
Order / Fill
      ↓
Position
      ↓
Portfolio
      ↓
Audit / Lineage
      ↓
Terminal
      ↓
Assistant
```

Both successful and failure paths must be verified.

---

# 72. V2 SUCCESS CRITERION

The strongest eventual V2 product test is not:

> "How many V2 phases were completed?"

It is:

> **Can an operator use AXIOM to observe a market, understand its structure, inspect intelligence and research, evaluate portfolio and risk conditions, test or simulate a strategy, operate a paper account, and—when explicitly authorized—execute and reconcile a real trade through a controlled broker pathway, while maintaining complete visibility into data source, uncertainty, risk, execution state, provenance and governance?**

If the answer is yes, V2 has achieved its product purpose.

---

# 73. STATUS OF THIS SPECIFICATION

This document is a **V2 Product & Architecture Specification**.

It establishes:

- product direction;
- capability scope;
- subsystem boundaries;
- architectural relationships;
- V1/V2 separation;
- data-provider strategy;
- execution architecture;
- paper-trading model;
- portfolio/account model;
- AI model;
- governance expectations.

It does not establish:

- Build Orders;
- implementation authorization;
- live-trading authorization;
- broker authorization;
- production certification.

---

# 74. REQUIRED NEXT GOVERNANCE ACTION

The Operator should now submit this specification to the ITRGA and DA.

## ITRGA Review

The ITRGA should independently determine:

- whether the V2 product definition is constitutionally coherent;
- whether any V2 capability conflicts with existing V1 governance;
- what additional security controls are required for execution;
- what governance controls are required for broker/account state;
- whether any existing governing documents require amendment;
- whether the specification is sufficient as the basis for DA design planning;
- whether the proposed V2 capability boundaries are complete.

## DA Review

The DA should assess:

- which V1 components can be reused;
- architecture boundaries;
- migration requirements;
- data/provider dependencies;
- broker/execution feasibility;
- paper-trading architecture;
- account/portfolio architecture;
- technical risks;
- security requirements;
- implementation feasibility;
- testing strategy;
- proposed technical decomposition.

Neither authority should interpret this specification as automatic implementation authorization.

---

# 75. FINAL V2 PRODUCT ARCHITECTURE

The intended long-term architecture is:

```text
                         AXIOM V2
                            │
     ┌──────────────────────┼──────────────────────┐
     │                      │                      │
 MARKET DATA          INTELLIGENCE             EXECUTION
     │                      │                      │
 Live                   Structure              Brokers
 Historical             Context                Exchanges
 Providers              Chart AI               Orders
 Vendors                Signals                Positions
 Ticks                  ML                     Accounts
 Depth                  Research               Fills
 Events                 Scenarios              Execution
     │                      │                      │
     └──────────────────────┼──────────────────────┘
                            │
                       PORTFOLIO
                            │
                          RISK
                            │
                     PAPER / SIMULATION
                            │
                      RESEARCH AUTOMATION
                            │
                    GOVERNED AI ASSISTANT
                            │
                       AXIOM TERMINAL
                            │
                      HUMAN OPERATOR
```

---

# 76. FINAL PRINCIPLE

> **AXIOM V2 expands capability without abandoning the engineering discipline established by AXIOM V1.**

The objective is not merely to add:

- brokers;
- orders;
- live data;
- paper trading;
- AI;
- portfolio management;
- execution.

The objective is to create one coherent institutional platform in which:

```text
Market
 ↓
Data
 ↓
Structure
 ↓
Context
 ↓
Intelligence
 ↓
Research
 ↓
Risk
 ↓
Simulation
 ↓
Paper Trading
 ↓
Execution
 ↓
Portfolio
 ↓
Evidence
 ↓
Governance
 ↓
Human Decision
```

form one traceable, secure and professionally usable system.

---

# 77. CLOSING STATEMENT

**AXIOM V1 established the foundation.**

**AXIOM V2 is the expansion.**

V2 should preserve everything that has already proven valuable while adding the capabilities required to transform AXIOM from an institutional research and decision-support workstation into a complete, governed trading and research platform.

The guiding principle remains:

> **Build capabilities. Connect them. Prove them. Govern them. Then expand.**

---

**AXIOM V2 — PRODUCT & ARCHITECTURE SPECIFICATION**

**Research-First · Explainable · Governed · Institutional · Human-Controlled · Extensible**
"""
print(content)
print("\n---END OF SPECIFICATION---")
cf = Path("/mnt/data/AXIOM_V2_PRODUCT_AND_ARCHITECTURE_SPECIFICATION.md")
cf.write_text(content, encoding="utf-8")
print(f"Created file: {cf}")