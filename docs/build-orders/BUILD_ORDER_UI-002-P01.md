# BUILD ORDER — UI-002-P01
## Workflow Metadata · Breadcrumb Foundation · UI-001 Registry Reconciliation

**Issuing authority:** Institutional Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-002 (Workflow Navigation Framework) · **Phase:** P01
**Predecessor:** `ITRGA_REVIEW_UI-002_DESIGN_PLAN.md` — **APPROVED WITH OBSERVATIONS + BINDING REFINEMENTS (R-1…R-6)** (authorizes this order)
**Governing:** Doc 12 §4; Doc 15 §12 (build-upon-not-modify UI-001); design plan §4/§6/§10 (UI-002-P01).
**Baseline (must be unchanged):** v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 26f/97t.
**Motto:** *We don't guess. We prove.*

---

## 1. Objective
Establish the **workflow navigation model** and a **deterministic breadcrumb foundation** that **extend** UI-001 without altering its architectural responsibilities. Presentation/navigation only: **no new backend/API/schema/ML/governance, no new capability, no new route, Gate CLOSED, no execution/actuation anywhere.**

## 2. Scope IN (per accepted plan UI-002-P01)
1. **Companion workflow metadata** keyed by UI-001 **`workspace.id`** — a **separate additive module**; **must NOT modify the 14-field Workspace Registration Contract** (R-1 binding). UI-001 remains the source of workspace identity/route/RBAC/layout/search/no-actuation.
2. **Metadata validation utilities** — every metadata entry references **only registered** workspaces; invalid/orphan keys rejected.
3. **Deterministic breadcrumb model** — derived from route + workspace + workflow metadata; no business logic; same input → same crumbs.
4. **`BreadcrumbTrail` in Region A** — presentation only; optional artifact crumb only from read-only route/context data already available (no privileged fetch solely for a label).

## 3. Scope OUT (do NOT implement in P01)
- Global search (P04/P04b — R-2), workspace switcher & recent-workspace persistence (P02 — R-3), command-palette extension & quick-actions (P03 — R-5), context-aware suggestions beyond breadcrumbs (P02/P05).
- Any new route; any backend/API/schema/migration/column; any new dependency; any execution/actuation/AI/plugin.
- Any modification to UI-001's registry, nav dock, palette, overlay family, or design tokens' architectural responsibilities (additive token *usage* is fine; no new hardcoded color).

## 4. Constitutional & architectural guardrails (binding)
- **R-1** — UI-001 14-field registry **unmodified**; workflow metadata is a distinct module keyed by `workspace.id`.
- **UG-1/UG-2/R-3(UI-002 R-5)** — no execution/actuation in any UI-002 nav element (grep + test).
- **UG-3** — no backend/API/alembic/schema change; head `20260717_0037`; UI-only diff; no new dependency (UG-15).
- **Doc 14 §10** — one integrated environment: **no independent navigation, no competing layout, no duplicate header**; breadcrumbs live in the existing Region A.
- **Doc 12 Part V** — semantic tokens only; never color alone; reuse UI-001 tokens (no new hardcoded color).
- **Accessibility first-class** — breadcrumbs keyboard-navigable + ARIA (`nav[aria-label]`, current-page marked).
- **No regression** — every route + all UI-001 tests still green.

## 5. MANDATORY EVIDENCE (operator-run on target; blank/errored grep = R7 non-result)
**(a) Build-identity** — `sed -n '1,15p'` of the P01 delivery report; confirm it is OF UI-002-P01 (grep markers; not a stale/wrong pack — this recurred in UI-001, I will check).
**(b) R-1 registry-unmodified proof** — `git diff` shows `workspaceRegistry.tsx` unchanged (or additively-only in an ITRGA-preapproved way); grep proving workflow metadata is a **separate module** keyed by `workspace.id`; a test that metadata references only registered workspaces.
**(c) Named tests (MUST be DISPLAYED passing by name — verbose reporter):**
  - `test_ui002_workflow_metadata_extends_ui001_registry_without_duplication`
  - `test_ui002_workflow_metadata_references_only_registered_workspaces`
  - `test_ui002_breadcrumbs_are_route_registry_derived_and_deterministic`
  - `test_ui002_breadcrumbs_are_accessible_and_keyboard_navigable`
  - `test_ui002_no_independent_navigation_or_competing_layout`
  - `test_ui002_workflow_navigation_contains_no_execution_or_actuation_controls`
**(d) No-actuation source grep (R-5)** — UI-002 nav/breadcrumb source (tests excluded): `buy|sell|place_order|execute|go-live|connect-broker|account_id|order_ticket|open_gate|allow_execution` → clean.
**(e) No-duplicate-navigation proof** — grep/test showing no second global nav / no competing layout / no duplicate header; breadcrumbs render in existing Region A only.
**(f) Regression** — backend `pytest -q` **≥414 passed**; frontend Vitest **>26f/97t** all passing; TS clean; build + bundle delta.
**(g) UI-only diff + head unchanged** — `git diff --stat` frontend/docs only; empty `git diff -- backend\app backend\alembic backend\pyproject backend\requirements frontend\package.json frontend\package-lock.json`; `alembic current` = `20260717_0037`.
**(h) Browser (served session) — R-6** — shots: breadcrumbs on ≥3 representative routes (e.g. `/`, `/signals`, `/research-management`) in Region A; keyboard focus on breadcrumb; Gate CLOSED/research framing; logged-out block. **Do not omit browser evidence.**
**(i) Networked CI (R-6)** — `& "C:\Program Files\Git\bin\bash.exe" scripts/local_ci.sh` → `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0` (audit clean).

## 6. Acceptance criteria (Determination: Approved · Approved with Observations · Corrective Actions Required · Rejected)
**Approved** requires: build-identity confirmed; (b) R-1 registry-unmodified + metadata-module proven; (c) all six named tests displayed passing; (d) no-actuation grep clean; (e) no-duplicate-navigation proven; (f) regression green with actual totals (backend ≥414, frontend grown); (g) UI-only diff + head unchanged; (h) browser breadcrumbs/framing/logged-out; (i) networked CI exit 0 + sentinel; no barred/unspiked dependency. **Only Approved / Approved-with-Observations authorizes `BUILD_ORDER_UI-002-P02` (Workspace Switcher & Context-Navigation Seam; binds R-3 recent-workspace persistence).**

*We don't guess. We prove.*
