# ITRGA DETERMINATION — UI-005-P04

**Trade Planning & Journal Continuity — Mutation-Boundary Phase**

| Field | Value |
|---|---|
| Authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-005 — Investigation & Planning Workspace |
| Phase | **UI-005-P04** |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-005-P04.md` |
| Governing docs | Doc 12 §7, `UI-005_ENGINEERING_DESIGN_PLAN.md` §10 (P04)/§4.3, `ITRGA_REVIEW_UI-005_DESIGN_PLAN.md` (R-1…R-7, esp. R-3), Doc 16 |
| Evidence standard | Level-I (operator-run on target) — report-claims alone never approve |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 46f/201t |
| **DETERMINATION** | ✅ **APPROVED WITH OBSERVATIONS** |
| Governance Gate | CLOSED (unchanged) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Build-identity verification (performed FIRST)

| Check | Result |
|---|---|
| Delivery report | `# DELIVERY REPORT — UI-005-P04` · Phase `**UI-005-P04**` (467 lines) — OF the unit |
| Operator transcript | Same session; greps `DELIVERY_REPORT_UI-005-P04.md` + `BUILD_ORDER_UI-005-P04.md` (1982 lines) — OF the unit |
| Predecessor | `ITRGA_REVIEW_UI-005-P03.md` (Approved-w-Obs) |

**Pack confirmed OF UI-005-P04.** No stale / wrong-phase / concatenated pack.

---

## 2. Level-I evidence verification (operator transcript, line-by-line)

| # | Mandatory item | Transcript evidence | Verdict |
|---|---|---|---|
| E-1 | 5 named tests DISPLAYED passing (incl. forbidden-field-rejection) | Isolated run → **5 passed (5)** (L62–69): trade_plans_use_existing_research_note_store_no_order_ticket / journal_uses_existing_reflection_store_no_broker_import / **planning_preserves_research_only_fields_and_forbidden_field_rejection** / plan_journal_links_are_artifact_ids_not_execution_paths / planning_journal_accessibility_and_brand_markers_hold | ✅ PASS |
| E-2 | 🔴 R-3 mutation-boundary proof (DB schema) | **Raw psql schema audit**: `trade_plan_notes` (16 cols, all research-note) + `manual_trade_journal_entries` (14 cols, all reflection); **`forbidden_w5_column_count: 0`** for `(order\|broker\|account\|position\|balance\|margin\|capital\|allocation\|real_pnl\|pnl\|execution\|fill\|quantity\|size)` (L462–509) | ✅ PASS (exemplary) |
| E-3 | 🔴 R-6 no-recompute + external-AI grep | clean | ✅ PASS |
| E-4 | 🔴 Whole-surface no-actuation grep (B-1 expanded) | `$actuationPattern` run (L272); clean | ✅ PASS |
| E-5 | Plan/journal links are artifact ids, not execution paths | named test #4 passed; browser shows Linked signal/report ids as context pointers | ✅ PASS |
| E-6 | No-drift: Alembic head | `alembic current` → **`20260717_0037 (head)`** (L296) | ✅ PASS |
| E-7 | No-drift: deps / endpoint / persistence key | `UI005_P04_NO_NEW_ENDPOINT_OR_PERSISTENCE_KEY`; manifest content displayed, no dep change | ✅ PASS |
| E-8 | No registry / route change (R-1) | `/trade-plans` + `/journal` only; `UI005_P04_REGISTRY_EXISTING_ROUTES_ONLY`; no `/investigation-planning` | ✅ PASS |
| E-9 | Backend ≥414 | `pytest -q` → **414 passed** (2488s — extraordinarily loaded machine) | ✅ PASS |
| E-10 | Browser served-session | logged-out `/login`; `/trade-plans` research-note editor (Title/Market context/Hypothesis/Linked signal-report ids/Scenario notes/Risk notes — **no order-ticket/position-sizing/broker fields**); `/journal` reflection editor (reflection text/linked ids/emotion-process tags/lesson notes — **no broker/account import**); GATE CLOSED/RESEARCH-ONLY framing | ✅ PASS |
| E-11 | **Gated full-suite exit 0 / ≥46f/201t, no test lost** | **🔴 RED — `FRONTEND_VITEST_EXIT_CODE: 1`; `1 failed \| 205 passed (206)`; DA script threw `FRONTEND_VITEST_FAILED:1`** (L1440–1475) | ⚠️ **FINDING — OBS-P04-1 (operator-adjudicated)** |
| E-12 | Networked CI | `LOCAL_CI_EXIT_CODE: 1` — **compound** of the vitest failure + tracked postcss-high (NOT solely the residual this turn) — see §4 | ⚠️ §4 |

---

## 3. Constitutional line — R-3 held at the strongest level

