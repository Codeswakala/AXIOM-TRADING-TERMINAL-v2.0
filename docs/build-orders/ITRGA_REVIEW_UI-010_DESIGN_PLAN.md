# ITRGA REVIEW — UI-010 ENGINEERING DESIGN PLAN
## Accessibility & Operator Experience — Determination

**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Review ID:** `ITRGA-DETERMINATION-UI010-DESIGN-PLAN`
**Review Subject:** `UI-010_ENGINEERING_DESIGN_PLAN.md` (396 lines, 35,976 bytes) + `DELIVERY_REPORT_UI-010_DESIGN_PLAN.md` (100 lines, 6,365 bytes)
**Governing Request:** `ITRGA_REQUEST_UI-010_DESIGN_PLAN.md` (Issued 2026-08-11 — 15 sections A–O + §4A)
**Workstream:** UI-010 — Accessibility & Operator Experience
**Preceding Milestone:** **UI-009 — Institutional Design System Implementation COMPLETE** (D-60 — 113 suites / 485 tests · 414 backend · Gate CLOSED · NOT CERTIFIED · `ITRGA-DECLARATION-UI009-COMPLETE-D60` 8.76.0)
**Baseline of Record:** Frontend 113/485 · Backend 414 · `tsc -b && vite build` exit 0 (D-60)
**Governing Corpus:** `10_CONSTITUTIONAL_HIERARCHY.md` + `DOCUMENT_PRECEDENCE.md` v2.0.0 (05 v2.0 canonical) + 00/01/02/03/04/05 v2.0/08/11 §7/12/13/14/15/16/17 + Prior D-54→D-60 (UI-009)
**Review Standard:** High-Grade — 12 Disciplines · 7-Stage Lifecycle · EVF-1…EVF-4 · Best Among All Possible Outcomes
**DA Operational State:** Design Plan submitted, implementation on **formal hold** (affirmed in both documents)

> **We don't guess. We prove.**

---

## STAGE 1 — ESTABLISH AUTHORITY

| Item | Value | Evidence | Assessment |
|------|-------|----------|------------|
| Request | `ITRGA_REQUEST_UI-010_DESIGN_PLAN.md` | Delivery Report §1 | ✅ Formal ITRGA request — Tier 8 Execution Governance, correctly traces to `12` Part VII §12 charter (verbatim), `12` Part II §9 / Part VIII §11, `08` Accessibility, `11` §7 (firewalled) |
| Design Plan | `docs/plans/UI-010_ENGINEERING_DESIGN_PLAN.md` | Header + TOC A–O + §4A (396L, 35,976 bytes) | ✅ Migratable path `docs/plans/` (correct per 10 Tier 8) — 18 chapters including Executive Summary, A–O, 4A, Closing |
| Delivery Report | `DELIVERY_REPORT_UI-010_DESIGN_PLAN.md` | 100L — 6-transcript intake | ✅ Reports design plan as deliverable, correct 6-phase summary, classification, hold affirmation |
| Preceding Baseline | UI-009 COMPLETE D-60 — 113/485 + 414 | Header + §4 Previous Baseline + §7 Test Inventory | ✅ Correct per `PROJECT_STATE.md` 8.76.0; monotonic chain UI-001→UI-009 preserved (83/376→113/485 +30/+109) |
| Gate / Production | CLOSED / NOT CERTIFIED (11 firewalled) | Header + §1 Invariants | ✅ Correct per 03/05/11 — no Gate opening implied; invariants explicitly listed (5 governance invariants) |
| Amendment | 27 rules (UI-008 precedent, carried UI-009→UI-010) | §1 Purpose + §3 Traceability | ✅ Referenced as process precedent; UI-010 will be governed by same principles (Master Prompt Part 10) |

**Stage 1 Closed — Authority Established to EVF-1 (Direct Documentary).** All required governance parents are present and correctly cited.

---

## STAGE 2 — ESTABLISH SCOPE

### Requested vs Delivered (Per ITRGA_REQUEST_UI-010 §2 A–O + §4A)

