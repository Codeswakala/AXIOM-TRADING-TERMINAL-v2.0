# BUILD ORDER — UI-006-P02

**Unified Artifact Catalog & Metadata Detail** — *(Read-Only)*

| Field | Value |
|---|---|
| Issuing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-006 — Unified Research Artifact Explorer |
| Phase | **UI-006-P02** |
| Predecessor verdict | `docs/ITRGA_REVIEW_UI-006-P01.md` — ✅ Approved with Observations |
| Governing docs | Doc 12 §8, `UI-006_ENGINEERING_DESIGN_PLAN.md` §10 (P02), `ITRGA_REVIEW_UI-006_DESIGN_PLAN.md` (R-1…R-8), Doc 16 |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend **50f/221t** |
| Governance Gate | CLOSED (must remain closed) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Purpose & scope

Build the **unified artifact catalog** across artifact families and the **metadata detail** view — as **read-only progressive disclosure of stored fields** (UI-004 report-viewer/drilldown patterns reused). **This phase remains strictly READ-ONLY (R-2).** No mutation.

**IN scope:**
1. Unified catalog listing artifacts across families (ids, family/type, key metadata) sourced from existing read seams (established in the P01 inventory).
2. Metadata detail per artifact — stored fields (status/verdict/confidence/uncertainty/limitations/sample count/report_hash/lineage/source ids) rendered **verbatim** (as-stored), no recompute.
3. Read-only collection/tag context shown alongside artifacts (display only; mutation still deferred to P04/P05).

**OUT of scope (do NOT build):**
- Lineage/relationships/advanced filtering (P03), **any mutation** (P04 collections / P05 tags), completion (P06).
- Any collection/tag/membership create/update/delete (R-2/R-4 — P02 is read-only).
- Any recompute / inference / re-derivation / reclassification / analytics engine / external AI-LLM (R-6/M-5).
- Any persistence / new table / migration / dependency / endpoint / **registry route** change (R-1/R-3).
- Any order/broker/account/position/balance/margin/capital/allocation/real-P&L/live/go-live/execute/Gate path (M-4).

---

## 2. Binding refinements applied (R-1…R-8)

- **R-1** — Enhance existing `/research-management`; no new route; 14-field registry contract unchanged.
- **R-2** — **P02 is strictly READ-ONLY** — no mutation control, no persistence write.
- **R-3** — No new table/migration/dependency; alembic `20260717_0037`.
- **R-4** — Mutation deferred to P04/P05; collection/tag context is display-only.
- **R-6 (SPINE)** — verbatim metadata rendering; no-recompute grep clean; catalog/detail = disclosure of stored fields, not recompute; no-cherry-picking (scope/sample/uncertainty/limitations visible where shown).
- **R-8** — Level-I evidence + Doc-16 brand + regression ≥ baseline, no test lost + whole-surface no-actuation grep (M-4 expanded).

---

## 3. Mandatory named tests (MUST be DISPLAYED passing by name — verbose reporter)

1. `test_ui006_catalog_lists_existing_artifacts_across_families_read_only`
2. `test_ui006_metadata_detail_renders_stored_fields_verbatim_without_recompute`
3. `test_ui006_catalog_preserves_no_cherry_picking_scope_sample_and_limitations`
4. `test_ui006_catalog_contains_no_mutation_actuation_or_gate_path`
5. `test_ui006_catalog_accessibility_and_doc16_brand_markers_hold`

---

## 4. Full mandatory evidence checklist (Level-I, operator-run on target)

Windows/PowerShell `C:\Users\Swakala\.vscode\AXIOM\axiom`; PostgreSQL `axiom`/`axiom_dev_password` db `axiom`; admin `admin`/`admin123`.

- (a) **Build identity** — delivery report + transcript header grep proving pack is OF UI-006-P02.
- (b) **5 named tests DISPLAYED passing** by name (verbose reporter).
- (c) **🔴 R-2/R-4 read-only proof** — no collection/tag/membership create/update/delete control present (grep + named test #4); mutation still deferred.
- (d) **🔴 R-6 verbatim + no-recompute grep CLEAN** — metadata rendered as-stored; `inferSignal|runInference|authoritativeRecompute|emitSignal|generateSignal|generateScenario|recompute|recalculat|deriveConfidence|reclassif|summariz.*(ai|llm|gpt)|new .*Engine|/api/v1/orders` clean; **AND external-AI grep CLEAN** — `openai|gpt|external_llm|llm_summary|ai_summary`; named test #2.
- (e) **🔴 No-cherry-picking** — where the catalog/detail shows analytics/report fields, scope/sample counts/uncertainty/limitations remain visible (named test #3).
- (f) **🔴 Whole-surface no-actuation grep CLEAN** (M-4 expanded): `buy|sell|place_order|execute|go-live|connect-broker|broker|account_id|order_ticket|position|balance|margin|capital|allocation|real_pnl|open_gate|allow_execution`.
- (g) **No-drift substitute** — `alembic current` = `20260717_0037`; `package.json`/`package-lock.json` content unchanged (no new dep); no new endpoint grep; **no registry/route change** (R-1); **no persistence** (R-3).
- (h) **Regression** — frontend Vitest **≥50f/221t** all passing (no test lost; verify FULL total; print the vitest sentinel alongside the CI sentinel); backend `pytest -q` **≥414 passed**; TS clean; production build + bundle delta. **Gated full run must exit 0.**
- (i) **🔴 Doc 16 brand B-1…B-7** — palette / `--font-mono` / `.mono` numerics (artifact ids/hashes/sample counts) / no hardcoded color in production TSX / unified iconography / institutional-not-retail / brand a11y (never color alone).
- (j) **Browser served-session screenshots** — logged-in `/research-management` unified catalog + a metadata detail view showing verbatim stored fields; GATE CLOSED / RESEARCH-ONLY framing + mutation-deferral copy; logged-out `/login` block.
- (k) **Networked local CI** `LOCAL_CI_EXIT_CODE: 0` + sentinel (prefer networked per OBS-P01-1); OR the TD-W6-CI-AUDIT offline npm-audit env-flake after substantive gates green → waiver; OR `LOCAL_CI_EXIT_CODE: 1` attributable **solely** to the tracked TD-UI-POSTCSS-HIGH after substantive gates green — disclosed, not relabeled. **Any other nonzero cause is a finding.**
- (l) **TD-UI-POSTCSS-HIGH note** — P02 introduces no dependency change; residual OPEN (remediation Build Order due at/before UI-006-P06 per OBS-DP-1).

---

## 5. Determination rule

A single CRITICAL, any mutation control present in this read-only phase, or any unmet mandatory evidence item ⇒ Corrective Actions Required / Rejected. Only **Approved** or **Approved with Observations** authorizes the next Build Order (UI-006-P03 — Lineage, Relationships & Advanced Filtering, read-only).

**DA does not self-approve. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.**

**We don't guess. We prove.**

*— AXIOM ITRGA*
