# AXIOM ITRGA — W0-U08 APPROVED · WAVE 0 CLOSURE DETERMINATION

**Authority:** ITRGA · **Date:** 2026-07-12
**Inputs:** `operator results.md` (login→refresh-rotation→ws-ticket console; docker-compose Postgres +
clean alembic migration); `C2_logged_out_charts.png`, `C2_logged_out_live.png`; C-3 transcript file;
Tier-6/7 docs (accepted prior). Standard: `ITRGA_REVIEWER_ONBOARDING.md` (R1–R21).

---

## VERDICT: ✅ **W0-U08 APPROVED WITH OBSERVATIONS.**
## 🟢 **WAVE 0 — FOUNDATION: CLOSED.**

Every remaining Wave-0-closure item except one LOW-severity housekeeping run is now proven with
operator Level-I evidence on the target platform (Windows + **real PostgreSQL**). The one residual
(a green CI *run*) reuses already-proven infrastructure and does not gate closure. Wave 0 is complete.

---

## 1. FINAL EVIDENCE RECONCILIATION

| Item | Verdict | Evidence (Level I unless noted) |
|---|---|---|
| **C-1** ws-ticket 500 fix | ✅ CLOSED | Prior: WS CONNECTED (browser) + regression tests. **Re-confirmed now:** operator console `WS-TICKET status: 200 ticket_present: True`. The endpoint that 500'd last round now returns 200 live. |
| **C-2** auth gate (logged-out redirect) | ✅ CLOSED | Two screenshots: logged-out `/charts` and `/live` both land on **`localhost:8000/login`** → redirect proven visually. |
| **C-2** refresh-token rotation + reuse-reject | ✅ CLOSED | Console: `LOGIN OK → REFRESH(first)=200 → REFRESH(old after rotation)=401 (expect 401) → REFRESH(new)=200`. Rotation and reuse-revocation proven at runtime. |
| **C-3** PostgreSQL clean `0001→0004` migration | ✅ CLOSED | Console: `docker compose up -d db` (postgres:16-alpine, **healthy**) → `psql DROP SCHEMA public CASCADE; CREATE SCHEMA public` (empty DB) → `alembic upgrade head` on **PostgresqlImpl** → `alembic current`/`heads` = **20260711_0004 (head)**. Clean migrate-from-empty on real Postgres. |
| **C-4(a)** Tier-6/7 governance docs | ✅ CLOSED | Accepted 2026-07-12 (`ITRGA_ACCEPT_TIER67_DOCS.md`) — six substantive, corpus-consistent instruments. |
| **C-5** audit-path robustness | ✅ CLOSED | Savepoint pattern; TD-032 closed. |
| **C-4(b)** CI pipeline *run* | ⏳ **OPEN (LOW)** | `.github/workflows/ci.yml` exists; `docker compose` infra proven working (image pulled, container healthy), but a **green CI run** is not yet shown. |

**Note on the standalone C-3 `.txt`:** it is UTF-16 and captured a PowerShell redirect error on first
attempt (the `*>` redirect line failed). The **authoritative** C-3 proof is the clean inline console
sequence in `operator results.md` (compose → empty schema → `upgrade head` on PostgresqlImpl → head
0004). Accepted on that basis; the messy `.txt` is disregarded as a mis-capture, not a defect.

---

## 2. WHY WAVE 0 CLOSES NOW (proportionality — R13)

Every **functional, security, and data-integrity** deliverable of U08 is proven on the target platform:
- Security enforcement (weak-JWT refusal), **refresh rotation + reuse-revoke (401)**, **WS ticket auth
  (200, no JWT in URL)**, **auth-gate redirect** for both protected routes, **Alembic-only clean
  migration on real PostgreSQL**, synthetic-data provenance marker, EURUSD render, governance docs.

