# UI-008 Engineering Design Plan — Institutional AI Experience
## Clean Re-Build & Full Design-Plan Reconciliation

| Field | Value |
|---|---|
| Document ID | `docs/plans/UI-008_ENGINEERING_DESIGN_PLAN.md` |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | **UI-008 — Institutional AI Experience** |
| Document Classification | Tier 8 — Engineering Design Plan (Reconciliation Edition) |
| Author | AXIOM Development Authority (DA) |
| Issuing Instrument | `AXIOM — OPERATOR DIRECTIVE.md` |
| Review Authority | Independent Technical Review & Governance Authority (ITRGA) |
| Predecessor Milestones | 🏛️ UI-001 through UI-007 COMPLETE (v0.62.0) · UI-008 P01 (D-30) · UI-008 P01 M-1 (D-45) |
| Active Branch | `migration/ui008-da-itrga-reset` |
| Verified Anchor Commit | `30169a4e6ac6457bf078290025327fa1aedcb5e9` (Tag `UI-008-P01-M1_INTEGRATED`) |
| Platform Baseline | **Frontend: 66 suites / 295 tests passed · Backend: 414 tests passed · Build: clean (exit 0)** |
| Governance Gate | **CLOSED** (Strictly Enforced; No Live Execution Affordances) |
| Production Status | **NOT CERTIFIED** (Doc 11 Production Readiness Certification Held Out-of-Band) |
| DA Operational State | **Design Plan Submitted for Independent Review; Implementation on Formal Hold** |

---

# 1. Executive Summary

In response to the **Operator Directive** (`AXIOM — OPERATOR DIRECTIVE.md`) and the formal ITRGA Request (`ITRGA_REQUEST_UI-008_DESIGN_PLAN_RECONCILIATION.md`), the **AXIOM Development Authority (DA)** has executed a comprehensive architectural reconciliation and established a clean, coherent forward baseline for **UI-008 (Institutional AI Experience)**.

UI-008 is the primary cognitive and research-assistance interface of the AXIOM Institutional Trading Platform. Operating under Phase III (Investigation & Decision Support), UI-008 surfaces the platform's existing deterministic AI reasoning, persisted assistant responses, and analytical explainability without introducing unauthorized platform functionality, live trading pathways, or external Large Language Model (LLM) dependencies.

This document establishes the authoritative, end-to-end engineering blueprint for the entire UI-008 workstream across **6 structured phases (P01 through P06)**. It reconciles historical deliverables, provides a rigorous 6-category classification of all existing UI-008 technical assets, defines the precise target end state, details cross-phase architecture, and enforces strict security, accessibility, and evidence standards.

---

# 2. UI-008 Objective

The overarching objective of UI-008 is to transform AXIOM's verified intelligence capabilities into an accessible, transparent, and non-actuating operator research companion.

### Core Institutional Objectives:
1. **Surface Analytical Explainability**: Present transparent feature contributions, regime contexts, model confidence estimates, and calibrated uncertainty bounds across institutional workspaces (`/intelligence`, `/investigation`, `/governance`).
2. **Enforce Constitutional Refusal Boundaries**: Codify and display deterministic, auditable refusal notices whenever an operator query violates grounding, requests speculative market predictions, or seeks automated order execution.
3. **Streamline Workspace Navigation**: Provide keyboard-driven navigation (`Ctrl+K`), quick-action dispatch, artifact lineage tracking, and documentation lookup through the Navigator Assistant.
4. **Preserve Human-in-the-Loop Primacy**: Enforce prominent `"RESEARCH-ONLY · NON-ACTUATING"` disclosures across all assistant surfaces, ensuring the operator retains exclusive decision authority.

---

# 3. Governing Requirements

