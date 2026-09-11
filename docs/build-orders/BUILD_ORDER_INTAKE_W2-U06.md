# Build Order Intake — W2-U06

| Item | Value |
|------|-------|
| Build Order | W2-U06 — Baseline Market-Agnostic Model Harness |
| Date received | 2026-07-14 |
| Authority | ITRGA, following W2-U05 APPROVED WITH OBSERVATIONS + Operator authorization |
| DA status | ACCEPTED — implementation authorized by issued Build Order |
| Approval | Not self-approved; delivery requires ITRGA review |

---

## 1. Governance confirmation

The Development Authority confirms receipt of `docs/build-orders/ITRGA_VERDICT_W2-U05_FINAL.md` and `docs/build-orders/BUILD_ORDER_W2-U06.md`.

W2-U05 is approved; the hard model gate is open only for this research-only baseline harness unit.

## 2. Objective

Implement the first baseline market-agnostic model harness that can train only through an approved, hash-pinned experiment and produces research-only model artifacts.

## 3. Scope interpretation

| Component | DA interpretation |
|-----------|-------------------|
| A Compatibility spike | Use pure-Python stdlib baseline to avoid unsupported ML wheels; record no new ML package. |
| B Baseline model | Deterministic majority-class baseline; proves harness mechanics, not skill. |
| C Governance-bound training | `train(experiment_id)` accepts only approved, pinned experiments and refuses off-governance paths. |
| D Model artifact registry | Extend `model_artifacts` with experiment, dataset, split, hyperparameters, artifact hash, research-only status. |
| E Inert evaluation | Store simple metrics as research artifacts only; no live signal or endpoint. |
| F Verification | Refusal tests, reproducibility, artifact fields, no live signal, no regression. |

## 4. Constraints

- No live signal, no execution, no broker connection, no production deployment.
- No training outside approved/pinned experiment.
- No random re-splitting or identity in model input.
- No fabricated or cherry-picked metrics; weak baseline acceptable.
- No new ML dependency unless target-compatible; pure-Python fallback used.

---

**End of intake**
