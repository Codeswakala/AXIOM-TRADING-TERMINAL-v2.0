# BUILD ORDER — UI-005-P02

**Signal Investigation Lineage & Related Evidence**

| Field | Value |
|---|---|
| Issuing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-005 — Investigation & Planning Workspace |
| Phase | **UI-005-P02** |
| Predecessor verdict | `docs/ITRGA_REVIEW_UI-005-P01.md` — ✅ Approved with Observations |
| Governing docs | Doc 12 §7, `UI-005_ENGINEERING_DESIGN_PLAN.md` §10 (P02), `ITRGA_REVIEW_UI-005_DESIGN_PLAN.md` (R-1…R-7), Doc 16 |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend **44f/191t** |
| Governance Gate | CLOSED (must remain closed) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Purpose & scope

Integrate the existing Signal Investigation surface with **lineage, validation, chart, and report context** as **read-only progressive disclosure of stored fields** — reusing the UI-004 report-viewer/drilldown patterns. Investigation reads persisted evidence; it never changes the signal, reruns the model, alters guardrails, recomputes confidence, or creates an instruction.

**IN scope:**
1. Signal investigation detail: rationale, guardrail states, calibrated confidence (as-stored), freshness, economic verdict, lineage (signal id / model / model version / experiment / feature set / input hash), linked validation and report ids.
2. Related-evidence links to existing reports/validation via UI-004 viewer patterns (navigation/disclosure, not recompute).
3. Chart/annotation context links where a signal references symbol/timeframe (UI-003 pattern; link-out only, no chart recompute).

**OUT of scope (do NOT build):**
- Scenario/portfolio (P03), Trade-Planning/Journal (P04), Execution Research (P05), completion (P06).
- Any signal recompute / model rerun / guardrail override / confidence derivation / reclassification / action recommendation / signal generation (R-6).
- Any persistence / saved-view state (R-2 — P02 does NOT persist).
- Any new table / migration / dependency / endpoint / **registry route** change (R-1).
- Any order/broker/account/position/balance/margin/capital/allocation/real-P&L/live/go-live/execute/Gate path (B-1).
- Client-side analytics engine; external AI/LLM.

---

## 2. Binding refinements applied (R-1…R-7)

- **R-1** — No new registered route (no `/investigation-planning`); registry 14-field contract unchanged; enhance existing `/investigate`.
- **R-2** — **P02 persists nothing** (no `operator_workspace_preferences` write, no key).
- **R-3** — No Trade-Planning / Journal mutation touched this phase.
- **R-4** — n/a to P02 (Execution Research is P05); any SIMULATED reference stays labeled.
- **R-5** — Confirmed mapping holds (P03=Scenario+Portfolio, P05=Execution Research SIMULATED only).
- **R-6 (SPINE this phase)** — verbatim rendering; no-recompute grep clean; lineage/validation/economic values rendered **as-stored**; related reports linked **without recompute** (UI-004 disclosure pattern).
- **R-7** — Level-I evidence + Doc-16 brand + regression ≥ baseline, no test lost.

---

## 3. Mandatory named tests (MUST be DISPLAYED passing by name — verbose reporter)

1. `test_ui005_signal_investigation_renders_existing_signal_lineage_read_only`
2. `test_ui005_investigation_uses_stored_confidence_validation_and_economic_values_verbatim`
3. `test_ui005_investigation_links_related_reports_without_recompute`
4. `test_ui005_investigation_contains_no_signal_generation_or_actuation`
5. `test_ui005_investigation_accessibility_and_brand_markers_hold`

---

## 4. Full mandatory evidence checklist (Level-I, operator-run on target)

Windows/PowerShell `C:\Users\Swakala\.vscode\AXIOM\axiom`; PostgreSQL `axiom`/`axiom_dev_password` db `axiom`; admin `admin`/`admin123`.

- (a) **Build identity** — delivery report + transcript header grep proving pack is OF UI-005-P02 (not stale/wrong-phase/concatenated).
- (b) **5 named tests DISPLAYED passing** by name (verbose reporter).
- (c) **🔴 R-6 no-recompute grep CLEAN** — `inferSignal|runInference|authoritativeRecompute|emitSignal|generateSignal|recompute|recalculat|deriveConfidence|reclassif|summariz.*(ai|llm|gpt)|new .*Engine|/api/v1/orders` on the investigation source; **AND external-AI grep CLEAN** — `openai|gpt|external_llm|llm_summary|ai_summary`.
- (d) **🔴 Verbatim proof** — lineage (signal id/model/model version/experiment/feature set/input hash), calibrated confidence, guardrail states, economic verdict rendered **as-stored** (source + named test #2); a raw score is NOT shown as calibrated confidence; stored `research_only`/`not_assessed`/`warning:*` never upgraded.
- (e) **🔴 Related-reports-without-recompute** — links resolve to existing report/validation ids via UI-004 viewer pattern; named test #3; no browser-side aggregate/derivation.
- (f) **🔴 Whole-surface no-actuation grep CLEAN** (B-1 expanded list): `buy|sell|place_order|execute|go-live|connect-broker|broker|account_id|order_ticket|position|balance|margin|capital|allocation|real_pnl|open_gate|allow_execution`.
- (g) **No-drift substitute** — `alembic current` = `20260717_0037`; `package.json`/`package-lock.json` content unchanged (no new dep); no new endpoint grep; **no registry/route change** (R-1); **no persistence** (R-2).
- (h) **Regression** — frontend Vitest **≥44f/191t** all passing (no test lost; verify FULL total, not a filtered `-t` run — print the vitest sentinel alongside the CI sentinel per OBS-P01-2); backend `pytest -q` **≥414 passed**; TS clean; production build + bundle delta. **Gated full run must exit 0.**
- (i) **🔴 Doc 16 brand B-1…B-7** — constitutional palette tokens / `--font-mono` / `.mono` numerics (ids/hashes/model versions) / no hardcoded color in production TSX / unified iconography / institutional-not-retail copy / brand a11y (never color alone).
- (j) **Browser served-session screenshots** — logged-in `/investigate` with a selected signal showing lineage/guardrails/economic verdict + related report/validation links; GATE CLOSED / RESEARCH-ONLY framing + "does not change this signal / rerun the model / alter guardrails / create an instruction" copy; logged-out `/login` block.
- (k) **Networked local CI** `LOCAL_CI_EXIT_CODE: 0` + sentinel; OR documented `TD-W6-CI-AUDIT` offline npm-audit env-flake **after** substantive gates green → operator/ITRGA waiver (do not relabel green).
- (l) **TD-UI-POSTCSS-HIGH note** — P02 introduces no dependency change; residual does not gate it; disclose any advisory (do not relabel green).

---

## 5. Determination rule

A single CRITICAL, or any unmet mandatory evidence item, ⇒ Corrective Actions Required / Rejected. Only **Approved** or **Approved with Observations** authorizes the next Build Order (UI-005-P03 — Scenario Comparison & Portfolio Research Context).

**DA does not self-approve. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.**

**We don't guess. We prove.**

*— AXIOM ITRGA*
