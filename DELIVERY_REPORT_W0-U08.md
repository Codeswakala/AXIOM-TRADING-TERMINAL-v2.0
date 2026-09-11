# Delivery Report — W0-U08

| Field | Value |
|-------|--------|
| Build Order | **W0-U08** Wave 0 Closeout & Hardening |
| Platform | **0.8.0** |
| Date | 2026-07-11 |
| Author | Development Authority |
| Status | **Completed — submitted for ITRGA review** |
| Approval | **Not self-approved** |
| Prior | W0-U07 **APPROVED WITH OBSERVATIONS** (final) |

---

## 1. Executive Summary

W0-U08 is a **debt-clearing unit** (no new product features). It hardens Wave 0 so Wave 1 does not inherit insecure defaults, dual schema authority, WS JWT leakage, or missing Tier-6/7 governance instruments.

### Components delivered

| Component | Status |
|-----------|--------|
| **A Security** | JWT enforced; bootstrap not silent; refresh rotation + reuse revoke; WS short-lived tickets |
| **B Data integrity** | `AUTO_CREATE_SCHEMA` default false / prod forbidden; seed `source=seed:synthetic` + UI banner |
| **C Evidence** | Operator checklist for remaining U07 screenshots + security demos |
| **D Governance docs** | Tier-6 + Tier-7 instruments authored; debt register consolidated; route `/charts` |
| **E CI / compose** | `docker-compose.yml`, `backend/Dockerfile`, `.github/workflows/ci.yml` |
| **F Verification** | Backend **63 passed**; frontend suite + build |

---

## 2. Hypothesis

Hardening security, schema authority, governance docs, and CI without changing approved product behavior will close Wave-0 residuals that would otherwise propagate into Wave 1.

### Counters

| Counter | Result |
|---------|--------|
| Hardening would break existing tests | **Falsified** — 63 backend tests green |
| WS would still require access JWT in query | **Falsified** — ticket path default; query JWT off |
| Production could still create_all | **Falsified** — validation forbids |

---

## 3. Security changes (Component A)

1. **JWT secret:** missing/weak secrets raise `RuntimeError` unless `AXIOM_ALLOW_INSECURE_DEV=true` in development/testing; production always enforces.  
2. **Bootstrap:** disabled by default; requires explicit username/password; blocks historical `admin123` unless insecure-dev allow.  
3. **Refresh rotation:** server-side `refresh_tokens` table; rotate on refresh; reuse → revoke family.  
4. **WS tickets:** `POST /auth/ws-ticket`; `/ws/market?ticket=…`; `AXIOM_WS_ALLOW_QUERY_JWT=false` by default.  
5. Migration **`20260711_0004`**: `refresh_tokens`, `ws_tickets`.

---

## 4. Data integrity (Component B)

- Default `database_auto_create_schema=false`  
- Production validation forbids auto-create  
- Seed remains `seed:synthetic`; chart UI provenance banner (U07-OBS-3)  
- CI runs Alembic against Postgres service  

---

## 5. Governance (Component D)

| Document | Path |
|----------|------|
| Developer reasoning | `docs/governance/08_DEVELOPER_REASONING_FRAMEWORK.md` |
| ITRGA reasoning | `docs/governance/09_ITRGA_REASONING_FRAMEWORK.md` |
| Quality gates | `docs/governance/QUALITY_GATE_SPEC.md` |
| Risk register | `docs/governance/RISK_REGISTER.md` |
| Technical debt | `docs/governance/TECHNICAL_DEBT_REGISTER.md` |
| Amendments | `docs/governance/GOVERNANCE_AMENDMENTS.md` |

Canonical chart route: **`/charts`** (alias `/chart`).

---

## 6. CI / Docker (Component E)

- `docker-compose.yml` — Postgres + API (`alembic upgrade head` then uvicorn)  
- `.github/workflows/ci.yml` — alembic on PG, pytest, vitest, tsc, build  

---

## 7. Evidence classification

| Claim | Class | Level |
|-------|-------|-------|
| 63 backend tests | Verified Fact | II |
| Hardening unit tests (secret, seed, ticket, rotation) | Verified Fact | II |
| Frontend tests/build | Verified Fact | II (run in delivery) |
| Operator security demos / PG transcript / U07 screenshots | **Operator Level-I** | Checklist provided |
| CI green on GitHub | **Unknown until push** | Config present |

### Confidence

| Dimension | Rating |
|-----------|--------|
| Automated hardening | **HIGH** |
| Operator/CI Level-I package | **MODERATE** until Operator attaches |
| Overall | **MODERATE–HIGH** |

---

## 8. Behavior preservation

Product features (ingestion, live, chart, auth login) retained. Defaults are **stricter**; local `.env` / test conftest set explicit allow for demos.

---

## 9. Reproduce (Windows PowerShell)

```powershell
cd backend
Copy-Item .env.example .env
# Edit .env: set AXIOM_JWT_SECRET_KEY (len>=32), optionally ALLOW_INSECURE_DEV for local
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
pytest -q
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

cd ..\frontend
npm install
npm test
npx tsc -b
npm run build
```

Docker:

```powershell
docker compose up --build
```

---

## 10. Readiness statement

> W0-U08 hardening implemented and automated-tested.  
> Submitted for ITRGA review. **Not self-approved.**  
> Upon approval, **Wave 0 may be formally closed** and Wave 1 Build Order issued by ITRGA only.

---

**End of Delivery Report W0-U08**
