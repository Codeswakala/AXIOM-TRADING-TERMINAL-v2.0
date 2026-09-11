# ITRGA INDEPENDENT TECHNICAL REVIEW — W3-U06

## Live Research Advisor: Monitoring, Drift & Health Alerts (inform a human, never act)

**Review ID:** ITRGA-REVIEW-W3-U06
**Unit:** W3-U06 · **Wave:** 3 — Live Research Advisor · **Unit:** 06
**Reviewer:** ITRGA · **Date:** 2026-07-15
**Inputs reviewed:** `DELIVERY_REPORT_W3-U06.md`; operator console transcript (`operator results.md`, 1445
lines; Windows/PowerShell + PostgreSQL 18); cross-checked against `BUILD_ORDER_W3-U06.md`, the accepted
Wave-3 plan §9, `07_ML_SPEC` §Drift, W1-U02/W2-U10, `05 v2.0` (§15/§16/§77), R-3.
**Motto:** *We don't guess. We prove.*

---

## 0. VERDICT

> ## ✅ **APPROVED** — Platform **v0.28.0** — alerts inform, never act; proven by the "changes nothing" test
>
> W3-U06 surfaces market/health/drift conditions as **inert, persisted, audited operator alerts** on
> **operator-run, target-platform Level-I evidence** — and it proves the wave's defining live-layer
> constraint by name: **a drift alert triggers no retrain, no model-change, no order, no auto-action**
> (`test_drift_alert_triggers_no_retrain_model_change_order_or_auto_action PASSED`), and **acknowledging an
> alert does not mutate the subject model** (`test_monitoring_alert_ack_does_not_mutate_subject_model
> PASSED`). The alert table is inert (no order/remediation/execution/model-mutation columns), the API is
> read-only (**401 / 405**, ack = read-state only), and three no-auto-action/no-execution greps — including
> model-mutation patterns (`auto_retrain\|model.status =\|advisory_status =`) — are **empty.** Persisted proof
> is delivered in **both forms** (`monitoring_alerts (2 rows)` + `audit_events (5 rows)` + API read-back).
> Clean PG migrate to `20260715_0018`, `pytest 188 passed` (183→188), frontend 20, CI green through
> completion, parity smoke green. **No CRITICAL, no HIGH, no residual owed.**
>
> The platform now watches itself and warns the operator — and a warning moves nothing but a human's
> attention.

**Why clean APPROVED:** the single brightest constraint (alerts inform, never act; drift ≠ auto-retrain) is
proven by *named negative tests* + grep + an inert schema, the alerts are persisted/audited/read-only, and
nothing crosses the advisory→action line. Per proportionality (R13), a clean approval.

---

## 1. Mandatory §5 Evidence — Line-by-Line Verification

| # | Required | Verdict | Basis |
|---|----------|---------|-------|
| 1 | pytest ≥183+new / vitest ≥20 / ruff / tsc / build | ✅ **PROVEN** | `188 passed` (183→188, +5); `All checks passed!`; frontend `20 passed`; build ok. |
| 2 | Migration on PostgreSQL, new head | ✅ **PROVEN** | `20260715_0017 -> 20260715_0018, W3-U06 monitoring alert records` → `20260715_0018 (head)`. |
| 3 | Alert-generation (captured `-vv`) | ✅ **PROVEN** | drift alert created (`DRIFT_TYPE: DRIFT_DETECTED`); alert types per §9.4; monitoring reuses W1-U02/W2-U10. |
| 4 | **No-auto-action (headline, captured `-vv`) + grep** | ✅ **PROVEN** | `test_drift_alert_triggers_no_retrain_model_change_order_or_auto_action PASSED`; grep `place_order\|cancel_order\|broker.\|execute\|auto_retrain\|model.status =\|advisory_status =\|order_payload\|remediation_payload` → **empty** (3 greps). |
| 5 | Monitoring does not mutate model/config | ✅ **PROVEN** | `test_monitoring_alert_ack_does_not_mutate_subject_model PASSED`; report §3 (`create_drift_alert` does not retrain/mutate). |
| 6 | Inert + read-only alerts API | ✅ **PROVEN** | table has no order/remediation/execution/model-mutation columns; `UNAUTH_ALERTS_STATUS: 401`; `POST_ALERT_COLLECTION_STATUS_EXPECT_405: 405`; ack = read-state only. |
| 7 | **Persisted-PG proof (both forms, first submission)** | ✅ **PROVEN** | raw `SELECT … monitoring_alerts` **`(2 rows)`** + `audit_events` **`(5 rows)`** (`monitoring_alert.created` + `monitoring_alert.acknowledged`) + authenticated API read-back (`alert_type: DRIFT_DETECTED`). |
| 8 | CI green on PostgreSQL through completion | ✅ **PROVEN (LOW: exit-0 echo not inline)** | orchestrated CI ran deps→alembic→ruff→`pytest 188`→frontend→build ✓→`==> Local CI equivalent complete`; **no `exit 1`** anywhere. The explicit `LOCAL_CI_EXIT_CODE: 0` echo isn't captured (transcript ends at the marker) — non-blocking. |
| 9 | Parity smoke | ✅ **PROVEN** | `WS-TICKET status: 200`; `persist_errors: 0`; `last_error: null`. |
| 10 | Confidence, honest | ✅ **COMPLIANT** | per-dimension; no fabricated %. |

