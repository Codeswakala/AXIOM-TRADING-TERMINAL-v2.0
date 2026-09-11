# AXIOM Wave 2 Engineering Design & Implementation Plan

| Item | Value |
|------|-------|
| Document | Wave 2 Engineering Design & Implementation Plan |
| Request | `docs/build-orders/ITRGA_REQUEST_WAVE2_DESIGN_PLAN.md` |
| Date | 2026-07-13 |
| Author | Development Authority |
| Status | **Plan submitted for ITRGA review — no construction authorized** |
| Wave | 2 — Machine Learning Research Framework |
| Governing architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` v2.0 |
| Governing ML spec | `docs/governance/07_ML_SPEC.md` |
| Binding decision | D-W2-001 — Option A: generalized, market-agnostic model |

---

## 0. Non-construction statement

This document is a **design and implementation plan only**.

The Development Authority will not implement code, schema migrations, pipelines, feature computation, datasets, experiments, models, or model registries until ITRGA accepts this plan and issues `BUILD_ORDER_W2-U01`.

This plan is therefore a blueprint and a set of reviewable constraints. It is not a delivery report and does not claim runtime evidence.

---

## 1. Executive Summary

Wave 2 establishes AXIOM's **Machine Learning Research Framework**. Its purpose is to build the research infrastructure needed for scientifically valid, reproducible, market-agnostic ML research.

Wave 2 is **research/advisory only**:

- no execution;
- no broker connection;
- no order path;
- no live operator-facing signals;
- no model-driven trading decisions;
- W1-U03 Constitutional Governance Gate remains **closed**.

The binding design decision is **D-W2-001: generalized, market-agnostic model**. The learned model must not encode symbol identity. It must learn transferable market behaviour from normalized features. Per-market evaluation, registries, versioning, and operating-domain guardrails remain required, but per-market specialized learned models are not the default and may not appear without formal `07_ML_SPEC` amendment.

The first Wave-2 unit should be:

> **W2-U01 — Canonical Dataset Architecture + Chronology & Data-Integrity Guard**

No model training or evaluation should occur until W2-U01 dataset governance and chronology guard layers are Level-I proven on the target platform.

---

## 2. Constitutional and Governance Frame

### 2.1 Non-negotiable rules

| Rule | Plan commitment |
|------|-----------------|
| Research/advisory only | Wave 2 produces research artifacts, datasets, feature stores, experiments, validations, and model registry entries; it produces no trades. |
| Broker gate closed | W1-U03 Constitutional Governance Gate remains closed through all Wave-2 units. |
| ML bounded context | ML Research System owns datasets, features, experiments, validation, and research registry artifacts. |
| No direct subsystem reach-around | ML consumes market data through approved Market Intelligence/Application Service contracts, not by reaching into unrelated internals. |
| Market-agnostic learning | Learned features exclude symbol identity. Symbol and market metadata may be used for governance/evaluation partitions, not as ordinary predictive identity features. |
| Dataset/chronology before models | Dataset governance and chronology guard are the hard gate before any model unit. |
| Scientific integrity | Experiments must be pre-registered; leakage, look-ahead, p-hacking, selective reporting, and hidden experiments are prohibited. |

### 2.2 Explicit D-W2-001 interpretation

The Wave-2 architecture enforces **one generalized research model family by default**, trained on normalized, market-agnostic features. It may be evaluated by market, timeframe, provider, and regime, but it must not learn a hard-coded symbol identity such as `EURUSD`, `BTCUSD`, or a Deriv instrument code.

Allowed as metadata:

- market class;
- provider;
- symbol;
- timeframe;
- source;
- regime label;
- dataset membership;
- evaluation partition.

Not allowed as ordinary model input without governance amendment:

- raw symbol string;
- one-hot symbol identity;
- broker-native symbol code as feature;
- provider-specific identity field that functions as symbol identity;
- per-symbol specialized learned model as default architecture.

---

## 3. Architecture and Bounded Context

### 3.1 Placement in `05_SYSTEM_ARCHITECTURE.md` v2.0

Wave 2 lives primarily in the **Machine Learning Research System** and interfaces with:

| External system | ML interaction | Boundary rule |
|-----------------|----------------|---------------|
| Market Data / Market Intelligence | obtains validated candle/market data through query contracts | no direct DB reach-around into unrelated persistence internals |
| Data Persistence Service | stores ML-owned dataset/feature/experiment registry tables through ML repositories | ML tables are owned by ML Research System |
| Observability Service | emits redacted/correlated telemetry | no secrets or dataset payload dumps in logs |
| Audit/Governance Service | records experiment registration, dataset freeze, validation runs | audit records are append-oriented governance evidence |
| External Integration System | no direct use in early Wave 2 | broker gate remains closed; broker data is not used |

### 3.2 ML Research System responsibilities

Owned responsibilities:

- dataset snapshot definitions and metadata;
- chronology/data-integrity guard contracts;
- feature definition and feature versioning;
- feature store;
- training/validation/test split definitions;
- experiment pre-registration;
- statistical validation framework;
- economic validation framework;
- model registry for research artifacts;
- drift monitoring design;
- reproducibility records.

Explicitly not owned:

- broker connection;
- live execution;
- chart rendering;
- order management;
- portfolio/account state;
- production trading signal dispatch;
- direct mutation of market ingestion internals.

### 3.3 Approved market-data access contract

Wave 2 should introduce or use a small explicit market-data query contract, for example:

```text
MarketDataQueryPort
  list_series(market_class, symbol, timeframe, source_filter, start, end)
  get_candles(series_key, start, end, order=asc)
  get_source_metadata(series_key)
