# DELIVERY REPORT — W5-U04

## Human-AI Collaboration: Signal Investigation Workspace

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Unit | W5-U04 — Signal Investigation Workspace |
| Wave | 5 — Human-AI Collaboration |
| Build Order | `docs/build-orders/BUILD_ORDER_W5-U04.md` |
| Prerequisite review | `docs/build-orders/ITRGA_REVIEW_W5-U03.md` — W5-U03 APPROVED CLEAN |
| Target platform version | `0.42.0` |
| Alembic head | `20260717_0025` unchanged; no W5-U04 migration |
| DA status | Implemented and locally validated |
| Approval status | Not self-approved; pending operator evidence, browser screenshots, and ITRGA review |

---

## 1. Executive summary

W5-U04 has been implemented as a read-only Signal Investigation Workspace.

The workspace lets operators investigate persisted advisory signals by viewing rationale, guardrail states, calibrated confidence, lineage, linked validation/report ids, and recent institutional intelligence reports. It reuses existing read-only APIs and adds no signal mutation endpoint, no new analytical artifact, no migration, and no assistant summary path.

No external LLM/API, new compiled/tokenizer dependency, signal mutation/re-emission/re-grade/guardrail override, action tool, order/sizing/account/broker/position path, execution path, Gate-opening path, auto-retraining, or auto-remediation path was added.

The Constitutional Governance Gate remains **CLOSED**.

---

## 2. Scope delivered

### A. Signal investigation UI

Added protected frontend route:

```text
/investigate
```

Implemented files:

```text
frontend/src/pages/SignalInvestigationPage.tsx
frontend/src/pages/SignalInvestigationPage.test.tsx
```

Modified:

```text
frontend/src/App.tsx
frontend/src/api/client.ts
frontend/src/layouts/TerminalLayout.tsx
frontend/src/styles/global.css
```

The workspace displays:

- persisted signal selector;
- signal rationale;
- guardrail states:
  - state reason;
  - operating domain;
  - calibration status;
  - economic verdict;
  - freshness;
  - expiry;
- calibrated confidence only;
- lineage:
  - signal id;
  - model id/version;
  - experiment id;
  - feature-set version;
  - inference input hash;
- linked validation/report ids;
- recent institutional intelligence report summaries;
- research/not-instruction disclaimer.

### B. Existing read-only APIs reused

W5-U04 uses existing APIs:

```text
GET /api/v1/signals/history
GET /api/v1/signals/history/{signal_id}
GET /api/v1/intelligence/correlation-reports
GET /api/v1/intelligence/regime-reports
GET /api/v1/intelligence/scenario-reports
GET /api/v1/intelligence/portfolio-risk-reports
GET /api/v1/intelligence/signal-validation-reports
```

No new backend route was required.

A small frontend API helper was added:

```text
fetchAdvisorySignal(signalId)
```

This helper is read-only and uses the existing detail endpoint.

### C. No-signal-mutation tests

Created backend test file:

```text
backend/tests/test_signal_investigation_workspace.py
```

Named tests:

```text
test_signal_investigation_reads_require_auth_and_return_persisted_context
test_signal_investigation_triggers_and_mutates_nothing
test_signal_investigation_has_no_signal_write_endpoint
test_signal_investigation_workspace_has_no_mutation_or_execution_path
```

The keystone test reads signal list/detail repeatedly and asserts:

- advisory signal row count unchanged;
- model artifact row count unchanged;
- investigated signal snapshot unchanged;
- model `status` unchanged;
- model `advisory_status` unchanged.

### D. No assistant-summary path

No assistant summary was implemented in W5-U04.

Therefore:

- no assistant summary persistence was added;
- no R5-7 assistant summary capture is triggered;
- no new assistant table or migration is added;
- W5-U01/W5-U02 safety tests remain in regression.

---

## 3. Governance guardrails preserved

| Guardrail / keystone | Result |
|---|---|
| No-signal-mutation keystone | Implemented and tested. Investigation reads mutate no advisory signal/model row and expose no write endpoint. |
| R5-6 browser evidence | UI implemented; operator evidence pack requires served-browser screenshots for investigation view and logged-out block. |
| R5-8 grep + CI | Evidence pack includes no-mutation/no-execution grep and Git-Bash CI invocation. |
| R5-2 no LLM/dependency | Preserved. No external LLM/API or new dependency added. |
| Presentation-only GR-8 | UI displays persisted signal/report data only and states no client-side inference or authoritative recompute. |
| No raw score | UI shows calibrated confidence only; frontend test verifies raw score is not rendered. |
| No action controls | UI tests verify no buy/sell/order/broker/execute/position controls. |
| No new report type | Preserved. Existing APIs only; no new artifact/migration. |
| Gate CLOSED | Preserved. No Gate-opening path added. |

---

## 4. Files changed or added for W5-U04

### Created

```text
backend/tests/test_signal_investigation_workspace.py
frontend/src/pages/SignalInvestigationPage.tsx
frontend/src/pages/SignalInvestigationPage.test.tsx
docs/build-orders/ITRGA_REVIEW_W5-U03.md
docs/build-orders/BUILD_ORDER_W5-U04.md
docs/build-orders/BUILD_ORDER_INTAKE_W5-U04.md
docs/adr/ADR-051_Signal_Investigation_Workspace.md
docs/evidence/W5-U04_OPERATOR_EVIDENCE_COMMANDS.md
DELIVERY_REPORT_W5-U04.md
```

