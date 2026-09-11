# BUILD ORDER INTAKE — UI-005-P03
## Scenario Comparison & Portfolio Research Context

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-005 — Investigation & Planning Workspace |
| Phase | UI-005-P03 |
| Intake date | 2026-07-24 |
| Issuing authority | ITRGA |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-005-P03.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-005-P02.md` |
| Predecessor determination | APPROVED WITH OBSERVATIONS |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 45 files / 196 tests |
| Governance Gate | CLOSED |
| Production status | Not certified |

---

## 1. Authorization accepted

The Development Authority records `ITRGA_REVIEW_UI-005-P02.md` as APPROVED WITH OBSERVATIONS. The review authorizes `BUILD_ORDER_UI-005-P03`.

---

## 2. Scope accepted

Accepted scope is limited to:

1. scenario comparison as read-only/hypothetical planning evidence over existing stored scenario reports;
2. portfolio research as hypothetical review context over existing portfolio research dashboard/report preview;
3. read-only context links between scenario/portfolio evidence and investigation workflow;
4. scope/sample/assumptions/uncertainty/limitations/source ids visible;
5. no generation, no recompute, no real portfolio/account/P&L/live allocation, no actuation.

---

## 3. Scope rejected / out of bounds

The DA will not implement in P03:

- Trade Planning / Journal changes;
- Execution Research integration;
- persistence/saved-view state;
- backend/API/schema/migration/dependency/endpoint changes;
- registry route changes;
- scenario generation / new what-if engine;
- portfolio recomputation / live allocation / real account / real P&L;
- external AI/LLM;
- order/broker/account/live-real/Gate path.

---

## 4. Planned DA deliverables

| Deliverable | Purpose |
|---|---|
| `frontend/src/pages/ScenarioComparisonPage.tsx` | scenario investigation context links and wording hardening |
| `frontend/src/pages/PortfolioResearchPage.tsx` | portfolio investigation context links and source id visibility |
| `frontend/src/workstation/investigation/ScenarioPortfolioContext.test.tsx` | five UI-005-P03 named tests |
| `DELIVERY_REPORT_UI-005-P03.md` | DA delivery report; not self-approval |
| `docs/evidence/UI-005-P03_OPERATOR_EVIDENCE_COMMANDS.md` | operator evidence command pack |

---

## 5. DA attestation

DA accepts UI-005-P03 as read-only scenario/portfolio context work only. DA does not self-approve the phase. Progression to UI-005-P04 requires ITRGA approval or approved-with-observations of P03.

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

---

**End of BUILD_ORDER_INTAKE_UI-005-P03.md**
