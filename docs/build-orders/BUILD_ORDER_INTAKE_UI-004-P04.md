# BUILD ORDER INTAKE — UI-004-P04
## Validation & Economic-Usefulness Integrity Panels

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-004 — Research & Intelligence Workspace |
| Phase | UI-004-P04 |
| Intake date | 2026-07-24 |
| Issuing authority | ITRGA |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-004-P04.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-004-P03.md` |
| Predecessor determination | APPROVED — CI env-flake waived by operator |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 40 files / 170 tests |
| Governance Gate | CLOSED |
| Production status | Not certified |

---

## 1. Authorization accepted

The Development Authority records `ITRGA_REVIEW_UI-004-P03.md` as APPROVED. The review explicitly authorizes `BUILD_ORDER_UI-004-P04` for Validation & Economic-Usefulness Integrity Panels.

---

## 2. Scope accepted

Accepted scope is limited to:

1. dedicated validation/economic-usefulness panels for existing reports/signals;
2. verbatim rendering of stored statuses/verdicts such as `research_only`, `not_assessed`, and `warning:*`;
3. sample counts, scope/source ids, uncertainty, and limitations visible;
4. research-only disclaimers and non-actionable presentation;
5. no re-derivation, no stronger relabeling, no client-side analytics engine, and Level-I evidence.

---

## 3. Scope rejected / out of bounds

The DA will not implement in P04:

- research artifacts/collections/saved-view persistence — deferred to P05;
- completion checkpoint — deferred to P06;
- re-derivation/recompute/stronger relabeling of validation or economic-usefulness verdicts;
- client-side analytics engine;
- backend/API/schema/migration/dependency changes;
- registry changes;
- external AI/LLM;
- live/real data;
- execution/order/broker/account/Gate paths.

---

## 4. Planned DA deliverables

| Deliverable | Purpose |
|---|---|
| `frontend/src/pages/InstitutionalIntelligencePage.tsx` | validation/economic integrity panel implementation |
| `frontend/src/styles/global.css` | validation/economic panel styling using existing tokens |
| `frontend/src/workstation/research/ResearchValidationEconomicIntegrity.test.tsx` | five UI-004-P04 named tests |
| `DELIVERY_REPORT_UI-004-P04.md` | DA delivery report; not self-approval |
| `docs/evidence/UI-004-P04_OPERATOR_EVIDENCE_COMMANDS.md` | operator evidence command pack |

---

## 5. No-drift method

UI-004-P04 no-drift evidence shall rely on:

- per-phase named frontend tests;
- target `alembic current` = `20260717_0037`;
- package manifest content check for no new dependency;
- no-new-endpoint/source grep;
- no registry-change proof;
- backend/frontend regression totals.

---

## 6. DA attestation

DA accepts UI-004-P04 as validation/economic integrity frontend presentation work only. DA does not self-approve the phase. Progression to UI-004-P05 requires ITRGA approval or approved-with-observations of P04.

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

---

**End of BUILD_ORDER_INTAKE_UI-004-P04.md**
