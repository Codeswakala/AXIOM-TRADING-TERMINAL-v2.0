# BUILD ORDER — UI-003-P01
## Professional Market Workspace Frame · Data-Source Inventory · Non-Authoritative Market Presentation

**Issuing authority:** Institutional Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-003 (Professional Market Workspace) · **Phase:** P01
**Predecessor:** `ITRGA_REVIEW_UI-003_DESIGN_PLAN.md` — **APPROVED WITH OBSERVATIONS + BINDING REFINEMENTS (R-1…R-6)** (authorizes this order)
**Governing:** Doc 12 §5; existing chart constitution (W0 candlesticks / W5-U03 inert annotations); design plan §2/§5/§10 (UI-003-P01); binding refinement **R-6**.
**Baseline (must be unchanged):** v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 31f/127t.
**Motto:** *We don't guess. We prove.*

---

## 1. Objective
Establish the **professional market workspace frame** inside the UI-001/UI-002 shell — chart-centered Region C composition with market overview/status **placeholders using existing data** and **explicit source-provenance labels** — **without capability expansion.** Presentation only: **no new analysis/computation/live-real-data, no new backend/API/schema/dependency, no execution/actuation, Gate CLOSED.**

## 2. Scope IN (per accepted plan UI-003-P01)
1. **Chart-centered Region C composition** — recompose the existing `/charts` (or a new market-workspace route) inside the shell using **existing** chart component (`lightweight-charts` / `PriceChart` / `useChartData`); mount via the 14-field Workspace Registry; navigation via UI-002 (no page-specific nav).
2. **Market overview / status placeholders** — present existing market/health/readiness/live-status data (reuse `useLiveMarket` / `LivePriceTable` / status surfaces); **no new data source.**
3. **Explicit source-provenance labels** — `seed:synthetic` = non-authoritative chart context; `live:simulated` = simulated/governed; CSV ingest labels; **never label simulated data as real** (must be visible in browser).
4. Accessible chart summary + controls.

## 3. Scope OUT (do NOT implement in P01)
- **Watchlist persistence** — P02 (R-1/R-2). **Chart overlays / research markers / advisory-signal markers / annotation integration** — P03 (R-3). Market-status full build / responsive polish — P04.
- Any new analytical computation / client-side inference / signal generation / regime inference / new algorithm; any real/live market feed; any broker/account/execution; any external AI; any new backend/API/schema/migration/column; any new dependency (reuse `lightweight-charts` — a new charting dep needs a spike + ITRGA sign-off).
- Any modification to UI-001/UI-002 architectural responsibilities.

## 4. Constitutional & architectural guardrails (binding, R-6)
- **🔴 Presentation, NOT new analysis** — display existing values only; no compute/derive/infer/recompute/generate. Grep + named test.
- **🔴 Market-data posture** — provenance labels preserved & visible; simulated/governed data never labeled real.
- **UG-1/UG-2/R-3(UI-002)** — no execution/actuation on the market surface (grep + named test).
- **Extend-not-duplicate** — mount in the single UI-001 shell; no second shell/nav/palette/overlay/header; UI-002 nav/breadcrumbs consistent.
- **UG-3/UG-15** — no backend/API/schema change; no new dependency without a spike; head `20260717_0037`; UI-only.
- **Accessibility first-class**; **no regression** (all UI-001/UI-002 tests green).

## 5. MANDATORY EVIDENCE (operator-run on target; blank/errored grep = R7 non-result)
**(a) Build-identity** — `sed -n '1,15p'` of the P01 delivery report; confirm it is OF UI-003-P01.
**(b) Named tests (MUST be DISPLAYED passing by name — verbose reporter):**
  - `test_ui003_market_workspace_mounts_inside_single_ui001_shell`
  - `test_ui003_market_workspace_uses_existing_chart_and_market_sources_only`
  - `test_ui003_market_workspace_labels_synthetic_and_simulated_data_non_authoritative`
  - `test_ui003_market_workspace_contains_no_execution_or_actuation_controls`
  - `test_ui003_market_workspace_has_accessible_chart_summary_and_controls`
**(c) No-new-analysis proof** — grep/test showing market-workspace source calls only **existing** read/data hooks (`fetchCandles`/`useChartData`/`useLiveMarket`/status hooks) and performs **no** authoritative compute/inference/signal-gen.
**(d) No-actuation source grep** — market-workspace source (tests excluded): `buy|sell|place_order|execute|go-live|connect-broker|account_id|order_ticket|open_gate|allow_execution` → clean.
**(e) Provenance-label proof** — grep/test that `seed:synthetic`/`live:simulated` (non-authoritative) labels render; no "real market data" labeling.
**(f) Extend-not-duplicate proof** — grep/test: single UI-001 shell, no second nav/palette/overlay; mounts via registry.
**(g) No-drift (retired-git-diff substitute, R-6)** — a per-phase test/assertion of **no backend/schema/dependency change**; `alembic current` = `20260717_0037`; **`package.json`/`package-lock.json` content unchanged** (no new dependency); no-new-endpoint grep.
**(h) Regression** — backend `pytest -q` **≥414 passed**; frontend Vitest **>31f/127t** all passing; TS clean; build + bundle delta.
**(i) Browser (served session) — R-6** — shots: professional market workspace mounted in-shell (chart-centered Region C + market overview/status); **provenance labels visible** (`seed:synthetic`/`live:simulated`); no actuation controls; Gate CLOSED/research framing; logged-out block.
**(j) Networked CI (R-6)** — `scripts/local_ci.sh` → `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0`.

## 6. Acceptance criteria (Determination: Approved · Approved with Observations · Corrective Actions Required · Rejected)
**Approved** requires: build-identity confirmed; (b) all five named tests displayed passing; (c) no-new-analysis proven; (d) no-actuation grep clean; (e) provenance labels rendered; (f) single-shell/no-duplicate proven; (g) no-drift substitute + head unchanged + no new dependency; (h) regression green with actual totals; (i) browser frame + provenance + framing/logged-out; (j) networked CI exit 0 + sentinel. **Only Approved / Approved-with-Observations authorizes `BUILD_ORDER_UI-003-P02` (Watchlists via existing preferences; binds R-1 + R-2 raw-psql read-back).**

*We don't guess. We prove.*