```

Implementation may be backed by existing candle repositories, but ML code should depend on the port/service contract, not direct ORM queries scattered through ML modules.

### 3.4 Data-flow diagram

```text
Raw market records
  │
  ├─ Chronology Guard G1: source timestamp sanity, as-of guard, source quarantine
  ▼
Cleaning
  │
  ├─ Chronology Guard G2: monotonic series validation, duplicate detection
  ▼
Normalization
  │
  ├─ Chronology Guard G3: UTC-aware timestamps, no future records, source authority check
  ▼
Validation
  │
  ├─ Quality scoring + quarantine table
  ▼
Feature Engineering
  │
  ├─ Chronology Guard G4: causal rolling windows only, no forward-looking features
  ▼
Feature Store
  │
  ├─ Immutable feature version + lineage hash
  ▼
Dataset Snapshot Builder
  │
  ├─ Chronology Guard G5: authoritative sources only, temporal split only
  ▼
Training / Validation / Testing datasets
  │
  ├─ Hard gate: no model unit until W2-U01/W2-U04 proven
  ▼
Training (later unit)
  │
  ├─ Pre-registered experiment required
  ▼
Evaluation
  │
  ├─ Statistical + calibration + economic validation
  ▼
Research Model Registry
  │
  ├─ No execution deployment; research use only
  ▼
