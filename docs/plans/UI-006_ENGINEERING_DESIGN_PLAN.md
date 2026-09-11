# UI-006 Engineering Design Plan — Unified Research Artifact Explorer

| Field | Value |
|---|---|
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-006 — Unified Research Artifact Explorer |
| Document type | Engineering Design Plan; pre-Build-Order; no implementation authorization |
| Development Authority | AXIOM DA |
| ITRGA request | `docs/build-orders/ITRGA_REQUEST_UI-006_DESIGN_PLAN.md` |
| Predecessor milestones | UI-001 COMPLETE · UI-002 COMPLETE · UI-003 COMPLETE · UI-004 COMPLETE · UI-005 COMPLETE |
| Platform baseline | v0.62.0 |
| Alembic head | `20260717_0037` |
| Baseline validation | backend 414 passed · frontend 49 files / 216 tests |
| Governance Gate | CLOSED |
| Production status | Not certified; governed separately by `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md` |
| Governing UI docs | `12_INSTITUTIONAL_UI_TRANSFORMATION_PLAN.md` §8 → `13_UI_TRANSFORMATION_MASTER_PLAN.md` → completed UI-001…UI-005 foundations → `16_BRAND_GOVERNANCE_STANDARD.md` |
| Security residual | `TD-UI-POSTCSS-HIGH` OPEN; accepted as pre-certification residual at UI-005 completion; dependency-touching phase must address it |

---

## 0. Executive summary

UI-006 shall provide centralized discovery, organization, traceability, and relationship navigation for existing institutional research artifacts.

Per Document 12 §8:

```text
Objective: Provide centralized access to institutional research artifacts.
Scope: Unified artifact explorer · Collections · Tags · Linked artifacts · Lineage · Metadata · Cross-artifact relationships · Advanced filtering.
Expected outcome: Every research artifact becomes discoverable, interconnected, and traceable.
```

This design plan is **not an implementation Build Order**. It proposes a controlled, evidence-driven UI-006 phase plan for ITRGA review. DA does not implement UI-006 until ITRGA approves or approves-with-observations this plan and issues `BUILD_ORDER_UI-006-P01`.

UI-006 differs from UI-004/UI-005 because it is the first UI workstream allowed to consider **research-artifact organization mutation**. The central risk is not market execution; it is accidentally turning organization actions into underlying artifact mutation, verdict mutation, analytical authorship, or hidden scope alteration. Therefore this plan treats collection/tag/membership mutation as a distinct, high-evidence phase and keeps early phases read-only.

Default design decisions:

```text
Route posture: enhance existing /research-management first; no new route in P01.
Schema posture: reuse existing W7-U03 research-management store/APIs; no new table by default.
Mutation posture: organization-only, split into narrowly reviewed phases.
Analytical posture: no recompute, no inference, no external AI/LLM, no client-side analytics engine.
Production posture: not certified; TD-UI-POSTCSS-HIGH remains pre-cert residual.
```

---

## 1. Doc 12 §8 scope mapping

| Doc 12 §8 item | Existing source / surface | UI-006 design interpretation | Explicit boundary |
|---|---|---|---|
| Unified artifact explorer | Existing W3/W4/W5/W6/W7 artifact read APIs and frontend seams | Central operator workspace for discovering research artifacts across signal, report, scenario, plan, journal, execution, portfolio, chart, collection, and tag sources. | Presentation/discovery only; no new artifact generation. |
| Collections | Existing W7-U03 `research_collections` store/API | Organization containers for artifact references. | Collection mutation is organization-only; no source artifact mutation. |
| Tags | Existing W7-U03 `research_tags` store/API | Operator-authored labels attached to artifact references. | Tag mutation changes labels/references only; no verdict/confidence/status mutation. |
| Linked artifacts | Existing source ids and existing collection members/tags | Link graph generated from stored ids and existing relationships. | No hidden materialization of source payloads into relationship stores. |
| Lineage | Existing artifact lineage fields, source ids, input lineage, hashes | Display traceability and provenance from stored artifact fields. | Verbatim display only; no lineage inference beyond explicit stored ids. |
| Metadata | Existing artifact fields | Display type, id, method/version, status, sample count, scope, timestamps, hash, operator attribution where stored. | No confidence/verdict recalculation. |
| Cross-artifact relationships | Existing source ids, linked report ids, plan/journal links, collection members, tags | Relationship panels and filters derived from explicit references. | No new analytical relationship score, ranking, or recommendation engine. |
| Advanced filtering | In-memory presentation filtering over fetched metadata | Type/status/date/source/tag/collection/route filtering for discovery. | Filtering never changes stored artifacts and never claims analytical truth. |

