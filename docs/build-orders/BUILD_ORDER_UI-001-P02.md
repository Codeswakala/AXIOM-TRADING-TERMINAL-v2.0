# BUILD ORDER — UI-001-P02
## Navigation Dock & Workflow Routing (registry-driven, permission-aware, keyboard-operable)

**Issuing authority:** Institutional Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-001 · **Phase:** P02
**Predecessor:** `ITRGA_REVIEW_UI-001-P01.md` — **APPROVED WITH OBSERVATIONS** (authorizes this order)
**Governing spec:** `15_UI-001_IMPLEMENTATION_SPECIFICATION.md` **Part V** (Navigation Dock & Workspace Registration); Doc 14 §4/§10; Doc 12 Part V.
**Baseline (must be unchanged):** platform v0.62.0 · Alembic head `20260717_0037` · backend 413 · frontend 22f/76t.
**Motto:** *We don't guess. We prove.*

---

## 1. Objective
Replace the P01 placeholder navigation with the **permanent, registry-driven Navigation Dock** and deterministic **workflow routing/activation** — task-oriented (not module-oriented) navigation generated **automatically** from `WorkspaceRegistry`. This is presentation infrastructure only: **no new backend/API/schema/ML/governance, no new capability, Gate stays CLOSED, no execution/actuation anywhere.**

## 2. Scope IN
1. **Widen `WorkspaceRegistry` to the 14-field canonical Workspace Registration Contract** (Doc 15 Part V §5) — folds **OBS-P01-3 (F-1), BINDING**: Workspace Identifier · Display Name · **Navigation Category** · Route · Icon · RBAC Requirements · Default Layout · Context-Panel Support · Activity-Dock Support · Search Support · Keyboard Shortcut · Telemetry Identifier · Workspace Version · Optional Feature Flag. **Retain ITRGA guard fields `requiresAuth` + `noActuation:true` on top.** Fields not yet exercised may be typed-optional but the type must exist now. Populate `Navigation Category` for all 15 current routes using the Part V §3 task taxonomy (Monitor · Research · Investigate · Compare · Plan · Review · Govern · Settings).
2. **Navigation Generator** (Part V §7) — automatically builds the dock from the registry: category grouping, ordering, collapse, icons, active-workspace indicator, **permission filtering**, feature-flag filtering. **Manual navigation construction is prohibited** (Part V §4/§7/§16).
3. **Navigation Dock** (Part V §8) — persistent visibility, expand/collapse, keyboard navigation, responsive adaptation, active highlighting, tooltip/badge/notification-indicator scaffolds. Dock remains visible throughout the session (Region B).
4. **Workspace Activation** (Part V §9) — deterministic route transition + workspace init + focus management + telemetry-event hook (hook only). Activation must be deterministic and regression-free for all 15 routes.
5. **Permission integration** (Part V §10) — navigation visibility respects RBAC via the **centralized** authorization path; **the dock implements NO independent permission logic**.
6. **Keyboard + responsive + accessibility** (Part V §12/§13/§15) — keyboard-operable dock, responsive collapse, ARIA nav landmark + focus order.

## 3. Scope OUT (deferred to later phases — do NOT implement)
Panel docking/resize/layout manager (P03); persistence to `operator_workspace_preferences` (P04); overlay/notification/full command-palette behaviour + Region-F three-layer split OBS-P01-4/F-2 (P05); legacy `TerminalLayout` retirement (P06); full token architecture completion OBS-P01-5/F-3 (progress across P02–P05, priority on Governance/Research/Execution-Research/Intelligence color roles used by the dock categories).

## 4. Constitutional & architectural guardrails (carry from P01, all binding)
- **UG-1/UG-2/R-3 — no execution/actuation in the dock or any region** (grep source clean + browser). Navigation is transition-only.
- **UG-3/R-1 — no backend/API/alembic/schema/pyproject/requirements change**; head `20260717_0037` unchanged; UI-only diff.
- **Doc 14 §10 — one integrated environment**: no page-specific nav, no duplicated headers, no independent sidebars, no competing layouts. The dock is **the** navigation for all workspaces.
- **Part V §16 — Navigation is infrastructure only**: no hardcoded workspace defs, no duplicated routing/RBAC logic, no workspace-specific behaviour, no business state.
- **UG-15 — no unspiked dependency.**

## 5. MANDATORY EVIDENCE (operator-run on target; a blank/errored grep or variable is an R7 non-result)

**(a) Build-identity** — `sed -n '1,15p'` of the P02 delivery report + confirm it is OF P02.
**(b) 14-field registry proof** — show the widened `WorkspaceRegistry` type/interface and one populated entry with all 14 canonical fields + guard fields; grep proving `Navigation Category` populated for all 15 routes.
**(c) No-manual-nav proof** — grep showing the dock is rendered from a generator over the registry (`.map`/generator), not a hardcoded menu; no page-specific nav components.
**(d) Named tests (must be DISPLAYED passing by name — verbose reporter):**
  - `test_navigation_generated_from_registry_not_hardcoded`
  - `test_navigation_dock_contains_no_execution_or_actuation`
  - `test_navigation_permission_filtering_hides_unauthorized_workspaces`
  - `test_workspace_activation_is_deterministic_for_all_routes`
**(e) No-actuation grep on dock/nav SOURCE (test files excluded)** — clean.
**(f) Regression** — backend `pytest -q` **≥413 passed**; frontend Vitest **>22f/76t** (grown), all passing; TypeScript clean; build succeeds + bundle delta reported.
**(g) Alembic head** — `alembic current` **printing `20260717_0037`** AND empty `git diff -- backend\app backend\alembic ...`. *(Closes OBS-P01-2.)*
**(h) OBS-P01-1 closure** — a verbose Vitest run that **displays `test_shell_hosts_only_no_business_logic_in_shell` passing BY NAME.**
**(i) Browser (served session)** — shots: dock with task-category grouping + active highlight; ≥3 routes activated via the dock in-shell (incl. Operations + ≥1 research + Govern/Settings if present); keyboard focus on dock; responsive collapsed state; Gate CLOSED / research framing still visible; logged-out block.
**(j) Local CI** — `& "C:\Program Files\Git\bin\bash.exe" scripts/local_ci.sh` → inline `LOCAL_CI_EXIT_CODE:` (0, or the TD-W6-CI-AUDIT offline-audit env-flake surfaced AFTER substantive gates green — never relabel green; disposition via operator).

## 6. Acceptance criteria (Determination vocabulary: Approved · Approved with Observations · Corrective Actions Required · Rejected)
**Approved** requires: build-identity confirmed; (b) 14-field registry proven (OBS-P01-3 closed); (c) navigation registry-generated with manual-nav absent; (d) all four named tests displayed passing; (e) source no-actuation clean; (f) regression green with actual totals (backend ≥413, frontend grown); (g) head unchanged (OBS-P01-2 closed); (h) OBS-P01-1 closed; (i) browser confirms dock/activation/permission/framing/logged-out; no barred dependency; build succeeds; CI exit 0 (or waived env-flake). **Only Approved / Approved-with-Observations authorizes `BUILD_ORDER_UI-001-P03`.**

*We don't guess. We prove.*
