# BUILD ORDER — UI-006-P03

**Lineage, Relationships & Advanced Filtering** — *(Read-Only)*

| Field | Value |
|---|---|
| Issuing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-006 — Unified Research Artifact Explorer |
| Phase | **UI-006-P03** (final read-only phase before mutation) |
| Predecessor verdict | `docs/ITRGA_REVIEW_UI-006-P02.md` — ✅ Approved with Observations |
| Governing docs | Doc 12 §8, `UI-006_ENGINEERING_DESIGN_PLAN.md` §10 (P03)/§8, `ITRGA_REVIEW_UI-006_DESIGN_PLAN.md` (R-1…R-8), Doc 16 |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend **51f/226t** |
| Governance Gate | CLOSED (must remain closed) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Purpose & scope

Add **lineage**, **cross-artifact relationships**, and **advanced filtering** to the explorer — as **read-only disclosure of stored relationships**. Filtering is **in-memory only** (no saved filters — design-plan Q6). **This phase remains strictly READ-ONLY (R-2); it is the FINAL read-only phase before the P04/P05 mutation phases.** No-cherry-picking is the spine.

**IN scope:**
1. Lineage view — surface stored lineage/source-ids/report-hash relationships between artifacts (disclosure, reusing UI-004/UI-005 patterns).
2. Cross-artifact relationships — artifact↔collection, artifact↔tag, artifact↔linked-ids as stored (read-only).
3. Advanced filtering — in-memory filter by family/status/tag/collection/symbol-timeframe ids; filtered views must never claim full-scope truth.

**OUT of scope (do NOT build):**
- **Any mutation** (P04 collections / P05 tags), completion (P06).
- Any collection/tag/membership create/update/delete (R-2/R-4 — P03 is read-only).
- **Saved filters / any persistence** (Q6 — in-memory only; R-3).
- Any recompute / inference / re-derivation / reclassification / analytics engine / relationship *inference* / external AI-LLM (R-6/M-5) — relationships are **stored**, not computed.
- Any new table / migration / dependency / endpoint / **registry route** change (R-1/R-3).
- Any order/broker/account/position/balance/margin/capital/allocation/real-P&L/live/go-live/execute/Gate path (M-4).

---

## 2. Binding refinements applied (R-1…R-8)

- **R-1** — Enhance existing `/research-management`; no new route; 14-field registry contract unchanged.
- **R-2** — **P03 is strictly READ-ONLY** — no mutation control, no persistence write.
- **R-3** — No new table/migration/dependency; **no saved-filter persistence** (in-memory only); alembic `20260717_0037`.
- **R-4** — Mutation deferred to P04/P05.
- **R-6 (SPINE)** — relationships/lineage are **stored, not inferred/computed**; no-recompute grep clean; **no-cherry-picking** — advanced filtering shows scope/sample/uncertainty/limitations and never presents a filtered subset as full-scope truth unless the stored artifact declares that scope.
- **R-8** — Level-I evidence + Doc-16 brand + regression ≥ baseline, no test lost + whole-surface no-actuation grep (M-4 expanded).

---

## 3. Mandatory named tests (MUST be DISPLAYED passing by name — verbose reporter)

1. `test_ui006_lineage_and_relationships_render_stored_links_read_only_no_inference`
2. `test_ui006_advanced_filtering_is_in_memory_only_no_persistence`
3. `test_ui006_filtered_views_preserve_no_cherry_picking_scope_and_limitations`
4. `test_ui006_lineage_relationships_filtering_contain_no_mutation_actuation_or_gate_path`
5. `test_ui006_lineage_relationships_filtering_accessibility_and_doc16_brand_hold`

---

## 4. Full mandatory evidence checklist (Level-I, operator-run on target)

Windows/PowerShell `C:\Users\Swakala\.vscode\AXIOM\axiom`; PostgreSQL `axiom`/`axiom_dev_password` db `axiom`; admin `admin`/`admin123`.

- (a) **Build identity** — delivery report + transcript header grep proving pack is OF UI-006-P03.
- (b) **5 named tests DISPLAYED passing** by name (verbose reporter).
- (c) **🔴 R-6 relationships-are-stored-not-inferred + no-recompute grep CLEAN** — `inferSignal|runInference|authoritativeRecompute|emitSignal|generateSignal|generateScenario|inferRelationship|recompute|recalculat|deriveConfidence|reclassif|summariz.*(ai|llm|gpt)|new .*Engine|/api/v1/orders`; **AND external-AI grep CLEAN** — `openai|gpt|external_llm|llm_summary|ai_summary`; named test #1.
- (d) **🔴 In-memory filtering / no persistence proof** — no `operator_workspace_preferences` write, no saved-filter key (grep + named test #2).
- (e) **🔴 No-cherry-picking** — filtered views retain scope/sample/uncertainty/limitations and do not claim full-scope truth (named test #3).
- (f) **🔴 R-2/R-4 read-only proof** — no collection/tag/membership create/update/delete control (grep + named test #4).
- (g) **🔴 Whole-surface no-actuation grep CLEAN** (M-4 expanded): `buy|sell|place_order|execute|go-live|connect-broker|broker|account_id|order_ticket|position|balance|margin|capital|allocation|real_pnl|open_gate|allow_execution`.
- (h) **No-drift substitute** — `alembic current` = `20260717_0037`; `package.json`/`package-lock.json` content unchanged (no new dep); no new endpoint grep; **no registry/route change** (R-1); **no persistence** (R-3).
- (i) **Regression** — frontend Vitest **≥51f/226t** all passing (no test lost; verify FULL total; print the vitest sentinel alongside the CI sentinel); backend `pytest -q` **≥414 passed**; TS clean; production build + bundle delta. **Gated full run must exit 0.**
- (j) **🔴 Doc 16 brand B-1…B-7** — palette / `--font-mono` / `.mono` numerics / no hardcoded color in production TSX / unified iconography / institutional-not-retail / brand a11y (never color alone).
- (k) **Browser served-session screenshots** — logged-in `/research-management` lineage/relationships view + advanced filtering (with scope/limitations preserved); GATE CLOSED / RESEARCH-ONLY framing + mutation-deferral copy; logged-out `/login` block.
- (l) **Networked local CI** `LOCAL_CI_EXIT_CODE: 0` + sentinel (prefer networked per OBS-P02-1); OR the TD-W6-CI-AUDIT offline npm-audit env-flake after substantive gates green → waiver; OR `LOCAL_CI_EXIT_CODE: 1` attributable **solely** to the tracked TD-UI-POSTCSS-HIGH after substantive gates green — disclosed, not relabeled. **Any other nonzero cause is a finding.**
- (m) **TD-UI-POSTCSS-HIGH note** — P03 introduces no dependency change; residual OPEN (remediation Build Order due at/before UI-006-P06). **This is the last read-only phase; P04 introduces the first mutation — the persistence-capture control and no-underlying-artifact-mutation discipline bind from P04.**

---

## 5. Determination rule

A single CRITICAL, any mutation control or saved-filter persistence present in this read-only phase, or any unmet mandatory evidence item ⇒ Corrective Actions Required / Rejected. Only **Approved** or **Approved with Observations** authorizes the next Build Order (**UI-006-P04 — Collections & Memberships Organization Mutation**, the first mutation phase).

**DA does not self-approve. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.**

**We don't guess. We prove.**

*— AXIOM ITRGA*
