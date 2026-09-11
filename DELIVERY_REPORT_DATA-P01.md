# DATA-P01 DELIVERY REPORT
## Simulated feed extended to all eleven instruments — per-symbol seeding, correlated walks, watchlist sparklines

| Field | Value |
|---|---|
| Delivery | DATA-P01 — first phase of the DATA programme (Build Order `BUILD_ORDER_DATA-P01.md`, Operator-authorized 2026-08-17) |
| Issued by | AXIOM Development Authority (DA) |
| Issued to | AXIOM ITRGA |
| Date | 2026-08-17 |
| Base chain | `34f4c62` + item3 `b7b4c4f7…` + item5 `4c03910c…` + item6 `f65da5c3…` + item4 Rev B `a516c2c1…` + SURF-P01 `62c4d021…` + OBS-SURF1-2 `69964afe…` + SURF-P02 `e039c74b…` + SURF-P03 `c18d5d05…` |
| Patch | `/home/user/data_p01.patch` — sha256 `2af54d600e736359857717a94e01ea566213f4692e0a021bcb2dc8a03d473693` (977 lines / 40,146 B / 10 files, LF, terminating newline) |
| Governance posture | Gate CLOSED · Production NOT CERTIFIED · advisory-only |

---

## 1. The eleven base prices and their basis (S1)

Reference inputs for the simulator — plausible round levels per class, **not market
claims** (stated in the code comment and here):

| Symbol | Base price | Class |
|---|---|---|
| EURUSD | 1.10000 | forex (existing) |
| GBPUSD | 1.27000 | forex (existing) |
| USDJPY | 150.000 | forex (existing) |
| AUDUSD | 0.66000 | forex (S1) |
| USDCAD | 1.36000 | forex (S1) |
| USDCHF | 0.88000 | forex (S1) |
| NZDUSD | 0.61000 | forex (S1) |
| EURGBP | 0.86000 | forex (S1) |
| BTCUSD | 42000.00 | crypto (existing) |
| ETHUSD | 2500.00 | crypto (existing) |
| SOLUSD | 150.00 | crypto (S1; `_infer_class` now classifies SOLUSD as crypto — previously it fell through to forex) |

**Root cause of the ten `--` rows, found by inspection:** the simulated feed's
configured symbol list was `EURUSD,BTCUSD` only — the other nine instruments were
never fed. The default in `config.py` now lists all eleven (the local `.env` matches;
gitignored, disclosed).

## 2. Per-symbol seed derivation (S2) and the determinism test (M7)

```
symbol_seed(symbol, timeframe) = int(sha256("axiom:seed:synthetic:{SYMBOL}:{timeframe}")[:8], 16)
class_factor_seed(class, timeframe) = int(sha256("axiom:seed:synthetic:factor:{class}:{timeframe}")[:8], 16)
```

Each symbol draws from its own RNG; the class factor streams are pre-generated per
call from the class seed. A symbol's series therefore depends only on
(symbol, timeframe) — never on seeding order.

**M7 named test:** `test_chart_seed_per_symbol_determinism_and_order_independence`
(`backend/tests/test_live_market.py`) — proves (a) seeding EURUSD twice reproduces
the identical 40-bar close series, and (b) EURUSD's series is identical whether
seeded before or after GBPUSD (and equals its solo seeding). The previous single-RNG
design failed the order-independence half; the named test pins the new behaviour.

## 3. Correlation approach (S3), stated plainly

One shared factor stream per class per call, blended linearly into each bar's step:

- **forex factor** (sigma 6e-5): USD-quoted majors (EURUSD/GBPUSD/AUDUSD/NZDUSD)
  take +1; USD-base pairs (USDJPY/USDCAD/USDCHF) take −1; **EURGBP takes 0** (cross —
  no direct factor).
- **crypto factor** (sigma 12): BTCUSD/ETHUSD/SOLUSD take +1.

The original per-class step/wick/volume distributions are preserved unchanged.

**What it does NOT model** (stated, per the Build Order): no covariance matrix, no
cross-class correlation, no volatility clustering, no mean reversion, no
crypto/forex interplay — and none is claimed. The walk is a presentation
enablement, not a market model.

## 4. M1 — provenance on every generated value

