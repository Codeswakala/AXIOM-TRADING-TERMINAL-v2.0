# BUILD ORDER INTAKE — UI-002-P02

| Field | Value |
|---|---|
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-002 — Workflow Navigation Framework |
| Phase | UI-002-P02 — Workspace Switcher · Context-Navigation Seam · Recent-Workspace Persistence (R-3) |
| Issuing authority | ITRGA |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-002-P02.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-002-P01.md` |
| Predecessor status | UI-002-P01 APPROVED CLEAN |
| DA disposition | Accepted for implementation under stated scope |
| Baseline | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 27f/103t |
| Governance Gate | CLOSED |

---

## 1. Binding refinements accepted

The DA accepts the following refinements as binding for UI-002-P02:

- **R-3:** if recents persist, they may persist only as route/workspace ids in existing `operator_workspace_preferences.layout_config`; no search queries, artifact payloads, business fields, table, migration, or column. For P02 DA will keep recents **in memory only** and will not persist them durably.
- **R-4:** one overlay infrastructure and one command system; the switcher is an inline Region-A shell control, not a second palette/overlay.
- **R-5:** switcher and context-navigation source must contain no execution or actuation paths.
- **R-6:** Level-I evidence bar applies, including operator-run target evidence, named tests displayed passing, browser evidence, networked CI, head unchanged, and UI-only diff.

---

## 2. Scope accepted

UI-002-P02 may implement:

1. `WorkspaceSwitcher` in existing Region A, driven by RBAC-visible UI-001 registry entries;
2. static context-navigation targets rendered through existing Region D / PanelHost;
3. keyboard operation and focus restoration;
4. in-memory previous/recent workspace ids only, with no durable persistence in this phase.

UI-002-P02 shall not implement global search, command-palette quick actions, backend-computed context suggestions, new route, backend/API/schema changes, dependency, execution/actuation path, external AI/LLM, dynamic plugin path, or production certification.

---

## 3. DA authorization posture

This intake records that ITRGA authorized `BUILD_ORDER_UI-002-P02` after approving UI-002-P01 clean.

The DA does not self-approve completion. Completion requires delivery report, operator evidence, and ITRGA review.

---

**End of BUILD_ORDER_INTAKE_UI-002-P02.md**
