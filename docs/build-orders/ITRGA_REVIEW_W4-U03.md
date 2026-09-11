# ITRGA INDEPENDENT REVIEW — W4-U03 (Regime Detection Reports)

| Field | Value |
|---|---|
| Reviewing authority | **AXIOM Independent Technical Review & Governance Authority (ITRGA)** |
| Unit | **W4-U03** — Regime Detection Reports |
| Wave | 4 — Institutional Intelligence |
| Build Order | `docs/BUILD_ORDER_W4-U03.md` |
| Evidence | `uploads/DELIVERY_REPORT_W4-U03.md` + `uploads/operator results.md` (1,042 lines) |
| DA-claimed platform | 0.33.0 |
| Review date | 2026-07-16 |
| **VERDICT** | **✅ APPROVED WITH OBSERVATIONS.** Platform advances to **v0.33.0** |
| Confidence | **HIGH** — all functional/governance gates proven on target; the lone red exit code is a proven-unrelated WSL shell artifact |

> **We don't guess. We prove.** Regime detection is explainable, look-ahead-safe, market-agnostic, non-signal, persisted+audited inline. The one red gate is a `/bin/bash` WSL spawn error, not a product failure — noted, not called green.

---

## 1. Bottom line

W4-U03 meets every functional and governance requirement on operator-run target evidence: **explainable-rule
regime labels over normalized features (no symbol identity, R-7), look-ahead-safe (R-2), confidence/
uncertainty on every label (GR-7), non-signal + no model mutation (R-6), persisted with the raw-SELECT +
no-orphan audit delivered INLINE (R-4 — the W4-U02 C-1 lesson applied), read-only API 401/list-200/detail-200/
POST-405, pure-Python rules (no learned model, no unspiked dep).** All 7 named tests pass; full suite 211.

The single red signal — `LOCAL_CI_EXIT_CODE: 1` — is investigated and **proven unrelated**: it is a WSL shell
error (`execvpe(/bin/bash) failed: No such file or directory`) caused by invoking CI with a bare `bash`
(→ WSL relay) instead of the documented Git-Bash path, *after* every gate ran green. Per the W3-U04/W3-U08
precedent (a red gate from a proven-unrelated environment artifact is a finding, not a withhold — never
relabelled green), this is **APPROVED WITH OBSERVATIONS**, with a required clean CI re-run (OBS-1).

---

## 2. What is PROVEN on target ✅

### 2.1 Build identity + migration
`Test-Path`×N True (BUILD_ORDER/ADR-042/`regime.py`/`regime_report.py`/test); v0.33.0. Alembic
`20260716_0019 → 20260716_0020 (head)`. `\d regime_reports` shows research-artifact fields + `audit_
correlation_id`; **no order/execution/broker/remediation/signal columns** (inert by schema).

### 2.2 R-2 no-look-ahead — proven twice
Named test `test_regime_no_lookahead_future_candle_excluded_label_unchanged PASSED`; live artifact
`excluded_future_candle_count: 1` (raw SELECT + payload). Backward-looking windows. ✅

### 2.3 R-7 market-agnostic — the keystone, proven
- Named test `test_regime_market_agnostic_same_normalized_inputs_same_label_without_symbol_feature PASSED`.
- Persisted + API field `feature_policy: normalized_features_no_symbol_identity`; `limitations` includes
  `normalized_features_exclude_symbol_identity`. Symbol stored only as metadata/lineage, **not a feature**.
- Explainable rules; **no learned/clustering model** (so no pre-registration/spike needed); no per-market
  model. D-W2-001 Option A + 07_ML_SPEC "avoid learning symbol identities" honored. ✅

### 2.4 GR-7 uncertainty + explainability
Raw SELECT: `regime_label trend`, `confidence 0.93`, `uncertainty_method threshold_margin_confidence_band`,
`uncertainty_n 5`, evidence carries feature values/thresholds. Named test
`test_regime_report_has_confidence_uncertainty_and_explainable_evidence PASSED`; bare-label rejected.
`economic_verdict not_assessed` (separate from statistical). ✅

### 2.5 R-6 non-signal + no model mutation
`test_regime_report_persisted_audited_no_signal_or_model_mutation PASSED` +
`test_regime_report_schema_is_inert_no_order_remediation_or_signal_payload PASSED`; grep for
`advisory_status =|model.status =|emit_signal|order_payload` benign. Regime triggers/changes nothing. ✅

### 2.6 R-4 persistence — INLINE raw SELECT + no-orphan audit (W4-U02 C-1 lesson applied)
For `43d8b2d4-…`:
- **Raw `SELECT … FROM regime_reports`** → **1 row** (label trend, confidence 0.93, feature_policy
  normalized_features_no_symbol_identity, excluded_future 1, research_only).
