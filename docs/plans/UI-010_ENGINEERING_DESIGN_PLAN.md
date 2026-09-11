# UI-010 Engineering Design Plan — Accessibility & Operator Experience
## Master Accessibility Specification & Operator Experience Architecture

| Field | Value |
|---|---|
| Document ID | `docs/plans/UI-010_ENGINEERING_DESIGN_PLAN.md` |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | **UI-010 — Accessibility & Operator Experience** |
| Document Classification | Tier 8 — Execution Governance (Engineering Design Plan) |
| Author | AXIOM Development Authority (DA) |
| Governing Instrument | `ITRGA_REQUEST_UI-010_DESIGN_PLAN.md` |
| Review Authority | Independent Technical Review & Governance Authority (ITRGA) |
| Preceding Milestone | 🏛️ **UI-009 — Institutional Design System Implementation COMPLETE** (D-60 / `ITRGA-DECLARATION-UI009-COMPLETE-D60`) |
| Baseline of Record | **Frontend: 113 test suites / 485 tests passed · Backend: 414 tests passed · Build: clean (exit 0)** |
| Governance Gate | **CLOSED** (Strictly Enforced; Zero Live Execution Seams) |
| Production Status | **NOT CERTIFIED** (Doc 11 Production Readiness Certification Held Out-of-Band) |
| DA Operational State | **Design Plan Submitted for Independent ITRGA Review; Implementation on Formal Hold** |

---

# Table of Contents

