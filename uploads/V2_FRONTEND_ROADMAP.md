# AXIOM V2 — Proposed Frontend and Terminal Roadmap

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-FE-ROADMAP-001 |
| Status | **PROPOSED — planning only** |
| Source | V2 Product & Architecture Specification; supplied visual-reference consultation set; V1 UI/UX and security governance |
| Relationship to V1 | Evolves the existing V1 terminal; preserves supported V1 routes/capabilities unless an explicit breaking change is approved |
| Implementation authority | **None conferred by this document** |
| Approval required | Operator constitutional adoption/amendment, approved V2 UI/UX plan, Build Order, and ITRGA review for every implementation unit |

---

## 1. Purpose

This roadmap converts the V2 product direction and visual-reference discussion into a bounded, incremental terminal programme. It is intentionally not a request for a fourth wholesale frontend rewrite.

The target is one coherent institutional workstation that can progressively host research, simulation, paper, and—only if separately authorized and certified—live execution workflows.

The roadmap uses the supplied images as **design-quality references only**. It does not authorize literal copying of external brand marks, text, third-party layouts, false market/account values, broker integrations, trading controls, or unsupported functionality.

## 2. Frontend invariants

Every V2 frontend unit must preserve these rules:

1. **One terminal, not disconnected products.** A stable global shell, shared design system, consistent terminology, and predictable navigation are mandatory.
2. **Truthful mode and provenance.** The UI must display `RESEARCH`, `SIMULATION`, `PAPER`, or `LIVE` from authoritative backend state; source/freshness must be visible where material.
3. **No fabricated UI state.** Empty, stale, unavailable, denied, unknown, and degraded data must be visibly distinct from real results.
4. **Presentation is not authority.** The frontend must not calculate authoritative analytics, risk, account, order, model, or execution state.
5. **No direct provider/broker/AI-secret connection.** Browser code never contacts brokers directly and never receives provider/broker secrets.
6. **Execution controls are absent until backend authority exists.** An attractive order ticket is still prohibited until the dedicated paper/live backend and governance gates permit it.
7. **Assistant is non-actuating.** It may explain authorized context but cannot create, approve, alter, submit, or cancel orders.
8. **Accessibility and responsive behavior are baseline requirements.** Keyboard operation, focus, screen-reader state announcements, contrast, reduced motion, and resilient narrow-layout behavior are not optional polish.
9. **Visual references require AXIOM adaptation.** No copied external brand identity, vendor claim, real quote, market-open state, provider label, P&L, account, or certification content may be fabricated.

## 3. Design direction adopted from the reference consultation

The proposed UI direction is a professional institutional workstation with:

- dark, low-glare surface hierarchy and restrained semantic color;
- compact data-dense tables with aligned numerical columns and mono styling for IDs/times;
- a clear global header, command/search capability, session/operator identity, visible mode state, and global health posture;
- a calm left navigation rail and contextual page/sub-workspace header;
- a chart-first operating surface where chart analysis is the active task;
- inspector/drawer patterns for evidence, lineage, methodology, and contextual detail;
- cards only for meaningful summaries; data tables for high-density records;
- persistent provenance, source, freshness, uncertainty, limitations, and status where material;
- first-class loading, empty, error, denied, stale, degraded, and unknown states;
- a visually unmistakable separation between Research, Simulation, Paper, and Live.

The UI must not use density as a substitute for information hierarchy. Each workspace has one primary task and bounded secondary context.

## 4. Reference-image adoption matrix

| Reference direction | Roadmap disposition |
|---|---|
| Institutional sign-in surface | **Adopt / adapt** — use AXIOM identity, approved auth flows, no unsupported SSO/reset claims |
| Terminal home / watchlist / chart / dock composition | **Adopt / adapt** — retain research-first state and remove V1-prohibited trading semantics until V2 authorization exists |
| Chart-focused workspace | **Adopt / adapt** — existing chart/drawing/indicator foundation, truthful simulated/live source state |
| Feed-health table | **Adopt / adapt** — actual supported instruments/source/latency only |
| Intelligence, signals, scenario, research, journal, artifact explorer | **Adopt / adapt** — use actual report/artifact data, uncertainty, lineage, and read/write permissions |
| Governance and evidence control room | **Adopt / adapt strictly** — actual data only; never invented readiness/certification/control scores |
| Workspace settings | **Adopt / adapt** — per-operator presentation preferences only |
| Assistant side panel | **Adopt / adapt** — local/read-only in early V2; no action tooling; external provider requires separate authorization |
| Order ticket, positions, balances, fills, account UI | **Defer** — only after corresponding paper/live backend, security, risk, and environment-isolation bands are approved |
| Buy/Sell, order book, broker/exchange UI, live P&L | **Exclude from early V2 frontend** — prohibited until separately authorized and production-ready |

