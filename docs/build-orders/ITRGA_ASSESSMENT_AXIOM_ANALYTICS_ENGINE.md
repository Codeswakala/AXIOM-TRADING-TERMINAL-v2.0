# ITRGA ASSESSMENT — AXIOM ANALYTICS ENGINE (11 ENGINES / ~70 INDICATORS)

**Question from Operator:** *"clarify if and when these other indicators can be applied."*
**Answer in one line:** roughly **half can be built now**, a quarter need **data the simulator does not produce**, and a handful are **constitutionally barred** — not by cost, by the safety boundaries.
**Method:** every classification below was checked against the current tree (12-element chain).

---

## 1. THE FOUR GATES

Any indicator must pass all four. This is the reusable test, not a per-item opinion.

| Gate | Question | Failure means |
|---|---|---|
| **G1 — Data** | Do the inputs exist? OHLCV only today. | Cannot build until the data exists |
| **G2 — History** | Enough bars at the target timeframe? | Must render `unavailable`, never a padded value |
| **G3 — Constitutional** | Does it imply execution, positions, or order flow? | **Barred** unless amended |
| **G4 — Provenance** | Can it be honestly labelled as derived from simulated data? | Must carry derived-value provenance |

### What the tree actually provides

- **OHLCV only.** `open · high · low · close · volume · open_time · source`. Confirmed against the candle model.
- **No bid/ask, no order book, no tick-level trade data.** The only `bid`/`ask` in the codebase is `external_integration/broker/models.py`, which is behind the closed gate and not a market-data source. A live test asserts the terminal contains no `"order book"`, `"depth ladder"` or `"bid size"` anywhere.
- **History is timeframe-limited.** From the six-day capture seed:

| | M1 | M5 | M15 | H1 | H4 | D1 |
|---|---|---|---|---|---|---|
| bars | 8,640 | 1,728 | 576 | 144 | 36 | 6 |
| SMA 50 | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| SMA 200 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |

**A 200-period average on D1 needs 200 days. We have six.** Any long-period indicator must return `unavailable` on the higher timeframes — the DATA-P02 discriminant already gives us the mechanism.

---

## 2. VERDICT BY ENGINE

### ✅ BUILDABLE NOW — OHLC-only, no new data (5 engines)

| Engine | Items | Note |
|---|---|---|
| **01 Trend** | EMA, SMA, HMA, Supertrend, Ichimoku | Supertrend/Ichimoku need ATR and 52-period lookback — G2 applies on H4/D1 |
| **02 Momentum** | RSI, MACD, Stochastic, CCI, ROC, ADX/DMI | All pure OHLC. The cleanest engine in the list |
| **03 Volatility** | Bollinger, ATR, Keltner, Donchian, Volatility Regime | Note: **Volatility Regime duplicates the existing `realized_volatility`** — reconcile, don't rebuild |
| **07 Levels** | Pivots, CPR, Fibonacci, Camarilla, Prev H/L, Session Levels | Session Levels compose directly with DATA-P02's session context |
| **09 Statistics** | Z-Score, Percentile, Regression, Correlation, Beta | Correlation/Beta are **honest here** — DATA-P01 built real cross-symbol correlation, so these measure something genuine |

**05 Market Structure** (Swing Points, HH/HL/LH/LL, BOS, CHoCH, MSS, FVG, Order Blocks) is **OHLC-derivable and buildable** — but see §3 on naming.

### ⚠️ BUILDABLE BUT THE OUTPUT WOULD BE MEANINGLESS — volume is fabricated noise

**04 Volume Engine** and **10 Regime Engine** partially.

`chart_seed_service.py:165` generates volume as:

```python
volume = Decimal(str(int(150000 + abs(rng.gauss(40000, 20000)))))
```

**Volume is drawn independently of the bar's own price movement.** It has no relationship to the step size, the direction, or the range. Real volume correlates with volatility and breakouts — that relationship is the entire informational content of every volume indicator.

So OBV, MFI, CMF, Relative Volume, VWAP and Volume Profile would all compute correctly and mean **nothing**. OBV on independent noise is a random walk. This is the `CA-DATA1-2` lesson one level up: *the arithmetic being right does not make the output informative.*

**Recommendation:** either **defer the volume engine** until the generator produces volume correlated to price action, or **build it only alongside that generator work**. Do not ship volume indicators over noise volume — an operator reading a VWAP would be reading an artifact of `gauss()`.

**Volatility Regime / Trending / Ranging / Breakout** are computable from OHLC and are fine; they only depend on volume if you choose to include it.

### ❌ CANNOT BUILD — data does not exist (2 engines)

