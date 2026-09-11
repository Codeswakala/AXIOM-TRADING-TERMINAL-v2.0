# BUILD ORDER — UI-003-P05 (FINAL)
## UI-003 Completion Checkpoint (integration evidence · constitutional + brand validation)

**Issuing authority:** Institutional Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-003 · **Phase:** P05 (final)
**Predecessor:** `ITRGA_REVIEW_UI-003-P04.md` — **APPROVED** (authorizes this order)
**Governing:** Doc 12 §5; design plan §10 (UI-003-P05) + §11; binding refinement **R-6**; **Doc 16 Brand Governance Standard Part XIV (B-1…B-7)**.
**Baseline (must be unchanged):** v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 35f/146t.
**Motto:** *We don't guess. We prove.*

---

## 1. Objective
Provide **final integration evidence** and bring UI-003 to its **completion checkpoint**: the Professional Market Workspace is chart-centered on the UI-001/UI-002 shell, presentation-only, constitutionally clean, and brand-compliant. No new capability. Gate CLOSED.

## 2. Scope IN (per accepted plan UI-003-P05)
1. **Route/browser integration evidence** across the market workspace (chart · overview/status · watchlist · overlays/markers) inside the shell.
2. **Whole-surface no-actuation grep** across all UI-003 market source.
3. **Completion regression** (backend + frontend, no loss).
4. **Watchlist persistence proof** (P02 raw psql read-back reaffirmed — symbol-ids-only row, if practical include a fresh save→SELECT).
5. **Final constitutional self-check** + **Doc 16 brand self-check**.

## 3. Scope OUT (do NOT implement)
- Any new capability / analysis / feed / backend / schema / dependency / execution / AI. Production certification (separate Doc-11 track, HELD).

## 4. Constitutional & architectural guardrails (binding)
- **Presentation-only / no new analysis / no live-real data / no execution** across the whole market surface (grep + tests).
- **Extend-not-duplicate** — single UI-001 shell + UI-002 navigation; no competing systems.
- **R-6** — Level-I bar; head `20260717_0037`; no new dependency; no-drift substitute.
- **🔴 Doc 16 brand gate (B-1…B-7)** — logo/monogram · constitutional palette (no off-palette / no new hardcoded brand color) · typography + monospace numerics · unified iconography · institutional-not-retail identity · brand accessibility · documentation branding. **UI shall not be approved where brand standards are violated (Doc 16 Part XIV).**
- **Gate CLOSED**; research-only posture preserved.

## 5. MANDATORY EVIDENCE (operator-run on target; blank/errored grep = R7 non-result)
**(a) Build-identity** — `sed -n '1,15p'` of the P05 delivery report; confirm it is OF UI-003-P05.
**(b) Named tests (MUST be DISPLAYED passing by name — verbose reporter):**
  - `test_ui003_completion_chart_workspace_is_operational_center_without_scope_expansion`
  - `test_ui003_completion_all_market_surfaces_are_presentation_only`
  - `test_ui003_completion_no_live_real_data_broker_execution_or_gate_path`
  - `test_ui003_completion_accessibility_responsive_and_registry_integration_hold`
  - `test_ui003_completion_regression_preserves_backend_and_ui002_navigation`
**(c) Whole-surface no-actuation grep** — all UI-003 market source (tests excluded): `buy|sell|place_order|execute|go-live|connect-broker|account_id|order_ticket|open_gate|allow_execution|emitSignal|inferSignal` → clean.
**(d) Watchlist persistence reaffirmation** — raw `psql SELECT` on `operator_workspace_preferences WHERE workspace_key='professional-market-workspace-v1'` showing ≥1 row, `watchlists` = symbol/timeframe ids only, no forbidden fields (reaffirms P02; API read-back does not substitute).
**(e) No-drift substitute (R-6)** — per-phase no-backend/schema/dep test; `alembic current` = `20260717_0037`; `package.json`/`package-lock.json` unchanged; no-new-endpoint grep.
**(f) Regression (completion)** — backend `pytest -q` **≥414 passed**; frontend Vitest **≥35f/146t** all passing (no test lost); TS clean; build + bundle delta.
**(g) 🔴 Doc 16 brand self-check + browser proof (B-1…B-7)** — evidence that the market workspace uses the constitutional palette / typography / monospace numerics / unified iconography / institutional-not-retail identity; no off-palette brand color (a no-hardcoded-color style grep is acceptable corroboration); documentation branding for the completion pack.
**(h) Browser (served session) — R-6** — route-by-route market workspace (chart · overview/status · watchlist · overlays) inside the shell; **responsive (narrow-width)**; keyboard walkthrough; provenance/`live:simulated` labels; Gate CLOSED/research framing; logged-out block.
**(i) Networked CI (R-6)** — `scripts/local_ci.sh` → `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0` (or the TD-W6-CI-AUDIT offline-audit env-flake AFTER substantive gates green — record; disposition via operator).
**(j) 🔴 UI-003 COMPLETION CHECKPOINT** — the delivery report presents the DA's completion self-check; ITRGA will independently apply the **constitutional validation** (hierarchy · no scope expansion · no new analysis/live-data/capability · governance preserved · research-only · no execution pathways · UI-001/UI-002 unmodified · single shell · **Gate CLOSED**) **AND the Doc 16 brand validation (B-1…B-7)**.

## 6. Acceptance criteria (Determination: Approved · Approved with Observations · Corrective Actions Required · Rejected)
**Approved** requires: build-identity confirmed; (b) all five named tests displayed passing; (c) whole-surface no-actuation grep clean; (d) watchlist persistence reaffirmed (raw psql ≥1 clean row); (e) no-drift substitute + head unchanged + no new dependency; (f) completion regression green with actual totals; **(g) Doc 16 brand self-check + browser proof pass (B-1…B-7 — a material brand violation ⇒ Corrective per Part XIV)**; (h) route-by-route + responsive + keyboard browser evidence; (i) networked CI exit 0 + sentinel (or waived env-flake); (j) constitutional + brand completion validation clean.

**On Approved: ITRGA will declare 🏛️ UI-003 — PROFESSIONAL MARKET WORKSPACE — COMPLETE** (chart-centered market observation on the UI-001/UI-002 shell; presentation-only; Doc 12 §5 / Doc 14 / **Doc 16** conformant; regression passed; ITRGA review complete). Future: UI-004+ (each needs its own Design Plan → Build Order → review) and, separately, the Production Readiness Certification track (Doc 11, HELD). **UI-003 completion does NOT open the Gate or authorize execution.**

*We don't guess. We prove.*
