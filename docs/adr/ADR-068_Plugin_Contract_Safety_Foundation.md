# ADR-068 — Plugin Contract Safety Foundation

| Field | Value |
|---|---|
| Status | Implemented by DA; pending operator evidence / ITRGA review |
| Date | 2026-07-18 |
| Unit | W7-U05 — Plugin Contract Safety Foundation |
| Platform candidate | v0.59.0 |
| Alembic head | `20260717_0037` unchanged |

## Context

W7-U05 authorizes plugin **contracts and refusal only**. Dynamic or third-party plugin code execution is explicitly hard-gated by R7-1 and is not authorized in this unit. The purpose is to publish safe extension contract descriptors while proving that hostile plugin requests are refused and audited.

## Decision

AXIOM adds a code-defined plugin contract safety package:

```text
backend/app/institutional_platform/plugins/
```

The package defines:

- read/research-only capability allowlist;
- built-in reference contract descriptors;
- request/decision metadata types;
- safety/refusal service that checks contract requests without running plugin code;
- audit-backed refusal seam using the existing `audit_events` table.

Allowed capabilities are:

```text
report.export
chart.type
analytics.view
```

AXIOM adds an authenticated read-only API endpoint:

```text
GET /api/v1/institutional-platform/plugin-contracts
```

The endpoint publishes contract descriptors and capability allowlist. It does not execute plugin code.

No plugin registry table is persisted. No migration is added. No frontend plugin catalogue UI is added. No dependency is added. No `plugin_execution_audit_events` table is added.

## Consequences

- Operators and future units can see the safe extension contract vocabulary.
- Hostile contract requests can be refused and audited through existing governance audit events.
- R7-1 remains intact: no dynamic/third-party plugin runtime exists.
- W7-U06 remains unauthorized until ITRGA approves W7-U05.

## Required proof

Operator evidence must prove:

- no dynamic plugin code path exists by raw grep;
- no broker/order/account/live/Gate reach exists in the plugin package by raw grep;
- hostile plugin request is refused and audited with a raw `audit_events` query;
- capability allowlist is read/research-only;
- no `plugin_execution_audit_events` table exists;
- plugin-contract surface requires authentication;
- no secret/PII markers appear in the contract surface;
- no dependency or migration was added;
- Gate remains CLOSED and broker suite remains green.

---

**End of ADR-068**
