# AXIOM System Architecture

| Item | Value |
|------|--------|
| Document Title | AXIOM System Architecture |
| Canonical Filename | `SYSTEM_ARCHITECTURE.md` |
| Version | 1.1.0 |
| Status | **ACTIVE — CANONICAL** |
| Classification | Core Technical Architecture (Governing Document) |
| Authority | Project Governance / Operator-approved merge |
| Supersedes | `05_SYSTEM_ARCHITECTURE.md` (v1.0), `06_SYSTEM_ARCHITECTURE.md` (v1.0) |
| Merge Date | 2026-07-10 |
| Merge Authorization | Operator directive to Development Authority |
| Parent Documents | `03_AXIOM_SPEC.md`, `00_VISION_AND_PRINCIPLES.md`, `04_PROJECT_ROADMAP.md` |

---

# Purpose

This document is the **single canonical technical architecture** for AXIOM.

It specifies:

- overall system architecture and topology
- primary logical layers
- core capability subsystems
- technology stack
- service boundaries
- communication and event patterns
- data flow and storage
- machine learning architecture
- broker integration
- security, observability, scalability
- deployment philosophy
- extension strategy
- architectural constraints

Implementation details belong to individual development units.

**No implementation may violate this architecture unless formally approved by governance.**

---

# Document Control & Supersession

This file is the sole active System Architecture governing document.

| Prior Document | Role | Status After Merge |
|----------------|------|--------------------|
| `05_SYSTEM_ARCHITECTURE.md` | Layered / capability-subsystem view | **SUPERSEDED** — content absorbed |
| `06_SYSTEM_ARCHITECTURE.md` | Stack / technology / event view | **SUPERSEDED** — content absorbed |

Historical copies may be retained for audit. They shall not be cited as active architecture authority.

If a future `SYSTEM_ARCHITECTURE.md` (or successor architecture document of the same domain family) is provided and the Development Authority is explicitly notified of the update, that newer document supersedes this one within the architecture domain. See `DOCUMENT_PRECEDENCE.md`.

---

# Architectural Vision

AXIOM is designed as a modular institutional-grade quantitative research and trading intelligence platform.

The architecture emphasizes:

- scalability
- maintainability
- testability
- modularity
- separation of concerns
- replaceable components
- observability
- reproducibility
- governance
- professional software engineering

over development speed.

The platform shall evolve without requiring architectural redesign.

---

# Architectural Philosophy

AXIOM follows an institutional layered architecture.

- Every subsystem has a clearly defined responsibility.
- Subsystems communicate through well-defined interfaces.
- No hidden coupling is permitted.
- Every layer must be independently testable.
- Business logic shall never reside inside API controllers.
- ML research is separated from execution.
- Governance is independent of every other subsystem.
- The architecture remains market-agnostic and deployment-independent.

---

# Two Complementary Views (Unified)

This document presents **one architecture** through two complementary views:

| View | Purpose |
|------|---------|
| **Logical Layers** | Vertical stack of concerns (how responsibility is ordered) |
| **Capability Subsystems** | Product/engineering domains (what is built and owned) |

Implementation topology (technology stack) maps onto both views. Neither view is optional; both are normative.

---

# Part A — Logical Layers

AXIOM consists of **eight primary logical layers**:

```
Operator Interface
        ↓
Application Layer
        ↓
API Layer
        ↓
Business Services
        ↓
AI & Quantitative Engine
        ↓
Data Layer
        ↓
External Integrations
        ↓
Infrastructure Layer
```

Each layer communicates through well-defined interfaces.

No layer may bypass another layer without explicit architectural justification.

---

# Part B — Capability Subsystems

The platform is divided into **eight independent capability subsystems**.

These are the primary ownership and delivery boundaries for engineering.

## 1. Frontend Terminal (Presentation)

**Purpose:** Complete operator experience; institutional trading research workstation.

**Contains:**

- Trading terminal
- TradingView chart workspace
- Analytics dashboards
- Research workspace
- Portfolio view
- Signal visualization and explorer
- Model diagnostics
- Strategy laboratory
- Operator settings
- Notification center
- Governance views
- Future AI collaboration workspace

**Technology:**

