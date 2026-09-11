# ADR-069 — Portfolio Research Dashboard and Advanced Reporting

| Field | Value |
|---|---|
| Status | Implemented by DA; pending operator evidence / ITRGA review |
| Date | 2026-07-18 |
| Unit | W7-U06 — Portfolio Research Dashboard / Advanced Reporting |
| Platform candidate | v0.60.0 |
| Alembic head | `20260717_0037` unchanged |

## Context

W7-U06 authorizes a portfolio research dashboard and advanced reporting/export preview over existing governed advisory/simulated artifacts. The central constitutional risk is that a portfolio dashboard may be mistaken for a real brokerage/account view. W7-U06 must therefore avoid real account, position, balance, margin, capital, and real P&L concepts entirely.

## Decision

AXIOM adds a generated, non-persisted portfolio research service and API:

```text
GET /api/v1/institutional-platform/portfolio-research/dashboard
GET /api/v1/institutional-platform/portfolio-research/report
```

The service reads existing current-operator governed artifacts, currently including simulated execution runs, simulated execution experiments, research collections, and research tags. It returns hypothetical research aggregate descriptors with:

- source artifact ids;
- sample counts;
- uncertainty descriptors;
- limitations;
- separate `economic_usefulness` statements;
- full included scope;
- deterministic report hash for the generated report preview.

No report table is persisted. No migration is added. Alembic head remains:

```text
20260717_0037
```

A protected frontend route is added:

```text
/portfolio-research
```

The UI is explicitly research-framed, shows uncertainty and limitations, renders a report/export preview, and exposes no execution/order/account/actuation controls.

## Consequences

- Operators can view research aggregates without real brokerage/account framing.
- The report/export preview is deterministic and generated on request.
- There is no new persistence or source-artifact mutation path.
- W7-U07 remains unauthorized until ITRGA approves W7-U06.

## Required proof

Operator evidence must prove:

- no report table was added and Alembic head remains `20260717_0037`;
- no forbidden real-account/P&L/source columns exist because no W7-U06 table exists;
- API output and UI labels avoid real account/P&L/balance framing;
- report figures carry uncertainty, limitations, sample count, separate economic usefulness, and full source scope;
- valid-token two-operator proof shows B cannot see A's dashboard/report source ids;
- no secret/PII markers appear in report/export payloads;
- served browser screenshots show hypothetical/SIMULATED research framing and no actuation controls;
- Gate remains CLOSED and broker suite remains green.

---

**End of ADR-069**
