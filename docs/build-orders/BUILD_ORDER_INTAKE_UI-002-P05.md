# BUILD ORDER INTAKE — UI-002-P05

| Field | Value |
|---|---|
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-002 — Workflow Navigation Framework |
| Phase | UI-002-P05 — Context-Aware Workflow Integration & UI-002 Completion Checkpoint |
| Issuing authority | ITRGA |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-002-P05.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-002-P04.md` |
| Predecessor status | UI-002-P04 APPROVED WITH OBSERVATIONS |
| DA disposition | Accepted for implementation under stated scope |
| Baseline | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 30f/121t |
| Governance Gate | CLOSED |

---

## 1. Binding refinements and gates accepted

The DA accepts the following as binding for UI-002-P05:

- **OBS-P04(UI002)-1 hard intake gate:** next delivery evidence must establish a phase-isolating baseline and provide a meaningful UI-only/no-drift diff plus `alembic current = 20260717_0037`.
- **R-2:** P04b remaining search adapters are optional; DA defers P04b in P05 unless explicitly authorized separately.
- **R-4:** one shell, one navigation system, one command palette, one overlay family.
- **R-5:** whole navigation/search/palette/switcher/breadcrumb surface contains no execution or actuation controls.
- **R-6:** Level-I evidence bar applies.

---

## 2. Scope accepted

UI-002-P05 may implement:

1. cross-route consistency validation for breadcrumbs, switcher, context navigation, search, and palette;
2. registry-consistency checks over all UI-002 navigation surfaces;
3. responsive hardening for shell navigation/search/palette surfaces;
4. UI-002 completion checkpoint tests and documentation.

UI-002-P05 shall not implement backend/API/schema changes, new dependency, new business capability, execution/actuation path, external AI/LLM, dynamic plugin path, production certification, or any second navigation/palette/overlay system.

---

## 3. P04b disposition

P04b remaining search adapters are **deferred** in this P05 implementation. This final P05 focuses on integration and UI-002 completion checkpoint over the accepted first-slice global search.

---

## 4. DA authorization posture

This intake records that ITRGA authorized `BUILD_ORDER_UI-002-P05` after approving UI-002-P04 with observations.

The DA does not self-approve completion. Completion requires delivery report, operator evidence, and ITRGA review.

---

**End of BUILD_ORDER_INTAKE_UI-002-P05.md**
