# Delivery Report — W2-U02

| Field | Value |
|-------|-------|
| Build Order | **W2-U02** ML Research: Market-Agnostic Data Access + Multi-Market Metadata Layer |
| Platform | **0.14.0** |
| Date | 2026-07-13 |
| Author | Development Authority |
| Status | **Implemented — submitted for ITRGA review** |
| Approval | **Not self-approved** |
| Governing decision | D-W2-001 — generalized, market-agnostic model |
| Builds on | W2-U01 approved with observations |

---

## 1. Executive Summary

W2-U02 matures the ML Research Framework's market-agnostic data-access boundary and multi-market metadata layer.

It delivers:

- canonical market class validation;
- `MarketSeriesKey` uniform address tuple;
- `CanonicalOHLCVRecord` boundary DTO;
- `authority_classification` for each canonical record;
- `MarketSeriesMetadataRead` governance/evaluation metadata;
- `market_series_metadata` storage table;
- `MarketDataQueryPort` hardened as ML market-data access seam;
- provider adapter contract;
- Deriv Synthetic Indices adapter skeleton under canonical market class `synthetic`;
- structural tests proving no provider vocabulary leak, no new top-level market, no symbol identity feature pattern, and no ML ORM reach-around outside the query adapter.

This unit adds **no features-for-training, no model, no training, no inference, no prediction, no broker connection, no provider live connection, no credentials, and no execution**.

---

## 2. Hypothesis / counter-hypotheses

### Hypothesis

AXIOM can expose all ML market data through one canonical, market-agnostic port and metadata layer while preserving D-W2-001: metadata may support evaluation and guardrails but must not become learned symbol identity.

### Counter-hypotheses

| Counter | Result | Evidence |
|---------|--------|----------|
| Provider might become new top-level market | **Falsified** | `MarketSeriesKey` rejects `market_class='deriv'`; Deriv adapter uses `synthetic` |
| Provider-native vocabulary might leak inward | **Falsified structurally** | provider term isolation test passes |
| ML code might scatter Candle ORM access | **Falsified structurally** | ORM reach-around test allows only `market_data_query.py` adapter |
| Symbol identity feature pattern might appear | **Falsified structurally** | no `symbol_id`, `one_hot_symbol`, `symbol_identity` pattern |
| Canonical DTO timestamps might be naive | **Falsified** | `CanonicalOHLCVRecord` requires UTC; adapter normalizes DB-driver output |
| Metadata might be learned feature | **Falsified by design/test** | metadata role is `governance_evaluation_only` |
| Duplicate/out-of-order validation might not work across markets/providers | **Falsified** | multi-market duplicate/order guard test passes |

---

## 3. Implementation Summary

### 3.1 Canonical market classes

Added in:

```text
backend/app/ml/dataset/market_data_query.py
```

Canonical market set:

```text
synthetic
forex
crypto
stocks
indices
etfs
commodities
futures
```

`MarketSeriesKey` validates the market class. `deriv` is rejected as a top-level market class.

### 3.2 Boundary DTOs

Added/extended:

- `MarketSeriesKey`
- `CanonicalOHLCVRecord`
- `SourceMetadata`
- `MarketSeriesMetadataRead`
- `CanonicalMarketClass`

`CanonicalOHLCVRecord` contains:

- `series_key`
- `open_time` UTC
- OHLCV
- `source`
- `ingestion_run_id`
- `authority_classification`
- `source_record_id`

### 3.3 MarketDataQueryPort

Hardened as canonical ML data entry point:

```text
MarketDataQueryPort
  list_series()
  get_candles(series_key, start, end, source_filter)
  get_source_metadata(source)
  get_series_metadata(series_key)
```

`CandleMarketDataQueryAdapter` is the only ML module allowed to import candle ORM details.

### 3.4 Market metadata storage

Added ORM model:

```text
backend/app/db/models/market_metadata.py
```

Added Alembic migration:

```text
backend/alembic/versions/20260713_0006_w2_u02_market_metadata.py
```

New table:

```text
market_series_metadata
```

Fields include:

- market class;
- provider;
- symbol;
- timeframe;
- session/calendar;
- tick size;
- precision;
- timezone assumption;
- source authority;
- known limitations;
- metadata role.

Metadata role is governance/evaluation only.

### 3.5 Provider adapter contract

Added:

```text
backend/app/ml/dataset/provider_adapters.py
```

Includes:

- `MarketDataProviderAdapter` protocol;
- `InternalProviderAdapter`;
- `DerivSyntheticIndicesAdapter` skeleton.

`DerivSyntheticIndicesAdapter`:

- provider name: `deriv`;
- market class: `synthetic`;
- no live connection;
- no credentials;
- no network I/O;
- known limitation states design skeleton only.

### 3.6 Metadata service

Added:

```text
backend/app/ml/dataset/metadata_service.py
```

Capabilities:

- upsert series metadata;
- get metadata by `MarketSeriesKey`;
- list stored market classes.

---

## 4. Governance / Documentation Updates

Added:

- `docs/build-orders/BUILD_ORDER_W2-U02.md`
- `docs/build-orders/BUILD_ORDER_INTAKE_W2-U02.md`
- `docs/adr/ADR-022_Market_Agnostic_Data_Access_Contract.md`
- `docs/evidence/W2-U02_OPERATOR_EVIDENCE_COMMANDS.md`

