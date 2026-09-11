# ADR-062 — Execution Research Workspace UI

| Field | Value |
|---|---|
| Status | Accepted for W6-U07 implementation by DA; pending operator evidence / ITRGA review |
| Date | 2026-07-17 |
| Unit | W6-U07 — Execution Research Workspace UI |
| Platform version | 0.53.0 |
| Alembic head | 20260717_0033 unchanged |
| Builds on | W6-U01…W6-U06 simulated execution research artifacts |

---

## Context

W6-U07 is the first Wave-6 UI unit. It must display server-persisted simulated execution research artifacts and remain display-only. Because this is a UI unit, served-browser evidence is mandatory. The page must show `SIMULATED` labels and the not-live disclaimer, and must not include execution/actuation controls.

---

## Decision

Add a protected frontend route:

```text
/execution-research
```

The page fetches existing server-persisted simulated artifacts through read-only APIs:

- simulated execution runs;
- simulated fill events;
- simulated paper ledger entries;
- execution risk research reports;
- execution research experiments;
- simulated execution analytics reports.

The UI is display-only. It does not trigger simulations, create runs/fills/reports, mutate state, or recompute authoritative analytics client-side.

Mandatory disclaimer constant:

```text
SIMULATED execution research only. Not a live order, not financial advice, not real P&L. AXIOM does not act. Governance Gate CLOSED.
```

---

## Prohibited UI behavior

The page must not render controls or affordances for:

- buy;
- sell;
- submit order;
- execute;
- place order;
- go live;
- connect broker;
- broker credentials;
- account selector;
- real balance/margin/capital;
- position management for real positions;
- order ticket.

Only read/refresh display behavior is included.

---

## Testing strategy

Frontend tests assert:

- SIMULATED labels and not-live disclaimer render;
- persisted artifacts render read-only;
- forbidden controls are absent;
- analytics uncertainty/limitations/economic usefulness framing is visible;
- the protected route blocks logged-out access.

Backend suite remains unchanged aside from W6-U07 version identity. No migration is added.

---

## Consequences

### Positive

- Operators can inspect the simulated execution research corpus in one workspace.
- UI remains explicitly simulation-only and advisory/research framed.
- Browser evidence can prove no actuation controls.

### Deliberately not included

- No backend write endpoint.
- No UI-triggered simulation write.
- No table or migration.
- No broker SDK or credentials.
- No live venue endpoint.
- No real order routing.
- No real account/position/balance/margin/capital state.
- No real P&L.
- No Gate opening.
- No W6-U08 closeout work.

---

**End of ADR-062**
