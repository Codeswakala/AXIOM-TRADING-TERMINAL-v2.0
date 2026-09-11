# Institutional Capability Assessment & UI Transformation Baseline

| Field | Value |
|---|---|
| Authority | ITRGA Instruction — Institutional Capability Assessment & UI Transformation Baseline |
| Classification | Post-roadmap capability assessment; not a Build Order |
| Date | 2026-07-19 |
| Platform of record | v0.62.0 |
| Alembic head | `20260717_0037` |
| Roadmap status | Waves 0–7 complete; Institutional Platform Complete declared by ITRGA |
| Production status | Not certified; governed by `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md` |
| Purpose | Establish baseline for Institutional UI Transformation without expanding roadmap scope |

---

## Part I — Executive Summary

AXIOM has successfully completed its approved implementation roadmap. The platform is now a mature institutional **research terminal foundation** with governed authentication, audit, data ingestion, ML research lifecycle, advisory signal generation, institutional intelligence reports, human-AI collaboration records, simulated execution research, operator workspace customization, research management, API catalogue, plugin contract safety, portfolio research dashboards, and closeout evidence proving the Governance Gate remained CLOSED across Waves 0–7.

The platform is capability-complete relative to the approved roadmap, but it is **not production certified** and is not yet presented as a fully polished institutional workstation. The largest remaining gap is not backend capability; it is **user experience integration**: many powerful capabilities exist as APIs, evidence flows, component pages, or research surfaces, but they are not yet unified into a professional, cohesive, operator-centered workstation.

The correct next phase is therefore **Institutional UI Transformation**, not new feature expansion. The transformation should expose and organize existing capabilities, improve workflows, unify visual language, strengthen empty/error/loading states, improve accessibility, and present research lineage, uncertainty, audit, and governance status in a professional interface.

---

## Part II — Capability Inventory

