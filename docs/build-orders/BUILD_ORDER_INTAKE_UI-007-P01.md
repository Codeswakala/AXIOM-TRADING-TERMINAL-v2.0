# BUILD ORDER INTAKE — UI-007-P01

**Governance Workspace Frame · `/governance` Route · Data-Source Inventory · Read-Only Guardrails**

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-007 — Governance & Evidence Workspace |
| Phase | **UI-007-P01** |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-007-P01.md` |
| Design-plan review | `docs/build-orders/ITRGA_REVIEW_UI-007_DESIGN_PLAN.md` — Approved with Observations + R-1…R-8 |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 55 files / 246 tests |
| Intake status | Accepted by DA under ITRGA Build Order; implementation confined to P01 |
| Governance Gate | CLOSED |
| Production | NOT CERTIFIED |

---

## 1. Authority confirmation

ITRGA approved the UI-007 Engineering Design Plan with binding refinements R-1…R-8 and issued `BUILD_ORDER_UI-007-P01`.

Recorded governance files:

```text
docs/build-orders/ITRGA_REVIEW_UI-007_DESIGN_PLAN.md
docs/build-orders/BUILD_ORDER_UI-007-P01.md
```

---

## 2. Accepted implementation scope

DA accepts only the P01 frame/inventory/guardrail scope:

```text
single protected /governance route
Governance & Evidence workspace frame
Doc 12 §9 data-source inventory
G-1…G-7 read-only guardrail framing
Gate CLOSED / Production NOT CERTIFIED / Doc 11 HELD / TD-UI-POSTCSS-HIGH residual displayed as inert facts
```

P01 does not implement P02 governance-status details, P03 audit explorer, P04 evidence viewer, P05 health/readiness/version panels, or P06 completion.

---

## 3. Explicit non-authorizations

UI-007-P01 does not authorize:

- governance mutation;
- Gate open/close/toggle control;
- certification actuation;
- production approval;
- residual disposition action;
- audit event create/edit/delete/redact/replay;
- validation/readiness verdict mutation;
- backend/API endpoint, service, schema, table, or migration change;
- dependency change inside P01;
- saved-view persistence;
- recompute/inference/reclassification;
- external AI/LLM;
- order/broker/account/live/real-money path;
- production certification.

---

## 4. Mandatory named tests accepted

```text
test_ui007_governance_workspace_mounts_inside_single_ui001_shell
test_ui007_governance_workspace_uses_single_governance_route_and_registry_contract
test_ui007_governance_workspace_maps_every_section_to_existing_read_seams
test_ui007_governance_workspace_contains_no_governance_mutation_gate_or_certification_control
test_ui007_governance_workspace_preserves_gate_closed_not_certified_verbatim_and_doc16_branding
```

---

**DA does not self-approve. Gate remains CLOSED. Production remains NOT CERTIFIED.**
