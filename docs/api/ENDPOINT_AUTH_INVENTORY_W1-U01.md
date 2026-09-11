# Endpoint Authorization Inventory — W1-U01

| Item | Value |
|------|-------|
| Unit | W1-U01 Core Platform: Service Architecture & API Hardening |
| Status | Implemented by DA; pending ITRGA review |
| Date | 2026-07-12 |
| Authority | BUILD_ORDER_W1-U01 Component B |

---

## 1. Authorization policy

W1-U01 narrows the public surface and treats operational APIs as authenticated operator capabilities.

Public endpoints are limited to non-sensitive liveness/readiness/discovery and credential bootstrap paths needed to establish an operator session. Operational data, audit, ingestion, market-control, and WebSocket status/market channels require authentication.

Authentication mechanism:

- REST: `Authorization: Bearer <access_token>` via the shared `CurrentOperatorDep` dependency.
- WebSocket: short-lived one-time ticket from `POST /api/v1/auth/ws-ticket`; legacy query JWT remains disabled by default unless explicitly configured.

---

## 2. Public endpoints

| Method | Path | Auth | Rationale |
|--------|------|------|-----------|
| GET | `/health` and `/api/v1/health` | Public | Liveness only; no sensitive data. |
| GET | `/ready` and `/api/v1/ready` | Public | Readiness probe; contains subsystem statuses but no secrets/operator data. |
| GET | `/api` | Public | Minimal API discovery root. |
| POST | `/auth/login` and `/api/v1/auth/login` | Public | Required to establish operator session. |
| POST | `/auth/refresh` and `/api/v1/auth/refresh` | Public with refresh credential | Refresh token itself is the credential; rotation/reuse detection applies. |

Note: the API router is still mounted both at root and `/api/v1` for Wave-0 compatibility. The auth policy applies to both mounts.

---

## 3. Authenticated REST endpoints

| Method | Path family | Auth | Rationale |
|--------|-------------|------|-----------|
| POST | `/auth/logout` | Bearer | Session revocation is operator-specific. |
| POST | `/auth/ws-ticket` | Bearer | Issues a short-lived WebSocket credential. |
| GET | `/operator/me` | Bearer | Operator identity. |
| GET | `/system/info` | Bearer | Operator terminal platform metadata. |
| GET | `/metrics` | Bearer | Read-only operational telemetry; no secrets. |
| POST/GET | `/persistence/*` | Bearer | Operational data and audit access. |
| POST/GET | `/ingestion/*` | Bearer | Historical data mutation and ingestion metadata. |
| GET/POST | `/market/live/*` | Bearer | Live-feed operational control/status. |

Equivalent `/api/v1/...` paths have the same authorization status.

---

## 4. Authenticated WebSocket endpoints

| Path | Auth | Rationale |
|------|------|-----------|
| `/ws/status` | Short-lived ticket or authorized Bearer-capable client | Closes TD-003; status channel is no longer unauthenticated. Payload remains narrowly scoped and non-sensitive. |
| `/ws/market` | Short-lived ticket preferred; legacy query JWT disabled by default | Preserves W0-U08 ticket hardening and live market stream authentication. |

---

## 5. Regression evidence targets

W1-U01 backend tests assert:

- public probes remain public;
- operational GET endpoints return `401` without Bearer;
- operational GET endpoints accept Bearer;
- ingestion writes require Bearer;
- `/ws/status` rejects unauthenticated clients and accepts a short-lived ticket;
- `/ws/market` ticket behavior remains intact.

---

**End of inventory**