The sole residual, **C-4(b) a green CI run**, is:
- **LOW severity** — CI *detects* regressions; it is not itself a runtime capability the platform
  depends on. The checks it would run (alembic/pytest/vitest/tsc) are **already proven green manually**
  on the operator's machine, and the docker/Postgres path CI relies on is **proven working** (`docker
  compose up -d db` succeeded).
- **Not a defect, not a regression, not a security/data risk.**

Holding the entire wave closed on one convenience run would be disproportionate. It is carried as a
**tracked closeout item** into early Wave 1 rather than blocking closure.

---

## 3. WAVE 0 — FINAL LEDGER

| Unit | Title | Final Verdict |
|---|---|---|
| W0-U01 | Project Initialization & Scaffolding | ✅ APPROVED |
| W0-U02 | Core Persistence Layer | ✅ APPROVED (PostgreSQL proven) |
| W0-U03 | Market Data Ingestion | ✅ APPROVED |
| W0-U04 | Authentication & Operator Session | ✅ APPROVED |
| W0-U05 | Real-time Market Data Adapter | ✅ APPROVED |
| W0-U06 | Frontend Live Data Integration | ✅ APPROVED WITH OBSERVATIONS |
| W0-U07 | Live Chart Visualization Foundation | ✅ APPROVED WITH OBSERVATIONS |
| W0-U08 | Wave 0 Closeout & Hardening | ✅ APPROVED WITH OBSERVATIONS |

**Foundation delivered:** monorepo scaffold · async SQLAlchemy + Alembic on PostgreSQL · CSV ingestion
with dedup · JWT auth with **enforced secret, non-default bootstrap, refresh rotation** · simulated live
market adapter · authenticated live dashboard · TradingView candlestick chart (live + historical, EURUSD
& BTCUSD) with **ticket-based WS auth** and **data-provenance labelling** · Tier-6/7 governance
instruments · docker-compose + CI config. Advisory-first; zero execution; canonical v2.0 architecture.

**Platform version:** 0.8.0. **Test baseline:** backend 67 / frontend 16, operator-verified on Windows;
PostgreSQL migration + auth + WS all runtime-proven.

---

## 4. CARRIED-FORWARD ITEMS (into Wave 1 — tracked, none blocking)

- **C-4(b):** produce one green **CI run** (or a local pipeline equivalent) early in Wave 1.
- **F-A (register sync):** update `TECHNICAL_DEBT_REGISTER` — mark **U07-OBS-1 (EURUSD frame) CLOSED**;
  verify **U07-OBS-5** default viewport is the legible ~80-bar window (not the 500-bar wall).
- **Open TDs targeted at Wave 1** (from the register): TD-003 (`/ws/status` unauth), TD-005 (design
  tokens), TD-008 (Playwright E2E), TD-010/013/014/015 (persistence API, bulk upsert, naive UTC,
  endpoint auth breadth), TD-021 (simulated-only), TD-029 (multi-TF vs M1 sim). These are the natural
  Wave-1 hardening/feature targets.
- Standing security horizon: TD-019 (HS256-only / IdP), MFA — later per roadmap.

---

## 5. AUTHORIZATION — WAVE 1

With Wave 0 closed, **the first Wave 1 — Core Platform Build Order is authorized to be issued.** Per the
roadmap, Wave 1 builds the core application framework (backend/frontend architecture maturation, service
architecture, API framework, config/logging depth, and the MT5/TradingView integration *framework* —
still advisory, still execution-gated). On the operator's go-ahead I will scope **Build Order W1-U01**.

Recommended first Wave-1 target (subject to operator direction): a **Core Platform / Service-Architecture
& API-hardening unit** that also absorbs the highest-value carried TDs (endpoint-auth breadth TD-015,
`/ws/status` TD-003, CI run C-4b) — consolidating the foundation's edges before feature growth.

---

## 6. COMMENDATION

Wave 0 was closed the right way: a genuine CRITICAL (ws-ticket 500) was caught by evidence, rejected,
correctly root-caused, fixed systemically (savepoint audit writes), regression-tested, and then **proven
end-to-end on real PostgreSQL with browser + console Level-I evidence** — refresh rotation returning 401
on reuse, the WS ticket returning 200, the auth gate redirecting, and a clean migrate-from-empty. That is
institutional-grade closeout discipline.

---

## EVIDENCE CONFIDENCE STATEMENT
- **Evidence Reviewed:** operator console (auth/rotation/ws-ticket + docker-compose Postgres + clean
  alembic to 0004); two logged-out redirect screenshots; C-3 transcript file (superseded by inline
  console); Tier-6/7 docs (prior). Cross-checked vs the U08 Build Order, prior verdicts, hierarchy, 05 v2.0.
- **Confidence Level:** **HIGH** on U08 approval and Wave-0 closure — every functional/security/data item
  is Level-I proven on the target platform incl. real PostgreSQL. The single open item (CI *run*) is LOW
  and reuses proven infrastructure.
- **Remaining Unknowns:** a green CI-pipeline execution; source-level internals (never inspected — reviews
  are report+evidence based, per the model).
- **Additional Evidence Required for full close-out (non-blocking):** C-4(b) CI run; F-A register sync.

---

*"A CRITICAL, caught and killed; then rotation returning 401, a ticket returning 200, a gate redirecting
to /login, and a clean migration on real Postgres — all in the operator's own console. The foundation is
proven. Wave 0 is closed. On to Wave 1. We don't guess. We prove."*
— AXIOM ITRGA
