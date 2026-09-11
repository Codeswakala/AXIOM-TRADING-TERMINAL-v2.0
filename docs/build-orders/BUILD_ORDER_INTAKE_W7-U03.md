# BUILD ORDER INTAKE — W7-U03

## Research Management Collections & Tags

| Field | Value |
|---|---|
| Build Order | `docs/build-orders/BUILD_ORDER_W7-U03.md` |
| Prerequisite verdict | `docs/build-orders/ITRGA_VERDICT_W7-U02_FINAL.md` — W7-U02 APPROVED |
| Platform of record before unit | v0.56.0 |
| Target candidate version | v0.57.0 |
| Starting Alembic head | `20260717_0034` |
| Target Alembic head | `20260717_0037` |
| Governance Gate | CLOSED |
| DA decision | Accepted for implementation under one-unit scope |

## Authorized scope

Implement research management metadata only:

- `research_collections` migration `20260717_0035`;
- `research_collection_members` migration `20260717_0036`;
- `research_tags` migration `20260717_0037`;
- authenticated/operator-scoped API for create/list/detail/delete collection metadata, member add/remove, and tag add/remove;
- authorize-before-validate for cross-operator mutation endpoints;
- protected `/research-management` frontend UI;
- create/delete audit rows;
- tests and operator evidence pack.

## Non-scope / prohibited

Not authorized and not implemented:

- mutation of source artifacts or source audits;
- source-artifact content copy/materialization;
- source-artifact cascading FK;
- execution/order/broker/account/Gate field or control;
- live broker, order routing, real account state, real P&L;
- plugin execution;
- external LLM/API;
- dependency changes;
- W7-U04+ functionality.

## Binding proof obligations

- R7-5 source before/after identity proof;
- R7-3 two real operators with valid tokens and raw 0 leakage;
- OBS-W7U02-AUTHZ-ORDER: cross-operator mutation with empty body returns `403`;
- R7-7 / GR7-8 no secrets/PII;
- GR7-9 persistence capture for all three tables;
- GR7-10 browser proof;
- GR7-1 Gate CLOSED.

---

**End of BUILD_ORDER_INTAKE_W7-U03**
