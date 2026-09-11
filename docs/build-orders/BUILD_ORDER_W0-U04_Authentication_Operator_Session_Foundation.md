# AXIOM Build Order
## W0-U04 — Authentication & Operator Session Foundation

**Build Order ID:** W0-U04  
**Wave:** 0 — Foundation  
**Unit:** 04  
**Version:** 1.0  
**Status:** ISSUED  
**Authority:** Independent Technical Review & Governance Authority (ITRGA)  
**Date Issued:** 2026-07-10  
**Authorized By:** ITRGA (following successful approval of W0-U03)  
**Classification:** Official Build Order  
**Governing Documents:**  
- 09_ITRGA_REASONING_FRAMEWORK.md  
- ITRGA_Enhanced_Investigation_Standards_v1.1.md  
- 03_AXIOM_SPEC_v1.1.md  
- 04_PROJECT_ROADMAP.md  
- GOVERNANCE_HIERARCHY.md  
- AXIOM_SYSTEM_ARCHITECTURE_MERGED.md (v1.1)  
- 02_DESIGN_PHILOSOPHY.md  
- 08_UI_UX_SPEC.md  
- 00_VISION_AND_PRINCIPLES.md  

---

## 1. Purpose

This Build Order authorizes the Development Authority to implement the foundational authentication and operator session management for AXIOM.

This unit introduces secure operator identity, token-based authentication, protected routes, and basic session handling — a critical foundation before any production-like operator workflows.

---

## 2. Objectives

1. Implement JWT-based authentication (access + refresh tokens) using industry-standard practices.
2. Create a minimal Operator / User model and repository.
3. Provide secure login, token refresh, and logout endpoints.
4. Implement dependency-based route protection (current operator context).
5. Add basic password hashing and credential handling.
6. Integrate authentication into the existing health/ready and ingestion APIs (optional protected versions).
7. Provide a minimal frontend authentication shell (login page + token storage + protected route guard).
8. Expand observability and audit logging for auth events.
9. Create comprehensive tests (unit + integration).
10. Update EKMS with rigorous ADRs and apply the full ITRGA Reasoning Framework in the Delivery Report.

---

## 3. Scope

### In Scope
- JWT token issuance, validation, and refresh (using `python-jose` or `authlib` + `passlib`).
- Password hashing (bcrypt).
- Basic Operator model (`id`, `username`, `hashed_password`, `role`, `created_at`).
- Repository for operators.
- FastAPI dependencies: `get_current_operator`, `require_role`.
- Protected API routes (example: protected ingestion stats or a new `/api/v1/operator/me`).
- Frontend:
  - Simple login form (institutional dark theme)
  - Token storage (localStorage or memory)
  - Auth context / provider
  - Route guard for dashboard
- Basic audit events for login/logout.
- Environment configuration for JWT secret (never hard-coded).
- Unit + integration tests (including token lifecycle).

### Explicitly Out of Scope
- Full RBAC or fine-grained permissions.
- OAuth2 / external identity providers (future).
- Multi-factor authentication.
- Session revocation lists / token blacklisting (beyond basic refresh).
- Password reset flows.
- Production-grade rate limiting on auth endpoints (basic protection only).
- Persistent "remember me" beyond refresh tokens.

---

## 4. Deliverables

1. **Backend Authentication Layer**
   - `app/auth/` module (jwt, hashing, dependencies)
   - `Operator` model + repository
   - Auth service (login, refresh, logout)
   - Protected dependency injection

2. **API Endpoints**
   - `POST /api/v1/auth/login`
   - `POST /api/v1/auth/refresh`
   - `POST /api/v1/auth/logout`
   - `GET  /api/v1/operator/me` (protected)
   - Example: make one existing endpoint (e.g. ingestion stats) optionally protected

3. **Frontend Authentication**
   - Login page/component (institutional styling)
   - Auth context/provider
   - Protected route wrapper
   - Token attachment to API calls (interceptor)

4. **Security & Configuration**
   - JWT secret via environment (with strong default warning)
   - Token expiration configuration
   - Secure cookie options where applicable

