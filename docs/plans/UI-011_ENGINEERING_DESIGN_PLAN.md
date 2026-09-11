# UI-011 Engineering Design Plan — Institutional Refinement & Version 1.0 Presentation
## Master Specification for Institutional Polish, Information Hierarchy, and Version 1.0 Workstation Presentation

| Field | Value |
|---|---|
| Document ID | `docs/plans/UI-011_ENGINEERING_DESIGN_PLAN.md` |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | **UI-011 — Institutional Refinement & Version 1.0 Presentation** |
| Document Classification | Tier 8 — Execution Governance (Engineering Design Plan) |
| Author | AXIOM Development Authority (DA) |
| Governing Instrument | `ITRGA_REQUEST_UI-011_DESIGN_PLAN.md` (Issued 2026-08-11) |
| Review Authority | Independent Technical Review & Governance Authority (ITRGA) |
| Preceding Milestone | 🏛️ **UI-010 — Accessibility & Operator Experience COMPLETE** (D-67 / `ITRGA-DECLARATION-UI010-COMPLETE-D67`) |
| Baseline of Record | **Frontend: 136 test suites / 556 tests passing · Backend: 414 tests passing · Build: clean (exit 0) · Total: 970 tests passing** |
| Governance Gate | **STRICTLY CLOSED** (Enforced: Zero Live Broker Execution, Order Routing, or Real Capital Actuation) |
| Production Status | **NOT CERTIFIED** (Doc 11 Production Readiness Certification Firewalled Out-of-Band) |
| DA Operational State | **Design Plan Submitted for Independent ITRGA Review; Implementation on Formal Hold** |

---

# Table of Contents

