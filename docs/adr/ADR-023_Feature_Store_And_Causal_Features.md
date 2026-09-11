# ADR-023 — Feature Definition Framework and Feature Store v1

| Field | Value |
|-------|-------|
| ID | ADR-023 |
| Title | Causal market-agnostic feature definitions and reproducible feature store |
| Date | 2026-07-13 |
| Status | Accepted |
| Deciders | Development Authority under Build Order W2-U03 |
| Domain | ML Research / Feature Engineering / Feature Store |

---

## Context

W2-U03 is the first unit to compute research features. This is the point where data leakage or symbol identity could enter the ML path. `07_ML_SPEC` requires feature engineering and feature store governance with versioning, reproducibility, low leakage, and no duplicate definitions. D-W2-001 requires generalized market-agnostic learning.

## Decision

Implement a feature framework with:

- `FeatureDefinitionSpec` declaring `feature_name`, `feature_version`, `formula_spec`, `input_requirements`, `lookback_window`, `causal`, and market compatibility notes;
- database uniqueness for `(feature_name, feature_version)`;
- rejection of non-causal/peeking definitions;
- initial normalized market-agnostic causal features: `return_1`, `range_pct`, and `rolling_return_3`;
- `FeatureStoreService` for definition registration, causal feature computation, deterministic feature hashing, and feature quality report persistence;
- feature outputs excluding `symbol`, `provider`, and `market_class` identity fields;
- evaluation metadata readable separately through the W2-U02 metadata service.

No labels, models, training, inference, or prediction are introduced.

## Alternatives Considered

| Option | Outcome | Rationale |
|--------|---------|-----------|
| Adopt pandas/numpy now | Rejected | W2-U03 can be implemented with stdlib/existing stack; target Py3.14 dependency risk deferred. |
| Use symbol/provider as categorical features | Rejected | Violates D-W2-001. |
| Allow non-causal definitions but mark them | Rejected | Look-ahead leakage must fail loudly. |
| Defer feature quality report | Rejected | Feature Store spec requires quality reporting foundation. |

## Consequences

- Feature definitions are versioned and unique.
- Feature records can be recomputed deterministically to the same hash.
- Feature quality report shape exists, but advanced stationarity/drift analysis is deferred.
- Metadata remains evaluation-readable but feature-excluded.

## Compliance

Supports `07_ML_SPEC` Feature Engineering, Feature Store, Feature Quality, and Research Integrity. Aligns with D-W2-001 and `05_SYSTEM_ARCHITECTURE.md` v2.0 ML Research boundaries.

---

**End ADR-023**
