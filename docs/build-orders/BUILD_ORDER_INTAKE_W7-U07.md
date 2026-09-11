# BUILD ORDER INTAKE — W7-U07

## Enterprise Scalability & Multi-User Readiness Hardening

| Field | Value |
|---|---|
| Build Order | `docs/build-orders/BUILD_ORDER_W7-U07.md` |
| Prerequisite verdict | `docs/build-orders/ITRGA_VERDICT_W7-U06_FINAL.md` — W7-U06 APPROVED |
| Platform of record before unit | v0.60.0 |
| Target candidate version | v0.61.0 |
| Starting Alembic head | `20260717_0037` |
| Target Alembic head | `20260717_0037` unchanged — no new table |
| Governance Gate | CLOSED |
| DA decision | Accepted for implementation under one-unit scope |

## Authorized scope

Implement enterprise scalability and multi-user readiness hardening only:

- default-deny RBAC re-proof;
- permission vocabulary re-check for no Gate/execution/order/account capabilities;
- valid-token two-operator isolation across at least two institutional resources;
- authorize-before-validate 403 re-proof;
- admin/admin123 production-framing rejection proof;
- abuse/rate guard disposition;
- observability/log redaction proof;
- representative audit no-orphan preservation proof.

## Explicit implementation choices

- No rate-limit dependency/storage is added in W7-U07.
- Abuse/rate guard is formally deferred under `TD-W7-U07-RATE-GUARD`.
- `admin/admin123` is not deferred; the existing bootstrap guard rejects the historical default when `AXIOM_ALLOW_INSECURE_DEV=false`, and W7-U07 adds explicit proof.
- No persistence table is added; Alembic head remains `20260717_0037`.
- No UI/config surface is added; browser evidence is not applicable.

## Non-scope / prohibited

Not authorized and not implemented:

- execution/order/broker/account/Gate capability;
- role or permission that opens the Gate;
- rate-limit dependency or storage without spike;
- production acceptance of historical default bootstrap password;
- observability/log secret leakage;
- audit weakening;
- frontend UI/config surface;
- W7-U08+ functionality.

---

**End of BUILD_ORDER_INTAKE_W7-U07**
