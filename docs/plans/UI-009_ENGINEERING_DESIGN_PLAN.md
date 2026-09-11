# UI-009 Engineering Design Plan — Institutional Design System Implementation
## Master Design Specification & Unification Architecture

| Field | Value |
|---|---|
| Document ID | `docs/plans/UI-009_ENGINEERING_DESIGN_PLAN.md` |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | **UI-009 — Institutional Design System Implementation** |
| Document Classification | Tier 8 — Execution Governance (Engineering Design Plan) |
| Author | AXIOM Development Authority (DA) |
| Governing Instrument | `ITRGA_REQUEST_UI-009_DESIGN_PLAN.md` |
| Review Authority | Independent Technical Review & Governance Authority (ITRGA) |
| Preceding Milestone | 🏛️ **UI-008 — Institutional AI Experience COMPLETE** (Determination D-53) |
| Baseline of Record | **Frontend: 83 test suites / 376 tests passed · Backend: 414 tests passed · Build: clean (exit 0)** |
| Governance Gate | **CLOSED** (Strictly Enforced; No Live Execution Affordances) |
| Production Status | **NOT CERTIFIED** (Doc 11 Production Readiness Certification Held Out-of-Band) |
| DA Operational State | **Design Plan Submitted for Independent ITRGA Review; Implementation on Formal Hold** |

---

# Table of Contents

