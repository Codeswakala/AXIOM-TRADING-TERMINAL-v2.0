# ITRGA INDEPENDENT TECHNICAL REVIEW — W2-U06

## ML Research: Baseline Market-Agnostic Model Harness (first model unit)

**Review ID:** ITRGA-REVIEW-W2-U06
**Unit:** W2-U06 · **Wave:** 2 — ML Research Framework · **Unit:** 06 (first model-touching unit)
**Reviewer:** ITRGA · **Date:** 2026-07-14
**Inputs reviewed:** `DELIVERY_REPORT_W2-U06.md`; operator console transcript (`operator results.md`, 1010
lines; Windows/PowerShell + PostgreSQL 18, Python 3.14.6); cross-checked against `BUILD_ORDER_W2-U06.md`,
`07_ML_SPEC`, D-W2-001, and the W2-U01–U05 chain.
**Motto:** *We don't guess. We prove.*

---

## 0. VERDICT

> ## ✅ **APPROVED** — Platform **v0.18.0** — first model trained, on governance rails
>
> W2-U06 delivers AXIOM's first model — a deliberately-minimal, **research-only, pure-Python majority-class
> baseline** — and proves, on **operator-run, target-platform Level-I evidence**, that a model can *only* be
> trained on honest, pinned, approved, identity-free data. **All four headline refusals are captured by
> name** (`EXPERIMENT_NOT_APPROVED`, `UNRESOLVED_PIN`, `IDENTITY_IN_MODEL_INPUT`, `NON_TEMPORAL_SPLIT`);
> the **compatibility risk is eliminated** (pure-Python, zero new ML wheels on Py3.14.6); a **research-only
> model artifact is persisted on PostgreSQL** (committing-script proof, `(1 row)`); retrain is
> **reproducible** (same artifact hash/metrics); and the baseline metric is reported **honestly**
> (`validation_accuracy: 0.0`, with an explicit "proves harness mechanics, not predictive skill" note).
> Clean PG migrate to `20260714_0010`, **pytest 135 passed** (127→135), ruff clean, frontend 16 + build,
> CI green on PG, parity smoke green. **No CRITICAL, no HIGH, no residuals owed.**

**Why clean APPROVED:** the unit's purpose — prove training *machinery under governance*, not skill — is
fully met and *proven by refusals*. Nothing is asserted where it should be shown; the DA even reported a
weak baseline honestly rather than dressing it up. Per proportionality (R13), a clean approval is correct.

---

## 1. Evidence Hierarchy Assessment (R2)
**Level-I (operator-run, Windows + PostgreSQL)** for every material claim, with named `-vv` captures and a
committing-script persistence proof. Seventh consecutive first-submission target-proven unit.

| Tier | Present? | Notes |
|------|----------|-------|
| Level-I — operator-run on Windows + PostgreSQL | ✅ | compat spike on Py3.14.6, pytest 135 on PG, 6 named `-vv` tests, committing-script persisted artifact, greps, CI, smoke |
| Level-II — DA sandbox (SQLite) | ✅ | 135/16 — corroborating |
| Level-III — source/ADR | ✅ | ADR-026; baseline/harness/errors files enumerated |
| Level-IV — report claims | ✅ | Present; not the basis for approval (R1) |

---

## 2. Mandatory §5 Evidence — Line-by-Line Verification

