# DELIVERY REPORT — UI-006 ENGINEERING DESIGN PLAN

## Unified Research Artifact Explorer

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-006 — Unified Research Artifact Explorer |
| Deliverable | `docs/plans/UI-006_ENGINEERING_DESIGN_PLAN.md` |
| ITRGA request | `docs/build-orders/ITRGA_REQUEST_UI-006_DESIGN_PLAN.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-005-P06_FINAL_AND_UI-005_COMPLETION.md` |
| Baseline | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 49f/216t |
| DA status | Design plan submitted; not self-approved; no implementation started |
| Governance Gate | CLOSED |
| Production status | Not certified |

---

## 1. Build identity

This delivery report is for the UI-006 design-plan deliverable requested by ITRGA:

```text
UI-006 — Unified Research Artifact Explorer
```

This is a planning deliverable only. It is not `BUILD_ORDER_UI-006-P01`, does not authorize implementation, and does not declare UI-006 started.

---

## 2. Review intake

Recorded:

```text
docs/build-orders/ITRGA_REVIEW_UI-005-P06_FINAL_AND_UI-005_COMPLETION.md
docs/build-orders/ITRGA_REQUEST_UI-006_DESIGN_PLAN.md
```

Key ITRGA facts recorded:

```text
UI-005-P06 APPROVED
UI-005 — INVESTIGATION & PLANNING WORKSPACE — COMPLETE
Baseline of record: v0.62.0 · head 20260717_0037 · backend 414 · frontend 49f/216t
UI-006 design plan requested first
BUILD_ORDER_UI-006-P01 not authorized until ITRGA accepts the design plan
Governance Gate CLOSED
Production NOT CERTIFIED
TD-UI-POSTCSS-HIGH remains OPEN as pre-certification residual
```

---

## 3. Design plan delivered

Created:

```text
docs/plans/UI-006_ENGINEERING_DESIGN_PLAN.md
```

The plan covers ITRGA-requested content:

1. Doc 12 §8 objective/scope mapping;
2. defining mutation-boundary section M-1…M-5;
3. route/registry posture;
4. persistence and schema posture;
5. exact proposed mutation model and first mutation phase;
6. existing read-surface mapping;
7. verbatim preservation and no-cherry-picking rules;
8. advanced filtering, UI-002-P04b, and UI-009 relationship;
9. architecture and state ownership;
10. phase decomposition UI-006-P01 through UI-006-P06;
11. evidence strategy;
12. TD-UI-POSTCSS-HIGH posture;
13. open questions for ITRGA;
14. DA recommendation for first Build Order;
15. constitutional and Doc 16 attestation.

---

## 4. Design decisions submitted for ITRGA review

DA recommends:

```text
Initial host route: /research-management
No new /artifacts route in P01
No new table by default
Reuse existing W7-U03 research-management collection/member/tag stores
Keep P01–P03 read-only
Introduce first organization-only mutation in P04
Split collections/memberships and tags into separate mutation phases
Select no dependency change in the design plan; TD-UI-POSTCSS-HIGH remains pre-cert residual
```

---

## 5. Mutation-boundary posture

The design plan treats mutation as the central UI-006 risk.

Permitted only if authorized in later Build Orders:

```text
collection creation
empty collection deletion if existing API/client support is confirmed
artifact-to-collection membership add/remove
tag creation
tag deletion if existing API/client support is confirmed
```

Explicitly prohibited:

```text
underlying artifact mutation
verdict/status/confidence/economic value mutation
source artifact body copying into collection/tag stores
order/account/broker/execution/live-real/Gate fields
external AI/LLM summaries
relationship scoring or analytical recommendations
new table by default
```

---

## 6. Recommended first Build Order

If ITRGA accepts the design plan, DA recommends:

```text
UI-006-P01 — Explorer Frame, Existing Route Posture, Data-Source Inventory, and Guardrails
```

Rationale:

- establishes the `/research-management` host and no-route-drift posture;
- maps all artifact families to existing sources;
- makes collection/tag mutation deferral explicit;
- proves no actuation, no recompute, no external AI, and no source mutation before any organization mutation;
- preserves review narrowness.

---

## 7. Files added

```text
docs/build-orders/ITRGA_REVIEW_UI-005-P06_FINAL_AND_UI-005_COMPLETION.md
docs/build-orders/ITRGA_REQUEST_UI-006_DESIGN_PLAN.md
docs/plans/UI-006_ENGINEERING_DESIGN_PLAN.md
DELIVERY_REPORT_UI-006_DESIGN_PLAN.md
```

---

## 8. Files modified

```text
PROJECT_STATE.md
CHANGELOG.md
docs/governance/GOVERNANCE_AMENDMENTS.md
```

No frontend source, backend source, API schema, Alembic migration, package manifest, dependency, route registry, or persistence store was modified by this design-plan deliverable.

---

## 9. Validation posture

No implementation validation is claimed because this is a documentation/planning deliverable only.

The plan sets the validation baseline for future authorized UI-006 Build Orders:

```text
backend >= 414 passed
frontend >= 49 files / 216 tests passed
alembic current = 20260717_0037 unless migration explicitly authorized
no new dependency unless separately authorized
Level-I browser evidence and Doc 16 brand proof every phase
mutation phases require raw PostgreSQL persistence capture
TD-UI-POSTCSS-HIGH remains open and must be remediated/accepted before Production Readiness Certification
```

---

## 10. DA disposition

DA submits the UI-006 Engineering Design Plan for ITRGA review.

DA does not self-approve the plan.

DA does not begin UI-006 implementation.

`BUILD_ORDER_UI-006-P01` remains unauthorized until ITRGA accepts this design plan and explicitly issues or authorizes the Build Order.

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

---

**End of DELIVERY_REPORT_UI-006_DESIGN_PLAN.md**
