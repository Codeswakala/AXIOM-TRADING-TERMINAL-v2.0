# AXIOM

**Institutional multi-market AI research and trading intelligence platform**

| Item | Value |
|------|-------|
| Version | v0.62.0 |
| Roadmap status | Waves 0–7 complete; final milestone declared |
| Current phase | TD-AXIOM-GIT-PROVENANCE remediation — Amendment 4 final operator-run baseline execution prepared |
| Architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` v2.0 |
| Status | UI-007 Governance & Evidence Workspace COMPLETE; provenance remediation submission is prepared under ITRGA Amendment 4 but no baseline commit/tag exists yet; production deployment not certified |

AXIOM augments human judgment with transparent, evidence-based market analysis. It is **not** a guaranteed profit system, signal-selling product, or black-box trading bot.

## Current governed capability

Wave 3 is closed and residual-free. Wave 5 is closed by ITRGA and the **Human-AI Collaborative Workspace Complete** milestone is declared at platform v0.46.0. Wave 6 is closed by ITRGA and the **Execution Research Environment Complete** milestone is declared at platform v0.54.0. Wave 7 is closed by ITRGA and the **Institutional Platform Complete** milestone is declared at platform v0.62.0. The implementation roadmap is complete. The Institutional UI Transformation is governed as a separate presentation programme. UI-007-P04 and UI-007-P05 are **Approved with Observations** at baseline backend 414 / frontend 60 files and 271 tests. UI-007-P06 is **Approved with Observations** and ITRGA has declared UI-007 — Governance & Evidence Workspace **COMPLETE** at backend 414 / frontend 61 files and 276 tests. `OBS-P06-2` remains a tracked audit-reachability residual. The subsequent provenance-remediation Build Order is authorized but halted at its mandatory credential-scan clarification; no baseline commit or tag has been made. UI-007 completion does not open a Gate or authorize production. Runtime readiness remains explicitly distinct from **Production NOT CERTIFIED / Doc 11 HELD**. Production deployment remains subject to `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md`.

- governed model eligibility and deterministic inference;
- inert advisory signal persistence;
- emit-time domain/calibration/economic/staleness guardrails;
- live-market inference adapter using the existing simulated live seam;
- operator advisory signal workspace;
- inert monitoring/drift/health alerts;
- advisory performance analytics with uncertainty and calibrated confidence;
- closeout evidence index and hardening evidence pack;
- Institutional Intelligence foundation and correlation research reports;
- non-actuating Human-AI collaboration foundation and audited assistant response/refusal records;
- inert chart research annotations/drawing tools with source linkage and no execution controls;
- read-only signal investigation workspace for rationale, guardrails, lineage, calibrated confidence, and linked intelligence reports;
- read-only scenario comparison workspace over existing persisted scenario reports;
- inert trade plan research notes with audited persistence and no order-ticket controls;
- inert manual research journal entries with audited persistence and no broker/account/execution/P&L fields;
- Wave-5 closeout evidence indexes for prompt-injection proof and artifact-audit completeness;
- Wave-6 SIMULATED execution research runs and deterministic simulated fill events;
- Wave-6 SIMULATED paper research ledger entries with uncertainty-bearing return estimates;
- Wave-6 SIMULATED execution-risk research reports with structured metrics, uncertainty, and economic-usefulness separation;
- Wave-6 immutable pre-registered simulated replay experiments with as-of bounded input lineage;
- Wave-6 simulated execution analytics reports with full-scope inclusion, uncertainty, and stat/economic separation;
- Wave-6 display-only execution research workspace UI with SIMULATED labels and no actuation controls;
- Wave-6 closeout evidence index for full-wave no-live-execution, Gate-CLOSED, no-orphan audit, and browser E2E proofs;
- Wave-7 institutional platform security/API foundation with default-deny RBAC and operator isolation;
- Wave-7 per-operator workspace preferences for layout/theme/visible modules;
- Wave-7 reference-only research management collections and tags over existing governed artifacts;
- Wave-7 authenticated API catalogue and research API hardening with no actuation surface;
- Wave-7 plugin contract safety foundation with contracts/refusal only and no dynamic plugin execution;
- Wave-7 hypothetical portfolio research dashboard and generated advanced reporting/export preview;
- Wave-7 enterprise readiness hardening with RBAC/isolation/redaction/audit re-proof;
- Wave-7 closeout and whole-project completion checkpoint evidence;
- UI-001-P01 institutional workspace shell skeleton and workspace registry;
- UI-001-P02 registry-driven Navigation Dock and workflow routing seam;
- UI-001-P03 registered panel infrastructure, deterministic docking primitives, and session layout seam;
- UI-001-P04 shell layout persistence via existing operator workspace preferences;
- UI-001-P05 shell-owned overlay/dialog/notification layers, command palette, and token hardening.

The platform remains advisory-only. AXIOM still has **no execution**, no broker dispatch, no order payload, no paper trading, no position path, no automatic remediation, no auto-retraining, no guaranteed-return framing, and the Constitutional Governance Gate remains CLOSED.

## Repository layout

```text
axiom/
├── backend/                 # FastAPI application
│   └── app/
│       ├── api/             # API layer (thin routers)
│       ├── auth/            # Operator auth, JWT, refresh rotation, WS tickets
│       ├── core/            # Config, logging, DI, time utilities
│       ├── db/              # SQLAlchemy models/session
│       ├── ingestion/       # Historical CSV ingestion
│       ├── market/          # Simulated live adapter + WS hub
│       ├── ml/              # ML research framework and governance services
│       ├── models/          # Pydantic schemas
│       ├── services/        # Application/domain services
│       ├── repositories/    # Persistence boundary
│       ├── trading_intelligence/ # Live inference, signal, monitoring, analytics, and live-market services
│       ├── institutional_intelligence/ # Wave-4 intelligence artifact contracts and foundations
│       └── collaboration/             # Wave-5 assistant and collaboration safety contracts
├── frontend/                # React + TypeScript operator terminal
├── docs/                    # Governance, ADRs, build orders, evidence
├── scripts/                 # Developer utilities
├── PROJECT_STATE.md
└── CHANGELOG.md
```

## Quick start

**Operators on Windows (VS Code + PowerShell):** follow the full runbook:

→ **[`PROJECT_LAUNCHER.md`](PROJECT_LAUNCHER.md)**

### Single process after setup

```powershell
cd frontend
npm run build

