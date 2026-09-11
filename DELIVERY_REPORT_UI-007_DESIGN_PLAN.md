# DELIVERY REPORT — UI-007 ENGINEERING DESIGN PLAN

## Governance & Evidence Workspace — ITRGA Submission Version

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-007 — Governance & Evidence Workspace |
| Deliverable | `docs/plans/UI-007_ENGINEERING_DESIGN_PLAN.md` |
| ITRGA request | `docs/build-orders/ITRGA_REQUEST_UI-007_DESIGN_PLAN.md` |
| Predecessor review | `docs/build-orders/ITRGA_REVIEW_UI-006-P06_FINAL_AND_UI-006_COMPLETION.md` |
| Baseline | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 55f/246t |
| DA status | Design plan submitted; not self-approved; no implementation started |
| Governance Gate | CLOSED |
| Production status | NOT CERTIFIED |

---

## 1. Build identity

This delivery report is for the UI-007 design-plan deliverable requested by ITRGA:

```text
UI-007 — Governance & Evidence Workspace
```

This is a planning deliverable only. It is not `BUILD_ORDER_UI-007-P01`, does not authorize implementation, and does not start UI-007 product work.

---

## 2. Review intake

Recorded:

```text
docs/build-orders/ITRGA_REVIEW_UI-006-P06_FINAL_AND_UI-006_COMPLETION.md
docs/build-orders/ITRGA_REQUEST_UI-007_DESIGN_PLAN.md
```

Key ITRGA facts recorded:

```text
UI-006-P06 APPROVED
UI-006 — UNIFIED RESEARCH ARTIFACT EXPLORER — COMPLETE
Baseline of record: v0.62.0 · head 20260717_0037 · backend 414 · frontend 55f/246t
UI-007 design plan requested first
BUILD_ORDER_UI-007-P01 not authorized until ITRGA accepts the design plan
Governance Gate CLOSED
Production NOT CERTIFIED
TD-UI-POSTCSS-HIGH Path-B re-accepted at UI-006 completion and is now a non-waivable pre-certification blocker
```

---

## 3. Design plan regenerated and submitted

Created/regenerated for ITRGA submission:

```text
docs/plans/UI-007_ENGINEERING_DESIGN_PLAN.md
```

The regenerated submission plan covers:

1. Doc 12 §9 objective/scope mapping;
2. existing read seam inventory;
3. confirmed audit-events read API over `audit_events`;
4. certification source honesty and Doc 11 separation;
5. dedicated read-only governance-boundary section G-1…G-7;
6. route/registry posture with `/governance` recommended but not implemented;
7. persistence/no-new-table posture;
8. verbatim/no-cherry-picking/no-recompute/self-surfacing rules;
9. TD-UI-POSTCSS-HIGH remediation scheduling recommendation;
10. phase decomposition UI-007-P01 through UI-007-P06;
11. evidence strategy;
12. no-drift policy;
13. Doc 16 brand/accessibility posture;
14. open questions for ITRGA;
15. DA recommendation for first Build Order;
16. constitutional attestation.

---

## 4. Design decisions submitted for ITRGA review

DA recommends:

```text
Add a single protected /governance route in UI-007-P01 if authorized
Use display name Governance & Evidence, not Control/Console wording
Keep all governance/audit/certification/evidence/health/version surfaces read-only
Render Gate CLOSED as an inert constitutional fact
Render Production NOT CERTIFIED / Doc 11 HELD as an inert governance fact
Render TD-UI-POSTCSS-HIGH as an open non-waivable pre-certification blocker
Use existing audit_events read API for audit explorer
Use existing health/readiness/metrics/system/route/API/plugin read APIs for platform posture
Use no new table/migration/backend endpoint/dependency by default
Keep filters in-memory by default
Schedule separate TD-UI-POSTCSS-HIGH dependency-remediation Build Order before UI-007 advances materially, preferably before P02
```

---

## 5. Read-only governance-boundary posture

The design plan treats governance-control contamination as the central UI-007 risk.

Permitted only as read-only display:

