# BUILD ORDER INTAKE — UI-006-P01

**Explorer Frame · Existing Route Posture · Data-Source Inventory · Guardrails — Read-Only**

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-006 — Unified Research Artifact Explorer |
| Phase | **UI-006-P01** |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-006-P01.md` |
| Design-plan review | `docs/build-orders/ITRGA_REVIEW_UI-006_DESIGN_PLAN.md` — Approved with Observations + R-1…R-8 |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 49 files / 216 tests |
| Intake status | Accepted by DA under ITRGA Build Order; implementation confined to P01 |
| Governance Gate | CLOSED |
| Production | NOT CERTIFIED |

---

## 1. Authority confirmation

ITRGA approved the UI-006 Engineering Design Plan with binding refinements R-1…R-8 and authorized UI-006-P01 as the first Build Order.

Recorded governance files:

```text
docs/build-orders/ITRGA_REVIEW_UI-006_DESIGN_PLAN.md
docs/build-orders/BUILD_ORDER_UI-006-P01.md
```

P01 is read-only and limited to explorer frame, existing route posture, data-source inventory, and guardrails.

---

## 2. Accepted implementation scope

DA will enhance only the existing route:

```text
/research-management
```

P01 does not authorize:

```text
/artifacts
/artifact-explorer
```

No registry route change is authorized.

---

## 3. R-2/R-4 read-only acceptance

P01 is strictly read-only:

- no collection create/update/delete control;
- no tag create/update/delete control;
- no membership add/remove control;
- no persistence write;
- organization mutation deferred to later approved phases;
- existing W7 research-management stores are read only in this phase.

---

## 4. Evidence obligations accepted

Mandatory named tests:

```text
test_ui006_explorer_mounts_inside_single_ui001_shell
test_ui006_explorer_uses_existing_route_and_registry_only
test_ui006_explorer_maps_every_artifact_family_to_existing_sources
test_ui006_explorer_contains_no_mutation_actuation_or_gate_path
test_ui006_explorer_preserves_research_only_verbatim_and_doc16_branding
```

Mandatory evidence includes:

- no mutation-control proof;
- data-source inventory proof;
- no-actuation / no-recompute / no-external-AI grep;
- no route/registry/schema/dependency drift;
- frontend/backend regression;
- Doc 16 brand and browser served-session evidence;
- TD-UI-POSTCSS-HIGH disclosure without relabeling.

---

**DA does not self-approve. Gate remains CLOSED. Production remains NOT CERTIFIED.**