| Required Section | Delivered | Assessment |
|------------------|-----------|------------|
| **A. UI-010 Objective** | §2 — traces to `12` Part VII §12 verbatim charter (8-item checklist), `12` Part II §9 / Part VIII §11, `08` performance benchmarks (`<100ms`, 60 FPS), `11` §7 (preparatory); explains Level D Refinement & sequencing after UI-009 (primitives exist to be made accessible) + before UI-011 (polish requires accessibility stable) | ✅ **Compliant** — correctly frames UI-010 as inclusive hardening, not expansion |
| **B. Governing Requirements** | §3 — Traceability matrix **19 rows** Tiers 1→10 (00 Principle 3/5, 01 institutional decision support, 02 dark-first/no color-alone, 11 §7 firewalled, 03 §8/§12, 04 sequencing, 05 Presentation Layer §13/§30/§67, 08 full Accessibility, 08 Reasoning, 09 ITRGA, 10 hierarchy, 12 Part VII §12/VIII §11, 13 Level D/Parts II/V, 14 6 Regions, 15 reduced-motion, 16 Part XII, 17 style-injection, Tier 8 UI-009 plan, Tier 10 D-50→D-60) | ✅ **Compliant** — hierarchical, tier-ordered per 10, cites canonical 05 v2.0, correctly marks 11 §7 as preparatory |
| **C. Roadmap Position** | §4 — Diagram: Waves 0–7 COMPLETE (v0.62.0) → UI-001→UI-008 COMPLETE → **UI-009 (P01→P06 D-55→D-60) 113/485 baseline** → **UI-010 ACTIVE 6 phases** → UI-011 → Doc 11 firewalled | ✅ **Compliant** — correctly places UI-010 as Level D Refinement bridging Foundational (UI-009) and Final Polish (UI-011) |
| **D. Phase Structure** | §5 — 6-phase lifecycle: **P01 Accessibility Foundation & Semantic Audit** (axe/Testing Library, ARIA landmarks Regions A–F, `SkipLink`), **P02 Responsive & Adaptive Layouts** (breakpoint tokens `--ix-breakpoint-*`, `1280px/1024px` reflow, table sticky headers), **P03 Feedback States** (Loading `Skeleton`, Empty `EmptyState`, Error `ErrorBanner`, Notification `ToastStack`), **P04 Keyboard & Focus** (skip links `#main-content`, focus trap validation, `Escape`/`Ctrl+K`/Tab/Arrow/Enter/Space), **P05 Screen-Reader & High-Contrast & Reduced-Motion** (`aria-live` polite/assertive, `.ix-sr-only`, no color-alone, `prefers-contrast`/`prefers-reduced-motion` → `0ms`), **P06 Whole-Surface Audit & Completion** (full regression, axe/WCAG, grep, handover) | ✅ **Compliant** — bounded, sequential, each with status/scope/boundary; correctly defers P06 audit to completion checkpoint |
| **E. Existing UI State Audit** | §6 — 6 workstation regions A–F detailed (A Command Bar, B Navigation Dock, C Primary Workspace/WorkspaceHost, D Context Panel, E Activity Dock, F Overlay Layer + portaled modals), 22 UI-009 primitives inventoried (8 atoms + 4 panels + 5 tables + 5 overlays + tokens), 7+ workspace pages (`/charts`, `/intelligence`, `/investigate`, `/governance`, `/trade-plans`, `/journal`, `/compare-scenarios`, `/execution-research`, `/research-management`), baseline contrast >4.5:1 (up to 16.5:1) + 0 ad-hoc hex, **4 identified gaps**: Skip Navigation, Responsive Reflow <1280px, Consistent Empty States, Screen-Reader Announcements | ✅ **Compliant** — exhaustive audit of shell/layout + primitives + workspaces; satisfies “what exists to be made accessible” with gap analysis |
| **F. Existing Tests** | §7 — Table categorizes 113 suites / 485 tests by a11y relevance: Tokens 1/5, Atoms 8/23, Panels 5/18, Tables 5/21, Modals 5/21, Security 8/27, Shell 12/70, Workspaces 69/300 + backend 414 — 100% pass | ✅ **Compliant** — correctly categorizes baseline by accessibility relevance, not just count |
| **G. Existing Documentation** | §8 — Catalog 15 items 00–17, 12/13/14/15/16/17, `UI-009_ENGINEERING_DESIGN_PLAN.md` (D-54), `PROJECT_STATE.md` 8.76.0 | ✅ **Compliant** — references canonical set; Delivery Report §2 correctly expands to 16 constitutional governance and security standards |
| **H. Retain / Extend / Supersede / Defer Matrix** | §9 — Table 11 rows: 5 RETAIN (5-tier tokens AAA >14:1, 8 atoms full ARIA, panel frames accessible, DataTable/Pagination ARIA, Dialog focus trap), 5 EXTEND (Shell `SkipLink` WCAG 2.4.1, layout grid breakpoint tokens WCAG 1.4.10, sub-panel Empty States, `RouteAnnouncer` live region WCAG 4.1.3, `prefers-contrast` high-contrast), 1 DEFER (Mobile <768px post-1.0 per 08 roadmap) | ✅ **Compliant** — each with traced rationale to 08/11/12/WCAG 2.4.1/1.4.10/4.1.3; summary 5-5-0-1-0 correct; no unwarranted SUPERSEDE (correct: 0 supersede because WCAG gaps are additive) |
| **I. Proposed P01** | §10 — 7-part: 1 Retained 22 UI-009 primitives + 5-tier tokens, 2 Extended `frontend/src/workstation/accessibility/` + `SkipLink.tsx/.css` + `accessibilityAudit.test.ts`, 3 Superseded None (no WCAG conflict), 4 Deferred viewport reflow/Toast harmonization/shortcut matrix/high-contrast to P02→P05, 5 Collective Satisfaction 92% WCAG 2.1 AA satisfied, 6 Re-baseline additive +1 suite /+5 → 114/490, 7 Build Order Boundary In: `SkipLink`, Shell Region A landmark, audit test suite, `docs/evidence/ui010/`; Out: responsive reflow, feedback rewrites, shortcut manager, whole-surface audit, backend, external AI, actuation | ✅ **Compliant** — fully satisfies Re-baseline Directive §I 7 parts; no silent supersede; additive, migratable |
| **J. Acceptance Criteria** | §11 — P01 AC-01…AC-06 (SkipLink focus Tab→`#main-content` WCAG 2.4.1, Shell Regions A–F ARIA landmark roles WCAG 1.3.1, heading hierarchy `h1→h2→h3` WCAG 1.3.1, 0 ad-hoc hex, zero actuation/LLM/dangerous HTML/eval, frontend ≥485→490 + backend 414 + `tsc`/`vite` exit 0) + Full workstream 5 targets (100% keyboard operability 2.1.1, focus visibility 2.4.7/2.4.3, reflow 1.4.10 ≤1024px zero horizontal scroll, multi-modal status 1.4.1, reduced-motion 2.3.3 0ms) | ✅ **Compliant** — each verifiable via Level I/II, correctly traced to WCAG criterion 1.3.1/1.4.1/1.4.3/1.4.10/2.1.1/2.4.1/2.4.7 + 08/11/12 |
| **K. Dependencies** | §12 — governance (10/12/13), brand/tokens (`16`/5-tier/`theme.ts`), component foundation (22 UI-009 primitives 113/485), shell (Regions A–F), a11y engine (`@testing-library/react` + WAI-ARIA), build toolchain (TS 5.6.3, Vite 8.1.4, Vitest) | ✅ **Compliant** — stack correct; `theme.ts` contrast helpers from UI-009 P01 correctly listed |
| **L. Cybersecurity** | §13 — Focus without credential exposure (no `value` in logs/DOM), style-injection defense (no `dangerouslySetInnerHTML`/`eval`), no hidden actuation via ARIA (S-1/S-2 greps), auditability on-tree `docs/evidence/ui010/` | ✅ **Compliant** — correctly anticipates ARIA not used to hide actuation controls |
| **M. UI/UX** | §14 — Keyboard `Tab`/`Shift+Tab`/`Enter`/`Space`/`Escape`/`Arrow`, focus `#8CC2FF` contrast ≥8.9:1, contrast >4.5:1 (>7.0:1 primary), responsive breakpoints ≥1440 / 1280–1439 / 1024–1279 with panel collapse + table horizontal scroll + sticky header, motion restraint + `prefers-reduced-motion` | ✅ **Compliant** — satisfies 08 + 16 Part XII; breakpoints correctly extend P01 token hierarchy |
| **N. Architecture** | §15 — Presentation Layer ownership 05 v2.0 §13, `frontend/src/workstation/accessibility/` + `frontend/src/components/ui/`, integration points `InstitutionalWorkspaceShell.tsx` (SkipLink + landmarks), `tokens.css` breakpoint variables, `WorkspaceHost.tsx` route announcement | ✅ **Compliant** — bounded context isolated, no backend coupling |
| **O. Documentation & State** | §16 — `PROJECT_STATE.md` 8.77.0→8.82.0 UI-010 COMPLETE, `CHANGELOG.md`, `RISK_REGISTER.md` & `TECHNICAL_DEBT_REGISTER.md` (0 new debt), `docs/evidence/ui010/` Level II logs | ✅ **Compliant** — monotonic versioning, migratable |
| **§4A Methodology Invariants** | §17 — Strict phased ordering Roadmap→Design Plan→Build Order→Implementation→Verification→Delivery→Review→Determination, prohibition parallel work (no speculative P02→P06), no conversational state (all on-tree) | ✅ **Compliant** — preserves Master Prompt 4A |

