# AXIOM Engineering Design Plan — Institutional Trading Terminal UI Rebuild
## Master Architecture, Component Reconciliation, Information Hierarchy, and 6-Phase Delivery Roadmap

| Field | Value |
|---|---|
| Document ID | `docs/plans/UI-NEW_ENGINEERING_DESIGN_PLAN.md` |
| Programme | AXIOM Institutional Trading Terminal Transformation |
| Workstream | **New Trading Terminal UI (Clean Rebuild)** |
| Document Classification | Tier 8 — Execution Governance (Engineering Design Plan) |
| Author | AXIOM Development Authority (DA) |
| Governing Instrument | `UI-NEW_ENGINEERING_DESIGN_PLAN.md` (Operator Directive Issued 2026-08-12) & `ITRGA_REQUEST_UI-NEW_DESIGN_PLAN.md` |
| Review Authority | Independent Technical Review & Governance Authority (ITRGA) |
| Baseline of Record | **Frontend: 148 test suites / 603 tests passing · Backend: 414 tests passing · Total: 1,017 automated tests passing** |
| Governance Gate | **STRICTLY CLOSED** (Enforced: Zero Live Broker Execution, Order Routing, or Real Capital Actuation) |
| Production Status | **NOT CERTIFIED** (Firewalled under `11_PRODUCTION_READINESS_CERTIFICATION.md`) |
| DA Operational State | **Design Plan Submitted for Independent ITRGA Review; Implementation on Formal Hold Pending Build Order** |

---

# Table of Contents