1. [Executive Summary & Charter](#1-executive-summary--charter)
2. [Section A — UI-009 Objective & Scope](#2-section-a--ui-009-objective--scope)
3. [Section B — Governing Requirements & Traceability Matrix](#3-section-b--governing-requirements--traceability-matrix)
4. [Section C — Roadmap Position & Workstream Dependencies](#4-section-c--roadmap-position--workstream-dependencies)
5. [Section D — Complete 6-Phase Delivery Lifecycle (P01 through P06)](#5-section-d--complete-6-phase-delivery-lifecycle-p01-through-p06)
6. [Section E — Existing UI State Audit (UI-001 through UI-008 Surfaces)](#6-section-e--existing-ui-state-audit-ui-001-through-ui-008-surfaces)
7. [Section F — Existing Test Inventory & Verification Baseline](#7-section-f--existing-test-inventory--verification-baseline)
8. [Section G — Existing Documentation & Governance Reference Catalog](#8-section-g--existing-documentation--governance-reference-catalog)
9. [Section H — Retain / Extend / Supersede / Defer Component Matrix](#9-section-h--retain--extend--supersede--defer-component-matrix)
10. [Section I — Proposed P01 (Design System Foundation & Token Architecture)](#10-section-i--proposed-p01-design-system-foundation--token-architecture)
11. [Section J — Objective Acceptance Criteria (P01 & Full Workstream)](#11-section-j--objective-acceptance-criteria-p01--full-workstream)
12. [Section K — Technical, Architectural & UI Dependencies](#12-section-k--technical-architectural--ui-dependencies)
13. [Section L — Cybersecurity Model & Style-Injection Defense](#13-section-l--cybersecurity-model--style-injection-defense)
14. [Section M — UI/UX Interaction Standards & WCAG 2.1 AA Accessibility](#14-section-m--uiux-interaction-standards--wcag-21-aa-accessibility)
15. [Section N — Design System Architecture & Token Hierarchy](#15-section-n--design-system-architecture--token-hierarchy)
16. [Section O — Documentation Synchronization & State Management](#16-section-o--documentation-synchronization--state-management)
17. [Section 4A — Operational Methodology Invariants & Non-Deviation Rules](#17-section-4a--operational-methodology-invariants--non-deviation-rules)
18. [Closing Recommendations & Governance Declaration](#18-closing-recommendations--governance-declaration)

---

# 1. Executive Summary & Charter

Following the formal completion and approval of workstreams **UI-001 through UI-008** (Milestone D-53 at baseline **83 suites / 376 tests**), the AXIOM platform has constructed all analytical, market, investigation, governance, and assistant presentation surfaces.

Workstream **UI-009 (Institutional Design System Implementation)** constitutes the **Foundational Harmonization Engine (Level A & Level D Dependency)** of the platform. In accordance with `12_INSTITUTIONAL_UI_TRANSFORMATION_PLAN.md` Part VII §11 and `13_UI_TRANSFORMATION_MASTER_PLAN.md` Parts IV/V, UI-009 does **not** introduce new backend endpoints, trading capabilities, or business logic. Instead, it unifies the disparate presentation components into a single, cohesive, tokenized institutional design language.

### Core Mandate:
```text
The purpose of UI-009 is to establish the permanent visual language, atomic component library,
typography hierarchy, semantic color system, and panel consistency standards across all
AXIOM workspaces (UI-001 through UI-008), delivering an institutional trading workstation
experience that satisfies WCAG 2.1 AA accessibility and Brand Governance Standard (Doc 16).
```

---

# 2. Section A — UI-009 Objective & Scope

### 2.1 Context & Traceability
* **`12_INSTITUTIONAL_UI_TRANSFORMATION_PLAN.md` Part VII §11**:
  > *"Apply the approved Design System across the entire platform — component library, typography, color system, tables, forms, cards, dialogs, alerts, tooltips, icons, panel consistency — workstation presents one cohesive institutional identity."*
* **`13_UI_TRANSFORMATION_MASTER_PLAN.md` Part V §1–14**:
  > Establishes the 3-stage rollout philosophy: **Foundation Tokens $\rightarrow$ Component Library $\rightarrow$ Workspace Harmonization**.

### 2.2 Why UI-009 is Foundational and Sequenced After UI-008
* **Level A (Foundational) & Level D (Refinement)**: Design tokens must govern every visual boundary. Deferring full harmonization until after UI-008 ensured that all functional research workspaces (`/charts`, `/signals`, `/analytics`, `/intelligence`, `/investigate`, `/governance`, `/research-management`) were fully implemented and stable before standardizing their shared components.

---

# 3. Section B — Governing Requirements & Traceability Matrix

UI-009 derives its binding requirements from across the constitutional corpus (`10_CONSTITUTIONAL_HIERARCHY.md`):

| Hierarchy Tier | Controlling Document | Binding Directives for UI-009 |
|---|---|---|
| **Tier 1 (Constitution)** | `00_VISION_AND_PRINCIPLES.md` | Principle 2 (Transparency), Principle 3 (Professional Engineering), Principle 4 (Professional Trading Standards). |
| **Tier 1 (Philosophy)** | `02_DESIGN_PHILOSOPHY.md` | Institutional workstation appearance; information density without clutter; dark-first theme; operator efficiency. |
| **Tier 1 (Certification)** | `11_PRODUCTION_READINESS_CERTIFICATION.md` | §7 User Experience & Accessibility Certification; WCAG 2.1 AA compliance (Firewalled out-of-band). |
| **Tier 2 (Specification)** | `03_AXIOM_SPEC.md` | Institutional visual identity; high information density; Definition of Done enforcement. |
| **Tier 3 (Roadmap)** | `04_PROJECT_ROADMAP.md` | Post Wave 0–7 UI Transformation sequencing; Gate CLOSED invariant. |
| **Tier 4 (Architecture)** | `05_SYSTEM_ARCHITECTURE.md` v2.0 | Part I §8 / Part II §13 (Single ownership of Presentation Layer); §64 Canonical Deployment. |
| **Tier 5 (Domain Spec)** | `08_UI_UX_SPEC.md` | Modular workstation layout; `<100ms` UI latency; color contrast >4.5:1; no color-alone encoding. |
| **Tier 6 (Reasoning)** | `08_DEVELOPER_REASONING_FRAMEWORK.md` | Systems thinking; reason before code; architectural integrity over shortcuts. |
| **Tier 7 (UI Charter)** | `12_INSTITUTIONAL_UI_TRANSFORMATION_PLAN.md` | Part V (Institutional Design System) & Part VII §11 (UI-009 Charter). |
| **Tier 7 (UI Master Plan)** | `13_UI_TRANSFORMATION_MASTER_PLAN.md` | Part IV (Component Rollout) & Part V (Design System Rollout). |
| **Tier 7 (Branding)** | `16_BRAND_GOVERNANCE_STANDARD.md` | Official AX monogram; Midnight Black (`#0B0E14`), Graphite (`#1A1F2C`), Electric Blue (`#2563EB`); `/branding` assets. |
| **Tier 7 (Security)** | `17_INSTITUTIONAL_SECURITY_STANDARD.md` | Part X (Secure Coding — Style Injection Prevention); Part XII (AppSec). |
| **Tier 8 (Process)** | `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` | 27 rules of execution, test accounting, and evidence integrity. |

---

# 4. Section C — Roadmap Position & Workstream Dependencies

UI-009 bridges foundational workspace construction with global refinement:

```
  ┌────────────────────────────────────────────────────────────────────────┐
  │                 PREDECESSORS (COMPLETED & VERIFIED)                    │
  ├──────────────────┬──────────────────┬──────────────────┬───────────────┤
  │ UI-001 (Shell)   │ UI-002 (Nav)     │ UI-003 (Market)  │ UI-004 (Intel)│
  │ UI-005 (Invest.) │ UI-006 (Explorer)│ UI-007 (Govern.) │ UI-008 (AI)   │
  └──────────────────┴──────────────────┴──────────────────┴───────────────┘
                                     │
                                     ▼
  ┌────────────────────────────────────────────────────────────────────────┐
  │         ACTIVE DESIGN WORKSTREAM: UI-009 (DESIGN SYSTEM)               │
  │    P01 (Tokens) ──► P02 (Components) ──► P03–P05 ──► P06 (Harmonize)   │
  └────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
  ┌────────────────────────────────────────────────────────────────────────┐
  │                   SUCCESSORS (FINAL TRANSFORMATION)                    │
  ├─────────────────────────────────────┬──────────────────────────────────┤
  │ UI-010 (Accessibility & UX Polish)  │ UI-011 (v1.0 Presentation)       │
  │ Handover to Doc 11 Production Readiness Certification (Firewalled)     │
  └─────────────────────────────────────┴──────────────────────────────────┘
```

---

# 5. Section D — Complete 6-Phase Delivery Lifecycle (P01 through P06)

The DA proposes a bounded, sequential 6-phase engineering lifecycle for UI-009:

```
  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
  │  UI-009-P01  │ ──► │  UI-009-P02  │ ──► │  UI-009-P03  │
  │ Design Tokens│     │Atomic Library│     │Panel Frames  │
  └──────────────┘     └──────────────┘     └──────────────┘
                                                   │
  ┌──────────────┐     ┌──────────────┐            │
  │  UI-009-P06  │ ◄── │  UI-009-P05  │ ◄──────────┘
  │ Full Audit/CK│     │Modals/Dialogs│
  └──────────────┘     └──────────────┘
```

### Phase Breakdown:

| Phase ID | Phase Title | Status | Scope & Boundary Definition |
|---|---|---|---|
| **`UI-009-P01`** | **Design System Foundation & Token Architecture** | **PROPOSED (FIRST)** | Codify the comprehensive 5-tier token hierarchy (Colors, Typography, Spacing, Elevation, Motion) in `tokens.css` and `theme.ts`. Align exact palette tokens with `16_BRAND_GOVERNANCE_STANDARD.md` and `08_UI_UX_SPEC.md`. |
| **`UI-009-P02`** | **Atomic Component Library** | **PROPOSED** | Construct standardized, reusable presentation primitives: `Button`, `Input`, `Select`, `Badge`, `Card`, `StatusChip`, `Tooltip`, and `Accordion` with comprehensive state tests. |
| **`UI-009-P03`** | **Workspace Panels & Frame Harmonization** | **PROPOSED** | Standardize panel wrappers, headers, action bars, and collapsible containers across `/charts`, `/intelligence`, `/investigate`, `/governance`, and `/research-management`. |
| **`UI-009-P04`** | **Data Tables & Visualization Grids** | **PROPOSED** | Standardize institutional data tables, monospace numerical alignments, uncertainty interval formatters, sortable column headers, and pagination controls. |
| **`UI-009-P05`** | **Modals, Overlays & Feedback Systems** | **PROPOSED** | Standardize Dialog overlays, Command Palette styling, skeleton loading primitives, toast notifications, and error recovery banners. |
| **`UI-009-P06`** | **Whole-Surface Harmonization & Completion Checkpoint** | **PROPOSED** | Full regression verification across all 83+ frontend test suites, whole-surface WCAG 2.1 AA audit, zero-actuation grep proofs, and handover for `UI-009 COMPLETE` declaration. |

---

# 6. Section E — Existing UI State Audit (UI-001 through UI-008 Surfaces)

The DA conducted an audit of all existing presentation assets across the repository:

### 1. Existing Shell & Layout Infrastructure (`UI-001` / `UI-002`)
* **6 Workstation Regions**: Region A (Global Command Bar), Region B (Navigation Dock), Region C (Primary Workspace), Region D (Context Panel), Region E (Activity Dock), Region F (Overlay Layer).
* **Command Palette**: `Ctrl+K` overlay containing 33 registered Quick Action items.
* **Tokens File**: `frontend/src/workstation/design/tokens.css` (Contains baseline CSS custom properties).

### 2. Existing Workspace Surfaces (`UI-003` through `UI-008`)
* **Market Workspace (`UI-003`)**: TradingView Lightweight Charts, watchlists, timeframe controls, drawing tool markups.
* **Research & Intelligence (`UI-004`)**: Advisory signals list, regime reports, correlation matrices, scenario drilldowns.
* **Investigation & Planning (`UI-005`)**: Signal investigation cards, trade planning notes, simulated execution research ledger.
* **Artifact Explorer (`UI-006`)**: Unified artifact catalog, collection/tag manager, relational lineage graph.
* **Governance Workspace (`UI-007`)**: Audit log explorer, platform health cards, Gate CLOSED indicators.
* **Institutional AI (`UI-008`)**: `AssistantCommandSurface`, `ContextualAssistantPanel`, `ResearchReportSummarizer`, `ArtifactLineageTree`, `UncertaintyBadge`, `DocumentationLookupSurface`.

### 3. Existing Brand Assets (`/branding/`)
* Master brand asset: `branding/brand-governance-embedded-logo.png` (Conforming to Doc 16 Part XI).

---

# 7. Section F — Existing Test Inventory & Verification Baseline

As certified in Determination **D-53 (UI-008 COMPLETE)**, the starting baseline for UI-009 is:

* **Frontend Test Baseline**: **83 passed test suites / 376 passed tests** (Vitest / JSDOM in 81.56s).
* **Backend Test Baseline**: **414 passed tests** (Pytest / AsyncIO in 114.98s).
* **Static Compiler Baseline**: `tsc -b && vite build` exits clean with code **0**.
* **Zero Actuation & Zero External LLMs**: Verified clean via whole-repository grep proofs.

---

# 8. Section G — Existing Documentation & Governance Reference Catalog

| Reference Identifier | File Path | Scope in UI-009 |
|---|---|---|
| `Doc 12` | `docs/governance/12_INSTITUTIONAL_UI_TRANSFORMATION_PLAN.md` | Part V & Part VII §11 (UI-009 Mandate). |
| `Doc 13` | `docs/governance/13_UI_TRANSFORMATION_MASTER_PLAN.md` | Parts IV & V (Component & Design System Rollouts). |
| `Doc 16` | `docs/governance/16_BRAND_GOVERNANCE_STANDARD.md` | Official color palette, AX monogram, typography standards. |
| `Doc 08` | `docs/governance/08_UI_UX_SPEC.md` | Dark-first workstation, density, accessibility. |
| `Doc 05` | `docs/governance/05_SYSTEM_ARCHITECTURE.md` | Canonical Presentation Layer architecture (§8/§13). |
| `Doc 17` | `docs/governance/17_INSTITUTIONAL_SECURITY_STANDARD.md` | Style-injection defense and SAL classification. |
| `Amendment` | `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` | 27 rules of execution and test accounting. |
| `Project State` | `PROJECT_STATE.md` | Version 8.70.0 (UI-008 COMPLETE recorded). |

---

# 9. Section H — Retain / Extend / Supersede / Defer Component Matrix

In accordance with Section 2.H of the Request, all existing presentation elements are classified:

| Presentation Component / Token | Classification | Technical & Governance Rationale | Implementation Impact |
|---|---|---|---|
| **Design Tokens CSS (`tokens.css`)** | **EXTEND** | Retain root CSS variables; extend in P01 with complete semantic & component token tiers. | Low risk / High reuse |
| **Theme Definition (`theme.ts`)** | **EXTEND** | Retain category definitions; extend with TypeScript token contracts. | Low risk |
| **Shell Layout (`InstitutionalWorkspaceShell.tsx`)** | **RETAIN** | 6-region shell architecture is verified, stable, and conforms to Doc 14. | Zero churn |
| **Navigation Dock (`NavigationDock.tsx`)** | **EXTEND** | Retain structure; align spacing and hover tokens in P03. | Low risk |
| **Command Palette (`OverlayLayer.tsx`)** | **EXTEND** | Retain 33-command routing; harmonize modal tokens in P05. | Low risk |
| **UncertaintyBadge (`UncertaintyBadge.tsx`)** | **RETAIN** | Discrete confidence levels (text + `◆◆◆` + `%`) already conform to 08/16. | Zero churn |
| **Lineage Tree (`ArtifactLineageTree.tsx`)** | **RETAIN** | Provenance node layout is stable and verified. | Zero churn |
| **Direct Inline Style Hex Overrides** | **SUPERSEDE** | Ad-hoc inline hex colors across legacy pages will be replaced by CSS custom properties. | Medium / Planned in P03 |
| **Future Multi-Monitor Layout Splitter** | **DEFER** | Advanced multi-window detachment deferred to post-v1.0 per Doc 12 §5. | Out of scope |

*Classification Summary*: **3 RETAIN**, **5 EXTEND**, **1 SUPERSEDE**, **1 DEFER**, **0 REMOVE**.

---

# 10. Section I — Proposed P01 (Design System Foundation & Token Architecture)

### 1. Retained Implementation
* Retain the existing `:root` variable structure in `tokens.css` and dark-first palette foundations (`#070A0F` root background, `#111822` surface).
* Retain `theme.ts` role mappings.

### 2. Extended Implementation (P01 Scope)
* **5-Tier Token Hierarchy**: Formally codify Foundation Tokens, Semantic Tokens, Component Tokens, Workspace Tokens, and Theme Override Tokens.
* **Brand Governance Palette**: Harmonize Midnight Black (`#0B0E14`), Graphite Gray (`#1A1F2C`), Electric Blue (`#2563EB`), Success Green (`#10B981`), Warning Amber (`#F59E0B`), and Critical Red (`#EF4444`).
* **Typography Scale**: Define strict CSS tokens for Display Titles (`1.5rem`), Workspace Titles (`1.2rem`), Section Headings (`1.0rem`), Panel Headings (`0.85rem`), Body Content (`0.9rem`), and Metadata/Monospace (`0.75rem`).
* **Spacing & Elevation Scales**: 4px base grid (`--ix-space-1` = 4px through `--ix-space-8` = 32px) and elevation drop shadows.

### 3. Superseded Implementation
* Disorganized CSS property names or conflicting token definitions will be superseded by the standardized `--ix-*` token prefix.

### 4. Deferred Implementation
* Dynamic theme customizer tools and user-editable color pickers remain deferred.

### 5. Collective Satisfaction Assessment
The DA determines that existing baseline tokens provide the core foundation, but formalizing the complete 5-tier token hierarchy in P01 is required to enable clean component construction in P02–P05 without regression.

### 6. Re-baseline Determination
**Clean continuation from the D-53 baseline (83 suites / 376 tests) is recommended.** No code rewrites are required; P01 is purely additive token architecture.

### 7. Next P01 Build Order Boundary (`BUILD_ORDER_UI-009-P01`)
* **In-Scope for P01**:
  - Full codification of `tokens.css` (5-tier token hierarchy).
  - TypeScript token contracts and validation helpers in `theme.ts`.
  - Comprehensive token audit test suite (`tokens.test.ts`) validating contrast ratios and token completeness.
  - Verification that all 376 frontend tests pass invariantly.
* **Out-of-Scope for P01**:
  - No workspace component rewrites.
  - No new backend endpoints or database changes.

---

# 11. Section J — Objective Acceptance Criteria (P01 & Full Workstream)

| # | Criterion | Verification Method | Governing Clause |
|---|---|---|---|
| **AC-01** | **5-Tier Token Architecture** | Full token set codified in `tokens.css` with `--ix-*` prefixes | Doc 12 Part V §1 |
| **AC-02** | **Brand Palette Fidelity** | Midnight Black, Graphite, Electric Blue, Semantic Green/Amber/Red present | Doc 16 Part VI |
| **AC-03** | **Contrast Compliance** | All text-to-background combinations achieve contrast ratio `>4.5:1` | Doc 08 §Accessibility |
| **AC-04** | **No Color-Alone Encoding** | Statuses and confidence levels include text labels and symbols | Doc 02 §Design |
| **AC-05** | **Zero Actuation Invariant** | Grep proof: 0 functional matches for order/buy/sell/trade | Doc 03 / Doc 05 |
| **AC-06** | **Zero External LLMs** | Grep proof: 0 imports for openai/anthropic/langchain | Doc 12 §5 / Doc 17 |
| **AC-07** | **Style-Injection Safety** | 0 `dangerouslySetInnerHTML`, 0 `eval()`, 0 raw `<script>` | Doc 17 Part X |
| **AC-08** | **Regression Invariance** | 100% of existing 376 frontend tests and 414 backend tests pass | Amendment §10 |

---

# 12. Section K — Technical, Architectural & UI Dependencies

```
┌────────────────────────────────────────────────────────────────────────┐
│                        DEPENDENCY MAPPING                              │
├─────────────────┬──────────────────────────────────────────────────────┤
│ Technical       │ React 18, TypeScript 5, Vite, Vitest, CSS3 Variables │
│ Architectural   │ Bounded context: `frontend/src/workstation/design/`  │
│ Predecessors    │ UI-001 through UI-008 COMPLETE (D-53 Baseline)       │
│ Brand Standard  │ `16_BRAND_GOVERNANCE_STANDARD.md` Master Palette     │
│ Security        │ `17_INSTITUTIONAL_SECURITY_STANDARD.md` CSS Sandbox  │
│ Governance      │ ITRGA Review & Build Order Authorization             │
└─────────────────┴──────────────────────────────────────────────────────┘
```

---

# 13. Section L — Cybersecurity Model & Style-Injection Defense

In accordance with `17_INSTITUTIONAL_SECURITY_STANDARD.md` Part X:
* **Style-Injection Prevention**: All design tokens are compiled as static CSS custom properties. No runtime string interpolation or `dangerouslySetInnerHTML` is permitted for theme injection.
* **CSS Isolation**: All workstation styles are scoped using the `.ix-*` namespace to prevent global CSS pollution.
* **Credential Isolation**: Design tokens strictly represent visual properties (color, spacing, font); zero system credentials, JWT secrets, or API keys may exist in design files.
* **Immutable Invariants**: Grep scans for actuation terms and external LLMs are enforced in every phase.

---

# 14. Section M — UI/UX Interaction Standards & WCAG 2.1 AA Accessibility

In accordance with `08_UI_UX_SPEC.md` and `16_BRAND_GOVERNANCE_STANDARD.md`:
* **Visual Identity**: Dark-first institutional aesthetic (`#0B0E14` base, `#1A1F2C` panels, `#2563EB` accent).
* **Information Density**: Clean data tables, tight padding, and monospace alignments enabling multi-dataset inspection.
* **Interaction Restraint**: Subtle, deterministic motion transitions (`--ix-motion-fast: 120ms`); respects `@media (prefers-reduced-motion: reduce)`.
* **Accessibility (WCAG 2.1 AA)**:
  * Contrast ratio `>4.5:1` on body text, `>3:1` on large headings.
  * Explicit focus rings (`--ix-color-focus: #8CC2FF`) on interactive controls.
  * Full keyboard accessibility (`Tab`, `Enter`, `Space`, `Escape`).

---

# 15. Section N — Design System Architecture & Token Hierarchy

UI-009 organizes design variables into a formal 5-tier hierarchy:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     5-TIER DESIGN TOKEN HIERARCHY                       │
├─────────────────────────────────────────────────────────────────────────┤
│ Tier 1: Foundation Tokens (Primitive Hex Colors, Base Grid, Fonts)     │
│         --ix-color-blue-600: #2563EB; --ix-space-base: 4px;             │
├─────────────────────────────────────────────────────────────────────────┤
│ Tier 2: Semantic Tokens (Role-Based Tokens)                             │
│         --ix-color-accent: var(--ix-color-blue-600);                    │
│         --ix-color-surface: #111822; --ix-color-surface-raised: #1A1F2C;│
├─────────────────────────────────────────────────────────────────────────┤
│ Tier 3: Component Tokens (Scoped Primitives)                            │
│         --ix-button-primary-bg: var(--ix-color-accent);                 │
│         --ix-card-border: var(--ix-border-subtle);                      │
├─────────────────────────────────────────────────────────────────────────┤
│ Tier 4: Workspace Tokens (Domain-Specific Contexts)                     │
│         --ix-color-charts: #4CC9F0; --ix-color-governance: #10B981;     │
├─────────────────────────────────────────────────────────────────────────┤
│ Tier 5: Runtime Theme Overrides (Dark / Light Theme Adaptations)        │
│         .theme-light { --ix-bg-root: #F8FAFC; --ix-text-primary: ... }  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

# 16. Section O — Documentation Synchronization & State Management

Upon completion of each UI-009 phase, the DA will synchronize:
1. `PROJECT_STATE.md`: Update UI-009 workstream status and test counts.
2. `CHANGELOG.md`: Record phase completions and token additions.
3. `RISK_REGISTER.md` & `TECHNICAL_DEBT_REGISTER.md`: Track residual observations.
4. `docs/plans/UI-009_ENGINEERING_DESIGN_PLAN.md`: Keep this plan updated as the single migratable truth.

---

# 17. Section 4A — Operational Methodology Invariants & Non-Deviation Rules

In accordance with Section 4A of the ITRGA Request:
* **No Silent Methodology Change**: The established sequence (`Roadmap -> Design Plan -> Build Order -> Implementation -> Testing -> Delivery Report -> ITRGA Review -> Determination`) is strictly preserved.
* **Prohibited Parallel Processes**: No ad-hoc branches, undocumented conversational states, or unreviewed component rewrites.
* **Traceable Continuity**: All evidence logs will be captured and committed to `docs/evidence/ui009/`.

---

# 18. Closing Recommendations & Governance Declaration

### Development Authority Recommendation:
1. **Design Plan Approval**: That the ITRGA review and approve this **`UI-009 Engineering Design Plan`**.
2. **Build Order Authorization**: That the ITRGA issue **`BUILD_ORDER_UI-009-P01` (Design System Foundation & Token Architecture)** to initiate Phase P01 implementation.

### Implementation Hold Affirmation:
The DA affirms that **implementation remains on formal hold** until the ITRGA completes its review and formally issues `BUILD_ORDER_UI-009-P01`.

---

**We don't guess. We prove.**

*— AXIOM Development Authority (DA)*
