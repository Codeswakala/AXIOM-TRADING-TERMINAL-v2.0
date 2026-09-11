# BUILD ORDER — UI-006-P05

**Tags Organization Mutation** — *SECOND MUTATION PHASE*

| Field | Value |
|---|---|
| Issuing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-006 — Unified Research Artifact Explorer |
| Phase | **UI-006-P05** (second mutation phase) |
| Predecessor verdict | `docs/ITRGA_REVIEW_UI-006-P04_ATTEMPT3_APPROVED.md` — ✅ Approved (corrective closed) |
| Governing docs | Doc 12 §8, `UI-006_ENGINEERING_DESIGN_PLAN.md` §5/§10 (P05), `ITRGA_REVIEW_UI-006_DESIGN_PLAN.md` (R-1…R-8, esp. R-4/R-5/R-7 + M-1…M-3), Doc 16 |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend **53f/236t** |
| Governance Gate | CLOSED (must remain closed) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Purpose & scope

Introduce **tag organization mutation** — create tag labels attached to an artifact reference, and delete a tag **only if existing API support is proven inline** — over the existing **W7-U03 `research_tags`** store. Same mutation discipline proven at P04. Organization-only; no underlying-artifact mutation.

**IN scope:**
1. **Tag create** — a tag label attached to an artifact **reference** (tag + artifact_type + artifact_id only) via the existing W7-U03 create-tag endpoint/repository (operator-scoped).
2. **Tag delete** — ONLY if existing backend AND client API support is proven inline (R-5); otherwise NOT in scope this phase (create-only).

**OUT of scope (do NOT build):**
- Completion (P06).
- **Any mutation of underlying artifacts** or their stored values (M-1/M-2) — tagging an artifact must never change any signal/report/validation/economic/scenario/plan/journal/execution artifact or any stored verdict/confidence/validation/economic/lineage value.
- Copying artifact **content/payloads** into tag rows (tag label + artifact reference ids only).
- Tag edit/label-rename (design-plan §5: NOT proposed; requires separate ITRGA authorization — use delete+create only if API supports and ITRGA authorizes).
- **Any new table / migration** (M-3 — reuse existing W7 `research_tags`; alembic stays `20260717_0037`).
- Any new dependency / endpoint / **registry route** change (R-1/R-3).
- Any order/broker/account/position/balance/margin/capital/allocation/real-P&L/live/go-live/execute/Gate path (M-4).
- Any recompute / inference / reclassification / analytics engine / external AI-LLM (R-6/M-5).

---

## 2. Binding refinements applied (R-1…R-8)

- **R-1** — Enhance existing `/research-management`; no new route; 14-field registry contract unchanged.
- **R-3** — **No new table/migration/dependency**; alembic `20260717_0037`. Mutation writes only to existing W7 `research_tags`.
- **R-4 (HARD)** — Mutation is **ORGANIZATION-ONLY** (M-1/M-2). No underlying-artifact mutation. Mandatory named tests: **`..._does_not_modify_underlying_artifact_values`** AND **`..._reject_order_account_execution_and_verdict_fields`**.
- **R-5** — **Create-first.** Tag **delete authorized only if existing backend AND client API support is proven inline**; otherwise create-only. No tag edit/rename.
- **R-6** — no-recompute + external-AI grep clean; verbatim posture on any displayed artifact value.
- **R-7 (persistence-capture control — HARD)** — INLINE raw psql: served/app tag save → `SELECT ≥ 1 row` from the CORRECT W7 table (`research_tags`) **keyed on the SAME artifact reference the UI wrote** (tag + artifact_type + artifact_id) → `operator_id → operators.id` no-orphan join → **forbidden-field-present = false** → `alembic current = 20260717_0037`. **API / in-process read-back NEVER substitutes; `(0 rows)` is disproof.** Also prove the referenced source artifact's stored values are unchanged after the tag mutation. **⚠️ LESSON FROM P04: the served tag add and the raw psql query MUST target the SAME artifact reference/id — two P04 corrective cycles were lost to a query/UI id mismatch. Bind the evidence script to the exact reference the UI wrote.**
- **R-8** — Level-I evidence + Doc-16 brand + regression ≥ baseline (**53f/236t**), no test lost + whole-surface no-actuation grep (M-4 expanded).

---

## 3. Mandatory named tests (MUST be DISPLAYED passing by name — verbose reporter)

1. `test_ui006_tags_mutate_existing_research_tag_store_only`
2. `test_ui006_tags_write_labels_and_artifact_references_not_source_payloads`
3. `test_ui006_tags_reject_order_account_execution_and_verdict_fields` **(forbidden-field-rejection — CRITICAL)**
4. `test_ui006_tag_mutation_does_not_modify_underlying_artifact_values` **(no-underlying-artifact-mutation — CRITICAL)**
5. `test_ui006_tag_mutation_accessibility_brand_and_operator_scope_hold`