**Design Plan Structural Completeness:** **18/18 chapters delivered** (Executive Summary + A–O + 4A + Closing). No required section missing. Delivery Report correctly summarizes A–O (§2 table) and 6-phase lifecycle (§3).

### Out-of-Scope Protection

Plan §10 P01 Out-of-Scope (responsive reflow P02, feedback rewrites P03, shortcut manager P04, high-contrast P05, whole-surface audit P06, backend mutations, external AI, actuation controls) — **explicit and correct** — UI-010 P01 is **landmark/skip-link/semantic audit only.**

**Stage 2 Closed — Scope Compliant. No scope creep.**

---

## STAGE 3 — ESTABLISH EVIDENCE

| Claim | Evidence | Type | Assessment |
|-------|----------|------|------------|
| Baseline 113/485 + 414 + exit 0 | §1 Header + §5 + §7 | Level II/III Documentary | **EVF-1** — directly cites D-60 UI-009 COMPLETE baseline; internally consistent with P06 113/485 |
| Shell 6 regions A–F + 33 quick actions + 22 UI-009 primitives + 7 workspace pages | §6 audit | Level III Documentary | **EVF-1** — correctly inventories `UI-001/002` shell + UI-003→UI-009 surfaces + `tokens.css` 5-tier + `CommandPalette.css` |
| 6-phase lifecycle P01→P06 | §5 | Level III | **EVF-1** — bounded, phases correctly aligned to 12 charter checklist (Accessibility, Responsive, Loading/Empty/Error/Toast, Keyboard/Focus, Screen-Reader/High-Contrast/Reduced-Motion, Whole-Surface) |
| Retain 5 / Extend 5 / Supersede 0 / Defer 1 | §9 matrix | Level III | **EVF-1** — each classified with WCAG-traced rationale (2.4.1, 1.4.10, 1.3.1, 4.1.3, prefers-contrast) |
| P01 7-part re-baseline + Build Order Boundary | §10 | Level III | **EVF-1** — directly verifiable design; +1 suite/+5 → 114/490 additive, no rework |
| AC-01…AC-06 + 5 full-workstream targets | §11 | Level III | **EVF-1** — each verifiable via `SkipLink.test.tsx`/`accessibilityAudit.test.ts` + axe/contrast + greps |
| Implementation Hold | §18 Closing + Delivery Report §5 | Level III | **EVF-1** — both documents affirm hold — `NO UI-010 implementation has been initiated` |

