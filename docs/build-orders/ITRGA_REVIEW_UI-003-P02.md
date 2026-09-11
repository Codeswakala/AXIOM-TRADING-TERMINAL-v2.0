# ITRGA REVIEW — UI-003-P02 (attempt 1)
## Watchlists via Existing Preferences — R-2 raw-psql read-back

**Authority:** Institutional Technical Review & Governance Authority (ITRGA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-003 · **Phase:** P02
**Build Order:** `BUILD_ORDER_UI-003-P02.md`
**Evidence submitted:** `DELIVERY_REPORT_UI-003-P01.md` (**WRONG — P01 report, not P02**), `operator results.md` (**concatenated P01+P02 transcript, 2477 lines**), 4 screenshots (chart workspace / annotations / login — P01-oriented, no watchlist UI shown).
**Determination:** ⛔ **CORRECTIVE ACTIONS REQUIRED**
**Authorizes:** *nothing* — `BUILD_ORDER_UI-003-P03` not authorized.
**Motto:** *We don't guess. We prove.*

---

## 0. Build-identity — TWO issues
| Artifact | Check | Status |
|---|---|---|
| Delivery report | File is **`DELIVERY_REPORT_UI-003-P01.md`**, self-declares **Phase UI-003-P01**. **The P02 delivery report was not attached.** | ⛔ **WRONG PACK** |
| `operator results.md` | **Concatenated**: opens with the **P01** evidence set (`Get-Content DELIVERY_REPORT_UI-003-P01.md`, L12), then includes a genuine **P02** run (74 P01 refs vs 26 P02). | ⚠️ **CONCATENATED** |
| Screenshots | Chart workspace + research annotations + login — **no watchlist UI** shown | ⚠️ P01-oriented |

## 1. 🔴 DECISIVE FAILURE — R-2 raw psql read-back ABSENT
P02's mandatory, order-defining gate (Build Order §5b/§6, binding refinement **R-2**) is the **one inline raw `psql SELECT`** on `operator_workspace_preferences WHERE workspace_key='professional-market-workspace-v1'` proving the persisted `watchlists` array holds **symbol/timeframe ids only** with no forbidden fields. Verified absent:
- **`grep -c psql` = 0** — there is **no raw DB command anywhere** in the transcript.
- No `layout_config` / `SELECT … preferences` / persisted-watchlist-row output of any kind.
- The Build Order is explicit: *"a missing/API-only persistence proof … ⇒ Corrective"* and the standing persistence-capture discipline (W7-U02/W4-U02/W6-U04) holds that **an API/in-process read-back NEVER substitutes for raw psql.**

The passing named test `test_ui003_watchlist_persistence_preserves_alembic_head` is **in-process** evidence — it confirms head is unchanged but does **not** prove a real watchlist row persisted to the DB with clean contents. So P02's central claim (watchlists durably persist as symbol-ids-only in the existing table) is **unproven on target.**

## 2. What DID pass (so the corrective is narrow)
| Check | Evidence (line) | Status |
|---|---|---|
| Five P02 named tests displayed passing | watchlists_use_op_prefs_no_new_table (L702) · store_symbol_ids_only (L703) · reject_execution_broker_account_payload_fields (L704) · keyboard_operable_accessible (L705) · persistence_preserves_alembic_head (L706) | **PASS (in-process)** |
| Regression + growth | frontend **33 files / 137 tests passed** (L1166–1167, up from 32f/132t = +5 P02 tests); backend **414 passed** (L1679, L2299) | **PASS** |
| Networked CI | `LOCAL_CI_EXIT_CODE: 0` (L2477) + sentinel | **PASS** |

The watchlist implementation appears complete and constitutionally aligned (symbol-ids-only + forbidden-field-rejection tests pass; no new table claimed). **But** none of that substitutes for the **operator-run raw psql read-back** that P02 was specifically ordered to produce.

## 3. Determination & required corrective actions
**CORRECTIVE ACTIONS REQUIRED.** Two correctives:

> **CA-P02(UI003)-1 — Supply the R-2 raw psql read-back.** With watchlists actually saved by an operator, run inline on target:
> `psql -h localhost -U axiom -d axiom -c "SELECT preference_id, operator_id, workspace_key, layout_config FROM operator_workspace_preferences WHERE workspace_key='professional-market-workspace-v1' ORDER BY updated_at DESC LIMIT 3;"`
> — showing the persisted `layout_config.watchlists` contains **symbol/timeframe ids only** and **NO** forbidden fields (quantity/position/order/side/broker/account/margin/capital/stop/target/pnl/gate). Include `alembic current` = `20260717_0037` and (if any column alleged) `information_schema.columns` unchanged. **API/in-process read-back does not substitute.**

> **CA-P02(UI003)-2 — Resubmit the CORRECT `DELIVERY_REPORT_UI-003-P02.md`** (not the P01 report) + a browser screenshot of the **watchlist UI** (add/remove symbol, keyboard-operable, restored after re-login).

No constitutional violation is alleged — the failure is **evidence-completeness on the mandatory persistence gate + wrong delivery report.** The five named tests, regression, and CI already passed and need not be re-run (a fresh transcript is welcome). On the raw psql read-back showing symbol-ids-only, ITRGA expects to resolve to **Approved / Approved-with-Observations**.

**No progression.** Last-good baseline (= UI-003-P01 approval): v0.62.0 · head `20260717_0037` · backend 414 · frontend **33f·137t** (this P02 attempt's suite passed; only the raw-DB persistence proof + correct report are missing). Residuals unchanged: TD-W7-U07-RATE-GUARD, TD-W6-CI-AUDIT, UI-002-P04b.

*We don't guess. We prove.*
