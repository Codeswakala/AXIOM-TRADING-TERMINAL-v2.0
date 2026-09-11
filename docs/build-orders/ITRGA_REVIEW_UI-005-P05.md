# ITRGA DETERMINATION — UI-005-P05

**Execution Research / SIMULATED Evidence Context**

| Field | Value |
|---|---|
| Authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-005 — Investigation & Planning Workspace |
| Phase | **UI-005-P05** |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-005-P05.md` |
| Governing docs | Doc 12 §7, `UI-005_ENGINEERING_DESIGN_PLAN.md` §10 (P05), `ITRGA_REVIEW_UI-005_DESIGN_PLAN.md` (R-1…R-7, esp. R-4), Doc 16 |
| Evidence standard | Level-I (operator-run on target) — report-claims alone never approve |
| Baseline entering phase | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 46f/201t (held pending green gated run) |
| **DETERMINATION** | ✅ **APPROVED WITH OBSERVATIONS** |
| Governance Gate | CLOSED (unchanged) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Build-identity verification (performed FIRST)

| Check | Result |
|---|---|
| Delivery report | `# DELIVERY REPORT — UI-005-P05` · Phase `**UI-005-P05**` (471 lines); explicitly acknowledges carrying mandatory OBS-P04-1 closure — OF the unit |
| Operator transcript | Same session; greps `DELIVERY_REPORT_UI-005-P05.md` + `BUILD_ORDER_UI-005-P05.md` (1833 lines) — OF the unit |
| Predecessor | `ITRGA_REVIEW_UI-005-P04.md` (Approved-w-Obs) |

**Pack confirmed OF UI-005-P05.** No stale / wrong-phase / concatenated pack.

---

## 2. 🔴🔴 OBS-P04-1 CLOSURE — SATISFIED (the mandatory, non-waivable item)

| Requirement | Evidence | Verdict |
|---|---|---|
| (a) Explicit `testTimeout` added to the timeout-fragile test | `ResearchPerformanceAnalytics.test.tsx:206: }, 30000);` on `test_ui004_analytics_accessibility_and_brand_markers_hold` (L103–105) | ✅ CLOSED |
| (b) Clean gated `FRONTEND_VITEST_EXIT_CODE: 0` full-suite re-run | **`FRONTEND_VITEST_EXIT_CODE: 0`** (L654) → **Test Files 48 passed (48) / Tests 211 passed (211)** (L619–620; evidence file L220–221); the previously-failing `ResearchPerformanceAnalytics` tests now all `✓` (L625–633) | ✅ CLOSED |

**The P04 red gate is resolved with a genuinely green gated run.** Baseline of record is now adopted at **48f/211t** (P04 +5 and P05 +5, no test lost).

---

## 3. Level-I evidence verification (operator transcript, line-by-line)

| # | Mandatory item | Transcript evidence | Verdict |
|---|---|---|---|
| E-1 | 5 named tests DISPLAYED passing | Isolated run → **5 passed (5)** (L77–78): execution_research_renders_existing_simulated_artifacts_only / never_claims_live_execution_or_real_fills / preserves_assumptions_uncertainty_limitations / contains_no_broker_order_account_or_gate_path / accessibility_and_brand_markers_hold | ✅ PASS |
| E-2 | 🔴 R-4 SIMULATED proof | Disclaimer "SIMULATED execution research only. Display-only evidence… AXIOM does not act"; cards aria "Simulated run/fill/ledger"; "Persisted SIMULATED artifacts"; read source `fetchExecutionResearchBundle`; `UI005_P05_SIMULATED_NEVER_LIVE_REAL_SOURCE_GREP_CLEAN` (L14–97) | ✅ PASS |
| E-3 | 🔴 R-6 no-recompute + external-AI grep | clean | ✅ PASS |
| E-4 | 🔴 Whole-surface no-actuation grep (B-1 expanded) | `$actuationPattern` incl. broker/order/account/open_gate/allow_execution — clean (L117) | ✅ PASS |
| E-5 | Assumptions/uncertainty/limitations preserved | named test #3 + source + browser (limitations `simulated_research_only`/`not_live_instruction`/`not_real_profit_loss`/`no_account_or_broker_linkage`/`no_actuating_sizing_output`/`economic_usefulness_not_assessed`) | ✅ PASS |
| E-6 | No-drift: Alembic head | `alembic current` → **`20260717_0037 (head)`** (L141) | ✅ PASS |
| E-7 | No-drift: deps / endpoint / persistence | no new dep; no `/api/v1/investigation-planning`; no persistence key | ✅ PASS |
| E-8 | No registry / route change (R-1) | `/execution-research` only; no `/investigation-planning` (L143); `$badRouteHits` empty | ✅ PASS |
| E-9 | No persistence (R-2 — P05 persists nothing) | no `operator_workspace_preferences` write, no key | ✅ PASS |
| E-10 | Regression ≥46f/201t, no test lost, GATED exit 0 | **48f/211t, `FRONTEND_VITEST_EXIT_CODE: 0`** (see §2) | ✅ PASS |
| E-11 | Backend ≥414 | `pytest -q` → **414 passed** (L1295) | ✅ PASS |
| E-12 | Doc-16 brand B-1…B-7 | monospace ids/hashes; SIMULATED badges; ARIA; institutional/SIMULATED copy; named test #5 + browser | ✅ PASS |
| E-13 | Browser served-session | logged-out `/login`; `/execution-research` every card badged **SIMULATED**, `research_only`, assumptions/uncertainty/limitations, Replay scope, no live/real/broker/account fields; GATE CLOSED/RESEARCH-ONLY framing | ✅ PASS |
| E-14 | Networked CI | `LOCAL_CI_EXIT_CODE: 1` SOLELY the tracked TD-UI-POSTCSS-HIGH — see §4 | ⚠️ §4 |

