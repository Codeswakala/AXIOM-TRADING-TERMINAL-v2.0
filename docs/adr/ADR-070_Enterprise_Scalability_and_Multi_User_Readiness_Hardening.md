# ADR-070 — Enterprise Scalability and Multi-User Readiness Hardening

| Field | Value |
|---|---|
| Status | Implemented by DA; pending operator evidence / ITRGA review |
| Date | 2026-07-19 |
| Unit | W7-U07 — Enterprise Scalability & Multi-User Readiness Hardening |
| Platform candidate | v0.61.0 |
| Alembic head | `20260717_0037` unchanged |

## Context

Before Wave-7 closeout, AXIOM must re-prove that the larger institutional platform remains safe under multi-user and enterprise-readiness pressure. W7-U07 is a hardening/proof unit, not a feature unit.

Two carried items must be disposed:

- W7-U04 abuse/rate guard deferred item;
- R7-6 `admin/admin123` production-framing concern.

## Decision

AXIOM adds a small code-defined readiness disposition module:

```text
backend/app/institutional_platform/readiness.py
```

It records:

```text
admin/admin123 -> rejected_when_insecure_dev_off
abuse/rate guard -> formally_deferred under TD-W7-U07-RATE-GUARD
```

No rate-limit dependency or storage is added in W7-U07. A future rate guard requires a dependency/storage spike and a dedicated Build Order.

The existing bootstrap guard is explicitly tested: bootstrap admin creation refuses the historical `admin123` default when `AXIOM_ALLOW_INSECURE_DEV=false`.

No table is added. No migration is added. No frontend UI/config surface is added.

## Consequences

- Default-deny RBAC and permission-vocabulary safety are re-proven.
- Two-operator isolation is re-proven across workspace preferences and research collections.
- Authorize-before-validate is re-proven on cross-operator research collection member mutation.
- Observability/log redaction and representative audit no-orphan integrity are re-proven.
- Abuse/rate guard remains a named standing technical debt rather than a silent omission.
- W7-U08 remains unauthorized until ITRGA approves W7-U07.

## Required proof

Operator evidence must prove:

- unprivileged operator receives `403` on default-deny institutional endpoints;
- permission vocabulary contains no Gate/execution/order/account capability;
- valid-token B cannot read/list/mutate A's resources across at least two resource types;
- cross-operator mutation with empty body returns `403`;
- `admin/admin123` is rejected when insecure-dev is off;
- abuse/rate guard is explicitly deferred under `TD-W7-U07-RATE-GUARD`;
- observability/log output is redacted and contains no secret/PII markers;
- representative audit no-orphan join remains `0`;
- no new table, migration, dependency, UI, execution path, or Gate mutation is present.

---

**End of ADR-070**
