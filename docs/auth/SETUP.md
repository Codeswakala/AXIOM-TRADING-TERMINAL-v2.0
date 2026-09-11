# Authentication Setup Guide

| Item | Value |
|------|-------|
| Current posture | W1-U01, built on W0-U08 hardening |
| Auth model | JWT access + server-side refresh rotation + WS tickets |

---

## 1. Security defaults

AXIOM no longer ships a silent usable `admin/admin123` bootstrap path.

Required for normal local operation:

```env
AXIOM_JWT_SECRET_KEY=replace-with-a-long-random-secret-at-least-32-chars
AXIOM_ALLOW_INSECURE_DEV=false
```

Bootstrap admin is disabled by default. Enable it only with explicit credentials:

```env
AXIOM_BOOTSTRAP_ADMIN_ENABLED=true
AXIOM_BOOTSTRAP_ADMIN_USERNAME=admin
AXIOM_BOOTSTRAP_ADMIN_PASSWORD=Choose-A-Strong-Local-Password-9
```

The historical `admin123` password is blocked unless `AXIOM_ALLOW_INSECURE_DEV=true` in isolated local/test use.

---

## 2. API

| Method | Path | Auth |
|--------|------|------|
| POST | `/api/v1/auth/login` | Public |
| POST | `/api/v1/auth/refresh` | Refresh token credential; rotates token |
| POST | `/api/v1/auth/logout` | Bearer |
| POST | `/api/v1/auth/ws-ticket` | Bearer |
| GET | `/api/v1/operator/me` | Bearer |

### Login example

```bash
curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"<configured-bootstrap-password>"}'
```

Use `tokens.access_token` as:

```bash
curl -s http://localhost:8000/api/v1/operator/me \
  -H "Authorization: Bearer <access_token>"
```

### Refresh rotation

```bash
curl -s -X POST http://localhost:8000/api/v1/auth/refresh \
  -H 'Content-Type: application/json' \
  -d '{"refresh_token":"<refresh_token>"}'
```

The old refresh token is revoked when a new one is issued. Reuse of an old refresh token returns `401` and revokes the family.

### WebSocket tickets

```bash
curl -s -X POST http://localhost:8000/api/v1/auth/ws-ticket \
  -H "Authorization: Bearer <access_token>"
```

Connect with the short-lived one-time ticket:

```text
ws://localhost:8000/ws/market?ticket=<ticket>
ws://localhost:8000/ws/status?ticket=<ticket>
```

Do not put long-lived access JWTs in WebSocket query strings.

---

## 3. Frontend

1. Open `/login`.
2. Sign in with configured operator credentials.
3. Dashboard, Live Market, and Chart Workspace routes require authentication.
4. Sign out clears the local browser session and revokes server-side refresh tokens for the operator.

---

## 4. Migrations

```bash
alembic upgrade head
```

Current auth migrations include:

- `20260710_0003` — operators
- `20260711_0004` — refresh tokens and WS tickets

---

**End of auth setup**
