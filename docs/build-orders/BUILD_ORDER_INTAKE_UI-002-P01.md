# BUILD ORDER INTAKE — UI-002-P01

| Field | Value |
|---|---|
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-002 — Workflow Navigation Framework |
| Phase | UI-002-P01 — Workflow Metadata · Breadcrumb Foundation · UI-001 Registry Reconciliation |
| Issuing authority | ITRGA |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-002-P01.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-002_DESIGN_PLAN.md` |
| Design plan status | Approved with observations + binding refinements R-1…R-6 |
| DA disposition | Accepted for implementation under stated scope |
| Baseline | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 26f/97t |
| Governance Gate | CLOSED |

---

## 1. Binding refinements accepted

The DA accepts the following refinements as binding for UI-002-P01:

- **R-1:** companion workflow metadata keyed by `workspace.id`; UI-001 14-field Workspace Registration Contract must not be modified.
- **R-5:** no hidden action surface; P01 navigation/breadcrumb source must contain no execution or actuation paths.
- **R-6:** Level-I evidence bar applies, including operator-run target evidence, named tests displayed passing, browser evidence, networked CI, head unchanged, and UI-only diff.

R-2, R-3, and R-4 are acknowledged as binding for later UI-002 phases and are not implemented in P01.

---

## 2. Scope accepted

UI-002-P01 may implement:

1. separate workflow metadata module keyed by existing UI-001 `workspace.id` values;
2. metadata validation utilities;
3. deterministic breadcrumb model derived from route + registry + workflow metadata;
4. `BreadcrumbTrail` rendered inside UI-001 Region A.

UI-002-P01 shall not implement global search, workspace switcher, recent-workspace persistence, command-palette quick actions, context-aware navigation suggestions, backend/API/schema changes, new dependency, new route, execution/actuation path, external AI/LLM, dynamic plugin path, or production certification.

---

## 3. DA authorization posture

This intake records that ITRGA authorized `BUILD_ORDER_UI-002-P01` after accepting the UI-002 design plan.

The DA does not self-approve completion. Completion requires delivery report, operator evidence, and ITRGA review.

---

**End of BUILD_ORDER_INTAKE_UI-002-P01.md**