---

## 4. Full mandatory evidence checklist (Level-I, operator-run on target)

Windows/PowerShell `C:\Users\Swakala\.vscode\AXIOM\axiom`; PostgreSQL `axiom`/`axiom_dev_password` db `axiom`; admin `admin`/`admin123`.

- (a) **Build identity** — delivery report + transcript header grep proving pack is OF UI-006-P05.
- (b) **5 named tests DISPLAYED passing** by name (verbose reporter) — **including the two CRITICAL tests #3/#4.**
- (c) **🔴 R-7 persistence-capture (tag create)** — served/app tag save → INLINE raw psql `SELECT ≥1 row` from `research_tags` **keyed on the SAME tag + artifact_type + artifact_id the UI wrote** (tag label + artifact reference only; **no source payload/content**) + `operator_id → operators.id` no-orphan join + `alembic current = 20260717_0037`. **API read-back does NOT substitute; `(0 rows)` = disproof.**
- (d) **🔴 M-1/M-2 no-underlying-artifact-mutation proof** — before/after raw psql fingerprint of the referenced source artifact (verdict/confidence/validation/economic/lineage/status) proving it is UNCHANGED by the tag mutation; named test #4.
- (e) **🔴 Forbidden-field-rejection** — a tag payload carrying order/account/broker/execution/verdict fields is rejected; named test #3.
- (f) **🔴 R-5 deletion gating** — if tag delete is included, INLINE proof of existing backend AND client API support (endpoint + client method) + before(1)/after(0) raw psql on the same tag row; if NOT included, state explicitly (create-only this phase).
- (g) **🔴 M-3 schema audit** — `research_tags` columns + `forbidden_org_column_count = 0` (order/broker/account/position/…/verdict/confidence/validation/economic/source content).
- (h) **🔴 R-6 no-recompute + external-AI grep CLEAN**; **🔴 whole-surface no-actuation grep CLEAN** (M-4 expanded): `buy|sell|place_order|execute|go-live|connect-broker|broker|account_id|order_ticket|position|balance|margin|capital|allocation|real_pnl|open_gate|allow_execution`.
- (i) **No-drift substitute** — `alembic current` = `20260717_0037` (**no new migration**); `package.json`/`package-lock.json` content unchanged (no new dep); no new endpoint grep (mutation uses EXISTING W7 endpoints); **no registry/route change** (R-1).
- (j) **Regression** — frontend Vitest **≥53f/236t** all passing (no test lost; verify FULL total; print the vitest sentinel alongside the CI sentinel); backend `pytest -q` **≥414 passed**; TS clean; production build + bundle delta. **Gated full run must exit 0.**
- (k) **🔴 Doc 16 brand B-1…B-7** — palette / `--font-mono` / `.mono` numerics (tag/artifact ids) / no hardcoded color in production TSX / unified iconography / institutional-not-retail / brand a11y (never color alone).
- (l) **Browser served-session screenshots** — logged-in `/research-management` performing a tag create against an artifact reference (organization-only, operator-scoped), showing the created tag; GATE CLOSED / RESEARCH-ONLY framing; **no order/account/execution/verdict field in the tag UI**; logged-out `/login` block.
- (m) **Networked local CI** `LOCAL_CI_EXIT_CODE: 0` + sentinel (prefer networked per prior OBS); OR the TD-W6-CI-AUDIT offline npm-audit env-flake after substantive gates green → waiver; OR `LOCAL_CI_EXIT_CODE: 1` attributable **solely** to the tracked TD-UI-POSTCSS-HIGH after substantive gates green — disclosed, not relabeled. **Any other nonzero cause is a finding.**
- (n) **TD-UI-POSTCSS-HIGH note** — P05 introduces no dependency change; residual OPEN. **The dependency-remediation Build Order is due at/before UI-006-P06 (OBS-DP-1) — the DA should be prepared to schedule it at P06.**

---

## 5. Determination rule

A single CRITICAL, a weak/absent persistence-capture (R-7 — API read-back, `(0 rows)`, or a query/UI id mismatch as in the P04 corrective cycles), a weak/absent no-underlying-artifact-mutation or forbidden-field-rejection proof, any underlying-artifact/verdict mutation, a new table/migration, deletion without proven API support, or any unmet mandatory evidence item ⇒ Corrective Actions Required / Rejected. Only **Approved** or **Approved with Observations** authorizes the next Build Order (UI-006-P06 — Completion Checkpoint).

**DA does not self-approve. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.**

**We don't guess. We prove.**

*— AXIOM ITRGA*