| Subsystem | Purpose | Current maturity | Operational status | Dependencies | User visibility |
|---|---|---|---|---|---|
| Constitutional governance | Defines hierarchy, roadmap, reviews, Build Orders, Gate discipline | Complete for roadmap | Active | Governance docs, ITRGA verdicts | Mostly documentation; not UI-native |
| Production certification governance | Defines final production deployment certification | Adopted | Pending future certification | `11_PRODUCTION_READINESS_CERTIFICATION.md` | Documentation only |
| Backend API platform | FastAPI service with versioned `/api/v1` APIs | Mature | Active | FastAPI, SQLAlchemy, Alembic | Indirect through UI/API docs |
| Authentication | Operator login, JWT, refresh rotation, WS tickets | Mature | Active | Operators table, JWT secret, refresh token tables | Login UI + protected routes |
| Authorization/RBAC | Default-deny institutional permissions and route protection | Mature | Active | Operator roles, RBAC constants | Mostly backend/API; limited UI visibility |
| Audit system | Immutable-oriented governance audit events | Mature | Active | `audit_events` table | Mostly backend/evidence; not surfaced as audit explorer |
| Observability/logging | Metrics, correlation IDs, redaction, health/readiness | Mature foundation | Active | Observability service, logging config | Limited: health/metrics API; no rich ops UI |
| Database architecture | PostgreSQL/SQLite-compatible SQLAlchemy models and Alembic migrations | Mature | Active | Alembic head `20260717_0037` | Hidden except evidence/API surfaces |
| Market data services | Simulated live market, persisted candles, chart history | Functional | Active research/simulated path | Candle repository, live market service | Live Market page, chart workspace |
| WebSockets | Status/live market sockets with ticket auth | Functional | Active | WS ticket auth | Used by UI hooks; limited operator controls |
| ML dataset architecture | Dataset snapshots, quarantine, metadata, temporal discipline | Mature backend | Active | ML dataset modules/tables | Mostly hidden behind tests/docs |
| Feature store | Causal feature definitions and feature records | Mature backend | Active | ML feature modules/tables | Mostly hidden |
| Experiment registry | Pre-registration and experiment governance | Mature backend | Active | Experiment tables/services | Mostly hidden |
| Model artifact registry | Baseline model artifact and governance status | Mature backend | Active | Model artifact tables/services | Mostly hidden |
| Validation/calibration/economic reports | Statistical, calibration, economic validation with uncertainty | Mature backend | Active | Validation/calibration/economic tables | Partly visible through intelligence/advisory surfaces |
| Generalization/drift | Drift and generalization records | Mature backend | Active | Drift/generalization tables | Partly visible through alerts/reports |
| Advisory signals | Governed inert signal records with guardrails | Mature | Active | ML artifacts, validation reports, signal service | Advisory Signals page |
| Advisory analytics | Metrics with uncertainty and confidence bands | Mature | Active | Signal history | Performance Analytics page |
| Monitoring alerts | Drift/health/monitoring alert records | Mature | Active | Alert service/table | Operations dashboard panel/API |
| Institutional Intelligence | Correlation, regime, scenario, portfolio/risk, signal validation reports | Mature | Active | W4 report services/tables | Institutional Intelligence page; limited detail drilldowns |
| Human-AI collaboration safety | Deterministic local assistant/refusal model, prompt-injection safety | Mature backend | Active | Assistant safety contracts/audits | Limited direct UI; some surfaces reuse artifacts |
| Assistant research responses | Audited assistant response/refusal records | Mature backend | Active | Assistant response table | Mostly hidden/API-level |
| Chart research annotations | Inert chart annotations/drawing records | Functional | Active | Chart annotation repository/API | Chart Workspace page |
| Signal investigation workspace | Read-only signal rationale/guardrail/lineage view | Functional | Active | Signal and intelligence APIs | Signal Investigation page |
| Scenario comparison | Read-only comparison of persisted scenarios | Functional | Active | Scenario report API | Scenario Comparison page |
| Trade planning | Inert trade plan research notes | Functional | Active | Trade plan table/API | Trade Planning page |
| Manual journal | Inert manual research journal entries | Functional | Active | Journal table/API | Research Journal page |
| Execution research | Simulated runs, fills, ledger, risk, experiments, analytics | Mature research subsystem | Active simulated-only | W6 execution research tables/services | Execution Research page |
| Workspace customization | Per-operator presentation preferences | Mature | Active | `operator_workspace_preferences` | Workspace Settings page |
| Research management | Collections/tags over existing artifacts, reference-only | Mature | Active | W7 research tables/services | Research Management page |
| API ecosystem catalogue | Authenticated generated API catalogue, no execution surface | Mature API-only | Active | FastAPI route metadata | API only; no UI |
| Plugin contract safety | Static plugin contracts, allowlist, hostile refusal audit | Mature API-only | Active | Existing audit table | API only; no UI |
| Portfolio research dashboard | Hypothetical research aggregation and report/export preview | Functional | Active | Existing simulated/research artifacts | Portfolio Research page |
| Enterprise readiness hardening | RBAC/isolation/redaction/admin default/rate guard disposition | Mature proof unit | Active as governance/tests | Readiness module/tests | Not UI-visible |
| Closeout evidence | Whole-wave/project proof, no-orphan, milestone reconciliation | Complete | Accepted by ITRGA | Closeout tests/evidence | Documentation only |

---

## Part III — Functional Completeness Assessment

| Area | Assessment | Evidence / rationale |
|---|---|---|
| Roadmap implementation | Complete | ITRGA W7-U08 final verdict closes Waves 0–7 and declares Institutional Platform Complete. |
| Constitutional governance | Complete for implementation; production governance pending | Build Orders, ITRGA verdicts, hierarchy, final production certification document. |
| Backend platform | Complete for v0.62.0 roadmap | Backend baseline 413 passed, API stack stable. |
| Authentication/session management | Functionally complete | JWT, refresh rotation, WS tickets, protected routes, insecure bootstrap rejection. |
| RBAC/multi-user isolation | Functionally complete | W7-U01/W7-U07 tests and evidence; default-deny and two-operator isolation proven. |
| Audit system | Functionally complete | W7 no-orphan proofs and audit event usage across artifacts. |
| Observability/logging | Functionally complete foundation; production certification pending | Redaction and metrics exist; production ops procedures still subject to certification. |
| ML research framework | Complete as research framework | Dataset, feature, experiment, model, validation, calibration, economic, drift/generalization layers implemented. |
| Advisory platform | Complete | Signals, guardrails, analytics, alerts, signal workspace implemented. |
| Institutional Intelligence | Complete as implemented roadmap layer | Reports and dashboard exist; richer drilldowns are UI transformation concern, not missing backend feature. |
| Human-AI collaboration | Complete within approved local/deterministic scope | Assistant responses/refusals, chart annotations, trade planning, journal, investigation surfaces implemented. External LLM remains hard-gated future work. |
| Execution research | Complete as simulated research environment | W6 closed; no live execution; simulated artifacts and UI implemented. |
| Institutional platform features | Complete through W7 | Workspace, research management, API catalogue, plugin contracts, portfolio research, readiness, closeout complete. |
| API catalogue/plugin contracts | Functionally complete but minimally surfaced | API-only by design; UI exposure may be useful in transformation. |
| UI/workstation experience | Partially complete | Many pages exist, but final workstation shell, layout, navigation, workflow integration, and professional UX remain incomplete. |
| Production readiness | Not certified | Governed by `11_PRODUCTION_READINESS_CERTIFICATION.md`; certification has not occurred. |

