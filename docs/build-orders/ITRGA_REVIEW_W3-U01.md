# ITRGA INDEPENDENT TECHNICAL REVIEW — W3-U01

## Live Research Advisor: Live Inference Engine + Governed Model Eligibility Gate (backend-only safe slice)

**Review ID:** ITRGA-REVIEW-W3-U01
**Unit:** W3-U01 · **Wave:** 3 — Live Research Advisor · **Unit:** 01 (first Wave-3 unit)
**Reviewer:** ITRGA · **Date:** 2026-07-15
**Inputs reviewed:** `DELIVERY_REPORT_W3-U01.md`; operator console transcript (`operator results.md`, 1296
lines; Windows/PowerShell + PostgreSQL 18); cross-checked against `BUILD_ORDER_W3-U01.md`, the accepted Wave-3
design plan (`ITRGA_REVIEW_WAVE3_DESIGN_PLAN.md`, incl. R-1), `05 v2.0` (§6/§15/§16/§42/§77), `07_ML_SPEC`
§Deployment Policy, D-W2-001.
**Motto:** *We don't guess. We prove.*

---

## 0. VERDICT

> ## ✅ **APPROVED** — Platform **v0.23.0** — the advisory safety foundation is proven
>
> W3-U01 delivers the backend safety foundation of the Live Research Advisor on **operator-run,
> target-platform Level-I evidence**, and — for the first time on a persisted-artifact unit — **honors the
> persistence-capture control on the first submission.** **Inference is deterministic** (`SCORE_1 = SCORE_2 =
> 0.7082440809163256`); the **eligibility gate refuses every ungoverned/ineligible case by name**; the
> **governed advisory promotion (R-1)** requires approver + reason + UTC + audit and is proven **persisted on
> PostgreSQL** (`advisory_approved | operator-evidence | 2026-07-15 14:11:47` + `model.advisory_approved`
> audit); the **no-execution bright line** is shown by two empty greps + a structural test; and **no
> operator-facing signal/UI/alert exists** in this unit. Clean PG migrate to `20260715_0015`, `pytest 164
> passed` (159→164), ruff clean, frontend 16 + build, broker gate still CLOSED, parity smoke green. **No
> CRITICAL, no HIGH, no residual owed.**
>
> This is the checked precondition for everything that follows: **only a fully-Wave-2-governed,
> formally-approved model can ever become eligible to speak — and no execution path exists.**

**Why clean APPROVED:** the unit's entire purpose — make "only a governed, approved model is eligible" and
"no execution" *proven preconditions* — is met by named tests + a persisted governed-promotion record + shown
greps. The R-1 refinement is discharged. Per proportionality (R13), a clean approval is correct.

---

## 1. Mandatory §5 Evidence — Line-by-Line Verification

