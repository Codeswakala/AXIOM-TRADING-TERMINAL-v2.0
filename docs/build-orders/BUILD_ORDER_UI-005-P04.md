# BUILD ORDER — UI-005-P04

**Trade Planning & Journal Continuity** — *Mutation-Boundary Phase*

| Field | Value |
|---|---|
| Issuing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-005 — Investigation & Planning Workspace |
| Phase | **UI-005-P04** |
| Predecessor verdict | `docs/ITRGA_REVIEW_UI-005-P03.md` — ✅ Approved with Observations |
| Governing docs | Doc 12 §7, `UI-005_ENGINEERING_DESIGN_PLAN.md` §10 (P04) + §4.3, `ITRGA_REVIEW_UI-005_DESIGN_PLAN.md` (R-1…R-7, esp. R-3), Doc 16 |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend **46f/201t** |
| Governance Gate | CLOSED (must remain closed) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Purpose & scope — MUTATION-BOUNDARY PHASE

Connect the existing **Trade Planning** and **Research Journal** surfaces to the investigation/planning workflow **without expanding their mutation scope**. This is the single most constitutionally sensitive UI-005 phase: the existing W5 plan/journal stores have authorized create/update callbacks, and "Trade Planning" is a named-risk term. **R-3 is the HARD gate.**

**IN scope:**
1. Trade Planning — surface existing W5 trade-plan **research notes** in the investigation/planning workflow; the existing authorized create/update research-note callbacks may remain, unchanged and unexpanded.
2. Research Journal — surface existing W5 manual journal **reflections** linked to signals/reports/plans/scenarios; existing authorized create/update reflection callbacks may remain, unchanged and unexpanded.
3. Read-only artifact-id links between plans/journal and investigation context.

**OUT of scope (do NOT build):**
- Execution Research (P05), completion (P06).
- **Any expansion of plan/journal mutation** — no new fields, no order/account/broker/position/P&L/execution field, **no plan-to-execution path**, no broker/account journal import (R-3).
- Any new backend endpoint / table / migration / dependency / **registry route** (R-1); any new persistence key beyond the existing authorized W5 stores (R-2 — no `operator_workspace_preferences` view-state this phase).
- Any recompute / inference / re-derivation / reclassification / analytics engine / external AI-LLM (R-6).
- Any order/broker/account/position/balance/margin/capital/allocation/real-P&L/live/go-live/execute/Gate path (B-1).

---

## 2. Binding refinements applied (R-1…R-7)

- **R-1** — No new registered route (no `/investigation-planning`); enhance existing `/trade-plans` + `/journal` (+ investigation links); 14-field registry contract unchanged.
- **R-2** — No new persistence key; only the **existing authorized W5 plan/journal stores** may be written (no expansion).
- **R-3 (HARD GATE this phase)** — Plan/journal fields remain **research-note / reflection fields only**. Prove: no order/account/broker/position/P&L/execution field; **no plan-to-execution path**; no broker/account journal import; existing APIs only; no new endpoint/table. **A forbidden-field-rejection named test is MANDATORY.**
- **R-4** — n/a (Execution Research is P05).
- **R-5** — Confirmed mapping holds.
- **R-6** — no-recompute grep clean; external-AI grep clean.
- **R-7** — Level-I evidence + Doc-16 brand + regression ≥ baseline, no test lost.

---

## 3. Mandatory named tests (MUST be DISPLAYED passing by name — verbose reporter)

1. `test_ui005_trade_plans_use_existing_research_note_store_no_order_ticket`
2. `test_ui005_journal_uses_existing_reflection_store_no_broker_import`
3. `test_ui005_planning_preserves_research_only_fields_and_forbidden_field_rejection` **(R-3 forbidden-field-rejection — CRITICAL)**
4. `test_ui005_plan_journal_links_are_artifact_ids_not_execution_paths`
5. `test_ui005_planning_journal_accessibility_and_brand_markers_hold`

---

## 4. Full mandatory evidence checklist (Level-I, operator-run on target)

Windows/PowerShell `C:\Users\Swakala\.vscode\AXIOM\axiom`; PostgreSQL `axiom`/`axiom_dev_password` db `axiom`; admin `admin`/`admin123`.