---

## 2. Defining mutation boundary — M-1 through M-5

### M-1 — Mutation scope is organization-only

UI-006 mutation, when authorized, is limited to research-artifact organization:

```text
collection name / description creation
empty collection deletion if supported by existing API
artifact-to-collection membership add/remove
tag label creation for an artifact reference
tag deletion if supported by existing API
```

UI-006 shall not mutate underlying artifacts such as:

```text
advisory_signals
correlation_reports
regime_reports
scenario_reports
portfolio_risk_reports
signal_validation_reports
assistant_research_responses
chart_research_annotations
trade_plan_notes
manual_trade_journal_entries
simulated_execution_runs
simulated_fill_events
simulated_paper_ledger_entries
execution_risk_research_reports
execution_research_experiments
simulated_execution_analytics_reports
operator_workspace_preferences
```

except existing stores may be read, and existing research-management collection/tag tables may be written only in the dedicated mutation phases.

### M-2 — No new analytical truth / no verdict mutation

Collection/tag/membership actions must never change:

```text
research_status
signal_state
state_reason
calibrated_confidence
calibration_status
economic_verdict
economic_usefulness
validation status
sample count
uncertainty
limitations
report_hash
lineage
scenario results
SIMULATED mode
```

No UI-006 control may relabel a stored artifact as approved, tradable, live, real, reliable, economically useful, or production-ready.

### M-3 — Existing authorized store + persistence discipline

Default persistence posture:

```text
Reuse existing W7-U03 research-management stores and APIs.
No new table.
No migration.
No new dependency.
```

Existing persistence surfaces expected:

```text
research_collections
research_collection_members
research_tags
```

If a mutation phase writes to these stores, Level-I evidence must include inline raw PostgreSQL capture:

```text
save action in served/app evidence
SELECT >= 1 row from the correct W7 table
operator_id -> operators.id join / no orphan
forbidden-field-present = false
alembic current = 20260717_0037 (head)
```

API read-back or in-process test read-back never substitutes for raw `psql` evidence. `(0 rows)` is disproof.

If ITRGA later decides a new relationship table is necessary, that is a separately justified heightened-evidence sub-decision and changes the no-drift posture. This plan does **not** propose a new table.

### M-4 — No actuation, ever

UI-006 shall not introduce or expose:

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

Artifact organization has no order, broker, account, live, real-money, or Governance Gate meaning.

### M-5 — No external AI/LLM, no analytics engine, no recompute/inference

