# ADR-008 — Operator Identity & Session Management

| Field | Value |
|-------|--------|
| ID | ADR-008 |
| Title | Minimal Operator model with coarse roles |
| Date | 2026-07-10 |
| Status | Accepted |
| Domain | Security / Product |

## Decision
- `operators` table: username, hashed_password, role (`operator`|`admin`), is_active
- Repository + AuthService; bootstrap admin when table empty (dev convenience)
- FastAPI deps: `get_current_operator`, `require_role`
- Frontend: AuthProvider, localStorage tokens, ProtectedRoute, login page
- Example protected API: `GET /ingestion/stats`
- Audit events: login success/fail, refresh, logout, bootstrap

## Alternatives
| Option | Outcome |
|--------|---------|
| Full RBAC matrices now | Out of scope |
| Cookie-only SPA sessions | Possible later; Bearer chosen for API clarity |
| External IdP | Future |

## Consequences
- Institutional login path exists before production workflows
- Bootstrap credentials must be changed for shared environments
- Single uvicorn can serve SPA + API after `npm run build`

## Related
W0-U04, ADR-007, UI_UX dark institutional login