**Net: every mandatory item proven, incl. the headline no-auto-action by name + inert schema + dual-form
persistence.**

---

## 2. Governance Envelope — Compliance (the live-layer bright line)

| Constraint (§9.3 / W2-U10 / R17) | Verdict | Basis |
|----------------------------------|---------|-------|
| ❌ No auto-action / auto-remediation (drift alert acts on nothing) | ✅ Upheld | headline negative test + grep; inert schema; drift alert doesn't retrain/mutate/order. |
| ❌ Monitoring does not mutate model/config | ✅ Upheld | ack-no-mutate test; monitoring reads only. |
| ❌ No execution / order / broker; gate CLOSED | ✅ Upheld | greps empty; broker gate green in the 188. |
| ❌ Alert inert + persisted + audited | ✅ Upheld | no action payload; `(2 rows)` + `(5 rows)` audit. |
| ❌ Read-only alerts surface (ack = read-state) | ✅ Upheld | 401 / 405; ack audited as read-state. |
| ❌ No regression | ✅ Upheld | 188 / 20 green; CI green; parity smoke; prior gates intact. |

**A warning is only ever a warning.** The flow still ends at Operator Decision (§15); the platform watches,
reasons, alerts — and does not act.

---

## 3. Findings (classified — R8)

**No CRITICAL. No HIGH. No MEDIUM. No residual owed.**

- **OBSERVATION (LOW, recurring) — `LOCAL_CI_EXIT_CODE: 0` echo not captured inline.** The CI reached its
  completion marker with all gates green and no `exit 1`, which is sufficient; the explicit `: 0` echo would
  make it airtight. Cosmetic; show it next unit.
- **OBSERVATION (commendable) — the no-mutation grep was rigorous.** Checking `auto_retrain`, `model.status
  =`, `advisory_status =`, `order_payload`, `remediation_payload` (not just execution verbs) is exactly the
  right scrutiny for a monitoring unit — it proves the alert can't quietly *change* the thing it watches.
- **OBSERVATION (informational) — no alert UI indicator added this unit.** Correctly scoped (report §3): the
  alert is backend + read-only API; a UI indicator can come later without an execution surface. No action.

No finding withholds or qualifies approval.

---

## 4. Evidence Confidence Statement (R6 — no fabricated percentages)

**Confidence in this APPROVAL: HIGH.** The defining constraint — alerts inform and never act — is proven by
two named negative tests (drift-alert-does-nothing; ack-does-not-mutate), an inert schema (no order/
remediation/model-mutation columns), three empty rigorous greps, a read-only API (401/405), and a dual-form
persisted+audited record on PostgreSQL, with the full suite (188) and CI green through completion and a green
parity smoke. The one LOW note (exit-0 echo) does not affect any guarantee. HIGH.

---

## 5. Commendation (earned)

The monitoring layer holds the live-layer bright line exactly: it lets the platform *warn* a human about
drift, staleness, degraded health, and withheld signals — and proves, by "changes nothing" tests and a
model-mutation-aware grep, that a warning **retrains nothing, mutates no model, places no order, remediates
nothing.** Inert, persisted, audited, read-only. This is the right shape for autonomy that stops at
informing a human.

---

## 6. Disposition

- **W3-U06: APPROVED.** Platform **v0.28.0**.
- **Residuals: NONE owed.** LOW: capture the `LOCAL_CI_EXIT_CODE: 0` echo inline next unit.
- **Gate posture unchanged:** research/advisory only — the platform now **alerts** the operator but **never
  acts**: no auto-retrain, no auto-remediation, no execution (Wave 6), no execution controls (R-3), broker
  gate CLOSED; flow ends at Operator Decision (§15).
- **Next:** ITRGA recommends authorizing **W3-U07 = Performance Analytics + Confidence Visualization**
  (accepted plan §13) — advisory *research* performance analytics with **uncertainty shown (no false
  precision)** and clear advisory labelling (not guaranteed performance), building on W2-U07 statistical
  discipline; presentation-only, no execution, browser evidence if UI. The DA does not self-authorize
  W3-U07, add any auto-action/execution, or open the broker gate. Await operator direction + a new Build
  Order.

---

*ITRGA — The platform now watches itself and warns the operator — drift, stale data, degraded health, a
withheld signal — and a warning was proven to be only ever a warning: it retrains nothing, changes no model,
places no order, remediates nothing, and cannot mutate what it watches. Inert, persisted, audited, read-only.
The platform watches, reasons, and alerts; it still does not act. We don't guess. We prove.*
