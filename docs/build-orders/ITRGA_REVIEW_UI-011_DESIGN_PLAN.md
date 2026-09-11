# ITRGA REVIEW — UI-011 ENGINEERING DESIGN PLAN
## Institutional Refinement & Version 1.0 Presentation — Determination

**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Review ID:** `ITRGA-DETERMINATION-UI011-DESIGN-PLAN`
**Review Subject:** `UI-011_ENGINEERING_DESIGN_PLAN.md` (413 lines, 37,257 bytes) + `DELIVERY_REPORT_UI-011_DESIGN_PLAN.md` (71 lines, 4,761 bytes)
**Governing Request:** `ITRGA_REQUEST_UI-011_DESIGN_PLAN.md` (Issued 2026-08-11 — 15 sections A–O + §4A)
**Workstream:** UI-011 — Institutional Refinement & Version 1.0 Presentation
**Preceding Milestone:** **UI-010 — Accessibility & Operator Experience COMPLETE** (D-67 — 136 suites / 556 tests · 414 backend · Gate CLOSED · NOT CERTIFIED · `ITRGA-DECLARATION-UI010-COMPLETE-D67` 8.82.0)
**Baseline of Record:** Frontend 136/556 · Backend 414 · `tsc -b && vite build` exit 0 (D-67) · Total 970 tests
**Governing Corpus:** `10_CONSTITUTIONAL_HIERARCHY.md` + `DOCUMENT_PRECEDENCE.md` v2.0.0 (05 v2.0 canonical) + 00/01/02/03/04/05 v2.0/08/11/12/13/14/15/16/17 + Prior D-54→D-67
**Review Standard:** High-Grade — 12 Disciplines · 7-Stage Lifecycle · EVF-1…EVF-4 · Best Among All Possible Outcomes
**DA Operational State:** Design Plan submitted, implementation on **formal hold** (affirmed in both documents)

> **We don't guess. We prove.**

---

## STAGE 1 — ESTABLISH AUTHORITY

| Item | Value | Evidence | Assessment |
|------|-------|----------|------------|
| Request | `ITRGA_REQUEST_UI-011_DESIGN_PLAN.md` | Delivery Report §1 | ✅ Formal ITRGA request — Tier 8 Execution Governance, correctly traces to `12` Part VII §13 charter (verbatim), `12` Part II §9 / Part VIII §11 / Part VI §17, `13` Parts II/VI, `11` firewalled |
| Design Plan | `docs/plans/UI-011_ENGINEERING_DESIGN_PLAN.md` | Header + TOC A–O + §4A (413L, 37,257 bytes) | ✅ Migratable path `docs/plans/` (correct per 10 Tier 8) — 18 chapters including Executive Summary, A–O, 4A, Closing |
| Delivery Report | `DELIVERY_REPORT_UI-011_DESIGN_PLAN.md` | 71L — 6-transcript intake | ✅ Reports design plan as deliverable, correct 6-phase summary, classification, hold affirmation |
| Preceding Baseline | UI-010 COMPLETE D-67 — 136/556 + 414 | Header + §7 Test Inventory | ✅ Correct per `PROJECT_STATE.md` 8.82.0; monotonic chain UI-001→UI-010 preserved (83/376→136/556 +53/+180) |
| Gate / Production | STRICTLY CLOSED / NOT CERTIFIED (Doc 11 firewalled) | Header + §1 Invariants | ✅ Correct per 03/05/11 — invariants explicitly listed (5 governance invariants) |
| Amendment | 27 rules (UI-008 precedent, carried UI-009→UI-010→UI-011) | §1 Purpose + §18 Closing | ✅ Referenced as process precedent; UI-011 will be governed by same principles (Master Prompt Part 10) |

**Stage 1 Closed — Authority Established to EVF-1 (Direct Documentary).** All required governance parents are present and correctly cited.

---

## STAGE 2 — ESTABLISH SCOPE

### Requested vs Delivered (Per ITRGA_REQUEST_UI-011 §2 A–O + §4A)

