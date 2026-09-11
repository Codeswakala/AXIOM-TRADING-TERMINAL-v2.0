# BUILD ORDER — UI-005-P06

## UI-005 Completion Checkpoint (integration evidence · constitutional + Doc 16 brand validation)

| Field | Value |
|---|---|
| Issuing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-005 — Investigation & Planning Workspace |
| Phase | **UI-005-P06 — Completion Checkpoint** |
| Predecessor verdict | `docs/ITRGA_REVIEW_UI-005-P05.md` — ✅ Approved with Observations |
| Governing docs | Doc 12 §7, `UI-005_ENGINEERING_DESIGN_PLAN.md` §10 (P06)/§11, `ITRGA_REVIEW_UI-005_DESIGN_PLAN.md` (R-1…R-7), Doc 16 Part XIV |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend **48f/211t** |
| Governance Gate | CLOSED (must remain closed) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Purpose

Provide **final integration evidence** and bring UI-005 to its **completion checkpoint**: the Investigation & Planning workspace is a continuous investigation→planning workflow on the completed UI-001/UI-002 shell, presentation-only over existing governed artifacts and existing authorized research-note stores, constitutionally clean (no execution/broker/account/live-data/AI/Gate path), SIMULATED-boundary-faithful, verbatim, no-cherry-picking, and brand-compliant. **No new capability.** On Approved, ITRGA declares 🏛️ UI-005 COMPLETE.

---

## 2. Scope

**IN scope:**
1. Route/browser integration evidence across the full investigation→planning workflow (`/investigate` `/compare-scenarios` `/portfolio-research` `/trade-plans` `/journal` `/execution-research`).
2. Whole-surface no-actuation **and** no-recompute/no-inference/no-external-AI grep.
3. Full regression (backend + frontend, no loss).
4. Final constitutional self-check + Doc 16 brand self-check (B-1…B-7).
5. Browser-served workflow proof (incl. SIMULATED boundary + logged-out block).

**OUT of scope:** any new capability / recompute / analytics engine / external AI / live data / broker-execution-Gate / new table / migration / dependency / endpoint / registry-route change / plan-journal mutation expansion / Production Readiness Certification (Doc 11, HELD).

---

## 3. Constitutional & architectural guardrails (binding)

- Gate CLOSED; no live broker/order/account/position/balance/margin/capital/allocation/real-P&L path anywhere.
- No external LLM/AI; no client-side analytics engine; no recompute/inference/re-derivation/reclassification.
- **Verbatim posture preserved** (UI-004 §2.2 discipline carried into investigation lineage / scenario / economic values).
- **No-cherry-picking:** scope / sample counts / assumptions / uncertainty / limitations / source ids visible.
- **SIMULATED boundary:** Execution Research remains SIMULATED/display-only, never live/real (R-4).
- **Trade Planning / Journal remain research-note/reflection stores** — no order/account/broker/execution field; no plan-to-execution path (R-3; DB schema proved `forbidden_w5_column_count=0` at P04).
- No-drift: Alembic `20260717_0037`; package manifests unchanged (no new dependency); no new endpoint; **no registry/route change** (R-1: existing routes only, no `/investigation-planning`).
- **🔴 Doc 16 brand gate (B-1…B-7)** — never color alone; material violation ⇒ Corrective (Part XIV).

---

## 4. Mandatory named tests (MUST be DISPLAYED passing by name — verbose reporter)

1. `test_ui005_completion_investigation_to_planning_workflow_is_continuous_without_scope_expansion`
2. `test_ui005_completion_all_surfaces_are_existing_artifact_presentation_or_existing_research_notes`
3. `test_ui005_completion_no_execution_broker_account_live_data_ai_or_gate_path`
4. `test_ui005_completion_verbatim_values_no_cherry_picking_and_simulated_boundaries_hold`
5. `test_ui005_completion_accessibility_brand_and_ui001_ui002_integration_hold`

---

## 5. 🔴 TD-UI-POSTCSS-HIGH DECISION POINT (mandatory at this checkpoint)

The high-severity transitive advisory `postcss <=8.5.17` (GHSA-r28c-9q8g-f849) has reproduced on target across UI-005-P02/P03/P05. At this completion checkpoint the delivery MUST take one of two paths, **explicitly stated in the delivery report**:
- **(A) Remediate:** run a separately-authorized dependency remediation (`npm audit fix` / bump) — which, being a dependency change, requires its own evidence: manifest diff, no functional regression (full suite still green), and a networked `npm audit --audit-level=high` exit 0; OR
- **(B) Accept as documented pre-cert residual:** declare UI-005 COMPLETE with TD-UI-POSTCSS-HIGH **explicitly carried** as an accepted pre-certification residual (no dependency change in UI-005 scope), on the condition it is remediated before Production Readiness Certification (Doc 11).

ITRGA will adjudicate the chosen path. **Silently relabeling the audit green is prohibited.**

---

