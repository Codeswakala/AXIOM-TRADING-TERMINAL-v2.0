# AXIOM — CAPABILITIES & VERIFIED BEHAVIOUR

**Status:** Programme CLOSED (all authorized phases approved by ITRGA, 2026-08-18).
**Nature of this terminal:** a **research terminal over a SIMULATED feed**. It does not connect
to any real market, broker or data source — that is by design and constitutionally required.
**Production is NOT CERTIFIED. The gate is CLOSED** (no automated execution, no external LLMs,
no dynamic plugins, no live trading).

Everything listed below was independently verified: by ITRGA's pristine-clone reviews (17
hash-reconciled deliveries), by 1,336 automated tests, and by the DA's full-browser
verification on 2026-08-19 (every page of the running app captured with **zero page errors**).

---

## 1. What it does when you launch it

### 1.1 Identity, login and role-based access
- **Login page** — dimensional split-screen sign-in, Operator-supplied compass/epsilon brand
  logo, pre-authentication governance chips (GATE: CLOSED · RESEARCH-ONLY · NON-ACTUATING),
  password reveal toggle, zero credential hints.
- **Three roles**: `admin`, `operator`, `unprivileged` — enforced on all **16 workspace routes**
  through `protectedWorkspace()` metadata.
- **Chunk-level RBAC**: an unauthorized role gets an explicit ACCESS DENIED page — *"This is an
  access restriction, not an empty result"* — and the route's code chunk is **never fetched**
  (proven by network trace, not just asserted).

### 1.2 The terminal workspace (the home surface)
- **Watchlist** — 11 instruments (8 FX + 3 crypto), live simulated quotes with:
  - provenance chips on every price (`LIVE:SIMULATED` / `SEED:SYNTHETIC` — never an unqualified "LIVE")
  - per-symbol sparklines rendered from the same seeded candle series the chart uses
  - honest absence: `--` when the feed has no quote for a symbol, never a fabricated value
  - search + FX/CRYPTO filter; row selection drives the chart
- **Candlestick chart** — lightweight-charts, 4 chart types, SMA/EMA/overlay rendering,
  bar-provenance breakdown (live vs seed counts).
- **Six timeframes with REAL server-side aggregation** (1m/5m/15m/1h/4h/1d):
  - each bar is a wall-clock-aligned bucket (open=first, high=max, low=min, close=last, volume=sum)
  - a typed state on every series: `native` / `aggregated` / `unavailable`
  - partial buckets are **excluded and disclosed**, never padded
  - the honesty notice only appears when aggregation genuinely happened
- **Session context strip** — Tokyo / London / New York on fixed UTC windows with overlap
  periods, weekend closure, and a hover readout for the bar under the crosshair.
- **Live feed control** — Start/Stop the simulated multi-instrument feed (11 symbols, M1).

### 1.3 Technical indicators — 29, computed server-side
Six engines, each indicator declared in a single registry (formula + required history + pane):

| Engine | Indicators |
|---|---|
| Trend | SMA 20, SMA 50, EMA 20, HMA 20, Supertrend, Ichimoku |
| Momentum | RSI 14, MACD, Stochastic, CCI 20, ROC 12, ADX/DMI |
| Volatility | Bollinger, ATR 14, Keltner, Donchian |
| Levels | Pivots, Camarilla, Prev H/L, Session Levels |
| Statistics | Z-Score, Percentile, Linear Regression Channel |
| Market Structure | Swings, HH/HL/LH/LL, BOS, CHoCH, FVG, Order Blocks (pattern) |

Guarantees (all tested):
- **insufficient history is typed, never padded** — "50 required, 5 available — no series rendered"
- **derived-value provenance** — an indicator never looks more authoritative than the bars beneath it
- **determinism** — same bars, same values, any order, repeat calls
- **grouped toolbar** — the three most-used stay one click away; all 29 reachable without scrolling
- **pane budget** — max 3 separate panes, explicit refusal, the price pane never shrinks below 280px
- **time-axis sync** — panes track the price pane after zoom/pan
- Market Structure is labelled **geometric pattern detection over simulated OHLC — not evidence of
  institutional activity or order placement** — the naming rule is visible in the product.

### 1.4 Evidence confluence (NON-ACTUATING)
Counts how many of the operator's **active** indicators point the same direction, shown as a
score with a **Wilson 95% uncertainty band**, exclusions stated, and the label
`NON-ACTUATING — evidence aggregation only`, plus the statement that it aggregates active
indicators over **simulated data**. No eligibility, no risk/reward, no trade verdict — the
surface counts evidence and refuses conclusions (constitutionally barred, deliberately unbuilt).

### 1.5 Drawing tools — 6, anchored to real data
Trendline · Horizontal Line · Ray · Rectangle · Fibonacci Retracement · Text Note.
- every drawing persists **(price, time)** per handle — never pixels, never percentages
- rendered at draw-time from those anchors, so drawings survive zoom, pan and timeframe
  changes (proven byte-identical across a 1m → 1h → 1m round-trip)
