# Delivery Report — W3-U08.1 Residual Hardening

| Field | Value |
|---|---|
| Build Order | **W3-U08.1** Wave-3 Residual Hardening |
| Platform | **0.30.1** |
| Wave | **3 — Live Research Advisor** |
| DA status | **Implemented and locally validated** |
| Approval status | **Not self-approved; pending operator evidence and ITRGA residual-closure review** |
| Date | 2026-07-16 |

---

## 1. Executive Summary

W3-U08.1 addresses the two non-blocking observations from the W3-U08 final verdict:

1. **OBS-1:** SQLite `StaticPool` local CI flake in `test_live_market.py::test_live_start_stop_and_status`.
2. **OBS-2:** incomplete Wave-3 browser E2E screenshot archive.

This unit introduces no product capability. It adds no endpoint, schema, migration, execution path, broker path, or Governance Gate change.

The code change is a SQLite in-memory test-harness lifecycle hardening: request-scoped DB sessions, `session_scope`, and live-market background persistence now share a per-event-loop async serialization guard only when using SQLite `:memory:` / `StaticPool`. PostgreSQL behavior is unchanged.

---

## 2. Authority and Traceability

| Artifact | Path |
|---|---|
| W3-U08 final verdict | `docs/build-orders/ITRGA_VERDICT_W3-U08_FINAL_AND_WAVE3_CLOSURE.md` |
| W3-U08.1 Build Order | `docs/build-orders/BUILD_ORDER_W3-U08.1_HARDENING.md` |
| W3-U08.1 Intake | `docs/build-orders/BUILD_ORDER_INTAKE_W3-U08.1.md` |
| SQLite hardening ADR | `docs/adr/ADR-039_SQLite_StaticPool_Test_Harness_Hardening.md` |
| Operator evidence commands | `docs/evidence/W3-U08.1_OPERATOR_EVIDENCE_COMMANDS.md` |

---

## 3. Implementation Summary

### 3.1 OBS-1 fix — SQLite StaticPool serialization

Modified:

```text
backend/app/db/session.py
backend/app/market/live_service.py
```

Added:

```text
sqlite_staticpool_serialization(settings)
```

The guard:

- activates only for SQLite `:memory:` configurations;
- serializes request-scoped session work and `session_scope` work;
- serializes live-market background persistence through the same guard;
- prevents the single shared aiosqlite connection from being used concurrently by the request-scoped seed write and background adapter writer;
- does not affect PostgreSQL.

### 3.2 OBS-2 evidence completion

No additional product UI was required. The existing W3-U08 read-only `MonitoringAlertsPanel` remains available for browser evidence.

Created a W3-U08.1 evidence command pack requiring the four missing screenshots:

```text
W3-U08.1_BROWSER_01_LOGIN_AND_SHELL.png
W3-U08.1_BROWSER_02_MONITORING_ALERTS_READ_ONLY.png
W3-U08.1_BROWSER_03_NO_EXECUTION_CONTROLS.png
W3-U08.1_BROWSER_04_LOGGED_OUT_BLOCKED.png
```

### 3.3 Documentation

Created:

```text
docs/adr/ADR-039_SQLite_StaticPool_Test_Harness_Hardening.md
docs/evidence/W3-U08.1_OPERATOR_EVIDENCE_COMMANDS.md
DELIVERY_REPORT_W3-U08.1.md
```

Updated:

```text
CHANGELOG.md
PROJECT_STATE.md
README.md
docs/governance/TECHNICAL_DEBT_REGISTER.md
docs/governance/GOVERNANCE_AMENDMENTS.md
docs/governance/04_PROJECT_ROADMAP.md
```

---

## 4. Scope Compliance

| Build Order Constraint | DA Result |
|---|---|
| No new product feature | Compliant |
| No new endpoint/UI capability | Compliant; only evidence instructions use existing UI surfaces |
| No schema/migration | Compliant |
| No execution/broker/order path | Compliant |
| No test assertion masking / no xfail | Compliant; affected test remains active and meaningful |
| Fix harness for right reason | Implemented SQLite connection-lifecycle serialization |
| Preserve PostgreSQL behavior | Guard is SQLite `:memory:` only |

---

## 5. Local Validation Evidence Collected by DA

### Backend lint

```text
ruff check .
All checks passed!
```

### Live-market targeted test

```text
pytest tests/test_live_market.py -q
7 passed, 1 warning in 4.26s
```

### Flake stability repeat

```text
pytest tests/test_live_market.py::test_live_start_stop_and_status -q
```

was run five consecutive times against the SQLite in-memory test harness:

```text
RUN 1: 1 passed
RUN 2: 1 passed
RUN 3: 1 passed
RUN 4: 1 passed
RUN 5: 1 passed
```

No `no active connection` failure occurred.

### Full local regression

```text
$ pytest -q
192 passed, 1 warning in 39.39s

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
20260715_0018 (head)
```

Full operator `local_ci.sh` remains to be proven on the target per `docs/evidence/W3-U08.1_OPERATOR_EVIDENCE_COMMANDS.md`.

---

## 6. Known Risks / Required Operator Evidence

| Item | Status |
|---|---|
| `local_ci.sh` full target run | Required; evidence pack includes completion marker and `LOCAL_CI_EXIT_CODE: 0` proof |
| OBS-2 screenshots | Required; evidence pack lists four screenshot names |
| PostgreSQL full regression | Required; evidence pack includes full pytest/ruff/frontend commands |
| No new capability/gate change | Evidence pack includes grep and docs proof |

---

## 7. Operator Evidence Command Pack

Use:

```text
docs/evidence/W3-U08.1_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes exact commands for:

1. build identity;
2. Alembic head / no migration proof;
3. repeated flaky-test stability proof;
4. full `local_ci.sh` with `LOCAL_CI_EXIT_CODE: 0`;
5. full backend/frontend regression gates;
6. four missing browser screenshots;
7. no new capability / no execution / gate-closed grep;
8. docs residual-closure proof.

---

## 8. DA Non-Approval Statement

W3-U08.1 is implemented and locally validated by the Development Authority. It is **not accepted or residual-free by DA declaration**.

Acceptance requires:

1. operator-run target evidence using `docs/evidence/W3-U08.1_OPERATOR_EVIDENCE_COMMANDS.md`;
2. browser screenshots for OBS-2;
3. ITRGA residual-closure review;
4. ITRGA verdict that OBS-1 and OBS-2 are closed.

DA will not begin Wave 4 or any subsequent work without ITRGA approval and a new Build Order.

---

**End of Delivery Report W3-U08.1**
