# AXIOM Project Roadmap

Version: 1.0
Status: ACTIVE
Classification: Master Development Roadmap
Authority: Project Governance

---

# Purpose

This document defines the official development roadmap for AXIOM.

It establishes the complete development lifecycle from project initialization to production readiness.

The roadmap defines:

- development waves
- implementation units
- dependencies
- milestones
- governance gates
- review checkpoints

This roadmap shall remain stable throughout development.

Project progress shall be recorded separately in PROJECT_STATE.md.

---

# Development Philosophy

AXIOM shall be developed incrementally.

Each completed unit must:

✓ be fully implemented

✓ fully tested

✓ documented

✓ independently reviewed

✓ approved

before the next unit begins.

Incomplete work shall never propagate into future waves.

---

# Development Lifecycle

Every unit follows the same lifecycle.

Operator Objective

↓

Development Authority Implementation

↓

Internal Verification

↓

Documentation Synchronization

↓

Delivery Report

↓

Independent Technical Review (ITRGA)

↓

Corrections (if required)

↓

Approval

↓

Next Unit Authorization

The Development Authority shall never authorize the next unit.

Build Orders are issued exclusively by the Independent Technical Review & Governance Authority (ITRGA).

---

# Project Overview

The project is divided into eight major development waves.

Each wave builds upon the previous one.

Dependencies are strictly enforced.

---

# Wave 0 — Foundation

Objective

Establish the professional project foundation.

Deliverables

Project governance

Documentation framework

Repository structure

Development standards

Review framework

Configuration management

Project initialization

Milestone

Project Constitution Approved

---

# Wave 1 — Core Platform

Objective

Build the core application framework.

Major Components

Backend architecture

Frontend architecture

Authentication

Configuration system

Logging

Database layer

Service architecture

API framework

TradingView integration

MT5 integration framework

Milestone

Core Platform Operational

---

# Wave 2 — Machine Learning Research Framework

Objective

Develop the institutional research environment.

Major Components

Dataset pipeline

Multi-market data ingestion

Feature engineering

Feature store

Experiment framework

Walk-forward validation

Statistical evaluation

Calibration

Economic viability analysis

Cross-market benchmarking

Generalization framework

Model registry

Experiment governance

Milestone

Research Framework Complete

---

# Wave 3 — Live Research Advisor

Objective

Transform research into a professional advisory platform.

Major Components

Live inference engine

Market monitoring

Signal generation

Governance dashboard

Performance analytics

Confidence visualization

Operator alerts

Drift monitoring

Health monitoring

Research audit trail

Signal history

Operator workspace

Milestone

Professional Advisor Platform Complete

---

# Wave 4 — Institutional Intelligence

Objective

Expand analytical capabilities.

Major Components

Cross-market intelligence

Correlation engine

Market regime detection

Macro analysis

Sector relationships

Portfolio analytics

Risk analytics

Professional signal validation

AI chart annotations

Trade scenario simulation

Milestone

Institutional Intelligence Layer Complete

---

# Wave 5 — Human-AI Collaboration

Objective

Create an interactive AI-assisted trading environment.

Major Components

Interactive AI chart assistant

Professional drawing tools

AI-generated annotations

Scenario comparison

Trade planning workspace

Professional signal investigation

Manual trade journal

Decision explanations

Interactive research assistant

Milestone

Human-AI Collaborative Workspace Complete

---

# Wave 6 — Execution Research

Objective

Research execution workflows without compromising governance.

Major Components

Execution simulator

Risk engine

Broker abstraction

Paper trading

Execution analytics

Position management research

Trade replay

Performance comparison

Execution experimentation

Milestone

Execution Research Environment Complete

Note:

No live automated execution shall be authorized unless future governance explicitly approves it.

---

# Wave 7 — Institutional Platform

Objective

Transform AXIOM into a complete institutional research terminal.

Major Components

Workspace customization

Portfolio dashboard

Research management

Strategy laboratory

Plugin architecture

API ecosystem

Advanced reporting

Enterprise scalability

Multi-user readiness

Milestone

Institutional Platform Complete

---

# Cross-Wave Capabilities

The following capabilities evolve continuously across multiple waves.

Machine Learning

Multi-market learning

Transfer learning

Cross-market validation

Model versioning

Continuous retraining

Performance monitoring

Operator Experience

Professional UI