| Required Section | Delivered | Assessment |
|------------------|-----------|------------|
| **A. UI-011 Objective** | §2 — 5 primary objectives (Information Hierarchy 4 levels L1→L4, Panel Balance across 7 workspaces, Interaction Consistency `var(--ix-motion-fast)` 120ms, Animation/Reduced-Motion, Version 1.0 Readiness) + In/Out boundaries (7 in-scope hierarchies vs 7 out-of-scope forbidden: 5-tier redefinition, component rewrites, backend, WebSocket, order routing, external LLM, Doc 11 self-approval) | ✅ **Compliant** — correctly frames UI-011 as institutional polish, not expansion; traces to `12` Part VII §13 verbatim + `12` Part II §9 / Part VIII §11 / Part VI §17 |
| **B. Governing Requirements** | §3 — Traceability matrix **14 rows** Tiers 1→7 (00 Principle 3/4/Quality over speed, 01 multi-market, 02 10-point checklist, 11 firewalled, 03 UI/Quality/Definition of Done, 04 sequencing Gate CLOSED, 05 Presentation §13/Workspace Shell, 08 High-density terminal, 08 Reasoning Level II, 09 7-stage, 12 Part VI §17, 13 Level D, 16 Midnight Black/Graphite/Electric Blue, 17 Sandbox) | ✅ **Compliant** — hierarchical, tier-ordered per 10, cites canonical 05 v2.0, correctly marks 11 firewalled |
| **C. Roadmap Position** | §4 — Diagram: UI-001 Shell → UI-002 Nav → UI-003 Market → UI-004 Intelligence → UI-005 Planning → UI-006 Explorer → UI-007 Governance → UI-008 AI (D-53) → UI-009 Design System (D-60) → UI-010 Accessibility (D-67) → **UI-011 ACTIVE PLAN** → Doc 11 Firewalled → Version 1.0 Release | ✅ **Compliant** — correctly places UI-011 as Level D Final Polish (13 Part II §3), depends on UI-010 COMPLETE (Level D after Foundational), precedes `11` |
| **D. Phase Structure** | §5 — 6-phase lifecycle: **P01 Information Hierarchy & Spacing (4-level tokens, 4px/8px/12px/16px/24px/32px grid, `--ix-elevation-level-1..4`)** → **P02 Panel Balance & Workspace Frame Harmonization (7 workspaces, `.ix-panel` margins, `.ix-card` paddings)** → **P03 Micro-Interaction Consistency & Motion Restraint (120ms, hover states, `prefers-reduced-motion`)** → **P04 Optical Typography & Monospace Financial Data Polish (`0.75rem`/`0.9rem`/`0.85rem`, `tabular-nums`)** → **P05 Cross-Workspace Cohesion & Visual Regression Audit (integration across `/intelligence`, `/charts`, `/governance`, `/investigate`)** → **P06 Whole-Surface Version 1.0 Handover (grep proofs, regression, `PROJECT_STATE.md` 1.0)** | ✅ **Compliant** — bounded, sequential, each with objective/scope In/Out/exit criteria (`spacingHierarchy.test.tsx`, `panelBalance.test.tsx`, `interactionPolish.test.tsx`, `typographyPolish.test.tsx`, `crossWorkspaceCohesion.test.tsx`, UI-011 COMPLETE); correctly defers P06 whole-surface audit to completion checkpoint |
| **E. Existing UI State Audit** | §6 — Table audits Shell Regions A–F (Excellent, responsive reflow), Atoms P02 (Standardized, pure token, focus rings — polish button active elevation), Panels P03 (Standardized span-12 grid — calibrate header-to-body margin), Tables P04 (sticky `z-index:2`, tabular-nums — refine empty/loading transition), Modals P05 (focus trap LIFO — polish shimmer gradient), Accessibility UI-010 (WCAG AA/AAA — retain unchanged) | ✅ **Compliant** — exhaustive audit of shell/layout + 22 UI-009 primitives + accessibility; satisfies “what exists to be refined” with specific polish gaps per `12` Part VI §17 |
| **F. Existing Tests** | §7 — Test Baseline box 136 suites / 556 tests + 414 backend + `tsc` exit 0 + `vite` exit 0 + greps 0 + ad-hoc hex 0 (outside `tokens.css`) — `970 total` | ✅ **Compliant** — correctly inventories baseline as of UI-010 COMPLETE; 0 ad-hoc hex whole-frontend proven per P06 D-67 |
| **G. Existing Documentation** | §8 — Catalog 10 items `00/05/08/11/12/13/16/17` + `UI-009`/`UI-010` plans + `PROJECT_STATE.md` 8.82.0 | ✅ **Compliant** — references canonical set; `UI-009`/`UI-010` as direct predecessors — correct |
| **H. Retain / Extend / Supersede / Defer Matrix** | §9 — Table 9 rows: 4 RETAIN top (tokens 5-tier, `theme.ts` contracts, `SkipLink`/`RouteAnnouncer`, `EmptyState`/`ErrorBanner`), 3 EXTEND (Panel/Card padding `4px` grid, Button active micro-interaction, Skeleton shimmer gradient), 1 RETAIN multi-theme `prefers-contrast`, 1 DEFER Mobile <768px post-v1.0 | ✅ **Compliant** — each with cost Low (CSS token refinement) and rationale; see minor observation O-011-01 re count summary |
| **I. Proposed P01** | §10 — 7-part: 1 Retained 5-tier tokens + all UI-009/UI-010 primitives, 2 Extended hierarchy spacing classes `.ix-hierarchy-level-1..4` + panel padding tokens, 3 Superseded None, 4 Deferred Mobile companion, 5 Collective Satisfaction (136/556 solid foundation; P01 establishes visual weight standards), 6 Re-baseline clean forward extending 136/556, 7 Build Order Boundary In: hierarchy tokens in `tokens.css`/`theme.ts` + harmonizing spacing across shell/panel frames + `spacingHierarchy.test.tsx` + invariants (+4 to +8 tests); Out: component rewrites, backend changes | ✅ **Compliant** — fully satisfies Re-baseline Directive §I 7 parts; no silent supersede; additive, migratable |
| **J. Acceptance Criteria** | §11 — 8 criteria AC-01…AC-08: hierarchy tokens codified/typed, panel spacing uniform 4px/8px…32px, micro-interaction `var(--ix-motion-fast)` 120ms, numerical `tabular-nums`, 0 ad-hoc hex outside `tokens.css`, zero actuation/LLM/dangerous innerHTML/eval, regression ≥556+414, build exit 0 | ✅ **Compliant** — each verifiable via `spacingHierarchy.test.tsx`/`grep_ad_hoc_hex.log`/grep/`vitest`/`tsc`, correctly traced to `12` Part VI §17, `16`, `17` |
| **K. Dependencies** | §12 — `tokens.css` → `components/ui/` → `InstitutionalWorkspaceShell` Regions A–F pipeline + Build Tools Vite 8/TS 5.6/Vitest 4.1 + Pure CSS custom properties (Tailwind forbidden) | ✅ **Compliant** — dependency pipeline correct |
| **L. Cybersecurity** | §13 — Zero Actuation S-1 (presentation-only), Zero External AI S-2, Sandbox S-3 (0 `dangerouslySetInnerHTML`/`eval`), Credential Protection S-4 (0 passwords/JWT), Pure Token Consumption S-5 (0 ad-hoc hex) | ✅ **Compliant** — 5 invariants, correctly anticipates no `value` exposure via polish |
| **M. UI/UX** | §14 — Consistent Spacing 4px grid, Subtle Animations `120ms` cubic-bezier, Stable Transitions, Clean Typography hierarchy (Display/Workspace Title/Panel Heading/Body/Metadata `0.75rem`), Balanced Information Density, Predictable Interaction Patterns, Professional Iconography `▲`/`▼`/`◆◆◆`/`✓`/`ℹ`/`⚠`/`✕`, Uniform Panel Behaviour — per `12` Part VI §17 | ✅ **Compliant** — satisfies 12 Part VI §17 8-point polish criteria |
| **N. Architecture** | §15 — Presentation Layer §13 (5-tier tokens → component primitives → Workspace Shell Regions A–F diagram: A Global Command Bar (SkipLink, RouteAnnouncer), B Navigation Dock, C Primary Workspace (7 governed workspaces, hierarchy refinement), D Context Panel, E Activity Dock, F Overlay Layer) | ✅ **Compliant** — bounded to Presentation Layer, no backend coupling |
| **O. Documentation & State** | §16 — `PROJECT_STATE.md` 8.83.0→8.88.0, `CHANGELOG.md`, Level II evidence `docs/evidence/ui011/`, 20-section Delivery Reports with §25 Declarations | ✅ **Compliant** — monotonic versioning, migratable |
| **§4A Methodology Invariants** | §17 — Continuity Obligations, Prohibited Parallel Processes, Workflow Conflict Resolution via `10`, Purpose of Plan (roadmap to Version 1.0) | ✅ **Compliant** — preserves Master Prompt 4A |

