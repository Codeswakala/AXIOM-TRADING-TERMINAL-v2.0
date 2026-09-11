# BUILD ORDER INTAKE — UI-003-P01

| Field | Value |
|---|---|
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-003 — Professional Market Workspace |
| Phase | UI-003-P01 — Professional Market Workspace Frame · Data-Source Inventory · Non-Authoritative Market Presentation |
| Issuing authority | ITRGA |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-003-P01.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-003_DESIGN_PLAN.md` |
| Predecessor status | UI-003 Engineering Design Plan approved with observations + binding refinements R-1…R-6 |
| DA disposition | Accepted for implementation under stated scope |
| Baseline | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 31f/127t |
| Governance Gate | CLOSED |

---

## 1. Binding refinements accepted

The DA accepts the following as binding for UI-003-P01:

- **R-6:** presentation-only, no new analysis, no live/real data, no execution/actuation, visible provenance labels, extend-not-duplicate, accessibility first-class, no new dependency, no-drift substitute evidence, named tests, browser evidence, networked CI.
- **R-1/R-2:** watchlists via existing preferences and raw psql proof bind P02, not P01.
- **R-3:** advisory-signal markers are deferred to P03, not P01.
- **R-4:** watchlist reorder accessibility binds P02/P04, not P01.
- **R-5:** UI-002 P04b is independent and non-blocking.

---

## 2. Scope accepted

UI-003-P01 may implement:

1. chart-centered professional market workspace framing inside the existing `/charts` workspace;
2. existing data-source inventory and market overview presentation;
3. explicit non-authoritative provenance labels for `seed:synthetic` and `live:simulated`;
4. accessible chart summary and controls.

UI-003-P01 shall not implement watchlist persistence, chart overlays/research markers/advisory markers, backend/API/schema changes, new dependency, execution/actuation path, external AI/LLM, dynamic plugin path, or production certification.

---

## 3. DA authorization posture

This intake records that ITRGA authorized `BUILD_ORDER_UI-003-P01` after accepting the UI-003 design plan.

The DA does not self-approve completion. Completion requires delivery report, operator evidence, and ITRGA review.

---

**End of BUILD_ORDER_INTAKE_UI-003-P01.md**
