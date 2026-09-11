# DELIVERY REPORT — BO-B-ML2
## Predictive Research Iteration: Feature & Target Expansion Under Multiple-Comparison Discipline

| Item | Value |
|---|---|
| Build Order | `BO-B-ML2` (Operator directive of 2026-08-20: "continue with the predictive track") |
| Predecessors | B-00 · B-01 · B-02 · B-DATA · B-ML (all APPROVED WITH OBSERVATIONS) · ITRGA Reconciliation (B-03 = predictive signals only) |
| Implementer | AXIOM Development Authority (DA) |
| Reviewer | ITRGA — determination pending |
| Date | 2026-08-20 |
| Governance Gate | CLOSED (unchanged) · Production NOT CERTIFIED (unchanged) |

**Prior-observation discipline applied (OBS-BML-1/OBS-BML-2):** every numeric figure in this report was transcribed mechanically from the executed log (`bml2_execute_r1.log`, sha256 `ec1a133a…`); the fail-first probe log is transmitted with the set and its hash is verified below. No declared-but-untransmitted artifact.

---

## 1. Claimed scope vs. this Build Order

| BO requirement | Delivered | Where |
|---|---|---|
| §1.1 one pre-registered primary hypothesis, plan hash, BEFORE training | ✓ 3 hypotheses pre-registered + approved with plan hashes + timestamps printed **before any training** (runner log lines 1–7) | §3 |
| §1.2 secondaries labeled; not reported as pre-registered | ✓ S1/S2 carry "labeled exploratory" in their registry notes, plan records, and report rows | §3 |
| §1.3 bounded budget (1 primary + ≤3 secondary) | ✓ 3 total (1 primary + 2 secondary) | §3, §8 |
| §1.4 multiple-comparison disclosure | ✓ §8 — primary evaluated alone at α=0.05 (stated); secondaries uncorrected + labeled inflation-prone | §8 |
| §1.5 no post-hoc selection | ✓ pre-registration hashes fixed before results; the primary was NOT swapped (it fails; the secondaries also fail) | §3, §7 |
| Phase 1 features ≤12, causal, market-agnostic, justified | ✓ 11 features in the primary set; 8 new, each justified §4; warm-up-None discipline; no identity | §4 |
| Phase 2 target pre-registered, no post-hoc switch | ✓ Primary: direction@H1 (unchanged target); S2 (labeled secondary): magnitude target — disclosed as reformulation, not substitution | §3, §5 |
| Phase 3 full lifecycle | ✓ 3× walk-forward (346/346/343 folds over 52,560 real bars), 3× calibration, 3× economic (six-class crypto costs), 3× cross-instrument generalization (unseen XRP/ADA/DOGE) | §6 |
| Phase 4 honest outcome | ✓ **THREE honest negatives; zero promotions** — every hypothesis refused by the unchanged fail-closed gate | §7 |
| §3 exclusions | No threshold-failing promotion; no relabeling; no p-hacking/post-hoc switching; no new dependency; no live/broker/actuation; no frontend/assistant/intelligence; no governance-document changes; no repo publication | — |
| §9 CA-B01-1 relay-accurate manifest | §11 — code-only set; corpus already in ITRGA custody | §11 |

## 2. What changed (files + SHAs + chain position)

Patch artifact: **`bml2.patch.txt`** — sha256 `1649e26f66bda3107c3e2f0d1e4687b9103b09f7835e46b7eff14cdf678cadb3`
- Applies clean (`git apply --check` exit 0) onto the verified 23-element chain over baseline `34f4c62`, in a pristine clone, as the **24th chain element**; post-apply, all 4 files byte-identical to the DA workspace (cmp-verified); clone-side B-ML2 + affected sets 26/26, ruff clean.

| File | Content SHA-256 |
|---|---|
| `backend/app/ml/features/definitions.py` | `1efd3c793a9a70dfda2e8d76e1f5243d4fd2f55d36346f6bf89e27c36196cb02` |
| `backend/app/ml/models/harness.py` | `12f0dac0a42fb8e5a2e4e010daf4faa9aaa1db37b814d647f7081c492d7bb84a` |
| `backend/app/ml/models/logistic_regression.py` | `30f684a54827b6d6268fb76ef1497020cad68821e2987d0c6e848bfb364712a4` |
| `backend/tests/test_bml2_features.py` (new) | `69d7ef0be214049aca022ce92e9c978334a333e2480f6872edade3d8c1b1d8e1` |

