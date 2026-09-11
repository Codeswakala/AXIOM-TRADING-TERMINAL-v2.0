# ITRGA INDEPENDENT REVIEW — W4-U01 (Scientific Dependency Compatibility + Intelligence Artifact Foundation)

| Field | Value |
|---|---|
| Reviewing authority | **AXIOM Independent Technical Review & Governance Authority (ITRGA)** |
| Unit | **W4-U01** — Institutional Intelligence foundation (dependency spike + artifact contract) |
| Wave | 4 — Institutional Intelligence (FIRST unit) |
| Build Order | `docs/BUILD_ORDER_W4-U01.md` |
| Evidence | `uploads/DELIVERY_REPORT_W4-U01 (1).md` + `uploads/operator results.md` (1,673 lines) |
| DA-claimed platform | 0.31.0 |
| Review date | 2026-07-16 |
| **VERDICT** | **✅ APPROVED — CLEAN.** Platform advances to **v0.31.0**. **TD-065 DISCHARGED for numpy/pandas/scipy.** |
| Confidence | **HIGH** — spike passed on the exact target with raw versions; artifact contract proven inert by test |

> **We don't guess. We prove.** The compiled stack is proven on Windows + Python 3.14.6, the artifact contract structurally cannot carry an action, and no feature was built ahead of the foundation. Approved.

---

## 1. Bottom line

W4-U01 does exactly what a foundation unit must: it **proves the compiled scientific stack on the target
before anything relies on it (R-1)** and stands up an **inert, lineage/uncertainty/audit-bearing artifact
contract** — with **no analytical feature, no schema, no execution/broker/gate path.** Every mandatory gate is
met on operator-run target evidence. **APPROVED, CLEAN, no residual.** Wave 4 opens on a proven footing.

---

## 2. Build identity — genuinely W4-U01 (proven first)

`Test-Path`×7 → True (BUILD_ORDER, INTAKE, ADR-040, `contracts.py`, foundation test, spike script, spike
policy); `__version__ = "0.31.0"`; `system.py unit="W4-U01"`; `TerminalLayout … W4-U01`; git status shows the
new `institutional_intelligence/` files. ✅

---

## 3. R-1 — the wheel-compat HARD GATE: DISCHARGED (numpy/pandas/scipy) ✅

The spike ran in an **isolated venv** (`.w4-u01-spike-venv`) on the exact target — so it proves compatibility
**without** polluting the app runtime:

| Dep | Resolved wheel (raw) | Import | Smoke | Verdict |
|---|---|---|---|---|
| numpy | `numpy-2.5.1-cp314-cp314-win_amd64.whl` | ✅ | `mean 2.0, shape [3]` | **PASS** |
| pandas | `pandas-3.0.3-cp314-cp314-win_amd64.whl` | ✅ | `mean 2.0, rows 3` | **PASS** |
| scipy | `scipy-1.18.0-cp314-cp314-win_amd64.whl` | ✅ | `pearsonr 0.9999…` | **PASS** |

- Environment: `Python 3.14.6 … [MSC v.1944 64 bit (AMD64)]`, `Windows-11`. Spike JSON `overall_status: PASS`;
  `SPIKE_EXIT_CODE: 0`. `pip freeze` captured to `W4-U01_SCIENTIFIC_DEPENDENCY_FREEZE.txt`.
- **No premature adoption:** app code holds `APPROVED_COMPILED_DEPENDENCIES = ()` and the policy
  *"No Wave-4 application code may import a compiled scientific dependency unless that dependency [is spiked]"*;
  the no-compiled-import grep over `institutional_intelligence` is **empty** (command + output).
- **Fallbacks committed:** `scientific_fallbacks.py` `mean(...)` + `pearson_correlation(...)`, proven by
  `test_pure_python_scientific_fallbacks_known_values PASSED`.
- **scikit-learn** correctly **not adopted** (future spike required if proposed).

**Effect:** TD-065 is **DISCHARGED for numpy 2.5.1 / pandas 3.0.3 / scipy 1.18.0 on Win+Py3.14.6.** Any future
Wave-4 unit may rely on exactly these; any other compiled dep (e.g. scikit-learn) still owes its own spike.
The register wording "Reduced… closure pending operator target spike + ITRGA verdict" is now upgraded by this
verdict to **discharged for those three deps** — DA to reflect that in TD-065 at the next unit.

---

## 4. Artifact contract — proven INERT and traceable (GR-4) ✅

`contracts.py` defines `IntelligenceArtifactContract` / `Draft` / `Factory` carrying **all plan §4.1 fields**
(artifact_id, created_at UTC, artifact_type, method_version, config, input_lineage, source_artifact_ids,
market_scope, as_of_start/end, sample_count, uncertainty, results, limitations, report_hash, research_status,
created_by, audit_correlation_id). The factory validates UTC range, `research_only` status, non-negative
sample count, uncertainty presence, deterministic report hash, **and rejects action/remediation keys**
(`order_payload, execution_payload, remediation_payload, broker_account_id, quantity, stop_loss, take_profit,
auto_retrain, retrain_triggered`).

Proven by named tests:
- `test_artifact_contract_contains_mandatory_fields_and_audit_details PASSED`
- `test_artifact_contract_rejects_action_or_remediation_payloads PASSED` ← **the inert keystone**
- `test_artifact_contract_rejects_missing_uncertainty_or_bad_time PASSED`
- `test_compiled_dependency_policy_has_candidates_but_no_unapproved_imports PASSED`
- `test_institutional_intelligence_context_has_no_execution_or_broker_path PASSED`

