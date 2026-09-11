# AXIOM ITRGA — REVIEW: W0-U07 (Live Chart Visualization Foundation)

**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Build Order:** `BUILD_ORDER_W0-U07.md` · **Delivery Report:** `DELIVERY_REPORT_W0-U07.md` (v0.7.0)
**Evidence:** Delivery report + **one browser screenshot** (`/chart` BTCUSD·M1, bars=226, FEED RUNNING).
Operator test evidence for U07 **not yet supplied** (report cites 55 backend / 16 frontend as DA-run).
**Date:** 2026-07-11 · **Standard:** `UNIVERSAL_ITRGA_REVIEWER_DIRECTIVE.md`; every claim a hypothesis.

---

## VERDICT: **PASS WITH OBSERVATIONS — CONDITIONAL (approval withheld pending completion of the §6 evidence set).**

This is a well-executed unit. The screenshot confirms a real TradingView-Lightweight-Charts candlestick
workspace rendering BTCUSD·M1 with symbol/timeframe/type controls, a live feed running, and an ▲Up/▼Down
legend (color paired with arrows — the accessibility intent is visible). Governance posture is clean:
presentation-only, no analytics/AI/execution, auth-gated, canonical v2.0 docs cited (F-4 corrected), and
the fabricated-percentage confidence habit dropped as instructed. **It is close to approval.** It is not
approved yet because the Build Order set a specific Level-I evidence bar for UI units and the supplied
evidence is **partial** — plus one additive-scope item to adjudicate and two minor findings.

---

## 1. WHAT IS PROVEN (credited)

- **Chart renders (Level-I):** the screenshot shows Lightweight Charts (TV logo), **BTCUSD·M1**,
  candlestick series, `bars=226`, `FEED RUNNING`, `last live 2026-07-11T20:22:38Z`, symbol dropdown
  (EURUSD/BTCUSD), timeframe M1, chart-type toggles, and Start/Stop/Seed/Reload controls. The core
  deliverable exists and works in a browser.
- **Accessibility intent:** ▲Up/▼Down legend pairs direction with shape+label, not color alone — matches
  the Build Order §3 requirement (confirm keyboard/focus/ARIA at code level).
- **Governance envelope respected (documentary + visual):** no indicators, no AI overlays, no order/exec
  UI; chart is render-only per Architecture §30; canonical v2.0 + hierarchy cited; confidence stated as
  HIGH/MODERATE/LIMITED (OBS-6 corrected). Good.
- **Design decisions recorded:** ADR-013 (engine), ADR-014 (live merge: forming-candle update + append).

## 2. FINDINGS

### F-1 (MEDIUM — evidence incomplete vs. Build Order §6.2) — the reason approval is withheld
The Build Order set a **mandatory** Level-I evidence set for this UI unit. Supplied vs. required:
| Required (BO §6.2) | Supplied | Status |
|---|---|---|
| Historical candles rendered | Yes (bars=226) | ✅ |
| Live updating — **≥2 frames at different timestamps** | **One** frame only | ⚠️ PARTIAL |
| Symbol/timeframe switch **reflected on the chart** | Dropdown shown open; only BTCUSD rendered | ⚠️ PARTIAL (no EURUSD render frame) |
| **Logged-out chart route blocked/redirected** | Not shown (screenshot is authenticated) | ❌ MISSING |
| Operator-run `pytest`/`vitest`/`tsc` console (raw) | Not supplied for U07 (DA-reported 55/16 only) | ❌ MISSING |
U06 set the precedent: multi-frame live proof + operator console. One authenticated frame proves *render*,
not *live update over time*, *cross-symbol render*, or the *auth gate*. Per the directive, a UI unit is
judged in the browser with the specified evidence — so this is **NOT VERIFIABLE** on those sub-claims yet.

### F-2 (LOW — additive scope) — Seed-history / Reload-history capability not in the Build Order
The unit adds a **Seed-history API (synthetic candles)** + Reload + an ascending candle-history endpoint.
The Build Order scoped rendering from *existing* persistence; seed-history is **additive**. It is defensible
(sparse simulated series need seeding to show a chart) and the report says it is *synthetic and labelled*
— which is the right safeguard. But: (a) additive scope must be flagged, not silently absorbed; and
(b) **synthetic data must be unmistakably non-authoritative** in the UI and DB (a `source`/label marker),
so it can never be mistaken for real market history in later ML/analytics units. Confirm the label is
persisted and visible. Accept as a reasonable in-spirit extension **with** that confirmation.

### F-3 (LOW — route-name inconsistency) — `/chart` vs `/charts`
Build Order §4 said route `/chart`; the report says `/charts` (§1) and "Chart Workspace" (§7). Trivial,
but the canonical path should be stated once and consistently (docs + PROJECT_STATE + tests). Confirm.

