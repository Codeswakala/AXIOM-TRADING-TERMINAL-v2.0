# ADR-018 — CI Gate Consolidation

| Field | Value |
|-------|-------|
| ID | ADR-018 |
| Title | Consolidated automated regression gate for Core Platform units |
| Date | 2026-07-13 |
| Status | Accepted |
| Deciders | Development Authority under Build Order W1-U02 |
| Domain | CI / DevOps / Quality Governance |

---

## Context

Wave 0 closed with one low residual: evidence of a green CI run. W1-U02 requires the automated gate to become part of every unit's delivery discipline and to include Alembic-on-PostgreSQL, backend tests, frontend tests, TypeScript/build, and Ruff.

## Decision

Update `.github/workflows/ci.yml` so backend CI runs:

1. PostgreSQL service container;
2. dependency install;
3. `alembic upgrade head` against PostgreSQL;
4. `ruff check .`;
5. `pytest -q` with isolated SQLite test DB.

Frontend CI runs:

1. `npm ci`;
2. `npm test`;
3. `npx tsc -b --pretty false`;
4. `npm run build`.

Add `scripts/local_ci.sh` as a reproducible local equivalent for environments where remote GitHub Actions evidence is unavailable.

## Alternatives Considered

| Option | Outcome | Rationale |
|--------|---------|-----------|
| Keep Ruff outside CI | Rejected | W1-U02 specifically requires CI consolidation and build failure on lint failure. |
| Run all backend tests only on PostgreSQL | Deferred | Current suite is intentionally SQLite-isolated; PostgreSQL Alembic path is still verified. Future units may add a dedicated PG API integration tier. |
| Depend only on local operator scripts | Rejected as sole path | Remote CI is preferred; local script is fallback evidence. |

## Consequences

- CI fails on migration, lint, backend, frontend, typecheck, or build failures.
- PostgreSQL schema path remains verified on every backend CI run.
- Local equivalent can reproduce the same gates for ITRGA evidence.

## Compliance

- Supports W1-U02 Component D and Quality Gate requirements.
- Closes the Wave-0 CI evidence residual once a green remote or operator local-equivalent run is supplied.

---

**End ADR-018**
