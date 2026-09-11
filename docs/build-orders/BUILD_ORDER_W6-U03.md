# BUILD ORDER — W6-U03

## Simulated Paper Research Ledger

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Wave:** 6 — Execution Research · **Unit:** W6-U03 · **Policy:** one unit per Build Order
**Date:** 2026-07-17
**Platform of record (pre-unit):** v0.48.0 · Alembic head `20260717_0029` · backend **307 passed** · frontend **17 files / 53 tests**
**Governing docs:** accepted `WAVE6_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` §5.4; `ITRGA_REVIEW_WAVE6_DESIGN_PLAN.md` (R6-1…R6-8); `05_SYSTEM_ARCHITECTURE.md` v2.0 §16/§43; `07_ML_SPEC.md`; `10_CONSTITUTIONAL_HIERARCHY.md`.
**Constitutional posture:** Governance Gate **CLOSED**. Persists a **SIMULATED**, inert research ledger only — no live/broker/account/P&L path.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

W6-U02 persisted simulated runs + fills. W6-U03 builds a **simulated paper research ledger** *over those simulated fills only* — a labelled, inert record of hypothetical entry/exit/return **estimates** for research. This unit's central risk is **R6-3**: the ledger carries `simulated_return_estimate`, the field most likely to be mistaken for real P&L. That contract is the sharpest acceptance criterion here.

---

## 2. Scope (build exactly this)

1. **Table + migration** from `20260717_0029`:
   - `simulated_paper_ledger_entries` → migration `20260717_0030`, with **FK `run_id` → `simulated_execution_runs`** and **FK `simulated_fill_id` → `simulated_fill_events`** (a ledger entry references simulated artifacts, never an account/broker/position).
2. **Committing service + read-only API** to create a ledger entry from an existing simulated run/fill and list/detail entries. Read-only GET; the create path writes ONLY simulated ledger persistence (no broker/live/Gate seam reachable — prove by grep + test).
3. **Audit rows** for each created ledger entry into immutable `audit_events` (for the no-orphan JOIN).
4. **No UI this unit** (UI is W6-U07). No browser evidence required.

### Field contract (accepted design §5.4)
`ledger_entry_id, created_at (UTC), simulation_mode='SIMULATED', run_id (FK), simulated_fill_id (FK), operator_id (FK operators.id — per W6-U02 Amendment 1 precedent), ledger_event_type, simulated_research_direction, simulated_units, simulated_entry_value, simulated_exit_value, simulated_return_estimate, uncertainty, limitations, research_status='research_only', simulation_disclaimer, audit_correlation_id`.

### FORBIDDEN fields (must be ABSENT — prove via `information_schema`)
`account_balance, real_account_balance, margin, capital, real_capital, broker_account_id, account_id, live_position_id, position_id, broker_endpoint, broker_credentials, order_payload, order_intent, real_pnl, pnl, realized_pnl, execution_status_as_live`.

---

## 3. Binding refinements applied

- **R6-2 — `operator_id` is a research-attribution FK to `operators.id` ONLY** (per W6-U02 Amendment 1; the `operators` table is canonical, no `users`). Owes a **no-orphan JOIN against `operators`** → 0. Never a broker/trading account.
- **R6-3 (CENTRAL this unit) — no real-P&L / not-real-value contract.** `simulated_entry_value`, `simulated_exit_value`, and especially **`simulated_return_estimate`** must be (a) `simulated_`-prefixed and framed as research estimates, not realized results; (b) carried with `SIMULATED` marker + disclaimer on every row; (c) covered by a test asserting **no "real P&L / realized / guaranteed return / profit" framing** on these fields. `simulated_units` stays dimensionless.
- **R6-4 — Gate-closed proof line in THIS pack** (`test_governance_gate_remains_closed_for_wave6` + broker suite green).
- **R6-7 — uncertainty is mandatory on the return estimate.** `simulated_return_estimate` must never appear without its `uncertainty` (and `limitations`) populated; a test must assert a ledger entry with a return estimate carries uncertainty (or an explicit insufficient-basis limitation). Stat ≠ economic: no economic-usefulness claim asserted from a simulated estimate.
- **R6-8 — read-only retrieval + write-safe create:** create path proven to reach ONLY simulated ledger persistence (bright-line grep on the new route + a passing test), never a broker/live/Gate seam.
- **Lineage integrity:** every ledger entry must reference an existing simulated run+fill (FK enforced); prove no ledger entry can be created against a non-simulated or non-existent fill.

---

## 4. Mandatory tests (deliver names + raw PASS lines)