1. [Executive Summary & Charter](#1-executive-summary--charter)
2. [Section A — UI-011 Objective & Scope](#2-section-a--ui-011-objective--scope)
3. [Section B — Governing Requirements & Traceability Matrix](#3-section-b--governing-requirements--traceability-matrix)
4. [Section C — Roadmap Position & Workstream Dependencies](#4-section-c--roadmap-position--workstream-dependencies)
5. [Section D — Complete 6-Phase Delivery Lifecycle (P01 through P06)](#5-section-d--complete-6-phase-delivery-lifecycle-p01-through-p06)
6. [Section E — Existing UI State Audit (UI-001 through UI-010 Surfaces)](#6-section-e--existing-ui-state-audit-ui-001-through-ui-010-surfaces)
7. [Section F — Existing Test Inventory & Verification Baseline](#7-section-f--existing-test-inventory--verification-baseline)
8. [Section G — Existing Documentation & Governance Reference Catalog](#8-section-g--existing-documentation--governance-reference-catalog)
9. [Section H — Retain / Extend / Supersede / Defer Component Matrix](#9-section-h--retain--extend--supersede--defer-component-matrix)
10. [Section I — Proposed P01 (Information Hierarchy & Spacing Refinement)](#10-section-i--proposed-p01-information-hierarchy--spacing-refinement)
11. [Section J — Objective Acceptance Criteria (P01 & Full Workstream)](#11-section-j--objective-acceptance-criteria-p01--full-workstream)
12. [Section K — Technical, Architectural & UI Dependencies](#12-section-k--technical-architectural--ui-dependencies)
13. [Section L — Cybersecurity Model & Security UX](#13-section-l--cybersecurity-model--security-ux)
14. [Section M — UI/UX Interaction Standards & Institutional Polish](#14-section-m--uiux-interaction-standards--institutional-polish)
15. [Section N — System Architecture & Integration Points](#15-section-n--system-architecture--integration-points)
16. [Section O — Documentation Synchronization & State Management](#16-section-o--documentation-synchronization--state-management)
17. [Section 4A — Operational Methodology Invariants & Non-Deviation Rules](#17-section-4a--operational-methodology-invariants--non-deviation-rules)
18. [Closing Recommendations & Governance Declaration](#18-closing-recommendations--governance-declaration)

---

# 1. Executive Summary & Charter

### Core Mandate (Verbatim per `12_INSTITUTIONAL_UI_TRANSFORMATION_PLAN.md` Part VII §13):
> *"Complete the transformation into a production-grade institutional workstation — Visual refinement, Workflow optimization, Workspace polish, Information hierarchy, Panel balance, Interaction consistency, Animation refinement, Final UX review — AXIOM presents itself as a mature institutional trading and research workstation suitable for Production Readiness Certification."*

### Purpose & Architectural Intent:
The `UI-011` workstream establishes the **final, high-grade institutional polish and presentation layer** across the entire AXIOM Trading Platform. Building directly upon the foundation of completed workstreams `UI-001` through `UI-010` (970 total automated platform tests passing, 5-tier design tokens, atomic and panel primitives, data tables, modals, overlays, responsive reflow, standardized feedback states, keyboard shortcuts, and screen-reader compliance), `UI-011` brings the entire visual presentation to institutional-grade maturity.

`UI-011` operates strictly as a **Level D (Refinement)** workstream. It does not reinvent architectural layers or introduce speculative features; rather, it harmonizes visual hierarchy, spacing proportions, micro-interaction states, typography weighting, and panel balance so that AXIOM presents itself as an uncompromised institutional workstation ready for **`11_PRODUCTION_READINESS_CERTIFICATION.md`**.

### Non-Negotiable Governance Invariants:
1. **Governance Gate STRICTLY CLOSED:** Zero live broker execution, order routing, or real capital actuation.
2. **Production Status: NOT CERTIFIED:** Production certification is governed exclusively out-of-band under Doc 11.
3. **Zero External AI / LLMs:** Zero third-party AI APIs (OpenAI, Anthropic, LangChain, etc.) without explicit constitutional amendment.
4. **Single Active Phase:** Only the currently authorized Build Order phase shall be implemented.
5. **Pure Token Consumption:** All visual styling must reference `var(--ix-*)` design tokens exclusively; zero ad-hoc hex literals outside `tokens.css`.

---

# 2. Section A — UI-011 Objective & Scope

### 2.1 Primary Objectives
1. **Information Hierarchy & Spacing Refinement**: Enforce strict 4-level information hierarchy (`Level 1: Mission-Critical Telemetry` $\rightarrow$ `Level 2: Active Context & Signals` $\rightarrow$ `Level 3: Supporting Analytics` $\rightarrow$ `Level 4: Administrative & Meta`) with mathematical 4px/8px/12px/16px/24px spacing rhythm.
2. **Panel Balance & Workspace Polish**: Harmonize header, body, action bar, and footer padding across all 7 primary workspace surfaces (`/charts`, `/intelligence`, `/investigate`, `/governance`, `/trade-plans`, `/journal`, `/compare-scenarios`) to eliminate visual density imbalances.
3. **Interaction Consistency**: Standardize hover, focus-visible, active, and disabled micro-interactions across atomic and composite controls with uniform tokenized transition curves (`var(--ix-motion-fast)` 120ms).
4. **Animation & Motion Restraint**: Ensure all animations (skeleton shimmers, dialog fades, toast slide-ins) are subtle, institutional, and strictly zero out under `@media (prefers-reduced-motion: reduce)`.
5. **Version 1.0 Presentation Readiness**: Assemble the final visual and architectural evidence demonstrating that AXIOM fulfills all institutional usability, visual dignity, and security requirements prior to formal Production Readiness Certification.

### 2.2 In-Scope vs. Out-of-Scope Boundaries

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                   IN-SCOPE (UI-011)                                     │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ • Information hierarchy & visual weight calibration across all 7 workspace surfaces    │
│ • Panel padding & card container balance harmonization (tokens.css + Panel.css)         │
│ • Micro-interaction transition timing curves (Button, Input, Select, Collapsible)       │
│ • Skeleton shimmer and feedback animation polish (subtle, non-distracting)              │
│ • Typography optical hierarchy (display, workspace title, panel title, body, metadata)  │
│ • Cross-workspace visual consistency verification harness                               │
│ • Final whole-surface Level II evidence package in docs/evidence/ui011/                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                               OUT-OF-SCOPE (STRICTLY FORBIDDEN)                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ 🚫 Redefinition of 5-tier design tokens or breaking CSS variable contracts              │
│ 🚫 Rewriting existing functional components from UI-001 through UI-010                  │
│ 🚫 Backend schema migrations, endpoint alterations, or database mutations               │
│ 🚫 WebSocket protocol modifications or real broker connections                           │
│ 🚫 Order routing, live trading, or order ticket actuation affordances                   │
│ 🚫 External LLM SDK integrations or generative UI agents                                │
│ 🚫 Doc 11 Production Readiness Certification self-approval (ITRGA out-of-band)          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

# 3. Section B — Governing Requirements & Traceability Matrix

| Requirement Tier | Governing Document | Mandatory Invariant / Standard | UI-011 Traceability |
|---|---|---|---|
| **Tier 1** | `00_VISION_AND_PRINCIPLES.md` | Principle 3 (Professional Engineering), Principle 4 (Professional Trading Standards), *Quality over speed* | Refinement elevates UI to institutional trading grade (Bloomberg/FactSet dignity). |
| **Tier 1** | `01_PRODUCT_MISSION.md` | Multi-market institutional research & AI trading intelligence platform | Clean separation of research observation from execution actuation. |
| **Tier 1** | `02_DESIGN_PHILOSOPHY.md` | Professional Quality Checklist: Correct, Tested, Documented, Maintainable, Reviewed, Secure | 10-point checklist enforced across all visual refinement deliverables. |
| **Tier 1** | `11_PRODUCTION_READINESS_CERTIFICATION.md` | Firewalled Production Certification Criteria | UI-011 prepares the UI surface to pass Doc 11 §7 UX & Accessibility audit. |
| **Tier 2** | `03_AXIOM_SPEC.md` | UI Standards, Quality Standards, Definition of Done | Monospace tabular numbers, 60 FPS charts, sub-100ms UI interaction responsiveness. |
| **Tier 3** | `04_PROJECT_ROADMAP.md` | Transformation sequence & Governance Gate invariant | Gate strictly CLOSED across all polish phases. |
| **Tier 4** | `05_SYSTEM_ARCHITECTURE.md` v2.0 | Presentation Layer §13 & Workspace Shell Regions A–F | UI-011 strictly confined to Presentation Layer; zero backend coupling. |
| **Tier 5** | `08_UI_UX_SPEC.md` | High-density terminal aesthetics, monospace numerical alignment, dark theme | Optical density balancing and typography hierarchy standards. |
| **Tier 6** | `08_DEVELOPER_REASONING_FRAMEWORK.md` | Systems thinking, reason before code, Level II evidence | Level II automated verification logs required for all determinations. |
| **Tier 6** | `09_ITRGA_REASONING_FRAMEWORK.md` | 7-stage review lifecycle, 12 disciplines, EVF-1..EVF-4 evidence | Formal independent ITRGA review of all delivery packages. |
| **Tier 7** | `12_INSTITUTIONAL_UI_TRANSFORMATION_PLAN.md` | Part VI §17 (Institutional Polish), Part VII §13 (UI-011 Charter) | Master charter and completion criteria for Version 1.0 presentation. |
| **Tier 7** | `13_UI_TRANSFORMATION_MASTER_PLAN.md` | Part II §3 (Level D Refinement), Part V (Design System Rollout) | Sequential dependency enforcement (depends on UI-010 COMPLETE). |
| **Tier 7** | `16_BRAND_GOVERNANCE_STANDARD.md` | Midnight Black (`#0B0E14`), Graphite (`#1A1F2C`), Electric Blue (`#2563EB`) | Pure token consumption; zero ad-hoc hex literals outside `tokens.css`. |
| **Tier 7** | `17_INSTITUTIONAL_SECURITY_STANDARD.md` | Sandbox safety, zero eval, zero dangerous HTML injection, secret protection | Security invariant test suites across all refinement modules. |

---

# 4. Section C — Roadmap Position & Workstream Dependencies

```
[UI-001 Shell Foundation] ──► [UI-002 Navigation] ──► [UI-003 Market Workspace]
                                                            │
┌───────────────────────────────────────────────────────────┘
▼
[UI-004 Intelligence] ──► [UI-005 Planning] ──► [UI-006 Explorer] ──► [UI-007 Governance]
                                                                             │
┌────────────────────────────────────────────────────────────────────────────┘
▼
[UI-008 Institutional AI] ──► [UI-009 Design System] ──► [UI-010 Accessibility]
                                                                │ (D-67 COMPLETE)
┌───────────────────────────────────────────────────────────────┘
▼
╔═══════════════════════════════════════════════════════════════════════════════╗
║   UI-011: Institutional Refinement & Version 1.0 Presentation (ACTIVE PLAN)   ║
╚═══════════════════════════════════════════════════════════════════════════════╝
                                │
                                ▼
╔═══════════════════════════════════════════════════════════════════════════════╗
║   DOC 11: Production Readiness Certification (FIREWALLED OUT-OF-BAND)        ║
╚═══════════════════════════════════════════════════════════════════════════════╝
                                │
                                ▼
               [ AXIOM VERSION 1.0 PRODUCTION RELEASE ]
```

---

# 5. Section D — Complete 6-Phase Delivery Lifecycle (P01 through P06)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ UI-011-P01: Information Hierarchy & Spacing Proportion Calibration                     │
│ Objective: Establish 4-level information hierarchy tokens and 4px grid spacing rhythm.  │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ UI-011-P02: Panel Balance & Workspace Frame Harmonization                               │
│ Objective: Balance header/body/footer padding and card container elevation across pages.│
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ UI-011-P03: Micro-Interaction Consistency & Motion Restraint                            │
│ Objective: Harmonize transition timings (120ms), hover states, and reduce-motion zeroing│
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ UI-011-P04: Optical Typography & Monospace Financial Data Polish                       │
│ Objective: Refine typography weights, optical sizes, and tabular-nums financial tables. │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ UI-011-P05: Cross-Workspace Cohesion & Visual Regression Audit                         │
│ Objective: End-to-end multi-workspace spot-checks and visual regression verification.   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ UI-011-P06: Whole-Surface Version 1.0 Handover & Completion Checkpoint                  │
│ Objective: Final whole-surface audit, documentation sync, and UI-011 COMPLETE handover. │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.1 Phase Specifications

#### Phase P01 — Information Hierarchy & Spacing Proportion Calibration
* **Objective**: Standardize visual weight tokens across Levels 1–4 and calibrate whitespace proportions on the 4px/8px/12px/16px/24px/32px grid.
* **Scope (In)**: Refine `--ix-space-*` scale usage in `Panel.css`, `Card.css`, `InstitutionalWorkspaceShell.css`. Add information elevation tokens (`--ix-elevation-level-1..4`).
* **Scope (Out)**: Component structural rewrites, backend changes.
* **Exit Criteria**: `spacingHierarchy.test.tsx` passing; 0 ad-hoc margin/padding values; build clean (exit 0).

#### Phase P02 — Panel Balance & Workspace Frame Harmonization
* **Objective**: Harmonize header, body, action bar, and footer padding across all 7 primary workspace surfaces (`/charts`, `/intelligence`, `/investigate`, `/governance`, `/trade-plans`, `/journal`, `/compare-scenarios`).
* **Scope (In)**: Standardize `.ix-panel` interior margins, `.ix-card` paddings, and data table frame alignments.
* **Scope (Out)**: Data model changes, endpoint modifications.
* **Exit Criteria**: `panelBalance.test.tsx` passing; uniform panel padding verified across 7 workspace pages.

#### Phase P03 — Micro-Interaction Consistency & Motion Restraint
* **Objective**: Calibrate transition curves, focus outlines, button hover/active elevations, and ensure motion restraint.
* **Scope (In)**: Standardize `transition: var(--ix-motion-fast)` (120ms) across `Button`, `Select`, `Collapsible`, `Toast`, `Dialog`. Verify `@media (prefers-reduced-motion: reduce)` zeroing.
* **Scope (Out)**: New interaction primitives or gesture libraries.
* **Exit Criteria**: `interactionPolish.test.tsx` passing; 0 uncurved transitions; reduced-motion verified.

#### Phase P04 — Optical Typography & Monospace Financial Data Polish
* **Objective**: Refine typography scaling, label/value optical contrast, and ensure strict `tabular-nums` monospace alignment for all financial figures.
* **Scope (In)**: Standardize metadata (`0.75rem`), body (`0.9rem`), panel headings (`0.85rem`), and table numbers across all financial columns (spreads, prices, confidence percentages, ECE metrics).
* **Scope (Out)**: Font family swaps outside `theme.ts`.
* **Exit Criteria**: `typographyPolish.test.tsx` passing; 100% numerical alignment verified.

#### Phase P05 — Cross-Workspace Cohesion & Visual Regression Audit
* **Objective**: Verify seamless visual flow across all workspace transitions without visual jumps, overlapping panels, or font shifts.
* **Scope (In)**: Integration test harness across `/intelligence`, `/charts`, `/governance`, and `/investigate`.
* **Scope (Out)**: Route re-architecting.
* **Exit Criteria**: `crossWorkspaceCohesion.test.tsx` passing; zero visual overlap.

#### Phase P06 — Whole-Surface Version 1.0 Handover & Completion Checkpoint
* **Objective**: Execute final whole-repository grep proofs (actuation, LLMs, sandbox, secrets, ad-hoc hex), verify full regression suite (556+ frontend, 414 backend), update documentation to Version 1.0 presentation status, and produce formal handover report.
* **Scope (In)**: Final verification harness, Level II logs in `docs/evidence/ui011/`, `PROJECT_STATE.md` update.
* **Scope (Out)**: Any functional development.
* **Exit Criteria**: **`UI-011 COMPLETE`** declared; platform certified ready for Doc 11 Production Readiness Certification.

---

# 6. Section E — Existing UI State Audit (UI-001 through UI-010 Surfaces)

| Surface / Primitive | Implementation Status | Visual Consistency Assessment | Polish / Refinement Required |
|---|---|---|---|
| **Workspace Shell (Regions A–F)** | `InstitutionalWorkspaceShell.tsx` | Excellent; responsive reflow at 1280px & 1024px, zero horizontal overflow. | Refine Region A header alignment and Activity Bar padding. |
| **Atomic Components (P02)** | `Button`, `Input`, `Select`, `Badge`, `Card`, `StatusChip`, `Tooltip`, `Accordion` | Standardized, pure token consumption, accessible focus rings. | Polish button active state elevation and select dropdown shadow. |
| **Panel Frame Infrastructure (P03)** | `Panel`, `PanelHeader`, `PanelActionBar`, `Collapsible` | Standardized, collapsible states, span-12 grid rules. | Calibrate header-to-body margin consistency. |
| **Data Tables & Grids (P04)** | `DataTable`, `SortableHeader`, `Pagination`, formatters | Sticky header (`z-index: 2`), `tabular-nums` monospace alignment. | Refine empty/loading state transition smoothing. |
| **Modals & Overlays (P05)** | `Dialog`, `Skeleton`, `Toast`, `ToastStack`, `ErrorBanner` | Focus trap, LIFO dismissal, multi-modal status encoding. | Polish Skeleton shimmer animation gradient subtlety. |
| **Accessibility Primitives (UI-010)** | `SkipLink`, `RouteAnnouncer`, `SrOnly`, `useKeyboardShortcuts` | WCAG 2.1 AA/AAA compliant, aria-live polite, high-contrast tokens. | Retain 100% unchanged; ensure zero visual collision. |

---

# 7. Section F — Existing Test Inventory & Verification Baseline

```text
================================================================================
AXIOM Test Baseline of Record (Pre-UI-011)
================================================================================
Frontend Vitest Suites  : 136 suites / 556 tests passing (100%)
Backend Pytest Suite    : 414 tests passing (100%)
Total Automated Tests   : 970 tests passing
TypeScript Compilation  : tsc -b exits with exit code 0
Vite Production Build   : vite build exits with exit code 0
Security Greps          : 0 actuation, 0 external LLMs, 0 eval, 0 dangerouslySetInnerHTML
Token Compliance        : 0 ad-hoc hex literals outside tokens.css across whole frontend/src
================================================================================
```

---

# 8. Section G — Existing Documentation & Governance Reference Catalog

* `docs/governance/00_VISION_AND_PRINCIPLES.md` — Fundamental commitments.
* `docs/governance/05_SYSTEM_ARCHITECTURE.md` v2.0 — Canonical Presentation Layer specification.
* `docs/governance/08_UI_UX_SPEC.md` — Institutional trading terminal aesthetic specification.
* `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md` — Out-of-band certification standard.
* `docs/governance/12_INSTITUTIONAL_UI_TRANSFORMATION_PLAN.md` — Part VII §13 UI-011 Charter.
* `docs/governance/13_UI_TRANSFORMATION_MASTER_PLAN.md` — Workstream dependencies and phase gates.
* `docs/governance/16_BRAND_GOVERNANCE_STANDARD.md` — Official color palette, contrast ratios, and typography.
* `docs/governance/17_INSTITUTIONAL_SECURITY_STANDARD.md` — Sandbox, injection, and credential standards.
* `docs/plans/UI-009_ENGINEERING_DESIGN_PLAN.md` & `docs/plans/UI-010_ENGINEERING_DESIGN_PLAN.md` — Direct architectural predecessors.
* `PROJECT_STATE.md` (v8.82.0) & `CHANGELOG.md` — Continuous project state ledger.

---

# 9. Section H — Retain / Extend / Supersede / Defer Component Matrix

| Component / Layer | Classification | Rationale | Cost of Change |
|---|---|---|---|
| `tokens.css` 5-tier architecture | **RETAIN** | Fundamental token structure is mature, tested, and WCAG AA/AAA compliant. | Zero (0) |
| `theme.ts` typed contracts | **RETAIN** | Strict TypeScript interfaces enforce token usage across all components. | Zero (0) |
| `SkipLink.tsx` & `RouteAnnouncer.tsx` | **RETAIN** | Screen-reader and bypass navigation fully verified in UI-010. | Zero (0) |
| `EmptyState.tsx` & `ErrorBanner.tsx` | **RETAIN** | Feedback primitives fully standardized in UI-010-P03. | Zero (0) |
| `Panel.css` & `Card.css` padding | **EXTEND** | Calibrate optical spacing rhythm (4px grid) for uniform visual balance. | Low (CSS token refinement) |
| `Button.css` active micro-interaction | **EXTEND** | Polish active/pressed transform and focus-visible glow smoothness. | Low (CSS token refinement) |
| `Skeleton.css` shimmer gradient | **EXTEND** | Soften shimmer gradient for institutional subtlety. | Low (CSS token refinement) |
| Multi-theme high contrast | **RETAIN** | `@media (prefers-contrast: more)` verified in UI-010-P05. | Zero (0) |
| Mobile viewports (<768px) | **DEFER** | Desktop/laptop (1280px/1024px) is the Version 1.0 institutional target. | Post-v1.0 Roadmap |

---

# 10. Section I — Proposed P01 (Information Hierarchy & Spacing Refinement)

### 10.1 Re-baseline & Boundary Formulation
1. **Retained Elements**: 5-tier token hierarchy in `tokens.css`, `theme.ts` contracts, all UI-009/UI-010 primitives.
2. **Extended Elements**: Information hierarchy spacing classes (`.ix-hierarchy-level-1..4`), panel padding harmonization tokens.
3. **Superseded Elements**: None.
4. **Deferred Elements**: Mobile companion layout (<768px).
5. **Collective Satisfaction**: Current 136 suites / 556 tests provide a rock-solid foundation; P01 establishes the visual weight standards.
6. **Re-baseline Determination**: Clean forward execution extending the 136/556 baseline without breaking changes.
7. **Next Build Order Boundary**: `BUILD_ORDER_UI-010-P01` shall authorize:
   - Defining visual hierarchy tokens in `tokens.css` and `theme.ts`.
   - Harmonizing spacing across shell regions and panel frames.
   - Adding `spacingHierarchy.test.tsx` and invariant tests (+4 to +8 tests).

---

# 11. Section J — Objective Acceptance Criteria (P01 & Full Workstream)

| # | Criterion | Verification Method | Governing Requirement |
|---|---|---|---|
| **AC-01** | Information hierarchy tokens (`--ix-hierarchy-*`) codified and typed in `theme.ts` | Unit test `spacingHierarchy.test.tsx` | `12` Part V §5, `16` |
| **AC-02** | Panel interior spacing uniformly conforms to 4px/8px/12px/16px/24px/32px scale | DOM snapshot & CSS token audit | `12` Part VI §17 (Consistent Spacing) |
| **AC-03** | Micro-interaction transitions strictly adhere to `var(--ix-motion-fast)` (120ms) | CSS transition audit | `12` Part VI §17 (Subtle Animations) |
| **AC-04** | Numerical data tables strictly render with monospace `tabular-nums` | Table formatter unit tests | `08_UI_UX_SPEC.md`, `03` |
| **AC-05** | Zero ad-hoc hex literals across `frontend/src/` (outside `tokens.css`) | `grep_ad_hoc_hex.log` exit 1 | `16_BRAND_GOVERNANCE_STANDARD.md` |
| **AC-06** | Zero actuation, zero external LLMs, zero dangerous innerHTML/eval | Whole-repo security greps exit 1 | `17_INSTITUTIONAL_SECURITY_STANDARD.md` |
| **AC-07** | Full platform regression suite passes with 100% success (≥556 frontend, 414 backend) | Vitest & Pytest execution logs | Definition of Done |
| **AC-08** | TypeScript compile (`tsc -b`) and Vite production build exit with code 0 | `tsc.log` and `vite_build.log` | Definition of Done |

---

# 12. Section K — Technical, Architectural & UI Dependencies

```
[Design Tokens (tokens.css)] ──► [Component Primitives (components/ui/)] ──► [Workspace Shell (Regions A-F)]
              │                                      │                                      │
              ▼                                      ▼                                      ▼
[Spacing & Hierarchy Tokens] ──► [Panel Frame Balance & Motion] ──► [Cross-Workspace Version 1.0 Polish]
```

* **Build Tools**: Vite 8, TypeScript 5.6, Vitest 4.1.
* **Testing Libraries**: `@testing-library/react`, `@testing-library/jest-dom`, `jsdom`.
* **CSS Framework**: Pure CSS custom properties (`var(--ix-*)`), zero external CSS utility frameworks (Tailwind/Bootstrap forbidden).

---

# 13. Section L — Cybersecurity Model & Security UX

1. **Zero Actuation Invariant (S-1)**: All UI controls are presentation-only. Buttons in refined panels trigger view updates or research state filters; zero connection to order execution engines or broker APIs.
2. **Zero External AI / LLMs (S-2)**: No third-party LLM APIs or browser-side inference SDKs.
3. **Sandbox Safety (S-3)**: Zero `dangerouslySetInnerHTML` and zero `eval()` / `new Function()` in any refinement module.
4. **Credential Protection (S-4)**: Zero passwords, API keys, or JWT tokens exposed in UI telemetry, logging, or DOM attributes.
5. **Pure Token Consumption (S-5)**: 0 ad-hoc hex literals outside `tokens.css`.

---

# 14. Section M — UI/UX Interaction Standards & Institutional Polish

In strict adherence to `12_INSTITUTIONAL_UI_TRANSFORMATION_PLAN.md` Part VI §17 (*Institutional Polish*):
* **Consistent Spacing**: Standardized 4px grid rhythm across margins, paddings, and gap properties.
* **Subtle Animations**: Restrained transitions (`120ms` cubic-bezier), zero bouncy or distracting effects.
* **Stable Transitions**: Smooth opacity and elevation changes on panel collapses and modal entries.
* **Clean Typography**: High-contrast typography hierarchy (Display, Workspace Title, Panel Heading, Body, Metadata).
* **Balanced Information Density**: Visual breathing room between dense financial tables and summary cards.
* **Predictable Interaction Patterns**: Identical hover, active, and focus-visible affordances across all components.
* **Professional Iconography**: Crisp, standardized Unicode glyphs (`▲`, `▼`, `◆◆◆`, `✓`, `ℹ`, `⚠`, `✕`).
* **Uniform Panel Behaviour**: Consistent header bars, action slots, collapsible toggles, and footer status indicators.

---

# 15. Section N — System Architecture & Integration Points

`UI-011` operates strictly within the **Presentation Layer** defined in `05_SYSTEM_ARCHITECTURE.md` v2.0 §13:

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         AXIOM WORKSTATION SHELL (REGIONS A–F)                           │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ Region A: Global Command Bar (SkipLink, RouteAnnouncer, Breadcrumbs, Status Chips, Search)│
├──────────────┬────────────────────────────────────────────────────────────┬──────────────┤
│ Region B:    │ Region C: Primary Workspace Host                           │ Region D:    │
│ Navigation   │  ┌──────────────────────────────────────────────────────┐  │ Context      │
│ Dock         │  │ 7 Governed Workspaces (/charts, /intelligence, etc.) │  │ Panel        │
│ (Alt+O..W)   │  │ Refined Information Hierarchy & Panel Balance         │  │ Inspector    │
│              │  └──────────────────────────────────────────────────────┘  │              │
├──────────────┴────────────────────────────────────────────────────────────┴──────────────┤
│ Region E: Activity Dock (Real-time Telemetry, System Health, Observability Gauges)       │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ Region F: Overlay Layer (Dialog Focus Traps, ToastStack Notifications, Command Palette)  │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

# 16. Section O — Documentation Synchronization & State Management

Upon completion of each UI-011 phase:
1. `PROJECT_STATE.md` version will increment monotonically (8.83.0 $\rightarrow$ 8.88.0).
2. `CHANGELOG.md` will record exact phase deliverables.
3. Level II evidence logs will be generated in `docs/evidence/ui011/`.
4. 20-section Delivery Reports with §25 DA Governance Declarations will be submitted to the ITRGA.

---

# 17. Section 4A — Operational Methodology Invariants & Non-Deviation Rules

1. **Continuity Obligations (§4A.1)**: DA and ITRGA maintain the established evidence-backed workflow. No conversational-only state.
2. **Prohibited Parallel Processes (§4A.2)**: No parallel development branches or out-of-order execution.
3. **Workflow Conflict Resolution (§4A.3)**: Canonical constitutional hierarchy (`10_CONSTITUTIONAL_HIERARCHY.md`) governs all disputes.
4. **Purpose of Plan (§4A.4)**: Establish the authoritative roadmap to deliver the final institutional polish required for AXIOM Version 1.0.

---

# 18. Closing Recommendations & Governance Declaration

```text
## DA Governance Declaration (Per Amendment §25)

The AXIOM Development Authority (DA) submits this UI-011 Engineering Design Plan to the ITRGA for formal review.

1. Scope: Establishes the complete 6-phase delivery lifecycle (P01 through P06) for institutional refinement and Version 1.0 presentation.
2. Baseline: Built upon the verified UI-010 COMPLETE baseline (136 suites / 556 tests frontend, 414 tests backend, 970 total tests passing).
3. Invariants: Governance Gate remains STRICTLY CLOSED. Production status remains NOT CERTIFIED. Zero live order execution, zero external LLMs, zero dangerous DOM injections, zero hardcoded secrets, and pure token consumption are enforced.
4. Recommendation: DA recommends approval of this Design Plan and issuance of BUILD_ORDER_UI-011-P01.

"We don't guess. We prove."

Submitted by: AXIOM Development Authority (DA)
Date: 2026-08-11
```

---

**End of UI-011_ENGINEERING_DESIGN_PLAN.md**