- React
- TypeScript
- Tailwind
- TradingView Lightweight Charts
- WebSocket client

**Computation boundary (normative):**

- The presentation layer performs **display, layout, interaction, and rendering transforms only**.
- Domain calculations, ML inference, risk math, feature engineering, and signal generation **shall not** execute in the browser as authoritative logic.
- Client-side chart math required for rendering (scales, pixel mapping, drawing handles, UI-only indicators for display) is permitted.
- Authoritative analytical results always originate from backend services.

**Major frontend modules:**

- Dashboard
- Chart Workspace
- Research Workspace
- Market Explorer
- Portfolio
- Signal Center
- Operator Settings
- Notification Center
- Governance Dashboard

Every UI component shall be reusable.

---

## 2. Backend API (Application / API)

**Purpose:** Coordinates communication between UI and backend; exposes the platform contract.

**Responsibilities:**

- REST API
- WebSocket endpoints
- Authentication
- Authorization
- Session management
- Request validation
- Rate limiting
- Request orchestration
- Chart synchronization coordination
- Live updates
- Health monitoring
- API documentation (OpenAPI)

**Technology:**

- FastAPI
- Pydantic
- WebSockets
- Dependency Injection

---

## 3. Business Services

**Purpose:** Domain application services; each service owns a single responsibility.

**Services include (non-exhaustive):**

| Service | Domain |
|---------|--------|
| SignalService | Signal lifecycle and presentation contracts |
| MarketService | Market metadata, watchlists, market state |
| AnalyticsService | Performance and analytical aggregates |
| GovernanceService | Governance operations surface |
| PerformanceService | Outcome and KPI tracking |
| NotificationService | Operator notifications |
| ConfigurationService | Runtime and operator configuration |
| AuditService | Audit event recording interfaces |
| RiskService | Risk evaluation (research/advisory scope) |
| ResearchService | Research workflow orchestration |
| PredictionService | Inference request orchestration |
| FeatureService | Feature retrieval interfaces |
| ExperimentService | Experiment metadata access |
| CalibrationService | Calibration result access |
| ChartService | Chart annotation / overlay contracts |
| BrokerService | Broker abstraction access |

Business logic lives in services and domain modules — never in API controllers alone.

---

## 4. Machine Learning Platform

**Purpose:** Research market behaviour. **Never executes trades.**

**Responsibilities:**

- Dataset management
- Feature engineering coordination (with Feature Engineering capability)
- Feature store
- Training pipeline
- Inference engine
- Model registry and versioning
- Evaluation
- Cross-market benchmarking
- Generalization analysis
- Continuous retraining (evidence-driven)
- Drift monitoring
- Economic viability assessment
- Probability calibration
- Confidence estimation
- Regime detection support
- Research notebook support

**ML module flow:**

```
Dataset Manager
      ↓
Feature Pipeline
      ↓
Feature Store
      ↓
Training Engine
      ↓
Validation Engine
      ↓
Model Registry
      ↓
Inference Engine
      ↓
Monitoring
      ↓
Performance Analytics
```

**Submodules:**

- Dataset Manager
- Training Engine
- Validation Engine
- Calibration Engine
- Experiment Registry
- Artifact Registry
- Model Registry
- Feature Registry
- Prediction Engine
- Research Notebook Support

The same architecture supports all supported markets.

---

## 5. Market Intelligence Layer

**Purpose:** Live and research-time market understanding beyond raw ticks.

**Responsibilities:**

- Live market monitoring
- Market regimes
- Cross-market relationships
- Correlation analysis
- Volatility analysis
- Trend detection
- Liquidity analysis
- Macro intelligence (roadmap-dependent)
- Professional signal validation support (future waves)

Market Intelligence consumes Market Data and ML outputs; it does not replace the ML training pipeline.

---

## 6. Chart Intelligence Layer

**Purpose:** Charts as intelligent collaborative workspaces.

**Responsibilities:**

- TradingView integration
- Drawing tools
- AI annotations (future waves)
- Probability overlays
- Support and resistance visualization
- Market structure visualization
- Liquidity zones
- Trade planning overlays
- Future collaborative AI drawing

**Chart capabilities:**

