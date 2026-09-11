# BUILD ORDER INTAKE — UI-006-P03

**Lineage, Relationships & Advanced Filtering — Read-Only**

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-006 — Unified Research Artifact Explorer |
| Phase | **UI-006-P03** |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-006-P03.md` |
| Predecessor verdict | `docs/build-orders/ITRGA_REVIEW_UI-006-P02.md` — Approved with Observations |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 51 files / 226 tests |
| Intake status | Accepted by DA under ITRGA Build Order; implementation confined to P03 |
| Governance Gate | CLOSED |
| Production | NOT CERTIFIED |

---

## 1. Authority confirmation

ITRGA approved UI-006-P02 with observations and authorized UI-006-P03 as the next phase.

Recorded governance files:

```text
docs/build-orders/ITRGA_REVIEW_UI-006-P02.md
docs/build-orders/BUILD_ORDER_UI-006-P03.md
```

P03 is the final read-only phase before the planned P04/P05 mutation phases.

---

## 2. Accepted implementation scope

DA will enhance only the existing route:

```text
/research-management
```

P03 remains strictly read-only:

- lineage and relationships are stored references only;
- filtering is temporary in-memory presentation state only;
- no saved-filter persistence;
- no collection/tag/membership create/update/delete controls;
- no persistence writes;
- no new route;
- no new backend/API/schema/migration/dependency.

---

## 3. Evidence obligations accepted

Mandatory named tests:

```text
test_ui006_lineage_and_relationships_render_stored_links_read_only_no_inference
test_ui006_advanced_filtering_is_in_memory_only_no_persistence
test_ui006_filtered_views_preserve_no_cherry_picking_scope_and_limitations
test_ui006_lineage_relationships_filtering_contain_no_mutation_actuation_or_gate_path
test_ui006_lineage_relationships_filtering_accessibility_and_doc16_brand_hold
```

---

**DA does not self-approve. Gate remains CLOSED. Production remains NOT CERTIFIED.**