- (a) **Build identity** — delivery report + transcript header grep proving pack is OF UI-005-P04.
- (b) **5 named tests DISPLAYED passing** by name (verbose reporter) — **including the forbidden-field-rejection test #3.**
- (c) **🔴 R-3 mutation-boundary proof** — the plan/journal create/update surface accepts **only** research-note/reflection fields; a forbidden-field payload (order/account/broker/position/P&L/execution) is **rejected** (named test #3 + source of the field schema); no plan-to-execution path; existing W5 APIs only (no new endpoint grep).
- (d) **🔴 R-6 no-recompute grep CLEAN** — `inferSignal|runInference|authoritativeRecompute|emitSignal|generateSignal|recompute|recalculat|deriveConfidence|reclassif|summariz.*(ai|llm|gpt)|new .*Engine|/api/v1/orders`; **AND external-AI grep CLEAN** — `openai|gpt|external_llm|llm_summary|ai_summary`.
- (e) **🔴 Whole-surface no-actuation grep CLEAN** (B-1 expanded): `buy|sell|place_order|execute|go-live|connect-broker|broker|account_id|order_ticket|position|balance|margin|capital|allocation|real_pnl|open_gate|allow_execution`.
- (f) **Plan/journal links are artifact ids, not execution paths** (named test #4 + source).
- (g) **No-drift substitute** — `alembic current` = `20260717_0037`; `package.json`/`package-lock.json` content unchanged (no new dep); **no new endpoint grep**; **no registry/route change** (R-1); **no new persistence key** (R-2).
- (h) **Persistence note** — if the operator exercises an existing authorized W5 plan/journal create/update during evidence, that is acceptable (existing store), but it is **not** new UI-005 persistence; if any write is shown, an inline raw psql read-back on the EXISTING W5 table proving research-note fields only (no forbidden fields) is welcome corroboration (not a new-table capture). No `operator_workspace_preferences` view-state key is expected this phase.
- (i) **Regression** — frontend Vitest **≥46f/201t** all passing (no test lost; verify FULL total; print the vitest sentinel alongside the CI sentinel); backend `pytest -q` **≥414 passed**; TS clean; production build + bundle delta. **Gated full run must exit 0.**
- (j) **🔴 Doc 16 brand B-1…B-7** — constitutional palette / `--font-mono` / `.mono` numerics (plan/journal/artifact ids) / no hardcoded color in production TSX / unified iconography / institutional-not-retail (research-note/reflection, not order-ticket) / brand a11y (never color alone).
- (k) **Browser served-session screenshots** — logged-in `/trade-plans` showing research-note fields (no order-ticket/position-sizing/broker fields) + `/journal` showing reflection fields (no broker/account import); GATE CLOSED / RESEARCH-ONLY framing; logged-out `/login` block.
- (l) **Networked local CI** `LOCAL_CI_EXIT_CODE: 0` + sentinel; OR: (i) documented `TD-W6-CI-AUDIT` offline npm-audit env-flake (ENOTFOUND/ECONNRESET) after substantive gates green → waiver; OR (ii) `LOCAL_CI_EXIT_CODE: 1` attributable **SOLELY** to the tracked `TD-UI-POSTCSS-HIGH` (networked audit reporting the real `postcss` high, identical advisory set) after substantive gates green — disclose, do NOT relabel green; proceeds under the standing P06 disposition. **Any OTHER nonzero cause is a finding.**

---

## 5. Split reservation (OBS-DP-2)

If the R-3 mutation-boundary evidence is **not crisp** — e.g. the forbidden-field-rejection test is weak, the field schema is ambiguous, or plan and journal boundaries are entangled — ITRGA will require **P04 to be split** into separate Trade-Planning and Journal phases for narrower review, and this delivery will be **Corrective** rather than Approved.

---

## 6. Determination rule

A single CRITICAL, a weak/absent forbidden-field-rejection proof (R-3), or any unmet mandatory evidence item ⇒ Corrective Actions Required / Rejected. Only **Approved** or **Approved with Observations** authorizes the next Build Order (UI-005-P05 — Execution Research / SIMULATED Evidence Context).

**DA does not self-approve. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.**

**We don't guess. We prove.**

*— AXIOM ITRGA*
