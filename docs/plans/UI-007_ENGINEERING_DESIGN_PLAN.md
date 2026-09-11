# UI-007 Engineering Design Plan — Governance & Evidence Workspace

**Submission version for ITRGA review**

| Field | Value |
|---|---|
| Programme | AXIOM Institutional UI Transformation |
| Workstream | **UI-007 — Governance & Evidence Workspace** |
| Document type | Engineering Design Plan; pre-Build-Order; no implementation authorization |
| Development Authority | AXIOM DA |
| ITRGA request | `docs/build-orders/ITRGA_REQUEST_UI-007_DESIGN_PLAN.md` |
| Predecessor verdict | `docs/build-orders/ITRGA_REVIEW_UI-006-P06_FINAL_AND_UI-006_COMPLETION.md` |
| Predecessor milestone | 🏛️ UI-006 — Unified Research Artifact Explorer — COMPLETE |
| Platform baseline | v0.62.0 |
| Alembic head | `20260717_0037` |
| Validation baseline | backend 414 · frontend 55 files / 246 tests |
| Governance Gate | CLOSED |
| Production status | NOT CERTIFIED; Doc 11 Production Readiness Certification HELD |
| Governing documents | Doc 12 §9 → Doc 13 → completed UI-001…UI-006 foundations → Doc 16 → constitutional corpus Docs 00–11 |
| Security residual | `TD-UI-POSTCSS-HIGH` OPEN; Path-B re-accepted at UI-006 completion; now non-waivable pre-certification blocker |

---

## 0. Executive summary

UI-007 shall make AXIOM governance visible to institutional operators without turning governance into a UI-controlled action surface.

Document 12 §9 defines the workstream:

```text
Objective: Expose constitutional governance through professional operator interfaces.
Scope: Governance status · Audit explorer · Certification status · Platform health · Evidence viewer · Validation summaries · System readiness · Version information.
Expected outcome: Governance becomes visible without disrupting analytical workflows.
```

This plan is **not a Build Order**. It does not authorize implementation, route creation, backend/API work, dependency remediation, or UI-007-P01. It is submitted for ITRGA review. DA will not implement UI-007 until ITRGA approves or approves-with-observations this plan and issues the first controlled Build Order.

The defining rule for UI-007 is:

```text
UI-007 may DISPLAY governance state.
UI-007 may NOT CHANGE governance state.
```

Default design posture:

```text
Route posture: DA recommends one protected /governance workspace route, only if authorized by UI-007-P01.
Governance posture: read-only display; no governance mutation.
Gate posture: Gate CLOSED rendered as inert constitutional fact; no toggle/control.
Certification posture: Production NOT CERTIFIED / Doc 11 HELD rendered as inert governance fact; no certify/approve/waive control.
Audit posture: read-only explorer over existing audit_events read API; no audit mutation.
Evidence posture: verbatim disclosure; no evidence mutation; no AI summary.
Health/readiness posture: runtime health/readiness is separate from production certification.
Persistence posture: no new table; no migration; no saved state by default.
Dependency posture: no dependency change inside UI-007 phases by default.
TD-UI-POSTCSS-HIGH posture: display honestly as non-waivable pre-certification blocker; schedule a separate remediation Build Order.
```

---

## 1. Doc 12 §9 scope mapping

| Doc 12 §9 item | Existing source / read seam | UI-007 design interpretation | Hard boundary |
|---|---|---|---|
| Governance status | UI-001 shell posture; route inventory; API catalogue; plugin contracts; ITRGA verdicts | Read-only board showing Gate CLOSED, no actuation surface, no dynamic plugin execution, no external AI path, current UI completion state. | No governance mutation or control. |
| Audit explorer | `audit_events` via `GET /api/v1/persistence/audit-events` | Read-only event list/detail with verbatim fields and reason-codes. | No create/edit/delete/redact/replay. |
| Certification status | Doc 11; ITRGA verdicts; residual register/disclosed TDs | Read-only status: Production NOT CERTIFIED, Doc 11 HELD, TD-UI-POSTCSS-HIGH blocker. | No certify/mark-ready/approve-production/waive control. |
| Platform health | Health/readiness/metrics/stats APIs | Read-only runtime health, readiness checks, observability, DB stats. | No restart/reset/retry/ops action. |
| Evidence viewer | Build Orders, delivery reports, ITRGA reviews, operator evidence records | Curated governance evidence index and selected verbatim metadata/excerpts if authorized. | No upload/edit/delete/sign/approve; no generated summary. |
| Validation summaries | Existing validation/report read APIs used by UI-004/UI-006 | Stored verdict/status/method/sample/scope/uncertainty/limitations display. | No recompute/reclassification/stronger relabeling. |
| System readiness | `/ready`; W7-U07 dispositions; standing residuals | Runtime readiness and governance readiness displayed separately from production certification. | Runtime `ready` must not imply certified. |
| Version information | `/system/info`; health/readiness/metrics; API catalogue; Project State docs | Platform version, API/workspace versioning, baseline, Alembic head evidence. | No version bump/release/certification control. |

