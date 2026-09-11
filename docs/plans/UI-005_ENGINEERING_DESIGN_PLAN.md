# UI-005 Engineering Design Plan — Investigation & Planning Workspace

| Field | Value |
|---|---|
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-005 — Investigation & Planning Workspace |
| Document type | Engineering Design Plan; pre-Build-Order; no implementation authorization |
| Development Authority | AXIOM DA |
| ITRGA request | `docs/build-orders/ITRGA_REQUEST_UI-005_DESIGN_PLAN.md` |
| Predecessor milestones | UI-001 COMPLETE · UI-002 COMPLETE · UI-003 COMPLETE · UI-004 COMPLETE |
| Platform baseline | v0.62.0 |
| Alembic head | `20260717_0037` |
| Baseline validation | backend 414 passed · frontend 43 files / 186 tests |
| Governance Gate | CLOSED |
| Production status | Not certified; governed separately by `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md` |
| Governing UI docs | `12_INSTITUTIONAL_UI_TRANSFORMATION_PLAN.md` §7 → `13_UI_TRANSFORMATION_MASTER_PLAN.md` → completed UI-001/UI-002/UI-003/UI-004 foundations → `16_BRAND_GOVERNANCE_STANDARD.md` |

---

## 0. Executive summary

UI-005 shall integrate existing analytical investigation and planning surfaces into a continuous, constitutionally safe research workflow. Per Document 12 §7, UI-005 scope is:

```text
Signal Investigation
Scenario Comparison
Trade Planning
Execution Research
Research Journal
Portfolio Research
```

Expected outcome:

> Operators move naturally from investigation to planning while preserving analytical context.

This design plan is **presentation/navigation/integration only**. It does not authorize implementation. UI-005 shall expose existing governed artifacts and existing authorized research-note stores through the completed UI-001 shell, UI-002 navigation, UI-003 market context patterns, and UI-004 research/intelligence patterns.

UI-005 is higher sensitivity than UI-004 because it names **Trade Planning** and **Execution Research**. Therefore the plan pre-registers the following: planning remains advisory and research-oriented; execution research remains **SIMULATED** and display-only; no order ticket, broker, account, position, balance, margin, live-real data, go-live, execute, or Gate path may appear.

Default persistence decision: **no new table**. Existing stores remain authoritative. If a future phase persists presentation-only investigation/planning view state, it shall reuse `operator_workspace_preferences` with ids/visibility/filter prefs only and raw psql evidence. This plan proposes no schema or dependency change.

---

## 1. Objective and scope mapping to Document 12 §7

| Doc 12 §7 item | Existing surface/store | UI-005 design interpretation | Explicit boundary |
|---|---|---|---|
| Signal Investigation | `/investigate`, advisory signal read APIs, W3 signal records, UI-004 report/lineage patterns | Primary investigation hub showing signal rationale, guardrails, lineage, related reports, chart/research context. | No signal recompute, guardrail override, confidence derivation, or action recommendation. |
| Scenario Comparison | `/compare-scenarios`, existing W4 scenario reports | Compare existing hypothetical scenario reports with assumptions, uncertainty, limitations, and scope visible. | No scenario generation, no new what-if engine, no cherry-picking. |
| Trade Planning | `/trade-plans`, existing W5-U06 trade plan note store/API | Research planning notes remain inert, advisory, and operator-authored. Existing authorized store may remain available; UI-005 does not expand it. | No order ticket, position sizing, stop/target as executable order, broker/account fields, or plan-to-execution path. |
| Execution Research | `/execution-research`, existing W6 simulated execution research artifacts | SIMULATED execution research context shown as evidence for planning, with assumptions and limitations. | No live execution, real fill, real order, broker connection, account state, or Gate path. |
| Research Journal | `/journal`, existing W5-U07 manual journal store/API | Research documentation and reflection context linked to signals, reports, plans, scenarios, and journal entries. | No broker import, account journal import, execution/P&L fields, or assistant drafting path. |
| Portfolio Research | `/portfolio-research`, existing W7 portfolio research dashboard/report preview | Review and portfolio research context for planning and investigation, with hypothetical/research framing. | No real account, real P&L, real portfolio state, or live allocation surface. |

