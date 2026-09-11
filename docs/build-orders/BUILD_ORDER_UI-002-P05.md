# BUILD ORDER — UI-002-P05 (FINAL)
## Context-Aware Workflow Integration · UI-002 Completion Checkpoint

**Issuing authority:** Institutional Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-002 · **Phase:** P05 (final)
**Predecessor:** `ITRGA_REVIEW_UI-002-P04.md` — **APPROVED WITH OBSERVATIONS** (authorizes this order)
**Governing:** Doc 12 §4; Doc 15 Part VII (state/context/history); design plan §6/§10 (UI-002-P05) + §11 evidence strategy; binding refinements **R-2/R-4/R-5/R-6**; carried hard gate **OBS-P04(UI002)-1**.
**Baseline (must be unchanged):** v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 30f/121t.
**Motto:** *We don't guess. We prove.*

---

## 0. 🔴 CARRIED HARD INTAKE GATE (OBS-P04(UI002)-1) — supply FIRST, or review does not begin
Establish a **phase-isolating git baseline** (commit the current tree / tag / stash-per-phase), then supply as the **first evidence lines** a **meaningful diff that isolates the UI-002 delta (P04 + P05)** — e.g. `git diff --stat <pre-P04-ref>..HEAD` or `git diff --stat` against a committed baseline — **positively showing NO backend/API/schema/migration/dependency change** (empty for `backend\app`, `backend\alembic`, `backend\pyproject.toml`, `backend\requirements.txt`, `frontend\package.json`, `frontend\package-lock.json`) — plus `alembic current` = **`20260717_0037`**. This supersedes OBS-P03/P02 and closes the diff-method churn. Absent a phase-isolating no-drift proof, ITRGA returns **Corrective** without further eval.

## 1. Objective
Integrate the UI-002 pieces (workflow navigation, breadcrumbs, workspace switcher, command palette, context navigation, global search) into a **cohesive, consistent** whole, harden responsiveness, and bring UI-002 to its **completion checkpoint** (per design plan §10 + §11). Presentation/navigation only: **no new backend/API/schema/ML/governance, no execution/actuation, Gate CLOSED.**

## 2. Scope IN (per accepted plan UI-002-P05)
1. **Cross-route context-aware navigation consistency** — breadcrumbs/switcher/context-nav/search/palette behave consistently across all routes; no business logic in navigation.
2. **Search/palette/breadcrumb coordination** — the surfaces stay **registry-consistent** (single source of truth = Workspace Registry + workflow metadata); no divergence.
3. **Responsive behavior hardening** — navigation surfaces degrade gracefully at narrow widths.
4. **UI-002 documentation & evidence pack** + **completion regression**.
5. *(Optional)* **P04b remaining search adapters** — if included, each is read-only jump-to over existing read APIs (R-2/R-5); state explicitly if deferred.

## 3. Scope OUT (do NOT implement)
- Any new backend/API/schema/migration/column/dependency; any execution/actuation/AI/plugin; any second nav/palette/overlay.
- Any modification to UI-001 architectural responsibilities; any new business capability.
- Production certification (separate Doc-11 track, HELD).

## 4. Constitutional & architectural guardrails (binding)
- **R-5** — whole navigation surface contains **no actuation controls** (grep + named test).
- **R-4 / Doc 14 §10** — single UI-001 shell navigation system across all routes; no competing systems.
- **R-2** — any P04b adapters are read-only first-slice-pattern; no backend index.
- **UG-3/UG-15** — no backend/API/schema change; no new dependency; head `20260717_0037`; UI-only diff (per §0).
- **Accessibility first-class**; **no regression** (all UI-001 + UI-002-P01…P04 tests green).
- **Gate CLOSED**; research-only posture preserved.

## 5. MANDATORY EVIDENCE (operator-run on target; blank/errored grep = R7 non-result)
**(a) 🔴 OBS-P04(UI002)-1 intake gate** — phase-isolating no-drift diff + `alembic current` = `20260717_0037`, FIRST (§0).
**(b) Build-identity** — `sed -n '1,15p'` of the P05 delivery report; confirm it is OF UI-002-P05.
**(c) Named tests (MUST be DISPLAYED passing by name — verbose reporter):**
  - `test_ui002_context_aware_navigation_preserves_workflow_without_business_logic`
  - `test_ui002_all_routes_keep_single_ui001_shell_navigation_system`
  - `test_ui002_workflow_navigation_full_surface_contains_no_actuation_controls`
  - `test_ui002_breadcrumbs_search_palette_and_switcher_remain_registry_consistent`
  - `test_ui002_completion_checkpoint_preserves_gate_closed_and_research_only_status`
  - `test_ui002_completion_checkpoint_frontend_routes_mount_in_shell_without_regression`
**(d) Whole-surface no-actuation grep (R-5)** — all UI-002 nav source (workflows/navigation/commands/search/overlays; tests excluded) → clean.
**(e) Single-shell / registry-consistency proof (R-4)** — grep/test showing one nav system; breadcrumbs/search/palette/switcher all derive from the registry + workflow metadata.
**(f) Regression (completion)** — backend `pytest -q` **≥414 passed**; frontend Vitest **>30f/121t** all passing; TS clean; build + bundle delta.
**(g) Browser (served session) — R-6 route-by-route** — screenshots across a **representative workflow progression** (e.g. Operations → Advisory Signals → Signal Investigation → Scenario Comparison → Journal); **keyboard-only** workflow walkthrough; **responsive** (narrow-width) screenshots; Gate CLOSED/research framing; logged-out block.
**(h) Networked CI (R-6)** — `scripts/local_ci.sh` → `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0`.
**(i) 🔴 UI-002 COMPLETION CHECKPOINT** — the delivery report presents the DA's completion self-check; ITRGA will independently apply a **constitutional validation** (hierarchy respected · no roadmap/scope expansion · no unauthorized business functionality · governance preserved · research-only preserved · no execution pathways · UI-001 unmodified · single shell navigation · **Gate CLOSED**), analogous to Doc 15 Part IX §15.

## 6. Acceptance criteria (Determination: Approved · Approved with Observations · Corrective Actions Required · Rejected)
**Approved** requires: **(a) OBS-P04(UI002)-1 phase-isolating no-drift proof satisfied** (else Corrective, no further eval); build-identity confirmed; (c) all six named tests displayed passing; (d) whole-surface no-actuation grep clean; (e) single-shell/registry-consistency proven; (f) completion regression green with actual totals; (g) route-by-route + keyboard + responsive browser evidence; (h) networked CI exit 0 + sentinel; (i) constitutional completion validation clean.

**On Approved: ITRGA will declare 🏛️ UI-002 — WORKFLOW NAVIGATION FRAMEWORK — COMPLETE** (workflow-oriented navigation integrated on the UI-001 shell; conforms to Doc 12 §4 / Doc 14; regression passed; ITRGA review complete). Future: UI-003+ (each needs its own Design Plan → Build Order → review) and, separately, the Production Readiness Certification track (Doc 11, HELD). **UI-002 completion does NOT open the Gate or authorize execution.**

*We don't guess. We prove.*
