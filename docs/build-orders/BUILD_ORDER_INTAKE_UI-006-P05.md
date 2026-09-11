# BUILD ORDER INTAKE — UI-006-P05

**Tags Organization Mutation — Second Mutation Phase**

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-006 — Unified Research Artifact Explorer |
| Phase | **UI-006-P05** |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-006-P05.md` |
| Predecessor verdict | `docs/build-orders/ITRGA_REVIEW_UI-006-P04_ATTEMPT3_APPROVED.md` — Approved; corrective closed |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 53 files / 236 tests |
| Intake status | Accepted by DA under ITRGA Build Order; implementation confined to P05 |
| Governance Gate | CLOSED |
| Production | NOT CERTIFIED |

---

## 1. Authority confirmation

ITRGA approved UI-006-P04 attempt-3 and authorized UI-006-P05 as the second organization-only mutation phase.

Recorded governance files:

```text
docs/build-orders/ITRGA_REVIEW_UI-006-P04_ATTEMPT3_APPROVED.md
docs/build-orders/BUILD_ORDER_UI-006-P05.md
```

---

## 2. Accepted implementation scope

DA will enhance only the existing route:

```text
/research-management
```

P05 mutation is limited to:

```text
tag create: tag + artifact_type + artifact_id only
```

Tag delete is not implemented in this phase. DA selects **create-only** for P05 because frontend tag-delete support is not introduced in this Build Order.

---

## 3. Evidence obligations accepted

Mandatory named tests:

```text
test_ui006_tags_mutate_existing_research_tag_store_only
test_ui006_tags_write_labels_and_artifact_references_not_source_payloads
test_ui006_tags_reject_order_account_execution_and_verdict_fields
test_ui006_tag_mutation_does_not_modify_underlying_artifact_values
test_ui006_tag_mutation_accessibility_brand_and_operator_scope_hold
```

R-7 raw PostgreSQL tag persistence capture is mandatory for operator evidence.

---

**DA does not self-approve. Gate remains CLOSED. Production remains NOT CERTIFIED.**
