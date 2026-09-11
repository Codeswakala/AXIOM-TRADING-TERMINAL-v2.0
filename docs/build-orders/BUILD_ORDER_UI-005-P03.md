# BUILD ORDER — UI-005-P03

**Scenario Comparison & Portfolio Research Context**

| Field | Value |
|---|---|
| Issuing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-005 — Investigation & Planning Workspace |
| Phase | **UI-005-P03** |
| Predecessor verdict | `docs/ITRGA_REVIEW_UI-005-P02.md` — ✅ Approved with Observations |
| Governing docs | Doc 12 §7, `UI-005_ENGINEERING_DESIGN_PLAN.md` §10 (P03), `ITRGA_REVIEW_UI-005_DESIGN_PLAN.md` (R-1…R-7, R-5 mapping), Doc 16 |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend **45f/196t** |
| Governance Gate | CLOSED (must remain closed) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Purpose & scope

Connect the existing **Scenario Comparison** and **Portfolio Research** surfaces as **read-only / hypothetical** planning-and-investigation evidence, preserving no-cherry-picking discipline. Per the confirmed R-5 mapping, **P03 = Scenario + Portfolio** (Execution Research is P05 only).

**IN scope:**
1. Scenario Comparison — compare existing stored **hypothetical** scenario reports side-by-side, with assumptions, uncertainty, limitations, scope, sample counts, and source ids visible (reuse `fetchScenarioReports` / `fetchScenarioReport`; UI-004 viewer patterns).
2. Portfolio Research — existing **hypothetical** portfolio research dashboard / report preview as review context (reuse `fetchPortfolioResearchDashboard` / `fetchAdvancedResearchReport`), with hypothetical/research framing.
3. Read-only context links between scenario/portfolio evidence and the investigation workflow.

**OUT of scope (do NOT build):**
- Trade-Planning/Journal (P04), Execution Research (P05), completion (P06).
- Any scenario generation / new what-if engine / portfolio recompute / real account / real P&L / real portfolio state / live allocation surface (B-1/B-2).
- Cherry-picking: no filtered view presented as full-scope truth unless the stored report declares that scope.
- Any recompute / inference / re-derivation / reclassification / client-side analytics engine / external AI-LLM (R-6).
- Any persistence / saved-view state (R-2 — P03 does NOT persist).
- Any new table / migration / dependency / endpoint / **registry route** change (R-1).
- Any order/broker/account/position/balance/margin/capital/allocation/real-P&L/live/go-live/execute/Gate path (B-1).

---

## 2. Binding refinements applied (R-1…R-7)

- **R-1** — No new registered route (no `/investigation-planning`); registry 14-field contract unchanged; enhance existing `/compare-scenarios` + `/portfolio-research` (+ `/investigate` links).
- **R-2** — **P03 persists nothing.**
- **R-3** — No Trade-Planning / Journal mutation touched.
- **R-4** — n/a (Execution Research is P05); any SIMULATED reference stays labeled.
- **R-5** — **P03 = Scenario + Portfolio** (confirmed mapping; Execution Research remains P05 only).
- **R-6 (SPINE)** — no scenario generation / portfolio recompute; scenarios/portfolio rendered from stored reports; no-recompute grep clean; no-cherry-picking (scope/sample/assumptions/uncertainty/limitations/source-ids/hashes visible).
- **R-7** — Level-I evidence + Doc-16 brand + regression ≥ baseline, no test lost.

---

## 3. Mandatory named tests (MUST be DISPLAYED passing by name — verbose reporter)

1. `test_ui005_scenarios_render_existing_hypothetical_reports_only`
2. `test_ui005_portfolio_research_remains_hypothetical_no_real_account_pnl`
3. `test_ui005_comparison_preserves_assumptions_uncertainty_limitations_scope`
4. `test_ui005_comparison_contains_no_generation_or_execution_path`
5. `test_ui005_scenario_portfolio_accessibility_and_brand_markers_hold`