---

## 2. Constitutional brightest lines

### B-1 — Gate CLOSED / no actuation anywhere

UI-005 shall not introduce or expose:

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

Trade Planning is research-note planning only. Execution Research is SIMULATED and display-only. The Governance Gate remains CLOSED.

### B-2 — No recompute / inference / re-derivation / external AI

UI-005 shall not:

- infer signal direction;
- recompute confidence or validation;
- generate scenarios;
- derive economic usefulness;
- run a client-side analytics engine;
- generate AI/LLM summaries;
- reclassify stored verdicts;
- generate action recommendations.

### B-3 — Verbatim posture preserved

UI-005 inherits UI-004's verbatim-verdict rule:

```text
research_only      -> research_only / Research-only, never tradable/executable
not_assessed       -> not_assessed / Not assessed, never economically usable
warning:*          -> warning as stored, never approved/reliable
SIMULATED          -> SIMULATED, never live/real
```

### B-4 — No-cherry-picking

Scenario, analytics, portfolio, and execution research views shall show:

- included scope;
- sample counts;
- assumptions;
- uncertainty;
- limitations;
- source artifact ids;
- report hashes where available.

Filtered or selected views shall not claim full-scope truth unless the stored artifact declares that scope.

### B-5 — Read-only reuse / no new analytical authorship

UI-005 consumes existing read APIs and existing authorized stores. It shall not add backend capability, analytical engines, new artifact generation, new dependency, or external AI.

---

## 3. Route / registry posture

### 3.1 Default route strategy

UI-005 shall enhance existing registered routes. No new workspace route is proposed by default.

| Existing route | Role in UI-005 |
|---|---|
| `/investigate` | Primary signal investigation and investigation/planning workflow hub. |
| `/compare-scenarios` | Existing scenario comparison workflow destination. |
| `/trade-plans` | Existing inert trade planning research notes destination. |
| `/execution-research` | Existing SIMULATED execution research evidence destination. |
| `/journal` | Existing research journal/documentation destination. |
| `/portfolio-research` | Existing portfolio research/review destination. |
| `/charts` | Existing chart context link target from UI-003. |
| `/intelligence`, `/signals`, `/analytics` | Existing UI-004 research context link targets. |

### 3.2 Registry rule

No registry route add/relabel is proposed for P01. Any future registry change requires ITRGA pre-approval, proof the 14-field Workspace Registry contract is unchanged, and no duplicate navigation.

---

## 4. Persistence posture

### 4.1 Default decision

No new table is proposed.

Existing stores remain authoritative:

| Need | Existing store/API | UI-005 posture |
|---|---|---|
| Advisory signals | W3 signal history/read API | Read-only investigation context. |
| Intelligence/validation/economic reports | W4/W7 report APIs and UI-004 viewers | Read-only supporting evidence. |
| Scenario reports | W4 scenario reports APIs | Read-only comparison of stored hypothetical reports. |
| Trade plans | W5-U06 trade plan notes | Existing authorized research-note create/update may remain; no expansion. |
| Journal entries | W5-U07 manual journal entries | Existing authorized research-reflection create/update may remain; no broker/account import. |
| Execution research | W6 simulated execution stores/APIs | Read-only SIMULATED evidence. |
| Portfolio research | W7 portfolio research APIs | Hypothetical/read-only aggregation. |
| Presentation saved state | `operator_workspace_preferences` if authorized | ids/visibility/filter prefs only, no payloads. |

### 4.2 Optional presentation preference key

If ITRGA authorizes saved view state in a later UI-005 phase, proposed key:

```text
investigation-planning-workspace-v1
```

Allowed values:

```text
active_investigation_signal_id
selected_scenario_report_ids
selected_plan_id
selected_journal_id
selected_execution_research_run_id
selected_portfolio_report_id
visible_sections
expanded_panels
filter ids / route ids / symbol-timeframe ids
```

