# AXIOM BUILD ORDER — W1-U01

## Core Platform: Service Architecture & API Hardening Foundation

**Build Order ID:** W1-U01
**Wave:** 1 — Core Platform · **Unit:** 01 (first Wave-1 unit)
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-12
**Authorized By:** ITRGA, following **Wave 0 CLOSURE** (`ITRGA_WAVE0_CLOSURE.md`) + Operator authorization.

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY.md`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` → **`05_SYSTEM_ARCHITECTURE.md` v2.0** →
`06_ML_SPEC` / `07_UI_UX_SPEC` → `08_DEVELOPER_REASONING_FRAMEWORK` / `09_ITRGA_REASONING_FRAMEWORK` →
Tier-7 (`QUALITY_GATE_SPEC`, `RISK_REGISTER`, `TECHNICAL_DEBT_REGISTER`, `GOVERNANCE_AMENDMENTS`) →
`UNIVERSAL_ITRGA_REVIEWER_DIRECTIVE.md`.

---

## 1. Purpose

Wave 1 builds the **Core Platform** (roadmap milestone: *Core Platform Operational*). This first unit
**consolidates and hardens the service/API architecture** on top of the closed Wave-0 foundation —
before feature growth — so the platform's edges are secure, its service boundaries are clean per
`05 v2.0`, and its highest-value carried debt is cleared. **It absorbs the Wave-0 carryover items** so
they do not propagate deeper into Wave 1.

This is primarily an **architecture-maturation + hardening** unit, not a large new-feature unit.

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No execution/trading/order/position logic.** MT5/broker work in this unit is **abstraction/
  framework only** — no real broker connection, no order path. Execution stays roadmap-gated (Wave 6 +
  governance gate; 05 v2.0 §15/§44).
- ❌ **No ML/AI product.** No model training/inference features (Wave 2+).
- ❌ **No chart feature expansion** (indicators/drawings/AI overlays remain future). Keep the existing
  W0-U07 chart working.
- ❌ **No regression of approved Wave-0 behavior.** Auth, persistence, ingestion, live adapter, live
  dashboard, chart, ticket-WS auth, provenance labelling must all still work (prove via the suite +
  targeted evidence).
- ✅ **Preserve:** advisory-first posture, single-uvicorn workflow, canonical v2.0 architecture, the
  Wave-0 security hardening (enforced secret, non-default bootstrap, refresh rotation, WS tickets,
  Alembic-only prod).

---

## 3. Scope — Components A–F

### Component A — Application Services layer (05 v2.0 §11.2) — architecture maturation
Establish/clarify the **Application Services** subsystem as a distinct bounded context that coordinates
workflows/session/command handling **without** containing market intelligence or business-domain
calculation. Refactor existing routers so **business logic lives in services, not controllers** (thin
routers / fat services), with dependency-inward wiring and interface-based access to Core Platform
Services. No behavior change to approved endpoints — this is structural consolidation with tests proving
parity.

### Component B — API authorization breadth (closes TD-015, TD-003) — SECURITY
1. **Audit every endpoint** and classify each as public (health/readiness/login only) vs.
   operator-authenticated. Bring currently-unauthenticated operational endpoints behind the auth
   dependency. Deliver an **endpoint inventory** (path · method · auth required · rationale).
2. **`/ws/status` (TD-003):** authenticate it or explicitly justify a narrowly-scoped public status
   (and document what it may/may not reveal). No unauthenticated endpoint may leak operator/system detail.
3. Apply consistent authorization via a single reusable dependency; no ad-hoc per-route auth.

### Component C — Time & data correctness (closes TD-014) — DATA INTEGRITY
Enforce **timezone-aware UTC** end-to-end (storage, API, serialization). Replace naive datetimes; add a
regression test proving timestamps are tz-aware UTC across candle/ingestion/audit/auth paths. This
matters before Wave-2 ML consumes candle history (naive-vs-aware bugs are a classic leakage/label hazard).

### Component D — Persistence service maturation (closes TD-010) — architecture
Mature the minimal persistence API into a proper **service-layer** interface (repository → service →
API), with transaction/session discipline per 05 v2.0 §23 (persistence logic isolated behind repository
interfaces; no DB details beyond repositories). Keep scope foundational — no new domain tables beyond
what's needed; this is layering/robustness, not feature growth.