---

# Band FE-0 — V2 UX Governance, Research, and Design Plan

## Objective

Establish a governed V2 terminal experience plan before visual implementation.

## Scope

- inventory V1 surfaces, routes, reusable components, design tokens, accessibility coverage, and UI technical debt;
- map every supplied reference component as **Adopt**, **Adapt**, or **Exclude**;
- define operator personas and primary task journeys;
- define V2 information architecture and navigation model;
- produce mode-safety visual rules; provenance/freshness/uncertainty rules; state/error/empty rules; and terminology rules;
- define initial V2 page contracts and component inventory;
- establish screenshot/browser/accessibility/performance evidence baseline.

## Required journeys

1. Sign in and understand current AXIOM mode/posture.
2. Select an instrument and inspect chart/data provenance.
3. Understand a signal or intelligence artifact without treating it as an order instruction.
4. Inspect evidence, lineage, and limitations.
5. Navigate directly to a re-homed workspace and know where it opened.
6. Recover from no data, stale data, denied access, and service degradation.

## Explicit exclusions

- No visual implementation, no new route, no styling rewrite, no order-ticket mock, no new backend behavior.

## Exit evidence

- approved V2 design plan;
- page/component contract inventory;
- Adopt/Adapt/Exclude register;
- design-token delta proposal;
- accessibility and acceptance criteria;
- approved migration sequence.

---

# Band FE-1 — Shared V2 Terminal Shell and Design System Evolution

## Objective

Evolve the existing V1 shell into the common V2 visual and interaction foundation while preserving V1 behavior.

## Scope

- global header: AXIOM identity, command/search entry, operator identity, time/status, current mode, global health;
- left navigation rail with clear active context, keyboard operation, collapse behavior, and role-aware visibility;
- page/workspace header with explicit title, primary task, context, and route announcement;
- core tokens: color, typography, spacing, elevation, density, tables, status semantics, borders, focus, motion;
- reusable primitives: data table, metric strip, provenance badge, mode badge, freshness indicator, uncertainty badge, limitation panel, inspector drawer, record header, contextual toolbar;
- common loading, empty, error, denied, stale, degraded, and unknown states;
- route-transition and focus-management behavior.

## Guardrails

- V1 routes must not silently break.
- The shell does not add accounts, orders, positions, or execution controls.
- `LIVE` cannot be client-selected; it derives from an authoritative backend mode/source response.

## Exit evidence

- V1 route regression suite;
- keyboard/focus/route-announcement evidence;
- desktop and narrow layout evidence;
- visual-regression captures for the shell;
- no changes to prohibited capability vocabulary or API calls.

---

# Band FE-2 — Research and Simulation Home Terminal

## Objective

Replace the first-use ambiguity of the V1 home surface with a clear professional research terminal.

## Scope

- chart-first operations/research home;
- concise watchlist with search, filters, source/freshness, and explicit empty states;
- instrument context header;
- chart stage with indicator/drawing/context integration;
- signals, telemetry, intelligence, alert, scenario, portfolio, trade-plan, and journal docks as appropriate;
- a first-run onboarding pattern that explains safe seeded/simulated data activation and no-actuation posture;
- contextual evidence/lineage actions;
- stable deep-link resolution with visible destination confirmation.

## Required behavior

- A user reaching `/charts`, `/signals`, `/analytics`, `/investigate`, `/compare-scenarios`, `/execution-research`, `/portfolio-research`, `/research-management`, `/governance`, or `/workspace` receives a route-specific context announcement rather than only “Operations.”
- No data means no data; no fabricated chart or value is shown.
- Simulated data is never visually indistinguishable from a future real source.

## Exit evidence

- first-use browser workflow evidence;
- direct-link/orientation tests;
- empty/loading/error/stale/denied state captures;
- browser console clear of unexpected errors;
- source/provenance visual assertions.

---

# Band FE-3 — Market Data and Chart Intelligence Surfaces

## Objective

Create the V2 chart and market-monitor visual language over existing simulated/historical contracts, then progressively support authorized provider states.

## Scope

- full chart workspace composition: chart, timeframe controls, indicator menus, drawing controls, annotations, chart tools, contextual inspector;
- market/quote table with sortable columns, provenance, freshness, class, timeframe, availability and source state;
- feed-health/status surface;
- market-context and chart-intelligence inspector panels;
- multi-timeframe context presentation;
- clear structural-vs-predictive visual differentiation.

