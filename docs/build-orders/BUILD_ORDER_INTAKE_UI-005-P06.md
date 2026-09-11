# BUILD ORDER INTAKE — UI-005-P06

**UI-005 Completion Checkpoint**

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-005 — Investigation & Planning Workspace |
| Phase | **UI-005-P06 — Completion Checkpoint** |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-005-P06.md` |
| Predecessor verdict | `docs/build-orders/ITRGA_REVIEW_UI-005-P05.md` — Approved with Observations |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 48 files / 211 tests |
| Intake status | Accepted by DA under ITRGA Build Order; implementation confined to P06 completion evidence |
| Governance Gate | CLOSED |
| Production | NOT CERTIFIED |

---

## 1. Authority confirmation

ITRGA approved UI-005-P05 with observations and authorized UI-005-P06 as the final completion checkpoint for UI-005.

Recorded governance files:

```text
docs/build-orders/ITRGA_REVIEW_UI-005-P05.md
docs/build-orders/BUILD_ORDER_UI-005-P06.md
```

P06 is an integration evidence and constitutional validation phase. It does not authorize new product capability.

---

## 2. Accepted implementation scope

DA will add completion evidence only:

```text
frontend/src/workstation/investigation/InvestigationPlanningCompletion.test.tsx
DELIVERY_REPORT_UI-005-P06.md
docs/evidence/UI-005-P06_OPERATOR_EVIDENCE_COMMANDS.md
```

P06 will validate the continuous investigation-to-planning workflow across existing routes:

```text
/investigate
/compare-scenarios
/portfolio-research
/trade-plans
/journal
/execution-research
```

No new route will be added. No `/investigation-planning` route will be added.

---

## 3. TD-UI-POSTCSS-HIGH decision path

DA selects Build Order §5 path **(B) Accept as documented pre-certification residual** for this P06 delivery.

Rationale:

- UI-005-P06 does not authorize dependency remediation as a product/UI phase.
- No separately authorized dependency-remediation Build Order is attached.
- The advisory is disclosed, remains open, and must be remediated or formally accepted before Production Readiness Certification under Doc 11.

No dependency change will be performed in P06.

---

## 4. Evidence obligations accepted

Mandatory named tests:

```text
test_ui005_completion_investigation_to_planning_workflow_is_continuous_without_scope_expansion
test_ui005_completion_all_surfaces_are_existing_artifact_presentation_or_existing_research_notes
test_ui005_completion_no_execution_broker_account_live_data_ai_or_gate_path
test_ui005_completion_verbatim_values_no_cherry_picking_and_simulated_boundaries_hold
test_ui005_completion_accessibility_brand_and_ui001_ui002_integration_hold
```

Mandatory evidence includes:

- whole-surface no-actuation and no-recompute/no-external-AI greps;
- no-drift substitute;
- backend and frontend full regression with no test loss;
- Doc 16 brand self-check and browser proof;
- served browser workflow proof across all six UI-005 routes;
- explicit TD-UI-POSTCSS-HIGH path B disclosure.

---

## 5. Non-authorizations

This intake does not authorize:

- UI-006 design or implementation;
- dependency remediation unless separately authorized;
- new backend/API/schema/migration work;
- new persistence key or table;
- new route or registry change;
- execution/order/broker/account/live-real path;
- Governance Gate opening;
- production deployment or certification.

---

**DA does not self-approve. Gate remains CLOSED. Production remains NOT CERTIFIED.**