- TradingView rendering
- Multi-timeframe synchronization
- Drawing tools
- Custom overlays
- Prediction visualization
- Market sessions
- Heatmaps (roadmap-dependent)
- Future ML annotations / AI drawings / strategy replay

Charts are first-class citizens. AI-generated drawings shall remain editable, reversible, and visually distinguishable from operator drawings.

---

## 7. Broker Integration Layer

**Purpose:** Communicate with trading platforms and market data sources related to broker connectivity.

**Supported platforms:**

- MT5 (primary)
- Future FIX
- Future cTrader
- Future Interactive Brokers
- Future REST brokers

**Responsibilities:**

- MT5 bridge
- Broker abstraction
- Market data (broker-sourced)
- Account data
- Positions and orders (when authorized)
- Execution monitoring
- Chart synchronization support
- Trade history
- Execution research
- Paper trading interfaces
- Future execution interfaces

**Constraints:**

- Broker-specific logic shall remain isolated behind abstractions.
- This layer **never decides trades**.
- It only performs **approved** actions.
- Live automated execution requires explicit future governance authorization (see Roadmap Wave 6 and Vision).
- “Optional broker execution” in signal lifecycle means **human-approved, paper, simulation, or governance-authorized** paths only — never silent auto-execution.

---

## 8. Governance Layer

**Purpose:** Institutional oversight, independent of product features.

**Modules:**

- Audit Logs
- Experiment Registry
- Decision Registry
- Version Registry
- Model Registry (governance view)
- Approval Registry
- Risk Registry
- Build Registry
- Review Registry
- Kill Switch
- Compliance
- Documentation synchronization hooks
- Project governance records

Governance is independent from every other subsystem.

---

# Part C — Implementation Topology (Technology Stack)

```
┌─────────────────────────────────┐
│        Operator Terminal        │
└───────────────┬─────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│   React Trading Terminal        │
│   TradingView Interface         │
│   MT5-style Workspace           │
└───────────────┬─────────────────┘
                │
         REST / WebSocket
                │
                ▼
┌─────────────────────────────────┐
│        FastAPI Backend          │
└───────────────┬─────────────────┘
                │
        ┌───────┴────────┐
        ▼                ▼
   ML Engine       Market Services
        │                │
        ▼                ▼
 Feature Engine    Broker Gateway
        │                │
        ▼                ▼
    Database      Live Market Streams
```

### Backend internal layering

```
API
  ↓
Application Services
  ↓
Domain Logic
  ↓
Repositories
  ↓
Database
```

---

# Market Data Layer (Cross-Cutting Data Concern)

**Purpose:** Collect and normalize data from multiple providers.

**Supported sources:**

- MT5
- Broker APIs
- CSV
- Historical datasets
- Future institutional feeds

**Responsibilities:**

- Tick collection
- OHLC aggregation
- Market normalization
- Timestamp validation
- Quality checks
- Missing data detection

**Supported markets (union set):**

- Forex
- Cryptocurrency
- Indices
- Metals / Precious Metals
- Commodities
- Equities / Stocks
- Exchange-Traded Funds (ETFs)
- Futures
- Synthetic Markets (where supported)

The architecture intentionally avoids dependence on a single market or instrument.

---

# Feature Engineering (Capability within ML Platform)

**Purpose:** Transform raw market data into robust machine learning features.

**Responsibilities:**

- Feature generation
- Normalization
- Lag creation
- Volatility / trend / session / market-structure features
- Future alternative data features

**Output:** Feature matrix / feature store records.

**Constraint:** No model training occurs inside pure feature generation modules.

---

# Multi-Market Framework

The ML and data architecture is market-agnostic.

- New instruments should require **configuration**, not architectural redesign.
- Markets may be isolated during training.
- Models are benchmarked across markets.
- Cross-market statistics are stored independently.

**Supported model strategies:**

- Single-market models
- Multi-market models
- Foundation-style models
- Transfer learning
- Zero-shot evaluation
- Market adaptation

---

# Data Pipeline

