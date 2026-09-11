# ADR-030 — Multi-Market Generalization, Model Registry Maturation, and Drift Design

| Field | Value |
|-------|-------|
| ID | ADR-030 |
| Title | Research-only generalization reports, operating-domain guardrails, model registry links, and no-auto-retrain drift design |
| Date | 2026-07-15 |
| Status | Accepted |
| Deciders | Development Authority under Build Order W2-U10 |
| Domain | ML Research / Generalization / Model Registry / Drift Monitoring |

---

## Context

W2-U10 is the final Wave-2 unit. It must demonstrate the primary D-W2-001 goal: a generalized market-agnostic model evaluated across held-out markets and bounded by an explicit operating domain. It must mature the research model registry by linking statistical, calibration, and economic verdicts, and design drift monitoring without live loops or auto-retraining.

## Decision

Implement pure-Python research-only services for:

- trained-on-X / evaluated-on-Y generalization reports;
- spatial holdout validation layered over temporal split assumptions;
- operating-domain warning for unsupported market/timeframe/regime;
- model registry maturation linking U07 statistical, U08 calibration, and U09 economic reports;
- drift monitoring records for feature/prediction/concept/calibration/performance/regime drift categories;
- no-auto-retrain guarantee: drift is recorded and governance-required, never automatically retrains.

No live monitoring loop, live signal, execution, broker connection, or auto-retrain path is introduced.

## Alternatives Considered

| Option | Outcome | Rationale |
|--------|---------|-----------|
| Live drift monitor loop | Rejected | Wave 3+; W2 remains historical/research only. |
| Auto-retrain on drift | Rejected | Violates ML_SPEC continuous learning governance. |
| Store report links only in docs | Rejected | Registry must answer usability from persisted fields. |
| Evaluate markets without operating-domain warning | Rejected | Out-of-domain guardrail required. |

## Consequences

- Registry entries link model, statistical, calibration, and economic evidence.
- Generalization reports can expose weak transfer honestly.
- Drift evidence is visible without silently changing models.
- Research Framework Complete milestone becomes reviewable by ITRGA after W2-U10 approval.

---

**End ADR-030**