### F-4 (LOW / OBSERVATION — chart readability) — default viewport density
The screenshot shows **226 M1 bars packed edge-to-edge**; individual candles are visually indistinguishable
at the default zoom (a dense wall). Not necessarily a defect (Lightweight Charts auto-fit), but
`07_UI_UX_SPEC` demands clarity/readability. Confirm the default viewport shows a legible window (e.g., last
N bars) and that zoom/scroll works — capture a zoomed-in frame to demonstrate legible candles.

### Not-a-defect note (evidence timing)
The report states screenshots are "operator-mandatory; sandbox cannot supply" and then the operator *did*
supply one. That's fine — the report predates the capture. It simply means the §6 set is **in progress**,
not refused. No finding; just reconciling.

## 3. ARCHITECTURE / SCOPE / SECURITY (v2.0)

- **Conformant (provisional):** UX/Presentation + Chart State (§30) render-only; consumes existing Market
  Intelligence/persistence + the authenticated WS from U05/U06; no new broker feed. No circular/omni
  coupling evident from the report. Source excerpts would let me certify §30 "no calc in chart layer" at
  code level (currently Supported Inference, Level III).
- **Scope:** respected except the additive seed-history (F-2), which is acceptable with labelling.
- **Security:** auth-gated route reuses W0-U04 guard; no new secrets. The Wave-0 security residuals (OBS-3
  dev creds / refresh rotation; OBS-5 WS token) remain carried — not U07's job, but still open.

## 4. REQUIRED CORRECTIONS (to convert to APPROVED)

- **C-1 (F-1):** Supply the full Build-Order §6 evidence: (a) **two live frames at different timestamps**
  showing candles updating (as U06 did for the table); (b) a frame showing **EURUSD** rendered after a
  symbol switch; (c) a **logged-out** attempt to reach `/chart(s)` showing block/redirect; (d) the
  **operator-run** `pytest`/`vitest`/`tsc` console with the `collected N` line (confirm the 55/16, no
  regression from 53/11 baseline).
- **C-2 (F-2):** Confirm synthetic seed-history is **persisted and displayed with a clear non-authoritative
  marker** (e.g., `source=seed/synthetic`) distinct from `live:simulated` and real ingested candles.
- **C-3 (F-3):** State the canonical chart route once; align report/docs/PROJECT_STATE/tests.

## 5. RECOMMENDATIONS (non-blocking)
- **R-1 (F-4):** Set a legible default viewport (recent-N bars) and include a zoomed-in screenshot.
- **R-2:** Provide the targeted **source excerpts** (chart component, `mergeLiveBar`, ChartState, route
  guard) so §30 render-only and the live-merge strategy are certified at Level I, not inferred.
- **R-3:** While capturing C-1(c), also grab the **logged-out `/live`** screenshot to close Wave-0 OBS-1.

## 6. DISPOSITION
**Do not yet mark U07 approved; do not issue W0-U08.** U07 is **PASS WITH OBSERVATIONS — CONDITIONAL**:
the engineering and governance are sound and one Level-I render frame is in hand, but the mandated
multi-frame + cross-symbol + logged-out + operator-console evidence (C-1) and the seed-labelling
confirmation (C-2) must be supplied. These are small; once provided and clean, I will issue **APPROVED**
promptly.

---

## EVIDENCE CONFIDENCE STATEMENT
- **Evidence Reviewed:** `DELIVERY_REPORT_W0-U07.md`; one `/chart` browser screenshot; cross-checked
  against `BUILD_ORDER_W0-U07.md`, canonical 05 v2.0 + hierarchy, and the Wave-0 verdicts.
- **Confidence Level:** **MODERATE.** The chart-render deliverable is proven at Level I; live-update-over-
  time, cross-symbol render, the auth gate, and the U07 test counts are **not yet** Level-I verified;
  source not inspected (§30 conformance is Supported Inference).
- **Remaining Unknowns:** multi-frame live behavior; EURUSD render; logged-out gate; operator U07 test
  results; seed-data labelling in DB/UI; default-viewport legibility; code-level §30 conformance.
- **Additional Evidence Required:** C-1 (evidence set), C-2 (seed label), C-3 (route name); optionally
  R-2 source excerpts and R-1 zoomed frame.

---

*"One frame proves the chart draws. It does not prove it lives, switches symbols, or locks out the
unauthenticated. Send the two live frames, the EURUSD frame, the logged-out frame, and the test console —
then this is approved. We don't guess. We prove — in the browser."*
— AXIOM ITRGA