TradingView-quality charts

MT5-inspired trade management

Responsive dashboards

Research workflows

Engineering

Testing

Documentation

Security

Performance optimization

Architecture refinement

Governance compliance

---

# Research Scope

The research framework shall support:

Forex

Cryptocurrency

Indices

Commodities

Stocks

Futures

Additional markets may be added through future governance approval.

---

# Future Research Initiatives

The following initiatives are intentionally deferred until the core roadmap has been completed.

Professional Signal Validation

Allow operators to manually enter external trading signals.

AXIOM shall independently evaluate:

market structure

trend alignment

multi-timeframe confluence

technical indicators

statistical confidence

historical context

risk-reward

AI Chart Collaboration

Future AI modules may interact directly with charts by:

drawing trendlines

marking support/resistance

identifying liquidity zones

creating trade plans

displaying probability regions

annotating market structure

These capabilities remain outside the scope of early development waves.

---

# Governance Rules

Every wave shall satisfy:

Architecture review

Source code review

Runtime verification

Security review

Performance review

Documentation review

Governance review

No wave shall advance without Independent Technical Review approval.

---

# Success Criteria

The project shall ultimately deliver:

✓ Institutional-grade architecture

✓ Multi-market machine learning

✓ Professional trading terminal

✓ TradingView-quality charting

✓ MT5-inspired trade workspace

✓ Explainable AI

✓ Human-centered decision support

✓ Independent governance

✓ Scientific integrity

✓ Long-term maintainability

---

# Implementation Progress Notes

