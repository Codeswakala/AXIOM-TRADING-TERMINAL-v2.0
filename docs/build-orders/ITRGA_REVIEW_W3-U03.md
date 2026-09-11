# ITRGA INDEPENDENT TECHNICAL REVIEW — W3-U03

## Live Research Advisor: Operating-Domain + Calibration/Economic Guardrails at Emit Time (+ signal staleness)

**Review ID:** ITRGA-REVIEW-W3-U03
**Unit:** W3-U03 · **Wave:** 3 — Live Research Advisor · **Unit:** 03
**Reviewer:** ITRGA · **Date:** 2026-07-15
**Inputs reviewed:** `DELIVERY_REPORT_W3-U03.md`; operator console transcript (`operator results.md`, 1765
lines; Windows/PowerShell + PostgreSQL 18); cross-checked against `BUILD_ORDER_W3-U03.md`, the accepted
Wave-3 plan (§7/§8, R-2), W2-U08/U09/U10 + W3-U01/U02, `05 v2.0` (§6/§15/§16/§77).
**Motto:** *We don't guess. We prove.*

---

## 0. VERDICT

> ## ✅ **APPROVED** — Platform **v0.25.0** — emit-time guardrails proven; R-2 (staleness) closed
>
> W3-U03 hardens the per-signal emit-time checks on **operator-run, target-platform Level-I evidence** — and
> it is the most complete Wave-3 delivery yet, closing every prior LOW note. Even an *eligible*
> `advisory_approved` model's signal is now **withheld / `warning` / `expired`** by name when out-of-domain,
> poorly-calibrated, economically-unusable, or stale — and **the guardrails are proven non-bypassable.**
> The persisted-PG proof is delivered in **both forms**: a raw `psql SELECT … FROM advisory_signals` →
> **`(5 rows)`** showing all five guardrail outcomes with freshness/validity/expiry, a raw `audit_events` →
> **`(5 rows)`**, *and* the authenticated API read-back. **R-2 is closed:** `current_only=true` →
> `EXPIRED_IN_CURRENT_COUNT_EXPECT_0: 0`. Clean PG migrate to `20260715_0017`, `pytest 177 passed`
> (171→177), ruff clean, frontend 16 + build, **CI green through completion (`LOCAL_CI_EXIT_CODE: 0`)**,
> parity smoke green. **No CRITICAL, no HIGH, no residual owed.**

**Why clean APPROVED:** every guardrail + the staleness contract + non-bypass are proven by named tests and
by a durable, dual-form persisted record; the two W3-U02 LOW notes (raw-SELECT form + CI marker) are both
discharged; the signal remains inert with no execution. Per proportionality (R13), a clean approval — and
this delivery is a model of the evidence standard.

---

## 1. Mandatory §5 Evidence — Line-by-Line Verification

| # | Required | Verdict | Basis |
|---|----------|---------|-------|
| 1 | Wheel spike (if compiled) | ✅ **N/A** | pure-Python. |
| 2 | pytest ≥171+new 0 failed; vitest 16; ruff; tsc/build | ✅ **PROVEN** | `177 passed … in 173.83s`; `All checks passed!`; `Tests 16 passed (16)`; audit 0. Backend 171→177 (+6). |
| 3 | Migration on PostgreSQL, new head | ✅ **PROVEN** | `20260715_0016 -> 20260715_0017, W3-U03 signal guardrail freshness fields` → `20260715_0017 (head)`. |
| 4 | Guardrails by name (captured `-vv`): domain / calibration / economic | ✅ **PROVEN** | `test_emit_time_provider_symbol_domain_guardrail_withheld_by_name`, `test_poor_calibration_ece_guardrail_warning_with_reason`, `test_economically_unusable_guardrail_warning_verdict_shown` — all PASSED. |
| 5 | **Staleness (R-2)**: stale → withheld; expired → not current | ✅ **PROVEN** | `test_stale_input_withheld_stale_input_reason` + `test_signal_past_validity_expired_and_not_returned_current` PASSED; API `current_only=true` → `EXPIRED_IN_CURRENT_COUNT_EXPECT_0: 0`. |
| 6 | Non-bypass | ✅ **PROVEN** | `test_guardrail_violating_case_cannot_be_forced_to_emitted PASSED`. |
| 7 | Calibrated-not-raw + economic independent | ✅ **PROVEN** | persisted rows: `calibration_status warning:POORLY_CALIBRATED` / `economic_verdict economically_unusable` distinct from score; raw score audit-only. |
| 8 | Inert / no-execution + read-only API | ✅ **PROVEN** | three empty greps (signal code/routes/frontend); no signal UI; API **401 / 200 / 405** (POST rejected). |
| 9 | **Persisted-PG proof (BOTH forms, first submission)** | ✅ **PROVEN (exceeds)** | raw `psql SELECT … advisory_signals` → **`(5 rows)`** (`withheld/UNSUPPORTED_DOMAIN`, `warning/POORLY_CALIBRATED`, `warning/ECONOMICALLY_UNUSABLE`, `withheld/STALE_INPUT`, `expired/SIGNAL_EXPIRED` + freshness/validity/expires_at); raw `audit_events` → **`(5 rows)`** (`advisory_signal.withheld/warning/expired`); **plus** authenticated API read-back. Closes the W3-U02 raw-SELECT LOW. |
| 10 | CI green on PostgreSQL through completion (marker inline) | ✅ **PROVEN** | `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0` (inline **and** grepped from `W3-U03_LOCAL_CI_TRANSCRIPT.txt:355`). Closes the W3-U02 CI-marker LOW. |
| 11 | Parity smoke | ✅ **PROVEN** | `WS-TICKET status: 200`; `persist_errors: 0`; `last_error: null`. |

