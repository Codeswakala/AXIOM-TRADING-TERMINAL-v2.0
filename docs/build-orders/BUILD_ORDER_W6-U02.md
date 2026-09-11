# BUILD ORDER — W6-U02

## Simulated Execution Runs & Fill Events (first Wave-6 persisted artifacts)

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Wave:** 6 — Execution Research · **Unit:** W6-U02 · **Policy:** one unit per Build Order
**Date:** 2026-07-17
**Platform of record (pre-unit):** v0.47.0 · Alembic head `20260717_0027` · backend **297 passed** · frontend **17 files / 53 tests**
**Governing docs:** accepted `WAVE6_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` §5.2/§5.3; `ITRGA_REVIEW_WAVE6_DESIGN_PLAN.md` (R6-1…R6-8); `05_SYSTEM_ARCHITECTURE.md` v2.0 §16/§43; `07_ML_SPEC.md`; `10_CONSTITUTIONAL_HIERARCHY.md`.
**Constitutional posture:** Governance Gate **CLOSED**. This unit persists **SIMULATED** research artifacts only; it opens nothing.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

W6-U01 proved the lock (Gate-closed refusal seam). W6-U02 builds the **first door behind that lock**: two persisted, **SIMULATED-labelled, inert** research tables — `simulated_execution_runs` and `simulated_fill_events` — produced by a **deterministic** fill model over historical/replayed candles. No live anything. This is the unit where Wave-6's persistence-capture control (R6-9) first applies, so evidence is strict.

---

## 2. Scope (build exactly this)

1. **Tables + Alembic migrations** (from `20260717_0027`):
   - `simulated_execution_runs` → migration `20260717_0028`
   - `simulated_fill_events` → migration `20260717_0029` (FK `run_id` → `simulated_execution_runs`)
2. **Deterministic simulated fill model** in `backend/app/execution_research/` — given a run spec + source candles, produces reproducible `simulated_fill_events` (same inputs → same outputs; no RNG without a fixed seed recorded on the run).
3. **Committing service + read-only API** to create a run and list/detail runs+fills. **Read-only GET** for retrieval; the create path is a **research write** that produces ONLY simulated artifacts (no broker/live seam reachable — prove by grep).
4. **Audit rows** for each created run/fill into immutable `audit_events` (for the no-orphan JOIN).
5. **No UI this unit** (UI is W6-U07). No browser evidence required.

### Field contracts (accepted design §5.2/§5.3)
- **`simulated_execution_runs`:** `run_id, created_at (UTC), operator_id, simulation_mode='SIMULATED', simulation_policy_version, input_artifact_ids, replay_scope, fill_model_name, fill_model_version, assumptions, limitations, research_status='research_only', simulation_disclaimer, audit_correlation_id`.
- **`simulated_fill_events`:** `simulated_fill_id, run_id (FK), created_at (UTC), simulation_mode='SIMULATED', market_class, symbol, timeframe, as_of_time, simulated_research_direction, simulated_units, requested_reference_price, simulated_fill_price, simulated_slippage_bps, source_candle_ids, fill_model_name, research_status, simulation_disclaimer, audit_correlation_id`.

### FORBIDDEN fields (must be ABSENT — prove via `information_schema` query)
`broker_account_id, account_id, real_account_balance, margin, capital, live_position_id, broker_endpoint, broker_credentials, order_payload, order_intent, execution_status_as_live` (runs) and any real account/broker/position/P&L column (fills).

---

## 3. Binding refinements applied (from the accepted Design Plan review)

- **R6-2 — `operator_id` is a research-attribution FK to the existing `users` table ONLY.** Never a trading/broker account. Owes a **no-orphan JOIN against `users`** in addition to the audit JOINs.
- **R6-3 — no-real-P&L / not-real-quantity contract.** `simulated_units` stays dimensionless (design note: "not an order quantity"); `simulated_fill_price` is a model output (not a broker fill). A test must assert no "real P&L / guaranteed return / live fill" framing on these fields, and every record carries the `SIMULATED` marker + disclaimer.
- **R6-4 — Gate-closed proof line in THIS pack:** `test_governance_gate_remains_closed_for_wave6` PASS + standing `test_broker_integration.py` green.
- **R6-6 — `simulation_policy_version` and `fill_model_version` are write-once per record (immutable)** and must appear in the raw SELECT + audit, so a later fill-model change cannot silently rewrite prior simulated history.
- **R6-8 — read-only retrieval + write-safe create:** the create endpoint must be proven to reach ONLY simulated persistence (bright-line grep on the new route), never a broker/live seam. No UI-triggered write this unit (no UI at all).

---

## 4. Mandatory tests (deliver names + raw PASS lines)

