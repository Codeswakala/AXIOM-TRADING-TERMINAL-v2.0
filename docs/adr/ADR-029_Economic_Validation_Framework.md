# ADR-029 — Economic Validation Framework

| Field | Value |
|-------|-------|
| ID | ADR-029 |
| Title | Research-only economic validation with cost provenance and sensitivity |
| Date | 2026-07-15 |
| Status | Accepted |
| Deciders | Development Authority under Build Order W2-U09 |
| Domain | ML Research / Economic Validation / Research Integrity |

---

## Context

`07_ML_SPEC` requires economic validation separate from predictive/statistical validation. A model may be statistically positive and still economically unusable after spread, commission, slippage, latency, liquidity, and transaction costs. Prior review also carried R-4: cost inputs must declare provenance and assumed ranges.

## Decision

Implement a pure-Python economic validation framework that:

- applies spread, commission, slippage, latency, liquidity, and transaction costs to hypothetical research P&L;
- classifies every cost input as measured, provider-published, or assumed;
- requires assumed costs to include sensitivity ranges;
- reports optimistic/base/pessimistic scenarios;
- reports statistical and economic conclusions independently;
- flags statistically-positive/economically-negative cases;
- persists research-only economic reports with deterministic report hashes and audit events.

No execution, order path, broker connection, paper trading, or live signal is introduced.

## Alternatives Considered

| Option | Outcome | Rationale |
|--------|---------|-----------|
| Single cost assumption | Rejected | False precision; violates R-4 sensitivity requirement. |
| Combine statistical/economic verdict | Rejected | Violates economic validation separation mandate. |
| Add execution simulator | Rejected | Wave 6 only. |
| Use compiled analytics dependency | Rejected | Pure Python sufficient for W2-U09. |

## Consequences

- Economic usability is independently visible.
- Cost assumption sensitivity is explicit.
- Good statistical/calibration results cannot hide negative economics.
- Reports remain research-only.

---

**End ADR-029**