| # | Required | Verdict | Basis |
|---|----------|---------|-------|
| 1 | Wheel spike (if compiled) | ✅ **N/A** | pure-Python inference/gate (no compiled dep). |
| 2 | pytest ≥159+new 0 failed; vitest 16; ruff; tsc/build | ✅ **PROVEN** | `164 passed … in 95.18s`; `All checks passed!`; `Tests 16 passed (16)`. Backend 159→164 (+5). |
| 3 | Migration on PostgreSQL, new head | ✅ **PROVEN** | `20260715_0014 -> 20260715_0015, W3-U01 advisory status fields` → `20260715_0015 (head)` on `PostgresqlImpl`. |
| 4 | Determinism (captured `-vv`, same input+version→same score+hash) | ✅ **PROVEN** | `test_deterministic_inference_same_input_same_score_and_hash PASSED`; committing script: `SCORE_1: 0.7082440809163256` = `SCORE_2: 0.7082440809163256`. |
| 5 | Eligibility refusals by name (captured `-vv`) | ✅ **PROVEN** | `test_eligibility_refusals_by_reason PASSED`; report §3.3 reason set incl. `MISSING_STATISTICAL/CALIBRATION/ECONOMIC/GENERALIZATION_REPORT`, `NOT_ADVISORY_APPROVED`, `FEATURE_VERSION_MISMATCH`, `IDENTITY_IN_INFERENCE_INPUT`. |
| 6 | **Governed promotion (R-1): refused w/o lineage, refused w/o approval, audited on success; only advisory_approved eligible** | ✅ **PROVEN** | `test_governed_promotion_refused_without_lineage_and_audited_on_success PASSED`; committing script `promote_to_advisory_approved(approver=…, approval_reason=…)`. |
| 7 | Identity/domain/chronology input refusals | ✅ **PROVEN** | `test_identity_out_of_domain_future_and_synthetic_inputs_refused PASSED` (`IDENTITY_IN_INFERENCE_INPUT`/`UNSUPPORTED_DOMAIN`/`FUTURE_INFERENCE_INPUT`/`SYNTHETIC_AUTHORITATIVE_INPUT_REFUSED`). |
| 8 | **No-execution bright line** (grep R7 + structural) | ✅ **PROVEN** | `test_no_execution_signal_or_broker_path_in_inference_modules PASSED`; two shown greps (`place_order\|cancel_order\|broker.\|live_signal\|emit_signal`) over inference modules + routes → **empty**. |
| 9 | **Persisted-PG proof (committing script, correct table, FIRST submission)** | ✅ **PROVEN** | `SELECT … FROM model_artifacts` → `(1 row)`: `advisory_status advisory_approved / advisory_approved_by operator-evidence / advisory_approved_at 2026-07-15 14:11:47`; `SELECT … audit_events` → `(1 row)` `model.advisory_approved | model_artifact`. Correct table; no re-paste. |
| 10 | No-signal-surface confirmation | ✅ **PROVEN** | No signal route/UI/emit added (report §3.5 + no-signal grep); broker `test_broker_integration.py` still green in the 164 (gate intact). |
| 11 | CI green on PostgreSQL through completion | ⚠️ **PARTIAL (LOW)** | `local_ci.sh` ran (deps→alembic-PG→ruff→`==> Pytest`) but the transcript **cuts off mid-CI** — no `Local CI equivalent complete` marker. **Non-blocking:** R-CI-01 is a standing preference; the gates are independently green (standalone 164 / ruff / vitest 16 / build). |
| 12 | Parity smoke | ✅ **PROVEN** | `WS-TICKET status: 200`; `persist_errors: 0`; `last_error: null`. |

**Net:** every mandatory functional + governance item proven, incl. the R-1 governed promotion and the
persisted-PG advisory record on first submission. The one soft spot is a truncated CI capture (LOW,
non-blocking).

---

## 2. Governance Envelope — Compliance (the brightest line, this wave)

| Constraint (Build-Order §2) | Verdict | Basis |
|-----------------------------|---------|-------|
| ❌ No execution/orders/broker/paper trading; gate CLOSED (R17) | ✅ Upheld | two empty greps + structural test; broker gate tests still green; External Integration untouched. |
| ❌ No operator-facing signal/UI/alert/emission this unit | ✅ Upheld | report §3.5 + no-signal grep; backend-only. |
| ❌ No ineligible model eligible | ✅ Upheld | eligibility refusals by name; full U05–U10 lineage required. |
| ❌ No advisory_approved without governed audited approval + lineage (R-1) | ✅ Upheld | governed-promotion test + persisted `advisory_approved_by` + `model.advisory_approved` audit. |
| ❌ No non-deterministic inference (§42) | ✅ Upheld | SCORE_1 = SCORE_2 identical; input hash recorded. |
| ❌ No chronology/identity violation at input | ✅ Upheld | future/synthetic/identity input refusals. |
| ❌ No DB reach-around / no secrets | ✅ Upheld | via seams; no token in transcript. |
| ❌ No regression (Wave-0/1 + W2-U01–U10) | ✅ Upheld | 164 passed incl. all prior suites; parity smoke green. |

