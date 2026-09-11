# DELIVERY REPORT — BO-B-07
## Cross-Cutting Hardening & Production-Readiness Evidence

| Item | Value |
|---|---|
| Build Order | `BO-B-07` (Operator directive of 2026-08-20: "authorized"; predictive track deferred) |
| Predecessors | B-00 → B-06 (all APPROVED WITH OBSERVATIONS) · Reconciliation Determination · predictive deferral |
| Implementer | AXIOM Development Authority (DA) |
| Reviewer | ITRGA — determination pending |
| Date | 2026-08-20 |
| Governance Gate | CLOSED (unchanged) · Production NOT CERTIFIED (unchanged) |

**Standing discipline:** CA-TRANSMIT-1 (fourth consecutive — every declared hash verified against the transmitted set) · figures transcribed from the executed logs · no design-plan artifacts produced unprompted (the Operator's correction stands; this delivery is the BO's scope only).

---

## 1. Claimed scope vs. this Build Order

| BO requirement | Delivered | Where |
|---|---|---|
| B-07.1 rate limiter (storage-backed/in-memory, operator-keyed, configurable, fail-safe) + deferral disposition updated | ✓ pure-stdlib in-memory sliding-window (`app/core/rate_limit.py`), operator-keyed (token username claim), per-route + global ceilings, admin allowlist, fail-safe deny on misconfiguration; `RATE_GUARD_DISPOSITION.status` → `implemented` with closure rationale | §3, §6 |
| B-07.2 security headers + CORS verify | ✓ nosniff · frame DENY · referrer · HSTS (configurable) · restrictive CSP; headers wrap the rate-limit layer (429s carry them too); CORS allowlist verified explicit | §4 |
| B-07.3 observability deepening (pipeline logs + metrics; health/ready documented) | ✓ per-pipeline `category/action` counters + correlation-id log lines for the B-04/B-05/B-06 pipelines; `/metrics` extended with `pipelines` + `resources` (stdlib rusage); health/ready documented | §5 |
| B-07.4 Doc 11 evidence inventory (reference, honest gaps, no certification claim) | ✓ `backend/docs/DOC11_EVIDENCE_INVENTORY.md` maps all 8 categories, names gaps, carries zero affirmative certification claims (test-pinned) | §6 |
| §3 exclusions | No certification claim; no ML; no gate/tier/guard/refusal/non-actuation weakening; no broker/account/execution surface; no new dependency (pure stdlib); no frontend; no governance-document changes; no repo publication | — |
| §6 allowed files | config.py · main.py · new rate_limit module · observability service/route (route unchanged) · readiness.py · docs · tests — nothing outside | §2 |

## 2. What changed (files + SHAs + chain position)

Patch artifact: **`b07.patch.txt`** — sha256 `cfe3b9278f4ae4f352a3463b4db1c57dbc8cccb3dc270dde7e409139d695feba`
- Applies clean (`git apply --check` exit 0) onto the verified 27-element chain over baseline `34f4c62`, in a pristine clone, as the **28th chain element**; post-apply, all 8 files byte-identical to the DA workspace (cmp-verified); clone-side B-07 + readiness + B-04/B-06 sets 33/33, ruff clean.

| File | Content SHA-256 |
|---|---|
| `backend/app/core/config.py` | `52768a09e056bb2aa7b11b176b669b48c882c5d84ce645e66cca7f0238a5456b` |
| `backend/app/main.py` | `f69c3628073e3747f16570284d7fd8275eff12f6a50f8386ca0e3d865efd4d7e` |
| `backend/app/core/rate_limit.py` (new) | `138d983bcc4e5e9f94b43b7a2aa0b692bc39a72e2bf1f65687e3e8ea9e8ea21e` |
| `backend/app/services/observability_service.py` | `b3ff9f7546087edd35c8dd9d411061083aba64f4b6e64894f44655d6b7736519` |
| `backend/app/institutional_platform/readiness.py` | `9ea3169e7c59ae5113fd7f5b4f650785fb2f1da7726671f292a0ae4ba6a12d56` |
| `backend/docs/DOC11_EVIDENCE_INVENTORY.md` (new) | `f65dcdec97ff6a70e86a10a3074067cc67a79b9965f18ceda52ac73a58c7b3e0` |
| `backend/tests/test_b07_hardening.py` (new) | `0827a0e0d92f0ee20daa81117a943975f3f13361dea9e5c4e3cb98a9650c1279` |
| `backend/tests/test_enterprise_readiness.py` (churn) | `10b5902922bad57fbca4367311bca5ef8b93036033e41e4c1e32c108a68f6e2a` |