Forbidden values:

```text
report body copies
journal/plan text copies into preferences
analytics payloads
execution payloads
order/account/broker/position/P&L fields
secrets
derived verdicts or scores
```

If implemented, raw PostgreSQL persistence capture is mandatory: save → inline `psql SELECT >= 1 row` on `operator_workspace_preferences`, no forbidden fields, `operator_id -> operators.id`, `alembic current = 20260717_0037`.

### 4.3 Trade Planning & Journal mutation boundary

Trade Planning and Journal already have authorized research-only create/update stores from W5. UI-005 does not propose expanding those mutations. Any phase that touches them must prove:

- fields remain research note/reflection fields only;
- no order/account/broker/execution/P&L fields;
- no plan-to-execution path;
- no broker/account journal import;
- existing APIs only;
- no new backend endpoint/table.

---

## 5. Data-source table

| Surface | Existing governed source | Existing frontend/API seam | UI-005 use | New backend? |
|---|---|---|---|---|
| Signal investigation | W3 advisory signals and linked report ids | `fetchAdvisorySignals`, `fetchAdvisorySignal`, `/investigate` | Rationale/guardrails/lineage/context disclosure | No |
| Intelligence/validation context | W4/W7 reports | UI-004 report viewers and `fetchInstitutionalIntelligenceBundle` | Related evidence and stored verdicts | No |
| Scenario comparison | W4 scenario reports | `fetchScenarioReports`, `fetchScenarioReport` | Existing hypothetical comparison | No |
| Trade plans | W5 trade plan notes | existing `fetchTradePlans`, create/update APIs | Existing research planning notes; no expansion | No |
| Execution research | W6 simulated runs/fills/ledger/risk/experiments/analytics | `fetchExecutionResearchBundle` | SIMULATED evidence context | No |
| Journal entries | W5 manual journal | `fetchJournalEntries`, create/update APIs | Research documentation links | No |
| Portfolio research | W7 portfolio dashboard/report preview | `fetchPortfolioResearchDashboard`, `fetchAdvancedResearchReport` | Hypothetical review context | No |
| Chart annotations/context | W5/UI-003 chart annotations and chart workspace | existing chart/annotation APIs | Related chart context links | No |
| Collections/tags | W7 research management | `fetchResearchManagementBundle` | Read-only context unless UI-006 authorizes mutation | No |

---

## 6. Architecture

```text
InstitutionalWorkspaceShell (UI-001)
├── UI-002 Navigation / Breadcrumbs / Search / Palette
├── Existing /investigate primary workflow surface
│   ├── Investigation workflow frame
│   ├── Active signal lineage and guardrails
│   ├── Related reports / validation / economic context (UI-004 patterns)
│   ├── Related scenario / plan / journal / execution research / portfolio links
│   └── No-actuation / research-only guardrails
├── Existing workflow destinations
│   ├── /compare-scenarios
│   ├── /trade-plans
│   ├── /execution-research
│   ├── /journal
│   └── /portfolio-research
└── Existing context/activity panels
```

State ownership:

| State | Owner | Persistence |
|---|---|---|
| Shell layout/navigation | UI-001/UI-002 | existing shell preferences |
| Active investigation selection | UI-005 presentation state | in-memory by default |
| Plan/journal content | Existing W5 stores if existing pages used | existing stores only |
| Saved UI view state | Optional future phase | `operator_workspace_preferences` if authorized |
| Analytical values | Existing backend artifacts | never browser-authored |

---

## 7. UI-001 / UI-002 / UI-003 / UI-004 reuse

| Foundation | UI-005 reuse |
|---|---|
| UI-001 shell/panels/layout | All UI-005 surfaces mount inside existing shell. |
| UI-002 workflow navigation | Existing routes, breadcrumbs, switcher, palette, context nav. |
| UI-003 chart context | Chart/annotation/source-provenance patterns for investigation links. |
| UI-004 report viewers/analytics/verbatim panels/artifact context | Investigation surfaces use these patterns for related evidence disclosure. |
| Doc 16 brand | B-1…B-7 gate applies every phase. |