- **Audit LEFT JOIN** → `regime_report.created`, resource_id matches, correlation id present.
- **`orphan_regime_report_count: 0`.** ✅ (Delivered inline this time — the C-1 gap did not recur.)

### 2.7 Read-only API (full)
`UNAUTH_REGIME_STATUS: 401`; **detail** `GET /{report_id}` → **200** (`DETAIL_REGIME_LABEL: trend`,
`DETAIL_UNCERTAINTY_METHOD: threshold_margin_confidence_band`, `DETAIL_FEATURE_POLICY:
normalized_features_no_symbol_identity`); `POST_REGIME_STATUS_EXPECT_405: 405`. Both list and detail proven. ✅

### 2.8 Dependency discipline + bright-line + regression
No-unspiked-import grep over `institutional_intelligence` benign; explainable pure-Python rules. Wave-wide grep
benign; **broker gate `test_broker_integration.py` 7 passed** incl. `test_governance_gate_refuses_connect_
and_execute`; Gate CLOSED. Backend **211 passed** (204→211, 0 failed); frontend **11 files / 25 tests**; ruff
`All checks passed!`; npm audit 0; `✓ built`. No UI (stated). ✅

---

## 3. The red gate — investigated, proven unrelated (OBS-1)

**Fact (not softened):** the CI step ended with `LOCAL_CI_EXIT_CODE: 1`. I do not call it green.

**Why non-blocking (proof):**
1. **Root cause is a WSL shell spawn error, not a test/product failure:** the transcript's final lines are
   `<3>WSL (32 - Relay) ERROR: CreateProcessCommon:818: execvpe(/bin/bash) failed: No such file or directory`
   immediately before the `1`. The CI was invoked as **bare `bash scripts/local_ci.sh`** (line 683), which on
   this Windows box routes to **WSL**, whose `/bin/bash` is not installed — the documented invocation is
   `& "C:\Program Files\Git\bin\bash.exe" scripts/local_ci.sh`.
2. **Zero test failures anywhere:** grep for FAILED/failed/Traceback/assert across the whole pack → nothing.
3. **Every gate is independently green** (run outside the CI wrapper): 211 backend, 25 frontend, ruff clean,
   audit 0, `✓ built` — the CI body's pytest even shows `collected 211 items … [all pass]`.
4. **Not W4-U03 code:** the error is a shell/environment artifact after the gates completed.

**Disposition:** OBS-1 (LOW–MEDIUM observation, non-blocking). Re-run CI with the documented Git-Bash path to
capture a clean `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0`. (Positive note: the CI
marker-check `Select-String` now correctly targets the **W4-U03** transcript — the prior cosmetic OBS about
pointing at the old transcript is retired.)

---

## 4. Findings ledger

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| OBS-1 | LOW–MED (obs) | `LOCAL_CI_EXIT_CODE: 1` from a **WSL `/bin/bash` spawn error** (bare-`bash` invocation), after all gates ran green; zero test failures | **Non-blocking.** Re-run CI via documented Git-Bash path for a clean exit 0 |
| — | — | R-2 / R-7 / GR-7 / R-6 / R-4-inline / API 401·list200·detail200·405 / dep-discipline / gate-closed / 211 tests | ✅ proven on target |

**No CRITICAL. No HIGH. No unmet mandatory functional/governance evidence.** Every risk item is Level-I
proven; the only red signal is a proven-unrelated environment artifact. Proportionality (R13): **approve with
observation.**

---

## 5. Disposition & next step

- **W4-U03 — ✅ APPROVED WITH OBSERVATIONS.** Platform **v0.32.0 → v0.33.0**. Residual: OBS-1 (clean CI re-run
  via Git-Bash — capture `LOCAL_CI_EXIT_CODE: 0`).
- Commendation: the **R-4 raw-SELECT + no-orphan audit was delivered inline** (the W4-U02 C-1 lesson landed),
  **R-7 is proven by both a named test and a persisted `feature_policy` field**, look-ahead is proven twice,
  and the DA chose the safe explainable-rules default over a learned model. Strong unit.
- **Next:** ITRGA recommends **W4-U04 — Scenario Simulation Research Reports**, carrying **R-2** (no-look-ahead),
  **R-4** (persistence-capture — inline raw SELECT + audit), **R-5** (economic-usefulness reported, not just
  "separate"), and **R-6** (scenario is hypothetical, cannot become an order/instruction — the highest-risk
  framing in the plan §8; prove no order/sizing payload). On operator authorization ITRGA issues
  `BUILD_ORDER_W4-U04.md`.
- DA does not self-authorize W4-U04, adopt an unspiked dep, add execution/broker, or open the Gate. Please
  close OBS-1's clean CI run either in the next delivery or a quick standalone re-run.

> **We don't guess. We prove.** — ITRGA
