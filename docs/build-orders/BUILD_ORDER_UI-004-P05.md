# BUILD ORDER — UI-004-P05  *(REISSUED)*

**Research Artifacts, Collections & Saved-View Preferences**

> **Reissue note (2026-07-24):** This Build Order is reissued at operator request. Content is unchanged and remains fully binding — same phase identity, same scope, same mandatory evidence. This supersedes the prior copy of `BUILD_ORDER_UI-004-P05.md`; no scope has been added or relaxed.

| Field | Value |
|---|---|
| Issuing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-004 — Research & Intelligence Workspace |
| Phase | **UI-004-P05** |
| Status | **REISSUED** (operator request) — original issuance authorized by operator "authorized" following P04 Approved-w-Obs |
| Predecessor verdict | `docs/ITRGA_REVIEW_UI-004-P04.md` — ✅ Approved with Observations |
| Governing docs | Doc 12 §6, `UI-004_ENGINEERING_DESIGN_PLAN.md` §6/§6.3, `ITRGA_REVIEW_UI-004_DESIGN_PLAN.md` (R-1…R-7), Doc 16 Brand Governance Standard |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend **41f/175t** |
| Governance Gate | CLOSED (must remain closed) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Purpose & scope

UI-004-P05 completes the Research & Intelligence workspace by surfacing **research artifacts and their collection/tag context** and, optionally, persisting **presentation-only saved-view state**. This is the phase that touches persistence, so it carries the persistence-capture control and R-2/R-4 as hard gates.

**IN scope:**
1. **Research artifact context surface** — list/link existing research artifacts (report ids, signal ids, journal references, collection membership, tag associations, source artifact ids, artifact metadata) sourced from existing read APIs: `fetchResearchManagementBundle`, `fetchResearchCollections`, `fetchResearchTags`, `fetchJournalEntries`, and the intelligence/advisory/analytics bundles already in use.
2. **Collections & tags as READ-ONLY context** (R-4) — display collections/tags to organize and navigate existing artifacts; drilldown/link only. **No create/update/delete mutation surface** (collection/tag mutation defers to UI-006 Artifact Explorer).
3. **Saved-view preferences (OPTIONAL — only if implemented this phase)** — presentation-only view state reusing the existing `operator_workspace_preferences` store under key **`research-intelligence-workspace-v1`**, `layout_config` carrying **ids / visibility / filter prefs only** per §6.3 sketch: `active_view`, `selected_artifact` (`artifact_type` + `artifact_id` only), `visible_sections`, `report_filters` (report_family/symbol/timeframe ids), `expanded_panels`. **No copied report body, no analytics payload, no positions/orders/accounts/balances, no secrets.**

**OUT of scope (do NOT build):**
- Any new table / migration / column / backend schema change (default: **no new table**).
- Collection/tag mutation (create/update/delete) — deferred to UI-006 (R-4).
- Copying source/report/artifact **content** into preference state (ids/visibility/filters only).
- UI-004-P06 completion checkpoint (separate phase).
- Any recompute / re-derivation / reclassification / upgrade of validation or economic-usefulness verdicts (carried R-6).
- Client-side analytics engine; external AI/LLM; live/real data; broker/account/order/execution/Gate path.
- Any new dependency, new endpoint, or workspace-registry / route change (R-1: enhance existing `/intelligence`, no `/research-intelligence` route).

---

## 2. Binding refinements carried into P05

- **R-1** — Enhance existing `/intelligence`; **no registry/route change**. Prove `research.intelligence` / `/intelligence` only; no `/research-intelligence`.
- **R-2 (BINDS THIS PHASE if saved-state is implemented)** — Default is **no new table**; saved-view state via `operator_workspace_preferences`, key `research-intelligence-workspace-v1`, ids/visibility/filter only. **If saved state is implemented, the persistence-capture control (§4) is MANDATORY: an INLINE raw psql save→SELECT returning ≥1 populated row on the CORRECT table, ids/prefs only with no forbidden fields, plus `alembic current` = head. An API / in-process read-back NEVER substitutes. A `(0 rows)` read-back is DISPROOF, not proof.** If saved state is NOT implemented this phase, state that explicitly and no psql is required — but then no persistence test may claim persistence.
- **R-4** — Collections/tags **READ-ONLY**. No mutation surface. Prove absence of create/update/delete controls.
- **R-6 (no-recompute spine)** — verbatim rendering; grep clean for `inferSignal|runInference|authoritativeRecompute|emitSignal|generateSignal|recompute|recalculat|deriveConfidence|reclassif|summariz.*(ai|llm|gpt)|new .*Engine|/api/v1/orders`.
- **R-7** — Level-I operator-run evidence + Doc-16 brand gate + full-suite ≥ baseline, no test lost.

---

## 3. Mandatory named tests (must be DISPLAYED passing by name)

