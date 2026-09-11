# DELIVERY REPORT — W7-U05

## Plugin Contract Safety Foundation

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Unit | W7-U05 — Plugin Contract Safety Foundation |
| Wave | 7 — Institutional Platform |
| Build Order | `docs/build-orders/BUILD_ORDER_W7-U05.md` |
| Prerequisite verdict | `docs/build-orders/ITRGA_VERDICT_W7-U04_FINAL.md` — W7-U04 APPROVED |
| Platform of record before unit | `0.58.0` |
| Target platform version | `0.59.0` candidate |
| Alembic head | `20260717_0037` unchanged |
| DA status | Implemented and locally validated |
| Approval status | Not self-approved; pending operator evidence / ITRGA review |

---

## 1. Executive summary

W7-U05 has been implemented as a **plugin contract safety foundation**: published extension contract descriptors, read/research-only capability allowlist, built-in reference contract descriptors, authenticated read-only contract listing API, and an audit-backed hostile contract refusal seam.

The implementation deliberately does **not** add dynamic plugin execution, third-party plugin loading, plugin runtime dispatch, plugin registry persistence, plugin execution audit table, plugin UI, dependency, broker/order/account/live/Gate path, or W7-U06+ capability.

Central R7-1 posture:

```text
contracts + refusal only
no dynamic/third-party plugin code execution
no plugin_execution_audit_events table
```

The hostile-plugin refusal seam checks a contract request as metadata and refuses unsafe requests. Refusals are audited to the existing immutable `audit_events` table with action:

```text
plugin_contract_request.refused
```

The Constitutional Governance Gate remains **CLOSED**.

---

## 2. Scope delivered

### A. Plugin contract package

Created:

```text
backend/app/institutional_platform/plugins/__init__.py
backend/app/institutional_platform/plugins/contracts.py
backend/app/institutional_platform/plugins/registry.py
backend/app/institutional_platform/plugins/service.py
```

Key implementation:

```text
PublishedPluginContract
PluginContractRequest
PluginContractDecision
PluginContractSafetyService
```

Static contract version:

```text
w7-u05.plugin_contracts.v1
```

Capability allowlist:

```text
report.export
chart.type
analytics.view
```

Built-in reference contract descriptors:

```text
builtin.report_export.markdown.v1
builtin.chart_type.research_overlay.v1
builtin.analytics_view.summary_cards.v1
```

All published contracts are marked:

```text
read_only: true
built_in: true
```

### B. Refusal seam

Implemented in:

```text
backend/app/institutional_platform/plugins/service.py
```

The service refuses requests for:

- unknown contract ids;
- non-allowlisted capabilities;
- capability mismatch against contract descriptor;
- imports outside the narrow allowed prefix list;
- non-current-operator data scope;
- governed-artifact writes;
- sensitive material reads;
- network access.

Refusal returns:

```text
accepted: false
reason_code: <...REFUSED>
audit_correlation_id: <uuid>
```

and appends an existing `audit_events` row:

```text
category: SECURITY
action: plugin_contract_request.refused
resource_type: plugin_contract_request
resource_id: <requested_contract_id>
details.reason_code: <...REFUSED>
details.accepted: false
```

### C. API

Extended:

```text
backend/app/api/routes/institutional_platform.py
backend/app/institutional_platform/rbac.py
```

New authenticated read-only endpoint:

```text
GET /api/v1/institutional-platform/plugin-contracts
```

The endpoint returns:

```text
contract_version
contracts
capability_allowlist
dynamic_code_execution_enabled: false
third_party_plugin_execution_enabled: false
plugin_execution_audit_table_present: false
governance_gate_capability_present: false
```

RBAC permission added:

```text
institutional.plugin_contracts.read
```

The permission vocabulary remains free of execution/order/account/broker/Gate capability markers.

### D. Persistence choice

No plugin contract registry table was added.

No migration was added.

No `plugin_execution_audit_events` table was added.

Alembic head remains:

```text
20260717_0037
```

Hostile-refusal audit uses the existing `audit_events` table.

### E. Frontend choice

No frontend plugin contract catalogue UI was added.

Only the shell unit label was updated to W7-U05.

Browser evidence is not applicable because W7-U05 is API-only.

---

## 3. Guardrail compliance

| Requirement | Result |
|---|---|
| R7-1 no dynamic/third-party execution | Implemented and tested. Plugin package has no `eval`, `exec(`, `importlib`, entry-point loading, subprocess, or compile dispatch. |
| R7-1 no plugin execution audit table | Implemented and tested. No `plugin_execution_audit_events` table or model exists. |
| R7-6 hostile-plugin refusal | Implemented and tested. Hostile request is refused and audited to existing `audit_events`. |
| §16/§17 containment | Implemented and tested. Plugin package has no broker/order/account/live/Gate reach markers. |
| Capability allowlist | Implemented and tested. Only `report.export`, `chart.type`, `analytics.view`; no execution/order/account/Gate vocabulary. |
| Auth on contract surface | Implemented and tested. Unauth `401`; auth `200`. |
| No secrets/PII | Implemented and tested. Contract surface marker scan is clean. |
| GR7-9 persistence capture | Not applicable for registry tables. Hostile refusal audit row is captured through existing `audit_events`. |
| GR7-10 browser proof | Not applicable. No W7-U05 UI surface added. |
| GR7-1 Gate CLOSED | Preserved and tested. |
| No dependency change | Preserved. No new package added. |

---