The contract structurally cannot carry a directive. **GR-4 designed in; GR-3 enforced at the contract layer.**

---

## 5. R-3 wave-wide bright-line grep — disclosed + all benign ✅

The grep (exec/mutation/gate patterns incl. `gate_open|allow_execution|guaranteed future|guaranteed return`)
produced **9 residual hits, all disclosed with command + output** (R7-correct — not a blank pass). Each
adjudicated benign:

| Hit | Nature | Benign? |
|---|---|---|
| `dependencies.py: import BrokerIntegrationService` | import of the hard-closed null broker (gate refuses execute) | ✅ import ≠ execution |
| `generalization.py: auto_retrain_requested … default=False` | W2-U10 data flag | ✅ |
| `contracts.py: "order_payload"/"remediation_payload"/"auto_retrain"` (×3) | the artifact contract's **forbidden-key list** | ✅ this IS the block, not a violation |
| `database_health.py: """Execute a trivial query…"""` | docstring | ✅ |
| `inference/service.py: model.advisory_status = "advisory_approved"` | W3-U01 **governed, audited advisory promotion** (not execution) | ✅ established exclusion |
| `signals/service.py: "no_order_payload"` | string asserting **absence** of an order payload | ✅ |
| `MonitoringAlertsPanel.tsx: "…do not retrain, remediate, or execute"` | UI disclaimer | ✅ |

**Gate closed:** `test_broker_integration.py` **7 passed** incl. `test_governance_gate_refuses_connect_and_
execute`; broker-seam grep (`gate_open|allow_execution|GovernanceGateOpen`) → empty. Gate remains CLOSED.

*(Observation OBS-A, LOW: hits 3–9 printed raw because the `$Benign` filter didn't pre-exclude the contract's
own forbidden-key literals or the `no_order_payload`/disclaimer strings. Disclosure over silence is the right
call and R7-correct; a tighter `$Benign` next time would make the "expected: none" line literally true. Non-
blocking.)*

---

## 6. Regression, CI, persistence, docs

| Gate | Result |
|---|---|
| Named foundation tests | **6 passed** by name |
| Backend full suite | **198 passed, 0 failed** (192→198, +6) on PostgreSQL |
| Frontend | **11 files / 25 tests** passed |
| ruff / npm audit / tsc / build | clean / 0 / clean / ✓ built |
| CI | `==> Local CI equivalent complete` + **`LOCAL_CI_EXIT_CODE: 0`** (line 1327–1328) |
| Migration | head `20260715_0018`, **no new migration** (foundation adds none) |
| Persistence (R-4) | **File-only** spike evidence, explicitly stated → persistence-capture control **not** triggered (correct; no table added) |
| Docs | CHANGELOG `[0.31.0]`; **GA-040** (foundation authorized, no analytics/execution, Gate CLOSED); TD-065 "Reduced"; RISK/roadmap updated; ADR-040 |
| D-W2-001 | No per-market model / no symbol-identity feature (test-proven) |

*(OBS-B, LOW: the CI marker-check `Select-String` on line 931 points at the old `W3-U08.1_LOCAL_CI_TRANSCRIPT.txt`
— a copy-paste leftover — but the live `local_ci.sh` run at line 1327–1328 shows the marker + `EXIT_CODE 0`
directly, so the requirement is met. Point the grep at the W4-U01 transcript next time. Non-blocking.)*

---

## 7. Findings ledger

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| — | — | R-1 spike PASS (numpy/pandas/scipy, raw versions, isolated venv, exit 0) | ✅ TD-065 discharged for those deps |
| — | — | Artifact contract inert + traceable, proven by named tests | ✅ |
| — | — | Wave-wide grep 9 hits, all disclosed + benign; gate closed (7 tests) | ✅ |
| OBS-A | LOW | `$Benign` filter didn't pre-exclude the contract's own forbidden-key literals / `no_order_payload` / disclaimer | Non-blocking; tighten filter |
| OBS-B | LOW | CI marker-check grep pointed at the W3-U08.1 transcript (leftover); live run shows marker + exit 0 anyway | Non-blocking; point at W4-U01 transcript |

**No CRITICAL/HIGH. No unmet mandatory evidence. No open blocking residual.** Proportionality (R13): approve.

---

## 8. Disposition & next step

- **W4-U01 — ✅ APPROVED, CLEAN.** Platform **v0.30.1 → v0.31.0**.
- **TD-065 DISCHARGED** for **numpy 2.5.1 / pandas 3.0.3 / scipy 1.18.0** on Windows + Python 3.14.6. Any other
  compiled dep still owes its own spike. DA to update TD-065 wording to "discharged for those three deps" at
  the next unit.
- Commendation: the spike was run in an isolated venv with **raw resolved versions and PASS/FAIL**, the
  artifact contract's inert-key rejection is proven by a named test, and the grep residuals were **disclosed
  with output and left for ITRGA to adjudicate** rather than filtered into silence — exactly the standard.
- **Next:** ITRGA recommends **W4-U02 — Correlation Intelligence Reports**, carrying **R-2** (no-look-ahead
  named negative test), **R-4** (persistence-capture on `correlation_reports` — committing script + raw SELECT
  + no-orphan audit), and **R-6** (correlation structurally cannot become a signal/action). On operator
  authorization ITRGA issues `BUILD_ORDER_W4-U02.md`.
- DA does not self-authorize W4-U02, adopt scikit-learn (unspiked), add execution/broker, or open the Gate.

> **We don't guess. We prove.** — ITRGA
