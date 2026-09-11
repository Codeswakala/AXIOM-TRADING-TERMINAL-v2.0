# Delivery Report — W2-U03

| Field | Value |
|-------|-------|
| Build Order | **W2-U03** ML Research: Feature Definition Framework + Feature Store v1 |
| Platform | **0.15.0** |
| Date | 2026-07-13 |
| Author | Development Authority |
| Status | **Implemented — submitted for ITRGA review** |
| Approval | **Not self-approved** |
| Governing decision | D-W2-001 — generalized, market-agnostic model |
| Builds on | W2-U01 dataset/chronology + W2-U02 market data query/metadata |

---

## 1. Executive Summary

W2-U03 implements AXIOM's **Feature Definition Framework** and **Feature Store v1**. It turns canonical market data into normalized, causal, versioned, market-agnostic feature records while enforcing the two highest-risk boundaries for this layer:

1. **No look-ahead / non-causal features** — peeking definitions are rejected.
2. **No symbol/provider/market identity in feature output** — metadata remains evaluation-readable but feature-excluded.

This unit computes research features only. It introduces **no labels, no model, no training, no inference, no prediction, no execution, no broker/provider live connection, and no credentials**.

---

## 2. Hypothesis / counter-hypotheses

### Hypothesis

AXIOM can compute an initial causal, market-agnostic feature set and persist reproducible feature records without leakage, duplicate definitions, or symbol identity contamination.

### Counter-hypotheses

| Counter | Result | Evidence |
|---------|--------|----------|
| Duplicate feature definitions may be allowed | **Falsified** | service validation + DB uniqueness; `test_feature_definition_uniqueness` |
| Peeking/non-causal feature may be accepted | **Falsified** | `test_non_causal_feature_definition_rejected` raises `NonCausalFeatureError` / `FEATURE_LOOKAHEAD` |
| Forward-dated guarded records may reach feature computation | **Falsified** | `test_forward_dated_guarded_record_blocked_before_feature_computation` |
| Symbol/provider/market identity may enter feature output | **Falsified** | `test_feature_output_excludes_identity_but_evaluation_metadata_readable` |
| Evaluation metadata may become unavailable | **Falsified** | same test proves metadata readable for evaluation while excluded from feature vector |
| Feature hash may be non-reproducible | **Falsified** | `test_feature_store_compute_hash_reproducible_and_quality_report` |
| Feature code may reach around the query port into candle ORM | **Falsified structurally** | `test_feature_code_uses_query_port_not_candle_orm` |

---

## 3. Implementation Summary

### 3.1 Feature definition framework

Added package:

```text
backend/app/ml/features/
```

Key files:

```text
definitions.py
errors.py
store.py
__init__.py
```

Feature definition contract:

```text
FeatureDefinitionSpec
  feature_name
  feature_version
  formula_spec
  input_requirements
  lookback_window
  causal
  market_compatibility_notes
```

### 3.2 Initial causal market-agnostic feature set

Added built-in feature set v1:

| Feature | Family | Causal window |
|---------|--------|---------------|
| `return_1` | returns | current bar only |
| `range_pct` | volatility/range normalization | current bar only |
| `rolling_return_3` | trend persistence | current + prior two closes |

All are normalized and market-agnostic. No volume/order-flow feature is fabricated.

### 3.3 Look-ahead guard

Non-causal definitions are rejected by:

```text
FeatureDefinitionSpec.assert_causal()
```

A definition with:

```text
causal=False
formula_spec.uses_future=True
```

raises:

```text
NonCausalFeatureError("FEATURE_LOOKAHEAD")
```

### 3.4 Feature store service

Added:

```text
FeatureStoreService
```

Capabilities:

- register feature definitions;
- reject duplicate `(feature_name, feature_version)`;
- register built-in definitions;
- compute causal features from `CanonicalOHLCVRecord` inputs;
- block feature computation if W2-U01 chronology guard rejects inputs;
- persist feature records;
- create feature quality report;
- compute deterministic feature content hash;
- expose evaluation metadata separately from feature output.

### 3.5 Feature store schema

Added Alembic migration:

```text
backend/alembic/versions/20260713_0007_w2_u03_feature_store.py
```

New tables:

```text
feature_definitions
feature_quality_reports
```

Extended existing table:

```text
feature_records
  provider
  source_dataset_hash
```

### 3.6 D-W2-001 enforcement

Feature output excludes identity fields:

```text
symbol
provider
market_class
```

Evaluation metadata remains readable through:

```text
MarketMetadataService
```

This implements the positive/negative pair requested by ITRGA:

- negative: identity is absent from feature vector;
- positive: metadata remains readable for evaluation/slicing.

---

## 4. Governance / Documentation Updates

Added:

- `docs/build-orders/ITRGA_REVIEW_W2-U02.md`
- `docs/build-orders/BUILD_ORDER_W2-U03.md`
- `docs/build-orders/BUILD_ORDER_INTAKE_W2-U03.md`
- `docs/adr/ADR-023_Feature_Store_And_Causal_Features.md`
- `docs/evidence/W2-U03_OPERATOR_EVIDENCE_COMMANDS.md`

