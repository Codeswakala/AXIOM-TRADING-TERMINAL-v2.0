# ITRGA REVIEW — UI-009 ENGINEERING DESIGN PLAN
## Institutional Design System Implementation — Determination

**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Review ID:** `ITRGA-DETERMINATION-UI009-DESIGN-PLAN`
**Review Subject:** `UI-009_ENGINEERING_DESIGN_PLAN.md` (374 lines, 29,239 bytes) + `DELIVERY_REPORT_UI-009_DESIGN_PLAN.md` (91 lines, 6,698 bytes)
**Governing Request:** `ITRGA_REQUEST_UI-009_DESIGN_PLAN.md` (Issued 2026-08-10 — 15 sections A–O + §4A)
**Workstream:** UI-009 — Institutional Design System Implementation
**Preceding Milestone:** UI-008 — Institutional AI Experience **COMPLETE** (D-53 — 83 suites / 376 tests · 414 backend · Gate CLOSED · NOT CERTIFIED)
**Baseline of Record:** Frontend 83/376 · Backend 414 · `tsc -b && vite build` exit 0 (D-53)
**Governing Corpus:** `10_CONSTITUTIONAL_HIERARCHY.md` + `DOCUMENT_PRECEDENCE.md` v2.0.0 (05 v2.0 canonical) + 00/02/03/04/05 v2.0/08/11/12/13/14/15/16/17 + Prior D-50→D-53
**Review Standard:** High-Grade — 12 Disciplines · 7-Stage Lifecycle · EVF-1…EVF-4 · Best Among All Possible Outcomes
**DA Operational State:** Design Plan submitted, implementation on **formal hold** (affirmed in both documents)

> **We don't guess. We prove.**

---

## STAGE 1 — ESTABLISH AUTHORITY

| Item | Value | Evidence | Assessment |
|------|-------|----------|------------|
| Request | `ITRGA_REQUEST_UI-009_DESIGN_PLAN.md` | Delivery Report §1 | ✅ Formal ITRGA request — Tier 8 Execution Governance, correctly traces to 12 Part VII §11 + 13 Part V |
| Design Plan | `docs/plans/UI-009_ENGINEERING_DESIGN_PLAN.md` | Header + TOC A–O + §4A | ✅ Migratable path `docs/plans/` (correct per 10 Tier 8) — 18 chapters including Executive Summary, A–O, 4A, Closing |
| Delivery Report | `DELIVERY_REPORT_UI-009_DESIGN_PLAN.md` | 91 lines | ✅ Reports design plan as deliverable, correct 6-phase summary, classification, hold affirmation |
| Preceding Baseline | UI-008 COMPLETE D-53 — 83/376 + 414 | Header + §7 + §4 Previous Baseline | ✅ Correct per `PROJECT_STATE.md` 8.70.0; monotonic chain UI-001→UI-008 preserved |
| Gate / Production | CLOSED / NOT CERTIFIED (11 firewalled) | Header | ✅ Correct — no Gate opening implied |
| Amendment | 27 rules (UI-008 precedent) | §8/G §3 | ✅ Referenced as process precedent; UI-009 will be governed by same principles (Master Prompt Part 10) |

**Stage 1 Closed — Authority Established to EVF-1 (Direct Documentary).** All required governance parents are present and correctly cited.

---

## STAGE 2 — ESTABLISH SCOPE

### Requested vs Delivered (Per ITRGA_REQUEST_UI-009 §2 A–O + §4A)