UI-008 is strictly bound by the following institutional requirements:
* **Explainability Mandate**: Every assistant output must disclose the underlying analytical evidence, model version, and uncertainty bounds (`00_VISION_AND_PRINCIPLES.md` Principle 7; `07_ML_SPEC.md`).
* **Zero Autonomous Execution**: The assistant is strictly non-actuating; no order ticket, sizing engine, broker connection, or automated trading pathway may exist on any assistant surface (`03_AXIOM_SPEC.md`; `05_SYSTEM_ARCHITECTURE.md` §37).
* **No External LLMs**: External third-party LLM APIs (OpenAI, Anthropic, etc.) are strictly prohibited without a formal, versioned constitutional amendment (`12_INSTITUTIONAL_UI_TRANSFORMATION_PLAN.md` §10).
* **Verbatim Refusal Auditing**: All query refusals must be categorized under the 6 approved constitutional reason codes and persisted to the audit ledger (`17_INSTITUTIONAL_SECURITY_STANDARD.md` Part XIV).
* **Authentication & Operator Isolation**: All assistant data queries require valid JWT authentication; multi-tenant operator isolation must remain inviolate (`17_INSTITUTIONAL_SECURITY_STANDARD.md` Part V, VI).

---

# 4. Governance Hierarchy

In accordance with `10_CONSTITUTIONAL_HIERARCHY.md`, all UI-008 engineering decisions observe the following immutable chain of precedence:

```
Tier 1 — Vision & Principles (00_VISION_AND_PRINCIPLES.md, 01_PRODUCT_MISSION.md, 02_DESIGN_PHILOSOPHY.md, 11_PRODUCTION_READINESS_CERTIFICATION.md)
  │
  ▼
Tier 2 — Constitutional Specification (03_AXIOM_SPEC.md)
  │
  ▼
Tier 3 — Strategic Roadmap (04_PROJECT_ROADMAP.md)
  │
  ▼
Tier 4 — Technical Constitution (05_SYSTEM_ARCHITECTURE.md)
  │
  ▼
Tier 5 — Domain Constitutions (07_ML_SPEC.md, 08_UI_UX_SPEC.md)
  │
  ▼
Tier 6 — Institutional Reasoning (08_DEVELOPER_REASONING_FRAMEWORK.md, 09_ITRGA_REASONING_FRAMEWORK.md)
  │
  ▼
Tier 7 — Operational Governance (12_INSTITUTIONAL_UI_TRANSFORMATION_PLAN.md, 13_UI_TRANSFORMATION_MASTER_PLAN.md, 16_BRAND_GOVERNANCE_STANDARD.md, 17_INSTITUTIONAL_SECURITY_STANDARD.md, PROJECT_STATE.md)
  │
  ▼
Tier 8 — Execution Governance (This Design Plan, Build Orders, ADRs)
  │
  ▼
Tier 9 — Engineering Evidence (Transcripts, Unit/Integration Tests, Builds)
  │
  ▼
Tier 10 — Institutional Investigation (ITRGA Verdicts & Determinations)
```

---

# 5. Roadmap Position

UI-008 is an **Integrative Workstream (Level C Dependency)** situated in **Phase III (Investigation & Decision Support)** of the Institutional UI Transformation Programme:

* **Predecessors (Completed & Verified)**:
  * Waves 0–7 (Core backend & research roadmap complete at v0.62.0 baseline).
  * `UI-001` (Institutional Workspace Shell — 5-region architecture).
  * `UI-002` (Workflow Navigation Framework — Command Palette & breadcrumbs).
  * `UI-003` (Professional Market Workspace — Chart-centered environment).
  * `UI-004` (Research & Intelligence Workspace — Advisory & intelligence reports).
  * `UI-005` (Investigation & Planning Workspace — Scenario comparison & trade plans).
  * `UI-006` (Unified Research Artifact Explorer — Tag & artifact lineage catalog).
  * `UI-007` (Governance & Evidence Workspace — Audit explorer & Gate-CLOSED status).
* **Active Workstream**:
  * `UI-008` (Institutional AI Experience — Active development phase).
* **Successors (Pending Workstreams)**:
  * `UI-009` (Institutional Design System Implementation).
  * `UI-010` (Accessibility & Operator Experience).
  * `UI-011` (Institutional Refinement & Version 1.0 Presentation).
  * Handover to out-of-band `Doc 11 Production Readiness Certification`.

---

# 6. Existing UI-008 State

UI-008 development commenced under previous authorized cards and is anchored in the repository on branch `migration/ui008-da-itrga-reset`:

