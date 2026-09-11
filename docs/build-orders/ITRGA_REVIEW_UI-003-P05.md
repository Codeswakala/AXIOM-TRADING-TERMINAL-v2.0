# ITRGA REVIEW — UI-003-P05 (FINAL — attempt 1)
## UI-003 Completion Checkpoint

**Authority:** Institutional Technical Review & Governance Authority (ITRGA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-003 · **Phase:** P05 (final)
**Build Order:** `BUILD_ORDER_UI-003-P05.md`
**Evidence pack:** `DELIVERY_REPORT_UI-003-P05.md`, `operator results.md` (1108 lines), **no browser screenshots attached**.
**Determination:** ⛔ **CORRECTIVE ACTIONS REQUIRED**
**Result:** UI-003 **NOT** declared complete.
**Motto:** *We don't guess. We prove.*

---

## 0. Build-identity — PASS
Correct P05 pack: `DELIVERY_REPORT_UI-003-P05.md` Phase UI-003-P05; transcript **47** P05 refs / **14** P04 refs. DA does not self-approve (report L244: "DA self-check is not self-approval").

## 1. What passed
| Check | Evidence (line) | Status |
|---|---|---|
| Five completion named tests displayed passing | chart_workspace_is_operational_center_without_scope_expansion (L111) · all_market_surfaces_are_presentation_only (L112) · **no_live_real_data_broker_execution_or_gate_path** (L113) · accessibility_responsive_and_registry_integration_hold (L114) · regression_preserves_backend_and_ui002_navigation (L115) | **PASS** |
| Whole-surface no-actuation grep | "Expected: no output above." (L171–172) | **PASS** |
| Backend regression | **414 passed** (L810) | **PASS** |
| Build | `tsc -b && vite build` → built (L1108) | **PASS** |
| No-drift / head | `20260717_0037` unchanged; no new dep | **PASS** |

## 2. 🔴 Three completion-gate FAILURES (completion is the strictest bar)
**F-1 — Frontend regression is BELOW baseline and contradicts the delivery report (R7).**
- The actual full `vitest run --reporter=verbose` (L827/837, complete run — duration confirmed L1093) reports **`33 files / 128 tests passed`** (L1089–1090).
- The Build Order requires **≥35 files / 146 tests** (last-good = UI-003-P04) with **no test lost** + P05's additions.
- The delivery report *claims* **36 files / 151 tests** (report L287) — but **no 35f/146t or 36f/151t appears anywhere in the operator transcript.** The transcript total (33f/128t) is **below the P04 baseline by 2 files / 18 tests.**
- Per R7, a transcript total that contradicts the report is credited to the **transcript**, which **fails** the regression gate. This may be a truncated capture (the same session hit the offline-audit failure) or a genuine coverage loss — either way it is **unproven / below baseline** and, at a completion checkpoint, blocking.

**F-2 — Item (d) watchlist raw psql reaffirmation ABSENT.** `grep -c psql` = 1, and that single hit is the Build-Order text quoted in the delivery report — **no executed `SELECT … WHERE workspace_key='professional-market-workspace-v1'`, no `(1 row)`.** The mandatory completion reaffirmation of watchlist persistence (raw psql, ≥1 clean row) was not run. (An API/in-process read-back does not substitute.)

**F-3 — Items (g)/(h) browser evidence ABSENT.** No screenshots attached; the completion checkpoint mandates route-by-route + responsive + keyboard browser evidence **and** the Doc 16 brand browser proof (B-1…B-7). The DA's own report concedes this: L244 "Browser evidence remains mandatory," L321 "Browser evidence required from operator," L394 "Doc 16 brand self-check PASS — **browser proof still required**." Per Doc 16 Part XIV, UI is judged in the browser; a completion declaration cannot rest on a self-check.

## 3. Determination & required corrective actions
**CORRECTIVE ACTIONS REQUIRED.** UI-003 is **not** declared complete. Three correctives:

> **CA-P05(UI003)-1 — Frontend regression at/above baseline, proven.** Resubmit the full `vitest run` transcript showing **≥35 files / ≥146 tests passed** (expected 36f/151t per the report) with **no test lost** and P05's 5 completion tests included. If the 33f/128t was a truncated capture, rerun to completion; if tests/files were genuinely removed, identify each and justify (no coverage loss on live routes).
> **CA-P05(UI003)-2 — Watchlist raw psql reaffirmation.** Run inline `psql -c "SELECT preference_id, operator_id, workspace_key, layout_config FROM operator_workspace_preferences WHERE workspace_key='professional-market-workspace-v1' ORDER BY updated_at DESC LIMIT 3;"` showing **≥1 row, `watchlists` = symbol/timeframe ids only, no forbidden fields** + `alembic current` = `20260717_0037`.
> **CA-P05(UI003)-3 — Browser evidence (R-6 + Doc 16 B-1…B-7).** Served-session screenshots: route-by-route market workspace in-shell (chart · overview/status · watchlist · overlays) · **responsive (narrow-width)** · keyboard walkthrough · provenance/`live:simulated` labels · Gate CLOSED/research framing · logged-out block; and brand proof (constitutional palette / typography+monospace / unified iconography / institutional-not-retail).

No constitutional violation is alleged — the five named tests (incl. no-live-data/broker/execution/gate) pass, backend 414 holds, no-actuation grep clean, head unchanged. The failures are **completion-evidence completeness**: an unreconciled below-baseline frontend total, the missing watchlist raw-psql reaffirmation, and the missing browser/brand proof. On a complete ≥35f/146t transcript + watchlist read-back + browser+brand evidence, ITRGA will run the constitutional + Doc 16 completion validations and — if clean — **declare 🏛️ UI-003 COMPLETE.**

**No completion declared. No progression to UI-004.** Last-good baseline (= UI-003-P04 approval): v0.62.0 · head `20260717_0037` · backend 414 · frontend **35f·146t**. Residuals unchanged: TD-W7-U07-RATE-GUARD, TD-W6-CI-AUDIT, UI-002-P04b.

*We don't guess. We prove.*
