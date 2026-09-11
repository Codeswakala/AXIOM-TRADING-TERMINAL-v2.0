# BUILD ORDER — W6-U04

## Execution Risk Research Reports

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Wave:** 6 — Execution Research · **Unit:** W6-U04 · **Policy:** one unit per Build Order
**Date:** 2026-07-17
**Platform of record (pre-unit):** v0.49.0 · Alembic head `20260717_0030` · backend **316 passed** · frontend **17 files / 53 tests**
**Governing docs:** accepted `WAVE6_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` §5.5 + fence-map "Risk engine" row + risk register ("Risk engine actuates sizing = CRITICAL"); `ITRGA_REVIEW_WAVE6_DESIGN_PLAN.md` (R6-1…R6-8); `05_SYSTEM_ARCHITECTURE.md` v2.0 §16/§43; `07_ML_SPEC.md`; `10_CONSTITUTIONAL_HIERARCHY.md`.
**Constitutional posture:** Governance Gate **CLOSED**. Advisory **research report only** — no actuating sizing, no account/capital/margin linkage, no live/broker/order path.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

This is the roadmap's **"Risk engine"** component, fenced to its constitutional interpretation: an **advisory research report** over hypothetical/simulated requests and the W6-U02/U03 simulated artifacts. It computes execution-risk **metrics** with mandatory uncertainty — and it **actuates nothing**. The CENTRAL risks this unit must falsify are: (i) the report **triggers no action / sizes nothing** (risk register CRITICAL); (ii) there is **no account/capital/margin/balance linkage**; (iii) statistical metrics are **not** asserted as economic success (R6-7).

---

## 2. Scope (build exactly this)

1. **Table + migration** from `20260717_0030`:
   - `execution_risk_research_reports` → migration `20260717_0031`.
2. **Report service + read-only API** to compute a report from `input_artifact_ids` (existing simulated runs/fills/ledger and/or governed advisory artifacts) and list/detail reports. The service **writes a report row only** — it returns no order, no sizing directive, no actuation; the create path reaches no broker/live/Gate seam (prove by grep + test).
3. **Audit rows** for each created report into immutable `audit_events` (no-orphan JOIN).
4. **No UI this unit** (UI is W6-U07). No browser evidence required.

### Field contract (accepted design §5.5)
`report_id, created_at (UTC), simulation_mode='SIMULATED', input_artifact_ids, simulated_request_summary, risk_metrics, uncertainty, limitations, economic_usefulness, research_status='research_only', simulation_disclaimer, audit_correlation_id`.
- **`risk_metrics`** must be **structured** (typed keys, e.g. `simulated_slippage_bps`, `simulated_adverse_excursion`, `simulated_fill_risk`) — not free text — so the no-real-P&L / no-sizing tests can assert over fields deterministically (accepted-design OBS-2).
- **`economic_usefulness`** is a **separate, explicit** statement, distinct from `risk_metrics` — the stat-vs-economic separation must be visible in the schema (R6-7).
- If the DA adds `operator_id`, it FKs **`operators.id`** (R6-2 precedent) and owes a no-orphan JOIN vs `operators`.

### FORBIDDEN fields (must be ABSENT — prove via `information_schema`)
`account_balance, real_account_balance, margin, capital, real_capital, broker_account_id, account_id, live_position_id, position_id, broker_endpoint, broker_credentials, order_payload, order_intent, real_pnl, pnl, realized_pnl, position_size, order_size, recommended_size, sizing_directive, execution_status_as_live`.
(Note the added **sizing** columns — a risk report that carries an actuating size is the CRITICAL failure mode; these must be absent.)

---

## 3. Binding refinements applied

- **R6-7 (CENTRAL) — uncertainty mandatory + stat ≠ economic.** Every report carries `uncertainty` and `limitations`; `risk_metrics` (statistical) and `economic_usefulness` (interpretation) are **separate fields**; a test asserts `economic_usefulness` is not derived-as-guaranteed from the metrics and that no "guaranteed/real-P&L/profit" language appears. No cherry-picking: if the report summarizes a set, it must state the included artifact set / sample_count.
- **No-actuation (risk register CRITICAL) — "triggers nothing."** A test must prove the report service produces **no order, no sizing output, no side effect** beyond persisting the report row + audit (an `assert_no_side_effect`-style guard on the create path).
- **No account/capital linkage** — forbidden-column proof (§2) incl. the sizing columns.
- **R6-2 —** any `operator_id` → `operators.id` + no-orphan JOIN.
- **R6-4 —** Gate-closed proof line in-pack.
- **R6-8 —** read-only retrieval + write-safe create; bright-line grep + test proving no live/broker/Gate path.
- **Lineage —** `input_artifact_ids` must reference existing simulated/governed artifacts; prove no dangling reference for the persisted report.