### Approved Historical Milestones:
1. **UI-008 P01 Safety Foundation Slice** (Commit `9b1bdf0` · Tag `UI-008-P01_APPROVED` · Verdict D-30):
   - Refusal taxonomy fixture (`ui008_refusal_taxonomy.fixture.ts`).
   - Disclosure register fixture (`ui008_disclosure_register.fixture.ts`).
   - Skeleton surfaces: `AssistantCommandSurface.tsx`, `AssistantAuditSubSection.tsx`, `AssistantReviewSubPanel.tsx`.
   - Disabled-state refusal testing: `ui008_assistant_disabled_state_refusal_persisted_and_audited.test.ts`.
   - Mount points in `GovernanceEvidencePage.tsx` and `InstitutionalIntelligencePage.tsx`.
2. **UI-008 P01 M-1 Palette Navigation Slice** (Commit `30169a4` · Tag `UI-008-P01-M1_INTEGRATED` · Verdict D-45):
   - Assistant command grouping in `commandTypes.ts`.
   - 4 Navigator quick-action commands in `quickActionCatalogue.ts` (re-basing catalog from 29 to 33).
   - Shell action `open-assistant-surfaces` and optional context callback `onOpenAssistantSurface` in `commandRegistry.ts`.
   - Integration context provider: `docs/M-1_PROVIDER.md`.

---

# 7. Existing Implementation Assessment

The DA has performed a line-by-line inspection of all existing UI-008 code, fixtures, mounts, and tests:
* **Code Quality**: Clean TypeScript, strong typing, zero circular dependencies, high cohesion, and strict separation of presentation from business logic.
* **Safety Adherence**: Hardcoded disclaimers, sanitized prompt inputs, and strict absence of POST/PUT/DELETE mutation calls on trading pathways.
* **Test Health**: All 6 UI-008 dedicated test suites (25 tests) pass cleanly without warnings.
* **Architecture Conformance**: Perfectly aligns with the UI-001 shell layout and UI-002 command registry contracts.

---

# 8. Retain / Extend / Rework / Supersede / Defer / Remove Matrix

In accordance with Section 5 of the Operator Directive, every existing UI-008 artifact is formally classified:

| Artifact / Component | Classification | Technical & Governance Rationale |
|---|---|---|
| `ui008_refusal_taxonomy.fixture.ts` | **RETAIN** | Accurately codifies all 6 constitutional refusal categories; zero defects. |
| `ui008_disclosure_register.fixture.ts` | **RETAIN** | Standardizes model uncertainty, calibration disclosures, and advisory boundaries. |
| `quickActionCatalogue.ts` (33 items) | **RETAIN** | 4 Navigator labels are read-only, fully tested, and integrate cleanly with Command Palette. |
| `commandTypes.ts` & `commandRegistry.ts` | **RETAIN** | Graceful degradation pattern (`onOpenAssistantSurface` -> `onUnavailable`) is backward-compatible. |
| `AssistantCommandSurface.tsx` | **EXTEND** | Retain UI skeleton and disclaimers; extend in P02 to connect to live read-only REST API endpoints. |
| `AssistantAuditSubSection.tsx` | **EXTEND** | Retain UI layout; extend in P02 to fetch and render live refusal audit events from backend persistence. |
| `AssistantReviewSubPanel.tsx` | **EXTEND** | Retain structure; extend in P03/P04 for contextual research report explanations. |
| `docs/M-1_PROVIDER.md` | **RETAIN** | Authoritative technical record of the M-1 palette navigation delivery. |
| Dynamic External LLM APIs | **DEFER** | Strictly prohibited by constitution; deferred to post-v1.0 governed amendment if ever authorized. |
| Autonomous Chart Annotations | **DEFER** | Autonomous drawing without operator confirmation is deferred per Wave 5/7 design rules. |

*Summary*: **4 Retained**, **3 Extended**, **0 Reworked**, **0 Superseded**, **2 Deferred**, **0 Removed**.

---

# 9. Clean UI-008 Baseline

The DA establishes the **clean UI-008 baseline anchored at commit `30169a4` (tag `UI-008-P01-M1_INTEGRATED`)**.

