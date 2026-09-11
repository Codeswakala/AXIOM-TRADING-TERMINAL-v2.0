# DELIVERY REPORT — W5-U02

## Human-AI Collaboration: Audited Assistant Research Responses

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Unit | W5-U02 — Audited Assistant Research Responses |
| Wave | 5 — Human-AI Collaboration |
| Build Order | `docs/build-orders/BUILD_ORDER_W5-U02.md` |
| Prerequisite review | `docs/build-orders/ITRGA_REVIEW_W5-U01.md` — W5-U01 APPROVED CLEAN |
| Target platform version | `0.40.0` |
| Alembic head | `20260717_0024` |
| DA status | Implemented and locally validated |
| Approval status | Not self-approved; pending operator evidence and ITRGA review |

---

## 1. Executive summary

W5-U02 has been implemented as an audited assistant response persistence and read-only API unit.

The deterministic W5-U01 assistant now persists every grounded research response and every refusal into the new `assistant_research_responses` table. Each row is inert, hash-only for request privacy, grounded-or-refused, carries the required disclaimer, and is linked to an immutable `audit_events` record by response id and audit correlation id.

No UI panel was added in this unit. No external LLM/API, new compiled/tokenizer dependency, action tool, prompt/mutation API, execution/order/sizing/account/broker/position path, Gate-opening path, auto-retraining, or auto-remediation path was added.

The Constitutional Governance Gate remains **CLOSED**.

---

## 2. Scope delivered

### A. Response persistence

Implemented a new persisted assistant research-response artifact:

- ORM model: `backend/app/db/models/assistant_research_response.py`
- Alembic migration: `backend/alembic/versions/20260717_0024_w5_u02_assistant_research_responses.py`
- Repository: `backend/app/collaboration/research_responses.py`
- Seed/evidence script: `scripts/w5_u02_seed_assistant_responses.py`

Table: `assistant_research_responses`

Key fields:

- `assistant_response_id`
- `created_at`
- `operator_id`
- `request_id`
- `request_text_hash`
- `assistant_policy_version`
- `provider_name`
- `provider_version`
- `model_or_engine_version`
- `source_artifact_ids`
- `grounding_summary`
- `response_text`
- `refused`
- `refusal_reason`
- `limitations`
- `disclaimer`
- `research_status`
- `audit_correlation_id`
- `provenance`

Privacy control implemented: the schema stores only `request_text_hash`; there is no raw request/prompt text column.

### B. Assistant integration

Modified the deterministic local assistant so each response/refusal is persisted through `AssistantResearchResponseRepository.create_from_response()`.

The repository:

1. validates grounded responses have source artifact ids;
2. validates refusals carry a refusal reason;
3. rejects sampled secret markers before persistence;
4. inserts the response/refusal row;
5. appends the required audit event;
6. raises on audit failure so the outer transaction rolls back instead of leaving an orphan row.

Audit actions:

- grounded response: `assistant.response_draft_created`
- refusal: `assistant.refused`

Audit relationship:

- `audit_events.resource_type = 'assistant_response'`
- `audit_events.resource_id = assistant_research_responses.assistant_response_id`
- `audit_events.correlation_id = assistant_research_responses.audit_correlation_id`

### C. Read-only API

Added authenticated read-only endpoints:

- `GET /api/v1/collaboration/assistant-responses`
- `GET /api/v1/collaboration/assistant-responses/{response_id}`

Implemented files:

- `backend/app/api/routes/collaboration.py`
- `backend/app/models/assistant_research_response.py`
- `backend/app/api/router.py`

No POST/mutation endpoint was added. POST to the collection returns framework-level `405/404` depending on runtime routing behavior.

### D. Documentation and governance artifacts

Created:

- `docs/build-orders/ITRGA_REVIEW_W5-U01.md`
- `docs/build-orders/BUILD_ORDER_W5-U02.md`
- `docs/build-orders/BUILD_ORDER_INTAKE_W5-U02.md`
- `docs/adr/ADR-049_Audited_Assistant_Research_Responses.md`
- `docs/evidence/W5-U02_OPERATOR_EVIDENCE_COMMANDS.md`
- `DELIVERY_REPORT_W5-U02.md`

Updated:

- `README.md`
- `PROJECT_STATE.md`
- `CHANGELOG.md`
- `docs/governance/RISK_REGISTER.md`
- `docs/governance/TECHNICAL_DEBT_REGISTER.md`
- `docs/governance/GOVERNANCE_AMENDMENTS.md`
- `docs/governance/04_PROJECT_ROADMAP.md`

---

## 3. Governance guardrails preserved

| Guardrail | Result |
|---|---|
| R5-1 — structural non-actuation | Preserved. Tool registry remains read + own-audited-artifact-write only. No action tool exists. |
| R5-2 — no external LLM/API or new dependency | Preserved. No external LLM/API, tokenizer, compiled dependency, or new runtime package added. |
| R5-3 — prompt-injection / secret-exfiltration refusal and audit | Implemented and re-tested. Refusals persist with reason codes and audit rows. |
| R5-5 — grounding-or-refuse | Implemented. Grounded rows require source artifact ids; ungrounded requests persist only as `GROUNDING_REQUIRED` refusals. |
| R5-6 — disclaimer | Implemented. Every stored row carries the disclaimer and response text includes “AXIOM does not act.” No UI panel added, so browser screenshot is N/A for this unit. |
| R5-7 — persistence capture | Implemented. New Alembic head `20260717_0024`; operator evidence includes raw SELECT + no-orphan audit join. |
| R5-8 — bright-line grep + CI | Evidence command pack includes wave-wide grep and documented Git-Bash CI invocation. Local targeted grep found no collaboration-context LLM/execution hits. |

