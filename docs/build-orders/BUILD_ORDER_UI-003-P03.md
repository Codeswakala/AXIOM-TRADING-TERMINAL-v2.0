# BUILD ORDER — UI-003-P03
## Chart Overlays · Research Markers · Annotation Integration (inert read-only — R-3)

**Issuing authority:** Institutional Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-003 · **Phase:** P03
**Predecessor:** `ITRGA_REVIEW_UI-003-P02.md` — **APPROVED** (authorizes this order)
**Governing:** Doc 12 §5; existing chart constitution (W0 candlesticks / **W5-U03 inert `chart_research_annotations`**); design plan §7/§10 (UI-003-P03); binding refinements **R-3/R-6**.
**Baseline (must be unchanged):** v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 33f/137t.
**Motto:** *We don't guess. We prove.*

---

## 1. Objective
Integrate **existing** governed annotations and **read-only** research markers as professional chart overlays — **inert presentation of existing artifacts, no generation/inference.** Presentation only: no new analysis/computation, no signal generation, no execution/actuation, Gate CLOSED.

## 2. Scope IN (per accepted plan UI-003-P03)
1. **Overlay visibility controls** — presentation toggles only (show/hide annotations, research markers, provenance) via existing token/preference state.
2. **W5-U03 annotation layer presentation hardening** — display **existing** `chart_research_annotations` (via `fetchChartResearchAnnotations` / `ChartResearchAnnotationLayer`); keep inert operator-authored annotation creation **only where already authorized** by the existing W5-U03 API (no new create capability).
3. **🔴 Optional read-only advisory-signal markers (R-3)** — display markers **from the existing advisory-signal read API** as **inert read-only badges**; **no generation, no inference, no mutation.** Markers are NOT signals/instructions/orders.
4. **Marker list alternative** for accessibility (non-visual equivalent of chart markers).
5. **Provenance + research-only labels** — every overlay/marker carries provenance + uncertainty + research-only labeling.

## 3. Scope OUT (do NOT implement)
- Any **signal generation / inference / authoritative recompute / new analytical algorithm**; any NEW annotation-creation capability beyond existing W5-U03; any new markers not sourced from an existing read API.
- Market status full/overview/responsive — P04. Any new backend/API/schema/migration/column/dependency; any execution/actuation/AI; any real/live-market data.

## 4. Constitutional & architectural guardrails (binding)
- **🔴 R-3 (spine)** — overlays/markers render **existing** governed artifacts **read-only**; markers are inert badges, not signals/instructions; **no generation/inference/mutation** (grep + named tests).
- **Overlay controls = presentation toggles only** (no data mutation, no compute).
- **Provenance/uncertainty/research-only labels preserved & visible** (Doc 12 Part V; never color alone).
- **UG-1/UG-2** — no execution/actuation on the overlay surface.
- **UG-3/UG-15/R-6** — no backend/API/schema change; no new dependency; head `20260717_0037`; UI-only (no-drift substitute); Level-I bar.
- **Accessibility first-class** (marker-list alternative; keyboard/screen-reader for overlay toggles). **No regression.**

## 5. MANDATORY EVIDENCE (operator-run on target; blank/errored grep = R7 non-result)
**(a) Build-identity** — `sed -n '1,15p'` of the P03 delivery report; confirm it is OF UI-003-P03.
**(b) Named tests (MUST be DISPLAYED passing by name — verbose reporter):**
  - `test_ui003_overlays_render_existing_annotations_read_only`
  - `test_ui003_research_markers_use_existing_read_artifacts_no_inference`
  - `test_ui003_overlay_controls_are_presentation_toggles_only`
  - `test_ui003_markers_preserve_provenance_uncertainty_and_research_only_labels`
  - `test_ui003_overlays_contain_no_signal_generation_or_actuation`
**(c) 🔴 R-3 read-only / no-generation proof** — grep/test showing overlay & marker source consumes only **existing** read APIs (`fetchChartResearchAnnotations`, advisory-signal read API) and performs **no** generation/inference/`emitSignal`/authoritative-recompute; markers are inert (no onClick that acts).
**(d) No-actuation source grep** — overlay/marker source (tests excluded): `buy|sell|place_order|execute|go-live|connect-broker|account_id|order_ticket|open_gate|allow_execution|emitSignal|inferSignal|runInference` → clean.
**(e) Provenance/research-only label proof** — grep/test that markers/overlays render provenance + uncertainty + research-only labels.
**(f) No-drift substitute (R-6)** — per-phase no-backend/schema/dep test; `alembic current` = `20260717_0037`; **`package.json`/`package-lock.json` content unchanged**; no-new-endpoint grep.
**(g) Regression** — backend `pytest -q` **≥414 passed**; frontend Vitest **>33f/137t** all passing; TS clean; build + bundle delta.
**(h) Browser (served session) — R-6** — shots: chart with **overlay visibility toggles**; existing annotations rendered (research-only); **read-only signal markers** as inert badges with provenance; **marker-list accessibility alternative**; keyboard overlay toggle; Gate CLOSED/research framing; logged-out block.
**(i) Networked CI (R-6)** — `scripts/local_ci.sh` → `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0` (or the TD-W6-CI-AUDIT offline-audit env-flake AFTER substantive gates green — record; disposition via operator).

## 6. Acceptance criteria (Determination: Approved · Approved with Observations · Corrective Actions Required · Rejected)
**Approved** requires: build-identity confirmed; (b) all five named tests displayed passing; (c) R-3 read-only/no-generation proven; (d) no-actuation grep clean; (e) provenance/research-only labels rendered; (f) no-drift substitute + head unchanged + no new dependency; (g) regression green with actual totals; (h) browser overlays/markers/marker-list/keyboard + framing/logged-out; (i) networked CI exit 0 + sentinel (or waived env-flake). **Only Approved / Approved-with-Observations authorizes `BUILD_ORDER_UI-003-P04` (Market Status, Overview & Responsive Professional Layout).**

*We don't guess. We prove.*
