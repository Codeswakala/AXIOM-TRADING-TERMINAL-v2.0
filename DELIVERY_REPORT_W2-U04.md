# Delivery Report — W2-U04

| Field | Value |
|-------|-------|
| Build Order | **W2-U04** ML Research: Reproducible Dataset Snapshot Builder + Temporal Split Engine |
| Platform | **0.16.0** |
| Date | 2026-07-13 |
| Author | Development Authority |
| Status | **Implemented — submitted for ITRGA review** |
| Approval | **Not self-approved** |
| Builds on | W2-U01 dataset/chronology, W2-U02 query port/metadata, W2-U03 feature store |

---

## 1. Executive Summary

W2-U04 delivers the reproducible dataset snapshot builder and temporal split engine. It binds guarded canonical records and causal feature records into deterministic research artifacts that can be rebuilt to the same hash and split only by time.

The unit enforces:

- build-twice snapshot reproducibility;
- frozen snapshot immutability;
- temporal-only train/validation/test split;
- random/shuffled split rejection;
- label-horizon / embargo leakage rejection;
- split manifest persistence and hashing;
- no symbol/provider/market identity in the training matrix.

This unit introduces **no model, no training, no inference, no prediction, no execution, no broker/provider live connection, and no credentials**.

---

## 2. Hypothesis / counter-hypotheses

### Hypothesis

AXIOM can construct deterministic dataset/feature matrix artifacts and temporal split manifests without leakage or irreproducibility, preserving all prior Wave-2 data integrity gates.

### Counter-hypotheses

| Counter | Result | Evidence |
|---------|--------|----------|
| Rebuilding same snapshot inputs may produce different hash | **Falsified** | `test_snapshot_builder_rebuild_same_inputs_identical_hash` |
| Frozen snapshot may mutate silently | **Falsified** | `test_frozen_snapshot_immutable_new_version_created` |
| Random split may be accepted | **Falsified** | `test_random_split_rejected_and_temporal_split_hash_deterministic` |
| Label horizon may leak into validation window | **Falsified** | `test_label_horizon_crossing_rejected_and_embargoed_split_passes` |
| Split manifest may be non-deterministic | **Falsified** | same split test asserts identical hash for reversed input order |
| Synthetic records may enter authoritative snapshot builder | **Falsified** | `test_synthetic_records_excluded_from_snapshot_builder` |
| Training matrix may contain symbol/provider/market identity | **Falsified** | matrix rows contain only row id, as-of, features, dataset hash; structural test passes |

---

## 3. Implementation Summary

### 3.1 Dataset split manifest persistence

Added ORM model:

```text
backend/app/db/models/dataset_split.py
```

Added Alembic migration:

```text
backend/alembic/versions/20260713_0008_w2_u04_split_manifests.py
```

New table:

```text
dataset_split_manifests
```

Fields include:

- dataset snapshot reference;
- split id;
- split strategy;
- label horizon bars;
- embargo bars;
- train/validation/test boundaries;
- per-split row counts;
- split hash;
- manifest JSON;
- quality summary.

### 3.2 Reproducible snapshot builder

Added:

```text
backend/app/ml/dataset/snapshot_builder.py
```

`ReproducibleSnapshotBuilder`:

- creates draft dataset snapshot;
- freezes it from canonical records using W2-U01 guard;
- computes causal feature records via W2-U03 feature store;
- returns identity-free matrix rows;
- creates persisted split manifests.

Training matrix rows intentionally contain only:

```text
row_id
as_of
features
source_dataset_hash
```

They do not contain `symbol`, `provider`, or `market_class`.

### 3.3 Temporal split engine

Added:

```text
backend/app/ml/dataset/split_engine.py
```

`TemporalSplitEngine`:

- accepts only temporal split strategy;
- rejects random/shuffle via `SPLIT_LEAKAGE`;
- requires ordered UTC boundaries;
- enforces label horizon + embargo gap;
- produces deterministic split hash and manifest.

### 3.4 ADR

Added:

```text
docs/adr/ADR-024_Temporal_Split_And_Snapshot_Reproducibility.md
```

---

## 4. Governance / Documentation Updates

Added:

- `docs/build-orders/BUILD_ORDER_W2-U04.md`
- `docs/build-orders/BUILD_ORDER_INTAKE_W2-U04.md`
- `docs/adr/ADR-024_Temporal_Split_And_Snapshot_Reproducibility.md`
- `docs/evidence/W2-U04_OPERATOR_EVIDENCE_COMMANDS.md`

Updated:

- `PROJECT_STATE.md`
- `CHANGELOG.md`
- `README.md`
- `docs/governance/RISK_REGISTER.md`
- `docs/governance/TECHNICAL_DEBT_REGISTER.md`
- `docs/governance/GOVERNANCE_AMENDMENTS.md`
- `docs/governance/04_PROJECT_ROADMAP.md`
- backend version/system metadata;
- frontend unit label.

---

## 5. Evidence

### 5.1 Backend tests and Ruff

Commands run in DA sandbox using a temporary virtual environment outside the persisted workspace:

