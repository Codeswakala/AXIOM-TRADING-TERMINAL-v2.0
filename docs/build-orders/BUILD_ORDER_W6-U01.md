# BUILD ORDER — W6-U01

## Execution Research Safety Foundation — Gate-Closed Simulation Envelope

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Wave:** 6 — Execution Research · **Unit:** W6-U01 (first unit) · **Policy:** one unit per Build Order
**Date:** 2026-07-17
**Platform of record (pre-unit):** v0.46.0 · Alembic head `20260717_0027` · backend **291 passed** · frontend **17 files / 53 tests**
**Governing docs:** `04_PROJECT_ROADMAP.md` (Wave 6); `05_SYSTEM_ARCHITECTURE.md` v2.0 §15/§16/§43/§46/§48; `10_CONSTITUTIONAL_HIERARCHY.md`; accepted `WAVE6_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md`; `ITRGA_REVIEW_WAVE6_DESIGN_PLAN.md` (R6-1…R6-8).
**Constitutional posture:** Governance Gate **CLOSED**. This unit does not, and cannot, open it.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose — "prove the lock before the door"

Before any simulated execution artifact, ledger, analytics, or UI is built, W6-U01 must **prove the safety envelope**: that the Execution Research bounded context exists as an inert skeleton with **no live-execution path by construction**, and that the broker seam **refuses connect and execute while the Gate is CLOSED** — with that refusal **audited**. This is the W3-U01/W4-U01/W5-U01 precedent applied to the highest-risk wave.

**This unit adds NO new table** (R6-1) and **NO UI** (browser evidence therefore not required this unit). It is a backend safety-foundation unit.

---

## 2. Scope (build exactly this — no more)

1. **Execution Research bounded-context skeleton** at `backend/app/execution_research/`:
   - simulation-only contracts (Pydantic) with the standing `SIMULATED` / `research_only` markers reserved as constants;
   - **no** broker client, **no** network egress, **no** credentials, **no** External Integration dependency except importing the refusal seam for tests;
   - a shared disclaimer constant (OBS-1) both layers can grep: exactly
     `SIMULATED execution research only. Not a live order, not financial advice, not real P&L. AXIOM does not act. Governance Gate CLOSED.`
2. **Broker refusal seam hardening** under `backend/app/external_integration/` ONLY (§16):
   - the Null/Simulated broker **refuses `connect` and refuses `execute`/`place_order` while the Gate is CLOSED**;
   - each refusal writes an `audit_events` row with a SCREAMING_SNAKE `reason_code` (style precedent: `*_REFUSED`) — required codes below (R6-1).
3. **Gate-closed proof** extension (see §4 tests). No Gate-state mutation code anywhere.
4. **No schema, no migration** — head stays `20260717_0027`.

**Out of scope (barred this unit):** any table; any UI; any simulated run/fill/ledger/analytics feature; any broker SDK/credential/endpoint; any dependency change; anything from W6-U02+.

---

## 3. Constitutional / guardrail requirements (binding)

- **GR6-1 / R6-4 — Gate stays CLOSED, proven in THIS pack** and in every W6 pack: include the `test_governance_gate_remains_closed_for_wave6` PASS line **and** the standing `test_broker_integration.py` green.
- **GR6-2 — simulation/research-only by construction:** no code path could execute against a live venue even if a credential/endpoint were supplied. Prove by construction + grep (§5).
- **GR6-3 — broker containment (§16):** broker-specific logic appears ONLY under `external_integration`. Prove by structural grep (§5).
- **GR6-4 — Null/Simulated broker refuses** connect + execute under closed Gate, extending `test_governance_gate_refuses_connect_and_execute`.
- **GR6-12 — no new/unspiked/broker-SDK dependency.** Prove requirements unchanged.
- **GR6-11 — CI via documented Git-Bash path.**

---

## 4. Mandatory tests (deliver names + raw PASS lines)

Backend, all green, and **named explicitly** in the pack:

```
test_governance_gate_remains_closed_for_wave6
test_null_or_simulated_broker_refuses_connect_when_gate_closed
test_null_or_simulated_broker_refuses_execute_when_gate_closed
test_broker_logic_contained_in_external_integration
test_execution_research_has_no_live_broker_sdk_or_credentials
test_wave6_bright_line_grep_no_live_execution_path
```