| Required Section | Delivered | Assessment |
|------------------|-----------|------------|
| **A. UI-009 Objective** | §2 — traces to `12` Part VII §11 (“Apply Design System…”) + `13` Part V 3-stage rollout; explains Level A Foundational + Level D Refinement sequencing after UI-008 | ✅ **Compliant** — correctly frames UI-009 as harmonization, not expansion |
| **B. Governing Requirements** | §3 — Traceability matrix 13 rows Tiers 1→8 (00 Principle 2/3/4, 02 dark-first, 11 §7 WCAG, 03 Definition of Done, 04 sequencing, 05 Part I §8/§13 Presentation ownership, 08 modular, 08 Reasoning, 12 Part V/VII, 13 Part IV/V, 16 brand palette + `/branding`, 17 style-injection, Amendment 27 rules) | ✅ **Compliant** — hierarchical, tier-ordered per 10, cites canonical 05 v2.0 |
| **C. Roadmap Position** | §4 — Diagram: UI-001→UI-008 predecessors → UI-009 ACTIVE (P01→P06) → UI-010/UI-011 + 11 Certification successors | ✅ **Compliant** — correctly places UI-009 as bridge Foundational → Refinement, dependencies per 13 Level A |
| **D. Phase Structure** | §5 — 6-phase lifecycle: P01 Tokens → P02 Atomic Library (Button/Input/Select/Badge/Card/StatusChip/Tooltip/Accordion) → P03 Panel Frames → P04 Tables/Grids → P05 Modals/Overlays/Feedback → P06 Whole-Surface Audit/CK | ✅ **Compliant** — bounded, sequential, each with title/scope/boundary; minimizes rework per 13 dependency |
| **E. Existing UI State Audit** | §6 — 6 workstation regions (A–F), `Ctrl+K` 33 commands, `tokens.css` baseline, UI-003→UI-008 surfaces listed (Market, Research, Investigation, Explorer, Governance, AI surfaces), `/branding` asset | ✅ **Compliant** — audit of shell/layout + all workspace surfaces + brand assets; satisfies “what exists to be unified” |
| **F. Existing Tests** | §7 — 83/376 frontend (81.56s) + 414 backend (114.98s) + `tsc` exit 0 + zero actuation/LLM greps (D-53) | ✅ **Compliant** — correct baseline, not invented |
| **G. Existing Documentation** | §8 — Catalog of Doc 12,13,16,08,05,17, Amendment, PROJECT_STATE 8.70.0 | ✅ **Compliant** — references canonical set; 00/03/10 not listed in this table but covered in §3 matrix — acceptable |
| **H. Retain/Extend/Supersede/Defer Matrix** | §9 — Table 9 rows: 3 RETAIN (Shell, UncertaintyBadge, LineageTree), 5 EXTEND (tokens.css, theme.ts, NavigationDock, Command Palette, panel headers), 1 SUPERSEDE (ad-hoc inline hex → CSS variables), 1 DEFER (multi-monitor splitter post-v1.0) | ✅ **Compliant** — each with technical/governance rationale + implementation impact; summary 3-5-1-1-0 correct |
| **I. Proposed P01** | §10 — 7-part: 1 Retained `:root` + `theme.ts` roles, 2 Extended 5-tier hierarchy + brand palette (6 colors) + typography/spacing/elevation, 3 Superseded disorganized `--ix-*` prefix, 4 Deferred theme customizer, 5 Collective Satisfaction (baseline foundation + need for formal hierarchy), 6 Re-baseline Determination (clean continuation from D-53, additive), 7 Build Order Boundary (P01 In: tokens.css 5-tier + theme.ts contracts + `tokens.test.ts` contrast; Out: no workspace rewrites, no backend/DB) | ✅ **Compliant** — fully satisfies Re-baseline Directive §I 7 parts; no silent supersede; additive, migratable |
| **J. Acceptance Criteria** | §11 — 8 criteria AC-01…AC-08: 5-tier architecture, brand fidelity, contrast >4.5:1, no color-alone, zero actuation/LLM greps, style-injection safety (0 `dangerouslySetInnerHTML`/`eval`), regression invariance (376+414) | ✅ **Compliant** — each verifiable via Level I/II, traced to 12/08/02/03/05/17/08/Amendment |
| **K. Dependencies** | §12 — Technical (React 18/TS5/Vite/Vitest/CSS3 vars), Architectural (`frontend/src/workstation/design/`), Predecessors UI-001→UI-008 COMPLETE, Brand 16, Security 17, Governance ITRGA Build Order | ✅ **Compliant** |
| **L. Cybersecurity** | §13 — Static CSS custom properties (no runtime interpolation), `.ix-*` CSS isolation, credential isolation, immutable invariants (actuation/LLM greps every phase) per 17 Part X | ✅ **Compliant** |
| **M. UI/UX** | §14 — Dark-first `#0B0E14`/`#1A1F2C`/`#2563EB`, density, motion `120ms` + `prefers-reduced-motion`, WCAG 2.1 AA contrast >4.5:1 (>3:1 large), focus `--ix-color-focus: #8CC2FF`, keyboard Tab/Enter/Space/Escape | ✅ **Compliant** — satisfies 08 + 16 |
| **N. Architecture** | §15 — 5-tier hierarchy diagram: T1 Foundation (primitive hex/base grid/fonts) → T2 Semantic (role tokens) → T3 Component (scoped) → T4 Workspace (domain contexts) → T5 Theme Overrides (`.theme-light`) | ✅ **Compliant** — correctly formalizes 14 Part VI token hierarchy |
| **O. Documentation & State** | §16 — PROJECT_STATE.md, CHANGELOG.md, RISK/DEBT, `docs/plans/UI-009…` as migratable truth | ✅ **Compliant** |
| **§4A Methodology Invariants** | §17 — No Silent Methodology Change (Roadmap→Design Plan→Build Order→Implementation→…), No Parallel Processes, Traceable Continuity to `docs/evidence/ui009/` | ✅ **Compliant** — preserves Master Prompt 4A |