---

## 2. Existing read seams and source inventory

UI-007 shall reuse existing read APIs/stores by default.

Canonical backend routes are mounted under `/api/v1`; frontend wrappers may use `API_BASE` and path helpers. The design intent is reuse of the existing backend routes listed below.

| Surface | Existing backend route / source | Existing frontend seam status | Notes |
|---|---|---|---|
| Liveness | `GET /api/v1/health` | `fetchHealth()` exists | Public liveness; read-only. |
| Runtime readiness | `GET /api/v1/ready` | `fetchReadiness()` exists | Runtime readiness only; not certification. |
| System info | `GET /api/v1/system/info` | `fetchSystemInfo()` exists | Authenticated platform identity. |
| Observability metrics | `GET /api/v1/metrics` | frontend wrapper may be added when authorized | Read-only, backend-redacted. |
| Persistence stats | `GET /api/v1/persistence/stats` | frontend wrapper may be added when authorized | Read-only counts/stats. |
| Audit events | `GET /api/v1/persistence/audit-events` | frontend wrapper may be added when authorized | Existing read API over `audit_events`. |
| Route inventory | `GET /api/v1/institutional-platform/route-inventory` | wrapper may be added when authorized | Includes no-actuation / no-Gate capability posture. |
| RBAC vocabulary | `GET /api/v1/institutional-platform/rbac/permissions` | wrapper may be added when authorized | Read-only permission vocabulary. |
| API catalogue | `GET /api/v1/institutional-platform/api-catalogue` | wrapper may be added when authorized | Read-only route/API catalogue. |
| Plugin contracts | `GET /api/v1/institutional-platform/plugin-contracts` | wrapper may be added when authorized | Shows dynamic execution disabled. |
| Operator scope | `GET /api/v1/institutional-platform/operator-scope-records` | wrapper may be added when authorized | Current operator scope only. |
| Validation/report summaries | existing UI-004/UI-006 intelligence, validation, research, artifact read seams | wrappers already exist for many surfaces | Use stored values only. |

### 2.1 Audit-events read API confirmation

The existing audit read seam is confirmed:

```text
GET /api/v1/persistence/audit-events?category=<optional>&limit=<1..200>
response_model=list[AuditEventRead]
source table: audit_events
fields: id, category, action, actor, message, resource_type, resource_id, details, created_at
```

UI-007-P03 may add a frontend client wrapper to this existing endpoint if authorized. That is frontend integration over an existing read API, not a backend capability expansion.

Reason-code rule:

```text
details.reason_code and *_REFUSED values render verbatim as returned.
No reinterpretation.
No stronger/weaker relabeling.
No inference that refusal implies an authorization path.
```

### 2.2 Certification source honesty

There is intentionally no backend endpoint that certifies production. Production Readiness Certification is an ITRGA governance track under Doc 11.

UI-007 certification display shall therefore use canonical governance records, not a mutation/control API:

```text
Production: NOT CERTIFIED
Production Readiness Certification: HELD under Doc 11
TD-UI-POSTCSS-HIGH: non-waivable pre-certification blocker until remediated or formally accepted at certification gate
```

If ITRGA later requires a read-only certification-status backend endpoint, that must be separately authorized. This design plan does **not** propose one by default.

---

## 3. Defining governance boundary — G-1 through G-7

### G-1 — Read-only governance display

UI-007 shall display existing governance/audit/certification/validation/health/readiness/version records only.

Forbidden:

```text
create governance status
update governance status
delete governance status
approve governance status
waive residual
accept risk
certify production
mark production ready
open Gate
close Gate
toggle Gate
edit audit event
delete audit event
redact audit event
replay audit event
change validation verdict
change readiness verdict
```

Required named-test pattern every phase:

```text
...contains_no_governance_mutation_gate_or_certification_control
```

### G-2 — Gate CLOSED is inert

