# AXIOM BUILD ORDER — W1-U02

## Core Platform: Observability Service & CI Gate Consolidation

**Build Order ID:** W1-U02
**Wave:** 1 — Core Platform · **Unit:** 02
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-13
**Authorized By:** ITRGA, following **W1-U01 APPROVED** + Operator direction (observability + CI first).

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY.md`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` → **`05_SYSTEM_ARCHITECTURE.md` v2.0** →
`06_ML_SPEC` / `07_UI_UX_SPEC` → `08_DEVELOPER_REASONING_FRAMEWORK` / `09_ITRGA_REASONING_FRAMEWORK` →
Tier-7 (`QUALITY_GATE_SPEC`, `RISK_REGISTER`, `TECHNICAL_DEBT_REGISTER`, `GOVERNANCE_AMENDMENTS`) →
`UNIVERSAL_ITRGA_REVIEWER_DIRECTIVE.md`.

---

## 1. Purpose

Establish the **Observability Service** as a first-class Core Platform Service (05 v2.0 §26/§69/§83) and
**consolidate the automated CI gate** so that from this point forward every unit has (a) diagnosable
runtime telemetry and (b) automatic regression detection. Observability must be *designed in*, not bolted
on later (05 v2.0 §26). This unit also **closes the last Wave-0 carryover (the green CI run, C-4b)** and
syncs the governance registers.

This is an **infrastructure/telemetry + tooling** unit. It adds visibility and automation — **not** new
product behavior.

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No execution/trading/broker connection.** MT5/broker untouched. Execution stays roadmap-gated.
- ❌ **No ML/AI product; no chart feature expansion; no new markets.**
- ❌ **No business logic in the observability/infrastructure layer** (05 v2.0 §32–34). Observability is
  **read-only telemetry** — it records/exposes; it must not make business decisions or mutate domain state.
- ❌ **No secrets, tokens, passwords, or PII in logs/metrics/traces** (05 v2.0 §77). This is the single
  most important constraint for a logging unit — a delivery that logs a JWT/credential/DB password is an
  automatic **FAIL**. Redaction must be demonstrated.
- ❌ **No regression of any approved capability** (Wave-0 + W1-U01). Prove via the suite + parity smoke.
- ✅ **Preserve:** advisory-first, single-uvicorn, canonical v2.0, and all W0-U08/W1-U01 hardening
  (enforced secret, non-default bootstrap, refresh rotation, WS tickets, endpoint auth, tz-aware UTC).

---

## 3. Scope — Components A–F

### Component A — Observability Service (05 v2.0 §26) — structured logging + correlation
Establish/mature a dedicated **Observability Service** as a Core Platform Service with a single
responsibility (telemetry), interface-based, independently testable, no business logic.
- **Structured logging** (JSON) with consistent fields: timestamp (tz-aware UTC), level, logger/component,
  message, and a **correlation/request ID** propagated per request (and per WS connection / per background
  task where practical). Build on the existing structured-log seam; do not duplicate.
- **Redaction**: a documented, tested mechanism that guarantees secrets/tokens/credentials/PII never reach
  logs (redact Authorization headers, tokens, passwords, DB URLs with credentials).

### Component B — Metrics & health/readiness maturation (05 v2.0 §69/§83)
- **Metrics endpoint** (e.g. Prometheus-style `/metrics`, or a documented JSON metrics surface) exposing:
  request counts/latency, error rates, DB pool/latency, live-feed health (messages, persist count/errors,
  lag), and process/resource basics. Keep it **read-only** and **authenticated or explicitly justified
  public** per the W1-U01 auth-breadth policy.
- **Mature `/health` and `/ready`** to reflect the real state of each subsystem check (config, logging,
  database, market_ingestion, authentication, live_market) with per-check status + latency — consistent
  with §83 operational monitoring. No secret leakage in health payloads.

### Component C — Runtime diagnostics / error observability
- Consistent **exception logging** with correlation IDs and stack context (no secret leakage); ensure
  unhandled errors are logged with enough context to diagnose (the U08 audit-500 class of bug should be
  immediately diagnosable from logs).
- A brief **operator diagnostics** surface (documented) — e.g. a diagnostics/health summary the operator
  can read — without exposing internals/secrets.

