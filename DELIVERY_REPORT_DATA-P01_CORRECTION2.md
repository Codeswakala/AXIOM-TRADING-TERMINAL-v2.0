# DATA-P01 CORRECTION REPORT — CYCLE 2 (CA-DATA1-2 · OBS-DATA1-1 · OBS-DATA1-2)

| Field | Value |
|---|---|
| Delivery | Correction cycle 2 against `ITRGA_DETERMINATION_DATA-P01_CORRECTION.md` (2026-08-18) |
| Issued by | AXIOM Development Authority (DA) |
| Issued to | AXIOM ITRGA |
| Date | 2026-08-18 |
| Base chain | `34f4c62` + item3 + item5 + item6 + item4 Rev B + SURF-P01 + OBS-SURF1-2 + SURF-P02 + SURF-P03 + DATA-P01 (`2af54d60…`) + DATA-P01 correction 1 (`1bbaee09…`) |
| Patch | `/home/user/data_p01_correction2.patch` — sha256 `34edc1762b8691f99fb0e2a7880a021f2ecb962308ee3d25cc8d4f725d6c17d9` (222 lines / 11,160 B / 5 files, LF, terminating newline) |
| Governance posture | Gate CLOSED · Production NOT CERTIFIED · advisory-only |

---

## 1. CA-DATA1-2 — CLOSED: proportional crypto steps in BOTH generators

ITRGA's diagnosis accepted: the absolute crypto step (±5/tick adapter; ±8/35 seeder)
was calibrated for BTC and made SOL +3.33%/tick — the same defect class as
CA-DATA1-1, one instrument-class further. The correction makes every crypto
step and wick **proportional to the current price**, in both files:

- `chart_seed_service.py`: crypto factor stream is now fractional (σ 0.2%/bar);
  idiosyncratic step is `price × gauss(0.0004, 0.0083)` (mean +0.04%/bar, σ
  0.83%/bar); wicks are `price × gauss(0.0012, 0.002)`. All three cryptos share
  one relative volatility profile.
- `adapters/simulated.py`: crypto tick is `price × 0.0005` (±0.05%/tick), wicks
  `price × 0.00025` — proportional for BTC, ETH and SOL alike.

**Closure evidence, machine-recorded** (fresh seeds, 80 bars, dev DB):

| Symbol | mean relative step | max relative step |
|---|---|---|
| BTCUSD | 0.6949% | 2.07% |
| ETHUSD | 0.6946% | 2.42% |
| SOLUSD | 0.6351% | 2.06% |

Mean relative steps within **10% of each other** — versus the pre-fix SOL mean of
23.3%/bar and the +397% 100-bar projection ITRGA computed. Capture 03 (Rev C) shows
the three crypto rows moving proportionally (BTC 42,020.88 · ETH 2,501.25 ·
SOL 150.08).

**Named test:** `test_chart_seed_crypto_steps_are_relative_across_price_levels`
(`backend/tests/test_live_market.py`) — seeds all three cryptos, asserts each mean
relative step < 3%/bar and the three within one order of magnitude. Suite 14/14.

**The sweep ITRGA recommended:** executed by grep — the `price >= 100` /
`>= Decimal("100")` pattern and any remaining absolute `Decimal("5")`/`Decimal("8")`
walk constants are gone from every executable line in `backend/app`. The only
price-magnitude conditionals that remain are the seeder's class booleans
(`is_crypto` / `is_jpy`), which branch on market class, not magnitude.

## 2. OBS-DATA1-2 — CLOSED: JPY display precision routed from the quote convention

`TerminalWatchlistDock.tsx` now routes precision from the instrument's convention:
crypto → 2 decimals (locale), **JPY pairs → 3 decimals**, other forex → 5 decimals.
The range column routes the same way. Capture 01 (Rev C) shows **USD/JPY 150.010**.
Named test: `test_data_p01_obs1_2_jpy_price_displays_three_decimal_ticks`
(`terminalWatchlistDepth.test.tsx`), asserting `price-usdjpy` renders `150.010` and
never 4+ decimals, while non-JPY forex keeps `1.08450`.

## 3. OBS-DATA1-1 — M6 guard: present in BOTH patches, and extended here

**Restated with the verified bytes, once more:** the M6 guard has been present since
`data_p01.patch` (sha256 `2af54d60…`): `test_watchlist_ui_module_has_no_forbidden_controls`
sits in the `test_live_market.py` hunk at patch line 201 (hunk
`@@ -178,3 +178,86 @@`), pinning `TerminalWatchlistDock.tsx` with the anchors
`"market watchlist"` and `"seed:synthetic"` and the six forbidden strings. The suite
ran 9/9 at the time. This cycle makes the matter undeniable by **extending the guard
in the new patch itself** — the cycle-2 diff to `test_live_market.py` displays the
existing guard function as context, and adds a third non-vacuity anchor:
`assert "tofixed(3)" in text`, which pins the JPY display-precision routing
(OBS-DATA1-2) so the tick convention cannot regress at the render layer. The guard
now covers: surface presence, synthetic provenance labelling, JPY display precision,
and the actuation vocabulary.

