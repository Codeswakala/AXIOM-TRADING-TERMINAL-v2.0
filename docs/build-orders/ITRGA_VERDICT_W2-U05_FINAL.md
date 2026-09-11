# ITRGA FINAL VERDICT — W2-U05

## ML Research: Experiment Registry + Pre-Registration Workflow (final gate layer)

**Review ID:** ITRGA-VERDICT-W2-U05-FINAL
**Unit:** W2-U05 · **Wave:** 2 · **Unit:** 05 · **Round:** correction #2 (final)
**Reviewer:** ITRGA · **Date:** 2026-07-14
**Inputs reviewed:** operator console transcript (`operator results.md`, C-2 persistence proof;
Windows/PowerShell + PostgreSQL 18); re-verified against `ITRGA_REVIEW_W2-U05.md` (C-1..C-4) +
`ITRGA_REVIEW_W2-U05_CORRECTION.md` (C-2 remaining).
**Journey:** CONDITIONAL (4 items) → correction #1 (C-1/C-3/C-4 closed; C-2 non-proof repeated) →
**correction #2: C-2 CLOSED → APPROVED.**
**Motto:** *We don't guess. We prove.*

---

## 0. VERDICT

> ## ✅ **APPROVED WITH OBSERVATIONS** — Platform **v0.17.0** — **ML Research FOUNDATION COMPLETE; model gate OPEN**
>
> The final required correction (**C-2**) is now **conclusively proven** on the target: a **committing
> script** created → pre-registered → **approved** one experiment on PostgreSQL, and the raw `psql SELECT`s
> returned the **persisted `experiments` row** (status `approved`, pinned snapshot+split hashes, approver
> `operator-evidence`, approval_timestamp) **and the three append-only `audit_events` rows**
> (`experiment.create` / `experiment.pre_register` / `experiment.approve`). Combined with C-1/C-3/C-4
> (closed in correction #1) and the already-verified suite (**127 passed** on PG, clean migrate to
> `20260713_0009`, registry table on PG, CI green), **every mandatory §5 item for W2-U05 is satisfied.**
>
> **W2-U05 is APPROVED.** This was the **last gate layer**: with W2-U01–U05 all proven, the **ML Research
> Framework foundation (dataset → chronology → market access → features → snapshots/splits → experiment
> registry) is complete**, and the **hard model gate now legitimately OPENS** — W2-U06 (baseline model
> harness) becomes reviewable, subject to its own constraints (§4).

The "WITH OBSERVATIONS" reflects only the two-round evidence journey (a process note), not any residual
technical gap — there is **no unmet item** and **no residual owed**.

---

## 1. Correction Ledger — final (R12: each finding independently re-proven)

| Item | Sev | Round closed | Proof |
|------|-----|--------------|-------|
| **C-1** rejection tests by name | HIGH | #1 | all 8 experiment tests incl. 5 rejections named-`-vv` PASSED |
| **C-2** persisted PG experiment + audit rows | HIGH | **#2 (now)** | committing script → `experiments` **`(1 row)` status approved** + `audit_events` **`(3 rows)`** create/pre_register/approve — see §2 |
| **C-3** no-model-code grep | MED | #1 | `fit(`/`predict(`/`train_test_split`/tree-libs over `app\ml` → empty |
| **C-4** parity smoke | LOW | #1 | ws-ticket 200, persist_errors 0 (+ bonus `local_ci.sh` green on PG) |

**All four closed. Nothing owed.**

---

## 2. C-2 Verification (the artifact that was owed)

The operator transcript shows, on PostgreSQL:
- **Committing script** (`… | python -`) using `ExperimentRegistryService`: `create` (pinning
  `dataset_content_hash` + `split_manifest_hash`) → `pre_register` → `approve(approver="operator-evidence")`
  within `session_scope` (committed). Console echoed `EXPERIMENT_STATUS: approved`.
- **Persisted `experiments` row** (`SELECT … WHERE experiment_id = '$ExpId'`):
  `operator-approved-experiment-proof-20260714184103 | version 1 | status **approved** |
  dataset_content_hash …-snapshot-hash | split_manifest_hash …-split-hash | approver **operator-evidence** |
  approval_timestamp 2026-07-14 18:41:09` → **`(1 row)`**.
- **Persisted append-only `audit_events`** (`WHERE resource_type='experiment' AND
  details->>'experiment_id' = '$ExpId' ORDER BY created_at ASC`): **`experiment.create` →
  `experiment.pre_register` → `experiment.approve`** → **`(3 rows)`**, in workflow order, all bound to the
  same experiment_id.

This is precisely the durable-governance-record proof required: an approved, pinned experiment and its full
audit trail **living on PostgreSQL**, survived a commit — not a rolled-back in-test artifact. The earlier
`(0 rows)` (which reflected transactional rollback) is now correctly superseded. **C-2 CLOSED.**