---

## Part IV — User Experience Exposure Analysis

### Features already accessible in the UI

- Login and protected app shell.
- Operations dashboard with platform status/alerts.
- Live Market page for simulated market data.
- Chart Workspace with chart research annotations.
- Advisory Signals page.
- Performance Analytics page.
- Institutional Intelligence summary page.
- Signal Investigation page.
- Scenario Comparison page.
- Trade Planning page.
- Research Journal page.
- Execution Research page.
- Workspace Settings page.
- Research Management page.
- Portfolio Research page.

### Capabilities mostly hidden behind APIs/tests/evidence

- API catalogue.
- Plugin contract catalogue and hostile refusal audit trail.
- Audit event exploration.
- Full ML dataset/feature/experiment/model registry lifecycle.
- Validation/calibration/economic/generalization report registry details.
- RBAC/default-deny vocabulary and role diagnostics.
- Production-readiness/security status.
- CI/evidence status.
- Governance milestone/audit indexes.
- Operator-scoped data lineage across all artifact types.

### Backend functionality lacking professional presentation

- Dataset/feature/model/experiment governance lineage.
- Report drilldowns for institutional intelligence artifacts.
- Assistant research response/refusal history.
- Audit event log and no-orphan traceability.
- Plugin contract safety status.
- API catalogue as operator/developer documentation surface.
- Readiness/certification status dashboards.

### Services requiring integration into the final workstation

- Unified artifact explorer across signals, reports, simulations, plans, journal entries, annotations, collections, and tags.
- Unified search/filtering across research artifacts.
- Unified lineage panel showing source artifacts, uncertainty, limitations, economic usefulness, audit correlation, and operator scope.
- Evidence/governance panel showing Gate status, no-actuation framing, version, head, and certification status.

---

## Part V — Institutional Trading Workstation Gap Analysis

AXIOM already has substantial institutional research capabilities, but its interface is still closer to a collection of governed research pages than a cohesive workstation.

### Existing institutional capabilities

- Governed research lifecycle from data ingestion through validation and advisory signals.
- Multi-market metadata and research artifacts.
- Advisory signal history with guardrail status.
- Institutional reports with uncertainty and economic-usefulness separation.
- Human research workflows: annotations, investigation, scenario comparison, trade planning, journal.
- Simulated execution research environment.
- Operator-scoped workspace preferences and research management.
- API catalogue and plugin contract safety.
- Portfolio research dashboard, explicitly not real account/P&L.
- Strong governance/audit/no-execution posture.

### Missing presentation-layer capabilities

- Professional multi-panel workstation layout.
- Persistent workspace layout management beyond basic preferences.
- Integrated artifact/lineage explorer.
- Unified search and filtering.
- Professional report viewer with drilldown sections.
- Governance/audit/status overlays usable by operators.
- Visual hierarchy consistent with institutional terminal expectations.
- Polished empty/loading/error states.
- Accessibility and keyboard navigation pass.

### Missing workflow integration

- Seamless movement from signal → investigation → chart → scenario → plan → journal → collection/report.
- Unified source-artifact linking and back-navigation.
- Cross-page state continuity.
- Operator task flows for research review sessions.
- Integrated export/preview experience for generated reports.

### Remaining user-facing gaps prior to Version 1.0

