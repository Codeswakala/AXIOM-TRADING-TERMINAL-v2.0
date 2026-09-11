# Delivery Report — W0-U08 Correction (C-1 CRITICAL)

| Field | Value |
|-------|--------|
| Parent unit | **W0-U08** Wave 0 Closeout & Hardening |
| Trigger | `ITRGA_REVIEW_W0-U08.md` — **FAIL** (WS-ticket HTTP 500) |
| Date | 2026-07-12 |
| Author | Development Authority |
| Status | **Correction complete — re-submitted for ITRGA review** |
| Approval | **Not self-approved** |

---

## 1. Verdict acknowledgement

ITRGA **FAIL** is accepted. The operator log was correct: `POST /api/v1/auth/ws-ticket` returned **500** due to `session.refresh()` on audit insert, breaking live WS authentication. The original Delivery Report’s claim that the ticket path worked is **void** (R12). This correction addresses **C-1** as the blocking item.

---

## 2. Root cause (Verified Fact)

```
issue_ws_ticket()
  → AuditRepository.append()
    → BaseRepository.add()
      → session.flush()
      → session.refresh(entity)  # InvalidRequestError / 500
```

Audit append could poison the request transaction and crash the endpoint. Live market (approved U05/U06) regressed because the browser could not obtain a ticket.

---

## 3. Fix applied (C-1 + C-5)

| Change | Purpose |
|--------|---------|
| `AuditRepository.append` uses **SAVEPOINT** (`begin_nested`) | Audit failure cannot roll back business writes |
| **No `refresh()`** on audit insert | Removes the exact 500 path |
| Audit failures **logged + swallowed** | Audit never 500s business endpoints |
| `BaseRepository.add(..., refresh=True)` with best-effort refresh | Other paths also tolerate refresh failures |
| Live candle persist already best-effort | Avoid SQLite contention cascading into request 500s |

### Mandatory regression tests (new)

| Test | Asserts |
|------|---------|
| `test_ws_ticket_endpoint_returns_200_not_500` | `POST /auth/ws-ticket` → **200** (not 500) |
| `test_ws_ticket_then_market_subscribe_no_jwt_in_url` | ticket → `/ws/market?ticket=…` **subscribed**; URL has **no** access JWT |
| `test_audit_append_does_not_break_business_writes` | multiple ticket issues remain 200 |
| `test_refresh_rotation_old_rejected` | rotation still works |

---

## 4. Automated evidence (Level II)

```
67 passed, 1 warning
```

Runtime smoke (this environment):

```
ws-ticket 200 + ticket payload
ws subscribed
OK ticket path healthy
```

Frontend suite: **16 passed** (prior); WS client uses **ticket**, not access JWT in query.

---

## 5. Corrected claim table (replaces void U08 §2 claim)

| Claim | Status |
|-------|--------|
| Query JWT off by default | **True** (`AXIOM_WS_ALLOW_QUERY_JWT=false`) |
| Ticket path issues 200 | **Verified** (tests + smoke) |
| Ticket opens WS without JWT in URL | **Verified** (integration test) |
| Live chart WS healthy in Operator browser | **Operator Level-I required** for final close |

---

## 6. Remaining ITRGA items (not blocking C-1 fix, still owed)

| ID | Item | Owner |
|----|------|--------|
| C-2 | Logged-out `/charts`+`/live` screenshots; refresh-rotation console demo | Operator |
| C-3 | PostgreSQL clean `0001→0004` transcript | Operator / compose |
| C-4 | Confirm Tier-6/7 docs present (authored under `docs/governance/`) + CI run | Docs present; CI on push |
| C-5 | Audit-path audit | **Done** — all appends use robust savepoint path |

---

## 7. Operator re-verify (PowerShell)

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pytest -q
# Expect 67 passed

# Manual:
# 1) Login, POST /api/v1/auth/ws-ticket → 200
# 2) Chart Workspace → Start live feed
# 3) Status must show WS connected (not WS ERROR)
# 4) Capture screenshot of healthy WS + live candles
```

---

## 8. Readiness statement

> **C-1 CRITICAL is fixed and regression-tested.**  
> Re-submitted for ITRGA re-verification.  
> DA does **not** self-approve. Wave 0 remains open until ITRGA converts FAIL → APPROVED.

---

**End of Correction Report**