The Governance Gate shall be displayed as an inert fact:

```text
Gate CLOSED — read-only constitutional state
```

It must not be a:

```text
button
switch
checkbox
select
text input
form
command-palette action
menu action
API mutation
workflow step
```

Grep pattern every phase must include governance-specific markers:

```text
open_gate|allow_execution|gate.*toggle|toggle.*gate|certify|mark_ready|approve_production|waive|risk_accept
```

plus the standing M-4 no-actuation pattern.

### G-3 — Certification status is display, not actuation

UI-007 may display:

```text
Production NOT CERTIFIED
Doc 11 Certification HELD
Certification outcome options from Doc 11: CERTIFIED / CERTIFIED WITH CONDITIONS / DEFERRED / NOT CERTIFIED
Current status: NOT CERTIFIED
```

UI-007 must not implement certification workflow, production approval, waiver, residual acceptance, sign-off, or readiness mutation.

### G-4 — Audit explorer is read-only

Audit events shall be read from `audit_events` and displayed verbatim.

Permitted UI behavior:

```text
view list
view detail
in-memory filter by category/action/reason-code/resource
in-memory sort
copy visible identifier text if browser allows normal selection
```

Forbidden UI behavior:

```text
create audit event
edit audit event
delete audit event
redact audit event
replay audit event
mark reviewed
acknowledge as approval
persist filter as governance state
```

### G-5 — Evidence viewer is verbatim disclosure

Evidence records and validation summaries must be shown as stored or recorded.

Where present, display:

```text
artifact id / evidence id
artifact type / document type
status/verdict as stored
method/version
sample count
scope
uncertainty
limitations
source ids
lineage/audit references
report hash
created_at / review date
```

Forbidden:

```text
AI-generated summaries
recomputed validation verdicts
stronger labels than source records
hidden-scope aggregate claims
cherry-picked filtered results presented as complete truth
```

### G-6 — No actuation / no external AI / no recompute

UI-007 shall not introduce:

```text
buy
sell
place_order
execute
go-live
connect-broker
broker
account_id
order_ticket
position
balance
margin
capital
allocation
real_pnl
open_gate
allow_execution
```

UI-007 shall not introduce:

```text
openai
gpt
external_llm
llm_summary
ai_summary
inferSignal
runInference
authoritativeRecompute
emitSignal
generateSignal
generateScenario
inferRelationship
recompute
recalculat
deriveConfidence
reclassif
new .*Engine
/api/v1/orders
```

### G-7 — Read-only reuse; no backend capability expansion by default

Default posture:

```text
No new backend endpoint.
No new backend service.
No new table.
No migration.
No dependency.
No governance-state persistence.
No certification-state persistence.
No audit mutation.
```

Allowed in authorized UI-007 phases:

```text
frontend client wrappers over existing read APIs
frontend presentation components
one authorized workspace registry entry if ITRGA approves /governance
in-memory filters and sorts
```

---

## 4. Route / registry posture

### 4.1 DA recommendation

DA recommends one new protected workspace route, if authorized by `BUILD_ORDER_UI-007-P01`:

```text
/governance
```

Recommended display name:

```text
Governance & Evidence
```

Recommended navigation category:

```text
Govern
```

Rationale:

1. UI-007 is a distinct governance/evidence workstream, not a subpanel of research management.
2. The expected outcome is governance visibility without disrupting analytical workflows.
3. Existing workspaces are market/research/investigation/planning/artifact focused; none is a dedicated governance evidence workspace.
4. The Workspace Registry already supports a `Govern` category, so a single `/governance` route is non-duplicative.
5. A dedicated route improves operator discoverability while preserving UI-001/UI-002 shell and registry discipline.

### 4.2 Registry contract preservation

Any authorized route must preserve the Workspace Registry contract:

```text
id
displayName
navigationCategory
route
icon
rbac
defaultLayout
contextPanel
activityDock
search
keyboardShortcut
telemetryId
workspaceVersion
featureFlag
requiresAuth
noActuation
```

The route must be protected/authenticated and have `noActuation: true`.

### 4.3 Forbidden route/control naming

Forbidden route/display/control posture:

```text
/admin
/control
/gate
/production-control
/certification-control
/execution
Governance Control
Certification Console
Open Gate
Approve Production
```

If ITRGA rejects the `/governance` route recommendation, DA will revise P01 to enhance an existing surface instead. No route is implemented by this design plan.

---

## 5. Persistence posture

Default:

```text
No new table.
No migration.
No saved filters.
No governance-state persistence.
No certification-state persistence.
No audit mutation.
No dependency change.
```

UI filters should be in-memory only by default.

If ITRGA later authorizes saved presentation state, it must reuse:

```text
operator_workspace_preferences
```

Allowed saved presentation fields, if separately authorized:

```text
selected tab
visible panel ids
filter text/category
sort key/direction
collapsed sections
```

Forbidden saved fields:

```text
Gate status
governance status
certification status
production approval
risk acceptance
waiver
residual disposition
audit event edits
validation verdicts
readiness verdicts
```

Any saved-view phase must include raw PostgreSQL evidence:

```text
SELECT >= 1 row from operator_workspace_preferences
operator_id -> operators.id no-orphan proof
forbidden governance/certification/Gate fields absent
alembic current = 20260717_0037 (head)
```

This design plan does not propose saved-view persistence.

---

## 6. Verbatim, no-cherry-picking, and self-surfacing rules

UI-007 must avoid misrepresenting the constitution or the platform state.

| Displayed item | Required wording | Forbidden implication |
|---|---|---|
| Gate CLOSED | Read-only constitutional fact. | Operator can open or toggle the Gate. |
| Production NOT CERTIFIED | Doc 11 certification track is held/not certified. | Runtime readiness means production certified. |
| TD-UI-POSTCSS-HIGH | Open non-waivable pre-certification blocker until remediated or formally accepted at certification gate. | Audit is green or residual is silently waived. |
| Audit `*_REFUSED` | Refusal reason-code as stored. | Refusal is an approval path. |
| Validation summary | Stored verdict/status with method/scope/sample/limitations. | UI recomputed a stronger verdict. |
| Health `ready` | Runtime readiness probe only. | System is production certified. |
| API catalogue no Gate capability | Existing route inventory fact. | Hidden Gate control exists. |
| Plugin contracts | Dynamic/third-party execution disabled. | Plugin execution is available. |

No filtered view may be presented as a full-scope analytical claim unless it clearly states scope and count.

---

## 7. TD-UI-POSTCSS-HIGH plan

UI-006 completion adjudicated Path B but hardened the residual:

```text
TD-UI-POSTCSS-HIGH
postcss <=8.5.17
GHSA-r28c-9q8g-f849
Status: OPEN
Governance posture: non-waivable pre-certification blocker
```

UI-007 introduces no dependency by default. However, UI-007 includes certification-status display, so the residual must be shown honestly.

DA recommendation:

```text
Schedule a dedicated TD-UI-POSTCSS-HIGH dependency-remediation Build Order before UI-007 advances materially, preferably before UI-007-P02, or at latest before UI-007 completion.
```

Required remediation evidence for the separate Build Order:

```text
package.json/package-lock.json manifest diff
networked npm audit --audit-level=high exit 0
frontend full suite green with no test loss
TypeScript clean
production build successful
backend regression unaffected / green
no functional UI drift
ITRGA adjudication
```

DA does not propose to silently remediate dependencies inside ordinary UI-007 phases.

---

## 8. Proposed phase decomposition

### UI-007-P01 — Governance Workspace Frame, Route, Data-Source Inventory, Read-Only Guardrails

Objective:

```text
Establish the Governance & Evidence workspace frame and prove it is read-only.
```

Scope:

```text
single protected /governance route if authorized
UI-001/UI-002 shell integration
data-source inventory for Doc 12 §9 surfaces
G-1…G-7 guardrail panel
no backend/API/schema/dependency change
no governance/audit/certification mutation
```

Mandatory named tests:

```text
test_ui007_governance_workspace_mounts_inside_single_ui001_shell
test_ui007_governance_workspace_uses_single_registry_route_without_duplicate_navigation
test_ui007_governance_workspace_maps_sources_to_existing_read_seams
test_ui007_governance_workspace_contains_no_governance_mutation_gate_or_certification_control
test_ui007_governance_workspace_accessibility_doc16_brand_and_research_only_posture_hold
```

### UI-007-P02 — Governance Status, Gate CLOSED, Certification Status Display

Objective:

```text
Render Gate CLOSED, Production NOT CERTIFIED, Doc 11 HELD, and standing residuals as inert read-only facts.
```

Scope:

```text
Gate CLOSED display
Production NOT CERTIFIED display
Doc 11 certification track display
TD-UI-POSTCSS-HIGH pre-certification blocker display
standing residuals display
baseline/version status summary
no Gate/certification controls
```