```
Raw / Historical Market Data
        ↓
Cleaning
        ↓
Normalization
        ↓
Validation
        ↓
Feature Engineering
        ↓
Feature Store
        ↓
Training / Validation / Test Datasets
        ↓
Model Training
        ↓
Calibration
        ↓
Evaluation
        ↓
Model Registry
        ↓
Live Inference
        ↓
Performance Tracking
        ↓
Continuous Monitoring
        ↓
Evidence-driven Retraining
```

---

# Feature Store

The feature store is the canonical repository for engineered features.

**Responsibilities:**

- Feature versioning
- Dataset versioning
- Cross-market compatibility
- Feature reproducibility
- Metadata
- Feature lineage
- Quality control

No duplicate conflicting feature definitions shall exist as competing sources of truth.

---

# Model Registry

Every trained model receives:

- unique identifier
- version
- training dataset(s)
- feature version
- hyperparameters (where applicable)
- evaluation metrics
- creation timestamp
- supported markets
- deployment status
- approval history
- rollback version

**No model may be deployed without registration.**

---

# Live Inference Pipeline

```
Market Data
      ↓
Feature Extraction
      ↓
Model Inference
      ↓
Confidence Estimation
      ↓
Validation Rules
      ↓
Operator Signal
      ↓
Analytics
      ↓
Governance Logging
```

---

# Signal Lifecycle

```
Market Update / Signal Generated
      ↓
Prediction + Confidence
      ↓
Risk Evaluation
      ↓
Governance Checks
      ↓
Displayed to Operator
      ↓
Human Decision
      ↓
Optional Broker Path
  (paper / simulation / human-approved /
   governance-authorized only)
      ↓
Logging
      ↓
Outcome Tracking
      ↓
Performance Evaluation
      ↓
Historical Archive
      ↓
Future Retraining Inputs
```

Every signal remains fully traceable.

---

# Event Architecture

AXIOM is event-driven where beneficial.

**Example flow:**

```
Market Tick Received
      ↓
Feature Update
      ↓
Prediction Generated
      ↓
Signal Logged
      ↓
Analytics Updated
      ↓
Dashboard Refreshed
      ↓
Audit Recorded
```

Events are immutable once recorded.

---

# Communication Patterns

Preferred communication:

- REST APIs
- WebSockets (live updates)
- Event bus
- Internal service interfaces
- Asynchronous event queue

Services remain loosely coupled.

---

# Database Architecture

**Primary database:** PostgreSQL

**Core domains / table families:**

- Market Data (ticks, candles)
- Features
- Predictions
- Signals
- Trade Ideas
- Model Artifacts
- Experiments
- Approvals
- Reviews
- Audit Events
- Users
- Accounts
- Configurations
- Performance Metrics

**Logical data domains:**

- Market Data
- Research Data
- Models
- Signals
- Operator Data
- Configurations
- Audit Logs
- Performance Metrics
- System Logs
- Historical Archives

Future large analytical datasets may use **Parquet** (or equivalent columnar object storage) for efficient ML pipelines while metadata remains in PostgreSQL.

---

# Security Architecture

Security is part of the architecture, not an afterthought.

**Controls include:**

- Authentication (JWT)
- Role-based access
- Authorization
- Credential isolation
- Encrypted secrets
- Broker isolation
- Immutable audit logs
- Signed model artifacts (as implemented)
- Configuration validation
- Input validation
- Rate limiting
- Least privilege

**Hard rules:**

- No credentials in source code.
- No secrets committed to the repository.

**Future (reserved):**

- Hardware security modules
- Multi-factor authentication
- Institutional identity providers

---

# Configuration Management

Environment-specific configuration remains external:

- Development
- Testing
- Staging
- Production

Each environment remains independently configurable.

---

# Observability

Every subsystem shall expose, as maturity allows:

- Structured logs
- Metrics
- Health checks
- Latency
- Error rates
- Prediction statistics
- Cache statistics
- Resource utilization
- ML monitoring
- Signal monitoring
- Drift monitoring
- Operator diagnostics

**Future:**

- Distributed tracing
- OpenTelemetry
- Grafana dashboards

Logging categories (aligned with DA Manual) include: SYSTEM, API, DATABASE, ML, MARKET, BROKER, SECURITY, GOVERNANCE, AUDIT.