- UI transformation into a cohesive workstation shell.
- Professional chart/research integration and panel layout.
- Clear operator mental model for all research artifacts.
- Surfacing of existing backend registries and governance states.
- Visual consistency, accessibility, responsiveness, and polished states.

No new business feature is required to address these gaps; they are primarily presentation and integration work.

---

## Part VI — UI Transformation Baseline

The Institutional UI Transformation should represent existing capabilities through the following workstreams.

### 1. Workspace architecture

Create a professional workstation shell with configurable panels, persistent layout, and clear separation between market view, research artifacts, intelligence, execution research, and governance/status.

### 2. Navigation model

Replace page-sprawl with task-oriented navigation: Monitor, Research, Investigate, Compare, Plan, Review, Report, Govern.

### 3. Panel organization

Introduce reusable panels for artifact list, artifact detail, lineage, uncertainty, economic usefulness, audit trail, notes, and related items.

### 4. Professional chart integration

Integrate chart annotations, signal overlays, scenario references, and research markers into a coherent chart workspace. This should use existing chart/annotation capabilities only; no new signal generation or execution controls.

### 5. Market workspaces

Expose simulated market data and chart history professionally with clear source/provenance labels and no live broker implication.

### 6. Research workspaces

Create unified workspaces for signals, reports, scenarios, execution research, portfolio research, collections, tags, plans, and journal entries.

### 7. AI interaction model

Represent existing deterministic assistant/refusal records and research explanations. Do not introduce external LLM behavior without future governance.

### 8. News integration

No external news ingestion exists in the completed roadmap. UI transformation should not invent news functionality. If needed later, it requires a governed post-roadmap design/Build Order.

### 9. Navigator Assistant integration

A navigator may be a UI layer over existing route/artifact/help metadata and assistant/refusal records, but must not introduce new AI action tools or external LLM behavior without governance.

### 10. Visual design system

Consolidate colors, typography, spacing, panels, tables, badges, disclaimers, alert states, and chart styling into a formal institutional design system.

### 11. Component consistency

Unify cards, tables, filters, forms, detail views, JSON viewers, lineage displays, uncertainty displays, and audit/correlation displays.

### 12. Accessibility and responsive behavior

Add keyboard navigation, focus states, ARIA consistency, responsive panel behavior, and readable empty/error/loading states.

---

## Part VII — Version 1.0 Readiness

### Platform capability readiness

**High / roadmap-complete.** AXIOM has implemented the approved platform capability roadmap and passed final W7 closeout. The foundation is sufficient to begin UI transformation.

### User experience readiness

**Partial.** The current UI exposes many capabilities, but not yet as a unified professional institutional workstation. The UI transformation phase is necessary before AXIOM can be presented as a polished Version 1.0 operator terminal.

### Production readiness

**Not certified.** Production readiness must be independently certified under:

```text
docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md
```

The completion of implementation and UI transformation does not automatically grant production deployment approval.

---

## Final Answers

### 1. What has AXIOM successfully implemented?

AXIOM has implemented the full approved roadmap: governed backend platform, auth/RBAC, audit, observability, market data research services, ML research lifecycle, advisory signals and analytics, institutional intelligence, human-AI collaboration records, simulated execution research, workspace customization, research management, API catalogue, plugin contract safety, portfolio research reporting, enterprise readiness hardening, and whole-project closeout.

### 2. What remains before AXIOM can be presented as a professional institutional trading platform?

The primary remaining work is not backend functionality but professional workstation presentation: unified shell, workflow integration, artifact navigation, lineage/audit/uncertainty presentation, design system, accessibility, responsive behavior, and polished operator experience. Production certification also remains separate and mandatory.

### 3. Which remaining tasks belong to the Institutional UI Transformation phase?

Workspace architecture, navigation, panel layout, chart/research integration, unified artifact explorer, report viewer/export preview, governance/audit/status surfaces, component standardization, design system, accessibility, empty/error/loading states, and professional workflow integration.

### 4. Is the platform foundation sufficiently complete to begin UI transformation?

Yes. The platform foundation is sufficiently complete to begin Institutional UI Transformation. The transformation should expose and organize existing capabilities, not expand the platform scope or introduce new business features.

---

**End of Institutional Capability Assessment & UI Transformation Baseline**