**Design Plan Structural Completeness:** **18/18 chapters delivered** (Executive Summary + A–O + 4A + Closing). No required section missing. Delivery Report correctly summarizes A–O (§2 table) and 6-phase lifecycle (§3).

### Out-of-Scope Protection

Plan §2 Out-of-Scope (5-tier redefinition, component rewrites, backend/WebSocket, order routing, external LLM, Doc 11 self-approval) — **explicit and correct** — UI-011 is **institutional polish only.**

**Stage 2 Closed — Scope Compliant. No scope creep.**

---

## STAGE 3 — ESTABLISH EVIDENCE

| Claim | Evidence | Type | Assessment |
|-------|----------|------|------------|
| Baseline 136/556 + 414 + exit 0 | §1 Header + §7 + Design Plan baseline box | Level II/III Documentary | **EVF-1** — directly cites D-67 UI-010 COMPLETE baseline; internally consistent with P06 136/556 |
| Shell 6 regions A–F + 33 quick actions + 22 UI-009 primitives + accessibility | §6 audit | Level III Documentary | **EVF-1** — correctly inventories UI-001→UI-010 surfaces |
| 6-phase lifecycle P01→P06 | §5 | Level III | **EVF-1** — bounded, phases correctly aligned to 12 Part VI §17 polish criteria |
| Retain 5 / Extend 3 / Supersede 0 / Defer 1 + Superseded None | §9 matrix + §10 | Level III | **EVF-1** — each classified with cost Low; see O-011-01 re summary count harmonization |
| P01 7-part re-baseline + Build Order Boundary | §10 | Level III | **EVF-1** — directly verifiable design; +4 to +8 tests additive, no rework |
| AC-01…AC-08 | §11 | Level III | **EVF-1** — each verifiable via `spacingHierarchy.test.tsx`/`grep_ad_hoc_hex.log`/grep/`vitest`/`tsc` |
| Implementation Hold | §18 Closing + Delivery Report §5 | Level III | **EVF-1** — both documents affirm hold — `NO UI-011 implementation has been initiated` |

