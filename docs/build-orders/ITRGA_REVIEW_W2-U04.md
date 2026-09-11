# ITRGA INDEPENDENT TECHNICAL REVIEW — W2-U04

## ML Research: Reproducible Dataset Snapshot Builder + Temporal Split Engine

**Review ID:** ITRGA-REVIEW-W2-U04
**Unit:** W2-U04 · **Wave:** 2 — ML Research Framework · **Unit:** 04
**Reviewer:** ITRGA (Independent Technical Review & Governance Authority)
**Date:** 2026-07-13
**Inputs reviewed:** `DELIVERY_REPORT_W2-U04.md`; operator console transcript (`operator results.md`,
Windows/PowerShell + PostgreSQL 18, Python 3.14.6); cross-checked against `BUILD_ORDER_W2-U04.md`,
`07_ML_SPEC`, D-W2-001, and the W2-U01 R-2/R-3 label-horizon/embargo contract.
**Motto:** *We don't guess. We prove.*

---

## 0. VERDICT

> ## ✅ **APPROVED** — Platform **v0.16.0**
>
> W2-U04 delivers the Reproducible Dataset Snapshot Builder and Temporal Split Engine on **operator-run,
> target-platform Level-I evidence**, and **all three headline guarantees are proven by named tests on the
> target**: (1) **build-twice → identical snapshot hash** (reproducibility); (2) **random/shuffled split
> rejected** (`SPLIT_LEAKAGE`) with a deterministic temporal-split hash; (3) **label-horizon crossing
> rejected** (`LABEL_HORIZON_LEAKAGE`) while a correctly-embargoed split passes (the R-2 contract, now
> enforced by the engine). Clean PostgreSQL migrate to head `20260713_0008`, **pytest 119 passed**
> (112→119), ruff clean, frontend 16 + build, and a green parity smoke. **No CRITICAL, no HIGH, no MEDIUM,
> no residuals owed.**
>
> **This completes the dataset layer.** With W2-U01–U04 proven, only **W2-U05 (experiment registry /
> pre-registration)** remains before the model gate (W2-U06+) may open.

**Why clean APPROVED:** the two mistakes this unit exists to prevent — irreproducibility and split/label
leakage — are *proven refused*, not asserted; every mandatory §5 item is present and visible; and the DA
even added a grep proving **no model/training code exists yet** (the gate is provably un-crossed). Per
proportionality (R13), a clean approval is correct.

---

## 1. Evidence Hierarchy Assessment (R2)

**Level-I (operator-run, Windows + PostgreSQL)** for every material claim, with named `-vv` captures
continued. Sixth consecutive first-submission target-proven unit.

| Tier | Present? | Notes |
|------|----------|-------|
| Level-I — operator-run on Windows + PostgreSQL | ✅ | PG migrate to `0008`, pytest 119 on PG, four per-test `-vv` runs, two containment greps, parity smoke |
| Level-II — DA sandbox (SQLite) | ✅ | 119/16 + SQLite migrate — corroborating |
| Level-III — source/ADR excerpts | ✅ | ADR-024 added; builder/split-engine files enumerated |
| Level-IV — report claims | ✅ | Present; not the basis for approval (R1) |

---

## 2. Mandatory §5 Evidence — Line-by-Line Verification

