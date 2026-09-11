# BUILD ORDER — W6-U08 (Wave-6 Closeout & Hardening — FINAL UNIT)

## Execution Research Environment — Closeout, Whole-Wave Proof & Milestone

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Wave:** 6 — Execution Research · **Unit:** W6-U08 (closeout — the LAST unit) · **Policy:** one unit per Build Order
**Date:** 2026-07-18
**Platform of record (pre-unit):** v0.53.0 · Alembic head `20260717_0033` · backend **345 passed** · frontend **18 files / 58 tests**
**Governing docs:** accepted `WAVE6_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` §11 W6-U08 + §13 Bright-Line Self-Check; `ITRGA_REVIEW_WAVE6_DESIGN_PLAN.md` (R6-1…R6-8, GR6-1…GR6-13); `04_PROJECT_ROADMAP.md` (Wave 6 milestone "Execution Research Environment Complete"); `05_SYSTEM_ARCHITECTURE.md` v2.0 §15/§16/§43/§46; `10_CONSTITUTIONAL_HIERARCHY.md`.
**Constitutional posture:** Governance Gate **CLOSED** — this closeout must **prove it stayed CLOSED for the entire wave**. No new feature; a proof-of-the-whole + hardening unit.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

W6-U01…U07 delivered the Execution Research Environment (safety envelope → runs/fills → paper ledger → risk reports → replay/experiments → analytics → workspace UI). **W6-U08 proves the whole wave is sound and non-actuating**, hardens residuals, and — on clean approval — declares the milestone **"Execution Research Environment Complete."** This unit is not a new capability; it is the wave-wide evidence + reconciliation, following the W3-U08 / W4-U08 / W5-U08 closeout precedent.

---

## 2. Scope (build/prove exactly this)

1. **Whole-wave no-live-execution & Gate-CLOSED proof** (backend + frontend surfaces).
2. **Artifact no-orphan completeness** across ALL six Wave-6 tables.
3. **Browser E2E** across the Execution Research surface (research-framed, SIMULATED, no actuation), incl. the logged-out block done properly this time.
4. **Docs/register reconciliation** — CHANGELOG v0.53.0→v0.54.0, ADRs, and the technical-debt register; **resolve or formally carry TD-W6-CI-AUDIT**.
5. **No new table / no migration** — head stays `20260717_0033` (closeout unit). Any hardening test-only additions permitted; no new feature/capability.

---

## 3. Binding requirements (whole-wave)

- **GR6-1 / R6-4 Gate CLOSED wave-wide:** `test_governance_gate_remains_closed_for_wave6` + standing `test_broker_integration.py::test_governance_gate_refuses_connect_and_execute` green; broker connect/execute still refuse and audit (`GATE_CLOSED_*_REFUSED`).
- **GR6-2 / GR6-3 no live-execution path anywhere:** whole-wave bright-line grep over `backend/app/execution_research` + all W6 routes → clean; broker-specific logic contained to `external_integration` (§16 grep).
- **GR6-6 SIMULATED + inert everywhere:** every W6 artifact type carries `simulation_mode='SIMULATED'` / `research_status='research_only'` / disclaimer.
- **R6-9 no-orphan completeness (ALL six tables), raw psql on target:** `simulated_execution_runs`, `simulated_fill_events`, `simulated_paper_ledger_entries`, `execution_risk_research_reports`, `execution_research_experiments`, `simulated_execution_analytics_reports` — each with row_count ≥1 and its no-orphan audit JOIN → `orphan_count 0`.
- **GR6-5 / GR6-10 UI:** browser E2E showing SIMULATED framing + **no execution/actuation controls** + a proper **logged-out block** (this time with the URL bar showing `/execution-research` → login, OR an operator-run unauth HTTP check returning 401/302).
- **TD-W6-CI-AUDIT:** either produce a clean `LOCAL_CI_EXIT_CODE: 0` on a networked host, OR make the CI audit step degrade gracefully when the registry is unreachable and show exit 0; if still environmentally blocked, formally carry the TD with the substitute-proof note (operator-waived precedent).
- **No regression:** backend 345 + any new hardening tests green; frontend 18/58 (+ any additions) green.

---

## 4. Mandatory tests

