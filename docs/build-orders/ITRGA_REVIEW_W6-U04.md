# ITRGA REVIEW — W6-U04

## Execution Risk Research Reports

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Unit:** W6-U04 (Wave 6) · **Reviewed pack:** `DELIVERY_REPORT_W6-U04.md` + `operator results.md`
**Build Order:** `BUILD_ORDER_W6-U04.md`
**Review date:** 2026-07-17
**Platform of record (pre-unit):** v0.49.0 · head `20260717_0030` · backend 316 / frontend 17f·53t
**Verdict:** 🟡 **CONDITIONAL APPROVAL** — core risk-report unit PROVEN; persistence-capture named-evidence gap (C-1) + migration-proof form (C-2). **Version bump to v0.50.0 HELD** until closure.
**Confidence:** HIGH on what was proven; the conditions are evidence-form gaps, not suspected failures.
**Governance Gate:** CLOSED (verified). **Motto:** *We don't guess. We prove.*

---

## 0. Build-identity check (done FIRST — recurring stale/concatenated-pack risk)

- `DELIVERY_REPORT_W6-U04.md`: Unit W6-U04, cites Build Order + W6-U03 prerequisite; target v0.50.0, head `20260717_0031`. ✔
- `operator results.md` is a **concatenated two-turn pack**: lines ~1–1400 are the **previous W6-U03 transcript** (shows `0030 (head)`, `0.49.0`, ledger tests, `simulated-ledger-entries/.../execute → 405`); the genuine **W6-U04 evidence begins ~line 1400** (`test_execution_risk_reports.py`, `execution-risk-reports` API, `325 passed`, W6-U04 CI). **I evaluated W6-U04 strictly against the W6-U04 half** and did NOT read the stale `0030 (head)` as this unit's migration proof. (Standing lesson reinforced: watch for prepended prior-turn transcripts.)

---

## 1. What is PROVEN (Level-I, operator-run — W6-U04 half)

| # | Requirement | Evidence | Result |
|---|---|---|---|
| b | Named tests | `test_execution_risk_reports.py` **9/9 PASSED** (all 8 named + API) | ✅ |
| — | Full regression | **325 passed** (+9 over 316) — runs against PostgreSQL after CI `Alembic upgrade head` | ✅ |
| f | **No-actuation (CRITICAL)** | `test_execution_risk_report_triggers_nothing_and_writes_report_only` PASS **and** API `/execute → 405` (endpoint proven **absent** — strongest form) | ✅ |
| — | No sizing/account columns (test) | `test_execution_risk_report_has_no_account_capital_margin_or_sizing_columns` PASS | ✅ (raw query owed — see C-1) |
| g | **R6-7 stat ≠ economic** | `test_..._separates_statistical_from_economic_usefulness` PASS; API `CREATE_ECONOMIC_VERDICT: not_assessed` (report explicitly does **not** assert economic success); `CREATE_UNCERTAINTY_METHOD: sample_range_or_single_sample_limitation` | ✅ |
| — | No real-P&L language | `test_execution_risk_report_has_no_real_pnl_or_guaranteed_language` PASS | ✅ |
| — | API auth | `UNAUTH → 401`, `LIST → 200`, `DETAIL → 200`, `SIMULATION_MODE: SIMULATED` | ✅ |
| h | Bright-line (R6-8) | `test_..._create_path_has_no_live_broker_or_gate_path` PASS; operator grep over `execution_research` → "no output" | ✅ |
| i | No barred dependency | barred-list grep → "no output"; existing stack only | ✅ |
| j | CI (GR6-11) | Git-Bash → `LOCAL_CI_EXIT_CODE: 0` → `W6-U04_LOCAL_CI_TRANSCRIPT.txt`; CI ran `Alembic upgrade head against PostgreSQL` then 325 passed | ✅ |
| k | Gate CLOSED (R6-4) | `test_governance_gate_remains_closed_for_wave6` PASS; broker+safety suite **13 passed** | ✅ |
| — | No UI | `ExecutionResearchPage`=False; only `<span>W6-U04</span>` label; frontend 17f·53t | ✅ |

**The "risk engine actuates nothing" red line is proven** — `/execute` is 405-absent, the triggers-nothing test passes, and the API report carries `economic_verdict: not_assessed` with uncertainty. Every *risk* item is green.

