# Build Order Intake — W2-U08

| Item | Value |
|------|-------|
| Build Order | W2-U08 — Calibration + Probability Quality Framework |
| Date received | 2026-07-14 |
| Authority | ITRGA, following W2-U07 APPROVED + Operator authorization |
| DA status | ACCEPTED — implementation authorized by issued Build Order |
| Approval | Not self-approved; delivery requires ITRGA review |

---

## 1. Governance confirmation

The Development Authority confirms receipt of `docs/build-orders/BUILD_ORDER_W2-U08.md`.

W2-U08 is authorized to implement calibration/probability-quality research reports only.

## 2. Objective

Add reliability bins, Brier score, ECE, per-slice calibration, miscalibration warnings, and base-rate-aware significance correction.

## 3. Scope interpretation

| Component | DA interpretation |
|-----------|-------------------|
| A Compatibility | Pure-Python implementation; no compiled dependency. |
| B Calibration metrics | reliability bins, Brier, ECE. |
| C Warning | miscalibrated fixture flagged; well-calibrated not flagged. |
| D Slices | market/timeframe/regime slice calibration. |
| E Base-rate null | no-information-rate significance default. |
| F Report | persisted research-only calibration report and hash. |

---

**End of intake**