### Modified

```text
backend/app/__init__.py
backend/app/core/config.py
backend/app/main.py
backend/app/models/system.py
backend/pyproject.toml
backend/tests/test_system.py
frontend/src/App.tsx
frontend/src/api/client.ts
frontend/src/layouts/TerminalLayout.tsx
frontend/src/styles/global.css
README.md
PROJECT_STATE.md
CHANGELOG.md
docs/governance/RISK_REGISTER.md
docs/governance/TECHNICAL_DEBT_REGISTER.md
docs/governance/GOVERNANCE_AMENDMENTS.md
docs/governance/04_PROJECT_ROADMAP.md
```

### Not created

```text
No W5-U04 Alembic migration
No W5-U04 backend table
No signal write endpoint
No assistant summary table/path
```

---

## 5. Local validation performed by DA

### Backend Ruff

Command:

```bash
cd /home/user/axiom/backend
ruff check .
```

Result:

```text
All checks passed!
```

### Targeted W5 tests

Command:

```bash
cd /home/user/axiom/backend
pytest tests/test_collaboration_safety.py tests/test_assistant_research_responses.py tests/test_chart_research_annotations.py tests/test_signal_investigation_workspace.py -q
```

Result:

```text
35 passed, 1 warning
```

### Backend full suite

Command:

```bash
cd /home/user/axiom/backend
pytest -q
```

Result:

```text
268 passed, 1 warning
```

### Alembic migration smoke

Command used a temporary SQLite database:

```bash
cd /home/user/axiom/backend
AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w5u04_alembic.db' \
AXIOM_DATABASE_AUTO_CREATE_SCHEMA=false \
alembic upgrade head

AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w5u04_alembic.db' \
AXIOM_DATABASE_AUTO_CREATE_SCHEMA=false \
alembic current
```

Result:

```text
20260717_0025 (head)
```

No W5-U04 migration was added.

### Frontend validation

Commands:

```bash
cd /home/user/axiom/frontend
npm ci
npm audit --audit-level=high
npm test
npm run lint
npm run build
```

Results:

```text
npm audit: found 0 vulnerabilities
Vitest: 14 files passed / 38 tests passed
TypeScript lint: clean
Build: successful
```

### Mutation and LLM grep

Signal-investigation mutation grep:

```bash
grep -RInE "advisory_status\s*=|model\.status\s*=|emit_signal|place_order|update.*signal|override.*guardrail" frontend/src/pages/SignalInvestigationPage.tsx backend/app/api/routes/advisory_signals.py || true
```

Result:

```text
No output
```

Collaboration context LLM/execution grep:

```bash
grep -RInE "openai|anthropic|transformers|langchain|llama|place_order|broker\.|emit_signal|gate_open|allow_execution|model\.status =|advisory_status =" backend/app/collaboration || true
```

Result:

```text
No output
```

---

## 6. Operator evidence pack

Operator evidence command pack is ready at:

```text
docs/evidence/W5-U04_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes exact Windows PowerShell + PostgreSQL + browser steps for:

1. build identity;
2. no migration / unchanged Alembic head proof;
3. named no-signal-mutation tests;
4. SQL before/after snapshot of an investigated signal;
5. API proof: unauth 401, auth list/detail 200, no signal-write endpoints;
6. mandatory served-browser screenshots showing investigation view and logged-out block;
7. presentation-only/no raw score/no assistant summary proof;
8. no LLM/no mutation/no execution bright-line grep;
9. full regression;
10. documented Git-Bash local CI invocation and parity smoke.

---

## 7. Browser evidence status

W5-U04 has UI, so browser evidence is mandatory for approval.

DA implemented the route and evidence pack. The operator must run the served app and capture:

```text
docs/evidence/W5-U04_BROWSER/01_signal_investigation_rendered.png
docs/evidence/W5-U04_BROWSER/02_logged_out_block.png
```

The first screenshot must show:

- signal rationale;
- guardrail states;
- lineage/report ids;
- linked intelligence reports;
- research/not-instruction framing;
- calibrated confidence;
- no raw score;
- no execution/order/broker/account/position controls.

Missing or unreachable browser screenshots should result in ITRGA approval being withheld per Build Order.

---

## 8. Deferred / explicitly not implemented

The following remain out of scope and were not implemented:

- signal mutation, re-emission, re-grade, or guardrail override;
- signal write endpoint;
- assistant summary path;
- external LLM/API/provider integration;
- new compiled, tokenizer, LLM, or ML dependency;
- new report type;
- new migration/table;
- scenario comparison workspace;
- trade planning workspace persistence;
- journal persistence;
- execution/order/sizing/broker/account/position path;
- Constitutional Governance Gate opening;
- paper trading;
- auto-retraining;
- auto-remediation;
- W5-U05 or later functionality;
- Wave-6 functionality.

---

## 9. DA disposition

W5-U04 is implemented and locally validated by the Development Authority.

This is **not** an approval. DA does not self-approve and does not self-authorize W5-U05.

Next required step: operator runs `docs/evidence/W5-U04_OPERATOR_EVIDENCE_COMMANDS.md` on the target Windows/PostgreSQL/browser environment and submits the transcript + screenshots to ITRGA for independent review.

---

**End of DELIVERY_REPORT_W5-U04.md**
