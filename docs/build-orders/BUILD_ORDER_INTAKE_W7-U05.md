# BUILD ORDER INTAKE — W7-U05

## Plugin Contract Safety Foundation

| Field | Value |
|---|---|
| Build Order | `docs/build-orders/BUILD_ORDER_W7-U05.md` |
| Prerequisite verdict | `docs/build-orders/ITRGA_VERDICT_W7-U04_FINAL.md` — W7-U04 APPROVED |
| Platform of record before unit | v0.58.0 |
| Target candidate version | v0.59.0 |
| Starting Alembic head | `20260717_0037` |
| Target Alembic head | `20260717_0037` unchanged — code-defined contract registry, no persisted plugin table |
| Governance Gate | CLOSED |
| DA decision | Accepted for implementation under one-unit scope |

## Authorized scope

Implement plugin contract safety foundation only:

- code-defined published extension contract interfaces under `backend/app/institutional_platform/plugins/`;
- read/research-only capability allowlist;
- built-in reference plugin contract descriptors only;
- refusal seam that rejects non-allowlisted or unsafe contract requests and audits refusal to existing `audit_events`;
- authenticated read-only API to list contracts/capabilities;
- hostile-plugin refusal tests and operator evidence script.

## Explicit implementation choices

- Registry is code-defined constants only.
- No `plugin_contracts` / `plugin_contract_capabilities` table is persisted.
- No migration is added; Alembic head remains `20260717_0037`.
- No frontend plugin catalogue UI is added; W7-U05 is API-only.
- No dynamic or third-party plugin code execution is implemented.
- No `plugin_execution_audit_events` table is added.

## Non-scope / prohibited

Not authorized and not implemented:

- dynamic plugin loading or execution;
- third-party plugin runtime;
- `importlib`, entry-point, `eval`, `exec`, subprocess, or code compilation dispatch;
- `plugin_execution_audit_events` table;
- broker/order/account/live/Gate path from plugins;
- external LLM/API;
- new dependency;
- W7-U06+ functionality.

---

**End of BUILD_ORDER_INTAKE_W7-U05**
