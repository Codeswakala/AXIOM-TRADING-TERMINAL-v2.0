# AXIOM — COMPLETE PLATFORM CAPABILITIES
## Institutional Trading, Research, Intelligence, Investigation, Risk & Governed Decision-Support Workstation

> **Purpose:** Complete capability catalogue for AXIOM based on the project's governing specifications, engineering records, UI workstreams, assistant design, research/investigation surfaces, and terminal-convergence direction.
>
> **Important status distinction:** A capability can be **DESIGNED**, **IMPLEMENTED**, **VERIFIED**, **APPROVED**, or **PRODUCTION CERTIFIED**. These states are different. This document describes the intended and evidenced capability set; it does not silently upgrade every capability to production certification.

---

# 1. Product Identity

AXIOM is an **institutional trading and research workstation** intended to unify:

- market and instrument information
- interactive charts
- technical analysis
- watchlists
- signals
- institutional intelligence
- research
- investigation
- scenario analysis
- portfolio and risk information
- alerts
- journals
- evidence and artifact lineage
- governance and audit visibility
- contextual AI-assisted research
- system and infrastructure status

AXIOM is intended to operate as **one coherent professional terminal**, rather than as a collection of unrelated dashboards and pages.

---

# 2. Core Operating Model

The intended workflow is:

```text
MARKET
   ↓
INSTRUMENT
   ↓
CHART
   ↓
ANALYSIS
   ↓
RESEARCH
   ↓
INTELLIGENCE
   ↓
INVESTIGATION
   ↓
RISK / PORTFOLIO
   ↓
DECISION SUPPORT
   ↓
GOVERNANCE / EVIDENCE
```

The operator remains the decision-maker.

AXIOM provides information, analysis, research, evidence, explanations, risk context, and governed decision support.

AXIOM is **not intended to become an autonomous trading actor**.

---

# 3. Professional Trading Terminal

## 3.1 Unified Terminal Shell

The terminal is intended to provide:

- persistent application identity
- global command/search
- workspace selection
- instrument selection
- timeframe controls
- alerts
- operator/session state
- connectivity state
- governance state
- persistent market context

The terminal architecture is intended to replace page-oriented navigation with a unified workspace.

## 3.2 Market Navigator / Watchlists

Capabilities include:

- instrument lists
- watchlists
- grouped watchlists
- symbol discovery
- market selection
- sorting/filtering
- quick instrument selection

Rows may show:

- symbol
- current price
- percentage change
- spread
- market/data state
- volatility/state indicators where available

## 3.3 Instrument Workspace

The selected instrument becomes the central context of the workspace.

The instrument header may expose:

- symbol
- full instrument name
- asset class
- current price
- percentage change
- bid/ask where available
- spread
- session
- data state

The selected instrument should remain available while the operator moves through related analysis, research, intelligence, and risk surfaces.

---

# 4. Market Data

AXIOM is designed to consume market information through its market/data infrastructure.

Capabilities include:

- instrument data
- historical market information
- live/streamed market information where configured
- market status
- session state
- connectivity state
- market monitoring
- data availability states

The platform includes live-market/WebSocket infrastructure and related client hooks/components.

### Data integrity requirements

AXIOM must distinguish between:

- live data
- simulated data
- stale data
- unavailable data
- disconnected state
- empty state
- loading state
- error state

AXIOM must never present fabricated market information as genuine market information.

---

# 5. Interactive Charting

Charting is a first-class AXIOM capability.

The platform includes Lightweight Charts infrastructure and a dedicated chart-stage architecture.

Capabilities include:

- price charts
- candlestick visualization
- timeframes
- zoom
- pan
- crosshair
- technical indicators
- analytical overlays
- market/price levels
- signal markers
- research markers
- contextual annotations

The chart is intended to be the main visual analysis surface of the terminal.

---

# 6. Technical Analysis

AXIOM is designed to support technical-analysis workflows through chart and analytical surfaces.

Potential analytical instruments include:

- EMA
- SMA
- RSI
- MACD
- Bollinger Bands
- ATR
- volume
- pivot points
- market structure
- support/resistance
- other registered indicators where supported

Technical analysis is decision-support context, not a guarantee of future outcomes.

---

# 7. Signals

AXIOM includes signal-oriented analytical capabilities.

Capabilities include:

- signal discovery
- signal context
- signal drill-down
- signal investigation
- signal-related metrics
- signal-related research
- signal-to-evidence relationships

