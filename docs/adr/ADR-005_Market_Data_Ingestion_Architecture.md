# ADR-005 — Market Data Ingestion Architecture

| Field | Value |
|-------|--------|
| ID | ADR-005 |
| Title | Historical CSV ingestion pipeline via service + repositories |
| Date | 2026-07-10 |
| Status | Accepted |
| Deciders | Development Authority (W0-U03) |
| Domain | Architecture / Market Data |

---

## Problem Statement

AXIOM needs a controlled path to load historical OHLCV into the `candles` table without live feeds or broker coupling.

## Context

W0-U02 delivered async persistence and `Candle` natural keys. W0-U03 requires CSV historical loading, validation, and observability while preserving multi-market extensibility.

## Constraints

- Repository pattern mandatory  
- Synchronous job orchestration only  
- No live WS, ticks, ML features, advanced gap fill  
- Path safety for verification APIs  

## Alternatives

| Option | Outcome |
|--------|---------|
| A. Service + CSV loader + normalize + repo upsert | **Selected** |
| B. Background workers / Celery | Deferred (scope) |
| C. Bulk SQL COPY bypassing repos | Rejected (architecture) |
| D. Live feed adapters | Out of scope |

## Decision

Implement `app/ingestion/` with:

- `csv_loader` (header alias mapping)
- `normalize` (UTC timestamps, OHLCV quality)
- `IngestionService` (orchestration, stats, audit)
- `ingestion_runs` table for job metadata
- Verification API under `/api/v1/ingestion/*` with allowlisted paths

## Trade-offs

- Sync jobs simpler, not for high-volume production loads  
- Row-by-row upsert correct for foundation; bulk insert deferred  

## Risks

- Path-based CSV API must remain allowlisted  
- Postgres production path still Operator-verified (TD-001b)

## Future Implications

Live feed adapters can emit `NormalizedCandleRow` into the same upsert path without changing natural keys.

## Related Roadmap

Wave 1 market services; Wave 2 feature pipelines; later live streams.

---

**End of ADR-005**
