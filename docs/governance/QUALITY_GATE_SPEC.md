# QUALITY_GATE_SPEC.md

| Version | 1.0.0 |
| Status | Active (Tier 7) |
| Issued | W0-U08 |

## Engineering Quality Gates (EQG)

| Gate | Requirement |
|------|-------------|
| EQG-1 Requirements | Build Order understood; ambiguities escalated |
| EQG-2 Architecture | Conforms to `05_SYSTEM_ARCHITECTURE.md` v2.0 |
| EQG-3 Implementation | Matches plan; no silent scope expansion |
| EQG-4 Testing | Unit/integration as applicable; suite green |
| EQG-5 Documentation | PROJECT_STATE, ADRs, guides synchronized |
| EQG-6 Governance | Hierarchy + security envelope respected |
| EQG-7 Code quality | Types/lint as configured; no placeholder “done” |
| EQG-8 Delivery | Delivery Report + evidence + debt recorded |

A unit is **not** ready for ITRGA until all applicable gates pass.

## Automated baseline (W0-U08)

- Backend: `pytest`  
- Frontend: `vitest`, `tsc -b`  
- Schema: `alembic upgrade head` (Postgres in CI/compose)  
- CI: `.github/workflows/ci.yml`  

## Security gates (post-U08)

- JWT secret enforced outside explicit local allow  
- Bootstrap credentials not silent defaults  
- Refresh rotation + reuse detection  
- Production `AUTO_CREATE_SCHEMA=false`  

---

**End**
