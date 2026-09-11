# DELIVERY REPORT — BO-B-01
## Data Foundation (Pipeline Execution & Validation-Tier Separation)

| Item | Value |
|---|---|
| Build Order | `BO-B-01` (Operator directive of 2026-08-19: "authorized") |
| Predecessor | `BO-B-00` — APPROVED WITH OBSERVATIONS (ITRGA_DETERMINATION_B-00_FINAL.md) |
| Implementer | AXIOM Development Authority (DA) |
| Reviewer | ITRGA — determination pending |
| Date | 2026-08-19 |
| Governance Gate | CLOSED (unchanged) · Production NOT CERTIFIED (unchanged) |

---

## 1. Claimed scope vs. this Build Order

| BO requirement | Delivered | Where |
|---|---|---|
| B-01.1 corpus ingested, truthful labels + provenance | 5-series labeled `synthetic` corpus (10,000 H1 bars) ingested through the governed API seam; `market_series_metadata` + ingestion-run rows populated | §3, `b01_api_ingestion.log`, `b01_execute_r1.log` |
| B-01.1 ingestion/stats/runs/candle-counts non-zero with labels | API probes: 5 runs completed, 10,000 candles, 0 invalid | `b01_api_ingestion.log` |
| B-01.1a tier rule documented and binding | `backend/docs/VALIDATION_TIER_SEPARATION.md` + code enforcement (tier-aware freeze, tier-aware features, shared source-authority classifier) | §4 |
| B-01.1a this unit declared pipeline-validation | Declared (§4); synthetic permitted and labeled | §4 |
| B-01.2 snapshots + members + lineage populated with content hashes | 5 frozen snapshots (tier persisted in `source_policy`), 10,000 lineage rows, 5 series members, content hashes computed | §5 |
| B-01.2 split manifests populated; temporal, as-of-bounded, no-look-ahead | 5 manifests persisted (train 1000 / val 600 / test 400 each, hashed) | §5 |
| B-01.2 random splits + label-horizon leakage rejection evidenced | Existing pinned guard tests re-executed green + negative-control live evidence | §6 |
| B-01.3 feature definitions registered; records + quality reports populated | 3 builtin definitions; 10,000 feature records; 5 quality reports | §5 |
| B-01.3 no-symbol-identity boundary proven | Asserted per row in tests + `leakage_checks.identity_fields_excluded=True` in every quality report | §7 |
| §3 exclusions honored | No training, no inference/signals/alerts/intelligence, no assistant work, no frontend changes, no research conclusions claimed, no real-provider integration, no gate/actuation, no governance-document changes, no repo publication | — |
| §6 allowed files honored | All changes inside `backend/app/ml/dataset/*`, `backend/app/ml/features/*`, `backend/app/ingestion/*`, `backend/tests/**`, `backend/docs/` | §2 |
| §9 evidence model honored | Detached patch + per-file SHAs + apply-check transcript; every declared hash resolves to a transmitted artifact (R3 mechanically verified) | §10 |

## 2. What changed (files + SHAs + chain position)

Patch artifact: **`b01.patch.txt`** — sha256 `a404953193b257b2dee90dfe327131e55130d0f012ea38263e0bc3e6e20e3d45`
- Applies clean (`git apply --check` exit 0) onto the verified 19-element chain over baseline `34f4c62`, in a pristine clone, as the **20th chain element**; post-apply, all 8 files byte-identical to the DA workspace (cmp-verified); clone-side B-01 tests 9/9, ruff clean.

| File | Content SHA-256 |
|---|---|
| `backend/app/ml/dataset/market_data_query.py` | `f13fd62e5baa04281db2bd0a6f6711b9786a71c6d114c0d6f647e2cfeacbb9f6` |
| `backend/app/ml/dataset/service.py` | `6c5d72a8942050b495e209aa4b0a4044ba5d9d61087703198a103a0ac57d99d0` |
| `backend/app/ml/dataset/split_store.py` (new) | `b4ca76388aba2796aa658cd828e18925d39c65f6de1dde0812211cc22951e197` |
| `backend/app/ml/dataset/synthetic_corpus.py` (new) | `0349f0dcc965966a23b9e26cdc858a12dfef2e13a638cd55a0245c29a9ec3119` |
| `backend/app/ml/features/store.py` | `a61ba157920ae89d2938cbc1b3a5d7f5db06ebcbfe0028f607f0651963b0c541` |
| `backend/app/ingestion/service.py` | `bec1d1645af39ca65eaa450b8ab4ddaab7d3138a9eb79b82ebf31fcbe75c44fb` |
| `backend/docs/VALIDATION_TIER_SEPARATION.md` (new) | `2bbd54fcb145d1571984c8e88cfdd8bb347fa297283e278c79c71a75d07ee8d0` |
| `backend/tests/test_b01_data_foundation.py` (new) | `e4b60a66aa781c665b59a1b6274e0d6212f3ef4f4d01cce2d85aac0a16cda688` |

