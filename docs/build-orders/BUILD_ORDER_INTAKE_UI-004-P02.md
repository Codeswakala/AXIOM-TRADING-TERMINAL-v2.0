# BUILD ORDER INTAKE — UI-004-P02
## Advisory Signals Integration

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-004 — Research & Intelligence Workspace |
| Phase | UI-004-P02 |
| Intake date | 2026-07-23 |
| Issuing authority | ITRGA |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-004-P02.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-004-P01.md` |
| Predecessor determination | APPROVED — CI env-flake waived by operator |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 37 files / 156 tests |
| Governance Gate | CLOSED |
| Production status | Not certified |

---

## 1. Authorization accepted

The Development Authority records `ITRGA_REVIEW_UI-004-P01.md` as APPROVED. The review explicitly authorizes `BUILD_ORDER_UI-004-P02` for advisory signals integration only, with analytics split to P02b under R-3.

---

## 2. Scope accepted

Accepted scope is limited to:

1. read-only advisory signal cards/details from existing `fetchAdvisorySignals` / existing advisory records;
2. stored guardrail, calibration, freshness, economic verdict, rationale, and lineage presentation;
3. calibrated confidence display from stored calibrated field only;
4. read-only context navigation links;
5. disclaimers and non-actionable presentation;
6. no-recompute/no-inference guardrail and Level-I evidence.

---

## 3. Scope rejected / out of bounds

The DA will not implement in P02:

- performance analytics integration — deferred to P02b;
- report viewers or drilldowns — deferred to P03;
- validation/economic-usefulness panels — deferred to P04;
- saved-view persistence — deferred to P05;
- collection/tag mutation — prohibited in UI-004;
- raw-score-as-confidence;
- backend/API/schema/migration/dependency changes;
- registry changes;
- client-side inference, authoritative recomputation, signal generation, verdict reclassification, or analytics computation;
- external AI/LLM;
- live/real data;
- execution/order/broker/account/Gate paths.

---

## 4. Planned DA deliverables

| Deliverable | Purpose |
|---|---|
| `frontend/src/pages/InstitutionalIntelligencePage.tsx` | integrated read-only advisory signal research panel in the research workspace |
| `frontend/src/styles/global.css` | advisory panel/card/detail styling using existing tokens |
| `frontend/src/workstation/research/ResearchAdvisorySignals.test.tsx` | five UI-004-P02 named tests |
| `DELIVERY_REPORT_UI-004-P02.md` | DA delivery report; not self-approval |
| `docs/evidence/UI-004-P02_OPERATOR_EVIDENCE_COMMANDS.md` | operator evidence command pack |

---

## 5. No-drift method

UI-004-P02 no-drift evidence shall rely on:

- per-phase named frontend tests;
- target `alembic current` = `20260717_0037`;
- package manifest content check for no new dependency;
- no-new-endpoint/source grep;
- no registry-change proof;
- backend/frontend regression totals.

---

## 6. DA attestation

DA accepts UI-004-P02 as advisory-only, frontend presentation/integration work. DA does not self-approve the phase. Progression to UI-004-P02b requires ITRGA approval or approved-with-observations of P02.

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

---

**End of BUILD_ORDER_INTAKE_UI-004-P02.md**
