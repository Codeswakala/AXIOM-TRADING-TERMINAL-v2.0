# BUILD ORDER INTAKE — UI-004-P05
## Research Artifacts, Collections & Saved-View Preferences

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-004 — Research & Intelligence Workspace |
| Phase | UI-004-P05 |
| Intake date | 2026-07-24 |
| Issuing authority | ITRGA |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-004-P05.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-004-P04.md` + determination copy |
| Predecessor determination | APPROVED WITH OBSERVATIONS |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 41 files / 175 tests |
| Governance Gate | CLOSED |
| Production status | Not certified |

---

## 1. Authorization accepted

The Development Authority records `BUILD_ORDER_UI-004-P05.md` as reissued and binding. UI-004-P05 is authorized after UI-004-P04 Approved-with-Observations.

---

## 2. Scope accepted

Accepted scope is limited to:

1. read-only research artifact context over existing collections, tags, member references, journal references, report ids, signal ids, and source artifact ids;
2. collections/tags read-only context only under R-4;
3. optional saved-view preferences — DA chooses **not** to implement saved-view persistence in P05, so no raw psql persistence capture is claimed or required;
4. P04 observation carry-forward evidence: timeout hardening, CI sentinel fix in evidence, and P04 panel screenshot requirement.

---

## 3. Scope rejected / out of bounds

The DA will not implement in P05:

- saved-view persistence;
- new table/migration/column/backend schema change;
- collection/tag mutation;
- copying report/artifact content into preference state;
- completion checkpoint;
- recompute / re-derivation / stronger relabeling;
- client-side analytics engine;
- external AI/LLM;
- live/real data;
- broker/account/order/execution/Gate path;
- new dependency, new endpoint, or registry/route change.

---

## 4. Planned DA deliverables

| Deliverable | Purpose |
|---|---|
| `frontend/src/pages/InstitutionalIntelligencePage.tsx` | read-only artifact context surface |
| `frontend/src/styles/global.css` | artifact context styling using existing tokens |
| `frontend/src/workstation/research/ResearchArtifactsContext.test.tsx` | six UI-004-P05 named tests |
| `DELIVERY_REPORT_UI-004-P05.md` | DA delivery report; not self-approval |
| `docs/evidence/UI-004-P05_OPERATOR_EVIDENCE_COMMANDS.md` | operator evidence command pack |

---

## 5. Observation closure plan

- OBS-P04-1: timeout-fragile route-loop tests receive explicit 30000 ms test timeout.
- OBS-P04-2: operator evidence pack requires served screenshot of P04 validation/economic panel.
- OBS-P04-3: operator evidence pack uses correct `$LASTEXITCODE` sentinel for local CI.

---

## 6. DA attestation

DA accepts UI-004-P05 as read-only artifact context work with no saved-view persistence. DA does not self-approve the phase. Progression to UI-004-P06 requires ITRGA approval or approved-with-observations of P05.

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

---

**End of BUILD_ORDER_INTAKE_UI-004-P05.md**
