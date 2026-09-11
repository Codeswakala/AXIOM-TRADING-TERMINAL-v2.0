# Delivery Report — W4-U06

| Field | Value |
|---|---|
| Build Order | **W4-U06** Professional Signal Validation Extension |
| Platform | **0.36.0** |
| Wave | **4 — Institutional Intelligence** |
| DA status | **Implemented and locally validated** |
| Approval status | **Not self-approved; pending operator evidence and ITRGA review** |
| Date | 2026-07-16 |

---

## 1. Executive Summary

W4-U06 implements persisted Professional Signal Validation Reports over declared as-of-bounded scopes of existing advisory signals. The report validates only what is legitimately available from persisted signal records and explicitly reports when governed forward outcome data is not available. It excludes raw model score from output even when raw score exists upstream.

Implemented outcomes:

- `signal_validation_reports` table and Alembic migration;
- `SignalValidationReportService` under Institutional Intelligence;
- declared validation scope persisted in config;
- full matching scope included with no silent exclusions;
- future signals excluded beyond `scope_end`;
- metrics with Wilson uncertainty intervals and sample counts;
- raw-score exclusion from report payload/output;
- honest outcome-data status;
- independent economic usefulness field;
- audit event on report creation;
- authenticated read-only API;
- no UI in this unit;
- no signal emission, model mutation, execution, broker, or order path.

DA does not self-approve. Operator-run Windows + PostgreSQL evidence remains mandatory.

---

## 2. Authority and Traceability

| Artifact | Path |
|---|---|
| W4-U05 review | `docs/build-orders/ITRGA_REVIEW_W4-U05.md` |
| W4-U06 Build Order | `docs/build-orders/BUILD_ORDER_W4-U06.md` |
| W4-U06 Build Order Intake | `docs/build-orders/BUILD_ORDER_INTAKE_W4-U06.md` |
| W4-U06 ADR | `docs/adr/ADR-045_Professional_Signal_Validation_Reports.md` |
| Operator evidence commands | `docs/evidence/W4-U06_OPERATOR_EVIDENCE_COMMANDS.md` |
| Migration | `backend/alembic/versions/20260716_0023_w4_u06_signal_validation_reports.py` |

---

## 3. Implementation Summary

### 3.1 Signal validation persistence

Added:

```text
backend/app/db/models/signal_validation_report.py
backend/alembic/versions/20260716_0023_w4_u06_signal_validation_reports.py
```

The table stores research artifact metadata, scope bounds, sample count, metrics, uncertainty, validation scope, outcome data status, economic usefulness, lineage/config/results/limitations, source signal ids, report hash, research status, actor, and audit correlation id.

It intentionally contains no raw score, order, execution, broker, remediation, or signal payload fields.

### 3.2 Signal validation service

Added:

```text
backend/app/institutional_intelligence/signal_validation.py
```

Key objects:

```text
SignalValidationScope
SignalValidationComputationResult
SignalValidationReportService
```

The service:

- reads persisted `advisory_signals` read-only;
- validates an as-of-bounded declared scope;
- includes all matching signals in the declared scope;
- excludes future signals after `scope_end`;
- computes clean advisory rate, guardrail intervention rate, and calibrated confidence coverage;
- attaches Wilson score uncertainty to each metric;
- excludes raw model score from all downstream output;
- reports `outcome_data_status.not_available` when governed forward outcomes are absent;
- persists `SignalValidationReport`;
- writes `signal_validation_report.created` audit event.

### 3.3 Raw-score exclusion

Tests seed source advisory signals with `raw_score=0.987654` and assert downstream report output contains neither:

```text
raw_score
0.987654
```

The report instead records:

```text
uncalibrated_model_score_excluded = true
```

### 3.4 Read-only API

Added:

```text
GET /api/v1/intelligence/signal-validation-reports
GET /api/v1/intelligence/signal-validation-reports/{report_id}
```

No POST/emit/write route was added.

### 3.5 UI decision

W4-U06 adds no UI. The Build Order allows API + tests to suffice if no UI is added.

---

## 4. Files Created

```text
backend/app/db/models/signal_validation_report.py
backend/app/models/signal_validation_report.py
backend/app/institutional_intelligence/signal_validation.py
backend/alembic/versions/20260716_0023_w4_u06_signal_validation_reports.py
backend/tests/test_signal_validation_reports.py
docs/build-orders/ITRGA_REVIEW_W4-U05.md
docs/build-orders/BUILD_ORDER_W4-U06.md
docs/build-orders/BUILD_ORDER_INTAKE_W4-U06.md
docs/adr/ADR-045_Professional_Signal_Validation_Reports.md
docs/evidence/W4-U06_OPERATOR_EVIDENCE_COMMANDS.md
DELIVERY_REPORT_W4-U06.md
```

