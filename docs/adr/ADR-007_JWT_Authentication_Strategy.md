# ADR-007 — JWT Authentication Strategy

| Field | Value |
|-------|--------|
| ID | ADR-007 |
| Title | Access + refresh JWT with bcrypt credentials |
| Date | 2026-07-10 |
| Status | Accepted |
| Domain | Security / Backend |

## Decision
- **Access JWT** (short-lived) + **refresh JWT** (longer-lived), HS256 via `python-jose`
- Passwords hashed with **bcrypt** (`passlib`)
- Secret from `AXIOM_JWT_SECRET_KEY` (never hard-code production secrets)
- Bearer tokens on `Authorization` header
- Logout is audit + client discard (no server-side denylist in this unit)

## Alternatives
| Option | Outcome |
|--------|---------|
| Opaque server sessions only | Deferred |
| OAuth2/OIDC | Out of scope |
| Full token blacklist | Out of scope |

## Consequences
- Stateless access validation scales easily
- Refresh rotation is re-issue only (no reuse detection yet — TD)
- Default secret warned at startup when insecure

## Related
W0-U04, Architecture security JWT note, ADR-008