**Net: 11/11 proven; two exceed (dual-form persistence, CI marker inline+file). Every prior LOW discharged.**

---

## 2. Governance Envelope — Compliance

| Constraint | Verdict | Basis |
|------------|---------|-------|
| ❌ No execution / order / broker; signal inert; gate CLOSED (R17) | ✅ Upheld | 3 empty greps + no order columns; broker gate green in the 177. |
| ❌ No guardrail-violating emission; non-bypassable | ✅ Upheld | each guardrail withholds/warns by name; non-bypass test PASSED. |
| ❌ No stale signal shown current (R-2) | ✅ Upheld | stale→withheld; expired→`SIGNAL_EXPIRED`; `current_only` excludes expired (count 0). |
| ❌ No raw-score-as-confidence; stat/econ independent | ✅ Upheld | calibrated status + economic verdict persisted independently. |
| ❌ No UI/alert/live push this unit | ✅ Upheld | frontend grep empty; read-only history API only. |
| ❌ No regression (Wave-0/1 + W2 + W3-U01/U02) | ✅ Upheld | 177 passed incl. all prior suites + gates; parity smoke green. |

---

## 3. Findings (classified — R8)

**No CRITICAL. No HIGH. No MEDIUM. No LOW residual owed.**

- **OBSERVATION (informational, commendable) — both W3-U02 LOW notes closed proactively.** The raw
  `psql SELECT` (alongside the API read-back) and the CI completion marker (inline + from file, exit 0) were
  both delivered without a re-request. The persistence-capture control is now consistently honored.
- **OBSERVATION (informational) — TD-056 background-expiry worker deferred.** The DA correctly notes there
  is no background worker to flip signals to `expired` on a timer; instead the `current_only` API filter
  prevents an expired record from ever being *returned as current* (proven, count 0). That is a sound
  interim design; the worker is a legitimate later operational item. No action.
- **RECOMMENDATION (W3-U05, when UI arrives):** the operator dashboard must render the guardrail outcome
  prominently — a `warning`/`withheld`/`expired` signal must be *visibly* not a clean recommendation (ties
  to design-plan R-3). Carry forward.

No finding withholds or qualifies approval.

---

## 4. Evidence Confidence Statement (R6 — no fabricated percentages)

**Confidence in this APPROVAL: HIGH.** Every guardrail (domain/calibration/economic), the staleness contract
(R-2), and non-bypass are backed by named `-vv` tests and by a **dual-form persisted record on PostgreSQL**
(raw SELECT `(5 rows)` + audit `(5 rows)` + authenticated API read-back), with `current_only` proven to
exclude the expired signal (count 0). CI is green through completion (exit 0), the signal stays inert (three
empty greps), and the API is read-only (401/200/405). No residual, no contradiction. HIGH.

---

## 5. Commendation (earned)

The most complete Wave-3 delivery to date: six guardrail/staleness guarantees proven by name **including
non-bypass**, persistence shown in both the raw-SELECT and API-read-back forms, the staleness harm
(stale-shown-as-current) closed with a measured `count 0`, and the two lingering W3-U02 LOW notes discharged
without prompting. This is the evidence discipline the riskiest wave demands, delivered cleanly on first
submission.

---

## 6. Disposition

- **W3-U03: APPROVED.** Platform **v0.25.0**. Design-plan **R-2 (staleness) CLOSED.**
- **Residuals: NONE owed.** TD-056 (background expiry worker) deferred, correctly mitigated by the API
  filter. Carry design-plan R-3 (UI advisory framing) → W3-U05.
- **Gate posture unchanged:** research/advisory only — inert signal; **no operator UI/alert/live push yet,
  no execution (Wave 6), broker gate CLOSED.**
- **Next:** ITRGA recommends authorizing **W3-U04 = Live Market Inference Adapter** (accepted plan §13) —
  feed live/near-real-time market data into inference input through the existing query/live seam (reuse the
  W1 WebSocket seam; no external broker/feed), with **as-of / no-look-ahead discipline** and deterministic
  scoring; still no UI/alerts/execution; persisted proof (both forms) first submission. The DA does not
  self-authorize W3-U04, push a live signal to an operator surface, or open the broker gate. Await operator
  direction + a new Build Order.

---

*ITRGA — Eligibility earned the right to speak; now the signal knows its limits and its age. Out of domain,
poorly calibrated, economically unusable, or stale — it withholds, warns, or expires, provably and
non-bypassably, and an expired advisory is never returned as current. Five outcomes, five audited rows,
proven twice over on PostgreSQL. The platform speaks only within what it has proven — and still does not act.
We don't guess. We prove.*