1. `test_ui004_research_artifacts_render_existing_collections_tags_and_ids_read_only`
2. `test_ui004_collections_and_tags_expose_no_create_update_or_delete_mutation` (R-4)
3. `test_ui004_saved_view_preferences_persist_ids_visibility_filters_only_no_report_body` — **if saved state implemented**; else provide `test_ui004_no_saved_view_persistence_is_implemented_this_phase` proving absence
4. `test_ui004_research_artifact_surface_contains_no_recompute_inference_or_signal_generation` (R-6)
5. `test_ui004_research_artifact_surface_contains_no_execution_order_broker_account_or_gate_path`
6. `test_ui004_research_artifacts_accessibility_and_brand_markers_hold` (Doc-16)

---

## 4. Persistence-capture control (ONLY if saved-view state is implemented)

Provide, INLINE in the operator transcript:
- The committing path (frontend save call + confirmation it targets `operator_workspace_preferences`).
- **Raw psql** `SELECT` on `operator_workspace_preferences WHERE workspace_key = 'research-intelligence-workspace-v1'` returning **≥1 populated row** (a save→SELECT, not an empty read-back).
- Proof the payload contains **only** ids / visibility / filter prefs (no report body, no positions/orders/accounts/balances/margin, no secrets).
- `operator_id → operators.id` JOIN (identity table is `operators`, not `users`).
- `alembic current` = `20260717_0037` (head) — confirming **no new migration**.

If saved-view state is NOT implemented this phase: say so explicitly; §4 is waived; test #3 becomes the absence-proof variant.

---

## 5. Full mandatory evidence checklist (Level-I, operator-run on target)

Windows/PowerShell `C:\Users\Swakala\.vscode\AXIOM\axiom`; PostgreSQL `axiom`/`axiom_dev_password` db `axiom`; admin `admin`/`admin123`.

- (a) **Build identity** — delivery report + transcript header grep proving pack is OF UI-004-P05 (not stale/wrong-phase/concatenated).
- (b) **6 named tests DISPLAYED passing** by name (verbose reporter).
- (c) **🔴 R-6 no-recompute grep CLEAN** on the artifact/collections surface source.
- (d) **R-4 read-only proof** — no create/update/delete mutation control on collections/tags (grep + named test).
- (e) **Persistence-capture (§4)** if saved state implemented — inline raw psql save→SELECT ≥1 row + no forbidden fields + `operator_id→operators.id` JOIN + alembic head; OR explicit absence declaration.
- (f) **No-actuation grep** clean (buy/sell/place_order/execute/go-live/connect-broker/account_id/order_ticket/open_gate/allow_execution).
- (g) **No-drift substitute** — `alembic current` = `20260717_0037`; `package.json`/`package-lock.json` content unchanged (no new dep); no new endpoint grep; **no registry/route change** (R-1).
- (h) **Full-suite regression** — frontend **≥41f/175t, no test lost** (verify FULL total, not a filtered `-t` run); backend **≥414**. **If the gated full run flakes on the two UI-001/UI-002 route-loop timeouts (OBS-P04-1), the DA must add an explicit `testTimeout` so the gate is deterministic — and any intervening red gate MUST be surfaced in the delivery report, not silently superseded.**
- (i) **Doc-16 brand B-1…B-7** — constitutional palette tokens / `--font-mono` / `.mono` numerics / no hardcoded color in production TSX / unified iconography / institutional-not-retail copy / brand a11y (never color alone).
- (j) **Browser served-session screenshots** — logged-in `/intelligence` showing the artifact/collections/tags context READ-ONLY; **AND (closing OBS-P04-2) a served screenshot of the P04 Validation & Economic-Usefulness Integrity panel showing at least one verbatim `research_only` / `not_assessed` / `warning:POORLY_CALIBRATED` verdict**; logged-out `/login` block.
- (k) **Networked local CI** exit 0 + sentinel — **fix the sentinel variable typo (OBS-P04-3);** if the offline npm-audit env-flake (TD-W6-CI-AUDIT) recurs after substantive gates are green, record it and request waiver (do not relabel green).

---

## 6. Observation closures folded into P05 intake

- **OBS-P04-1** — add explicit `testTimeout` to the two timeout-fragile route-loop tests so the gated full-suite run is deterministic; surface any intervening red gate in the delivery report.
- **OBS-P04-2** — supply the served P04-panel verbatim-verdict screenshot (item (j)).
- **OBS-P04-3** — fix the `LOCAL_CI_EXIT_CODE` sentinel variable typo.

---

## 7. Determination rule

A single CRITICAL, or any unmet mandatory evidence item, ⇒ Corrective Actions Required / Rejected. Only **Approved** or **Approved with Observations** authorizes the next Build Order (UI-004-P06 completion checkpoint).

**DA does not self-approve. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.**

**We don't guess. We prove.**

*— AXIOM ITRGA*
