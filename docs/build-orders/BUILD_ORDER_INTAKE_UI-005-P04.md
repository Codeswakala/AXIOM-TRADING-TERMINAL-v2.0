# BUILD ORDER INTAKE — UI-005-P04

**Trade Planning & Journal Continuity — Mutation-Boundary Phase**

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-005 — Investigation & Planning Workspace |
| Phase | **UI-005-P04** |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-005-P04.md` |
| Predecessor verdict | `docs/build-orders/ITRGA_REVIEW_UI-005-P03.md` — Approved with Observations |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 46 files / 201 tests |
| Intake status | Accepted by DA under ITRGA Build Order; implementation confined to P04 |
| Governance Gate | CLOSED |
| Production | NOT CERTIFIED |

---

## 1. Authority confirmation

ITRGA approved UI-005-P03 with observations and authorized issuance of UI-005-P04 as the next phase.

Recorded governance files:

```text
docs/build-orders/ITRGA_REVIEW_UI-005-P03.md
docs/build-orders/BUILD_ORDER_UI-005-P04.md
```

The P04 Build Order is constitutionally sensitive because it touches existing W5 plan/journal mutation surfaces. DA accepts R-3 as the hard gate for this phase.

---

## 2. Accepted implementation scope

DA will enhance only existing UI surfaces:

```text
/trade-plans
/journal
```

Implementation remains presentation/integration over existing W5 stores and callbacks:

```text
fetchTradePlans / createTradePlan / updateTradePlan
fetchJournalEntries / createJournalEntry / updateJournalEntry
```

No new registered workspace route will be added. No `/investigation-planning` route will be added.

---

## 3. R-3 mutation-boundary acceptance

P04 may preserve the already-authorized W5 create/update callbacks, but DA must prove they remain confined to research-note/reflection fields.

Accepted boundaries:

- trade planning fields remain title, market context, hypothesis, linked signal/report ids, scenario notes, risk notes, invalidating conditions, and review status;
- journal fields remain title, reflection text, linked plan/signal/report ids, tags, and lesson notes;
- artifact links are route navigation and displayed artifact ids only;
- no new API endpoint, table, migration, dependency, registry route, or preference key;
- no plan-to-execution path or external venue import path;
- no external AI/LLM, browser-side analytics engine, inference, recompute, or reclassification.

The mandatory forbidden-field-rejection named test will be implemented as UI-side write-payload schema rejection over the existing W5 payload shapes, without backend/API/schema drift.

---

## 4. Evidence obligations accepted

DA will produce:

```text
frontend/src/workstation/investigation/PlanningJournalContinuity.test.tsx
DELIVERY_REPORT_UI-005-P04.md
docs/evidence/UI-005-P04_OPERATOR_EVIDENCE_COMMANDS.md
```

Mandatory named tests:

```text
test_ui005_trade_plans_use_existing_research_note_store_no_order_ticket
test_ui005_journal_uses_existing_reflection_store_no_broker_import
test_ui005_planning_preserves_research_only_fields_and_forbidden_field_rejection
test_ui005_plan_journal_links_are_artifact_ids_not_execution_paths
test_ui005_planning_journal_accessibility_and_brand_markers_hold
```

---

## 5. Non-authorizations

This intake does not authorize:

- UI-005-P05 Execution Research integration;
- UI-005-P06 completion;
- new backend/API/schema/migration/dependency work;
- new persistence key or table;
- new route or registry change;
- execution/order/broker/account/live-real path;
- Governance Gate opening;
- production deployment or certification.

---

**DA does not self-approve. Gate remains CLOSED. Production remains NOT CERTIFIED.**
