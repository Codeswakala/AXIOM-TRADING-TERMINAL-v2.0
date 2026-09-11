# AXIOM BUILD ORDER — W0-U07

## Live Chart Visualization Foundation

**Build Order ID:** W0-U07
**Wave:** 0 — Foundation · **Unit:** 07
**Version:** 1.0 · **Status:** ISSUED
**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Date Issued:** 2026-07-11
**Authorized By:** ITRGA, following Wave-0 closure clearance and explicit Operator authorization (2026-07-11)

**Governing Documents (canonical — constitutional order per `10_CONSTITUTIONAL_HIERARCHY.md`):**
1. `00_VISION_AND_PRINCIPLES.md`
2. `03_AXIOM_SPEC.md`
3. `04_PROJECT_ROADMAP.md`
4. `05_SYSTEM_ARCHITECTURE.md` **(v2.0 — the single authoritative architecture; supersedes all prior/merged versions)**
5. `06_ML_SPEC.md`, `07_UI_UX_SPEC.md`
6. `UNIVERSAL_ITRGA_REVIEWER_DIRECTIVE.md`

> **Governing-baseline notice (F-4):** Prior Build Orders (U01–U06) cited the *old* baseline
> (`03_AXIOM_SPEC_v1.1`, `AXIOM_SYSTEM_ARCHITECTURE_MERGED v1.1`, old ML/UI numbering). **This and all
> future Build Orders cite the canonical set above.** The Delivery Report must reference the canonical
> documents, not the retired ones.

---

## 1. Purpose

This unit delivers AXIOM's first **professional charting capability**: an institutional-grade candlestick
chart that renders historical candles and updates in real time from the authenticated live market feed
already delivered in W0-U05/U06. This is the transition from a live *price table* to a live *chart* — the
analytical centrepiece of the platform per `07_UI_UX_SPEC` ("charts are the center of AXIOM") and
`05_SYSTEM_ARCHITECTURE` v2.0 (Chart State Service §30).

It must be executed to institutional standard and reviewed under `UNIVERSAL_ITRGA_REVIEWER_DIRECTIVE.md`
— **every claim in the Delivery Report is a hypothesis until proven with Level-I evidence.**

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No trading, order entry, positions, or execution UI** of any kind. Execution remains roadmap-gated
  behind the Constitutional Governance Gate (05 v2.0 §15/§44; roadmap Wave 6).
- ❌ **No ML/AI content on the chart** — no predictions, no probability zones, no AI annotations, no
  indicators. Those are Wave 3+/future (07_UI_UX "AI Chart Intelligence = future"). This unit is
  presentation-only.
- ❌ **No analytical computation in the chart layer.** Per 05 v2.0 §11.1 and §30, the UX/Presentation
  subsystem and Chart State Service handle **display/presentation state ONLY** — never analytical
  reasoning or authoritative calculations. Candle data comes from the Market Intelligence/persistence and
  live WS channels; the chart renders, it does not compute signals.
- ❌ **No new broker/external feed.** Continue using the existing simulated multi-symbol adapter + the
  authenticated `/ws/market` channel and persistence APIs.
- ✅ **Auth-gated:** the chart view is only accessible to authenticated operators (reuse the W0-U04 guard),
  consistent with the live dashboard.

---

## 3. Scope

### In scope
- **Charting engine integration:** TradingView **Lightweight Charts** (the primary engine named in
  `07_UI_UX_SPEC`) in the React frontend.
- **Historical render:** load and display historical candles for a selected symbol/timeframe from the
  existing persistence/market API (candles produced by U03 ingestion and/or U05 live persistence).
- **Live update:** the chart updates in real time from the authenticated live WS feed (U05/U06) — the
  forming/last candle updates and new candles append without a full re-fetch.
- **Symbol + timeframe selection:** operator can switch between the available symbols (EURUSD, BTCUSD) and
  at least the live timeframe (M1); timeframe list may be minimal but must be architected for extension.
- **Chart types (minimum):** candlestick; line/area acceptable as toggles. (Heikin-Ashi/Renko/etc. are
  explicitly future per 07_UI_UX.)
- **Presentation state via a Chart State concept** (05 v2.0 §30): symbol, timeframe, chart type, viewport
  — cleanly separated from data fetching and from any analytics.
- **Institutional dark theme + accessibility** per `07_UI_UX_SPEC`: color-not-sole-signal for up/down
  (also use labels/shape where a colorblind user must distinguish), keyboard-reachable controls, visible
  focus, ARIA labels on interactive controls.
- **Single-uvicorn workflow preserved** (build frontend → served by uvicorn), as in U04–U06.
- **Tests + ADRs + docs + Delivery Report.**

### Explicitly out of scope (do not build)
- Technical indicators (RSI/MACD/EMA/etc.), drawing tools, Fibonacci, multi-chart layouts, replay mode,
  saved workspaces/layout persistence, AI overlays/annotations, order/DOM/volume-profile — all reserved
  for later units.
- Real broker data; ML inference; any execution.

---

## 4. Deliverables

1. **Chart component + data layer**
   - Lightweight-Charts-based candlestick component (React/TS), typed data models.
   - Historical fetch from the existing candle/market API; **live append/update** from the authenticated
     WS feed (no full re-render per tick; update the forming candle, append on new bar).
   - A `ChartState` concept (symbol/timeframe/chart-type/viewport) separated from data + analytics.
2. **Chart workspace page/route** (auth-gated), replacing the current chart **placeholder** with a working
   chart; symbol + timeframe selectors; chart-type toggle; clear "no data / loading / disconnected" states.
