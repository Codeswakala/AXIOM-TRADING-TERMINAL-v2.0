# ITRGA INDEPENDENT TECHNICAL REVIEW — W2-U05

## ML Research: Experiment Registry + Pre-Registration Workflow (final gate layer)

**Review ID:** ITRGA-REVIEW-W2-U05
**Unit:** W2-U05 · **Wave:** 2 — ML Research Framework · **Unit:** 05
**Reviewer:** ITRGA (Independent Technical Review & Governance Authority)
**Date:** 2026-07-13
**Inputs reviewed:** `DELIVERY_REPORT_W2-U05.md`; operator console transcript (`operator results.md`,
Windows/PowerShell + PostgreSQL 18, Python 3.14.6); cross-checked against `BUILD_ORDER_W2-U05.md`,
`07_ML_SPEC` §Experiment Governance, D-W2-001.
**Motto:** *We don't guess. We prove.*

---

## 0. VERDICT

> ## ⚠️ **CONDITIONAL — APPROVAL WITHHELD** (targeted evidence re-capture required)
>
> The W2-U05 **implementation appears sound** — clean PostgreSQL migrate to head `20260713_0009`, **pytest
> 127 passed** (119→127, +8), ruff clean, frontend 16 + build, and three registry tests captured by name
> `-vv` (accepted / immutable / audit). **But the evidence for this unit's *headline* guarantees was not
> captured**, and this is the **final gate layer that opens the model gate** — so the bar is exact: the
> *bad* experiment must be **proven refused**, not merely counted in an aggregate.
>
> **Four mandatory §5 evidence items are missing or mis-targeted (R5 caps the verdict; R11 no-roll-forward):**
> C-1 the **five rejection/negative tests are not shown by name** (only the *acceptance* tests were `-vv`
> captured — inverted from what matters most); C-2 the **persisted-PostgreSQL experiment + audit rows
> returned `(0 rows)`** (the G-2 rollback pattern — no committing proof); C-3 the **no-model-code grep**
> (§5.8) is absent; C-4 the **parity smoke** (§5.10) is absent.
>
> This is **not** a finding against the code (the +8 aggregate + the three named tests indicate it works).
> It is an **unmet-mandatory-evidence** hold, applied exactly as at W2-U01 — resolvable by a short,
> targeted re-capture, after which I expect to approve.

**Why withheld rather than approved-with-observations:** for the unit whose entire purpose is to *refuse
undocumented and unpinned experiments*, the rejection proofs are the core function — and they were the ones
not captured. Aggregate `127 passed` is necessary but not sufficient (the U08 lesson). A governance gate is
approved when its refusals are *shown*, not inferred. The gap is narrow and the fix is quick, so this is a
CONDITIONAL, not a FAIL.

---

## 1. Evidence Hierarchy Assessment (R2)

| Tier | Present? | Notes |
|------|----------|-------|
| Level-I — operator-run on Windows + PostgreSQL | ✅ (partial) | PG migrate to `0009`, pytest 127 on PG, 3 named `-vv` registry tests |
| Level-I — the unit's **headline rejection proofs** | ❌ **not captured by name** | see C-1 |
| Level-I — **persisted** experiment/audit record | ❌ `(0 rows)` | see C-2 |
| Level-II — DA sandbox (SQLite) | ✅ | 127/16 — corroborating |
| Level-IV — report claims | ✅ | Present; **not** a basis for approving the missing items (R1) |

The DA's *report* asserts all rejections pass with specific reason codes (`UNDOCUMENTED_EXPERIMENT`,
`UNREPRODUCIBLE_EXPERIMENT_PIN`, `SPLIT_LEAKAGE`) — but a report is the lowest tier (R1), and for a gate
unit the operator console must *show* those refusals. It does not.

---

## 2. Mandatory §5 Evidence — Line-by-Line Verification

