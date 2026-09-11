# BUILD ORDER — UI-004-P01
## Research Workspace Frame · Data-Source Inventory · No-Recompute Guardrail

**Issuing authority:** Institutional Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-004 (Research & Intelligence Workspace) · **Phase:** P01
**Predecessor:** `ITRGA_REVIEW_UI-004_DESIGN_PLAN.md` — **APPROVED WITH OBSERVATIONS + BINDING REFINEMENTS (R-1…R-7)** (authorizes this order)
**Governing:** Doc 12 §6; existing intelligence/signals/analytics constitution (W3/W4/W6, calibrated-confidence/uncertainty/economic-usefulness); design plan §2/§5/§12 (UI-004-P01); binding refinements **R-1/R-6/R-7**; **Doc 16 brand gate (B-1…B-7)**.
**Baseline (must be unchanged):** v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 36f/151t.
**Motto:** *We don't guess. We prove.*

---

## 1. Objective
Establish the **Research & Intelligence workspace frame** inside the UI-001/UI-002 shell and **prove every surface maps to existing governed data sources** — with the **no-recompute guardrail** established up front. Presentation only: no recompute/inference/re-derivation, no new backend/API/schema/ML/dependency, no execution/actuation, no external AI, Gate CLOSED.

## 2. Scope IN (per accepted plan UI-004-P01)
1. **Mount/enhance the research workspace frame** inside UI-001/UI-002 — prefer enhancing existing `/intelligence` as the primary workspace (R-1); mount via 14-field Workspace Registry; navigation via UI-002 (no page-specific nav). **Any registry route add/relabel requires ITRGA pre-approval** (R-1) — P01 should not change the registry unless explicitly authorized here (it is not).
2. **Overview of intelligence / signals / analytics / validation / economic-usefulness / artifacts** as **placeholders or thin read-only cards** over existing governed data.
3. **Complete data-source inventory** — visible in UI **and** in tests: every surface's origin = an existing governed read API / report store.
4. **No-recompute guardrail** established (R-6) as the workspace's constitutional spine.

## 3. Scope OUT (do NOT implement in P01)
- Advisory-signal + analytics integration — P02/P02b (R-3). Report viewers/drilldowns — P03. Validation/economic-usefulness panels — P04. Saved-view persistence — P05 (R-2). Collections/tags mutation — never in UI-004 (R-4).
- Any recompute/inference/re-derivation/signal-generation/regime-inference/external-AI; any new backend/API/schema/migration/column/dependency; any execution/actuation; any registry change.

## 4. Constitutional & architectural guardrails (binding)
- **🔴 R-6 no-recompute/no-inference (spine)** — surfaces display existing governed values only; **no** client-side inference/authoritative-recompute/new-algorithm/signal-gen/regime-inference/verdict-change (grep + named test).
- **Verbatim-integrity readiness** — even thin cards must render stored statuses/verdicts as-is (no reclassification); uncertainty/sample-count/limitations not hidden (no-cherry-picking readiness).
- **Advisory posture** — any signal preview is read-only, calibrated-confidence, disclaimered, non-actionable.
- **Extend-not-duplicate** — single UI-001 shell + UI-002 nav; no second shell/nav/palette/overlay; **no browser-side analytics engine**; reuse Design System tokens (no off-palette).
- **UG-3/UG-15** — no backend/API/schema change; no new dependency; head `20260717_0037`; UI-only (no-drift substitute).
- **🔴 Doc 16 brand gate (B-1…B-7)** — constitutional palette / typography+monospace numerics / unified iconography (Intelligence/Research/Signals categories) / institutional-not-retail / brand a11y; no off-palette color.
- **Accessibility first-class**; **no regression** (all UI-001/UI-002/UI-003 tests green).

## 5. MANDATORY EVIDENCE (operator-run on target; blank/errored grep = R7 non-result)
**(a) Build-identity** — `sed -n '1,15p'` of the P01 delivery report; confirm it is OF UI-004-P01.
**(b) Named tests (MUST be DISPLAYED passing by name — verbose reporter):**
  - `test_ui004_research_workspace_mounts_inside_single_ui001_shell`
  - `test_ui004_research_workspace_registers_through_ui002_navigation_only`
  - `test_ui004_research_workspace_maps_every_surface_to_existing_sources`
  - `test_ui004_research_workspace_contains_no_recompute_inference_or_signal_generation`
  - `test_ui004_research_workspace_preserves_gate_closed_research_only_branding`
**(c) 🔴 No-recompute/no-inference source grep (R-6)** — research-workspace source (tests excluded): `inferSignal|runInference|authoritativeRecompute|emitSignal|generateSignal|recompute|recalculat|deriveConfidence|new .*Engine|/api/v1/orders` → clean.
**(d) Data-source inventory proof** — grep/test that every surface reads an **existing** governed API/store (e.g. `fetchInstitutionalIntelligenceBundle`, `fetchAdvisorySignals`, `fetchAdvisoryAnalytics`, report/read APIs); no new endpoint.
**(e) No-actuation source grep** — research-workspace source → clean (`buy|sell|place_order|execute|...|open_gate`).
**(f) No-drift substitute (R-7)** — per-phase no-backend/schema/dep test; `alembic current` = `20260717_0037`; `package.json`/`package-lock.json` unchanged; no-new-endpoint grep; **no registry change** (confirm `workspaceRegistry.tsx` unmodified unless pre-approved).
**(g) Regression (R-7)** — backend `pytest -q` **≥414 passed**; frontend Vitest **≥36f/151t all passing, NO test lost** (verify the FULL-SUITE total, not a filtered run — UI-003-P05 lesson); TS clean; build + bundle delta.
**(h) 🔴 Doc 16 brand proof (B-1…B-7)** — grep/test + browser: constitutional palette (no off-palette / no new hardcoded brand color), typography+monospace numerics, unified iconography, institutional-not-retail; `test_ui004_research_workspace_preserves_gate_closed_research_only_branding` covers framing.
**(i) Browser (served session) — R-7** — shots: research workspace mounted in-shell (intelligence/signals/analytics/validation/economic/artifacts overview cards); Gate CLOSED/RESEARCH-ONLY framing + Doc 16 brand; UI-002 breadcrumb/nav; no actuation; logged-out block.
**(j) Networked CI (R-7)** — `scripts/local_ci.sh` → `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0` (or the TD-W6-CI-AUDIT offline-audit env-flake AFTER substantive gates green — record; disposition via operator).

## 6. Acceptance criteria (Determination: Approved · Approved with Observations · Corrective Actions Required · Rejected)
**Approved** requires: build-identity confirmed; (b) all five named tests displayed passing; (c) no-recompute/no-inference grep clean; (d) data-source inventory (existing sources only) proven; (e) no-actuation grep clean; (f) no-drift substitute + head unchanged + no new dependency + no registry change; (g) full-suite regression **≥36f/151t, no test lost** + backend ≥414; (h) Doc 16 brand proof (B-1…B-7); (i) browser frame + framing + brand + logged-out; (j) networked CI exit 0 + sentinel (or waived env-flake). **Only Approved / Approved-with-Observations authorizes `BUILD_ORDER_UI-004-P02` (Advisory Signals integration; analytics split to P02b per R-3).**

*We don't guess. We prove.*
