# Delivery Report — W3-U03

| Field | Value |
|---|---|
| Build Order | **W3-U03** Operating-Domain + Calibration/Economic Guardrails at Emit Time (+ signal staleness) |
| Platform | **0.25.0** |
| Wave | **3 — Live Research Advisor** |
| DA status | **Implemented and locally validated** |
| Approval status | **Not self-approved; pending operator evidence and ITRGA review** |
| Date | 2026-07-15 |

---

## 1. Executive Summary

W3-U03 matures AXIOM's advisory signal emit-time guardrails. W3-U01 eligibility remains mandatory and W3-U02 persistence remains inert, but an eligible model's specific signal is now further checked for operating-domain, calibration, economic, and freshness constraints before it can be stored as a clean `emitted` record.

Implemented outcomes:

- provider/symbol/source emit-time domain violations are `withheld` with `UNSUPPORTED_DOMAIN`;
- stale input is `withheld` with `STALE_INPUT`;
- poor calibration becomes `warning` with `POORLY_CALIBRATED`;
- economically unusable verdicts become `warning` with `ECONOMICALLY_UNUSABLE`;
- signal validity/expiry fields are persisted;
- expired signals are marked `expired` with `SIGNAL_EXPIRED`;
- signal-history API supports `current_only=true` so expired records are not returned as current;
- calibrated confidence and economic verdict are recorded independently;
- the signal remains inert: no UI, alert, live stream, broker, order, execution, paper trading, or position path was added.

DA does not self-approve. This delivery is submitted for operator evidence collection and ITRGA independent review.

---

## 2. Authority and Traceability

| Artifact | Path |
|---|---|
| W3-U03 Build Order | `docs/build-orders/BUILD_ORDER_W3-U03.md` |
| W3-U03 Build Order Intake | `docs/build-orders/BUILD_ORDER_INTAKE_W3-U03.md` |
| Guardrails/staleness ADR | `docs/adr/ADR-033_Signal_Emit_Time_Guardrails_Staleness.md` |
| Operator evidence commands | `docs/evidence/W3-U03_OPERATOR_EVIDENCE_COMMANDS.md` |
| Migration | `backend/alembic/versions/20260715_0017_w3_u03_signal_guardrails_staleness.py` |

---

## 3. Implementation Summary

### 3.1 Freshness/Staleness Schema

Alembic revision `20260715_0017` adds these fields to `advisory_signals`:

```text
input_staleness_seconds
signal_validity_seconds
expires_at
freshness_status
```

Indexes were added for `expires_at` and `freshness_status`.

### 3.2 Configurable Freshness Contract

Runtime settings added:

```text
AXIOM_SIGNAL_MAX_INPUT_STALENESS_SECONDS = 300
AXIOM_SIGNAL_VALIDITY_SECONDS = 300
AXIOM_SIGNAL_CALIBRATION_WARNING_ECE_THRESHOLD = 0.15
```

`SignalGuardrailConfig` allows tests and future services to provide explicit guardrail values without changing global process settings.

### 3.3 Operating-Domain Guardrail

W3-U01 already validates market/timeframe/regime. W3-U03 adds signal-time checks for:

- provider;
- symbol;
- input source authority.

Violations are persisted as:

```text
signal_state = withheld
state_reason = UNSUPPORTED_DOMAIN
operating_domain_status = unsupported
```

### 3.4 Calibration Guardrail

The calibration guardrail now evaluates:

- calibration report warnings;
- aggregate expected calibration error;
- relevant per-slice ECE when available.

Violations are persisted as:

```text
signal_state = warning
state_reason = POORLY_CALIBRATED
calibration_status = warning:POORLY_CALIBRATED
```

The record still stores calibrated confidence from calibration evidence. Raw score remains an audit field only.

### 3.5 Economic Guardrail

Economically unusable/negative/loss verdicts are persisted as warning records:

```text
signal_state = warning
state_reason = ECONOMICALLY_UNUSABLE
economic_verdict = economically_unusable
```

This preserves the independence of statistical signal score and economic usability.

### 3.6 Signal Expiry and Current-History API

Signals have `expires_at` and `freshness_status`. A signal past its validity can be persisted as:

```text
signal_state = expired
state_reason = SIGNAL_EXPIRED
freshness_status = expired
```

The history API remains read-only and now supports:

```text
GET /api/v1/signals/history?current_only=true
```

This returns only `emitted`/`warning` records with `expires_at > now`, excluding expired records from current reads.

---

## 4. Files Created

```text
backend/alembic/versions/20260715_0017_w3_u03_signal_guardrails_staleness.py
backend/tests/test_signal_guardrails.py
docs/adr/ADR-033_Signal_Emit_Time_Guardrails_Staleness.md
docs/build-orders/BUILD_ORDER_W3-U03.md
docs/build-orders/BUILD_ORDER_INTAKE_W3-U03.md
docs/evidence/W3-U03_OPERATOR_EVIDENCE_COMMANDS.md
DELIVERY_REPORT_W3-U03.md
```

---

## 5. Files Modified

