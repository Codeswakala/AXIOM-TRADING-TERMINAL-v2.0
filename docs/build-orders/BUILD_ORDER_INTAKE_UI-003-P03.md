# BUILD ORDER INTAKE — UI-003-P03

| Field | Value |
|---|---|
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-003 — Professional Market Workspace |
| Phase | UI-003-P03 — Chart Overlays · Research Markers · Annotation Integration |
| Issuing authority | ITRGA |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-003-P03.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-003-P02_FINAL.md` |
| Predecessor status | UI-003-P02 APPROVED |
| DA disposition | Accepted for implementation under stated scope |
| Baseline | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 33f/137t |
| Governance Gate | CLOSED |

---

## 1. Binding refinements accepted

The DA accepts the following as binding for UI-003-P03:

- **R-3:** advisory-signal markers, if included, are inert read-only badges over existing records only. They are not generated signals, instructions, actions, or orders.
- **R-6:** no new analysis, no inference, no actuation, no backend/schema/dependency drift, accessibility first-class, named tests displayed, browser evidence, CI.

---

## 2. Scope accepted

UI-003-P03 may implement:

1. overlay visibility controls as presentation toggles only;
2. W5-U03 annotation layer presentation hardening over existing chart research annotations;
3. read-only advisory-signal markers from existing `fetchAdvisorySignals` read API;
4. marker-list accessibility alternative;
5. provenance, uncertainty, and research-only labels.

UI-003-P03 shall not implement signal generation, inference, authoritative recompute, new annotation creation beyond existing W5-U03 API, backend/API/schema changes, new dependency, execution/actuation path, external AI/LLM, dynamic plugin path, or production certification.

---

## 3. DA authorization posture

This intake records that ITRGA authorized `BUILD_ORDER_UI-003-P03` after approving UI-003-P02.

The DA does not self-approve completion. Completion requires delivery report, operator evidence, and ITRGA review.

---

**End of BUILD_ORDER_INTAKE_UI-003-P03.md**