| # | Required (Build Order §5) | Verdict | Basis |
|---|---------------------------|---------|-------|
| 1 | Operator test console: pytest ≥119+new, 0 failed; vitest 16; ruff; tsc/build | ✅ **PROVEN** | `127 passed … in 83.38s` under PG env (set lines 3–4); `All checks passed!`; `Tests 16 passed (16)`. Backend 119→127 (+8). |
| 2 | Migration on PostgreSQL, new head shown | ✅ **PROVEN** | `Running upgrade 20260713_0008 -> 20260713_0009, W2-U05 experiment registry` → `20260713_0009 (head)` on `PostgresqlImpl`; single new revision. |
| 3 | **Rejection evidence (headline): undocumented + unpinned/unfrozen/unhashed-split rejected, reason codes visible** | ❌ **C-1 NOT SHOWN** | The dedicated `-vv` runs captured **only** `test_pre_registered_and_approved_experiment_accepted`, `test_approved_plan_immutable_new_version_created`, `test_audit_events_written_for_workflow`. The five rejection/negative tests (`..._undocumented_experiment_rejected`, `..._unpinned_unfrozen_or_unhashed_experiment_rejected`, `..._random_split_evaluation_plan_rejected`, `..._approval_required_before_runnable`, `..._no_model_training_code...`) appear **nowhere by name**; the aggregate run was `pytest -q` (no per-test lines). Reason codes not visible in console. |
| 4 | Acceptance evidence: pinned experiment accepted; **show the stored record** | ⚠️ **PARTIAL / C-2** | The *test* `..._accepted PASSED`, but the **persisted `SELECT … FROM experiments` returned `(0 rows)`** — the stored record is not shown (tests roll back; no committing proof). |
| 5 | Immutability evidence | ✅ **PROVEN (test-level)** | `test_approved_plan_immutable_new_version_created PASSED` (named `-vv`). |
| 6 | **Audit evidence: persisted append-only events on PostgreSQL** | ❌ **C-2 NOT SHOWN** | `SELECT … FROM audit_events WHERE resource_type='experiment'` → **`(0 rows)`**. The in-test `test_audit_events_written_for_workflow` passes, but a *persisted* audit row on PG (the G-2-style committing proof) is absent. |
| 7 | Named-test capture (`-vv`) for W2-U05 tests | ⚠️ **PARTIAL** | 3 of 8 captured by name; the 5 that matter most (rejections) were not. |
| 8 | **No-model-code grep** (`fit(`/`predict(`/`train_test_split`/tree-libs) | ❌ **C-3 NOT SHOWN** | Absent from the transcript (was present and exemplary in W2-U04). |
| 9 | CI evidence | ✅ **N/A** | Not owed (R-CI-01 satisfied W2-U03; standing preference only). |
| 10 | **Parity smoke** (login → ws-ticket → live feed → candles) | ❌ **C-4 NOT SHOWN** | No smoke in the transcript (present in every prior unit). |
| 11 | Confidence HIGH/MODERATE/LIMITED, no fabricated % | ✅ **COMPLIANT** | Per-dimension; "No percentage confidence is asserted." |

**Net:** 4 of the mandatory items are proven (console, migration, immutability, confidence). **Four are
unmet** — and three of those four (C-1, C-2 acceptance/audit persistence, and the fact the *rejection*
proofs specifically were skipped) go to the **core function** of a governance-gate unit.

---

## 3. Required Corrections (to move from CONDITIONAL → APPROVED)

- **C-1 (HIGH) — capture the rejection proofs by name.** Run and **capture** (`-vv | Tee-Object` / `-rA`)
  each of: `test_undocumented_experiment_rejected`, `test_unpinned_unfrozen_or_unhashed_experiment_rejected`,
  `test_random_split_evaluation_plan_rejected`, `test_approval_required_before_runnable`,
  `test_no_model_training_code_introduced_in_experiment_registry` — each **PASSED**, visible by name. Ideally
  also surface the reason codes (`UNDOCUMENTED_EXPERIMENT`, `UNREPRODUCIBLE_EXPERIMENT_PIN`, `SPLIT_LEAKAGE`)
  in the output. *This is the headline evidence for the unit and must be shown, not asserted.*
- **C-2 (HIGH) — persisted PostgreSQL proof (the G-2 method, reused).** A **committing** script that
  registers → approves one experiment (pinning a real frozen snapshot hash + split manifest hash), then a
  raw `psql SELECT` showing the **experiments** row (status `approved`, hashes, approver, approval_timestamp)
  **and** the append-only **audit_events** rows (`experiment.create/pre_register/approve`). The post-test
  `(0 rows)` is expected from rolled-back tests — prove *persistence* the way G-2 was proven at W2-U02.
- **C-3 (MEDIUM) — no-model-code grep** (§5.8): shown grep (R7: cmd + empty output) that
  `fit(`/`predict(`/`train_test_split`/tree-model libs are absent — confirming the model gate is still
  un-crossed by this governance unit (as W2-U04 did).
- **C-4 (LOW) — parity smoke** (§5.10): login → WS ticket 200 → live feed → candle fetch, unaffected.

None require code changes if the implementation is as reported — they are **evidence captures.** If any
rejection test does *not* actually pass on the target, that becomes a real finding.

