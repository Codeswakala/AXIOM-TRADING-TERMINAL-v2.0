# ADR-022 — Market-Agnostic Data Access Contract

| Field | Value |
|-------|-------|
| ID | ADR-022 |
| Title | Canonical market-agnostic data access and provider metadata layer |
| Date | 2026-07-13 |
| Status | Accepted |
| Deciders | Development Authority under Build Order W2-U02 |
| Domain | ML Research / Market Data Access / Anti-Corruption |

---

## Context

W2-U02 requires the W2-U01 market data query seam to become the canonical ML entry point for market data. It must support every canonical market class through one uniform contract, while preserving D-W2-001: market-agnostic learning with no symbol identity as a learned feature.

Provider-specific vocabulary must be mapped at the adapter boundary and must not leak inward.

## Decision

Extend the ML dataset access layer with:

- `CanonicalMarketClass` fixed to the canonical market set: synthetic, forex, crypto, stocks, indices, etfs, commodities, futures;
- `MarketSeriesKey(market_class, provider, symbol, timeframe)`;
- `CanonicalOHLCVRecord` with source authority classification;
- `MarketSeriesMetadataRead` for governance/evaluation-only metadata;
- `MarketDataQueryPort` as the sole ML market-data access contract;
- `CandleMarketDataQueryAdapter` as the only ML module that reads existing candle ORM;
- `MarketDataProviderAdapter` contract and `DerivSyntheticIndicesAdapter` skeleton under the Synthetic market class;
- `market_series_metadata` table for stored/queryable metadata.

Deriv Synthetic Indices are modeled as provider `deriv` under market class `synthetic`, never as a new top-level market.

## Alternatives Considered

| Option | Outcome | Rationale |
|--------|---------|-----------|
| Add provider as market class | Rejected | Violates canonical market scope and Build Order. |
| Let ML services query Candle ORM directly | Rejected | Violates port boundary / no reach-around. |
| Store provider metadata only in code | Rejected | Not queryable/governed enough for ML evaluation. |
| Introduce pandas/numpy for this layer | Rejected | Out of scope; existing stack sufficient. |

## Consequences

- Future feature engineering consumes canonical records, not provider-native or ORM rows.
- Metadata remains available for evaluation and guardrails, not model features.
- Provider adapters can be added without changing top-level market classes.
- Live provider connections remain future-gated.

## Compliance

Supports `05_SYSTEM_ARCHITECTURE.md` v2.0 §5, §12, §16, §77 and `07_ML_SPEC` Market-Agnostic Learning / Data Pipeline requirements.

---

**End ADR-022**
