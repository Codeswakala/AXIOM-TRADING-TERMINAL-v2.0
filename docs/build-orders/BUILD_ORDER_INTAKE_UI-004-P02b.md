# BUILD ORDER INTAKE — UI-004-P02b
## Performance Analytics Integration

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-004 — Research & Intelligence Workspace |
| Phase | UI-004-P02b |
| Intake date | 2026-07-23 |
| Issuing authority | ITRGA |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-004-P02b.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-004-P02.md` |
| Predecessor determination | APPROVED — CI env-flake waived by operator |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 38 files / 161 tests |
| Governance Gate | CLOSED |
| Production status | Not certified |

---

## 1. Authorization accepted

The Development Authority records `ITRGA_REVIEW_UI-004-P02.md` as APPROVED. The review explicitly authorizes `BUILD_ORDER_UI-004-P02b` for performance analytics integration with no-cherry-picking focus.

---

## 2. Scope accepted

Accepted scope is limited to:

1. read-only analytics metric and confidence-band panels from existing `fetchAdvisoryAnalytics`;
2. stored sample counts, uncertainty, notes, limitations, included scope, source artifact ids, and unreliability warnings;
3. read-only signal-to-analytics context navigation;
4. no client-side performance metric computed from displayed rows;
5. no-recompute/no-inference/no-cherry-picking guardrail and Level-I evidence.

---

## 3. Scope rejected / out of bounds

The DA will not implement in P02b:

- report viewers/drilldowns — deferred to P03;
- validation/economic-usefulness panels — deferred to P04;
- saved-view persistence — deferred to P05;
- collection/tag mutation — prohibited in UI-004;
- client-side aggregate/metric computation from displayed rows;
- raw-score-as-confidence;
- backend/API/schema/migration/dependency changes;
- registry changes;
- external AI/LLM;
- live/real data;
- execution/order/broker/account/Gate paths.

---

## 4. Planned DA deliverables

| Deliverable | Purpose |
|---|---|
| `frontend/src/pages/InstitutionalIntelligencePage.tsx` | integrated read-only performance analytics panel in the research workspace |
| `frontend/src/styles/global.css` | analytics panel/card/scope styling using existing tokens |
| `frontend/src/workstation/research/ResearchPerformanceAnalytics.test.tsx` | four UI-004-P02b named tests |
| `DELIVERY_REPORT_UI-004-P02b.md` | DA delivery report; not self-approval |
| `docs/evidence/UI-004-P02b_OPERATOR_EVIDENCE_COMMANDS.md` | operator evidence command pack |

---

## 5. No-drift method

UI-004-P02b no-drift evidence shall rely on:

- per-phase named frontend tests;
- target `alembic current` = `20260717_0037`;
- package manifest content check for no new dependency;
- no-new-endpoint/source grep;
- no registry-change proof;
- backend/frontend regression totals.

---

## 6. DA attestation

DA accepts UI-004-P02b as analytics-only, frontend presentation/integration work. DA does not self-approve the phase. Progression to UI-004-P03 requires ITRGA approval or approved-with-observations of P02b.

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

---

**End of BUILD_ORDER_INTAKE_UI-004-P02b.md**