**Design Plan Structural Completeness:** **18/18 chapters delivered** (Executive Summary + A–O + 4A + Closing). No required section missing. Delivery Report correctly summarizes A–O (§2) and confirms hold.

### Out-of-Scope Protection

Plan §10 P01 Out-of-Scope (no workspace rewrites, no backend/DB) + §18 Closing (“No new backend endpoints, trading capabilities, or business logic”) and §12 Scope Boundaries per 12 Part I §5 are **explicit and correct** — UI-009 is **presentation-layer unification only**.

**Stage 2 Closed — Scope Compliant. No scope creep.**

---

## STAGE 3 — ESTABLISH EVIDENCE

| Claim | Evidence | Type | Assessment |
|-------|----------|------|------------|
| Baseline 83/376 + 414 + exit 0 | §7 + Header + Delivery Report baseline | Level II/III Documentary | **EVF-1** — directly cites D-53 approved baseline; internally consistent with P06 83/376 |
| Shell 6 regions + 33 commands + tokens.css + brand asset | §6 audit | Level III Documentary | **EVF-1** — correctly inventories `UI-001/UI-002` infrastructure + UI-003→UI-008 surfaces |
| 6-phase lifecycle P01→P06 | §5 | Level III | **EVF-1** — bounded, phase titles match `13` rollout |
| Retain 3 / Extend 5 / Supersede 1 / Defer 1 | §9 matrix | Level III | **EVF-1** — each classified with rationale |
| P01 5-tier hierarchy + brand palette 6 colors | §10 + §15 | Level III | **EVF-1** — directly verifiable design |
| AC-01…AC-08 | §11 | Level III | **EVF-1** — each verifiable via grep/vitest/axe/contrast |
| Implementation Hold | §18 Closing + Delivery Report §4 | Level III | **EVF-1** — both documents affirm hold |

---

## STAGE 4 — INVESTIGATE — 12 DISCIPLINES

