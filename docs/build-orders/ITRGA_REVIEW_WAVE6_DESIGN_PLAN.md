# ITRGA REVIEW — WAVE 6 ENGINEERING DESIGN & IMPLEMENTATION PLAN ("EXECUTION RESEARCH")

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Document reviewed:** `uploads/WAVE6_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` (669 lines, dated 2026-07-17)
**Review date:** 2026-07-17
**Platform of record:** v0.46.0 · Alembic head `20260717_0027` · backend **291 passed** · frontend **17 files / 53 tests**
**Verdict:** ✅ **ACCEPTED WITH REFINEMENTS** (R6-1 … R6-8, binding)
**Confidence:** HIGH — the plan was verified line-by-line against every pre-registered guardrail; refinements are bounded and closable at Build-Order time.
**Motto:** *We don't guess. We prove.*

---

## 0. Build-identity check (done FIRST)

- Title line 1: `# Wave 6 Engineering Design and Implementation Plan` ✔
- Header table: `Wave | 6 — Execution Research`, `Platform of record v0.46.0`, `Alembic head 20260717_0027`, `Constitutional posture: Governance Gate CLOSED` ✔ — **matches the platform of record; this is the correct, current plan (not a stale re-attachment).**
- References `ITRGA_REQUEST_WAVE6_DESIGN_PLAN.md` and answers GR6-1…GR6-13 by number ✔.

The pack is genuinely the Wave 6 Design Plan under review. Proceeding.

---

## 1. Verdict rationale

This is a disciplined, evidence-aware plan that treats Wave 6 correctly as **simulation/research only with the Governance Gate CLOSED**. Every pre-registered guardrail (GR6-1…GR6-13) receives a concrete design response (§3), each roadmap component is fenced individually (§2), every candidate table carries an explicit **forbidden-field list** (§5 — the strongest no-account-linkage proof pattern), the bright-line refusal/containment test suite is pre-registered (§6), the dependency declaration explicitly **bars a broker SDK** (§9), and the unit decomposition opens with **W6-U01 = the Gate-closed safety envelope** ("prove the lock before the door," §11/§12) exactly per the W3-U01/W4-U01/W5-U01 precedent.

No CRITICAL and no HIGH design defects were found. The refinements below are boundary-tightening that must be bound into the relevant Build Orders; none blocks acceptance of the plan.

---

## 2. Strengths accepted as-designed

| Area | Finding |
|---|---|
| Constitutional posture | Gate CLOSED asserted throughout; explicitly out-of-scope list (§1.2) names go-live switch, Gate opening, real account/position/balance/margin/capital, order routing, broker SDK, external LLM — all barred. |
| Fence map (§2) | Per-component construction fence + hard-prohibition **proof** column (not "mitigated" — *proven*). |
| Data model (§5) | Every table has a forbidden-field list; `simulation_mode='SIMULATED'` + `research_status='research_only'` + disclaimer on every artifact. `simulated_units` declared dimensionless; `simulated_fill_price` declared model-output not broker-fill. |
| Test plan (§6) | Bright-line suite pre-registered incl. `test_governance_gate_remains_closed_for_wave6`, connect/execute refusal, `test_broker_logic_contained_in_external_integration`, `test_wave6_bright_line_grep_no_live_execution_path`, per-table no-orphan. |
| UI plan (§7) | Mandatory `SIMULATED`/not-live disclaimer text; forbidden-controls list (buy/sell/submit/go-live/connect-broker/account/balance); browser + logged-out block mandatory. |
| Dependencies (§9) | Existing stack only; broker SDK **barred regardless**; any other compiled dep owes a spike + ITRGA review. |
| Sequencing (§11/§12) | U01 safety envelope first; artifacts before analytics; UI only after persistence+refusal proven; U08 full-wave no-actuation closeout. |

---

## 3. BINDING REFINEMENTS (R6-1 … R6-8)

These are pre-registered as binding; each will be enforced at the Build Order it touches.

**R6-1 — W6-U01 persistence decision, made now (removes the "no schema unless ITRGA requests" ambiguity).**
For **W6-U01 there shall be NO new table.** Refusal/Gate-closed proof uses the **existing `audit_events`** table. However, U01 **must still deliver raw evidence**: a `psql SELECT` of the refusal `audit_events` rows produced by the connect/execute refusal tests (e.g. a `GATE_CLOSED_*` / `BROKER_CONNECT_REFUSED` / `BROKER_EXECUTE_REFUSED` reason code), with a `GROUP BY reason_code` count. This is the U01 analogue of the persistence-capture control — a refusal that leaves no audit trail is not proven.