```
test_simulated_execution_run_persists_and_audit_no_orphan
test_simulated_fill_events_persist_and_audit_no_orphan
test_simulated_fill_model_is_deterministic          # same inputs → identical fills
test_simulated_tables_have_no_forbidden_broker_or_account_columns
test_simulated_artifacts_labelled_simulated_and_disclaimer_present
test_simulated_records_have_no_real_pnl_or_live_fill_language     # R6-3
test_simulation_policy_and_fill_model_versions_are_immutable      # R6-6
test_execution_research_create_path_has_no_live_broker_or_gate_path  # R6-8 bright-line
test_governance_gate_remains_closed_for_wave6                     # R6-4
```
Plus standing `test_broker_integration.py` green. Full backend regression must PASS (expected ≥ 297 + new). Report the operator's actual total.

---

## 5. Mandatory evidence (operator-run on target — Level-I)

Deliver `DELIVERY_REPORT_W6-U02.md` + `operator results.md` with, **inline**:

**(a) Build identity.** `Test-Path` new files (migrations + service) + first 4 lines / grep proving the pack is OF **W6-U02** (not a prior turn's pack).

**(b) Test transcript.** Raw run of the named tests + broker suite + full backend total.

**(c) Migration proof.** `alembic upgrade head` then `alembic current` = **`20260717_0029`** (head advanced by exactly the two W6-U02 migrations); show both revision files exist.

**(d) PERSISTENCE-CAPTURE (R6-9 — first W6 application, deliver INLINE):**
  1. committing script/command that creates ≥1 run and ≥1 fill;
  2. raw `psql SELECT` of **≥1 row from `simulated_execution_runs`** (showing `simulation_mode='SIMULATED'`, `research_status='research_only'`, `simulation_policy_version`, `fill_model_version`, disclaimer);
  3. raw `psql SELECT` of **≥1 row from `simulated_fill_events`** (showing `SIMULATED`, `simulated_units`, `simulated_fill_price`, `as_of_time`);
  4. **no-orphan audit JOIN for EACH table** — `LEFT JOIN audit_events ae ON ae.resource_type=… AND ae.resource_id=… AND ae.correlation_id=… AND ae.action=… WHERE ae.id IS NULL` → **`orphan_count 0`** each;
  5. **no-orphan JOIN of `operator_id` against `users`** (R6-2) → `orphan_count 0`.
  (An API read-back does NOT substitute for the named raw SELECT + audit JOIN — W4-U02 C-1.)

**(e) Forbidden-column proof.** `information_schema.columns` query over both tables showing the §2 forbidden columns return **0 rows** (absent).

**(f) Determinism proof.** Run the fill model twice on identical inputs; show identical outputs (e.g. `Compare-Object` empty or identical `simulated_fill_price`/hash).

**(g) Bright-line grep (R6-8).** `grep -RInE "place_order|broker\.(connect|execute)|go_live|live_order|real_account|account_balance|margin"` over `backend/app/execution_research` (incl. the new route) → **empty** (or only disclosed rejection-list strings).

**(h) No barred dependency.** Grep the barred list (broker/exchange/LLM SDK) → empty; state any dep change explicitly and accurately (W6-U01 C-2 lesson — no over-broad "no dependency" claims).

**(i) CI (GR6-11).** Git-Bash path → `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0`.

**(j) Gate-closed proof (R6-4).** Named test PASS + broker suite green.

---

## 6. Acceptance criteria

APPROVED requires ALL of (a)–(j) inline and verifiable; named tests + broker suite green; regression green with the actual total; both raw SELECTs ≥1 row with SIMULATED/disclaimer/version fields; **all no-orphan JOINs = 0** (both tables + users); forbidden columns absent; determinism shown; bright-line grep clean; CI exit 0; Gate CLOSED.

- A single CRITICAL (any live/broker/account/order path, any forbidden column present, any Gate mutation, broker logic outside External Integration) ⇒ **WITHHELD.**
- Every *risk* item proven but a *named* proof missing ⇒ **CONDITIONAL** (→ `_FINAL` on closure).
- A red gate is a finding, never relabeled green.

On approval: platform bump to **v0.48.0**; head `20260717_0029`; onboarding updated; W6-U03 (simulated paper ledger) becomes next authorizable.

---

## 7. Reminders to DA

- Persistence-capture is INLINE and named — raw SELECT + no-orphan JOIN per table + operator_id-vs-users JOIN. No API read-back substitution.
- Determinism is mandatory (no unseeded RNG). Versions are immutable.
- No UI this unit. No broker/live path reachable from the create endpoint — prove it.
- Verify the pack is OF W6-U02 before submitting; state dep changes accurately.

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