## 6. Full mandatory evidence checklist (Level-I, operator-run on target)

Windows/PowerShell `C:\Users\Swakala\.vscode\AXIOM\axiom`; PostgreSQL `axiom`/`axiom_dev_password` db `axiom`; admin `admin`/`admin123`.

- (a) **Build identity** — delivery report + transcript header grep proving pack is OF UI-005-P06.
- (b) **5 named completion tests DISPLAYED passing** by name (verbose reporter).
- (c) **🔴 Whole-surface no-recompute/no-inference grep CLEAN** — `inferSignal|runInference|authoritativeRecompute|emitSignal|generateSignal|generateScenario|recompute|recalculat|deriveConfidence|reclassif|summariz.*(ai|llm|gpt)|new .*Engine|/api/v1/orders`; **AND external-AI grep CLEAN** — `openai|gpt|external_llm|llm_summary|ai_summary`.
- (d) **🔴 Whole-surface no-actuation grep CLEAN** (B-1 expanded): `buy|sell|place_order|execute|go-live|connect-broker|broker|account_id|order_ticket|position|balance|margin|capital|allocation|real_pnl|open_gate|allow_execution`.
- (e) **Verbatim + no-cherry-picking + SIMULATED boundaries reaffirmed** (named test #4 + browser).
- (f) **No-drift substitute** — `alembic current` = `20260717_0037`; `package.json`/`package-lock.json` content unchanged unless §5(A) remediation is chosen (then supply the manifest diff); no new endpoint grep; **no registry/route change** (R-1).
- (g) **Completion regression** — backend `pytest -q` **≥414 passed**; frontend Vitest **≥48f/211t** all passing (no test lost). **Gated full run must exit 0** (keep the timeout-hardened tests deterministic; surface any intervening red gate).
- (h) **🔴 Doc 16 brand self-check + browser proof (B-1…B-7)** — palette / typography / monospace numerics / unified iconography / institutional-not-retail / brand a11y; no off-palette hardcoded brand color.
- (i) **Browser served-session** — the continuous investigation→planning workflow across all six routes; GATE CLOSED / RESEARCH-ONLY / SIMULATED framing; logged-out `/login` block.
- (j) **Networked local CI** `LOCAL_CI_EXIT_CODE: 0` + sentinel; OR the TD-W6-CI-AUDIT env-flake waiver; OR `LOCAL_CI_EXIT_CODE: 1` attributable **solely** to the tracked TD-UI-POSTCSS-HIGH (if §5(B) is chosen) after substantive gates green — disclosed, not relabeled. **Any other nonzero cause is a finding ⇒ Corrective.**
- (k) **🔴 UI-005 COMPLETION VALIDATION** — the delivery report presents the DA's completion self-check; ITRGA will independently apply the **constitutional validation** (governing hierarchy Docs 00–16 · no scope expansion · no new analysis/live-data/capability · governance preserved · research-only · no execution pathways · SIMULATED boundary · Trade-Planning/Journal research-note-only · UI-001/UI-002 unmodified · single shell · **Gate CLOSED**) **AND the Doc 16 brand validation (B-1…B-7)** — plus the §5 residual decision.

---

## 7. Determination rule

**Approved** requires: build-identity confirmed; (b) all five named completion tests displayed passing; (c) whole-surface no-recompute + external-AI grep clean; (d) whole-surface no-actuation grep clean; (e) verbatim + no-cherry-picking + SIMULATED reaffirmed; (f) no-drift + head unchanged (or a clean §5(A) remediation with green suite); (g) completion regression green with actual totals (gated exit 0); (h) Doc 16 brand pass; (i) browser workflow + logged-out; (j) CI exit 0 or the pre-authorized/waived exception; (k) constitutional + brand completion validation clean **and** the §5 TD-UI-POSTCSS-HIGH decision explicitly stated and adjudicated.

A single CRITICAL, an un-remediated/undeclared postcss decision, a red gated run, or any unmet mandatory evidence item ⇒ Corrective Actions Required / Rejected.

**On Approved: ITRGA will declare 🏛️ UI-005 — INVESTIGATION & PLANNING WORKSPACE — COMPLETE** (continuous investigation→planning workflow over existing governed artifacts + existing authorized research-note stores on the UI-001/UI-002 shell; presentation-only; SIMULATED-faithful; verbatim; no-cherry-picking; Doc 12 §7 / Doc 16 conformant; regression passed; ITRGA review complete). **UI-005 completion does NOT open the Gate or authorize execution.**

Future after UI-005: **UI-006 — Unified Research Artifact Explorer** (Doc 12 §8 — NEW workstream → request Design Plan first; inherits the deferred collection/tag mutation), then UI-007/UI-008/UI-009/UI-010; and separately the Production Readiness Certification track (Doc 11, HELD — gated by TD-UI-POSTCSS-HIGH remediation).

**DA does not self-approve. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.**

**We don't guess. We prove.**

*— AXIOM ITRGA*
