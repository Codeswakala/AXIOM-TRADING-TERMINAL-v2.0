# ITRGA INDEPENDENT TECHNICAL REVIEW — W2-U10

## ML Research: Multi-Market Generalization + Model Registry / Drift Design (final Wave-2 unit)

**Review ID:** ITRGA-REVIEW-W2-U10
**Unit:** W2-U10 · **Wave:** 2 — ML Research Framework · **Unit:** 10 (LAST)
**Reviewer:** ITRGA · **Date:** 2026-07-15
**Inputs reviewed:** `DELIVERY_REPORT_W2-U10.md`; operator console transcript (`operator results.md`, 883
lines; Windows/PowerShell + PostgreSQL 18); cross-checked against `BUILD_ORDER_W2-U10.md`, `07_ML_SPEC`
§Generalization/§Model Registry/§Drift, D-W2-001, and the **escalated persistence-capture control** (W2-U09:
"next recurrence → HIGH").
**Motto:** *We don't guess. We prove.*

---

## 0. VERDICT

> ## ⚠️ **CONDITIONAL — APPROVAL WITHHELD** (persisted-PG artifacts) + **HIGH process finding**
> ## "Research Framework Complete" milestone **NOT YET declared** — pending this correction.
>
> The W2-U10 **implementation is strong and every functional requirement is proven by name** with a captured
> `-vv | Tee-Object` run: **trained-on-X / evaluated-on-Y** generalization; **market-holdout-overlap refused**
> (`MARKET_HOLDOUT_LEAKAGE`); **operating-domain warning pair** (`UNSUPPORTED_DOMAIN`); **registry matured
> with U07/U08/U09 links + operating domain**; **drift signal does NOT auto-retrain** (`retrain_triggered=
> False`, `governance_required=True`); reproducible; no identity/live-signal/auto-retrain loop. `pytest 159
> passed` on PostgreSQL, CI green through completion, parity smoke green.
>
> **But the mandatory persisted-PostgreSQL proof for the THREE new artifact types is entirely absent from the
> operator transcript** — there is **no committing script and no `SELECT`** on `generalization_reports`,
> `drift_monitoring_records`, or the matured `model_artifacts` registry columns. The delivery report §8 *says*
> the command pack includes it, but **a documented command is not captured evidence** (the W2-U02/U08 lesson).
>
> **This is the FIFTH persistence-capture recurrence and the SECOND since the W2-U08 standing instruction.**
> Per the escalation I pre-declared at W2-U09 ("next recurrence → HIGH"), this is a **HIGH process finding.**
> Because W2-U10 is the unit that would trigger the Wave-2 milestone, and its **three core new artifacts are
> unproven on disk**, I withhold approval and **do not declare "Research Framework Complete."**

**Why withheld (and why the milestone waits):** the framework's *final* deliverables are a persisted
generalization report, a persisted drift record, and a matured model registry — a "Research Framework
Complete" declaration on artifacts not proven durable would be exactly the kind of report-claim approval this
engagement forbids (R1/R5). The fix is quick and in the DA's repertoire (used at W2-U05/U07/U08/U09). **Why
not FAIL:** all functionality is proven by named, captured tests; nothing is contradicted — this is an
evidence-capture omission, aggravated by its recurrence.

---

## 1. Mandatory §5 Evidence — Line-by-Line Verification