---

## 2. CONDITIONS (named mandatory evidence missing on target — must close before FINAL)

### 🟡 C-1 — Persistence-capture raw SELECT + no-orphan audit JOIN + forbidden-column query were NOT operator-run on the target DB (only proven by test + API read-back).
Build Order §5(d)/(e) named, INLINE and mandatory:
- raw `psql SELECT ≥1 row` from **`execution_risk_research_reports`** (structured `risk_metrics`, `uncertainty`, distinct `economic_usefulness`, disclaimer);
- **no-orphan audit JOIN** (`LEFT JOIN audit_events … WHERE ae.id IS NULL`) → `orphan_count 0`;
- `information_schema.columns` **forbidden-column** query (incl. sizing cols) → **0 rows**.

The transcript contains **none** of these against `execution_risk_research_reports` (the string appears **0 times** as a psql target). Persistence was shown via **API create + LIST/DETAIL read-back** — which the Build Order §5(d) and the **standing W4-U02 C-1 rule explicitly state does NOT substitute** for the named raw SELECT + audit JOIN. The `..._persists_and_audit_no_orphan` and `..._no...sizing_columns` **tests** pass (good), but the persistence-capture control requires the operator-run raw SELECT/JOIN/`information_schema` on the reviewed target, not a test-DB assertion alone. This is the standing control applied identically at W6-U02 and W6-U03 (both delivered it); W6-U04 owes the same.
**To close C-1:** run, on target PostgreSQL, the three raw queries and submit command + output (SELECT ≥1 row; `orphan_count 0`; forbidden columns `(0 rows)`).

### 🟡 C-2 — Standalone `alembic current = 20260717_0031` on PostgreSQL not shown in the operator transcript.
The only operator `alembic current` prints `0030 (head)` (the prepended W6-U03 half). The W6-U04 head advance to `0031` is shown only in the DR's **SQLite temp-DB smoke** (Level-IV claim). It is *indirectly* corroborated at Level-I — the CI ran `Alembic upgrade head against PostgreSQL` and then `collected 325 items` passed against that schema — so this is a **minor** form gap, not a suspected failure.
**To close C-2:** submit the operator `alembic current` = `20260717_0031 (head)` on PostgreSQL (one line), and confirm the `20260717_0031_w6_u04_execution_risk_reports.py` revision file exists.

---

## 3. Classification

- **C-1** — MEDIUM (standing persistence-capture control; behavior proven by test + API, but the named raw SELECT + audit JOIN + `information_schema` on target is absent — the exact W4-U02 C-1 substitution the rule forbids).
- **C-2** — LOW (migration head corroborated via CI-on-PostgreSQL + 325 pass; owes the one-line standalone `alembic current`).
- No CRITICAL, no HIGH. No-actuation, no-account/sizing (by test), stat≠economic, bright-line, Gate CLOSED — all proven. Per proportionality (R13): every *risk* item Level-I proven, two *named* evidence items open ⇒ **CONDITIONAL**, not WITHHELD. **v0.50.0 HELD**; platform stays **v0.49.0**.

---

## 4. Not a finding (disclosed)

- The concatenated W6-U03 preamble in `operator results.md` is a re-attachment artifact, not a stale pack — the W6-U04 evidence is genuinely present and was reviewed in isolation.
- `economic_verdict: not_assessed` is **correct**, not a defect — a simulated single-input risk report should not assert economic usefulness (R6-7 stat≠economic).

---

## 5. Path to FINAL

On receipt of C-1 (three raw target-DB queries) and C-2 (one-line `alembic current 0031`), I will write `ITRGA_VERDICT_W6-U04_FINAL.md` superseding this CONDITIONAL, bump to **v0.50.0** / head `20260717_0031`, update onboarding, and W6-U05 becomes authorizable. A single failing item stays a finding; nothing here is relabeled green.

---

## 6. Posture note

Strong unit — the hardest risk (a "risk engine" that must actuate nothing) is proven by an absent `/execute` (405) plus the triggers-nothing test, and economic usefulness is explicitly `not_assessed`. The gap is purely the persistence-capture *evidence form*: the raw SELECT + audit JOIN that W6-U02/U03 both delivered and that the standing control requires. Close it and this unit is FINAL.

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
