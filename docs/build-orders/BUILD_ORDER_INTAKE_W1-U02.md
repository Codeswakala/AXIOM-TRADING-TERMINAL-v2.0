# Build Order Intake — W1-U02

| Item | Value |
|------|-------|
| Build Order | W1-U02 — Core Platform: Observability Service & CI Gate Consolidation |
| Date received | 2026-07-13 |
| Authority | ITRGA, following W1-U01 APPROVED + Operator direction |
| DA status | ACCEPTED — implementation authorized by issued Build Order |
| Approval | Not self-approved; delivery requires ITRGA review |

---

## 1. Governance confirmation

The Development Authority confirms receipt of `docs/build-orders/BUILD_ORDER_W1-U02.md`.

The Build Order states W1-U01 is **APPROVED** and authorizes W1-U02. Implementation may proceed within the W1-U02 scope.

## 2. Objective

Establish a first-class Observability Service and consolidate CI gates without adding product behavior. This unit must improve telemetry, diagnostics, metrics, redaction, health/readiness, and automated regression detection while preserving all approved Wave-0 and W1-U01 behavior.

## 3. Scope interpretation

| Component | DA interpretation |
|-----------|-------------------|
| A Observability Service | Create a single-responsibility telemetry service, request correlation ID support, structured log redaction, and request logging. |
| B Metrics/health | Add authenticated read-only metrics surface; add latency/status details to health/readiness. |
| C Runtime diagnostics | Log unhandled exceptions with correlation ID and redacted context only. |
| D CI gate | Add Ruff to CI and provide a local pipeline script for operator evidence where remote CI is unavailable. |
| E Registers | Sync project state, debt/risk/amendments, ADRs, and explicit simulated-data chronology risk. |
| F Verification | Add tests for log fields, redaction, correlation, metrics, health readiness, and preserve prior suite. |

## 4. Constraints

- No execution, broker, ML/AI product, chart expansion, or new market feature.
- Observability must be read-only and must not contain business logic.
- No secrets/tokens/passwords/DB credentials in logs or metrics.
- Preserve W0-U08 and W1-U01 hardening.

## 5. Initial risk assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Secret leakage through logs/metrics | Critical | Central redaction utility + tests using raw token/password/DB URL negative checks. |
| Metrics endpoint leaks internals unauthenticated | High | Require Bearer auth per W1-U01 policy. |
| Middleware breaks existing routes/SPA | Medium | Minimal HTTP middleware; preserve path routing; regression tests. |
| CI evidence unavailable in DA sandbox | Medium | Provide local script and operator checklist; remote CI remains operator/GitHub evidence. |

## 6. Implementation authorization posture

Build Order accepted. DA will implement, verify, document, and submit a Delivery Report. DA does not self-approve W1-U02.

---

**End of intake**