| Discipline | Assessment |
|------------|------------|
| **Software Engineering** | Plan correctly treats tokens as **primitive constants** (`--ix-*`), not runtime logic; P01 additive codification in `tokens.css` + `theme.ts` TypeScript contracts + `tokens.test.ts` audit is maintainable, modular, and testable. No new dependencies beyond CSS3 vars + existing React/TS/Vite. High cohesion (design tokens isolated in `frontend/src/workstation/design/`). |
| **System Architecture** | Correctly places UI-009 in **Presentation Layer** per 05 v2.0 §13 single ownership; 6-phase rollout respects 13 Parts II dependency (P01 tokens → P02 atoms → P03 panels → P04 tables → P05 overlays → P06 audit) and 14 Part VI token hierarchy (Foundation→Semantic→Component→Workspace→Theme). No circular deps, no backend coupling, no broker logic — **preserves 05 layered flow.** |
| **Cybersecurity** | **Strong:** Static CSS custom properties (no runtime string interpolation), `.ix-*` namespace scoping prevents global pollution, credential isolation (tokens = visual only), style-injection defense (0 `dangerouslySetInnerHTML`/`eval`/`<script>`) per 17 Part X, plus actuation/LLM grep invariants every phase per §13. Sandboxed Markdown precedent from UI-008 P05 carries forward. |
| **UI/UX** | Dark-first `#0B0E14`/`#1A1F2C`/`#2563EB` + semantic Green/Amber/Red (16), typography scale 1.5rem→0.75rem, 4px grid (`--ix-space-1` 4px→`--ix-space-8` 32px), motion `120ms` with `prefers-reduced-motion` — **institutional, information-dense, restrained** per 08. Contrast >4.5:1 + >3:1 large + focus `#8CC2FF` + keyboard Tab/Enter/Space/Escape satisfies **WCAG 2.1 AA** per 08 §Accessibility + 11 §7. No color-alone encoding (retained `UncertaintyBadge` text+`◆◆◆`+`%` pattern). |
| **Data Engineering** | **No data impact:** No persistence schema, no migrations, no provenance mutation — presentation-token only. Correctly notes no dataset changes. |
| **ML / AI** | **No ML/AI in scope:** No training, inference, dataset, or generative AI — correctly out-of-scope per 07; respects external-LLM prohibition. |
| **Trading / Quant** | **No trading logic:** No signal generation, execution, or quant reports — correctly out-of-scope per 12 Part I §5. |
| **DevOps / Infrastructure** | Dependencies React 18/TS5/Vite/Vitest/CSS3 vars are already in stack — no new infra; verification via `tsc -b`/`vite build`/`vitest`/`grep`/`axe` per §11/§13 — **build reproducible**. |
| **Governance** | **20-section plan** + Delivery Report correctly traces tiers per 10 hierarchy; 6-phase lifecycle bounded with exit criteria; implementation hold affirmed (no unauthorized P01); `NO DEVIATIONS` correctly anticipated for P01 (read-only token work); Gate CLOSED / NOT CERTIFIED held; debt `TD-UI-POSTCSS-HIGH`/`OBS-P06-2` correctly carried. No silent methodology change (§4A). |
| **Testing & Verification** | `tokens.test.ts` token completeness + contrast ratio validation + `AC-08` regression invariance (376+414) is **proportionate** for P01. Plan correctly requires Level II `vitest`/`tsc`/`grep` + Level I axe/DOM per 09. |
| **Documentation & Knowledge Continuity** | Plan is **migratable** (`docs/plans/UI-009_ENGINEERING_DESIGN_PLAN.md` as single truth, per §16), plus Delivery Report as intake; correctly lists docs 00–17, ADRs, registers, Amendment, PROJECT_STATE 8.70.0 — **institutional memory preserved** per 10 Tier 7. |
| **Product / Operator Integrity** | Advisory-only posture preserved; unification improves discoverability without misrepresenting simulated vs live telemetry; operator efficiency via consistent tokens — **honest state per 02.** |

**No discipline reveals a defect that would prevent approval.**

---

## STAGE 5 — COMPARE — REQUEST → PLAN → GOVERNING REQUIREMENTS

