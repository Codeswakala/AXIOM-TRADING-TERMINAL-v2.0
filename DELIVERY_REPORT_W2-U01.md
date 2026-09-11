# Delivery Report — W2-U01

| Field | Value |
|-------|-------|
| Build Order | **W2-U01** ML Research: Canonical Dataset Architecture + Chronology & Data-Integrity Guard |
| Platform | **0.13.0** |
| Date | 2026-07-13 |
| Author | Development Authority |
| Status | **Implemented — submitted for ITRGA review** |
| Approval | **Not self-approved** |
| Governing decision | D-W2-001 — generalized, market-agnostic model |
| Canonical architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` v2.0 |
| ML spec | `docs/governance/07_ML_SPEC.md` |

---

## 1. Executive Summary

W2-U01 implements the hard-gate foundation of the ML Research Framework:

1. **Canonical Dataset Architecture** — immutable/versioned dataset snapshots carrying mandatory governance fields, content hashes, lineage, and quarantine records.
2. **Chronology & Data-Integrity Guard** — a formal testable contract that quarantines/rejects future, leaked, out-of-order, synthetic/simulated, naive, duplicate, random-split, and label-horizon-leaking data.
3. **MarketDataQueryPort** — an explicit market-data query contract so ML code consumes market data through a boundary instead of scattered ORM reach-around.

This unit contains **no model, no training, no inference, no prediction, no broker use, no execution, and no live signals**.

---

## 2. Hypothesis / counter-hypotheses

### Hypothesis

AXIOM can establish ML dataset governance and chronology integrity as a provable infrastructure layer before any model work, preserving D-W2-001 market-agnostic learning and all Wave-0/Wave-1 hardening.

### Counter-hypotheses

| Counter | Result | Evidence |
|---------|--------|----------|
| Dataset snapshots may be anonymous | **Falsified** | mandatory-field validation; `test_no_anonymous_dataset_rejected` |
| Frozen datasets may mutate silently | **Falsified** | immutable refreeze rejection; new version creation test |
| Content hash may not be reproducible | **Falsified** | recomputed hash equals frozen hash in test |
| Future records may enter dataset | **Falsified** | `FUTURE_OPEN_TIME` quarantine test |
| Out-of-order authoritative records may be silently resorted | **Falsified** | `OUT_OF_ORDER_TIME` quarantine-not-resort test |
| Synthetic/simulated records may enter authoritative training data | **Falsified** | `SYNTHETIC_SOURCE_NOT_AUTHORITATIVE` and `SIMULATED_FORWARD_DATED` tests |
| Random split / label horizon leakage may pass | **Falsified** | `SPLIT_LEAKAGE` and `LABEL_HORIZON_LEAKAGE` tests |
| Spoofed self-declared future-safe time may bypass guard | **Falsified** | guard uses authoritative anchor, not self-declared timestamp |
| ML code may introduce symbol identity feature pattern | **Falsified structurally** | no `symbol_id`, `one_hot_symbol`, or `symbol_identity` in ML modules |

---

## 3. Implementation Summary

### 3.1 Dataset schema

Added Alembic migration:

```text
backend/alembic/versions/20260713_0005_w2_u01_dataset_architecture.py
```

New ORM models:

```text
backend/app/db/models/dataset.py
```

Tables:

| Table | Purpose |
|-------|---------|
| `dataset_snapshots` | dataset governance metadata and immutable/frozen snapshot identity |
| `dataset_series_members` | series-level membership summary and series hash |
| `dataset_lineage_records` | trace source candle membership into snapshots |
| `dataset_quarantine_records` | bad data quarantine with reason code and detected stage |

`DatasetSnapshot` carries the required `07_ML_SPEC` dataset governance fields:

- dataset identifier;
- market;
- timeframe;
- date range;
- source;
- feature version;
- creation timestamp;
- quality score.

### 3.2 Dataset service

Added:

```text
backend/app/ml/dataset/service.py
```

Capabilities:

- create draft dataset snapshot;
- validate mandatory governance fields;
- freeze snapshot from candles/query-port data;
- compute deterministic SHA-256 `content_hash`;
- write series membership and lineage;
- write quarantine rows;
- prevent mutation/refreeze of frozen snapshots;
- create new version from frozen snapshot.

### 3.3 Chronology guard

Added:

```text
backend/app/ml/dataset/chronology_guard.py
```

Guard stages:

- ingestion;
- dataset construction;
- training-set generation;
- experiment execution.

Reason codes include:

```text
FUTURE_OPEN_TIME
OUT_OF_ORDER_TIME
DUPLICATE_NATURAL_KEY
SYNTHETIC_SOURCE_NOT_AUTHORITATIVE
SIMULATED_FORWARD_DATED
NAIVE_TIMESTAMP
SPLIT_LEAKAGE
UNKNOWN_SOURCE_AUTHORITY
LABEL_HORIZON_LEAKAGE
```

Required refinements implemented:

| Refinement | Implementation |
|------------|----------------|
| R-1 no silent resort | authoritative out-of-order records quarantine by default |
| R-2 label-horizon guard | `validate_label_horizon()` rejects horizon crossing validation boundary |
| R-3 trustworthy anchors | guard uses immutable `as_of_time` / `ingestion_finished_at`, ignores self-declared future-safe timestamp |

### 3.4 Market data query port

Added:

```text
backend/app/ml/dataset/market_data_query.py
```

Includes:

- `MarketDataQueryPort` protocol;
- `MarketSeriesKey`;
- `SourceMetadata`;
- `CandleMarketDataQueryAdapter` backed by existing candle table/repository.

This establishes the ML market-data access seam and avoids direct ad-hoc ORM use across ML modules.

### 3.5 ADRs

Added:

- `docs/adr/ADR-020_Dataset_Snapshot_Architecture.md`
- `docs/adr/ADR-021_Chronology_Guard_Contract.md`

---

## 4. Verification Evidence

### 4.1 Backend tests and Ruff

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
97 passed, 1 warning
```

