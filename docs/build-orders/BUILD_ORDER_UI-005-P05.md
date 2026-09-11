# BUILD ORDER — UI-005-P05

**Execution Research / SIMULATED Evidence Context**

| Field | Value |
|---|---|
| Issuing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-005 — Investigation & Planning Workspace |
| Phase | **UI-005-P05** |
| Predecessor verdict | `docs/ITRGA_REVIEW_UI-005-P04.md` — ✅ Approved with Observations (carries mandatory OBS-P04-1 closure) |
| Governing docs | Doc 12 §7, `UI-005_ENGINEERING_DESIGN_PLAN.md` §10 (P05), `ITRGA_REVIEW_UI-005_DESIGN_PLAN.md` (R-1…R-7, esp. R-4/R-5), Doc 16 |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend **46f/201t** (P04 +5 tests adopted only on a green gated run — see §5) |
| Governance Gate | CLOSED (must remain closed) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Purpose & scope

Integrate the existing **SIMULATED execution research** artifacts into the investigation/planning workflow as **display-only evidence**, with assumptions, uncertainty, and limitations. Per the confirmed R-5 mapping, **P05 = Execution Research (SIMULATED) only.** This is a named-risk domain ("Execution Research") — **R-4 (SIMULATED/display-only, never live/real) is the spine.**

**IN scope:**
1. Execution Research surface — existing W6 SIMULATED execution research artifacts (runs / fills / ledger / risk / experiments / analytics) shown as display-only evidence for planning, via `fetchExecutionResearchBundle`.
2. Assumptions / uncertainty / limitations preserved; every surface labeled **SIMULATED** and never presented as live/real execution.
3. Read-only context links between execution research evidence and the investigation/planning workflow.

**OUT of scope (do NOT build):**
- Completion checkpoint (P06).
- Any live execution / real fill / real order / broker connection / account state / real P&L / Gate path (B-1/R-4).
- Any recompute / inference / re-derivation / reclassification / analytics engine / external AI-LLM (R-6).
- Any persistence / saved-view state (R-2 — P05 does NOT persist); any plan/journal mutation (R-3).
- Any new table / migration / dependency / endpoint / **registry route** change (R-1).

---

## 2. Binding refinements applied (R-1…R-7)

- **R-1** — No new registered route (no `/investigation-planning`); enhance existing `/execution-research`; 14-field registry contract unchanged.
- **R-2** — **P05 persists nothing.**
- **R-3** — No plan/journal mutation touched.
- **R-4 (SPINE this phase)** — Execution Research is **SIMULATED / display-only**; the `SIMULATED` label is rendered and never relabeled live/real; no live execution / real fill / real order / broker / account / Gate.
- **R-5** — Confirmed mapping: **P05 = Execution Research only.**
- **R-6** — no-recompute grep clean; external-AI grep clean.
- **R-7** — Level-I evidence + Doc-16 brand + regression ≥ baseline, no test lost.

---

## 3. Mandatory named tests (MUST be DISPLAYED passing by name — verbose reporter)

1. `test_ui005_execution_research_renders_existing_simulated_artifacts_only`
2. `test_ui005_execution_research_never_claims_live_execution_or_real_fills`
3. `test_ui005_execution_research_preserves_assumptions_uncertainty_limitations`
4. `test_ui005_execution_research_contains_no_broker_order_account_or_gate_path`
5. `test_ui005_execution_research_accessibility_and_brand_markers_hold`

---

## 4. Full mandatory evidence checklist (Level-I, operator-run on target)

Windows/PowerShell `C:\Users\Swakala\.vscode\AXIOM\axiom`; PostgreSQL `axiom`/`axiom_dev_password` db `axiom`; admin `admin`/`admin123`.

