# BUILD ORDER — UI-004-P06

## UI-004 Completion Checkpoint (integration evidence · constitutional + Doc 16 brand validation)

| Field | Value |
|---|---|
| Issuing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-004 — Research & Intelligence Workspace |
| Phase | **UI-004-P06 — Completion Checkpoint** |
| Predecessor verdict | `docs/ITRGA_REVIEW_UI-004-P05.md` — ✅ Approved with Observations |
| Governing docs | Doc 12 §6, `UI-004_ENGINEERING_DESIGN_PLAN.md` §UI-004-P06 / §13, `ITRGA_REVIEW_UI-004_DESIGN_PLAN.md` (R-1…R-7), Doc 16 Brand Governance Standard (Part XIV) |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend **42f/181t** |
| Governance Gate | CLOSED (must remain closed) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Purpose

Provide **final integration evidence** and bring UI-004 to its **completion checkpoint**: the Research & Intelligence workspace is a continuous research workflow on the completed UI-001/UI-002 shell + navigation foundations, presentation-only over existing governed artifacts, constitutionally clean (no recompute / inference / external AI / live data / execution / Gate path), verbatim-verdict-faithful, no-cherry-picking, and brand-compliant. **No new capability.** On Approved, ITRGA declares 🏛️ UI-004 COMPLETE.

---

## 2. Scope

**IN scope:**
1. Route/browser integration evidence across the full `/intelligence` research workflow (and its `/signals` `/analytics` `/intelligence` read destinations).
2. Whole-surface no-actuation **and** no-recompute/no-inference grep.
3. Full regression (backend + frontend, no loss).
4. Final constitutional self-check + Doc 16 brand self-check (B-1…B-7).
5. Browser-served workflow proof — **including the two panels owed from prior phases (see §5 HARD GATE).**

**OUT of scope (do NOT build):** any new capability / recompute / re-derivation / reclassification / client-side analytics engine / external AI / live data / broker/account/order/execution/Gate path / new table / migration / dependency / endpoint / registry-route change / saved-view persistence not already reviewed / Production Readiness Certification (Doc 11, HELD).

---

## 3. Constitutional & architectural guardrails (binding)

- Gate CLOSED; no live broker/order/account/position/balance/margin/real-money path anywhere.
- No external LLM/AI in any feature; no dynamic/third-party plugin execution; no client-side analytics engine.
- **Verbatim-verdict integrity (§2.2):** stored `research_only` / `not_assessed` / `warning:POORLY_CALIBRATED` rendered as-stored — never reclassified/upgraded to tradable/approved/economically-usable.
- **No-cherry-picking:** included scope / sample counts / source artifact ids / uncertainty / limitations remain visible; filtered UI never claims full-scope performance truth unless the stored report declares that scope.
- Collections/tags remain **read-only** (R-4; mutation stays deferred to UI-006).
- No-drift: Alembic `20260717_0037`; package manifests unchanged (no new dependency); no new endpoint; **no registry/route change** (R-1: `/intelligence` only, no `/research-intelligence`).
- **🔴 Doc 16 brand gate (B-1…B-7)** — logo/monogram · constitutional palette (no off-palette / no new hardcoded brand color) · typography + monospace numerics · unified iconography · institutional-not-retail identity · brand accessibility · documentation branding. **UI shall not be approved where brand standards are violated (Doc 16 Part XIV). Never color alone.**

---

## 4. Mandatory named tests (MUST be DISPLAYED passing by name — verbose reporter)

1. `test_ui004_completion_research_intelligence_workflow_is_continuous_without_scope_expansion`
2. `test_ui004_completion_all_research_surfaces_are_existing_artifact_presentation_only`
3. `test_ui004_completion_no_recompute_inference_external_ai_live_data_or_execution_path`
4. `test_ui004_completion_validation_economic_usefulness_and_no_cherry_picking_hold`
5. `test_ui004_completion_accessibility_brand_and_ui001_ui002_integration_hold`

---

## 5. 🔴 HARD, NON-WAIVABLE BROWSER GATE (OBS-P05-1 / OBS-P04-2 closure)

This closure has **slipped twice** (P04 → P05). It will **not** be waived a third time. The delivery pack MUST include served-session screenshots of **both**:

- **(A)** the **P04 "Validation & Economic-Usefulness Integrity" panel** showing at least one **verbatim verdict** (`research_only` / `not_assessed` / `warning:POORLY_CALIBRATED` or an actual stored verdict such as `economic_usefulness` / `economic_verdict`) rendered as-stored; and
- **(B)** the **P05 "Research Artifact Context" panel** (collections / member references / tags / journal references / artifact-id inventory + the saved-view **absence** card).

Absence of either served screenshot ⇒ **Corrective Actions Required** (not an Observation). Source/named-test proof does **not** substitute for these two shots at the completion checkpoint.

---

## 6. Full mandatory evidence checklist (Level-I, operator-run on target)

