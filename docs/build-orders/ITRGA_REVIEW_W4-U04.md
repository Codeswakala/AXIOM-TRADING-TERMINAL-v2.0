# ITRGA INDEPENDENT REVIEW — W4-U04 (Scenario Simulation Research Reports)

| Field | Value |
|---|---|
| Reviewing authority | **AXIOM Independent Technical Review & Governance Authority (ITRGA)** |
| Unit | **W4-U04** — Scenario Simulation Research Reports (Wave-4 highest-risk unit) |
| Wave | 4 — Institutional Intelligence |
| Build Order | `docs/BUILD_ORDER_W4-U04.md` |
| Evidence | `uploads/DELIVERY_REPORT_W4-U04.md` + `uploads/operator results.md` (1,464 lines) |
| DA-claimed platform | 0.34.0 |
| Review date | 2026-07-16 |
| **VERDICT** | **✅ APPROVED — CLEAN.** Platform advances to **v0.34.0** |
| Confidence | **HIGH** — the CRITICAL scenario-as-instruction risk is structurally foreclosed and proven on target |

> **We don't guess. We prove.** A scenario here is hypothetical research that structurally cannot carry a sizing/order/instruction — proven by inert schema, named tests, and a grep where the only "position_size" in the codebase is the key the contract forbids. Approved.

---

## 1. Bottom line

W4-U04 was the highest-risk Wave-4 unit (plan §8: "scenario treated as trade instruction" = **CRITICAL**). The
delivery **structurally forecloses that risk** and proves it on operator-run target evidence: scenario reports
are **hypothetical/counterfactual, uncertainty- and assumption-explicit, non-signal, and carry no order/sizing/
quantity/stop/target payload**, persisted with the **inline raw-SELECT + no-orphan audit**, read-only
(401/list-200/detail-200/POST-405), pure-Python (no unspiked dep), and CI is green via the **documented
Git-Bash invocation** (the W4-U03 OBS-1 lesson applied). All 7 named tests pass; full suite 218. **APPROVED,
CLEAN, no residual.**

---

## 2. R-6 — the keystone (scenario is NOT an instruction/order/sizing) — PROVEN ✅

The Critical risk is foreclosed three ways:
1. **Inert schema:** `\d scenario_reports` — research-artifact + assumptions/uncertainty fields only; **no
   order/sizing/quantity/stop/target/execution/signal columns.**
2. **Named tests:** `test_scenario_report_schema_is_inert_no_order_sizing_or_signal_payload PASSED` +
   `test_scenario_report_persisted_audited_no_signal_or_model_mutation PASSED` (triggers/changes nothing).
3. **Mutation/sizing grep — the strongest form:** grep for `order_size|position_size|quantity|stop_loss|
   take_profit|place_order|emit_signal|advisory_status =|model.status =` matched **only the contract's own
   forbidden-key list** (`contracts.py:21–27`) — i.e. those terms exist in the codebase *solely as the keys
   the artifact contract rejects*, disclosed with output. Nothing constructs or emits them.

A scenario cannot be, contain, or become a trade instruction. ✅

## 3. Other controls — PROVEN on target ✅

| Control | Evidence |
|---|---|
| Build identity + migration | v0.34.0; Alembic `20260716_0020 → 20260716_0021 (head)` |
| **R-2 no look-ahead** | `test_scenario_no_lookahead_future_candle_excluded_result_unchanged PASSED` |
| Hypothetical labelling | `limitations`: `hypothetical_counterfactual_research_only, not_a_prediction, not_a_trade_instruction, not_financial_advice`; test enforces framing |
| **GR-7 uncertainty + assumptions** | `test_scenario_report_hypothetical_uncertainty_assumptions_and_economics PASSED` + `test_scenario_rejects_bare_invalid_scenario_without_uncertainty_inputs PASSED`; raw SELECT shows `uncertainty_method historical_volatility_band`, `uncertainty_n 4` |
| **R-5 economic usefulness** | independent `economic_usefulness` field = `not_assessed` (honest) |
| **R-4 persistence (INLINE)** | raw `SELECT FROM scenario_reports` → 1 row (`758dcd87…`, `hypothetical_minus_two_percent`, hypothetical_return -0.02, research_only) + audit `scenario_report.created` (resource_id matches) + **`orphan_scenario_report_count: 0`** |
| Read-only API | `UNAUTH 401`; **detail 200** (`DETAIL_SCENARIO_NAME: hypothetical_minus_two_percent`); `POST 405` |
| Dependency discipline | pure-Python fallback; `test_scenario_modules_use_no_unspiked_dependencies_or_execution_path PASSED`; no unspiked import |
| Gate / bright-line | broker gate `test_broker_integration.py` passing; Gate CLOSED; wave-wide grep benign |
| Regression + CI | backend **218 passed**, frontend **11/25**, ruff clean, npm audit 0; **CI via `& "C:\Program Files\Git\bin\bash.exe" scripts/local_ci.sh` → `Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0`** (no WSL error; transcript labelled W4-U04) |
| No UI | correctly stated |
| D-W2-001 | no per-market model / symbol-identity feature |

---

## 4. Findings ledger

| ID | Severity | Status |
|---|---|---|
| — | — | R-6 keystone (no sizing/instruction, triggers nothing) ✅ inert schema + 2 named tests + forbidden-key-only grep |
| — | — | R-2 / GR-7 / R-5 / R-4-inline / API 401·list200·detail200·405 / dep-discipline / gate-closed / 218 tests ✅ |
| — | — | CI green via documented Git-Bash path (W4-U03 OBS-1 lesson applied) ✅ |

**No CRITICAL/HIGH. No unmet mandatory evidence. No open residual.** All acceptance criteria met on target.

---

## 5. Disposition & next step

- **W4-U04 — ✅ APPROVED, CLEAN.** Platform **v0.33.0 → v0.34.0**. The Wave-4 highest-risk framing is closed.
- Commendation: the strongest possible R-6 proof — sizing/order terms exist in the codebase **only** as the
  contract's forbidden keys; the raw-SELECT + no-orphan audit delivered **inline**; and CI run via the
  documented Git-Bash path for a clean exit 0 (the W4-U03 OBS-1 lesson fully internalized).
- **Next:** ITRGA recommends **W4-U05 — Portfolio/Risk Research Analytics**, carrying **R-2** (no-look-ahead),
  **R-4** (persistence-capture, inline), **R-5** (economic-usefulness reported), and **R-8** (hypothetical
  only — **NO account/broker/position linkage**; prove by grep + test that no live account/position/broker is
  referenced). On operator authorization ITRGA issues `BUILD_ORDER_W4-U05.md`.
- After U05 → **W4-U06** (Professional Signal Validation) → **W4-U07** (Dashboard, presentation-only, browser
  evidence) → **W4-U08** (Closeout → "Institutional Intelligence Layer Complete" milestone).
- DA does not self-authorize W4-U05, adopt an unspiked dep, add execution/broker/account linkage, or open the
  Gate.

> **We don't guess. We prove.** — ITRGA