---

## STAGE 4 — INVESTIGATE — 12 DISCIPLINES

| Discipline | Assessment |
|------------|------------|
| **Software Engineering** | `SkipLink.tsx/.css` + `accessibilityAudit.test.ts` as P01 additive module in `frontend/src/workstation/accessibility/` is maintainable, isolated, low-coupling (shell landmark integration only); audit test querying all 113 suites for landmark/heading/focusability is correct harness for WCAG 1.3.1. |
| **System Architecture** | Correctly places UI-010 in **Presentation Layer** per 05 v2.0 §13 single ownership; bounded contexts `frontend/src/workstation/accessibility/` (new) + `frontend/src/components/ui/` (113/485 existing) + `InstitutionalWorkspaceShell.tsx` Regions A–F isolated; no new backend bounded context, no circular deps; integration points Shell/`tokens.css`/Component Library correctly respect 05 §13. |
| **Cybersecurity** | **Strong:** Focus management without credential exposure (no `value` in logs/DOM), style-injection defense (no `dangerouslySetInnerHTML`/`eval` for ARIA), no hidden actuation via ARIA labels (S-1/S-2 greps 0 actuation/LLM remain enforced per §13), auditability on-tree `docs/evidence/ui010/` — correctly anticipates ARIA not used to hide dormant execution triggers. |
| **UI/UX** | **High-grade:** Keyboard-first `Tab`/`Shift+Tab`/`Enter`/`Space`/`Escape`/`Arrow` per 08, focus `#8CC2FF` ≥8.9:1 contrast (WCAG 2.4.7), contrast >4.5:1 text / >7.0:1 primary (WCAG 1.4.3), responsive breakpoints ≥1440 / 1280–1439 / 1024–1279 with panel collapse + table sticky headers (WCAG 1.4.10 Reflow — zero horizontal page scroll at 1280/1024), multi-modal status encoding (no color-alone 1.4.1), reduced-motion `0ms` (2.3.3) — **all WCAG 1.3.1/1.4.1/1.4.3/1.4.10/2.1.1/2.4.1/2.4.3/2.4.7/4.1.3 prepared correctly.** |
| **Data Engineering** | **No data impact:** No persistence/migration/provenance mutation — accessibility/operator experience only; `RISK_REGISTER.md`/`TECHNICAL_DEBT_REGISTER.md` correctly state 0 new debt. |
| **ML / AI** | **No ML/AI in scope:** No training/inference — correctly out-of-scope per 07; screen-reader announcements are deterministic ARIA live regions, not generative AI. |
| **Trading / Quant** | **No trading logic:** No signal/execution/quant — correctly out-of-scope per 12 Part I §5; Gate CLOSED invariant explicitly listed (§1). |
| **DevOps / Infrastructure** | Dependencies axe-core/`@testing-library/react`/`prefers-reduced-motion`/`prefers-contrast` + TS 5.6.3/Vite/Vitest + build toolchain correctly listed; verification via `vitest`/`tsc`/`vite`/`grep`/`axe` per 10 hierarchy — **build reproducible.** |
| **Governance** | **20-section plan** + Delivery Report correctly trace tiers per 10 hierarchy via §3 matrix; 6-phase lifecycle bounded with explicit In/Out per §10 P01; implementation hold affirmed (no speculative P02→P06 per §17); `NO DEVIATIONS` correctly anticipated for P01 (landmark audit only); Gate CLOSED / NOT CERTIFIED held; debt `TD-UI-POSTCSS-HIGH`/`OBS-P06-2` correctly carried per §1 invariants. |
| **Testing & Verification** | `accessibilityAudit.test.ts` scanning landmark completeness `banner`/`navigation`/`main`/`complementary`/`region` + heading hierarchy `h1→h2→h3` + focusability is **correct high-grade harness** for WCAG 1.3.1 (Info & Relationships) — proportionate for P01; `SkipLink.test.tsx` (Tab → `#main-content` 2.4.1) is minimal and focused. |
| **Documentation & Knowledge Continuity** | Plan is **migratable** (`docs/plans/UI-010_ENGINEERING_DESIGN_PLAN.md` as single truth, per §16) + Delivery Report as intake; correctly lists docs 00–17, ADRs, registers, Amendment, `PROJECT_STATE.md` 8.76.0 — **institutional memory preserved** per 10 Tier 7. |
| **Product / Operator Integrity** | Keyboard-first + whole-surface `aria-live` route announcements + honest empty `role="status"` / error `role="alert"` correctly improve operator efficiency without misrepresenting simulated vs live telemetry; `prefers-contrast` high-contrast overrides respect operator preference — **honest state per 02.** |

