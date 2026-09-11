# AXIOM — CAPABILITY IMPLEMENTATION CHECKLIST
## Response to Operator request: which capabilities of AXIOM_COMPLETE_PLATFORM_CAPABILITIES.md are implemented, and which are not

**Date:** 2026-08-19 · **Reviewer:** AXIOM Development Authority (DA)
**Method:** Item-by-item source verification against the working tree (baseline `34f4c62` + the 16-element verified patch chain + 2 post-closure Operator directives), NOT against documentation claims. Every status below cites the file/endpoint evidence inspected this session.
**Status vocabulary** (per the catalogue's own §45 maturity model, extended):

| Status | Meaning |
|---|---|
| **IMPLEMENTED** | Code exists in the working tree and provides the capability |
| **VERIFIED** | Standing independent evidence (ITRGA determinations, capture/hash records, test logs) covers it |
| **APPROVED** | Covered by an ITRGA phase/workstream determination |
| **PARTIAL** | Implemented, with sub-items genuinely absent (each absent sub-item named) |
| **NOT IMPLEMENTED** | Not built (with the reason: deferred, gate-closed, or by design) |
| **GOVERNED ABSENCE** | Correctly absent — the constitution/gate requires it not to exist |
| **DESIGNED** | Specified/narrative only — no code claim made |
| **PRODUCTION CERTIFIED** | — not granted to any item; programme gate CLOSED |

---

## §1 Product Identity — IMPLEMENTED
The unified terminal exists as one coherent workstation: `TradingTerminalWorkspace.tsx` + `InstitutionalWorkspaceShell.tsx` mount every listed domain (market, charts, analysis, watchlists, signals, intelligence, research, investigation, scenarios, portfolio/risk, alerts, journal, lineage, governance, assistant, system status) in one shell with docks, stage views and overlays — not a collection of unrelated pages.

## §2 Core Operating Model — IMPLEMENTED (as designed)
Every step of the MARKET → INSTRUMENT → CHART → ANALYSIS → RESEARCH → INTELLIGENCE → INVESTIGATION → RISK/PORTFOLIO → DECISION SUPPORT → GOVERNANCE chain has a surface in the terminal: watchlist/telemetry → instrument context (`TerminalContext`) → chart stage → 29 indicators → ResearchHub view → intelligence dock → investigation frames → risk/scenario/portfolio bottom-dock tabs → governance overlay/badge. Operator remains decision-maker; no autonomous-actor pathway exists (§26).

## §3.1 Unified Terminal Shell — IMPLEMENTED
- Persistent identity: shell header "AXIOM Institutional Workstation · v0.62.0" (`InstitutionalWorkspaceShell.tsx`).
- Global command/search: Ctrl+K command palette (`workstation/overlays/CommandPalette.tsx`, binding at `InstitutionalWorkspaceShell.tsx:210`) + global search overlay with multi-source client index (`workstation/search/GlobalSearchOverlay.tsx`, `globalSearchSources.ts`).
- Workspace selection: `WorkspaceSwitcher.tsx` (recent workspaces + history via `workspaceHistory.ts`).
- Instrument selection: `TerminalWatchlistDock` + `TerminalContext` selected-symbol state.
- Timeframe controls: chart stage, 6 timeframes (M1/M5/M15/H1/H4/D1).
- Alerts: right dock ALERTS tab.
- Operator/session state: shell operator tag; auth session.
- Connectivity state: feed telemetry (WebSocket state, tick rate, lag).
- Governance state: `TerminalGovernanceBadge` — "GATE: CLOSED · RESEARCH-ONLY · NON-ACTUATING".
- Persistent market context: selected symbol flows to signals, intelligence, chart, watchlist.

## §3.2 Market Navigator / Watchlists — PARTIAL
IMPLEMENTED: instrument list (11 symbols FX+crypto), watchlist dock with search filter, category filter (ALL/FX/crypto), quick selection, per-row symbol, provenance-labelled price ("LIVE never claimed — source field shown", `TerminalWatchlistDock.tsx:32`), percentage change, intraperiod range (labelled "Range, never spread" — no fabricated spread), sparklines, honest per-symbol degradation (`status:"error"` when series unavailable).
NOT IMPLEMENTED: user-created/grouped watchlists (one built-in list; category filter only), sorting controls (filtering yes, sorting no), external symbol discovery (client-side search of the supported list only).

## §3.3 Instrument Workspace — PARTIAL
IMPLEMENTED: selected instrument is the central context of chart/signals/intelligence/telemetry; header shows symbol, price, change; session context strip (`SessionContextStrip.tsx` — session clock, session of bar under crosshair, Tokyo/London/New York fixed UTC windows); data state.
NOT IMPLEMENTED: bid/ask and broker spread — deliberately absent and disclosed: `TerminalMarketTelemetry` renders an explicit "Level-2 depth and broker spread are Gate-closed" notice (B-P02-1/C-1 discipline). Full instrument name/asset class: asset class inferable (FX vs crypto categories), full legal instrument name not present.

## §4 Market Data — IMPLEMENTED (VERIFIED, APPROVED — DATA-P01/DATA-P02)
- Instrument data + historical: 95,040 seeded M1 bars (11 symbols × 6 days, zero-mean walks); candle endpoints with typed responses `native/aggregated/unavailable`.
- Live/streamed where configured: WebSocket hub (`backend/app/market/hub.py`, `live_service.py`) with one-time-ticket auth (`api/routes/ws.py`, close code 4401); start/stop/subscribe/status/stats control endpoints (`api/routes/market.py`).
- Market status/session/connectivity: live feed status endpoint + telemetry + session strip.
- Data availability states: typed series kinds + honest empty states; provenance labels `seed:synthetic+live:simulated` (R4, `TerminalChartStage.tsx:328`).
- Integrity discipline confirmed: simulated data never presented as genuine; stale/unavailable states explicit.

## §5 Interactive Charting — IMPLEMENTED (VERIFIED, APPROVED — CHART-P01/P02/P03)
Lightweight-charts infrastructure in `PriceChart.tsx`; candle visualization; 6 timeframes; zoom/pan with crosshair (`CrosshairMode.Normal`) and zoom/pan-synced stacked indicator panes (CHART-P02 M7); 29 technical indicators (overlay + pane); 6 drawing tools (trendline/hline/ray/rect/fib/text — `ChartDrawingOverlay.tsx`); price levels (PIVOTCL/CAMARILLA/PREVHL/SESSLVL); signal markers (P04 banner, `chart-signal-marker-*` testids); research markers = audited chart annotations with provenance/uncertainty fields (`collaboration.py /chart-annotations`); contextual annotations with inertness validation (actuation-term rejection). Confluence strip (Wilson-95% band, non-actuating, `ConfluenceStrip.tsx`).

## §6 Technical Analysis — IMPLEMENTED, one documented exception
IMPLEMENTED (29 registered, `indicator_registry.py`): EMA20 ✓, SMA20/50 ✓, RSI14 ✓, MACD ✓, Bollinger ✓, ATR14 ✓, pivot points ✓ (PIVOTCL + CAMARILLA + PREVHL), market structure ✓ (SWINGS/STRUCT/BOS/CHOCH/FVG/Order-Block-Pattern), plus HMA, Supertrend, Ichimoku, Stochastic, CCI, ROC, ADX/DMI, Keltner, Donchian, session levels, Z-Score, percentile, regression channel.
NOT IMPLEMENTED (documented, deliberate): a volume indicator (VWMA) — registry docstring: "volume is gauss() noise uncorrelated to price; a volume-weighted indicator over noise volume is arithmetically correct and informationally empty." Raw candle volume IS displayed in telemetry. Support/resistance as a named indicator is not registered; swing/level pattern indicators cover the territory (no fabricated S/R claims).
Verified by hand-computed fixtures (required_bars = full definition: Ichimoku 78 = 52+26, HMA 23 = n+√n−1, etc.).

## §7 Signals — IMPLEMENTED (VERIFIED, APPROVED — SURF-P03 scope)
`advisory_signals.py` (GET history/detail); `TerminalSignalStream` dock with drill-down (`SignalInvestigationFrame` — rationale, guardrails, lineage, explainability, B-CONV2-2); signal metrics via validation reports (ECE, Brier, Wilson); stale/expired signals tagged with absolute UTC (B-P04-4); signal-to-evidence lineage (source artifact ids); zero client-side statistic computation (B-P04-2); advisory notes only, never trade instructions (B-P04-3).

## §8 Market Intelligence — IMPLEMENTED (VERIFIED, APPROVED — POLISH-P01 scope)
`intelligence.py` read seams: correlation reports (Pearson r + Fisher Z confidence intervals), regime reports (HMM/classifier labels + posterior uncertainty), signal-validation reports, scenario reports, portfolio-risk reports. `TerminalIntelligenceCards` dock (CALIBRATION/CORRELATION/REGIME tabs) renders server figures verbatim with uncertainty intervals (B-P04-1). Explanations, confidence/uncertainty, model info (method_version), calibration metrics, contextual intelligence (symbol-scoped). Institutional Intelligence lazy page adds the research-management bundle + journal continuity.

## §9 Research Management — IMPLEMENTED (VERIFIED, APPROVED — UI-CONV-P03 item 4)
`ResearchHubView` (full-height RESEARCH stage view): explorer frame, source inventory, catalog, metadata detail, lineage, relationships, filtering, collections (`research_collections`/`research_collection_members`), tag organization (`research_tags`), report inspection, evidence review, research status, limitations, uncertainty, provenance — with audited write seams (collection/membership/tag mutation behind strict field whitelists, `ResearchHubView.tsx:194-234`).

## §10 Research Artifact Explorer — IMPLEMENTED
`workstation/artifacts/ArtifactExplorerFrame.tsx` + catalog/metadata/lineage/relationships/collection/tag surfaces above. Functions as a structured knowledge/evidence environment, not a folder view.

## §11 Investigation — IMPLEMENTED
Instrument→Signal→Context→Research→Evidence→Intelligence→Scenario path: signal drill-down (`SignalInvestigationFrame`), execution-research context with assumptions/uncertainty/limitations and pre-registration plans with SHA-256 `plan_hash` (`workstation/investigation/`), scenario examination (`ScenarioComparisonPanel`), planning/journal continuity, evidence inspection (lineage tree + artifact ids).

## §12 Scenario Analysis — IMPLEMENTED (read-only by design)
Persisted scenario selector, side-by-side comparison, hypothetical result, assumptions, uncertainty, provenance, limitations, economic-usefulness verdict, research status, relationships (`ScenarioComparisonPanel.tsx`, `scenario_report` model). Scenario creation and client-side computation deliberately absent ("No scenario creation or client-side computation (T-1 / R3)" — panel header comment). Scenarios framed as research tools, not guarantees.

## §13 Portfolio Analytics — PARTIAL
IMPLEMENTED: `PortfolioResearchPanel` — investigation context, hypothetical aggregate figures with sample counts, uncertainty methods, economic-usefulness verdicts and source artifact ids per metric, report builder/export preview, uncertainty/limitations + included scope; backend `PortfolioResearchService` (`institutional_platform.py`).
NOT IMPLEMENTED: live account positions, exposure, allocation, performance history, and historical order information from a broker — no account/broker feed exists (gate-closed); the only order-like records are explicitly SIMULATED fills/ledger in Execution Research (§26).

## §14 Risk Management — IMPLEMENTED (research-scope)
RISK & DRAWdown bottom-dock tab; portfolio risk reports with max drawdown, realized volatility and per-metric uncertainty (`institutional_intelligence/portfolio_risk.py`, `intelligence.py` GET seams); scenario risk; risk-related alerts (monitoring alerts); model uncertainty and research limitations rendered with every metric. Research-only framing: risk context, not risk actuation.

## §15 Alerts & Monitoring — IMPLEMENTED
`monitoring_alerts.py` backend + `AlertsProvider` + `MonitoringAlertsPanel` in the ALERTS dock: list, detail fetch, acknowledge (acknowledged alerts stay visible). Monitoring/connection/data-state monitoring: feed telemetry (WS state, tick rate, message count, lag), `/health` liveness + `/ready` readiness (live DB check), `/system/info` identity, audit-event activity records. Alerts inform; nothing silently executes.

## §16 Journal / Operator Research Record — IMPLEMENTED
Manual research journal (`ManualJournalPage` + JOURNAL dock tab): list/create/update entries, reflections, research history (`collaboration.py` journal endpoints, audited, inert). Planning notes in governed research context (trade plans); journal↔planning continuity tested (`PlanningJournalContinuity.test.tsx`). No autonomous strategy execution.

## §17 Artifact Lineage & Evidence — IMPLEMENTED
Lineage fields on all report models (`lineage` columns: correlation, regime, scenario, portfolio-risk, signal-validation, dataset, execution experiments, monitoring alerts); `ArtifactLineageTree` UI; provenance per artifact; audit records (audit-events read seam); hash-based relationships (SHA-256 `plan_hash` for pre-registered execution plans; artifact-identity hashes in the governance record); source context; limitation disclosure; evidence inspection surfaces.

## §18 Governance & Audit — IMPLEMENTED (VERIFIED, APPROVED — UI-CONV-P03 item 5, POLISH-P01)
Governance overlay (`GovernanceOverlay.tsx`, 1,072 lines): read-only audit explorer over `GET /api/v1/persistence/audit-events` with in-memory filters/sort; refusal records rendered as stored text; technical-debt/standing-residual sections always visible (no tooltips/closed accordions); section-level independent degradation; no mutation of governance records. Governance badge in every terminal view. Constitutional disclosures carried in-product (structure disclosures on MarketStructure indicators, confluence non-actuation, drawing/annotation guard vocabularies).

## §19 Security & Access Control — IMPLEMENTED (VERIFIED)
Authentication (JWT + one-time WebSocket tickets, close 4401, W1-U01); RBAC (role deps `RbacOperatorDep`/`RouteInventoryOperatorDep`/`CurrentOperatorDep`; chunk-level route gating — `GatedRouteElement` runs the RBAC gate BEFORE lazy chunk fetch; unprivileged operators get real 403s, `route-access-denied` testid, denial text "This is an access restriction, not an empty result."); protected routes (all 16 registered routes auth-required, ITRGA guard); 401 handling; secure token handling; restricted state handling; safe error presentation (explicit error banners, never optimistic); input/payload discipline (field whitelists on every write seam — e.g. `COLLECTION_WRITE_FIELDS`); secret protection (no credential/token exposure; security-invariant test suites ui008–ui011, uiconv, uinew). NullBroker + `ConstitutionalGovernanceGate` refuse any broker mutation (`GATE_CLOSED_CONNECT_REFUSED`, `GATE_CLOSED_EXECUTE_REFUSED`).

## §20 Governed AI Assistant — IMPLEMENTED (VERIFIED, APPROVED — UI-008/009 scope)
`AssistantCommandSurface` (+ `ContextualAssistantPanel`, `DocumentationLookupSurface`, `ResearchReportSummarizer`, `UncertaintyBadge`, `ArtifactLineageTree`): grounded research responses (read-only persisted `assistant_research_response` records), research explanation, summarization, related-artifact discovery, documentation lookup (static local index — zero external calls), refusal handling, uncertainty disclosure, audit presentation, assistant-surface quick actions in the command palette. Indicator explanation: indicator explanations exist via registry disclosures/annotations rather than an assistant chat flow (stated as-is).

## §21 AI Refusal System — IMPLEMENTED
Backend policy (`backend/app/collaboration/assistant.py:28-37`): `ORDER_INSTRUCTION_REFUSED`, `GATE_OPEN_INSTRUCTION_REFUSED`, `SECRET_EXFILTRATION_REFUSED`, `UNBOUNDED_TOOL_REQUEST_REFUSED`; taxonomy fixture adds `GROUNDING_REQUIRED` and `ASSISTANT_DISABLED`. Refusals persisted and surfaced in the UI refusal surface (six-code taxonomy rendered read-only, `AssistantCommandSurface.tsx:318+`).

## §22 AI Disclosure & Uncertainty — IMPLEMENTED
Verbatim disclaimer in-product (`AssistantReviewSubPanel.tsx:7`): "AI-generated research assistance only. Not financial advice, not an instruction, may be wrong. Operator judgment required. AXIOM does not act." Uncertainty/limitations/scope/refusal state/advisory boundary/research-only posture carried in text (UncertaintyBadge, refusal badges, governance badge) — not by color alone.

## §23 AI Auditability — IMPLEMENTED
Persisted assistant response records + refusal records (`assistant_research_response` model + repository), audit events, refusal persistence and auditing (ui008 disabled-state test verifies persistence + audit), review surface (`AssistantReviewSubPanel`), disclosure register, refusal taxonomy. Read-only lineage surfacing; no fabricated histories.

## §24 AI API Seams — IMPLEMENTED
`GET /api/v1/collaboration/assistant-responses` and `/assistant-responses/{response_id}` confirmed in `collaboration.py` (authenticated, read-only, list + detail summaries). No action/emission verbs on the assistant surface. (The same router's POST/PUT/PATCH/DELETE verbs belong to chart annotations, trade-plan notes and journal entries — audited inert research writes, not assistant mutation.)

## §25 AI Boundaries — GOVERNED ABSENCE (enforced)
No external LLM integration (zero outbound AI calls; documentation lookup is a static local index); not autonomous (cannot place orders/open gates/execute tools/mutate state); not a writer of platform state (assistant responses are read-only; assistant itself has no write seam); not financial advice (disclaimer enforced); not an independent governance authority (gate state rendered, never controlled).

## §26 Non-Actuation — GOVERNED ABSENCE (enforced, VERIFIED)
No order-placement/execution/broker-mutation endpoints exist (route inventory inspected: no order verbs anywhere in `api/routes/`); `NullBroker` performs zero I/O and refuses connect/execute with recorded refusals; gate-opening actions absent; execution research is explicitly SIMULATED (runs/fills/ledger labelled "simulated"); guard vocabularies reject actuation language in drawing labels (`drawingLabelRejection`: entry/stop_loss/take_profit/position_size/lot/order/risk_reward/setup), research annotations, and confluence terms (`CONFLUENCE_FORBIDDEN_TERMS`); anchor sentence pinned in the chart stage: "Indicators describe data, they never advise a trade." Positions/historical orders/account state are representable in principle but not present (no data feed) — nothing fabricated.

## §27 Command Palette & Operator Productivity — IMPLEMENTED
Ctrl+K global palette (`CommandPalette.tsx` + `quickActionCatalogue.ts`): workspace navigation, assistant-surface navigation (`qa.open.assistant-surfaces`, `qa.open.recent-assistant-responses`), research/intelligence/governance/settings/journey quick actions, shell actions (governance notification), keyword search; global search overlay for instruments/workspaces/signals/journal/collections; keyboard-oriented workflows (`useKeyboardShortcuts.ts`).

## §28 Workspace / Layout System — IMPLEMENTED
16 registered workspaces/routes with layout definitions (`workspaceRegistry.tsx` — `/`, `/live`, `/charts`, `/chart`, `/signals`, `/analytics`, `/intelligence`, `/investigate`, `/compare-scenarios`, `/trade-plans`, `/execution-research`, `/portfolio-research`, `/journal`, `/research-management`, `/governance`, `/workspace`); multi-pane terminal layout (`TerminalMultiPaneLayout` — left dock/watchlist, center chart stage, right dock, bottom dock); recent-workspace switching. Named presets: Trading/Research/Risk/Investigation/Intelligence compositions are achieved through dock/panel/stage deep links (`?view=`, `?dock=`, `?panel=`, `?open=`) rather than five separate saved layouts — stated as-is.

## §29 Contextual Docking — IMPLEMENTED (VERIFIED, APPROVED — UI-CONV-P03/SURF-P01)
Right dock tabs SIGNALS/TELEMETRY/INTELLIGENCE/ALERTS; bottom dock tabs TRADE_PLANS/JOURNAL/RISK/SCENARIOS/PORTFOLIO; overlays (global search, settings, governance, command palette) via `OverlayLayer`; stage views research/execution/chart; signal drill-down; contextual panels (watchlist, confluence, session strip, telemetry). Legacy routes re-pointed to dock/panel/stage deep links (12 redirect components).

## §30 Global / Terminal Status — IMPLEMENTED
API state (`/health`, `/ready` with live DB check), WebSocket state (tick rate, message count, lag), market-data connectivity, system health/info (`/system/info`), environment, operator/session state (shell), governance gate (badge), research-only state. Telemetry subordinate to the market workspace.

## §31 Data-State Handling — IMPLEMENTED
Explicit states evidenced: Loading (skeleton/checking states) · Ready (typed native series) · Empty ("No … returned." discipline — empty results named, not fabricated) · Stale (stale signals tagged with absolute UTC) · Disconnected (WS state) · Unauthorized (401/403 with explanatory denial text) · Error (explicit error banners) · Restricted (route-access-denied) · Research-only (badges everywhere) · Degraded (sparkline/telemetry honest degradation, dashes for absent fields). Typed `native/aggregated/unavailable` series kinds propagate honesty to the UI.

## §32 Accessibility — IMPLEMENTED (test-evidenced; not externally audited)
Keyboard navigation + shortcuts (`useKeyboardShortcuts.ts`, palette), focus management (Dialog focus trap + restoration tests, `focusTrap.ts`, focusVisibility), semantic structure (regions A–F, roles, `SrOnly`), ARIA support (96 component files carry aria-*), state announcements (`RouteAnnouncer`, `role="status"` surfaces, multiModalStatus), readable contrast (`highContrast.test.tsx`), accessible command interactions, critical-workflow coverage (skip link, responsive reflow/tokens, `accessibilityAudit.test.tsx`). Caveat disclosed: no independent WCAG conformance audit; evidence is test-based.

## §33 Performance — PARTIAL
IMPLEMENTED: route-level code splitting (4 heavy lazy chunks; RBAC gate prevents unauthorized chunk fetch — POLISH-P01 M2); measured build evidence (initial chunk 626.74 kB + 6 lazy chunks, `vite_build_brand_r1.log`); synced chart panes; WebSocket live updates; controlled layout regions. NOT IMPLEMENTED: formal measurable interaction-latency targets/SLAs — performance claims remain evidence-based, not target-certified (as the catalogue itself requires: "Performance claims must be established by evidence").

## §34 Design System — IMPLEMENTED
Dark-first terminal presentation; `--ix-*` design tokens (276 token references in `global.css`); typography hierarchy; reusable component patterns (`components/ui/`, Dialog, StatusPill); institutional branding (Operator logo via `LogoMark.tsx`, login + shell header, `branding/axiom-logo.png`); state semantics (governance badge, badges/stubs, provenance labels).

## §35 Market + Research Convergence — IMPLEMENTED
Instrument → chart → signal → research → artifact → intelligence → investigation flows inside one terminal: symbol context propagates to signals/intelligence/research surfaces; signals carry artifact lineage; research hub links chart context; investigation frames join signals to research to scenarios.

## §36 Market + Risk Convergence — IMPLEMENTED
Same instrument context connects to portfolio research, risk/drawdown, scenario comparison and alerts via bottom-dock tabs (all symbol-contextual where applicable); no page-isolation.

## §37 Intelligence + Governance Convergence — IMPLEMENTED
Intelligence outputs carry evidence/provenance/uncertainty/disclosure fields; governance overlay exposes audit/refusals/debt; intelligence surfaces render uncertainty intervals and method versions; the "what does the system indicate, why, how certain, what evidence, what restrictions" chain is answerable in-product.

## §38 Operator Workflow — IMPLEMENTED (VERIFIED)
All 11 steps of the representative workflow (select instrument → market state → chart → technical context → signals → intelligence → research → evidence → scenarios → risk/portfolio → assistant explanation → human decision) were exercised end-to-end in the post-closure cold-start smoke test (login → terminal → 1h/1d/1m → SMA20+RSI → confluence → trendline round-trip → market structure → lazy routes → stage views): zero page errors. Human decision remains terminal.

## §39 Governance Protections — IMPLEMENTED
Programme governance instruments active: patch chain (18 verified elements), technical debt register, observation ledger (one open finding OBS-SURF3-1, non-blocking), delivery/hash discipline (OBS-DELIVERY-PROCESS standing rule), gate state rendered in-product, no self-certification.

## §40 Engineering & Operational Infrastructure — IMPLEMENTED (VERIFIED)
Backend services (FastAPI routers: auth, market, ws, intelligence, collaboration, persistence, execution_research, monitoring_alerts, system, health, observability, operator, institutional_platform, ingestion, advisory_signals, advisory_analytics); database persistence + Alembic migrations (`backend/alembic/versions/`, 0001+); frontend architecture (React+TS+Vite); test suites (476 backend / 860 frontend passing, last run 2026-08-19 post-hotfix); static/type checking (tsc clean); build tooling (production build reproduced); runtime health endpoints; live-market/WebSocket infrastructure; authN/authZ; reusable UI components.

## §41 Research-Only Platform Posture — ENFORCED (VERIFIED)
GOVERNANCE GATE: CLOSED · PRODUCTION: NOT CERTIFIED · RESEARCH-ONLY · NON-ACTUATING — rendered persistently (`TerminalGovernanceBadge`), enforced in code (no actuation seams), and separated from phase-approval in every record.

## §42 Complete High-Level Capability Map — DESIGNED (satisfied by implementation)
The MARKETS/ANALYSIS/INTELLIGENCE → INVESTIGATION → EVIDENCE/LINEAGE → PORTFOLIO/RISK → GOVERNANCE → CONTEXTUAL AI → HUMAN DECISION map is a design statement; every leaf of it is assessed individually in §1–§41 above and found implemented (with the partials named). No separate implementation item.

## §43 What AXIOM Can Do at Intended Full Capability — IMPLEMENTED (list fully covered above)
Monitor markets: §3.2/§3.3/§4 · Analyze markets: §5/§6 · Research: §9/§10 · Investigate: §11 · Evaluate portfolio/risk: §13/§14 (research-scope — live account positions NOT implemented) · Use intelligence: §8 · Use the assistant: §20/§21 · Maintain institutional traceability: §17/§18 · Operate efficiently: §27/§29. Every bullet of §43 is adjudicated in the cited sections; no bullet is unaddressed.

## §44 What AXIOM Explicitly Does Not Do — CONFIRMED (governed absence holds)
Autonomous trading: absent (§26) · hidden execution pathways: absent (route inventory inspected) · opening governance gates: absent (§25/§26) · self-certification: absent (production certification never claimed) · fabricated market data: absent (provenance labels, dashes discipline) · hiding uncertainty: absent (uncertainty rendered everywhere) · exposing secrets: absent (§19) · silent external AI: absent (no external LLM, static local doc index) · silent platform-state mutation: absent (audited seams only) · financial-advice engine: absent (disclaimer enforced) · replacing the human operator: absent (all surfaces advisory).

## §45 Capability Maturity Model — ADOPTED (the model this checklist uses)
The five-state model (DESIGNED/IMPLEMENTED/VERIFIED/APPROVED/PRODUCTION CERTIFIED) is exactly the vocabulary applied throughout this checklist. No capability in the platform is PRODUCTION CERTIFIED.

## §46 Full Product Vision — DESIGNED (satisfied by implementation)
"One governed institutional trading and research workstation" — not merely a charting tool, research database, assistant, governance console, or dashboard: established by §35–§38 convergence evidence. Statement-level design item; no separate code claim.

## §47 Current-Evidence Qualification — ACCURATE (accepted as correct framing)
The distinction between implemented / verified / approved / production-certified matches the programme record; the "approved in substance but not landed" UI-CONV-P03 history is reflected in the record and was resolved by the re-landed convergence phases (subsequent determinations APPROVED the landed work).

## §48 The Correct Launch Test — VERIFIED
The launch test ("open AXIOM, select an instrument, understand the market, inspect the chart, investigate signals, review intelligence and research, inspect evidence and risk, use the governed assistant for explanation, retain awareness of uncertainty/provenance/governance/non-actuation without leaving the terminal") was executed as the post-closure cold-start verification (2026-08-19): every step completed in-terminal, zero page errors, unprivileged RBAC denials confirmed. Evidence: `docs/evidence/uiconv/` smoke logs + per-phase verification JSONs.

## §49 Final Capability Statement — IMPLEMENTED with disclosed partials
The statement is substantially true of the shipped platform with these disclosed exceptions (also named in their sections): no user-defined watchlist groups/sorting (§3.2); no bid/ask/broker-spread (§3.3); no volume-based indicator (§6, documented decision); no live account portfolio/positions/orders (§13); no formal latency SLAs (§33); no external WCAG audit (§32); scenario/portfolio capability is read-only by design (§12/§13); all post-closure changes carry the standing "not ITRGA-reviewed" rider.

---

## Summary counts (51 items assessed — 49 catalogue sections, §3 assessed as its three sub-sections)

| Status | Sections |
|---|---|
| IMPLEMENTED (full) | 37 — §1, 2, 3.1, 4, 5, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 27, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 40, 43, 49* |
| PARTIAL (absent sub-items named) | 5 — §3.2, 3.3, 6, 13, 33 |
| GOVERNED ABSENCE (correctly absent) | 3 — §25, 26, 44 (confirmed) |
| ENFORCED posture | 1 — §41 |
| DESIGNED (satisfied by implementation) | 2 — §42, 46 |
| Meta/qualification | 3 — §45 (model adopted by this checklist), §47, §48 |
| NOT IMPLEMENTED (whole section) | 0 |

(*§49 carries the disclosed partials listed above; §32 carries the no-external-WCAG-audit caveat.)

**Post-closure rider:** `postclosure_hotfix.patch.txt` and `postclosure_brand.patch.txt` (Operator directives TD-UI-POSTCLOSURE-HOTFIX / -BRAND) are applied and verified in the chain but are not ITRGA-reviewed; routing them for record completeness remains at the Operator's discretion.

---

Gate CLOSED · Production NOT CERTIFIED · We don't guess. We prove.

---

# R2 ADDENDUM (2026-08-19) — reconciliation with ITRGA capability assessment

The ITRGA post-closure capability assessment (`docs/build-orders/CAPABILITY_ASSESSMENT.md`, sha256 `979f815f…`) applied a runtime lens (data presence + end-to-end operability) finer than this checklist's R1 code-presence lens. Per the programme principle "if an aspect has already been built, it must be presented in the best possible way", R2 adopts the runtime lens. R1 content above is preserved verbatim as the delivered record.

| § | R1 status | ITRGA | Reconciled R2 (adopted) |
|---|---|---|---|
| 7 Signals | IMPLEMENTED | 🟡 | **SCAFFOLD-BY-DESIGN** — read/drill-down operable; generation absent by design (R3, no model authorization) |
| 8 Market intelligence | IMPLEMENTED | 🟡 | **SCAFFOLD-BY-DESIGN** — list/get operable; `create_report` uncalled for the five families by design |
| 9 Research management | IMPLEMENTED | 🟡 | **OPERABLE for operator-authored artifacts** (collections/tags/membership/annotation CRUD) — empty of generated artifacts by design |
| 10 Artifact explorer | IMPLEMENTED | 🟡 | **OPERABLE** (10 sources read) — rows empty by design |
| 11 Investigation | IMPLEMENTED | 🟡 | **OPERABLE** (planning/journal/execution continuity) — signal-dependent stages empty by design |
| 12 Scenario analysis | IMPLEMENTED | 🟡 | **SCAFFOLD-BY-DESIGN** — read-only by T-1/R3 |
| 13 Portfolio analytics | PARTIAL | 🟡 | **PARTIAL** (unchanged) — hypothetical research descriptors; live venue records governed-absent |
| 14 Risk management | IMPLEMENTED | 🟡 | **SCAFFOLD-BY-DESIGN** — read seams operable; report generation absent by design |
| 15 Alerts & monitoring | IMPLEMENTED | 🟡 | **IMPLEMENTED (partial-operable)** — list/detail/acknowledge operable; auto-trigger generation absent by design |
| 17 Artifact lineage | IMPLEMENTED | 🟡 | **OPERABLE** (lineage over operator-authored artifacts) — empty of generated artifacts by design |
| 20 Governed AI assistant | IMPLEMENTED | 🔴 | **NOT IMPLEMENTED as an operable assistant** — audited record viewer only; no request path (UI-008 read-only scope); engine exists, tested, not exposed |
| 21 AI refusal system | IMPLEMENTED | 🟡 | **IMPLEMENTED (engine)** — policy/persistence/tests; unreachable from UI because no request path |
| 23 AI auditability | IMPLEMENTED | 🟡 | **IMPLEMENTED (record viewer)** — empty pending generated responses |
| 33 Performance | PARTIAL | 🔴 | **PARTIAL** (unchanged) — build/chunk evidence exists; no interaction-latency targets; ITRGA 🔴 accepted for that absence |
| 35–37 Convergences | IMPLEMENTED | 🟡 | **OPERABLE as a terminal** — research/intelligence content empty by design |
| 38 Operator workflow | IMPLEMENTED + VERIFIED | 🟡 | **VERIFIED through the analysis stage** — signal/intelligence/assistant stages empty by design |
| 32 Accessibility | IMPLEMENTED | 🟢 | **IMPLEMENTED** + new carried observation OBS-CAPASSESS-H1 (no `<h1>` on `/`) |

Staged corrections awaiting Operator routing (full designs in `RESPONSE_CAPABILITY_ASSESSMENT.md` §4): **FIND-5** simulated-clock cap (never emit a bar dated past wall-clock UTC; accelerated catch-up preserved while behind) and **FIND-6** nanoid ≥3.3.18 transitive bump (GHSA-2v37-7h3g-55p8, HIGH, breaches the project's own `--audit-level=high` gate). Neither is executed without an Operator directive. Register rows: TD-UI-CAPASSESS-GENERATION-WIRING · TD-UI-CAPASSESS-SIMCLOCK · TD-UI-CAPASSESS-NANOID-HIGH · OBS-CAPASSESS-H1.

Gate CLOSED · Production NOT CERTIFIED · We don't guess. We prove.
