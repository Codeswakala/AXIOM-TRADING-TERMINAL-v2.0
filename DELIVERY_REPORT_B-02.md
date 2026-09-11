# DELIVERY REPORT — BO-B-02
## ML Research Machinery Executed + Substantive-Threshold Gate

| Item | Value |
|---|---|
| Build Order | `BO-B-02` (Operator directive of 2026-08-19: "authorized") |
| Predecessors | BO-B-00 APPROVED-WITH-OBS · BO-B-01 APPROVED-WITH-OBS (CA-B01-1 binding here) |
| Implementer | AXIOM Development Authority (DA) |
| Reviewer | ITRGA — determination pending |
| Date | 2026-08-19 |
| Governance Gate | CLOSED (unchanged) · Production NOT CERTIFIED (unchanged) |

---

## 1. Claimed scope vs. this Build Order

| BO requirement | Delivered | Where |
|---|---|---|
| B-02.1 lifecycle executed (pre-register→approve→train→validation→calibration→economic→generalization→eligibility) | Executed end-to-end over the B-01 synthetic corpus (dev DB) AND pinned as tests that run the full chain | §3, §5, `b02_execute_r1.log` |
| B-02.1 every report carries pipeline_validation tier + truthful data class | Tier label on experiment notes, artifact notes, and all four report notes (persisted); corpus is `synthetic` end-to-end | §3 |
| B-02.1 honest NOT-eligible decision recorded | Gate returned eligible=False with 3 threshold reasons; promotion refused with the same reasons; recorded in runner output | §4 |
| B-02.2 threshold framework documented (ADR) | `backend/docs/SUBSTANTIVE_THRESHOLD_FRAMEWORK.md` — 4 gates, numeric criteria per gate | §5 |
| B-02.2 gate enforces thresholds in code + new rejection reasons | `GovernedModelEligibilityGate.evaluate()` checks `STATISTICAL_THRESHOLD_NOT_MET`, `CALIBRATION_THRESHOLD_NOT_MET`, `ECONOMIC_NOT_USABLE`, `GENERALIZATION_THRESHOLD_NOT_MET`; `promote_to_advisory_approved` inherits them as blocking | §6 |
| B-02.2 baseline expected to fail — failure recorded, not overridden | Dev-DB run: 97 folds, accuracy 0.5134, effect +0.0134 (<0.05), p=0.239, Brier 0.2499 (>0.20), net −11,524 bps → 3 threshold refusals; nothing overridden | §4 |
| B-02.3 generalization as distinct governed research question | Report records its own domain scope (trained forex/H1/trend, hold-out crypto/H1/trend), hold-out separation, independence from prior closed work | §7 |
| §7 calibration-probability gap disclosed + addressed | Baseline extended with labeled degenerate training-prior probabilities (`PROBABILITIES_ARE_DEGENERATE`); disclosure below | §7 |
| §3 exclusions honored | No promotion of any model (the gate refused it); no skill/viability/validity claims; no real data fabricated; no new model families; no inference/signals/alerts work; no assistant/frontend/gate/actuation changes; no governance-document modification (ADR is new, not an amendment); no repo publication | — |
| §6 allowed files honored | Changes confined to `ml/models/*`, `trading_intelligence/inference/service.py`, `tests/**`, `docs/**`; dataset/features consumed read-only, guards not weakened | §2 |
| §9 CA-B01-1 transmission manifest | §12 — every declared artifact mapped to transmitted filename + hash, mechanically verified | §12 |

## 2. What changed (files + SHAs + chain position)

Patch artifact: **`b02.patch.txt`** — sha256 `d5e4a3c876c0bff826cc05f3e9dd58a3f9382607df3bc5a93acbf253a035b1fe`
- Applies clean (`git apply --check` exit 0) onto the verified 20-element chain over baseline `34f4c62`, in a pristine clone, as the **21st chain element**; post-apply, all 8 files byte-identical to the DA workspace (cmp-verified); clone-side B-02/gate/guardrail/harness tests 30/30, ruff clean.