| # | Required (Build Order §5) | Verdict | Proof in operator console |
|---|---------------------------|---------|---------------------------|
| 1 | Operator test console: pytest ≥112+new, 0 failed; vitest 16; ruff; tsc/build | ✅ **PROVEN** | `119 passed, 263 warnings in 46.69s` under the PG env (set at transcript lines 7–8, run line 52); `All checks passed!`; `Tests 16 passed (16)`; frontend build ok. Backend 112→119 (+7 = the 7 named tests). |
| 2 | Migration on PostgreSQL, new head shown | ✅ **PROVEN** | `Running upgrade 20260713_0007 -> 20260713_0008, W2-U04 dataset split manifests`; `alembic current → 20260713_0008 (head)` on `PostgresqlImpl`; single new revision. |
| 3 | Reproducibility: build-twice → identical hash; frozen rejects mutation | ✅ **PROVEN** | `test_snapshot_builder_rebuild_same_inputs_identical_hash PASSED` (dedicated `-vv`); `test_frozen_snapshot_immutable_new_version_created` in the +7. |
| 4 | Split-leakage: random split rejected; temporal boundary correct | ✅ **PROVEN** | `test_random_split_rejected_and_temporal_split_hash_deterministic PASSED` (dedicated `-vv`) — `SPLIT_LEAKAGE`, deterministic split hash (incl. reversed input order). |
| 5 | Label-horizon: crossing rejected; embargoed split passes | ✅ **PROVEN** | `test_label_horizon_crossing_rejected_and_embargoed_split_passes PASSED` (dedicated `-vv`) — `LABEL_HORIZON_LEAKAGE` refusal + embargoed pass (the R-2 headline). |
| 6 | Named-test capture (`-vv`) | ✅ **PROVEN** | Four dedicated per-test `-vv` runs captured by name, incl. `test_split_manifest_persisted_with_counts_and_hash PASSED`. Capture standard from W2-U03 continued. |
| 7 | Containment / D-W2-001 grep (R7: cmd+output) | ✅ **PROVEN (exceeds)** | Grep on `snapshot_builder.py` for `"symbol"/"provider"/"market_class"` → **empty** (training matrix identity-free); **plus** a grep over `app\ml` for `fit(\|predict(\|train_test_split\|RandomForest\|XGBoost\|LightGBM\|CatBoost` → **empty**, proving **no model/training code exists** (the model gate is provably un-crossed). |
| 8 | CI evidence | ✅ **N/A this unit** | No CI run in this transcript. **Not owed:** R-CI-01 was satisfied at W2-U03 (orchestrated pipeline green on PG) and is now a standing preference only. Non-blocking. |
| 9 | Parity smoke (no regression) | ✅ **PROVEN** | `WS-TICKET status: 200 ticket_present: True`; `persist_errors: 0`; live feed + candles intact. |
| 10 | Confidence HIGH/MODERATE/LIMITED, no fabricated % | ✅ **COMPLIANT** | Per-dimension with justification; "No percentage confidence is asserted." |

**Independently verified:** the +7 delta matches the 7 named snapshot/split tests; the 119-passed run is on
the PG environment; `test_synthetic_records_excluded_from_snapshot_builder` (in the +7) confirms the W2-U01
chronology guard still governs what enters a snapshot (OBS-1 enforced through the builder path).

---

## 3. Governance Envelope — Compliance

| Constraint (Build-Order §2) | Verdict | Basis |
|-----------------------------|---------|-------|
| ❌ No model / training / inference / prediction | ✅ Upheld (proven) | §9 out-of-scope; **grep for `fit(`/`predict(`/`train_test_split`/tree-libs → empty**; suite has no model tests. |
| ❌ No execution / broker / provider live connection / credentials; gate CLOSED | ✅ Upheld | External Integration untouched; broker tests still green in the 119. |
| ❌ No random/shuffled split | ✅ Upheld | `SPLIT_LEAKAGE` rejection test. |
| ❌ No label-horizon leakage | ✅ Upheld | `LABEL_HORIZON_LEAKAGE` rejection + embargoed pass. |
| ❌ No non-reproducible snapshot | ✅ Upheld | build-twice → identical hash test. |
| ❌ No authoritative use of synthetic/forward-dated | ✅ Upheld | `test_synthetic_records_excluded_from_snapshot_builder`; guard governs builder inputs. |
| ❌ No symbol identity in training matrix (D-W2-001) | ✅ Upheld | matrix rows = `row_id/as_of/features/source_dataset_hash` only; identity-field grep empty + structural test. |
| ❌ No DB reach-around / no secrets / no fabricated data | ✅ Upheld | port-based; no token in transcript; labels inert (not training targets). |
| ❌ No regression (Wave-0/1 + W2-U01/U02/U03) | ✅ Upheld | 119 passed incl. all prior suites + guards; parity smoke green; frontend 16 + build. |
| ✅ Preserve advisory-first, tz-UTC, observability, dataset+guard+port+features | ✅ Upheld | confirmed by suite + smoke. |