| # | Required | Verdict | Basis |
|---|----------|---------|-------|
| 1 | Wheel spike (if compiled) | ✅ **N/A (pure-Python)** | `GENERALIZATION_STACK: pure-python-stdlib`, `NO_COMPILED_GENERALIZATION_DEPENDENCY: True`. |
| 2 | pytest ≥152+new 0 failed; vitest 16; ruff; tsc/build | ✅ **PROVEN** | `159 passed … in 77.37s`; `All checks passed!`; `Tests 16 passed (16)`. Backend 152→159 (+7). |
| 3 | Migration on PostgreSQL, new head | ✅ **PROVEN** | `20260715_0013 -> 20260715_0014, W2-U10 generalization reports, drift records, model registry links` → `20260715_0014 (head)` on `PostgresqlImpl`. |
| 4 | Generalization (trained-on-X/eval-on-Y, leak-free) `-vv` | ✅ **PROVEN** | `test_trained_on_x_evaluated_on_y_generalization_report` + `test_market_holdout_overlap_refused` (`MARKET_HOLDOUT_LEAKAGE`) PASSED, captured via `Tee-Object`. |
| 5 | Operating-domain guardrail pair | ✅ **PROVEN** | `test_operating_domain_warning_pair PASSED` (`UNSUPPORTED_DOMAIN`). |
| 6 | Registry matured + U07/U08/U09 links | ✅ **PROVEN (test-level)** | `test_model_registry_matured_with_report_links_and_domain PASSED`. |
| 7 | Drift does NOT auto-retrain | ✅ **PROVEN** | `test_drift_signal_does_not_auto_retrain PASSED` (`retrain_triggered=False`, `governance_required=True`). |
| 8 | Reproducibility | ✅ **PROVEN** | `test_generalization_report_reproducible_same_hash PASSED`. |
| 9 | **Persisted-PG proofs (committing script, ALL new artifacts, correct tables, FIRST submission)** | ❌ **C-1 NOT DELIVERED** | **No committing heredoc and no `SELECT`** on `generalization_reports` / `drift_monitoring_records` / matured `model_artifacts` anywhere in the transcript (0 references). §5.9 unmet. Report §8 claims the pack has it — not captured. |
| 10 | No-live-signal/execution/auto-retrain/identity grep | ⚠️ **PARTIAL** | `test_no_identity_live_signal_or_auto_retrain_loop_added PASSED` (structural), but the **shown grep (R7)** is not in this transcript. Structural test substitutes but the explicit grep §5.10 is owed (fold into C-1 re-capture). |
| 11 | CI green on PostgreSQL through completion | ✅ **PROVEN** | `==> Local CI equivalent complete` (line 738). |
| 12 | Parity smoke | ✅ **PROVEN** | `WS-TICKET status: 200`; candles returned. |
| 13 | Confidence, honest | ✅ **COMPLIANT** | per-dimension; no fabricated %. |

**Net:** functionality fully proven (with captured `-vv`), but the unit's **defining persisted artifacts are
unproven on disk** (C-1) and the R7 grep is owed.

---

## 2. Findings (classified — R8)

- **C-1 (HIGH — unmet mandatory evidence).** The persisted-PostgreSQL proof for **all three** new artifact
  types is absent: no committing script; no `SELECT` returning ≥1 row for `generalization_reports`,
  `drift_monitoring_records`, or the matured `model_artifacts` (statistical/calibration/economic_report_id +
  operating_domain) with their audit events. **Required (C-1):** a committing script (`GeneralizationService`
  → commit) persisting one generalization report, one drift record, and one matured registry entry, then
  `SELECT ≥1 row` for **each of the three tables** (correct tables — the W2-U09 lesson) + their audit events.
  Reuse the proven method; no code change expected.
- **PROCESS FINDING (HIGH — escalation triggered).** Fifth persistence-capture recurrence (G-2@U01,
  C-2@U05, C-1@U08, C-1@U09, now U10) and **second after the W2-U08 standing instruction.** Per the W2-U09
  pre-declaration ("next recurrence → HIGH"), recorded as a **HIGH process finding on W2-U10.** Aggravating:
  the delivery report **asserted** the pack contains the committing proof while the operator transcript does
  not — restating R1 (a report is the lowest evidence tier; a described command is not a run one). This is
  now a persistent evidence-assembly discipline problem, not a one-off.
- **R7 grep (LOW, fold into C-1):** the no-identity/no-live-signal/no-auto-retrain **shown grep** is owed
  (the structural test passed, but §5.10 asked for the visible grep).
- **NOT a FAIL / NOT a regression:** all generalization/registry/drift functionality is proven by named,
  captured tests; nothing is contradicted. Narrow-but-important CONDITIONAL + a HIGH process finding on the
  recurrence.

---

## 3. Required Corrections (before W2-U10 approval AND the Wave-2 milestone)

