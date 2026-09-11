# ITRGA DETERMINATION — BO-B-01
## Data Foundation (Pipeline Execution & Validation-Tier Separation)

| Item | Value |
|------|-------|
| Review identity | ITRGA independent review of DA Delivery Report `DELIVERY_REPORT_B-01.md` |
| Build Order | `BO-B-01` (Operator-authorized 2026-08-19) |
| Predecessor | `BO-B-00` — APPROVED WITH OBSERVATIONS |
| Date | 2026-08-19 |
| Evidence standard | Level I (direct) / Level II (executed) / Level III (documentary) |

---

## 1. What I verified (Level I/II — reproduced independently in my own environment)

| Check | Result |
|-------|--------|
| Patch `b01.patch.txt` sha256 | `a4049531…` — **matches** report |
| `git apply --check` onto my clone | **Applies clean** (exit 0) |
| 8 post-apply file SHAs | **All 8 match** the report's cited hashes exactly |
| New B-01 test suite (9 tests) | **9/9 passed** (1.53s) |
| **Full backend suite** | **489 passed** (135.53s) — matches report (489 / 134.03s) |
| Corpus generator determinism | **Confirmed** — regenerates byte-identical, honestly-labeled (`source=synthetic`, 2025 timestamps) series |
| Source-authority classification | **Confirmed** — `synthetic→SYNTHETIC`, `historical:real→AUTHORITATIVE`, `live:simulated→SIMULATED`, unknown→UNKNOWN |

## 2. Acceptance criteria vs. Build Order — line-by-line

| BO §8 criterion | Status |
|-----------------|--------|
| B-01.1: corpus ingested, truthful labels + provenance | ✓ 5 synthetic series, 10,000 bars, labeled end-to-end; API-probe log shows 5 completed runs, 0 invalid |
| B-01.1: ingestion stats/runs/candle-counts non-zero | ✓ `candle_count_total: 10000` (API log) |
| B-01.1a: tier rule documented + binding | ✓ `VALIDATION_TIER_SEPARATION.md` (SHA-verified) + code enforcement |
| B-01.1a: unit declared pipeline-validation | ✓ declared, synthetic permitted |
| B-01.2: snapshots + members + lineage populated w/ hashes | ✓ 9/9 test + execute log row counts; content hashes present |
| B-01.2: split manifests, temporal/no-look-ahead | ✓ split_store.py + manifest persistence test |
| B-01.2: random-split + label-horizon leakage rejected | ✓ existing pinned guards remain green (in 489 run) |
| B-01.3: features registered, records + quality reports | ✓ 3 builtin defs, feature records with lineage, quality reports |
| B-01.3: no-symbol-identity boundary | ✓ per-row assertion test + `identity_fields_excluded` |

**All acceptance criteria met.**

## 3. Tier-gate strict-direction (the pivotal safety property)

The most important claim — that synthetic data can prove the pipeline but can **never** reach a research conclusion — is proven in both directions:

- **Permissive direction:** `pipeline_validation` tier accepts labeled synthetic (test `test_b01_synthetic_corpus_freezes_under_pipeline_validation_tier` → `status=frozen`).
- **Strict direction:** `research_validation` tier quarantines the same corpus with reason `SYNTHETIC_SOURCE_NOT_AUTHORITATIVE` (test `test_b01_synthetic_corpus_quarantined_under_research_tier` → `status=quarantined`).

This is exactly the Operator's §4.3 correction, implemented and pinned. I independently re-executed both tests (green in the 9/9 run).

## 4. Evidence-completeness finding (R3 enforcement)

- `b01_execute_r1.log` (hash `cd078b88…`) is declared in the report's evidence inventory but was **not among the five relayed files**. This is a repeat of the B-00 observation pattern (the missing `pipaudit` log).
- **However:** the substance it would have evidenced — the executed pipeline row counts — is independently reproduced by the 9-test suite (which runs the full corpus→ingestion→snapshot→split→feature pipeline end-to-end against a real database in `test_b01_full_pipeline_end_to_end` and the other tests) and by my own execution. The gap is a **transmission-completeness** issue (protocol R3), not an outcome issue.

### Finding OBS-B01-1 (Low, delivery process)
The DA's own protocol R3 ("every declared hash must resolve to a transmitted artifact") has now been **violated twice in a row** (B-00: `pipaudit` log; B-01: `b01_execute_r1.log`). The report even claims §9 was "mechanically verified" — but a declared-hash-to-transmitted-artifact check would have caught this. This must be treated as a **standing corrective action**: the next Build Order will elevate R3 compliance to an explicit, separately-verified acceptance criterion with a mandatory transmission manifest (see §7).

## 5. Deviations — reviewed

| ID | Deviation | Assessment |
|----|-----------|------------|
| D1 | `compute_and_store` gained a `tier` keyword | Accepted — strictly necessary for B-01.3's own synthetic corpus; same strict default direction as the snapshot path |
| D2 | Runner tooling untracked | Accepted — generator + tests reproduce the pipeline; precedent B-00 D6 |
| D3 | No schema migration | Accepted — tier in existing `source_policy` JSON; manifests table pre-existed |
| D4 | Sandbox clock jumps | Accepted — corpus timestamps fixed in 2025; B-00 wall-clock bind untouched |
| D5 | Negative-control rows in dev DB | Accepted — deliberate evidence of the tier gate; additive; covered by BO §11 rollback |

## 6. Other observations (non-blocking)

- **OBS-B01-2 (Info):** fixture-convention labels (`sample:`/`csv:`/`test` → AUTHORITATIVE) remain for W2-U01 compatibility. The report correctly discloses this as a future reclassification risk. Not a defect — but ITRGA notes the convention is a latent honesty risk (a future ingest could mislabel real data as `sample:*` and be treated authoritative without explicit declaration). A future unit should tighten this.
- **OBS-B01-3 (Info):** features are the v1 builtin set only (3 features). Breadth is correctly deferred to B-02.

## 7. Corrective action (binding on the next Build Order)

**CA-B01-1:** BO-B-02's evidence section will (a) require a **transmission manifest** — a table mapping every declared artifact to its actual transmitted filename and hash, checked mechanically by the DA *and* independently by ITRGA before any determination; and (b) treat a missing declared artifact as an automatic **CORRECTION REQUIRED** on the delivery process, regardless of whether the substance is independently reproducible. This closes the twice-observed R3 gap.

---

## 8. Determination

| Field | Value |
|-------|-------|
| Determination | **APPROVED WITH OBSERVATIONS** |
| Basis | All BO §8 acceptance criteria met; all 8 file SHAs reproduced; 9/9 new tests + 489/489 full suite independently executed; tier gate proven in both directions |
| Observations | OBS-B01-1 (delivery process), OBS-B01-2, OBS-B01-3 (non-blocking) |
| Corrective action | CA-B01-1 (transmission manifest, binding on BO-B-02) |
| Next authorization state | **B-01 CLOSED** — BO-B-02 (ML Research Executed) may be issued |
| What this is not | Not production certification; not gate-opening; not authorization beyond BO-B-01 |

## 9. Record

- Patch sha256: `a404953193b257b2dee90dfe327131e55130d0f012ea38263e0bc3e6e20e3d45`
- Post-apply: 8/8 file SHAs reproduced · 9/9 new tests · 489/489 full suite
- Tier gate proven both directions (pipeline accepts, research quarantines)

> **We don't guess. We prove.** The pipeline now runs; the tier rule is enforced; the honest-labeling discipline holds end-to-end. Approved — with a standing fix on evidence transmission.

**End of ITRGA Determination BO-B-01**