1. [Executive Summary & Charter](#1-executive-summary--charter)
2. [Section A — Workstream Objective & Scope](#2-section-a--workstream-objective--scope)
3. [Section B — Product Vision & Institutional Experience Model](#3-section-b--product-vision--institutional-experience-model)
4. [Section C — Existing-State Assessment & Repository Inventory](#4-section-c--existing-state-assessment--repository-inventory)
5. [Section D — Existing-Asset Reconciliation Matrix](#5-section-d--existing-asset-reconciliation-matrix)
6. [Section E — Target Trading Terminal Architecture](#6-section-e--target-trading-terminal-architecture)
7. [Section F — UX Principles & Visual Direction](#7-section-f--ux-principles--visual-direction)
8. [Section G — Information Architecture & Hierarchy](#8-section-g--information-architecture--hierarchy)
9. [Section H — Workspace Architecture & Multi-Pane Layout](#9-section-h--workspace-architecture--multi-pane-layout)
10. [Section I — Navigation Architecture & Command System](#10-section-i--navigation-architecture--command-system)
11. [Section J — Component Architecture & Terminal Primitives](#11-section-j--component-architecture--terminal-primitives)
12. [Section K — Design-System & Token Strategy](#12-section-k--design-system--token-strategy)
13. [Section L — Data-Flow & State Management Architecture](#13-section-l--data-flow--state-management-architecture)
14. [Section M — API Integration Boundaries & Contracts](#14-section-m--api-integration-boundaries--contracts)
15. [Section N — Zero-Actuation & Data-Honesty Boundary (T-1…T-7)](#15-section-n--zero-actuation--data-honesty-boundary-t-1t-7)
16. [Section O — Accessibility Model (WCAG 2.1 AA/AAA)](#16-section-o--accessibility-model-wcag-21-aaaaa)
17. [Section P — Performance Model & Latency Targets](#17-section-p--performance-model--latency-targets)
18. [Section Q — Testing Strategy & Quality Assurance](#18-section-q--testing-strategy--quality-assurance)
19. [Section R — Verification & Level-I/II Evidence Methodology](#19-section-r--verification--level-iii-evidence-methodology)
20. [Section S — Governance Controls & Controlling Instruments](#20-section-s--governance-controls--controlling-instruments)
21. [Section T — Risk Register & Mitigation Strategy](#21-section-t--risk-register--mitigation-strategy)
22. [Section U — Technical Debt Reconciliation](#22-section-u--technical-debt-reconciliation)
23. [Section V — Phase-by-Phase Delivery Roadmap (P01 through P06)](#23-section-v--phase-by-phase-delivery-roadmap-p01-through-p06)
24. [Section W — Objective Acceptance Criteria Matrix](#24-section-w--objective-acceptance-criteria-matrix)
25. [Section X — Evidence Requirements & Verification Commands](#25-section-x--evidence-requirements--verification-commands)
26. [Section Y — Completion Definition & Handover Gate](#26-section-y--completion-definition--handover-gate)
27. [Section Z.1 — Explicit Answers to the 22 Mandatory Operator Questions](#27-section-z1--explicit-answers-to-the-22-mandatory-operator-questions)
28. [Section Z.2 — Open Questions & Resolutions for ITRGA](#28-section-z2--open-questions--resolutions-for-itrga)

---

# 1. Executive Summary & Charter

### 1.1 The Operator Directive
On 2026-08-12, the AXIOM Operator issued a binding directive mandating a **clean rebuild of the AXIOM user interface as an institutional trading terminal**. 

The directive determined that while previous UI transformation workstreams through `UI-011` successfully instituted critical foundational engineering (1,017 passing platform tests, WCAG 2.1 AA accessibility, strict token consumption, zero-actuation security invariants, and responsive shell mechanics), the resulting presentation remained an administrative, documentation-heavy operations dashboard rather than a high-density, cohesive trading terminal.

### 1.2 The Clean-Build Principle
Under §4 of the Directive:
- **Existing Implementation is Engineering Capital**: Reusable, battle-tested services (REST API client, WebSocket consumers, authentication, design tokens, formatters, and testing harnesses) are recovered and leveraged.
- **New UI Built From First Principles**: The terminal experience is redesigned from first principles around the workflow of a professional institutional quantitative research and trading desk.

---

# 2. Section A — Workstream Objective & Scope

### 2.1 Primary Objective
Replace the fragmented, card-stacked dashboard presentation with an integrated, high-information-density **Institutional Trading Terminal** that provides immediate market visibility, first-class TradingView candlestick charting, live spread and tick rate monitoring, quantitative signal attribution, macroeconomic intelligence, and risk oversight within a unified multi-pane layout.

### 2.2 Scope Boundaries
- **In-Scope**:
  - Full-bleed multi-pane trading terminal shell with persistent global ticker header.
  - Multi-asset watchlist dock (Forex & Crypto pairs) with real-time spread and price change telemetry.
  - Primary interactive candlestick charting stage (`LightweightCharts` / TradingView) with multi-timeframe controls (M1, M5, 15M, 1H, 4H, 1D), technical indicator overlays, and drawing tools.
  - Quantitative advisory signal stream with calibrated confidence gauges, uncertainty bounds, and explainability attribution.
  - Institutional intelligence & cross-asset correlation matrix viewer.
  - Risk & portfolio exposure decomposition dock.
  - Read-only simulated execution journal & research planning surfaces.
  - Terminal Command Palette (`Ctrl+K` / `Cmd+K`) for rapid keyboard-driven instrument and timeframe navigation.
- **Out-of-Scope (Explicit Exclusions)**:
  - Live broker execution, order routing, or buy/sell execution affordances (Gate CLOSED).
  - External AI SDK integrations.
  - Backend schema migrations or database mutations (Alembic Head `20260717_0037` locked).
  - Mobile viewports <768px (Deferred per Design Plan §10).

---

# 3. Section B — Product Vision & Institutional Experience Model

### 3.1 Terminal vs. Administrative Dashboard
| Attribute | Previous Administrative Dashboard | Target Institutional Trading Terminal |
|---|---|---|
| **Primary Visual Focus** | Sprawling text cards, server health metrics, database stats | **Live Candlestick Chart, Ticker Header, Market Watchlist** |
| **Information Density** | Low (large vertical spacing, text disclaimers pushing content 1000px down) | **High (compact multi-pane layout, immediate multi-asset scanability)** |
| **Operational Flow** | Fragmented page jumps across disparate routes | **Unified multi-pane workstation with docked context & activity** |
| **Visual Language** | Generic SaaS dashboard with oversized status boxes | **Precision institutional terminal (calm, dark-first, monospace tabular numbers)** |
| **Chart Positioning** | Secondary card far down the page | **First-class operational centerpiece visible immediately upon launch** |

### 3.2 Information Hierarchy Flow
The terminal enforces an intuitive mental model for trading and quantitative research:
```text
[ Global Market & Session Context ] (Persistent Header Ticker)
               ↓
[ Instrument Discovery & Watchlist ] (Asset Selector & Spread Telemetry)
               ↓
[ Primary Chart & Technical Analysis ] (Interactive Candlestick Stage)
               ↓
[ Quantitative Signals & ML Decision Support ] (Calibrated Confidence Stream)
               ↓
[ Risk & Exposure Oversight ] (Econometric & Portfolio Shock Models)
               ↓
[ Operator Research Action ] (Structured Journal & Research Planning Note)
```

---

# 4. Section C — Existing-State Assessment & Repository Inventory

### 4.1 Frontend Inventory (148 Test Suites / 603 Tests)
- **Design Tokens (`frontend/src/workstation/design/`)**:
  - `tokens.css`: 5-tier design tokens + motion (`--ix-motion-fast: 120ms`, `--ix-motion-ease`), hierarchy (`--ix-hierarchy-level-1..4`), elevation (`--ix-elevation-level-1..4`), optical typography scale (`--ix-font-size-display` down to `metadata: 0.75rem`), high-contrast overrides, and reduced-motion zeroing.
  - `theme.ts`: Typed contracts `BRAND_TOKENS`, `TYPOGRAPHY_TOKENS`, `SPACING_SCALE`, `MOTION_TOKENS`, `HIERARCHY_TOKENS`, `ELEVATION_TOKENS`, `HIGH_CONTRAST_TOKENS`.
- **Component Library (`frontend/src/components/ui/`)**:
  - Atoms: `Button`, `Input`, `Select`, `Badge`, `Card`, `StatusChip`, `Tooltip`, `Accordion`, `Skeleton`.
  - Panel Frames: `Panel`, `PanelHeader`, `PanelActionBar`, `Collapsible`.
  - Tables: `DataTable`, `SortableHeader`, `Pagination`, `formatters.ts`.
  - Overlays & Feedback: `Dialog`, `CommandPalette.css`, `Toast`, `ToastStack`, `ErrorBanner`, `EmptyState`.
- **Accessibility Primitives (`frontend/src/workstation/accessibility/`)**:
  - `SkipLink`, `RouteAnnouncer`, `SrOnly`, `focusTrap.ts`, `useKeyboardShortcuts.ts`.
- **Workspaces & Shell (`frontend/src/workstation/`)**:
  - `InstitutionalWorkspaceShell.tsx` & `.css`: Regions A–F (Header, Navigation Dock, Primary Workspace Host, Context Panel, Activity Dock, Overlay Layer).
  - Navigation: `NavigationDock.tsx`, `WorkspaceSwitcher.tsx`, `BreadcrumbTrail.tsx`.
  - Commands: `CommandRegistry.tsx`, `commandRegistry.ts`.
- **Domain Pages (`frontend/src/pages/`)**:
  - `/charts`: `ChartWorkspacePage.tsx` & `PriceChart.tsx` (TradingView LightweightCharts).
  - `/live`: `LiveMarketPage.tsx`.
  - `/signals`: `AdvisorySignalsPage.tsx`.
  - `/investigate`: `SignalInvestigationPage.tsx`.
  - `/intelligence`: `InstitutionalIntelligencePage.tsx`.
  - `/compare-scenarios`: `ScenarioComparisonPage.tsx`.
  - `/trade-plans`: `TradePlanningPage.tsx`.
  - `/journal`: `ManualJournalPage.tsx`.
  - `/execution-research`: `ExecutionResearchPage.tsx`.
  - `/portfolio-research`: `PortfolioResearchPage.tsx`.
  - `/governance`: `GovernanceEvidencePage.tsx`.

### 4.2 Backend Capabilities Inventory (414 Tests)
- **Authentication & RBAC**: `/api/v1/auth/login`, `/refresh`, `/logout`, `/ws-ticket`, `/operator/me`.
- **Market Data & Live Streaming**:
  - REST: `/api/v1/market/status`, `/stats`, `/start`, `/stop`, `/seed-history`, `/persistence/candles`.
  - WebSocket: `/ws/market` (ticket-authenticated live price ticks) and `/ws/status` (platform telemetry).
- **Quantitative Signals & Reports**:
  - Advisory signals: `/api/v1/signals/history`, `/signals/history/{id}`.
  - Analytics & Intelligence: `/api/v1/analytics/advisory-performance`, `/api/v1/intelligence/correlation-reports`, `/regime-reports`, `/scenario-reports`, `/portfolio-risk-reports`, `/signal-validation-reports`.
- **Research Collaboration & Journaling**:
  - `/api/v1/collaboration/trade-plans`, `/journal-entries`, `/chart-annotations`, `/assistant-responses`.
  - `/api/v1/platform/research-collections`, `/research-tags`.
- **Observability & Health**: `/health`, `/ready`, `/system/info`, `/api/v1/metrics`, `/api/v1/alerts`.

---

# 5. Section D — Existing-Asset Reconciliation Matrix

```text
Asset reconciliation repository: /home/user/axiom (DA-local workspace)
Branch: migration/ui008-da-itrga-reset (DA-local, not yet pushed)
HEAD: Committed on-tree
Working tree state: clean
```

| Existing Asset Path | Existence (Local) | Classification | Technical Rationale | Target Role in UI-NEW | Target Phase | Dependencies |
|---|---|---|---|---|---|---|
| `workstation/design/tokens.css` | Present | **RETAIN** | Proven 5-tier tokens + motion + optical typography + contrast | Core design system tokens | P01–P06 | None |
| `workstation/design/theme.ts` | Present | **RETAIN** | Typed token contracts (`TYPOGRAPHY_TOKENS`, `MOTION_TOKENS`) | Central theme contract | P01–P06 | `tokens.css` |
| `components/ui/` (20+ primitives) | Present | **RETAIN** | 100% tokenized atomic library (`Button`, `DataTable`, `Dialog`, etc.) | Terminal UI building blocks | P01–P06 | `tokens.css` |
| `api/client.ts` | Present | **RETAIN** | Robust authenticated REST API client | Backend data integration | P01–P05 | Backend REST APIs |
| `hooks/useLiveMarket.ts` | Present | **RETAIN** | Ticket-authenticated WebSocket streaming with reconnection | Live market feed consumer | P01–P03 | `/ws/market` |
| `workstation/accessibility/` | Present | **RETAIN** | WCAG 2.1 AA/AAA bypass links, live route announcer, focus traps | Accessibility subsystem | P01–P06 | `tokens.css` |
| `components/chart/PriceChart.tsx` | Present | **ADAPT** | TradingView `lightweight-charts` canvas with dynamic token resolver | Centerpiece chart canvas | P03 | `lightweight-charts` |
| `workstation/commands/` | Present | **ADAPT** | Command palette with focus restoration and shortcut manager | Terminal Command Palette | P01 | `useKeyboardShortcuts` |
| `workstation/components/InstitutionalWorkspaceShell.tsx` | Present | **REWORK** | Refactor from single-column dashboard into multi-pane terminal grid | Full-bleed terminal shell | P01 | Terminal layout tokens |
| `pages/ChartWorkspacePage.tsx` | Present | **REWORK** | Relocate chart to primary top-center stage; remove bulky card stacks | Terminal Chart Workspace | P03 | `PriceChart.tsx` |
| `pages/LiveMarketPage.tsx` | Present | **ADAPT** | Embed spread telemetry into right/bottom docks | Terminal Spread Telemetry | P02 | `useLiveMarket.ts` |
| `pages/DashboardPage.tsx` (`/`) | Present | **REPLACE** | Replace root server health dashboard with Unified Trading Terminal | Root Terminal Workstation | P01 | `TerminalMultiPaneLayout` |

---

# 6. Section E — Target Trading Terminal Architecture

```text
+---------------------------------------------------------------------------------------------------------------+
| AXIOM TERMINAL | EUR/USD 1.08450 (+0.35%) | SPREAD: 0.8 | VOL: 14.2M | WS: LIVE [●] | GATE: CLOSED [RESEARCH]  |
+---------------------------------------------------------------------------------------------------------------+
| WATCHLIST      | CHART WORKSPACE (TradingView Candlestick Engine)               | ADVISORY SIGNALS & ML       |
| EUR/USD 1.0845 | [1m] [5m] [15m] [1h] [4h] [1D] | [Candles▼] | [Start Feed] [Seed] | Pair: EUR/USD | M1          |
| GBP/USD 1.2912 | +------------------------------------------------------------+ | Signal: POSITIVE_BIAS (94%) |
| USD/JPY 154.20 | |  ▲  [Price Candlesticks with Real-Time Tick Updates]       | | ECE: 0.042 | Brier: 0.118   |
| BTC/USD 64,250 | |                                                            | | Guardrail: VALID DOMAIN     |
| ETH/USD  3,420 | |                                                            | | Lineage: model.v1 / feat.v1 |
|                | |                                                            | +-----------------------------+
|                | |                                                            | SPREAD & MARKET TELEMETRY     |
|                | |                                                            | Current Spread: 0.8 pts       |
|                | |  ▼  [Volume Histogram & Technical Indicator Sub-Panels]    | Tick Freq: 2.0s · Vol: 14.2M  |
|                | +------------------------------------------------------------+ | Posture: live:simulated     |
+----------------+--------------------------------------------------------------+-------------------------------+
| TERMINAL DOCK  | [Trade Plans] [Research Journal] [Econometric Scenarios] [Correlation Matrix] [Audit Log]    |
| Telemetry: active | Last tick: 1.08450 at 09:14:22Z | Non-actuating institutional research environment        |
+---------------------------------------------------------------------------------------------------------------+
```

---

# 7. Section F — UX Principles & Visual Direction

1. **Information Density without Chaos**: Utilize 4px/8px micro-spacing grid to maximize visual information throughput without visual clutter.
2. **Dark-First Institutional Aesthetics**: High-contrast Midnight Black (`#0B0E14`), Graphite (`#1A1F2C`), Electric Blue (`#2563EB`), Emerald Green (`#10B981`), and Ruby Red (`#EF4444`).
3. **Optical Monospace Precision**: All numeric prices, spreads, percentages, and metrics formatted with `font-family: var(--ix-font-mono)` and `font-variant-numeric: tabular-nums; text-align: right;`.
4. **Immediate Interaction Feedback**: Micro-interactions standardized to `120ms` (`var(--ix-motion-fast)`) with subtle tactile active states (`scale(0.98)` / `filter: brightness(0.95)`).
5. **Honest & Non-Fabricated Telemetry**: Explicit visual states for `Loading`, `Empty`, `Stale`, `Disconnected`, `Unauthorized`, `Research-Only`, and `Degraded`.
6. **Doc 8 Supersession / Displacement Disclosure**: Under Operator Directive §1 and pending amendment GA-167, the legacy card-stacked layout and multi-window popout detachment mandated by `08_UI_UX_SPEC.md` are displaced in favor of a modern, unified multi-pane docked terminal workstation.

---

# 8. Section G — Information Architecture & Hierarchy

- **Level 1 (Mission-Critical Telemetry / 700 Weight)**: Live candlestick chart, real-time bid/ask prices, active signal bias, primary ticker.
- **Level 2 (Active Context & Signals / 600 Weight)**: Timeframe controls, watchlist quote rows, confidence percentages, spread telemetry.
- **Level 3 (Supporting Analytics / 500 Weight)**: Correlation matrix heatmaps, scenario shock summaries, research journal entries.
- **Level 4 (Administrative & Meta / 400 Weight)**: Audit trail timestamps, database connection badges, disclaimers, documentation links.

---

# 9. Section H — Workspace Architecture & Multi-Pane Layout

The terminal consolidates the previous 14 separate pages into **4 Core Workstation Contexts**:
1. **Live Trading & Charting Workstation (Primary)**: Unified multi-pane layout combining Watchlist, Candlestick Chart, Spread Telemetry, and Signal Stream.
2. **Quantitative Intelligence & Research Workstation**: Cross-asset correlation matrix, market regime classifier, and macroeconomic scenario simulator.
3. **Signal Investigation & Lineage Workstation**: Deep-dive feature attribution, anomaly inspection, and uncertainty calibration curves.
4. **Governance, Evidence & Audit Workstation**: Model artifact verification, audit event explorer, platform health posture, and operator settings.

---

# 10. Section I — Navigation Architecture & Command System

- **Terminal Command Palette (`Ctrl+K` / `Cmd+K`)**: Rapid keyboard search for symbols (`EURUSD`, `BTCUSD`), timeframes (`1m`, `5m`, `1h`, `1d`), workspaces, research reports, and layout toggles.
- **Compact Activity Dock**: Minimizable bottom dock providing instant tab switching between Trade Plans, Research Journal, Correlation Analytics, and Audit Logs.
- **Keyboard Shortcut Mapping**:
  - `Alt+T`: Open Terminal Trading Workstation
  - `Alt+C`: Focus Candlestick Chart Stage
  - `Alt+W`: Toggle Watchlist Panel
  - `Alt+S`: Focus Advisory Signal Stream
  - `Alt+I`: Open Quantitative Intelligence
  - `Alt+G`: Open Governance & Audit
  - `Ctrl+K`: Open Command Palette
  - `Esc`: Close Overlays / Reset Focus

---

# 11. Section J — Component Architecture & Terminal Primitives

```text
frontend/src/
├── components/
│   ├── terminal/
│   │   ├── TerminalTopTicker.tsx          (Persistent global ticker & session bar)
│   │   ├── TerminalMultiPaneLayout.tsx     (Full-bleed grid layout engine)
│   │   ├── TerminalWatchlistDock.tsx      (Multi-asset watchlist & quote list)
│   │   ├── TerminalChartStage.tsx         (TradingView canvas + timeframe toolbar)
│   │   ├── TerminalSpreadTelemetry.tsx    (Real-time spread & tick rate monitor)
│   │   ├── TerminalSignalStream.tsx       (ML advisory signals & confidence gauges)
│   │   ├── TerminalBottomDock.tsx         (Tabbed analytics & research drawer)
│   │   └── TerminalGovernanceBadge.tsx    (Compact governance & non-actuating indicator)
│   ├── chart/
│   │   └── PriceChart.tsx                 (Dynamic token-resolved TradingView canvas)
│   └── ui/                                (Retained 20+ atomic primitives)
```

---

# 12. Section K — Design-System & Token Strategy

- **Pure Token Consumption (`var(--ix-*)`)**: Zero ad-hoc hex literals outside `tokens.css`.
- **Contrast Ratios**: Verified >4.5:1 (WCAG 2.1 AA) and >7:1 (WCAG 2.1 AAA) across dark surfaces.
- **Typography Scale**:
  - Display Title: `1.5rem` (`--ix-font-size-display`)
  - Workspace/Ticker Title: `1.2rem` (`--ix-font-size-workspace-title`)
  - Section Heading: `1.0rem` (`--ix-font-size-section-heading`)
  - Panel Heading: `0.85rem` (`--ix-font-size-panel-heading`)
  - Body Text: `0.9rem` (`--ix-font-size-body`)
  - Metadata / Monospace: `0.75rem` (`--ix-font-size-metadata`)

---

# 13. Section L — Data-Flow & State Management Architecture

```text
[ Backend FastAPI / Database ]
        │
        ├── WebSocket (/ws/market) ──► useLiveMarket Hook ──► TerminalWatchlist & Spread
        ├── WebSocket (/ws/status) ──► usePlatformTelemetry ──► TerminalTopTicker Status
        └── REST (/api/v1/...)     ──► useChartData Hook    ──► PriceChart (Bars & Annotations)
```

---

# 14. Section M — API Integration Boundaries & Contracts

- All backend endpoints remain strictly **read-only and non-actuating**.
- Validated REST Seams: `/api/v1/market/status`, `/api/v1/market/seed-history`, `/api/v1/persistence/candles`, `/api/v1/signals/history`, `/api/v1/collaboration/trade-plans`, `/api/v1/collaboration/journal-entries`, `/api/v1/collaboration/chart-annotations`, `/api/v1/intelligence/*`.
- Zero database schema migrations or backend mutations required.

---

# 15. Section N — Zero-Actuation & Data-Honesty Boundary (T-1…T-7)

The proposed terminal design strictly pre-registers the defining governance boundaries:

- **T-1 ZERO ACTUATION (Directive §18)**: Zero Buy/Sell buttons, order tickets, broker connection mutations, account mutations, execution triggers, automated trading triggers, or execution shortcuts. The terminal is strictly `RESEARCH-ONLY · NON-ACTUATING`.
- **T-2 SPREAD & MARKET TELEMETRY IS DISPLAY-ONLY**: The market spread monitor, tick telemetry, and price cards carry zero click-to-trade affordances and are explicitly labeled as simulated telemetry.
- **T-3 READ-ONLY TRADING REPRESENTATIONS**: Position, order, and account views represent existing simulated records. Zero fictitious controls or unbacked data paths are rendered.
- **T-4 ZERO EXTERNAL LLM (§19)**: Zero dependencies on external AI APIs (OpenAI, Anthropic, LangChain). The dependency set remains strictly locked to `lightweight-charts`, `react`, `react-dom`, `react-router-dom`.
- **T-5 ASSISTANT IS SUBORDINATE (§10)**: AI capabilities remain supporting advisory features, explicitly labeled `RESEARCH-ONLY · NON-ACTUATING`.
- **T-6 DATA HONESTY & PROVENANCE LABELING (§20)**: The terminal never fabricates prices, positions, orders, signals, or confidence values. Explicit states for `Loading`, `Empty`, `Stale`, `Disconnected`, `Unauthorized`, `Research-Only`, and `Degraded` are enforced at the point of display. Simulated streams are prominently labeled `live:simulated` and `seed:synthetic`.
- **T-7 INSTITUTIONAL SECURITY PRESERVATION (§17)**: Authenticated access, RBAC, secure tokens, and zero DOM vulnerabilities (`dangerouslySetInnerHTML = 0`, `eval = 0`).

---

# 16. Section O — Accessibility Model (WCAG 2.1 AA/AAA)

- Complete keyboard navigation with logical tab indexing.
- Modal focus traps (`Dialog`, `CommandPalette`) and focus restoration.
- Screen-reader announcements via `RouteAnnouncer` (`aria-live="polite"`).
- High-contrast mode (`@media (prefers-contrast: more)`) and reduced-motion zeroing (`@media (prefers-reduced-motion: reduce)`).

---

# 17. Section P — Performance Model & Latency Targets

| Metric | Target | Measurement Method |
|---|---|---|
| Initial Terminal Load | `< 1.2s` | Lighthouse / Performance Navigation Timing |
| Workspace / Route Switch | `< 50ms` | React Profiler / User Timing API |
| Chart Render (60fps) | `< 16ms` | RequestAnimationFrame / Canvas Profiler |
| WebSocket Tick-to-DOM | `< 10ms` | Performance.now() delta on `onmessage` |
| Command Palette Open | `< 20ms` | React State Transition |

---

# 18. Section Q — Testing Strategy & Quality Assurance

- **Vitest & React Testing Library**: Component unit tests, interaction tests, and integration harnesses.
- **Pytest**: Backend API contracts, WebSocket ticket issuance, database persistence.
- **Grep Invariant Tests**: Automated security checks verifying zero actuation, zero LLM, zero dangerous innerHTML, and zero ad-hoc hex.
- **Zero Regression Rule**: All 1,017 existing platform tests must remain passing.

---

# 19. Section R — Verification & Level-I/II Evidence Methodology

- **Level-I Browser Evidence Methodology (OBS-4)**:
  - *Producer*: Operator / DA executing the local build in a real browser (Chrome/Edge/Firefox).
  - *Form*: Full-bleed 1920x1080 visual viewport screenshots, DOM tree accessibility inspection dumps, and browser interaction logs.
  - *Storage*: Committed to `docs/evidence/uinew/` and `branding/`.
  - *Acceptance*: Zero layout clipping, zero NaN/undefined text fields, verified WCAG contrast >4.5:1, strict visual fidelity to target terminal layout.
- **Level-II Automated Engineering Evidence**: Full Vitest test logs, Pytest logs, `tsc -b` logs, Vite build logs, grep transcripts.
- **Level-III Documentary Evidence**: 20-section Delivery Reports, Design Plans, Diff logs.

---

# 20. Section S — Governance Controls & Controlling Instruments

The workstream operates under verified controlling instruments:
1. `QUALITY_GATE_SPEC.md` (Engineering Quality Gates EQG-1 through EQG-8).
2. `REPOSITORY_PROVENANCE_PROTOCOL.md` §2 (Commit worktree, annotated tags, provenance verification).
3. `12_INSTITUTIONAL_UI_TRANSFORMATION_PLAN.md` §14 & `13_UI_TRANSFORMATION_MASTER_PLAN.md`.
4. `16_BRAND_GOVERNANCE_STANDARD.md` (Brand token conformance & contrast).
5. Operator Directive §§26–32 (Single Active Phase, 20-section delivery reports, independent review).

---

# 21. Section T — Risk Register & Mitigation Strategy

| Risk ID | Description | Severity | Mitigation Strategy |
|---|---|---|---|
| **RSK-NEW-01** | Scope creep during clean rebuild | High | Strict adherence to phase-by-phase Build Orders; all features outside active BO strictly excluded. |
| **RSK-NEW-02** | TradingView Canvas color parsing failure | Medium | Use `getComputedToken` dynamic resolver reading computed CSS variables before passing to canvas. |
| **RSK-NEW-03** | Regression of previous workspace tests | High | Preserve compatibility aliases and update component props cleanly while maintaining test contracts. |
| **RSK-NEW-04** | Performance degradation under high-frequency ticks | Medium | Batch WebSocket state updates via `useLiveMarket` timestamp windowing. |

---

# 22. Section U — Technical Debt Reconciliation (CA-4 / C-2)

Reconciliation against `docs/governance/TECHNICAL_DEBT_REGISTER.md` (v3.0.12):

| ID | Register State | Relevance to UI-NEW |
|---|---|---|
| **`TD-UI-POSTCSS-HIGH`** | **CLOSED** (Line 116) | Remediation verified with `postcss@8.5.23` (exit 0). Non-blocking. |
| **`TD-AXIOM-DEV-CREDENTIAL-LITERALS`** | **OPEN** (Doc 11 §2 pre-cert blocker) | Disclosed as open debt under ITRGA D-2 disposition. Governed under separate security remediation. |
| **`TD-UI-REACTROUTER-MODERATE`** | **OPEN** (Line 117) | Disclosed as non-blocking moderate advisory. |
| **`TD-005`** | **OPEN** (Handcrafted CSS / no tokens) | UI-NEW enforces 100% pure token consumption (`var(--ix-*)`) across all new terminal surfaces. |
| **`TD-008` / `TD-060` / `TD-086` / `TD-089` / `TD-092` / `TD-093` / `TD-099`** | **OPEN** (No automated browser E2E) | UI-NEW utilizes Level-I browser render captures and Vitest integration harnesses pending future Playwright unit. |
| **`TD-021`** | **OPEN** (Simulated live only) | UI-NEW binds T-6 data honesty, labeling simulated streams as `live:simulated` at point of display. |
| **`TD-029`** | **OPEN** (Multi-TF UI vs M1 sim) | UI-NEW provides multi-timeframe switching (M1, M5, 1H, 1D) with honest resolution notice. |

- **New Technical Debt**: **0 (Zero)**.

---

# 23. Section V — Phase-by-Phase Delivery Roadmap (P01 through P06)

```text
[ P01: Terminal Foundation & Shell ] ──► [ P02: Watchlist & Spread Telemetry ] ──► [ P03: Primary Chart Stage ]
                                                                                          │
[ P06: Whole-Terminal Handover ]   ◄── [ P05: Risk, Portfolio & Journal ]    ◄── [ P04: Signals & Intelligence ]
```

### Phase Specifications & 8-Factor Justification:

#### Phase P01 — Terminal Foundation & Multi-Pane Shell Architecture
- **Objective**: Establish the unified full-bleed trading terminal shell, persistent global ticker header, terminal layout tokens, and workspace state manager.
- **8-Factor Boundary Justification**:
  1. *Architectural Boundaries*: Establishes the foundational presentation grid (`TerminalMultiPaneLayout`) and persistent global state layer without domain coupling.
  2. *UX Dependencies*: Foundational prerequisite for all docked panels (ticker bar and layout slots must exist before docking watchlists or charts).
  3. *Risk*: Minimal (layout and presentation scaffolding; zero domain computation).
  4. *Testability*: Highly isolated unit tests verifying DOM landmark mounting and responsive reflow (`terminalShell.test.tsx`).
  5. *Security*: Enforces zero-actuation scaffolding and clean authenticated session boundaries.
  6. *Integration Complexity*: Low (shell composition only).
  7. *Operator Workflow*: Establishes immediate top-level terminal orientation and session clock visibility.
  8. *Verification Requirements*: Level-I browser viewport capture + Level-II Vitest shell tests.
- **Deliverables**:
  - `TerminalTopTicker.tsx`: Live ticker bar (symbol, price, 24h change, high/low, clock, WS status, governance badge).
  - `TerminalMultiPaneLayout.tsx`: Multi-pane grid container with docked panel slots.
  - Restructure default route (`/`) to mount the unified trading terminal workstation.
  - Test harness `terminalShell.test.tsx` + security invariants.

#### Phase P02 — Market Watchlist & Real-Time Spread Telemetry Surface (Re-scoped per C-1)
- **Objective**: Build the multi-asset watchlist and live spread / tick rate telemetry dock.
- **8-Factor Boundary Justification**:
  1. *Architectural Boundaries*: Bounded to market telemetry consumers (`/api/v1/market/status` and `/ws/market`).
  2. *UX Dependencies*: Depends on P01 left/right dock slots; provides active symbol selection for P03 chart.
  3. *Risk*: T-2 spread telemetry must be strictly display-only with zero click-to-order affordances; zero synthetic order-book fabrication.
  4. *Testability*: Deterministic mock quote feed testing (`terminalWatchlistDepth.test.tsx`).
  5. *Security*: Enforces T-6 data honesty (labeled `live:simulated` at point of display).
  6. *Integration Complexity*: Medium (WebSocket streaming integration).
  7. *Operator Workflow*: Allows rapid instrument discovery and spread comparison across Forex and Crypto pairs.
  8. *Verification Requirements*: WebSocket tick stream latency proof + Level-I spread telemetry rendering snapshot.
- **Deliverables**:
  - `TerminalWatchlistDock.tsx`: Multi-asset watchlist (Forex & Crypto) with real-time price quotes, search, and active symbol switching.
  - `TerminalSpreadTelemetry.tsx`: Real-time spread points, tick frequency, session volume profile, and candle volatility.
  - Test harness `terminalWatchlistDepth.test.tsx` + security invariants.

#### Phase P03 — Primary Chart Stage & Technical Analysis Workspace
- **Objective**: Transform the candlestick chart into the terminal's first-class centerpiece.
- **8-Factor Boundary Justification**:
  1. *Architectural Boundaries*: Bounded to TradingView Canvas engine (`lightweight-charts`) and historical candle storage (`/api/v1/persistence/candles`).
  2. *UX Dependencies*: Consumes active symbol/timeframe from P01/P02; provides visual substrate for P04 signal overlays.
  3. *Risk*: Canvas token parsing resilience (preventing black-void crashes via `getComputedToken`).
  4. *Testability*: Canvas resize observation, timeframe switching, and annotation store verification (`terminalChartStage.test.tsx`).
  5. *Security*: Zero client-side indicator recomputation or trade execution shortcuts.
  6. *Integration Complexity*: High (Canvas drawing, multi-timeframe resolution, drawing annotations).
  7. *Operator Workflow*: Primary visual analysis stage for price action, support/resistance, and volume profiling.
  8. *Verification Requirements*: Level-I interactive chart screenshot + 60fps frame timing verification.
- **Deliverables**:
  - `TerminalChartStage.tsx`: Full-height interactive TradingView candlestick chart stage positioned directly at top-center.
  - Integrated timeframe toolbar (`M1`, `M5`, `15M`, `1H`, `4H`, `1D`), chart style toggles (`Candles`, `Bar`, `Line`, `Area`), and feed controls (`Start Feed`, `Seed Data`).
  - Interactive technical overlays, research annotations (`/api/v1/collaboration/chart-annotations`), and drawing tools.
  - Test harness `terminalChartStage.test.tsx` + security invariants.

#### Phase P04 — Quantitative Signals, Intelligence & Uncertainty Stream
- **Objective**: Integrate quantitative machine learning signals and market intelligence into the terminal.
- **8-Factor Boundary Justification**:
  1. *Architectural Boundaries*: Bounded to signal history (`/api/v1/signals/history`) and intelligence analytics (`/api/v1/intelligence/*`).
  2. *UX Dependencies*: Docks into P01 right-dock and overlays visual markers onto P03 chart canvas.
  3. *Risk*: Signals must remain strictly advisory research notes (`RESEARCH-ONLY · NON-ACTUATING`).
  4. *Testability*: Deterministic statistical formatter testing for Wilson intervals, ECE, and Brier scores (`terminalSignalsIntelligence.test.tsx`).
  5. *Security*: T-4 zero external LLM enforcement and T-5 assistant subordination.
  6. *Integration Complexity*: Medium (statistical metric formatting and uncertainty interval rendering).
  7. *Operator Workflow*: Provides quantitative decision support with explainable feature attribution.
  8. *Verification Requirements*: Calibration curve DOM snapshots + mathematical formatter tests.
- **Deliverables**:
  - `TerminalSignalStream.tsx`: Live quantitative advisory signal feed with calibrated confidence gauges, uncertainty bounds, and model attribution.
  - Docked intelligence cards (cross-asset correlation, market regime detection).
  - Test harness `terminalSignalsIntelligence.test.tsx` + security invariants.

#### Phase P05 — Risk, Portfolio Analytics & Research Journal
- **Objective**: Integrate risk exposure monitors, scenario shock analytics, and research journaling into the terminal bottom dock.
- **8-Factor Boundary Justification**:
  1. *Architectural Boundaries*: Bounded to trade planning (`/api/v1/collaboration/trade-plans`), manual journal (`/api/v1/collaboration/journal-entries`), and risk reports (`/api/v1/intelligence/portfolio-risk-reports`).
  2. *UX Dependencies*: Docks into P01 bottom analytics drawer; contextualized by P02/P03 active instruments.
  3. *Risk*: T-3 read-only trading representations; trade plans are inert research notes only.
  4. *Testability*: Form state validation, tabbed drawer switching, and audit hash verification (`terminalRiskJournal.test.tsx`).
  5. *Security*: Zero position modification or broker order placement.
  6. *Integration Complexity*: Medium (tabbed multi-view state and audit trail persistence).
  7. *Operator Workflow*: End-of-cycle trade reflection, risk limit verification, and structured research documentation.
  8. *Verification Requirements*: Level-I drawer tab captures + journal persistence verification.
- **Deliverables**:
  - `TerminalBottomDock.tsx`: Tabbed multi-drawer for Trade Planning Notes (`/api/v1/collaboration/trade-plans`), Research Journal (`/api/v1/collaboration/journal-entries`), Macro Scenarios, and Audit Logs.
  - Risk & drawdown decomposition viewer.
  - Test harness `terminalRiskJournal.test.tsx` + security invariants.

#### Phase P06 — Whole-Terminal Integration, Visual Audit & Handover
- **Objective**: Final whole-surface visual audit, regression validation, whole-frontend token audit, and handover to Production Readiness Certification.
- **8-Factor Boundary Justification**:
  1. *Architectural Boundaries*: Programme-wide whole-surface synthesis across all terminal panes and existing routes.
  2. *UX Dependencies*: All P01–P05 subsystems fully operational and verified.
  3. *Risk*: Final gatekeeper before Production Readiness Certification (`11_PRODUCTION_READINESS_CERTIFICATION.md`).
  4. *Testability*: Whole-surface integration harness (`terminalWholeSurface.test.tsx`) + 1,017+ regression baseline.
  5. *Security*: Whole-frontend AST grep audit (0 ad-hoc hex outside `tokens.css`, 0 actuation, 0 LLM).
  6. *Integration Complexity*: Low (verification and governance closure).
  7. *Operator Workflow*: Complete end-to-end institutional quantitative research workflow validated.
  8. *Verification Requirements*: Full Level-I and Level-II evidence package committed on-tree.
- **Deliverables**:
  - Whole-surface integration test harness `terminalWholeSurface.test.tsx`.
  - Whole-frontend token audit (0 ad-hoc hex outside `tokens.css`).
  - Final project-state synchronization and delivery report for declaration of `UI-NEW COMPLETE`.

---

# 24. Section W — Objective Acceptance Criteria Matrix

| Phase | Core Deliverable | Acceptance Criteria |
|---|---|---|
| **P01** | Terminal Shell & Ticker | Global ticker header renders persistent price, 24h change, clock, WS status; multi-pane grid mounts without DOM collisions. |
| **P02** | Watchlist & Spread Telemetry | Multi-asset watchlist switches symbols instantly; spread telemetry renders live spread points and tick rate without synthetic book fabrication. |
| **P03** | Primary Chart Stage | TradingView candlestick chart renders at top-center; timeframes switch seamlessly; 100% tokenized canvas colors. |
| **P04** | Signals & Intelligence | ML advisory signals render with calibrated confidence percentages; uncertainty intervals format deterministically. |
| **P05** | Risk, Scenarios & Journal | Bottom dock tabs switch smoothly without layout jumps; research notes save to audit log. |
| **P06** | Whole-Terminal Handover | 100% platform tests pass; 0 ad-hoc hex across `frontend/src`; 0 actuation; clean `tsc -b && vite build`. |

---

# 25. Section X — Evidence Requirements & Verification Commands

For each phase, the DA will capture and commit 12 Level II evidence logs in `docs/evidence/uinew/`:
1. `vitest.log`: Full frontend test suite execution.
2. `pytest.log`: Full backend test suite execution.
3. `tsc.log` & `vite_build.log`: TypeScript compilation and production build packaging (`exit 0`).
4. `grep_actuation.log`: Whole-repo actuation grep (`exit 1`).
5. `grep_llm.log`: External LLM grep (`exit 1`).
6. `grep_sandbox_danger.log`: `dangerouslySetInnerHTML` grep (`exit 1`).
7. `grep_eval.log`: `eval` / `new Function` grep (`exit 1`).
8. `grep_ad_hoc_hex.log`: Whole-frontend ad-hoc hex grep outside `tokens.css` (`exit 1`).
9. `grep_secrets.log`: Secrets scan (`exit 1`).
10. `accessibility.log`: WCAG 2.1 AA/AAA visual audit transcript.
11. `project_state_diff.log` & `changelog_diff.log`: Git diffs.

---

# 26. Section Y — Completion Definition & Handover Gate

The `UI-NEW` transformation programme shall be declared **`UI-NEW COMPLETE`** only when:
1. The AXIOM interface functions and visually presents as an uncompromised **Institutional Trading Terminal**.
2. All 6 implementation phases (P01 through P06) have been approved by the ITRGA.
3. All platform tests pass with 100% success (0 regressions).
4. All 5 constitutional security invariants remain fully verified.
5. The terminal is formally handed over to **`11_PRODUCTION_READINESS_CERTIFICATION.md`**.

---

# 27. Section Z.1 — Explicit Answers to the 22 Mandatory Operator Questions

### 1. What should the final AXIOM terminal look like?
A sleek, high-information-density, dark-first institutional trading workstation (akin to professional terminals like TradingView Pro, Bloomberg, and Refinitiv Eikon), centered around a prominent live candlestick charting canvas, persistent top ticker bar, multi-asset watchlist, real-time spread telemetry, quantitative signal stream, and tabbed analytics drawer.

### 2. What should the operator be able to do?
The operator should be able to instantly monitor multi-asset market prices, inspect multi-timeframe candlestick price action, analyze ML advisory signals and calibrated confidence scores, review cross-asset correlation and macroeconomic scenarios, create research annotations, and log trade plans—all within a unified, keyboard-navigable terminal.

### 3. What information should always be visible?
The **Persistent Global Ticker Bar** (Symbol, Bid/Ask, 24h Change, High/Low, Session Clock, WebSocket Connection Health, and Governance Gate Status) and the **Primary Candlestick Chart Stage**.

### 4. What information should be contextual?
Technical indicators, drawing tool properties, deep econometric feature lineage, uncertainty interval drill-downs, trade planning forms, and audit trail records (accessible via docked side panels or the bottom drawer).

### 5. What existing UI should be retained?
All 20+ tokenized UI primitives (`Button`, `Badge`, `DataTable`, `Dialog`, `Toast`, etc.), design tokens (`tokens.css`, `theme.ts`), accessibility utilities (`SkipLink`, `RouteAnnouncer`), API client, and WebSocket hooks.

### 6. What should be adapted?
`PriceChart.tsx` (elevated to full-height primary stage with dynamic token resolution), `CommandRegistry.tsx` (expanded terminal commands), and `LiveMarketPage.tsx` (converted into a docked spread telemetry panel).

### 7. What should be reworked?
`ChartWorkspacePage.tsx` (reorganized to put the chart and ticker toolbar at top-center) and `InstitutionalWorkspaceShell.tsx` (refactored from a generic dashboard frame into a multi-pane terminal grid).

### 8. What should be replaced?
The root administrative Operations Dashboard (`DashboardPage.tsx` at `/`), replaced by the **Unified Institutional Trading Terminal**.

### 9. What should be removed?
Oversized 200px text disclaimer cards and redundant administrative status tables that previously pushed the chart 1,000px down the page.

### 10. What should be deferred?
Mobile viewports (<768px) and multi-window popout detachment (deferred to post-1.0 to focus on a high-density unified docked terminal, acknowledging Doc 8 displacement pending Operator amendment GA-167).

### 11. What APIs already exist?
All required backend APIs already exist: `/api/v1/market/status`, `/ws/market`, `/ws/status`, `/api/v1/signals/history`, `/api/v1/analytics/*`, `/api/v1/intelligence/*`, `/api/v1/collaboration/trade-plans`, `/api/v1/collaboration/journal-entries`, `/api/v1/collaboration/chart-annotations`, and `/api/v1/auth/*`.

### 12. What APIs are missing?
An external Level-2 Order Book / Market Depth API is missing from the platform because external broker connections remain hard-closed under the Governance Gate. The terminal honestly presents candle-derived spread and tick rate telemetry instead of fabricating unbacked depth data (Directive §20 / T-6).

### 13. What frontend architecture should be used?
React 18 / TypeScript with Vite, organized into modular terminal domain components (`components/terminal/`) consuming centralized design tokens (`var(--ix-*)`) and custom React hooks (`useLiveMarket`, `useChartData`).

### 14. What workspace architecture should be used?
A **Multi-Pane Docked Grid Architecture** with a persistent top ticker, collapsible left watchlist, center chart stage, right signals/spread dock, and bottom tabbed analytics drawer.

### 15. What design-system changes are required?
None to token values; maintain pure token consumption (`var(--ix-*)`) with strict monospace `tabular-nums` right-alignment for all financial figures, supported by the `getComputedToken` dynamic canvas resolver.

### 16. What security constraints apply?
Strict Zero-Actuation default (no buy/sell order routing), Zero External AI SDKs, Zero dangerouslySetInnerHTML/eval, Zero hardcoded secrets, and authenticated RBAC.

### 17. What accessibility requirements apply?
Full WCAG 2.1 AA/AAA compliance, keyboard shortcuts (`Alt+T`, `Ctrl+K`), ARIA live regions, focus management, high-contrast palette, and reduced-motion zeroing (`0ms`).

### 18. What performance requirements apply?
Initial load `<1.2s`, workspace switch `<50ms`, chart 60fps render `<16ms`, WebSocket tick-to-DOM `<10ms`, Command Palette response `<20ms`.

### 19. How many implementation phases are actually required?
**6 discrete, technically justified phases (P01 through P06)**, bounded by clean architectural and domain boundaries.

### 20. What are the exact acceptance criteria for each phase?
Codified in Section W Acceptance Criteria Matrix.

### 21. What evidence must the DA produce?
12 Level II evidence logs in `docs/evidence/uinew/` plus 20-section Delivery Reports for each phase.

### 22. What constitutes final completion?
Formal ITRGA approval of all 6 phases, 100% regression test pass (1,017+ tests), 0 ad-hoc hex literals, 0 actuation, and successful handover to `11_PRODUCTION_READINESS_CERTIFICATION.md`.

---

# 28. Section Z.2 — Open Questions & Resolutions for ITRGA

1. **Reconciliation Source**: Asset reconciliation was performed against the **active DA-local workspace on branch `migration/ui008-da-itrga-reset`**, containing the complete 148-suite / 603-test frontend and 414-test backend codebase.
2. **UI-008…UI-011 Disposition**: The outputs of UI-008 through UI-011 (tokens, component library, accessibility primitives, chart tokenization) are present on the active DA-local branch and recovered as **engineering capital**.
3. **Doc 8 Supersession**: UI-NEW respects Operator Directive §1 and replaces the legacy card-stacked layout with a modern multi-pane docked terminal while preserving all non-negotiable core principles (uncertainty disclosure, dark-first aesthetics, WCAG accessibility, and zero actuation).
4. **Route & Registry Posture**: The root route `/` directly mounts the **Unified Institutional Trading Terminal Workstation**, while existing workspace routes (`/charts`, `/intelligence`, `/governance`, `/investigate`) remain available as specialized focus views via the Workspace Registry.
5. **Data-Source Inventory per Pane**:
   - *Top Ticker Bar*: Backed by `/ws/market` & `/ws/status` (`live:simulated`).
   - *Watchlist Dock*: Backed by `/api/v1/market/status` & `/ws/market` (`live:simulated`).
   - *Chart Stage*: Backed by `/api/v1/persistence/candles` & `/api/v1/market/seed-history` (`seed:synthetic` / `live:simulated`).
   - *Signals Dock*: Backed by `/api/v1/signals/history` (persisted research signals).
   - *Bottom Drawer*: Backed by `/api/v1/collaboration/trade-plans`, `/api/v1/collaboration/journal-entries`, `/api/v1/collaboration/chart-annotations`, and `/api/v1/intelligence/*` (persisted research artifacts).
6. **Chart Architecture**: Retains `lightweight-charts@^4.2.0` with dynamic CSS token resolution (`getComputedToken`) preventing canvas color parsing failures, supporting multi-timeframe switching and technical drawing layers.
7. **Persistence Posture**: Zero new database tables. Workspace layout preferences reuse existing `operator_workspace_preferences` (presentation settings only; no execution state).
8. **Performance Targets**: Load `<1.2s`, workspace switch `<50ms`, chart 60fps render `<16ms`, WebSocket tick-to-DOM `<10ms`, command palette `<20ms` (measured via User Timing API and performance benchmarks).
9. **Level-I Evidence Method**: Operator-verified browser captures (1920x1080) and DOM snapshots generated at each phase boundary.
10. **Phase Count Justification**: 6 phases are strictly justified across all 8 factors (architectural boundaries, UX dependencies, risk, testability, security, integration complexity, operator workflow, verification requirements).

---

**End of UI-NEW_ENGINEERING_DESIGN_PLAN.md**