**R6-2 — `operator_id` is research-attribution only.**
Where `operator_id` appears (`simulated_execution_runs`, `simulated_paper_ledger_entries`, etc.) it must be a FK to the existing **users** table for research attribution ONLY. It must never be, alias, or join to any broker/trading account. Each such table's first submission owes the no-orphan audit JOIN **against `users`** (`orphan_count 0`), in addition to the run/fill lineage joins.

**R6-3 — Bind the "not real quantity / not real P&L" contract on value fields.**
`simulated_units`, `simulated_entry_value`, `simulated_exit_value`, and especially **`simulated_return_estimate`** must (a) keep the `simulated_`/dimensionless framing in schema, API, and UI; and (b) be covered by the "no real-P&L / no guaranteed-return language" text test (§8 hard-prohibition), extended to the **ledger** artifact, not only the analytics report. A simulated return estimate rendered without its `SIMULATED`+uncertainty framing is a finding.

**R6-4 — Gate-closed evidence is a per-unit acceptance item, not just U01/U08.**
GR6-1 already asserts "Gate status evidence appears in every unit pack." Bind it: **every** W6 delivery pack (U01→U08) must include the Gate-closed proof line (`test_governance_gate_remains_closed_for_wave6` PASS + the standing `test_broker_integration.py` refusal green). A pack missing it is incomplete.

**R6-5 — No client-side authoritative recomputation (tighten §4.3 Institutional Intelligence row).**
Wave-6 UI is **display-only over server-persisted simulated reports**. Any metric/analytic shown must be read from a server-persisted, audited simulated artifact — no client-side recomputation may be presented as authoritative. Bind at W6-U06/U07.

**R6-6 — `simulation_policy_version` and `fill_model_version` are immutable-per-record and audited.**
Bind these as write-once per run/fill and require them to appear in the U02 raw SELECT + audit, so a later change of fill model is provable and cannot silently rewrite prior simulated history (supports pre-registration / no-cherry-picking, GR6-7).

**R6-7 — Replay no-look-ahead must be proven with the strong pattern (W-precedent).**
For W6-U05 trade replay, "no look-ahead" must be proven with the **as-of / future-row-exclusion** evidence pattern (frozen replay scope + demonstration that no candle with `time > as_of_time` enters the simulation), not merely asserted. Deliver the bounding query + a negative check.

**R6-8 — Any "run simulation" write from the UI (W6-U07 optional) is a separate acceptance gate.**
The plan floats "optional authorized simulated replay creation" in the UI. If a Build Order authorizes a UI-triggered simulation *write*, it must carry: the persistence-capture control for the written rows, a proof the write path cannot reach any broker/live seam (bright-line grep on the new endpoint), and browser evidence that the control is labelled `SIMULATED` and produces only simulated artifacts. Otherwise W6-U07 stays **read-only**.

---

## 4. Observations (non-binding, for DA awareness)

- **OBS-1:** Consider a single shared `SIMULATED` disclaimer constant (backend + frontend) so the mandatory §7 label text is grep-verifiable and cannot drift per surface.
- **OBS-2:** `execution_risk_research_reports.risk_metrics` and analytics `risk_metrics` should be structured (typed keys) rather than free-text so the "no real-P&L language" test can assert over fields deterministically.
- **OBS-3:** TD-063/TD-064 (analytics snapshot / outcome-return attribution) and TD-076/TD-077 (report drill-down) remain deferred and are **not** in Wave 6 scope — good; keep them out unless a future Build Order names them.

---

## 5. Scope confirmation

- **Accepted in-scope (smallest safe set):** §1.1 list — safety foundation → simulated runs/fills → paper ledger → risk reports → replay/experiments → analytics/comparison → workspace UI → closeout. Milestone candidate: **"Execution Research Environment Complete."**
- **Confirmed out-of-scope (barred):** §1.2 list — live broker adapter, broker SDK, credentials, live venue endpoint, real order/routing, real account/position/balance/margin/capital, real P&L claim, go-live switch, **Gate opening**, external LLM/API, unspiked compiled dep, Wave-7 work.

---

## 6. Decision & next step

**ACCEPTED WITH REFINEMENTS.** The plan is the correct constitutional footing for Wave 6. R6-1…R6-8 are binding and will be enforced at the Build Orders they touch.

- **W6-U01 confirmed** as the first Build Order: *Execution Research Safety Foundation — Gate-Closed Simulation Envelope*, with **R6-1** (no new table; `audit_events` refusal SELECT + `GROUP BY reason_code`) and **R6-4** (Gate-closed proof line) applied.
- On operator authorization I will issue `BUILD_ORDER_W6-U01.md` (one unit per Build Order, operator-agreed policy).
- The Constitutional Governance Gate remains **CLOSED**. Nothing in this acceptance opens it.

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
