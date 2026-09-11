# ITRGA DETERMINATION — UI-005-P03

**Scenario Comparison & Portfolio Research Context**

| Field | Value |
|---|---|
| Authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-005 — Investigation & Planning Workspace |
| Phase | **UI-005-P03** |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-005-P03.md` |
| Governing docs | Doc 12 §7, `UI-005_ENGINEERING_DESIGN_PLAN.md` §10 (P03), `ITRGA_REVIEW_UI-005_DESIGN_PLAN.md` (R-1…R-7, R-5), Doc 16 |
| Evidence standard | Level-I (operator-run on target) — report-claims alone never approve |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 45f/196t |
| **DETERMINATION** | ✅ **APPROVED WITH OBSERVATIONS** |
| Governance Gate | CLOSED (unchanged) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Build-identity verification (performed FIRST)

| Check | Result |
|---|---|
| Delivery report | `# DELIVERY REPORT — UI-005-P03` · Phase `**UI-005-P03**` (378 lines) — OF the unit |
| Operator transcript | Same session; greps `DELIVERY_REPORT_UI-005-P03.md` + `BUILD_ORDER_UI-005-P03.md` (2392 lines) — OF the unit |
| Predecessor | `ITRGA_REVIEW_UI-005-P02.md` (Approved-w-Obs) |

**Pack confirmed OF UI-005-P03.** No stale / wrong-phase / concatenated pack.

---

## 2. Level-I evidence verification (operator transcript, line-by-line)

| # | Mandatory item | Transcript evidence | Verdict |
|---|---|---|---|
| E-1 | 5 named tests DISPLAYED passing | Isolated run → **5 passed (5)** (L153–160): scenarios_render_existing_hypothetical_reports_only / portfolio_research_remains_hypothetical_no_real_account_pnl / comparison_preserves_assumptions_uncertainty_limitations_scope / comparison_contains_no_generation_or_execution_path / scenario_portfolio_accessibility_and_brand_markers_hold | ✅ PASS |
| E-2 | 🔴 R-6 no-recompute / no-scenario-generation grep CLEAN | spine grep incl. `generateScenario` → no output (L457) | ✅ PASS |
| E-3 | 🔴 External-AI grep CLEAN | `openai\|gpt\|external_llm\|llm_summary\|ai_summary` → no output (L458) | ✅ PASS |
| E-4 | 🔴 No-cherry-picking | Source: `uncertaintyText` (lower/upper/method/sample_count), `assumptions`, `limitations`, `source_artifact_ids`, `report_hash` rendered from stored reports; named test #3 passed | ✅ PASS |
| E-5 | 🔴 Portfolio hypothetical (no real account/P&L) | Portfolio renders uncertainty method + source ids; browser "not a live venue record" / `descriptive_count_only` / `not_assessed`; named test #2 passed | ✅ PASS |
| E-6 | 🔴 Whole-surface no-actuation grep CLEAN (B-1 expanded) | `…\|position\|balance\|margin\|capital\|allocation\|real_pnl\|open_gate\|allow_execution` → no output (L468) | ✅ PASS |
| E-7 | No-drift: Alembic head | `alembic current` → **`20260717_0037 (head)`** (L910) | ✅ PASS |
| E-8 | No-drift: deps / endpoint / persistence | package grep = `lightweight-charts@^4.2.0` only; no `/api/v1/investigation-planning`, no CREATE TABLE / persistence markers | ✅ PASS |
| E-9 | No registry / route change (R-1) | `/compare-scenarios` + `/portfolio-research` only; **no `/investigation-planning`** (L934) | ✅ PASS |
| E-10 | No persistence (R-2 — P03 persists nothing) | no `operator_workspace_preferences` write, no key | ✅ PASS |
| E-11 | Regression ≥45f/196t, no test lost | **Gated** `FRONTEND_VITEST_EXIT_CODE: 0` (L1871) → **46 files / 201 tests passed** (L1842–1843; evidence file L294–295) +1 file/+5 tests | ✅ PASS |
| E-12 | Backend ≥414 | `pytest -q` → **414 passed** (two runs) | ✅ PASS |
| E-13 | Doc-16 brand B-1…B-7 | monospace ids/hashes; ARIA; institutional/hypothetical copy; named test #5 + browser | ✅ PASS |
| E-14 | Browser served-session | logged-out `/login` block (closes OBS-P02-1); `/compare-scenarios` side-by-side hypothetical (both `research_only`, hypothetical return, `not_assessed`, assumptions, "does not create or compute scenarios"); `/portfolio-research` hypothetical ("not a live venue record", source ids, `descriptive_count_only`, limitations `descriptive_research_aggregation_only`/`not_a_live_venue_record`) | ✅ PASS |
| E-15 | Networked CI / npm audit | CI exit-1 SOLELY the tracked **TD-UI-POSTCSS-HIGH** (per pre-authorized P03 clause) — see §3 | ⚠️ §3 |

