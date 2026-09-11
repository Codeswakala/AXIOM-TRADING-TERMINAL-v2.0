# ITRGA INDEPENDENT REVIEW — W4-U05 (Portfolio/Risk Research Analytics)

| Field | Value |
|---|---|
| Reviewing authority | **AXIOM Independent Technical Review & Governance Authority (ITRGA)** |
| Unit | **W4-U05** — Portfolio/Risk Research Analytics |
| Wave | 4 — Institutional Intelligence |
| Build Order | `docs/BUILD_ORDER_W4-U05.md` |
| Evidence | `uploads/DELIVERY_REPORT_W4-U05.md` + `uploads/operator results.md` (1,579 lines) |
| DA-claimed platform | 0.35.0 |
| Review date | 2026-07-16 |
| **VERDICT** | **✅ APPROVED — CLEAN.** Platform advances to **v0.35.0** |
| Confidence | **HIGH** — the R-8 account/position-linkage boundary is structurally foreclosed and proven on target |

> **We don't guess. We prove.** Risk analytics here are hypothetical market-series research that structurally cannot touch a real account or position — proven by inert schema, a named test, and a grep where the only `broker_account_id` in the codebase is the key the contract forbids. Approved.

---

## 1. Bottom line

W4-U05 delivers hypothetical, uncertainty-mandatory risk analytics that **structurally cannot reference a real
account, broker, or live position (R-8)**, carry **no guaranteed-return framing**, are look-ahead-safe (R-2),
non-signal (R-6), and persisted with the **inline raw-SELECT + no-orphan audit (R-4)**. Read-only
(401/list-200/detail-200/POST-405), pure-Python (no unspiked dep), CI green via the documented Git-Bash path.
All 7 named tests pass; full suite 225. **APPROVED, CLEAN, no residual.**

---

## 2. R-8 — the keystone (no account/broker/position linkage) — PROVEN ✅

Foreclosed three ways:
1. **Inert schema:** `\d portfolio_risk_reports` — research-artifact + market-series risk fields
   (max_drawdown, realized_volatility, stress_loss, uncertainty, assumptions) only; **no account/broker/
   position/order columns.**
2. **Named test:** `test_portfolio_risk_schema_has_no_account_broker_position_or_order_linkage PASSED`.
3. **Linkage grep — the strongest form:** grep for `broker_account|account_id|position_id|holding|
   live_position|place_order|order_payload|advisory_status =|model.status =` matched **only the contract's own
   forbidden-key list** (`contracts.py:15 "order_payload"`, `:20 "broker_account_id"`) — those terms exist in
   the codebase *solely as keys the artifact rejects*, disclosed with output. The service reads no broker/
   account/position source. ✅

The "unless future governance authorizes" clause (plan §5.4) is correctly **deferred/out of scope.**

## 3. Other controls — PROVEN on target ✅

| Control | Evidence |
|---|---|
| Build identity + migration | v0.35.0; Alembic `20260716_0021 → 20260716_0022 (head)` |
| No guaranteed return (§8 HIGH) | `limitations` hypothetical/not-guaranteed; test enforces framing |
| **GR-7 + R-5** | `test_portfolio_risk_metrics_have_uncertainty_and_economic_usefulness PASSED` + `test_portfolio_risk_rejects_invalid_bare_metric_assumptions PASSED`; raw SELECT shows per-metric `uncertainty_method volatility_scaled_interval`, `uncertainty_n 5`; independent `economic_verdict not_assessed` |
| **R-2 no look-ahead** | `test_portfolio_risk_no_lookahead_future_candle_excluded_metrics_unchanged PASSED` |
| **R-6 non-signal / no mutation** | `test_portfolio_risk_persisted_audited_no_signal_or_model_mutation PASSED`; grep benign |
| **R-4 persistence (INLINE)** | raw `SELECT FROM portfolio_risk_reports` → 1 row (`7fa133fc…`, max_drawdown -0.0294, realized_vol 0.0285, stress_loss -0.0588, research_only) + audit `portfolio_risk_report.created` (resource_id matches) + **`orphan_portfolio_risk_report_count: 0`** |
| Read-only API | `UNAUTH 401`; **detail 200** (`DETAIL_MAX_DRAWDOWN: -0.0294`, `DETAIL_UNCERTAINTY_METHOD: volatility_scaled_interval`, `DETAIL_ECONOMIC_VERDICT: not_assessed`); `POST 405` |
| Dependency discipline | pure-Python fallback; `test_portfolio_risk_modules_use_no_unspiked_dependencies_or_execution_path PASSED`; no unspiked import |
| Gate / bright-line | broker gate `test_broker_integration.py` passing incl. `test_governance_gate_refuses_connect_and_execute`; Gate CLOSED |
| Regression + CI | backend **225 passed**, frontend **11/25**, ruff clean, npm audit 0; **CI via `& "C:\Program Files\Git\bin\bash.exe" scripts/local_ci.sh` → `Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0`** (transcript labelled W4-U05, no WSL error) |
| No UI | correctly stated |
| D-W2-001 | no per-market model / symbol-identity feature |

---

## 4. Findings ledger

| ID | Severity | Status |
|---|---|---|
| — | — | R-8 keystone (no account/broker/position linkage) ✅ inert schema + named test + forbidden-key-only grep |
| — | — | R-2 / GR-7 / R-5 / R-6 / R-4-inline / API 401·list200·detail200·405 / dep-discipline / gate-closed / 225 tests / CI exit 0 ✅ |

**No CRITICAL/HIGH. No unmet mandatory evidence. No open residual.** All acceptance criteria met on target.

---

## 5. Disposition & next step

- **W4-U05 — ✅ APPROVED, CLEAN.** Platform **v0.34.0 → v0.35.0**.
- Commendation: the R-8 proof in its strongest form (account/broker/position terms appear **only** as the
  contract's forbidden keys), the raw-SELECT + no-orphan audit **inline**, and CI via the documented Git-Bash
  path for a clean exit 0 — every prior lesson held.
- **Next:** ITRGA recommends **W4-U06 — Professional Signal Validation Extension**, carrying **R-2** (no
  look-ahead), **R-4** (persistence-capture, inline), **R-5** (economic-usefulness reported), **R-6**
  (non-signal), plus (plan §5.5) **raw-score-exclusion preserved** and **no cherry-picking** (validate against
  pre-registered/persisted signals honestly; no selective window/metric that flatters). On operator
  authorization ITRGA issues `BUILD_ORDER_W4-U06.md`.
- After U06 → **W4-U07** (Institutional Intelligence Dashboard — presentation-only, **browser evidence
  mandatory**) → **W4-U08** (Closeout → "Institutional Intelligence Layer Complete" milestone).
- DA does not self-authorize W4-U06, adopt an unspiked dep, add execution/broker/account linkage, or open the
  Gate.

> **We don't guess. We prove.** — ITRGA