This clean baseline:
1. Retains all verified P01 safety fixtures, skeleton surfaces, and M-1 command registry extensions.
2. Maintains complete test regression invariance across all 66 frontend test suites (295 tests) and 414 backend tests.
3. Prepares the workspace for structured forward implementation without code churn, regressions, or procedural ambiguity.

---

# 10. UI-008 Target End State

When UI-008 reaches complete delivery (at Phase P06), the **Institutional AI Experience** will present the following unified characteristics:

* **Surfaces & Accessibility**:
  * **Global Navigator Assistant**: Accessible from any workspace via `Ctrl+K` or the Command Bar.
  * **Contextual Research Assistant**: Docked in the Context Panel on `/intelligence`, `/investigation`, and `/charts`, automatically providing insights relevant to the active market or artifact.
  * **Assistant Audit & Refusal Explorer**: Embedded in `/governance`, providing full visibility into system refusals and query lineage.
  * **Documentation & Formula Lookup**: In-app searchable knowledge base for platform architecture and statistical definitions.
* **Information Consumed & Displayed**:
  * Consumes persisted research reports, regime classifications, calibration metrics, correlation matrices, and audit logs.
  * Displays explainable rationales, contributing indicator weights, scenario comparisons, and historical analogues.
* **Forbidden Capabilities (Hard Invariants)**:
  * **NO live order placement, trade sizing, or broker actuation.**
  * **NO external LLM API calls.**
  * **NO speculative profit predictions or ungrounded claims.**
  * **NO unauthenticated access or cross-operator data leakage.**
* **Refusals & Disclosures**:
  * Displays verbatim refusal badges with exact reason codes.
  * Embeds permanent `"RESEARCH-ONLY · NON-ACTUATING"` warning banners on every surface.

---

# 11. Complete Phase Structure

UI-008 progresses through 6 sequentially bounded phases:

```
  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
  │  UI-008-P01  │ ──► │  UI-008-P02  │ ──► │  UI-008-P03  │
  │ Safety/Shell │     │  API Wiring  │     │ Context Embed│
  └──────────────┘     └──────────────┘     └──────────────┘
                                                   │
  ┌──────────────┐     ┌──────────────┐            │
  │  UI-008-P06  │ ◄── │  UI-008-P05  │ ◄──────────┘
  │ Completion CK│     │ Docs Lookup  │
  └──────────────┘     └──────────────┘
```

---

# 12. Phase P01 Design — Safety Foundation & Shell Surfaces

* **Identifier**: `UI-008-P01`
* **Status**: **APPROVED & RE-BASELINED** (Verdicts D-30 & D-45 · Commit `30169a4`)
* **Objective**: Establish the constitutional safety taxonomy, disclosure registers, skeleton assistant surfaces, and Command Palette navigation quick actions.
* **Scope**:
  * Refusal taxonomy fixture (`ui008_refusal_taxonomy.fixture.ts`).
  * Disclosure register fixture (`ui008_disclosure_register.fixture.ts`).
  * Skeleton surfaces (`AssistantCommandSurface`, `AssistantAuditSubSection`, `AssistantReviewSubPanel`).
  * 4 Assistant quick-action commands (re-basing catalogue from 29 to 33).
  * Shell action `open-assistant-surfaces` with graceful degradation.
* **Out of Scope**: Live API wiring, external AI calls, order actuation.
* **Inputs**: Existing UI-001 shell layout, UI-002 Command Registry.
* **Outputs**: `frontend/src/workstation/ai/`, `frontend/src/workstation/commands/` updates, test fixtures.
* **Security**: Client-side refusal taxonomy enforcement, zero-actuation guarantees.
* **UI/UX**: Standard dark-first panel styling, mandatory disclaimers, keyboard navigation.
* **Tests**: 6 dedicated test suites (25 tests passing).
* **Evidence**: Vitest execution transcripts, byte-preserved SHA-256 manifests.
* **Dependencies**: UI-001, UI-002, UI-007 completed.
* **Exit Criteria**: All safety fixtures in place, skeleton surfaces mounted, all tests passing (exit 0).
* **Governance Boundary**: Approved by ITRGA (Verdicts D-30 / D-45).

---

# 13. Phase P02 Design — API Seam & Data Integration