Per protocol R5: no commits, pushes, or pulls — the patch artifact is the record.

## 3. Corpus description and source labels

**Corpus: 5 series × 2,000 H1 bars = 10,000 bars, all labeled `source="synthetic"`.**

| Series | market_class | Base | Generator |
|---|---|---|---|
| EURUSD · GBPUSD | forex | 1.10000 / 1.27000 | zero-mean walk, σ=0.00015 (chart-seeder discipline) |
| USDJPY | forex | 150.000 | zero-mean walk, σ=0.015 (JPY tick convention) |
| BTCUSD · ETHUSD | crypto | 65000 / 3200 | zero-mean walk, σ=0.0083 |

- Deterministic per (market_class, symbol, seed) — `app/ml/dataset/synthetic_corpus.py` (in the patch); ITRGA can regenerate byte-identical CSVs.
- Ingested through the **governed API seam** (`POST /api/v1/ingestion/csv`, operator-authenticated, path-allowlisted to `tests/fixtures/`) with explicit `source="synthetic"`; the ALLOWED_ROOTS discipline was preserved, not loosened (§7 of the BO).
- Every series persisted a `market_series_metadata` row with `source_authority=synthetic` (the ingestion service now upserts metadata on every successful ingest).
- **No series is labeled real.** The two built-in sample CSVs were not used as "real" evidence of anything; the corpus honesty rule is followed end-to-end.

## 4. Tier declaration for this unit

**This unit is `pipeline_validation` tier over a labeled `synthetic` corpus** — declared per the binding rule in `backend/docs/VALIDATION_TIER_SEPARATION.md` (§R4) and enforced in code:

1. `DatasetSnapshotInput.tier` (strict default `research_validation`; unknown tiers rejected).
2. `create_draft_snapshot` persists `source_policy = {source, authoritative_only, tier}`.
3. `freeze_from_canonical_records` runs the chronology guard in authoritative mode unless the persisted tier is `pipeline_validation`.
4. `FeatureStoreService.compute_and_store` accepts a `tier` (strict default) and applies the same gate.
5. `authority_from_source()` is now the **single** classifier: `synthetic`→SYNTHETIC, `historical:real`→AUTHORITATIVE (both additive); legacy labels unchanged (all existing tests preserved).

## 5. Snapshot / split / feature evidence (executed)

From `b01_execute_r1.log` (dev database, fresh schema, Level-I query output):

```
[b01] ingested H1 series found: 5 -> crypto/BTCUSD, crypto/ETHUSD, forex/EURUSD, forex/GBPUSD, forex/USDJPY
[b01] registered feature definitions: ['return_1', 'range_pct', 'rolling_return_3']
[b01] frozen BTCUSD: status=frozen tier=pipeline_validation content_hash=4e080ab0…
[b01] split split-b01-btcusd: train=1000 val=600 test=400 hash=9dc8b548…
[b01] features BTCUSD: records=2000 quality_report=3e64fd77… leakage_checks={'causal': True, 'identity_fields_excluded': True}
     … (same for ETHUSD, EURUSD, GBPUSD, USDJPY — 5/5 frozen, 5/5 split, 10,000 feature rows)
[b01] ---- table row counts (post-execution) ----
[b01] ingestion_runs: 5
[b01] market_series_metadata: 5
[b01] dataset_snapshots: 6            (5 pipeline-validation + 1 negative control)
[b01] dataset_lineage_records: 10000
[b01] dataset_series_members: 5
[b01] dataset_split_manifests: 5
[b01] feature_definitions: 3
[b01] feature_records: 10000
[b01] feature_quality_reports: 5
[b01] dataset_quarantine_records: 200
```

API-probe evidence (`b01_api_ingestion.log`): 5 `POST /ingestion/csv` responses all `completed`, rows_read/valid/inserted 2000 each, invalid 0; `GET /ingestion/runs` shows 5 runs with labels; `GET /ingestion/stats` → `candle_count_total: 10000`; `GET /ingestion/candle-counts` → 10000.

## 6. Leakage / random-split rejection evidence

- **Random split rejected:** `ChronologyGuard.validate_temporal_split` raises `SPLIT_LEAKAGE` for `random|shuffle|random_row` — pinned by the existing `test_random_split_rejected_and_label_horizon_leakage_rejected` (green in the 489-run).
- **Label-horizon leakage rejected:** `validate_label_horizon` raises `LABEL_HORIZON_LEAKAGE` when `label_horizon_end + embargo > validation_start` — same pinned test.
- **Live negative control (tier gate):** a `research_validation` freeze attempt over the synthetic corpus returned `status=quarantined` with 200 quarantine rows, reason `SYNTHETIC_SOURCE_NOT_AUTHORITATIVE` — the tier gate blocks synthetic data from any research conclusion, in the running system, not just in tests.
- **Fail-first:** `b01_probe_prefix.log` records the pre-fix state — the test module could not even collect because none of the B-01 mechanisms existed (tier concept, honest labels, split store, corpus generator, tier document). 9/9 post-fix.

