# BUILD ORDER INTAKE — UI-004-P01
## Research Workspace Frame · Data-Source Inventory · No-Recompute Guardrail

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-004 — Research & Intelligence Workspace |
| Phase | UI-004-P01 |
| Intake date | 2026-07-23 |
| Issuing authority | ITRGA |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-004-P01.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-004_DESIGN_PLAN.md` |
| Predecessor determination | APPROVED WITH OBSERVATIONS + BINDING REFINEMENTS R-1…R-7 |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 36 files / 151 tests |
| Governance Gate | CLOSED |
| Production status | Not certified |

---

## 1. Authorization accepted

The Development Authority records `ITRGA_REVIEW_UI-004_DESIGN_PLAN.md` as APPROVED WITH OBSERVATIONS + BINDING REFINEMENTS R-1…R-7. The review explicitly authorizes `BUILD_ORDER_UI-004-P01`.

UI-004-P01 is authorized for the narrow frontend-only frame/data-source/no-recompute guardrail scope defined in the Build Order.

---

## 2. Scope accepted

Accepted scope is limited to:

1. enhancing the existing `/intelligence` workspace frame inside the existing UI-001/UI-002 shell;
2. adding overview cards for intelligence/signals/analytics/validation/economic-usefulness/artifacts as thin read-only/data-source inventory surfaces;
3. proving every surface maps to existing governed read APIs/stores;
4. establishing the no-recompute/no-inference guardrail as the spine of UI-004;
5. preserving Doc 16 brand gates and Level-I evidence.

---

## 3. Scope rejected / out of bounds

The DA will not implement in P01:

- registry route additions, relabels, or 14-field contract changes;
- advisory-signal integration beyond source-inventory cards;
- analytics integration beyond source-inventory cards;
- report viewers or drilldowns;
- validation/economic-usefulness panels beyond readiness/source inventory;
- saved-view persistence;
- collection/tag mutation;
- backend/API/schema/migration/dependency changes;
- client-side inference, authoritative recomputation, signal generation, regime inference, verdict reclassification, or no-cherry-picking violations;
- external AI/LLM;
- live/real data;
- execution/order/broker/account/Gate paths.

---

## 4. Planned DA deliverables

| Deliverable | Purpose |
|---|---|
| `frontend/src/pages/InstitutionalIntelligencePage.tsx` | UI-004-P01 research workspace frame and governed data-source inventory |
| `frontend/src/styles/global.css` | responsive/brand-consistent frame and inventory styling using existing tokens |
| `frontend/src/workstation/research/ResearchWorkspaceFrame.test.tsx` | five UI-004-P01 named tests |
| `DELIVERY_REPORT_UI-004-P01.md` | DA delivery report; not self-approval |
| `docs/evidence/UI-004-P01_OPERATOR_EVIDENCE_COMMANDS.md` | operator evidence command pack |

---

## 5. No-drift method

Per ITRGA standing method for this single-commit DA repository, git-diff phase isolation is not used. UI-004-P01 no-drift evidence shall rely on:

- per-phase named frontend tests;
- target `alembic current` = `20260717_0037`;
- package manifest content check for no new dependency;
- no-new-endpoint/source grep;
- no registry-change proof;
- backend/frontend regression totals.

---

## 6. DA attestation

The DA accepts UI-004-P01 as a narrow presentation/inventory/guardrail phase only. DA will not self-approve the phase. Progression to UI-004-P02 requires ITRGA approval or approved-with-observations of P01.

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

---

**End of BUILD_ORDER_INTAKE_UI-004-P01.md**