| Dimension | Comparison | Result |
|-----------|------------|--------|
| Request A–O + §4A → Plan A–O + §4A | All 15+1 sections present and mapped with same titles; 6-phase structure as requested; 7-part P01 re-baseline as required | ✅ **No mismatch** |
| Plan → 12 Part VII §11 + 13 Part V | Plan correctly operationalizes “component library, typography, color, tables, forms, cards, dialogs, alerts, tooltips, icons, panel consistency” via P01 tokens → P02 atoms → P03 frames → P04 tables → P05 overlays → P06 audit | ✅ **No mismatch** |
| Plan §10 P01 boundary → 16 Brand | Palette `#0B0E14/#1A1F2C/#2563EB/#10B981/#F59E0B/#EF4444` + typography/spacing/elevation directly traceable to 16 + 08 — see Observation O-009-01 for single hex harmonization | ⚠️ **Minor harmonization** (not a mismatch) |
| Plan §11 AC-01…AC-08 → 08 WCAG / 02 no-color-alone / 17 style-injection | Each AC verifiable and traced | ✅ |
| Plan §16 docs sync → 10 operational governance | PROJECT_STATE/CHANGELOG/RISK/DEBT + `docs/plans/` truth + `docs/evidence/ui009/` correctly listed | ✅ |

---

## STAGE 6 — DETERMINE FINDINGS

### 6.1 Classification

| Finding Type | Count | Detail |
|--------------|-------|--------|
| Blocker | 0 | None |
| Major Defect | 0 | None |
| Material Observation | 0 | None |
| **Minor Observation** | **2** | O-009-01 (palette hex harmonization), O-009-02 (contrast verification scope) |
| Governance Issue | 0 | None |

### 6.2 Observations Detail

