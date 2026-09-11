# ITRGA REVIEW — UI-003-P01
## Professional Market Workspace Frame · Data-Source Inventory · Non-Authoritative Market Presentation

**Authority:** Institutional Technical Review & Governance Authority (ITRGA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-003 · **Phase:** P01
**Build Order:** `BUILD_ORDER_UI-003-P01.md`
**Evidence pack:** `DELIVERY_REPORT_UI-003-P01.md`, `operator results.md` (correct UI-003-P01 target transcript, 1991 lines), 2 served-session screenshots.
**Determination:** ✅ **APPROVED** (CI env-flake waived by operator)
**Authorizes:** `BUILD_ORDER_UI-003-P02` (Watchlists via existing preferences; binds R-1 + R-2 raw-psql read-back).
**Motto:** *We don't guess. We prove.*

---

## 0. Build-identity — PASS
Correct P01 pack: **67** `UI-003-P01` refs, **34** named-test hits. Not stale/wrong-pack. DA does not self-approve. Operator disclosed the network dropped mid-final-command (assessed §2, CI).

## 1. Verification matrix (Level-I, line-by-line) — substantively CLEAN
| # | Requirement | Evidence (line) | Verdict |
|---|---|---|---|
| (b) Five named tests displayed passing | verbose reporter | mounts_inside_single_ui001_shell (L92) · uses_existing_chart_and_market_sources_only (L93) · **labels_synthetic_and_simulated_non_authoritative** (L94) · **contains_no_execution_or_actuation_controls** (L95) · has_accessible_chart_summary_and_controls (L96) | **PASS** |
| **(c) 🔴 No new analysis (domain brightest line)** | existing hooks only, no compute/infer | market source uses `useChartData`/`fetchCandles`/`useLiveMarket` (L112–126); grep `inferSignal\|runInference\|authoritativeRecompute\|emitSignal\|/api/v1/orders\|/api/v1/search` → **no output** (L280–281) | **PASS** |
| **(e) Provenance labels (market-data posture)** | seed:synthetic/live:simulated non-authoritative | `test_..._labels_synthetic_and_simulated_data_non_authoritative` ✓ (L94, isolated re-run L316); source renders `seed:synthetic`/`live:simulated`/`non-authoritative`/"authoritative live venue" negation (L282) | **PASS** |
| (d) No-actuation source grep | clean | market-workspace source scan → clean (no execution/order/broker/account/gate) | **PASS** |
| (f) Extend-not-duplicate / single shell | mounts in UI-001 shell | `test_..._mounts_inside_single_ui001_shell` ✓ (L92); no second nav/palette/overlay | **PASS** |
| **(g) No-drift substitute + no new dep** | head + manifests | `alembic current` = **`20260717_0037 (head)`** (L633); charting-lib grep → **only existing `lightweight-charts@^4.2.0`** (no fuse/chart.js/echarts/highcharts) (L634–637); `/api/v1/search\|/api/v1/orders\|new_table\|watchlists` grep confirms **no new endpoint/table/watchlist persistence** (deferred to P02) | **PASS** |
| (h) Regression + growth | backend ≥414, frontend grown | frontend **32 files / 132 tests passed** (L844–845, up from 31f/127t = +5 P01 tests); backend **414 passed** (L1358, L1978) | **PASS** |
| (i) Browser (served) — R-6 | frame + provenance in-shell | shots: **Professional Market Workspace** mounted in Region C inside the shell (Active Market/Timeframe/Chart Type/Bars/Simulated Feed/Connection/Source Inventory panels); **"Non-authoritative data posture: seed:synthetic is chart context only, live:simulated is a governed simulated stream… never labels simulated data as authoritative live venue data"** banner; candlestick chart with inert RESEARCH NOTE / RESEARCH ZONE annotations (research_only, sourced W5-U03 evidence); "Research markup only… not a signal, not an order" disclaimer; Gate CLOSED/RESEARCH-ONLY framing; UI-002 breadcrumb `AXIOM › Observe › Chart Workspace` | **PASS** |
| Constitutional line | Gate CLOSED, no execution, no new analysis/live-real data | grep clean; provenance preserved; existing data only | **PASS** |
| (j) Local CI | exit 0 or waived | `LOCAL_CI_EXIT_CODE: 1` — offline `npm audit` (`read ECONNRESET`) AFTER **backend 414 + frontend 132 green**; network dropped mid-command per operator = **TD-W6-CI-AUDIT** env-flake | **WAIVED by operator** |

## 2. CI disposition (network-drop-induced env-flake)
The CI ran substantive gates green — backend **414**, frontend **32f/132t** — then died at the offline npm-audit step with `read ECONNRESET`, yielding `LOCAL_CI_EXIT_CODE: 1` and no completion sentinel (consistent: the run ended at audit). Operator disclosed the network disconnected during this command. This is the recurring **TD-W6-CI-AUDIT** class (offline audit endpoint) surfacing *after* all substantive gates passed. **Operator waived** (consistent with all prior instances). Fix remains: networked rerun / graceful-audit; **never `strict-ssl false`**.

## 3. Determination & rationale
**APPROVED (clean; CI env-flake waived).** UI-003-P01 is a substantively clean pass and — decisively for the first *domain* workstream — the two pre-registered brightest lines held: the market workspace is **presentation over existing governed data with NO new analysis** (only existing `useChartData`/`fetchCandles`/`useLiveMarket` hooks; no inference/recompute/signal-gen grep hits), and **market-data provenance is preserved and visibly non-authoritative** (`seed:synthetic`/`live:simulated`, "never labels simulated data as authoritative live venue data"). No execution/actuation, single UI-001 shell mount (no duplication), no new dependency (only existing `lightweight-charts`), no new endpoint/table (watchlist persistence correctly deferred to P02), head `20260717_0037`, and regression grew cleanly (backend 414, frontend 32f/132t). The sole non-green item is the offline-audit CI exit-1 — a network-drop-induced TD-W6-CI-AUDIT env-flake occurring after all substantive gates green — **waived by operator**.

Per the UI-Transformation vocabulary, **Approved authorizes progression.** → **`BUILD_ORDER_UI-003-P02` (Watchlists via existing preferences) is authorized**, binding **R-1** (watchlists via `operator_workspace_preferences`, symbol/timeframe ids only, no new table) and **R-2** (one inline raw psql read-back on `WHERE workspace_key='professional-market-workspace-v1'` proving symbol/timeframe ids only, no forbidden fields), carrying R-4/R-6.

Baseline of record: v0.62.0 · head `20260717_0037` · backend **414** · frontend **32f·132t**. Residuals unchanged & non-blocking: TD-W7-U07-RATE-GUARD, TD-W6-CI-AUDIT, UI-002-P04b (outstanding).

*We don't guess. We prove.*
