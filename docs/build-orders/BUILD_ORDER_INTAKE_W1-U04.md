# Build Order Intake — W1-U04

| Item | Value |
|------|-------|
| Build Order | W1-U04 — Wave 1 Closure & Hardening |
| Date received | 2026-07-13 |
| Authority | ITRGA, following W1-U03 APPROVED WITH OBSERVATIONS + Operator authorization |
| DA status | ACCEPTED — implementation authorized by issued Build Order |
| Approval | Not self-approved; delivery requires ITRGA review |

---

## 1. Governance confirmation

The Development Authority confirms receipt of `docs/build-orders/BUILD_ORDER_W1-U04.md`.

The Build Order records W1-U03 as **APPROVED WITH OBSERVATIONS** and authorizes W1-U04 as the Wave-1 closure/hardening unit.

## 2. Objective

Close Wave 1 cleanly by remediating frontend critical/high supply-chain vulnerabilities, consolidating the CI gate including npm-audit, syncing registers, and declaring the roadmap milestone **Core Platform Operational** only after evidence.

## 3. Scope interpretation

| Component | DA interpretation |
|-----------|-------------------|
| A Green CI run | Update CI/local gate to include npm audit; produce commands for real green run evidence. |
| B Frontend supply-chain | Remediate critical/high vulnerabilities; prove fresh `npm ci` + `npm audit` 0 vulnerabilities/highs and no frontend regression. |
| C Registers/milestone | Reconcile TD/Risk/Amendments/Project State/Roadmap; mark TD-012 closed; carry OBS-1 into Wave 2. |
| D Verification | Re-run backend/frontend, broker-gate tests, parity smoke commands, and evidence pack. |

## 4. Constraints

- No product behavior, broker connection, execution, ML/AI, chart features, or new markets.
- Broker Governance Gate remains closed.
- No secrets in code/config/CI/logs.
- No regression of approved behavior.

## 5. Initial risk assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Dependency major upgrades break frontend | High | Run `npm ci`, vitest, tsc, build; document versions. |
| CI audit gate blocks due unresolved advisory | Medium | Remediate first; then add audit gate at high/critical threshold. |
| Broker gate weakened by unrelated changes | Critical | Re-run `test_broker_integration.py -vv`; no broker changes intended. |
| Remote CI unavailable | Medium | Provide local orchestration fallback; remote green run remains preferred. |

## 6. Implementation authorization posture

Build Order accepted. DA will implement, verify, document, and submit a Delivery Report. DA does not self-approve W1-U04 or self-authorize Wave 2.

---

**End of intake**
