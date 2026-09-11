# AXIOM — BUILD ORDER B-07
## Cross-Cutting Hardening & Production-Readiness Evidence

| Item | Value |
|------|-------|
| Build Order ID | `BO-B-07` |
| Programme | Backend Operationalization (reconciled v2; predictive track deferred per Operator decision) |
| Authorizing authority | **Operator** (directive of 2026-08-20: "authorized") |
| Predecessors | B-00 → B-06 (all APPROVED WITH OBSERVATIONS) · Reconciliation Determination · predictive deferral |
| Governing documents | `05_SYSTEM_ARCHITECTURE.md` v2.0 §69, §78–85 · `17_INSTITUTIONAL_SECURITY_STANDARD.md` · `11_PRODUCTION_READINESS_CERTIFICATION.md` · W7-U07 rate-guard deferral |
| Implementer | Development Authority (DA) |
| Reviewer | ITRGA |
| Status | **ISSUED — awaiting DA implementation** |
| Governance Gate | CLOSED (unchanged) · Production NOT CERTIFIED (unchanged) |

---

## 0. Purpose and honest framing

This is the final backend unit. It closes the known **hardening deferrals** and assembles the production-readiness evidence, without claiming certification. Three verified facts scope it:

1. **Rate limiting is `formally_deferred`** (W7-U07, `RATE_GUARD_TECHNICAL_DEBT_ID`), documented as requiring "a dedicated dependency/storage spike." No rate limiter exists. **This must be closed.**
2. **Observability exists but is basic** — correlation IDs + HTTP request metrics + a `/metrics` endpoint. No structured per-pipeline tracing, no resource-utilization metrics.
3. **No security headers** exist (no X-Content-Type-Options, X-Frame-Options, HSTS, Content-Security-Policy, etc.). Only CORS + the observability middleware are installed.

**This order hardens; it does not certify.** Production certification remains a separate Operator/ITRGA decision under Doc 11, and this order explicitly does **not** claim it.

---

## 1. Objective

1. Close the rate-guard deferral with a dependency/storage-spiked, bounded rate limiter.
2. Add baseline security headers and tighten the middleware posture.
3. Deepen observability (structured logs, per-pipeline metrics, resource utilization).
4. Assemble Doc 11 evidence across the eight certification categories — as an **evidence inventory**, not a certification verdict.

---

## 2. Scope

### B-07.1 — Rate limiting (close the W7-U07 deferral)
- **Spike:** a bounded rate guard. Preference (not mandate): no new compiled dependency — a storage-backed (SQLite/Postgres via the existing session) or in-memory token/leaky-bucket limiter, keyed by operator identity, with per-route and global ceilings.
- **Config:** `AXIOM_RATE_LIMIT_ENABLED`, per-operator window + ceiling, and a small admin allowlist. Defaults fail-safe (deny on misconfiguration, never silently open).
- **Scope of application:** the operator-authenticated write surfaces (ingestion, intelligence generation, collaboration POSTs, alert checks) — read surfaces and health endpoints are not rate-limited by default.
- **Update** `RATE_GUARD_DISPOSITION` in `readiness.py` from `formally_deferred` to the implemented state (with the new technical-debt closure).

