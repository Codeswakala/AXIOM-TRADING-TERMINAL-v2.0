# Build Order Intake — W2-U03

| Item | Value |
|------|-------|
| Build Order | W2-U03 — Feature Definition Framework + Feature Store v1 |
| Date received | 2026-07-13 |
| Authority | ITRGA, following W2-U02 APPROVED WITH OBSERVATIONS + Operator authorization |
| DA status | ACCEPTED — implementation authorized by issued Build Order |
| Approval | Not self-approved; delivery requires ITRGA review |

---

## 1. Governance confirmation

The Development Authority confirms receipt of `docs/build-orders/BUILD_ORDER_W2-U03.md` and `docs/build-orders/ITRGA_REVIEW_W2-U02.md`.

W2-U02 is **APPROVED WITH OBSERVATIONS**. W2-U03 is **ISSUED**.

## 2. Objective

Build Feature Definition Framework and Feature Store v1 for normalized, causal, versioned, market-agnostic research features, with no model/training/inference/prediction/execution.

## 3. Scope interpretation

| Component | DA interpretation |
|-----------|-------------------|
| A Feature definitions | Versioned feature definitions with uniqueness, lookback window, causal flag, initial normalized causal features. |
| B Causal computation | Reject non-causal/peeking definitions and block guard-quarantined inputs. |
| C D-W2-001 boundary | Feature output excludes symbol/provider/market identity while evaluation metadata remains readable. |
| D Feature Store v1 | Add feature definitions/quality reports; use existing feature records with dataset hash/provider metadata. |
| E Governance/re-captures | ADR/register updates; provide G-1/R-CI evidence commands. |
| F Verification | Add tests for uniqueness, causal negative, feature hash, quality report, D-W2-001 pair, port-only access. |

## 4. Constraints

- No labels, model, training, inference, prediction, execution, broker/provider live connection, or credentials.
- Features must be causal and market-agnostic.
- Metadata may be evaluation-readable but must be feature-excluded.
- No symbol identity feature.
- No direct feature code ORM reach-around.

## 5. Initial risk assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Look-ahead leakage in features | Critical | causal flag, lookback windows, negative peeking test. |
| Symbol/provider identity enters feature vector | High | feature output guard and positive/negative metadata test. |
| Duplicate feature definitions | Medium | DB unique constraint + service validation. |
| Feature reproducibility failure | High | deterministic feature hash test. |

---

**End of intake**