## 3. Rate-limit spike description

- **Algorithm:** monotonic-clock sliding window per operator (deque of timestamps); every write passes BOTH the route-group bucket (per-route ceiling) and the global bucket (global ceiling).
- **Storage:** in-memory, per-process — the BO's explicitly permitted alternative; no schema migration, no new dependency, removable by restart. **Residual deferral disclosed:** multi-instance deployments need a shared store (future separately-governed unit).
- **Keying:** operator identity from the token's `username` claim (fallback `sub`); unauth requests pass to the endpoints' own 401s.
- **Config:** `AXIOM_RATE_LIMIT_ENABLED` (default true) · window 60s · global ceiling 1200 · per-route ceiling 400 · admin allowlist (comma usernames). All bounded.
- **Fail-safe:** invalid window/ceiling → deny every request (unit-pinned).
- **Scope:** POST/PUT/PATCH/DELETE under ingestion / intelligence / collaboration / alerts — on BOTH API mounts (bare + `/api/v1`); reads and health unlimited; auth excluded.
- **Disposition:** `RATE_GUARD_DISPOSITION` → `implemented` with the BO-B-07.1 closure rationale.

## 4. Security-header set + rationale

`X-Content-Type-Options: nosniff` · `X-Frame-Options: DENY` · `Referrer-Policy: strict-origin-when-cross-origin` · `Strict-Transport-Security` (only when `AXIOM_SECURITY_HSTS_ENABLED=true` — HTTPS-configured deployments) · `Content-Security-Policy: default-src 'none'; frame-ancestors 'none'; base-uri 'none'` (API responses; `/docs`+`/redoc` excluded because Swagger UI requires inline assets — and those surfaces are disabled in production anyway). CORS stays on the explicit origin allowlist. The headers middleware wraps the rate-limit layer so 429 responses carry the header set too (test-pinned).

## 5. Observability extension

