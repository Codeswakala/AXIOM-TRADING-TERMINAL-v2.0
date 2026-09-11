# BUILD ORDER — UI-004-P02b
## Performance Analytics Integration (no-cherry-picking · no-recompute · read-only)

**Issuing authority:** Institutional Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-004 · **Phase:** P02b (analytics split from P02 per R-3)
**Predecessor:** `ITRGA_REVIEW_UI-004-P02.md` — **APPROVED** (authorizes this order)
**Governing:** Doc 12 §6; W6 analytics constitution (no-cherry-picking; uncertainty/sample-counts); design plan §2.3/§7.3/§12 (analytics portion of UI-004-P02); binding refinements **R-3/R-6/R-7**; **Doc 16 brand gate (B-1…B-7)**.
**Baseline (must be unchanged):** v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 38f/161t.
**Motto:** *We don't guess. We prove.*

---

## 1. Objective
Integrate **existing Performance Analytics** into the Research & Intelligence workspace as a **read-only** surface that **displays governed metrics with uncertainty and sample counts** — the **no-cherry-picking** surface. Presentation only: no recompute/inference, no aggregate computed from displayed rows, no new backend/API/schema/dependency, no execution, Gate CLOSED.

## 2. Scope IN
1. **Analytics metric / confidence-band panels** from existing `fetchAdvisoryAnalytics` — display existing metrics, calibrated confidence bands, sample counts, uncertainty.
2. **Signal → analytics context links** (read-only navigation) tying the P02 advisory surface to analytics.
3. **No-cherry-picking rendering** — included scope, sample counts, source-artifact ids, uncertainty, and limitations surfaced; unreliability/low-sample warnings shown; filtered views must not claim full-scope performance unless the stored report declares that scope.

## 3. Scope OUT (do NOT implement)
- Report viewers/drilldowns — P03. Validation/economic panels — P04. Saved-view persistence — P05 (R-2). Collections mutation — never (R-4).
- **Any client-side aggregate/metric computed from displayed rows**; any recompute/inference/re-derivation of analytics/confidence; raw-score-as-confidence; any new backend/API/schema/dependency; any execution/actuation/AI; any registry change.

## 4. Constitutional & architectural guardrails (binding)
- **🔴 R-6 no-recompute (spine)** — analytics rendered as stored from `fetchAdvisoryAnalytics`; **no client-side computation of aggregates/metrics/confidence** (grep + named test).
- **🔴 No-cherry-picking (W6 discipline)** — sample counts, uncertainty, limitations, included scope, source-artifact ids visible; **no code path computes new aggregate performance from displayed rows** (named test); low-sample/unreliability warnings preserved; filtered UI labels do not claim full-scope truth.
- **Calibrated confidence, not raw score** — confidence bands from stored calibrated fields.
- **Extend-not-duplicate** — reuse existing `PerformanceAnalyticsPage`/`fetchAdvisoryAnalytics` + UI-001/UI-002 shell/nav; no second nav/palette/overlay; **no browser-side analytics engine**; reuse Design System tokens.
- **UG-3/UG-15** — no backend/API/schema change; no new dependency; head `20260717_0037`; UI-only (no-drift substitute); no registry change.
- **🔴 Doc 16 brand (B-1…B-7)** — palette / typography+monospace (metrics/sample-counts/confidence) / iconography / institutional-not-retail / a11y (dense analytics tables).
- **Accessibility first-class**; **no regression**.

## 5. MANDATORY EVIDENCE (operator-run on target; blank/errored grep = R7 non-result)
**(a) Build-identity** — `sed -n '1,15p'` of the P02b delivery report; confirm it is OF UI-004-P02b (analytics).
**(b) Named tests (MUST be DISPLAYED passing by name — verbose reporter):**
  - `test_ui004_analytics_render_existing_metrics_with_uncertainty_and_sample_counts`
  - `test_ui004_analytics_do_not_recompute_or_cherry_pick` *(no aggregate computed from displayed rows)*
  - `test_ui004_analytics_surfaces_contain_no_execution_order_or_gate_path`
  - `test_ui004_analytics_accessibility_and_brand_markers_hold`
**(c) 🔴 No-recompute / no-cherry-picking proof (R-6 + W6)** — grep/test: analytics source uses `fetchAdvisoryAnalytics` only; no `inferSignal|runInference|authoritativeRecompute|recompute|recalculat|reduce\(|aggregate|deriveConfidence|new .*Engine`; a **named test proving no aggregate is computed from displayed rows** + sample-counts/uncertainty/limitations visible.
**(d) No-actuation source grep** — analytics source (tests excluded) → clean.
**(e) No-drift substitute (R-7)** — per-phase no-backend/schema/dep test; `alembic current` = `20260717_0037`; package manifests unchanged; no-new-endpoint grep; no registry change.
**(f) Regression (R-7)** — backend `pytest -q` **≥414 passed**; frontend Vitest **FULL SUITE ≥38f/161t all passing, NO test lost** (verify the full-suite total, not a filtered run); TS clean; build + bundle delta.
**(g) 🔴 Doc 16 brand (B-1…B-7)** — grep/test + browser: palette/typography+monospace/iconography/institutional-not-retail; no-hardcoded-color grep clean.
**(h) Browser (served session) — R-7** — shots: analytics metric/confidence-band panels with **sample counts + uncertainty + limitations + unreliability warnings visible**; signal→analytics context link; no action controls; Gate CLOSED/research framing + brand; logged-out block.
**(i) Networked CI (R-7)** — `scripts/local_ci.sh` → `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0` (or the TD-W6-CI-AUDIT offline-audit env-flake AFTER substantive gates green — record; disposition via operator).

## 6. Acceptance criteria (Determination: Approved · Approved with Observations · Corrective Actions Required · Rejected)
**Approved** requires: build-identity confirmed; (b) named tests displayed passing; (c) no-recompute + **no-cherry-picking proven (no aggregate from displayed rows; sample-counts/uncertainty/limitations/scope visible)**; (d) no-actuation grep clean; (e) no-drift + head unchanged + no dep + no registry change; (f) full-suite regression **≥38f/161t, no test lost** + backend ≥414; (g) Doc 16 brand (B-1…B-7); (h) browser analytics with uncertainty/sample-counts/warnings + framing + brand + logged-out; (i) networked CI exit 0 + sentinel (or waived env-flake). **Only Approved / Approved-with-Observations authorizes `BUILD_ORDER_UI-004-P03` (Intelligence Report Viewers & Drilldowns).**

*We don't guess. We prove.*