Updated:

- `PROJECT_STATE.md`
- `CHANGELOG.md`
- `README.md`
- `docs/governance/RISK_REGISTER.md`
- `docs/governance/TECHNICAL_DEBT_REGISTER.md`
- `docs/governance/GOVERNANCE_AMENDMENTS.md`

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
pytest
```

Result:

```text
All checks passed!
collected 105 items
105 passed, 1 warning
```

### 5.2 Alembic local migration

Command:

```bash
cd backend
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w2u02.db' \
AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
alembic upgrade head
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w2u02.db' alembic current
```

Result:

```text
Running upgrade 20260713_0005 -> 20260713_0006
20260713_0006 (head)
```

PostgreSQL migration evidence is required from Operator per Build Order.

### 5.3 Frontend no-regression

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

## 6. Tests Added

New file:

```text
backend/tests/test_market_agnostic_access.py
```

Tests:

| Test | Purpose |
|------|---------|
| `test_market_series_key_rejects_new_top_level_market` | proves Deriv cannot be top-level market |
| `test_deriv_adapter_is_provider_under_synthetic_no_live_connection` | proves Deriv is provider under Synthetic and no live connection is present |
| `test_canonical_ohlcv_mapping_and_authority_across_markets` | maps Forex and Crypto candles to canonical records and authority classifications |
| `test_metadata_stored_queryable_and_not_learned_feature` | persists/query metadata and verifies governance/evaluation role |
| `test_duplicate_and_ordering_validation_across_markets_and_providers` | duplicate/order validation across market/provider series |
| `test_provider_terms_do_not_leak_outside_provider_adapter` | provider-native terms isolated |
| `test_ml_modules_use_query_port_not_scattered_candle_orm` | only query adapter accesses candle ORM |
| `test_no_symbol_identity_learned_feature_pattern` | D-W2-001 no symbol identity feature pattern |

Backend baseline increased from **97** to **105**.

---

## 7. W2-U01 Observation Recapture Support

W2-U02 evidence commands include closure steps for W2-U01 observations:

| Observation | Evidence command |
|-------------|------------------|
| G-1 visible named tests | `pytest tests/test_ml_dataset_architecture.py -vv | Tee-Object ...` |
| G-2 persisted PostgreSQL quarantine row | provided Python script that commits one `FUTURE_OPEN_TIME` quarantine row and SQL `SELECT` proof |
| R-CI-01 CI run | local/remote CI command included |

---

## 8. Explicit Negative Evidence

| Prohibited item | Status |
|-----------------|--------|
| New top-level `deriv` market class | Rejected by `MarketSeriesKey` validation |
| Live Deriv/provider connection | Not implemented |
| Provider credentials | Not implemented |
| Provider terms leaking into ML internals | Structural test passes |
| Symbol identity learned feature | Structural test passes |
| Direct ML ORM reach-around | Structural test passes |
| Model/training/inference/features-for-training | Not implemented |
| Broker/execution/order path | Not implemented |

---

## 9. Operator Evidence Command Pack

Created:

```text
docs/evidence/W2-U02_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes Windows/PowerShell + PostgreSQL commands for:

1. PostgreSQL migration to `20260713_0006`;
2. backend full test console;
3. frontend no-regression proof;
4. W2-U01 G-1 named-test recapture;
5. W2-U02 tests by name;
6. W2-U01 G-2 persisted quarantine row proof;
7. Deriv/provider/canonical market evidence;
8. provider isolation / no symbol identity / no ORM reach-around grep;
9. CI/local equivalent;
10. parity smoke.

---

## 10. Risks and Unknowns

| Risk / Unknown | Status | Mitigation |
|----------------|--------|------------|
| PostgreSQL migration not DA-run | Operator evidence required | command pack includes PG migration |
| Deriv/provider live connection absent | Intentional deferral | recorded as TD-042 |
| Metadata not yet consumed by features/evaluation | Intentional deferral | recorded as TD-043 |
| Remote CI run | Still carried | command pack includes local/remote evidence |

---

## 11. Confidence Statement

| Dimension | Rating | Justification |
|-----------|--------|---------------|
| Market-agnostic access design | **HIGH** | canonical DTOs, market validation, query port, metadata service implemented |
| Provider isolation | **HIGH in DA tests** | Deriv under Synthetic; provider term structural test passes |
| D-W2-001 compliance | **HIGH for W2-U02 scope** | no symbol identity pattern; metadata role is governance/evaluation only |
| Target-platform correctness | **LIMITED until Operator evidence lands** | Windows + PostgreSQL evidence required by Build Order |
| Overall package | **MODERATE-HIGH for implementation; conditional for approval evidence** | mandatory operator evidence remains required |

No percentage confidence is asserted.

---

## 12. Readiness Statement

> W2-U02 is implemented, tested locally, documented, and submitted for independent ITRGA review.  
> No features-for-training, model, training, inference, prediction, execution, broker connection, provider live connection, or credentials have been introduced.  
> DA does **not** self-approve.  
> Operator-run Windows + PostgreSQL evidence remains mandatory for approval.  
> W2-U03 must not begin until ITRGA disposition and subsequent Build Order authorization.

---

**End of Delivery Report W2-U02**
