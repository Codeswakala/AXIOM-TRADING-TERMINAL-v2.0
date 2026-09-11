# ADR-021 — Chronology & Data-Integrity Guard Contract

| Field | Value |
|-------|-------|
| ID | ADR-021 |
| Title | Testable chronology guard for ML dataset integrity |
| Date | 2026-07-13 |
| Status | Accepted |
| Deciders | Development Authority under Build Order W2-U01 |
| Domain | ML Research / Data Integrity / Scientific Integrity |

---

## Context

Wave 2 must prevent leakage, look-ahead, synthetic-as-real contamination, and chronology defects before any model work. ITRGA required the chronology guard to be a testable contract with negative tests.

## Decision

Implement `ChronologyGuard` with explicit stages:

- ingestion;
- dataset construction;
- training-set generation;
- experiment execution.

Guard rules include:

- timezone-aware UTC at trusted boundaries;
- no future record relative to immutable `as_of_time` / `ingestion_finished_at` anchors;
- monotonic non-decreasing `open_time` within series;
- out-of-order authoritative records quarantine by default, not silent resort;
- duplicate natural-key detection;
- synthetic and simulated source exclusion from authoritative training sets;
- temporal-only splits;
- label-horizon/embargo leakage rejection;
- unknown authority quarantine.

Bad records produce `DatasetQuarantineRecord` entries with reason code and detected stage.

## Alternatives Considered

| Option | Outcome | Rationale |
|--------|---------|-----------|
| Sort out-of-order records automatically | Rejected | Could hide source chronology defects and leakage. |
| Drop invalid records silently | Rejected | Violates auditability and scientific integrity. |
| Defer label-horizon checks to split engine | Rejected | W2-U01 must establish the contract and reason code now. |

## Consequences

- Negative tests prove bad records are refused/quarantined.
- Future model units inherit leakage protection.
- Source policies are explicit and auditable.
- Future split engine will build on the existing guard contract.

## Compliance

Supports `07_ML_SPEC` Research Integrity, Dataset Governance, and Statistical Integrity principles. Satisfies W2-U01 R-1, R-2, and R-3 refinements.

---

**End ADR-021**
