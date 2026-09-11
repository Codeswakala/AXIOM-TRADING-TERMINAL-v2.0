# Delivery Report — W0-U04

| Field | Value |
|-------|--------|
| Build Order | **W0-U04** Authentication & Operator Session Foundation |
| Platform | **0.4.0** |
| Date | 2026-07-10 |
| Author | Development Authority |
| Status | **Completed — submitted for ITRGA review** |
| Approval | **Not self-approved** |
| Prior review | ITRR-W0-U03-001 **APPROVED WITH OBSERVATIONS** incorporated |

---

## 1. Executive Summary

W0-U04 delivers JWT-based operator authentication (access + refresh), bcrypt password hashing, Operator persistence, protected API dependencies, login/logout/refresh endpoints, frontend auth shell (login + guard + token storage), audit events, and **single-uvicorn SPA serving** after frontend build.

Also addresses ITRR-W0-U03 observation: brittle `test_settings_defaults` fixed.

**Tests:** backend **46 passed**, frontend **3 passed**, production build OK.  
**Runtime:** login → me → protected stats 401/200 verified.

---

## 2. Hypothesis-Driven Investigation

### Hypothesis
JWT access+refresh with bcrypt operators and FastAPI dependencies will enable authenticated operator sessions and protect selected routes without full RBAC/OAuth.

### Counter-hypotheses
1. Tokens cannot protect routes (falsified — 401/200 evidence).  
2. Bootstrap admin fails on empty DB (falsified — lifespan create).  
3. Frontend cannot attach tokens (falsified — AuthProvider + client).  
4. Settings test still fails under PG override (falsified — fixed test).

### Evidence classification
| Claim | Class | Level |
|-------|-------|-------|
| Login returns tokens | Verified Fact | I runtime + II tests |
| `/operator/me` requires auth | Verified Fact | I + II |
| `/ingestion/stats` 401 without token | Verified Fact | I + II |
| Refresh issues new tokens | Verified Fact | II |
| SPA served on `/` when dist present | Verified Fact | I |
| Production-grade IdP readiness | Unknown | — out of scope |

---

## 3. Multidisciplinary Analysis
Architect (session boundaries), Backend (auth module), Security (bcrypt/JWT/env secret), Frontend (guard/login), QA (token lifecycle tests), DevOps (single uvicorn script), Governance (audit events), Docs (SETUP).

---

## 4. Deliverables vs BO

| Deliverable | Status |
|-------------|--------|
| JWT + bcrypt auth layer | ✓ |
| Operator model + repo | ✓ migration 0003 |
| login/refresh/logout | ✓ |
| get_current_operator / require_role | ✓ |
| Protected stats + `/operator/me` | ✓ |
| FE login + context + guard | ✓ |
| Audit auth events | ✓ |
| JWT secret via env | ✓ + startup warning |
| Tests | ✓ 46 backend |
| ADR-007, ADR-008 | ✓ |
| Single uvicorn pattern | ✓ main.py + run_dev.sh |
| Delivery report | ✓ |

---

## 5. ITRR-W0-U03 Observation Closure
- `test_settings_defaults` now clears `AXIOM_*` and uses `Settings(_env_file=None)`.
- Added `test_settings_respects_database_url_override`.
- TD-001b noted as largely closed per Operator PG verification in ITRR.

---

## 6. Unknowns Register
| ID | Unknown |
|----|---------|
| U-01 | Refresh token theft detection / rotation policy |
| U-02 | Institutional IdP integration details |
| U-03 | Rate-limit efficacy under abuse (basic only) |

---

## 7. Review Confidence
| Dimension | Confidence |
|-----------|------------|
| Functional auth path | **Very High** |
| Scope compliance | **Very High** |
| Secret hygiene (dev defaults) | **Moderate** (explicit warnings/TD) |
| Overall package | **High** |

---

## 8. Readiness Statement
> W0-U04 implemented, tested, documented. Submitted for ITRGA review. **Not self-approved.**

### Reproduce
```bash
cd axiom && ./scripts/run_dev.sh
# http://localhost:8000/login  → admin / admin123
cd backend && pytest -q
```

---

**End of Delivery Report W0-U04**