* **Identifier**: `UI-008-P02`
* **Status**: **NEXT AUTHORIZED PHASE CANDIDATE**
* **Objective**: Wire assistant presentation surfaces to existing read-only backend collaboration and persistence endpoints.
* **Scope**:
  * Typed API client service for assistant responses (`GET /api/v1/collaboration/assistant-responses`) and refusal audit events (`GET /api/v1/persistence/audit-events?category=SECURITY`).
  * React hooks (`useAssistantResponses`, `useAssistantAudit`) with loading, error, and empty states.
  * Update `AssistantCommandSurface` and `AssistantAuditSubSection` to consume live API data.
  * Strict 401 unauthenticated session handling (redirect/guard).
* **Out of Scope**: New backend endpoints, database migrations, WebSocket streams, write/mutation calls.
* **Inputs**: Backend collaboration API (`app/api/routes/collaboration.py`), P01 skeleton components.
* **Outputs**: `frontend/src/api/assistantClient.ts`, updated React components and test suites.
* **Architecture**: Client-side service layer interacting exclusively via HTTP GET with JWT authorization.
* **Security**: Zero Trust, token authentication, SAL-3 data handling, no secret exposure.
* **UI/UX**: Skeleton loading placeholders, graceful error handling, responsive table layouts.
* **Tests**: API mocking tests, 401 unauth tests, empty state tests, regression suite.
* **Evidence**: Vitest test logs, network inspection transcripts, TypeScript build validation.
* **Dependencies**: UI-008-P01 approved baseline.
* **Exit Criteria**: Live assistant responses and refusal logs render correctly; 100% tests pass.
* **Governance Boundary**: Requires ITRGA Build Order `BUILD_ORDER_UI-008-P02`.

---

# 14. Phase P03 Design — Contextual Assistant & Workspace Embedding

* **Identifier**: `UI-008-P03`
* **Status**: **PROPOSED**
* **Objective**: Embed context-aware assistant panels into the Context Panel across primary analytical workspaces.
* **Scope**:
  * Context-aware assistant panel component (`ContextualAssistantPanel.tsx`).
  * Workspace integration into `/intelligence` (Market Intelligence context), `/investigation` (Signal Investigation context), and `/charts` (Active Symbol context).
  * Automated contextual prompt suggestions based on selected symbol/timeframe/artifact.
* **Out of Scope**: Autonomous chart manipulation, order execution, client-side recomputation.
* **Inputs**: UI-003 Market Workspace, UI-004 Intelligence Workspace, UI-005 Investigation Workspace.
* **Outputs**: `frontend/src/workstation/ai/ContextualAssistantPanel.tsx`, context provider wiring.
* **Architecture**: Subscribed to active workspace context via React Context; decoupled presentation.
* **Security**: Read-only context inspection; no privilege escalation.
* **UI/UX**: Collapsible panel in Region D (Context Panel), non-intrusive prompt chips, dark-first styling.
* **Tests**: Context synchronization tests, workspace switching tests, accessibility checks.
* **Evidence**: Browser DOM snapshots, context-switch test transcripts.
* **Dependencies**: UI-008-P02 completed.
* **Exit Criteria**: Contextual assistant dynamically adapts to active workspace without layout disruption.
* **Governance Boundary**: Requires ITRGA Build Order `BUILD_ORDER_UI-008-P03`.

---

# 15. Phase P04 Design — Artifact Lineage & Report Summarization

* **Identifier**: `UI-008-P04`
* **Status**: **PROPOSED**
* **Objective**: Provide explainable, deterministic summarization of institutional research reports and artifact lineage.
* **Scope**:
  * Report summarizer view (`ResearchReportSummarizer.tsx`) for Regime Reports, Correlation Reports, and Scenario Simulations.
  * Visual lineage tree display connecting raw market inputs -> ML features -> advisory outputs -> assistant explanations.
  * Verbatim uncertainty metrics and calibration status badges.