---

## 3. Full-unit confirmation (no roll-forward on stale evidence — R12)

W2-U05's complete evidence base (across the three rounds, all operator-run Windows + PostgreSQL Level-I):
- **Schema & migration:** clean migrate to `20260713_0009 (head)` on `PostgresqlImpl`; `experiments` table
  present on PG; mandatory `07_ML_SPEC` fields + snapshot/split hash pinning + plan versioning.
- **Rejections proven by name:** undocumented, unpinned/unfrozen/unhashed-split, random-split-eval,
  approval-required-before-runnable, no-model-code — all PASSED (C-1).
- **Acceptance + immutability + audit:** pre-register→approve accepted; approved plan immutable
  (new-version-on-change); audit events emitted — proven by named tests **and** by the persisted PG record
  (C-2).
- **Suite & hygiene:** `pytest 127 passed` (119→127, +8) on PG; ruff clean; frontend 16 + build;
  orchestrated `local_ci.sh` green on PG; no-model-code grep empty (gate un-crossed); parity smoke green.
- **Governance envelope:** no model/training/inference/execution; broker gate CLOSED; D-W2-001 preserved
  (`model_family`/`model_spec` inert plan metadata); no secrets/PII.

No regression; no contradiction; no residual. Confidence **HIGH**.

---

## 4. What now opens — and the constraints that ride with it

**The hard model gate is OPEN.** W2-U06 (Baseline Market-Agnostic Model Harness) becomes reviewable — but
it inherits **non-negotiable constraints** the whole foundation was built to enforce:
1. **Consume only a pre-registered, approved, hash-pinned experiment** (this unit) — no ad-hoc training.
2. **Train only on reproducible, temporally-split, embargoed, leak-free snapshots** (W2-U01/U04) — no
   random split, no label-horizon leakage, no synthetic/forward-dated authoritative data.
3. **Market-agnostic model — no symbol identity as a feature** (D-W2-001; re-assert the exclusion at the
   *model input boundary*, per the W2-U03/U04 forward notes).
4. **Target-platform package-compatibility spike FIRST** (numpy/scikit-learn on Windows + Py3.14.6, plan
   §4.2) — delivered and reviewed as its own acceptance gate *before* the model harness is judged, so a
   wheel failure surfaces early, not at the operator run.
5. **Research/advisory only** — no live signals (Wave 3), no execution ever until Wave 6 governance; broker
   gate stays CLOSED.

---

## 5. Evidence Confidence Statement (R6 — no fabricated percentages)

**Confidence in this APPROVAL: HIGH.** Every mandatory item is now backed by operator-run, Windows +
PostgreSQL Level-I evidence I verified directly, including the previously-missing persisted governance
record (an approved experiment + 3 audit rows living on PostgreSQL). The registry refuses undocumented and
unpinned experiments (proven by name), the suite is green on PG, and the model gate is un-crossed. No
residual, no contradiction. HIGH without caveat.

---

## 6. Commendation & process note

The registry design was strong from the first submission; the shortfall was purely **evidence discipline**,
and the DA ultimately delivered the exact committing-script proof required (reusing its own G-2 technique).
Process note for the record: it took two correction rounds because correction #1 *re-ran the non-proof*
(the rolled-back `SELECT`) instead of the committing script — a reminder, logged in onboarding, that a
repeated non-proof is not a proof. Credit for closing it cleanly on round #2; the standard held, and the
gate opened on evidence.

---

## 7. Disposition

- **W2-U05: APPROVED WITH OBSERVATIONS.** Platform **v0.17.0**.
- **Residuals: NONE owed.** (Remote CI run remains a standing preference only.)
- **ML Research Framework FOUNDATION COMPLETE (W2-U01–U05 all proven).** **Hard model gate OPEN.**
- **Next:** ITRGA recommends authorizing **W2-U06 = Baseline Market-Agnostic Model Harness**, whose Build
  Order will (a) require the Py3.14 package-compatibility spike as its own gate, (b) consume only a
  pre-registered/approved/pinned experiment, (c) enforce the D-W2-001 exclusion at the model input boundary,
  and (d) remain research-only (no live signals, gate CLOSED). The DA does not self-authorize W2-U06 or open
  the broker gate. Await operator direction + a new Build Order.

---

*ITRGA — The last lock is proven shut and, therefore, the model gate opens: an approved experiment and its
audit trail now live on PostgreSQL, pinned to a dataset we can rebuild to the same hash and split with a
moat no label can cross. Five units built the foundation so the first model can only ever be trained on
honest, reproducible, leak-free, pre-registered data. Now — and only now — we may build a model. We don't
guess. We prove.*
