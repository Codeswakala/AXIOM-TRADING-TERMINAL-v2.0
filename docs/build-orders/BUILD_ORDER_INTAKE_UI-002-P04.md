# BUILD ORDER INTAKE — UI-002-P04

| Field | Value |
|---|---|
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-002 — Workflow Navigation Framework |
| Phase | UI-002-P04 — Global Search Framework · Read-Only Source Adapters · Search Overlay |
| Issuing authority | ITRGA |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-002-P04.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-002-P03.md` |
| Predecessor status | UI-002-P03 APPROVED WITH OBSERVATIONS |
| DA disposition | Accepted for implementation under stated scope |
| Baseline | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 29f/115t |
| Governance Gate | CLOSED |

---

## 1. Binding refinements and gates accepted

The DA accepts the following as binding for UI-002-P04:

- **OBS-P03(UI002)-1 hard intake gate:** P04 operator evidence must begin with clean `SCOPED_DIFF_NO_MATCHING_FILENAMES` and `alembic current` output matching `20260717_0037`.
- **R-2:** first search slice is limited to workspace + signals + journal + research-collections.
- **R-5:** search results are read-only navigation targets only; no hidden action surface.
- **R-6:** Level-I evidence bar applies.

---

## 2. Scope accepted

UI-002-P04 may implement:

1. `GlobalSearchResult` model with `resultAction: "navigate"` and `readonly: true`;
2. first-party deterministic client-side search ranking/index utility;
3. read-only source adapters for exactly workspace, signals, journal, and research-collections using existing read APIs;
4. Region-F global search overlay using the existing overlay family;
5. keyboard/focus/screen-reader behavior;
6. no query/artifact persistence.

UI-002-P04 shall not implement backend search index, new endpoint/table/migration/column, sources beyond R-2 first slice, new dependency, second overlay/search shell, external AI/LLM, dynamic plugin path, execution/actuation path, or production certification.

---

## 3. DA authorization posture

This intake records that ITRGA authorized `BUILD_ORDER_UI-002-P04` after approving UI-002-P03 with observations and hard P04 intake gate.

The DA does not self-approve completion. Completion requires delivery report, operator evidence, and ITRGA review.

---

**End of BUILD_ORDER_INTAKE_UI-002-P04.md**