* **Out of Scope**: Dynamic report generation, modification of historical research records.
* **Inputs**: UI-004 research reports, UI-006 artifact explorer catalog.
* **Outputs**: `frontend/src/workstation/ai/ResearchReportSummarizer.tsx`, lineage visualization components.
* **Architecture**: Consumes read-only artifact metadata; renders deterministic summaries.
* **Security**: Preserves artifact immutability; strict redaction of sensitive markers.
* **UI/UX**: Clear visual badges for confidence levels (High/Moderate/Limited), expandable lineage tree.
* **Tests**: Report summarization rendering tests, lineage integrity tests, uncertainty display tests.
* **Evidence**: Visual test outputs, DOM structure validation.
* **Dependencies**: UI-008-P03 completed.
* **Exit Criteria**: Research reports and artifact lineages render with explainable summaries and uncertainty disclosures.
* **Governance Boundary**: Requires ITRGA Build Order `BUILD_ORDER_UI-008-P04`.

---

# 16. Phase P05 Design — Documentation Lookup & Operator Guidance

* **Identifier**: `UI-008-P05`
* **Status**: **PROPOSED**
* **Objective**: Provide an integrated in-app documentation and knowledge lookup surface.
* **Scope**:
  * Documentation lookup panel (`DocumentationLookupSurface.tsx`).
  * Searchable index of platform architecture, statistical formulas, indicator definitions, and governance rules.
  * Quick-action integration with Command Palette (`qa.open.documentation-lookup`).
* **Out of Scope**: External web browsing, uncontrolled search queries, external LLM lookups.
* **Inputs**: Local platform documentation corpus (`docs/governance/`, `docs/api/`).
* **Outputs**: `frontend/src/workstation/ai/DocumentationLookupSurface.tsx`, static document index.
* **Architecture**: Local client-side static indexing with fast fuzzy search.
* **Security**: Sandboxed documentation rendering; no script execution in Markdown previews.
* **UI/UX**: Split-pane search and reading view, keyboard shortcut support (`Esc` to close).
* **Tests**: Search indexing tests, Markdown rendering safety tests, keyboard navigation tests.
* **Evidence**: Search query test logs, accessibility verification.
* **Dependencies**: UI-008-P04 completed.
* **Exit Criteria**: Operators can search and view all governance/technical documentation in-app.
* **Governance Boundary**: Requires ITRGA Build Order `BUILD_ORDER_UI-008-P05`.

---

# 17. Phase P06 Design — Completion Checkpoint & Whole-Surface Verification

* **Identifier**: `UI-008-P06`
* **Status**: **PROPOSED (FINAL WORKSTREAM PHASE)**
* **Objective**: Execute comprehensive whole-surface verification, regression testing, and handover to ITRGA for final UI-008 completion declaration.
* **Scope**:
  * Dedicated completion test suite (`InstitutionalAICompletion.test.tsx`).
  * Whole-surface no-actuation grep proofs (`order`, `buy`, `sell`, `execute`, `trade`).
  * Whole-surface no-external-AI grep proofs (`openai`, `anthropic`, `langchain`, `external_llm`).
  * Full regression testing across entire frontend (all test files) and backend (all 414 tests).
  * Level-I directly verified browser evidence and Delivery Report preparation.
* **Out of Scope**: New features, architectural modifications.
* **Inputs**: All delivered P01–P05 artifacts and test suites.
* **Outputs**: `InstitutionalAICompletion.test.tsx`, `DELIVERY_REPORT_UI-008-P06.md`, evidence package.
* **Architecture**: Verification harness confirming system integrity and governance compliance.
* **Security**: Final security posture audit, SAL-3 compliance confirmation, RBAC validation.
* **UI/UX**: Final accessibility audit (WCAG 2.1 AA), brand governance compliance (Doc 16).
* **Tests**: Complete test suite execution with 100% pass rate and zero regressions.
* **Evidence**: Full execution transcripts, test logs, DOM snapshots, grep proofs.
* **Dependencies**: UI-008-P01 through P05 completed.
* **Exit Criteria**: All completion tests pass; zero actuation paths proven; ITRGA declares UI-008 COMPLETE.
* **Governance Boundary**: Final ITRGA milestone review and workstream closeout determination.

---

# 18. Cross-Phase Architecture

