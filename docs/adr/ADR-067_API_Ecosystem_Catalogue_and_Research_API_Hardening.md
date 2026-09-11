# ADR-067 — API Ecosystem Catalogue and Versioned Research API Hardening

| Field | Value |
|---|---|
| Status | Implemented by DA; pending operator evidence / ITRGA review |
| Date | 2026-07-18 |
| Unit | W7-U04 — API Ecosystem Catalogue & Versioned Research API Hardening |
| Platform candidate | v0.58.0 |
| Alembic head | `20260717_0037` unchanged |

## Context

W7-U04 authorizes an authenticated, documented, versioned catalogue for existing research and institutional API routes. The unit extends the W7-U01 institutional route-inventory foundation to the broader research API surface while preserving the constitutional bright line: no execution/order/account/broker/open-gate endpoint may be introduced or documented.

## Decision

AXIOM adds a generated API catalogue endpoint:

```text
GET /api/v1/institutional-platform/api-catalogue
```

The catalogue is generated from registered FastAPI route metadata at request time and includes route path, methods, permission descriptor, API version, description, tags, auth requirement, operator-scoped flag, and mutation flag.

No catalogue table is persisted. Therefore no migration is added and Alembic head remains:

```text
20260717_0037
```

No frontend catalogue UI is added. Therefore W7-U04 is API-only and browser evidence is not applicable.

No rate-limit dependency or storage is added. The catalogue response explicitly declares abuse/rate guard status as deferred for this catalogue unit while preserving existing auth, role, and operator scoping.

## Consequences

- Existing research/institutional API routes are discoverable through an authenticated catalogue.
- The catalogue asserts `actuation_surface_present:false` and `governance_gate_capability_present:false`.
- R7-2 no-execution-surface proof is supported by catalogue response plus 404/405 probes for forbidden route names.
- No new persistence or dependency risk is introduced.
- W7-U05 remains unauthorized until ITRGA approves W7-U04.

## Required proof

Operator evidence must prove:

- the catalogue endpoint is authenticated and returns versioned research routes;
- the catalogue response has `actuation_surface_present:false` and `governance_gate_capability_present:false`;
- exact forbidden endpoint probes return `404/405`;
- catalogued route representative set is auth-gated;
- operator scoping remains enforced using valid two-operator tokens;
- cross-operator mutation still returns `403` before body validation;
- no secret/PII markers appear in catalogue/API responses;
- no migration/table was added and `alembic current` remains `20260717_0037`;
- rate/abuse guard is declared deferred;
- CI exits 0 and Gate remains CLOSED.

---

**End of ADR-067**