**No discipline reveals a defect that would prevent approval.** Gaps identified in §6 (Skip Navigation, Responsive Reflow, Consistent Empty States, Screen-Reader Announcements) are **correctly mapped to P01→P05** — not hidden.

---

## STAGE 5 — COMPARE — REQUEST → PLAN → GOVERNING REQUIREMENTS

| Dimension | Comparison | Result |
|-----------|------------|--------|
| Request A–O + §4A → Plan A–O + §4A | All 15+1 sections present and mapped with same titles; 6-phase structure as requested; 7-part P01 re-baseline as required | ✅ **No mismatch** |
| Plan → `12` Part VII §12 (8-item checklist) + `12` Part II §9 / Part VIII §11 | Plan correctly operationalizes Keyboard, Accessibility, Responsive, Loading, Empty, Error, Notifications, Polish via P01 semantic audit → P02 responsive → P03 feedback → P04 keyboard/focus → P05 screen-reader/high-contrast/reduced-motion → P06 audit | ✅ **No mismatch** |
| Plan §10 P01 boundary → 11 §7 (8 categories + focus) | `SkipLink` + ARIA landmark inventory + heading hierarchy + 0 ad-hoc hex + greps directly prepare the platform to *pass* future 11 §7 certification (without self-certifying) — correctly **preparatory, not self-certification** | ✅ |
| Plan §11 AC-01…AC-06 → WCAG 1.3.1/1.4.1/1.4.3/1.4.10/2.1.1/2.4.1/2.4.7 + 08/11/12 | Each AC verifiable via `SkipLink.test.tsx`/`accessibilityAudit.test.ts` + axe/contrast + greps | ✅ |
| Plan §16 docs sync → 10 operational governance | `PROJECT_STATE.md` 8.77.0→8.82.0 `UI-010 COMPLETE` + `CHANGELOG.md` + `RISK`/`DEBT` + `docs/evidence/ui010/` correctly listed | ✅ |