UI-008 enforces Clean Architecture principles across all phases:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER (FRONTEND)                       │
│  ┌───────────────────────────┐       ┌───────────────────────────────┐  │
│  │ AssistantCommandSurface   │ ◄───► │ CommandRegistry & QuickAction │  │
│  ├───────────────────────────┤       ├───────────────────────────────┤  │
│  │ ContextualAssistantPanel  │ ◄───► │ Workspace Context Providers   │  │
│  ├───────────────────────────┤       ├───────────────────────────────┤  │
│  │ ResearchReportSummarizer  │ ◄───► │ Artifact & Lineage Stores     │  │
│  ├───────────────────────────┤       ├───────────────────────────────┤  │
│  │ AssistantAuditSubSection  │ ◄───► │ Governance Audit Explorer     │  │
│  └─────────────┬─────────────┘       └───────────────────────────────┘  │
└────────────────┼────────────────────────────────────────────────────────┘
                 │ (Typed Async Client Hooks / Bearer JWT)
┌────────────────▼────────────────────────────────────────────────────────┐
│                      APPLICATION & BACKEND SERVICES                     │
│  ┌───────────────────────────┐       ┌───────────────────────────────┐  │
│  │ /collaboration/assistant  │ ────► │ AssistantResearchResponseRepo │  │
│  ├───────────────────────────┤       ├───────────────────────────────┤  │
│  │ /persistence/audit-events │ ────► │ AuditPersistenceService       │  │
│  └───────────────────────────┘       └───────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

# 19. Security Model & SAL Classification

In accordance with `17_INSTITUTIONAL_SECURITY_STANDARD.md`:
* **Classification**: UI-008 components are categorized as **`SAL-3` (Institutional Confidential Information)**.
* **Zero Trust Policy**: Every API request is authenticated via Bearer JWT; unauthenticated calls are rejected with 401.
* **Input Validation & Sanitization**: All user inputs undergo client-side sanitization against XSS, script injection, and SQL injection patterns.
* **Refusal Auditing**: Any attempt to elicit restricted actions triggers an immutable audit log entry.
* **Zero External Network Exfiltration**: No network requests are made outside the governed backend API origin.

---

# 20. UI/UX Model & Brand Governance

In accordance with `08_UI_UX_SPEC.md` and `16_BRAND_GOVERNANCE_STANDARD.md`:
* **Theme**: Dark-first institutional palette (`#0B0E14` base, `#1A1F2C` panels, `#2563EB` accent, `#10B981` success, `#F59E0B` warning, `#EF4444` critical).
* **Typography**: Monospace numerals for timestamps/hashes, clean sans-serif for UI copy.
* **Accessibility**: Full keyboard navigability (`Tab` focus rings, `Enter` execution, `Esc` dismissal), ARIA landmarks, contrast ratios `>4.5:1`.
* **State Indicators**: Skeleton loaders during network fetch; clear error banners with recovery guidance.

---

# 21. API and Data Architecture

* **Assistant Responses Seam**:
  * Method: `GET /api/v1/collaboration/assistant-responses`
  * Query: `limit: int = 50`
  * Response Model: `List[AssistantResearchResponseRead]`
  * Read-Only: Strictly immutable; responses represent historical research records.
* **Audit Events Seam**:
  * Method: `GET /api/v1/persistence/audit-events`
  * Query: `category: str = "SECURITY"`, `limit: int = 50`
  * Response Model: `List[AuditEventRead]`

---

# 22. Testing Strategy

Multi-tier testing is enforced for every phase:
1. **Unit Testing**: Isolated component rendering, prop handling, and state transitions.
2. **Mock API Integration Testing**: Verification of HTTP client hooks, loading states, error boundaries, and 401 unauth handling.
3. **Negative & Edge-Case Testing**: Empty datasets, malformed payloads, excessive input lengths, and refusal rendering.
4. **Whole-Surface Grep Testing**: Automated scanning verifying the complete absence of actuation controls and external LLM references.
5. **Full Regression Testing**: Invariant execution of all 66 frontend test suites and 414 backend tests.

---

# 23. Evidence Strategy

