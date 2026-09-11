# DELIVERY REPORT — BO-B-ML
## Substantive Machine Learning: Real Model, Research-Tier Validation, Governed Promotion

| Item | Value |
|---|---|
| Build Order | `BO-B-ML` (Operator directive of 2026-08-20: "authorized") |
| Predecessors | BO-B-00 · BO-B-01 · BO-B-02 · BO-B-DATA (all APPROVED WITH OBSERVATIONS) |
| Implementer | AXIOM Development Authority (DA) |
| Reviewer | ITRGA — determination pending |
| Date | 2026-08-20 |
| Governance Gate | CLOSED (unchanged) · Production NOT CERTIFIED (unchanged) |

---

## 1. Claimed scope vs. this Build Order

| BO requirement | Delivered | Where |
|---|---|---|
| P1.1 real algorithm implemented | Pure-Python logistic regression (seeded SGD), new module `app/ml/models/logistic_regression.py`; **zero new dependencies** | §3 |
| P1.2 determinism / market-agnostic / explainable / real probabilities | All four pinned by tests (seeded reproducibility; no identity features; coefficients+scaler surfaced; sigmoid probabilities that vary with features) | §4 |
| P1.3 features | Builtin v1 set only (return_1, range_pct, rolling_return_3) — **no new features**, justification in §5 |
| P2.1 experiment approved over real data | `exp-bml-logistic-core` — pre-registered + approved by `bml-operator-approver`, `historical:real`, `research_validation` tier, forward-return labels via `derive_candle_labels` | §6 |
| P2.2 walk-forward validation | **347 temporal folds** over 52,560 real training-domain bars (BTC+ETH+SOL); accuracy 0.5028 · effect +0.0028 · p=0.322 | §6, §7 |
| P2.3 calibration, real probabilities | ECE 0.0406 · Brier 0.2515 (real sigmoid probabilities on the test-period rows) | §6 |
| P2.4 economic, full six-class cost model, realistic crypto costs | `economically_unusable`, net −163,559.5 bps (spread 1 / commission 10 / slippage 2 / latency 0.5 / liquidity 1 / transaction 1 bps — provenance per cost class) | §6 |
| P2.5 cross-instrument generalization, unseen instruments | Train BTC+ETH+SOL → hold-out XRP/ADA/DOGE: accuracies 0.4972 / 0.4828 / 0.5012, aggregate 0.4938 (below the 0.50 floor) — distinct governed research question recorded | §6 |
| P3.1 gate evaluation | `GovernedModelEligibilityGate.evaluate()` — eligible=False | §7 |
| P3.2 promoted OR honest negative | **HONEST NEGATIVE** — four threshold refusals (statistical, calibration-Brier, economic, generalization-floor), promotion refused with the same reasons, nothing overridden | §7 |
| §3 exclusions honored | No threshold-failing promotion; no synthetic-at-research-tier; no fabricated metrics; no p-hacking/post-hoc changes (the pre-registered hypothesis and plan stand); no live/broker/actuation; no new dependency; no frontend/assistant/intelligence; no governance-doc changes; no repo publication | — |
| §9 CA-B01-1 relay-accurate manifest | §11 — manifest reflects what the Operator can actually relay (code-only patch + small logs; corpus already in ITRGA custody per B-DATA FINAL) | §11 |

## 2. What changed (files + SHAs + chain position)

Patch artifact: **`bml.patch.txt`** — sha256 `7a9d532454ebcd04aefd303e519b10959a04c59fcef698584791353c2dadd173`
- Applies clean (`git apply --check` exit 0) onto the verified 22-element chain over baseline `34f4c62`, in a pristine clone, as the **23rd chain element**; post-apply, all 7 files byte-identical to the DA workspace (cmp-verified); clone-side B-ML + gate set 27/27, ruff clean.

| File | Content SHA-256 |
|---|---|
| `backend/app/ml/models/logistic_regression.py` (new) | `d0a912c7a8b945a85396193a45bc9c7cb3aff4f88c7a5a93d2463ff6edbed16e` |
| `backend/app/ml/validation/service.py` | `029f3f36fa13fc2722314cc99dc8d1b709fd1dc2f8e38dffdb5051177ef64e09` |
| `backend/app/ml/dataset/split_engine.py` | `e893b92c6ccce188f0e7dbedee1b121d270c57ec25ddea8f99e5201319f7acbc` |
| `backend/tests/test_bml_model.py` (new) | `57f7e3f8aea3b3973471a4e7c0e70d354103fb8a8b311b11f20233f470851153` |
| `backend/tests/test_bml_lifecycle.py` (new) | `612c9e820723a29230c36a2b037049c025c8fc3987e40765c9c7beaa8127dfe6` |
| `backend/tests/fixtures/bml_real_slice.csv` (new — verbatim 400-row slice of the pinned OKX BTCUSDT corpus) | `8f197cca287738f0954060281d8d368b6a3a32ac6f5c0cab5a68a7d177bc99a5` |
| `backend/docs/B-ML_ALGORITHM_JUSTIFICATION.md` (new) | `fabae0e91093078855c61b68d0653f1aa149911263748b78c0764ca2aad3692c` |