- (a) **Build identity** — delivery report + transcript header grep proving pack is OF UI-005-P05.
- (b) **5 named tests DISPLAYED passing** by name (verbose reporter).
- (c) **🔴 R-4 SIMULATED proof** — every execution-research surface renders the `SIMULATED` label; no "live"/"real" execution/fill/order claim (named tests #1/#2 + source); `fetchExecutionResearchBundle` read source.
- (d) **🔴 R-6 no-recompute grep CLEAN** — `inferSignal|runInference|authoritativeRecompute|emitSignal|generateSignal|recompute|recalculat|deriveConfidence|reclassif|summariz.*(ai|llm|gpt)|new .*Engine|/api/v1/orders`; **AND external-AI grep CLEAN** — `openai|gpt|external_llm|llm_summary|ai_summary`.
- (e) **🔴 Whole-surface no-actuation grep CLEAN** (B-1 expanded): `buy|sell|place_order|execute|go-live|connect-broker|broker|account_id|order_ticket|position|balance|margin|capital|allocation|real_pnl|open_gate|allow_execution`.
- (f) **Assumptions/uncertainty/limitations preserved** (named test #3 + source).
- (g) **No-drift substitute** — `alembic current` = `20260717_0037`; `package.json`/`package-lock.json` content unchanged (no new dep); no new endpoint grep; **no registry/route change** (R-1); **no persistence** (R-2).
- (h) **Regression** — frontend Vitest **≥46f/201t** all passing (no test lost; verify FULL total); backend `pytest -q` **≥414 passed**; TS clean; production build + bundle delta. **Gated full run must exit 0.**
- (i) **🔴🔴 OBS-P04-1 CLOSURE (MANDATORY, NON-WAIVABLE):** (1) add an explicit `testTimeout` to `ResearchPerformanceAnalytics.test.tsx > test_ui004_analytics_accessibility_and_brand_markers_hold` (same remedy as the prior route-loop timeout hardening); AND (2) supply a **clean gated `FRONTEND_VITEST_EXIT_CODE: 0` full-suite re-run** with the actual total displayed. **A red gated run again ⇒ Corrective.** On a clean green run, the baseline of record is adopted (expected ~48f/206t: P04 +5 + P05 +5, no test lost).
- (j) **🔴 Doc 16 brand B-1…B-7** — palette / `--font-mono` / `.mono` numerics / no hardcoded color in production TSX / unified iconography / institutional-not-retail (SIMULATED research, not live venue) / brand a11y (never color alone).
- (k) **Browser served-session screenshots** — logged-in `/execution-research` showing SIMULATED evidence + assumptions/uncertainty/limitations; GATE CLOSED / RESEARCH-ONLY + SIMULATED framing; logged-out `/login` block.
- (l) **Networked local CI** `LOCAL_CI_EXIT_CODE: 0` + sentinel; OR: (i) documented `TD-W6-CI-AUDIT` offline npm-audit env-flake after substantive gates green → waiver; OR (ii) `LOCAL_CI_EXIT_CODE: 1` attributable **SOLELY** to the tracked `TD-UI-POSTCSS-HIGH` (networked audit reporting the real `postcss` high, identical advisory set) after substantive gates green — disclose, do NOT relabel green; proceeds under the standing P06 disposition. **Any OTHER nonzero cause (e.g. a vitest failure like OBS-P04-1) is a finding and ⇒ Corrective.**
- (m) **TD-UI-POSTCSS-HIGH note** — P05 introduces no dependency change; the residual does not gate it but remains OPEN for pre-certification remediation.

---

## 5. Baseline-adoption note

The UI-004-P02b timeout at P04 left the +5 P04 tests recorded on a RED run; the baseline of record is therefore **held at 46f/201t** until this phase supplies a **green gated full-suite run**. On that green run, the confirmed total (P04 +5 and P05 +5, no test lost) is adopted as the new baseline.

---

## 6. Determination rule

A single CRITICAL, a red gated full-suite run (incl. an unremediated OBS-P04-1 timeout), or any unmet mandatory evidence item ⇒ Corrective Actions Required / Rejected. Only **Approved** or **Approved with Observations** authorizes the next Build Order (UI-005-P06 — Completion Checkpoint).

**DA does not self-approve. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.**

**We don't guess. We prove.**

*— AXIOM ITRGA*
