# BUILD ORDER INTAKE — UI-002-P03

| Field | Value |
|---|---|
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-002 — Workflow Navigation Framework |
| Phase | UI-002-P03 — Command Palette Extension · Quick-Action Catalogue |
| Issuing authority | ITRGA |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-002-P03.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-002-P02.md` |
| Predecessor status | UI-002-P02 APPROVED WITH OBSERVATIONS |
| DA disposition | Accepted for implementation under stated scope |
| Baseline | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 28f/109t |
| Governance Gate | CLOSED |

---

## 1. Binding refinements and observations accepted

The DA accepts the following as binding for UI-002-P03:

- **R-4:** one overlay infrastructure and one command system; extend the existing UI-001 Command Palette, do not create a second palette or overlay.
- **R-5:** quick actions are navigation/UI-toggle only; registry must reject unsupported command definitions and no-actuation source grep must be clean.
- **R-6:** Level-I evidence bar applies.
- **OBS-P02(UI002)-1:** close at P03 intake/evidence by providing clean scoped UI-only diff proof and `alembic current` printing `20260717_0037`.

---

## 2. Scope accepted

UI-002-P03 may implement:

1. typed `CommandRegistry` restricted to `navigation` and `ui-toggle`;
2. the ITRGA-vetted 28-action quick-action catalogue only;
3. existing Command Palette consumption of the registry;
4. rejection tests for unsupported or unvetted commands;
5. accessibility/focus validation for the existing palette.

UI-002-P03 shall not implement global search, backend/API/schema changes, new dependency, second palette/overlay, external AI/LLM, dynamic plugin path, execution/actuation path, or production certification.

---

## 3. DA authorization posture

This intake records that ITRGA authorized `BUILD_ORDER_UI-002-P03` after approving UI-002-P02 with observations.

The DA does not self-approve completion. Completion requires delivery report, operator evidence, and ITRGA review.

---

**End of BUILD_ORDER_INTAKE_UI-002-P03.md**
