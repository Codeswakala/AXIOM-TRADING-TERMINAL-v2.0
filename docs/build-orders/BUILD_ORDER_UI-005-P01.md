# BUILD ORDER — UI-005-P01

**Investigation & Planning Workspace Frame · Data-Source Inventory · No-Actuation Guardrail**

| Field | Value |
|---|---|
| Issuing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-005 — Investigation & Planning Workspace |
| Phase | **UI-005-P01** |
| Design-plan review | `docs/ITRGA_REVIEW_UI-005_DESIGN_PLAN.md` — ✅ Approved w/ Obs + R-1…R-7 |
| Governing docs | Doc 12 §7, `UI-005_ENGINEERING_DESIGN_PLAN.md` §10 (P01), Doc 16 Part XIV |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend **43f/186t** |
| Governance Gate | CLOSED (must remain closed) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Purpose & scope

Establish the UI-005 Investigation & Planning **workflow frame** on the completed UI-001 shell + UI-002 navigation, prove **every UI-005 surface maps to an existing governed store/read API**, and lay down the **no-actuation / no-recompute guardrail** BEFORE any surface integration. Presentation/navigation/integration only. No new capability.

**IN scope:**
1. Enhance the existing `/investigate` route as the primary UI-005 workflow hub (no new route).
2. **Data-source inventory** covering all six §7 surfaces — Signal Investigation, Scenario Comparison, Trade Planning, Execution Research (SIMULATED), Research Journal, Portfolio Research — each mapped to its existing store + existing read seam.
3. No-actuation / no-recompute / research-only guardrail framing (GATE CLOSED · RESEARCH-ONLY · SIMULATED labels).

**OUT of scope (do NOT build):**
- Any surface deep-integration (P02 investigation lineage, P03 scenario+portfolio, P04 trade-planning+journal, P05 execution-research — later phases).
- Mutation changes to Trade Planning / Journal (R-3).
- Any persistence / saved-view state (R-2 — P01 does NOT persist).
- New table / migration / column / backend schema / dependency / endpoint / **registry route** change (R-1).
- Any recompute / inference / re-derivation / reclassification / scenario generation / client-side analytics engine / external AI-LLM / action recommendation (R-6).
- Any order/broker/account/position/balance/margin/capital/allocation/real-P&L/live-data/go-live/execute/Gate path (B-1).

---

## 2. Binding refinements applied (R-1…R-7 from design-plan review)

- **R-1** — Enhance existing routes; **no new registered route** (no `/investigation-planning`); registry 14-field contract unchanged; no duplicate navigation.
- **R-2** — **P01 persists nothing.** No `operator_workspace_preferences` write, no `investigation-planning-workspace-v1` key this phase.
- **R-3** — No expansion of W5 Trade-Planning / Journal mutation (P01 is frame/inventory only; no mutation surface touched).
- **R-4** — Execution Research shown as **SIMULATED / display-only** in the inventory; never labeled live/real.
- **R-5** — Confirm the phase mapping at intake: **P03 = Scenario + Portfolio; P05 = Execution Research (SIMULATED) only** (supersedes the stray design-plan §13 wording). Closes OBS-DP-1.
- **R-6** — No-recompute spine grep clean + no external-AI grep clean.
- **R-7** — Level-I evidence + Doc-16 brand + regression ≥ baseline, no test lost.

---

## 3. Mandatory named tests (MUST be DISPLAYED passing by name — verbose reporter)

1. `test_ui005_workspace_mounts_inside_single_ui001_shell`
2. `test_ui005_workspace_uses_existing_routes_and_registry_only`
3. `test_ui005_workspace_maps_every_surface_to_existing_sources`
4. `test_ui005_workspace_contains_no_actuation_or_gate_path`
5. `test_ui005_workspace_preserves_research_only_and_doc16_branding`

---

## 4. Full mandatory evidence checklist (Level-I, operator-run on target)

Windows/PowerShell `C:\Users\Swakala\.vscode\AXIOM\axiom`; PostgreSQL `axiom`/`axiom_dev_password` db `axiom`; admin `admin`/`admin123`.

- (a) **Build identity** — delivery report + transcript header grep proving pack is OF UI-005-P01 (not stale/wrong-phase/concatenated).
- (b) **5 named tests DISPLAYED passing** by name (verbose reporter).
- (c) **🔴 R-6 no-recompute grep CLEAN** — `inferSignal|runInference|authoritativeRecompute|emitSignal|generateSignal|recompute|recalculat|deriveConfidence|reclassif|summariz.*(ai|llm|gpt)|new .*Engine|/api/v1/orders` on UI-005 source; **AND external-AI grep CLEAN** — `openai|gpt|external_llm|llm_summary|ai_summary`.
- (d) **🔴 Whole-surface no-actuation grep CLEAN** (B-1 expanded list) — `buy|sell|place_order|execute|go-live|connect-broker|broker|account_id|order_ticket|position|balance|margin|capital|allocation|real_pnl|open_gate|allow_execution`.
- (e) **Data-source inventory proof** — each of the six surfaces shown mapping to an existing store + existing read seam (source grep + named test #3); Execution Research labeled SIMULATED (R-4).
- (f) **No-drift substitute** — `alembic current` = `20260717_0037`; `package.json`/`package-lock.json` content unchanged (no new dep); no new endpoint grep; **no registry/route change** (R-1: existing `/investigate` etc. only, no `/investigation-planning`).
- (g) **Regression** — frontend Vitest **≥43f/186t** all passing (no test lost; verify FULL total, not a filtered `-t` run); backend `pytest -q` **≥414 passed**; TS clean; production build + bundle delta. **Gated full run must exit 0.**
- (h) **🔴 Doc 16 brand B-1…B-7** — constitutional palette tokens / `--font-mono` / `.mono` numerics / no hardcoded color in production TSX / unified iconography / institutional-not-retail copy / brand a11y (never color alone).
- (i) **Browser served-session screenshots** — logged-in `/investigate` frame with the data-source inventory; GATE CLOSED / RESEARCH-ONLY framing + SIMULATED label on Execution Research source; logged-out `/login` block.
- (j) **Networked local CI** `LOCAL_CI_EXIT_CODE: 0` + sentinel; OR documented `TD-W6-CI-AUDIT` offline npm-audit env-flake **after** substantive gates green → operator/ITRGA waiver (do not relabel green).
- (k) **TD-UI-POSTCSS-HIGH note** — P01 introduces no dependency change, so this residual does not gate it; if any advisory surfaces, disclose it (do not relabel green).

---

## 5. Determination rule

A single CRITICAL, or any unmet mandatory evidence item, ⇒ Corrective Actions Required / Rejected. Only **Approved** or **Approved with Observations** authorizes the next Build Order (UI-005-P02 — Signal Investigation Lineage & Related Evidence).

**DA does not self-approve. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.**

**We don't guess. We prove.**

*— AXIOM ITRGA*
