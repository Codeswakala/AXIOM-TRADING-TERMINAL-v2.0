# ITRGA REQUEST — UI-002 ENGINEERING DESIGN PLAN
## UI-002 — Workflow Navigation Framework

**Authority:** Institutional Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-002 (2nd UI workstream)
**Governing docs:** `12_INSTITUTIONAL_UI_TRANSFORMATION_PLAN.md` **§4 (UI-002 objective/scope)**; `13_UI_TRANSFORMATION_MASTER_PLAN.md` (sequencing: UI-002 depends on UI-001, required before UI-003–008); `14_UI-001_TECHNICAL_DESIGN_SPECIFICATION.md` §11 / `15_..._IMPLEMENTATION_SPECIFICATION.md` §12 (subsequent workstreams **build upon UI-001 without modifying its architectural responsibilities**).
**Predecessor milestone:** 🏛️ **UI-001 COMPLETE** (`ITRGA_REVIEW_UI-001-P06_FINAL_AND_UI-001_COMPLETION.md`).
**Sequence note (operator-corrected):** ITRGA **requests this Design Plan first**; a Build Order (`BUILD_ORDER_UI-002-P01`) is issued only after ITRGA accepts the plan.
**Motto:** *We don't guess. We prove.*

---

## 1. What ITRGA is requesting
A DA **Engineering Design Plan** for **UI-002 — Workflow Navigation Framework** (Doc 12 §4). Objective (verbatim): *"Transform navigation from page-oriented access into workflow-oriented operation."* Full Doc 12 §4 scope is in play:
- Workflow navigation
- Global search
- Command palette
- Breadcrumbs
- Context-aware navigation
- Workspace switching
- Quick actions

Expected outcome: *"Operators navigate according to institutional workflows rather than software modules."*

The plan is **not** an implementation and **not** self-approving. On receipt, ITRGA will review it and return **Approved / Approved with Observations + binding refinements / Corrective / Rejected**; only an accepted plan authorizes `BUILD_ORDER_UI-002-P01`.

## 2. 🔴 Mandatory framing — EXTEND UI-001, do NOT duplicate or modify it
UI-001 already delivered, and UI-002 must **consume/extend** (Doc 15 §12), not rebuild or fork:
- **Navigation Dock + 14-field Workspace Registry** (UI-001 P02) — registry-driven, permission-aware.
- **Command Palette** (UI-001 P05) — globally accessible, **type-enforced navigation/UI-toggle only** (`commandType: "navigation" | "ui-toggle"`).
- **Overlay/Dialog/Notification (Region F)**, **Design System** (11 token categories / 18 semantic color roles), **session persistence via `operator_workspace_preferences`** (P04).

**The plan MUST include a UI-001 reconciliation section** mapping each Doc 12 §4 item to: *(a)* already-delivered-in-UI-001 (reuse as-is), *(b)* extends an existing UI-001 primitive (how, without modifying its architectural responsibility), or *(c)* net-new. **No new independent navigation/palette/overlay system.** Any change to UI-001's architectural responsibilities is out-of-scope and would require a constitutional amendment (Doc 14 §11 / Doc 15 §12).

## 3. 🔴 Constitutional guardrails (pre-registered — the plan must honor all)
- **UG-1/UG-2 — presentation-only, no scope expansion.** UI-002 is navigation presentation; **no new backend business logic, no new trading/research capability, no execution/actuation surface, no external AI/LLM, no dynamic plugin execution.**
- **UG-3 — no backend/API/schema/governance/ML change** unless the plan makes a *specific, justified* case for a **search-index/read-only** backend touch; if so it must be flagged for a dedicated persistence/endpoint review (no execution surface, RBAC-scoped, and — if any table — the standing persistence-capture control applies). **Default expectation: frontend-only or reuse existing read APIs.**
- **UG-4 — no regression:** current baseline **backend 414 / frontend 26f·97t / head `20260717_0037`** must be preserved; route-by-route in-shell + UI-only diff.
- **Doc 14 §10 — one integrated environment:** no page-specific nav, no duplicated headers, no independent sidebars, no competing layouts. UI-002 navigation is the *one* navigation, extending the UI-001 dock/palette.
- **Doc 12 Part V design system:** semantic color roles only; **never color alone**; typography hierarchy; reuse UI-001 tokens (no new hardcoded color).
- **Accessibility is a primary requirement** (Doc 15 Part VIII §15): global search + breadcrumbs + palette must be keyboard-operable, ARIA-correct, focus-managed, reduced-motion aware.
- **UG-15 — no new dependency without a wheel/bundle-compat spike + ITRGA sign-off** (prefer first-party; a search/fuzzy-match lib, if proposed, needs a spike).
- **Gate stays CLOSED throughout.**

