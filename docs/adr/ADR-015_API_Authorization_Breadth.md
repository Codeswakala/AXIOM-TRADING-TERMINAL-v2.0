# ADR-015 — API Authorization Breadth and Authenticated Status WebSocket

| Field | Value |
|-------|-------|
| ID | ADR-015 |
| Title | Operator-authenticated operational APIs and status WebSocket |
| Date | 2026-07-12 |
| Status | Accepted |
| Deciders | Development Authority under Build Order W1-U01 |
| Domain | Security / API Architecture / Core Platform |

---

## Context

Wave 0 intentionally exposed several operational endpoints for foundation verification. W1-U01 requires the Core Platform to harden API seams before feature growth, closing TD-015 (many public endpoints) and TD-003 (`/ws/status` unauthenticated).

The canonical architecture requires least privilege, centralized authorization, thin controllers, and traceable operator access to operational platform state.

## Decision

1. Keep public access only for liveness/readiness/discovery and credential-establishment endpoints:
   - `/health`, `/ready`, `/api`
   - `/auth/login`
   - `/auth/refresh` using refresh-token credential semantics.
2. Require Bearer access-token authentication for operational REST endpoints:
   - operator identity, system info, persistence, audit, ingestion, and live market APIs.
3. Require WebSocket authentication for `/ws/status` using the same short-lived ticket mechanism as `/ws/market`.
4. Preserve the W0-U08 default that long-lived access JWTs are not placed in WebSocket query strings.
5. Document endpoint classification in `docs/api/ENDPOINT_AUTH_INVENTORY_W1-U01.md`.

## Alternatives Considered

| Option | Outcome | Rationale |
|--------|---------|-----------|
| Keep Wave-0 public operational endpoints | Rejected | Propagates TD-015 into Wave 1 and weakens least-privilege posture. |
| Auth every endpoint including `/health` and `/ready` | Rejected for now | Common deployment probes need unauthenticated liveness/readiness; payload remains non-secret. |
| Remove `/ws/status` | Deferred | The operator dashboard still uses it as a scoped status channel; authentication closes the security concern without feature removal. |
| Introduce full RBAC now | Out of scope | Build Order excludes RBAC expansion; existing coarse roles remain. |

## Consequences

- Frontend data calls must attach Bearer tokens for system info and persistence candle reads.
- Dashboard status socket must request a WS ticket before connecting.
- Existing Wave-0 behavior remains available after login.
- External unauthenticated scripts that called operational endpoints must be updated to login first.
- Test coverage now asserts 401/200 authorization behavior.

## Compliance

- Supports `05_SYSTEM_ARCHITECTURE.md` v2.0 §75–77 least privilege and centralized authorization.
- Supports W1-U01 Component B.
- Closes TD-003 and TD-015 pending ITRGA approval.

---

**End ADR-015**