Raw non-quiet test run should show:

```text
collected 97 items
```

### 4.2 Alembic local migration

Command:

```bash
cd backend
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w2u01.db' \
AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
alembic upgrade head
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w2u01.db' alembic current
```

Result:

```text
Running upgrade 20260711_0004 -> 20260713_0005
20260713_0005 (head)
```

PostgreSQL migration evidence is required from the Operator per Build Order.

### 4.3 Frontend no-regression

Commands:

```bash
cd frontend
npm ci
npm audit --audit-level=high
npm test
npm run lint
npm run build
```

Result:

```text
found 0 vulnerabilities
Test Files  8 passed (8)
Tests       16 passed (16)
tsc         clean
vite build  successful
```

---

## 5. Tests Added

New file:

```text
backend/tests/test_ml_dataset_architecture.py
```

Tests:

| Test | Purpose |
|------|---------|
| `test_dataset_snapshot_freeze_hash_lineage_and_new_version` | mandatory fields, freeze, content hash reproducibility, immutability, new version |
| `test_no_anonymous_dataset_rejected` | no anonymous/incomplete dataset allowed |
| `test_forward_dated_record_quarantined_with_reason` | future record produces quarantine row |
| `test_out_of_order_authoritative_quarantined_not_resorted` | R-1 quarantine-not-resort |
| `test_synthetic_and_forward_simulated_excluded_from_authoritative_training` | OBS-1 enforcement |
| `test_random_split_rejected_and_label_horizon_leakage_rejected` | random split + R-2 label horizon leakage rejected |
| `test_spoofed_future_safe_timestamp_cannot_bypass_authoritative_anchor` | R-3 immutable anchor proof |
| `test_market_data_query_port_lists_and_fetches_candles` | query port boundary |
| `test_ml_dataset_modules_do_not_introduce_symbol_identity_feature_pattern` | D-W2-001 no symbol identity pattern |

Backend baseline increased from **88** to **97**.

---

## 6. Explicit Negative Evidence