| ID | Severity | Description | Required Action | Blocking? |
|----|----------|-------------|-----------------|-----------|
| **O-009-01** | Minor | **Palette Hex Harmonization** — §10 Retained Implementation cites dark root `#070A0F` / surface `#111822`, while §10 Extended Palette + §15 correctly cites Brand Standard 16 Midnight Black `#0B0E14` / Graphite `#1A1F2C` / Electric Blue `#2563EB`. Both are dark-first, but the two dark hexes differ by ~8 luminance. At high-grade, the single source of truth must be **16**: `#0B0E14` / `#1A1F2C` (as listed in 16 Part VI + §10’s 6-color extended palette). The retained `#070A0F` note should be harmonized to `#0B0E14` in the final `tokens.css` to avoid drift. | In `BUILD_ORDER_UI-009-P01` and/or `tokens.css` P01 delivery, **harmonize all dark tokens to 16**: `--ix-bg-root: #0B0E14` (not #070A0F). If DA’s audit shows legacy `#070A0F` is already in use, explicitly record it as **SUPERSEDE** with one-line diff and grep `grep -R "#070A0F" frontend/src`. | **No** |
| **O-009-02** | Minor | **Contrast Verification Scope** — AC-03 requires `>4.5:1` body text and `>3:1` large headings (correct). The smallest token in §10 is Metadata/Monospace `0.75rem` (≈12px) — this is **not** “large text” per WCAG, so it requires **4.5:1**, not 3:1. The `tokens.test.ts` contrast audit must validate this smallest size at 4.5:1, not only headings. | In P01 delivery, ensure `tokens.test.ts` validates **all** tier combinations, including `0.75rem` metadata on both `--ix-bg-root` and `--ix-color-surface` backgrounds, at **>4.5:1**. Provide `accessibility.log` (axe) covering this. | **No** |

*No other observations. The two above are **non-blocking refinement** for P01 implementation — they do not affect the design plan’s approvability.*

---

## STAGE 7 — VERDICT

### **APPROVED WITH OBSERVATIONS**

**Determination ID:** `D-54`
**Phase:** UI-009 Engineering Design Plan — Institutional Design System Implementation
**Verdict:** **APPROVED WITH OBSERVATIONS** (2 Minor Observations — O-009-01, O-009-02)
**Evidence Level:** Plan satisfies all 15+1 required sections; traceability Tier 1→8 is complete; 6-phase lifecycle bounded; Retain 3 / Extend 5 / Supersede 1 / Defer 1 matrix is sound; collaborative governance preserved
**Blockers / Major Defects:** **0**
**Regressions:** N/A — design plan phase (no code)
**Next Authorized Unit:** **`BUILD_ORDER_UI-009-P01` — Design System Foundation & Token Architecture**

#### Rationale

**Design completeness:** All 15 sections A–O + §4A + Executive Summary + Closing are present, correctly bounded for a Foundational + Refinement workstream that unifies UI-001→UI-008 surfaces without introducing new trading/backend/execution/external-AI. 6-phase lifecycle (P01 Tokens → P02 Atoms → P03 Frames → P04 Tables/Grids → P05 Modals/Overlays → P06 Audit) is logically sequenced and dependency-correct per 13 Part II Level A/C and 13 Part IV component-first hierarchy.

**Governance compliance:** Correctly traces to 00/02/03/04/05 v2.0/08/11/12/13/16/17 + Amendment 27 rules + D-53 baseline 83/376+414; implementation hold is correctly affirmed (DA will not implement until Build Order); no silent methodology change (Roadmap→Design Plan→Build Order→… preserved).

**Technical soundness:** 5-tier token hierarchy (Foundation → Semantic → Component → Workspace → Theme Override) is the correct formalization of 14 Part VI; brand palette alignment to 16 (Midnight Black/Graphite/Electric Blue + semantic Green/Amber/Red), typography scale, 4px grid, elevation, motion `120ms` with `prefers-reduced-motion`, and `.ix-*` isolation are all institution-grade. Style-injection defense (static CSS vars, 0 `dangerouslySetInnerHTML`/`eval`) per 17 is correctly enforced.

**Security & product integrity:** Correctly holds invariants — zero actuation, zero external LLM, style-injection defense, credential isolation, Gate CLOSED / NOT CERTIFIED — no new attack surface.

**Observations do not prevent approval** — both are minor implementation-guidance for P01 delivery and will be verified via `tokens.test.ts` + `accessibility.log` in the P01 evidence package.

---

## AUTHORIZATION

With this determination **D-54**, the **UI-009 Engineering Design Plan is APPROVED WITH OBSERVATIONS.**

**The ITRGA now authorizes issuance of:**

> **`BUILD_ORDER_UI-009-P01` — Design System Foundation & Token Architecture**
> *Codify the comprehensive 5-tier token hierarchy in `tokens.css` + `theme.ts` with brand palette (16), typography, spacing, elevation, motion, and `tokens.test.ts` contrast audit — regression invariance 83/376 + 414 + `tsc`/`vite` exit 0 required.*

The DA is authorized to begin **P01 implementation only after** receipt of that Build Order. No workspace rewrites, backend changes, or P02–P06 work is authorized.

---

## DOCUMENT CONTROL

| Field | Value |
|-------|-------|
| Review ID | D-54 |
| Reviewed By | ITRGA — Independent Technical Review & Governance Authority |
| Review Date | 2026-08-10 |
| Governing Request | `ITRGA_REQUEST_UI-009_DESIGN_PLAN.md` |
| Design Plan | `docs/plans/UI-009_ENGINEERING_DESIGN_PLAN.md` (374L) + Delivery Report (91L) |
| Preceding Milestone | D-53 UI-008 COMPLETE (83/376 + 414) |
| Gate / Production | CLOSED / NOT CERTIFIED (unchanged) |
| Distribution | Operator → DA; copy to `docs/plans/` + governance register |

### Independent Review Declaration (Per Amendment §26)

> The ITRGA independently assessed the submitted design plan. DA assertions were not treated as verification without supporting evidence — all 15+1 sections were verified against the governing corpus Tier 1→10. Scope was compared against `ITRGA_REQUEST_UI-009_DESIGN_PLAN.md` and 12 Part VII §11. Implementation approach was compared against 05 v2.0 Presentation Layer and 14 Workspace Shell. No deviations were assessed. Test-count claims (83/376 + 414) were reconciled against D-53. Security boundaries (no actuation, no external LLM, static CSS tokens) were independently assessed. Production certification was not inferred. This determination applies only to the design plan and does not authorize implementation beyond the forthcoming P01 Build Order.

**ITRGA STATUS: UI-009 DESIGN PLAN APPROVED WITH OBSERVATIONS (O-009-01, O-009-02). BUILD_ORDER_UI-009-P01 AUTHORIZED.**

**We don't guess. We prove.**

— AXIOM Independent Technical Review & Governance Authority (ITRGA)