In accordance with `09_ITRGA_REASONING_FRAMEWORK.md`:
* **Level-I Evidence (Direct Runtime)**: Captured browser DOM snapshots, HTTP request/response transcripts, raw database read-backs.
* **Level-II Evidence (Automated Tests & Builds)**: Unaltered Vitest test run logs, Pytest test logs, TypeScript compiler outputs (`tsc -b`).
* **Level-III Evidence (Documentary)**: Phase delivery reports, design plan references, and ADRs.

---

# 24. Documentation and State Management

* **Authoritative State Files**: `PROJECT_STATE.md`, `CHANGELOG.md`, `RISK_REGISTER.md`, `TECHNICAL_DEBT_REGISTER.md`.
* **Maintenance Ownership**: Development Authority updates state documents upon each phase completion.
* **Update Triggers**: Formal ITRGA phase approvals and Build Order completions.

---

# 25. Technical Debt Management

The DA tracks and manages the following active items:
1. `TD-UI-POSTCSS-HIGH`: PostCSS supply-chain vulnerability (Carried pre-certification blocker; scheduled for separate remediation).
2. `OBS-P06-2`: Governance audit refusal reachability window (Carried from UI-007; addressed via pagination in governance).
3. `UI-008 Placeholder Seams`: Optional context callbacks (`onOpenAssistantSurface`) cleanly resolve as phases are implemented.

---

# 26. Risk Register (UI-008 Workstream Risks)

| Risk ID | Risk Description | Severity | Likelihood | Mitigation Strategy |
|---|---|---|---|---|
| **R-UI008-1** | Accidental actuation affordance on assistant surface | High | Low | Automated whole-surface grep tests; read-only component architecture. |
| **R-UI008-2** | Ambiguity between advisory insight and guaranteed performance | High | Low | Permanent mandatory disclaimers and prominent uncertainty intervals. |
| **R-UI008-3** | External LLM dependency creep | High | Low | Hard architectural boundary; no external HTTP client libraries permitted. |
| **R-UI008-4** | Client-side performance degradation during search/lineage | Med | Low | Virtualized lists, debounced inputs, memoized rendering. |

---

# 27. Dependencies Summary

* **Technical**: React 18, TypeScript 5, Vite, Vitest, React Router 6.
* **Architectural**: UI-001 shell layout, UI-002 Command Registry, UI-007 Audit Explorer.
* **Security**: Bearer JWT auth context, SAL-3 data handling.
* **Governance**: Formal ITRGA review and Build Order authorization per phase.

---

# 28. Completion Criteria for Workstream UI-008

UI-008 will be declared complete when:
1. All phases P01 through P06 have been implemented and approved by ITRGA.
2. All assistant surfaces (`CommandSurface`, `ContextualPanel`, `ReportSummarizer`, `AuditSubSection`, `DocsLookup`) are fully operational.
3. 100% of frontend and backend tests pass with zero regressions.
4. Whole-surface grep tests prove zero actuation controls and zero external LLM dependencies.
5. All documentation (`PROJECT_STATE.md`, `CHANGELOG.md`) is fully synchronized.

---

# 29. Governance Gates

```
  [ Design Plan Submission ] ──► [ ITRGA Re-baseline Determination ]
                                            │ (If Approved)
                                            ▼
                               [ BUILD_ORDER_UI-008-P02 ]
                                            │
                               [ DA Implementation & Testing ]
                                            │
                               [ Delivery Report & Evidence ]
                                            │
                               [ ITRGA Phase Determination ] ──► Next Phase
```

---

# 30. Open Questions & Declarations

* **Declaration 1**: The Development Authority affirms that all existing P01 and M-1 implementations are sound and verified.
* **Declaration 2**: No dynamic LLM services are required or proposed for Version 1.0.
* **Declaration 3**: Implementation remains strictly on hold pending ITRGA Build Order authorization.

---

# 31. Development Authority Recommendation

The Development Authority formally recommends:
1. **Re-baseline Approval**: That ITRGA accept this reconciled Design Plan and confirm the clean baseline anchored at commit `30169a4`.
2. **Build Order Issuance**: That ITRGA issue **`BUILD_ORDER_UI-008-P02` (API Seam & Data Integration)** to initiate Phase P02 implementation.

---

**We don't guess. We prove.**

*— AXIOM Development Authority (DA)*
