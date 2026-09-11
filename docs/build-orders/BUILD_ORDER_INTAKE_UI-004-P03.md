# BUILD ORDER INTAKE — UI-004-P03
## Intelligence Report Viewers & Drilldowns

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-004 — Research & Intelligence Workspace |
| Phase | UI-004-P03 |
| Intake date | 2026-07-24 |
| Issuing authority | ITRGA |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-004-P03.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-004-P02b.md` |
| Predecessor determination | APPROVED — CI env-flake waived by operator |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 39 files / 165 tests |
| Governance Gate | CLOSED |
| Production status | Not certified |

---

## 1. Authorization accepted

The Development Authority records `ITRGA_REVIEW_UI-004-P02b.md` as APPROVED. The review explicitly authorizes `BUILD_ORDER_UI-004-P03` for Intelligence Report Viewers & Drilldowns.

---

## 2. Scope accepted

Accepted scope is limited to:

1. first-party report family navigation over existing intelligence report families;
2. first-party report detail viewer over existing stored W4/W7 report payloads;
3. progressive disclosure of stored artifact fields, source lineage, report integrity, limitations, and stored payload;
4. verbatim display of report hashes, method/version, sample counts, uncertainty, lineage, source ids, and limitations;
5. no recompute, no report generation, no external renderer, no AI/LLM summary, and Level-I evidence.

---

## 3. Scope rejected / out of bounds

The DA will not implement in P03:

- validation/economic-usefulness integrity panels — deferred to P04;
- research artifacts/collections/saved views — deferred to P05;
- report generation;
- recomputation, re-derivation, or reclassification of stored verdicts;
- external renderer/markdown/AI/LLM dependency;
- backend/API/schema/migration/dependency changes;
- registry changes;
- browser-side analytics engine;
- live/real data;
- execution/order/broker/account/Gate paths.

---

## 4. Planned DA deliverables

| Deliverable | Purpose |
|---|---|
| `frontend/src/pages/InstitutionalIntelligencePage.tsx` | first-party intelligence report viewer and drilldown implementation |
| `frontend/src/styles/global.css` | report viewer/drilldown styling using existing tokens |
| `frontend/src/workstation/research/ResearchReportViewers.test.tsx` | five UI-004-P03 named tests |
| `DELIVERY_REPORT_UI-004-P03.md` | DA delivery report; not self-approval |
| `docs/evidence/UI-004-P03_OPERATOR_EVIDENCE_COMMANDS.md` | operator evidence command pack |

---

## 5. No-drift method

UI-004-P03 no-drift evidence shall rely on:

- per-phase named frontend tests;
- target `alembic current` = `20260717_0037`;
- package manifest content check for no new dependency;
- no-new-endpoint/source grep;
- no registry-change proof;
- backend/frontend regression totals.

---

## 6. DA attestation

DA accepts UI-004-P03 as report-viewer/drilldown-only frontend presentation work. DA does not self-approve the phase. Progression to UI-004-P04 requires ITRGA approval or approved-with-observations of P03.

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

---

**End of BUILD_ORDER_INTAKE_UI-004-P03.md**
