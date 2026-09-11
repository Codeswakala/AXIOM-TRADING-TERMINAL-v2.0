# BUILD ORDER — UI-004-P02
## Advisory Signals Integration (read-only · calibrated-confidence · non-actionable — R-3 split, advisory only)

**Issuing authority:** Institutional Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-004 · **Phase:** P02
**Predecessor:** `ITRGA_REVIEW_UI-004-P01.md` — **APPROVED** (authorizes this order)
**Governing:** Doc 12 §6; W3 advisory-signals constitution (guardrails/calibrated-confidence/lineage/freshness/disclaimers); design plan §2.4/§8/§12 (UI-004-P02); binding refinements **R-3/R-6/R-7**; **Doc 16 brand gate (B-1…B-7)**.
**Baseline (must be unchanged):** v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 37f/156t.
**Motto:** *We don't guess. We prove.*

---

## 1. Objective
Integrate **existing advisory signals** into the Research & Intelligence workspace as a **read-only, calibrated-confidence, non-actionable** research surface. Per **R-3, this phase is ADVISORY SIGNALS ONLY** — **Performance Analytics is split to P02b** for a narrower no-cherry-picking review. Presentation only: no recompute/inference, no new backend/API/schema/dependency, no execution/actuation, Gate CLOSED.

## 2. Scope IN (R-3 split — advisory only)
1. **Read-only advisory signal cards/details** — from existing `fetchAdvisorySignals`/`fetchAdvisorySignal`; integrated into the research workflow with links to related reports/context.
2. **Guardrail/calibration fidelity** — preserve signal state + state reason, rationale, lineage, model/report ids, freshness/expiry, **calibrated confidence (NOT raw-score-as-confidence)**, economic verdict, operating-domain + calibration status.
3. **Disclaimers + non-actionable presentation** — "not financial advice / not a trade instruction / operator decides"; no action controls.
4. **Signal → context links** (to reports/investigation) as read-only navigation.

## 3. Scope OUT (do NOT implement)
- **Performance Analytics integration — P02b (R-3).** Report viewers/drilldowns — P03. Validation/economic panels — P04. Saved-view persistence — P05 (R-2). Collections/tags mutation — never (R-4).
- Any recompute/inference/re-derivation/signal-generation; **raw-score-as-confidence** (forbidden); any new backend/API/schema/dependency; any execution/actuation/AI; any registry change (unless pre-approved).

## 4. Constitutional & architectural guardrails (binding)
- **🔴 R-6 no-recompute/no-inference (spine)** — signals rendered as stored; no re-derivation of confidence/verdict/state; **calibrated confidence displayed, never raw score relabeled as confidence** (grep + named test).
- **Advisory posture (R-2.4)** — read-only, non-actionable; disclaimers preserved.
- **No-cherry-picking readiness** — signal lists show state/freshness honestly; no favorable-only filtering presented as full truth.
- **Extend-not-duplicate** — reuse existing `AdvisorySignalsPage`/APIs + UI-001/UI-002 shell/nav; no second nav/palette/overlay; reuse Design System tokens.
- **UG-3/UG-15** — no backend/API/schema change; no new dependency; head `20260717_0037`; UI-only (no-drift substitute); **no registry change**.
- **🔴 Doc 16 brand (B-1…B-7)** — constitutional palette / typography+monospace (ids/confidence/freshness) / iconography / institutional-not-retail / a11y.
- **Accessibility first-class**; **no regression** (all prior tests green).

## 5. MANDATORY EVIDENCE (operator-run on target; blank/errored grep = R7 non-result)
**(a) Build-identity** — `sed -n '1,15p'` of the P02 delivery report; confirm it is OF UI-004-P02 (advisory only).
**(b) Named tests (MUST be DISPLAYED passing by name — verbose reporter):**
  - `test_ui004_signals_render_existing_records_read_only_with_guardrails`
  - `test_ui004_signals_and_analytics_do_not_recompute_or_cherry_pick` *(advisory portion — analytics assertions land at P02b)*
  - `test_ui004_signal_surfaces_contain_no_execution_order_or_gate_path`
  - `test_ui004_signal_analytics_accessibility_and_brand_markers_hold` *(advisory/brand portion)*
  - plus a calibrated-confidence integrity test: `test_ui004_signals_show_calibrated_confidence_not_raw_score` (or equivalent named assertion)
**(c) 🔴 No-recompute + calibrated-confidence proof (R-6)** — grep/test: signal source uses `fetchAdvisorySignals` only; no `inferSignal|emitSignal|recompute|deriveConfidence|rawScore.*confidence`; calibrated confidence rendered from the stored calibrated field.
**(d) No-actuation source grep** — signal source (tests excluded): `buy|sell|place_order|execute|go-live|connect-broker|account_id|order_ticket|open_gate|allow_execution` → clean.
**(e) Guardrail/disclaimer render proof** — grep/test that state/rationale/lineage/freshness/economic-verdict/calibration-status + "not financial advice/not a trade instruction/operator decides" render.
**(f) No-drift substitute (R-7)** — per-phase no-backend/schema/dep test; `alembic current` = `20260717_0037`; package manifests unchanged; no-new-endpoint grep; no registry change.
**(g) Regression (R-7)** — backend `pytest -q` **≥414 passed**; frontend Vitest **FULL SUITE ≥37f/156t all passing, NO test lost** (verify the full-suite total, not a filtered run); TS clean; build + bundle delta.
**(h) 🔴 Doc 16 brand (B-1…B-7)** — grep/test + browser: palette/typography+monospace/iconography/institutional-not-retail; no-hardcoded-color grep clean.
**(i) Browser (served session) — R-7** — shots: advisory signal cards/detail read-only in the research workspace; **calibrated confidence** + guardrails + disclaimers visible; no action controls; Gate CLOSED/research framing + brand; logged-out block.
**(j) Networked CI (R-7)** — `scripts/local_ci.sh` → `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0` (or the TD-W6-CI-AUDIT offline-audit env-flake AFTER substantive gates green — record; disposition via operator).

## 6. Acceptance criteria (Determination: Approved · Approved with Observations · Corrective Actions Required · Rejected)
**Approved** requires: build-identity confirmed (advisory-only scope); (b) named tests displayed passing (incl. calibrated-confidence-not-raw-score); (c) no-recompute + calibrated-confidence proven; (d) no-actuation grep clean; (e) guardrails/disclaimers rendered; (f) no-drift + head unchanged + no dep + no registry change; (g) full-suite regression **≥37f/156t, no test lost** + backend ≥414; (h) Doc 16 brand (B-1…B-7); (i) browser advisory read-only + framing + brand + logged-out; (j) networked CI exit 0 + sentinel (or waived env-flake). **Only Approved / Approved-with-Observations authorizes `BUILD_ORDER_UI-004-P02b` (Performance Analytics integration; no-cherry-picking focus).**

*We don't guess. We prove.*