Monitoring / Drift / Retraining design
```

---

## 4. Target Platform and Technology Choices

### 4.1 Target platform

Operator target platform for evidence:

```text
Windows / PowerShell
PostgreSQL 18
Python 3.14.6
Node/npm frontend toolchain
```

### 4.2 Dependency adoption rule

No new ML dependency may be adopted merely because it is common. Every non-standard package must pass a target-platform compatibility check:

1. install on Windows with Python 3.14.6;
2. import successfully;
3. run a minimal smoke test;
4. pass CI/local gate;
5. be recorded in an ADR or unit delivery note with version.

### 4.3 Initial technology approach by stage

| Stage | Preferred approach | Reason |
|-------|--------------------|--------|
| W2-U01 dataset/chronology | Python stdlib + existing FastAPI/Pydantic/SQLAlchemy/Alembic/PostgreSQL | Avoid premature numerical stack risk on Py3.14.6. |
| W2-U02/W2-U03 feature framework | Evaluate `numpy`, `pandas` or `polars`, `pyarrow` only after compatibility spike | Dataframe/Parquet stack can be problematic on newest Python versions. |
| First baseline model unit | Evaluate `scikit-learn`, `numpy`, `scipy` versions on Windows/Py3.14.6 before build | Avoid failed operator run due unsupported wheels. |
| Advanced models | Deferred; candidate libraries require separate ADR | No XGBoost/LightGBM/CatBoost until target compatibility and governance need proven. |
| Artifact storage | PostgreSQL metadata + deterministic local artifact files initially | Reproducibility before scale. |

### 4.4 Package risk matrix

| Package family | Current stance | Risk |
|----------------|----------------|------|
| `numpy` / `scipy` | candidate for later model/stat units | Py3.14 wheel compatibility must be verified. |
| `pandas` | candidate for feature/dataset tooling | Possible heavy dependency; deterministic serialization concerns. |
| `polars` | candidate alternative for deterministic tabular processing | Windows/Py3.14 wheel verification required. |
| `pyarrow` / Parquet | optional artifact format | May be delayed if wheels/tooling problematic. |
| `scikit-learn` | candidate baseline model framework | Must verify Py3.14 support and calibration utilities. |
| `statsmodels` | optional statistical validation | Candidate only after compatibility proof. |

W2-U01 should avoid these where possible and focus on schema/contracts/guards.

---

## 5. Canonical Dataset Architecture

### 5.1 Dataset governance fields

Every dataset snapshot must include the `07_ML_SPEC` fields:

| Required field | Design mechanism |
|----------------|------------------|
| dataset identifier | immutable `dataset_id`, e.g. UUID plus semantic name |
| market | market class + series membership metadata |
| timeframe | timeframe per series and snapshot-level allowed timeframes |
| date range | `start_time`, `end_time`, UTC-aware |
| source | allowed source labels and authority classification |
| feature version | `feature_set_version` bound to snapshot |
| creation timestamp | UTC-aware `created_at` |
| quality score | snapshot quality score and component-level checks |

No anonymous dataset may enter production research.

### 5.2 Proposed logical data model

No schema is implemented yet. W2-U01 should design and migrate tables conceptually like:

```text
dataset_snapshots
  id
  dataset_id
  name
  version
  market_scope
  timeframe_scope
  start_time
  end_time
  source_policy
  feature_set_version
  content_hash
  quality_score
  status: draft | frozen | quarantined | deprecated
  created_at
  frozen_at
  created_by
  notes

dataset_series_members
  id
  dataset_snapshot_id
  market_class
  provider
  symbol
  timeframe
  source
  authoritative: bool
  record_count
  first_open_time
  last_open_time
  series_hash

dataset_lineage_records
  id
  dataset_snapshot_id
  source_candle_id
  normalized_record_hash
  feature_record_id nullable
  lineage_stage
  created_at

dataset_quarantine_records
  id
  source_record_id
  market_class
  symbol
  timeframe
  open_time
  source
  reason_code
  detail
  detected_stage
  detected_at
