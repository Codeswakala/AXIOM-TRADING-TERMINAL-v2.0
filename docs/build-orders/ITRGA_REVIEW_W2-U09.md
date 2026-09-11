# ITRGA INDEPENDENT TECHNICAL REVIEW — W2-U09

## ML Research: Economic Validation Framework

**Review ID:** ITRGA-REVIEW-W2-U09
**Unit:** W2-U09 · **Wave:** 2 — ML Research Framework · **Unit:** 09
**Reviewer:** ITRGA · **Date:** 2026-07-15
**Inputs reviewed:** `DELIVERY_REPORT_W2-U09.md`; operator console transcript (`operator results.md`, 1105
lines; Windows/PowerShell + PostgreSQL 18); cross-checked against `BUILD_ORDER_W2-U09.md`, `07_ML_SPEC`
§Economic Validation, D-W2-001, and the **standing persistence-capture instruction** issued at W2-U08.
**Motto:** *We don't guess. We prove.*

---

## 0. VERDICT

> ## ⚠️ **CONDITIONAL — APPROVAL WITHHELD** (one item: persisted-PG economic report) + **MEDIUM process finding**
>
> The W2-U09 **implementation is strong and every functional requirement is proven by name**: the headline
> **statistically-positive-but-economically-negative** case is reported with both conclusions **separate**
> (`STATISTICALLY_POSITIVE_ECONOMICALLY_NEGATIVE`); cost inputs require **provenance + sensitivity** (R-4
> discharged in code); conflated/undeclared-cost reports are **rejected**; scenario sensitivity + per-slice
> delivered; **no execution/live-signal** path (structural test + grep); `pytest 152 passed` on PostgreSQL;
> CI green through completion; parity smoke green.
>
> **But the mandatory persisted-PostgreSQL economic-report proof (§5.8) is NOT delivered:** `SELECT … FROM
> economic_reports` and `… audit_events WHERE resource_type='economic_report'` both returned **`(0 rows)`**,
> and the one committing script in the transcript **persists a *calibration* report** (the W2-U08 proof
> re-pasted by mistake — `operator-calibration-proof-20260715010839`), **not an economic report.**
>
> **This is the FOURTH occurrence of the persistence-capture gap, and the FIRST since the W2-U08 standing
> instruction** ("any unit persisting a new report/artifact type must ship the committing-script + `SELECT
> ≥1 row` proof in its FIRST submission; next recurrence → MEDIUM process finding"). Per that trigger, a
> **MEDIUM PROCESS FINDING is recorded.** The unit is one committing proof from approval — but the process
> lapse is now formally flagged, not merely re-requested.

**Why withheld:** the economic report is this unit's core deliverable; its durable-on-disk record is
mandatory (R5). **Why not FAIL:** functionality is proven by named tests; nothing is contradicted — the
only defect is the (recurring) evidence-capture omission, aggravated by pasting the wrong committing script.

---

## 1. Mandatory §5 Evidence — Line-by-Line Verification

| # | Required (Build Order §5) | Verdict | Basis |
|---|---------------------------|---------|-------|
| 1 | (If compiled dep) wheel spike | ✅ **N/A (pure-Python)** | `ECONOMIC_VALIDATION_STACK: pure-python-stdlib`, `NO_COMPILED_ECONOMIC_DEPENDENCY: True`. |
| 2 | pytest ≥146+new 0 failed; vitest 16; ruff; tsc/build | ✅ **PROVEN** | `152 passed … in 57.48s`; `All checks passed!`; `Tests 16 passed (16)`. Backend 146→152 (+6). |
| 3 | Migration on PostgreSQL, new head | ✅ **PROVEN** | `20260714_0012 -> 20260715_0013, W2-U09 economic validation reports` → `20260715_0013 (head)` on `PostgresqlImpl`. |
| 4 | Cost model + provenance/sensitivity (R-4) | ✅ **PROVEN** | `test_cost_model_requires_provenance_and_sensitivity PASSED` (dedicated `-vv`); `CostInput(...provenance=MEASURED, low_bps/high_bps...)`; spread/commission/slippage/latency/liquidity/txn covered. |
| 5 | **Independence + headline (stat-positive/econ-negative separate)** (`-vv`) | ✅ **PROVEN** | `test_statistically_positive_but_economically_negative_reported_separately PASSED` (dedicated `-vv`); `STATISTICALLY_POSITIVE_ECONOMICALLY_NEGATIVE`; `test_conflated_or_undeclared_cost_report_rejected PASSED`. |
| 6 | Scenario sensitivity + per-slice | ✅ **PROVEN** | `test_scenario_sensitivity_and_per_slice PASSED` (opt/base/pess; min/max net bps; market/timeframe/regime slices). |
| 7 | Reproducibility (seeded → same) | ✅ **PROVEN (test-level)** | `test_economic_report_persisted_and_reproducible PASSED` (named `-vv`). |
| 8 | **Persisted-PG economic report (committing script, FIRST submission)** | ❌ **C-1 NOT DELIVERED** | `SELECT … economic_reports` → **`(0 rows)`**; `… audit_events (economic_report)` → **`(0 rows)`**. The transcript's committing heredoc persists a **calibration** report (W2-U08 proof re-pasted), not economic. §5.8 unmet; standing instruction breached. |
| 9 | No-execution / no-live-signal / no-identity grep | ✅ **PROVEN** | grep over `app\ml\economic` for `place_order\|cancel_order\|broker\|live_signal` → empty; routes grep hit only `persistence.py order=asc/desc` (a benign sort param, **not** execution). No execution path. |
| 10 | CI green on PostgreSQL through completion | ✅ **PROVEN** | `==> Local CI equivalent complete` (line 777). |
| 11 | Parity smoke | ✅ **PROVEN** | `WS-TICKET status: 200`; `persist_errors: 0`; `last_error: null`. |
| 12 | Confidence, honest | ✅ **COMPLIANT** | per-dimension; no fabricated %. |

**Net:** 11 of 12 proven — including the entire economic-validation *function* (the point of the unit). The
single unmet item is the persisted-PG economic record (C-1).

---

## 2. Findings (classified — R8)

- **C-1 (HIGH — unmet mandatory evidence).** The persisted-PostgreSQL **economic-report** + audit proof
  (§5.8) is absent — the `SELECT`s returned `(0 rows)` and the sole committing script persists a *calibration*
  report (`calibration_reports (1 row)`, `calibration.report_created`), i.e. the **W2-U08 proof was
  re-pasted** in place of the W2-U09 one. **Required (C-1):** a committing script that computes + persists one
  **economic report** on PostgreSQL (`EconomicValidationService` → commit), then `SELECT … FROM
  economic_reports` and `… audit_events WHERE resource_type='economic_report'` returning **≥1 row** each
  (with statistical_conclusion + economic_conclusion + scenario_results + cost_model + report_hash +
  research_only, and the `economic_report` audit event). No code change expected — point the proven method at
  the *economic* report.
- **PROCESS FINDING (MEDIUM — escalation triggered).** This is the **fourth** persisted-PG capture gap
  (G-2@U01, C-2@U05, C-1@U08, now U09) and the **first after the W2-U08 standing instruction** that required
  the committing proof in the first submission. Per the pre-declared trigger, it is recorded as a **MEDIUM
  process finding on W2-U09** (not a mere repeat correction). Aggravating detail: the committing script that
  *was* run belonged to the **previous unit** (calibration), indicating an evidence-assembly copy/paste
  slip. **Standing control reinforced:** for the remaining Wave-2 unit (W2-U10) and beyond, the
  committing-script + `SELECT ≥1 row` proof for each new persisted artifact is a **first-submission
  gating item**; a further recurrence escalates to HIGH.
- **OBSERVATION (benign) — routes grep false-positive.** `persistence.py:62/64 order=asc|desc` is the candle
  sort parameter, not an order/execution path. No concern.
- **NOT a FAIL / NOT a regression:** economic-validation functionality (incl. the headline independence and
  the no-execution boundary) is proven; nothing contradicted. Narrow single-item CONDITIONAL + a process
  finding on the recurrence.

---

## 3. Required Correction (the only thing between W2-U09 and approval)

- **C-1:** deliver the **committing-script persisted-PG proof for the ECONOMIC report** (per §2) —
  operator-run, Windows + PostgreSQL, `SELECT` returning ≥1 row for `economic_reports` **and** the
  `economic_report` audit event. **Verify the script targets the economic report, not calibration.** Do not
  re-run the rolled-back tests or the wrong committing script.

Everything else is accepted; do not redo it.

---

## 4. What is already solid (do not redo)

Economic function fully proven by named `-vv` tests on target: cost model + provenance/sensitivity (R-4),
independent statistical/economic conclusions, the **statistically-positive-but-economically-negative**
headline, conflation/undeclared-cost rejections, scenario sensitivity + per-slice, no-execution/no-signal
(structural + grep). Suite 152 green on PG; migrate `0013 (head)`; CI green through completion; parity smoke
green; pure-Python (no wheel risk). Only the *economic-report persistence capture* is owed.

---

## 5. Evidence Confidence Statement (R6 — no fabricated percentages)

**Confidence W2-U09 is approvable once C-1 lands: HIGH.** The economic-validation framework is functionally
demonstrated on the target (152 on PG, six named tests incl. the independence headline and no-execution
boundary), CI green through completion, envelope intact. **Confidence it is *currently* proven to standard:
LIMITED — solely because the persisted-PostgreSQL economic record (C-1) was not delivered (wrong committing
script pasted).** One correctly-targeted committing proof — the DA's own method — converts this to APPROVED.

---

## 6. Commendation & process note

The economic-validation design is excellent and squarely on-spec: statistical and economic conclusions kept
**independent**, the "significant-but-unusable" case surfaced explicitly, cost provenance/sensitivity
enforced (R-4 discharged), and the no-execution boundary proven — all research-only, gate CLOSED. The lone
failure is **evidence assembly**: the persisted-PG proof for the new (economic) artifact was omitted and the
prior unit's calibration committing script was pasted instead. Because this capture gap has now recurred
four times — and once *after* the standing instruction — it is escalated to a MEDIUM process finding. The
fix is trivial and functional approval is imminent; the escalation is about discipline, not the code.

---

## 7. Disposition

- **W2-U09: CONDITIONAL — APPROVAL WITHHELD (C-1 only) + MEDIUM process finding (persistence-capture
  recurrence).** Platform stays **v0.20.0** for gating (DA 0.21.0 provisional).
- **R-4 (cost-input provenance/sensitivity): SATISFIED in code** (closed on approval).
- **Gate posture unchanged:** research-only; no execution/orders/broker/live signal (proven); Wave 6/Wave 3
  reserved; broker gate CLOSED.
- **Next:** DA resubmits **only the C-1 committing-script persisted-PG ECONOMIC-report proof** (operator-run,
  Win+PG, verified to target `economic_reports`). On that single artifact, ITRGA approves W2-U09 and then
  authorizes **W2-U10 = Multi-Market Generalization + Model Registry / Drift** (the LAST Wave-2 unit → then
  *Research Framework Complete*). The DA does not self-authorize W2-U10 or open the broker gate.

---

*ITRGA — The economics are right: the framework reports the statistical verdict and the after-costs verdict
side by side, and it says plainly when a significant model still loses money. But the proof that the economic
report lives on PostgreSQL never came — the committing script that ran was last unit's calibration proof
pasted by mistake. Fourth time for this exact gap, first since we made it a standing rule, so it is now a
process finding, not just a re-request. Persist ONE economic report, select it, confirm it's the economic
table — and this is approved. We don't guess. We prove.*
