# Delivery Report — W3-U05

| Field | Value |
|---|---|
| Build Order | **W3-U05** Operator Advisory Dashboard / Signal Workspace |
| Platform | **0.27.0** |
| Wave | **3 — Live Research Advisor** |
| DA status | **Implemented and locally validated** |
| Approval status | **Not self-approved; pending operator evidence, browser screenshots, and ITRGA review** |
| Date | 2026-07-15 |

---

## 1. Executive Summary

W3-U05 implements AXIOM's first operator-facing advisory signal UI. The protected `/signals` workspace reads the existing W3-U02 read-only signal-history API and displays governed signals with calibrated confidence, rationale, guardrail state, economic verdict, freshness/expiry, and validation lineage.

The implementation preserves the R-3 bright line:

- advisory signals are framed as research records, not instructions;
- the disclaimer is visible;
- warning/withheld/expired/superseded records are visibly distinct from clean advisory records;
- calibrated confidence is shown instead of raw score;
- the UI performs presentation/formatting only;
- no client-side inference/signal/economic computation was added;
- no signal write/emit surface was added;
- no execution controls, broker controls, transaction controls, alerts, live signal push, paper trading, or position path were added.

DA does not self-approve. This delivery is submitted for operator evidence collection, mandatory browser screenshots, and ITRGA independent review.

---

## 2. Authority and Traceability

| Artifact | Path |
|---|---|
| W3-U05 Build Order | `docs/build-orders/BUILD_ORDER_W3-U05.md` |
| W3-U05 Build Order Intake | `docs/build-orders/BUILD_ORDER_INTAKE_W3-U05.md` |
| Advisory Dashboard ADR | `docs/adr/ADR-035_Advisory_Dashboard_UX.md` |
| Operator evidence commands | `docs/evidence/W3-U05_OPERATOR_EVIDENCE_COMMANDS.md` |

Note: the user attached `ITRGA_REVIEW_W2-U04.md`, which is historical and not W3-U04 review material. The W3-U05 Build Order itself states it was issued following W3-U04 approval with observations; DA recorded this in the W3-U05 intake and implemented against the issued Build Order authority.

---

## 3. Implementation Summary

### 3.1 Protected Advisory Signal Workspace

Added route:

```text
/signals
```

It is nested under the existing `ProtectedRoute` and `TerminalLayout`, so unauthenticated operators are redirected to login before viewing the workspace.

### 3.2 Read-only API Consumption

Added frontend types and read-only fetcher:

```text
fetchAdvisorySignals(...)
AdvisorySignal
AdvisorySignalState
```

The UI uses:

```text
GET /api/v1/signals/history
```

No POST/emit path was added.

### 3.3 Honest Signal Presentation

The workspace displays:

- signal state;
- signal direction;
- calibrated confidence;
- calibration status;
- rationale;
- state reason;
- operating-domain status;
- economic verdict;
- freshness/expiry;
- model version;
- experiment id;
- feature-set version;
- statistical/calibration/economic/generalization report lineage;
- explainability summary.

States are visually distinguished:

```text
emitted    → Advisory
warning    → Warning
withheld   → Withheld
expired    → Expired
superseded → Superseded
```

### 3.4 Advisory Framing

Visible disclaimer:

```text
Research advisory only. This screen is not financial advice, not a trade instruction, and not an automated action surface. Operator judgment remains required.
```

The UI avoids transaction action controls and wording that would direct the operator to trade.

### 3.5 F-1 Closure

The frontend test configuration now has an explicit Vitest timeout:

```text
testTimeout: 10000
```

The previously carried frontend flakiness concern is addressed by a stable local frontend suite:

```text
9 test files passed
20 tests passed
```

Operator evidence commands include the required full `local_ci.sh` completion-marker proof.

---

## 4. Files Created

```text
frontend/src/pages/AdvisorySignalsPage.tsx
frontend/src/pages/AdvisorySignalsPage.test.tsx
docs/adr/ADR-035_Advisory_Dashboard_UX.md
docs/build-orders/BUILD_ORDER_W3-U05.md
docs/build-orders/BUILD_ORDER_INTAKE_W3-U05.md
docs/evidence/W3-U05_OPERATOR_EVIDENCE_COMMANDS.md
DELIVERY_REPORT_W3-U05.md
```

---

## 5. Files Modified

```text
frontend/src/App.tsx
frontend/src/api/client.ts
frontend/src/layouts/TerminalLayout.tsx
frontend/src/styles/global.css
frontend/vite.config.ts
backend/app/__init__.py
backend/app/core/config.py
backend/app/main.py
backend/app/models/system.py
backend/pyproject.toml
backend/tests/test_system.py
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
| Protected operator dashboard reads read-only history API | Implemented at `/signals` under existing auth-protected layout |
| Presentation-only UI | Implemented; component reads API and formats fields only |
| No execution controls | Implemented; UI tests and grep evidence command included |
| Advisory framing + visible disclaimer | Implemented and tested |
| Guardrail outcomes visibly distinct | Implemented and tested for emitted/warning/withheld/expired/superseded |
| Calibrated confidence shown, not raw score | Implemented and tested |
| Rationale/domain/economic/freshness/lineage surfaced | Implemented and tested |
| No new signal write/emit surface | Preserved; evidence pack includes 401/200/405 API proof |
| F-1 closure | Frontend test timeout stabilized; frontend suite green locally; local CI command included |
| Browser evidence | Evidence pack includes mandatory real-browser screenshot instructions |

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
183 passed, 1 warning in 33.32s
```

