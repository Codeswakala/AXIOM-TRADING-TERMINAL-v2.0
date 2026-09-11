# DELIVERY REPORT — UI-004 ENGINEERING DESIGN PLAN

## Research & Intelligence Workspace

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-004 — Research & Intelligence Workspace |
| Deliverable | `docs/plans/UI-004_ENGINEERING_DESIGN_PLAN.md` |
| ITRGA request | `docs/build-orders/ITRGA_REQUEST_UI-004_DESIGN_PLAN.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-003-P05_FINAL_AND_UI-003_COMPLETION.md` |
| Baseline | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 36 files / 151 tests |
| DA status | Design plan submitted; not self-approved; no implementation started |
| Governance Gate | CLOSED |
| Production status | Not certified |

---

## 1. Build identity

This delivery report is for the UI-004 design-plan deliverable requested by ITRGA:

```text
UI-004 — Research & Intelligence Workspace
```

This is a planning deliverable only. It is not `BUILD_ORDER_UI-004-P01`, does not authorize implementation, and does not declare UI-004 started.

---

## 2. Review intake

Recorded:

```text
docs/build-orders/ITRGA_REVIEW_UI-003-P05_FINAL_AND_UI-003_COMPLETION.md
docs/build-orders/ITRGA_REQUEST_UI-004_DESIGN_PLAN.md
```

Key ITRGA facts recorded:

```text
UI-003-P05 APPROVED
UI-003 — PROFESSIONAL MARKET WORKSPACE — COMPLETE
Baseline of record: v0.62.0 · head 20260717_0037 · backend 414 · frontend 36f/151t
UI-004 design plan requested first
BUILD_ORDER_UI-004-P01 not authorized until ITRGA accepts the design plan
```

---

## 3. Design plan delivered

Created:

```text
docs/plans/UI-004_ENGINEERING_DESIGN_PLAN.md
```

The plan covers ITRGA-requested content:

1. Doc 12 §6 objective/scope mapping;
2. reconciliation table across UI-001/UI-002/UI-003 and UI-009 status;
3. architecture and state ownership;
4. data-source table using existing governed APIs/stores;
5. validation/economic-usefulness/drilldown integrity;
6. advisory-signal read-only presentation;
7. persistence decision — reuse existing stores and `operator_workspace_preferences` if saved view state is needed;
8. Doc 16 brand plan B-1…B-7;
9. accessibility plan;
10. phase decomposition UI-004-P01 through UI-004-P06;
11. Level-I regression/evidence strategy;
12. constitutional + Doc 16 attestation;
13. open questions for ITRGA.

---

## 4. Bright-line posture

The plan preserves the highest-risk UI-004 boundaries:

- display existing governed intelligence only;
- no client-side inference;
- no authoritative recompute;
- no new analytical algorithm;
- no validation/economic-usefulness re-derivation;
- no signal generation;
- no no-cherry-picking violation;
- no external AI/LLM;
- no live/real data;
- no execution/order/broker/account path;
- Governance Gate CLOSED.

---

## 5. Persistence posture

Default persistence decision:

```text
No new table proposed.
```

Research artifacts already persist in existing W3/W4/W5/W6/W7 stores. If saved UI view state is authorized later, the plan proposes reuse of:

```text
operator_workspace_preferences
workspace_key = research-intelligence-workspace-v1
```

Allowed state is presentation-only ids/filters/section visibility. Report payload bodies, derived verdicts, action fields, secrets, and execution/account/broker fields are prohibited.

---

## 6. Recommended first Build Order

If ITRGA accepts the design plan, DA recommends:

```text
UI-004-P01 — Research Workspace Frame, Existing Data-Source Inventory, and No-Recompute Guardrail
```

Rationale:

- establishes frame and data-source inventory first;
- proves no-recompute/no-inference before report viewers and saved state;
- avoids persistence complexity in the first phase;
- provides early browser/brand/accessibility evidence.

---

## 7. Files added

```text
docs/build-orders/ITRGA_REVIEW_UI-003-P05_FINAL_AND_UI-003_COMPLETION.md
docs/build-orders/ITRGA_REQUEST_UI-004_DESIGN_PLAN.md
docs/plans/UI-004_ENGINEERING_DESIGN_PLAN.md
DELIVERY_REPORT_UI-004_DESIGN_PLAN.md
```

---

## 8. Files modified

```text
PROJECT_STATE.md
CHANGELOG.md
docs/governance/GOVERNANCE_AMENDMENTS.md
```

No frontend source, backend source, API schema, migration, or dependency was modified.

---

## 9. Validation posture

No implementation validation is claimed because this is a documentation/planning deliverable only.

The plan sets the validation baseline for future authorized UI-004 Build Orders:

```text
backend >= 414 passed
frontend >= 36 files / 151 tests passed
alembic current = 20260717_0037 unless migration explicitly authorized
no new dependency unless spike approved
Level-I browser evidence and Doc 16 brand proof every phase
```

---

## 10. DA disposition

DA submits the UI-004 Engineering Design Plan for ITRGA review.

DA does not self-approve the plan.

DA does not begin UI-004 implementation.

`BUILD_ORDER_UI-004-P01` remains unauthorized until ITRGA accepts this design plan and explicitly issues or authorizes the Build Order.

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

---

**End of DELIVERY_REPORT_UI-004_DESIGN_PLAN.md**