---

## 4. Findings (classified — R8)

- **C-1 / C-2 (HIGH — unmet mandatory evidence for the core function).** The gate's *refusals* and its
  *persisted governance record* are exactly what a reviewer must see for a pre-registration/audit unit;
  neither is shown. R5 caps the verdict; R11 forbids opening the model gate on this.
- **C-3 (MEDIUM), C-4 (LOW) — unmet mandatory evidence** (§5.8/§5.10), both routinely supplied in prior
  units; their absence here is part of a **thinner-than-usual capture** for this delivery.
- **OBSERVATION — the capture was inverted.** The DA captured `-vv` for the *acceptance/immutable/audit*
  tests (which pass) but not the *rejection* tests (the point of the unit). Capture the negatives first —
  a governance gate is proven by what it refuses.
- **OBSERVATION (C-2 root cause is benign) — the `(0 rows)` is the known rollback pattern, not a defect.**
  It is *correct* that transactional tests don't persist to the operator DB; the remedy is the committing
  proof (identical to how G-2 was closed at W2-U02). No suggestion the code is wrong — only that persistence
  is unproven as presented.
- **NOT a regression / NOT a FAIL:** `127 passed` + clean migration + the three named tests indicate the
  unit works; nothing in the evidence contradicts a claim (contrast the U08 "report says works, server says
  500" case — here there is no failing artifact, only *absent* required artifacts). Hence CONDITIONAL.

---

## 5. What is already solid (so the DA knows what NOT to redo)

- Registry schema with the `07_ML_SPEC` mandatory fields + snapshot/split hash pinning + plan_hash +
  versioning — migrated cleanly on PostgreSQL to `0009`.
- The create → pre-register → approve workflow, immutability (new-version-on-change), and audit-event
  emission are **test-proven** (three named `-vv` PASSED).
- No regression: full suite 127 green; frontend 16 + build; ruff clean. D-W2-001 posture preserved
  (`model_family`/`model_spec` are inert plan metadata).

Only the **evidence capture** (C-1..C-4) is required — no re-implementation expected.

---

## 6. Evidence Confidence Statement (R6 — no fabricated percentages)

**Confidence that W2-U05 is APPROVABLE: MODERATE.** The implementation is very likely correct — the
aggregate `127 passed` on PostgreSQL, the clean migration, and three named-and-captured registry tests all
point to a sound unit, and nothing in the evidence contradicts the DA's claims. **Confidence that it is
*currently proven to the W2-U05 standard*: LIMITED** — the unit's defining guarantees (rejection of
undocumented/unpinned/random-split/unapproved experiments) and its persisted governance record (experiment
+ audit rows on PG) were **not captured**, and this is the final gate before models. I do not approve a
gate on inferred refusals. A short, targeted re-capture (C-1..C-4) should convert this to APPROVED.

---

## 7. Commendation (genuine — but it does not close the gap)

The registry design is strong and correctly scoped: mandatory fields verbatim from the spec, reproducible
pinning carried forward from W2-U04, immutability + audit, and inert model metadata (gate respected). The
three tests that *were* captured are clean. The shortfall here is **evidence discipline on this specific
delivery**, not design — and it is exactly recoverable. Capture the refusals and the persisted record, and
this unit is ready.

---

## 8. Disposition

- **W2-U05: CONDITIONAL — APPROVAL WITHHELD.** Platform remains **v0.16.0** for gating purposes until
  approved (the DA's `0.17.0` tag is provisional pending approval).
- **Required to approve:** **C-1** (rejection tests captured by name), **C-2** (persisted PG experiment +
  audit rows via committing proof), **C-3** (no-model-code grep), **C-4** (parity smoke). All are captures;
  no code change expected.
- **Hard model gate: STILL CLOSED.** W2-U06 does **not** become reviewable until W2-U05 is APPROVED (R11).
  Broker gate CLOSED throughout Wave 2.
- **Next:** DA resubmits a **W2-U05 correction** with the C-1..C-4 captures (operator-run, Windows + PG).
  On clean re-verification, ITRGA approves W2-U05 and *then* authorizes W2-U06 (baseline model harness) —
  which will additionally owe its target-platform package-compatibility spike. The DA does not
  self-authorize W2-U06 or open any gate.

---

*ITRGA — The registry looks right, and the suite is green — but a gate is judged by the doors it slams, and
those were the shots not captured. Show us the undocumented experiment refused, the unpinned one refused,
and one approved experiment with its audit trail living on PostgreSQL — then the model gate opens on proof,
not on trust. We don't guess. We prove.*