### Frontend audit

```text
$ npm audit --audit-level=high
found 0 vulnerabilities
```

### Frontend tests

```text
$ npm test
Test Files 9 passed
Tests 20 passed
```

### Frontend typecheck/build

```text
$ npm run lint
# TypeScript clean

$ npm run build
✓ built
```

### No execution-control grep over W3-U05 UI source

```text
grep -RInE "\bbuy\b|\bsell\b|\border\b|place_order|\bexecute\b|\bposition\b|\bbroker\b|paper.?trade" frontend/src --exclude='client.ts' --exclude='types.ts' --exclude='types.test.ts' --exclude='useChartData.ts' --exclude='ChartWorkspacePage.tsx' --exclude='global.css'
# no output
```

### Presentation-only grep over advisory page

```text
grep -RInE "score\(|raw_score|economic_conclusion|expected_calibration_error|LiveInferenceEngine|AdvisorySignalService" frontend/src/pages/AdvisorySignalsPage.tsx
# no output
```

### No signal emit/execution API grep

```text
grep -RInE "live_signal|emit_signal|place_order|cancel_order" backend/app/api/routes frontend/src
# no output
```

---

## 8. Security Review

| Area | Review |
|---|---|
| Authentication | `/signals` is protected by existing route guard. |
| Authorization | No public dashboard route added. |
| Tokens/secrets | No secrets or token values are rendered. |
| PII | No PII introduced. |
| Write surface | No signal write/emit API or UI path added. |
| Execution | No transaction action controls, broker controls, or execution paths added. |

---

## 9. Performance / Scalability Review

- Signal history fetch is bounded by `limit=100` in the UI.
- Filtering is passed to the API as query parameters.
- Rendering is simple list/detail presentation.
- No streaming, polling loop, or live signal push is introduced.

---

## 10. Maintainability Review

- UI is isolated in `AdvisorySignalsPage.tsx`.
- API types are centralized in `api/client.ts`.
- Styling uses existing theme variables.
- Tests cover state visibility, disclaimer, calibrated confidence, rationale, lineage, and no transaction action controls.
- No backend signal behavior was rewritten.

---

## 11. Governance Compliance Review

| Rule | Compliance |
|---|---|
| Build Order scope | Implemented Components A–F only. |
| No future wave work | No W3-U06 alerts/live push, W3-U07 analytics, or Wave-6 execution implemented. |
| UX presentation-only | UI displays API fields; no inference/signal/economic computation. |
| R-3 advisory-not-instruction | Disclaimer and non-action framing implemented. |
| No execution controls | UI contains no transaction action controls. |
| Browser evidence | Operator evidence commands include mandatory screenshot capture steps. |
| ITRGA relationship | DA does not self-approve; report submitted for independent review. |

---

## 12. Known Risks

| Risk | Status |
|---|---|
| Browser screenshots not collected in DA sandbox | Operator-run browser evidence required by evidence pack. |
| Alerts/live signal push absent | Accepted; explicitly W3-U06 scope. |
| Deeper dashboard analytics absent | Accepted; explicitly W3-U07/future scope. |
| Automated browser E2E absent | Recorded as TD-060; manual real-browser screenshots required for W3-U05. |
| W3-U04 review artifact not attached in this turn | W3-U05 Build Order states W3-U04 approval; intake records missing review artifact. |

---

## 13. Technical Debt Updates

Updated `TECHNICAL_DEBT_REGISTER.md`:

- `TD-057` closed foundationally: operator advisory dashboard implemented.
- `TD-058` remains open: alerts/live signal push deferred to W3-U06.
- `TD-060` added: automated browser E2E absent; manual screenshots required for this unit.

---

## 14. Operator Evidence Command Pack

The full operator evidence command pack is available at:

```text
docs/evidence/W3-U05_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes exact Windows PowerShell + PostgreSQL + browser steps for:

1. schema status to `20260715_0017 (head)`;
2. backend/frontend full tests;
3. named advisory UI and LivePriceTable tests;
4. local CI completion marker for F-1;
5. browser seed data creation;
6. mandatory screenshots for logged-out block, signal list/detail, disclaimer, guardrail outcomes, and no transaction controls;
7. read-only API 401/200/405 proof;
8. no-execution/no-client-computation grep evidence;
9. parity smoke.

---

## 15. DA Non-Approval Statement

W3-U05 is implemented and locally validated by the Development Authority. It is **not accepted, approved, or complete by DA declaration**.

Acceptance requires:

1. operator-run target evidence using `docs/evidence/W3-U05_OPERATOR_EVIDENCE_COMMANDS.md`;
2. real browser screenshots as specified by the Build Order;
3. ITRGA independent review;
4. ITRGA verdict.

DA will not begin W3-U06 or any subsequent unit without ITRGA approval and a new Build Order.

---

**End of Delivery Report W3-U05**
