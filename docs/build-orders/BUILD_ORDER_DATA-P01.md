# BUILD ORDER — DATA-P01

**Issuing authority:** Independent Technical Review & Governance Authority
**Authorized by:** Operator, 2026-08-17
**Programme:** DATA — Make it live · Phase 1 of 2
**Base:** `34f4c62` + item3 (`b7b4c4f7…`) + item5 (`4c03910c…`) + item6 (`f65da5c3…`) + item4 Rev B (`a516c2c1…`) + SURF-P01 (`62c4d021…`) + OBS-SURF1-2 (`69964afe…`) + SURF-P02 (`e039c74b…`) + SURF-P03 (`c18d5d05…`)
**Predecessor:** SURF programme — COMPLETE

---

## 1. OBJECTIVE

Blueprint §5, verbatim:

> **DATA-P01** Extend the simulated feed to all 11 instruments with correlated realistic walks; per-symbol seeding; watchlist sparklines from real series. *(Ten rows showing `--` is the single largest perceived-quality defect.)*

---

## 2. ⚠ THIS PHASE GENERATES DATA — THE CONSTITUTIONAL POSTURE CHANGES

CONV re-homed existing surfaces. SURF surfaced existing capability. **DATA-P01 produces values that did not previously exist and renders them as prices.**

Every prior phase could be judged on whether it faithfully presented what the backend returned. **This phase creates what the backend returns.** The governing risk inverts: not *"is a real value hidden?"* but *"could a manufactured value be mistaken for a market observation?"*

`OBS-CONV2-1` — invented calibration statistics presented as server-validated — survived five determinations. **That defect class is native to this phase.** The difference between acceptable and unacceptable here is provenance labelling, not data quality.

**The existing provenance vocabulary is `seed:synthetic`** and it is already load-bearing across the backend:

```
services/chart_seed_service.py:94              source="seed:synthetic"
trading_intelligence/live_market/adapter.py:110  if any_source[-1].source == "seed:synthetic"
trading_intelligence/inference/service.py:163    if inference_input.source == "seed:synthetic"
ml/dataset/service.py:293                        if source == "seed:synthetic"
```

**M1 — Every generated bar, tick and derived series must carry `source="seed:synthetic"`.** No new provenance value may be introduced. No generated value may be written with a null, empty, or absent source. The inference and dataset services branch on this string; a mislabelled bar would propagate into model inputs.

**M2 — The UI must label synthetic series wherever they render.** The terminal already displays `Provenance: SEED:SYNTHETIC (0 live · 80 seed)` and `LIVE:SIMULATED`. Sparklines and watchlist prices are new render sites and must be covered. **A price without visible provenance is the defect this phase most plausibly introduces.**

**M3 — Never present synthetic data as market data.** No label, tooltip, or heading may say "live", "market", "real-time" or "current" without the simulated qualifier. The existing `LIVE:SIMULATED` badge is the correct pattern — `LIVE` alone is not.

---

## 3. VERIFIED STARTING STATE

### 3.1 Eleven instruments, six base prices

`TerminalContext.tsx:13` — `SUPPORTED_INSTRUMENTS`:

```
EUR/USD  GBP/USD  USD/JPY  AUD/USD  USD/CAD  USD/CHF  NZD/USD  EUR/GBP
BTC/USD  ETH/USD  SOL/USD
```

`backend/app/market/live_service.py:152` — `_base_price()`:

```python
defaults = {"EURUSD": 1.10000, "GBPUSD": 1.27000, "USDJPY": 150.000,
            "BTCUSD": 42000.00, "ETHUSD": 2500.00, "XAUUSD": 2300.00}
return defaults.get(s, Decimal("1.00000"))
```

**Five of the eleven have no base price** — `AUD/USD`, `USD/CAD`, `USD/CHF`, `NZD/USD`, `EUR/GBP` — and fall through to `1.00000`. `SOL/USD` likewise. `XAUUSD` has a price but is not in the watchlist.

**A `USD/JPY`-style pair rendering at `1.00000` would be a plausible-looking wrong number** — worse than `--`. See M4.

### 3.2 The `--` is honest, not a bug

`TerminalWatchlistDock.tsx:127-166` renders `--` only when `quote.close` is absent:

```ts
const hasQuote = quote != null && quote.close != null && quote.close !== "";
let formattedPrice = "--";
if (closeNum !== null && !isNaN(closeNum)) { ... }
```

Change %, range and price each degrade independently. **This is correct absence rendering and must be preserved** — the fix is to supply real series, not to remove the `--` path.

Quotes populate from `useLiveMarket` via WebSocket and a `latest_by_symbol` snapshot. With the feed stopped, all eleven are legitimately absent.

### 3.3 A single RNG shared across all symbols

`chart_seed_service.py:34`:

```python
rng = random.Random(42)          # ← ONE generator
for symbol in symbols:           # ← consumed sequentially by every symbol
```

**There is no per-symbol seeding.** Each symbol's walk continues the same stream, so its path depends on how many symbols preceded it. Re-seeding a subset produces different series for the same symbol. The blueprint's *"per-symbol seeding"* addresses exactly this.

The walk branches on `price >= 100` — crypto versus forex — with plausible per-class step, wick and volume distributions. **That logic is sound and should be preserved**, not rewritten.

---

## 4. SCOPE

### IN SCOPE

**S1 — Base prices for all eleven instruments.** Realistic values for the five missing forex pairs and `SOL/USD`. This is reference data for a simulator, not a market claim.

**S2 — Per-symbol deterministic seeding.** Derive each symbol's RNG from a stable per-symbol seed so a symbol's series is reproducible independent of seeding order. State the derivation.

