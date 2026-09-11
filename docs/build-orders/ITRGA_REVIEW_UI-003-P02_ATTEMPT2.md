# ITRGA REVIEW — UI-003-P02 (attempt 2, on corrective evidence)
## Watchlists via Existing Preferences — R-2 raw-psql read-back

**Authority:** Institutional Technical Review & Governance Authority (ITRGA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-003 · **Phase:** P02
**Build Order:** `BUILD_ORDER_UI-003-P02.md` · **Supersedes:** attempt-1 review (wrong report + R-2 absent).
**Evidence:** `DELIVERY_REPORT_UI-003-P02.md` (correct), `operator results.md` (raw-psql read-back rerun, 69 lines), 1 watchlist-UI screenshot.
**Determination:** ⛔ **CORRECTIVE ACTIONS REQUIRED**
**Authorizes:** *nothing* — `BUILD_ORDER_UI-003-P03` not authorized.
**Motto:** *We don't guess. We prove.*

---

## 0. Build-identity — PASS (both attempt-1 pack issues fixed)
Correct P02 pack now: `DELIVERY_REPORT_UI-003-P02.md` self-declares Phase UI-003-P02; transcript 11 P02 refs / **0 P01**; watchlist-UI screenshot supplied (**CA-P02(UI003)-2 satisfied**). DA does not self-approve.

## 1. 🔴 R-2 read-back was SUPPLIED but returns `(0 rows)` — persistence DISPROVEN, not proven
CA-P02(UI003)-1 asked for the raw psql read-back. It is now present — and the DA even exceeded the ask (full-row SELECT + forbidden-field regex + count + no-orphan JOINs). **But the outputs show NO persisted watchlist row on target:**

```
SELECT preference_id, operator_id, workspace_key, layout_config
  FROM operator_workspace_preferences WHERE workspace_key='professional-market-workspace-v1' …   → (0 rows)
SELECT … layout_config->'watchlists' … forbidden_field_present …                                  → (0 rows)
SELECT COUNT(*) AS professional_market_watchlist_rows …                                           → 0
operator_orphan_count → 0   audit_orphan_count → 0   (trivially, no rows exist)
alembic current → 20260717_0037 (head)
```

**Root cause (from the transcript order):** the read-back queries were run **FIRST, with no preceding watchlist save** — the operator queried an empty table before (or without) persisting a watchlist through the UI. Therefore R-2's central requirement — *prove a real watchlist row persisted as symbol/timeframe ids only* — is **not demonstrated.** An empty read-back where a populated row was required is an **R7 non-result / R1 finding**, not a pass: the delivery report claims durable persistence via `operator_workspace_preferences`, but the raw DB shows the key is **empty**.

This is exactly the gap R-2 exists to expose: the watchlist **UI renders** (screenshot: Focus EURUSD/BTCUSD, timeframes M1/H1) and the **in-process tests pass**, yet **no durable row exists on target** — leaving open whether persistence is actually wired, debounced-and-unflushed, or simply not exercised before the query.

## 2. What is now in place (so the corrective is the last mile)
| Item | Status |
|---|---|
| Correct `DELIVERY_REPORT_UI-003-P02.md` | ✅ (fixes attempt-1 wrong-pack) |
| Watchlist-UI screenshot (add symbol / Focus / Remove / timeframes) | ✅ CA-P02(UI003)-2 |
| R-2 read-back **harness** (raw psql, forbidden-field check, count, no-orphan JOINs, alembic head) | ✅ correct method |
| `alembic current` = `20260717_0037` | ✅ |
| 5 P02 named tests + regression (backend 414 / frontend 33f·137t) + CI exit 0 | ✅ (attempt-1, unchanged) |
| **R-2 read-back RESULT — persisted watchlist row present** | ⛔ **(0 rows)** |

## 3. Determination & required corrective action
**CORRECTIVE ACTIONS REQUIRED.** Single, narrow corrective:

> **CA-P02(UI003)-3 — Persist a watchlist, THEN read it back.** As the signed-in operator, **save a watchlist via the UI** (add ≥1 symbol/timeframe so it writes to `operator_workspace_preferences`), **then** re-run the R-2 read-back so it returns **≥1 row** for `workspace_key='professional-market-workspace-v1'` with `layout_config->'watchlists'` populated by **symbol/timeframe ids only** and `forbidden_field_present = f` (false). Keep the count (≥1), the `operator_id → operators.id` no-orphan JOIN (`orphan_count 0`), and `alembic current` = `20260717_0037`. If the watchlist does **not** persist after a UI save, that is itself the finding to fix (wire the write to the existing preference API) before re-submitting.

No constitutional violation is alleged — symbol-ids-only + forbidden-field-rejection tests pass and no new table is claimed. The failure is that **P02's defining persistence claim is unproven** (read-back empty). On a populated symbol-ids-only read-back, ITRGA expects to resolve to **Approved**.

**No progression.** Last-good baseline (= UI-003-P01 approval): v0.62.0 · head `20260717_0037` · backend 414 · frontend **33f·137t**. Residuals unchanged: TD-W7-U07-RATE-GUARD, TD-W6-CI-AUDIT, UI-002-P04b.

*We don't guess. We prove.*
