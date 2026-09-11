# ITRGA INDEPENDENT TECHNICAL REVIEW — W2-U08

## ML Research: Calibration + Probability Quality Framework

**Review ID:** ITRGA-REVIEW-W2-U08
**Unit:** W2-U08 · **Wave:** 2 — ML Research Framework · **Unit:** 08
**Reviewer:** ITRGA · **Date:** 2026-07-14
**Inputs reviewed:** `DELIVERY_REPORT_W2-U08.md`; operator console transcript (`operator results.md`, 941
lines; Windows/PowerShell + PostgreSQL 18, Python 3.14.6); cross-checked against `BUILD_ORDER_W2-U08.md`
(incl. the **blocking base-rate-null criterion** escalated at the W2-U07 re-review), `07_ML_SPEC`
§Statistical Validation, D-W2-001.
**Motto:** *We don't guess. We prove.*

---

## 0. VERDICT

> ## ⚠️ **CONDITIONAL — APPROVAL WITHHELD** (one item: persisted-PG calibration report)
>
> The W2-U08 **implementation is strong and the blocking criterion is met**: the **base-rate-aware
> significance null** is proven (`test_base_rate_null_majority_baseline_not_significant_skill PASSED` by
> name — the W2-U07 carry-forward is discharged), miscalibration is **detected** (bad fixture flagged /
> good not flagged), Brier + ECE + reliability bins + per-slice calibration are delivered, a
> report-without-bins is rejected, `pytest 146 passed` on PostgreSQL, CI green through completion, parity
> smoke green. **But one mandatory §5 item is unmet:** the **persisted-PostgreSQL calibration-report proof
> (§5.8) returned `(0 rows)`** — no committing script was run, so the calibration report + audit events are
> not shown to *live on disk*.
>
> **This is the recurring persistence-capture gap (G-2 @ W2-U01, C-2 @ W2-U05) — third occurrence.** It is
> a capture gap, not a behaviour gap (the in-test persistence test passes), and the DA has already executed
> the exact fix twice. **One targeted re-capture converts this to APPROVED.**

**Why withheld, not approved-with-observations:** for a unit whose deliverable *is* a persisted research
report/governance artifact, the durable record on PostgreSQL is core evidence (R5 caps the verdict). The
Build Order §5.8 named it explicitly. **Why not a FAIL:** nothing failed and nothing is contradicted — the
functionality is proven by named tests; only the persistence *capture* is missing (contrast a real
regression). Hence a narrow CONDITIONAL, exactly as at W2-U05 correction #1.

---

## 1. Evidence Hierarchy Assessment (R2)

| Tier | Present? | Notes |
|------|----------|-------|
| Level-I — operator-run Win+PG (functionality) | ✅ | compat spike, pytest 146 on PG, 6 named tests incl. base-rate-null + miscalibration pair, greps, CI green, smoke |
| Level-I — **persisted-PG report/audit record** | ❌ `(0 rows)` | §5.8 unmet — no committing script (C-1) |
| Level-II — DA sandbox (SQLite) | ✅ | 146/16 — corroborating |
| Level-IV — report claims | ✅ | present; not the approval basis (R1) |

---

## 2. Mandatory §5 Evidence — Line-by-Line Verification

| # | Required (Build Order §5) | Verdict | Basis |
|---|---------------------------|---------|-------|
| 1 | (If compiled dep) wheel spike | ✅ **N/A (pure-Python)** | `CALIBRATION_STACK: pure-python-stdlib`, `NO_COMPILED_CALIBRATION_DEPENDENCY: True`. |
| 2 | pytest ≥140+new 0 failed; vitest 16; ruff; tsc/build | ✅ **PROVEN** | `146 passed … in 64.86s`; `All checks passed!`; `Tests 16 passed (16)`. Backend 140→146 (+6). |
| 3 | Migration on PostgreSQL, new head | ✅ **PROVEN** | `20260714_0011 -> 20260714_0012, W2-U08 calibration reports` → `20260714_0012 (head)` on `PostgresqlImpl`. |
| 4 | Calibration: reliability curve + Brier + ECE + bins | ✅ **PROVEN** | `test_calibration_curve_brier_ece_and_per_slice_shape PASSED`; config `bin_count=10, equal_width, warning_threshold_ece=0.15`. |
| 5 | **Miscalibration detection pair** (`-vv`) | ✅ **PROVEN** | `test_miscalibrated_fixture_flagged_and_well_calibrated_not_flagged PASSED` (dedicated `-vv`) → `POORLY_CALIBRATED`. |
| 6 | **Base-rate-null (BLOCKING carry-forward)** (`-vv`) | ✅ **PROVEN — blocking criterion MET** | `test_base_rate_null_majority_baseline_not_significant_skill PASSED` (dedicated `-vv`); §3.5 `base_rate=max(pos,neg); skill_over_base_rate=accuracy-base_rate`. The W2-U07 escalation is satisfied. |
| 7 | Reproducibility (seeded → same) | ✅ **PROVEN (test-level)** | `test_calibration_report_persisted_and_reproducible PASSED` (named `-vv`). |
| 8 | **Persisted-PG proof (committing script)** | ❌ **C-1 NOT SHOWN** | `SELECT … FROM calibration_reports` → **`(0 rows)`**; `SELECT … FROM audit_events WHERE resource_type='calibration_report'` → **`(0 rows)`**. The line-3 `python -c` is the compat spike, **not** a committing persistence script. §5.8 unmet. |
| 9 | No identity-as-feature / no live-signal grep | ✅ **PROVEN** | two shown greps → empty (`symbol_id\|…` in `app\ml\calibration`; `model/signal\|predict\|inference\|live_signal` in routes). |
| 10 | CI green on PostgreSQL (capture completion) | ✅ **PROVEN** | `==> Local CI equivalent complete` (line 798) — the W2-U07 LOW note is addressed. |
| 11 | Parity smoke | ✅ **PROVEN** | `WS-TICKET status: 200`; `persist_errors: 0`; `last_error: null`. |
| 12 | Confidence, no fabricated % | ✅ **COMPLIANT** | per-dimension; no percentage asserted. |

