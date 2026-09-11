# AXIOM ITRGA — RE-VERIFICATION: W1-U01 Correction

**Authority:** ITRGA · **Prior verdict:** PASS WITH OBSERVATIONS — CONDITIONAL (approval withheld)
**Inputs:** `DELIVERY_REPORT_W1-U01_CORRECTION.md` + **operator results console** (Windows/PowerShell,
PostgreSQL). **Date:** 2026-07-12 · **Standard:** R1–R21.

---

## VERDICT: **STILL CONDITIONAL — APPROVAL WITHHELD.** DA-side corrections (C-2/C-3/C-4) cleared; **C-1 not only remains unmet but the operator run surfaced a NEW HIGH finding: a target-platform test FAILURE in an approved (Wave-0) path, and an invalid auth transcript.**

Real progress: the UTC fix is exactly right, document integrity is proven, and confidence is honestly
restated. **But I read the operator's own console, not the correction report's framing** — and it shows
the target-platform run went wrong in two ways the correction report does not address (because it was
written before the run). Per the operator's own "no room for error," this cannot approve.

---

## 1. DA-SIDE CORRECTIONS — CLEARED

- **C-2 (UTC boundary) — ACCEPTED (design).** Exactly the fix I required: `require_utc()` **rejects naive
  datetimes at trusted boundaries** (`NormalizedCandleRow.__post_init__`, `CandleService.create_candle`,
  `CandleRepository` natural-key/upsert) while `coerce_external_utc()` **logs-and-assumes** only at
  external boundaries (API/CSV/SQLite). Fail-loud internally, lenient-and-logged externally. +2 tests
  (baseline 74→76). Accept at MODERATE pending the operator's `test_time_utc.py -vv` output.
- **C-4 (doc integrity) — CLOSED.** SHA-256 of the DA's `ITRGA_WAVE0_CLOSURE.md` and `BUILD_ORDER_W1-U01.md`
  copies match the ITRGA originals; `cmp` identical. No migration drift. Good.
- **C-3 (confidence) — CLOSED.** Restated honestly: target-platform correctness = LIMITED, security =
  LIMITED–MODERATE until the transcript lands. Correct posture.

---

## 2. THE OPERATOR RUN — TWO PROBLEMS (C-1 remains unmet + a new HIGH)

The correction report says C-1 is "pending operator run." The operator *did* run it — and the console
shows it **did not pass**. Reading the raw evidence:

### F-5 (HIGH — target-platform test FAILURE; regression in an approved path)
```
pytest -q  →  1 failed, 75 passed
FAILED tests/test_live_market.py::test_live_start_stop_and_status
  sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no active connection
```
- The DA sandbox reported **76 passed**; the operator's **target-platform** run reports **1 failed, 75
  passed.** This is precisely the sandbox-vs-target divergence the mandatory-evidence rule exists to
  catch (the U08 lesson, repeating).
- The failing test is in **`test_live_market.py` — an approved Wave-0 (W0-U05) capability.** Build Order
  §2 **forbids regressing approved behavior.** A live-market test failing after a persistence/service
  refactor is a **regression signal**, not flakiness — it names a specific test and a specific
  **connection-lifecycle error** (`no active connection`), which points at the Application-Services /
  PersistenceService session-management refactor (Components A/D) disturbing the live-market session
  lifecycle.
- **Unexplained + in an approved path = HIGH.** It must be diagnosed and fixed (or proven to be a genuine
  test-harness artifact with evidence), not waved through.

### F-6 (HIGH — the auth transcript is INVALID; the "200 with token" half was never shown)
The endpoint-auth transcript is void because **login never succeeded**:
```
$loginBody = @{ username = $admin; password = $admin123 } | ConvertTo-Json   # $admin/$admin123 UNDEFINED
→ 422  "Input should be a valid string" (username/password = null)
→ "LOGIN OK token_present: False"          # token is EMPTY
→ all 7 endpoints: without=401  with=401   # "with" carried an EMPTY bearer
```
- The script used **undefined PowerShell variables** (`$admin`, `$admin123`) instead of the literal
  strings, so the body sent `null/null`, login 422'd, and every subsequent call used an **empty token.**
- Therefore `with=401` proves nothing about authenticated access. **Build Order C-1(b) required BOTH
  `401 without` AND `200 with` a valid token** — the **`200 with` half was never demonstrated.**
- This is not just a script typo to shrug off: with the endpoints now newly auth-locked, and **no proof
  they accept a valid token**, I cannot rule out that they are **over-locked / broken for authenticated
  operators too.** The transcript must be re-run with a real token showing **200 with**.