---

## 5. Files Modified

```text
backend/app/__init__.py
backend/app/api/routes/intelligence.py
backend/app/core/config.py
backend/app/db/models/__init__.py
backend/app/institutional_intelligence/__init__.py
backend/app/main.py
backend/app/models/system.py
backend/pyproject.toml
backend/tests/test_endpoint_auth.py
backend/tests/test_system.py
frontend/src/layouts/TerminalLayout.tsx
README.md
PROJECT_STATE.md
CHANGELOG.md
backend/README.md
docs/governance/RISK_REGISTER.md
docs/governance/TECHNICAL_DEBT_REGISTER.md
docs/governance/GOVERNANCE_AMENDMENTS.md
docs/governance/04_PROJECT_ROADMAP.md
```

---

## 6. Acceptance Criteria Mapping

| Requirement | DA Result |
|---|---|
| No cherry-picking | Declared scope stored and all matching signals included; deterministic tests |
| Raw-score exclusion | Source raw score present; report output excludes `raw_score` and value |
| No guaranteed performance / outcome honesty | Outcome status is `not_available`; no fabricated realized performance |
| Uncertainty + sample count | Wilson intervals and sample counts on every metric |
| R-2 no look-ahead | Future signal excluded and counted |
| R-6 non-signal/no mutation | Implemented and tested |
| R-4 persisted report + audit | Implemented and tested; operator raw SELECT/no-orphan proof required |
| Read-only API | Implemented and tested 401/200/405 |
| Dependency discipline | Pure-Python arithmetic; no unspiked imports |
| No UI | Explicitly no UI this unit |
| No execution / Gate closed | Preserved; evidence pack includes grep and broker gate proof |

---

## 7. Local Validation Evidence Collected by DA

### Backend lint

```text
$ ruff check .
All checks passed!
```

### Named W4-U06 tests

```text
$ pytest tests/test_signal_validation_reports.py -q
8 passed, 1 warning
```

### Backend full suite

```text
$ pytest -q
233 passed, 1 warning
```

### Frontend validation

```text
$ npm audit --audit-level=high
found 0 vulnerabilities

$ npm test
Test Files 11 passed
Tests 25 passed

$ npm run lint
# TypeScript clean

$ npm run build
✓ built
```

### Alembic local migration smoke

```text
Running upgrade 20260716_0022 -> 20260716_0023, W4-U06 professional signal validation reports
20260716_0023 (head)
```

---

## 8. Security / Governance Review

| Area | Review |
|---|---|
| Authentication | API requires existing Bearer operator auth. |
| Authorization | No public signal validation endpoint added. |
| Write surface | No signal validation write API exposed. |
| Execution | No broker/order/execution path added. |
| Raw score | Raw source score excluded from report output. |
| Outcome honesty | No fabricated forward outcomes; status reports not available. |
| Signal boundary | No advisory signal side-effect; report is not a signal. |
| Dependencies | Uses pure-Python/Wilson arithmetic; no unspiked dependency. |
| Persistence | New table via Alembic; audit event on create. |

---

## 9. Known Risks / Required Operator Evidence

| Risk | Status |
|---|---|
| PostgreSQL persistence proof not run in DA sandbox | Operator evidence pack includes committing script + raw SELECT + audit/no-orphan proof |
| No UI for signal validation reports | Accepted; no UI in W4-U06 scope |
| Governed forward outcome data absent | Explicitly reported as not available; no realized performance fabricated |
| Economic usefulness not assessed | Explicitly stored as `not_assessed`; no trading implication |

---

## 10. Operator Evidence Command Pack

Use:

```text
docs/evidence/W4-U06_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes exact commands for:

1. build identity;
2. PostgreSQL migration to `20260716_0023 (head)`;
3. named W4-U06 tests;
4. committed signal validation report proof;
5. raw `signal_validation_reports` SELECT;
6. audit/no-orphan proof;
7. read-only API 401/200/405 proof;
8. raw-score exclusion proof;
9. dependency/no-execution/gate proof;
10. full regression and CI through Git Bash;
11. explicit no-UI statement;
12. parity smoke.

---

## 11. DA Non-Approval Statement

W4-U06 is implemented and locally validated by the Development Authority. It is **not accepted or approved by DA declaration**.

Acceptance requires:

1. operator-run target evidence using `docs/evidence/W4-U06_OPERATOR_EVIDENCE_COMMANDS.md`;
2. PostgreSQL migration/persistence/audit proof;
3. ITRGA independent review;
4. ITRGA verdict.

DA will not begin W4-U07 or any subsequent work without ITRGA approval and a new Build Order.

---

**End of Delivery Report W4-U06**