A signal is not itself an execution instruction.

---

# 8. Market Intelligence

AXIOM includes an institutional intelligence layer intended to provide higher-level analytical context.

Capabilities include:

- market-regime information
- correlation information
- scenario analysis
- intelligence summaries
- analytical explanations
- confidence/uncertainty information
- model-related information
- calibration-related information
- research intelligence
- contextual intelligence

---

# 9. Research Management

Research is a major AXIOM capability.

The system supports a structured research environment containing institutional research artifacts and reports.

Capabilities include:

- research discovery
- research cataloguing
- metadata
- artifact lookup
- filtering
- lineage
- relationships
- collection organization
- tag organization
- report inspection
- evidence review
- research status
- research limitations
- uncertainty information
- artifact provenance

---

# 10. Research Artifact Explorer

The research environment includes an explorer-oriented capability for institutional artifacts.

Capabilities include:

- discovery
- catalog
- metadata
- lineage
- filtering
- relationship inspection
- organized artifact collections
- tag-based organization
- research artifact references

This allows research to function as a structured knowledge/evidence environment rather than a folder of documents.

---

# 11. Investigation

AXIOM includes an investigation workflow.

A representative investigation path is:

```text
Instrument
   ↓
Signal
   ↓
Market Context
   ↓
Research
   ↓
Evidence
   ↓
Intelligence
   ↓
Scenario
```

Capabilities include:

- signal investigation
- contextual analysis
- evidence inspection
- related research discovery
- artifact relationships
- intelligence drill-down
- scenario examination

---

# 12. Scenario Analysis

AXIOM includes scenario-oriented research capabilities.

Capabilities include:

- scenario reports
- scenario comparison
- scenario metadata
- uncertainty
- limitations
- economic usefulness/context
- research status
- scenario relationships

Scenarios are research/analysis tools and must not be presented as guaranteed outcomes.

---

# 13. Portfolio Analytics

AXIOM is designed to provide portfolio/account analytical visibility where supported.

Capabilities include:

- portfolio overview
- positions
- exposure
- allocation
- performance information
- risk context
- historical order information where available
- account/portfolio state

This is decision-support functionality, not automatic order execution.

---

# 14. Risk Management

AXIOM provides risk-oriented decision support.

Capabilities include:

- portfolio risk
- exposure
- concentration
- drawdown context
- risk metrics
- scenario risk
- alerts
- risk-related intelligence
- model uncertainty
- research limitations

---

# 15. Alerts & Monitoring

AXIOM supports alert and monitoring concepts across market, intelligence, risk, and infrastructure domains.

Capabilities include:

- market alerts
- signal alerts
- risk alerts
- research/analysis alerts where implemented
- system monitoring
- connection monitoring
- data-state monitoring
- application activity monitoring

Alerts inform the operator; they do not silently execute restricted actions.

---

# 16. Journal / Operator Research Record

AXIOM includes an institutional journal/research record concept.

Capabilities include:

- research notes
- planning notes in the governed research context
- analytical observations
- scenario notes
- investigation notes
- operator reflections
- research history

The journal is an information and reasoning aid, not an autonomous strategy-execution mechanism.

---

# 17. Artifact Lineage & Evidence

AXIOM treats evidence lineage as a first-class capability.

Capabilities include:

- artifact identity
- artifact relationships
- provenance
- lineage
- audit records
- hash-based evidence relationships where applicable
- research/source context
- disclosure of limitations
- evidence inspection

The goal is to let an operator and reviewer answer:

> **Where did this information come from, what supports it, and what are its limitations?**

---

# 18. Governance & Audit

Governance is embedded into the product.

Capabilities include:

- governance state
- audit exploration
- refusal records
- evidence display
- constitutional disclosures
- technical debt visibility
- risk register visibility
- governance findings
- review/verification context
- system posture

The platform is designed so governance information can be visible within the terminal rather than living entirely outside the product.

---

# 19. Security & Access Control

AXIOM includes institutional security capabilities such as:

- authentication
- authorization
- RBAC
- protected routes
- 401/unauthorized handling
- secure token handling
- restricted state handling
- safe error presentation
- input sanitization
- secret protection
- controlled data exposure

The system must never expose credentials, tokens, database secrets, or protected information.

---

# 20. Governed AI Assistant

AXIOM includes a contextual assistant capability.

The assistant is a **research and explanation component**, not the core identity of the product.

Capabilities include:

- grounded research responses
- research explanation
- indicator explanation
- chart-context explanation
- research summarization
- evidence summarization
- limitation explanation
- related artifact discovery
- governance/documentation lookup where implemented
- refusal handling
- uncertainty disclosure
- audit presentation

---

# 21. AI Refusal System

Recorded refusal classes include:

- `ORDER_INSTRUCTION_REFUSED`
- `GATE_OPEN_INSTRUCTION_REFUSED`
- `SECRET_EXFILTRATION_REFUSED`
- `UNBOUNDED_TOOL_REQUEST_REFUSED`
- `GROUNDING_REQUIRED`
- `ASSISTANT_DISABLED`

The assistant is designed to constrain requests that violate:

- no-actuation boundaries
- governance boundaries
- security/secrecy boundaries
- grounding requirements
- controlled operational boundaries

---

# 22. AI Disclosure & Uncertainty

Assistant and intelligence surfaces communicate:

- uncertainty
- limitations
- scope
- refusal state
- advisory boundary
- research-only posture

The documented assistant disclaimer is:

> **"AI-generated research assistance only. Not financial advice, not an instruction, may be wrong. Operator judgment required. AXIOM does not act."**

Status and disclosure are intended to be carried in text, not by color alone.

---

# 23. AI Auditability

The assistant is designed around an auditable, read-only model.

Capabilities include:

- assistant response records
- refusal records
- audit events
- persisted/hash-based lineage
- refusal persistence
- refusal auditing
- review surfaces
- disclosure register
- refusal taxonomy

The UI displays governed records; it is not intended to silently create unsupported histories.

---

# 24. AI API Seams

The documented UI-008 assistant integration includes authenticated read-only API seams such as:

- `GET /api/v1/collaboration/assistant-responses`
- `GET /api/v1/collaboration/assistant-responses/{response_id}`

Documented properties include:

- authentication
- 401 handling
- read-only behavior
- no action/emission verbs

---

# 25. AI Boundaries

The AXIOM assistant is explicitly:

### NOT an external LLM integration

External LLM providers are not part of the current governed design.

### NOT an autonomous actor

It cannot:

- place orders
- open gates
- execute tools
- mutate state

### NOT a writer of platform state

The assistant surfaces read-only persisted lineage.

### NOT financial advice

The interface maintains the research/advisory boundary.

### NOT an independent governance authority

It does not approve builds, open gates, or certify production.

---

# 26. Non-Actuation

Unless separately authorized by an explicit future governing instrument, AXIOM must not provide:

- autonomous Buy
- autonomous Sell
- automated order placement
- autonomous trade execution
- gate-opening actions
- execution triggers
- broker mutation
- unauthorized account mutation

AXIOM may represent:

- positions
- historical orders
- account state
- portfolio information
- risk
- trading concepts
- simulated state

without becoming an execution engine.

---

# 27. Command Palette & Operator Productivity

AXIOM includes command-oriented navigation and operator productivity infrastructure.

Capabilities include:

- global command palette
- quick actions
- workspace navigation
- assistant-surface navigation
- research navigation
- intelligence navigation
- governance navigation
- documentation lookup
- contextual shortcuts
- keyboard-oriented operator workflows

The command system is intended to make a dense terminal fast to operate.

---

# 28. Workspace / Layout System

AXIOM is intended to support multiple terminal workspaces and compositional layouts.

Possible workspace concepts include:

### Trading Workspace

Watchlist + Chart + Signals + Context + Positions

### Research Workspace

Watchlist + Chart + Research + Intelligence + Evidence

### Risk Workspace

Portfolio + Exposure + Risk + Alerts + Positions

### Investigation Workspace

Instrument + Chart + Research + Evidence + Intelligence

### Intelligence Workspace

Market + Chart + Intelligence + Assistant + Research

The exact final layout is governed by the active terminal design and implementation.

---

# 29. Contextual Docking

AXIOM uses a dock-oriented terminal model.

The convergence architecture has been organized around concepts such as:

- dock tabs
- overlays
- stage views
- signal drill-down
- contextual panels

The purpose is to keep multiple capabilities accessible without repeatedly leaving the active terminal.

---

# 30. Global / Terminal Status

The terminal can communicate operational state such as:

- API state
- database state
- WebSocket state
- market-data connectivity
- system health
- environment
- operator/session state
- governance gate
- research-only state

Infrastructure telemetry should remain subordinate to the market workspace.

---

# 31. Data-State Handling

AXIOM should communicate explicit states for data-driven surfaces:

1. Loading
2. Ready
3. Empty
4. Stale
5. Disconnected
6. Unauthorized
7. Error
8. Restricted
9. Research-only
10. Degraded

The UI must not fabricate results when a dataset is unavailable.

---

# 32. Accessibility

AXIOM is intended to provide institutional accessibility, including:

- keyboard navigation
- focus management
- semantic structure
- ARIA support
- state announcements
- readable contrast
- accessible command interactions
- accessible critical workflows
- accessibility-conscious data presentation

---

# 33. Performance

The terminal is intended to support professional interaction.

Performance concerns include:

- fast workspace switching
- responsive command palette interaction
- responsive instrument selection
- chart rendering
- live-data updates
- panel rendering
- controlled layout shifts
- measurable interaction-latency targets

Performance claims must be established by evidence.

---

# 34. Design System

AXIOM has an institutional visual/design system with:

- dark-first terminal presentation
- semantic color tokens
- typography hierarchy
- UI design tokens
- reusable component patterns
- institutional branding
- state semantics

Existing token infrastructure includes `--ix-*` design tokens.

---

# 35. Market + Research Convergence

A major AXIOM capability is that market information does not remain isolated from research.

The intended workflow allows:

```text
Instrument
   ↓
Chart
   ↓
Signal
   ↓
Research
   ↓
Artifact
   ↓
Intelligence
   ↓
Investigation
```

This makes AXIOM an institutional research trading terminal rather than simply a charting application.

---

# 36. Market + Risk Convergence

The same instrument context can connect to:

- portfolio
- positions
- exposure
- risk
- scenario analysis
- alerts
- research

Analysis therefore remains contextual rather than page-specific.

---

# 37. Intelligence + Governance Convergence

AXIOM is designed to connect intelligence outputs to:

- evidence
- provenance
- uncertainty
- disclosures
- audit
- governance

The product aims to answer:

> **What does the system indicate, why does it say that, how certain is it, what evidence supports it, and what restrictions apply?**

---

# 38. Operator Workflow

A representative AXIOM workflow is:

```text
Select instrument
      ↓
Inspect market state
      ↓
Open chart
      ↓
Analyze technical context
      ↓
Inspect signals
      ↓
Review intelligence
      ↓
Open research
      ↓
Inspect evidence/artifacts
      ↓
Investigate scenarios
      ↓
Review risk / portfolio context
      ↓
Use contextual assistant for explanation
      ↓
Make an informed human decision
```

AXIOM supports the workflow.

The human operator remains responsible for the final decision.

---

# 39. Governance Protections

AXIOM's governance model exists to protect against:

- undocumented behavior
- constitutional violations
- architectural drift
- security regression
- repository/provenance degradation
- governance inconsistency
- unsupported certification

These are part of the platform's institutional reliability model.

---

# 40. Engineering & Operational Infrastructure

The platform includes supporting engineering capabilities such as:

- backend services
- API routing
- database persistence
- migrations
- frontend application architecture
- test suites
- static/type checking
- build tooling
- runtime health
- live-market/WebSocket infrastructure
- authentication/authorization
- reusable UI components

These form the infrastructure beneath the terminal experience.

---

# 41. Research-Only Platform Posture

The governed platform posture is:

```text
GOVERNANCE GATE: CLOSED
PRODUCTION: NOT CERTIFIED
RESEARCH-ONLY
NON-ACTUATING
```

The project deliberately separates:

- implementation complete
- phase approved
- workstream complete
- production certified

Passing tests alone does not imply production certification.

---

# 42. Complete High-Level Capability Map

```text
                         AXIOM
                INSTITUTIONAL TERMINAL
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
     MARKETS            ANALYSIS          INTELLIGENCE
        │                   │                   │
   Watchlists            Charts             Signals
   Instruments           Indicators         Research
   Market Data           Scenarios           Explanations
   Market Status         Overlays            Uncertainty
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                      INVESTIGATION
                            │
                    EVIDENCE / LINEAGE
                            │
                      PORTFOLIO / RISK
                            │
                        GOVERNANCE
                            │
                       CONTEXTUAL AI
                            │
                       HUMAN DECISION
```

---

# 43. What AXIOM Can Do at Intended Full Capability

At intended full capability, AXIOM should allow an operator to:

## Monitor markets

- watch instruments
- inspect prices
- monitor market data
- observe market/session state

## Analyze markets

- chart instruments
- use timeframes
- use technical indicators
- inspect signals
- investigate market structure