**No mismatches. Minor note: `WCAG 2.4.1` bypass blocks is correctly prepared by `SkipLink` in P01, not deferred — correct prioritization per 13 Level D.**

---

## STAGE 6 — DETERMINE FINDINGS

### 6.1 Classification

| Finding Type | Count | Detail |
|--------------|-------|--------|
| Blocker | 0 | None |
| Major Defect | 0 | None |
| Material Observation | 0 | None |
| **Minor Observation** | **1** | **O-010-01** (responsive table sticky-header detail — not a defect) |
| Governance Issue | 0 | None |

### 6.2 Observation Detail

| ID | Severity | Description | Required Action | Blocking? |
|----|----------|-------------|-----------------|-----------|
| **O-010-01** | Minor | **Responsive Table Sticky-Header Token Detail** — §14 Responsive Breakpoints correctly lists Desktop Large ≥1440 / Standard 1280–1439 / Laptop Compact 1024–1279 with panel collapse + table horizontal scroll. The P02 proposal for tables (`DataTable` sticky headers via `var(--ix-table-header-bg)`) would benefit from explicit token `--ix-table-sticky-header-z-index` for stacking context when panels collapse and tables scroll horizontally on 1024px. This is **not a WCAG failure** — current tables already pass 1.4.10 via horizontal scroll — it is an implementation detail that improves stacking predictability during responsive reflow. | In `BUILD_ORDER_UI-010-P02` (Responsive Behaviour & Adaptive Layouts) and/or P02 delivery, **define `--ix-table-sticky-header-z-index: 2`** (or similar) alongside `--ix-breakpoint-*` tokens, and ensure `DataTable` sticky header `z-index` references it. Verify via `accessibility.log` or `DataTable.test.tsx` at 1024px viewport. | **No** |

*No other observations. The single minor observation is **non-blocking refinement** for P02 responsive work — it does not affect the design plan's approvability.*

---

## STAGE 7 — VERDICT

### **APPROVED WITH OBSERVATIONS**

**Determination ID:** `D-61`
**Phase:** UI-010 Engineering Design Plan — Accessibility & Operator Experience
**Verdict:** **APPROVED WITH OBSERVATIONS** (1 Minor Observation — O-010-01)
**Evidence Level:** Plan satisfies all 15+1 required sections; traceability Tier 1→10 is complete; 6-phase lifecycle bounded; Retain 5 / Extend 5 / Supersede 0 / Defer 1 matrix is sound; collaborative governance preserved
**Blockers / Major Defects:** **0**
**Regressions:** N/A — design plan phase (no code)
**Next Authorized Unit:** **`BUILD_ORDER_UI-010-P01` — Accessibility Foundation & Semantic Audit**

#### Rationale

**Design completeness:** All 15 sections A–O + §4A + Executive Summary + Closing are present, correctly bounded for a Level D Refinement workstream that finalizes accessibility and operator experience across UI-001→UI-009 surfaces without introducing new trading/backend/execution/external-AI. 6-phase lifecycle (P01 Semantic Audit & SkipLink → P02 Responsive Breakpoints & Reflow → P03 Feedback States → P04 Keyboard & Focus → P05 Screen-Reader & High-Contrast & Reduced-Motion → P06 Whole-Surface Audit) is logically sequenced and dependency-correct per 13 Part II Level D and 13 Part V §8/§9 (Accessibility/Responsive Integration).