5. **Testing**
   - Unit tests for JWT, hashing, auth service
   - Integration tests for login → protected route flow
   - Test fixtures for operators

6. **Engineering Knowledge**
   - ADR-007: JWT Authentication Strategy
   - ADR-008: Operator Identity & Session Management
   - Updated Technical Debt Register and Decision Log

7. **Documentation**
   - Auth setup guide
   - Updated `PROJECT_STATE.md`
   - Example protected usage

8. **Delivery Report**
   - `DELIVERY_REPORT_W0-U04.md` that rigorously applies **09_ITRGA_REASONING_FRAMEWORK.md**

---

## 5. Success Criteria / Definition of Done

- [ ] Login with valid credentials returns access + refresh tokens
- [ ] Protected routes return 401/403 when unauthenticated
- [ ] Token refresh works and issues new tokens
- [ ] Frontend can login and access protected UI sections
- [ ] All new tests pass
- [ ] At least two new ADRs with deep rationale
- [ ] Delivery Report follows full ITRGA Reasoning Framework
- [ ] JWT secret is never committed and is configurable
- [ ] Scope strictly respected
- [ ] Implementation is independently reviewable

---

## 6. Constraints & Standards

- Must follow **09_ITRGA_REASONING_FRAMEWORK.md** in the Delivery Report.
- Use established patterns from W0-U01–U03 (Clean Architecture, repositories, observability).
- No hard-coded secrets.
- Future-compatible with institutional identity providers.
- Audit events for security-relevant actions.

---

## 7. Combined Frontend + Backend Execution (Operator Request)

**Goal:** Run both frontend and backend from a **single terminal** using uvicorn.

### Recommended Production-Style Approach (Single uvicorn process)

1. Build the frontend once:
   ```bash
   cd frontend
   npm run build
   ```

2. In FastAPI, mount the built frontend as static files:

   In `backend/app/main.py` (or a new `app/api/static.py`):

   ```python
   from fastapi.staticfiles import StaticFiles
   from fastapi.responses import FileResponse
   import os

   # ... existing app setup ...

   # Serve built React app
   frontend_dist = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist")
   if os.path.exists(frontend_dist):
       app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

       @app.get("/{full_path:path}")
       async def serve_frontend(full_path: str):
           index_path = os.path.join(frontend_dist, "index.html")
           if os.path.exists(index_path):
               return FileResponse(index_path)
           return {"detail": "Frontend not built"}
   ```

3. Run with a single command:
   ```bash
   cd backend
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

   Access everything at `http://localhost:8000`

   - API routes continue to work under `/api/v1/...`
   - Frontend SPA served for all other paths (SPA fallback)

### Alternative (if you prefer separate processes but one terminal)

Use `concurrently`:

```bash
cd backend
npm install -g concurrently   # or npx
concurrently "uvicorn app.main:app --port 8000 --reload" "cd ../frontend && npm run dev"
```

However, the **recommended single-process approach** above (FastAPI + static mount) is cleaner for development and matches many institutional full-stack patterns.

**Action for Development Authority in this unit (optional but encouraged):**
- Make the single-uvicorn approach the default documented way to run the platform.
- Update `README.md` and `docs/` with the exact commands.
- Add a `scripts/run_dev.sh` that builds frontend (if needed) and starts uvicorn.

---

## 8. References & Dependencies

- W0-U01, W0-U02, W0-U03 (all approved)
- 09_ITRGA_REASONING_FRAMEWORK.md (mandatory)
- All prior governing documents

---

## 9. Authorization & Signature

**This Build Order is hereby issued by the Independent Technical Review & Governance Authority.**

**Issued By:** ITRGA  
**Date:** 2026-07-10  

**Next Action Required from Development Authority:**
1. Acknowledge receipt.
2. Implement while applying the full ITRGA Reasoning Framework.
3. Consider implementing the single-uvicorn run pattern as part of this unit's deliverables.
4. Submit complete Delivery Report + evidence for review.

---

**End of Build Order W0-U04**

*ITRGA — Engineering truth through disciplined investigation.*