## 4. What changed, where (cycle 2)

| File | Change |
|---|---|
| `backend/app/services/chart_seed_service.py` | Crypto factor stream fractional; proportional crypto steps + wicks (CA-DATA1-2) |
| `backend/app/market/adapters/simulated.py` | Proportional crypto tick + wicks (CA-DATA1-2) |
| `backend/tests/test_live_market.py` | +`test_chart_seed_crypto_steps_are_relative_across_price_levels` (CA-DATA1-2 proof); M6 guard extended with the JPY-precision anchor |
| `frontend/src/components/terminal/TerminalWatchlistDock.tsx` | JPY display precision routing (OBS-DATA1-2) |
| `frontend/src/terminal/terminalWatchlistDepth.test.tsx` | +JPY quote fixture; +`test_data_p01_obs1_2_jpy_price_displays_three_decimal_ticks` |

**Untouched, per ITRGA's instruction:** seeding derivation (S2), correlation betas
(S3), provenance labelling (M1/M2/M3), M4 fallback-raise, M5 absence path, the JPY
walk from correction 1, and all sparkline logic.

## 5. Executed-test position (fresh transcripts, this cycle)

```
$ pytest -q (in-memory)                                  → 421 passed, 1 warning in 124.84s
$ pytest tests/test_live_market.py tests/test_chart_history.py -q  → 14 passed
$ npx vitest run                                         → Test Files 170 passed · Tests 819 passed
$ npx tsc -b --force --pretty false                      → 0 errors
$ npm run build                                          → index-Dejk2QKj.js 720.67 kB (frontend precision delta; OBS-5)
$ git apply --check data_p01_correction2.patch (pristine chain)  → GIT_APPLY_CHECK_EXIT=0
$ 5-path tree audit vs DA tree                           → identical
$ verify-tree build sha256                               → 42d7c2cf3e64efcfc68ff8f91d2de24e3c0ae2bbe0dc2d50e78976abac810b9b (identical to DA tree)
```

Platform: **421 backend + 819 frontend = 1,240 tests** (was 1,238; +2 named tests).
Logs: `docs/evidence/uiconv/pytest_data_p01_r2.log`,
`vitest_data_p01_r2.log`, `tsc_data_p01_r2.log`, `vite_build_data_p01_r2.log`.

## 6. Rev C captures (all five re-shot; full hash table)

| Capture | Proof | SHA-256 |
|---|---|---|
| 01 All eleven populated | USD/JPY **150.010** (3 decimals); 11/11 prices, 0 dashes | `5a06d29ea9085f169f5784bab6c079e701827704750f4844f95ae1819ec15a67` |
| 02 Row selection interaction | hit-test TRUE; selection landed | `766eb716486a63ddf46223665422646266cdc7ca0958fe9ae2c10612b41d0ca4` |
| 03 Crypto rows scrolled | **proportional crypto moves** (BTC/ETH/SOL); provenance in frame | `5f89ca05496180dad989c31a980fba25334b2f9cd48222c6ad26b48ab45623ca` |
| 04 Feed stopped | all eleven `--`; sparklines persist; 0 price chips | `a83991693bb816fea4adb12c3ebba8ada6babdfba82e14a63c72914b1ef91ed4` |
| 05 Single-symbol failure | only GBP/USD sparkline absent; 11 rows | `8f160e77c1b700cb1705b278181a1e32bd944e10efe85372d26adcee62e57731` |

Gallery `DATA-P01_CAPTURES.html` (Rev C) sha256
`770d8e895ce9589d2050fcb2e223ef181a3b52a0564496ced25cf003d7cece7e`;
JSON (Rev C) sha256 `b4d5e4f3d709360f140d98e053ae09af83c42d56c554be45fbea6b9b1c982f35`.
Raw PNGs: `/home/user/data_p01_upload/`.

## 7. Disclosures

1. **Report transport correction:** the cycle-1 correction addendum was appended to
   `DELIVERY_REPORT_DATA-P01.md` in the workspace but evidently not transmitted;
   this cycle ships a **standalone** correction report (this file) so the record is
   unambiguous.
2. The local dev DB's `live:simulated` rows from stopped feeds were cleared
   (gitignored local file) before each capture session to keep absence-path evidence
   honest.
3. Series values changed again by design (proportional steps); the determinism and
   proportionality tests assert properties, not golden values — all green.
4. Bundle 720.62 → 720.67 kB (+0.05 kB) — the JPY precision routing; OBS-5.

**Nothing else was reworked.** DATA-P02, CHART, POLISH remain unauthorized.

---

**Gate CLOSED · Production NOT CERTIFIED**

*— AXIOM Development Authority (DA)*
*2026-08-18*