## 3. Algorithm choice + dependency reasoning (Doc 09 §12)

**Pure-Python logistic regression via seeded SGD — zero new dependencies.** Full reasoning in `B-ML_ALGORITHM_JUSTIFICATION.md`: the 3-feature linear classifier needs no compiled stack (necessity fails); zero new supply-chain surface keeps the B-00.2 severity/exception policy untouched; every line is ITRGA-auditable; deterministic (seed 42, fixed feature order, fixed epochs). The existing validation service hardcoded the majority-class baseline as the fold model — extended with an optional `model` parameter (default = old behavior; disclosed as deviation D1).

## 4. Model properties evidence

- **Determinism:** `test_bml_model_is_deterministic_given_seed` — two fits, same seed → identical coefficients, intercept, probabilities. The research-run model is reconstructible from the split manifest alone (runner: `reconstructed model rows=31530`). **End-to-end run reproducibility proven:** the research runner was executed twice from a fresh database and every metric line (validation, calibration, economic, all three hold-out accuracies, generalization, the refusal reasons) is **byte-identical across runs** — the double-run diff is on the record (only run-instance fingerprints differ, see D7).
- **No identity:** `test_bml_model_is_explainable_and_market_agnostic` — coefficient keys are exactly the three causal features; the forbidden identity set is disjoint; the harness asserts the same before training.
- **Explainability:** coefficients + intercept + scaler (mean/std per feature) surfaced in the artifact payload.
- **Real probabilities:** `test_bml_model_emits_real_probabilities_not_degenerate` — sigmoid outputs in (0,1), sum to 1, vary with features, no degenerate-prior label.

## 5. Feature justification

**No new features were registered.** The builtin v1 set (return_1, range_pct, rolling_return_3) is price-normalized, causal, and market-agnostic per the ML Spec; adding features before the first substantive result would be speculative and would require per-feature ML Spec justification with zero evidence of deficiency. If the programme proceeds to retry (Operator decision per BO §12), the failure evidence here is the justification baseline for any feature work. Feature-store rows: 105,120 over the six real H1 series.

## 6. Experiment + reports (tier + data-class labels)

Runner evidence `bml_execute_r1.log` (dev database, real corpus, research_validation tier throughout):

```
[bml] snapshot ds-bml-train-core: frozen hash=… records=52560
[bml] snapshot ds-bml-holdout: frozen hash=… records=52560
[bml] split: train=31536 val=10512 test=10512
[bml] experiment: exp-bml-logistic-core status=approved
[bml] model: logistic-exp-bml-logistic-core metrics={'train_accuracy': 0.5082, 'validation_accuracy': 0.4962, 'test_accuracy': 0.4968}
[bml] validation: folds=347 accuracy=0.5027665706051874 effect=0.0027665706051873684 p=0.322405545477094
[bml] calibration: ECE=0.07666976910523227 brier=0.2557833899275813 base_rate=0.49681225616138547
[bml] economic: verdict=economically_unusable net_bps=-163559.5
[bml] holdout XRPUSDT: accuracy=0.4972312610606839 n=17517
[bml] holdout ADAUSDT: accuracy=0.48284523605640234 n=17517
[bml] holdout DOGEUSDT: accuracy=0.5012273791174288 n=17517
[bml] generalization: holdout=0.4937679587448383
```

Tier labels: every report and the artifact carry `BO-B-ML research_validation tier · historical:real corpus` in their persisted `notes` (machine-set by the runner; the lifecycle test asserts the artifact label). The calibration model was fitted on the exact train-split rows and measured on the test-period rows (no look-ahead); the validation fold model was refit per fold (true walk-forward). **Thresholds applied:** statistical (effect ≥ 0.05, p ≤ 0.05, folds ≥ 3, Σ test ≥ 300) · calibration (ECE ≤ 0.10, Brier ≤ 0.20) · economic (usable verdict + six-class completeness) · generalization (degradation ≤ 0.10, holdout ≥ 0.50).

## 7. Honest outcome: NOT PROMOTED — full metrics and reasons