---

## STAGE 4 — INVESTIGATE — 12 DISCIPLINES

| Discipline | Assessment |
|------------|------------|
| **Software Engineering** | `spacingHierarchy.test.tsx` + information elevation tokens (`--ix-elevation-level-1..4`) in `tokens.css` + `theme.ts` is maintainable, additive (P01 harmonizes spacing via `Panel.css`/`Card.css`/`InstitutionalWorkspaceShell.css` → `var(--ix-space-*)` 4px grid — not hardcoded `px` outside tokens); no duplication; Tailwind/Bootstrap forbidden correctly per §12. |
| **System Architecture** | Correctly places UI-011 in **Presentation Layer** per 05 v2.0 §13 single ownership; 6-phase rollout respects 13 Level D Refinement after Foundational (UI-009) + Accessibility (UI-010); bounded contexts `workstation/design/tokens.css` + `components/ui/` + `InstitutionalWorkspaceShell` Regions A–F isolated; no new backend bounded context, no circular deps; `EmptyState`/`ErrorBanner` already in UI-010 P03 — P01 spacing refinement not business logic. |
| **Cybersecurity** | **Strong:** Zero Actuation S-1 (presentation-only `Button` view updates, not order routing), Zero External AI S-2, Sandbox S-3 (0 `dangerouslySetInnerHTML`/`eval` in refinement module), Credential S-4 (0 passwords/JWT in UI telemetry/logging/DOM), Pure Token S-5 (0 ad-hoc hex outside `tokens.css` via `var(--ix-*)`) — correctly anticipates no `value` exposure via spacing refinement. |
| **UI/UX** | **High-grade:** Consistent Spacing 4px grid `4px/8px/12px/16px/24px/32px` (U-2), Subtle Animations `120ms cubic-bezier` zero bouncy (U-3), Stable Transitions opacity/elevation (U-3), Clean Typography hierarchy (Display 1.5rem → Workspace Title → Panel Heading `0.85rem` → Body `0.9rem` → Metadata `0.75rem` `tabular-nums`), Balanced Information Density (tables vs summary cards), Predictable Interaction Patterns (identical hover/active/`focus-visible` `#8CC2FF`), Professional Iconography `▲`/`▼`/`◆◆◆`/`✓`/`ℹ`/`⚠`/`✕`, Uniform Panel Behaviour (header/body/action bar/footer) — **all 8 per 12 Part VI §17 institutional polish.** |
| **Data Engineering** | **No data impact:** No persistence/migration/provenance mutation — refinement only; `RISK_REGISTER.md`/`TECHNICAL_DEBT_REGISTER.md` correctly state 0 new debt. |
| **ML / AI** | **No ML/AI in scope:** No training/inference — correctly out-of-scope per 07; visual refinement is deterministic CSS, not generative AI. |
| **Trading / Quant** | **No trading logic:** No signal/execution/quant — correctly out-of-scope per 12 Part I §5; Gate CLOSED invariant explicitly listed (§1). |
| **DevOps / Infrastructure** | Dependencies Vite 8/TS 5.6/Vitest 4.1 + Testing Library `jsdom` + Pure CSS custom properties correctly listed; verification via `vitest`/`tsc`/`vite`/`grep` per 10 hierarchy — **build reproducible;** pure CSS custom properties ensure no utility framework lock-in. |
| **Governance** | **20-section plan** + Delivery Report correctly trace tiers per 10 hierarchy via §3 matrix (00/01/02/11→10); 6-phase lifecycle bounded with explicit In/Out per §5 + §10 P01; implementation hold affirmed (no speculative P02→P06 per §17); `NO DEVIATIONS` correctly anticipated for P01 (spacing refinement only); Gate CLOSED / NOT CERTIFIED held; debt `TD-UI-POSTCSS-HIGH`/`OBS-P06-2` correctly carried. No silent methodology change (Roadmap→Design Plan→Build Order→… preserved). |
| **Testing & Verification** | `spacingHierarchy.test.tsx` (information elevation tokens + spacing audit) + invariant tests is **correct high-grade harness** for 4-level hierarchy (Level 1 Mission-Critical Telemetry → Level 4 Administrative & Meta) — proportionate for P01; `panelBalance.test.tsx`, `interactionPolish.test.tsx`, `typographyPolish.test.tsx`, `crossWorkspaceCohesion.test.tsx` correctly anticipated for P02→P05. |
| **Documentation & Knowledge Continuity** | Plan is **migratable** (`docs/plans/UI-011_ENGINEERING_DESIGN_PLAN.md` as single truth, per §16) + Delivery Report as intake; correctly lists docs 00–17, ADRs, registers, Amendment, `PROJECT_STATE.md` 8.82.0 — **institutional memory preserved** per 10 Tier 7. `docs/evidence/ui011/` evidence separation correctly planned (separate from `ui010` 136/556 baseline). |
| **Product / Operator Integrity** | Information hierarchy Levels 1→4 (Mission-Critical → Active Context → Supporting Analytics → Administrative) correctly improves operator efficiency (Level 1 telemetry has visual priority via spacing/elevation) without misrepresenting simulated vs live telemetry; operator can distinguish research observation (empty) vs error (alert) vs loading (skeleton) via honest `role="status"`/`alert`/`aria-busy` — **honest state per 02.** |