## 3. Pre-registration record (Level I — before any training)

```
[bml2] PRE-REGISTERED PRIMARY          exp-bml2-primary        plan_hash=d97e59ef93dd4b50fef9238250c3f9ab7fa6a94e05a39779aa9d38f3d1474083 approved_at=2026-08-20 14:27:31.412846+00:00
[bml2] PRE-REGISTERED SECONDARY-S1     exp-bml2-secondary-s1   plan_hash=fd8bd4f36bd5467bd515f5a3779df983d4e1635db763c9a2ccfd7076bba31808 approved_at=2026-08-20 14:27:31.420957+00:00
[bml2] PRE-REGISTERED SECONDARY-S2     exp-bml2-secondary-s2   plan_hash=cc18c577048374d38ef6088dadf94c013e846bd2265902df17fd28a81541e810 approved_at=2026-08-20 14:27:31.428794+00:00
[bml2] hypothesis budget: 1 primary + 2 secondary (bound: 1+3). Primary is the determination basis.
```

- **PRIMARY (the determination basis):** direction@H1 · full v1+v2 feature set (11 features) · logistic regression (seed 42) · temporal walk-forward. Hypothesis: "The expanded feature set contains directional structure absent from the v1 set."
- **SECONDARY-S1 (labeled exploratory):** direction@H1 · ablation subset {return_1, range_pct, rolling_return_3, atr_norm_14, structure_bos_rec} (5 features).
- **SECONDARY-S2 (labeled exploratory):** magnitude target — next-bar range above the trailing 200-bar median · full v1+v2 set.
- The reported primary is the pre-registered primary (same plan hash); no post-hoc swap occurred.

## 4. Feature additions + per-feature justification

| Feature | ML Spec basis | Deficiency addressed | Causality / no-identity |
|---|---|---|---|
| `atr_norm_14` (volatility) | §Feature Engineering — normalized volatility | v1 has only the instantaneous range; no rolling volatility regime | True ranges of bars ≤ t only; price-normalized; no identity |
| `roc_12` (momentum) | §Momentum features | v1 momentum is the 3-bar rolling return only | close[t]/close[t−12] — no future bars |
| `ema_dist_20` (trend) | §Trend/position features | no trend-position state in v1 | EMA over bars ≤ t; normalized by price |
| `bband_pos_20` (volatility/mean-reversion) | §Volatility statistics | no mean-reversion position in v1 | SMA/std over bars ≤ t |
| `vol_change_1` (volume) | §Volume features | no volume dynamics; log-change is scale-free → market-agnostic across instruments | bars ≤ t only |
| `hour_sin`, `hour_cos` (calendar) | §Session features | crypto has documented intraday seasonality; the UTC clock is global, not identity | timestamp known at bar close |
| `structure_bos_rec` (market structure) | BO-B-ML2 §Phase 1 explicit permission — the bridge to the deterministic indicator layer | v1 has no market-structure state | BoS-class breakout recency over bars ≤ t, capped at 200 |

All 8 carry `feature_version="v2"`, `causal=True` (asserted at registration), warm-up windows returning `None` (excluded from matrices, never fabricated — pinned by `test_bml2_v2_features_deterministic_and_warmup_disciplined`). Primary count: 11 ≤ 12 (pinned by `test_bml2_primary_feature_count_within_budget`). Determinism: two full passes over identical input produce identical values (pinned).

## 5. Target choice + rationale

