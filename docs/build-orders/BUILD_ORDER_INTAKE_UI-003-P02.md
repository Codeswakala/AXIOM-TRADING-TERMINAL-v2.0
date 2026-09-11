# BUILD ORDER INTAKE — UI-003-P02

| Field | Value |
|---|---|
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-003 — Professional Market Workspace |
| Phase | UI-003-P02 — Watchlists via Existing Preferences |
| Issuing authority | ITRGA |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-003-P02.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-003-P01.md` |
| Predecessor status | UI-003-P01 APPROVED |
| DA disposition | Accepted for implementation under stated scope |
| Baseline | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 32f/132t |
| Governance Gate | CLOSED |

---

## 1. Binding refinements accepted

The DA accepts the following as binding for UI-003-P02:

- **R-1:** watchlists persist through existing `operator_workspace_preferences`; no new table/migration/column.
- **R-2:** operator evidence must include one raw psql read-back for `workspace_key='professional-market-workspace-v1'`; API read-back does not substitute.
- **R-4:** reorder only if keyboard-accessible; DA defers reorder in P02 and implements keyboard-operable add/remove/focus controls only.
- **R-6:** no execution/actuation, no backend/schema/dependency drift, Level-I evidence.

---

## 2. Scope accepted

UI-003-P02 may implement:

1. watchlist model with symbol/timeframe ids only;
2. existing workspace preference API read/write path;
3. forbidden-field validation;
4. inherited operator scoping through existing endpoint;
5. keyboard-operable add/remove/focus controls.

UI-003-P02 shall not implement a new table, migration, backend endpoint, dependency, execution/actuation path, watchlist positions/quantities/orders/P&L, chart overlays, advisory markers, external AI/LLM, dynamic plugin path, or production certification.

---

## 3. DA authorization posture

This intake records that ITRGA authorized `BUILD_ORDER_UI-003-P02` after approving UI-003-P01.

The DA does not self-approve completion. Completion requires delivery report, operator evidence, and ITRGA review.

---

**End of BUILD_ORDER_INTAKE_UI-003-P02.md**