- **C-1 (HIGH):** committing-script persisted-PG proof for **all three** artifacts — `generalization_reports`,
  `drift_monitoring_records`, matured `model_artifacts` (with U07/U08/U09 report-id links + operating_domain)
  — each `SELECT` returning ≥1 row from its **correct table**, plus the corresponding audit events.
  Operator-run, Windows + PostgreSQL.
- **C-2 (LOW):** the shown R7 grep (no identity-as-feature / no live-signal route / no auto-retrain loop) —
  command + empty output.

Do **not** re-run the rolled-back tests or re-paste a prior unit's committing script (the W2-U09 aggravating
error). Verify each `SELECT` names the W2-U10 table.

---

## 4. What is already solid (do not redo)

Generalization + registry + drift **function fully proven** by named `-vv | Tee-Object` tests on target:
trained-on-X/eval-on-Y, market-holdout-leakage refused, operating-domain warning pair, registry U07/U08/U09
links, drift-no-auto-retrain (governance-gated), reproducibility. Suite 159 green on PG; migrate `0014
(head)`; CI green through completion; parity smoke green; pure-Python. Only the **persisted-PG capture** (and
the R7 grep) are owed.

---

## 5. Evidence Confidence Statement (R6 — no fabricated percentages)

**Confidence W2-U10 is approvable once C-1/C-2 land: HIGH.** The functionality — the keystone generalization
objective, operating-domain guardrail, registry maturation, and no-auto-retrain gate — is demonstrated on the
target with captured named tests, CI green, envelope intact. **Confidence it is *currently* proven to
standard: LIMITED — because the three defining persisted artifacts are unshown on disk (C-1), a HIGH process
finding on the recurring capture gap.** A committing proof targeting the three W2-U10 tables converts this to
APPROVED and unlocks the milestone declaration.

---

## 6. Commendation & process note

The generalization layer is excellent and squarely on-spec — it answers the transfer question D-W2-001 was
chosen for, fences models to their validated domain, links the full statistical/calibration/economic evidence
into the registry, and keeps drift human-gated (no auto-retrain). The DA also **captured the `-vv` named tests
with `Tee-Object`** as instructed. The shortfall is, once more, **persisted-artifact evidence capture** — now
recurring to the point of a HIGH process finding, and aggravated by the report claiming the proof exists when
the transcript shows it does not. The fix is trivial and functional approval (plus the milestone) is one
correctly-targeted committing proof away — but the standard holds: the framework is not "complete" until its
final artifacts are proven durable.

---

## 7. Disposition

- **W2-U10: CONDITIONAL — APPROVAL WITHHELD (C-1 persisted-PG; C-2 grep) + HIGH process finding
  (persistence-capture recurrence).** Platform stays **v0.21.0** for gating (DA 0.22.0 provisional).
- **"Research Framework Complete" milestone: NOT declared** — reserved for W2-U10 approval on complete
  evidence.
- **Gate posture unchanged:** research-only; no live signal/monitoring loop/auto-retrain/execution (proven);
  broker gate CLOSED.
- **Next:** DA resubmits **only C-1 (three-table committing persisted-PG proof) + C-2 (R7 grep)**, operator-
  run, each `SELECT` verified against its W2-U10 table. On that evidence, ITRGA approves W2-U10 and — with
  W2-U01–U09 already approved — **declares the Wave-2 milestone "Research Framework Complete"** in a closure
  verdict, then recommends the operator consider scoping **Wave 3 — Live Research Advisor** (opens the
  live-signal surface; needs its own governance envelope + Build Orders). The DA does not self-approve,
  self-declare the milestone, self-authorize Wave 3, or open the broker gate.

---

*ITRGA — The keystone is cut true: a model's transfer measured honestly, fenced to its domain, its full
evidence linked in one registry entry, and drift that records but never silently retrains — all proven by
named tests. But the three artifacts that *are* the framework's memory — generalization report, drift record,
matured registry — were never shown alive on PostgreSQL, and the report claiming the proof cannot stand in
for the proof. Fifth time for this gap, second since we made it a rule, so it is now a HIGH finding, and the
"Research Framework Complete" banner stays furled. Persist the three, select each from its own table — and I
will raise it. We don't guess. We prove.*