The seeder's candle construction is unchanged in one respect that now matters most:
every bar is written with `source="seed:synthetic"` — **no new provenance value was
introduced anywhere in this patch** (verified by grep for source assignments across
the three touched backend files). The live feed's own rows carry
`source="live:simulated"` from the untouched adapter. Inference/dataset/ML services
are untouched — they branch on `seed:synthetic` exactly as before.

## 5. M2/M3 — provenance at every render site

- **Watchlist price rows:** a provenance chip derived directly from the quote's
  `source` field — `LIVE:SIMULATED` (never "LIVE" alone; M3) — `watchlist-provenance-*`
  testids. Capture 01 records 11 chips; capture 04 records 0 chips when quotes are
  absent (absence, not a fallback label).
- **Sparklines:** each sparkline carries a source tag derived from the candles'
  `source` field — `SEED:SYNTHETIC` — `watchlist-sparkline-source-*` testids. Capture
  01 records 11 tags.
- The existing terminal badges (`LIVE:SIMULATED`, `Provenance: SEED:SYNTHETIC
  (0 live · 80 seed)`) are untouched.

## 6. M4 disposition — unknown symbols now raise

`_base_price` raises `KeyError("no simulated base price for symbol … (seed:synthetic
reference data)")` for symbols outside the table. The `1.00000` fallback is gone —
an unknown symbol now fails loudly at adapter build/seeding instead of rendering a
plausible-looking wrong number. In practice unreachable: the config lists exactly the
eleven covered symbols.

## 7. M5 — the `--` absence path preserved

The watchlist's per-field absence logic is byte-identical (price/change/range each
degrade independently). Capture 04 proves it under a fresh backend where the feed
never started: **all eleven prices `--`** while the sparklines still render from the
persisted seeded candles — candle-derived context never fabricates a price.

## 8. M6 — frontend T-1 guard

`test_watchlist_ui_module_has_no_forbidden_controls` appended to
`backend/tests/test_live_market.py` (suite now **9/9**), pinning
`TerminalWatchlistDock.tsx` with two non-vacuity anchors (`market watchlist`,
`seed:synthetic` — the second anchors the provenance label, so M2 cannot be silently
removed) and the forbidden list (`place_order`, `submit order`, `go live`, `connect
broker`, `broker_account`, `execute`). No disclaimer-exclusion was needed — the
module contains no legitimate forbidden term.

## 9. R-requirements

| Req | Result |
|---|---|
| R1 | Per-symbol sparkline fetches degrade independently; capture 05 proves one aborted symbol removes only its sparkline (11 rows intact) |
| R2 | RBAC unchanged — no registry/route/role change in the patch |
| R3 | No new scroll container; the watchlist rows container scroll metrics recorded in capture 03; captures reviewed (the images are the check) |
| R4 | **170 suites / 818 frontend + 420 backend = 1,238 tests** (floor 1,231) |
| R5 | `npm ci` before `tsc -b` in both trees |
| R6 | No new seeded fixture — the feed itself is the fixture; the `.env` symbol-list change is local-only and disclosed |

## 10. Raw console transcripts (excerpts; full logs in `docs/evidence/uiconv/`)

```
$ git clone /home/user/axiom /tmp/d1verify && cd /tmp/d1verify
$ git apply item3.patch && … && git apply surf_p03.patch
$ git apply --check data_p01.patch
GIT_APPLY_CHECK_EXIT=0
$ git apply data_p01.patch
$ <10-path tree audit vs DA tree>
all paths identical
$ npm ci --no-audit --no-fund
added 148 packages in 2s
$ npx tsc -b --force --pretty false
(no errors)
$ npx vitest run
Test Files  170 passed (170)
     Tests  818 passed (818)
$ .venv/bin/python -m pytest -q
420 passed, 1 warning in 113.33s (0:01:53)
$ .venv/bin/python -m pytest tests/test_live_market.py -q
9 passed, 1 warning in 4.70s
$ npm run build
dist/assets/index-CH3UlO52.js   720.62 kB │ gzip: 192.83 kB
$ sha256sum dist/assets/index-*.js
19e8e3b669aa92b4e1c7ddcc093c3d585450822ae5719c6edae35bfde707cb22  (verify tree)
19e8e3b669aa92b4e1c7ddcc093c3d585450822ae5719c6edae35bfde707cb22  (DA tree)  ← identical
```

