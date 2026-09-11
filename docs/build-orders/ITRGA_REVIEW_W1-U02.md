# AXIOM ITRGA — REVIEW: W1-U02 (Observability Service & CI Gate Consolidation)

**Authority:** ITRGA · **Build Order:** `BUILD_ORDER_W1-U02.md` · **Delivery Report:** `DELIVERY_REPORT_W1-U02.md` (v0.10.0)
**Evidence tier:** Delivery report only (DA-sandbox / SQLite). **No operator-run target-platform evidence
supplied this round.** No source inspected. **Date:** 2026-07-13 · **Standard:** R1–R21.

---

## VERDICT: **PASS WITH OBSERVATIONS — CONDITIONAL. APPROVAL WITHHELD.**

The implementation is well-designed, correctly scoped, and the redaction/no-secrets discipline is
addressed at the test level. **But the Build Order's mandatory §5 evidence set is entirely unmet:**
everything is DA-sandbox (Level II) or asserted (Level III) — no operator-run Windows+PostgreSQL console,
no runtime metrics/health payloads, no redaction *log sample*, no correlation-ID runtime sample, no
**green CI run**, no parity smoke. For an **observability unit** — whose entire value (runtime telemetry +
automatic regression gate) and whose #1 risk (secrets-in-logs) are runtime-dependent — that is
disqualifying for approval under R3/R5/R9. This is not a FAIL (no CRITICAL defect visible; the design is
sound) and the DA is commendably honest that the evidence is still owed. It simply cannot be approved yet.

---

## 1. WHAT IS GOOD (documentary / design — Level II/III, credited)

- **Architecture-correct:** `ObservabilityService` is a single-responsibility, **read-only telemetry**
  Core Platform Service with **no business logic / no domain mutation** (05 v2.0 §26/§32–34). ADR-017/018.
- **Redaction addressed at the right level:** a **negative test**
  (`test_redaction_removes_tokens_passwords_and_db_credentials`) asserts raw tokens/passwords/DB-cred URLs
  do **not** survive redaction; coverage spans Bearer/access/refresh tokens, WS tickets, PG-credential
  URLs; bodies/raw headers intentionally not logged. This is the correct design for the unit's top risk.
- **Metrics auth-gated** (`/api/v1/metrics` 401 without token, with a test); **health/ready gain per-check
  latency**; correlation-ID middleware (`X-Correlation-ID` in/out); structured JSON log fields.
- **CI consolidated in config:** alembic-on-PostgreSQL + ruff + pytest + vitest + tsc/build, fails on
  failure; `scripts/local_ci.sh` local equivalent added. This closes OBS-2 **in code** (not yet proven).
- **Test growth 76→81 (+5)** matches the five new observability tests; registers synced; OBS-1 (simulated
  chronology) documented as an ML risk; confidence honestly rated (target-platform = LIMITED); no
  self-approval; scope clean (no exec/ML/chart/new-market).

The design would likely approve — *once proven on the operator's machine.*

---

## 2. THE BLOCKING FINDING

### F-1 (HIGH — mandatory operator evidence entirely absent)
Build Order §5 requires operator-run, Windows + PostgreSQL evidence for approval. Reconciliation:

| §5 mandatory item | Supplied | Status |
|---|---|---|
| Operator `pytest`/`vitest`/`tsc`/`ruff` (Win+PG, 0 fail, no regress from 76/16) | DA-sandbox **SQLite** run (`81 passed`, `16 passed`), bash env | ⚠️ Level II — **UNMET on target** |
| **Redaction runtime evidence** (a log sample proving a token is redacted / absent) | Test asserted; **no log sample** | ❌ MISSING (the unit's #1 risk) |
| Correlation-ID runtime evidence (shared cid across a request's log lines) | Header test asserted; **no runtime sample** | ❌ MISSING |
| **Metrics + health runtime payloads** (curl/Invoke-RestMethod output) | Shape described; **no actual output** | ❌ MISSING |
| **Green CI run** (or local-equivalent shown green) | CI config + `local_ci.sh`; **no green run** | ❌ MISSING (this was the whole point of Component D / OBS-2) |
| Parity smoke (login → WS ticket 200 → live feed → candle fetch) | **Not supplied** | ❌ MISSING |
| Alembic on **PostgreSQL** | DA ran **SQLite** local equivalent only | ⚠️ UNMET on target |

The DA itself states this repeatedly ("Operator-run Windows + PostgreSQL evidence remains mandatory for
approval") and delivered an **operator checklist** in place of the evidence. Honest — but the checklist is
the *plan* to produce evidence, not the evidence. **Approval requires the run, not the recipe.**

### Why this matters more for THIS unit (not less)
- **Secrets-in-logs** can only be *proven absent* by inspecting **actual emitted logs** on a real run. A
  passing redaction unit test proves the redactor function works on its inputs; it does **not** prove that
  every real log path routes through it. An operator log sample (showing a request with an Authorization
  header, and the corresponding log lines with the token redacted / not present) is the required proof.
- **CI's value is that it actually runs.** A workflow file that has never executed green is unproven
  automation. OBS-2/C-4b is closed only by a **green run**, not by committing YAML.
- The W1-U01 history is directly relevant: its DA-sandbox suite was green while the operator's target run
  had a **failing live-market test** and a **broken auth transcript**. Sandbox-green here does not rule out
  a target-platform regression from the new middleware.

---

## 3. REQUIRED CORRECTIONS (to convert to APPROVED)

Supply operator-run, Windows + PostgreSQL evidence:
- **C-1 — Full test console on target:** backend `pytest` (`collected 81`, **0 failed**), `ruff`, frontend
  `vitest`/`tsc`/build — no regression from 76/16.
- **C-2 — Redaction proof (the key item):** a real log sample from a request carrying an Authorization
  token showing the token **redacted / absent** in the emitted logs (plus the negative-check that the raw
  token string does not appear). This is the unit's top risk and must be shown at runtime, not asserted.
- **C-3 — Runtime metrics + health/ready payloads:** `/api/v1/metrics` (401 without token, 200 with) and
  `/health`+`/ready` output showing per-check status/latency and **no secrets/DB-cred leakage**.
- **C-4 — Correlation-ID runtime sample:** a request whose response carries `X-Correlation-ID` and whose
  log lines share that id.
- **C-5 — Green CI run (or local-equivalent shown green):** the pipeline executing alembic-on-PostgreSQL /
  ruff / pytest / vitest / tsc, all green — closing OBS-2/C-4b for real.
- **C-6 — Parity smoke + PostgreSQL alembic:** login → WS ticket 200 → live feed → candle fetch (no
  regression), and `alembic upgrade head` on **PostgresqlImpl**.

## 4. RECOMMENDATIONS (non-blocking)
- In the redaction test, add a case that exercises a **real request→log path** (integration-level), not
  just the redactor in isolation, so the "every log path is redacted" claim is test-backed too.
- Confirm the correlation-ID also appears on **error/exception** log lines (the U08-class diagnosability
  goal).

## 5. DISPOSITION
**W1-U02: PASS WITH OBSERVATIONS — CONDITIONAL. Not approved. No next Build Order.** Strong, correctly
scoped design; approval withheld **solely** because the mandatory operator-run target-platform evidence is
absent (F-1). Run the operator evidence — especially the **redaction log sample** and the **green CI run**
— and I will approve promptly.

**Note to the DA (fair):** you were honest that the evidence was owed and you built the right operator
checklist — good. But a delivery is not "submitted for approval-ready review" until that operator run is
attached and green. Producing the checklist and then submitting *without* the run just guarantees a
withhold. Next time, run the checklist first and submit the results with the report.

---

## EVIDENCE CONFIDENCE STATEMENT
- **Evidence Reviewed:** `DELIVERY_REPORT_W1-U02.md` (DA-sandbox SQLite tests, CI config, asserted
  redaction/metrics/correlation). Cross-checked vs `BUILD_ORDER_W1-U02.md`, 05 v2.0, and W1-U01 history.
- **Confidence Level:** **MODERATE** on design/implementation intent; **LIMITED** on runtime correctness,
  redaction-in-practice, and CI actually running (no operator/target evidence; source not inspected). No
  approval rests on report-claims.
- **Remaining Unknowns:** whether every real log path is redacted (secrets-in-logs); metrics/health
  runtime behavior on target; correlation-ID at runtime; whether the new middleware regresses anything on
  Windows+PG; whether CI runs green.
- **Additional Evidence Required:** C-1..C-6 (operator-run, target-platform).

---

*"An observability unit is proven by what its logs actually show and by a CI pipeline that actually runs —
not by a checklist describing them. Show me a real log with the token redacted and a green CI run, and
this approves. We don't guess. We prove."*
— AXIOM ITRGA