- scoped per (symbol, timeframe) — a 1m drawing never leaks onto 1h
- persisted through the **audited** annotation contract (create/reposition/delete all audited)
- legacy pre-anchoring notes are listed as UNANCHORED — never given an invented position

### 1.6 Research annotations on the chart
Notes saved from the chart render **on the chart at their (price, time) anchors** — the
`+ Note (N)` count matches what is visible; legacy percentage-based notes are handled
honestly in a labelled list below the chart.

### 1.7 The docks, panels, overlays and stage views
- **Right dock**: SIGNALS (advisory signals with calibrated confidence, uncertainty,
  NON-ACTUATING labels, state filters) · TELEMETRY (spread/status telemetry) ·
  INTELLIGENCE (model calibration & validation metrics) · ALERTS (severity-styled list,
  unread badge that shows nothing rather than a false zero, read-state-only acknowledge
  with an audit row).
- **Bottom dock**: TRADE PLANS · JOURNAL · RISK (risk & drawdown) · SCENARIOS · PORTFOLIO.
- **Overlays**: workspace settings; governance overlay (audit explorer, certification status,
  evidence workspace, platform records with per-source states — loading/error/ready/denied).
- **Stage views**: Chart stage · Research Hub (Unified Research Artifact Explorer with the
  governed data-source inventory and catalog) · Execution Research (simulated runs, ledger,
  risk reports, experiments, analytics — read-only research surfaces).
- **Deep links**: every legacy route redirects correctly (`/charts`, `/chart`, `/signals`,
  `/analytics`, `/investigate`, `/compare-scenarios`, `/execution-research`,
  `/portfolio-research`, `/research-management`, `/governance`, `/workspace`), plus the
  `?view=` / `?dock=` / `?panel=` / `?open=` parameters.

### 1.8 The data-honesty contract (the programme's whole point)
- provenance vocabulary is **exactly two values** — `seed:synthetic` · `live:simulated` —
  across eight phases it never grew, and no derived value ever wears a more authoritative label
  than its source
- unknown symbols raise instead of falling back to a fabricated `1.00000` price
- empty states are real (`--`, absence text) — never improvised series
- the simulated walks are zero-mean (no fake multi-day trends) and deterministic per symbol
- simulated data is never presentable as market data

### 1.9 Performance & engineering posture
- initial bundle **626.74 kB** (down from 748 kB) with route-level code splitting (6 lazy chunks)
- **1,336 tests** — 476 backend (pytest) + 860 frontend (vitest) — plus tsc with 0 errors
- every phase's patch chain applies clean onto the baseline commit in order; the artifact of
  record is the verified patch, not a commit

---

## 2. What it CANNOT do (by design — not brokenness)

- **No real market data.** The feed is a simulator. Prices, candles, indicators and drawings
  all derive from labelled synthetic data. Nothing connects to a broker, exchange or data vendor.
- **No execution.** No buy/sell, no orders, no positions, no broker connection, no account
  balances. The actuation vocabulary is banned at the source-code and rendered-surface level.
- **No trade recommendations.** No "Trade Eligibility", no Risk/Reward, no setup-quality
  verdicts, no entry/stop/target output. Indicators display; they do not advise. Confluence
  counts; it does not conclude.
- **No external LLMs, no dynamic plugins, no order-book/depth information** (constitutionally barred).
- **No volume indicators** — the simulator's volume is noise uncorrelated to price, so VWAP/OBV
  etc. were deliberately not shipped (they would be arithmetically correct and informationally empty).
- **Not production-certified.** The programme reviewed a UI transformation against Build Orders;
  it was not a security audit, performance qualification or release-readiness assessment.

If you ever see the terminal behave in a way that *implies* any of the above, that is a defect —
please report it.

---

## 3. How to verify it works (10-minute checklist)

1. `npm run dev` / backend up → **http://localhost:5173**
2. Log in: `admin` / `AxiomSecurePass2026!`
3. Watchlist shows 11 rows with prices + provenance chips (press Start Feed if empty)
4. Click `1H`, `1D`, `1M` — notices change and the bars genuinely differ per timeframe
5. Click `SMA 20` + Momentum menu → `RSI 14` — line appears, pane appears, confluence strip appears
6. Draw a trendline, switch `1M → 1H → 1M` — the drawing returns to the same bars
7. MarketStructure menu → `Swings` — markers + the "not evidence of institutional activity" line
8. Log in as `surf-p03-unprivileged-028efc57` / `operator-pass-123` → `/intelligence` shows ACCESS DENIED
9. Full test suites: `pytest -q` (476) · `npm test` (860) · `tsc -b` (0 errors)

The DA performed exactly this verification on 2026-08-19 (plus a 30-page crawl): **zero page
errors across every surface**. The terminal works as intended — its intention is simply
narrower than a trading platform: it is a research terminal that shows simulated data with
total honesty about where every value came from.

---

Gate **CLOSED** · Production **NOT CERTIFIED** · Programme **CLOSED**.

**We don't guess. We prove.**