```
test_simulated_paper_ledger_entry_persists_and_audit_no_orphan
test_ledger_entry_references_existing_simulated_run_and_fill_only        # lineage/FK integrity
test_simulated_paper_ledger_has_no_forbidden_account_or_pnl_columns
test_simulated_return_estimate_carries_uncertainty_and_limitations       # R6-7
test_simulated_ledger_records_have_no_real_pnl_or_realized_language       # R6-3
test_simulated_ledger_artifacts_labelled_simulated_and_disclaimer_present
test_execution_research_ledger_create_path_has_no_live_broker_or_gate_path # R6-8 bright-line
test_governance_gate_remains_closed_for_wave6                             # R6-4
```
Plus standing `test_broker_integration.py` green. Full backend regression must PASS (expected ≥ 307 + new). Report the operator's actual total.

---

## 5. Mandatory evidence (operator-run on target — Level-I)

Deliver `DELIVERY_REPORT_W6-U03.md` + `operator results.md` with, **inline**:

**(a) Build identity.** `Test-Path` new files (migration + service + tests) + first 4 lines / grep proving the pack is OF **W6-U03**.

**(b) Test transcript.** Raw run of the named tests + broker suite + full backend total.

**(c) Migration proof.** `alembic upgrade head` then `alembic current` = **`20260717_0030`** (head advanced by exactly the one W6-U03 migration); revision file exists.

**(d) PERSISTENCE-CAPTURE (R6-9, deliver INLINE):**
  1. committing script/command that creates ≥1 ledger entry from an existing simulated run/fill;
  2. raw `psql SELECT` of **≥1 row from `simulated_paper_ledger_entries`** showing `simulation_mode='SIMULATED'`, `research_status='research_only'`, `simulated_return_estimate`, **`uncertainty`** and `limitations` populated, `simulation_disclaimer`, and the `run_id`/`simulated_fill_id` lineage;
  3. **no-orphan audit JOIN** (`LEFT JOIN audit_events … WHERE ae.id IS NULL`) → **`orphan_count 0`**;
  4. **no-orphan JOIN of `operator_id` against `operators`** → `0`;
  5. **lineage no-orphan JOIN** — every `simulated_fill_id` resolves to `simulated_fill_events` (and `run_id` to `simulated_execution_runs`) → `0` orphans.
  (An API read-back does NOT substitute for the named raw SELECT + JOINs — W4-U02 C-1.)

**(e) Forbidden-column proof.** `information_schema.columns` over `simulated_paper_ledger_entries` for the §2 forbidden list → **0 rows**.

**(f) R6-3 / R6-7 proof.** Show (via the SELECT + the two passing tests) that `simulated_return_estimate` is `simulated_`-framed, carries uncertainty/limitations, and has no real-P&L/realized/guaranteed language.

**(g) Bright-line grep (R6-8).** `grep -RInE "place_order|broker\.(connect|execute)|go_live|live_order|real_account|account_balance|margin|real_pnl|realized"` over `backend/app/execution_research` + the ledger route → **empty** (or only disclosed rejection-list strings).

**(h) No barred dependency.** Barred-list grep empty; state any dep change accurately (no over-broad "no dependency" claim — W6-U01 C-2 lesson).

**(i) CI (GR6-11).** Git-Bash path → `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0`.

**(j) Gate-closed proof (R6-4).** Named test PASS + broker suite green.

---

## 6. Acceptance criteria

APPROVED requires ALL of (a)–(j) inline and verifiable; named tests + broker suite green; regression green with actual total; raw SELECT ≥1 row with SIMULATED/disclaimer/return-estimate/**uncertainty**; **all no-orphan JOINs = 0** (audit + operators + lineage); forbidden columns absent; R6-3/R6-7 proven; bright-line clean; CI exit 0; Gate CLOSED.

- A single CRITICAL (any live/broker/account/order path, any forbidden column present, any real-P&L claim on `simulated_return_estimate`, any Gate mutation, broker logic outside External Integration) ⇒ **WITHHELD.**
- Every *risk* item proven but a *named* proof missing ⇒ **CONDITIONAL** (→ `_FINAL` on closure).
- A red gate is a finding, never relabeled green.

On approval: platform bump to **v0.49.0**; head `20260717_0030`; onboarding updated; W6-U04 (execution risk research reports) becomes next authorizable.

---

## 7. Reminders to DA

- `simulated_return_estimate` is the red-line field this unit — it is a research **estimate with uncertainty**, never realized P&L. Prove the framing and the uncertainty.
- Ledger entries reference simulated run+fill only (FK); prove no orphan/lineage escape.
- `operator_id → operators.id` (not `users`). Persistence-capture INLINE, named; no API read-back substitution.
- No UI this unit. Verify the pack is OF W6-U03; state dep changes accurately.

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
