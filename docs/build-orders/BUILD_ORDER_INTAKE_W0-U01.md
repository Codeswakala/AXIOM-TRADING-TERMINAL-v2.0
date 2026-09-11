# Build Order Intake Assessment — W0-U01

| Item | Value |
|------|--------|
| Build Order ID | W0-U01 |
| Title | Project Initialization & Foundation Scaffolding |
| Wave / Unit | Wave 0 — Foundation / Unit 01 |
| Issued By | ITRGA |
| Date Issued | 2026-07-10 |
| Intake By | Development Authority |
| Intake Date | 2026-07-10 |
| Status | ACCEPTED — IMPLEMENTATION AUTHORIZED |

---

## 1. Acknowledgement

The Development Authority acknowledges receipt of Build Order **W0-U01** and accepts authorization to implement within the defined scope.

---

## 2. Objectives Understood

1. Professional governance-compliant project structure  
2. Minimal production-aligned backend (FastAPI) + frontend (React/TS) scaffolding  
3. Configuration management  
4. Observability (logging, health)  
5. Initial EKMS artifacts  
6. Initial `PROJECT_STATE.md`  
7. Documentation synchronization  
8. Minimal end-to-end health demonstration  
9. Repeatable test/documentation/delivery patterns  

---

## 3. Scope Boundaries

| In Scope | Out of Scope |
|----------|--------------|
| Repo structure, backend health, frontend dark shell | ML pipelines |
| Config, logging, DI foundation | Trading, charting, market data |
| Frontend↔backend health integration | Broker integration |
| EKMS, PROJECT_STATE, CHANGELOG, Delivery Report | Full auth, production deploy, containers |
| Unit + integration tests | Live/external data |

---

## 4. Governing Document Mapping

Build Order cites some filenames that differ from the workspace corpus. DA maps as follows (domain precedence applies):

| Build Order Reference | Workspace Authority |
|----------------------|---------------------|
| AXIOM_SYSTEM_ARCHITECTURE_MERGED.md (v1.1) | `governance/SYSTEM_ARCHITECTURE.md` v1.1.0 |
| 03_AXIOM_SPEC_v1.1.md | `uploads/03_AXIOM_SPEC.md` (v1.0 active; note version delta) |
| GOVERNANCE_HIERARCHY.md | `governance/DOCUMENT_PRECEDENCE.md` |
| 04_PROJECT_ROADMAP.md | `uploads/04_PROJECT_ROADMAP.md` |
| 02_DESIGN_PHILOSOPHY.md | `uploads/02_DESIGN_PHILOSOPHY.md` |
| 07_ML_SPEC.md | `uploads/07_ML_SPEC.md` (no ML implementation this unit) |
| 08_UI_UX_SPEC.md | `uploads/08_UI_UX_SPEC.md` |
| 00_VISION_AND_PRINCIPLES.md | `uploads/00_VISION_AND_PRINCIPLES.md` |

**Assumption (documented):** Filename differences are citation aliases; content authority is the active domain document in workspace. No AXIOM_SPEC v1.1 file was provided — DA proceeds under v1.0 content unless a later update notice is issued.

---

## 5. Architecture Alignment

Scaffolding will reflect merged architecture:

```
Presentation  → frontend/
Application   → backend/app/api + core
Business      → backend/app/services (stubs)
ML/Research   → backend/app/ml (stub package only — no logic)
Data          → backend/app/repositories (stub)
Infrastructure→ backend/app/core (config, logging)
```

---

## 6. Risks (Unit-Level)

| Risk | Severity | Mitigation |
|------|----------|------------|
| Spec filename/version mismatch (v1.1 cited, v1.0 present) | Medium | Map + record in Delivery Report; no invented v1.1 content |
| Node/Python toolchain availability | Medium | Use available runtimes; pin deps; document |
| Scope creep into charts/auth | High | Strict checklist against §3 Out of Scope |
| WebSocket “readiness” vs full WS server | Low | Minimal placeholder endpoint / client hook only |

---

## 7. Implementation Plan (Summary)

1. Create monorepo root layout + README  
2. Backend: FastAPI app, config, logging, health, DI, pytest  
3. Frontend: Vite React TS, dark institutional shell, health client  
4. Integration verification  
5. EKMS + PROJECT_STATE + CHANGELOG  
6. Sync governance docs status  
7. Delivery Report  

---

## 8. Engineering Decision Approval (Internal)

| Gate | Status |
|------|--------|
| Requirements understood | ✓ |
| Architecture reviewed | ✓ |
| Dependencies known | ✓ (stdlib + FastAPI stack; Vite React) |
| Risks documented | ✓ |
| Implementation strategy complete | ✓ |

**Proceed to implementation.**

---

**End of Intake**