Plus the standing broker suite: `test_broker_integration.py` incl. `test_governance_gate_refuses_connect_and_execute` — must remain green.

Full backend regression must PASS (expected ≥ 291 + the new tests). Report the exact operator total.

---

## 5. Mandatory evidence (operator-run on target — Level-I; report-claims alone are Level-IV and will NOT be accepted)

Deliver `DELIVERY_REPORT_W6-U01.md` + `operator results.md` containing, **inline**:

**(a) Build identity.** `Test-Path` on the new `backend/app/execution_research/` files; first 4 lines + a grep proving the pack is OF W6-U01.

**(b) Test transcript.** Raw operator run showing the six named tests + broker suite PASS and the full backend total (e.g. `NNN passed`).

**(c) Refusal AUDIT proof (R6-1 — this replaces the new-table persistence-capture for U01).** Raw `psql` against `audit_events`:
```sql
SELECT reason_code, COUNT(*) FROM audit_events
WHERE reason_code IN ('GATE_CLOSED_CONNECT_REFUSED','GATE_CLOSED_EXECUTE_REFUSED')
GROUP BY reason_code ORDER BY reason_code;
```
(DA may name the codes; they MUST be SCREAMING_SNAKE `*_REFUSED`, be produced by the refusal tests, and each show `COUNT ≥ 1`.) A blank/errored grep is a non-result (R7) — show command **and** output.

**(d) Broker-containment structural grep (GR6-3).** Command + output proving broker-specific logic exists ONLY under `external_integration/`, e.g.:
```
grep -RInE "connect\(|place_order|execute\(|broker_endpoint|broker_credentials|BrokerClient|mt5|MetaTrader" backend/app --include=*.py
```
Expected: hits only under `backend/app/external_integration/` (plus the refusal-test files). Any hit inside `execution_research/` or intelligence/signals/UX layers ⇒ CRITICAL. Disclose known-benign residuals (e.g. `BrokerIntegrationService` in `dependencies.py`) with the line.

**(e) Bright-line grep (GR6-2).** Command + output proving no live-execution path in the new context:
```
grep -RInE "place_order|cancel_order|go_live|live_order|real_account|account_balance|margin|broker\.(connect|execute)" backend/app/execution_research
```
Expected: **empty** (or only rejection-list/forbidden-constant strings, disclosed).

**(f) No-dependency proof (GR6-12).** `git diff` (or equivalent) showing `requirements*.txt` / `package.json` **unchanged**; no broker/exchange/LLM/tokenizer package added.

**(g) No-migration proof.** `alembic current` = `20260717_0027` (unchanged); no new migration file.

**(h) CI (GR6-11).** `& "C:\Program Files\Git\bin\bash.exe" scripts/local_ci.sh` → `==> Local CI equivalent complete` + inline `LOCAL_CI_EXIT_CODE: 0`.

---

## 6. Acceptance criteria

APPROVED requires ALL of: (a)–(h) delivered inline and verifiable; the six named tests + broker suite green; full regression green with the operator's actual total; refusal audit rows present (c); containment grep clean (d); bright-line grep clean (e); no dep/no migration (f,g); CI exit 0 (h); Gate proven CLOSED (R6-4).

- A single CRITICAL (any live-execution path, any broker logic outside `external_integration`, any Gate mutation, any real-account field) ⇒ **APPROVAL WITHHELD.**
- A named-but-missing evidence item with all *risk* items proven ⇒ **CONDITIONAL** (superseded by `_FINAL` on closure).
- A red gate is a finding, never relabeled green; a proven-unrelated flake is investigated, not used to withhold.

On approval: platform bump to **v0.47.0**, onboarding updated, W6-U02 (simulated runs/fills) becomes the next authorizable Build Order.

---

## 7. Reminders to DA

- Do not attach the previous turn's `operator results.md` — the pack must be OF W6-U01 (verify unit id + version first).
- Cross-check your claimed test counts against the operator's actual totals.
- No new table, no UI, no dependency this unit. Prove the lock. Then we build the door.

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
