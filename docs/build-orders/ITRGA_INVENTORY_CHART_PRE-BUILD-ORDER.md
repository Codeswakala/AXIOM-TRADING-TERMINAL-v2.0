# ITRGA RE-INVENTORY — CHART PHASE SCOPE (PRE-BUILD-ORDER)

**Purpose:** re-inventory the CHART scope against the current tree before a Build Order is issued.
**Method:** pristine clone + 12-element patch chain (through `data_p02`). Verified in tree, not read from the blueprint.
**Standing lesson applied:** blueprint scope lists written before intervening phases must be re-inventoried before a Build Order is issued.

**Status: NO BUILD ORDER ISSUED. One finding requires an Operator scope decision first.**

---

## 1. HEADLINE

The chart stage is in better shape than the blueprint assumes — real `lightweight-charts` integration, working timeframes, honest provenance after DATA-P02. **But the three indicator controls on the toolbar do nothing.**

| Capability | State in tree | Verdict |
|---|---|---|
| Candlestick chart engine | `lightweight-charts`, real `createChart` | **BUILT** |
| Chart types (Candlestick/Bar/Line/Area) | Rendered, series switching works | **BUILT** |
| Timeframes + aggregation | DATA-P02, native/aggregated/unavailable | **BUILT** |
| Research annotations + markers | `ChartOverlayControls`, marker layers | **BUILT & routed** |
| **Indicators (SMA 20 / SMA 50 / EMA 20)** | **Toolbar pills that compute nothing** | 🔴 **`F-CHART-1`** |
| Drawing tools (trendline, fib, h-line) | Nothing exists | **PENDING — greenfield** |
| Additional indicators (RSI/MACD/etc.) | Nothing exists, no backend either | **PENDING — greenfield** |
| `ChartPlaceholderPage.tsx` | Referenced nowhere | 🟠 **`OBS-CHART-1`** orphan |

---

## 2. 🔴 `F-CHART-1` — THE INDICATOR TOGGLES ARE INERT

`TerminalChartStage.tsx:362–391` renders three buttons — `SMA 20`, `SMA 50`, `EMA 20`. Each toggles a boolean:

```tsx
onClick={() => setOverlays((prev) => ({ ...prev, sma20: !prev.sma20 }))}
```

I traced every use of `overlays` in the file. It appears at exactly four places: the `useState` declaration, and the three `className={... overlays.smaXX ? "active" : ""}` bindings.

**It is never passed to the chart.** The stage renders:

```tsx
<PriceChart bars={chartBars} chartType={chartType} symbol={selectedSymbol}
            height={480} onBarHover={setHoveredBar} />
```

No overlay prop. And `PriceChart.tsx:3` states its own contract: *"Renders series data; does not compute indicators or analytics."* It creates exactly one candlestick or line series — there is no second series for a moving average, and no SMA/EMA computation anywhere in the frontend or backend (`grep` for `sma|ema|moving_average|indicator` across `backend/app` returns only unrelated ML feature definitions).

**Clicking SMA 20 highlights the pill and changes nothing on the chart.**

### Why this is a finding and not a nice-to-have

Under the governing reframe — *every already-built capability must be surfaced in the best possible way* — this is the inverse case: **a control that advertises a capability the system does not have.** The button is styled `active`, which tells the operator the overlay is on. Nothing appears. The most likely reading is that the indicator is broken, or worse, that it is displayed and they cannot distinguish it.

This is adjacent to the `OBS-CONV2-1` class the DATA programme has been policing: the UI asserting something the data does not support. `F-DATA2-1` was a *timeframe* label applied to unaggregated data; this is an *indicator* control applied to a chart with no indicator. The tooltip says *"Presentation Only"*, which I read as an honest acknowledgement by an earlier phase that the control was cosmetic — but a tooltip is not a substitute for either building it or removing it.

**Three options for the Operator (§5).**

---

## 3. 🟠 `OBS-CHART-1` — ORPHANED PLACEHOLDER PAGE

`frontend/src/pages/ChartPlaceholderPage.tsx` reads *"Reserved for TradingView Lightweight Charts integration (Wave 1+)"* and *"TradingView Workspace — Not Initialized"*.

That integration **has since been built**. The file is referenced nowhere — not by the registry, not by any component, not by a test. It is dead code describing the absence of a feature that now exists.

Non-blocking. `OBS-CONV2-4` established the precedent of eliminating orphaned unrouted page files; this one survived. **Recommended** for removal in whichever phase touches the chart tree.

---

## 4. WHAT IS ALREADY BUILT — DO NOT REBUILD

- **Chart engine.** `PriceChart.tsx:67` `createChart`, `:131` `addCandlestickSeries`, `:140` `addLineSeries`. Real integration with dynamic CSS token resolution.
- **Timeframes and aggregation.** DATA-P02, closed this session. Do not touch.
- **Research annotation layer.** `ChartResearchMarkerLayer`, `ChartResearchMarkerList`, `ChartResearchAnnotationLayer`, `ChartOverlayControls` — all exported from `ChartWorkspaceSurface.tsx` and rendered at `:830`. Note `ChartOverlayControls` governs **annotation-marker visibility**, not indicators; the names are similar and should not be conflated in a Build Order.
- **Routing.** `/charts` and `/chart` redirect to `/?view=chart`. 16 routes intact.

---

## 5. DECISION REQUIRED BEFORE I ISSUE

**Q1 — `F-CHART-1` routing.** Three options:

- **(a) Build the indicators for real** — compute SMA/EMA and render them as overlay series. Makes the existing controls honest and is the natural CHART-phase work. *My recommendation*, provided we also decide where computation lives (§Q2).
- **(b) Remove the three controls** until indicators are built. Most conservative; applies *"a wrong price is worse than no price"* to controls. Removes the false affordance immediately.
- **(c) Disable and label them** explicitly as not-yet-available. Honest, but leaves dead chrome on the primary surface.

**Q2 — If (a): where does computation live?** DATA-P02 established that derived series are **server** work with a typed provenance discriminant, and that precedent is strong — an SMA is a derived value, and computing it client-side would re-open the divide DATA-P02 just closed. But indicators over an already-fetched window are cheap, and a round-trip per toggle is a real UX cost. **My recommendation: server-side**, consistent with DATA-P02, with the indicator series carrying explicit derived-value provenance.

**Q3 — Scope breadth.** The programme target is *"TradingView-class analysis depth"*. Options: **(i)** fix `F-CHART-1` only — SMA/EMA honest, nothing new; **(ii)** fix plus a small indicator set (RSI/MACD/Bollinger); **(iii)** fix plus indicators plus drawing tools (trendline/horizontal/fib). **My recommendation: (ii)** — drawing tools are a large, stateful, persistence-touching surface and deserve their own phase rather than being bolted onto an indicator fix.

---

## 6. WHAT I HAVE NOT DONE

No Build Order issued. No repository modification — the inventory tree is a scratch clone at `/tmp/d3` and will not persist. `F-CHART-1` is raised as a **finding**, not as authorization to fix it. I have not decided Q1–Q3; those are scope choices with real cost implications.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This inventory is **not** authorization for CHART or POLISH.

**We don't guess. We prove.**
