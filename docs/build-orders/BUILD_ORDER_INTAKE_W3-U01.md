# Build Order Intake — W3-U01

| Item | Value |
|------|-------|
| Build Order | W3-U01 — Live Inference Engine + Governed Model Eligibility Gate |
| Date received | 2026-07-15 |
| Authority | ITRGA, following Wave 3 Design Plan acceptance + Operator authorization |
| DA status | ACCEPTED — implementation authorized by issued Build Order |
| Approval | Not self-approved; delivery requires ITRGA review |

---

## 1. Governance confirmation

The Development Authority confirms receipt of `docs/build-orders/BUILD_ORDER_W3-U01.md`.

W3-U01 is backend-only and safety-focused. It authorizes deterministic inference and governed eligibility checks only. It does not authorize operator-facing signal emission, UI, alerts, live signal WebSocket, execution, broker connection, orders, positions, or paper trading.

## 2. Objective

Implement the Live Inference Engine and Governed Model Eligibility Gate so only fully governed, explicitly advisory-approved models are eligible to score deterministic inference inputs.

## 3. Scope interpretation

| Component | DA interpretation |
|-----------|-------------------|
| A Deterministic inference | score same model/input twice → same score and input hash. |
| B Eligibility gate | full W2 lineage + advisory_approved + input/domain checks required. |
| C Promotion lifecycle | advisory status fields and audited promotion action. |
| D No execution boundary | no broker/order/signal surface; structural tests/grep. |
| E Governance | ADR/register/state/changelog/evidence updates. |
| F Verification | refusal tests, deterministic tests, persisted promotion proof, no regression. |

---

**End of intake**