```text
governance status
Gate CLOSED status
audit events and reason-codes
certification posture
production NOT CERTIFIED / Doc 11 HELD
platform health/runtime readiness
evidence records
validation summaries
version/API/route/plugin posture
standing residuals
```

Explicitly prohibited:

```text
governance mutation
Gate open/close/toggle
certification actuation
production approval
risk acceptance/waiver control
audit event create/edit/delete/redact/replay
validation/readiness verdict mutation
recompute/reclassification
external AI/LLM summaries
order/broker/account/live/real-money path
dynamic plugin execution
```

Required named-test pattern every phase:

```text
...contains_no_governance_mutation_gate_or_certification_control
```

---

## 6. Route posture

DA recommends a new single protected route:

```text
/governance
```

This route is only a design recommendation. It is not implemented and is not authorized until ITRGA approves the design plan and issues `BUILD_ORDER_UI-007-P01`.

---

## 7. Data-source posture

The regenerated plan maps existing seams including:

```text
GET /api/v1/persistence/audit-events
GET /api/v1/health
GET /api/v1/ready
GET /api/v1/metrics
GET /api/v1/persistence/stats
GET /api/v1/system/info
GET /api/v1/institutional-platform/route-inventory
GET /api/v1/institutional-platform/rbac/permissions
GET /api/v1/institutional-platform/api-catalogue
GET /api/v1/institutional-platform/plugin-contracts
GET /api/v1/institutional-platform/operator-scope-records
existing research/intelligence/validation read APIs already surfaced by UI-004/UI-006
```

Audit seam explicitly confirmed:

```text
audit_events
details.reason_code
*_REFUSED values rendered verbatim
```

Certification is intentionally not an API control. The plan proposes read-only certification posture from Doc 11 and ITRGA governance records, not a backend certification endpoint.

---

## 8. TD-UI-POSTCSS-HIGH recommendation

The design plan does not propose dependency changes inside ordinary UI-007 phases.

DA recommendation:

```text
Schedule a dedicated TD-UI-POSTCSS-HIGH remediation Build Order before UI-007 implementation advances materially, preferably immediately after design-plan approval and before UI-007-P02 certification-status display, or at latest before UI-007 completion.
```

Until remediated or formally dispositioned at certification gate, UI-007 must display:

```text
TD-UI-POSTCSS-HIGH open
postcss <=8.5.17
GHSA-r28c-9q8g-f849
non-waivable pre-certification blocker
```

DA does not relabel the residual green and does not self-authorize dependency remediation.

---

## 9. Proposed phase plan

```text
UI-007-P01 — Governance Workspace Frame, Route, Data-Source Inventory, Read-Only Guardrails
UI-007-P02 — Governance Status, Gate CLOSED, Certification Status Display
UI-007-P03 — Read-Only Audit Explorer and Refusal Reason-Code Viewer
UI-007-P04 — Evidence Viewer and Validation Summary Panels
UI-007-P05 — Platform Health, System Readiness, Version and API Posture
UI-007-P06 — Completion Checkpoint
```

Each phase carries:

```text
no-governance-mutation/Gate/certification-control named test
whole-surface no-actuation grep
whole-surface no-recompute/no-external-AI grep
Doc 16 brand gate
no-drift proof
frontend/backend regression
Level-I operator evidence
```

---

## 10. Open questions submitted to ITRGA

The plan asks ITRGA to adjudicate:

1. whether `/governance` is approved for P01 route posture;
2. whether static/canonical governance-record certification display is sufficient or a future read-only endpoint is required;
3. the allowed depth of the evidence viewer;
4. how W7-U07 readiness dispositions should be surfaced;
5. when to schedule the dedicated TD-UI-POSTCSS-HIGH remediation Build Order;
6. whether raw psql audit-event evidence is required every audit-related phase or only P03/P06.

---

## 11. DA disposition

DA submits the regenerated UI-007 design plan for ITRGA review.

DA does not self-approve the plan.

No UI-007 implementation has started.

`BUILD_ORDER_UI-007-P01` remains unauthorized until ITRGA reviews the design plan and issues the first Build Order.

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.
