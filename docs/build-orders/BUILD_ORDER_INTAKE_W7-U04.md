# BUILD ORDER INTAKE — W7-U04

## API Ecosystem Catalogue & Versioned Research API Hardening

| Field | Value |
|---|---|
| Build Order | `docs/build-orders/BUILD_ORDER_W7-U04.md` |
| Prerequisite verdict | `docs/build-orders/ITRGA_VERDICT_W7-U03_FINAL.md` — W7-U03 APPROVED |
| Platform of record before unit | v0.57.0 |
| Target candidate version | v0.58.0 |
| Starting Alembic head | `20260717_0037` |
| Target Alembic head | `20260717_0037` unchanged — generated catalogue, no persisted table |
| Governance Gate | CLOSED |
| DA decision | Accepted for implementation under one-unit scope |

## Authorized scope

Implement API ecosystem catalogue and research API hardening only:

- authenticated/versioned API catalogue endpoint;
- generated route inventory over existing research/institutional FastAPI routes;
- no persisted catalogue table and no new migration;
- no frontend catalogue UI;
- no new dependency and no rate-limit library;
- no execution/order/account/broker/open-gate route;
- proof of auth, no secret/PII response markers, no execution surface, operator scoping, and Gate CLOSED.

## Explicit implementation choices

- Catalogue generation is runtime/OpenAPI-style introspection over registered FastAPI routes.
- Alembic head remains `20260717_0037`.
- Rate/abuse guard is declared deferred for this catalogue unit; no dependency or rate-limit storage is introduced.
- No browser evidence is required because no UI surface is added.

## Non-scope / prohibited

Not authorized and not implemented:

- persisted API contract table;
- API access audit summary table;
- frontend catalogue/docs surface;
- execution/order/broker/account/open-gate endpoint;
- Gate mutation;
- plugin execution;
- external API/LLM;
- new dependency;
- W7-U05+ functionality.

---

**End of BUILD_ORDER_INTAKE_W7-U04**