- `record_pipeline(category, action)` counters + a `Pipeline event category=… action=… cid=…` log line per governed pipeline — derived in the observability middleware from the request shape (no router edits): intelligence × 5 families, monitoring × 2, assistant × 1, ingestion × 1.
- `/metrics` now includes `observability.pipelines` and `observability.resources` (process CPU user/system, maxrss — stdlib `resource`, None-valued where the platform doesn't expose them).
- `/health` (liveness) and `/ready` (live-DB readiness) verified responding with the new subsystems active; documented in the Doc 11 inventory (the health router itself is unchanged — outside §6).

## 6. Doc 11 evidence inventory

`backend/docs/DOC11_EVIDENCE_INVENTORY.md` — all eight categories (security, secrets, state management, error management, deployment, performance, accessibility, operational) mapped to concrete artifacts, gaps named as gaps, and a closing statement carrying no certification claim (test-pinned: "is certified" absent; the posture phrase appears only negated).

## 7. Test evidence (executed)

| Run | Result | Log |
|---|---|---|
| B-07 fail-first probe (against the 27-element chain) | **8/8 failed** — no limiter, no headers, no pipeline/resource metrics, disposition still deferred, no inventory | `b07_probe_prefix.log` |
| B-07 hardening suite (post-fix) | 9 passed (burst 429 + minimal body + 429-headers + allowlist + failsafe + scope + metrics shape + disposition + inventory) | in `pytest_b07_postfix.log` |
| Enterprise-readiness suite (churn verified) | 9 passed | in `pytest_b07_postfix.log` |
| **Full backend suite** | **546 passed, 1 warning, 160.66s** (537 + 9 new; 0 failed/skipped) | `pytest_b07_postfix.log` |
| Clone-side (applied patch content) | 33 passed, ruff clean, apply-check exit 0 | `b07_applycheck_transcript.txt` |

Level-I probe (`b07_api_probe.log`): headers on `/health`; ceiling=4 → four 422s then **429×3** on regime generation; reads unlimited (5×200); `/metrics` shows `pipelines: {intelligence: {regime_report_generated: 1}, monitoring: {alert_check_executed: 1}, assistant: {ask_responded: 1}}` + resource rusage; pipeline log lines carry correlation ids.

## 8. Deviations register

- **D1 — One spec-driven churn.** `test_enterprise_readiness.py::test_abuse_or_rate_guard_enforced_or_documented_deferred` pinned the old `formally_deferred` disposition; the BO's own acceptance criterion supersedes it. Re-pinned to `implemented` + closure rationale (debt id unchanged; assertion stricter, none weakened — the same discipline as B-04 D1 / B-05 D2, inline supersession comment).
- **D2 — Middleware shadowing fix.** The pre-existing local `from app.core.config import get_settings` inside `create_app`'s except-branch shadowed the module-level name for the new middleware closures (NameError at request time). Fixed by aliasing the fallback import (`_fallback_get_settings`); no behavior change to the pre-existing path.
- **D3 — Both API mounts guarded.** The router is mounted twice (bare + `/api/v1`); `route_group` and the pipeline taxonomy normalize the prefix so both mounts are rate-limited and counted.
- **D4 — Pipeline taxonomy found and fixed during the probe.** The first metrics probe returned empty pipelines (taxonomy compared normalized paths against family-only suffixes); fixed and re-probed (counters now populate). Disclosed as an implementation-time correction, not a post-delivery one.
- **D5 — Readiness disposition is not HTTP-exposed** (no route publishes `readiness_dispositions()`; pre-existing). The BO's criterion targets the disposition object, which is updated and test-pinned via direct import.
- **D6 — No schema migration, no new dependency** (pure stdlib `threading`/`collections`/`time`/`resource`); per-process state documented as the residual deferral.

## 9. Transmission manifest (CA-TRANSMIT-1 — every hash verified on the transmitted files)

| # | Declared artifact | Transmitted filename | sha256 |
|---|---|---|---|
| 1 | B-07 patch (chain position 28) | `b07.patch.txt` | `cfe3b9278f4ae4f352a3463b4db1c57dbc8cccb3dc270dde7e409139d695feba` |
| 2 | Apply-check transcript (pristine clone, 27-chain) | `b07_applycheck_transcript.txt` | `eeb99346c82f6ec8dc7c0ce346919ae1e69f793e4ad0bb4d701273d2d5b7d9be` |
| 3 | Fail-first probe log | `b07_probe_prefix.log.txt` | `1aeded88120b4a7e5d4c000c89fd1ea728d9dbece59b582c06958c1588bde5a6` |
| 4 | API probe log (headers + 429 + metrics) | `b07_api_probe.log.txt` | `ed4f71f96fd5f46b3e3b50267a0054d746208661f2463cd0ff263c08f0ff4a82` |
| 5 | Full-suite log (546 passed) | `pytest_b07_postfix.log.txt` | `4d374a953cc998240d30f5f829d0c92dfd9934ebb11af32c76dd3d32af3a0e8a` |
| 6 | Delivery report | `DELIVERY_REPORT_B-07.txt` | (declared in the DA closing message) |

Every hash above resolves to a file in `/home/user/b07_transmission/` (sha256sum -c exit 0 this session).

## 10. Known limitations / technical debt

- **Residual rate-limit deferral:** per-process state — multi-instance deployment requires a shared store (named in the disposition rationale; register row updated).
- CSP/HSTS are config-driven; production values are a deployment decision (documented defaults are restrictive).
- Carried: PROJECT_STATE.md inventory staleness; W3-U03 semantic-narrowing record; fingerprint-determinism hardening; TD-AXIOM-DEV-CREDENTIAL-LITERALS (named in the Doc 11 inventory as a pre-certification item).
- Register: TD-B07-UNIT added; TD-B06-UNIT updated to CLOSED (APPROVED WITH OBSERVATIONS).

---

Gate CLOSED · Production NOT CERTIFIED · We don't guess. We prove.