Mandatory named tests:

```text
test_ui007_governance_status_renders_gate_closed_and_not_certified_as_inert_facts
test_ui007_certification_status_discloses_doc11_held_and_postcss_blocker_without_actuation
test_ui007_governance_status_preserves_itrga_verdicts_and_residuals_verbatim
test_ui007_governance_status_contains_no_governance_mutation_gate_or_certification_control
test_ui007_governance_status_accessibility_doc16_brand_hold
```

### UI-007-P03 — Read-Only Audit Explorer and Refusal Reason-Code Viewer

Objective:

```text
Expose audit_events and refusal reason-codes verbatim with in-memory filtering only.
```

Scope:

```text
frontend read wrapper for existing GET /api/v1/persistence/audit-events
audit event list/detail
category/action/reason-code/resource filters in memory
verbatim details.reason_code and *_REFUSED rendering
no audit mutation
```

Mandatory named tests:

```text
test_ui007_audit_explorer_reads_existing_audit_events_verbatim
test_ui007_audit_reason_codes_and_refusals_render_as_stored_without_reclassification
test_ui007_audit_filters_are_in_memory_only_and_no_cherry_picking
test_ui007_audit_explorer_contains_no_governance_mutation_gate_or_certification_control
test_ui007_audit_explorer_accessibility_doc16_brand_hold
```

Operator evidence must include read-only raw PostgreSQL comparison:

```sql
SELECT id, category, action, actor, details->>'reason_code', created_at
FROM audit_events
ORDER BY created_at DESC
LIMIT 20;
```

This is verbatim read proof, not mutation persistence capture.

### UI-007-P04 — Evidence Viewer and Validation Summary Panels

Objective:

```text
Display governance evidence and validation summaries without recompute, mutation, or reclassification.
```

Scope:

```text
curated evidence manifest for ITRGA verdicts, Build Orders, delivery reports, evidence packs
validation summary cards from existing report/validation read seams
scope/sample/limitations/method/version display
no generated summaries
no evidence mutation
```

Mandatory named tests:

```text
test_ui007_evidence_viewer_lists_existing_governance_evidence_without_edit_or_approval_controls
test_ui007_validation_summaries_render_stored_scope_sample_limitations_and_verdicts_verbatim
test_ui007_evidence_viewer_preserves_no_cherry_picking_and_no_recompute_boundaries
test_ui007_evidence_viewer_contains_no_governance_mutation_gate_or_certification_control
test_ui007_evidence_viewer_accessibility_doc16_brand_hold
```

### UI-007-P05 — Platform Health, System Readiness, Version and API Posture

Objective:

```text
Render platform health, readiness, metrics, persistence stats, route/API/plugin posture, and version information as read-only operations evidence.
```

Scope:

```text
/health display
/ready display
/api/v1/metrics display
/api/v1/persistence/stats display
/api/v1/system/info display
route inventory / RBAC / API catalogue / plugin contracts display
runtime readiness separated from production certification
```

Mandatory named tests:

```text
test_ui007_platform_health_version_and_readiness_render_existing_read_api_values
test_ui007_runtime_readiness_is_not_displayed_as_production_certification
test_ui007_api_route_plugin_posture_discloses_no_gate_dynamic_plugin_or_actuation_capability
test_ui007_platform_health_contains_no_governance_mutation_gate_or_certification_control
test_ui007_platform_health_accessibility_doc16_brand_hold
```

### UI-007-P06 — Completion Checkpoint

Objective:

```text
Prove UI-007 is complete: governance is visible without becoming governable from the UI.
```

Scope:

```text
completion evidence only
browser end-to-end workflow
whole-surface no-governance-mutation/Gate/certification-control proof
whole-surface no-actuation proof
whole-surface no-recompute/no-external-AI proof
Doc 16 validation
full regression
TD-UI-POSTCSS-HIGH display/remediation status adjudication
```

Mandatory named tests:

```text
test_ui007_completion_governance_audit_evidence_health_and_version_are_discoverable
test_ui007_completion_all_governance_surfaces_are_read_only_and_inert
test_ui007_completion_no_actuation_recompute_external_ai_gate_or_certification_control
test_ui007_completion_verbatim_no_cherry_picking_and_residual_disclosure_hold
test_ui007_completion_accessibility_doc16_brand_and_ui001_ui002_integration_hold
```

---

## 9. Evidence strategy

Every UI-007 phase requires Level-I operator evidence.