**Net:** 11 of 12 proven — including the **blocking base-rate-null criterion** and the miscalibration
headline. The single unmet item is the persisted-PG record (C-1).

---

## 3. Governance & the escalated criterion

- **Base-rate-null (escalated to blocking at the W2-U07 re-review): SATISFIED.** `§3.5` implements the
  No-Information-Rate null and the named test proves a majority baseline is **not** reported as significant
  skill against it — closing the W2-U07 misleading-significance artifact. Good.
- **Envelope upheld** (proven): no new model/live signal/economic/execution; broker gate CLOSED; D-W2-001
  slicing-not-feature (grep empty); calibration report `research_only`; no regression (146 incl. all prior
  suites; CI + smoke green).

---

## 4. Findings (classified — R8)

- **C-1 (HIGH — unmet mandatory evidence; recurring pattern, 3rd occurrence).** The persisted-PostgreSQL
  calibration-report + audit proof (§5.8) is absent — the `SELECT`s returned `(0 rows)` because only the
  rolled-back tests + the compat-spike heredoc ran; **no committing script persisted a report.** This is the
  identical gap the DA *closed correctly* at **W2-U05 (C-2)** and **W2-U07** (committing heredoc → `(1 row)`).
  **Required (C-1):** a committing script (`… | python -`) that computes + persists one calibration report
  on PostgreSQL (register/compute → commit), then the two `psql SELECT`s returning **≥1 row** each
  (`calibration_reports` with brier/ECE/base_rate/base_rate_significance/report_hash/research_only, and the
  `calibration_report` audit event). No code change expected — reuse the proven method.
- **OBSERVATION (process, escalating) — persistence-capture is now a *repeat* miss across units.** The DA
  reliably proves persistence *in-test* but intermittently omits the *committing* proof (W2-U01, W2-U05, now
  W2-U08). **Standing instruction going forward:** any unit that persists a new report/artifact type MUST
  include the committing-script + `SELECT ≥1 row` proof in its *first* submission. Tracked; if it recurs
  again after this, it escalates to a MEDIUM process finding on the offending unit.
- **NOT a FAIL / NOT a regression:** functionality (incl. the blocking base-rate-null) is proven by named
  tests; nothing is contradicted. Narrow single-item CONDITIONAL.

---

## 5. Required Correction (the only thing between W2-U08 and approval)

- **C-1:** deliver the **committing-script persisted-PG proof** for one calibration report (per §4) —
  operator-run, Windows + PostgreSQL, `SELECT` returning ≥1 row for `calibration_reports` **and** the
  `calibration_report` audit event. Do **not** re-run the rolled-back tests or the post-test `SELECT` again;
  they are already accepted for what they prove (in-memory behaviour).

Everything else is accepted; do not redo it.

---

## 6. Evidence Confidence Statement (R6 — no fabricated percentages)

**Confidence W2-U08 is approvable once C-1 lands: HIGH.** The calibration framework is functionally
demonstrated on the target (146 on PG, six named tests incl. the miscalibration pair and the **blocking
base-rate-null**), CI is green through completion, and the envelope holds. **Confidence it is *currently*
proven to standard: LIMITED — solely because the persisted-PostgreSQL calibration record (C-1) is unshown.**
One committing proof — a method the DA has executed twice — converts this to APPROVED.

---

## 7. Commendation (genuine — but does not close C-1)

The DA discharged the escalated W2-U07 correction cleanly (base-rate-aware null, proven by name), delivered
the miscalibration-detection pair exactly as specified, kept the stack pure-Python (no wheel risk), and —
addressing the prior LOW note — **captured the CI completion marker** this time. The lone shortfall is the
persisted-PG report capture, which is quick and already in the DA's repertoire. Strong unit, one artifact short.

---

## 8. Disposition

- **W2-U08: CONDITIONAL — APPROVAL WITHHELD (C-1 only).** Platform stays **v0.19.0** for gating (DA's
  0.20.0 provisional pending approval).
- **Escalated base-rate-null criterion: SATISFIED** (no longer blocking).
- **Gate posture unchanged:** research-only; no live signals (Wave 3); no execution (Wave 6); broker CLOSED.
- **Next:** DA resubmits **only the C-1 committing-script persisted-PG proof** (operator-run, Win+PG). On
  that single artifact, ITRGA approves W2-U08 and then authorizes **W2-U09 = Economic Validation Framework**.
  The DA does not self-authorize W2-U09 or open the broker gate.

---

*ITRGA — The calibration layer works and the base-rate ghost is finally exorcised: the miscalibrated model
is caught, and the majority baseline no longer masquerades as skill. One thing missing — the calibration
report proven alive on PostgreSQL, the same committing proof you've shown twice before. Persist one report,
select it, and this is approved. We don't guess. We prove.*
