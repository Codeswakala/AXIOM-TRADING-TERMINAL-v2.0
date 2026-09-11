# Engineering Knowledge Management System (EKMS) — Overview

| Item | Value |
|------|--------|
| Version | 0.2.0 |
| Status | Active (W0-U02) |
| Authority | Development Authority Manual §53 |
| Last Updated | 2026-07-10 |

## Purpose

The EKMS preserves institutional engineering knowledge independently of any single AI session or individual contributor. The **repository** is the authoritative knowledge store.

## Initial Structure

| Path | Purpose |
|------|---------|
| `docs/adr/` | Architecture Decision Records |
| `docs/adr/ADR-000_TEMPLATE.md` | ADR template |
| `docs/adr/ADR-001_Monorepo_Layout.md` | Monorepo decision |
| `docs/adr/ADR-002_Config_And_Observability.md` | Config/logging decision |
| `docs/adr/ADR-003_Database_Technology.md` | Postgres/async SQLAlchemy/Alembic |
| `docs/adr/ADR-004_Repository_Pattern.md` | Repository + session boundaries |
| `docs/adr/EDR-001_ARCHITECTURE_MERGE.md` | Pre-W0 architecture merge record |
| `docs/database/SETUP_AND_MIGRATIONS.md` | DB setup & migration workflow |
| `docs/decision-log.md` | Chronological decision index |
| `docs/technical-debt.md` | Explicit debt register |
| `docs/ekms-overview.md` | This document |
| `docs/governance/` | Synced governing documents |
| `docs/build-orders/` | Build orders and intake assessments |
| `docs/templates/` | Reusable document templates |

## Future EKMS expansions

- Lessons learned register  
- Engineering patterns catalog  
- Research notes (Wave 2+)  
- Known limitations index  
- Project terminology glossary  
- Review outcome archive (ITRGA findings)

## Rules

1. Significant architectural choices → ADR.  
2. Significant implementation choices → EDR (or ADR if architecture-level).  
3. Accepted shortcuts → Technical Debt Register.  
4. Strategic decisions → Decision Log.  
5. No undocumented production behaviour.

---

**End of EKMS Overview**
