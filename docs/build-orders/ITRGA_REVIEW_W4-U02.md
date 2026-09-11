# ITRGA INDEPENDENT REVIEW — W4-U02 (Correlation Intelligence Reports)

| Field | Value |
|---|---|
| Reviewing authority | **AXIOM Independent Technical Review & Governance Authority (ITRGA)** |
| Unit | **W4-U02** — Correlation Intelligence Reports (first Wave-4 feature) |
| Wave | 4 — Institutional Intelligence |
| Build Order | `docs/BUILD_ORDER_W4-U02.md` |
| Evidence | `uploads/DELIVERY_REPORT_W4-U02.md` + `uploads/operator results.md` (1,869 lines) |
| DA-claimed platform | 0.32.0 |
| Review date | 2026-07-16 |
| **VERDICT** | **🟡 CONDITIONAL APPROVAL — C-1 (R-4 raw SELECT + no-orphan audit not run) + C-2 (detail endpoint unproven) must be closed. Core function APPROVED.** |
| Confidence | **HIGH** on core correctness; the two conditions are evidence gaps, not defects |

> **We don't guess. We prove.** The correlation engine is correct, look-ahead-safe, and non-signal — proven. But the R-4 persistence control's *named* proof (raw psql SELECT + audit join) was not run, so approval is conditional.

---

## 1. Bottom line

The core deliverable is **right and safe**: correlation is computed as-of-bounded with **look-ahead proven
excluded on target**, carries **uncertainty + sample_count**, keeps **significance and economic usefulness
separate**, is **structurally inert (not a signal/action)**, uses **only the pure-Python fallback** (no
unspiked compiled dep), and is exposed **read-only (401/list-200/POST-405)**. All 6 named tests pass; full
suite 204; CI green. **This is approvable on function.**

Two conditions hold it at CONDITIONAL rather than clean APPROVED:
- **C-1 (the decisive one):** the **R-4 persistence-capture control's named proof — a raw `psql SELECT ≥1 row`
  on `correlation_reports` AND a no-orphan audit JOIN — was not run.** Only `\d correlation_reports` (schema)
  executed. This is a standing, named mandatory control; the API read-back is strong corroboration but is not
  the raw-SELECT + audit-join the Build Order required (R-4).
- **C-2:** the **detail endpoint `GET /correlation-reports/{report_id}` was not proven** (an evidence-script
  path typo blanked the `DETAIL_*` outputs). Only the list endpoint was exercised.

Neither is a governance breach or a defect. Per proportionality (R13), core function is approved and the two
gaps are correctable with a short, targeted re-run.

---

## 2. What is fully PROVEN on target ✅

### 2.1 Build identity + migration
`Test-Path`×N True (BUILD_ORDER/INTAKE/ADR-041/`correlation.py`/`correlation_report.py`/test); v0.32.0;
`system.py unit="W4-U02"`. Alembic `20260715_0018 → 20260716_0019 (head)` on PostgreSQL. `\d correlation_
reports` shows the table with research-artifact fields + `audit_correlation_id` (indexed) and **no order/
execution/broker/remediation/signal columns** (inert by schema).

### 2.2 R-2 no-look-ahead — proven twice
- Named test `test_correlation_no_lookahead_future_candle_excluded_result_unchanged PASSED`.
- **Live API payload** independently corroborates: `excluded_future_candle_count: 2`;
  `EXCLUDED_FUTURE_CANDLE_COUNT: 2`; `aligned_timestamps` all within `as_of_start…as_of_end`. Data beyond
  `as_of_end` is provably excluded. ✅

### 2.3 Uncertainty + economic honesty (GR-7)
API payload: `uncertainty {method: fisher_z_interval, lower, upper, confidence_level 0.95, sample_count 4}`;
`significance` and `economic_usefulness` are **separate fields** (`not_assessed`, "Correlation is research
context and is not an economic edge or signal"); `limitations` = `[correlation_does_not_imply_causation,
research_only_not_a_signal, not_a_trade_instruction, economic_usefulness_not_assessed]`. No point estimate.
Test `test_correlation_report_has_uncertainty_and_separate_economic_context PASSED`. ✅

### 2.4 R-6 non-signal + inert
`test_correlation_report_persisted_audited_and_no_signal_side_effect PASSED` +
`test_correlation_report_schema_is_inert_no_order_or_signal_payload PASSED`. The artifact carries no order/
remediation/signal payload; correlation cannot become/emit a signal or action. ✅

### 2.5 Dependency discipline (R-1 standing)
`correlation.py` uses `pearson_correlation` from the W4-U01 **pure-Python fallback** (`implementation:
pure_python_fallback`); no-compiled-import grep over `institutional_intelligence` empty; no sklearn/statsmodels.
`test_correlation_modules_use_no_unspiked_dependencies_or_execution_path PASSED`. ✅

### 2.6 Read-only API (partial)
`UNAUTH_CORRELATION_STATUS: 401`; **list** `GET /intelligence/correlation-reports` → **200** returning the
full persisted report (lineage, uncertainty, economic fields, `audit_correlation_id: 8b0bb8bb…`);
`POST_CORRELATION_STATUS_EXPECT_405: 405`. ✅ (detail endpoint — see C-2)

### 2.7 Bright-line + regression
Wave-wide grep: **8 residual hits, all disclosed + benign** (broker import; `auto_retrain_requested` flag;
the contract's own forbidden-key literals `order_payload`/`remediation_payload`/`auto_retrain`; "Execute"
docstring; W3-U01 governed `advisory_status=` promotion; alerts-panel disclaimer). Gate closed:
`test_broker_integration.py` **7 passed** incl. `test_governance_gate_refuses_connect_and_execute`; broker-seam
grep empty. Backend **204 passed** (198→204, 0 failed); frontend **11 files / 25 tests**; ruff clean; npm
audit 0; **`LOCAL_CI_EXIT_CODE: 0`** + marker. No UI (correctly stated). No D-W2-001 breach. ✅

---

## 3. Conditions to close (targeted re-run — no re-implementation)

### C-1 (must close) — R-4 raw SELECT + no-orphan audit was NOT run
The **only** `psql` on the table was `\d correlation_reports` (schema). The persistence-capture control — a
standing, named mandatory rule and an explicit W4-U02 acceptance criterion (R-4) — requires, on the CORRECT
table:
1. `psql … -c "SELECT id, left_symbol, right_symbol, sample_count, correlation_value, research_status,
   audit_correlation_id FROM correlation_reports WHERE id = '<REPORT_ID>';"` → **≥1 row**; and