| Engine | Blocker |
|---|---|
| **08 Order Flow** — Delta, CVD, Imbalance, Volume Delta | **Requires per-trade buy/sell side.** The simulator produces a single aggregate volume per bar with no side attribution. Delta is definitionally `buy_volume − sell_volume`; neither exists. **Not a cost question — the data is absent.** |
| **06 Liquidity** — Equal Highs/Lows, Liquidity Pools, Sweeps, Stop Runs | Equal Highs/Lows are OHLC-derivable. But **"Liquidity Pools", "Liquidity Sweeps" and "Stop Runs" describe resting order behaviour** — where stops sit and when they are triggered. That is order-book information the system does not have and is barred from having (§3). Inferring them from price alone and labelling them as liquidity events would manufacture a market microstructure claim. |

### 🔴 CONSTITUTIONAL REVIEW REQUIRED — 11 Confluence Engine

**Bullish Evidence · Bearish Evidence · Setup Quality · Risk/Reward · Confidence · Trade Eligibility**

The constitutional boundary is **no automated execution**, and the terminal is labelled `RESEARCH-ONLY · NON-ACTUATING` throughout. A live test enforces a forbidden-term list including `buy`, `sell`, `execute`, `position`, `order_ticket`.

**"Trade Eligibility" is the problem term.** An engine that scores a setup and then emits an eligibility verdict is a trade recommendation in all but name. Add "Risk/Reward" — which requires an implied entry, stop and target — and the surface is producing actionable trade parameters. The existing Advisory Signals panel is the precedent for how far this system goes: it emits a **calibrated probability with an uncertainty interval and an explicit `NON-ACTUATING` label**, and it deliberately stops short of saying *take this trade*.

**This is not mine to decide.** Per standing instruction I declare it unresolved and refer it to you:

- **Confluence as evidence aggregation** — counting how many indicators align, displayed as a score with uncertainty — is **consistent** with the advisory-signal precedent and buildable.
- **"Trade Eligibility" as a go/no-go verdict** — I assess as **crossing the non-actuating line** and requiring a formal amendment before any build.

If you want it, the safe framing is: rename to evidence confluence, express as a score with an uncertainty band, and keep the `NON-ACTUATING` disclosure. **I will not build a trade-eligibility verdict under the current constitution without your explicit amendment.**

---

## 3. NAMING CAUTION — 05 MARKET STRUCTURE

BOS, CHoCH, MSS, FVG and Order Blocks are **computable from OHLC** and I raise no data objection.

But these are Smart-Money-Concepts terms that assert *institutional order placement*. "Order Block" claims a zone where institutions accumulated. On a **synthetic feed produced by `gauss()`**, that claim is false — there are no institutions and no orders. The pattern-detection arithmetic is real; the market-microstructure interpretation is not.

**Recommended:** build them as **geometric pattern detections** with honest naming and provenance (`derived from seed:synthetic OHLC`), not as institutional-behaviour claims. This is precisely the DATA-P01 discipline — the values are simulator outputs, not market observations.

---

## 4. SEQUENCING — THE "WHEN"

| Phase | Content | Rationale |
|---|---|---|
| **CHART-P01** *(authorized now)* | Fix `F-CHART-1`; SMA/EMA real; RSI, MACD, Bollinger, ATR | Establishes the server-side indicator architecture end to end |
| **CHART-P02** | Remainder of Trend + Momentum + Volatility; Levels (07); Statistics (09) | Pure extension once the architecture exists — mostly formulae |
| **CHART-P03** | Market Structure (05) with honest naming; drawing tools | Stateful, persistence-touching; deserves its own phase |
| **DATA-P03** *(prerequisite)* | Volume correlated to price action; **`OBS-DATA2-1`** drift | Unblocks the volume engine |
| **CHART-P04** | Volume engine (04) — **only after DATA-P03** | Otherwise indicators over noise |
| **Blocked** | Order Flow (08); liquidity-pool subset of (06) | Data does not exist and is constitutionally barred |
| **Operator decision** | Confluence (11) | Requires ruling or amendment |

**Roughly 45 of ~70 items are buildable on current data.** The architecture CHART-P01 establishes — server-side computation, typed provenance, `unavailable` when history is short — is what makes the rest incremental.

---

## 5. THE ARCHITECTURAL POINT

The single most valuable thing CHART-P01 delivers is **not three indicators — it is the pattern**. Every indicator afterwards is then a formula plus a registry entry, rather than a new argument about where computation lives and how insufficiency is disclosed.

That is why I recommended fix + small set over the full list: **get the contract right on four indicators, then scale it to seventy.**

---

Gate **CLOSED**. Production **NOT CERTIFIED**.
This assessment authorizes nothing beyond `BUILD_ORDER_CHART-P01.md`.

**We don't guess. We prove.**