### B-07.2 — Security headers & middleware posture
- Add baseline response headers: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`, `Strict-Transport-Security` (when configured for HTTPS), and a restrictive `Content-Security-Policy` (or a documented, justified default).
- Verify CORS origin allowlist remains explicit (no wildcard in non-dev).

### B-07.3 — Observability deepening
- Structured, correlation-id-bearing logs already exist — extend coverage to the new B-04/B-05/B-06 pipelines (report generation, alert emission, assistant asks) with explicit `category`/`action` fields.
- Add resource-utilization and per-pipeline counters to the existing `/metrics` surface (still read-only, no secrets, no business decisions).
- Document the health/readiness endpoints (`/health`, `/ready`) and confirm they reflect the new subsystems.

### B-07.4 — Doc 11 evidence assembly
- Produce an **evidence inventory** mapping each Doc 11 certification category to the concrete artifacts that would support it: security, secrets, state management, error management, deployment/compatibility, performance/scalability, UX/accessibility, operational readiness.
- The inventory is a **reference document**, not a certification claim. It must not state or imply CERTIFIED.

---

## 3. Exclusions (out of scope — do NOT do)

- **No** production certification claim (Doc 11 is a separate Operator/ITRGA decision).
- **No** ML model, prediction, or promotion (predictive track deferred).
- **No** weakening of the threshold gate, tier rule, chronology guard, refusal policy, or non-actuation invariants.
- **No** broker/account/execution/order surface.
- **No** new compiled dependency unless justified (Doc 09 §12); any added dependency must be pinned and removable.
- **No** frontend changes (F-06 polish comes later).
- **No** modification of the governance hierarchy or constitutional documents.
- **No** repository publication (custody model).

---

## 4. Exact deliverables

1. Rate limiter (storage-backed, operator-keyed, configurable, fail-safe) + the deferral disposition updated.
2. Security headers middleware + evidence of the header set.
3. Observability extension (pipeline logs + metrics) + evidence.
4. Doc 11 evidence inventory document.
5. Tests (new/churn): rate-limit enforcement, header presence, metrics shape, no-weakening invariants.
6. Delivery Report (§9) with relay-accurate transmission manifest.

---

## 5. Dependencies

- **Upstream:** all prior B-units (their endpoints are the rate-limit/observability subjects).
- **Downstream:** X-01 (end-to-end verification) consumes the hardened platform; the Doc 11 inventory feeds any future certification.
- **Independent of:** any promoted model.

---

## 6. Allowed files / components

- `backend/app/core/config.py` (rate-limit + header settings).
- `backend/app/main.py` (middleware).
- New rate-limit module (e.g. `backend/app/services/rate_limit.py` or `backend/app/core/rate_limit.py`).
- `backend/app/services/observability_service.py` and `backend/app/api/routes/observability.py`.
- `backend/app/institutional_platform/readiness.py` (update the deferral disposition).
- `backend/docs/**` (Doc 11 evidence inventory; any ADR for the rate-limit spike).
- `backend/tests/**` (new/churn tests).
- The Delivery Report.

Anything outside this list is **not authorized**.

---

## 7. Security & integrity constraints (binding)

- Rate limiter must **fail safe** (misconfiguration → deny, never open), and must not leak operator-identity details in responses (429 body minimal).
- Security headers must not break the frontend (CSP must be verified against the terminal's own assets; no third-party script/style allowance beyond what the app itself uses).
- No secrets/credentials; no new external network surface.
- The threshold gate, tier rule, chronology guard, refusal policy, and non-actuation invariants are **unchanged**.
- Doc 11 inventory must be honest: it lists evidence, states gaps as gaps, and makes **no** certification claim.

---

## 8. Acceptance criteria

- [ ] Rate limiter enforces per-operator ceilings on the write surfaces (test-pinned: burst beyond ceiling → 429; below → pass; admin allowlist honored).
- [ ] Rate-guard deferral disposition updated from `formally_deferred` to implemented (with closure note).
- [ ] Security headers present on responses (test-pinned presence of the required set).
- [ ] Observability: new pipeline categories/actions logged with correlation ids; `/metrics` extended; `/health`/`/ready` reflect subsystems.
- [ ] Doc 11 evidence inventory exists, maps all eight categories, states gaps honestly, claims nothing certified.
- [ ] No-weakening invariants intact (gate/tier/guard/refusal/non-actuation tests still green).
- [ ] Full backend suite green; new tests executed with output.

---

## 9. Evidence requirements (custody model + CA-TRANSMIT-1, hard gate)

**Binding (CA-TRANSMIT-1):** artifacts must be uploaded and confirmed against the review channel. A declared-but-untransmitted artifact is an automatic CORRECTION REQUIRED.

| Item | Class | Form |
|------|-------|------|
| Patch artifact + per-file SHAs + `git apply --check` transcript | Level I | patch + transcript |
| Executed test output (new/churn) | Level II | run transcript |
| Rate-limit evidence (429 on burst, pass below ceiling, admin allowlist) | Level I | API probe output |
| Header presence evidence | Level I | API probe output (response headers) |
| Observability evidence (pipeline logs + metrics) | Level I | probe/log output |
| Doc 11 evidence inventory | Level III | document |
| Transmission manifest (relay-accurate) | — | table in Delivery Report |
| Delivery Report | Level III | §10 structure |

---

## 10. Delivery Report structure (required)

1. Claimed scope vs. this Build Order
2. What changed (files + SHAs + chain position)
3. Rate-limit spike description (algorithm, storage, config, fail-safe)
4. Security-header set + rationale
5. Observability extension description
6. Doc 11 evidence inventory (reference; honest gaps)
7. Test evidence (executed)
8. Deviations register
9. Transmission manifest (relay-accurate)
10. Known limitations / technical debt (incl. any residual deferrals)

---

## 11. Rollback / containment

- Rate limiter, headers, and metrics are additive; revert = revert patch. No schema migration authorized by default (rate-limit storage, if any, must be documented and removable).
- Security headers are reversible per-header via config if they break a client.
- No data produced affects production (Gate CLOSED).

---

## 12. Completion condition

Complete when: all §8 criteria met, evidence (§9) transmitted and verified, the Delivery Report submitted, **and ITRGA issues its independent determination**. A DA declaration of completion is not evidence and does not close this unit.

**Next authorization state:** upon ITRGA approval of B-07, the backend operationalization is complete and **X-01 (End-to-End Platform Verification)** may be issued — the joint backend+frontend gate.

---

**End of Build Order B-07**