Logs shall never expose confidential credentials or sensitive operator secrets.

---

# Scalability Strategy

The architecture supports horizontal growth and does **not** assume single-machine deployment.

**Includes:**

- Horizontal API scaling
- Background workers
- Feature caching
- Prediction caching
- Database indexing
- Object storage
- Stream processing
- GPU inference (where justified)
- Distributed training (where justified)
- Additional brokers, markets, models, research modules
- Cloud and hybrid deployment
- Plugin ecosystem (later waves)

---

# Deployment Model

Supported environments:

- Local development
- Research workstation
- Dedicated server
- Cloud deployment
- Hybrid deployment

Architecture remains deployment-independent.

---

# Testing Strategy

Testing exists at multiple layers. No subsystem is exempt.

- Unit Testing
- Integration Testing
- End-to-End Testing
- Regression Testing
- Performance Testing
- Security Testing
- User Acceptance Testing
- Machine Learning Validation (per ML_SPEC)

---

# Extension Strategy

Future modules plug into defined interfaces without redesign.

**Examples:**

- Professional Signal Validation
- AI Chart Collaboration
- Portfolio Intelligence / Optimizer
- News Intelligence
- Economic Calendar
- Macro Engine
- Options Analytics
- Institutional Order Flow
- Alternative Data
- Vision Models
- LLM Copilot
- Strategy Marketplace
- Plugin Marketplace
- Social Trading
- Mobile Companion
- Enterprise Collaboration

---

# Architecture Principles

Every subsystem should satisfy:

1. Single Responsibility  
2. Open for Extension  
3. Closed for Modification  
4. Dependency Inversion  
5. Loose Coupling  
6. High Cohesion  
7. Interface Segregation  
8. Testability  
9. Replaceability  
10. Scalability  
11. Professional Maintainability  
12. Auditability  

---

# Architectural Constraints (Immutable unless governance amends)

1. ML research is separated from execution.  
2. Governance is independent.  
3. Every prediction is auditable.  
4. Every experiment is reproducible.  
5. Every component is testable.  
6. Market support is extensible.  
7. Human oversight remains available.  
8. Architecture must remain modular.  
9. No live automated execution without explicit future governance authorization.  
10. Presentation is non-authoritative for domain/ML computation.  
11. No credentials in source code.  
12. No undocumented production behaviour.

---

# Mapping: Prior Documents → This Merge

| Concept | Source 05 | Source 06 | Canonical Resolution |
|---------|-----------|-----------|----------------------|
| Layer count | 8 logical layers | 7 major systems | **8 logical layers + 8 capability subsystems**; 06 systems mapped into them |
| Stack | Implicit | Explicit FastAPI/React/PG | **Explicit stack from 06** |
| Feature Engineering | Under ML Platform | Separate major system | **Capability within ML Platform; first-class pipeline stage** |
| Market Intelligence | First-class subsystem | Distributed | **First-class capability subsystem** |
| Chart Intelligence | First-class subsystem | Chart architecture section | **First-class capability subsystem** |
| UI calculations | Not stated | “Never performs calculations” | **Display/render only; no authoritative domain/ML math client-side** |
| Execution | Research-oriented | “Optional Broker Execution” | **Human-approved / paper / sim / governance-authorized only** |
| Events | Communication patterns | Event-driven examples | **Event-driven where beneficial; immutable events** |

---

# Long-Term Objective

The final architecture shall support a professional institutional trading research platform capable of combining:

- Machine Learning
- Artificial Intelligence
- Professional Visualization
- TradingView-quality charting
- MT5-inspired trade management
- Multi-market analytics
- Scientific validation
- Institutional governance
- Human expertise

within one unified ecosystem.

---

# Approval & Status

| Field | Value |
|-------|--------|
| Status | **ACTIVE — CANONICAL** |
| Classification | CORE GOVERNING DOCUMENT |
| Version | 1.1.0 |
| Effective | 2026-07-10 |
| Merge authorized by | Operator |
| Merge performed by | Development Authority |

This architecture defines the technical foundation of AXIOM and shall govern all future software development until superseded by a newer architecture document of the same domain family under the project’s document precedence rules.

---

**End of Document**