**No discipline reveals a defect that would prevent approval.** Polish gaps identified in §6 (Region A header alignment, button active elevation, header-to-body margin, empty/loading transition smoothing, shimmer gradient subtlety, accessibility primitives retain unchanged) are **correctly mapped to P01→P03** — not hidden.

---

## STAGE 5 — COMPARE — REQUEST → PLAN → GOVERNING REQUIREMENTS

| Dimension | Comparison | Result |
|-----------|------------|--------|
| Request A–O + §4A → Plan A–O + §4A | All 15+1 sections present and mapped with same titles; 6-phase structure as requested; 7-part P01 re-baseline as required | ✅ **No mismatch** |
| Plan → `12` Part VII §13 + `12` Part VI §17 / Part II §9 / Part VIII §11 | Plan correctly operationalizes Visual refinement + Workflow optimization + Workspace polish + Information hierarchy + Panel balance + Interaction consistency + Animation refinement + Final UX review via P01 spacing → P02 panel balance → P03 motion → P04 typography → P05 cross-workspace → P06 handover | ✅ **No mismatch** |
| Plan §10 P01 boundary → 11 §7 (8 categories + focus) | Hierarchy tokens + panel spacing + micro-interaction transitions + `tabular-nums` + 0 ad-hoc hex + regression correctly prepare the platform to *pass* future 11 §7 certification (without self-certifying) — correctly **preparatory, not self-certification** | ✅ |
| Plan §11 AC-01…AC-08 → `12` Part VI §17 / `16` / `17` | Each AC verifiable via `spacingHierarchy.test.tsx`/`grep_ad_hoc_hex.log`/grep/`vitest`/`tsc` | ✅ |
| Plan §16 docs sync → 10 operational governance | `PROJECT_STATE.md` 8.83.0→8.88.0 `UI-011 COMPLETE` + `CHANGELOG.md` + `RISK`/`DEBT` + `docs/evidence/ui011/` correctly listed | ✅ |