### C-1 evidence still owed (unchanged)
- **UTC test output** (`test_time_utc.py -vv`) — not shown.
- **Parity smoke** (login → WS ticket 200 → live feed → candle fetch) — could not execute (login broke),
  and is further undermined by F-5.

---

## 3. WHAT *IS* PROVEN THIS ROUND (credited)

- ✅ **PostgreSQL clean migrate-from-empty:** `docker compose … db (healthy)` → `DROP/CREATE SCHEMA` →
  `alembic upgrade head` on **PostgresqlImpl** → `alembic current = 20260711_0004`. Genuine PG target
  evidence. (Closes the PG-migration portion of C-1.)
- ✅ **ruff clean; frontend 16 passed; tsc/build clean** on target.
- ✅ **Unauthenticated rejection:** all 7 operational endpoints return **401 without a token** — the
  *reject* half of the auth hardening is demonstrated (the *accept* half is not).
- ✅ C-2 / C-3 / C-4 as above.

So Component B is *half*-proven (rejects unauth ✓; accepts valid token ✗-unproven), and the PG migration
and lint/frontend gates are proven.

---

## 4. REQUIRED CORRECTIONS (to convert to APPROVED)

- **C-1a (F-5, HIGH) — Diagnose and resolve the `test_live_start_stop_and_status` failure.** Determine
  whether the Application-Services/PersistenceService refactor broke the live-market session/connection
  lifecycle (the `no active connection` error). Fix it (or prove, with evidence, it is a harness-only
  artifact and make the test robust). Re-run the **full backend suite on the target platform** showing
  **0 failed** — no regression of the approved live-market path.
- **C-1b (F-6, HIGH) — Re-run the endpoint-auth transcript with a REAL login.** Use literal credentials
  (`admin`/`admin123`), obtain a valid token (`token_present: True`), and show **`without=401` AND
  `with=200`** for the operational endpoints, plus **`/ws/status` rejecting unauthenticated / accepting a
  ticket.** The 200-with-token proof is mandatory (guards against over-locking).
- **C-1c — Supply** the `test_time_utc.py -vv` output and the **parity smoke** (login → WS ticket 200 →
  live feed → candle fetch/status) with no regression.
- (C-2/C-3/C-4 accepted; no further action.)

## 5. DISPOSITION
**W1-U01: STILL CONDITIONAL — NOT APPROVED. No next Build Order.** The DA-controllable items are fixed
well, and PG migration + lint/frontend gates are proven on target. But the operator run exposed a **real
target-platform test failure in an approved path (F-5)** and an **invalid auth transcript that never
proved authenticated access (F-6)** — both HIGH. Diagnose/fix the live-market failure, re-run a clean full
suite (0 failed) on target, and supply a **valid** auth transcript (401 without / 200 with) plus the UTC
output and parity smoke. Then this approves.

**Note to the new DA (fair, not punitive):** your corrections were correct and honest; the block is the
*operator-run evidence*, which came back with a genuine failure and a broken login script. Two process
points: (1) a delivery should not be considered evidence-complete until the operator run is reviewed and
**green** — a failing test in the evidence is a finding, not a footnote; (2) provide the operator a
**copy-paste-safe** auth script with literal credentials so the transcript can't silently no-op.

---

## EVIDENCE CONFIDENCE STATEMENT
- **Evidence Reviewed:** correction report; operator console (PG alembic to 0004; pytest **1 failed/75
  passed**; ruff; frontend 16; invalid auth transcript). Cross-checked vs the Build Order, prior review,
  and Wave-0 history.
- **Confidence Level:** **HIGH** on the two blocking findings (the failing test and the null-login are
  directly in the operator's own output). **MODERATE** on C-2 design; **HIGH** on C-4. LIMITED on overall
  target-platform correctness — a suite with a failure and no valid-token proof cannot support approval.
- **Remaining Unknowns:** root cause of the live-market test failure; whether operational endpoints
  actually return 200 to a valid token; UTC test output; parity behavior.
- **Additional Evidence Required:** C-1a (green full suite on target + failure fix), C-1b (valid auth
  transcript with 200-with-token), C-1c (UTC output + parity smoke).

---

*"The UTC fix is right and the Postgres migration is real — but the operator's console shows a live-market
test FAILING and a login that sent null, so '401 with token' proves nothing. A failing test in the
evidence is a finding, not a footnote. Fix the regression, log in for real, and prove 200-with-token.
We don't guess. We prove."*
— AXIOM ITRGA
