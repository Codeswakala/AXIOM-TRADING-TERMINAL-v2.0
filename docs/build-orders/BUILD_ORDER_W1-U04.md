# AXIOM BUILD ORDER — W1-U04

## Wave 1 Closure & Hardening: Green CI Run · Frontend Supply-Chain Remediation · "Core Platform Operational" Milestone

**Build Order ID:** W1-U04
**Wave:** 1 — Core Platform · **Unit:** 04 (Wave-1 **closure/hardening** unit)
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-13
**Authorized By:** ITRGA, following **W1-U03 APPROVED WITH OBSERVATIONS** (Platform v0.11.0) + explicit Operator authorization ("wave 1 hardening unit authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY.md`):**
`00_VISION_AND_PRINCIPLES` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` → **`05_SYSTEM_ARCHITECTURE.md` v2.0 (CANONICAL)** →
`06_ML_SPEC` / `07_UI_UX_SPEC` → `08_DEVELOPER_REASONING_FRAMEWORK` / `09_ITRGA_REASONING_FRAMEWORK` →
Tier-7 (`QUALITY_GATE_SPEC`, `RISK_REGISTER`, `TECHNICAL_DEBT_REGISTER`, `GOVERNANCE_AMENDMENTS`, `PROJECT_STATE`) →
`UNIVERSAL_ITRGA_REVIEWER_DIRECTIVE.md`.

---

## 1. Purpose

**Close Wave 1 cleanly.** With Service architecture (W1-U01), Observability + CI gate (W1-U02), and the
MT5 integration framework (W1-U03) delivered, every *named* "Core Platform" component in
`04_PROJECT_ROADMAP` is built. This unit does **not** add product behavior — it **discharges the two
tracked residuals that outlived their originating units** and then formally declares the roadmap milestone
**"Core Platform Operational."**

The two residuals are the *only* mandatory deliverables of substance:
1. **OBS-3 — the real green CI *run*** (owed since W1-U02; the platform's oldest residual). Every gate is
   already proven green *manually* on target; this unit must prove them green **as one orchestrated,
   fail-closed pipeline run**.
2. **OBS-4 / TD-012 / R-FE-01 — the frontend supply-chain vulnerabilities** (npm audit: **1 critical, 1
   high**, +3 moderate). Risk-assessed in W1-U03 but **not remediated.** This unit must **remediate them —
   or, only if remediation is genuinely infeasible, file a written, time-boxed governance exception** with
   a named owner and expiry. A *critical* may not be carried a third time silently.

This is a **tooling / supply-chain / governance-closure** unit. It hardens and finalizes; it adds no new
markets, ML/AI, chart features, broker behavior, or execution.

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No new product behavior.** No new markets (§5 unchanged), no ML/AI, no chart features, no new API
  surface beyond what CI/health needs.
- ❌ **No broker connection, no execution, no orders, no credentials.** The W1-U03 Governance Gate stays
  **CLOSED and enforced**; this unit must not weaken, bypass, or add an override to it. A dependency bump
  must not accidentally introduce a broker/execution path.
- ❌ **No secrets in code/config/logs/CI.** CI must inject secrets via the runner's secret store / env —
  never commit a JWT secret, DB password, or token into `ci.yml`, fixtures, or logs (05 v2.0 §77;
  W1-U02 redaction standard). CI logs must not print secrets.
- ❌ **No regression of any approved capability** (Wave-0 + W1-U01 + W1-U02 + W1-U03). A dependency
  upgrade that breaks a test, the build, or a runtime path is a finding, not a footnote — prove the full
  suite + parity smoke still green **after** remediation.
- ✅ **Preserve:** advisory/research-first, single-uvicorn, canonical v2.0 boundaries, and **all** prior
  hardening (enforced secret, non-default bootstrap, refresh rotation, WS tickets, endpoint auth, tz-aware
  UTC, structured logging + redaction + correlation, metrics/health, broker gate closed).

---

## 3. Scope — Components A–D

### Component A — Green CI Run (closes OBS-3, the long-owed C-4b/OBS-2 carryover)
Deliver a **single orchestrated pipeline that actually runs green**, fail-closed on any failure, covering
**all** gates:
- **`alembic upgrade head` against PostgreSQL** (a real PG **service container**, not SQLite) — the same
  `0001→0004` path proven manually on target;
- **backend `pytest`** (currently **88** — must stay green, 0 failed);
- **backend `ruff`**;
- **frontend `vitest`** (currently **16**), **`tsc`/type-check**, and **`vite build`**;
- **frontend `npm audit`** gate at an agreed threshold (see Component B — after remediation this gate
  should pass at "no critical/high," or be explicitly configured with the documented exception).
Requirements:
- The pipeline **must fail the build on any single failure** (prove it fails-closed — e.g. a screenshot/
  log of an intentional red run, or a description of the failing behavior, is welcome but at minimum the
  config must demonstrably gate on exit codes).
- Provide a **real green run** — GitHub Actions (or the project's chosen runner) **run log/URL or
  screenshot**. If remote CI is truly unavailable, a **single documented local orchestration script**
  (one command runs every gate against PostgreSQL and returns non-zero on any failure) executed by the
  operator and shown green is the fallback — but the standing goal, now overdue, is a **real remote run**.
- No secrets committed; CI reads secrets from the runner secret store.

### Component B — Frontend Supply-Chain Remediation (closes OBS-4 / TD-012 / R-FE-01)
- Run `npm audit` and **remediate the critical and high** vulnerabilities (and moderates where feasible):
  `npm audit fix` / targeted dependency upgrades / `overrides` as appropriate.
- **After remediation, prove:** a fresh `npm ci` + `npm audit` showing **0 critical, 0 high** (moderates,
  if any remain, listed and justified); **and** `vitest 16` + `tsc` + `vite build` **still green** (no
  regression from the upgrade).
- **If — and only if — a critical/high cannot be remediated** (e.g. no fixed version exists), file a
  **written, time-boxed governance exception** in `RISK_REGISTER`/`GOVERNANCE_AMENDMENTS`: the specific
  advisory, why it is not exploitable in AXIOM's usage, a named owner, and an **explicit expiry date**.
  "Deferred to a future unit" without an expiry is **not** acceptable this time.
- **Correct the register severity:** `TECHNICAL_DEBT_REGISTER` currently lists TD-012 as "Low–Med," but
  the actual audit is **1 critical / 1 high** — reconcile the recorded severity to reality, then mark
  Closed (or Exception-tracked) with evidence.

### Component C — Register & Milestone Sync (governance closure)
- **`TECHNICAL_DEBT_REGISTER`:** mark **TD-006/CI** fully closed *with the green-run evidence*; mark
  **TD-012** Closed (or Exception-tracked); reconcile any stale Wave-0 observations (U07-OBS-2 logged-out
  screenshots if still open, U07-OBS-1/OBS-5 statuses) — clear or explicitly carry with a reason.
- **`RISK_REGISTER`:** land **R-FE-01** formally (it was added in the DA workspace during W1-U03 but is
  not in the canonical register); confirm **R-PROD-01** (premature broker/execution) remains *Controlled*
  by the W1-U03 gate; confirm R-SEC-01/02 statuses.
- **`PROJECT_STATE` + `04_PROJECT_ROADMAP`:** record all named Wave-1 Core Platform components delivered
  and, once A–C are proven, **declare the "Core Platform Operational" milestone** (the Wave-1 milestone in
  the roadmap). Bump platform version.
- **OBS-1 (synthetic-candle chronology):** re-affirm as a standing note carried **into Wave 2** (the first
  ML unit must not train on forward-dated synthetic candles as if real). Not closed here — explicitly
  hand it forward.
- **ADR** (optional but recommended): record the CI design + the audit-gate/exception policy.

### Component D — Verification & Delivery
- Full suite green **after** remediation: backend **88** / frontend **16** — 0 failed, no regression.
- Broker gate still **CLOSED** (re-run `test_broker_integration.py -vv`, 7 passed) — prove the dependency
  changes did not weaken it.
- Parity smoke green (login → WS ticket 200 → live feed → candle fetch).
- Delivery Report per §5.

### Explicitly OUT of scope (defer / hand forward)
Any new product feature; new markets; ML/AI; chart features; real MT5 adapter / broker connection /
execution (Wave 6); TradingView deepening; RBAC/MFA. This unit closes Wave 1 — it does not open Wave 2.

---

## 4. Success Criteria (Definition of Done)

- [ ] **A single orchestrated CI pipeline runs GREEN**, fail-closed, covering alembic-on-**PostgreSQL** /
      pytest / ruff / vitest / tsc / build / npm-audit — with a **real run log/URL/screenshot** (OBS-3
      closed).
- [ ] **Frontend `npm audit` shows 0 critical / 0 high** after remediation (moderates listed+justified),
      **or** a written time-boxed exception with named owner + expiry exists for any unfixable item
      (OBS-4 / TD-012 / R-FE-01 closed or exception-tracked).
- [ ] **No regression:** backend 88 / frontend 16 green after the dependency changes; `tsc` + build clean.
- [ ] **Broker Governance Gate still CLOSED & enforced** (`test_broker_integration.py` 7 passed); no
      override introduced; no broker/execution path added by any dependency change.
- [ ] Registers reconciled (TD-006/TD-012 severity+status, R-FE-01 landed, R-PROD-01 Controlled);
      `PROJECT_STATE` + roadmap updated; **"Core Platform Operational" milestone declared**; version bumped.
- [ ] OBS-1 explicitly handed forward to Wave 2; no secrets in code/config/CI/logs; advisory-first + all
      prior hardening intact; conforms to 05 v2.0 (§77 especially).

---

## 5. Delivery Report & Evidence Requirements (MANDATORY — operator-run, target platform)

Per the reinforced standard (sandbox-green ≠ target-proven; a runtime failure/red gate in evidence
overrides any report claim; a failing test/red gate inside the evidence is a finding, not a footnote):

1. **Green CI run evidence:** the actual run — GitHub Actions run **URL/log or screenshot** (preferred),
   showing every gate green including **alembic-on-PostgreSQL**; or the operator-run local-orchestration
   fallback shown green with the single command + its exit status. Fail-closed behavior demonstrated.
2. **npm-audit before/after:** the original audit (1 critical/1 high visible) **and** the post-remediation
   `npm ci` + `npm audit` showing **0 critical / 0 high** — or the exception record if unfixable.
3. **Post-remediation frontend proof:** `vitest` 16 passed + `tsc` clean + `vite build` success **after**
   the dependency changes (proving no regression from the upgrade).
4. **Operator backend proof:** `pytest` **88 passed, 0 failed** on Windows + PostgreSQL; `ruff` clean.
5. **Broker-gate-intact proof:** `pytest tests/test_broker_integration.py -vv` → **7 passed** after the
   changes (gate still refuses connect + execute).
6. **Register/milestone evidence:** the reconciled `TECHNICAL_DEBT_REGISTER`/`RISK_REGISTER` rows and the
   `PROJECT_STATE`/roadmap "Core Platform Operational" declaration.
7. **Parity smoke:** login → WS ticket 200 → live feed → candle fetch, unaffected.
8. Confidence stated **HIGH / MODERATE / LIMITED with justification — NO fabricated percentages.**

---

## 6. Standards & Constraints

Supply-chain hygiene (05 v2.0 §77 / R21): no known critical/high vulnerabilities shipped without an
explicit, time-boxed, owner-named exception; **no secrets in code/config/CI/logs**; least privilege in CI
(secrets from the runner store). CI must be **fail-closed** and cover the real target datastore
(PostgreSQL, not SQLite). No regression; tz-aware UTC preserved; broker gate authority preserved. Every
change recorded in the debt/decision/amendment registers (R20). Cross-platform (Windows + docker/PG).

---

## 7. Process

Remediate + build CI → internal verify (full suite + audit + gate + build) → doc sync (PROJECT_STATE +
registers + roadmap milestone + ADR) → Delivery Report with §5 evidence (operator-run, green pipeline,
0 critical/high, gate intact, no failing tests) → **submit to ITRGA** → independent review → corrections
if required → approval → **Wave 1 formally CLOSED** → await operator authorization for the first Wave-2
Build Order. **The DA does not self-approve, does not self-authorize Wave 2, and does not open the broker
gate.**

---

## 8. Priority Guidance (if staged)

**B (remediate frontend criticals/highs) → D-partial (prove no regression from the bump) → A (green CI
run, now including the passing audit gate) → C (registers + "Core Platform Operational" milestone).**

Remediate *before* wiring the audit gate into CI, so the green pipeline reflects a genuinely-clean tree —
not a gate lowered to accommodate a known critical. The green CI run (OBS-3) is the headline deliverable
and is overdue; the supply-chain remediation (OBS-4) is the highest *security* risk. Neither may be
faked, deferred without expiry, or shown as anything less than actually green.

---

*ITRGA — Close the wave the way it was built: proven, not promised. A green pipeline you can point to, a
dependency tree with no known critical, and a milestone earned on evidence. Then — and only then — Wave 1
is done. We don't guess. We prove.*