Updated:

- `PROJECT_STATE.md`
- `CHANGELOG.md`
- `README.md`
- `docs/governance/RISK_REGISTER.md`
- `docs/governance/TECHNICAL_DEBT_REGISTER.md`
- `docs/governance/GOVERNANCE_AMENDMENTS.md`
- `docs/governance/04_PROJECT_ROADMAP.md`

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
collected 112 items
112 passed, 1 warning
```

### 5.2 Alembic local migration

Command:

```bash
cd backend
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w2u03.db' \
AXIOM_ENVIRONMENT=testing \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_JWT_SECRET_KEY="<REDACTED_JWT_SECRET>" \
alembic upgrade head
AXIOM_DATABASE_URL='sqlite+aiosqlite:////tmp/axiom_w2u03.db' alembic current
```

Result:

```text
Running upgrade 20260713_0006 -> 20260713_0007
20260713_0007 (head)
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
backend/tests/test_feature_store.py
```

Tests:

| Test | Purpose |
|------|---------|
| `test_feature_definition_uniqueness` | duplicate definition rejected |
| `test_non_causal_feature_definition_rejected` | peeking feature rejected with `FEATURE_LOOKAHEAD` |
| `test_feature_store_compute_hash_reproducible_and_quality_report` | feature records + deterministic hash + quality report |
| `test_feature_output_excludes_identity_but_evaluation_metadata_readable` | D-W2-001 positive/negative pair |
| `test_forward_dated_guarded_record_blocked_before_feature_computation` | chronology guard blocks bad feature inputs |
| `test_feature_code_uses_query_port_not_candle_orm` | no feature-code ORM reach-around |
| `test_no_symbol_identity_feature_pattern_in_feature_modules` | no symbol identity pattern in feature modules |

Backend baseline increased from **105** to **112**.

---

## 7. Explicit Negative Evidence

| Prohibited item | Proof |
|-----------------|-------|
| duplicate feature definition | rejected |
| peeking feature | rejected `FEATURE_LOOKAHEAD` |
| guard-quarantined future record in feature computation | rejected before computation |
| symbol/provider/market identity in feature vector | absent from feature output |
| metadata unavailable for evaluation | metadata readable separately |
| non-reproducible feature hash | recomputed hash matches |
| feature code Candle ORM reach-around | structural test passes |
| model/training/inference | not implemented |

---

## 8. Operator Evidence Command Pack

Created:

```text
docs/evidence/W2-U03_OPERATOR_EVIDENCE_COMMANDS.md
```

It includes Windows/PowerShell + PostgreSQL commands for:

1. PostgreSQL migration to `20260713_0007`;
2. full backend/frontend test console;
3. G-1 named ML test capture;
4. causal/look-ahead negative tests;
5. D-W2-001 feature exclusion evidence;
6. reproducible feature hash and quality report evidence;
7. port-only and no-symbol-identity grep;
8. CI/local equivalent;
9. parity smoke.

---

## 9. Out of Scope Confirmed

Not implemented in W2-U03:

- labels/targets;
- temporal split engine;
- experiment registry;
- model training;
- model evaluation;
- inference;
- prediction;
- execution;
- broker/provider live connection;
- credentials;
- numpy/pandas/scikit-learn adoption.

---

## 10. Risks and Unknowns

| Risk / Unknown | Status | Mitigation |
|----------------|--------|------------|
| PostgreSQL migration not DA-run | Operator evidence required | command pack includes PG migration |
| Remote CI run | Still carried | command pack includes local/remote evidence |
| Advanced statistical feature quality | Deferred | report shape present; deeper stats later |
| Feature consumption by models | Deferred | W2-U06+ only after W2-U01–U05 proven |

---

## 11. Confidence Statement

| Dimension | Rating | Justification |
|-----------|--------|---------------|
| Feature framework design | **HIGH** | definitions, uniqueness, causal guard implemented |
| Causal/look-ahead protection | **HIGH in DA tests** | peeking feature and future input negative tests pass |
| D-W2-001 feature exclusion | **HIGH in DA tests** | feature vector excludes identity; metadata readable separately |
| Feature reproducibility | **HIGH in DA tests** | deterministic hash recomputation passes |
| Target-platform correctness | **LIMITED until Operator evidence lands** | Windows + PostgreSQL evidence required by Build Order |
| Overall package | **MODERATE-HIGH for implementation; conditional for approval evidence** | mandatory operator evidence remains required |

No percentage confidence is asserted.

---

## 12. Readiness Statement

> W2-U03 is implemented, tested locally, documented, and submitted for independent ITRGA review.  
> No labels, model, training, inference, prediction, execution, broker connection, provider live connection, or credentials have been introduced.  
> DA does **not** self-approve.  
> Operator-run Windows + PostgreSQL evidence remains mandatory for approval.  
> W2-U04 must not begin until ITRGA disposition and subsequent Build Order authorization.

---

**End of Delivery Report W2-U03**