---

## 4. Refusal reasons persisted

The following refusal reasons are supported and tested/persisted:

- `ORDER_INSTRUCTION_REFUSED`
- `GATE_OPEN_INSTRUCTION_REFUSED`
- `SECRET_EXFILTRATION_REFUSED`
- `UNBOUNDED_TOOL_REQUEST_REFUSED`
- `GROUNDING_REQUIRED`
- `ASSISTANT_DISABLED`

Each refusal is persisted with:

- `refused = true`
- `research_status = 'refused'`
- `refusal_reason = <reason>`
- required disclaimer
- audit event `assistant.refused`

---

## 5. Files changed or added for W5-U02

### Backend created

```text
backend/app/db/models/assistant_research_response.py
backend/app/collaboration/research_responses.py
backend/app/api/routes/collaboration.py
backend/app/models/assistant_research_response.py
backend/alembic/versions/20260717_0024_w5_u02_assistant_research_responses.py
backend/tests/test_assistant_research_responses.py
```

### Backend modified

```text
backend/app/__init__.py
backend/app/api/router.py
backend/app/collaboration/__init__.py
backend/app/collaboration/assistant.py
backend/app/collaboration/contracts.py
backend/app/core/config.py
backend/app/db/models/__init__.py
backend/app/main.py
backend/app/models/system.py
backend/pyproject.toml
backend/tests/test_system.py
```

### Frontend modified

```text
frontend/src/layouts/TerminalLayout.tsx
```

Note: no assistant UI panel was added; the frontend change updates the shell unit badge to `W5-U02`.

### Scripts/docs created or updated

```text
scripts/w5_u02_seed_assistant_responses.py
docs/build-orders/ITRGA_REVIEW_W5-U01.md
docs/build-orders/BUILD_ORDER_W5-U02.md
docs/build-orders/BUILD_ORDER_INTAKE_W5-U02.md
docs/adr/ADR-049_Audited_Assistant_Research_Responses.md
docs/evidence/W5-U02_OPERATOR_EVIDENCE_COMMANDS.md
DELIVERY_REPORT_W5-U02.md
README.md
PROJECT_STATE.md
CHANGELOG.md
docs/governance/RISK_REGISTER.md
docs/governance/TECHNICAL_DEBT_REGISTER.md
docs/governance/GOVERNANCE_AMENDMENTS.md
docs/governance/04_PROJECT_ROADMAP.md
```

---

## 6. Local validation performed by DA

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

### Targeted W5 collaboration tests

Command:

```bash
cd /home/user/axiom/backend
pytest tests/test_collaboration_safety.py tests/test_assistant_research_responses.py -q
```

Result:

```text
24 passed, 1 warning
```

### Backend full suite

Command:

```bash
cd /home/user/axiom/backend
pytest -q
```

Result:

```text
257 passed, 1 warning
```

### Alembic migration smoke

Command used a temporary SQLite database:

```bash
cd /home/user/axiom/backend
AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w5u02_alembic.db' \
AXIOM_DATABASE_AUTO_CREATE_SCHEMA=false \
alembic upgrade head

AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w5u02_alembic.db' \
AXIOM_DATABASE_AUTO_CREATE_SCHEMA=false \
alembic current
```

Result:

```text
20260717_0024 (head)
```

### Frontend validation

Command:

```bash
cd /home/user/axiom/frontend
npm ci
npm audit --audit-level=high
npm test
npm run lint
npm run build
```

Result:

```text
npm audit: found 0 vulnerabilities
Vitest: 12 files passed / 29 tests passed
TypeScript lint: clean
Build: successful
```

### Collaboration context grep

Command:

```bash
grep -RInE "openai|anthropic|transformers|langchain|llama|place_order|broker\.|emit_signal|gate_open|allow_execution|model\.status =|advisory_status =" backend/app/collaboration || true
```

Result:

```text
No output
```

---

## 7. Operator evidence pack

Operator evidence command pack is ready at:

```text
docs/evidence/W5-U02_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes exact Windows PowerShell + PostgreSQL commands for:

1. build identity;
2. Alembic head advance to `20260717_0024`;
3. committing seed script;
4. raw `psql SELECT` from `assistant_research_responses`;
5. no-orphan audit JOIN with expected `orphan_count = 0`;
6. persisted refusal reason proof;
7. no raw request text column proof;
8. secret-marker stored-output check;
9. disclaimer check;
10. read-only API proof: unauth 401, list 200, detail 200, POST 405/404;
11. no LLM/no execution bright-line grep;
12. full regression;
13. documented Git-Bash local CI invocation and parity smoke.

---

## 8. Deferred / explicitly not implemented

The following remain out of scope and were not implemented:

- external LLM/API/provider integration;
- new compiled, tokenizer, LLM, or ML dependency;
- assistant UI panel;
- prompt/mutation API;
- assistant action tool;
- chart annotations/drawing tools;
- trade planning workspace persistence;
- journal persistence;
- signal investigation workspace;
- scenario comparison workspace;
- execution/order/sizing/broker/account/position path;
- Constitutional Governance Gate opening;
- paper trading;
- auto-retraining;
- auto-remediation;
- W5-U03 or later functionality;
- Wave-6 functionality.

---

## 9. DA disposition

W5-U02 is implemented and locally validated by the Development Authority.

This is **not** an approval. DA does not self-approve and does not self-authorize W5-U03.

Next required step: operator runs `docs/evidence/W5-U02_OPERATOR_EVIDENCE_COMMANDS.md` on the target Windows/PostgreSQL environment and submits the transcript to ITRGA for independent review.

---

**End of DELIVERY_REPORT_W5-U02.md**