## 4. 🔴 Quick-actions — the plan MUST enumerate a catalogue for ITRGA vetting
Doc 12 §4 lists "Quick actions." In UI-001 the palette was held to **navigation/UI-toggle only** (constitutional red-line). Per operator direction, the Design Plan must **enumerate every proposed quick-action** with, for each: name, what it does, the target (route/panel/overlay/theme/workspace), and an explicit assertion that it is **navigation/UI-toggle only — never a business/trading/execution/order/broker/account/Gate action.** ITRGA will vet the catalogue item-by-item; any action that actuates or mutates business state is **rejected at plan stage**. Global search results are **read-only navigation targets** (jump-to), not action surfaces.

## 5. Content ITRGA expects in the Design Plan
1. **Objective & scope** restatement mapped to Doc 12 §4; **UI-001 reconciliation table** (§2 above).
2. **Architecture** — how workflow navigation, breadcrumbs, context-aware nav, workspace switching, and global search compose within the UI-001 shell (Regions A/B/F), consuming the Workspace Registry; state ownership (Shell owns nav/routing; no business state in nav).
3. **Global search design** — sources (existing read APIs / registry searchable entities per Doc 15 Part V §11: reports, signals, journal, collections, portfolio reports, annotations, trade plans), indexing approach (client-side over existing data vs any backend touch — justify), result model = read-only jump-to.
4. **Breadcrumbs & context-aware navigation** — deterministic, derived from route/registry; no business logic.
5. **Command-palette extension** — how UI-002 extends the existing palette (register commands via the Workspace Registration Contract) without a second palette; the quick-action catalogue (§4).
6. **Accessibility plan** (keyboard/ARIA/focus/reduced-motion) as a first-class section.
7. **Phase decomposition** (UI-002-P01…Pn) with a dependency rule (no later phase until ITRGA accepts the prior slice), each phase's named tests + evidence anchors.
8. **Regression & evidence strategy** — reaffirm the Level-I bar: operator-run on-target evidence, named tests displayed passing, no-actuation source grep, browser-judged served sessions, networked CI, head unchanged, UI-only diff.
9. **Constitutional attestation** — no scope expansion, Gate CLOSED, no execution/AI, extends-not-modifies UI-001, quick-actions navigation-only.
10. **Risks/assumptions/open questions** for ITRGA.

## 6. Acceptance anchors (how ITRGA will judge the plan)
Accepted (→ authorizes `BUILD_ORDER_UI-002-P01`) requires: Doc 12 §4 scope covered; **UI-001 reconciliation shows extend-not-duplicate** with no modification of UI-001 architectural responsibilities; **quick-action catalogue enumerated and constitutionally clean**; global search is read-only navigation (backend touch, if any, justified + flagged for dedicated review); accessibility is first-class; presentation-only / Gate CLOSED attested; phase decomposition sound; evidence strategy meets the Level-I bar. Otherwise: Approved-with-Observations + binding refinements, Corrective, or Rejected.

Baseline of record: v0.62.0 · head `20260717_0037` · backend 414 · frontend 26f·97t. Standing residuals (non-blocking): TD-W7-U07-RATE-GUARD, TD-W6-CI-AUDIT.

**Please deliver `UI-002_ENGINEERING_DESIGN_PLAN.md`.**

*We don't guess. We prove.*
