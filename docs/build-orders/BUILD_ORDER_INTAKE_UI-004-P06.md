# BUILD ORDER INTAKE — UI-004-P06
## UI-004 Completion Checkpoint

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-004 — Research & Intelligence Workspace |
| Phase | UI-004-P06 — Completion Checkpoint |
| Intake date | 2026-07-24 |
| Issuing authority | ITRGA |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-004-P06.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-004-P05.md` |
| Predecessor determination | APPROVED WITH OBSERVATIONS |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 42 files / 181 tests |
| Governance Gate | CLOSED |
| Production status | Not certified |

---

## 1. Authorization accepted

The Development Authority records `BUILD_ORDER_UI-004-P06.md` as binding. UI-004-P06 is authorized as a completion checkpoint.

---

## 2. Scope accepted

Accepted scope is limited to:

1. completion checkpoint tests and final integration evidence;
2. whole-surface no-recompute/no-inference/no-external-AI/no-actuation proof;
3. regression and no-drift evidence;
4. hard non-waivable browser screenshot gate for P04 and P05 panels;
5. constitutional and Doc 16 brand self-check.

---

## 3. Scope rejected / out of bounds

The DA will not implement in P06:

- any new capability;
- recomputation/re-derivation/reclassification;
- client-side analytics engine;
- external AI/LLM;
- live/real data;
- broker/account/order/execution/Gate path;
- new table/migration/dependency/endpoint/registry route;
- saved-view persistence not already reviewed;
- production readiness certification.

---

## 4. Planned DA deliverables

| Deliverable | Purpose |
|---|---|
| `frontend/src/workstation/research/ResearchIntelligenceCompletion.test.tsx` | five UI-004-P06 completion tests |
| `DELIVERY_REPORT_UI-004-P06.md` | DA delivery report and completion self-check; not self-approval |
| `docs/evidence/UI-004-P06_OPERATOR_EVIDENCE_COMMANDS.md` | operator evidence command pack |

---

## 5. DA attestation

DA accepts UI-004-P06 as a completion checkpoint only. DA will not self-declare UI-004 complete. ITRGA must independently review and declare completion if satisfied.

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

---

**End of BUILD_ORDER_INTAKE_UI-004-P06.md**
