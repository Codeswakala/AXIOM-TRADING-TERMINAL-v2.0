# ITRGA REVIEW — UI-002 ENGINEERING DESIGN PLAN
## UI-002 — Workflow Navigation Framework

**Authority:** Institutional Technical Review & Governance Authority (ITRGA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-002
**Plan under review:** `UI-002_ENGINEERING_DESIGN_PLAN.md` (1075 lines) · Request: `ITRGA_REQUEST_UI-002_DESIGN_PLAN.md`
**Determination:** ✅ **APPROVED WITH OBSERVATIONS + BINDING REFINEMENTS (R-1…R-6)**
**Authorizes:** `BUILD_ORDER_UI-002-P01` (Workflow Metadata, Breadcrumb Foundation & Registry Reconciliation) — subject to the refinements below.
**Motto:** *We don't guess. We prove.*

---

## 0. Build-identity — PASS
Correct plan: references the ITRGA request + UI-001 completion; baseline v0.62.0 / head `20260717_0037` / backend 414 / frontend 26f·97t; Gate CLOSED; DA does not self-approve.

## 1. What the plan gets right (verified against the acceptance anchors)
- **Doc 12 §4 scope fully covered** (workflow nav · global search · command palette · breadcrumbs · context-aware nav · workspace switching · quick actions) with the expected outcome restated.
- **🔴 EXTEND-not-duplicate (mandate met).** §2 reconciliation maps every §4 item to reuse/extends/net-new; the key decision — **companion workflow metadata keyed by `workspace.id`, NOT forking the 14-field Workspace Registry** — preserves UI-001's architectural responsibilities (Doc 15 §12). §2.1 anti-duplication commitments (no second nav/palette/overlay/search-shell; command types limited to `navigation`/`ui-toggle`) are exactly as required.
- **🔴 Quick-action catalogue (§8) — constitutionally CLEAN.** ITRGA vetted all **28** actions item-by-item: **16 navigation** (jump-to existing registered routes / previous / recent) + **12 ui-toggle** (region/theme/focus/search-overlay/status-dialog/governance-notification). **Zero** business/execution/order/broker/account/Gate actions. The explicit **Rejected action classes** list (place order, execute trade, connect broker, open Gate, approve certification, allocate capital, size position, mutate journal/plan/tag/collection, external AI/LLM, load plugin) and the "`execution`/`trade` are workspace *names*, never actuation verbs" discriminator show correct constitutional understanding.
- **Global search (§5) = read-only jump-to.** Type-enforced result model (`resultAction:"navigate"`, `readonly:true`, no executable callback, no POST/PUT/PATCH/DELETE/execute/approve/connect/place/size/allocate/Gate); sources are **existing read APIs** only; ephemeral client-side index; **first-party matching, no fuzzy-search dependency** (UG-15 honored); **no table/migration/endpoint** — backend index explicitly deferred to a dedicated persistence-capture review.
- **Accessibility (§9)** is a first-class section (keyboard/ARIA/focus/reduced-motion for search, breadcrumbs, switcher, palette, context-nav).
- **Phase decomposition (§10)** is sound: P01 metadata/breadcrumbs → P02 switcher/context-nav seam → P03 palette extension/quick-actions → P04 global search → P05 context-aware + UI-002 completion checkpoint; each frontend-only with named tests + no-backend-diff; dependency rule stated (no later phase until ITRGA accepts the prior slice).
- **Evidence strategy (§11)** reaffirms the Level-I bar; **§12 attestation** comprehensive; DA does not self-approve.

## 2. Binding refinements (fold into the relevant Build Orders; conditions of acceptance)
- **R-1 (answers §13.3 Q1) — ACCEPTED: companion workflow metadata keyed by `workspace.id` is the approved extension mechanism.** The UI-001 **14-field Workspace Registration Contract MUST NOT be modified**; UI-002 metadata is additive and keyed by `workspace.id`. P01 must prove (test + grep) that `workspaceRegistry.tsx` is unchanged (or changed only additively in a way ITRGA pre-approves) and that workflow metadata is a separate module.
- **R-2 (answers §13.3 Q2) — BIND P04 SCOPE: first global-search slice limited to workspace + signals + journal + research-collections.** The remaining adapters (intelligence, scenario, portfolio, chart-annotations, trade-plans, execution-research) are a **second P04 slice or P04b**, each added only after the read-only/no-actuation pattern is proven on the first four. Prevents a broad hidden-action surface landing at once.
- **R-3 (answers §13.3 Q3) — recent-workspace ids MAY persist in existing `operator_workspace_preferences.layout_config` ONLY**, provided: **search queries and artifact payloads are NEVER persisted**; the write reuses the P04(UI-001) path (no new table/column — R-4 no schema creep); and it carries the persistence-capture control **only if it writes a new row-shape** (else the existing shell-pref row suffices). Recent-workspace persistence is **deferred to the phase that needs it** (P02 switcher), not P01.
- **R-4 (answers §13.3 Q4) — ONE overlay infrastructure, ONE command system is mandatory.** Whether global search is a separate Region-F overlay or a tabbed command/search overlay is the DA's choice **provided** it (a) reuses the single UI-001 overlay family, (b) does not create a second palette/command system, and (c) the palette stays type-enforced navigation/UI-toggle only. State the chosen approach in the P03/P04 Build-Order response.
- **R-5 — Global-search "hidden action surface" is the top constitutional risk (plan §13.1 agrees).** Every phase touching search/palette MUST include a named test asserting **results/commands cannot mutate** (no callback other than navigate; reject disallowed verbs) + a no-actuation source grep. This is a standing acceptance condition for P03 and P04.
- **R-6 — Standing Level-I evidence bar (unchanged, restated as binding):** each phase owes operator-run on-target evidence, **named tests displayed passing by name**, no-actuation source grep clean, browser-judged served sessions (UI is judged in the browser — do not omit screenshots as happened at P06 attempt-1), **networked CI exit 0 + sentinel**, head `20260717_0037` unchanged, UI-only diff (empty backend/alembic/pyproject/requirements/package-manifest diff), no unspiked dependency, backend ≥414 / frontend grown. Build-identity verified first every turn (stale/wrong-pack recurred twice in UI-001).

## 3. Determination & rationale
**APPROVED WITH OBSERVATIONS + BINDING REFINEMENTS.** The plan meets every acceptance anchor from the ITRGA request: full Doc 12 §4 coverage; a rigorous extend-not-duplicate reconciliation that leaves UI-001's architecture intact; a constitutionally clean, fully-enumerated quick-action catalogue; read-only global search with no backend expansion or dependency; first-class accessibility; a sound phased plan; and the correct evidence posture. It is not a *clean* Approve only because the plan raised **four legitimate open questions (§13.3)** that require ITRGA rulings — now issued as **R-1…R-4** — plus two standing conditions (**R-5/R-6**). None of these are defects; they are the reviewer's binding answers that shape the Build Orders.

Per the UI-Transformation sequence, **an accepted plan authorizes the first Build Order.** → **`BUILD_ORDER_UI-002-P01` is authorized** (Workflow Metadata, Breadcrumb Foundation & Registry Reconciliation), with **R-1 folded as binding** (metadata keyed by `workspace.id`, registry unmodified) and R-5/R-6 applied; R-2/R-3/R-4 bind their respective later phases.

**Constitutional posture:** Gate CLOSED; presentation/navigation only; no execution/AI/plugin/schema change; UI-001 unmodified. Baseline of record: v0.62.0 · head `20260717_0037` · backend 414 · frontend 26f·97t. Residuals unchanged: TD-W7-U07-RATE-GUARD, TD-W6-CI-AUDIT.

*We don't guess. We prove.*