```

### 5.3 Immutability and versioning

A frozen dataset snapshot should be immutable.

Mechanism:

- deterministic ordering by `(market_class, provider, symbol, timeframe, open_time, source, id)`;
- canonical serialization format for hash calculation;
- SHA-256 `content_hash` over snapshot membership and feature version metadata;
- status transition from `draft` to `frozen` only after chronology/quality gates pass;
- any change creates a new dataset version, never mutates a frozen version.

### 5.4 Provenance and lineage

Lineage must be bidirectional:

```text
source candle → normalized record → feature row → dataset snapshot row → experiment input
experiment result → dataset snapshot → feature version → source candle ids
```

Every training row must be traceable back to its source candle(s) and feature definition version.

### 5.5 Reproducible training snapshots

Rebuilding dataset `vX` must produce identical artifact hash when source data, feature version, code version, and configuration are unchanged.

Required mechanisms:

- pinned feature definition version;
- deterministic ordering;
- deterministic numeric precision/rounding policy;
- UTC timestamp normalization;
- environment manifest;
- code revision or source tree hash;
- artifact checksum;
- no wall-clock-derived feature values except recorded snapshot metadata.

---

## 6. Chronology & Data-Integrity Guard

### 6.1 Guard as testable contract

The Chronology Guard is a formal contract, not prose.

Minimum checks:

| Rule | Contract |
|------|----------|
| UTC-aware time | all dataset/feature timestamps are timezone-aware UTC |
| monotonicity | `open_time` monotonic non-decreasing within each `(market_class, provider, symbol, timeframe)` series after dedup |
| no future record | `open_time <= as_of_time` and `open_time <= ingestion_finished_at` where applicable |
| no unauthorized synthetic | `source=seed:synthetic` excluded from authoritative training sets |
| no forward simulated leakage | forward-dated `source=live:simulated` excluded/quarantined from authoritative training sets |
| temporal splits | train/validation/test split by time only, never random row split |
| duplicate policy | duplicates detected by natural key and either deduped or quarantined with reason |
| source authority | each source classified authoritative / simulated / synthetic / unknown |

### 6.2 Guard stages

The guard runs at all required stages:

| Stage | Guard responsibility |
|-------|----------------------|
| ingestion | timestamp parsing, UTC, future check, duplicate detection, source classification |
| dataset construction | source policy, monotonic series, date range, authority exclusion |
| training-set generation | temporal split validation, no leakage across split boundaries |
| experiment execution | verify frozen dataset hash, feature version, split manifest, and pre-registration |

### 6.3 Quarantine behavior

Bad records are not silently dropped. They are quarantined with:

- source record id;
- series key;
- timestamp;
- reason code;
- detected stage;
- detection timestamp;
- detail message.

Example reason codes:

```text
FUTURE_OPEN_TIME
OUT_OF_ORDER_TIME
DUPLICATE_NATURAL_KEY
SYNTHETIC_SOURCE_NOT_AUTHORITATIVE
SIMULATED_FORWARD_DATED
NAIVE_TIMESTAMP
SPLIT_LEAKAGE
UNKNOWN_SOURCE_AUTHORITY
```

### 6.4 Required negative tests

W2-U01 must include tests proving bad records fail to pass:

| Negative test | Expected result |
|---------------|-----------------|
| forward-dated candle with `open_time > as_of_time` | rejected/quarantined |
| out-of-order candle in series | rejected/quarantined or sorted only if source order is not authoritative and no split leakage results |
| `seed:synthetic` in authoritative dataset policy | quarantined/excluded |
| forward-generated `live:simulated` used as real chronology | quarantined/excluded |
| random train/val/test split request | rejected |
| naive timestamp at trusted boundary | rejected |

This is the ML analogue of W1-U03 gate refusal: the proof is a bad record being refused.

---

## 7. Multi-Market Ingestion Design

### 7.1 Canonical market classes

Wave 2 supports the canonical architecture market classes:

```text
Synthetic
Forex
Crypto
Stocks
Indices
ETFs
Commodities
Futures
```

Deriv Synthetic Indices are a **provider adapter under Synthetic**, not a new top-level market.

### 7.2 Market-agnostic ingestion contract

Market ingestion for ML must normalize into a common record shape:

```text
MarketSeriesKey
  market_class
  provider
  symbol
  timeframe

CanonicalOHLCVRecord
  series_key
  open_time UTC
  open/high/low/close
  volume nullable
  source
  ingestion_run_id
  authority_classification