Standing evidence checklist:

```text
build identity verified first
named tests displayed passing by name
whole-surface no-governance-mutation/Gate/certification-control grep
whole-surface no-actuation grep
whole-surface no-recompute/no-external-AI grep
route/registry no-duplicate proof
no backend/API/schema/dependency drift unless explicitly authorized
alembic current = 20260717_0037 (head)
frontend full suite >= current baseline and no test loss
backend >=414 passed
Doc 16 browser proof
served browser screenshot(s)
logged-out block for /governance if route authorized
networked local CI or disclosed accepted exception
TD-UI-POSTCSS-HIGH status disclosed honestly
```

UI-007-P03 and UI-007-P06 require raw PostgreSQL read-only audit proof for reason-code/verbatim verification.

---

## 10. No-drift policy

Default no-drift posture:

```text
Alembic head remains 20260717_0037
No new backend route
No new backend service
No new table
No migration
No dependency
No package manifest change
No governance-state persistence
No certification-state persistence
No audit mutation
```

Planned exception, if authorized:

```text
UI-007-P01 may add one frontend Workspace Registry route /governance.
```

This exception is not implemented by this design plan and requires ITRGA Build Order authorization.

---

## 11. Doc 16 brand and accessibility posture

| Doc 16 check | UI-007 design rule |
|---|---|
| B-1 Logo / monogram | Reuse existing UI-001 shell identity; no new logo. |
| B-2 Palette | Use existing design tokens/classes; status text must not rely on color alone. |
| B-3 Typography | Monospace treatment for ids, versions, audit ids, hashes, reason-codes, Alembic head. |
| B-4 Iconography | Use existing icon conventions; no new icon set. |
| B-5 Institutional-not-retail | Governance/evidence/readiness wording only; no gamified/action-promotional copy. |
| B-6 Accessibility | Semantic headings, tables/lists, ARIA labels, keyboard navigation, visible text labels. |
| B-7 Documentation branding | AXIOM governance format in reports/evidence. |

Material Doc 16 violation remains a phase-blocking issue.

---

## 12. Open questions for ITRGA

1. **Route authorization:** Does ITRGA accept DA's recommendation for a single protected `/governance` route in `BUILD_ORDER_UI-007-P01`, or require an existing route to be enhanced instead?
2. **Certification source:** Does ITRGA accept read-only certification posture from canonical governance records/Doc 11, or require a separately authorized read-only certification-status backend endpoint?
3. **Evidence viewer depth:** Should P04 present only an evidence manifest/index, or may it render selected bundled markdown excerpts via frontend raw imports, with no backend file-listing API?
4. **Readiness dispositions:** Should W7-U07 readiness dispositions be displayed from static governance records, existing code constants, or only if a backend read route is separately authorized?
5. **TD-UI-POSTCSS-HIGH scheduling:** Should the dedicated remediation Build Order occur before UI-007-P01, between P01 and P02, or later with explicit blocker display in every phase?
6. **Audit raw evidence cadence:** Should raw PostgreSQL audit proof be mandatory only in P03/P06, or every phase after audit explorer introduction?

---

## 13. DA recommendation for first Build Order

If ITRGA approves or approves-with-observations this plan, DA recommends issuing:

```text
BUILD_ORDER_UI-007-P01 — Governance Workspace Frame, Route, Data-Source Inventory, Read-Only Guardrails
```

Recommended P01 scope:

```text
single protected /governance route under existing Workspace Registry contract
workspace frame on UI-001/UI-002 shell
data-source inventory for Doc 12 §9 surfaces
read-only G-1…G-7 guardrails
no governance mutation
no Gate control
no certification control
no audit mutation
no backend/API/schema/dependency change
```

DA separately recommends scheduling a dedicated TD-UI-POSTCSS-HIGH remediation Build Order before UI-007-P02.

---

## 14. Constitutional attestation

DA attests this design plan proposes no implementation and preserves:

```text
Governance Gate CLOSED
Production NOT CERTIFIED
No governance mutation
No Gate control
No certification actuation
No audit mutation
No validation/readiness verdict mutation
No backend/API/schema/dependency change by default
No new table/migration
No execution/order/broker/account/live/real-money path
No external AI/LLM
No dynamic plugin execution
No recompute/inference/reclassification
Doc 16 brand gate
UI-001/UI-002 shell and navigation discipline
```

DA does not self-approve this plan. UI-007 implementation shall not begin until ITRGA reviews the plan and issues the first Build Order.