### Component E — CI green run (closes Wave-0 carryover C-4b) + register sync (F-A)
1. Produce **one green CI pipeline run** (`.github/workflows/ci.yml`: alembic-on-Postgres · pytest ·
   vitest · tsc) — or a documented local equivalent if GitHub is unavailable — as evidence the automated
   gate actually executes. This closes the last Wave-0 residual.
2. **Sync `TECHNICAL_DEBT_REGISTER`:** mark U07-OBS-1 (EURUSD frame) CLOSED; verify/record U07-OBS-5
   default viewport is the legible window; reconcile any other stale statuses.

### Component F — Verification & Delivery
- Full existing suite green (backend 67 / frontend 16 baseline) **plus** new tests for A–D (service-layer
  parity, endpoint-auth coverage, tz-aware UTC, persistence-service transactions).
- Delivery Report per §5, written to `09_ITRGA_REASONING_FRAMEWORK` / `UNIVERSAL_ITRGA_REVIEWER_DIRECTIVE`
  standard.

### Explicitly OUT of scope
MT5 real connection/execution; ML training/inference; chart feature growth; new markets; RBAC beyond
existing roles (ABAC/MFA remain future, TD-019); design-token migration (TD-005) unless trivially
incidental. Record anything deferred in the debt register.

---

## 4. Success Criteria (Definition of Done)

- [ ] Application Services layer established as a clean bounded context; routers thin, business logic in
      services; **no approved-endpoint behavior change** (parity tests pass).
- [ ] Endpoint inventory delivered; **all operational endpoints authenticated** (or public status
      explicitly justified + scoped); `/ws/status` resolved (TD-003).
- [ ] **tz-aware UTC** enforced end-to-end with a regression test (TD-014).
- [ ] Persistence matured to a service-layer interface with transaction discipline (TD-010).
- [ ] **One green CI run** (or documented local equivalent) covering alembic-on-Postgres/pytest/vitest/tsc
      (C-4b).
- [ ] Technical-debt register synced (F-A) with accurate statuses.
- [ ] No execution/ML/chart-expansion; advisory-first + Wave-0 security hardening preserved.
- [ ] Full suite green + new tests; `tsc` clean; single-uvicorn preserved; conforms to 05 v2.0.

---

## 5. Delivery Report & Evidence Requirements (MANDATORY — operator-run, target platform)

1. **Operator test console** (raw, with `collected N`): backend `pytest`, frontend `vitest`, `tsc` — no
   regression from 67/16 + the new tests.
2. **Endpoint-auth evidence:** a transcript showing previously-open operational endpoints now returning
   **401 without a token** and **200 with** (spot-check the ones changed, incl. `/ws/status` handling).
3. **tz-aware UTC evidence:** a query/response (or test output) showing tz-aware UTC timestamps.
4. **CI evidence:** a green pipeline run (screenshot/log) or the documented local-equivalent transcript.
5. **Parity evidence:** confirmation the Wave-0 capabilities still work (a quick live smoke: login →
   chart/live feed → WS ticket 200) — no regression.
6. Confidence stated **HIGH/MODERATE/LIMITED with justification — no fabricated percentages** (per 09
   framework).

---

## 6. Standards & Constraints
Clean architecture / SRP / dependency-inward / bounded contexts (05 v2.0 §10–16); no business logic in
infra services (§32–34); no secrets in code; least privilege (§75–77); every change recorded in the
debt/decision/amendment registers; cross-platform (Windows/PowerShell + docker path); minimal-diff where
refactoring approved behavior (prove parity).

---

## 7. Process
Implement → internal verify → doc sync (PROJECT_STATE + registers + ADRs) → Delivery Report with §5
evidence → **submit to ITRGA** → independent review → corrections if required → approval → next Build
Order. The Development Authority does not self-approve or self-authorize the next unit.

---

## 8. Priority Guidance (if staged)
**B (endpoint auth) → C (tz-UTC) → A (service layer) → D (persistence service) → E (CI + register).**
Security and data-correctness are what Wave-1 features will most build upon; clear them first.

---

*ITRGA — Wave 0 is closed; Wave 1 begins by hardening the seams before we widen them. We don't guess. We prove.*