```

Provider-specific terms must be isolated in provider adapters and mapped to canonical DTOs before reaching ML Research.

### 7.3 Metadata

Market metadata is required for evaluation and guardrails, not ordinary learned symbol identity.

Metadata examples:

- market class;
- provider;
- trading session/calendar where known;
- tick size/precision;
- timezone assumptions;
- data source authority;
- known limitations.

### 7.4 Duplicate and ordering validation

Duplicate detection uses natural keys:

```text
market_class + provider + symbol + timeframe + open_time + source
```

Ordering validation occurs per series. Corrections to historical data must produce new lineage/hash records so dataset snapshots remain reproducible.

---

## 8. Feature Engineering and Feature Store

### 8.1 Feature principles

Features must be:

- normalized;
- market-agnostic;
- causal only;
- versioned;
- reproducible;
- explainable where practical;
- compatible across market classes where possible.

### 8.2 No symbol identity

The feature layer must not emit:

- `symbol_id`;
- one-hot symbol vectors;
- broker-native symbol code;
- provider-specific instrument ID as a learned feature.

Symbol and provider remain metadata for slicing/evaluation, not model input.

### 8.3 Candidate generalized features

Feature families from `07_ML_SPEC`:

| Family | Example normalized features |
|--------|-----------------------------|
| trend persistence | normalized rolling return signs, trend duration, slope normalized by volatility |
| volatility expansion | ATR percentile, realized volatility ratio, range expansion score |
| mean reversion | z-score distance from rolling mean, normalized deviation decay |
| momentum | rolling return, normalized momentum acceleration |
| liquidity imbalance | placeholder until reliable volume/order-flow exists; not fabricated |
| breakout behaviour | range break normalized by ATR, prior consolidation length |
| regimes | volatility/trend/range regime labels derived causally |
| distributions | rolling skew/kurtosis/quantile bands where statistically justified |

### 8.4 Feature store design

Logical tables/artifacts:

```text
feature_definitions
  feature_name
  feature_version
  formula_spec
  input_requirements
  lookback_window
  causal: bool
  created_at

feature_records
  feature_set_version
  series_key
  as_of_time
  feature_values
  source_dataset_hash
  quality_score

feature_quality_reports
  feature_set_version
  missing_rate
  drift_summary
  leakage_checks
  stationarity_notes
