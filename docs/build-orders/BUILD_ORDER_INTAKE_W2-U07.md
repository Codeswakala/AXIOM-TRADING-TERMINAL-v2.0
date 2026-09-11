# Build Order Intake — W2-U07

| Item | Value |
|------|-------|
| Build Order | W2-U07 — Statistical Validation Framework |
| Date received | 2026-07-14 |
| Authority | ITRGA, following W2-U06 APPROVED + Operator authorization |
| DA status | ACCEPTED — implementation authorized by issued Build Order |
| Approval | Not self-approved; delivery requires ITRGA review |

---

## 1. Governance confirmation

The Development Authority confirms receipt of `docs/build-orders/ITRGA_REVIEW_W2-U06.md` and `docs/build-orders/BUILD_ORDER_W2-U07.md`.

W2-U06 is approved. W2-U07 is authorized to implement statistical validation framework only.

## 2. Objective

Add research-only statistical validation reports with temporal walk-forward validation, bootstrap confidence intervals, effect size, significance, uncertainty-mandatory contract, and leakage refusals.

## 3. Scope interpretation

| Component | DA interpretation |
|-----------|-------------------|
| A Compatibility | Use pure-Python/stdlib implementation; no compiled ML dependency. |
| B Walk-forward | Time-ordered folds with embargo respected. |
| C OOS/CV | Temporal validation only; random CV refused. |
| D Uncertainty | Bootstrap distribution, confidence interval, effect size, p-value. |
| E Reports | Persist validation reports bound to experiment/model artifact, research-only. |
| F Governance | ADR/register/state/changelog; no calibration/economic validation yet. |

## 4. Constraints

- No live signals, execution, broker/provider live connection, or new model family.
- No point-estimate-only reports.
- No random/shuffled validation.
- No p-hacking or post-hoc plan changes.
- No symbol identity as feature.

---

**End of intake**