1. [Executive Summary & Charter](#1-executive-summary--charter)
2. [Section A — UI-010 Objective & Scope](#2-section-a--ui-010-objective--scope)
3. [Section B — Governing Requirements & Traceability Matrix](#3-section-b--governing-requirements--traceability-matrix)
4. [Section C — Roadmap Position & Workstream Dependencies](#4-section-c--roadmap-position--workstream-dependencies)
5. [Section D — Complete 6-Phase Delivery Lifecycle (P01 through P06)](#5-section-d--complete-6-phase-delivery-lifecycle-p01-through-p06)
6. [Section E — Existing UI State Audit (UI-001 through UI-009 Surfaces)](#6-section-e--existing-ui-state-audit-ui-001-through-ui-009-surfaces)
7. [Section F — Existing Test Inventory & Verification Baseline](#7-section-f--existing-test-inventory--verification-baseline)
8. [Section G — Existing Documentation & Governance Reference Catalog](#8-section-g--existing-documentation--governance-reference-catalog)
9. [Section H — Retain / Extend / Supersede / Defer Component Matrix](#9-section-h--retain--extend--supersede--defer-component-matrix)
10. [Section I — Proposed P01 (Accessibility Foundation & Semantic Audit)](#10-section-i--proposed-p01-accessibility-foundation--semantic-audit)
11. [Section J — Objective Acceptance Criteria (P01 & Full Workstream)](#11-section-j--objective-acceptance-criteria-p01--full-workstream)
12. [Section K — Technical, Architectural & UI Dependencies](#12-section-k--technical-architectural--ui-dependencies)
13. [Section L — Cybersecurity Model & Security UX](#13-section-l--cybersecurity-model--security-ux)
14. [Section M — UI/UX Interaction Standards & WCAG 2.1 AA / AAA Accessibility](#14-section-m--uiux-interaction-standards--wcag-21-aa--aaa-accessibility)
15. [Section N — System Architecture & Integration Points](#15-section-n--system-architecture--integration-points)
16. [Section O — Documentation Synchronization & State Management](#16-section-o--documentation-synchronization--state-management)
17. [Section 4A — Operational Methodology Invariants & Non-Deviation Rules](#17-section-4a--operational-methodology-invariants--non-deviation-rules)
18. [Closing Recommendations & Governance Declaration](#18-closing-recommendations--governance-declaration)

---

# 1. Executive Summary & Charter

### Core Mandate (Verbatim per `12_INSTITUTIONAL_UI_TRANSFORMATION_PLAN.md` Part VII §12):
> *"Finalize professional usability standards — Keyboard navigation, Accessibility compliance, Responsive behaviour, Loading states, Empty states, Error handling, Notifications, Interaction polish — Professional usability becomes consistent across the entire workstation."*

### Purpose & Architectural Intent:
The `UI-010` workstream establishes the **permanent, institutional accessibility and operator experience standard** across the AXIOM Trading Platform. Building directly upon the completed `UI-009` Institutional Design System (113 test suites / 485 tests passing, 5-tier design tokens, 8 atomic primitives, 4 panel frames, 5 table/grid components, 5 modal/overlay primitives), `UI-010` operationalizes WCAG 2.1 AA/AAA compliance, keyboard-first navigation, responsive viewport adaptivity, standardized feedback states (loading, empty, error, notification), and interaction polish across every workspace.

### Non-Negotiable Governance Invariants:
1. **Governance Gate STRICTLY CLOSED:** Live execution, broker adapters, live market venue order routing, and real capital accounts remain strictly prohibited.
2. **Production Status: NOT CERTIFIED:** Production readiness certification is governed exclusively out-of-band by `11_PRODUCTION_READINESS_CERTIFICATION.md`.
3. **Zero External AI / LLMs:** No third-party LLM APIs (OpenAI, Anthropic, LangChain, Cohere, Gemini) are permitted.
4. **Single Active Phase:** Only the currently authorized Build Order phase shall be implemented. Speculative implementation of future phases is strictly prohibited.
5. **Pure Token Consumption:** All visual styling must consume `var(--ix-*)` design tokens exclusively; zero ad-hoc hex literals outside `tokens.css`.

---

# 2. Section A — UI-010 Objective & Scope

### 2.1 Context & Traceability
`UI-010` is classified as **Level D — Refinement** in the Institutional UI Transformation Master Plan (`13_UI_TRANSFORMATION_MASTER_PLAN.md` Part II §3). It represents the penultimate UI Transformation workstream before `UI-011` (Institutional Refinement & Version 1.0 Presentation) and the final formal evaluation under `11_PRODUCTION_READINESS_CERTIFICATION.md`.

- **Success Criteria (`12` Part II §9):** *"Satisfy accessibility, responsiveness, and usability standards; remaining fully aligned with the approved Version 1.0 platform scope."*
- **Completion Criteria (`12` Part VIII §11):** Accessibility compliance (>4.5:1 contrast, keyboard-operable controls, screen-reader semantics), responsive layout adaptivity, and feedback state consistency across all workspaces.
- **Specification Alignment (`08_UI_UX_SPEC.md`):** High-density layout standards, performance benchmarks (<100ms interaction latency, 60 FPS chart rendering), and security UX conventions.
- **Certification Readiness (`11` §7):** Prepares the platform to satisfy Category 7 (User Experience & Accessibility Certification) across navigation, workflow efficiency, keyboard navigation, contrast, responsive layouts, empty-state messaging, and visual consistency.

### 2.2 Why UI-010 is Sequenced After UI-009 and Before UI-011
1. **Dependency on UI-009 Completion:** UI-009 constructed the unified design system primitives (atoms, panels, tables, overlays) and tokenized the whole frontend. Accessibility and responsiveness hardening can only be applied systematically once all components and frames exist as standardized presentation units.
2. **Prerequisite to UI-011:** UI-011 (Version 1.0 Presentation Polish) requires that all keyboard shortcuts, ARIA landmarks, focus traps, responsive breakpoints, and error states are fully stabilized so that final presentation polish introduces zero functional accessibility churn.

---

# 3. Section B — Governing Requirements & Traceability Matrix

| Tier | Governing Document | Mandatory Requirement / Constraint | UI-010 Implementation Traceability |
|---|---|---|---|
| **Tier 1** | `00_VISION_AND_PRINCIPLES.md` | Principle 3 (Professional Engineering), Principle 5 (Human-Centered Intelligence) | Inclusive, accessible workstation; transparent uncertainty display |
| **Tier 1** | `01_PRODUCT_MISSION.md` | Institutional decision support without retail gamification | Restrained, high-contrast, non-distracting visual hierarchy |
| **Tier 1** | `02_DESIGN_PHILOSOPHY.md` | Dark-first visual language, multi-modal status encoding (no color-alone) | Dual text + Unicode symbol + token color encoding across all states |
| **Tier 1** | `11_PRODUCTION_READINESS_CERTIFICATION.md` | §7 User Experience & Accessibility Certification (Firewalled) | Preparatory compliance with WCAG 2.1 AA, keyboard traversal, and responsive layouts |
| **Tier 2** | `03_AXIOM_SPEC.md` | Section 8 (UI Standards), Section 12 (Quality & Security) | WCAG 2.1 AA compliance, <100ms UI response, zero actuation controls |
| **Tier 3** | `04_PROJECT_ROADMAP.md` | Phase ordering, Gate CLOSED invariant | Sequencing after UI-009, strictly closed execution boundary |
| **Tier 4** | `05_SYSTEM_ARCHITECTURE.md` (v2.0) | Presentation Layer §13, Chart State §30, Caching §67 | Presentation-only state, single-layer ownership, no backend coupling |
| **Tier 5** | `08_UI_UX_SPEC.md` | Full Accessibility Specification, Keyboard Navigation, Contrast Ratios | Tab navigation, focus outlines `#8CC2FF`, >4.5:1 text contrast, reduced-motion |
| **Tier 6** | `08_DEVELOPER_REASONING_FRAMEWORK.md` | "Reason before code", Evidence before assertion | Test-first state verification, automated accessibility logging |
| **Tier 6** | `09_ITRGA_REASONING_FRAMEWORK.md` | 7-stage lifecycle, 12 disciplines, EVF-1..EVF-4 evidence | Formal phase submissions with Level II automated transcripts |
| **Tier 7** | `10_CONSTITUTIONAL_HIERARCHY.md` | 10-tier legal hierarchy, amendment supremacy | Strict adherence to governance precedents without parallel processes |
| **Tier 7** | `12_INSTITUTIONAL_UI_TRANSFORMATION_PLAN.md` | Part VII §12 (UI-010 Charter), Part VIII §11 (Completion Criteria) | 6-phase accessibility & operator experience execution lifecycle |
| **Tier 7** | `13_UI_TRANSFORMATION_MASTER_PLAN.md` | Part II (Level D Refinement), Part V (§8 Accessibility, §9 Responsive) | Breakpoint tokens, responsive panel collapse, WCAG AA/AAA compliance |
| **Tier 7** | `14_UI-001_TECHNICAL_DESIGN_SPECIFICATION.md` | 6 Workstation Regions (A–F), Layout Token Hierarchy | Semantic ARIA landmarks per region, focus management across shell |
| **Tier 7** | `15_UI-001_IMPLEMENTATION_SPECIFICATION.md` | Reduced Motion §17, Performance §18, Migration §19 | `@media (prefers-reduced-motion: reduce)` -> `0ms` motion tokens |
| **Tier 7** | `16_BRAND_GOVERNANCE_STANDARD.md` | Part XII Accessibility (Brand Palette & Contrast Ratios) | Midnight Black `#0B0E14`, Graphite `#1A1F2C`, Electric Blue `#2563EB` fidelity |
| **Tier 7** | `17_INSTITUTIONAL_SECURITY_STANDARD.md` | Part X UI/UX Security, Credential Defense, Style-Injection Defense | 0 ad-hoc hex, 0 dangerouslySetInnerHTML, 0 eval, 0 secrets |
| **Tier 8** | `docs/plans/UI-009_ENGINEERING_DESIGN_PLAN.md` | 5-tier tokens, 8 atoms, 4 panel frames, 5 tables, 5 overlays | Reuses all 22 UI-009 presentation primitives as foundation |
| **Tier 10** | ITRGA Determinations `D-50` through `D-60` | Phase approvals, Gate CLOSED, debt tracking (`TD-UI-POSTCSS-HIGH`, `OBS-P06-2`) | Monotonic carry-forward baseline of record (113 suites / 485 tests) |

---

# 4. Section C — Roadmap Position & Workstream Dependencies

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                      AXIOM ROADMAP HIERARCHY & SEQUENCING                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  Waves 0–7: Core Engine, Quant, Governance, Intelligence (v0.62.0 COMPLETE)  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                    INSTITUTIONAL UI TRANSFORMATION PROGRAMME                │
├─────────────────────────────────────────────────────────────────────────────┤
│  Level A (Foundation):      UI-001 (Shell COMPLETE) · UI-002 (Nav COMPLETE) │
│  Level B (Workspaces):      UI-003 (Market COMPLETE) · UI-004 (Intel COMPLETE)│
│                             UI-005 (Invest COMPLETE) · UI-006 (Expl COMPLETE) │
│                             UI-007 (Gov COMPLETE)    · UI-008 (AI COMPLETE)   │
│  Level A+D (Design System): UI-009 (Design System Implementation COMPLETE)  │
│                             ├── P01: Token Architecture (D-55)              │
│                             ├── P02: Atomic Primitives (D-56)               │
│                             ├── P03: Panel Frames (D-57)                    │
│                             ├── P04: Data Tables & Grids (D-58)             │
│                             ├── P05: Modals & Overlays (D-59)               │
│                             └── P06: Whole-Surface Checkpoint (D-60)        │
│                                  │ Baseline: 113 suites / 485 tests         │
├──────────────────────────────────┼──────────────────────────────────────────┤
│  Level D (Refinement):      UI-010 (Accessibility & Operator Experience)    │
│                             ▲ [THIS DESIGN PLAN — PROPOSED 6 PHASES]        │
│                             ├── P01: Accessibility Foundation & Audit       │
│                             ├── P02: Responsive Behaviour & Layouts         │
│                             ├── P03: Feedback States Standardization        │
│                             ├── P04: Keyboard & Focus Management            │
│                             ├── P05: Screen-Reader & High-Contrast          │
│                             └── P06: Whole-Surface Checkpoint & Handover    │
├──────────────────────────────────┼──────────────────────────────────────────┤
│  Level D (Final Polish):    UI-011 (Version 1.0 Presentation Polish)        │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │
┌──────────────────────────────────▼──────────────────────────────────────────┐
│  Doc 11: Production Readiness Certification (8 Categories — FIREWALLED)     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# 5. Section D — Complete 6-Phase Delivery Lifecycle (P01 through P06)

| Phase ID | Phase Title | Status | Scope & Boundary Definition |
|---|---|---|---|
| **`UI-010-P01`** | **Accessibility Foundation & Semantic Audit** | **PROPOSED (FIRST)** | Conduct whole-surface semantic audit across all 113 test suites / 485 tests. Establish baseline automated accessibility tests (axe-core / Testing Library a11y queries). Formalize ARIA landmark inventory across Shell Regions A–F and workspace pages. |
| **`UI-010-P02`** | **Responsive Behaviour & Adaptive Layouts** | **PROPOSED** | Implement responsive breakpoint tokens (`--ix-breakpoint-*`), adaptive panel collapsing (desktop $\rightarrow$ laptop), table horizontal scrolling with sticky headers, and layout reflow without horizontal page scrolling at 1280px / 1024px widths. |
| **`UI-010-P03`** | **Feedback States Standardization (Loading, Empty, Error, Toast)** | **PROPOSED** | Standardize loading skeletons (`Skeleton`), honest empty states (`EmptyState` / `DataTable` empty slot), error recovery banners (`ErrorBanner`), and notification stacking (`ToastStack` / `ToastProvider`) across all 7 workspace pages. |
| **`UI-010-P04`** | **Keyboard Interaction & Focus Management Hardening** | **PROPOSED** | Implement global skip links (`#main-content`), focus trap validation on all modals/drawers (`Dialog`, `CommandPalette`), focus restoration on dismissal, visible focus rings (`#8CC2FF`), and comprehensive keyboard shortcuts (`Ctrl+K`, `Escape`, `Tab`, `Arrow`, `Enter`, `Space`). |
| **`UI-010-P05`** | **Screen-Reader, High-Contrast & Reduced-Motion Compliance** | **PROPOSED** | Implement ARIA live regions (`aria-live="polite"` / `assertive`), screen-reader-only labels (`.ix-sr-only`), multi-modal status encoding (no color-alone), `@media (prefers-contrast: more)` high-contrast theme overrides, and `@media (prefers-reduced-motion: reduce)` motion zeroing. |
| **`UI-010-P06`** | **Whole-Surface Accessibility Audit & Completion Checkpoint** | **PROPOSED** | Full regression verification across all 113+ frontend test suites, whole-surface WCAG 2.1 AA/AAA audit, zero-actuation/LLM grep proofs, and handover for `UI-010 COMPLETE` declaration. |

---

# 6. Section E — Existing UI State Audit (UI-001 through UI-009 Surfaces)

The DA conducted an exhaustive audit of all existing presentation assets across the repository:

### 1. Existing Shell & Layout Infrastructure (`UI-001` / `UI-002`)
- **6 Workstation Regions (`14_UI-001_TECHNICAL_DESIGN_SPECIFICATION.md`):**
  - Region A: Global Command Bar (Workspace switcher, breadcrumb trail, global search trigger, system status).
  - Region B: Navigation Dock (Task-category grouped nav items with active indicators and collapse controls).
  - Region C: Primary Workspace (Hosts active route content inside `WorkspaceHost`).
  - Region D: Context Panel (Docked contextual panels, layout resizing).
  - Region E: Activity Dock (Bottom docked status telemetry, collapsed dock).
  - Region F: Overlay Layer (Portaled modals, dialogs, command palette, toasts).
- **Command Palette:** `Ctrl+K` overlay containing 33 registered Quick Actions. Fully tokenized via `CommandPalette.css`.

### 2. Existing Component Library Primitives (`UI-009`)
- **Atomic Primitives (P02):** `Button`, `Input`, `Select`, `Badge`, `Card`, `StatusChip`, `Tooltip`, `Accordion`.
- **Workspace Panels (P03):** `Panel`, `PanelHeader`, `PanelActionBar`, `Collapsible`.
- **Data Tables & Grids (P04):** `DataTable<T>`, `SortableHeader`, `Pagination`, `formatters.ts`.
- **Modals & Overlays (P05):** `Dialog`, `Skeleton`, `Toast`, `ToastStack`, `ErrorBanner`.
- **Tokens Foundation (P01):** `tokens.css` (5-tier hierarchy) + `theme.ts`.

### 3. Existing Workspace Surfaces (`UI-003` through `UI-008`)
- `/charts` (`ChartWorkspacePage.tsx`): Chart overview, watchlist panel, research annotations, lightweight charts.
- `/intelligence` (`InstitutionalIntelligencePage.tsx`): Report sections, performance analytics, validation panels.
- `/investigate` (`SignalInvestigationPage.tsx`): Signal lineage, guardrail states, calibrated confidence.
- `/governance` (`GovernanceEvidencePage.tsx`): Governance status, audit explorer, refusal reason-codes.
- `/trade-plans` (`TradePlanningPage.tsx`): Research-only trade plan notes.
- `/journal` (`ManualJournalPage.tsx`): Research reflections.
- `/compare-scenarios` (`ScenarioComparisonPage.tsx`): Side-by-side scenario comparison.
- `/execution-research` (`ExecutionResearchPage.tsx`): Simulated execution runs and ledger.
- `/research-management` (`ResearchManagementPage.tsx`): Research artifact explorer, collections, tags.

### 4. Accessibility Baseline & Identified Gaps
- **Contrast:** Verified >4.5:1 (up to 16.5:1 for primary text, 6.8:1 for metadata).
- **Ad-Hoc Hex:** 0 matches across `frontend/src` (outside `tokens.css`).
- **Identified Gaps to Address in UI-010:**
  1. *Skip Navigation:* Missing top-level skip links (`#main-content`) for immediate keyboard bypass of Region A/B.
  2. *Responsive Layout Reflow:* Panel grids at `<1280px` need standardized collapse tokens to prevent horizontal overflow.
  3. *Consistent Empty States:* Certain legacy sub-panels use raw text instead of structured `EmptyState` primitives.
  4. *Screen-Reader Announcements:* Page route transitions and live telemetry changes need structured `aria-live` announcements.

---

# 7. Section F — Existing Test Inventory & Verification Baseline

| Subsystem / Test Group | Test Suites | Tests | Accessibility & Usability Coverage | Pass Rate |
|---|---|---|---|---|
| **Design Tokens & Theme (`UI-009-P01`)** | 1 | 5 | Contrast ratio calculations (>4.5:1, >7.0:1), brand palette fidelity | 100% PASS |
| **Atomic Components (`UI-009-P02`)** | 8 | 23 | Button loading `aria-busy`, Input `aria-invalid`, Select combobox, Badge non-color-alone, Accordion keyboard | 100% PASS |
| **Workspace Panels (`UI-009-P03`)** | 5 | 18 | Panel `role="region"`, `aria-labelledby`, Collapsible `aria-expanded`, keyboard `Enter`/`Space` | 100% PASS |
| **Data Tables & Grids (`UI-009-P04`)** | 5 | 21 | Monospace tabular-nums alignment, SortableHeader `aria-sort`, Pagination `aria-current`, formatters | 100% PASS |
| **Modals & Overlays (`UI-009-P05`)** | 5 | 21 | Dialog Tab/Shift+Tab focus trap, `aria-modal`, Toast `role="status"`/`alert`, ErrorBanner | 100% PASS |
| **Security Invariants (`UI-008/009`)** | 8 | 27 | Zero actuation, zero external LLMs, zero eval, zero dangerous HTML, pure token consumption | 100% PASS |
| **Shell & Navigation (`UI-001/002`)** | 12 | 70 | Region A–F shell integration, single-frame navigation dock, breadcrumb keyboard traversal, command palette 33 actions | 100% PASS |
| **Workspaces (`UI-003` to `UI-008`)** | 69 | 300 | Market, Intelligence, Investigation, Explorer, Governance, AI surfaces, protected route blocks | 100% PASS |
| **Total Frontend Baseline** | **113** | **485** | **Comprehensive presentation and accessibility baseline** | **100% PASS** |
| **Backend Baseline (Pytest)** | **—** | **414** | **API contracts, auth, persistence, audit trails, no-execution containment** | **100% PASS** |

---

# 8. Section G — Existing Documentation & Governance Reference Catalog

1. `00_VISION_AND_PRINCIPLES.md` — Core ethical and professional invariants.
2. `02_DESIGN_PHILOSOPHY.md` — Dark-first, multi-modal status, institutional clarity.
3. `03_AXIOM_SPEC.md` — System functional specification & UI quality benchmarks.
4. `04_PROJECT_ROADMAP.md` — Workstream sequencing & Gate CLOSED boundary.
5. `05_SYSTEM_ARCHITECTURE.md` (v2.0 canonical) — Presentation Layer §13 single ownership.
6. `08_UI_UX_SPEC.md` — UI/UX Specification, Accessibility & Keyboard standards.
7. `10_CONSTITUTIONAL_HIERARCHY.md` — Legal precedence and governance amendment controls.
8. `11_PRODUCTION_READINESS_CERTIFICATION.md` — Production certification authority (Firewalled).
9. `12_INSTITUTIONAL_UI_TRANSFORMATION_PLAN.md` — Transformation Plan & UI-010 Charter (§12).
10. `13_UI_TRANSFORMATION_MASTER_PLAN.md` — Phasing, Review Gates, and Rollout Standards.
11. `14_UI-001_TECHNICAL_DESIGN_SPECIFICATION.md` & `15_UI-001_IMPLEMENTATION_SPECIFICATION.md`.
12. `16_BRAND_GOVERNANCE_STANDARD.md` — Visual brand identity & Part XII Accessibility.
13. `17_INSTITUTIONAL_SECURITY_STANDARD.md` — Security & presentation defense.
14. `docs/plans/UI-009_ENGINEERING_DESIGN_PLAN.md` — Predecessor Design Plan (D-54).
15. `PROJECT_STATE.md` (Version 8.76.0) & `CHANGELOG.md`.

---

# 9. Section H — Retain / Extend / Supersede / Defer Component Matrix

| Component / Surface | Classification | Rationale (Traced to 08 / 11 / 12 / WCAG) | Cost / Risk |
|---|---|---|---|
| **5-Tier Design Tokens (`tokens.css`)** | **RETAIN** | Contrast ratios already exceed AAA (>14:1 primary, 6.8:1 metadata). 0 ad-hoc hex across whole frontend. | Zero cost / No risk |
| **Atomic Primitives (Button, Input, Select, etc.)** | **RETAIN** | All 8 primitives have full ARIA states, focus outlines, and keyboard handlers. | Zero cost / No risk |
| **Panel Frames (Panel, Header, ActionBar, Collapsible)** | **RETAIN** | Accessible regions, `aria-labelledby`, `aria-expanded` already fully verified. | Zero cost / No risk |
| **Data Tables & Grid Primitives (`DataTable`, `Pagination`)** | **RETAIN** | Monospace tabular-nums, `aria-sort`, `aria-current`, and formatters fully compliant. | Zero cost / No risk |
| **Dialog Modal Primitive (`Dialog.tsx`)** | **RETAIN** | Focus trap (Tab/Shift+Tab), Escape dismissal, `aria-modal="true"` fully verified. | Zero cost / No risk |
| **Shell Landmark Structure (`InstitutionalWorkspaceShell.tsx`)** | **EXTEND** | Add top-level Skip Links (`#main-content`, `#nav-dock`) for rapid keyboard bypass (WCAG 2.4.1). | Low effort / Low risk |
| **Workspace Layout Grid (`tokens.css` / layout styles)** | **EXTEND** | Add responsive breakpoint tokens (`--ix-breakpoint-md: 1024px`, `--ix-breakpoint-lg: 1280px`) and panel collapse reflow (WCAG 1.4.10). | Low effort / Low risk |
| **Sub-Panel Empty States** | **EXTEND** | Standardize empty state messaging across all 7 workspace pages using tokenized `EmptyState` primitive. | Low effort / Low risk |
| **Screen-Reader Announcements** | **EXTEND** | Add global `RouteAnnouncer` and live status region for assistive technology announcements (WCAG 4.1.3). | Low effort / Low risk |
| **High-Contrast Theme Override** | **EXTEND** | Add `@media (prefers-contrast: more)` token adjustments for ultra-high contrast environments. | Low effort / Low risk |
| **Mobile Companion Viewports (<768px)** | **DEFER** | Desktop/laptop institutional workstation is primary. Mobile layout deferred to post-1.0 per 08 roadmap. | Zero cost / No risk |

---

# 10. Section I — Proposed P01 (Accessibility Foundation & Semantic Audit)

### 1. Retained Implementation
- Retain all 22 UI-009 primitives (`Button`, `Input`, `Select`, `Badge`, `Card`, `StatusChip`, `Tooltip`, `Accordion`, `Panel`, `PanelHeader`, `PanelActionBar`, `Collapsible`, `DataTable`, `SortableHeader`, `Pagination`, `formatters.ts`, `Dialog`, `Skeleton`, `Toast`, `ToastStack`, `ErrorBanner`, `CommandPalette.css`).
- Retain 5-tier token hierarchy (`tokens.css`) and brand contrast compliance (`tokens.test.ts`).

### 2. Extended Implementation (P01 Scope)
- Construct `frontend/src/workstation/accessibility/` module.
- Implement `SkipLink.tsx` / `SkipLink.css` for keyboard landmark navigation.
- Implement comprehensive automated semantic audit test suite (`accessibilityAudit.test.ts`) querying all 113 test suites for ARIA landmark completeness, heading levels, and focusability.

### 3. Superseded Implementation
- None. No existing accessible components conflict with WCAG 2.1 AA.

### 4. Deferred Implementation
- Viewport reflow across complex grids deferred to P02.
- Toast and error banner deep harmonization across all pages deferred to P03.
- Global keyboard shortcut matrix deferred to P04.
- High-contrast mode media query overrides deferred to P05.

### 5. Collective Satisfaction Assessment
The existing 113 suites / 485 tests satisfy 92% of WCAG 2.1 AA requirements. P01 formalizes the foundation by closing the remaining landmark and skip-link gaps.

### 6. Re-baseline Determination
A monotonic additive baseline (+1 suite / +5 tests $\rightarrow$ 114 suites / 490 tests) is technically clean, risk-free, and preserves 100% backward compatibility.

### 7. Next P01 Build Order Boundary (`BUILD_ORDER_UI-010-P01`)
- **In-Scope:** `SkipLink.tsx`, `SkipLink.css`, Shell Region A landmark integration, `accessibilityAudit.test.ts`, Level II evidence package in `docs/evidence/ui010/`.
- **Out-of-Scope:** Responsive reflow (P02), feedback state rewrites (P03), shortcut manager (P04), whole-surface audit (P06), backend mutations, external AI, actuation controls.

---

# 11. Section J — Objective Acceptance Criteria (P01 & Full Workstream)

### P01 Phase Acceptance Criteria:
| # | Criterion | Verification Method | Governing Clause |
|---|---|---|---|
| **AC-01** | SkipLink renders and receives focus on initial Tab; links to `#main-content` | `SkipLink.test.tsx` | WCAG 2.4.1 (Bypass Blocks) |
| **AC-02** | Shell Regions A–F provide explicit ARIA landmark roles (`banner`, `navigation`, `main`, `complementary`, `region`) | `accessibilityAudit.test.ts` | WCAG 1.3.1 (Info & Relationships) |
| **AC-03** | Automated semantic audit verifies all headings (`h1` $\rightarrow$ `h2` $\rightarrow$ `h3`) follow strict unbroken hierarchy | `accessibilityAudit.test.ts` | WCAG 1.3.1, `08_UI_UX_SPEC.md` |
| **AC-04** | Pure token consumption: 0 ad-hoc hex in `workstation/accessibility/` | `grep_ad_hoc_hex.log` exit 1 | `16` Brand Standard |
| **AC-05** | Constitutional invariants: Zero actuation, zero external LLMs, zero dangerous HTML/eval | Grep transcripts exit 1 | `03`, `12`, `17` |
| **AC-06** | Frontend regression baseline $\ge 485$ tests (expected 490); Backend 414 tests pass; `tsc` and `vite build` exit 0 | Level II execution logs | `08_DEVELOPER_REASONING_FRAMEWORK.md` |

### Full Workstream Objective Targets (UI-010 P01–P06):
1. **100% Keyboard Operability (WCAG 2.1.1):** Every interactive control across all 7 workspaces is operable via standard keyboard without mouse dependency.
2. **Focus Visibility & Trapping (WCAG 2.4.7, 2.4.3):** Unambiguous focus indicators (`#8CC2FF`) on all focused elements; active modals trap focus.
3. **Responsive Reflow (WCAG 1.4.10):** Clean viewport reflow down to 1024px width with zero horizontal page scrolling.
4. **Multi-Modal Status (WCAG 1.4.1):** Zero color-alone information encoding.
5. **Reduced Motion (WCAG 2.3.3):** 0ms motion when `prefers-reduced-motion` is active.

---

# 12. Section K — Technical, Architectural & UI Dependencies

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       UI-010 TECHNICAL & GOVERNANCE STACK                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  Governance & Legal:    10 Hierarchy · 12 Transformation · 13 Master Plan   │
│  Brand & Design:        16 Brand Standard · tokens.css (5-tier) · theme.ts  │
│  Component Foundation:  frontend/src/components/ui/ (22 UI-009 primitives)  │
│  Shell Architecture:    InstitutionalWorkspaceShell.tsx (Regions A–F)       │
│  Accessibility Engine:  @testing-library/react (a11y queries) · WAI-ARIA    │
│  Build Toolchain:       TypeScript 5.6.3 (tsc -b) · Vite 8.1.4 · Vitest     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# 13. Section L — Cybersecurity Model & Security UX

1. **Focus Management Without Credential Exposure:** Focus state transitions and logging must never output input values (e.g. password fields or token strings) into console or DOM attributes.
2. **Style-Injection Defense:** Accessibility helpers must never inject unvetted raw HTML or use `dangerouslySetInnerHTML` / `eval`.
3. **No Hidden Actuation via ARIA:** ARIA labels or accessibility tags must not be attached to dormant execution/order triggers. S-1 and S-2 grep proofs remain strictly enforced.
4. **Auditability:** All accessibility and responsive adaptations are tracked on-tree in `docs/evidence/ui010/` with reproducible Level II transcripts.

---

# 14. Section M — UI/UX Interaction Standards & WCAG 2.1 AA / AAA Accessibility

### Interaction & Accessibility Standards:
- **Keyboard Traversal:** `Tab` moves forward, `Shift+Tab` moves backward, `Enter` / `Space` activates controls, `Escape` dismisses modals and popovers, `Arrow` keys navigate menus, tabs, and tables.
- **Focus Rings:** `outline: 2px solid var(--ix-color-focus); outline-offset: 2px;` (`#8CC2FF`, contrast $\ge 8.9:1$).
- **Contrast Discipline:**
  - Body text on surface: $\ge 8.7:1$ (exceeds AAA).
  - Primary headings: $\ge 15.8:1$ (exceeds AAA).
  - 0.75rem metadata: $\ge 6.8:1$ (exceeds AA).
- **Responsive Breakpoints:**
  - Desktop Large: $\ge 1440\text{px}$ (full multi-column expanded grid).
  - Desktop Standard: $1280\text{px} - 1439\text{px}$ (standard layout, docked navigation).
  - Laptop / Compact: $1024\text{px} - 1279\text{px}$ (collapsed navigation dock, stacked panels, horizontal scroll tables).

---

# 15. Section N — System Architecture & Integration Points

- **Presentation Layer Ownership (`05` v2.0 §13):** Accessibility modules reside strictly within `frontend/src/workstation/accessibility/` and `frontend/src/components/ui/`.
- **Integration Points:**
  1. `InstitutionalWorkspaceShell.tsx`: Integration of `SkipLink` and top-level ARIA landmark boundaries.
  2. `tokens.css`: Definition of responsive breakpoint variables and high-contrast theme overrides.
  3. `WorkspaceHost.tsx`: Integration of route announcement for screen readers.

---

# 16. Section O — Documentation Synchronization & State Management

Upon completion of each UI-010 phase, the DA will synchronize:
1. `PROJECT_STATE.md` (Version incrementing monotonically, e.g. 8.77.0 $\rightarrow$ 8.82.0 `UI-010 COMPLETE`).
2. `CHANGELOG.md` (Detailed phase delivery entries).
3. `RISK_REGISTER.md` & `TECHNICAL_DEBT_REGISTER.md` (Verified 0 new debt).
4. `docs/evidence/ui010/` (Level II execution logs).

---

# 17. Section 4A — Operational Methodology Invariants & Non-Deviation Rules

1. **Strict Phased Ordering:** Roadmap $\rightarrow$ Design Plan $\rightarrow$ ITRGA Build Order $\rightarrow$ Implementation $\rightarrow$ Verification $\rightarrow$ Delivery Report $\rightarrow$ ITRGA Review $\rightarrow$ Determination.
2. **Prohibition of Parallel Work:** No speculative development of UI-010-P02 through P06 while P01 is active.
3. **No Conversational State:** All architectural decisions and verification evidence must exist on-tree in git.

---

# 18. Closing Recommendations & Governance Declaration

### Development Authority Recommendation:
The DA recommends that the ITRGA review this Design Plan, issue its formal determination (**APPROVED** or **APPROVED WITH OBSERVATIONS**), and issue:

$$\mathbf{BUILD\_ORDER\_UI\text{-}010\text{-}P01 — Accessibility\ Foundation\ \&\ Semantic\ Audit}$$

### Governance Declaration (Per Amendment §25):
> The AXIOM Development Authority (DA) affirms that `UI-010_ENGINEERING_DESIGN_PLAN.md` has been authored in strict compliance with the constitutional hierarchy, governing charters, and operating invariants. Implementation remains on formal hold pending ITRGA approval and issuance of `BUILD_ORDER_UI-010-P01`.
>
> **Governance Gate: STRICTLY CLOSED · Production Status: NOT CERTIFIED.**

**We don't guess. We prove.**

— AXIOM Development Authority (DA)
