# ITRGA REVIEW — UI-003-P02 (attempt 3 — corrective closed)
## Watchlists via Existing Preferences — R-2 raw-psql read-back

**Authority:** Institutional Technical Review & Governance Authority (ITRGA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-003 · **Phase:** P02
**Build Order:** `BUILD_ORDER_UI-003-P02.md` · **Supersedes:** attempt-1 (wrong report + R-2 absent) and attempt-2 (R-2 read-back returned 0 rows).
**Evidence:** `DELIVERY_REPORT_UI-003-P02.md` (correct), attempt-2 + **CA-P02(UI003)-3 rerun `operator results.md`** (save→read-back), watchlist-UI screenshot.
**Determination:** ✅ **APPROVED**
**Authorizes:** `BUILD_ORDER_UI-003-P03` (Chart Overlays, Research Markers & Annotation Integration; binds R-3 inert read-only markers).
**Motto:** *We don't guess. We prove.*

---

## 0. Build-identity — PASS
Correct P02 pack across the corrective sequence; CA rerun shows a real save + read-back on target. DA does not self-approve.

## 1. 🔴 R-2 raw psql read-back — NOW SATISFIED (save → SELECT, ≥1 clean row)
CA-P02(UI003)-3 required a populated read-back after an actual save. Proven, in correct order:

| Step | Evidence (line) | Result |
|---|---|---|
| Save preceded query | `PUT /api/v1/institutional-platform/workspace-preferences/331d5bc3… → 200` (L2–3) | ✅ real write first |
| Raw psql full-row SELECT | `preference_id 331d5bc3…`, `operator_id 90264969…`, `workspace_key professional-market-workspace-v1`, `layout_config.watchlists = [{watchlist_id: primary-market-watchlist, symbols:[EURUSD,BTCUSD], timeframes:[M1,H1,M5]}]` (L21) | ✅ **1 row, symbol/timeframe ids only** |
| Forbidden-field check | `forbidden_field_present = f` (L26) | ✅ no qty/position/order/broker/account/margin/capital/stop/target/pnl/gate |
| Count | `professional_market_watchlist_rows = 1` (L32) | ✅ ≥1 |
| `operator_id → operators.id` no-orphan JOIN | `operator_orphan_count = 0` (L39) | ✅ |
| audit no-orphan JOIN | `audit_orphan_count = 0` (L45) | ✅ |
| Alembic head | `20260717_0037 (head)` (L53) | ✅ no schema change |

**An API read-back did not substitute** — this is raw psql on the real table. P02's central claim (watchlists durably persist as symbol-ids-only in the existing `operator_workspace_preferences`, no new table) is now **proven on target.** The attempt-2 empty-read-back finding is resolved: the watchlist IS wired to durable persistence (the earlier `(0 rows)` was a query-before-save artifact).

## 2. Full P02 verification (across the corrective sequence)
| # | Requirement | Evidence | Verdict |
|---|---|---|---|
| R-1 no new table | reuses `operator_workspace_preferences`; head `20260717_0037`; full persistence-capture battery satisfied | **PASS** |
| R-2 raw psql read-back | §1 — 1 clean row, symbol-ids only, forbidden_field_present f, orphans 0 | **PASS** |
| Five named tests displayed passing | watchlists_use_op_prefs_no_new_table · store_symbol_ids_only_no_positions_orders_or_accounts · reject_execution_broker_account_payload_fields · keyboard_operable_accessible · persistence_preserves_alembic_head (attempt-1 L702–706) | **PASS** |
| Symbol-ids-only + forbidden-field rejection | tests + raw-DB forbidden_field_present f | **PASS** |
| No-actuation / no execution | symbol references only; no order/broker/account/gate | **PASS** |
| Regression + growth | backend **414**; frontend **33f/137t** (up from 32f/132t) | **PASS** |
| No new dependency / no-drift | package manifests unchanged; head unchanged | **PASS** |
| Networked CI | `LOCAL_CI_EXIT_CODE: 0` + sentinel | **PASS** |
| Browser (R-6) | watchlist UI (add/Focus/Remove, timeframes; "symbol and timeframe ids only — no positions/quantities/orders/accounts/brokers/margin/capital/P&L"); Gate CLOSED/research framing | **PASS** |
| Constitutional line | Gate CLOSED; symbol references only; no execution/AI | **PASS** |

## 3. Determination & rationale
**APPROVED.** The corrective is closed: the R-2 raw psql read-back now returns **one clean persisted watchlist row** — symbol/timeframe ids only, `forbidden_field_present = f`, count 1, both no-orphan JOINs 0 — after a real PUT-200 save, with `alembic current = 20260717_0037` and no new table (R-1). This is exactly the raw-DB proof the persistence-capture discipline requires (no API substitution). All five named tests, regression (backend 414, frontend 33f/137t), networked CI, and the watchlist-UI browser evidence are in place; the constitutional line holds (symbol references only, no positions/orders/execution, Gate CLOSED). Both prior correctives (wrong report; absent read-back) and the attempt-2 empty-read-back finding are resolved.

Per the UI-Transformation vocabulary, **Approved authorizes progression.** → **`BUILD_ORDER_UI-003-P03` (Chart Overlays, Research Markers & Annotation Integration) is authorized**, binding **R-3** (advisory-signal markers = inert read-only badges over existing records; a named test must prove markers are not signals/instructions and generate nothing) and carrying R-6.

Baseline of record: v0.62.0 · head `20260717_0037` · backend **414** · frontend **33f·137t**. Residuals unchanged & non-blocking: TD-W7-U07-RATE-GUARD, TD-W6-CI-AUDIT, UI-002-P04b.

*We don't guess. We prove.*