cd ..\backend
.\.venv\Scripts\Activate.ps1
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open **http://localhost:8000/login** and sign in with the explicit bootstrap/operator credentials configured in `backend/.env`.

### Tests

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pytest -q

cd ..\frontend
npm test
npx tsc -b --pretty false
npm run build
```

## Current authentication posture

- Strong `AXIOM_JWT_SECRET_KEY` required outside explicit local/test escape hatch.
- Bootstrap admin is disabled by default and must be explicitly configured.
- Operational REST endpoints require Bearer authentication.
- Signal history, alerts API, analytics API, advisory dashboard, analytics view, and Operations alert panel require operator authentication.
- Live/status WebSockets use short-lived one-time tickets from `POST /api/v1/auth/ws-ticket`.
- Production schema management is Alembic-only.

## Governance

- Build Orders are issued by ITRGA; the Development Authority implements and submits for review.
- Wave 0 is closed by ITRGA: `docs/build-orders/ITRGA_WAVE0_CLOSURE.md`.
- W3-U08 Build Order: `docs/build-orders/BUILD_ORDER_W3-U08.md`.
- W3-U08 Final Verdict / Wave-3 Closure: `docs/build-orders/ITRGA_VERDICT_W3-U08_FINAL_AND_WAVE3_CLOSURE.md`.
- W3-U08.1 Final Verdict: `docs/build-orders/ITRGA_VERDICT_W3-U08.1_FINAL.md`.
- Wave-4 Design Plan: `docs/plans/WAVE4_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md`.
- W4-U01 Review: `docs/build-orders/ITRGA_REVIEW_W4-U01.md`.
- Wave-5 Design Review: `docs/build-orders/ITRGA_REVIEW_WAVE5_DESIGN_PLAN.md`.
- W5-U01 Review: `docs/build-orders/ITRGA_REVIEW_W5-U01.md`.
- W5-U02 Review: `docs/build-orders/ITRGA_REVIEW_W5-U02.md`.
- W5-U03 Review: `docs/build-orders/ITRGA_REVIEW_W5-U03.md`.
- W5-U04 Review: `docs/build-orders/ITRGA_REVIEW_W5-U04.md`.
- W5-U08 Final Verdict / Wave-5 Closure: `docs/build-orders/ITRGA_VERDICT_W5-U08_FINAL_AND_WAVE5_CLOSURE.md`.
- W6-U08 Final Verdict / Wave-6 Closure: `docs/build-orders/ITRGA_VERDICT_W6-U08_FINAL_AND_WAVE6_CLOSURE.md`.
- Wave-7 Design Review: `docs/build-orders/ITRGA_REVIEW_WAVE7_DESIGN_PLAN.md`.
- W7-U01 Final Verdict: `docs/build-orders/ITRGA_VERDICT_W7-U01_FINAL.md`.
- W7-U02 Build Order: `docs/build-orders/BUILD_ORDER_W7-U02.md`.
- W7-U02 Final Verdict: `docs/build-orders/ITRGA_VERDICT_W7-U02_FINAL.md`.
- W7-U03 Build Order: `docs/build-orders/BUILD_ORDER_W7-U03.md`.
- W7-U03 Final Verdict: `docs/build-orders/ITRGA_VERDICT_W7-U03_FINAL.md`.
- W7-U04 Build Order: `docs/build-orders/BUILD_ORDER_W7-U04.md`.
- W7-U04 Final Verdict: `docs/build-orders/ITRGA_VERDICT_W7-U04_FINAL.md`.
- W7-U05 Approval Review: `docs/build-orders/ITRGA_REVIEW_W7-U05.md`.
- W7-U06 Final Verdict: `docs/build-orders/ITRGA_VERDICT_W7-U06_FINAL.md`.
- W7-U07 Final Verdict: `docs/build-orders/ITRGA_VERDICT_W7-U07_FINAL.md`.
- W7-U08 Build Order: `docs/build-orders/BUILD_ORDER_W7-U08.md`.
- W7-U08 Final Verdict / Wave-7 Closure: `docs/build-orders/ITRGA_VERDICT_W7-U08_FINAL_AND_WAVE7_CLOSURE.md`.
- Production readiness certification authority: `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md`.
- UI-001-P01 Build Order: `docs/build-orders/BUILD_ORDER_UI-001-P01.md`.
- UI-001-P01 ITRGA Review: `docs/build-orders/ITRGA_REVIEW_UI-001-P01.md`.
- UI-001-P02 Build Order: `docs/build-orders/BUILD_ORDER_UI-001-P02.md`.
- UI-001-P02 Review: `docs/build-orders/ITRGA_REVIEW_UI-001-P02.md`.
- UI-001-P03 Review: `docs/build-orders/ITRGA_REVIEW_UI-001-P03.md`.
- UI-001-P04 Review: `docs/build-orders/ITRGA_REVIEW_UI-001-P04.md`.
- UI-001-P05 Build Order: `docs/build-orders/BUILD_ORDER_UI-001-P05.md`.
- Current UI evidence command pack: `docs/evidence/UI-001-P05_OPERATOR_EVIDENCE_COMMANDS.md`.
- Wave-6 Closeout Evidence Index: `docs/evidence/W6-U08_WAVE6_CLOSEOUT_EVIDENCE_INDEX.md`.
- Wave-5 Closeout Evidence Index: `docs/evidence/W5-U08_WAVE5_CLOSEOUT_EVIDENCE_INDEX.md`.
- Closeout evidence index: `docs/evidence/W3-U08_WAVE3_CLOSEOUT_EVIDENCE_INDEX.md`.
- Canonical architecture: `docs/governance/05_SYSTEM_ARCHITECTURE.md` v2.0.

## Out of current scope

Real broker/MT5 connection, live execution/order/position logic, real account/balance/margin/capital integration, real P&L, live/paper trading ledger, automatic remediation, auto-retraining, external LLM/API integration, external notification providers, external market-data-provider integration, broker/account journal import, trade-plan-to-execution conversion, new scenario generation, advanced chart feature expansion, and post-roadmap work and production deployment remain governance-gated; production deployment requires ITRGA certification under `11_PRODUCTION_READINESS_CERTIFICATION.md`.