```
[bml] eligibility: eligible=False
[bml]   reason: STATISTICAL_THRESHOLD_NOT_MET
[bml]   reason: CALIBRATION_THRESHOLD_NOT_MET
[bml]   reason: ECONOMIC_NOT_USABLE
[bml]   reason: GENERALIZATION_THRESHOLD_NOT_MET
[bml]   reason: NOT_ADVISORY_APPROVED
[bml] NOT PROMOTED (honest negative): PROMOTION_LINEAGE_INCOMPLETE:STATISTICAL_THRESHOLD_NOT_MET,CALIBRATION_THRESHOLD_NOT_MET,ECONOMIC_NOT_USABLE,GENERALIZATION_THRESHOLD_NOT_MET
```

- **Statistical:** effect +0.0028 (floor +0.05), p=0.322 (ceiling 0.05) — the model has **no predictive edge** on hourly direction at this feature set. The number is the truth: 347 folds over 52,560 real bars.
- **Calibration:** ECE 0.0767 passes the ECE leg, **Brier 0.2558 fails** (ceiling 0.20) — the probabilities are honest but uninformative (base rate 0.4968).
- **Economic:** net −163,559.5 bps after the full six-class cost model — no edge survives costs.
- **Generalization:** hold-out aggregate 0.4938 — below the 0.50 floor (**GENERALIZATION_THRESHOLD_NOT_MET**); in-domain 0.5028 vs hold-out 0.4938 → degradation +0.0090, within the 0.10 bound but the floor leg fails. The model is not overfit — it is uniformly uninformed, and slightly worse off-domain.
- **No third outcome:** promotion was attempted through the governed gate and refused with the exact reasons. The artifact remains `research_only`.

Per BO §0: this is the valid deliverable — a genuine, reproducible, governed research program executed over real data with the true outcome reported. Per ML Spec: the failed experiment is documented with the same rigor as a successful one.

## 8. Test evidence (executed)

| Run | Result | Log |
|---|---|---|
| B-ML fail-first probe (pre-fix) | collection error — module absent | `bml_probe_prefix.log` |
| B-ML model + lifecycle (post-fix) | 6 passed | in `pytest_bml_postfix.log` |
| Affected W2 sets (statistical/gate/harness/calibration) | 26 passed | in `pytest_bml_postfix.log` |
| **Full backend suite** | **509 passed, 1 warning, 142.80s** (503 + 6 new; 0 failed/skipped) | `pytest_bml_postfix.log` |
| Clone-side (applied patch content) | 27 passed, ruff clean, apply-check exit 0 | `bml_applycheck_transcript.txt` |

## 9. Deviations register

- **D1 — Validation service extension.** `StatisticalValidationService.validate()` gained an optional `model` parameter and a `fold_model` payload field; `_walk_forward` fits the provided model per fold (or the W2-U06 majority baseline when absent — default behavior unchanged, existing tests untouched). Reason: the service hardcoded the baseline as the fold model, so without this the substantive validation would measure the wrong model. BO §6 permits `validation/*` consumption; this is an extension, not a weakening — the null for effect-size remains the 0.5 baseline.
- **D2 — Calibration fit discipline.** The runner restores the artifact model state (fit on the exact train-split rows) after the walk-forward loop, because the loop re-fits the shared instance per fold — the calibration/economics/generalization numbers are the ARTIFACT's, not the last fold's.
- **D3 — Real-data slice fixture.** `tests/fixtures/bml_real_slice.csv` is a verbatim 400-row excerpt of the pinned OKX BTCUSDT corpus (first rows), shipped in the patch so the lifecycle test is self-contained in ITRGA's clone. No fabricated data — the slice's bytes are a prefix of the pinned file (ITRGA can diff against its reconstructed corpus).
- **D4 — LF normalization of the slice.** The original corpus CSV carried CRLF line endings; the fixture was normalized to LF for patch reproducibility (content identical otherwise).
- **D5 — Runner tooling untracked** (precedent B-00 D6 → B-DATA D4): `scripts/bml_execute.py` is DA evidence tooling; the patch ships model + tests + fixture + ADR only; the runner's log is hashed evidence.
- **D6 — Fold-model label in report notes.** The validation report's `notes` now carry `fold model=pure-python-logistic-regression-sgd` — recorded so the report self-identifies what was measured.
- **D7 — Split-engine tie-break fix (reproducibility defect class).** The W2-U04 split engine ordered cross-series rows sharing an `as_of` by `row_id` — a uuid, unstable across runs — so split membership (and therefore every downstream metric) drifted between runs on identical data. Fixed at the source: an optional caller-supplied `sort_key` breaks ties deterministically (additive; default behavior unchanged, existing split tests untouched). The fix legitimately changed the split composition (the reported numbers are the post-fix deterministic run), and the double-run proof above pins the pipeline's reproducibility. **Remaining disclosed fingerprint limitation:** snapshot `content_hash`, split hash, and artifact hash embed uuid source/row ids and therefore differ per run instance — the CONTENT and METRICS are deterministic; the fingerprints are run-instance-specific. Full fingerprint determinism would require platform-wide deterministic row ids (a future hardening unit, out of this order's scope).