2. a **no-orphan audit JOIN**, e.g.
   `SELECT COUNT(*) AS orphan FROM correlation_reports c LEFT JOIN audit_events a ON a.resource_type=
   'correlation_report' AND a.resource_id=c.id WHERE c.id='<REPORT_ID>' AND a.id IS NULL;` → **0**, plus the
   `correlation_report.created` event row.

*Why not waived:* the API list-200 proves the row is durable and audited **in substance**, and I credit that
as strong corroboration — but R-4's raw-SELECT + audit-join is the *named* proof precisely because the wrong
table / a missing audit event has bitten before (W2-U09 wrong-table correction). The control is not satisfied
by an API read-back when the Build Order named the raw SELECT. Run it.

### C-2 (must close) — detail endpoint unproven
`GET /correlation-reports/{report_id}` returned nothing measurable: the evidence script had
`$Ids = Get-Content path\to\axiom\...` (an unsubstituted placeholder path), so `Get-Content` failed and
`DETAIL_SAMPLE_COUNT/UNCERTAINTY_METHOD/ECONOMIC_VERDICT` printed **blank**. Re-run the detail read with the
correct IDs-file path and show **200 + the report fields**. (The endpoint likely works — the list route does
— but it is currently unproven on target.)

*Cosmetic note (OBS, non-blocking):* the CI marker-check `Select-String` again points at the W3-U08.1
transcript (leftover); the live run shows the marker + `EXIT_CODE 0` regardless — point it at the W4-U02
transcript.

---

## 4. Findings ledger

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| **C-1** | **MEDIUM** | R-4 raw `psql SELECT` on `correlation_reports` + no-orphan audit JOIN not run (only `\d`); API read-back corroborates but is not the named proof | **Condition — run the raw SELECT + audit join** |
| **C-2** | LOW–MEDIUM | Detail endpoint `GET /{report_id}` unproven (evidence-script path typo blanked DETAIL_*) | **Condition — re-run detail read (200 + fields)** |
| OBS | LOW | CI marker-check grep points at the old W3-U08.1 transcript | Non-blocking; retarget |
| — | — | R-2 / R-6 / uncertainty / inert / dep-discipline / API 401·200·405 / gate-closed / regression / CI | ✅ proven |

**No CRITICAL. No governance breach. Core function proven.** Two evidence conditions ⇒ **CONDITIONAL
APPROVAL** (not withheld — the risk items are all proven; the gaps are named-proof completeness).

---

## 5. Disposition & next step

- **W4-U02 — 🟡 CONDITIONAL APPROVAL.** Core correlation function (look-ahead-safe, uncertainty-mandatory,
  non-signal, inert, read-only) is **APPROVED**. Platform advances to **v0.32.0 on closure of C-1 + C-2**
  (until then, v0.31.0 remains the version of record for ITRGA purposes).
- **To close:** a short targeted re-run supplying (C-1) the raw `SELECT` on `correlation_reports` + no-orphan
  audit JOIN for `REPORT_ID 9e9b3939…` (or a freshly seeded id), and (C-2) the detail-endpoint 200 read. No
  re-implementation needed. On that evidence ITRGA issues the FINAL verdict, advances to v0.32.0, and (on
  operator authorization) issues `BUILD_ORDER_W4-U03.md` (Regime Detection) carrying R-2/R-4/R-6/**R-7**.
- Commendation: the R-2 look-ahead is proven *twice* (test + live `excluded_future_candle_count`), the payload
  models economic honesty exactly (significance vs economic-usefulness separate; correlation≠causation in
  `limitations`), and dependency discipline held (pure-Python fallback, no unspiked import). The gaps are
  narrow.
- DA does not self-approve, self-advance the version, begin W4-U03, adopt an unspiked dep, or open the Gate.

> **We don't guess. We prove.** — ITRGA