**S3 — Correlated walks.** Blueprint §5 asks for correlation. **Keep it defensible and simple** — USD-quoted majors sharing a common USD factor, crypto sharing a risk factor, is sufficient. Do not build a covariance model; that would be scope expansion and unverifiable.

**S4 — Watchlist sparklines from real series.** Rendered from the seeded candles, not synthesised at render time. **One code path per statistic** (`CA-P04-2`).

**S5 — `data-testid` on new regions.** Prior deliveries: 8, 10, 20, 17, 23, 20, 27, 33.

### 🔴 OUT OF SCOPE

- **`_base_price` for symbols not in `SUPPORTED_INSTRUMENTS`.** Do not extend `XAUUSD` or add instruments.
- **Any change to the live feed's real-adapter path.** This phase extends the *simulated* feed only.
- **Any change to inference, dataset, or ML services** — they branch on `seed:synthetic` and must not be touched.
- **DATA-P02** (session context, volatility state, multi-timeframe aggregation, `TD-029` resampling) · CHART · POLISH · the 718.83 kB bundle (`OBS-5`) · `F-BRAND-1`.
- **No new endpoint, schema or model.**

---

## 5. MANDATORY — BEYOND M1–M3

**M4 — No fabricated fallback price.** The current `defaults.get(s, Decimal("1.00000"))` fallback is precisely the `OBS-CONV2-1` pattern: an unknown input yields a plausible-looking number. Once all eleven are covered, an unknown symbol must **not** silently receive `1.00000`. Either raise, or return a value the UI renders as absence. **A wrong price is worse than no price.**

**M5 — Preserve the `--` absence path.** With the feed stopped, or a symbol unseeded, the watchlist must still render `--`. Do not replace absence with a last-known or zero value.

**M6 — Frontend T-1 guard.** Three phases have each added one; this domain needs its own. Extend the market/live test suite with a source-inspection guard over the watchlist/sparkline module:
- **non-vacuity anchors** — positive assertions the module renders the surface,
- assert the **provenance label is present**,
- absence of `place_order`, `submit order`, `go live`, `connect broker`, `broker_account`, `execute`.

Apply the SURF-P02 disclaimer-exclusion technique if a legitimate string contains a forbidden term.

**M7 — Determinism must be evidenced.** Seeding the same symbol twice with the same inputs must produce the same series. Prove it with a named test, not an assertion in the report.

---

## 6. STANDING REQUIREMENTS

**R1 — Independent degradation.** One symbol failing to seed must not blank the watchlist. The SURF per-source pattern is the standard.

**R2 — RBAC not widened.** 16/16 `protectedWorkspace()` wrappers; `ALL_AUTHENTICATED_ROLES = ["admin","operator"]`.

**R3 — Layout.** `OBS-SURF1-2`'s `flex-shrink: 0` is in the base. Verify any new container at 1920×1080 **by looking at the capture**.

**R4 — Suite green.** Current: **813 frontend / 418 backend = 1,231**. Never delete a failing test to reach green.

**R5 — `npm ci` before `tsc -b`.**

**R6 — Seeded evidence fixtures** go in the deviation register, per the pattern established in SURF-P03.

---

## 7. DELIVERY REQUIREMENTS

**Transport — eight consecutive hash-reconciled deliveries; repeat exactly.** Neither authority commits to the repository; the verified patch is the artifact of record.

```bash
git diff <base> > data_p01.patch
git apply --check data_p01.patch ; echo "exit=$?"
sha256sum data_p01.patch
```

Inline in the message body · **LF endings, terminating newline** · **state the full nine-element base chain**.

**Report must contain:**

1. The eleven base prices and their basis.
2. Per-symbol seed derivation (S2) and the determinism test name (M7).
3. Correlation approach (S3), stated plainly — including what it does **not** model.
4. **M1** confirmation: every generated row carries `source="seed:synthetic"`; no new provenance value.
5. **M2/M3** confirmation: every render site of a synthetic price, and its provenance label.
6. **M4** disposition: what an unknown symbol now does.
7. **M6** guard: anchors, forbidden list, passing.
8. Raw console transcripts — vitest, tsc -b, vite build, pytest.
9. **Level-I captures — raw PNGs**:
   - **the watchlist populated across all eleven instruments** — the defect this phase exists to fix,
   - sparklines rendering from seeded series,
   - **provenance labelling visible alongside prices** (M2),
   - **the `--` absence path still working** with the feed stopped (M5),
   - a single-symbol seed failure showing independent degradation.
10. **Interaction trace** for any click-dependent affordance.
11. Exact wording: *deleted* / *relocated* / *extended* / *surfaced* / *generated*.

---

## 8. ACCEPTANCE

1. All eleven instruments have base prices; none falls through to a default.
2. Per-symbol seeding; series reproducible independent of order, proven by named test (M7).
3. Correlation implemented and described; no unverifiable covariance model.
4. Sparklines from seeded series, one code path.
5. **M1** every generated row `source="seed:synthetic"`; inference/dataset/ML untouched.
6. **M2** provenance visible at every synthetic render site.
7. **M3** no "live"/"market"/"real-time" without the simulated qualifier.
8. **M4** no fabricated fallback price.
9. **M5** `--` absence path preserved.
10. **M6** frontend T-1 guard, non-vacuous, passing.
11. `data-testid` on new regions.
12. R1 independent degradation.
13. Suite green ≥ 1,231; nothing deleted to force green.
14. `tsc -b` clean; `vite build` succeeds.
15. RBAC not widened.
16. Captures attached incl. all-eleven populated, provenance visible, `--` path intact.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This Build Order authorizes **DATA-P01 only**. It is not authorization for DATA-P02, CHART or POLISH.
**Simulated data must never be presentable as market data.**

**We don't guess. We prove.**