UI-006 shall not add:

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
recompute
recalculat
deriveConfidence
reclassif
new .*Engine
/api/v1/orders
```

Relationship mapping and filtering are first-party deterministic presentation over stored ids and metadata only.

---

## 3. Route / registry posture

### 3.1 Recommended route posture

DA recommends enhancing the existing protected route:

```text
/research-management
```

as the initial UI-006 host.

Rationale:

- It already exists in the UI-001 registry and UI-002 navigation.
- It already maps to W7-U03 research-management collections/tags.
- It avoids route/registry drift in the first UI-006 phase.
- It keeps collection/tag mutation discipline anchored to the existing store.
- It can evolve from “Research Management” into the unified artifact explorer without adding a duplicate navigation entry.

### 3.2 Deferred optional route alias

A new `/artifacts` or `/artifact-explorer` route is **not** proposed for P01. If ITRGA later wants a dedicated route or alias for operator clarity, it should be explicitly authorized in a separate phase with proof that:

- the Workspace Registry contract remains intact;
- no duplicate navigation is introduced;
- route auth/no-actuation flags are preserved;
- UI-002 navigation and breadcrumbs remain coherent;
- no `/investigation-planning` or other unauthorized route is introduced.

---

## 4. Persistence and schema posture

### 4.1 Default no-new-table posture

UI-006 shall reuse existing W7-U03 stores:

| Store | Existing purpose | UI-006 role |
|---|---|---|
| `research_collections` | Operator-scoped collection metadata | Create/list/delete empty collections if existing API supports the operation. |
| `research_collection_members` | Artifact membership references | Add/remove artifact references to/from collections. |
| `research_tags` | Operator-scoped artifact tags | Create/delete artifact labels. |

No new Alembic migration is proposed.

### 4.2 Forbidden persisted fields

Research-management persistence must not contain or accept:

```text
order
order_payload
order_intent
side
quantity
lot_size
order_size
position_size
entry_price_order
stop_loss
take_profit
broker
broker_account_id
account_id
position_id
execution_status
live_position
balance
margin
capital
allocation
real_pnl
pnl
fill
real_fill
live_fill
open_gate
allow_execution
api_key
secret
password
jwt
access_token
refresh_token
```

### 4.3 No copied artifact bodies

Collections/tags/memberships may store artifact type/id references and label metadata. They must not copy source artifact bodies, verdicts, report payloads, journal text, trade plan text, or execution research payloads into organization tables.

---

## 5. Mutation model

### 5.1 Proposed organization mutations

UI-006 should introduce mutation only in dedicated phases after read-only explorer evidence is accepted.

| Mutation | Existing backend support posture | Proposed phase | Evidence requirement |
|---|---|---|---|
| Create collection | Existing W7-U03 create collection endpoint/repository | P04 | Raw psql collection row, operator join, forbidden-field proof. |
| Delete empty collection | Existing backend route supports empty collection delete | P04 or P06 corrective only if UI included | Raw psql before/after if implemented. |
| Add collection member | Existing W7-U03 member endpoint/repository | P04 | Raw psql member row, artifact_type/artifact_id only, no copied source body. |
| Remove collection member | Existing backend route supports remove member | P04 or P06 corrective only if UI included | Raw psql before/after if implemented. |
| Create tag | Existing W7-U03 create tag endpoint/repository | P05 | Raw psql tag row, tag label + artifact reference only. |
| Delete tag | Existing backend route supports delete tag | P05 or P06 corrective only if UI included | Raw psql before/after if implemented. |
| Rename/update collection | Not assumed available in current frontend client | Not proposed by default | Would require explicit ITRGA authorization if backend change needed. |
| Edit tag label | Not proposed by default | Not proposed | Use delete + create only if existing API supports and ITRGA authorizes. |

### 5.2 First mutation phase

DA recommends the first mutation phase be:

```text
UI-006-P04 — Collections & Memberships Organization Mutation
```

P01–P03 should remain read-only to establish route, source inventory, artifact catalog, lineage, and filtering before mutation is introduced.

---

## 6. Read-surface design

UI-006 shall compose a unified artifact index from existing read seams.

| Artifact family | Existing read seam | Fields displayed verbatim |
|---|---|---|
| Advisory signals | `fetchAdvisorySignals`, `fetchAdvisorySignal` | signal id, state, state reason, calibrated confidence, operating domain, calibration status, economic verdict, lineage ids, freshness. |
| Institutional intelligence reports | `fetchInstitutionalIntelligenceBundle` | report id/type, method version, sample count, uncertainty, limitations, source ids, hashes, economic/validation fields. |
| Scenario reports | `fetchScenarioReports`, `fetchScenarioReport` | scenario name, assumptions, hypothetical result, uncertainty, limitations, source ids, report hash. |
| Portfolio research | `fetchPortfolioResearchDashboard`, `fetchAdvancedResearchReport` | included scope, source ids, limitations, economic usefulness, report hash, preview metadata. |
| Trade plans | `fetchTradePlans` | plan id, title, linked signal/report ids, research status, decision status. |
| Research journal | `fetchJournalEntries` | journal id, linked plan/signal/report ids, tags, research status. |
| Execution research | `fetchExecutionResearchBundle` | SIMULATED runs/fills/ledger/risk/experiments/analytics ids, uncertainty, limitations, source ids, hashes. |
| Chart research annotations | existing chart annotation read seam | annotation id/type, chart context, source ids, uncertainty, research status. |
| Collections/tags | `fetchResearchManagementBundle`, `fetchResearchCollections`, `fetchResearchTags` | collection id/name/description, members, tag labels, artifact refs, research status. |

No new analytical authorship is introduced. UI-006 creates a presentation index, not an analytical artifact.

---

## 7. Verbatim preservation and no-cherry-picking

UI-006 must preserve the following display rules:

- artifact values are rendered from stored response fields only;
- verdicts and statuses are never upgraded or softened;
- absence is labeled honestly (`not supplied`, `not_assessed`, `not_available`, `—`) rather than inferred;
- every artifact detail panel includes source id / lineage / scope / uncertainty / limitations where available;
- filters do not claim full scope unless the displayed artifact itself declares full scope;
- count summaries must be labeled as UI presentation counts, not analytical conclusions;
- relationship panels must identify the source of the relationship (`source_artifact_ids`, `linked_report_ids`, collection member, tag, journal link, plan link, execution source id).

---

## 8. Advanced filtering and UI-002-P04b relationship

### 8.1 Filtering posture

UI-006 advanced filtering is presentation-only and in-memory by default:

```text
artifact type
research status
source id presence
method/version
collection membership
tag label
linked signal/report/plan id
SIMULATED mode
sample count presence
limitation presence
```

Filtering must not persist query text or source payloads unless a future Build Order explicitly authorizes saved presentation preferences.

### 8.2 UI-002-P04b search adapters

UI-002-P04b remains an independent residual. UI-006 may later provide artifact explorer source adapters for global search only under a separate authorized phase. The UI-006 plan does not close UI-002-P04b by default.

### 8.3 UI-009 design-system dependency

UI-006 should use existing institutional cards, panels, badges, `.mono` identifiers, and tokenized styles. Any new reusable explorer/filter/relationship components should be marked as candidates for later UI-009 design-system harvest, but UI-006 must not wait on UI-009 to deliver governed functionality.

---

## 9. Architecture

```text
InstitutionalWorkspaceShell (UI-001)
└── Existing /research-management route (UI-001 registry, UI-002 navigation)
    ├── UI-006 Explorer Frame
    │   ├── Artifact family tabs / filters
    │   ├── Unified artifact metadata list
    │   ├── Selected artifact detail panel
    │   ├── Lineage / source-id panel
    │   ├── Relationship panel
    │   └── Organization panel (collections/tags; mutation only in later authorized phases)
    ├── Existing W7-U03 research-management read/write APIs
    └── Existing UI-004/UI-005 read seams for artifact metadata