---

## 3. npm audit posture — CI exit-1 solely the tracked TD-UI-POSTCSS-HIGH (pre-authorized)

The CI ran green substantive gates first — pytest **414 passed** (L1609), full frontend **46f/201t** with `FRONTEND_VITEST_EXIT_CODE: 0` (L1871), tsc/build clean — then the npm-audit high gate reported exactly **`3 vulnerabilities (2 moderate, 1 high)`**: `postcss <=8.5.17` GHSA-r28c-9q8g-f849 (high) + 2 react-router moderates → `NPM_AUDIT_HIGH_EXIT_CODE: 1` (L1678) / `LOCAL_CI_EXIT_CODE: 1` / `LOCAL_CI_NONZERO_REVIEW_REQUIRED: 1` (L1648–1649).

This matches **Build-Order §4(k)(ii) exactly**: `LOCAL_CI_EXIT_CODE: 1` attributable **solely** to the tracked `TD-UI-POSTCSS-HIGH` after substantive gates green. The advisory set is identical to the P02 finding (no new advisory). The DA disclosed it and did **not** relabel green. **No new fork required — proceeds under the standing P06 disposition** (no dependency change in P03 scope; presentation-only phase not gated). **TD-UI-POSTCSS-HIGH remains OPEN**; must be remediated/accepted before Production Readiness Certification via a separately-authorized dependency-remediation Build Order.

---

## 4. Constitutional line

| Property | State |
|---|---|
| Governance Gate | CLOSED |
| Scenario generation / what-if engine / portfolio recompute | NONE (no-recompute + `generateScenario` grep clean; "does not create or compute scenarios") |
| Real account / real P&L / real portfolio / live allocation | NONE (portfolio hypothetical; "not a live venue record"; expanded no-actuation grep clean) |
| Cherry-picking | NONE — assumptions/uncertainty/limitations/scope/sample/source-ids/hashes visible |
| External LLM / AI-summary | NONE (external-AI grep clean) |
| Persistence / new table / registry / route | NONE (R-1/R-2 held; head unchanged) |
| Verbatim posture | HELD — scenarios/portfolio rendered from stored reports; `research_only`/`not_assessed` as-stored |

---

## 5. Observations (non-blocking)

- **OBS-P03-1 (CLOSED from OBS-P02-1):** Logged-out `/login` block screenshot supplied this turn — OBS-P02-1 closed.
- **OBS-P03-2 (informational):** TD-UI-POSTCSS-HIGH reproduced on target again (identical advisory set); handled under the standing disposition. A dependency-remediation Build Order should be scheduled before UI-005 completion pressure or Production Readiness Certification, whichever comes first.

---

## 6. Carried standing residuals

- **TD-UI-POSTCSS-HIGH** — high-severity transitive advisory `postcss <=8.5.17` (GHSA-r28c-9q8g-f849) — reproduced on target; OPEN; requires a separately-authorized dependency-remediation Build Order; MUST be remediated/accepted before Production Readiness Certification.
- TD-W7-U07-RATE-GUARD (deferred)
- TD-W6-CI-AUDIT (offline npm-audit env-flake — did NOT occur this turn; audit was networked)
- UI-002-P04b (independent)

---

## 7. Disposition

**UI-005-P03 is APPROVED WITH OBSERVATIONS.** This authorizes issuance of the next Build Order (**UI-005-P04 — Trade Planning & Journal Continuity**) upon operator "authorized". P04 is the **mutation-boundary phase** (R-3 HARD): existing W5 plan/journal create/update may remain but must be proven research-note/reflection fields only — no order/account/broker/position/P&L/execution field, no plan-to-execution path, no broker/account journal import; existing APIs only; forbidden-field-rejection named test required. ITRGA reserves the right (OBS-DP-2) to require P04 be split into separate Trade-Planning and Journal phases if the mutation-boundary evidence is not crisp.

Baseline advances to: **v0.62.0 · head `20260717_0037` · backend 414 · frontend 46f/201t.**

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

**We don't guess. We prove.**

*— AXIOM ITRGA*