No duplicate shell, navigation, palette, overlay, chart engine, report viewer library, or analytics engine is proposed.

---

## 8. Accessibility plan

UI-005 must support:

- keyboard-operable investigation selection;
- semantic headings and regions;
- text labels for every status, never color alone;
- accessible scenario comparison tables/cards;
- accessible plan/journal forms where existing forms remain;
- clear SIMULATED labels for execution research;
- screen-reader summaries of limitations, uncertainty, and lineage;
- visible focus and logical tab order;
- responsive stacked layouts.

---

## 9. Doc 16 brand plan

| Brand gate | UI-005 design |
|---|---|
| B-1 Logo/monogram | Existing shell identity only; no logo change. |
| B-2 Color | Existing tokens only; semantic colors for statuses/warnings. |
| B-3 Typography | Monospace ids, hashes, sample counts, symbol/timeframe, plan/report ids. |
| B-4 Iconography | Existing registry/navigation icon style; no mixed icon set. |
| B-5 Institutional-not-retail | Copy emphasizes investigation, evidence, assumptions, limitations, research-only planning. |
| B-6 Accessibility | Contrast, focus, non-color status labels, keyboard forms/drilldowns. |
| B-7 Documentation branding | AXIOM governance report/evidence format. |

---

## 10. Phase decomposition

### UI-005-P01 — Investigation & Planning Workspace Frame / Data-Source Inventory

Objective: establish the UI-005 workflow frame and prove all surfaces map to existing sources.

Scope:

- enhance existing `/investigate` as primary workflow hub;
- data-source inventory for signal investigation, scenario comparison, trade plans, execution research, journal, portfolio research;
- no mutation changes;
- no persistence;
- no backend/schema/dependency.

Named test anchors:

```text
test_ui005_workspace_mounts_inside_single_ui001_shell
test_ui005_workspace_uses_existing_routes_and_registry_only
test_ui005_workspace_maps_every_surface_to_existing_sources
test_ui005_workspace_contains_no_actuation_or_gate_path
test_ui005_workspace_preserves_research_only_and_doc16_branding
```

### UI-005-P02 — Signal Investigation Lineage & Related Evidence

Objective: integrate existing signal investigation with lineage, validation, chart, and report context.

Named test anchors:

```text
test_ui005_signal_investigation_renders_existing_signal_lineage_read_only
test_ui005_investigation_uses_stored_confidence_validation_and_economic_values_verbatim
test_ui005_investigation_links_related_reports_without_recompute
test_ui005_investigation_contains_no_signal_generation_or_actuation
test_ui005_investigation_accessibility_and_brand_markers_hold
```

### UI-005-P03 — Scenario Comparison & Portfolio Research Context

Objective: connect existing scenario comparison and portfolio research surfaces as read-only/hypothetical planning evidence.

Named test anchors:

```text
test_ui005_scenarios_render_existing_hypothetical_reports_only
test_ui005_portfolio_research_remains_hypothetical_no_real_account_pnl
test_ui005_comparison_preserves_assumptions_uncertainty_limitations_scope
test_ui005_comparison_contains_no_generation_or_execution_path
test_ui005_scenario_portfolio_accessibility_and_brand_markers_hold
```

### UI-005-P04 — Trade Planning & Journal Continuity

Objective: connect existing research plans and journal reflections to investigation context without expanding mutation scope.

Named test anchors:

```text
test_ui005_trade_plans_use_existing_research_note_store_no_order_ticket
test_ui005_journal_uses_existing_reflection_store_no_broker_import
test_ui005_planning_preserves_research_only_fields_and_forbidden_field_rejection
test_ui005_plan_journal_links_are_artifact_ids_not_execution_paths
test_ui005_planning_journal_accessibility_and_brand_markers_hold
```

### UI-005-P05 — Execution Research / SIMULATED Evidence Context

Objective: integrate existing SIMULATED execution research artifacts into planning context as display-only evidence.