Bundle 718.83 → **720.62 kB (+1.79 kB)** — sparkline SVG + provenance chips;
disclosed per OBS-5.

## 11. Level-I captures (raw PNGs, per BO §7.9)

Gallery `DATA-P01_CAPTURES.html` sha256 `bbd1f86d45114becaa4029b076a873de10aa4d5ddfb1dda9acc4a4102baa0943`;
raw PNGs in `/home/user/data_p01_upload/`; machine-recorded DOM state
`DATA-P01_CAPTURE_VERIFICATION.json` sha256 `03375da8e4b92f57e43d074432769ebf6f0cb48266fe4248a5f6fb0953449fae`.

| Capture | Proof | SHA-256 |
|---|---|---|
| 01 All eleven populated | **11/11 prices, 0 dashes**; 11 provenance chips; 11 sparkline source tags | `79616147…71c5e8` |
| 02 Row selection interaction | hit-test **TRUE**; ticker EUR/USD → GBP/USD; row selected | `e187527f…8b0232` |
| 03 Crypto rows, scrolled | scroll metrics recorded; SOL/USD price + LIVE:SIMULATED chip in frame | `df478b44…b3544` |
| 04 Feed stopped — `--` path | **all 11 prices `--`**; 22 sparkline elements still render; 0 price chips | `56c174be…f8cf91` |
| 05 Single-symbol failure | GBPUSD sparkline absent; price intact; 11 rows | `36220ed8…26601f` |

**OBS-SURF3-1 closure:** the previously untransmitted
`SURF-P03_03_OPERATOR_ROLE_REAL_403_PARTIAL_DENIAL.png` (`f08ab63d…`) is included in
`/home/user/data_p01_upload/` with this delivery.

## 12. Deviations and disclosures (unprompted)

1. **Capture ordering:** capture 04 was shot against a *fresh backend process* (feed
   never started) so the `--` path is genuinely quote-less; the verification JSON
   records it after capture 05 (execution order, not capture numbering).
2. **Local `.env` change** (gitignored, disclosed): the live-feed symbol list now
   lists all eleven symbols — the same value as the shipped `config.py` default.
3. **`request()` status attachment / SURF-P03 remains in the base; nothing new.**
4. **Bundle +1.79 kB** — OBS-5.
5. Seeded series values changed from the previous single-RNG stream (they are now
   per-symbol deterministic) — no test pinned the old values; the non-degenerate
   geometry test still passes.

**No backend endpoint, schema or model change. No change to inference, dataset or ML
services. No change to the real-adapter path — the simulated feed only.**

## 13. Standing

CONV COMPLETE · SURF COMPLETE (OBS-SURF3-1 closure supplied herewith) · DATA-P01
delivered per this report and awaiting determination. DATA-P02, CHART, POLISH remain
unauthorized. Repository untouched — Operator-only.

---

**Gate CLOSED · Production NOT CERTIFIED**

*— AXIOM Development Authority (DA)*
*2026-08-17*

---

## 14. POST-DETERMINATION ADDENDUM (2026-08-17) — CA-DATA1-1 CORRECTION

ITRGA issued `ITRGA_DETERMINATION_DATA-P01`: **CORRECTION REQUIRED** — `CA-DATA1-1`
(blocker): USD/JPY generated on the crypto walk (`price >= 100` branch, not market
class; quantified 80 bars → 155.00, 100 bars → ~976), and `OBS-DATA1-1`: the M6
frontend T-1 guard claimed absent from the patch.

**OBS-DATA1-1 — factual answer, stated with the verified bytes.** The M6 guard IS in
the hash-verified artifact: `data_p01.patch` (sha256 `2af54d60…`, the exact file ITRGA
recorded) carries `test_watchlist_ui_module_has_no_forbidden_controls` at patch line
201, in the same `backend/tests/test_live_market.py` hunk as the determinism test
(`@@ -178,3 +178,86 @@`), pinning
`frontend/src/components/terminal/TerminalWatchlistDock.tsx` with the non-vacuity
anchors `"market watchlist"` and `"seed:synthetic"` and the full forbidden list. The
suite runs 9/9 and the full backend battery 420/420. The DA restates this with the
artifact rather than re-adding the test — but if ITRGA's extraction genuinely lacks
the hunk, the guard is reproduced verbatim below in the correction patch's transcript
note and can be re-applied at ITRGA's direction.