### Component D — CI gate consolidation (closes OBS-2 / C-4b) — the carried Wave-0 item
- Deliver a **working CI pipeline** (`.github/workflows/ci.yml` or the project's chosen runner) that runs,
  on push/PR: **`alembic upgrade head` against PostgreSQL** (service container), **backend `pytest`**,
  **frontend `vitest`**, **`tsc`/build**, and **`ruff`**. It must **fail the build on any failure**.
- Provide evidence the pipeline **actually runs green** (a real run log/screenshot) — or, if remote CI is
  unavailable, a **documented, reproducible local pipeline script** that runs all gates against PostgreSQL
  and is shown green by the operator. (Per prior allowance, but the goal is a real green run.)

### Component E — Governance register sync + carried notes (closes F-A; documents OBS-1/OBS-3)
- **Sync `TECHNICAL_DEBT_REGISTER`:** mark U07-OBS-1 (EURUSD frame) **Closed**; verify/record U07-OBS-5
  default viewport; reconcile any stale statuses; record OBS-2 closed once CI is green.
- **Document OBS-1** (simulated candles are forward-dated / synthetic) as an explicit note/risk so it can
  never be mistaken for real chronology by future ML units (the `source=live:simulated` marker stands).
- Provide the full **`test_time_utc.py -vv`** paste (closes OBS-3 trivially).
- Update `RISK_REGISTER`/`GOVERNANCE_AMENDMENTS`/`PROJECT_STATE`/ADRs as applicable (ADR for the
  observability design + the CI design).

### Component F — Verification & Delivery
- Full existing suite green (backend 76 / frontend 16 baseline) **plus** new tests for A–C (structured-log
  fields present, **redaction test proving a token is NOT logged**, correlation-ID propagation, metrics
  endpoint shape, health per-check accuracy).
- Delivery Report per §5.

### Explicitly OUT of scope
MT5/broker connection or execution; ML/AI; chart features; new markets; full distributed tracing backends
(OpenTelemetry/Grafana are *future* per 05 v2.0 §69 — a clean structured-log + metrics + correlation-ID
foundation is enough now); RBAC/MFA (future). Record deferrals in the debt register.

---

## 4. Success Criteria (Definition of Done)

- [ ] Observability Service exists as a single-responsibility Core Platform Service (no business logic).
- [ ] Structured JSON logs with correlation/request IDs across requests (and WS/background where practical).
- [ ] **Redaction proven:** a test demonstrates secrets/tokens are NOT present in emitted logs.
- [ ] Metrics surface (read-only) exposing request/error/latency/DB/live-feed metrics; auth per policy.
- [ ] `/health` + `/ready` reflect real per-subsystem state with status + latency; no secret leakage.
- [ ] **CI pipeline runs green** (alembic-on-PG / pytest / vitest / tsc / ruff) and fails on any failure
      — with a real run shown (OBS-2 / C-4b closed).
- [ ] Registers synced (F-A); OBS-1 documented; OBS-3 UTC `-vv` provided.
- [ ] No execution/ML/chart/new-market; advisory-first + prior hardening preserved; no regression.
- [ ] Full suite green + new tests; single-uvicorn preserved; conforms to 05 v2.0 (§26/§32–34/§69/§77/§83).

---

## 5. Delivery Report & Evidence Requirements (MANDATORY — operator-run, target platform)

Per the reinforced standard (and the W1-U01 lesson: sandbox-green ≠ target-proven; a failing test in the
evidence is a finding). Provide operator-run, Windows + PostgreSQL evidence:
1. **Operator test console** (raw, `collected N`): backend `pytest`, frontend `vitest`, `tsc`, `ruff` —
   **0 failed**, no regression from 76/16 + new tests.
2. **Redaction evidence:** a log sample (or test output) proving an Authorization/token/password is
   **redacted** — plus a negative check that the raw token does **not** appear in logs.
3. **Correlation-ID evidence:** a request whose log lines share a correlation/request ID.
4. **Metrics + health evidence:** a `curl`/`Invoke-RestMethod` of the metrics endpoint and `/health`
   `/ready` showing real per-subsystem status (with auth as per policy).
5. **CI evidence:** a **green pipeline run** (log/screenshot) covering all gates against PostgreSQL — or a
   documented local-equivalent shown green.
6. **Parity smoke:** login → WS ticket 200 → live feed → candle fetch, proving no regression.
7. Confidence stated **HIGH/MODERATE/LIMITED with justification — no fabricated percentages**.

---

## 6. Standards & Constraints
Clean architecture / SRP / interface-based Core Platform Service (05 v2.0 §26/§32–34); **no secrets in
telemetry** (§77); tz-aware UTC in all timestamps (W1-U01); no business logic in infra; every change in
the debt/decision/amendment registers; cross-platform (Windows + docker/PG).

---

## 7. Process
Implement → internal verify → doc sync (PROJECT_STATE + registers + ADRs) → Delivery Report with §5
evidence (operator-run, green, no failing tests) → **submit to ITRGA** → independent review → corrections
if required → approval → next Build Order. DA does not self-approve or self-authorize the next unit.

---

## 8. Priority Guidance (if staged)
**A (structured logging + redaction) → C (error observability) → B (metrics/health) → D (CI gate) →
E (registers).** Redaction (no-secrets-in-logs) is the highest-risk item for a logging unit and must be
proven, not assumed.

---

*ITRGA — Make the platform observable and self-checking before it grows further. And never log a secret. We don't guess. We prove.*
