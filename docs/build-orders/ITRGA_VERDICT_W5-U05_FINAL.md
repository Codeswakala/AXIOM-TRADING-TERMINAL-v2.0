# ITRGA FINAL VERDICT — W5-U05 (Scenario Comparison Workspace)

| Field | Value |
|---|---|
| Reviewing authority | **AXIOM Independent Technical Review & Governance Authority (ITRGA)** |
| Unit | **W5-U05** — Scenario Comparison Workspace |
| Supersedes | `ITRGA_REVIEW_W5-U05.md` (2026-07-17, CONDITIONAL — C-1 ≥2-scenario comparison not exercised) |
| Evidence | C-1 closure `operator results.md` (298 lines) + 3 browser screenshots |
| Platform | **0.43.0** |
| Review date | 2026-07-17 |
| **VERDICT** | **✅ APPROVED — CLEAN. C-1 CLOSED.** Platform advances to **v0.43.0** |
| Confidence | **HIGH** — genuine ≥2-scenario comparison now proven on target; no-generation holds with real data |

> **We don't guess. We prove.** With two real scenarios present, the side-by-side comparison renders — and still creates no rows. The core function is proven; the condition is closed.

---

## 1. Bottom line

The CONDITIONAL verdict approved safety + read function and held one condition: the workspace's headline
function (compare ≥2 scenarios) was unproven on target because the DB held only 1 scenario. The closure re-run
seeds **≥2 existing scenarios via the prior-wave path (not generation)** and demonstrates a genuine
side-by-side comparison. **C-1 is CLOSED; W5-U05 is APPROVED, CLEAN; Platform advances to v0.43.0.**

---

## 2. C-1 — CLOSED ✅

- **≥2 existing scenarios present, seeded the prior-wave way (NOT generation):** the seed script writes into
  `scenario_reports` with `source="w5-u05-c1:w4-u04-scenario-seed"` / `actor="operator_w5_u05_c1_w4_u04_seed"`
  — i.e. persisting existing scenario artifacts as W4-U04 does, **not** via any W5-U05 generation path (which
  correctly does not exist). Count `1 → 3`; both new rows `research_only` with proper uncertainty/provenance/
  limitations (`not_a_prediction, not_a_trade_instruction, …`).
- **Genuine two-scenario comparison exercised on target:** `C1_COMPARE_SCENARIO_IDS: b2a643e4… d88f2c72…`
  (two real ids), `DETAIL1_STATUS:200`, `DETAIL2_STATUS:200`.
- **No-generation still holds with real data:** `C1_SCENARIO_COUNT_BEFORE_COMPARISON: 3` =
  `C1_SCENARIO_COUNT_AFTER_COMPARISON: 3` — comparison created no rows.
- **Browser — real side-by-side:** two scenarios rendered together — `w5_u05_c1_existing_plus_one_percent`
  (hypothetical return **+1.00%**, counterfactual 1.0504) and `w5_u05_c1_existing_minus_two_percent`
  (**-2.00%**, counterfactual 1.0192) — each with distinct assumptions (shock_return +0.01 / -0.02),
  uncertainty (`0.99%–1.01%` / `-2.01%–-1.99%`, n=5, historical_volatility_band), provenance/source ids, and
  limitations; "Hypothetical comparison only… not a prediction, not guaranteed… AXIOM does not act" banner
  visible. The headline function is proven on target. ✅

## 3. No regression

Named `test_scenario_comparison_workspace.py` **5 passed**; ruff clean; no-generation grep on the page clean;
frontend build ok. The W5-U05 gates from the CONDITIONAL review (backend 273 / frontend 15·43 / CI Git-Bash
exit 0 / no migration / API 401·200 · POST/generate/compare 405) stand; this closure adds the ≥2-scenario
proof only.

---

## 4. Findings ledger

| ID | Severity | Status |
|---|---|---|
| C-1 (was MEDIUM) | — | **CLOSED** — ≥2 scenarios seeded (prior-wave, not generation); real side-by-side comparison on target; BEFORE 3 = AFTER 3 |
| — | — | no-generation / read-only API / no raw score / no LLM / gate-closed / 273·15·43 / CI exit 0 | ✅ (from CONDITIONAL review) |

**No CRITICAL/HIGH. No open residual.** All W5-U05 acceptance criteria met on target.

---

## 5. Disposition & next step

- **W5-U05 — ✅ APPROVED, CLEAN.** Platform **v0.42.0 → v0.43.0**. Scenario Comparison Workspace: compares
  existing persisted scenarios read-only, ≥2 side-by-side proven, uncertainty/provenance/not-guaranteed framing,
  no generation, no raw score, no execution.
- Commendation: the closure seeded the second scenario the **right way** (prior-wave persistence, not a W5-U05
  generation path that doesn't exist), and re-proved no-generation with real data (BEFORE 3 = AFTER 3) — exactly
  the standard. The DA's original precondition guard (throwing on <2) was the correct honest behavior that
  surfaced the gap.
- **Next:** ITRGA recommends **W5-U06 — Inert Trade Planning Workspace** (the GR-9 keystone surface): persisted
  research-only trade-plan notes that **reject order/sizing/account fields and trigger nothing**, carrying
  **R5-4** (inert — schema + reject-forbidden-fields + triggers-nothing), **R5-6** (browser mandatory — no
  order-ticket patterns/buttons), **R5-7** (persistence-capture inline), **R5-8**. On operator authorization
  ITRGA issues `BUILD_ORDER_W5-U06.md`.
- After U06 → **W5-U07** (Manual Research Journal) → **W5-U08** (Closeout → "Human-AI Collaborative Workspace
  Complete"). External LLM remains future hard-gated (R5-2). DA does not self-authorize W5-U06, ship an LLM,
  add an actuating tool/execution/order/account linkage, or open the Gate.

> **We don't guess. We prove.** — ITRGA