## 7. No-symbol-identity boundary evidence

- `test_b01_features_computed_with_quality_report_and_no_identity` asserts per-row: no `symbol`, `provider`, or `market_class` key in any feature output.
- Every quality report carries `leakage_checks={'causal': True, 'identity_fields_excluded': True}` (machine-written by the store's own assertion path — `_assert_no_identity_output` raises on identity keys; the builtin set is `return_1 / range_pct / rolling_return_3`, all price-normalized, market-agnostic).
- The existing `test_ml_dataset_modules_do_not_introduce_symbol_identity_feature_pattern` remains green.

## 8. Test evidence (executed)

| Run | Result | Log |
|---|---|---|
| B-01 fail-first probe (pre-fix) | collection error — mechanisms absent | `b01_probe_prefix.log` |
| B-01 suite (post-fix, workspace) | **9 passed** | in `pytest_b01_postfix.log` |
| **Full backend suite** | **489 passed, 1 warning, 134.03s** (480 prior + 9 new; 0 failed/skipped) | `pytest_b01_postfix.log` |
| Clone-side (applied patch content) | **9 passed**, ruff clean, re-apply exit 0 | `b01_applycheck_transcript.txt` |

## 9. Deviations register

- **D1 — Feature-store tier parameter.** BO §6 authorizes `backend/app/ml/features/*`; `compute_and_store` gained a `tier` keyword (strict default `research_validation`) because the store hardcoded authoritative mode — without it, B-01.3's own synthetic corpus could not be feature-encoded under any circumstances. Same rule, same default direction as the snapshot path.
- **D2 — Runner tooling untracked.** `scripts/b01_execute.py` is DA evidence tooling (precedent: B-00 D6); the patch ships the deterministic corpus generator + tests, which reproduce the entire pipeline. Generated corpus CSVs live under `backend/tests/fixtures/b01_corpus/` (untracked, regenerable byte-identically).
- **D3 — No schema migration.** BO §11 allows migrations only if strictly required; none was — the tier lives in the existing `source_policy` JSON column, and `dataset_split_manifests` already existed (W2-U04 model, previously unpopulated).
- **D4 — Sandbox clock jumps.** Corpus timestamps are fixed in 2025 (deterministic); the B-00 wall-clock bind is untouched; no future-dating introduced.
- **D5 — Negative-control rows remain in the dev DB.** The 200 quarantine rows and the quarantined control snapshot are deliberate evidence of the tier gate; they are additive rows in the local gitignored dev database (BO §11 rollback covers them: stop ingestion, drop rows, revert patch).

## 10. Known limitations / remaining risk

1. **The corpus is synthetic by design** — it proves the pipeline; it cannot and will not substantiate market conclusions (tier rule, enforced).
2. **Fixture-convention labels** (`sample:`/`csv:`/`test` → AUTHORITATIVE) remain for W2-U01 test compatibility; production ingestions must pass explicit source labels — documented in the tier rule; a future unit may reclassify the convention.
3. **Features are the v1 builtin set only** (returns/range/rolling-return) — breadth is B-02+'s concern.
4. **The dev DB now contains execution evidence rows** (10,000 candles + lineage + features ≈ 40 MB) — local, gitignored, disclosed; removable per BO §11 without any effect on the artifact chain.

## 11. Technical-debt entries

Register updated: `TD-B01-UNIT` (this unit) · `OBS-B00-1` disposition (corrective applied this delivery: every declared hash mechanically verified against transmitted files) · `OBS-B00-2` disposition (resolved by BO-B-01 §9's ratified wording) · `OBS-B00-3` carried (PROJECT_STATE.md inventory update still deferred — outside this order's allowed files).

## Evidence inventory (all hashes verified on disk this session)

| Artifact | sha256 |
|---|---|
| `b01.patch.txt` (chain position 20) | `a404953193b257b2dee90dfe327131e55130d0f012ea38263e0bc3e6e20e3d45` |
| `b01_applycheck_transcript.txt` | `e99ee12c8fc4600e2824a52eaf0804e64ac688e1f06ca086180ba935e674dd7d` |
| `docs/evidence/uiconv/b01_probe_prefix.log` | `e48d8fab49132443e6b80cf72a1ae08ec1842420360229d8cefde5d56c75dca9` |
| `docs/evidence/uiconv/b01_api_ingestion.log` | `53c2a2641e8f44977b2ca237957ec423468a31e517f6756c32845e8f38f2f0b3` |
| `docs/evidence/uiconv/b01_execute_r1.log` | `cd078b883f1e4de475d458a2d84d6bfe34f5345d319a7b272ee3b1f9a3d723b1` |
| `docs/evidence/uiconv/pytest_b01_postfix.log` | `15319df181d34de8f5ed2514e6238f1169b63fb1bd7ea102edc17e5b6b6e27b5` |

---

Gate CLOSED · Production NOT CERTIFIED · We don't guess. We prove.
