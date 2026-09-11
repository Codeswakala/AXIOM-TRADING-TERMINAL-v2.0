# AXIOM ITRGA — FINAL VERDICT: W0-U07 (Live Chart Visualization Foundation)

**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Prior verdict:** PASS WITH OBSERVATIONS — CONDITIONAL (approval withheld pending §6 evidence)
**New evidence:** operator test console (55 backend / 16 frontend / `tsc -b` clean) + 3 screenshots
(login page; BTCUSD·M1 live frame @42005.00; BTCUSD·M1 live frame @42007.76 w/ crosshair "12 Jul '26 04:05").
**Date:** 2026-07-11

---

## VERDICT: ✅ **APPROVED WITH OBSERVATIONS.**

The conditional evidence gap is now substantially closed with genuine Level-I evidence. The core
deliverable is proven in the browser, the operator-run test console is supplied and matches the report,
and the one residual with any real risk (the auth gate) is already tested at the API/WS layer and reuses a
previously-approved pattern. The remaining items are **verification-completeness, not defect-risk**, and
are carried as **mandatory closure items into the next evidence batch** rather than blocking approval.

---

## 1. HOW THE REQUIRED CORRECTIONS RESOLVED

| Required (prior C-1/C-2/C-3) | Status | Evidence |
|---|---|---|
| C-1(a) **≥2 live frames, different timestamps** | ✅ **CLOSED** | Two BTCUSD·M1 frames: last=42005.00 (green) vs 42007.76 + crosshair "12 Jul '26 04:05" — distinct price/viewport/time progression |
| C-1(d) **operator-run pytest/vitest/tsc console** | ✅ **CLOSED** | `55 passed` backend; frontend `8 files / 16 passed` incl. new `chart/types` (4) + `chart/useChartState` (1) + `useLiveMarket "embeds token query param"`; `tsc -b` clean. Matches the report's 55/16 — now operator-verified, no regression from 53/11. |
| C-1(c) **logged-out chart route blocked** | ⚠️ **PARTIAL** | Login page supplied; auth is tested at API/WS layer (`test_live_endpoints_require_auth`, `test_ws_market_requires_token`, token-embed test) and reuses the ProtectedRoute approved in U04/U06 — but the *visual redirect from `/chart` when logged out* is not directly shown. **Risk LOW; carry as OBS.** |
| C-1(b) **EURUSD rendered after symbol switch** | ⚠️ **OPEN** | Both chart frames are BTCUSD; symbol switching is unit-tested (`useChartState`) and the dropdown lists EURUSD, but no EURUSD *render* frame. **Risk LOW; carry as OBS.** |
| C-2 **seed-history synthetic label** | ⏳ **OPEN** | No new evidence that seed candles carry a persisted `source=seed/synthetic` marker distinct from `live:simulated`/real. **Governance-relevant for future ML units; carry.** |
| C-3 **route name `/chart` vs `/charts`** | ⏳ **OPEN** | Cosmetic; still unreconciled. Carry. |

**Why this is APPROVED, not held again:** the *core function* (chart renders + updates live) is now
Level-I proven, and the mandated operator test console is in hand. The four open items are LOW-severity
completeness/cosmetic/forward-governance items — none is a demonstrated defect. Holding the entire unit for
an EURUSD screenshot and a route-name edit would be disproportionate. This is the correct application of
the standard: approve the proven work, track the small residuals, and require their closure in the next
batch.

---

## 2. WHAT IS NOW PROVEN (Level-I)

- **Chart workspace renders and lives:** TradingView Lightweight Charts, BTCUSD·M1, candlestick series,
  live price line, two frames showing price+time progression (42005.00 → 42007.76; crosshair at 04:05).
- **Operator test suite green on target platform:** 55 backend + 16 frontend (8 files) + `tsc -b`, with
  the new chart tests present and WS token-auth tested. No regression.
- **Accessibility intent:** ▲Up/▼Down legend (color + shape + label).
- **Governance:** presentation-only, no analytics/AI/execution, auth-gated, canonical v2.0 + hierarchy
  cited (F-4 corrected), confidence stated qualitatively (OBS-6 corrected). ADR-013/014 recorded.

---

## 3. CARRIED-FORWARD OBSERVATIONS (must close in the next evidence batch)

- **U07-OBS-1 (C-1b):** capture one **EURUSD** chart frame after a symbol switch (proves cross-symbol render).
- **U07-OBS-2 (C-1c):** capture a **logged-out attempt at `/chart(s)`** showing block/redirect (also do the
  analogous `/live` frame to finally close Wave-0 OBS-1). *Auth is tested at data layer; this is the visual
  confirmation.*
- **U07-OBS-3 (C-2):** confirm seed/synthetic candles are **persisted + displayed with a clear
  non-authoritative marker** distinct from real/live data — this matters before any ML/analytics unit
  consumes candle history.
- **U07-OBS-4 (C-3):** reconcile the canonical chart route name across docs/PROJECT_STATE/tests.
- **U07-OBS-5 (F-4 readability):** the ~8-hour M1 viewport still renders as a dense wall; set a legible
  default window (recent-N bars) and demonstrate zoom/scroll — capture a zoomed-in frame.

These are tracked closure items; they do not reopen the approval, but **the next unit's evidence batch must
include OBS-1 and OBS-2** (they are simple screenshots) and the seed-label confirmation.

Plus the standing **Wave-0 residuals** remain open and scheduled: OBS-3 auth hardening (dev creds/refresh
rotation), OBS-4 dual schema path, OBS-5 WS-token migration, OBS-7 Tier-6/7 governance docs.

---

## 4. DISPOSITION & NEXT STEP

- **W0-U07: APPROVED WITH OBSERVATIONS (2026-07-11).** Platform v0.7.0.
- **Wave 0 status:** U01–U07 now approved. The foundation includes a working, live, auth-gated chart.
- **Next Build Order authorized to be issued** at the operator's direction. Per the roadmap, Wave 0 is
  essentially complete at the foundation level; the logical next step is either a final Wave-0
  consolidation/hardening unit (closing OBS-3/4/5/7 + the U07 observations) **or** the first **Wave 1 —
  Core Platform** unit. My recommendation: **a short Wave-0 hardening/closeout unit** to clear the security
  and governance-doc residuals before Wave 1 builds on them — but the choice is the operator's.

---

## EVIDENCE CONFIDENCE STATEMENT
- **Evidence Reviewed:** U07 delivery report; operator test console (55/16/tsc); 3 screenshots (login +
  two live BTCUSD frames); cross-checked vs `BUILD_ORDER_W0-U07.md`, canonical 05 v2.0 + hierarchy, and
  Wave-0 verdicts.
- **Confidence Level:** **MODERATE–HIGH.** Chart render + live update + operator tests are Level-I proven;
  EURUSD render and the visual logged-out gate are inferred (unit-tested + pattern-reuse) but not
  screenshotted; source not directly inspected (§30 render-only is Supported Inference).
- **Remaining Unknowns:** EURUSD render frame; visual logged-out redirect; seed-data labelling in DB/UI;
  canonical route name; default-viewport legibility; code-level §30 conformance.
- **Additional Evidence Required (next batch):** U07-OBS-1, OBS-2, OBS-3 (mandatory); OBS-4/OBS-5 (housekeeping).

---

*"Two live frames, a green tick, a crosshair at 04:05, and 71 passing tests with their names. The chart
draws and it lives — proven, not claimed. Approved, with the last few frames owed on the next pass. We
don't guess. We prove."*
— AXIOM ITRGA