## 4. Files changed or added for W7-U05

### Backend created

```text
backend/app/institutional_platform/plugins/__init__.py
backend/app/institutional_platform/plugins/contracts.py
backend/app/institutional_platform/plugins/registry.py
backend/app/institutional_platform/plugins/service.py
backend/tests/test_plugin_contracts.py
```

### Backend modified

```text
backend/app/__init__.py
backend/app/api/routes/institutional_platform.py
backend/app/core/config.py
backend/app/institutional_platform/__init__.py
backend/app/institutional_platform/rbac.py
backend/app/main.py
backend/app/models/system.py
backend/tests/test_system.py
```

### Frontend modified

```text
frontend/src/layouts/TerminalLayout.tsx
```

### Scripts/docs created or updated

```text
scripts/w7_u05_seed_plugin_refusal.py
docs/build-orders/ITRGA_VERDICT_W7-U04_FINAL.md
docs/build-orders/BUILD_ORDER_W7-U05.md
docs/build-orders/BUILD_ORDER_INTAKE_W7-U05.md
docs/adr/ADR-068_Plugin_Contract_Safety_Foundation.md
docs/evidence/W7-U05_OPERATOR_EVIDENCE_COMMANDS.md
DELIVERY_REPORT_W7-U05.md
README.md
PROJECT_STATE.md
CHANGELOG.md
```

---

## 5. Mandatory tests implemented

Backend tests in:

```text
backend/tests/test_plugin_contracts.py
```

Mandatory tests implemented:

```text
test_plugin_contract_layer_has_no_dynamic_or_thirdparty_code_execution
test_plugin_contract_disallows_broker_order_account_gate_imports
test_hostile_plugin_request_refused_and_audited
test_plugin_capabilities_are_allowlisted_read_research_only
test_no_plugin_execution_audit_events_table
test_plugin_contract_surface_requires_auth
test_plugin_contract_has_no_secret_or_pii_markers
test_gate_remains_closed_for_wave7
```

No persistence-capture/forbidden-column/operator-scoping tests were added for plugin registry tables because no plugin registry table was persisted.

No frontend plugin-contract tests were added because no W7-U05 UI surface was added.

---

## 6. Local validation performed by DA

### Backend Ruff

```bash
cd /home/user/axiom/backend
ruff check .
```

Result:

```text
All checks passed!
```

### Targeted backend tests

```bash
cd /home/user/axiom/backend
pytest tests/test_plugin_contracts.py tests/test_api_catalogue.py tests/test_research_management.py tests/test_workspace_preferences.py tests/test_institutional_platform_security.py tests/test_broker_integration.py -q
```

Result:

```text
48 passed, 1 warning
```

### Backend full suite

```bash
cd /home/user/axiom/backend
pytest -q
```

Result:

```text
391 passed, 1 warning
```

### Alembic migration state

```bash
cd /home/user/axiom/backend
alembic upgrade head
alembic current
```

Result:

```text
20260717_0037 (head)
```

No W7-U05 migration was created.

### Hostile-refusal seed smoke

```bash
python scripts/w7_u05_seed_plugin_refusal.py
```

Result:

```text
W7_U05_PLUGIN_REFUSAL_SEED_COMPLETE
PLUGIN_REQUEST_ACCEPTED=False
PLUGIN_REFUSAL_REASON_CODE=PLUGIN_CONTRACT_IMPORT_REFUSED
PLUGIN_REFUSAL_AUDIT_COUNT=1
PLUGIN_CAPABILITY_ALLOWLIST=report.export,chart.type,analytics.view
```

### Frontend validation

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
Vitest: 20 files / 64 tests passed
TypeScript: clean
Build: successful
```

---

## 7. Operator evidence pack

Operator evidence command pack is ready at:

```text
docs/evidence/W7-U05_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes exact Windows PowerShell + PostgreSQL commands for:

1. build identity;
2. Alembic head unchanged at `20260717_0037`;
3. no plugin registry / execution audit tables;
4. raw no-dynamic-execution grep;
5. raw §16/§17 containment grep;
6. hostile-plugin refusal script;
7. raw `audit_events` refusal row proof;
8. authenticated plugin-contract surface proof;
9. read/research-only allowlist proof;
10. no-secret/PII marker checks;
11. no dependency / no UI declaration;
12. full regression and Git-Bash local CI.

---

## 8. Deferred / explicitly not implemented

The following remain out of scope and were not implemented:

- dynamic plugin loading;
- third-party plugin runtime;
- plugin code execution;
- `plugin_execution_audit_events` table;
- plugin registry persistence table;
- frontend plugin catalogue UI;
- broker/order/account/live/Gate path from plugins;
- external LLM/API;
- new dependency;
- live broker adapter;
- broker SDK or credentials;
- real order routing;
- real account/position/balance/margin/capital state;
- real P&L;
- Gate opening;
- W7-U06 or later functionality.

---

## 9. DA disposition

W7-U05 is implemented and locally validated by the Development Authority.

This is **not** an approval. DA does not self-approve W7-U05, self-authorize W7-U06, open the Governance Gate, add live broker connectivity, add execution/order/account paths, add dynamic plugin execution, or begin any W7-U06+ feature.

Next required step: operator runs `docs/evidence/W7-U05_OPERATOR_EVIDENCE_COMMANDS.md` on the target Windows/PostgreSQL environment and submits the transcript to ITRGA for independent review.

---

**End of DELIVERY_REPORT_W7-U05.md**