3. **Performance:** smooth rendering at the `07_UI_UX` targets (aim 60 FPS render, <100ms interaction);
   heavy work stays server-side; the client renders.
4. **Accessibility:** per §3 (color-not-sole-signal, keyboard nav, focus, ARIA).
5. **Tests:** frontend component/integration tests for historical render, live update on simulated WS
   messages, symbol/timeframe switch, and disconnected/empty states; backend tests only if a new/changed
   candle-history endpoint is introduced (prefer reusing existing APIs).
6. **EKMS:** ADR-013 (charting engine choice + alternatives/consequences), ADR-014 (live chart update
   strategy: forming-candle update vs. append, and how it reuses the U05/U06 WS contract).
7. **Docs:** `docs/frontend/CHART_WORKSPACE.md`; updated `PROJECT_STATE.md`; single-uvicorn repro steps.
8. **Delivery Report** per §6.

---

## 5. Success Criteria (Definition of Done)

- [ ] Authenticated operator sees a **candlestick chart** for a selected symbol (historical candles render).
- [ ] Chart **updates live** from the simulated feed — forming candle updates and new candles append —
      visible without page refresh, for at least EURUSD and BTCUSD.
- [ ] Symbol and timeframe switching work and re-load the chart correctly.
- [ ] Chart type toggle (at least candlestick + one of line/area) works.
- [ ] Loading / empty / disconnected states are handled and clearly shown.
- [ ] Unauthenticated users cannot access the chart route (reuse W0-U04 guard).
- [ ] No analytics/indicators/AI/execution present (scope respected).
- [ ] Accessibility: up/down not conveyed by color alone; controls keyboard-navigable with visible focus.
- [ ] Single-uvicorn workflow still runs the full stack after `npm run build`.
- [ ] Frontend tests pass (incl. a test that feeds simulated WS candle messages and asserts the series
      updates); existing 53 backend + 11 frontend remain green (no regression).
- [ ] ADR-013 + ADR-014 present with alternatives + consequences.
- [ ] Conforms to `05_SYSTEM_ARCHITECTURE.md` v2.0 (Chart State = presentation only; no calc in UI layer).

---

## 6. Delivery Report & Evidence Requirements (MANDATORY — set the evidence bar up front)

The Delivery Report must be written to `UNIVERSAL_ITRGA_REVIEWER_DIRECTIVE.md` standard and **include the
Level-I evidence this unit will be judged on.** Because this is a UI unit, **operator-run browser evidence
is mandatory for approval** (the W0-U06 lesson): report-claims alone will not be approved.

Provide:
1. **Operator-run test output** (raw console, with the `collected N` line): backend `pytest`, frontend
   `vitest`, `tsc --noEmit`. Show no regression from the 53/11 baseline plus the new chart tests.
2. **Browser screenshots (Level-I):**
   - Historical candles rendered for a symbol.
   - The chart **updating live** — at least two frames at different timestamps showing new/updated candles
     (as the U06 evidence did for the table).
   - Symbol/timeframe switch reflected on the chart.
   - **A logged-out attempt to reach the chart route showing it is blocked/redirected** (this also closes
     Wave-0 residual OBS-1 for the analogous `/live` gate — capture the same for `/live` if convenient).
3. **Performance note:** a brief, honest statement on render smoothness (fps/interaction latency
   observed), even if qualitative.
4. Standard sections: hypothesis/counter-hypothesis, evidence classification (Levels I–IV),
   discipline-by-discipline, deviations, technical debt, ADR summaries, reproduction steps.

> **Confidence-reporting rule (OBS-6 correction):** Do **not** state review/confidence as a fabricated
> percentage. Use HIGH / MODERATE / LIMITED with a one-paragraph justification tied to evidence tiers.

---

## 7. Standards & Constraints

- Clean architecture, SRP, typed models, no secrets in code; structured logging if backend touched.
- Reuse existing services (auth guard, WS client `useLiveMarket`, persistence/market APIs) — do not
  duplicate. New broker/feed logic is prohibited.
- Cross-platform: the operator runs Windows/PowerShell; ensure the build + single-uvicorn flow works there.
- Record all technical debt with rationale + planned resolution.

---

## 8. Carried-Forward Wave-0 Residuals (track; not all are U07 work)

These do **not** block U07 but must remain visible in `PROJECT_STATE.md` / a technical-debt or risk
register and be scheduled:
- **OBS-1** — capture logged-out `/live` (and now `/chart`) auth-gate screenshot (fold into §6.2).
- **OBS-3 (security)** — replace dev bootstrap `admin/admin123`, enforce JWT secret (not warning-only),
  add refresh-token rotation — schedule a hardening unit before any shared/production exposure.
- **OBS-4** — confirm production disables `AUTO_CREATE_SCHEMA` (Alembic-only).
- **OBS-5 / TD-022** — plan WS-JWT migration from query param to header/subprotocol.
- **OBS-7** — supply/author the Tier-6/Tier-7 governance instruments (reasoning frameworks; quality-gate,
  risk, technical-debt, amendment registers). Required before a governance-heavy unit.
- **F-4** — update U01–U06 governing-doc citations to the canonical v2.0 set (housekeeping).

---

## 9. Process

Development Authority implements → internal verification → documentation sync → Delivery Report with the
§6 evidence → **submit to ITRGA** → independent review → corrections if required → approval → next Build
Order. **The Development Authority does not self-approve and does not authorize the next unit.**

---

*ITRGA — We don't guess. We prove. This unit is judged in the browser, not on the page.*