---

## 4. Full mandatory evidence checklist (Level-I, operator-run on target)

Windows/PowerShell `C:\Users\Swakala\.vscode\AXIOM\axiom`; PostgreSQL `axiom`/`axiom_dev_password` db `axiom`; admin `admin`/`admin123`.

- (a) **Build identity** — delivery report + transcript header grep proving pack is OF UI-005-P03.
- (b) **5 named tests DISPLAYED passing** by name (verbose reporter).
- (c) **🔴 R-6 no-recompute / no-scenario-generation grep CLEAN** — `inferSignal|runInference|authoritativeRecompute|emitSignal|generateSignal|generateScenario|recompute|recalculat|deriveConfidence|reclassif|summariz.*(ai|llm|gpt)|new .*Engine|/api/v1/orders`; **AND external-AI grep CLEAN** — `openai|gpt|external_llm|llm_summary|ai_summary`.
- (d) **🔴 No-cherry-picking proof** — scenario/portfolio views show included scope / sample counts / assumptions / uncertainty / limitations / source ids (source + named test #3); filtered ≠ full-scope truth.
- (e) **🔴 Portfolio hypothetical proof** — no real account / real P&L / real portfolio state / live allocation; hypothetical/research framing (named test #2); no real-P&L label.
- (f) **🔴 Whole-surface no-actuation grep CLEAN** (B-1 expanded): `buy|sell|place_order|execute|go-live|connect-broker|broker|account_id|order_ticket|position|balance|margin|capital|allocation|real_pnl|open_gate|allow_execution`.
- (g) **No-drift substitute** — `alembic current` = `20260717_0037`; `package.json`/`package-lock.json` content unchanged (no new dep); no new endpoint grep; **no registry/route change** (R-1); **no persistence** (R-2).
- (h) **Regression** — frontend Vitest **≥45f/196t** all passing (no test lost; verify FULL total; print the vitest sentinel alongside the CI sentinel); backend `pytest -q` **≥414 passed**; TS clean; production build + bundle delta. **Gated full run must exit 0.**
- (i) **🔴 Doc 16 brand B-1…B-7** — constitutional palette / `--font-mono` / `.mono` numerics (report ids/hashes/sample counts) / no hardcoded color in production TSX / unified iconography / institutional-not-retail / brand a11y (never color alone).
- (j) **Browser served-session screenshots** — logged-in `/compare-scenarios` side-by-side hypothetical scenarios (assumptions/uncertainty/limitations/scope visible) + `/portfolio-research` hypothetical framing; GATE CLOSED / RESEARCH-ONLY framing; **AND a logged-out `/login` block shot (closes OBS-P02-1)**.
- (k) **Networked local CI** `LOCAL_CI_EXIT_CODE: 0` + sentinel; OR: (i) documented `TD-W6-CI-AUDIT` offline npm-audit env-flake (ENOTFOUND/ECONNRESET) after substantive gates green → waiver; OR (ii) **`LOCAL_CI_EXIT_CODE: 1` attributable SOLELY to the tracked `TD-UI-POSTCSS-HIGH`** (networked audit reporting the real `postcss` high) after substantive gates green — disclose, do NOT relabel green; proceeds under the standing P06 disposition (no dependency change in P03 scope). Any OTHER nonzero cause is a finding.
- (l) **TD-UI-POSTCSS-HIGH note** — P03 introduces no dependency change; the residual does not gate it but remains OPEN for pre-certification remediation.

---

## 5. Determination rule

A single CRITICAL, or any unmet mandatory evidence item, ⇒ Corrective Actions Required / Rejected. Only **Approved** or **Approved with Observations** authorizes the next Build Order (UI-005-P04 — Trade Planning & Journal Continuity).

**DA does not self-approve. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.**

**We don't guess. We prove.**

*— AXIOM ITRGA*