**Governance compliance:** Correctly traces to 00/01/02/11 §7 (firewalled preparatory)/03/04/05 v2.0/08/10/12 Part VII §12 & Part VIII §11/13 Part II Level D & Parts V/VI/14 6 Regions/15/16 Part XII/17 + UI-009 Design Plan 374L + D-55→D-60 (113/485); implementation hold is correctly affirmed (DA will not implement until Build Order); no silent methodology change (Roadmap→Design Plan→Build Order→… preserved).

**Technical soundness:** 5 RETAIN (tokens AAA >14:1, 8 atoms full ARIA, panel frames accessible, DataTable/Pagination ARIA, Dialog focus trap) + 5 EXTEND (Shell SkipLink WCAG 2.4.1, layout grid breakpoint tokens WCAG 1.4.10, sub-panel Empty States, RouteAnnouncer live region WCAG 4.1.3, `prefers-contrast` high-contrast) + 1 DEFER (Mobile <768px post-1.0) matrix is correct; P01 additive +1 suite/+5 →114/490 is risk-free and additive; `SkipLink` + `accessibilityAudit.test.ts` is the correct minimal, focused P01 harness for WCAG 1.3.1/2.4.1.

**Security & product integrity:** Correctly holds invariants — focus without credential exposure, style-injection defense, no hidden actuation via ARIA (S-1/S-2 greps 0 actuation/LLM) — no new attack surface.

**Observation does not prevent approval** — O-010-01 is minor implementation-guidance for P02 responsive work and will be verified via `--ix-table-sticky-header-z-index` + `accessibility.log` in the P02 evidence package.

---

## AUTHORIZATION

With this determination **D-61**, the **UI-010 Engineering Design Plan is APPROVED WITH OBSERVATIONS.**

**The ITRGA now authorizes issuance of:**

> **`BUILD_ORDER_UI-010-P01` — Accessibility Foundation & Semantic Audit**
> *Implement `SkipLink.tsx/.css` + Shell Region A landmark integration + comprehensive automated semantic audit test suite (`accessibilityAudit.test.ts`) querying all 113 test suites for ARIA landmark completeness, heading levels, and focusability — pure token consumption, 0 ad-hoc hex, WCAG 2.4.1/1.3.1.*

The DA is authorized to begin **P01 implementation only after** receipt of that Build Order. No P02–P06 work is authorized.

---

## DOCUMENT CONTROL

| Field | Value |
|-------|-------|
| Review ID | D-61 |
| Reviewed By | ITRGA — Independent Technical Review & Governance Authority |
| Review Date | 2026-08-11 |
| Governing Request | `ITRGA_REQUEST_UI-010_DESIGN_PLAN.md` |
| Design Plan | `docs/plans/UI-010_ENGINEERING_DESIGN_PLAN.md` (396L) + Delivery Report (100L) |
| Preceding Milestone | D-60 UI-009-P06 (113/485 + 414) — UI-009 COMPLETE 8.76.0 |
| Gate / Production | CLOSED / NOT CERTIFIED (unchanged) |
| Distribution | Operator → DA; copy to `docs/plans/` + governance register |

### Independent Review Declaration (Per Amendment §26)

> The ITRGA independently assessed the submitted design plan. DA assertions were not treated as verification without supporting evidence — all 15+1 sections were verified against the governing corpus Tier 1→10. Scope was compared against `ITRGA_REQUEST_UI-010_DESIGN_PLAN.md` and 12 Part VII §12. Implementation approach was compared against 05 v2.0 Presentation Layer + 14 Workspace Shell Regions A–F. No deviations were assessed. Test-count claims (113/485 + 414) were reconciled against D-60. Security boundaries (no actuation, no external LLM, style-injection defense) were independently assessed. Production certification was not inferred. This determination applies only to the design plan and does not authorize implementation beyond the forthcoming P01 Build Order.

**ITRGA STATUS: UI-010 DESIGN PLAN APPROVED WITH OBSERVATIONS (O-010-01). BUILD_ORDER_UI-010-P01 AUTHORIZED.**

**We don't guess. We prove.**

— AXIOM Independent Technical Review & Governance Authority (ITRGA)