**CA-DATA1-1 — corrected in two places, because the defect was in two places:**

1. `chart_seed_service.py`: the walk now branches on `market_class`, not price
   magnitude. JPY-quote pairs take their own tick scale — 3-decimal quantization,
   step sigma 0.015 (15 pips of 0.001, mean 0.004), wick sigma 0.006; the forex
   factor stream is scaled ×100 for JPY pairs so the beta-correlation keeps the same
   relative weight (0.4 of one idiosyncratic sigma) as the majors instead of being
   numerically inert. **Chosen scale stated:** JPY pip = 0.01 (100× the EUR/USD pip
   of 0.0001), displayed at 3 decimals.
2. `adapters/simulated.py` (the live feed): the same class-blind `price >= 100`
   branch existed in `_next_candle` — the watchlist renders FEED quotes, so the
   closure capture required this fix too. JPY pairs now tick ±0.010 per tick on the
   3-decimal scale (was ±5.00 — capture 01 Rev A showed 155.00000; Rev B shows
   150.00000). Crypto and non-JPY forex branches are unchanged.

**Post-fix magnitudes (machine-recorded):** USD/JPY mean |step| 0.0136/bar, relative
9.06e-05 — the same order as EUR/USD (1.14e-04); 80 bars carry it 149.988 → 150.332
(+0.23%). ITRGA's closure criteria met; determinism test re-run green (series values
changed by design — the test proves determinism properties, not golden values).

**Correction patch:** `data_p01_correction.patch` — sha256
`1bbaee09eb06f22f724982a654f305e652489797c7afa4521cbf61a1229cd8b5` (86 lines /
4,988 B / 2 files, LF), base `34f4c62` + item3 + item5 + item6 + item4 + SURF-P01 +
OBS-SURF1-2 + SURF-P02 + SURF-P03 + DATA-P01. `git apply --check` exit 0 in a
pristine clone; both paths diff-identical; verify-tree pytest **420 passed**.

**Fresh transcripts (post-fix):** vitest **170 suites / 818 tests** · pytest
**420 passed** · `tsc -b` 0 errors · build `index-CH3UlO52.js` 720.62 kB unchanged
(correction is backend-only). Logs: `docs/evidence/uiconv/*_data_p01_correction.log`.

**Rev B captures (all five re-shot; USD/JPY 150.00000 in frame):**

| File | SHA-256 |
|---|---|
| 01 All eleven populated (USD/JPY corrected) | `f7eb407e7e37f74d3bb2874db864da4ef6d4a2314d2923fd99bd915b8e6ee73f` |
| 02 Row selection interaction | `ba9faa6d4fc2cf4220d4d1aac5841c2e2195cf0a46854502b6fc5cedd8304125` |
| 03 Crypto rows scrolled | `b719cd2f4181171c1d7e0ea448a20aa0ad43bb99eac7a3579fc45f0ab2cb36f5` |
| 04 Feed stopped — `--` path | `ed636b76310df9b9e9c57ccb2cf99dba7e8df93bef4f17d87be1c68a4078777e` |
| 05 Single-symbol failure | `8e2ee0298fe10758466ae8d17125c002bef65857ac922ce1b2c1a44bae55e01f` |

Gallery `DATA-P01_CAPTURES.html` (Rev B) sha256 `13f3bec3c28a596f0e510e61c3f22b52de9339e7765a7f2521ef71f04d74ddb9`;
JSON (Rev B) sha256 `e4273f49b4d7505a6009afdcd569979254c348703d10085185fe079ef730f653`.
Raw PNGs in `/home/user/data_p01_upload/`.

**Disclosures:** the local dev DB's stale forward-stamped `live:simulated` rows from
the stopped feed were cleared (gitignored local file) to permit re-seeding and a
clean capture 04; the correction touches only the two walk implementations — the
seeding, correlation, provenance, labelling and M4 fallback-raise are untouched, per
ITRGA's instruction not to rework them.