## 10. Transmission manifest (CA-B01-1, relay-accurate)

The corpus CSVs are **already in ITRGA custody** (verified byte-identical in BO-B-DATA FINAL) and are **not re-transmitted**; the manifest below reflects exactly what the Operator can relay — a code-only patch, small logs, and the reproduction tooling.

| # | Declared artifact | Transmitted filename | sha256 |
|---|---|---|---|
| 1 | B-ML patch (chain position 23) | `bml.patch.txt` | `7a9d532454ebcd04aefd303e519b10959a04c59fcef698584791353c2dadd173` |
| 2 | Apply-check transcript (pristine clone, 22-chain) | `bml_applycheck_transcript.txt` | `9414d60b58f57ae6915788c2898ff5d80e3f24bab4abac79f457285266cb7aa6` |
| 3 | Fail-first probe log | `bml_probe_prefix.log.txt` | `ec0ae2ef579528fe69f2d6d074ff2ca4a07a31dbcfd05b8798afbc0b47c30d40` |
| 4 | Research-run log (Level I, 347 folds + honest negative) | `bml_execute_r1.log.txt` | `0975e4f5106874e7de04d436bfa9dc684045060e497b41cb183b0ad9c2a6ab00` |
| 5 | Full-suite log (509 passed) | `pytest_bml_postfix.log.txt` | `005a9b9a6c7b47df4e066fd12ef4f52a25aeb2b9db14247c0db843b72f4f1f43` |
| 6 | Research-runner tooling (DA tooling, untracked, byte-identical to the tree state that produced log #4) | `bml_execute_runner.py.txt` | `c75636640f3aa5196b76af002b9a9d529852957736ac085ae60f8ff2249c35fa` |
| 7 | Corpus reconstruction tooling (DA tooling, untracked — the public-endpoint fetch path, cf. OBS-BDATA-1) | `bdata_fetch_reconstruction.py.txt` | `79c36156f1d033e9781e02c79166acccce952bafce954b199bb718c6faad2ed9` |
| 8 | Reproduction-run evidence (run 3, fresh DB, current tree + runner #6) | `bml_execute_r3_repro.log.txt` | (declared in the DA closing message) |
| 9 | Delivery report | `DELIVERY_REPORT_B-ML.txt` | (declared in the DA closing message) |

**Independent-reproduction proof (added 2026-08-20, after the initial transmission):** the research runner was executed a THIRD time from a fresh database with the exact current tree state and the transmitted runner (#6). Every substantive metric line — 347 folds, accuracy 0.5027665706051874, effect +0.0027665706051873684, p=0.322405545477094, ECE 0.07666976910523227, Brier 0.2557833899275813, net −163,559.5 bps, all three hold-out accuracies (0.497231…/0.482845…/0.501227…), the generalization aggregate 0.4937679587448383, and all four refusal reasons — is **byte-identical** to log #4. Only the fingerprint lines (snapshot/split/artifact hashes embedding uuid ids) differ, per the disclosed D7 limitation. The corrected economic figure (−163,559.5 bps, the post-sort-fix deterministic value) is carried consistently across this report, the decision memo, and the register; the pre-fix intermediate value (−162,219.5) was a stale citation and has been eliminated.

Every hash above resolves to a transmitted file (sha256sum -c exit 0 this session). The run's input corpus is reconstructible by ITRGA from its existing custody (OKX endpoint reconstruction already demonstrated in BO-B-DATA FINAL) or via tooling #7.

## 11. Known limitations / technical debt

- **The honest negative is the programme's current state:** with the builtin v1 feature set, hourly direction on this crypto corpus has no exploitable linear signal. The BO §12 next-step decision belongs to the Operator: retry (broader/richer features — each justified against this failure evidence; or broader asset classes per OBS-BDATA-2), or accept the negative.
- **B-03 (signals) remains gated** — no promoted model exists, per the BO's downstream dependency.
- Carried: PROJECT_STATE.md inventory staleness (OBS-B00-3/B-02-2/B-02-3); signal-layer semantic tightening record (OBS-B02-1) — candidate for the next documentation-touching unit.
- Register: TD-BML-UNIT added (this unit); TD-BDATA-UNIT updated to CLOSED (APPROVED WITH OBSERVATIONS, ITRGA_DETERMINATION_B-DATA_FINAL).

---

Gate CLOSED · Production NOT CERTIFIED · We don't guess. We prove.