Named test anchors:

```text
test_ui005_execution_research_renders_existing_simulated_artifacts_only
test_ui005_execution_research_never_claims_live_execution_or_real_fills
test_ui005_execution_research_preserves_assumptions_uncertainty_limitations
test_ui005_execution_research_contains_no_broker_order_account_or_gate_path
test_ui005_execution_research_accessibility_and_brand_markers_hold
```

### UI-005-P06 — UI-005 Completion Checkpoint

Objective: final integration evidence and ITRGA completion review.

Named test anchors:

```text
test_ui005_completion_investigation_to_planning_workflow_is_continuous_without_scope_expansion
test_ui005_completion_all_surfaces_are_existing_artifact_presentation_or_existing_research_notes
test_ui005_completion_no_execution_broker_account_live_data_ai_or_gate_path
test_ui005_completion_verbatim_values_no_cherry_picking_and_simulated_boundaries_hold
test_ui005_completion_accessibility_brand_and_ui001_ui002_integration_hold
```

---

## 11. Evidence and regression strategy

Every UI-005 phase shall provide:

- build identity;
- named tests displayed passing by verbose reporter;
- no-actuation grep;
- no-recompute/no-inference/no-external-AI grep;
- no new endpoint/schema/dependency proof;
- no registry change proof unless pre-approved;
- Alembic current = `20260717_0037` unless separately authorized;
- full frontend regression at/above baseline with no test loss;
- backend regression at/above 414;
- TypeScript/build/audit evidence;
- browser served-session evidence;
- Doc 16 brand proof;
- networked CI with sentinel or disclosed TD-W6-CI-AUDIT env-flake.

Standing residual `TD-UI-POSTCSS-HIGH` remains open and must be remediated/accepted before Production Readiness Certification. Any phase that touches dependencies must address it.

---

## 12. Open questions for ITRGA

1. Does ITRGA accept enhancing existing `/investigate` as the primary UI-005 workflow hub while preserving existing `/compare-scenarios`, `/trade-plans`, `/execution-research`, `/journal`, and `/portfolio-research` routes?
2. Does ITRGA accept no-new-table as the default persistence posture, with optional `operator_workspace_preferences` saved view state only if a later phase explicitly needs it?
3. Should trade-planning and journal existing create/update surfaces remain unchanged in UI-005, or should early phases be read-only until a planning-specific phase?
4. Should UI-005-P04 be split into trade planning and journal as separate phases if ITRGA wants narrower mutation-boundary review?
5. Should UI-005-P05 cover execution research and portfolio context together, or split simulated execution research into its own dedicated phase?
6. Should UI-002-P04b search adapters remain independent/non-blocking until UI-006 Artifact Explorer?

---

## 13. DA recommendation for first Build Order

If ITRGA accepts this plan, DA recommends:

```text
UI-005-P01 — Investigation & Planning Workspace Frame, Data-Source Inventory, and No-Actuation Guardrail
```

Rationale:

- proves route/registry posture before surface integration;
- establishes the no-actuation boundary for trade planning/execution research terminology;
- maps every UI-005 surface to existing stores;
- avoids persistence and mutation scope in the first phase;
- creates the baseline browser/brand/accessibility evidence for the workstream.

---

## 14. Constitutional and Doc 16 attestation

The DA attests this design plan is:

- presentation/navigation/integration only;
- no new analysis/computation/live-data/capability;
- no client-side inference;
- no authoritative recompute;
- no validation/economic-usefulness re-derivation;
- no scenario generation;
- no execution/order/broker/account/Gate path;
- execution research remains SIMULATED/display-only;
- trade planning remains research-note/advisory only;
- no external AI/LLM;
- no dynamic plugin execution;
- no new table by default;
- no new dependency;
- Doc 16 B-1…B-7 applies;
- production remains not certified.

DA does not self-approve this design plan and does not begin UI-005 implementation. Implementation awaits ITRGA design acceptance and a controlled Build Order.

---

**End of UI-005_ENGINEERING_DESIGN_PLAN.md**