| # | Required (Build Order §5) | Verdict | Basis |
|---|---------------------------|---------|-------|
| 1 | **Compatibility spike** (staged, first) on Win/Py3.14.6 | ✅ **PROVEN (risk eliminated)** | `python --version → 3.14.6`; `MajorityClassBaseline` imports + fits; `BASELINE_FRAMEWORK: pure-python-majority-baseline`, `NO_EXTERNAL_ML_DEPENDENCY: True`. **No new ML wheel adopted** — the numpy/sklearn Py3.14 risk is *removed*, not deferred-unproven. Legitimate spike outcome. |
| 2 | Operator test console: pytest ≥127+new, 0 failed; vitest 16; ruff; tsc/build | ✅ **PROVEN** | `135 passed … in 62.25s`; `All checks passed!`; `Tests 16 passed (16)`. Backend 127→135 (+8). |
| 3 | Migration on PostgreSQL, new head | ✅ **PROVEN** | `Running upgrade 20260713_0009 -> 20260714_0010, W2-U06 model artifact registry fields` → `20260714_0010 (head)` on `PostgresqlImpl`. |
| 4 | **Refusals captured `-vv` by name, reason codes** | ✅ **PROVEN** | `test_train_without_approved_experiment_refused`, `test_unresolved_pin_refused`, `test_identity_in_model_input_refused`, `test_non_temporal_split_refused` — all **PASSED** (lines 287–290, dedicated `-vv`), reason codes per Delivery Report §7. |
| 5 | End-to-end train on an **approved, pinned** experiment → artifact w/ research-only status + experiment link | ✅ **PROVEN** | `test_baseline_model_trains_approved_pinned_experiment PASSED`; committing script trained on `operator-model-harness-approved-exp` → `MODEL_STATUS: research_only`. |
| 6 | Reproducibility: retrain same exp+seed → same hash/metrics | ✅ **PROVEN** | `test_reproducible_retrain_same_artifact_hash_and_metrics PASSED` (named `-vv`). |
| 7 | **Persisted-PG proof (committing script)** | ✅ **PROVEN** | Heredoc `… | python -` → `psql SELECT … FROM model_artifacts` → **`(1 row)`**: `status research_only / research_status research_only / dataset_content_hash / split_manifest_hash / artifact_hash a8f6a7fb… / note "…not predictive skill"`; `audit_events` (model_artifact) `(1 row)`. |
| 8 | Identity-exclusion + no-live-signal evidence | ✅ **PROVEN** | Two shown greps → **empty**: `symbol_id\|one_hot_symbol\|symbol_identity` over `app\ml`, and `model/signal\|predict\|inference\|live_signal` over `app\api\routes`. |
| 9 | CI green on PostgreSQL, fail-closed | ✅ **PROVEN** | `==> Local CI equivalent complete` (orchestrated `local_ci.sh` on PG). |
| 10 | Parity smoke (no regression) | ✅ **PROVEN** | `WS-TICKET status: 200`; `persist_errors: 0`. |
| 11 | Confidence + **honest metric** | ✅ **PROVEN (exemplary)** | `METRICS: train 0.667 / validation 0.0 / test 1.0` reported plainly + `baseline_note: "Majority-class baseline; proves harness mechanics, not predictive skill."` No cherry-picking. |

**Independently verified:** the +8 delta matches the 8 named harness tests (incl. the two structural tests —
`..._no_external_ml_dependency`, `..._no_live_signal_or_model_api_endpoint_added` — corroborated by the two
empty greps). The 135-passed run is post-migration on the PG-configured environment.

---

## 3. Governance Envelope — Compliance

| Constraint (Build-Order §2) | Verdict | Basis |
|-----------------------------|---------|-------|
| ❌ No training except via APPROVED, hash-pinned experiment | ✅ Upheld | `..._without_approved_experiment_refused` + `..._unresolved_pin_refused` PASSED; e2e train used an approved pinned exp. |
| ❌ No leakage / no non-temporal split | ✅ Upheld | `..._non_temporal_split_refused` PASSED; harness consumes W2-U04 manifest as-is. |
| ❌ No symbol identity at model input (D-W2-001) | ✅ Upheld | `..._identity_in_model_input_refused` PASSED + identity grep empty. |
| ❌ No execution/broker/live signal | ✅ Upheld | no-live-signal grep empty; no prediction/inference route; `research_only` artifact; broker tests still green in 135. |
| ❌ No fabricated / cherry-picked results | ✅ Upheld | weak metrics reported honestly incl. `validation_accuracy: 0.0`. |
| ❌ No non-reproducible training | ✅ Upheld | reproducible-retrain test PASSED (seed 42). |
| ❌ No untested dependency | ✅ Upheld | pure-Python; `no_external_ml_dependency` test + zero `requirements.txt` ML add. |
| ❌ No secrets/PII; no DB reach-around | ✅ Upheld | no token in transcript; artifact via harness. |
| ❌ No regression (Wave-0/1 + W2-U01–U05) | ✅ Upheld | 135 passed incl. all prior suites/guards/registry; CI + smoke green. |
| ✅ Preserve prior chain + hardening | ✅ Upheld | guard→features→snapshot→split→experiment→model all intact. |