| Date | Unit | Note |
|------|------|------|
| 2026-07-13 | W1-U03 | MT5 integration **framework** delivered as broker-neutral External Integration seam. Real broker connection, broker credentials, live broker quotes, and execution remain explicitly deferred and governance-gated. |
| 2026-07-13 | W1-U04 | Wave-1 closure/hardening: frontend critical/high supply-chain vulnerabilities remediated; CI/local gates include npm audit. **Core Platform Operational** milestone candidate pending ITRGA closure approval. |
| 2026-07-13 | W2-U01 | Canonical dataset architecture and chronology guard implemented; model work remains gated. |
| 2026-07-13 | W2-U02 | Market-agnostic data access and multi-market metadata layer implemented; provider adapters remain non-live and research-only. |
| 2026-07-13 | W2-U03 | Feature definition framework and Feature Store v1 implemented with causal/no-symbol-identity feature boundaries. |
| 2026-07-13 | W2-U04 | Reproducible dataset snapshot builder and temporal split engine implemented; random splits and label-horizon leakage rejected. |
| 2026-07-13 | W2-U05 | Experiment registry and pre-registration workflow implemented; first model unit remains gated until ITRGA approval. |
| 2026-07-14 | W2-U06 | Baseline market-agnostic model harness implemented as pure-Python research-only baseline; no live signals/execution. |
| 2026-07-14 | W2-U07 | Statistical validation framework implemented with temporal walk-forward folds and uncertainty-mandatory validation reports. |
| 2026-07-14 | W2-U08 | Calibration and probability quality framework implemented with Brier/ECE, reliability bins, miscalibration warnings, and base-rate-aware significance. |
| 2026-07-15 | W2-U09 | Economic validation framework implemented with cost provenance, scenario sensitivity, and separate statistical/economic conclusions. |
| 2026-07-15 | W2-U10 | Multi-market generalization, model registry maturation, and drift design implemented; Research Framework Complete candidate pending ITRGA closure. |
| 2026-07-15 | W3-U01 | Live inference engine and governed eligibility gate implemented as backend-only safety foundation; no operator signal surface. |
| 2026-07-15 | W3-U02 | Advisory signal contract and persistence implemented as inert backend/API record; read-only history API; no UI, alerts, live signal stream, broker, or execution. |
| 2026-07-15 | W3-U03 | Emit-time operating-domain, calibration, economic, and staleness guardrails implemented for inert advisory signal records; no UI, alerts, live push, broker, or execution. |
| 2026-07-15 | W3-U04 | Live market inference adapter implemented using existing W1 live seam with as-of/no-look-ahead discipline; no external feed, UI, alerts, broker, or execution. |
| 2026-07-15 | W3-U05 | Operator advisory dashboard/signal workspace implemented as protected read-only UI with advisory disclaimer and guardrail visibility; no alerts, live push, broker, or execution controls. |
| 2026-07-15 | W3-U06 | Monitoring, drift, and health alerts implemented as inert persisted/audited records with read-only/ack API; no auto-action, auto-retraining, remediation, broker, or execution. |
| 2026-07-16 | W3-U07 | Performance analytics and confidence visualization implemented with uncertainty-mandatory metrics, calibrated confidence bands, advisory-not-guaranteed UI framing, and no execution controls. |
| 2026-07-16 | W3-U08 | Wave-3 closeout and hardening artifacts implemented; evidence index, ADR, audit/no-execution/security proof pack, read-only alert panel hardening; pending ITRGA milestone declaration. |
| 2026-07-16 | W3-U08.1 | Residual hardening implemented for SQLite StaticPool local CI flake and browser evidence archive completion; no product capability, schema, execution, or gate change. |
| 2026-07-16 | W4-U01 | Institutional Intelligence foundation implemented: scientific dependency spike framework, bounded context skeleton, inert artifact contract, pure-Python fallback primitives; no analytical feature, schema, UI, or execution. |
| 2026-07-16 | W4-U02 | Correlation intelligence reports implemented as persisted, audited, as-of-bounded research artifacts with uncertainty/sample counts and read-only API; no UI, signal emission, or execution. |
| 2026-07-16 | W4-U03 | Regime detection reports implemented as persisted, audited, explainable normalized-feature research artifacts with confidence/uncertainty and read-only API; no UI, signal emission, learned model, or execution. |
| 2026-07-16 | W4-U04 | Scenario simulation research reports implemented as persisted, audited, hypothetical research artifacts with assumptions, uncertainty, economic-usefulness field, and read-only API; no UI, order/sizing, signal emission, or execution. |
| 2026-07-16 | W4-U05 | Portfolio/risk research reports implemented as persisted, audited, hypothetical market-series artifacts with uncertainty/sample count and no account/broker/position linkage; no UI, signal emission, or execution. |
| 2026-07-16 | W4-U06 | Professional signal validation reports implemented as persisted, audited research artifacts over declared advisory-signal scopes with uncertainty, raw-score exclusion, and honest outcome-data status; no UI, signal emission, or execution. |
| 2026-07-16 | W4-U07 | Institutional Intelligence dashboard implemented as protected presentation-only UI over existing W4 reports with uncertainty/sample count and research framing; no client recompute, signal emission, or execution controls. |
| 2026-07-16 | W4-U08 | Wave-4 closeout and hardening artifacts implemented; W4-U07 interval-bound display fixed; evidence index, audit/no-execution/auth proof pack, docs/register reconciliation prepared; pending ITRGA milestone declaration. |
| 2026-07-16 | W5-U01 | Collaboration safety foundation implemented with deterministic non-actuating assistant boundary, grounding/refusal policy, audited refusals, and inert plan/journal contracts; no external LLM, UI, persistence table, execution, or gate change. |
| 2026-07-17 | W5-U02 | Audited assistant research responses implemented as persisted hash-only response/refusal records with no-orphan audit linkage and read-only API; no external LLM, UI panel, action tool, execution, or gate change. |
| 2026-07-17 | W5-U03 | Chart research annotations/drawing tools implemented as inert persisted/audited operator markups rendered presentation-only on charts; no AI generation, signal emission, order/execution/account path, or gate change. |
| 2026-07-17 | W5-U04 | Signal investigation workspace implemented as read-only/presentation-only signal rationale, guardrail, lineage, and linked-report surface; no signal mutation, action controls, execution, or gate change. |
| 2026-07-17 | W5-U05 | Scenario comparison workspace implemented as read-only/presentation-only comparison of existing persisted scenario reports; no scenario generation, action controls, execution, or gate change. |
| 2026-07-17 | W5-U06 | Inert trade planning workspace implemented as persisted/audited research notes with forbidden order/sizing/account/execution fields rejected; no order ticket, execution, or gate change. |
| 2026-07-17 | W5-U07 | Manual research journal implemented as persisted/audited reflections with broker/account/execution/fill/P&L fields rejected; no broker import, execution, or gate change. |
| 2026-07-17 | W5-U08 | Wave-5 closeout and hardening approved by ITRGA; Wave 5 closed; Human-AI Collaborative Workspace Complete milestone declared at v0.46.0. |
| 2026-07-17 | Wave 6 Design | Wave-6 Execution Research design plan accepted with refinements R6-1…R6-8; simulation-only / Gate CLOSED. |
| 2026-07-17 | W6-U01 | Execution Research safety foundation implemented: simulation-only bounded-context skeleton and audited closed-Gate broker connect/execute refusals; no schema, UI, dependency, live broker, or Gate change. |
| 2026-07-17 | W6-U02 | Simulated execution runs and fill events implemented as persisted/audited SIMULATED research artifacts with deterministic fill model; no UI, live broker, account linkage, real order, or Gate change. |
| 2026-07-17 | W6-U03 | Simulated paper research ledger implemented over simulated fills only with uncertainty-bearing simulated return estimates; no UI, real P&L, account/broker linkage, or Gate change. |
| 2026-07-17 | W6-U04 | Execution risk research reports implemented over simulated artifacts with structured metrics, uncertainty, and separate economic usefulness; no sizing engine, account linkage, UI, or Gate change. |
| 2026-07-17 | W6-U05 | Trade replay and execution experiment pre-registration implemented with immutable plan hash and as-of bounded replay lineage; no look-ahead, live feed, broker path, UI, or Gate change. |
| 2026-07-17 | W6-U06 | Simulated execution analytics and performance comparison reports implemented with full declared scope, per-metric uncertainty, deterministic report hash, and stat/economic separation; no UI, real P&L, or Gate change. |
| 2026-07-17 | W6-U07 | Execution research workspace UI implemented as display-only surface over persisted simulated artifacts with SIMULATED labels and no actuation controls; approved with operator-authorized CI/logged-out evidence dispositions. |
| 2026-07-18 | W6-U08 | Wave-6 closeout and hardening approved by ITRGA; Wave 6 closed; Execution Research Environment Complete milestone declared at v0.54.0. |
| 2026-07-18 | Wave 7 Design | Wave-7 Institutional Platform design plan accepted with refinements R7-1…R7-8; Gate CLOSED. |
| 2026-07-18 | W7-U01 | Institutional Platform security/API foundation implemented with authenticated institutional route inventory, default-deny RBAC policy, two-operator isolation, and no execution/order/broker/account endpoint; no table, UI, plugin execution, or Gate change. |
| 2026-07-18 | W7-U02 | Operator workspace customization implemented with per-operator presentation preferences, operator-scoped API/UI, secret-marker rejection, and no action/account/execution fields; Gate CLOSED. |
| 2026-07-18 | W7-U03 | Research management collections and tags approved by ITRGA; reference-only metadata over existing governed artifacts, source no-mutation, operator isolation, and Gate CLOSED proven. |
| 2026-07-18 | W7-U04 | API ecosystem catalogue and versioned research API hardening approved by ITRGA; authenticated generated catalogue, no persisted table/UI, no execution surface, and Gate CLOSED. |
| 2026-07-18 | W7-U05 | Plugin contract safety foundation approved by ITRGA; published read-only contracts plus hostile-request refusal/audit only; no dynamic plugin execution, no plugin execution audit table, Gate CLOSED. |
| 2026-07-18 | W7-U06 | Portfolio research dashboard and advanced reporting approved by ITRGA; hypothetical research aggregation/export preview with uncertainty, no real account/P&L framing, no report table, Gate CLOSED. |
| 2026-07-19 | W7-U07 | Enterprise scalability and multi-user readiness hardening approved by ITRGA; RBAC/isolation/redaction/audit re-proof, admin default rejection, rate guard formal defer, Gate CLOSED. |
| 2026-07-19 | W7-U08 | Wave-7 closeout and whole-project completion approved clean by ITRGA; Wave 7 closed; Institutional Platform Complete final milestone declared at v0.62.0; roadmap implementation complete; production certification remains separate. |
| 2026-07-13 | W2-U05 | Experiment registry and pre-registration workflow implemented; model gate candidate pending ITRGA approval. |

---

# Long-Term Vision

AXIOM is intended to become a professional quantitative research and trading intelligence platform that combines:

Artificial Intelligence

Machine Learning

Professional Market Analysis

Institutional Software Engineering

Advanced Visualization

Scientific Validation

Governance

Human Expertise

into a unified decision-support ecosystem suitable for serious financial research.

---

End of Document