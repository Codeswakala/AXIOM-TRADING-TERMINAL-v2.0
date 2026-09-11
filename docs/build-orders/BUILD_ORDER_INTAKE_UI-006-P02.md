# BUILD ORDER INTAKE — UI-006-P02

**Unified Artifact Catalog & Metadata Detail — Read-Only**

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-006 — Unified Research Artifact Explorer |
| Phase | **UI-006-P02** |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-006-P02.md` |
| Predecessor verdict | `docs/build-orders/ITRGA_REVIEW_UI-006-P01.md` — Approved with Observations |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 50 files / 221 tests |
| Intake status | Accepted by DA under ITRGA Build Order; implementation confined to P02 |
| Governance Gate | CLOSED |
| Production | NOT CERTIFIED |

---

## 1. Authority confirmation

ITRGA approved UI-006-P01 with observations and authorized UI-006-P02 as the next phase.

Recorded governance files:

```text
docs/build-orders/ITRGA_REVIEW_UI-006-P01.md
docs/build-orders/BUILD_ORDER_UI-006-P02.md
```

P02 is read-only and limited to unified artifact catalog and metadata detail.

---

## 2. Accepted implementation scope

DA will enhance only the existing route:

```text
/research-management
```

P02 remains strictly read-only:

- no collection/tag/membership create/update/delete controls;
- no persistence writes;
- no new route;
- no new backend/API/schema/migration/dependency;
- metadata detail renders stored fields verbatim.

---

## 3. Evidence obligations accepted

Mandatory named tests:

```text
test_ui006_catalog_lists_existing_artifacts_across_families_read_only
test_ui006_metadata_detail_renders_stored_fields_verbatim_without_recompute
test_ui006_catalog_preserves_no_cherry_picking_scope_sample_and_limitations
test_ui006_catalog_contains_no_mutation_actuation_or_gate_path
test_ui006_catalog_accessibility_and_doc16_brand_markers_hold
```

---

**DA does not self-approve. Gate remains CLOSED. Production remains NOT CERTIFIED.**