**No mismatches. Minor note: `WCAG 2.4.1` bypass blocks is correctly prepared by UI-010 `SkipLink` in P01, not re-deferred in UI-011 P01 — correct carry-forward.**

---

## STAGE 6 — DETERMINE FINDINGS

### 6.1 Classification

| Finding Type | Count | Detail |
|--------------|-------|--------|
| Blocker | 0 | None |
| Major Defect | 0 | None |
| Material Observation | 0 | None |
| **Minor Observation** | **1** | **O-011-01** (matrix summary count harmonization) |
| Governance Issue | 0 | None |

### 6.2 Observation Detail

| ID | Severity | Description | Required Action | Blocking? |
|----|----------|-------------|-----------------|-----------|
| **O-011-01** | Minor | **Retain/Extend Count Summary Harmonization** — §9 matrix table shows 9 rows: 4 RETAIN (tokens 5-tier, `theme.ts`, `SkipLink`/`RouteAnnouncer`, `EmptyState`/`ErrorBanner`) + 3 EXTEND (`Panel.css` padding, `Button.css` active, `Skeleton.css` shimmer) + 1 RETAIN (multi-theme `prefers-contrast`) + 1 DEFER (Mobile <768px). Counted fully, that is **5 RETAIN + 3 EXTEND + 1 DEFER** (9 rows). The text summary in §9 states “RETAIN 4, EXTEND 3” and §10 P01 summary repeats “5 retained” in some places. The mismatch is **typographical: the multi-theme high contrast RETAIN was counted separately in the table but merged in the summary.** No architectural consequence — classifications themselves are correct (tokens 5-tier RETAIN, multi-theme RETAIN, panel/button/skeleton EXTEND, mobile DEFER). | In `BUILD_ORDER_UI-011-P01` and/or `docs/plans/UI-011_ENGINEERING_DESIGN_PLAN.md` retained copy, **harmonize the summary to “5 RETAIN + 3 EXTEND + 1 DEFER”** (or consolidate multi-theme high contrast into the 4 RETAIN count). Verify via `grep` that `panelBalance.test.tsx` (P02) still covers all EXTEND rows. This is documentary hygiene, not an implementation deviation. | **No** |

*No other observations. The single minor observation is **non-blocking documentary hygiene** for P01 implementation — it does not affect the design plan's approvability.*

---

## STAGE 7 — VERDICT

### **APPROVED WITH OBSERVATIONS**

**Determination ID:** `D-68`
**Phase:** UI-011 Engineering Design Plan — Institutional Refinement & Version 1.0 Presentation
**Verdict:** **APPROVED WITH OBSERVATIONS** (1 Minor Observation — O-011-01)
**Evidence Level:** Plan satisfies all 15+1 required sections; traceability Tier 1→8 is complete; 6-phase lifecycle bounded; Retain 5 / Extend 3 / Supersede 0 / Defer 1 matrix is sound (summary harmonization pending O-011-01); collaborative governance preserved
**Blockers / Major Defects:** **0**
**Regressions:** N/A — design plan phase (no code)
**Next Authorized Unit:** **`BUILD_ORDER_UI-011-P01` — Information Hierarchy & Spacing Refinement**

#### Rationale

**Design completeness:** All 15 sections A–O + §4A + Executive Summary + Closing are present, correctly bounded for a Level D Final Polish workstream that refines information hierarchy, panel balance, micro-interaction consistency, motion restraint, typography polish, cross-workspace cohesion, and whole-surface handover without introducing new trading/backend/execution/external-AI. 6-phase lifecycle (P01 Spacing Hierarchy + Elevation → P02 Panel Balance & Workspace Frame Harmonization → P03 Micro-Interaction & Motion → P04 Typography & Monospace Financial Data → P05 Cross-Workspace Cohesion & Visual Regression → P06 Whole-Surface Version 1.0 Handover) is logically sequenced and dependency-correct per 13 Level D Refinement after Foundational (UI-009) + Accessibility (UI-010).