| File | Content SHA-256 |
|---|---|
| `backend/docs/SUBSTANTIVE_THRESHOLD_FRAMEWORK.md` (new) | `381823cf21e13b24164a24042dcfab88a6a840bc2930c1d8bdf6a51180b63163` |
| `backend/app/trading_intelligence/inference/service.py` | `25f107129d0c48753f4a4850a75de02bf12ece649d514a62d5dc4d57366d9234` |
| `backend/app/ml/models/baseline.py` | `6632684be6f514e8520c49444d2d7bd7d2e126f059c5951b268e50bf5f4b69ad` |
| `backend/app/ml/models/harness.py` | `9bd5f2d664622d8e1f92e7fe75f1948d9342196cb5e4ea0f106fe74272a5aace` |
| `backend/tests/test_b02_threshold_gate.py` (new) | `1ca4fb43fade97ce2a8dd23e1bddea75ed1798eec7a820ca1c26e7d92aca65aa` |
| `backend/tests/test_b02_lifecycle.py` (new) | `4af8077d56ffa456b31ed887f338aaee86c8c5f8371f7a26514946373929e7c6` |
| `backend/tests/test_live_inference_gate.py` (fixture churn) | `e9d19cbcf4fa2f97ebdb9df34335480f888455f6288021324593d2b3a598d11c` |
| `backend/tests/test_signal_guardrails.py` (3 tests churned) | `a8e978ba1d9546fbba44300c805a0eb957201a9856fb95b99be2cb91e99c5afc` |

## 3. Experiment + model + reports produced (tier and data-class labels)

Dev-database run (`b02_execute_r1.log`), over the BO-B-01 synthetic corpus (source `synthetic`, snapshot `ds-b01-forex-eurusd`, 2,000 feature rows):

| Artifact | Facts |
|---|---|
| Experiment | `exp-b02-eurusd-baseline` — draft → pre_registered → **approved** by `b02-operator-approver`; notes carry `pipeline_validation tier · synthetic corpus · no research conclusion` |
| Model artifact | `baseline-exp-b02-eurusd-baseline` — status `research_only`; train/val/test accuracy ≈ 0.509/0.520/0.511 (the majority-class rate — no skill, honestly recorded) |
| Validation report | 97 walk-forward folds; accuracy 0.5134; effect +0.0134; p=0.239 |
| Calibration report | ECE 0.0 (degenerate prior equals base rate — mechanically correct, no skill); Brier 0.2499; base_rate 0.4882 |
| Economic report | verdict `economically_unusable`; net −11,524 bps under the full six-class cost model |
| Generalization report | trained_on forex/H1/trend; hold-out crypto/H1/trend; aggregate accuracy 0.5 |

All four reports carry the tier label in their persisted `notes` (machine-set by the runner; asserted by the lifecycle test). No report states or implies any research conclusion.

## 4. Honest eligibility evaluation (decision + reasons)

```
[b02] eligibility: eligible=False
[b02]   reason: STATISTICAL_THRESHOLD_NOT_MET
[b02]   reason: CALIBRATION_THRESHOLD_NOT_MET
[b02]   reason: ECONOMIC_NOT_USABLE
[b02]   reason: NOT_ADVISORY_APPROVED
[b02] promotion refused (expected): PROMOTION_LINEAGE_INCOMPLETE:STATISTICAL_THRESHOLD_NOT_MET,CALIBRATION_THRESHOLD_NOT_MET,ECONOMIC_NOT_USABLE
```

The majority-class baseline failed exactly as the BO expected — for the right, explicit, threshold-level reasons — and the failure is recorded, never overridden, never hidden. (Generalization passed its floor: hold-out 0.50, degradation 0.0134 ≤ 0.10 — correctly no generalization reason.)

## 5. Substantive-threshold framework (ADR)

`backend/docs/SUBSTANTIVE_THRESHOLD_FRAMEWORK.md` (BINDING). Numeric criteria as proposed by the DA:

| Gate | Criteria |
|---|---|
| Statistical | `effect_size.value ≥ 0.05` · `p_value ≤ 0.05` · `folds ≥ 3` · `Σ test_count ≥ 300` |
| Calibration | `ECE ≤ 0.10` (warning threshold 0.15 stays a warning, not a pass) · `Brier ≤ 0.20` |
| Economic | `verdict == economically_usable` · base scenario lists all six cost classes with non-negative values |
| Generalization | `validation_accuracy − holdout_accuracy ≤ 0.10` · `holdout ≥ 0.50` |

