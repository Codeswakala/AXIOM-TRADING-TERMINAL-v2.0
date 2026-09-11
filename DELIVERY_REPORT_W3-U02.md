# Delivery Report — W3-U02

| Field | Value |
|---|---|
| Build Order | **W3-U02** Advisory Signal Contract + Signal Persistence |
| Platform | **0.24.0** |
| Wave | **3 — Live Research Advisor** |
| DA status | **Implemented and locally validated** |
| Approval status | **Not self-approved; pending operator evidence and ITRGA review** |
| Date | 2026-07-15 |

---

## 1. Executive Summary

W3-U02 implements the first governed advisory signal record for AXIOM. A signal is now a persisted, audited, inert research/advisory record created only through the Trading Intelligence backend service.

The implementation preserves the Wave-3 safety boundary:

- signal production reuses the W3-U01 `GovernedModelEligibilityGate`;
- only an eligible `advisory_approved` model with full W2 lineage can produce an `emitted` signal;
- ineligible, `research_only`, out-of-domain, or no-rationale candidates are persisted as `withheld` records;
- poor calibration is persisted as `warning`, not emitted certainty;
- stored confidence is calibrated from W2-U08 calibration evidence, not raw-score-as-confidence;
- every signal decision is persisted and audited;
- the API surface is read-only history only;
- no UI, alert, live signal stream, broker, execution, order, paper trading, or position path was added.

DA does not self-approve. This report and `docs/evidence/W3-U02_OPERATOR_EVIDENCE_COMMANDS.md` are submitted for operator evidence collection and ITRGA review.

---

## 2. Authority and Traceability

| Artifact | Path |
|---|---|
| W3-U01 ITRGA approval | `docs/build-orders/ITRGA_REVIEW_W3-U01.md` |
| W3-U02 Build Order | `docs/build-orders/BUILD_ORDER_W3-U02.md` |
| W3-U02 Build Order Intake | `docs/build-orders/BUILD_ORDER_INTAKE_W3-U02.md` |
| Signal ADR | `docs/adr/ADR-032_Advisory_Signal_Contract_Persistence.md` |
| Operator evidence commands | `docs/evidence/W3-U02_OPERATOR_EVIDENCE_COMMANDS.md` |
| Migration | `backend/alembic/versions/20260715_0016_w3_u02_advisory_signals.py` |

---

## 3. Implementation Summary

### 3.1 Advisory Signal Contract and Table

Added `AdvisorySignal` ORM model and Alembic migration for `advisory_signals`.

Key fields include:

- `signal_id`, `created_at`, `as_of_time`;
- `market_class`, `provider`, `symbol`, `timeframe`;
- `model_artifact_id`, `model_version`, `feature_set_version`, `experiment_id`;
- `statistical_report_id`, `calibration_report_id`, `economic_report_id`, `generalization_report_id`;
- `inference_input_hash`, `raw_score`, `calibrated_confidence`;
- `signal_direction`, `signal_state`, `state_reason`, `eligibility_reasons`;
- `operating_domain_status`, `calibration_status`, `economic_verdict`, `risk_notes`;
- `rationale`, `explainability_summary`, `state_transition_history`;
- `audit_correlation_id`.

The table intentionally contains no order payload, broker account, quantity, stop-loss/take-profit, dispatch, or execution columns.

### 3.2 Governed Signal Service

Added `backend/app/trading_intelligence/signals` with:

- `AdvisorySignalService`;
- `AdvisorySignalHistoryFilter`;
- signal service error types.

Signal service behavior:

| Candidate | Result |
|---|---|
| W3-U01 eligible, rationale present, calibration clean | `emitted` |
| `research_only` / not advisory approved | `withheld`, reason includes `NOT_ADVISORY_APPROVED` |
| Out of operating domain | `withheld`, reason includes `UNSUPPORTED_DOMAIN` |
| Missing rationale | `withheld`, reason `RATIONALE_REQUIRED` |
| Calibration report warning | `warning`, reason from calibration warning |

### 3.3 Calibrated Confidence

The service records `raw_score` for audit traceability but stores operator-facing confidence as `calibrated_confidence` derived from the calibration report bins. If the raw score's bin has no observations, the calibration report `base_rate` is used.

This prevents raw model score from being represented as confidence.

### 3.4 Explainability

Each signal record includes:

- model identity and version;
- experiment and feature-set lineage;
- input identity and deterministic input hash;
- signal state and reason;
- eligibility refusal reasons when applicable;
- calibrated confidence and calibration state;
- operating-domain status;
- economic verdict;
- advisory-only limitations.

No-rationale candidates are withheld.

### 3.5 Read-only Signal-History API

Added authenticated read-only endpoints:

```text
GET /api/v1/signals/history
GET /api/v1/signals/history/{signal_id}
```

Supported filters include:

- `signal_id`;
- `model_artifact_id`;
- `market_class`;
- `symbol`;
- `timeframe`;
- `signal_state`;
- `limit`.

No POST/PUT/PATCH/DELETE signal emission endpoint was added.

### 3.6 Audit

Each persisted signal writes an append-only audit event:

```text
resource_type = advisory_signal
action = advisory_signal.emitted | advisory_signal.withheld | advisory_signal.warning
```

Audit details include signal id, model artifact id, signal state, reason, input hash, and calibrated confidence.

---

## 4. Files Created

```text
backend/app/db/models/advisory_signal.py
backend/app/models/advisory_signal.py
backend/app/api/routes/advisory_signals.py
backend/app/trading_intelligence/signals/__init__.py
backend/app/trading_intelligence/signals/errors.py
backend/app/trading_intelligence/signals/service.py
backend/alembic/versions/20260715_0016_w3_u02_advisory_signals.py
backend/tests/test_advisory_signals.py
docs/adr/ADR-032_Advisory_Signal_Contract_Persistence.md
docs/build-orders/ITRGA_REVIEW_W3-U01.md
docs/build-orders/BUILD_ORDER_W3-U02.md
docs/build-orders/BUILD_ORDER_INTAKE_W3-U02.md
docs/evidence/W3-U02_OPERATOR_EVIDENCE_COMMANDS.md
DELIVERY_REPORT_W3-U02.md
```

---

## 5. Files Modified

```text
backend/app/__init__.py
backend/app/core/config.py
backend/app/api/router.py
backend/app/db/models/__init__.py
backend/app/models/system.py
backend/pyproject.toml
backend/README.md
backend/tests/test_endpoint_auth.py
backend/tests/test_system.py
frontend/src/layouts/TerminalLayout.tsx
README.md
PROJECT_STATE.md
CHANGELOG.md
docs/governance/RISK_REGISTER.md
docs/governance/TECHNICAL_DEBT_REGISTER.md
docs/governance/GOVERNANCE_AMENDMENTS.md
docs/governance/04_PROJECT_ROADMAP.md
```

---

## 6. Acceptance Criteria Mapping

| Build Order Requirement | DA Result |
|---|---|
| Signal DTO + PG table with lineage/calibrated confidence/rationale/state | Implemented in `AdvisorySignal` and migration `20260715_0016` |
| Inert signal, no executable order payload | Implemented; schema has no order/broker/dispatch fields; structural test added |
| Emission gated by W3-U01 eligibility gate | Implemented in `AdvisorySignalService.produce` |
| Ineligible/research-only/out-of-domain withheld by name | Implemented and tested |
| Poor calibration warning/withheld | Implemented as `warning`, tested |
| No rationale ⇒ withhold | Implemented and tested |
| Calibrated confidence, not raw-score confidence | Implemented and tested (`calibrated_confidence != raw_score`) |
| Read-only authenticated signal-history API | Implemented and tested |
| Audit event for every signal | Implemented and tested |
| No UI/alerts/live stream/execution | Preserved; no signal UI/alert/live WS stream added |
| Persisted-PG proof first submission | Evidence command pack includes committing script and SELECTs for emitted + withheld rows and audit events |

---

## 7. Local Validation Evidence Collected by DA

### Backend lint

```text
$ ruff check .
All checks passed!
```

### Backend tests

```text
$ pytest -q
171 passed, 1 warning in 32.17s
```

### Named W3-U02 tests

```text
$ pytest tests/test_advisory_signals.py -q
7 passed, 1 warning in 1.41s
```

### Alembic local migration smoke

```text
Running upgrade 20260715_0015 -> 20260715_0016, W3-U02 advisory signal contract and persistence
20260715_0016 (head)
```

### Frontend validation

```text
npm audit --audit-level=high
found 0 vulnerabilities

npm test
Test Files 8 passed
Tests 16 passed

npm run lint
# TypeScript clean

npm run build
✓ built
```