```text
backend/app/__init__.py
backend/app/core/config.py
backend/app/db/models/advisory_signal.py
backend/app/models/advisory_signal.py
backend/app/models/system.py
backend/app/api/routes/advisory_signals.py
backend/app/main.py
backend/app/trading_intelligence/signals/__init__.py
backend/app/trading_intelligence/signals/service.py
backend/pyproject.toml
backend/README.md
backend/tests/test_advisory_signals.py
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
| Out-of-domain withhold/warn, never clean emitted | Implemented and tested via provider/symbol/source emit-time guardrail |
| Poor calibration warning/withhold, calibrated confidence shown | Implemented and tested via ECE/warnings/slice checks |
| Economically unusable warning, verdict shown | Implemented and tested |
| Stale input withheld with `STALE_INPUT` | Implemented and tested |
| Signal past validity expired and not shown current | Implemented and tested via `expired` state and `current_only` API filter |
| Guardrail non-bypassable | Implemented; no force-emission path; test proves economic guardrail prevails |
| No raw-score-as-confidence | Preserved; raw score audit field remains separate from calibrated confidence |
| Inert/no-execution | Preserved; no order/broker fields or paths added |
| History API read-only 401/200/405 | Preserved/tested; evidence pack includes operator commands |
| Persisted-PG proof first submission | Evidence pack includes committing script, raw `SELECT`, audit proof, and API read-back |

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
177 passed, 1 warning in 38.47s
```

### Named guardrail/signal tests

```text
$ pytest tests/test_advisory_signals.py tests/test_signal_guardrails.py -q
13 passed, 1 warning in 3.08s
```

### Alembic local migration smoke

```text
Running upgrade 20260715_0016 -> 20260715_0017, W3-U03 signal guardrail freshness fields
20260715_0017 (head)
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

### No-execution grep over W3-U03 signal code and route

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
| Authentication | Signal-history API remains Bearer-authenticated. |
| Authorization | No public signal-history access; unauthenticated reads tested as 401. |
| Secrets | No new secrets or credentials introduced. |
| PII | Signal records store model/input lineage, market identifiers, and guardrail metadata only. |
| Execution | No broker/order/execution path added. |
| Write surface | No signal creation API exposed; signal production remains backend service logic only. |

---

## 9. Performance / Scalability Review

- Added indexes for expiry/current-history filtering.
- History API remains bounded to max 200 rows.
- Emit-time checks are bounded metadata checks against already-linked reports and model metadata.
- No scheduler, stream, or polling surface was added in W3-U03.

---

## 10. Maintainability Review

- Guardrail defaults are centralized in settings and exposed through `SignalGuardrailConfig`.
- Signal service remains isolated under Trading Intelligence.
- W3-U01 eligibility and W3-U02 persistence are extended rather than rewritten.
- Tests cover every new guardrail and staleness state.
- Backward compatibility: new DB fields are nullable so existing W3-U02 rows can survive migration.

---

## 11. Governance Compliance Review

| Rule | Compliance |
|---|---|
| Build Order scope | Implemented Components A–F only. |
| No future wave work | No W3-U04 live adapter, W3-U05 UI, W3-U06 alerts, W3-U07 analytics, or Wave-6 execution implemented. |
| Database integrity | New fields added through Alembic migration only. |
| ML governance | W3-U01 eligibility and W2 lineage remain prerequisites. |
| Staleness R-2 | Implemented in DA code and tests; submitted for ITRGA closure. |
| Evidence | Operator command pack includes migration, tests, named guardrails, stale/expired proof, raw SELECT, API read-back, CI marker, parity smoke. |
| ITRGA relationship | DA does not self-approve; report submitted for independent review. |

---

## 12. Known Risks

| Risk | Status |
|---|---|
| Live-market inference adapter absent | Accepted; explicitly W3-U04 scope. |
| Signal UI absent | Accepted; explicitly W3-U05 scope. |
| Alerts/live signal stream absent | Accepted; explicitly W3-U06 scope. |
| Background expiry worker absent | Recorded as TD-056; current API filter prevents expired records being returned as current. |
| PostgreSQL operator evidence not yet run in DA sandbox | Requires operator-run target evidence per command pack. |

---

## 13. Technical Debt Updates

Updated `TECHNICAL_DEBT_REGISTER.md`:

- `TD-054` closed foundationally: emit-time domain/calibration/economic/staleness guardrails implemented.
- `TD-055` remains open: live market inference adapter deferred to W3-U04.
- `TD-056` added: background expiry worker absent, deferred until later operational need.

---

## 14. Operator Evidence Command Pack

The full operator evidence command pack is available at:

```text
docs/evidence/W3-U03_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes exact Windows PowerShell + PostgreSQL commands for:

1. clean PostgreSQL migration to `20260715_0017 (head)`;
2. full backend/frontend tests;
3. named W3-U03 guardrail and staleness tests;
4. W3-U01/W3-U02/broker regression tests;
5. persisted guardrail-outcome proof against `advisory_signals`;
6. audit-event proof against `audit_events`;
7. authenticated API read-back proving expired records are not current;
8. no-execution/no-signal grep evidence;
9. local CI completion marker capture;
10. parity smoke.

---

## 15. DA Non-Approval Statement

W3-U03 is implemented and locally validated by the Development Authority. It is **not accepted, approved, or complete by DA declaration**.

Acceptance requires:

1. operator-run target evidence using `docs/evidence/W3-U03_OPERATOR_EVIDENCE_COMMANDS.md`;
2. ITRGA independent review;
3. ITRGA verdict.

DA will not begin W3-U04 or any subsequent unit without ITRGA approval and a new Build Order.

---

**End of Delivery Report W3-U03**
