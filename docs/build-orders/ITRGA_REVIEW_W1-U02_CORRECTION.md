# AXIOM ITRGA — RE-VERIFICATION: W1-U02 Correction

**Authority:** ITRGA · **Prior verdict:** CONDITIONAL (mandatory operator evidence absent)
**Inputs:** operator results console (Windows/PowerShell + **PostgreSQL 18**). **Date:** 2026-07-13 · **Std:** R1–R21.

---

## VERDICT: **CONDITIONAL — APPROVAL WITHHELD on ONE item.** Four of six corrections are now proven on the target platform; **C-5 (CI run) is downgraded to a tracked observation; C-2 (the redaction LOG SAMPLE) is NOT satisfied and remains a hard requirement** because it is this unit's defining risk.

This is a big step up from the report-only prior round — real operator evidence on Windows + PostgreSQL,
a full green suite, metrics/health at runtime, correlation-ID echo, and a clean parity smoke. It is **one
cheap artifact from approval.** I am withholding on the single item I said up front I would not wave for a
logging unit: an actual runtime log line showing a real Bearer token **redacted**.

---

## 1. CORRECTIONS PROVEN ON TARGET (operator-run, Windows + PostgreSQL)

| Item | Status | Evidence |
|---|---|---|
| **C-1** full green suite on target | ✅ CLOSED | `alembic 0001→0004` on **PostgresqlImpl** from `DROP/CREATE SCHEMA` (empty DB); **`81 passed, 0 failed`** (Py3.14/win32) incl. `test_observability`, `test_hardening`, `test_ws_ticket_e2e`; `ruff` clean; vitest 8 files/16; tsc/build clean. No regression. |
| **C-3** metrics + health runtime | ✅ CLOSED | `/api/v1/metrics` **401 without token / 200 with**; payload = request/status/latency + correlation IDs; `/health`+`/ready` per-check detail. **No token/password/DB-credential visible** in the returned payloads. |
| **C-4** correlation-ID runtime | ✅ CLOSED | `X-Correlation-ID: operator-evidence-correlation-001` echoed in the response header; metrics recent-requests carry `correlation_id`. |
| **C-6** parity smoke + PG alembic | ✅ CLOSED | login 200; ws-ticket 200; live/status `running:true, persist_count:46, persist_errors:0`, EURUSD+BTCUSD; candle fetch returns rows with **both** `source=seed:synthetic` **and** `source=live:simulated` (provenance markers working). No Wave-0 regression. |

DA-side (prior): C-2-design (require_utc/coerce split) etc. carried from W1-U01; observability service is
read-only/no-business-logic; registers synced. Good.

---

## 2. C-5 (green CI run) — DOWNGRADED to OBSERVATION (not blocking)

The CI *pipeline execution* was not shown. **However**, every constituent gate the pipeline runs was
demonstrated **green in this very operator console on the target platform**: `alembic upgrade head` on
PostgreSQL, `pytest 81`, `ruff`, `vitest 16`, `tsc`, `vite build`. A CI pipeline is those same steps
orchestrated; the residual risk is only that the *orchestration* wrapper fails, which is LOW given the
steps themselves pass. Per proportionality (R13), I **downgrade C-5 to a tracked OBSERVATION** (still
owed as OBS-2/C-4b closeout, capture a real run early — but not a wave-blocker now that all its checks are
proven green manually on target).

---

## 3. THE ONE BLOCKING ITEM

### F-1 (MEDIUM–HIGH) — C-2 redaction LOG SAMPLE still not shown (the unit's defining risk)
The **no-secrets-in-logs** guarantee is the entire reason a redaction mechanism exists in an observability
unit. What is proven: the **redaction unit test passes** (inside the 81), and **no secret is visible in
the metrics/health payloads.** What is **not** proven: an **actual emitted log line** where a real request
carrying an `Authorization: Bearer <token>` produces a log entry with the token **redacted / absent.**
- A passing redactor unit test proves the *function* redacts its inputs; it does **not** prove every real
  log path routes through it.
- "No secret in two API payloads" is necessary but not sufficient — those are responses, not the logs.
- The Build Order §5.2 and my prior C-2 required a **log sample**. It is absent (grep of the entire
  console: no `redact`, no redaction marker, no log line with a masked token).

This is cheap to produce: make **one authenticated request** (there are several in the evidence already),
then show the **corresponding structured-log lines** demonstrating (a) the request was logged with its
correlation ID, and (b) the Authorization token does **not** appear in the log (masked/absent). Optionally
grep the log for the raw token string and show zero matches.

**Why I hold on this specifically (and only this):** for a logging unit, an unproven redaction path is a
latent **credential-leak** — exactly the class of risk the standard exists to catch, and the one I named
as the top item for this unit twice. Everything else is proven; I will not approve around the one
security-critical artifact that is missing.

---

## 4. REQUIRED CORRECTION (single, to convert to APPROVED)

- **C-2 (final) — Supply the redaction log sample:** operator-run, an authenticated request + the emitted
  structured log lines showing the Bearer token **redacted/absent** (and, ideally, a grep of the log file
  for the raw token returning zero matches). One request, one log excerpt.

## 5. TRACKED (non-blocking) — carry to next unit
- **OBS-2 / C-5:** capture one real **green CI pipeline run** (its steps are already proven green on target).
- **npm audit (TD-012):** `npm ci` reported **5 vulnerabilities (3 moderate, 1 high, 1 critical)** in the
  frontend toolchain. Not W1-U02 scope and not new, but the **critical/high** should be scheduled and
  risk-assessed soon (record in RISK_REGISTER with a target unit) — flagging per R8.
- Deprecation warnings (asyncio policy, httpx/starlette) are noise; note for a future cleanup.

## 6. DISPOSITION
**W1-U02: CONDITIONAL — one artifact from APPROVED. No next Build Order yet.** Four of six corrections are
proven on the target platform; C-5 is a tracked observation. **Supply the C-2 redaction log sample** and I
will approve immediately — this is the last, security-critical piece for a logging unit.

**Note to the DA:** genuinely strong evidence this round — real PG, 81 green, metrics/health/correlation
all shown at runtime. The single miss is the one item most central to the unit's purpose: *prove the logs
don't leak the token by showing the logs.* Run one authenticated request and paste the redacted log lines.

---

## EVIDENCE CONFIDENCE STATEMENT
- **Evidence Reviewed:** operator console — PG clean migrate to 0004; `pytest 81`; ruff; vitest 16; tsc/
  build; `/metrics` 401/200 payload; `/health`/`/ready`; `X-Correlation-ID` echo; ws-ticket 200; live/
  status + candle fetch with provenance markers. Cross-checked vs the Build Order, prior review, W1 history.
- **Confidence Level:** **HIGH** that C-1/C-3/C-4/C-6 are met and that all CI constituent gates pass on
  target; **MODERATE** that logs are secret-free (unit test + payload evidence, but no runtime log sample);
  the redaction-in-practice guarantee is **not yet Level-I proven** — hence the single withhold.
- **Remaining Unknowns:** whether every real log path redacts (C-2 log sample); CI orchestration green run;
  frontend npm-audit critical/high remediation.
- **Additional Evidence Required:** C-2 redaction log sample (blocking). Tracked: C-5 CI run; TD-012.

---

*"Five-sixths proven on real Postgres — 81 green, metrics gated, correlation IDs echoing, provenance
markers intact. The one thing still owed is the whole point of a logging unit: show me a log line where
the token is redacted. One request, one excerpt, and this approves. We don't guess. We prove."*
— AXIOM ITRGA