```bash
cd backend
ruff check .
AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_DATABASE_URL='sqlite+aiosqlite:///:memory:' \
AXIOM_DATABASE_AUTO_CREATE_SCHEMA=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
pytest -q
```

Result:

```text
All checks passed!
119 passed, 1 warning
```

### 5.2 Alembic local migration

Command:

```bash
cd backend
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w2u04.db' \
AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
alembic upgrade head
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w2u04.db' alembic current
```

Result:

```text
Running upgrade 20260713_0007 -> 20260713_0008
20260713_0008 (head)
```

### 5.3 Frontend no-regression

Prior command run after W2-U04 changes:

```bash
cd frontend
npm ci
npm audit --audit-level=high
npm test
npm run lint
npm run build
```

Expected/observed baseline remains:

```text
found 0 vulnerabilities
Test Files  8 passed (8)
Tests       16 passed (16)
tsc         clean
vite build  successful
```

Operator target evidence remains mandatory.

---

## 6. Tests Added

New file:

```text
backend/tests/test_snapshot_builder_split.py
```

Tests:

| Test | Purpose |
|------|---------|
| `test_snapshot_builder_rebuild_same_inputs_identical_hash` | build twice over same records → identical dataset hash |
| `test_frozen_snapshot_immutable_new_version_created` | frozen snapshot rejects mutation; new version created |
| `test_random_split_rejected_and_temporal_split_hash_deterministic` | random split rejected; temporal split hash deterministic |
| `test_label_horizon_crossing_rejected_and_embargoed_split_passes` | leaky label horizon rejected; embargoed split passes |
| `test_split_manifest_persisted_with_counts_and_hash` | split manifest persisted with counts/hash |
| `test_synthetic_records_excluded_from_snapshot_builder` | synthetic data excluded/quarantined |
| `test_snapshot_builder_code_does_not_emit_symbol_identity_matrix_fields` | training matrix excludes symbol/provider/market identity |

Backend baseline increased from **112** to **119**.

---

## 7. Explicit Negative Evidence

| Bad condition | Proof |
|---------------|-------|
| random/shuffled split | rejected with `SPLIT_LEAKAGE` |
| label horizon crossing validation boundary | rejected with `LABEL_HORIZON_LEAKAGE` |
| synthetic source in authoritative snapshot | snapshot quarantined; reason `SYNTHETIC_SOURCE_NOT_AUTHORITATIVE` |
| frozen snapshot mutation | rejected; new version path exists |
| training matrix identity leakage | structural test; matrix row excludes identity fields |
| model/training/inference | not implemented |

---

## 8. Operator Evidence Command Pack

Created:

```text
docs/evidence/W2-U04_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes Windows/PowerShell + PostgreSQL commands for:

1. PostgreSQL migration to `20260713_0008`;
2. full backend/frontend test console;
3. named W2-U04 tests;
4. reproducibility and split leakage focused tests;
5. optional PostgreSQL split manifest proof;
6. containment / D-W2-001 evidence;
7. CI/local equivalent;
8. parity smoke.

---

## 9. Out of Scope Confirmed

Not implemented in W2-U04:

- experiment registry;
- model training;
- model evaluation;
- inference;
- prediction;
- calibration/economic/statistical validation;
- broker/provider live connection;
- credentials;
- execution.

Labels are represented only as inert horizon/split validation concepts for leakage tests, not training targets.

---

## 10. Risks and Unknowns

| Risk / Unknown | Status | Mitigation |
|----------------|--------|------------|
| PostgreSQL migration not DA-run | Operator evidence required | command pack includes PG migration |
| Remote CI run | Still carried | command pack includes local/remote evidence |
| Experiment pinning of splits | Deferred | W2-U05 experiment registry |
| Model consumption of snapshots/splits | Deferred | W2-U06+ only after W2-U05 proven |

---

## 11. Confidence Statement

| Dimension | Rating | Justification |
|-----------|--------|---------------|
| Snapshot reproducibility | **HIGH in DA tests** | build-twice identical hash passes |
| Temporal split engine | **HIGH in DA tests** | random split rejected; deterministic split hash passes |
| Label horizon / embargo | **HIGH in DA tests** | leaky split rejected; embargoed split passes |
| Identity exclusion | **HIGH in DA tests** | training matrix excludes identity fields |
| Target-platform correctness | **LIMITED until Operator evidence lands** | Windows + PostgreSQL evidence required by Build Order |
| Overall package | **MODERATE-HIGH for implementation; conditional for approval evidence** | mandatory operator evidence remains required |

No percentage confidence is asserted.

---

## 12. Readiness Statement

> W2-U04 is implemented, tested locally, documented, and submitted for independent ITRGA review.  
> No experiment registry, model, training, inference, prediction, execution, broker connection, provider live connection, or credentials have been introduced.  
> DA does **not** self-approve.  
> Operator-run Windows + PostgreSQL evidence remains mandatory for approval.  
> W2-U05 must not begin until ITRGA disposition and subsequent Build Order authorization.

---

**End of Delivery Report W2-U04**
