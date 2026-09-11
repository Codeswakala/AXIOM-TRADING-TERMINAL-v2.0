# Build Order Intake — W2-U01

| Item | Value |
|------|-------|
| Build Order | W2-U01 — ML Research: Canonical Dataset Architecture + Chronology & Data-Integrity Guard |
| Date received | 2026-07-13 |
| Authority | ITRGA, following Wave 2 Design Plan acceptance + Operator authorization |
| DA status | ACCEPTED — implementation authorized by issued Build Order |
| Approval | Not self-approved; delivery requires ITRGA review |

---

## 1. Governance confirmation

The Development Authority confirms receipt of `docs/build-orders/BUILD_ORDER_W2-U01.md`.

The Build Order authorizes the first Wave-2 implementation unit: dataset architecture and chronology/data-integrity guard. No model, training, inference, broker, execution, or live signal behavior is authorized.

## 2. Objective

Build the hard-gate foundation of the ML Research Framework: immutable/versioned dataset snapshots with mandatory governance fields, provenance/lineage/quarantine tables, a formal chronology guard contract, and a market-data query port.

## 3. Scope interpretation

| Component | DA interpretation |
|-----------|-------------------|
| A Dataset architecture | Add Alembic tables for dataset snapshots, series members, lineage, and quarantine. |
| B Chronology guard | Implement formal guard rules for UTC, future records, monotonicity, synthetic/simulated exclusion, temporal splits, duplicate/source authority. |
| C Required refinements | Implement R-1 no silent resort, R-2 label-horizon leakage, R-3 immutable trusted anchors. |
| D Query port | Add explicit MarketDataQueryPort backed by existing candle repository/table. |
| E Registers/ADRs | Add dataset and chronology ADRs; update risks/debt/state/changelog. |
| F Verification | Add negative tests proving bad records are quarantined/rejected; preserve full suite. |

## 4. Constraints

- No model, training, inference, prediction, signal, broker, execution, or order path.
- No direct ML reach-around scattered through ORM; use query port seam.
- No symbol identity as learned feature.
- No anonymous datasets.
- No silent dropping or reordering of bad data.
- Preserve all Wave-0/Wave-1 hardening.

## 5. Initial risk assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Data leakage/look-ahead | Critical | Chronology guard + temporal split/label horizon negative tests. |
| Synthetic chronology enters training | High | source authority classification + quarantine/exclusion. |
| Dataset not reproducible | High | deterministic content hash and frozen snapshot immutability. |
| ML code reaches around persistence boundaries | Medium | MarketDataQueryPort contract and tests. |

## 6. Implementation authorization posture

Build Order accepted. DA will implement, verify, document, and submit a Delivery Report. DA does not self-approve W2-U01 or authorize W2-U02.

---

**End of intake**
