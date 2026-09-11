# AXIOM — Doc 11 Evidence Inventory
## Production-Readiness evidence mapping (BO-B-07.4)

| Item | Value |
|---|---|
| Instrument | `BO-B-07` §B-07.4 |
| Document class | **Evidence inventory — a reference map from Doc 11's certification categories to the concrete artifacts that would support them. It is NOT a certification verdict and claims nothing certified.** |
| Prepared | 2026-08-20 · AXIOM Development Authority |

**Posture (restated, binding):** Governance Gate CLOSED · Production NOT CERTIFIED · RESEARCH-ONLY · NON-ACTUATING. Production certification is a separate Operator/ITRGA decision under Doc 11. This inventory lists what exists; where evidence is missing, the gap is named as a gap.

---

## 1. Security

| Evidence that exists | Where |
|---|---|
| Authentication (JWT + one-time WebSocket tickets, close-4401) | `app/auth/`, `app/api/routes/ws.py`; W0/W1 test suites |
| RBAC (role-scoped dependencies; chunk-level frontend gate; unprivileged fixture 403s) | `app/auth/dependencies.py`; SURF-P03 evidence; `route-access-denied` testid |
| Rate limiting (operator-keyed sliding window, per-route + global ceilings, fail-safe deny, admin allowlist) | `app/core/rate_limit.py` + middleware in `app/main.py` (BO-B-07.1); `test_b07_hardening.py` |
| Security headers (nosniff / frame DENY / referrer / HSTS configurable / restrictive CSP) | middleware in `app/main.py` (BO-B-07.2); header-presence tests |
| Endpoint security surface (no order/broker/execution/account code in any router; static guards green) | W3/W4/W5 suites; `test_*_has_no_execution_path` family |
| **Gap:** permission-granular RBAC on the B-04/B-05/B-06 families is `CurrentOperatorDep`-depth (recorded; future hardening if authorized) | Register TD-B04-UNIT D2 |

## 2. Secrets

| Evidence that exists | Where |
|---|---|
| Secret-marker redaction (assistant prompts/responses, observability) | `redact_secret_markers`, `app/collaboration/contracts.py` |
| No credential literals in the new B-series code (env-driven settings only) | B-00 → B-07 patches; `app/core/config.py` |
| Audit rows never carry payloads/headers | `app/repositories/audit_repository.py` usage across all B-units |
| **Gap:** TD-AXIOM-DEV-CREDENTIAL-LITERALS remains open (pre-certification for Doc 11 §2 per the register) | Register row |

## 3. State management

| Evidence that exists | Where |
|---|---|
| Research-only state discipline (reports/alerts/responses additive; no actuation state) | B-04/B-05/B-06 non-actuation + mutation-boundary tests |
| Immutable snapshots + split manifests (frozen, content-hashed, versioned) | B-01/B-02; `dataset_snapshots`, `dataset_split_manifests` |
| Alert read-state-only ack (subject rows byte-unchanged) | `test_b05_ack_read_state_only_no_actuation` |
| **Gap:** multi-instance rate-limit state (per-process limiter) — named residual deferral | Register TD-B07 disposition |

## 4. Error management

| Evidence that exists | Where |
|---|---|
| Structured insufficient-data failures (422 + error_code + insufficient_data flag; zero fabricated rows) | B-04 suite + probes |
| Structured 429 rate-limit body (minimal, no identity) | `test_b07_burst_beyond_ceiling_returns_429` |
| Honest empty states ("No … returned." discipline) | SURF-P03-approved surfaces; capability checklist R2 |
| Unhandled-exception logging with correlation ids | observability middleware |

## 5. Deployment / compatibility

| Evidence that exists | Where |
|---|---|
| Pin-range dependency policy + severity/exception model (B-00.2) | `requirements.txt`, `pyproject.toml`, pip-audit records |
| Alembic migration history (37 migrations; no B-series migrations) | `backend/alembic/versions/` |
| Local run guides (bash + PowerShell) with exact clone/apply-chain commands | `LOCAL_RUN_GUIDE.md`, `LOCAL_RUN_GUIDE_POWERSHELL.md` |
| **Gap:** multi-process/multi-instance deployment verification (no container/orchestration evidence) | Named gap |

## 6. Performance / scalability

| Evidence that exists | Where |
|---|---|
| Full-suite execution times recorded per delivery (backend 537 · frontend 860) | `docs/evidence/uiconv/*.log` |
| Rate-limit ceilings bound write abuse (documented defaults) | `app/core/config.py` |
| Resource-utilization metrics (CPU, maxrss) on `/metrics` | BO-B-07.3 |
| **Gap:** no load/soak measurements beyond the rate-limit burst tests; no DB query-plan analysis | Named gap |

## 7. UX / accessibility (frontend surface)

| Evidence that exists | Where |
|---|---|
| Accessibility suite (skip link, focus traps, route announcements, contrast, responsive reflow) | `frontend/src/workstation/accessibility/` |
| **Gap:** no independent WCAG conformance audit (recorded OBS-CAPASSESS-H1 for the `<h1>` item) | Register |

## 8. Operational readiness

| Evidence that exists | Where |
|---|---|
| `/health` liveness + `/ready` readiness (live DB check) | `app/api/routes/health.py` |
| WebSocket feed telemetry (state, tick rate, message count, lag) | `app/api/routes/market.py`; telemetry dock |
| Monitoring alert emission with dedup + audit (B-05) | `app/trading_intelligence/monitoring/` |
| Readiness dispositions (rate guard implemented; admin123 rejected outside insecure-dev) | `app/institutional_platform/readiness.py` |
| **Gap:** scheduled/background health checks (generation/emission are on-request) | OBS-B04-1 / OBS-B05-1 |

## 9. X-01 end-to-end verification (backend tier) — evidence executed 2026-08-21

| Evidence that exists | Where |
|---|---|
| Eight-hop governed workflow over the real corpus (109,326 bars, 12 files sha256-verified vs B-DATA MANIFEST `2a2c0921…`) — hops 1–8 with per-hop Level-I/II logs | `docs/evidence/x01/x01_hop{1..8}.log`, `x01_hop4_digest.log`, `x01_supplement.log`, `x01_server_log.log`, `x01_nonetwork_scan.log`, `x01_pytest_fullsuite.log` |
| Full verification report (hop walk, non-actuation, gap list) | `backend/docs/DOC12_X01_VERIFICATION_REPORT.md` |
| Full backend suite re-executed during X-01: 546 passed, exit 0 | `docs/evidence/x01/x01_pytest_fullsuite.log` |
| **Gap (named):** X-01 Terminal Tier deferred — depends on frontend units F-01 → F-06 (per BO-X-01 §0) | Report §4 |
| **Gap (named):** predictive track deferred (no promoted model → predictive signals gated) | Operator Decision Record |
| **Gap (named):** per-process rate-limit store; multi-instance deployment; no load/soak measurements | Report §4 / §8 here |

---

**Closing statement:** this inventory maps evidence and names gaps. It contains no certification verdict, claims no certification, and changes no posture: Gate CLOSED · Production NOT CERTIFIED · We don't guess. We prove.