| Property | State |
|---|---|
| Governance Gate | CLOSED |
| Plan/journal mutation expansion | NONE — **DB schema proves 0 forbidden columns**; only research-note/reflection fields exist |
| Order / broker / account / position / balance / margin / capital / allocation / P&L / execution / fill / quantity / size field | NONE (raw psql `forbidden_w5_column_count: 0`; no-actuation grep clean) |
| Plan-to-execution path | NONE (named test #4; links are artifact ids only) |
| Broker/account journal import | NONE |
| New endpoint / table / dependency / registry / route / persistence key | NONE (R-1/R-2 held; head unchanged) |
| Recompute / inference / external AI | NONE (greps clean) |

**R-3 is proven at the database schema level — the strongest possible mutation-boundary evidence.** The split reservation (OBS-DP-2) is NOT triggered: the forbidden-field-rejection test is present and passing, the field schema is unambiguous (enumerated columns), and plan/journal boundaries are cleanly separated.

---

## 4. 🔴 RED GATE FINDING — the full-suite failure (operator-adjudicated to Observation)

**A red gate is a finding, not a footnote.** The gated full frontend suite returned **RED**:
- `Test Files 1 failed | 46 passed (47)`; `Tests 1 failed | 205 passed (206)`; `FRONTEND_VITEST_EXIT_CODE: 1`; DA script threw `FRONTEND_VITEST_FAILED:1`.
- **The single failure** is `ResearchPerformanceAnalytics.test.tsx > UI-004-P02b > test_ui004_analytics_accessibility_and_brand_markers_hold` — **`Test timed out in 10000ms`** (ran 12304 ms, L1289/L1426–1429).

Assessment: this is a **10 s-timeout flake on a pre-existing UI-004-P02b test — NOT P04 code, NOT an assertion failure** — the **same class as OBS-P04-1** (which hardened only the two UI-001/UI-002 route-loop tests to 30000 ms; this UI-004-P02b test was left at the default 10 s cap). The machine was extraordinarily loaded this session (backend pytest took **41 minutes**; environment 750 s). The 5 P04 named tests and all R-3 evidence passed cleanly.

**Crucial discipline point: there is NO clean green re-run in this pack** (unlike UI-004-P04, which had an 11:58 green re-run). The red gate therefore stands unresolved in the evidence.

**Operator disposition (this review):** record as a timeout flake; approve P04 on the exemplary R-3 evidence; make the fix + proof a **mandatory, non-optional item at UI-005-P05** (below). This red gate is **documented as a finding and NOT relabeled green.**

---

## 5. Observations

- **OBS-P04-1 (RED GATE — MANDATORY closure at P05):** The gated full suite failed on `ResearchPerformanceAnalytics.test.tsx > test_ui004_analytics_accessibility_and_brand_markers_hold` (10 s timeout). At **UI-005-P05 the DA MUST**: (a) add an explicit `testTimeout` to this test (same remedy applied to the OBS-P04-1 route-loop tests), and (b) supply a **clean gated `FRONTEND_VITEST_EXIT_CODE: 0` full-suite re-run**. This is non-waivable at P05. (Recurring lesson: timeout-fragile tests at the default 10 s cap must be hardened whenever the machine is loaded.)
- **OBS-P04-2 (CI exit-1 is COMPOUND this turn):** `LOCAL_CI_EXIT_CODE: 1` this turn is NOT solely the tracked postcss-high — it also carries the vitest failure. The postcss-high (`3 vulnerabilities (2 moderate, 1 high)`) still reproduces (TD-UI-POSTCSS-HIGH, unchanged); the additional cause is the E-11 timeout. Both are surfaced, not relabeled.

---

## 6. Carried standing residuals

- **TD-UI-POSTCSS-HIGH** — reproduced again; OPEN; separately-authorized dependency-remediation Build Order required before Production Readiness Certification.
- TD-W7-U07-RATE-GUARD (deferred)
- TD-W6-CI-AUDIT (offline npm-audit env-flake — not the cause this turn)
- UI-002-P04b (independent)

---

## 7. Disposition

**UI-005-P04 is APPROVED WITH OBSERVATIONS.** R-3 mutation-boundary is proven at the strongest level (DB schema audit, forbidden_w5_column_count=0). This authorizes issuance of the next Build Order (**UI-005-P05 — Execution Research / SIMULATED Evidence Context**) upon operator "authorized" — **carrying the mandatory OBS-P04-1 closure** (harden the ResearchPerformanceAnalytics accessibility test testTimeout + supply a green gated `FRONTEND_VITEST_EXIT_CODE: 0` full-suite re-run).

Baseline advances to: **v0.62.0 · head `20260717_0037` · backend 414 · frontend 46f/201t** (unchanged — the +1 file/+5 tests from P04 are counted once the gated suite is green at P05; the 206-test total was recorded on a red run and is not adopted as the baseline of record until a green gated run confirms it).

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

**We don't guess. We prove.**

*— AXIOM ITRGA*
