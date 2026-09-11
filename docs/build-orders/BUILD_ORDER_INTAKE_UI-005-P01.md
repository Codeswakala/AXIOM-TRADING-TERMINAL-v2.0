# BUILD ORDER INTAKE — UI-005-P01
## Investigation & Planning Workspace Frame · Data-Source Inventory · No-Actuation Guardrail

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-005 — Investigation & Planning Workspace |
| Phase | UI-005-P01 |
| Intake date | 2026-07-24 |
| Issuing authority | ITRGA |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-005-P01.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-005_DESIGN_PLAN.md` |
| Predecessor determination | APPROVED WITH OBSERVATIONS + BINDING REFINEMENTS R-1…R-7 |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 43 files / 186 tests |
| Governance Gate | CLOSED |
| Production status | Not certified |

---

## 1. Authorization accepted

The Development Authority records `ITRGA_REVIEW_UI-005_DESIGN_PLAN.md` as APPROVED WITH OBSERVATIONS + BINDING REFINEMENTS R-1…R-7. The review authorizes `BUILD_ORDER_UI-005-P01`.

---

## 2. Scope accepted

Accepted scope is limited to:

1. enhancing existing `/investigate` as the primary UI-005 workflow hub;
2. showing a data-source inventory for Signal Investigation, Scenario Comparison, Trade Planning, Execution Research, Research Journal, and Portfolio Research;
3. no-actuation, no-recompute, research-only guardrail framing;
4. no persistence and no mutation changes.

---

## 3. Scope rejected / out of bounds

The DA will not implement in P01:

- surface deep integration;
- mutation changes to Trade Planning / Journal;
- persistence or saved-view state;
- backend/API/schema/migration/dependency/endpoint changes;
- registry route changes;
- recomputation, inference, re-derivation, scenario generation, client-side analytics engine, external AI/LLM, or action recommendation;
- order/broker/account/live-real/Gate path.

R-5 mapping accepted at intake:

```text
P03 = Scenario Comparison + Portfolio Research
P05 = Execution Research (SIMULATED) only
```

---

## 4. Planned DA deliverables

| Deliverable | Purpose |
|---|---|
| `frontend/src/pages/SignalInvestigationPage.tsx` | UI-005 frame and data-source inventory on existing `/investigate` |
| `frontend/src/styles/global.css` | frame/inventory styling using existing tokens |
| `frontend/src/workstation/investigation/InvestigationPlanningFrame.test.tsx` | five UI-005-P01 named tests |
| `DELIVERY_REPORT_UI-005-P01.md` | DA delivery report; not self-approval |
| `docs/evidence/UI-005-P01_OPERATOR_EVIDENCE_COMMANDS.md` | operator evidence command pack |

---

## 5. No-drift method

UI-005-P01 no-drift evidence shall rely on:

- per-phase named frontend tests;
- target `alembic current` = `20260717_0037`;
- package manifest content check for no new dependency;
- no-new-endpoint/source grep;
- no registry-change proof;
- backend/frontend regression totals.

---

## 6. DA attestation

DA accepts UI-005-P01 as frame/inventory/guardrail work only. DA does not self-approve the phase. Progression to UI-005-P02 requires ITRGA approval or approved-with-observations of P01.

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

---

**End of BUILD_ORDER_INTAKE_UI-005-P01.md**
