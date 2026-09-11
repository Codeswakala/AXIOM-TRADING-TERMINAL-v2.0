# BUILD ORDER INTAKE — W7-U08

## Institutional Platform — Closeout, Whole-Wave Proof, Whole-Project Completion & Milestone

| Field | Value |
|---|---|
| Build Order | `docs/build-orders/BUILD_ORDER_W7-U08.md` |
| Prerequisite verdict | `docs/build-orders/ITRGA_VERDICT_W7-U07_FINAL.md` — W7-U07 APPROVED |
| Platform of record before unit | v0.61.0 |
| Target candidate version | v0.62.0 |
| Starting Alembic head | `20260717_0037` |
| Target Alembic head | `20260717_0037` unchanged — closeout/proof unit, no table |
| Governance Gate | CLOSED |
| DA decision | Accepted for implementation under one-unit scope |

## Authorized scope

Implement W7 closeout and whole-project completion proof only:

- whole-wave W7 no-execution / no-Gate-reach tests;
- W7 four-table audit completeness tests/evidence;
- whole-project Gate-CLOSED and broker containment re-proof;
- milestone reconciliation tests across prior project milestones;
- W7 closeout ADR, delivery report, evidence commands, docs/register reconciliation;
- browser evidence checklist across institutional surfaces.

## Explicit implementation choices

- No new product feature is added.
- No table/migration is added; Alembic head remains `20260717_0037`.
- No dependency is added.
- Version advances to candidate `0.62.0` for closeout review.
- Milestone declaration remains reserved for ITRGA final approval.

## Non-scope / prohibited

Not authorized and not implemented:

- execution/order/broker/account/Gate capability;
- dynamic plugin execution;
- new analytics/report persistence;
- new UI feature beyond existing surfaces;
- real-money/live execution path;
- external LLM/API;
- any W7 post-closeout unit.

---

**End of BUILD_ORDER_INTAKE_W7-U08**