## Conditional capabilities

- Real source labels, delayed/stale states, provider badges, depth, and live market status appear only after their backend/provider contracts are authorized and available.

## Explicit exclusions

- No trade panel, order book, order entry, broker connection, real venue claim, or unlabelled external-market data.

## Exit evidence

- chart-data/source-state visual tests;
- no-data and insufficient-history tests;
- annotation/drawing persistence regression;
- server-side-result display contract tests;
- responsive and accessibility evidence.

---

# Band FE-4 — Intelligence, Signals, Investigation, and Evidence Workspaces

## Objective

Create deep institutional research workspaces that expose truth, uncertainty, lineage, and limitations without presenting research as execution instruction.

## Scope

- intelligence reports: correlations, regimes, scenarios, portfolio/risk, signal validation, model diagnostics;
- signal workspace: structural/predictive family separation, guardrails, freshness, confidence, calibration, limitations, lineage, withholding/refusal states;
- investigation workspace: signal rationale, market context, linked evidence and research artifacts;
- lineage/evidence inspector and trace graph;
- standardized report metadata: source, as-of, computation version, sample, uncertainty, limitation, artifact ID;
- contextual assistant read-only explanation handoff.

## Guardrails

- No entry, stop, target, risk/reward, trade-quality, Buy/Sell, or execution CTA.
- “Bullish/bearish” or similar language, where used, is a clearly bounded analytical classification with uncertainty and not an instruction.
- Every displayed figure must be API-sourced and correctly classified.

## Exit evidence

- structural/predictive state tests;
- stale/withheld/expired/refused views;
- lineage traceability UI tests;
- research wording and non-actuation source scans;
- direct browser evidence of limitation/uncertainty treatment.

---

# Band FE-5 — Scenario, Research, Journal, and Artifact Workspaces

## Objective

Unify AXIOM’s research lifecycle into professional artifact-oriented workspaces.

## Scope

- scenario comparison for existing persisted scenario reports;
- research management/artifact explorer: search, filters, collections, tags, tables, metadata, lineage, relationship inspector;
- structured trade-plan research notes;
- manual research journal/reflection workflow;
- governed write UX only for approved operator-authored artifacts;
- artifact status, attribution, audit, and limitation displays.

## Guardrails

- Current unapproved scenario generation, arbitrary artifact mutation, uncontrolled scheduling, and unverified export behavior remain absent.
- Any creation/edit UI must match an audited backend mutation contract, correct RBAC, and a specific Build Order.
- No artifact state is labelled production, certified, reviewed, or approved unless the actual backend record supports it.

## Exit evidence

- permissions and audit UI tests;
- read-only versus mutable state tests;
- artifact/lineage accuracy evidence;
- save/failure/conflict/reload evidence for any authorized mutation.

---

# Band FE-6 — Hypothetical Portfolio, Risk, Backtest, and Simulation Research

## Objective

Present portfolio/risk, backtest, replay, and simulation results as transparent research before account or order UI exists.

## Scope

- hypothetical portfolio allocation/exposure/risk workspace;
- scenario/stress comparison;
- backtest/replay result views;
- simulation analytics and methodology views;
- risk metric, assumption, confidence/uncertainty, data-source, and limitation panels;
- report preview where approved;
- immutable experiment/research record inspector.

## Explicit exclusions

- No real account identity, holdings, balances, margin, actual positions, live P&L, or order ticket.
- Backtest/simulation is never rendered as live performance or a promise.

## Exit evidence

- display classification tests: backtest vs simulation vs paper vs live;
- metric/uncertainty/source mapping tests;
- no-live-account/no-order UI source scans;
- browser evidence for incomplete/insufficient data states.

---

# Band FE-7 — Paper Trading User Experience

## Objective

Introduce paper-order and paper-account UI only after the authorized paper backend, risk gateway, and environment-isolation controls exist.

## Scope

- persistent `PAPER` environment treatment with unmistakable visual identity;
- paper account selection/context;
- order-intent form for supported paper instruments/types;
- validation and pre-trade risk result display;
- explicit confirmation step;
- paper order lifecycle, simulated fill, simulated position, paper balance/margin, and research P&L views;
- discrepancy/error/unknown-state views;
- paper audit/lineage inspector.

## Non-negotiable UX controls

- Paper state is visible in the global shell, page header, ticket, confirmation, order status, account, position, reports, and assistant context.
- The UI does not use a generic green/red Buy/Sell action alone; it requires explicit paper mode, order summary, validation, risk result, and confirmation.
- A paper account can never be mistaken for a live account.