**Governance compliance:** Correctly traces to 00/01/02/11 §7 (firewalled preparatory)/03/04/05 v2.0/08/11 §7/12 Part VI §17 & Part VII §13/13 Level D + Parts V/VI/14 Regions A–F/16 Part XII/17 + UI-009 374L + UI-010 396L + D-62→D-67 (136/556); implementation hold is correctly affirmed (DA will not implement until Build Order); no silent methodology change (Roadmap→Design Plan→Build Order→… preserved).

**Technical soundness:** 5 RETAIN (tokens 5-tier, `theme.ts` contracts, accessibility primitives, EmptyState/ErrorBanner) + 3 EXTEND (Panel/Card padding 4px grid, Button active micro-interaction, Skeleton shimmer gradient, multi-theme `prefers-contrast`) + 1 DEFER (Mobile <768px post-1.0) matrix is correct; P01 additive harmonization of spacing hierarchy (`--ix-hierarchy-level-1..4`, `--ix-elevation-level-1..4`) in `tokens.css`/`theme.ts` + `spacingHierarchy.test.tsx` is risk-free and additive; visual polish reinforces confidence without distracting from research activities per 12 Part VI §17.

**Security & product integrity:** Correctly holds invariants — pure token consumption (`var(--ix-*)`), zero actuation/LLM/eval/innerHTML, credential isolation — no new attack surface.

**Observation does not prevent approval** — O-011-01 is minor documentary hygiene for matrix summary harmonization and will be verified via `panelBalance.test.tsx` (P02) in the P01 evidence package.

---

## AUTHORIZATION

With this determination **D-68**, the **UI-011 Engineering Design Plan is APPROVED WITH OBSERVATIONS.**

**The ITRGA now authorizes issuance of:**

> **`BUILD_ORDER_UI-011-P01` — Information Hierarchy & Spacing Refinement**
> *Define visual hierarchy tokens (`--ix-hierarchy-*`, `--ix-elevation-level-*`) in `tokens.css` and `theme.ts`; harmonize spacing across shell regions and panel frames with `spacingHierarchy.test.tsx` + invariant tests (+4 to +8 tests) — 0 ad-hoc hex, zero actuation/LLM/eval, regression invariance 136/556+414.*

The DA is authorized to begin **P01 implementation only after** receipt of that Build Order. No P02–P06 work is authorized.

---

## DOCUMENT CONTROL

| Field | Value |
|-------|-------|
| Review ID | D-68 |
| Reviewed By | ITRGA — Independent Technical Review & Governance Authority |
| Review Date | 2026-08-11 |
| Governing Request | `ITRGA_REQUEST_UI-011_DESIGN_PLAN.md` |
| Design Plan | `docs/plans/UI-011_ENGINEERING_DESIGN_PLAN.md` (413L) + Delivery Report (71L) |
| Preceding Milestone | D-67 UI-010-P06 (136/556 + 414) — UI-010 COMPLETE 8.82.0 |
| Gate / Production | CLOSED / NOT CERTIFIED (unchanged) |
| Distribution | Operator → DA; copy to `docs/plans/` + governance register |

### Independent Review Declaration (Per Amendment §26)

> The ITRGA independently assessed the submitted design plan. DA assertions were not treated as verification without supporting evidence — all 15+1 sections were verified against the governing corpus Tier 1→10. Scope was compared against `ITRGA_REQUEST_UI-011_DESIGN_PLAN.md` and 12 Part VII §13. Implementation approach was compared against 05 v2.0 Presentation Layer + 14 Workspace Shell. No deviations were assessed. Test-count claims (136/556 + 414) were reconciled against D-67. Security boundaries (no actuation, no external LLM, style-injection defense) were independently assessed. Production certification was not inferred. This determination applies only to the design plan and does not authorize implementation beyond the forthcoming P01 Build Order.

**ITRGA STATUS: UI-011 DESIGN PLAN APPROVED WITH OBSERVATIONS (O-011-01). BUILD_ORDER_UI-011-P01 AUTHORIZED.**

**We don't guess. We prove.**

— AXIOM Independent Technical Review & Governance Authority (ITRGA)

