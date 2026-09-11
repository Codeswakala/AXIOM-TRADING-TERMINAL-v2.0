# BUILD ORDER — UI-001-P06 (FINAL)
## Legacy `TerminalLayout` Retirement · Migration Completion · UI-001 Completion Checkpoint

**Issuing authority:** Institutional Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-001 · **Phase:** P06 (final)
**Predecessor:** `ITRGA_REVIEW_UI-001-P05.md` — **APPROVED (CLEAN)** (authorizes this order)
**Governing spec:** `15_UI-001_IMPLEMENTATION_SPECIFICATION.md` **§11 Definition of Completion**, **Part II §5 Legacy UI Assessment**, **Part IX §13–§15, §17–§20** (Regression / Operator Acceptance / Constitutional Validation / Acceptance / Formal Acceptance / ITRGA Final Review); Doc 14 (whole).
**Baseline (must be unchanged):** platform v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 26f/94t.
**Motto:** *We don't guess. We prove.*

---

## 1. Objective
Complete UI-001: **retire the legacy `TerminalLayout`** (dead since P01 replaced the active frame) and any orphaned legacy layout code, **complete migration** so the Institutional Workspace Shell is the *sole* application frame, and satisfy the **Doc 15 §11 completion checkpoint** + **Part IX formal acceptance**. Presentation only: **no new backend/API/schema/ML/governance, no new capability, Gate CLOSED, no execution/actuation anywhere.**

## 2. Scope IN
1. **Legacy `TerminalLayout` retirement (Part II §5)** — remove `TerminalLayout` and any now-dead legacy layout/nav files it depended on; delete unused imports/routes; ensure **no reachable code path** renders the legacy frame. Grep must prove `TerminalLayout` is gone from source (or reduced to nothing referenced).
2. **Sole-frame proof** — the shell is the *only* protected application frame; no duplicate/competing layout remains (Doc 14 §10). All 15 routes render **only** through `InstitutionalWorkspaceShell` → `WorkspaceHost`.
3. **Migration completion** — remove any transitional shims/aliases introduced across P01–P05 that are no longer needed; no orphaned dead code.
4. **UI-001 completion deliverable** — a completion summary mapping the delivered infrastructure to Doc 15 §18 (Shell, Navigation, Registry, Panels, Docking, Layout Manager, Routing, State, Session Coordination, Design System) and confirming Doc 14 conformance.

## 3. Scope OUT (do NOT implement)
- Any NEW workspace/feature/business capability (UI-001 is infrastructure only; future = UI-002+).
- Any new table/migration/schema/column; any execution/actuation/broker/account/Gate surface; external AI.
- The Production Readiness Certification (separate future track, Doc 11 — HELD).

## 4. Constitutional & architectural guardrails (binding)
- **UG-1/UG-2/R-3** — no execution/actuation anywhere; retirement removes code, adds none.
- **UG-3/R-1/R-4** — no backend/API/alembic/schema change; head `20260717_0037` unchanged; no new dependency (UG-15); removals only.
- **Doc 14 §10** — one integrated environment; after retirement, exactly one frame.
- **No regression** — the retirement must not break any route or test; every P01–P05 test + all existing suites stay green.

## 5. MANDATORY EVIDENCE (operator-run on target; blank/errored grep = R7 non-result)
**(a) Build-identity** — `sed -n '1,15p'` of the P06 delivery report; confirm it is OF P06 (grep P06 markers, not a stale re-attach — I will check).
**(b) Legacy retirement proof** — grep over `frontend/src` for `TerminalLayout` → **no output** (or only a tombstone comment); grep confirming no route/import references it; the file removed (Test-Path → False or file deleted in `git diff`).
**(c) Sole-frame proof** — grep/test showing every protected route mounts through `InstitutionalWorkspaceShell`/`WorkspaceHost` and NO other layout frame exists; a test `test_terminal_layout_retired_shell_is_sole_frame`.
**(d) UI-only removal diff** — `git diff --stat` showing frontend-only removals; empty `git diff -- backend\app backend\alembic backend\pyproject backend\requirements frontend\package.json frontend\package-lock.json` (no backend/schema/dep change); `alembic current` = `20260717_0037`.
**(e) Regression (Part IX §13) — 8 subsystems unaffected** — backend `pytest -q` **≥414 passed** (auth, RBAC, market data, research, execution-research, intelligence, portfolio, governance suites all green); frontend Vitest **≥ prior count, all passing, no test lost** (retirement may reduce file count if legacy tests removed — if so, state which and why, and net must not drop coverage of live routes); TS clean; build + bundle delta (expect a size **decrease** from dead-code removal).
**(f) Route-by-route in-shell (Part IX §14 operator acceptance)** — browser walkthrough of representative workflows still working in-shell: market review, signal investigation, scenario comparison, trade planning, journaling, execution-research review, portfolio analysis, governance review — **uninterrupted**.
**(g) No-actuation source grep (whole shell)** — clean (tests excluded).
**(h) Named tests (MUST be DISPLAYED passing by name — verbose reporter):**
  - `test_terminal_layout_retired_shell_is_sole_frame`
  - `test_all_routes_mount_only_through_workspace_shell_no_regression`
  - `test_shell_contains_no_execution_or_actuation_after_retirement`
**(i) Browser (served session)** — shots: representative workspaces in-shell post-retirement; Gate CLOSED/research framing; logged-out block. (No legacy frame anywhere.)
**(j) Local CI — networked** — `& "C:\Program Files\Git\bin\bash.exe" scripts/local_ci.sh` → `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0`.
**(k) 🔴 UI-001 COMPLETION CHECKPOINT (Doc 15 §11 / Part IX §15, §19–20)** — the delivery report must present the DA's formal-acceptance self-check (§19) AND assert the §11 completion conditions; ITRGA will independently apply the **Part IX §15 Constitutional Validation** checklist (hierarchy respected · no roadmap expansion · no unauthorized business functionality · governance preserved · research-only preserved · no execution pathways · UI Transformation scope respected · **Gate CLOSED**).

## 6. Acceptance criteria (Determination: Approved · Approved with Observations · Corrective Actions Required · Rejected)
**Approved** requires: build-identity confirmed; (b) TerminalLayout retired (grep clean / file removed); (c) sole-frame proven + `test_terminal_layout_retired_shell_is_sole_frame` passing; (d) UI-only removal diff + empty backend/dep diff + head unchanged; (e) regression green across the 8 subsystems with actual totals (backend ≥414); (f)/(i) browser operator-acceptance walkthrough uninterrupted; (g) whole-shell no-actuation clean; (h) three named tests displayed passing; (j) networked CI exit 0 + sentinel; (k) §11 completion conditions met + ITRGA §15 constitutional validation clean.

**On Approved: ITRGA will declare 🏛️ UI-001 COMPLETE** (Institutional Workspace Shell = permanent application frame, conforms to Doc 14, regression passed, ITRGA final review complete per Doc 15 §11/§20). Future work = UI-002+ (new Design Plan) and, separately, the Production Readiness Certification track (Doc 11). **UI-001 completion does NOT open the Gate or authorize execution.**

*We don't guess. We prove.*