## Exit evidence

- paper workflow end-to-end browser tests;
- validation/risk-blocked/rejected/partial/unknown state captures;
- proof that paper routes cannot call live endpoints;
- role/permission/focus/accessibility evidence;
- ITRGA review of mode-safety behavior.

---

# Band FE-8 — Broker Account Visibility and Reconciliation UX

## Objective

Expose authorized broker/account information read-first, with reconciliation and discrepancy visibility, before live order submission exists.

## Scope

- read-only live account/instrument/position/order/fill views when backend authorization exists;
- account/provider/source/freshness/reconciliation status;
- discrepancy records with severity, timestamp, correlation, affected object and resolution state;
- read-only account/portfolio/risk context;
- provider/broker health and degraded-state presentation.

## Guardrails

- No broker credential display.
- No direct browser-to-broker traffic.
- No order creation/cancel/modify in this band.
- Data is hidden or redacted by role/account entitlement.

## Exit evidence

- RBAC and data-isolation tests;
- stale/unavailable/mismatch/unknown-state captures;
- reconciliation drill-down evidence;
- sensitive-value redaction tests.

---

# Band FE-9 — Controlled Live Execution UX

## Objective

Render live execution controls only after backend execution gateway, risk controls, reconciliation, incident procedures, Operator authorization, and production certification permit the defined scope.

## Scope

- persistent high-salience `LIVE` mode identity;
- live account and provider confirmation;
- limited order-intent/ticket for approved instruments and order types;
- authoritative validation/risk preview;
- explicit human confirmation/step-up flow;
- immutable order intent and audit correlation display;
- execution lifecycle states: Draft, Validating, Risk Blocked, Ready, Submitted, Acknowledged, Partially Filled, Filled, Cancelled, Rejected, Failed, Unknown;
- reconciliation and emergency/kill-switch status display;
- safe failure, uncertainty, and escalation guidance.

## Absolute prohibitions

- No automatic execution from a signal, chart pattern, model output, or assistant text.
- No “success” display without authoritative backend/broker confirmation.
- No generic default account/provider selection.
- No hiding of risk blocks, discrepancy, timeout, or unknown states.

## Exit evidence

- end-to-end success and failure browser evidence in an approved controlled environment;
- role, account, instrument, and mode authorization tests;
- confirmation, idempotency, retry, duplicate, partial-fill and unknown-state tests;
- independent security/production-readiness certification evidence.

---

# Band FE-10 — Contextual Assistant V2

## Objective

Evolve the current contextual assistant in a controlled sequence.

## Scope before external AI approval

- selected-instrument/timeframe/chart/signal/research/scenario/risk explanation;
- grounded source-artifact cards;
- uncertainty and limitation display;
- deterministic/local identity, audit trail, refusal language, and read-only interaction;
- explicit distinction between observation, prediction, interpretation, recommendation, and action.

## Conditional scope after separate AI/provider authorization

- approved external-provider disclosure and selection state;
- data-sharing notice and consent/entitlement posture;
- source-grounded response evidence, provider/model identity, failure/fallback state;
- read-only explanation of authorized account/order/execution state.

## Permanent prohibitions

- No assistant execution authority;
- no order create/modify/approve/cancel through natural language;
- no broker secrets/accounts in assistant prompts beyond governed, minimized, permitted context;
- no hidden external provider;
- no unsupported financial advice framing.

## Exit evidence

- prompt-injection/refusal tests;
- source-grounding/lineage tests;
- action-boundary tests;
- role/data-redaction evidence;
- clear user-facing disclosure evidence.

---

## 5. Required frontend quality gates

Each authorized frontend unit must include:

- approved page/component contract and scope boundary;
- design-token and component reuse assessment;
- route/RBAC/feature-flag behavior;
- browser evidence at required desktop and narrow viewports;
- keyboard-only, focus, screen-reader announcement, contrast, reduced-motion, and error/empty-state evidence;
- visual regression baseline;
- API-state mapping: loading, ready, stale, unavailable, denied, degraded, unknown;
- mode/provenance/uncertainty/limitation visibility where applicable;
- no prohibited trading/secret/provider vocabulary or endpoint calls for the approved band;
- V1 regression results;
- Delivery Report, evidence index, technical debt and project-state updates.

## 6. Frontend roadmap completion condition

The V2 terminal is not complete when it resembles a professional trading interface. It is complete only when its rendered UI truthfully represents the authorized backend capability, current mode, source, permissions, uncertainty, risk and execution state—and each approved workflow is accessible, evidenced, secure, and governable.