The primary keeps **direction@H1** — the identical target of B-ML — so the retry is a clean feature-iteration comparison against the failure evidence (the BO's justification baseline). The magnitude target is tested only as the labeled secondary S2 (a legitimate reformulation per §Phase 2, disclosed as such, not substituted for the primary).

## 6. Experiment + reports (executed, from `bml2_execute_r1.log`)

Corpus: OKX H1 real corpus (6 instruments), `historical:real`, `research_validation` tier throughout; train BTC+ETH+SOL (52,560 bars), hold-out XRP/ADA/DOGE; feature rows 105,120 (feature_set.v2).

| Measure | PRIMARY | S1 (secondary) | S2 (secondary) |
|---|---|---|---|
| Model metrics (train/val/test) | 0.4999 / 0.4910 / 0.4967 | 0.5085 / 0.4962 / 0.4968 | 0.4676 / 0.4548 / 0.4607 |
| Walk-forward folds | 346 | 346 | 343 |
| Accuracy | 0.5005202312138729 | 0.5011753371868979 | 0.5331389698736638 |
| Effect (floor ≥ 0.05) | **+0.0005202312138729015** | **+0.0011753371868978846** | **+0.033138969873663826** |
| p (ceiling ≤ 0.05) | **0.8527561502731951** | **0.6807830557717602** | 0.00004553490451601022 |
| ECE (≤ 0.10) | **0.20898634813717992** | **0.43844579156170044** | **0.4440267974601218** |
| Brier (≤ 0.20) | **0.3098735886994965** | **0.4582898870483323** | **0.4685363405055726** |
| Economic net bps | **−163,579.5** | **−163,559.5** | **−171,139.5** |
| Hold-out (XRP/ADA/DOGE) | 0.4891 / 0.4864 / 0.4985 | 0.4973 / 0.4828 / 0.5014 | 0.5045 / 0.4927 / 0.5086 |
| Hold-out aggregate (≥ 0.50) | **0.49131575196509053** | **0.49386964014734946** | 0.501953844454217 |

Reports: 3 experiments · 3 model artifacts · 3 validation · 3 calibration · 3 economic · 3 generalization — all carrying the tier label; hypothesis labels persisted in report notes.

## 7. Honest outcome: NOT PROMOTED (all three) — full reasons

```
[bml2] PRIMARY: NOT PROMOTED: PROMOTION_LINEAGE_INCOMPLETE:STATISTICAL_THRESHOLD_NOT_MET,CALIBRATION_THRESHOLD_NOT_MET,ECONOMIC_NOT_USABLE,GENERALIZATION_THRESHOLD_NOT_MET
[bml2] S1:       NOT PROMOTED: PROMOTION_LINEAGE_INCOMPLETE:STATISTICAL_THRESHOLD_NOT_MET,CALIBRATION_THRESHOLD_NOT_MET,ECONOMIC_NOT_USABLE,GENERALIZATION_THRESHOLD_NOT_MET
[bml2] S2:       NOT PROMOTED: PROMOTION_LINEAGE_INCOMPLETE:STATISTICAL_THRESHOLD_NOT_MET,CALIBRATION_THRESHOLD_NOT_MET,ECONOMIC_NOT_USABLE
```

**The scientifically notable result (disclosed plainly):** S2's walk-forward shows a nominally significant p vs the 0.5 null (4.55e-05) — the volatility-clustering structure (current range features genuinely predict next-bar range *regime*) — but its **effect +0.0331 is below the +0.05 floor**, its **probabilities are deeply miscalibrated (ECE 0.444, Brier 0.4685 — worse than the 0.25 balanced null)**, and its **economics are the worst of the three (net −171,139.5 bps)**. The gate refused it for exactly those reasons. This is precisely the multiple-comparison trap the BO anticipated: a "significant-looking" exploratory result that fails every substantive bar — and the fail-closed gate did what it was built to do.

**The primary's verdict, stated without softening:** the expanded 11-feature set finds **no directional structure** — effect +0.00052 (≈100× below floor), p=0.853, Brier 0.3099. Two governed iterations, two feature sets, two targets: hourly crypto prediction from price-derived causal features has no exploitable linear edge on this corpus. The negative is now twice-established.

## 8. Multiple-comparison disclosure (binding)

- **Hypotheses tested: 3** (1 primary + 2 secondary; budget bound 1+3 — met).
- **Correction:** the primary is evaluated alone at **α = 0.05** (stated per §1.4); the secondaries are **uncorrected and labeled inflation-prone** — their nominal metrics may not be interpreted as family-adjusted significance.
- **Primary-basis statement:** the determination basis is the pre-registered primary (plan hash `d97e59ef…`), which fails. No secondary outcome is reported as if pre-registered; no hypothesis was swapped post hoc (pre-registration hashes predate all training lines in the log).

## 9. Test evidence (executed)

| Run | Result | Log |
|---|---|---|
| B-ML2 fail-first probe (against the 23-element chain) | collection error — v2 module absent | `bml2_probe_prefix.log` |
| B-ML2 features (post-fix) | 5 passed | in `pytest_bml2_postfix.log` |
| **Full backend suite** | **514 passed, 1 warning, 140.09s** (509 + 5 new; 0 failed/skipped) | `pytest_bml2_postfix.log` |
| Clone-side (applied patch content) | 26 passed (features + B-ML + W2 sets), ruff clean, apply-check exit 0 | `bml2_applycheck_transcript.txt` |

## 10. Deviations register

- **D1 — Harness per-hypothesis controls.** `PredictiveModelHarness.train()` gained `label_overrides` (custom labels for S2) and `feature_filter` (subset selection for S1) — additive optional parameters; default behavior unchanged (pinned by the existing B-ML suite remaining green). The base harness's `_matrix_and_labels` gained the corresponding filter (None-values still excluded, never fabricated).
- **D2 — Structure feature implementation.** `structure_bos_rec` computes BoS-class breakout recency locally (k=20, capped 200) rather than importing the chart engine's `bos()` — the engine's bar interface is chart-typed; the local computation is deterministic, causal, and functionally the same event class. Disclosed as an implementation choice, not a semantic substitution.
- **D3 — Fold-count variance.** 346/346/343 folds (vs 347 in B-ML) — the v2 warm-up windows exclude slightly more early rows; expected, disclosed.
- **D4 — Runner tooling untracked** (precedent B-00 D6 → B-ML D5): `scripts/bml2_execute.py`; the patch ships features + harness + tests only.
- **D5 — No schema migration, no new dependency.** Feature rows ride the existing `feature_records` table under `feature_set_version="feature_set.v2"`; the logistic model is reused unchanged.

## 11. Transmission manifest (CA-B01-1, relay-accurate)

Corpus CSVs already in ITRGA custody (BO-B-DATA FINAL) — **not re-transmitted**. Code-only set:

| # | Declared artifact | Transmitted filename | sha256 |
|---|---|---|---|
| 1 | B-ML2 patch (chain position 24) | `bml2.patch.txt` | `1649e26f66bda3107c3e2f0d1e4687b9103b09f7835e46b7eff14cdf678cadb3` |
| 2 | Apply-check transcript (pristine clone, 23-chain) | `bml2_applycheck_transcript.txt` | `4f5c7b9bcc81a82584b8db5143b2fb9875cd77685670b349667090ad3774649d` |
| 3 | Fail-first probe log | `bml2_probe_prefix.log.txt` | `e42ffff51f39c9855ad4a200eafef82962ef6c02d1660697c9f30e4fa6011c05` |
| 4 | Research-run log (3 hypotheses + pre-registration + honest negatives) | `bml2_execute_r1.log.txt` | `ec1a133afe0624fc83f1085fef1ce3addbb284794d144ca09329c9e23f29229f` |
| 5 | Full-suite log (514 passed) | `pytest_bml2_postfix.log.txt` | `d6ccc917f268c5b5ef06217424b24424c3999041d896168b5c5fbad9c8a5166b` |
| 6 | Research-runner tooling (DA tooling, untracked) | `bml2_execute_runner.py.txt` | `55946ff3ffc02ca51513f1249d9a2703fea557b8149ca9b4b4bee2fbd02a948b` |
| 7 | Delivery report | `DELIVERY_REPORT_B-ML2.txt` | (declared in the DA closing message — no self-referential hash in the table) |

Every hash above resolves to a transmitted file (sha256sum -c exit 0 this session — OBS-BML-2 discipline: nothing declared that is not in the set).

## 12. Known limitations / technical debt

- The predictive track now has **two governed negative iterations** on hourly crypto data. Per BO §12, the next step is the Operator's decision: further reformulation, broader real asset classes via a new R1-style data order (OBS-BDATA-2), or accepting the predictive track's negative status. **B-03 remains gated.**
- S2's nominal significance is disclosed as uncorrected, exploratory, and substantively failed (effect/calibration/economic) — it must not be cited as evidence of skill.
- Carried: PROJECT_STATE.md inventory staleness; W3-U03 semantic-narrowing record; fingerprint-determinism hardening (D7-class, full row-id determinism).

---

Gate CLOSED · Production NOT CERTIFIED · We don't guess. We prove.
