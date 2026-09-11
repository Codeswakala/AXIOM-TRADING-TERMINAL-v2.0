# BUILD ORDER — W6-U05

## Trade Replay & Execution Experiment Pre-Registration

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Wave:** 6 — Execution Research · **Unit:** W6-U05 · **Policy:** one unit per Build Order
**Date:** 2026-07-17
**Platform of record (pre-unit):** v0.50.0 · Alembic head `20260717_0031` · backend **325 passed** · frontend **17 files / 53 tests**
**Governing docs:** accepted `WAVE6_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` §5.6 + fence-map "Trade replay" / "Execution experimentation" rows; `ITRGA_REVIEW_WAVE6_DESIGN_PLAN.md` (R6-1…R6-8, esp. **R6-7**); `07_ML_SPEC.md` (pre-registered experiments, no cherry-picking, avoid look-ahead); `05_SYSTEM_ARCHITECTURE.md` v2.0 §16/§43; `10_CONSTITUTIONAL_HIERARCHY.md`.
**Constitutional posture:** Governance Gate **CLOSED**. Replay over frozen historical/simulated inputs + immutable pre-registered experiment plans — no live feed, no broker, no actuation.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

This unit delivers the roadmap's **"Trade replay"** + **"Execution experimentation"** components, fenced to research/simulation only. Its two distinctive controls are:
1. **R6-7 no-look-ahead (CENTRAL) —** replay is **frozen / as-of bounded**; **no candle with `time > as_of_time` may enter** a replay/experiment. This must be proven with the **strong as-of / future-row-exclusion pattern** (bounding query + a negative check), not merely asserted (BO precedent: I named this as R6-7's required form).
2. **Pre-registration immutability & no-cherry-picking —** an experiment plan is **pre-registered with an immutable plan hash** declaring its full scope *before* results; the plan cannot be silently narrowed/rewritten after the fact.

---

## 2. Scope (build exactly this)

1. **Table + migration** from `20260717_0031`:
   - `execution_research_experiments` → migration `20260717_0032`.
2. **Experiment pre-registration service + read-only API:** register a plan (immutable `plan_hash` over the declared scope) and list/detail; and a **replay execution** that runs the pre-registered plan over frozen/as-of-bounded inputs, producing simulated outputs referencing existing W6-U02/U03 artifacts. The service writes experiment/plan rows + audit only — no order, no actuation, no broker/live/Gate seam (prove by grep + test).
3. **Audit rows** for each registered experiment / replay run into immutable `audit_events` (no-orphan JOIN).
4. **No UI this unit** (UI is W6-U07). No browser evidence required.

### Field contract (accepted design §5.6, expanded for the controls)
`experiment_id, created_at (UTC), simulation_mode='SIMULATED', operator_id (FK operators.id), experiment_title, pre_registration_plan (declared full scope: symbols/timeframes/as_of window/fill_model/included_artifact_ids/hypothesis), plan_hash (immutable, over the plan), as_of_time / as_of_window, replay_input_lineage (source run/fill/candle ids), included_scope_summary, uncertainty, limitations, research_status='research_only', simulation_disclaimer, audit_correlation_id`.
- **`plan_hash`** is write-once (immutable); recomputable deterministically from `pre_registration_plan`.
- **`as_of_time` / `as_of_window`** bound the replay; no input may post-date it.

### FORBIDDEN fields (must be ABSENT — prove via `information_schema`)
`account_balance, real_account_balance, margin, capital, real_capital, broker_account_id, account_id, live_position_id, position_id, broker_endpoint, broker_credentials, order_payload, order_intent, real_pnl, pnl, realized_pnl, position_size, order_size, live_feed_url, execution_status_as_live`.

---

## 3. Binding refinements applied

- **R6-7 no-look-ahead (CENTRAL):** prove via the **as-of / future-row-exclusion** pattern — (a) the bounding query that selects only inputs with `time <= as_of_time`; (b) a **negative check** demonstrating a future-dated candle (`time > as_of_time`) is **excluded** from the replay/experiment; and a test `test_replay_excludes_future_rows_beyond_as_of`.
- **Pre-registration immutability / no cherry-picking:** `plan_hash` is immutable and matches the declared `pre_registration_plan`; a test proves (i) the hash is stable/recomputable, (ii) the executed replay's included scope equals the pre-registered scope (no post-hoc narrowing), and (iii) an attempt to mutate a registered plan is refused.
- **R6-7 uncertainty / stat ≠ economic:** experiment/replay outputs carry uncertainty + limitations; no economic-success or real-P&L claim.
- **R6-2 —** `operator_id → operators.id` + no-orphan JOIN vs `operators`.
- **R6-4 —** Gate-closed proof line in-pack.
- **R6-8 —** read-only retrieval + write-safe register/replay; bright-line grep + test proving no live-feed/broker/Gate path (incl. **no live feed** — replay uses frozen inputs only).
- **Lineage —** `replay_input_lineage` references existing simulated/governed artifacts; prove no dangling reference.

---

## 4. Mandatory tests (deliver names + raw PASS lines)

```
test_execution_research_experiment_persists_and_audit_no_orphan
test_experiment_plan_hash_is_immutable_and_matches_preregistration
test_replay_excludes_future_rows_beyond_as_of                       # R6-7 no-look-ahead
test_replay_included_scope_equals_preregistered_scope_no_cherry_picking
test_registered_plan_mutation_is_refused
test_execution_experiment_has_no_forbidden_account_pnl_or_sizing_columns
test_execution_experiment_carries_uncertainty_and_limitations
test_execution_research_experiment_create_path_has_no_live_feed_broker_or_gate_path  # R6-8 bright-line
test_governance_gate_remains_closed_for_wave6                       # R6-4
```
Plus standing `test_broker_integration.py` green. Full backend regression must PASS (expected ≥ 325 + new). Report the operator's actual total.

---

## 5. Mandatory evidence (operator-run on target — Level-I)

Deliver `DELIVERY_REPORT_W6-U05.md` + `operator results.md` with, **inline**:

**(a) Build identity.** `Test-Path` new files + first 4 lines / grep proving the pack is OF **W6-U05**.

**(b) Test transcript.** Named tests + broker suite + full backend total.

**(c) Migration proof.** `alembic upgrade head` then `alembic current` = **`20260717_0032 (head)`** on PostgreSQL; revision file exists.

**(d) PERSISTENCE-CAPTURE (R6-9, INLINE — target PostgreSQL, raw `psql`, NOT API read-back):**
  1. committing script that registers ≥1 experiment + runs its replay;
  2. raw `psql SELECT ≥1 row` from **`execution_research_experiments`** showing `SIMULATED`, `research_only`, `plan_hash`, `as_of_time`/`as_of_window`, `replay_input_lineage`, `uncertainty`, disclaimer;
  3. **no-orphan audit JOIN** → `orphan_count 0`;
  4. **no-orphan JOIN vs `operators`** → 0;
  5. **lineage no-orphan JOIN** — `replay_input_lineage` resolves to existing simulated artifacts → 0.

**(e) Forbidden-column proof.** `information_schema.columns` over `execution_research_experiments` for the §2 list → **0 rows**.

**(f) R6-7 NO-LOOK-AHEAD proof (raw, on target).** Show:
  1. the bounding query returning only `time <= as_of_time` inputs for the replay; and
  2. a **negative check** — a `SELECT COUNT(*)` of any replayed/included input with `time > as_of_time` → **0** (no future row entered). Plus the passing `test_replay_excludes_future_rows_beyond_as_of`.

**(g) Pre-registration immutability / no cherry-picking.** Show `plan_hash` recomputed equals stored; included-scope == pre-registered scope (via SELECT and/or the passing tests); mutation-refused test PASS.

**(h) Bright-line grep (R6-8).** `grep -RInE "place_order|broker\.(connect|execute)|go_live|live_order|live_feed|real_account|account_balance|margin|position_size|order_size|real_pnl"` over `backend/app/execution_research` + the experiment route → **empty** (or only disclosed rejection-list strings).

**(i) No barred dependency.** Barred-list grep empty; state any dep change accurately.

**(j) CI (GR6-11).** Git-Bash path → `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0`.

**(k) Gate-closed proof (R6-4).** Named test PASS + broker suite green.

---

## 6. Acceptance criteria

APPROVED requires ALL of (a)–(k) inline and verifiable; named tests + broker suite green; regression green with actual total; raw SELECT ≥1 row with SIMULATED/plan_hash/as_of/uncertainty; **all no-orphan JOINs = 0** (audit + operators + lineage); forbidden columns absent; **no-look-ahead future-row-exclusion proven (bounding + negative check)**; pre-registration immutability + no-cherry-picking proven; bright-line clean; CI exit 0; Gate CLOSED.

- A single CRITICAL (any look-ahead leak, any live-feed/broker/order/account path, any forbidden column present, any post-hoc scope narrowing that defeats pre-registration, any Gate mutation) ⇒ **WITHHELD.**
- Every *risk* item proven but a *named* proof missing ⇒ **CONDITIONAL** (→ `_FINAL` on closure).
- A red gate is a finding, never relabeled green.

On approval: platform bump to **v0.51.0**; head `20260717_0032`; onboarding updated; W6-U06 (simulated execution analytics & performance comparison) becomes next authorizable.

---

## 7. Reminders to DA

- **No-look-ahead is the red line here** — prove future rows are *excluded* (bounding query + negative-count check), not just that replay "uses history."
- Pre-registration must be **immutable and honest** — plan_hash write-once, executed scope == declared scope, mutation refused (no cherry-picking).
- Replay uses **frozen inputs only** — no live feed. `operator_id → operators.id`.
- Persistence-capture INLINE, raw `psql`, no API read-back substitution (W4-U02 C-1 / W6-U04 C-1 lesson). No UI this unit. Verify the pack is OF W6-U05; state dep changes accurately.

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
