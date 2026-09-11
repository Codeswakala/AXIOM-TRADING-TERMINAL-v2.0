# BUILD ORDER — UI-003-P02
## Watchlists via Existing Preferences (symbol-ids only · no new table · R-1 / R-2)

**Issuing authority:** Institutional Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-003 · **Phase:** P02
**Predecessor:** `ITRGA_REVIEW_UI-003-P01.md` — **APPROVED** (authorizes this order)
**Governing:** Doc 12 §5; design plan §6/§10 (UI-003-P02); binding refinements **R-1/R-2/R-4/R-6**; W7-U02 persistence contract.
**Baseline (must be unchanged):** v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 32f/132t.
**Motto:** *We don't guess. We prove.*

---

## 1. Objective
Implement operator **watchlists as presentation preferences** using the existing `operator_workspace_preferences` table — **symbol/timeframe ids only, NO new table (R-1).** Presentation only: no execution/actuation, Gate CLOSED, no new backend logic beyond reusing the existing preference read/write path.

## 2. Scope IN (per accepted plan UI-003-P02)
1. **Watchlist model** — symbol/timeframe **ids only**, stored in `operator_workspace_preferences.layout_config` under key `professional-market-workspace-v1` (per §6.2 sketch).
2. **Preference read/write via the existing preference API** — reuse the W7-U02/P04(UI-001) path; **no new endpoint** unless strictly necessary (if any, read/write of preferences only, no execution surface).
3. **Forbidden-field validation** — reject quantity/position/order/side/buy/sell/broker/account/balance/margin/capital/allocation/stop_loss/take_profit/pnl/open_gate/allow_execution (§6.3).
4. **Operator scoping** inherited from the existing endpoint.
5. Watchlist reorder **only if keyboard-accessible** (R-4); else defer to P04.

## 3. Scope OUT (do NOT implement)
- **Any new table/migration/column** (R-1 — reuse only; if the DA believes a new table is unavoidable, STOP and request an ITRGA amendment).
- Chart overlays / research markers / annotation integration — P03 (R-3). Market-status full/responsive — P04.
- Any positions/quantities/orders/P&L in watchlist payloads; any execution/actuation/AI; any new dependency; any new analysis.

## 4. Constitutional & architectural guardrails (binding)
- **R-1** — watchlists in existing `operator_workspace_preferences`; **no new table/migration/column**; head `20260717_0037` (prove; `information_schema` if a column is alleged).
- **🔴 R-2** — **one inline raw `psql SELECT` read-back** on the persisted watchlist row (see §5b); **an API read-back NEVER substitutes.**
- Forbidden-field validation + operator-scoping preserved (W7-U02 contract); no secrets persisted.
- **UG-1/UG-2** — no execution/actuation; watchlists store symbol references only.
- **UG-3/UG-15/R-6** — no backend/schema change beyond reused persistence; no new dependency; UI-only diff (no-drift substitute); Level-I bar.
- **No regression** — all UI-001/UI-002/UI-003-P01 tests green.

## 5. MANDATORY EVIDENCE (operator-run on target; blank/errored grep = R7 non-result)
**(a) Build-identity** — `sed -n '1,15p'` of the P02 delivery report; confirm it is OF UI-003-P02.
**(b) 🔴 R-2 raw psql read-back (MANDATORY — no API substitution):**
  - a **raw `psql SELECT`** on `operator_workspace_preferences WHERE workspace_key='professional-market-workspace-v1'` showing the persisted `layout_config` `watchlists` array contains **symbol/timeframe ids only** — and **NO** forbidden fields (quantity/position/order/side/broker/account/margin/capital/stop/target/pnl/gate).
  - `alembic current` = `20260717_0037`; if any new column alleged, `information_schema.columns` on `operator_workspace_preferences` unchanged.
  - (Because this reuses an existing table, the full orphan-JOIN battery is NOT required — but if a new row-shape is written, include the audit no-orphan + `operator_id → operators.id` JOINs, `orphan_count 0`.)
**(c) Named tests (MUST be DISPLAYED passing by name — verbose reporter):**
  - `test_ui003_watchlists_use_operator_workspace_preferences_no_new_table`
  - `test_ui003_watchlists_store_symbol_ids_only_no_positions_orders_or_accounts`
  - `test_ui003_watchlists_reject_execution_broker_account_payload_fields`
  - `test_ui003_watchlists_are_keyboard_operable_and_accessible`
  - `test_ui003_watchlist_persistence_preserves_alembic_head`
**(d) Symbol-ids-only + no-forbidden-field proof** — grep/test that the watchlist payload/model contains symbol/timeframe ids only; forbidden-field validation rejects the barred set.
**(e) No-actuation source grep** — watchlist/market source (tests excluded) → clean.
**(f) No-drift substitute (R-6)** — per-phase no-backend/schema/dep test; `alembic current` = `20260717_0037`; **`package.json`/`package-lock.json` content unchanged**; no-new-endpoint grep.
**(g) Regression** — backend `pytest -q` **≥414 passed** (incl. `test_workspace_preferences.py` green); frontend Vitest **>32f/132t** all passing; TS clean; build + bundle delta.
**(h) Browser (served session) — R-6** — shots: watchlist UI in the market workspace; add/remove a symbol; **keyboard-operable** watchlist; **watchlist restored after re-login** (persistence); Gate CLOSED/research framing; logged-out block.
**(i) Networked CI (R-6)** — `scripts/local_ci.sh` → `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0` (or the TD-W6-CI-AUDIT offline-audit env-flake AFTER substantive gates green — record; disposition via operator).

## 6. Acceptance criteria (Determination: Approved · Approved with Observations · Corrective Actions Required · Rejected)
**Approved** requires: build-identity confirmed; **(b) R-2 inline raw psql read-back showing symbol/timeframe ids only + no new table/column + head unchanged** (*a missing/API-only persistence proof, or any forbidden field / new table ⇒ Corrective*); (c) all five named tests displayed passing; (d) symbol-ids-only + forbidden-field-rejection proven; (e) no-actuation grep clean; (f) no-drift substitute + no new dependency; (g) regression green with actual totals; (h) browser watchlist add/remove/keyboard/restore + framing/logged-out; (i) networked CI exit 0 + sentinel (or waived env-flake). **Only Approved / Approved-with-Observations authorizes `BUILD_ORDER_UI-003-P03` (Chart Overlays, Research Markers & Annotation Integration; binds R-3 inert read-only markers).**

*We don't guess. We prove.*