```

State ownership:

| State | Owner | Persistence |
|---|---|---|
| Active explorer filters | UI presentation state | In-memory by default. |
| Selected artifact id/type | UI presentation state | In-memory by default. |
| Collections | Existing W7 store | Existing DB table, mutation only in dedicated phase. |
| Collection memberships | Existing W7 store | Existing DB table, mutation only in dedicated phase. |
| Tags | Existing W7 store | Existing DB table, mutation only in dedicated phase. |
| Artifact truth values | Existing source artifact stores | Read-only; never copied/mutated. |
| Saved presentation view | Not proposed by default | Future `operator_workspace_preferences` only if explicitly authorized. |

---

## 10. Phase decomposition

### UI-006-P01 — Explorer Frame, Route Posture, Data-Source Inventory, Guardrails

Objective: establish the explorer frame on existing `/research-management`, map artifact families to existing sources, and prove no actuation/recompute/mutation.

Scope:

- enhance existing `/research-management` route;
- add UI-006 explorer frame and source inventory;
- display read-only posture and mutation deferral;
- no collection/tag mutation yet;
- no backend/schema/dependency/route change.

Acceptance anchors:

```text
test_ui006_explorer_mounts_inside_single_ui001_shell_existing_route
test_ui006_explorer_registry_route_posture_adds_no_unapproved_route
test_ui006_explorer_maps_artifact_families_to_existing_sources
test_ui006_explorer_contains_no_actuation_recompute_external_ai_or_mutation
test_ui006_explorer_accessibility_and_doc16_brand_markers_hold
```

### UI-006-P02 — Unified Artifact Catalog & Metadata Detail (Read-Only)

Objective: display a unified metadata catalog across existing artifact families.

Scope:

- artifact family filters/tabs;
- artifact metadata list;
- selected detail panel with status/verdict/uncertainty/limitations/source ids/hashes;
- honest absence labels;
- no mutation.

Acceptance anchors:

```text
test_ui006_catalog_renders_existing_artifact_metadata_read_only
test_ui006_catalog_preserves_verdicts_statuses_confidence_and_economic_values_verbatim
test_ui006_catalog_shows_scope_uncertainty_limitations_source_ids_and_hashes
test_ui006_catalog_contains_no_artifact_generation_or_source_mutation
test_ui006_catalog_accessibility_and_brand_markers_hold
```

### UI-006-P03 — Lineage, Relationships & Advanced Filtering (Read-Only)

Objective: expose traceability and relationships from stored references and provide advanced filtering.

Scope:

- relationship graph/list from explicit ids only;
- lineage/source-id panels;
- filtering by type/status/tags/collections/source ids/linked ids;
- no relationship scoring or AI summary;
- no saved query persistence.

Acceptance anchors:

```text
test_ui006_relationships_use_explicit_stored_references_only
test_ui006_lineage_preserves_source_ids_hashes_and_method_versions
test_ui006_filters_are_presentation_only_and_do_not_claim_analytical_truth
test_ui006_relationships_contain_no_recompute_inference_or_external_ai
test_ui006_relationship_filter_accessibility_and_brand_markers_hold
```

### UI-006-P04 — Collections & Memberships Organization Mutation

Objective: introduce first organization-only mutation slice using existing W7 collection/member store.

Scope:

- collection create;
- optional empty collection delete only if existing API/client support is confirmed;
- member add/remove;
- artifact references only;
- no source artifact mutation;
- mandatory raw PostgreSQL persistence capture.

Acceptance anchors:

```text
test_ui006_collections_mutate_existing_research_management_store_only
test_ui006_collection_membership_writes_artifact_references_not_source_payloads
test_ui006_collections_reject_order_account_execution_and_verdict_fields
test_ui006_collection_mutation_does_not_modify_underlying_artifact_values
test_ui006_collection_mutation_accessibility_brand_and_operator_scope_hold
```

### UI-006-P05 — Tags Organization Mutation

Objective: introduce tag create/delete over existing W7 tag store.

Scope:

- create tag labels attached to artifact references;
- delete tag if existing API/client support is confirmed;
- no tag-driven artifact mutation;
- mandatory raw PostgreSQL persistence capture.

Acceptance anchors:

```text
test_ui006_tags_mutate_existing_research_tag_store_only
test_ui006_tags_write_labels_and_artifact_references_not_source_payloads
test_ui006_tags_reject_order_account_execution_and_verdict_fields
test_ui006_tag_mutation_does_not_modify_underlying_artifact_values
test_ui006_tag_mutation_accessibility_brand_and_operator_scope_hold
```

### UI-006-P06 — Completion Checkpoint

Objective: final integration evidence and ITRGA completion review.

Acceptance anchors:

```text
test_ui006_completion_artifact_explorer_discovery_organization_and_traceability_hold
test_ui006_completion_mutations_are_organization_only_and_existing_store_bound
test_ui006_completion_no_actuation_recompute_external_ai_schema_or_route_drift
test_ui006_completion_verbatim_no_cherry_picking_and_relationship_boundaries_hold
test_ui006_completion_accessibility_doc16_brand_and_ui001_ui002_integration_hold
```

---

## 11. Evidence strategy

Every UI-006 phase shall provide:

- build identity first;
- named tests displayed passing with verbose reporter;
- no-actuation grep;
- no-recompute/no-inference/no-external-AI grep;
- no new endpoint/schema/dependency proof unless explicitly authorized;
- registry/route proof;
- Alembic current = `20260717_0037` unless a separately justified migration is approved;
- frontend regression at/above baseline 49f/216t, no test loss;
- backend regression at/above 414;
- TypeScript/build/audit evidence;
- browser served-session evidence;
- Doc 16 brand proof;
- networked CI with sentinel or disclosed accepted residual condition.

Mutation phases additionally require:

- organization-only source proof;
- no-underlying-artifact-mutation named test;
- raw PostgreSQL persistence capture on the correct table;
- operator_id lineage/no-orphan proof;
- forbidden-field proof;
- source artifact values unchanged proof where practical.

---

## 12. TD-UI-POSTCSS-HIGH posture

`TD-UI-POSTCSS-HIGH` remains open after UI-005 completion:

```text
postcss <=8.5.17
GHSA-r28c-9q8g-f849
```

This design plan does not remediate dependencies. UI-006 phases that do not touch dependencies may proceed under the accepted pre-certification residual posture if ITRGA agrees. Any UI-006 phase that touches dependencies must address the advisory and provide dependency-remediation evidence.

Production Readiness Certification remains blocked until the residual is remediated or formally accepted under Doc 11.

---

## 13. Open questions for ITRGA

1. Does ITRGA accept enhancing existing `/research-management` as the initial UI-006 Artifact Explorer host, with no new route in P01?
2. Should `/artifacts` or `/artifact-explorer` be considered later as an alias/dedicated route, or should UI-006 remain anchored to `/research-management` throughout?
3. Does ITRGA accept the default no-new-table posture and reuse of existing W7-U03 collection/tag/member stores?
4. Does ITRGA accept splitting organization mutation into separate P04 collections/memberships and P05 tags phases for narrower review?
5. Should collection deletion and tag deletion be included if existing API/client support is present, or should UI-006 initially implement create/add-only organization controls?
6. Should advanced filtering remain in-memory only for UI-006, with saved filters deferred to a later workstream or explicit Build Order?
7. Should UI-002-P04b global search adapters remain independent, or should a later UI-006 phase propose read-only artifact explorer search adapters?
8. Should a dependency-remediation Build Order for TD-UI-POSTCSS-HIGH be scheduled before UI-006 mutation phases, before UI-006 completion, or only before Production Readiness Certification?

---

## 14. DA recommendation for first Build Order

If ITRGA accepts this plan, DA recommends:

```text
UI-006-P01 — Explorer Frame, Existing Route Posture, Data-Source Inventory, and Guardrails
```

Rationale:

- establishes the `/research-management` host and no-route-drift posture;
- maps all artifact families to existing sources;
- makes collection/tag mutation deferral explicit;
- proves no actuation, no recompute, no external AI, and no source mutation before any organization mutation;
- preserves review narrowness for the first phase.

---

## 15. Constitutional and Doc 16 attestation

The DA attests this design plan is:

- centralized discovery and organization over existing research artifacts;
- no underlying artifact mutation;
- no verdict/status/confidence/economic value mutation;
- no live data, broker, order, account, execution, real-P&L, or Gate path;
- no external AI/LLM;
- no client-side analytics engine;
- no recompute/inference/re-derivation/reclassification;
- no new table by default;
- no new route by default;
- no new dependency;
- mutation phases strictly organization-only and raw-psql-evidence-bound;
- Doc 16 B-1…B-7 applies;
- production remains not certified.

DA does not self-approve this design plan and does not begin UI-006 implementation. Implementation awaits ITRGA design acceptance and a controlled Build Order.

---

**End of UI-006_ENGINEERING_DESIGN_PLAN.md**
