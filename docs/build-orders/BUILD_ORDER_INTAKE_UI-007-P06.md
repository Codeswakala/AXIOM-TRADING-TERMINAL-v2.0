# BUILD ORDER INTAKE — UI-007-P06

**UI-007 Completion Checkpoint** — *(Proof unit · final UI-007 phase)*

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-007 — Governance & Evidence Workspace |
| Phase | **UI-007-P06 — Completion Checkpoint** |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-007-P06.md` |
| Predecessor verdict | `docs/build-orders/ITRGA_REVIEW_UI-007-P05_FINAL.md` — Approved with Observations |
| Baseline of record | v0.62.0 · Alembic `20260717_0037` · backend 414 · frontend 60 files / 271 tests |
| Intake status | Accepted under ITRGA Build Order; proof-only scope |
| Governance Gate | CLOSED |
| Production | NOT CERTIFIED |

---

## 1. Authority confirmation

P05 is approved with observations. P06 is authorized as the final UI-007 **proof unit**, not as a product or feature unit.

The accepted work thesis is:

> Governance is visible without becoming governable from the UI.

No production capability, control, panel, field, filter, endpoint, dependency, or persistence addition is authorized.

---

## 2. Accepted completion work

P06 will provide only:

- five named whole-workspace completion tests;
- a P06 evidence runner and operator command pack;
- R-6 raw PostgreSQL read-only audit-verbatim command sequence;
- browser evidence checklist covering P01 through P05 plus logged-out protection;
- documentation/register synchronization and residual disposition.

The existing P01…P05 workspace implementation remains unchanged except for an evidence-prompt punctuation clarification required by OBS-P05-5.

---

## 3. Explicit non-authorizations

P06 does not authorize:

- a new UI surface, panel, control, field, filter, or user capability;
- backend/API/schema/table/migration/dependency/route/registry/persistence modification;
- governance/audit/Gate/certification/validation/readiness/residual mutation;
- operations controls or any actuation;
- AI/LLM, recompute, inference, reclassification, or generated summary;
- remediation of `TD-AXIOM-GIT-PROVENANCE`, `TD-UI005-COMPLETION-TIMEOUT`, or Vite chunk-size observation;
- production certification, execution, order, broker, account, or live-money functionality.

---

## 4. Completion proof design

| Requirement | P06 proof method |
|---|---|
| Discoverability | Whole workspace test renders P01 governance frame, P02 status/certification/residuals, P03 audit, P04 evidence/validation, and P05 operational posture. |
| Read-only inert boundary | Rendered-control and full-source tests reject governance mutation, Gate/certification control, operations actuation, recompute, and external AI. |
| G-5 integrity | Fixtures verify refusal text, validation scope/sample/uncertainty/limitations, runtime/certification separation, and all residuals including provenance debt. |
| R-6 audit proof | Operator raw `psql SELECT` with a stored `*_REFUSED` row and served UI matching-row screenshot; no audit write is permitted. |
| UI-001/UI-002 | Shell, protected route, registry/navigation invariants validated by completion test and browser pass. |
| Residual honesty | Command pack lists every required residual and requires final visible status confirmation. |

---

## 5. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Completion implies production certification | Critical | Explicit same-surface `Production NOT CERTIFIED / Doc 11 HELD` completion assertions. |
| Completion hides a P01…P05 boundary gap | Critical | Whole-source and whole-workspace named tests plus browser pass. |
| Audit proof fabricates a new row | High | Existing row only; read-only psql SELECT; no save/mutation step. |
| Green-only residual summary | High | Explicit all-residual disclosure requirement, including high provenance debt. |
| Evidence relay repeats wrong-phase attachment | High | Runner transcript must contain `UI007_P06`; operator command pack requires pre-send check. |

**DA does not self-approve. Gate remains CLOSED. Production remains NOT CERTIFIED.**