Fail-closed rule: malformed, unparsable, or absent values inside a PRESENT report → the corresponding `*_THRESHOLD_NOT_MET`. Threshold passage is necessary, not sufficient (experiment approval, lineage, tier rule still apply).

## 6. Gate-enforcement evidence

- `test_b02_statistical_threshold_not_met` / `test_b02_calibration_threshold_not_met` / `test_b02_economic_not_usable` / `test_b02_generalization_threshold_not_met` — one pin per rejection reason.
- `test_b02_malformed_report_fails_closed` — a present-but-malformed report withholds (no silent bypass).
- `test_b02_promotion_blocked_by_thresholds` — `promote_to_advisory_approved` raises with the threshold reason in the message.
- `test_b02_gate_passes_all_thresholds_and_promotes` — positive machinery proof: a model whose reports genuinely pass every threshold is eligible and promotable (the gate is threshold-driven, not permanently closed).
- `test_b02_lifecycle_executes_and_eligibility_is_honestly_negative` — the full chain runs and the negative decision is explicit.
- Fail-first: `b02_probe_prefix.log` — pre-fix, the module could not even collect (`derive_candle_labels` did not exist; neither did `predict_proba` or the threshold reasons).
- **Full backend suite: 500 passed, 1 warning, 138.05s** (489 prior + 11 new; 0 failed/skipped) — `pytest_b02_postfix.log`. (One precision note: the 500-pass run predates a whitespace-only import reorder in `harness.py`; the affected modules were re-executed green after the reorder, and the clone-side 30/30 run covers the final content.)

## 7. Calibration-probability gap + generalization governance

- **Gap disclosed as required (§7):** the majority-class baseline emits no skill probabilities. Resolution: `predict_proba()` now emits the **degenerate training prior** (constant class frequencies), with `PROBABILITIES_ARE_DEGENERATE = True` and a per-row `degenerate_prior=True` label — calibration over these values measures the prior, not the model, and the Brier threshold (0.20 < the balanced-class null 0.25) still rejects it. Nothing was skipped; nothing was fabricated.
- **Generalization governance:** the hold-out report records its own domain scope, its hold-out separation (crypto vs forex training domain — `MARKET_HOLDOUT_LEAKAGE` would have refused overlap), and its independence from prior closed work. It does not reopen or alter any closed outcome.

## 8. Standing-dependency note (§8)

The substantive ML path (real model, real conclusions, any `advisory_approved` promotion) requires **real historical market data**, which does not exist in this project. Per the BO, this is an Operator decision — **Option R1** (authorize real-data acquisition in a future governed unit) or **Option R2** (accept that the substantive path, and therefore B-03 signal production with an eligible model, remains blocked until real data exists). The DA substituted nothing and promoted nothing. **B-03 cannot proceed to a promoted-model state without this decision.**

## 9. Deviations register

- **D1 — Spec-driven test churn (three files, disclosed in full).** (a) `test_live_inference_gate.py::_eligible_artifact` fixture upgraded to threshold-passing report values (accuracy 0.72/effect 0.22/p 0.001/3 folds/450 test rows; ECE 0.05/Brier 0.18; economically_usable + full cost model; holdout 0.70). Reason: BO §11 requires the threshold gate not break existing eligibility tests, while the BO §2.2 semantics make the old fixture's promotion (with `economically_unusable` economics) forbidden; the fixture was upgraded to the new spec, and the promotion-success test now proves a genuinely threshold-passing promotion. (b) `test_signal_guardrails.py` — three tests pinned the W3-U03 "warning" tier for post-promotion calibration/economic degradation; under BO-B-02 those degradations are now **hard-withheld at emit** with explicit threshold reasons (the BO's "evaluate must reject" wording). The three tests were re-pinned to the superseding semantics: ECE 0.30 → `withheld` + `CALIBRATION_THRESHOLD_NOT_MET`; economically-unusable → `withheld` + `ECONOMIC_NOT_USABLE` (verdict still visible on the withheld record); the "cannot be forced to emitted" property is preserved and strengthened. **Consequence disclosed:** the signal layer's warning tier for calibration/economic degradation is now unreachable for threshold-failing values by design — the warning tier remains for values within thresholds. No test was deleted; no assertion was weakened; every changed test got stricter.
- **D2 — Harness labeling + warm-up handling (in-scope "labeling" per BO §6).** `train(labels_from_candles=True)` derives forward labels from candle closes (no look-ahead; final bar excluded); feature rows with warm-up `None` values (rolling lookback) are excluded from matrices, never fabricated.
- **D3 — SQLite-naive timestamps.** `derive_candle_labels` coerces naive `as_of` values to UTC before comparison (dev-DB reality; Postgres would store aware values). Fail-honest: unresolvable rows are excluded.
- **D4 — Runner tooling untracked.** `scripts/b02_execute.py` is DA evidence tooling (precedent B-00 D6 / B-01 D2); the lifecycle test in the patch reproduces the entire chain in CI.
- **D5 — No schema migration.** Tier labels ride existing `notes` fields; no new tables or columns.
- **D6 — The 500-pass full-suite run predates a whitespace-only import reorder** (see §6); the reordered content is covered by the post-reorder module re-run (10/10) and the clone-side run (30/30).

