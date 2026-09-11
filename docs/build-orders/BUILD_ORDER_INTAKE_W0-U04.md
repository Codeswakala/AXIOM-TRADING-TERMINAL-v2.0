# Build Order Intake — W0-U04

| Item | Value |
|------|--------|
| Build Order | W0-U04 Authentication & Operator Session Foundation |
| Prerequisite | W0-U03 APPROVED WITH OBSERVATIONS (ITRR-W0-U03-001) |
| Status | ACCEPTED |
| Date | 2026-07-10 |

## Hypothesis
JWT access+refresh with bcrypt-hashed operators, FastAPI dependencies, and a minimal React login/guard will establish secure operator identity without full RBAC/OAuth/MFA.

## Also from ITRR-W0-U03
- Fix brittle `test_settings_defaults` (do not hard-assert sqlite when override present)
- Close/update TD-001b given Operator PG verification

## Alternatives
| Option | Decision |
|--------|----------|
| JWT access+refresh + bcrypt | Selected |
| Session cookies only | Deferred |
| OAuth/OIDC now | Out of scope |
| Full RBAC | Out of scope |

## Proceed
Architecture: auth module → Operator model/repo → AuthService → routes → FE AuthProvider + Login + guard → static mount for single uvicorn.