---

## 4. npm audit posture — CI exit-1 solely the tracked TD-UI-POSTCSS-HIGH (pre-authorized clause)

The CI ran green substantive gates first — full frontend **48f/211t** with `FRONTEND_VITEST_EXIT_CODE: 0`, backend **414 passed** (L1295), tsc/build clean — then the npm-audit high gate reported the **identical** advisory set `3 vulnerabilities (2 moderate, 1 high)` (postcss `<=8.5.17` GHSA-r28c-9q8g-f849 + 2 react-router moderates) → `NPM_AUDIT_HIGH_EXIT_CODE: 1` / `LOCAL_CI_EXIT_CODE: 1` / `LOCAL_CI_NONZERO_REVIEW_REQUIRED: 1` (L1334–1335).

This matches **Build-Order §4(l)(ii) exactly**: exit-1 attributable **solely** to the tracked `TD-UI-POSTCSS-HIGH` after substantive gates green. **Unlike P04, there is NO vitest failure this turn** — the OBS-P04-1 timeout is fixed and the gated run is green. DA disclosed, did not relabel green. **Proceeds under the standing P06 disposition** (no dependency change in P05 scope). TD-UI-POSTCSS-HIGH remains OPEN for pre-certification remediation.

---

## 5. Constitutional line — R-4 held

| Property | State |
|---|---|
| Governance Gate | CLOSED |
| Live execution / real fill / real order / broker / account / real P&L / Gate | NONE — SIMULATED/display-only; no-actuation grep clean; limitations `not_live_instruction`/`not_real_profit_loss`/`no_account_or_broker_linkage`/`no_actuating_sizing_output` |
| SIMULATED labeling | HELD — every surface badged SIMULATED, never relabeled live/real |
| Recompute / inference / external AI | NONE (greps clean) |
| Persistence / new table / registry / route | NONE (R-1/R-2 held; head unchanged) |

---

## 6. Observations (non-blocking)

- **OBS-P05-1 (CLOSED — OBS-P04-1 fully resolved):** testTimeout hardened + green gated `FRONTEND_VITEST_EXIT_CODE: 0` (48f/211t) supplied. The recurring timeout-flake lesson is now applied to this test too.
- **OBS-P05-2 (informational):** TD-UI-POSTCSS-HIGH reproduced again (identical set); CI exit-1 is solely this residual per the pre-authorized clause. A dependency-remediation Build Order should be scheduled at or before the UI-005-P06 completion checkpoint (recommend addressing before declaring UI-005 COMPLETE, or explicitly carrying it as an accepted pre-cert residual at completion).

---

## 7. Carried standing residuals

- **TD-UI-POSTCSS-HIGH** — reproduced again; OPEN; separately-authorized dependency-remediation Build Order required before Production Readiness Certification.
- TD-W7-U07-RATE-GUARD (deferred)
- TD-W6-CI-AUDIT (offline npm-audit env-flake — not the cause this turn)
- UI-002-P04b (independent)

---

## 8. Disposition

**UI-005-P05 is APPROVED WITH OBSERVATIONS.** R-4 SIMULATED/display-only is held; the mandatory OBS-P04-1 closure is satisfied with a genuine green gated run. This authorizes issuance of the final Build Order (**UI-005-P06 — Completion Checkpoint**) upon operator "authorized" — which will declare 🏛️ UI-005 COMPLETE on approval, carrying the standing constitutional + Doc-16 brand + full-suite (≥48f/211t, no test lost) + backend (≥414) validation, and a decision point on TD-UI-POSTCSS-HIGH (remediate before completion, or accept as a documented pre-certification residual).

Baseline advances to: **v0.62.0 · head `20260717_0037` · backend 414 · frontend 48f/211t.**

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

**We don't guess. We prove.**

*— AXIOM ITRGA*
