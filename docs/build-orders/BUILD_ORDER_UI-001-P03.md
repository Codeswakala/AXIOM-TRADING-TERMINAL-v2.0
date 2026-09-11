# BUILD ORDER — UI-001-P03
## Panel Infrastructure & Layout Manager (registered panels · deterministic docking · operator-scoped layout seam)

**Issuing authority:** Institutional Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-001 · **Phase:** P03
**Predecessor:** `ITRGA_REVIEW_UI-001-P02.md` — **APPROVED WITH OBSERVATIONS** (authorizes this order)
**Governing spec:** `15_UI-001_IMPLEMENTATION_SPECIFICATION.md` **Part VI** (Panel Infrastructure); Doc 14 §4 (Regions C/D/E), §10; Doc 12 Part V.
**Baseline (must be unchanged):** platform v0.62.0 · Alembic head `20260717_0037` · backend 413 · frontend 23f/80t.
**Motto:** *We don't guess. We prove.*

---

## 1. Objective
Deliver the **presentation-only panel infrastructure** that lets workspaces compose panels within Regions C/D/E: a canonical **Panel Registry**, a deterministic **Docking Engine**, and a **Layout Manager** with a **serialization/restoration seam** (in-memory/session for now). Persistence to `operator_workspace_preferences` is **explicitly P04** — build the seam, do NOT wire the backend. Presentation infrastructure only: **no new backend/API/schema/ML/governance, no new capability, Gate CLOSED, no execution/actuation anywhere.**

## 2. Scope IN
1. **Panel Registration Contract** (Part VI §5) — canonical panel metadata type: Panel Identifier · Display Name · Panel Category · Supported Workspaces · Default/Minimum/Maximum Dimensions · Resizable · Dockable · Closable · Persistence Support · Context Dependencies · Telemetry Identifier · Panel Version. **Retain ITRGA guard `noActuation:true`** on every panel entry. **Only registered panels participate in layouts** (§5/§6). Register the panels already present in the current shell workspaces (Context Panel content, Activity Dock content) as the initial catalogue — do not invent new business panels.
2. **Panel Registry** (Part VI §6) — authoritative catalogue; no panel bypasses it; no hardcoded workspace-specific layouts.
3. **Docking Engine** (Part VI §7) — deterministic left/right/top/bottom/center + split/nested/grouping placement primitives. **Docking behaviour deterministic** (given the same layout descriptor → same arrangement).
4. **Layout Manager** (Part VI §8) — layout init, positioning, **resize management**, workspace-transition layout swap, **layout serialization + restoration** (to an operator-scoped in-memory/session store this phase), layout validation. Layouts are **operator-specific** in shape but **NOT yet persisted to the DB** (P04).
5. **Panel Manager** (Part VI §9) + **responsive resizing** (§13) + **panel accessibility** (§14: focusable panels, ARIA, keyboard resize/close where applicable).
6. **Shell Event Bus integration** (Part VI §17 forbids bypass) — panel↔shell coordination goes through the shell event/context seam, not direct workspace coupling.

## 3. Scope OUT (do NOT implement)
- **Persistence to `operator_workspace_preferences`** and any new table/migration/API — **P04** (this order forbids backend/schema change; the layout store must be in-memory/session only).
- Overlay/Notification/Dialog Region-F three-layer split — **P05** (OBS-P01-4/F-2).
- Full command-palette behaviour — **P05**.
- Legacy `TerminalLayout` retirement — **P06**.
- New business panels / new trading/research capability (register only existing shell panels).

## 4. Constitutional & architectural guardrails (all binding)
- **UG-1/UG-2/R-3** — no execution/actuation in any panel, docking control, or layout control (grep source clean + browser). Panels are presentation only.
- **UG-3/R-1** — no backend/API/alembic/schema/pyproject/requirements change; head `20260717_0037` unchanged; UI-only diff. **No new dependency without a wheel-compat spike (UG-15)** — if a docking/layout lib is proposed, it needs a dependency spike + ITRGA sign-off BEFORE use; prefer a first-party implementation.
- **Doc 14 §10 / Part VI §17** — panel infra is presentation-oriented infrastructure only: no business workflows, no duplicated workspace logic, no backend communication, no Shell-Event-Bus bypass, no hardcoded workspace-specific layouts, **no independent persistence system**.
- **No regression** — every current route + all P01/P02 shell/nav tests still green.

## 5. MANDATORY EVIDENCE (operator-run on target; blank/errored grep or variable = R7 non-result)
**(a) Build-identity** — `sed -n '1,15p'` of the P03 delivery report; confirm it is OF P03 (grep P03 markers, not a stale P01/P02 re-attach).
**(b) Panel Registration Contract proof** — grep the panel-metadata **type** showing all 13 canonical fields + guard `noActuation`; grep the registry listing the initial registered panels; prove "only registered panels participate" (registry-driven, not hardcoded).
**(c) Deterministic docking proof** — a test showing the same layout descriptor yields the same arrangement; docking primitives present.
**(d) Named tests (MUST be DISPLAYED passing by name — verbose reporter):**
  - `test_panel_registry_only_registered_panels_participate`
  - `test_docking_engine_placement_is_deterministic`
  - `test_layout_manager_serialize_restore_roundtrip_no_persistence_backend`
  - `test_panel_infrastructure_contains_no_execution_or_actuation`
**(e) No-actuation grep on panel/docking/layout SOURCE (test files excluded)** — clean.
**(f) No-backend-persistence proof** — grep proving the layout store is in-memory/session (no `fetch`/API call, no `operator_workspace_preferences`, no `/api/v1/` in panel/layout source); empty `git diff -- backend\app backend\alembic backend\pyproject.toml backend\requirements.txt`.
**(g) Regression** — backend `pytest -q` **≥413 passed**; frontend Vitest **>23f/80t** all passing; TS clean; build + bundle delta.
**(h) Alembic head** — `alembic current` **printing `20260717_0037`**.
**(i) Browser (served session)** — shots: a workspace with panels docked in Regions C/D/E; a **resize** interaction; a **workspace transition** showing layout swap/restore; keyboard focus on a panel; Gate CLOSED/research framing intact; logged-out block.
**(j) Local CI** — **run the consolidated wrapper** `& "C:\Program Files\Git\bin\bash.exe" scripts/local_ci.sh` and paste inline `LOCAL_CI_EXIT_CODE:` + the `==> Local CI equivalent complete` sentinel (closes OBS-P02-2). If the offline-audit TD-W6-CI-AUDIT flake surfaces AFTER substantive gates green, record it — never relabel green; disposition via operator.
**(k) OBS-P02-1 closure** — re-run the registry route-count check via a **here-doc or `.js` file** (not an escaped inline `-e`) so `REGISTRY_ROUTE_COUNT: 15` prints cleanly.

## 6. Acceptance criteria (Determination: Approved · Approved with Observations · Corrective Actions Required · Rejected)
**Approved** requires: build-identity confirmed; (b) panel contract + registry proven; (c)/(d) deterministic docking + all four named tests displayed passing; (e) source no-actuation clean; (f) no-backend-persistence proven + empty backend diff; (g) regression green with actual totals (backend ≥413, frontend grown); (h) head unchanged; (i) browser confirms docking/resize/transition/framing/logged-out; no barred/unspiked dependency; build succeeds; (j) CI wrapper exit 0 (or waived env-flake) + sentinel; (k) OBS-P02-1 closed. **Only Approved / Approved-with-Observations authorizes `BUILD_ORDER_UI-001-P04` (Workspace Persistence via `operator_workspace_preferences`, R-4).**

*We don't guess. We prove.*
