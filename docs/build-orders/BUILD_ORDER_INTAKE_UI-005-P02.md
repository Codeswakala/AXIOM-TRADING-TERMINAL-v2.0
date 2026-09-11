# BUILD ORDER INTAKE — UI-005-P02
## Signal Investigation Lineage & Related Evidence

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-005 — Investigation & Planning Workspace |
| Phase | UI-005-P02 |
| Intake date | 2026-07-24 |
| Issuing authority | ITRGA |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-005-P02.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-005-P01.md` |
| Predecessor determination | APPROVED WITH OBSERVATIONS |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 44 files / 191 tests |
| Governance Gate | CLOSED |
| Production status | Not certified |

---

## 1. Authorization accepted

The Development Authority records `ITRGA_REVIEW_UI-005-P01.md` as APPROVED WITH OBSERVATIONS. The review authorizes `BUILD_ORDER_UI-005-P02`.

---

## 2. Scope accepted

Accepted scope is limited to:

1. signal investigation lineage and guardrail context;
2. stored calibrated confidence, validation/report ids, freshness, economic verdict, and related evidence links;
3. read-only navigation to existing report/chart/signal context;
4. no recompute, no model rerun, no signal mutation, no guardrail override, no action recommendation.

---

## 3. Scope rejected / out of bounds

The DA will not implement in P02:

- Scenario/Portfolio integration;
- Trade Planning/Journal changes;
- Execution Research integration;
- persistence/saved-view state;
- backend/API/schema/migration/dependency/endpoint changes;
- registry route changes;
- recomputation/inference/re-derivation/signal generation/action recommendation/external AI;
- order/broker/account/live-real/Gate path.

---

## 4. Planned DA deliverables

| Deliverable | Purpose |
|---|---|
| `frontend/src/pages/SignalInvestigationPage.tsx` | related evidence links and lineage/context enhancements |
| `frontend/src/styles/global.css` | related evidence link styling using existing tokens |
| `frontend/src/workstation/investigation/SignalInvestigationLineage.test.tsx` | five UI-005-P02 named tests |
| `DELIVERY_REPORT_UI-005-P02.md` | DA delivery report; not self-approval |
| `docs/evidence/UI-005-P02_OPERATOR_EVIDENCE_COMMANDS.md` | operator evidence command pack |

---

## 5. DA attestation

DA accepts UI-005-P02 as read-only signal-investigation lineage/evidence work only. DA does not self-approve the phase. Progression to UI-005-P03 requires ITRGA approval or approved-with-observations of P02.

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

---

**End of BUILD_ORDER_INTAKE_UI-005-P02.md**