---

## 4. Mandatory tests (deliver names + raw PASS lines)

```
test_execution_risk_research_report_persists_and_audit_no_orphan
test_execution_risk_report_triggers_nothing_and_writes_report_only     # no-actuation CRITICAL
test_execution_risk_report_has_no_account_capital_margin_or_sizing_columns
test_execution_risk_report_carries_uncertainty_and_limitations         # R6-7
test_execution_risk_report_separates_statistical_from_economic_usefulness  # R6-7 stat≠economic
test_execution_risk_report_has_no_real_pnl_or_guaranteed_language
test_execution_research_risk_create_path_has_no_live_broker_or_gate_path  # R6-8 bright-line
test_governance_gate_remains_closed_for_wave6                           # R6-4
```
Plus standing `test_broker_integration.py` green. Full backend regression must PASS (expected ≥ 316 + new). Report the operator's actual total.

---

## 5. Mandatory evidence (operator-run on target — Level-I)

Deliver `DELIVERY_REPORT_W6-U04.md` + `operator results.md` with, **inline**:

**(a) Build identity.** `Test-Path` new files + first 4 lines / grep proving the pack is OF **W6-U04**.

**(b) Test transcript.** Named tests + broker suite + full backend total.

**(c) Migration proof.** `alembic upgrade head` then `alembic current` = **`20260717_0031`**; revision file exists.

**(d) PERSISTENCE-CAPTURE (R6-9, INLINE):**
  1. committing script that creates ≥1 report from existing `input_artifact_ids`;
  2. raw `psql SELECT` of **≥1 row from `execution_risk_research_reports`** showing `simulation_mode='SIMULATED'`, `research_status='research_only'`, structured `risk_metrics`, populated `uncertainty` + `limitations`, a **distinct** `economic_usefulness`, `simulation_disclaimer`;
  3. **no-orphan audit JOIN** → `orphan_count 0`;
  4. if `operator_id` present: **no-orphan JOIN vs `operators`** → 0.

**(e) Forbidden-column proof.** `information_schema.columns` over `execution_risk_research_reports` for the §2 forbidden list (incl. sizing columns) → **0 rows**.

**(f) No-actuation proof.** Show (via the passing `..._triggers_nothing_...` test) that the create path persists only the report + audit and returns no order/sizing/side-effect.

**(g) R6-7 proof.** SELECT + the two passing tests show uncertainty populated and `risk_metrics` vs `economic_usefulness` separated with no guaranteed/real-P&L language.

**(h) Bright-line grep (R6-8).** `grep -RInE "place_order|broker\.(connect|execute)|go_live|live_order|real_account|account_balance|margin|position_size|order_size|real_pnl"` over `backend/app/execution_research` + the report route → **empty** (or only disclosed rejection-list strings).

**(i) No barred dependency.** Barred-list grep empty; state any dep change accurately.

**(j) CI (GR6-11).** Git-Bash path → `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0`.

**(k) Gate-closed proof (R6-4).** Named test PASS + broker suite green.

---

## 6. Acceptance criteria

APPROVED requires ALL of (a)–(k) inline and verifiable; named tests + broker suite green; regression green with actual total; raw SELECT ≥1 row with SIMULATED/structured risk_metrics/uncertainty/**separate economic_usefulness**/disclaimer; no-orphan JOIN(s) = 0; forbidden columns (incl. sizing) absent; **no-actuation proven**; R6-7 separation proven; bright-line clean; CI exit 0; Gate CLOSED.

- A single CRITICAL (any actuating/sizing output, any account/capital/margin column, any live/broker/order path, any Gate mutation, broker logic outside External Integration, any guaranteed-P&L claim) ⇒ **WITHHELD.**
- Every *risk* item proven but a *named* proof missing ⇒ **CONDITIONAL** (→ `_FINAL` on closure).
- A red gate is a finding, never relabeled green.

On approval: platform bump to **v0.50.0**; head `20260717_0031`; onboarding updated; W6-U05 (trade replay + execution experiment pre-registration) becomes next authorizable.

---

## 7. Reminders to DA

- This is a **report engine, not a sizing engine** — it triggers nothing and sizes nothing. Prove it (triggers-nothing test + absent sizing columns).
- `risk_metrics` structured; `economic_usefulness` a separate, non-guaranteed statement.
- Persistence-capture INLINE, named; no API read-back substitution. No UI this unit.
- Verify the pack is OF W6-U04; state dep changes accurately.

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