---

## 4. Findings (classified — R8)

**No CRITICAL. No HIGH. No MEDIUM. No LOW residuals owed.**

- **OBSERVATION (informational, commendable) — the DA proactively proved the model gate is un-crossed.**
  The additional grep (`fit(`/`predict(`/`train_test_split`/tree-model libs → empty) is not something the
  Build Order strictly demanded; it is exactly the kind of self-supplied negative evidence that makes
  review fast and trustworthy. No action — noted as good practice.
- **OBSERVATION (informational) — R-CI-01 remote run** remains a standing preference (satisfied via local
  orchestration at W2-U03). Capture a remote run opportunistically. No action.
- **RECOMMENDATION (forward, W2-U05):** the experiment registry must let an experiment **pin an exact
  (snapshot hash + split manifest hash)** and **reject** an experiment referencing a mutated/unfrozen
  snapshot or an unhashed split — so reproducibility carries from the dataset layer into every recorded
  experiment. (Design note for the W2-U05 Build Order; deferrals TD for split-pinning already recorded.)

**No finding withholds or qualifies approval.**

---

## 5. Required Actions
**None blocking.** Hygiene only: a real *remote* CI run when convenient (R-CI-01 preference).

---

## 6. Evidence Confidence Statement (R6 — no fabricated percentages)

**Confidence in this APPROVAL: HIGH.** Justification: every claim material to the unit is backed by
**operator-run Windows + PostgreSQL Level-I evidence** I verified directly — a clean PG migrate to
`20260713_0008`, `pytest 119 passed` on PG, four dedicated per-test `-vv` runs proving the three headline
guarantees (reproducible hash, random-split rejection, label-horizon rejection + embargoed pass) plus split
manifest persistence, two shown-and-empty containment greps (identity-free matrix **and** no model/training
code), and a green parity smoke. The chronology guard still governs snapshot inputs. No residuals owed; no
countervailing evidence. Confidence is HIGH without caveat.

---

## 7. Commendation (earned)

Sixth consecutive first-submission target-proven unit, and it closes the dataset layer the right way: the
two most damaging ML errors — **irreproducibility** and **leakage** — are *proven refused* by named tests
(same-hash rebuild, `SPLIT_LEAKAGE`, `LABEL_HORIZON_LEAKAGE`). The training matrix is identity-free by
construction, and the DA went beyond the ask to **prove the model gate is un-crossed** (empty grep for
`fit`/`predict`/split/tree-libs) — pre-empting the exact question a reviewer asks at the boundary before
model work. Disciplined, reviewer-aware, and honest (labels kept inert, no fabricated data).

---

## 8. Disposition

- **W2-U04: APPROVED.** Platform **v0.16.0**.
- **Residuals: NONE owed.** (R-CI-01 remote run a standing preference only.)
- **OBS-1:** enforced by contract; re-confirmed the guard governs snapshot builder inputs.
- **Dataset layer COMPLETE (W2-U01–U04 proven).** **Hard gate:** only **W2-U05 (experiment registry /
  pre-registration)** remains before any model unit (W2-U06+) is reviewable.
- **Next:** ITRGA recommends authorizing **W2-U05 = Experiment Registry + Pre-Registration Workflow** (per
  accepted plan §10; `07_ML_SPEC` §Experiment Governance "no undocumented experiment exists") — every
  experiment pre-registered with purpose/hypothesis/datasets/features/model/evaluation-plan/approval-
  timestamp/version, **pinning an exact snapshot+split hash**, with an undocumented-experiment **rejected**
  by negative test. That unit is the **final gate layer**; after it, the first model unit (W2-U06) becomes
  reviewable. The DA does not self-authorize the next unit and does not open the broker gate. Await
  operator direction + a new Build Order.

---

*ITRGA — A dataset you can rebuild to the same hash, split by time with a moat no label can cross, and a
matrix that never learns a symbol's name — each proven by a bad case refused. The dataset layer is done and
the model gate has one lock left: pre-registered, reproducibly-pinned experiments. We don't guess. We
prove.*
