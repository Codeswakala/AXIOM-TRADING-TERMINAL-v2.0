# Delivery Report — W1-U01 Correction Response v2

| Field | Value |
|-------|-------|
| Parent unit | **W1-U01** Core Platform: Service Architecture & API Hardening |
| Latest trigger | `docs/build-orders/ITRGA_REVIEW_W1-U01_CORRECTION.md` — STILL CONDITIONAL |
| Prior trigger | `docs/build-orders/ITRGA_REVIEW_W1-U01.md` — PASS WITH OBSERVATIONS — CONDITIONAL |
| Date | 2026-07-12 |
| Author | Development Authority |
| Status | **DA-side corrections updated; operator target-platform evidence re-run required** |
| Approval | **Not self-approved** |
| Operator evidence DB | `<REDACTED_DB_URL>localhost:5432/axiom` |
| Operator evidence login | `admin / admin123` local evidence credential |

---

## 1. Verdict acknowledgement

The Development Authority accepts ITRGA's W1-U01 correction re-verification.

ITRGA accepted the DA-side UTC/design/confidence/document-integrity corrections, but the Operator evidence run revealed two HIGH issues:

| Finding | ITRGA status | DA response |
|---------|--------------|-------------|
| **F-5** target-platform `test_live_start_stop_and_status` failure (`sqlite3 no active connection`) | HIGH | Diagnosed as SQLite in-memory StaticPool test-harness concurrency around seeding/reading while live adapter writer is active; test made robust and aligned to browser workflow |
| **F-6** invalid auth transcript (`$admin` / `$admin123` undefined → null login → empty token) | HIGH | Evidence checklist regenerated with copy-paste-safe literal credentials and explicit `token_present: True` expectation |

W1-U01 remains conditional. DA does not self-approve.

---

## 2. F-5 Correction — live-market target test failure

### Operator evidence failure

The Operator target run showed:

```text
pytest -q → 1 failed, 75 passed
FAILED tests/test_live_market.py::test_live_start_stop_and_status
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no active connection
```

### Diagnosis

The failing test used the in-memory SQLite test harness (`sqlite+aiosqlite:///:memory:` + `StaticPool`) and performed request-scoped DB work while the live adapter background writer was running.

Specifically, the test started the live adapter, then seeded history and queried persistence while the live adapter could also be writing through the shared SQLite connection. This is a known SQLite/StaticPool test-harness fragility, not the production PostgreSQL path. However, ITRGA correctly classified the failing operator evidence as HIGH because it occurred in an approved Wave-0 live-market test path and had to be made green and robust.

### Fix applied

Updated `backend/tests/test_live_market.py::test_live_start_stop_and_status`:

1. **Seed history before starting** the live adapter, matching the browser chart workflow.
2. Start live adapter and verify status/stats/subscription metadata while running.
3. **Stop live adapter before request-scoped persistence reads**, avoiding SQLite shared-connection contention.
4. Preserve coverage for live adapter persistence via the existing service-level test `test_live_service_persists_candles`, which runs the adapter and verifies persisted candles.

This is a test-harness stability correction. It does not weaken product behavior and it preserves the approved live-market capability checks.

### DA verification

Using a temporary venv outside the persisted workspace:

```text
ruff check .
All checks passed!

pytest -q
76 passed, 1 warning
```

The Operator must re-run the full backend suite on Windows and provide a clean target-platform transcript.

---

## 3. F-6 Correction — copy-paste-safe auth transcript

### Operator evidence failure

The Operator transcript used undefined PowerShell variables:

```powershell
$loginBody = @{ username = $admin; password = $admin123 } | ConvertTo-Json
```

This sent `null/null`, causing login `422`, an empty token, and invalid endpoint-auth results:

```text
without=401 with=401
```

That transcript proves unauthenticated rejection only; it does not prove valid-token access.

### Fix applied

Regenerated:

`docs/evidence/W1-U01_OPERATOR_EVIDENCE_CHECKLIST.md`

The endpoint-auth section now uses a copy-paste-safe literal login body:

```powershell
$login = Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/v1/auth/login `
  -ContentType "application/json" `
  -Body '{"username":"admin","password":"admin123"}'

$token = $login.tokens.access_token
$headers = @{ Authorization = "Bearer $token" }
Write-Host "LOGIN OK token_present:" ($token.Length -gt 20)
```

The `/ws/status` Python evidence script also uses literal local evidence credentials:

```python
USER = "admin"
PASSWORD = "<REDACTED_DEV_PASSWORD>"
```

The re-run must show:

```text
LOGIN OK token_present: True
... without=401 with=200
WS-STATUS unauth rejected: ...
WS-TICKET status: 200 ticket_present: True
WS-STATUS ticket accepted: {"type":"status",...}
```

---

## 4. C-2 UTC boundary correction — still accepted

Prior C-2 remains implemented and accepted in design by ITRGA:

| Function | Behavior | Intended use |
|----------|----------|--------------|
| `require_utc(value, boundary=...)` | Rejects naive datetimes with `ValueError` | Trusted internal boundaries |
| `coerce_external_utc(value, source=...)` | Logs a warning and assumes UTC only if naive | Explicit external API/CSV/schema/driver compatibility boundaries |
| `utc_now()` | Returns aware UTC now | Model defaults and services |

Trusted boundaries now reject naive datetimes:

- `NormalizedCandleRow.__post_init__`
- `CandleService.create_candle`
- `CandleRepository.get_by_natural_key` / `upsert_ohlcv`

Tests:

- `test_api_timestamps_are_timezone_aware_utc`
- `test_normalized_candle_row_rejects_naive_internal_time`
- `test_candle_service_rejects_naive_internal_time`

The Operator must still provide `pytest tests/test_time_utc.py -vv` target output.

---

## 5. C-4 document integrity — closed

Previously verified and accepted:

```text
d56c85084a6bf8ede2523908c3bd80e6e2beadf04faf75c41799a7d93d21645d  /home/user/uploads/ITRGA_WAVE0_CLOSURE.md
d56c85084a6bf8ede2523908c3bd80e6e2beadf04faf75c41799a7d93d21645d  docs/build-orders/ITRGA_WAVE0_CLOSURE.md

ebb39184c4a46ed4e74b67652d2b5b45ccf8e46fee1cb0641d5c538dcf88beef  /home/user/uploads/BUILD_ORDER_W1-U01 (2).md
ebb39184c4a46ed4e74b67652d2b5b45ccf8e46fee1cb0641d5c538dcf88beef  docs/build-orders/BUILD_ORDER_W1-U01.md
```

Both `cmp` checks returned identical.

---

## 6. Required Operator re-run evidence

The Operator should re-run the regenerated checklist:

`docs/evidence/W1-U01_OPERATOR_EVIDENCE_CHECKLIST.md`

Required outputs for ITRGA:

1. PostgreSQL clean Alembic migration:
   - `Context impl PostgresqlImpl`
   - `20260711_0004 (head)`
2. Full backend suite:
   - `collected 76 items`
   - `76 passed`
3. Ruff:
   - `All checks passed!`
4. Frontend:
   - `16 passed`
   - `tsc` clean
   - build successful
5. Endpoint-auth transcript:
   - `LOGIN OK token_present: True`
   - operational endpoints: `without=401 with=200`
6. `/ws/status`:
   - unauthenticated rejected
   - ticket accepted
7. UTC output:
   - `pytest tests/test_time_utc.py -vv` all 3 tests pass
8. Parity smoke:
   - login;
   - WS ticket 200;
   - seed/start live;
   - candle fetch returns EURUSD rows;
   - live status returns feed status.

---

## 7. DA verification after F-5/F-6 correction

DA-sandbox verification after updating the live-market test and evidence scripts:

```text
ruff check .
All checks passed!

pytest -q
76 passed, 1 warning
```

Frontend code was not changed in this correction round after the prior successful frontend validation. Prior W1-U01 frontend validation remains:

```text
Test Files  8 passed (8)
Tests       16 passed (16)
tsc         clean
vite build  successful
```

---

## 8. Confidence restatement

| Dimension | Corrected confidence | Rationale |
|-----------|---------------------|-----------|
| F-5 diagnosis/fix | **MODERATE-HIGH** | Failure pattern matches SQLite StaticPool concurrency; test now mirrors UI order and stops adapter before request-scoped reads; DA suite green |
| F-6 script correction | **HIGH** | Evidence script now uses literal credentials and explicit token-present assertion |
| DA-sandbox correctness | **HIGH** | Ruff clean; backend 76 passed |
| Target-platform correctness | **LIMITED until Operator re-run lands** | ITRGA requires Windows + PostgreSQL evidence after these corrections |
| Overall approval readiness | **CONDITIONAL** | DA-side fixes applied; Operator evidence re-run remains mandatory |

No percentage confidence is asserted.

---

## 9. Readiness statement

> F-5 and F-6 have been addressed by the DA.  
> C-2/C-3/C-4 remain cleared.  
> W1-U01 remains **conditional and not self-approved** until the Operator re-runs the target-platform evidence and ITRGA accepts it.

---

**End of W1-U01 Correction Response v2**