---

## 4. Findings (classified — R8)

**No CRITICAL. No HIGH. No MEDIUM. No residuals owed.**

- **OBSERVATION (informational, NOT a finding) — degenerate small-sample metrics.** `test_accuracy: 1.0`
  and `validation_accuracy: 0.0` on a majority-class baseline over tiny synthetic splits are **small-sample
  artifacts, not leakage or skill** — a test fold that happens to be single-class trivially scores 1.0.
  The DA labelled them correctly ("not predictive skill"). Real metrics require real data + the W2-U07/U08/
  U09 validation suites. No action.
- **OBSERVATION — compatibility spike satisfied by *avoidance*.** Choosing a pure-Python baseline
  *eliminates* the numpy/sklearn Py3.14 risk for now; it does **not** discharge it for future model
  families. **The first unit that adopts numpy/scikit-learn (or any wheel dependency) still owes the
  install/import/smoke spike on Windows+Py3.14.6** as its own gate (carried to W2-U07+ where relevant).
  Recorded as a standing note, not owed by W2-U06.
- **RECOMMENDATION (W2-U07):** the statistical-validation unit should run on a **realistically-sized**
  dataset so metrics are meaningful, and must keep the leakage/temporal-split guards active — this is where
  honest *skill* numbers (with uncertainty) first become the point.

No finding withholds or qualifies approval.

---

## 5. Required Actions
**None owed.** Standing note (not blocking): the wheel-compatibility spike is still owed by the first unit
that adopts a compiled ML dependency.

---

## 6. Evidence Confidence Statement (R6 — no fabricated percentages)

**Confidence in this APPROVAL: HIGH.** Every claim is backed by operator-run Windows + PostgreSQL Level-I
evidence I verified directly — a Py3.14.6 compat spike (pure-Python, no wheels), `pytest 135 passed` on PG,
four refusals captured by name, an end-to-end train on an approved pinned experiment, a reproducible
retrain, a persisted research-only model artifact on PostgreSQL via committing script, two empty
containment greps, CI green on PG, and a green parity smoke — with the baseline metric reported honestly.
No residual, no contradiction. HIGH without caveat.

---

## 7. Commendation (earned)

Seventh consecutive first-submission target-proven unit, and a textbook first-model delivery: the DA (a)
**eliminated** the platform risk rather than gambling on wheels (pure-Python baseline — exactly the
conservative sequencing the plan §4.2 called for); (b) proved the model can *only* train on-governance via
four named refusals; (c) persisted the artifact on PostgreSQL with the committing-script method learned from
the W2-U05 C-2 correction; and (d) — most importantly for scientific integrity — **reported a weak baseline
honestly** (`validation_accuracy: 0.0`, "not predictive skill"), the exact anti-cherry-picking behaviour R18
demands. This is how the first model should arrive: humble, honest, and on rails.

---

## 8. Disposition

- **W2-U06: APPROVED.** Platform **v0.18.0**.
- **Residuals: NONE owed.** Standing note: wheel-compat spike owed by the first compiled-ML-dependency unit.
- **Gate posture unchanged:** research/advisory only — no live signals (Wave 3), no execution (Wave 6),
  broker gate CLOSED. The model artifact is `research_only` and cannot emit signals.
- **Next:** ITRGA recommends authorizing **W2-U07 = Statistical Validation Framework** (accepted plan §10;
  `07_ML_SPEC` §Statistical Validation) — walk-forward, out-of-sample, time-series CV, bootstrap, confidence
  intervals, effect size, significance, **uncertainty reported (not just point estimates)** — run on a
  realistically-sized dataset, guards active, and carrying the wheel-compat spike **if** it adopts numpy/
  scipy/statsmodels. The DA does not self-authorize W2-U07 or open the broker gate. Await operator direction
  + a new Build Order.

---

*ITRGA — The first model is trained, and it could only ever be trained the right way: through an approved,
hash-pinned experiment, on reproducible, leak-free, symbol-blind data, its weak baseline reported without
flinching. No skill was claimed and none was needed — the point was to prove the rails hold, and they held.
Now the validation frameworks can turn honest data into honest, uncertain numbers. We don't guess. We
prove.*