## Research

- discover artifacts
- inspect reports
- organize collections
- tag artifacts
- inspect metadata
- trace lineage
- review evidence

## Investigate

- drill into signals
- compare scenarios
- relate signals to research
- connect intelligence to evidence
- inspect limitations and uncertainty

## Evaluate portfolio/risk

- inspect positions
- review exposure
- examine risk
- compare scenarios
- monitor alerts

## Use intelligence

- inspect model/intelligence outputs
- understand uncertainty
- review explanations
- compare analytical context

## Use the assistant

- ask grounded research questions
- explain analytical outputs
- summarize evidence
- inspect related research
- receive constitutional refusals where required

## Maintain institutional traceability

- inspect audit events
- inspect refusal records
- inspect artifact lineage
- understand governance posture
- see system state

## Operate efficiently

- use command palette
- search instruments
- switch workspaces
- use docked/contextual surfaces
- navigate through a unified terminal

---

# 44. What AXIOM Explicitly Does Not Do

AXIOM is not intended to:

- autonomously trade
- provide hidden execution pathways
- open governance gates
- certify itself
- present fabricated market data
- hide uncertainty
- expose secrets
- silently use external AI providers
- silently mutate governed platform state
- act as a financial-advice engine
- replace the human operator

---

# 45. Capability Maturity Model

Every capability should ultimately be evaluated using:

| State | Meaning |
|---|---|
| **DESIGNED** | Capability is specified in governing/design material |
| **IMPLEMENTED** | Code exists and provides the capability in the development workspace |
| **VERIFIED** | Independent evidence demonstrates the capability |
| **APPROVED** | ITRGA has issued the relevant phase/workstream determination |
| **PRODUCTION CERTIFIED** | Capability and platform have passed the separate production-certification process |

A capability must not be described as production-ready solely because it is designed or implemented.

---

# 46. Full Product Vision

The complete AXIOM vision is:

```text
                 AXIOM
       INSTITUTIONAL TERMINAL
                  │
    ┌─────────────┼─────────────┐
    │             │             │
  MARKETS      ANALYSIS    INTELLIGENCE
    │             │             │
 Watchlists    Charts        Signals
 Instruments   Indicators    Research
 Market Data   Scenarios     Explanations
    │             │             │
    └─────────────┼─────────────┘
                  │
             INVESTIGATION
                  │
           EVIDENCE / LINEAGE
                  │
            PORTFOLIO / RISK
                  │
              GOVERNANCE
                  │
             CONTEXTUAL AI
                  │
             HUMAN DECISION
```

The final product is not simply:

- a charting tool;
- a research database;
- an AI assistant;
- a governance console;
- or a dashboard.

It is intended to combine these capabilities into **one governed institutional trading and research workstation**.

---

# 47. Current-Evidence Qualification

This file is a **capability showcase and product reference**.

It must not be interpreted as claiming that every listed feature is currently:

- fully implemented;
- integrated into the latest terminal build;
- independently verified;
- phase-approved;
- or production-certified.

The project records contain evidence limitations, phase-specific holds, implementation-vs-repository distinctions, and historical custody issues.

For example, a recorded UI-CONV-P03 determination stated that the work was **approved in substance but not landed**: the review could establish that the work was correct but could not establish that the platform repository contained it.

That distinction is fundamental to evaluating AXIOM honestly.

---

# 48. The Correct Launch Test

The strongest eventual launch test is not:

> "How many UI phases did AXIOM complete?"

It is:

> **Can an operator open AXIOM, select an instrument, understand the market, inspect the chart, investigate signals, review intelligence and research, inspect evidence and risk, use the governed assistant for explanation, and retain complete awareness of uncertainty, provenance, governance, and non-actuation boundaries without leaving the terminal?**

If yes, AXIOM has become the product it was intended to be.

If some links remain disconnected, those are the remaining product gaps.

---

# 49. Final Capability Statement

> **AXIOM is an institutional trading and research terminal that unifies market observation, instrument analysis, interactive charting, technical studies, signals, institutional intelligence, research management, investigation, scenario analysis, portfolio and risk context, alerts, journaling, artifact/evidence lineage, governance and audit visibility, and a governed contextual research assistant into one professional workstation—while preserving human decision-making, research-only boundaries, security, provenance, explainability, and non-actuation controls.**

---

## AXIOM

**Research-First · Explainable · Governed · Human-in-the-Loop · Non-Actuating**