### No-execution grep over W3-U02 signal code and route

```text
grep -RInE "place_order|cancel_order|broker\.|execute|order_intent dispatch" backend/app/trading_intelligence/signals backend/app/api/routes/advisory_signals.py
# no output
```

### No live-signal / signal-emission API grep

```text
grep -RInE "live_signal|emit_signal|place_order|cancel_order" backend/app/api/routes frontend/src
# no output
```

---

## 8. Security Review

| Area | Review |
|---|---|
| Authentication | Signal-history API requires existing Bearer operator auth. |
| Authorization | No public signal-history endpoint; unauthenticated request tested as 401. |
| Secrets | No new secrets or credentials introduced. |
| PII | Signal records store model/input lineage and market identifiers only; no operator credentials or secrets. |
| Execution | No broker/execution/order code added. |
| Write surface | No signal creation API exposed; service is backend domain logic only. |

---

## 9. Performance / Scalability Review

- Signal table has indexes on created time, state, model artifact, market/symbol/timeframe, and audit correlation id.
- History API limits results to a maximum of 200 rows per request.
- Signal service performs bounded single-record creation and lineage lookups.
- No streaming or polling signal surface was introduced in this unit.

---

## 10. Maintainability Review

- Signal logic is isolated under `app/trading_intelligence/signals`.
- API route is thin and read-only.
- ORM schema is explicit and migration-backed.
- Tests cover governed emission, withholds, warning, rationale requirement, inert schema, API auth, API readback, and audit.
- W3-U01 inference/gate code is reused rather than rewritten.

---

## 11. Governance Compliance Review

| Rule | Compliance |
|---|---|
| Build Order scope | Implemented Components A–F only. |
| No future wave work | No W3-U03 guardrail maturation, W3-U04 live adapter, W3-U05 UI, W3-U06 alerts, or Wave-6 execution implemented. |
| Database integrity | New table added through Alembic migration; no manual schema mutation. |
| ML governance | Full W2 lineage required for emitted signals through W3-U01 gate. |
| Evidence | Operator evidence command pack includes migration, tests, named withholds, API, grep, persisted-PG proof, CI marker, and parity smoke. |
| ITRGA relationship | DA does not self-approve; report submitted for independent review. |

---

## 12. Known Risks

| Risk | Status |
|---|---|
| Deeper emit-time guardrail maturation not implemented | Accepted; explicitly W3-U03 scope. |
| Live market inference adapter absent | Accepted; explicitly W3-U04 scope. |
| No operator UI for signals | Accepted; explicitly W3-U05 scope. |
| PostgreSQL operator evidence not yet run in DA sandbox | Requires operator-run target evidence per command pack. |
| Remote CI evidence not captured in DA sandbox | Operator command pack includes local CI transcript capture and completion marker. |

---

## 13. Technical Debt Updates

Updated `TECHNICAL_DEBT_REGISTER.md`:

- `TD-052` closed foundationally: signal contract/persistence exists.
- `TD-053` remains open: dashboard/alerts are deferred.
- `TD-054` added: deeper emit-time guardrail maturation deferred to W3-U03.
- `TD-055` added: live market inference adapter deferred to W3-U04.

---

## 14. Operator Evidence Command Pack

The full operator evidence command pack is available at:

```text
docs/evidence/W3-U02_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes exact Windows PowerShell + PostgreSQL commands for:

1. clean PostgreSQL migration to `20260715_0016 (head)`;
2. full backend/frontend tests;
3. named W3-U02 and W3-U01 regression tests;
4. persisted emitted + withheld advisory signal proof against `advisory_signals`;
5. audit-event proof against `audit_events`;
6. signal-history API 401/200/405 evidence;
7. no-execution/no-signal grep evidence;
8. local CI completion marker capture;
9. parity smoke.

---

## 15. DA Non-Approval Statement

W3-U02 is implemented and locally validated by the Development Authority. It is **not accepted, approved, or complete by DA declaration**.

Acceptance requires:

1. operator-run target evidence using `docs/evidence/W3-U02_OPERATOR_EVIDENCE_COMMANDS.md`;
2. ITRGA independent review;
3. ITRGA verdict.

DA will not begin W3-U03 or any subsequent unit without ITRGA approval and a new Build Order.

---

**End of Delivery Report W3-U02**