```

Feature values are bound to dataset snapshots through feature version and content hash.

---

## 9. Experiment, Validation, and Registry Design

### 9.1 Experiment pre-registration

Every experiment must be pre-registered before execution.

Required fields:

- experiment id;
- purpose;
- hypothesis;
- dataset snapshot id/hash;
- feature set version;
- model family;
- evaluation plan;
- temporal split plan;
- metrics to be reported;
- calibration plan;
- economic validation assumptions;
- approval timestamp;
- version;
- operator/reviewer notes.

No undocumented experiment exists.

### 9.2 Statistical validation

Later validation units must support:

- walk-forward validation;
- out-of-sample testing;
- cross-validation suitable for time series;
- calibration analysis;
- confidence intervals;
- bootstrap validation;
- effect size;
- statistical significance;
- uncertainty reporting.

Results must report uncertainty, not just point estimates.

### 9.3 Economic validation

Economic validation is mandatory and separate from predictive performance.

Must model/report:

- spread;
- commission;
- slippage;
- latency;
- liquidity assumptions;
- transaction costs;
- market impact where relevant later.

A statistically significant model may be economically unusable. Both conclusions must be reported independently.

### 9.4 Calibration

Calibration must be a named validation layer, not an afterthought:

- reliability curve / calibration curve;
- Brier score or equivalent probability scoring;
- calibration by market class/timeframe/regime;
- confidence bins;
- explicit warning when confidence is poorly calibrated.

### 9.5 Multi-market evaluation and generalization

The evaluation framework must answer:

> If trained on markets X, does the behaviour hold on markets Y?

Required slices:

- per market class;
- per timeframe;
- per provider;
- per regime;
- cross-market holdout;
- unseen instrument evaluation;
- stress periods if available.

### 9.6 Model registry

Research model registry fields:

- model id;
- model version;
- model family;
- training dataset snapshot id/hash;
- feature version;
- hyperparameters;
- statistical metrics;
- calibration metrics;
- economic validation summary;
- supported operating domain;
- unsupported markets/regimes;
- approval history;
- rollback/reference version;
- research deployment status.

Deployment here means research deployment only, not execution.

### 9.7 Drift monitoring

Drift monitoring design includes:

- feature drift;
- prediction drift;
- concept drift;
- calibration drift;
- market regime shift;
- performance degradation.

Drift does not automatically retrain a model. Evidence must justify retraining.

---

## 10. Proposed Wave-2 Unit Breakdown

### W2-U01 — Canonical Dataset Architecture + Chronology & Data-Integrity Guard

| Item | Detail |
|------|--------|
| Type | Infrastructure / data integrity |
| Scope | Dataset snapshot metadata, chronology guard contract, quarantine design, Alembic schema, dataset query interfaces |
| Satisfies | `07_ML_SPEC` Dataset Governance, Data Pipeline, Research Integrity |
| No model? | Yes — no model training |
| Evidence owed | PostgreSQL migration, dataset snapshot create/freeze, negative chronology tests, quarantine proof, synthetic exclusion proof, target Windows run |

### W2-U02 — Market-Agnostic Data Access + Multi-Market Metadata Layer

| Item | Detail |
|------|--------|
| Type | Infrastructure / ingestion contract |
| Scope | MarketSeriesKey, provider metadata, canonical market classes, Deriv Synthetic as provider under Synthetic, duplicate/order validation extensions |
| Satisfies | Multi-market policy, market-agnostic ingestion |
| Evidence owed | multi-market fixture ingestion/query, no new top-level market, provider isolation tests |

### W2-U03 — Feature Definition Framework + Feature Store v1

| Item | Detail |
|------|--------|
| Type | Infrastructure / feature engineering |
| Scope | feature definitions, feature versioning, causal feature computation contract, feature quality reports |
| Evidence owed | feature version creation, causal window negative test, no symbol identity emitted, reproducible feature hash |

### W2-U04 — Reproducible Dataset Snapshot Builder + Temporal Split Engine

| Item | Detail |
|------|--------|
| Type | Dataset artifact infrastructure |
| Scope | deterministic snapshot build, train/val/test temporal split, artifact checksums, rebuild reproducibility |
| Evidence owed | build dataset twice → same hash; random split rejected; temporal split boundary proof |

### W2-U05 — Experiment Registry + Pre-Registration Workflow

| Item | Detail |
|------|--------|
| Type | Governance infrastructure |
| Scope | experiment registry schema, pre-registration fields, approval/audit trail, immutable experiment plan |
| Evidence owed | undocumented experiment rejected; pre-registered experiment accepted; audit events |

### W2-U06 — Baseline Market-Agnostic Model Harness

| Item | Detail |
|------|--------|
| Type | First model-touching unit |
| Prerequisite | W2-U01 through W2-U05 approved |
| Scope | simplest baseline model family after dependency compatibility proof; no production/live signals |
| Evidence owed | target-platform package compatibility, pre-registered baseline, no symbol identity, research-only output |

### W2-U07 — Statistical Validation Framework

| Item | Detail |
|------|--------|
| Scope | walk-forward, out-of-sample, time-series CV, bootstrap, confidence intervals, effect size, significance |
| Evidence owed | validation report with uncertainty; leakage guard remains active |

### W2-U08 — Calibration + Probability Quality Framework

| Item | Detail |
|------|--------|
| Scope | calibration curves, Brier score, confidence bins, regime/market calibration slices |
| Evidence owed | intentionally miscalibrated fixture detected; calibration report generated |

### W2-U09 — Economic Validation Framework

| Item | Detail |
|------|--------|
| Scope | spread, commission, slippage, latency, liquidity, transaction-cost assumptions |
| Evidence owed | model statistically positive but economically negative scenario reported separately |

### W2-U10 — Multi-Market Generalization + Model Registry / Drift Design

| Item | Detail |
|------|--------|
| Scope | cross-market evaluation, holdout markets, operating-domain guardrails, research model registry, drift monitoring design |
| Evidence owed | trained-on-X evaluated-on-Y report; unsupported domain warning; registry entry complete |

---

## 11. Governance, Risks, and Planned ADRs

### 11.1 Registers touched

| Register | Planned Wave-2 updates |
|----------|------------------------|
| `TECHNICAL_DEBT_REGISTER` | dataset/feature/model deferrals and closures per unit |
| `RISK_REGISTER` | leakage, chronology, synthetic source, package compatibility, drift, calibration, economic validity risks |
| `GOVERNANCE_AMENDMENTS` | only if new standing rules are accepted |
| `PROJECT_STATE` | unit status, evidence status, milestone progression |
| `CHANGELOG` | implementation changes per unit |

### 11.2 Pre-listed risks

| Risk | Severity | Planned mitigation |
|------|----------|--------------------|
| Data leakage / look-ahead | Critical | chronology guard, temporal split engine, negative tests |
| Synthetic/forward simulated records used as real history | High | source authority policy, quarantine, OBS-1 handoff |
| Symbol identity leaks into model | High | feature contract excludes symbol identity, structural tests |
| Py3.14 ML package incompatibility | Medium-High | compatibility spike before adoption |
| Dataset not reproducible | High | content hashes, deterministic ordering, frozen snapshots |
| Calibration omitted | High | dedicated calibration unit |
| Economic viability omitted | High | dedicated economic validation unit |
| P-hacking / undocumented experiments | High | pre-registration gate |
| Drift ignored | Medium | drift monitoring design |

### 11.3 Planned ADRs

| ADR | Unit |
|-----|------|
| Dataset Snapshot Architecture | W2-U01 |
| Chronology Guard Contract | W2-U01 |
| Market-Agnostic Data Access Contract | W2-U02 |
| Feature Store and Feature Versioning | W2-U03 |
| Temporal Split / Snapshot Reproducibility | W2-U04 |
| Experiment Registry and Pre-Registration | W2-U05 |
| Baseline Model Harness | W2-U06 |
| Statistical + Calibration Validation | W2-U07/W2-U08 |
| Economic Validation | W2-U09 |
| Model Registry / Drift Monitoring | W2-U10 |

### 11.4 LOW Wave-1 residuals

| Residual | Plan |
|----------|------|
| R-CI-01 remote CI run | Close opportunistically in W2-U01 if still not closed by W1-U04 ITRGA review. |
| CI pytest-on-PG alignment | Consider adding dedicated PostgreSQL integration tier in W2-U01/W2-U02 when dataset schema arrives. |

---

## 12. Plan Self-Check Against ITRGA Criteria

| Criterion | Plan status |
|-----------|-------------|
| No execution/broker/order path | Satisfied; broker gate remains closed. |
| D-W2-001 honored | Satisfied; generalized market-agnostic default stated and enforced. |
| Dataset governance fields concrete | Satisfied; fields and logical tables listed. |
| Chronology guard testable | Satisfied; contract, stages, quarantine, negative tests defined. |
| Calibration included | Satisfied; dedicated design/unit included. |
| Economic validation included | Satisfied; dedicated design/unit included. |
| Market-agnostic enforced | Satisfied; no symbol identity in learned features. |
| Target-platform realism | Satisfied; package adoption rule for Windows/Py3.14/PostgreSQL 18 included. |
| Unit granularity | Satisfied; W2-U01..W2-U10 independently reviewable. |
| No construction started | Satisfied; this is plan only. |

---

## 13. DA Readiness Statement

> The Development Authority submits this Wave-2 Engineering Design & Implementation Plan for ITRGA review.  
> No Wave-2 implementation, schema migration, dataset pipeline, feature pipeline, experiment, or model training has begun.  
> On ITRGA acceptance, DA will await `BUILD_ORDER_W2-U01` and will not self-authorize construction.

---

**End of Wave 2 Engineering Design & Implementation Plan**
