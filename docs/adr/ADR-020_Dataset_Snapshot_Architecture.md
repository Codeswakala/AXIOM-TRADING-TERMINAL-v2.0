# ADR-020 — Canonical Dataset Snapshot Architecture

| Field | Value |
|-------|-------|
| ID | ADR-020 |
| Title | Immutable ML dataset snapshots with lineage and quarantine |
| Date | 2026-07-13 |
| Status | Accepted |
| Deciders | Development Authority under Build Order W2-U01 |
| Domain | ML Research / Data Architecture |

---

## Context

Wave 2 requires dataset governance before model work. `07_ML_SPEC` requires every dataset to carry dataset identifier, market, timeframe, date range, source, feature version, creation timestamp, and quality score. No anonymous dataset may enter production research.

## Decision

Add ML-owned dataset governance tables:

- `dataset_snapshots`
- `dataset_series_members`
- `dataset_lineage_records`
- `dataset_quarantine_records`

Dataset snapshots transition `draft → frozen` only after chronology/quality checks. Frozen snapshots are immutable in the service layer. Any modification creates a new version. A deterministic SHA-256 `content_hash` is computed from sorted membership and feature version metadata.

Lineage records trace source candle membership. Quarantine records preserve rejected records with reason code and stage.

## Alternatives Considered

| Option | Outcome | Rationale |
|--------|---------|-----------|
| Store datasets only as files | Rejected | Weak governance/queryability for first ML foundation. |
| Mutate dataset rows in place | Rejected | Breaks reproducibility and auditability. |
| Build feature/model schema first | Rejected | Chronology/dataset integrity is the hard gate before feature/model work. |

## Consequences

- Dataset snapshots are reviewable, traceable, and reproducible.
- Bad data is quarantined instead of silently dropped.
- Future feature/model units can bind to immutable dataset hashes.
- No model training is introduced by this architecture.

## Compliance

Supports `07_ML_SPEC` Dataset Governance, Data Pipeline, and Research Integrity. Aligns with `05_SYSTEM_ARCHITECTURE.md` v2.0 ML Research System ownership.

---

**End ADR-020**
