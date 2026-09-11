# AXIOM BUILD ORDER — W0-U08

## Wave 0 Closeout & Hardening

**Build Order ID:** W0-U08
**Wave:** 0 — Foundation · **Unit:** 08 (Wave-0 closeout)
**Version:** 1.0 · **Status:** ISSUED
**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Date Issued:** 2026-07-11
**Authorized By:** ITRGA, following U07 approval + Operator direction to harden Wave 0 before Wave 1.

**Governing Documents (canonical order per `10_CONSTITUTIONAL_HIERARCHY.md`):**
`00_VISION_AND_PRINCIPLES` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` →
`05_SYSTEM_ARCHITECTURE.md` **(v2.0, canonical)** → `06_ML_SPEC` / `07_UI_UX_SPEC` →
`UNIVERSAL_ITRGA_REVIEWER_DIRECTIVE.md`.

---

## 1. Purpose

This is a **debt-clearing and hardening unit**, not a feature unit. Its sole purpose is to close every
open Wave-0 residual — security, data-integrity, evidence, governance-documentation, and CI — so that
**Wave 1 (Core Platform) builds on a proven, secure, fully-governed foundation.** No new product
capability is introduced.

Rationale: Wave 1 will extend authentication, configuration, database, and services. Extending on top of
known-soft foundations (dev credentials, warning-only secrets, dual schema paths, missing governance
instruments) would propagate risk upward — which the roadmap forbids ("incomplete work shall never
propagate").

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No new features, no scope expansion.** No ML, no AI, no execution/trading, no new markets, no chart
  feature growth (indicators/drawings/replay). This unit only hardens and documents what exists.
- ❌ **No behavioral change to approved units beyond the specific hardening items below.** Refactors must
  be minimal and justified; approved behavior must be preserved (prove via the existing test suite).
- ✅ **Preserve** the single-uvicorn workflow, advisory-first posture, and canonical v2.0 architecture.
- ✅ **All changes recorded** in the technical-debt / decision / amendment registers.

---

## 3. Scope — Six Components (A–F)

### Component A — Security Hardening (HIGHEST PRIORITY) — closes OBS-3, OBS-5/TD-022
1. **Eliminate insecure defaults:** the dev bootstrap `admin/admin123` must no longer be a silent default.
   Require an explicit, environment-provided bootstrap credential (or a first-run setup flow); refuse to
   start — or start in a clearly-marked, non-networked dev-only mode — if a real credential is absent.
2. **Enforce the JWT secret:** replace the startup *warning* with **enforcement** — the app must refuse to
   run with a missing/weak/default `AXIOM_JWT_SECRET_KEY` outside explicit local-dev. Document minimum
   entropy.
3. **Refresh-token rotation + revocation:** implement rotation on refresh and a revocation/invalidation
   path (e.g., rotating refresh tokens with reuse detection, or server-side session/refresh store).
   Document the chosen model.
4. **WebSocket auth hardening (OBS-5/TD-022):** move the JWT off the query string to a subprotocol/header/
   short-lived ticket mechanism, so tokens aren't leaked in proxy/access logs. If a full migration is too
   large for this unit, deliver a documented interim mitigation + a scheduled follow-up, and justify.
5. Align with `05 v2.0` §75–77 (least privilege, secure-by-default, zero-trust, secret management).

### Component B — Persistence / Data-Integrity Hardening — closes OBS-4/TD-009, U07-OBS-3
1. **Single schema authority:** production must rely on **Alembic only**; `AUTO_CREATE_SCHEMA`/`create_all`
   must be disabled outside tests. Prove with a Postgres transcript that a clean DB migrates via Alembic
   `0001→0003` from empty (this also fully closes the earlier from-scratch-migration observation).
2. **Synthetic-data safety (U07-OBS-3):** seed/synthetic candles must persist a **clear, queryable
   non-authoritative marker** (e.g., `source` in {`seed`,`synthetic`} distinct from `live:simulated` and
   real ingested candles), and the UI must indicate when displayed data is synthetic. This is a
   pre-requisite safety control before any ML/analytics unit consumes candle history.

### Component C — Evidence Completeness (owed from U07) — closes U07-OBS-1, OBS-2, OBS-5, Wave-0 OBS-1
Provide the browser Level-I evidence still owed:
1. An **EURUSD** chart render frame after a symbol switch (cross-symbol render).
2. A **logged-out attempt at `/chart(s)`** showing block/redirect, **and** the same for **`/live`**
   (closes Wave-0 OBS-1 for the live dashboard gate).
3. A **legible default chart viewport** (recent-N bars) + a zoomed-in frame demonstrating distinguishable
   candles and working zoom/scroll (chart-readability, U07-OBS-5).

### Component D — Governance Documentation — closes OBS-7, F-4, U07-OBS-4
1. **Author/supply the missing constitutional instruments** named by the hierarchy but not yet present:
   `08_DEVELOPER_REASONING_FRAMEWORK.md`, `09_ITRGA_REASONING_FRAMEWORK.md` (Tier 6); and Tier-7:
   `QUALITY_GATE_SPEC.md`, `RISK_REGISTER.md`, `TECHNICAL_DEBT_REGISTER.md`, `GOVERNANCE_AMENDMENTS.md`.
   These must be real, usable documents consistent with the existing corpus (not placeholders).
2. **Citation alignment (F-4):** update U01–U07 governing-doc references to the canonical set (05 v2.0 +
   hierarchy); retire references to `03_AXIOM_SPEC_v1.1`, `AXIOM_SYSTEM_ARCHITECTURE_MERGED v1.1`,
   `GOVERNANCE_HIERARCHY.md`, and old ML/UI numbering.
3. **Route-name reconciliation (U07-OBS-4):** state the canonical chart route once; align docs/
   PROJECT_STATE/tests.
4. **Consolidate the technical-debt register** so every TD/OBS referenced across units has a single,
   current status (open/closed/scheduled) with target unit.

### Component E — CI / Reproducibility — closes TD-006
1. **Containerized dev stack:** `docker-compose.yml` bringing up **PostgreSQL + backend** for a one-command
   foundation (aligns with 05 v2.0 §63 Infrastructure-as-Code, environment consistency).
2. **CI pipeline:** automated run of `alembic upgrade head` (against Postgres), backend `pytest`, frontend
   `vitest`, and `tsc` on push — so regressions are caught automatically, not by manual operator runs.
   (This does not remove the operator-run evidence requirement for UI units; it complements it.)

### Component F — Verification & Delivery
1. **No regression:** the full existing suite (55 backend / 16 frontend) must still pass, plus new tests
   for the hardening (refresh-token rotation, secret enforcement refusal, WS-auth mechanism, synthetic-
   source marker, Alembic-only guard).
2. **Delivery Report** per §5, written to `UNIVERSAL_ITRGA_REVIEWER_DIRECTIVE.md` standard.

---

## 4. Success Criteria (Definition of Done)

- [ ] No insecure default credential path; JWT secret **enforced** (app refuses weak/missing outside dev).
- [ ] Refresh-token rotation + revocation implemented and tested.
- [ ] WS auth no longer leaks tokens via query string (or documented interim + scheduled fix, justified).
- [ ] Production schema is **Alembic-only**; clean-DB `0001→0003` migration transcript on PostgreSQL.
- [ ] Synthetic/seed candles carry a persisted, queryable non-authoritative marker; UI indicates synthetic.
- [ ] Owed U07 browser evidence supplied: EURUSD render, logged-out `/chart` + `/live` block, legible/zoom chart.
- [ ] Tier-6 + Tier-7 governance documents authored and consistent with the corpus.
- [ ] U01–U07 citations updated to canonical v2.0 + hierarchy; chart route name reconciled.
- [ ] `docker-compose` (Postgres + backend) + CI pipeline (alembic/pytest/vitest/tsc) working.
- [ ] Full existing suite green + new hardening tests; `tsc` clean; single-uvicorn preserved.
- [ ] Consolidated technical-debt register with current status per item.
- [ ] No new features / no scope expansion / approved behavior preserved.

---

## 5. Delivery Report & Evidence Requirements (MANDATORY)

Operator-run evidence on the target platform is required (report-claims are insufficient):
1. **Operator test console** (raw, with `collected N`): backend `pytest`, frontend `vitest`, `tsc` — no
   regression from 55/16, plus the new hardening tests.
2. **Security evidence:** show the app **refusing to start** with a missing/weak JWT secret (or default
   credential) outside dev; show a **refresh rotation** cycle (old refresh rejected after rotation); show
   the **WS auth** mechanism no longer carrying the token in the URL.
3. **PostgreSQL clean-migration transcript** (`0001→0003` from empty) with `AUTO_CREATE_SCHEMA` disabled.
4. **Synthetic-marker evidence:** a query/response showing seed candles tagged distinctly + a UI frame
   indicating synthetic data.
5. **Owed chart screenshots** (Component C).
6. **CI run** output (or config + a green run) proving the pipeline executes the four checks.
7. Confidence stated as HIGH/MODERATE/LIMITED with justification — **no fabricated percentages**.

---

## 6. Constraints & Standards

- Minimal-diff hardening; preserve approved behavior; reuse existing patterns/services.
- No secrets in code; least-privilege; align to 05 v2.0 §74–85 (security/governance).
- Cross-platform: operator runs Windows/PowerShell; container path must also work.
- Every change recorded in the (now-consolidated) technical-debt / decision / amendment registers.

---

## 7. Process

Implement → internal verify → doc sync → Delivery Report with §5 evidence → **submit to ITRGA** →
independent review → corrections if required → approval → **Wave 0 formally CLOSED** → then the first
**Wave 1 — Core Platform** Build Order is issued. The Development Authority does not self-approve or
self-authorize the next unit.

---

## 8. Priority Guidance

If the unit must be staged, order by risk: **A (security) → B (data integrity) → D (governance docs) →
C (owed evidence) → E (CI).** Security and data-integrity are the items Wave 1 will most directly build
upon and therefore must not carry forward unresolved.

---

*ITRGA — Close the foundation properly before building the next floor. We don't guess. We prove.*
