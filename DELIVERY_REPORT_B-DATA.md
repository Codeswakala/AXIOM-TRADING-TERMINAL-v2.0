# DELIVERY REPORT — BO-B-DATA (R1)
## Real Historical Data Acquisition & Authority-Label Hardening

| Item | Value |
|---|---|
| Build Order | `BO-B-DATA` (Operator R1 decision of 2026-08-19: "proceed with R1") |
| Predecessors | BO-B-00 · BO-B-01 · BO-B-02 (all APPROVED WITH OBSERVATIONS; CA-B01-1 binding) |
| Implementer | AXIOM Development Authority (DA) |
| Reviewer | ITRGA — determination pending (incl. source/license provenance review; lawfulness remains the Operator's legal responsibility per BO §0) |
| Date | 2026-08-20 |
| Governance Gate | CLOSED (unchanged) · Production NOT CERTIFIED (unchanged) |

---

## 1. Claimed scope vs. this Build Order

| BO requirement | Delivered | Where |
|---|---|---|
| Part A lands and is verified **first** | ✓ — Part A code + tests executed and green (61/61 affected, full suite 503) **before** any real-data ingestion | §3, §8 |
| A1 `historical:real` → AUTHORITATIVE (explicit only) | ✓ `authority_from_source` grants authority to exactly one label | §3 |
| A2 `sample:*`/`csv:*`/`test` → non-authoritative | ✓ mapped to UNKNOWN (guard-quarantined in authoritative mode; no new bypass class) | §3 |
| A3 sample-ingestion default cannot manufacture authority | ✓ default `sample:{name}` label is now honestly non-authoritative (code comment pinned) | §3 |
| A4 tests pin all of the above; W2-U01 churn disclosed | ✓ 3 new tests + 3 churned sites, each disclosed with reason | §3, §9 |
| A5 real-data ingest without explicit label quarantined from research tier | ✓ pinned test: `csv:*`-labeled rows → `UNKNOWN_SOURCE_AUTHORITY` quarantine | §3 |
| B1 source + license declaration | ✓ `B-DATA_SOURCE_LICENSE_DECLARATION.md` — two sources, terms references, bounded permitted-use statements, retrieval date/method; **Binance probed and rejected** (terms-eligibility refusal — treated as dispositive) | §4 |
| B2 corpus definition (multi-market, multi-symbol, honest) | ✓ 6 instruments × 2-year complete H1 (OKX, 17,520 bars each) + 6 instruments × 2-year D1 (Kraken, 701 bars each) = **109,326 real bars**; no fabricated/backfilled bars; complete windows | §5 |
| B3 retrieval + pinning | ✓ repeatable no-key GET method; per-file SHA-256 manifest (hash-recorded, itself hashed); corpus transmitted with this delivery | §5 |
| B4 ingestion with honest labels | ✓ 12 API ingestions, `source="historical:real"`, 0 invalid; **12/12 metadata rows `source_authority=AUTHORITATIVE`** | §6 |
| B5 ChronologyGuard at authoritative tier | ✓ research-tier freeze over real BTCUSDT H1: **frozen, 0 quarantine rows** (17,520 bars); first=2024-08-01T00:00Z last=2026-07-31T23:00Z — no future/duplicate/naive bars | §7 |
| B6 research-tier snapshot proof + negative control | ✓ real snapshot frozen at `research_validation` tier; synthetic control quarantined `SYNTHETIC_SOURCE_NOT_AUTHORITATIVE` | §7 |
| §3 exclusions honored | No live feed/broker/actuation; no disallowed data (Binance refused and dropped); no fabrication/backfill/relabeling; no research conclusions; no training/promotion/inference/signals/frontend/governance-doc changes; no repo publication | — |
| §9 CA-B01-1 transmission manifest | §11 — every declared artifact → transmitted filename + hash, mechanically verified | §11 |

## 2. What changed (files + SHAs + chain position)

Patch artifact: **`bdata.patch.txt`** — sha256 `72ca93eef292ccaa083099f189c9f22ab86b06716f4d409681d1ab8f386ff139`
- Applies clean (`git apply --check` exit 0) onto the verified 21-element chain over baseline `34f4c62`, in a pristine clone, as the **22nd chain element**; post-apply, all 6 files byte-identical to the DA workspace (cmp-verified); clone-side Part-A set 34/34, ruff clean.

| File | Content SHA-256 |
|---|---|
| `backend/app/ml/dataset/market_data_query.py` | `bc9b1af43cff6f3519b0609bff8b40e81b6804a127c71e2f84612bfe1d62c220` |
| `backend/app/api/routes/ingestion.py` | `cca4dd889be7bc0a4d6ab2ca447ac890d4c4952beaefb32601d9a51bd8917136` |
| `backend/tests/test_bdata_authority_labels.py` (new) | `26bc01542075366ed69e3409f044f2a6ad325b3455a7627e8b1a2876fec50129` |
| `backend/tests/test_market_agnostic_access.py` (churn) | `09b2034936ffba9844692ae5f704bfa8d4ef2bd057814b3ceb671d850abb882d` |
| `backend/tests/test_ml_dataset_architecture.py` (churn ×2) | `af01eeab3f636ed1a3a78e47028ea3decc16558678082b18a605ec0c4c0d74ba` |
| `backend/docs/B-DATA_SOURCE_LICENSE_DECLARATION.md` (new) | `5577ac861d639e8b199ff95a4d38f3287d95a80467b4b272ac49e269d84d18ca` |

## 3. Part A — label-hardening description + test churn disclosure

- `authority_from_source()` now grants AUTHORITATIVE to **exactly one string**: `historical:real`. `sample:*`, `csv:*`, `test` → UNKNOWN (the guard already quarantines UNKNOWN in authoritative mode, so no new authority class or bypass is introduced). `synthetic`/`seed:synthetic`/`live:simulated` unchanged.
- The `/sample` route default label is unchanged in string but now honestly non-authoritative; a comment pins the semantics (A3).
- **Test churn (3 sites, each disclosed with reason — same discipline as B-02 deviation D1, no deletion, no weakening):**
  1. `test_market_agnostic_access.py` — the mapping test's `sample:eurusd.csv` candle asserted AUTHORITATIVE; re-pinned to UNKNOWN with an inline comment citing A2.
  2. `test_ml_dataset_architecture.py` (a) — `get_source_metadata("sample:unit.csv")` asserted `"authoritative"`; re-pinned to `"unknown"` plus a new `historical:real` positive assertion.
  3. `test_ml_dataset_architecture.py` (b) — the freeze-mechanics snapshot fixture now declares `tier="pipeline_validation"` (fixture rows are non-authoritative under A2; machinery tests must not claim research authority).
- **Fail-first:** `bdata_probe_prefix.log` — 3/3 new tests failed pre-fix, including the exact hazard: an unlabeled snapshot *froze* at research tier under the legacy convention (now quarantined).

## 4. Data Source & License Declaration (summary — full text in `B-DATA_SOURCE_LICENSE_DECLARATION.md`)

| Source | Endpoint | Instruments | Retrieval | License/terms reference |
|---|---|---|---|---|
| OKX | `GET api.okx.com/api/v5/market/history-candles` (bar=1H) | BTC/ETH/SOL/XRP/ADA/DOGE-USDT spot | 2026-08-20 UTC, no key | OKX Terms of Service + public market-data API docs |
| Kraken | `GET api.kraken.com/0/public/OHLC` (interval=1440) | XBT/ETH/SOL/XRP/ADA/DOGE-USD | 2026-08-20 UTC, no key | Kraken Terms of Service + public REST API docs |

- **Permitted-use statement:** internal research and pipeline validation within this project only; pinned and hash-recorded; **not redistributed** as a data product.
- **Binance probed and rejected:** its API refused service from this environment citing its terms' eligibility clause ("b. Eligibility") — treated as dispositive per BO §3 (no data whose terms do not permit this use).
- **Lawfulness boundary restated:** the Operator retains final legal responsibility; ITRGA verifies provenance/honesty/reproducibility, not legality.
- **Honesty attestations:** bars written exactly as returned; unconfirmed OKX candles excluded; no gap-filling, interpolation, backfill, or relabeling.

## 5. Corpus description + pin manifest

- **OKX H1:** 6 instruments × 17,520 bars = 105,120 bars; window 2024-08-01T00:00Z → 2026-07-31T23:00Z (complete, zero missing hours).
- **Kraken D1:** 6 instruments × 701 bars = 4,206 bars; window 2024-08-30T00:00Z → 2026-07-31T00:00Z (exchange daily-window start disclosed).
- **Total: 109,326 real bars.** Pin manifest: `tests/fixtures/bdata_corpus/MANIFEST.json` (sha256 `2a2c09217e2bc450885ee9dfebc6943083caabfb0193a3684706c23dfa8bed4b`) — per-file SHA-256, bar counts, first/last timestamps, source tags. All 12 CSVs transmitted with this delivery (transmission manifest §11).

## 6. Ingestion + metadata evidence (executed)

`bdata_api_ingestion.log` — 12 × `POST /api/v1/ingestion/csv` with explicit `source="historical:real"`: every run `completed`, rows_valid = rows_inserted (17,520 ×6; 701 ×6), **0 invalid, 0 updated, 0 unchanged**; `GET /ingestion/stats` → `candle_count_total: 119,326` (109,326 real + the prior 10,000 synthetic corpus). `bdata_execute_r1.log` + direct query: **12/12 `market_series_metadata` rows with `source_authority=authoritative`** (BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT/ADAUSDT/DOGEUSDT H1 · BTCUSD/ETHUSD/SOLUSD/XRPUSD/ADAUSD/DOGEUSD D1).

## 7. Research-tier snapshot proof + negative control (executed)

`bdata_execute_r1.log`:
```
[bdata] research-tier REAL snapshot: status=frozen content_hash=a084ca77577a01a9…
[bdata] quarantine rows for real snapshot: 0 (must be 0)
[bdata] negative control status: quarantined (must be quarantined)
[bdata] negative control reasons: ['SYNTHETIC_SOURCE_NOT_AUTHORITATIVE']
```
The ChronologyGuard accepted 17,520 real bars at the authoritative tier with **zero quarantines** (no future-dated, out-of-order, duplicate, or naive timestamps); the same tier still refuses synthetic data. The tier rule now accepts genuinely authoritative data — the R1 unblock is real.

## 8. Test evidence (executed)

| Run | Result | Log |
|---|---|---|
| Part-A fail-first probe (pre-fix) | 3/3 failed incl. the silent-authority hazard | `bdata_probe_prefix.log` |
| Part-A + affected W2-U01 set | 61 passed | in `pytest_bdata_postfix.log` |
| **Full backend suite** | **503 passed, 1 warning, 140.71s** (500 + 3 new; 0 failed/skipped) | `pytest_bdata_postfix.log` |
| Clone-side (applied patch content) | 34 passed (Part-A + W2-U01 sets), ruff clean | `bdata_applycheck_transcript.txt` |

## 9. Deviations register

- **D1 — Corpus files are transmitted, not patched.** BO §6 allows pinned corpus files; the 6.5 MB of CSVs are hash-recorded (manifest) and transmitted with this delivery rather than embedded in the patch — the patch stays code+docs; the corpus is pinned evidence (real data cannot be regenerated; pinning is the audit mechanism).
- **D2 — Source substitution.** Binance-class sources were probed first (the BO names "public exchange historical klines" as a candidate class); Binance refused service on its own terms; **OKX + Kraken** — same candidate class, both keyless public endpoints — supplied the corpus. Disclosed in the declaration.
- **D3 — Kraken H1 depth limit.** Kraken's public H1 window is depth-limited to ~720 bars (verified empirically); the declaration records this and OKX supplies the deep H1 corpus. Kraken contributes the 2-year D1 cross-venue series.
- **D4 — Runner/fetch tooling untracked** (precedent B-00 D6 / B-01 D2 / B-02 D4); the pinned CSVs + manifest + logs are the evidence.
- **D5 — No schema migration.** Nothing new; labels ride existing fields.
- **D6 — W2-U01 test churn** fully disclosed in §3 (3 sites, each with reason; no deletions, no weakened assertions).

## 10. Known limitations / technical debt

- **License caveats:** both exchanges grant no explicit open-data license; the bounded internal-research posture is documented, and the Operator's legal responsibility per BO §0 stands. Any future redistribution or publication of this corpus requires a separate Operator legal review.
- **Real data is live-moving:** the corpus is pinned at retrieval time; re-retrieval yields different data — reproducibility rests on the hashes, not regeneration.
- Carried: PROJECT_STATE.md inventory stale (OBS-B00-3/OBS-B02-2); signal-layer semantic tightening record pending (OBS-B02-1); fixture-label convention now closed by this unit (OBS-B01-2/OBS-B02-3).

## 11. TRANSMISSION MANIFEST (CA-B01-1 — binding; mechanically verified before submission)

| # | Declared artifact | Transmitted filename | sha256 |
|---|---|---|---|
| 1 | B-DATA patch (chain position 22) | `bdata.patch.txt` | `72ca93eef292ccaa083099f189c9f22ab86b06716f4d409681d1ab8f386ff139` |
| 2 | Apply-check transcript (pristine clone) | `bdata_applycheck_transcript.txt` | `6e514644a2ef9275ecd222ead3a4bc1171931507dda995cfc2dbe404ed853bd6` |
| 3 | Fail-first probe log | `bdata_probe_prefix.log.txt` | `a1107a7364ffcb4a061d8603d463249dd5f9f067af554aafe20b39630d0026d6` |
| 4 | Retrieval log (both sources) | `bdata_fetch_r1.log.txt` | `eb16d3d9ee89d2c4838a9fa85147aaa7135b3384e7fe4096f4292b1f10767004` |
| 5 | API ingestion log | `bdata_api_ingestion.log.txt` | `7d43eff53c2f1489d56ce2ce43b909466b4b0a91cd2ce70b16db369a81a0f307` |
| 6 | Research-tier proof runner log | `bdata_execute_r1.log.txt` | `18814a67033dcd46252d6c4c3fc2113b5aa35e56146c33a9832d64d92e0b7e1b` |
| 7 | Full-suite log (503 passed) | `pytest_bdata_postfix.log.txt` | `b15f0434a602f1643c1fe0e55939fc07f932699474e4d365e7cc9fcdc070cfec` |
| 8 | Pin manifest | `MANIFEST.json.txt` | `2a2c09217e2bc450885ee9dfebc6943083caabfb0193a3684706c23dfa8bed4b` |
| 9–20 | Pinned corpus files (12 CSVs) | `corpus/okx_*_H1.csv`, `corpus/kraken_*_D1.csv` | per-file hashes in MANIFEST.json — **cross-checked this session: all 12 match** |
| 21 | License declaration | `B-DATA_SOURCE_LICENSE_DECLARATION.txt` | `5577ac861d639e8b199ff95a4d38f3287d95a80467b4b272ac49e269d84d18ca` |
| 22 | Delivery report | `DELIVERY_REPORT_B-DATA.txt` | (declared in the DA closing message — no self-referential hash in the table) |

**Every hash declared in this report resolves to a transmitted file in `/home/user/bdata_transmission/` — sha256sum -c exit 0 this session. All 22 entries newly transmitted.**

---

Gate CLOSED · Production NOT CERTIFIED · We don't guess. We prove.