## 10. Test evidence (executed)

| Run | Result | Log |
|---|---|---|
| B-02 fail-first probe (pre-fix) | collection error — mechanisms absent | `b02_probe_prefix.log` |
| B-02 gate + lifecycle (post-fix) | 11 passed | in `pytest_b02_postfix.log` |
| Full backend suite | **500 passed, 1 warning, 138.05s** (0 failed/skipped) | `pytest_b02_postfix.log` |
| Clone-side (applied patch content) | 30 passed (gate 9 + lifecycle 2 + W3 gate 10 + guardrails 6 + harness 3), ruff clean | `b02_applycheck_transcript.txt` |
| Dev-DB research run (Level I) | full lifecycle + honest NOT-eligible | `b02_execute_r1.log` |

## 11. Known limitations / technical debt

- The substantive path is **blocked on real data** (Operator R1/R2 — §8). Until then, every model is a pipeline-tier machinery artifact and the gate will refuse promotion of anything the DA can currently produce — by design.
- `PROJECT_STATE.md` test inventory remains stale (carried OBS-B00-3).
- Fixture-convention source labels (`sample:*` → AUTHORITATIVE) remain (carried OBS-B01-2) — a future unit should tighten.

## 12. TRANSMISSION MANIFEST (CA-B01-1 — binding; mechanically verified before submission)

| # | Declared artifact | Transmitted filename | sha256 | Verified |
|---|---|---|---|---|
| 1 | B-02 patch (chain position 21) | `b02.patch.txt` | `d5e4a3c876c0bff826cc05f3e9dd58a3f9382607df3bc5a93acbf253a035b1fe` | ✓ on disk |
| 2 | Apply-check transcript (fresh, pristine clone) | `b02_applycheck_transcript.txt` | `989d42dfcd14f9b6c0bcd3598e23e76de4822e3ba27eac1c939928c51562cdce` | ✓ on disk |
| 3 | Fail-first probe log | `b02_probe_prefix.log.txt` | `ab79dc2dd67378412ddf2b907e0069a84a688d88d51f4dea5569c82018067488` | ✓ on disk |
| 4 | Dev-DB research-run log (Level I) | `b02_execute_r1.log.txt` | `f02de74d2dedaffd0f0f4e23f030cd98efd587ed58b9489e614bee2b82c34fbb` | ✓ on disk |
| 5 | Full-suite log (500 passed) | `pytest_b02_postfix.log.txt` | `d16782386f2f3529415a63ee907bd2fbe27b5b5af95dd8bbe651ee62dafab84f` | ✓ on disk |
| 6 | Delivery report | `DELIVERY_REPORT_B-02.txt` | (see transmission) | ✓ on disk |

Every declared hash above resolves to an actual file in `/home/user/b02_transmission/` (sha256sum -c exit 0 this session). Per-file content SHAs in §2. No "ATTACHED" claim exists for anything not transmitted. **All six artifacts are newly transmitted this delivery.**

---

Gate CLOSED · Production NOT CERTIFIED · We don't guess. We prove.