```
test_wave6_bright_line_grep_no_live_execution_path            # whole-wave
test_governance_gate_remains_closed_for_wave6
test_broker_logic_contained_in_external_integration
test_all_wave6_simulated_tables_labelled_and_inert            # SIMULATED/research_only across 6 tables
(plus the standing per-unit W6 suites remain green)
```
Plus standing `test_broker_integration.py` green. Full backend regression ≥ **345** green (report actual). Frontend ≥ **18f/58t** green.

---

## 5. Mandatory evidence (operator-run on target — Level-I)

Deliver `DELIVERY_REPORT_W6-U08.md` + `operator results.md` (+ browser screenshots) with, **inline**:

**(a) Build identity.** `Test-Path` any new closeout files/tests + proof the pack is OF **W6-U08**; version `0.54.0`.
**(b) Test transcript.** Named whole-wave tests + broker suite + full backend total + frontend total.
**(c) Migration state.** `alembic current` = `20260717_0033` (unchanged — no closeout migration).
**(d) WAVE-WIDE NO-ORPHAN COMPLETENESS (raw psql, INLINE).** For **each of the six** W6 tables: `SELECT COUNT(*)` (row_count ≥ 1) **and** its no-orphan audit JOIN → `orphan_count 0`. A single consolidated transcript is fine; all six must appear.
**(e) Whole-wave bright-line grep.** over `backend/app/execution_research` + W6 routes → empty; §16 containment grep (broker logic only in `external_integration`) → disclosed benign only.
**(f) Gate-CLOSED proof.** named test PASS + broker suite green + (optional but welcome) a raw `audit_events` `GATE_CLOSED_*_REFUSED` count.
**(g) SIMULATED-everywhere check.** raw query or test proving all six tables' rows carry `SIMULATED`/`research_only`.
**(h) Browser E2E (GR6-10).** served-session shots across the Execution Research surface: SIMULATED framing, no actuation controls, and a **proper logged-out block** (URL bar `/execution-research`→login, or operator unauth HTTP 401/302).
**(i) TD-W6-CI-AUDIT disposition.** either `LOCAL_CI_EXIT_CODE: 0` on a networked run / graceful-audit exit 0, OR a formal carry note with substitute proof.
**(j) CI (GR6-11).** Git-Bash path → `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE` (0 if resolved; if still env-blocked, disclose per (i)).
**(k) Docs reconciliation.** CHANGELOG v0.54.0, ADR(s), TD register updated.

---

## 6. Acceptance criteria (milestone gate)

APPROVED (and milestone declared) requires ALL of (a)–(k); named whole-wave tests + broker suite green; regression green with actual totals; **all six tables row_count ≥1 with no-orphan audit JOIN = 0**; whole-wave bright-line + §16 containment clean; Gate proven CLOSED wave-wide; SIMULATED-everywhere; **browser E2E incl. a proper logged-out block**; TD-W6-CI-AUDIT resolved or formally carried; docs reconciled.

- A single CRITICAL (any live-execution path anywhere in W6, any broker logic outside External Integration, any Gate mutation, any actuation control on a W6 surface, any orphaned artifact) ⇒ **WITHHELD** — no milestone.
- Every *risk* item proven but a *named* proof missing ⇒ **CONDITIONAL** (→ `_FINAL` on closure, then milestone).
- A red gate is a finding, never relabeled green.

**On clean approval:** platform bump to **v0.54.0**; head `20260717_0033`; **WAVE 6 CLOSED**; ITRGA declares 🏛️ **"EXECUTION RESEARCH ENVIRONMENT COMPLETE"** — the roadmap's Wave-6 milestone. Onboarding updated; `ITRGA_VERDICT_W6-U08_FINAL_AND_WAVE6_CLOSURE.md` written.

---

## 7. Reminders to DA

- This is the **proof-of-the-whole** unit — reconcile all six tables, prove the Gate stayed CLOSED across the wave, and show no live-execution path anywhere.
- **Get the logged-out block right this time** (URL bar `/execution-research`→login, or an operator unauth HTTP 401/302) — GR6-10 is back in full force for the closeout browser E2E.
- Resolve or formally carry TD-W6-CI-AUDIT.
- No new table/feature. Verify the pack is OF W6-U08; attach only this unit's operator pack + shots; state dep changes accurately.

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