Windows/PowerShell `C:\Users\Swakala\.vscode\AXIOM\axiom`; PostgreSQL `axiom`/`axiom_dev_password` db `axiom`; admin `admin`/`admin123`.

- (a) **Build identity** — delivery report + transcript header grep proving pack is OF UI-004-P06 (not stale/wrong-phase/concatenated).
- (b) **5 named completion tests DISPLAYED passing** by name (verbose reporter).
- (c) **🔴 Whole-surface no-recompute/no-inference grep CLEAN** — `inferSignal|runInference|authoritativeRecompute|emitSignal|generateSignal|recompute|recalculat|deriveConfidence|reclassif|summariz.*(ai|llm|gpt)|new .*Engine|/api/v1/orders`.
- (d) **Whole-surface no-actuation grep CLEAN** — buy/sell/place_order/execute/go-live/connect-broker/account_id/order_ticket/open_gate/allow_execution.
- (e) **No external AI/LLM grep** on UI-004 source.
- (f) **Verbatim-verdict + no-cherry-picking reaffirmed** — validation/economic verdicts as-stored; sample counts/scope/uncertainty/limitations visible (named test #4 + browser (A)).
- (g) **No-drift substitute** — `alembic current` = `20260717_0037`; `package.json`/`package-lock.json` content unchanged (no new dep); no new endpoint grep; **no registry/route change** (R-1).
- (h) **Completion regression** — backend `pytest -q` **≥414 passed**; frontend Vitest **≥42f/181t** all passing (no test lost); TS clean; production build + bundle delta. **Gated full run must exit 0** (the two route-loop tests already carry explicit `testTimeout` from OBS-P04-1 — keep them deterministic; surface any intervening red gate in the delivery report).
- (i) **🔴 §5 HARD BROWSER GATE** — served screenshots (A) P04 verbatim-verdict panel **and** (B) P05 artifact-context panel — **both mandatory, non-waivable.**
- (j) **Route/responsive/keyboard/accessibility browser evidence** — the continuous research workflow served in-session; GATE CLOSED / RESEARCH-ONLY / PRESENTATION SHELL framing visible; logged-out `/login` block.
- (k) **🔴 Doc 16 brand self-check + browser proof (B-1…B-7)** — constitutional palette / typography / monospace numerics / unified iconography / institutional-not-retail identity; no off-palette hardcoded brand color (no-hardcoded-color style grep is acceptable corroboration); documentation branding for the completion pack.
- (l) **Networked local CI** `LOCAL_CI_EXIT_CODE: 0` + sentinel; OR documented `TD-W6-CI-AUDIT` offline npm-audit env-flake **after** substantive gates are green → operator/ITRGA waiver (do not relabel green).
- (m) **🔴 UI-004 COMPLETION VALIDATION** — the delivery report presents the DA's completion self-check; ITRGA will independently apply the **constitutional validation** (governing hierarchy Docs 00–16 · no scope expansion · no new analysis/live-data/capability · governance preserved · research-only · no execution pathways · UI-001/UI-002 unmodified · single shell · **Gate CLOSED**) **AND the Doc 16 brand validation (B-1…B-7)**.

---

## 7. Determination rule

**Approved** requires: build-identity confirmed; (b) all five named completion tests displayed passing; (c) whole-surface no-recompute grep clean; (d) whole-surface no-actuation grep clean; (f) verbatim-verdict + no-cherry-picking reaffirmed; (g) no-drift + head unchanged + no new dependency + no registry/route change; (h) completion regression green with actual totals (gated run exit 0); **(i) the §5 HARD BROWSER GATE satisfied — both (A) and (B) served (a missing shot ⇒ Corrective, not Observation)**; (j) route/responsive/keyboard/a11y browser evidence; (k) Doc 16 brand self-check + browser proof pass (a material brand violation ⇒ Corrective per Part XIV); (l) networked CI exit 0 + sentinel (or waived env-flake); (m) constitutional + brand completion validation clean.

A single CRITICAL, a missing §5 screenshot, or any unmet mandatory evidence item ⇒ **Corrective Actions Required / Rejected.**

**On Approved: ITRGA will declare 🏛️ UI-004 — RESEARCH & INTELLIGENCE WORKSPACE — COMPLETE** (continuous research workflow over existing governed artifacts on the UI-001/UI-002 shell; presentation-only; verbatim-verdict-faithful; no-cherry-picking; Doc 12 §6 / Doc 16 conformant; regression passed; ITRGA review complete). **UI-004 completion does NOT open the Gate or authorize execution.**

Future after UI-004: UI-005 Investigation & Planning (Doc 12 §7 — **request Design Plan first**, then Build Order), UI-006 Artifact Explorer (inherits deferred collection/tag mutation), UI-007/UI-008/UI-009; and, separately, the Production Readiness Certification track (Doc 11, HELD).

**DA does not self-approve. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.**

**We don't guess. We prove.**

*— AXIOM ITRGA*