**The advisory-only bright line is proven, not asserted.** AXIOM cannot, in this unit, act — and only a
governed, approved model can even become eligible to (later) speak.

---

## 3. Findings (classified — R8)

**No CRITICAL. No HIGH. No MEDIUM. No residual owed.**

- **OBSERVATION (LOW) — CI completion marker not captured** (transcript truncated mid-`local_ci.sh`).
  Non-blocking: R-CI-01 is a standing preference and the constituent gates are independently green. Capture
  the completion marker next unit for tidiness.
- **COMMENDATION-worthy (noted here, not a finding) — persistence-capture control honored first-submission.**
  After the W2 recurrences (escalated to HIGH), W3-U01 shipped the committing-script persisted-PG proof for
  the new advisory-status/promotion record in its first delivery, correctly targeted. The control worked.
- **OBSERVATION (informational) — W3-U01 correctly builds NO signal surface.** The eligibility gate + engine
  exist; nothing emits to an operator yet. This is the intended sequencing (safety foundation before any
  signal). Carry the design-plan R-2 (staleness) and R-3 (UI advisory framing) into W3-U03/U04/U05.

No finding withholds or qualifies approval.

---

## 4. Evidence Confidence Statement (R6 — no fabricated percentages)

**Confidence in this APPROVAL: HIGH.** Every material claim is backed by operator-run Windows + PostgreSQL
Level-I evidence I verified directly — deterministic inference with identical scores, five named `-vv`
refusal/gate tests, a persisted governed-promotion record on PostgreSQL (advisory_approved + approver +
timestamp + audit), two empty no-execution greps + structural test, broker gate still CLOSED, and a green
parity smoke. The advisory-only bright line and the governed-model-only precondition are proven. The one LOW
note (truncated CI capture) does not affect any delivered guarantee. HIGH.

---

## 5. Commendation (earned)

The first Wave-3 unit lands the safety foundation exactly right: it builds the lock **before** the door, it
proves the ungoverned model is refused **before** any signal can reach a human, it makes "going live" a
governed, audited, persisted approval (R-1 discharged), and it shows — by grep and structure — that **no
execution path exists.** It also finally honored the persistence-capture control on first submission. This is
the disciplined posture the riskiest wave demands, applied from its first unit.

---

## 6. Disposition

- **W3-U01: APPROVED.** Platform **v0.23.0**.
- **Residuals: NONE owed.** LOW: capture the CI completion marker next unit. Carry design-plan R-2 (signal
  staleness) → W3-U03/U04 and R-3 (UI advisory framing) → W3-U05.
- **Gate posture unchanged:** research/advisory only — **no operator-facing signal yet, no execution (Wave
  6), broker gate CLOSED.**
- **Next:** ITRGA recommends authorizing **W3-U02 = Advisory Signal Contract + Signal Persistence** (accepted
  plan §13) — the inert advisory signal record (full lineage + calibrated confidence + rationale + audit),
  emitted/withheld states, signal-history API; **still no UI/alerts/execution**; persisted-artifact committing
  proof first submission; and it is the first unit where a *governed signal* is produced (from an
  `advisory_approved` model only) — so the eligibility gate + emit-time guardrails must gate emission. The DA
  does not self-authorize W3-U02, emit a live signal outside a governed unit, or open the broker gate. Await
  operator direction + a new Build Order.

---

*ITRGA — Before AXIOM speaks, the lock is built and proven: inference that is deterministic to the digit, a
gate that refuses every model that didn't earn its way through all of Wave 2, a "go-live" that is approved,
audited, and recorded on PostgreSQL, and — behind it all — no execution path at all. No signal left this
unit; it exists so that when one finally does, it could only have come from a model that earned the right.
The platform may advise; it may not act. We don't guess. We prove.*