| Bad condition | Proof |
|---------------|-------|
| missing dataset identifier | rejected |
| future `open_time` | quarantined `FUTURE_OPEN_TIME` |
| authoritative out-of-order record | quarantined `OUT_OF_ORDER_TIME`, not resorted |
| `source=seed:synthetic` authoritative dataset | quarantined/excluded |
| `source=live:simulated` authoritative dataset | quarantined/excluded |
| random split | rejected `SPLIT_LEAKAGE` |
| label horizon crosses validation boundary | rejected `LABEL_HORIZON_LEAKAGE` |
| spoofed self-declared safe timestamp | rejected by authoritative anchor check |
| naive trusted timestamp | rejected by existing strict UTC boundary tests |
| symbol identity feature pattern | structural test asserts absent |

---

## 7. Governance / Register Updates

Updated:

- `PROJECT_STATE.md`
- `CHANGELOG.md`
- `README.md`
- `docs/governance/RISK_REGISTER.md`
- `docs/governance/TECHNICAL_DEBT_REGISTER.md`
- `docs/governance/GOVERNANCE_AMENDMENTS.md`
- `docs/build-orders/BUILD_ORDER_INTAKE_W2-U01.md`

OBS-1 transition:

```text
from carried note → enforced by W2-U01 source authority + quarantine contract
```

New/updated risks:

- data leakage/look-ahead;
- synthetic/simulated chronology pollution;
- label-horizon leakage;
- dataset reproducibility;
- symbol identity leakage.

---

## 8. Operator Evidence Command Pack

Created:

```text
docs/evidence/W2-U01_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes Windows/PowerShell + PostgreSQL commands for:

1. PostgreSQL migration to `20260713_0005`;
2. backend `pytest`/Ruff;
3. frontend audit/tests/type/build;
4. chronology negative tests with `-vv`;
5. quarantine-row proof;
6. reproducibility/immutability proof;
7. no-anonymous-dataset proof;
8. query port / no symbol identity evidence;
9. CI/local equivalent;
10. parity smoke.

---

## 9. Out of Scope Confirmed

Not implemented in W2-U01:

- feature computation for training;
- feature store computations;
- dataset split engine beyond guard contract;
- experiment registry;
- model training;
- inference;
- prediction;
- live signals;
- broker connection;
- execution/order path;
- numpy/pandas/scikit-learn adoption.

---

## 10. Risks and Unknowns

| Risk / Unknown | Status | Mitigation |
|----------------|--------|------------|
| PostgreSQL migration not DA-run | Operator evidence required | Evidence command pack includes migration proof |
| Quarantine table row on PostgreSQL | Operator evidence preferred | Negative tests prove behavior; SQL query included if PG state persists |
| Full CI remote run | Still carried | local equivalent and CI config exist |
| Feature/model units later | Deferred | W2-U03+ / W2-U06+ |

---

## 11. Confidence Statement

| Dimension | Rating | Justification |
|-----------|--------|---------------|
| Dataset architecture design | **HIGH** | schema, service, mandatory fields, immutability, hashes, lineage implemented and tested |
| Chronology guard implementation | **HIGH in DA tests** | required negative tests pass locally |
| Market-agnostic posture | **HIGH for W2-U01 scope** | no symbol identity feature pattern; no model/features introduced |
| PostgreSQL target evidence | **LIMITED until Operator evidence lands** | DA sandbox local migration was SQLite; Build Order requires PG evidence |
| Overall package | **MODERATE-HIGH for implementation; conditional for approval evidence** | Mandatory operator evidence remains required |

No percentage confidence is asserted.

---

## 12. Readiness Statement

> W2-U01 is implemented, tested locally, documented, and submitted for independent ITRGA review.  
> No model, training, inference, prediction, execution, broker connection, or order path has been introduced.  
> DA does **not** self-approve.  
> Operator-run Windows + PostgreSQL evidence remains mandatory for approval.  
> W2-U02 must not begin until ITRGA disposition and subsequent Build Order authorization.

---

**End of Delivery Report W2-U01**
