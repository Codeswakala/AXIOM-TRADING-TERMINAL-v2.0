# UI-004 Engineering Design Plan — Research & Intelligence Workspace

| Field | Value |
|---|---|
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-004 — Research & Intelligence Workspace |
| Document type | Engineering Design Plan; pre-Build-Order; no implementation authorization |
| Development Authority | AXIOM DA |
| ITRGA request | `docs/build-orders/ITRGA_REQUEST_UI-004_DESIGN_PLAN.md` |
| Predecessor milestones | UI-001 COMPLETE · UI-002 COMPLETE · UI-003 COMPLETE |
| Platform baseline | v0.62.0 |
| Alembic head | `20260717_0037` |
| Baseline validation | backend 414 passed · frontend 36 files / 151 tests |
| Governance Gate | CLOSED |
| Production status | Not certified; governed separately by `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md` |
| Governing UI docs | `12_INSTITUTIONAL_UI_TRANSFORMATION_PLAN.md` §6 → `13_UI_TRANSFORMATION_MASTER_PLAN.md` → UI-001/UI-002/UI-003 completed foundations → `16_BRAND_GOVERNANCE_STANDARD.md` |

---

## 0. Executive summary

UI-004 shall unify AXIOM's existing institutional research and intelligence capabilities into a continuous professional research workflow. Per Document 12 §6, UI-004 scope is:

```text
Institutional Intelligence
Advisory Signals
Performance Analytics
Research artifacts
Validation
Economic usefulness
Report viewers
Intelligence drilldowns
```

Expected outcome:

> Institutional research becomes a continuous analytical workflow rather than isolated pages.

This plan is **presentation/navigation/integration only**. UI-004 shall display existing governed intelligence, advisory, analytics, validation, economic-usefulness, research-artifact, and report data. It shall not recompute, reinterpret, re-score, infer, generate signals, derive validation status, derive economic-usefulness verdicts, cherry-pick favorable analytics, introduce external AI/LLM, introduce live/real data, introduce execution controls, or open the Governance Gate.

Default persistence decision: **reuse existing stores**. Research artifacts already exist in W3/W4/W5/W6/W7 stores. Saved view/layout state, if needed, shall reuse `operator_workspace_preferences` under a UI-004 preference key with artifact ids, route ids, filter ids, panel visibility, and section expansion only. No new table is proposed by default.

This plan does not authorize implementation. It is submitted for ITRGA design review. Only an accepted plan and a subsequent `BUILD_ORDER_UI-004-P01` may authorize implementation.

---

## 1. Objective and scope mapping to Document 12 §6

### 1.1 Objective restatement

UI-004 shall turn AXIOM's existing research, intelligence, signal, analytics, validation, and report pages into a coherent institutional research workspace. The operator should move from advisory signal context to intelligence reports, validation evidence, economic-usefulness framing, analytics metrics, collections/tags, and report drilldowns without losing orientation or constitutional context.

The workstream must preserve the difference between:

```text
stored governed research evidence
```

and

```text
new analysis or interpretation
```

UI-004 may organize, display, link, filter, and navigate existing artifacts. UI-004 may not author new analytical truth.

### 1.2 Scope mapping

| Doc 12 §6 item | UI-004 design interpretation | Explicit boundary |
|---|---|---|
| Institutional Intelligence | Present existing W4 intelligence report families and W7 portfolio-research report previews in a unified intelligence workspace. | No new intelligence computation, no regime/scenario/correlation recompute, no generated summary beyond stored report fields. |
| Advisory Signals | Present existing advisory signal records with state, rationale, lineage, guardrails, freshness, calibrated confidence, and disclaimers. | No signal generation, no signal mutation, no guardrail override, no action controls. |
| Performance Analytics | Present existing advisory performance analytics and confidence bands with sample counts and uncertainty. | No client-side metric recompute, no cherry-picking, no favorable filtering that misrepresents performance. |
| Research artifacts | Surface existing research collections, tags, journal references, report ids, signal ids, and artifact metadata. | No new artifact table by default; no copying source content into preference state. |
| Validation | Display existing validation/generalization/calibration/drift statuses and report fields verbatim where available. | No validation re-derivation, no status upgrades/downgrades, no hidden scoring. |
| Economic usefulness | Display existing economic-usefulness/economic verdict fields and limitations verbatim. | No reinterpretation or operator-facing upgrade from `not_assessed` to usable. |
| Report viewers | Create first-party viewers for existing report payloads, source ids, limitations, uncertainty, and hashes. | No new report generation; no external report renderer dependency. |
| Intelligence drilldowns | Provide read-only drilldown panels and navigation from summary cards to stored report details. | Drilldown means progressive disclosure of stored values, not compute or inference. |

---

## 2. Bright-line constitutional controls

### 2.1 Brightest line #1 — display existing governed intelligence, do not recompute

UI-004 must preserve the following hard rule:

```text
Continuous analytical workflow = presentation/navigation over existing governed artifacts.
```

UI-004 may:

- display existing reports;
- display existing signals;
- display existing analytics metrics;
- display stored validation/economic-usefulness statuses;
- provide artifact-level navigation and drilldowns;
- render report payloads in accessible institutional viewers;
- reuse existing collections/tags for context;
- persist presentation state only.

UI-004 shall not:

- perform client-side inference;
- perform authoritative recomputation;
- introduce a new analytical algorithm;
- generate signals;
- infer regimes;
- recompute correlations, scenarios, validation, calibration, drift, portfolio risk, or economic usefulness;
- generate new intelligence summaries using external AI/LLM;
- change any stored verdict;
- hide unfavorable sample counts, uncertainty, or limitations;
- introduce live/real data;
- introduce execution/order/broker/account controls;
- open or bypass the Governance Gate.

### 2.2 Validation and economic-usefulness integrity

Validation statuses and economic-usefulness fields shall be rendered exactly as stored. The UI may explain where a value came from and show related limitations. It may not reclassify, relabel, normalize into stronger claims, or infer a higher-confidence verdict.

Examples:

| Stored value | UI-004 permitted rendering | Forbidden rendering |
|---|---|---|
| `research_only` | Research-only | Tradable / executable |
| `not_assessed` | Not assessed | Economically usable |
| `warning:POORLY_CALIBRATED` | Warning: poorly calibrated | Approved / reliable |
| low sample count | Low sample count; uncertainty visible | Hidden from dashboard |
| limitations array | Limitations displayed | Omitted when unfavorable |

### 2.3 No-cherry-picking discipline

UI-004 shall preserve the W6 analytics discipline: report viewers must surface included scope, sample counts, source artifact ids, uncertainty, and limitations. UI filters may help the operator find records, but the UI must not present filtered views as full-scope performance truth unless the stored report itself declares that scope.

### 2.4 Advisory signal posture

Advisory signals remain research-advisory records. UI-004 must preserve:

- signal state and state reason;
- rationale and lineage;
- model/report ids;
- freshness/expiry;
- calibrated confidence, not raw-score-as-confidence;
- economic verdict;
- operating-domain and calibration status;
- disclaimers: not financial advice, not a trade instruction, operator decides;
- non-actionable presentation.

---

## 3. UI-001 / UI-002 / UI-003 reconciliation and no-duplication table

| UI-004 scope item | Existing primitive/source | Classification | UI-004 design decision |
|---|---|---|---|
| Research workspace frame | UI-001 shell Region C, Region D context panel, Region E activity dock; UI-002 breadcrumbs/workflow navigation/search/palette. | Extend | Mount within the existing shell; no new frame, no page-owned global nav, no second command system. |
| Research/intelligence primary route | Existing `/intelligence`, `/signals`, `/analytics`, `/research-management`, `/portfolio-research` routes in the Workspace Registry. | Reuse/extend | Prefer enhancing `/intelligence` as the primary Research & Intelligence workspace while preserving existing routes as workflow destinations unless a Build Order authorizes registry changes. |
| Advisory signal list/detail | Existing `AdvisorySignalsPage`, `fetchAdvisorySignals`, `fetchAdvisorySignal`. | Reuse | Integrate read-only signal cards/drilldowns with links to reports and analytics. |
| Performance analytics | Existing `PerformanceAnalyticsPage`, `fetchAdvisoryAnalytics`. | Reuse | Display existing metrics/confidence bands with uncertainty and sample counts; no recompute. |
| Institutional intelligence reports | Existing `InstitutionalIntelligencePage`, `fetchInstitutionalIntelligenceBundle`, W4 report APIs. | Reuse/extend | Professional report viewers and drilldowns over stored reports. |
| Research collections/tags | Existing W7-U03 research management APIs and UI-002 search first-slice. | Reuse | Use collections/tags as artifact context; no new artifact table. |
| Report viewers | Existing JSON/report payloads and first-party panel/card/table CSS primitives. | Extend | Build first-party viewers; no external renderer dependency. |
| Related market/chart context | UI-003 chart/source-provenance and marker patterns. | Reuse pattern | Link out to chart context where stored artifacts reference symbols/timeframes; do not compute chart overlays in UI-004. |
| Overlay/dialog needs | UI-001 Region-F overlay family. | Reuse | Drilldowns use existing dialog/overlay only if needed; no second overlay family. |
| Saved view/layout state | Existing `operator_workspace_preferences`. | Reuse | Persist view ids/section visibility only if authorized; no new table by default. |

### 3.1 No-duplication commitments

UI-004 shall not introduce:

- a second application shell;
- a second navigation dock;
- a second command palette;
- a second global search framework;
- a second overlay/dialog/notification family;
- page-local route maps independent of Workspace Registry;
- independent design tokens or off-palette styles;
- third-party report/chart/table dependencies without ITRGA-approved spike;
- browser-side analytics engines.

### 3.2 UI-009 dependency status

UI-004 depends conceptually on UI-009, but existing completed workstreams already provide substantial first-party component foundations:

| Needed UI-004 component class | Existing status | UI-009 posture |
|---|---|---|
| Shell/panels/layout | UI-001 complete | Reuse directly. |
| Navigation/breadcrumbs/search/palette | UI-002 complete | Reuse directly. |
| Chart/source/marker/provenance patterns | UI-003 complete | Reuse patterns where report artifacts link to market context. |
| Cards/badges/status pills/tables | Existing first-party CSS/components | Reuse and improve locally; flag reusable pieces for later UI-009 harvesting. |
| Report viewer | Net-new first-party component candidate | Implement locally in UI-004 phase if authorized; no third-party dependency. |
| Lineage/uncertainty/economic panels | Net-new first-party component candidates | Implement as UI-004 local components first; flag for UI-009 library. |
| Drilldown panels | Existing PanelHost + overlay family | Reuse shell infrastructure; local content components only. |

No UI-009 standalone implementation is required before UI-004-P01, provided UI-004 uses existing primitives and flags reusable components for later component-library consolidation.

---

## 4. Architecture

### 4.1 Proposed workspace composition

Primary strategy: enhance the existing Institutional Intelligence route as the Research & Intelligence workspace center, then progressively connect existing signals, analytics, and research-management routes through UI-002 navigation.

```text
InstitutionalWorkspaceShell (UI-001)
├── Region A — Global Header / UI-002 breadcrumbs/search/palette/switcher
├── Region B — Navigation Dock (UI-002 workflow nav)
├── Region C — Research & Intelligence Workspace (UI-004)
│   ├── Research Command/Scope Bar (view filters only)
│   ├── Intelligence Overview Cards (stored report counts/statuses)
│   ├── Advisory Signal Context Panel (stored signals, read-only)
│   ├── Performance Analytics Summary (stored metrics, uncertainty)
│   ├── Validation & Economic Usefulness Panels (stored verdicts)
│   ├── Report Viewer / Drilldown Region (stored payloads)
│   └── Research Artifact Context (collections/tags/source ids)
├── Region D — Context Panel
│   ├── Selected artifact lineage
│   ├── Uncertainty/limitations summary
│   ├── Related workflow navigation
│   └── Governance/research-only framing
├── Region E — Activity Dock
│   ├── Recent viewed artifacts (session/presentation only)
│   └── Research status/activity summary using existing artifacts
└── Region F — Existing overlay family for optional drilldowns/dialogs
```

### 4.2 State ownership

| State | Owner | Persistence | Notes |
|---|---|---|---|
| Shell layout/session | UI-001 shell | Existing shell preference | UI-004 consumes; does not replace. |
| Navigation/search/palette/breadcrumbs | UI-002 | Existing UI-002 modules | UI-004 contributes metadata only if authorized. |
| Active research view | UI-004 presentation state | Optional existing preferences | View id only; no report payload storage. |
| Selected report/signal/artifact id | UI-004 presentation state | Optional existing preferences | Artifact ids only; no copied report body. |
| Filters/sort/visible sections | UI-004 presentation state | Optional existing preferences | Presentation-only. |
| Report payloads | Existing backend read APIs | Existing stores | UI reads and displays; no mutation. |
| Collections/tags | Existing W7-U03 stores | Existing stores | UI reads/writes only if existing route already authorizes collection/tag actions; UI-004 P01 should read only. |
| Drilldown open/closed | UI-004 presentation state | In-memory or preference | No business state. |

---

## 5. Data-source table

| Surface | Existing governed origin | Existing API/frontend seam | UI-004 usage | New backend? |
|---|---|---|---|---|
| Advisory signal records | W3 `advisory_signals` | `fetchAdvisorySignals`, `fetchAdvisorySignal`, `AdvisorySignalsPage` | Read-only signal context cards, detail panels, lineage links | No |
| Advisory performance analytics | W3/W4 analytics service over existing advisory records | `fetchAdvisoryAnalytics`, `PerformanceAnalyticsPage` | Display stored/generated response fields with uncertainty/sample counts | No |
| Institutional intelligence bundle | W4 report families | `fetchInstitutionalIntelligenceBundle`, `InstitutionalIntelligencePage` | Intelligence overview and report group panels | No |
| Correlation reports | W4 correlation reports | Existing `/api/v1/intelligence/correlation-reports` via bundle | Report viewer drilldowns | No |
| Regime reports | W4 regime reports | Existing `/api/v1/intelligence/regime-reports` via bundle | Report viewer drilldowns, stored labels only | No |
| Scenario reports | W4 scenario reports | `fetchScenarioReports`, `fetchScenarioReport` | Stored hypothetical scenario report viewer links | No |
| Portfolio/risk reports | W4/W7 portfolio research | `fetchPortfolioResearchDashboard`, `fetchAdvancedResearchReport`, portfolio page | Read-only report preview/context where in research scope | No |
| Signal validation reports | W4 signal validation | Existing bundle group / report payloads | Validation status panels, stored values only | No |
| Calibration/economic/generalization ids | W2/W3/W4 report references stored on signals/reports | Existing signal/report payload fields | Display lineage and status references; no recompute | No |
| Monitoring/health alert context | W3 monitoring alerts | `fetchMonitoringAlerts` where already used | Optional research-status context only | No |
| Research collections/tags | W7-U03 research management | `fetchResearchManagementBundle`, `fetchResearchCollections`, `fetchResearchTags` | Related artifacts/context and saved research organization | No |
| Research journal entries | W5 manual journal | `fetchJournalEntries` / existing journal route/search | Related-artifact navigation only in early phases | No |
| Chart/market context links | UI-003 chart workspace and source-provenance patterns | Existing chart route and source labels | Link to chart context by symbol/timeframe where stored | No |
| UI saved view state | W7-U02 operator preferences | Existing workspace preference API | Optional presentation preferences only | No new table |

### 5.1 Explicit no-new-analysis statement

Every surface in the table above uses existing governed values. UI-004 shall not recompute metrics, derive confidence, infer regimes, recalculate economic usefulness, generate report summaries, generate new advisory signals, or run external AI/LLM.

---

## 6. Persistence design

### 6.1 Decision

UI-004 shall **reuse existing stores** and **reuse `operator_workspace_preferences` for saved view state if needed**.

No new table is proposed by default.

### 6.2 Existing stores reused

| Need | Existing store/API | Reuse mode |
|---|---|---|
| Research reports | W4 report tables and read APIs | Read existing reports. |
| Advisory signals | W3 `advisory_signals` | Read existing signals. |
| Performance analytics | Existing analytics API | Read response. |
| Collections/tags | W7-U03 research management | Read/link existing artifacts; existing route may retain authorized create/update where already approved. |
| Journal references | W5 journal APIs | Read/search/navigation only in UI-004 early phases. |
| View/layout preferences | W7-U02 `operator_workspace_preferences` | Store ids/visibility/filter prefs only. |

### 6.3 Optional preference key and safe payload sketch

If a Build Order authorizes saved view state, proposed key:

```text
research-intelligence-workspace-v1
```

Payload sketch:

```json
{
  "workspace_key": "research-intelligence-workspace-v1",
  "layout_config": {
    "active_view": "overview",
    "selected_artifact": {
      "artifact_type": "advisory_signal",
      "artifact_id": "signal-id-only"
    },
    "visible_sections": [
      "intelligence_overview",
      "advisory_signals",
      "performance_analytics",
      "validation",
      "economic_usefulness",
      "report_viewer"
    ],
    "report_filters": {
      "report_family": "all",
      "symbol": "EURUSD",
      "timeframe": "M1"
    },
    "expanded_panels": ["validation", "limitations"]
  },
  "visible_modules": [
    "institutional_intelligence",
    "advisory_signals",
    "performance_analytics"
  ],
  "theme_config": { "density": "institutional" },
  "metadata": { "ui_workstream": "UI-004", "version": "research-intelligence-v1" }
}
```

Allowed persisted values:

```text
artifact ids
workspace/view ids
route ids
filter ids
symbol/timeframe ids
visible-section ids
expanded/collapsed panel ids
sort keys / display density
```

Forbidden persisted values:

```text
report payload bodies
raw prompt text
secret values
model outputs generated by UI
order/position/account/broker/P&L fields
derived validation/economic verdicts
client-side computed analytics
```

### 6.4 If ITRGA requires a new table

No new table is proposed. If ITRGA later requires one, the first Build Order touching persistence must include:

- justified RBAC-scoped backend touch;
- Alembic migration with head progression;
- committing seed/capture script;
- raw `psql SELECT >= 1 row`;
- no-orphan audit JOIN;
- `operator_id -> operators.id` JOIN;
- `information_schema` forbidden-column proof;
- no positions/orders/P&L/actionable fields;
- no API read-back substitution for raw psql.

---

## 7. Validation, economic-usefulness, and drilldown integrity

### 7.1 Verbatim rendering rule

UI-004 shall render stored verdicts and statuses verbatim. Examples include:

```text
research_status
economic_verdict
economic_usefulness
calibration_status
operating_domain_status
freshness_status
validation status
sample_count
limitations
uncertainty
report_hash
source_artifact_ids
```

### 7.2 Drilldown semantics

A UI-004 drilldown is progressive disclosure of stored artifact fields:

```text
summary card -> selected artifact -> detail panel -> source/lineage/limitations
```

A drilldown is not:

- recomputation;
- model explanation generated in the browser;
- natural-language summary generated by an external service;
- reclassification of status;
- signal/action generation.

### 7.3 No-cherry-picking proof design

Per-phase tests and evidence shall prove:

- sample counts visible where analytics are visible;
- uncertainty/limitations visible in metric/report cards;
- full included scope or source artifact ids visible in report viewers;
- filtered UI labels do not claim full-scope performance unless the stored report declares full scope;
- no code path computes new aggregate performance from displayed rows.

---

## 8. Advisory-signal presentation plan

UI-004 signal surfaces shall present:

- signal id;
- symbol/timeframe;
- signal state and reason;
- calibrated confidence with calibration status;
- freshness/expiry;
- operating domain status;
- economic verdict;
- model/report lineage ids;
- rationale;
- limitations/risk notes where present;
- research-only disclaimer.

They shall not present:

- buy/sell buttons;
- order tickets;
- trade direction as instruction;
- broker/account state;
- position size;
- Gate-open or execution controls;
- raw score as confidence;
- generated next-step recommendations.

---

## 9. Doc 16 brand plan (B-1…B-7)

| Brand gate | UI-004 plan |
|---|---|
| B-1 Logo/monogram | Use existing UI-001 shell AX monogram and AXIOM identity. No new logo variant or recoloring. |
| B-2 Color | Use constitutional palette and existing tokens. Intelligence/research/signal statuses use semantic token roles only. No off-palette brand color. |
| B-3 Typography | Maintain institutional hierarchy; use monospace for ids, symbols, sample counts, confidence values, report hashes, timestamps. |
| B-4 Iconography | Use existing registry icon style and UI-002 navigation categories. No mixed icon set. |
| B-5 Institutional-not-retail | Copy emphasizes research evidence, uncertainty, limitations, non-authoritative/advisory posture; no speculative/retail cues. |
| B-6 Accessibility | Dark-theme contrast, visible focus, readable dense tables/cards, non-color status labels, screen-reader report summaries. |
| B-7 Documentation branding | Delivery reports/evidence/design docs use AXIOM governance format and reference Doc 16 completion gates. |

Browser evidence for every implementation phase must include brand proof, not just grep.

---

## 10. Accessibility plan

UI-004 surfaces are data-dense and report-heavy; accessibility is first-class.

### 10.1 Report viewers

Required:

- semantic headings for report families and sections;
- table captions and column headers;
- keyboard navigation through report cards and drilldowns;
- screen-reader-readable summary of uncertainty, sample count, limitations, and source ids;
- copyable report ids/hashes as text, not image-only;
- no color-only state communication;
- focus return after dialogs/drilldowns close.

### 10.2 Drilldowns and panels

Required:

- `aria-expanded` where sections collapse;
- `aria-controls` for drilldown toggles;
- role/label discipline for dialogs if Region-F is used;
- Escape/close focus handling through existing overlay family;
- reduced-motion-compatible expansion.

### 10.3 Analytics and signal cards

Required:

- calibrated confidence expressed in text;
- status text next to color chips;
- warnings and limitations in text;
- keyboard-operable selection;
- visible focus;
- empty/loading/error states explaining research impact.

---

## 11. Responsive and layout plan

| Viewport | Behavior |
|---|---|
| Large desktop | Overview + signal context + analytics + report viewer visible in coordinated panels. |
| Standard desktop | Research overview primary; selected artifact and report viewer stacked below/alongside. |
| Laptop | Report families collapse into sections; selected drilldown occupies main width. |
| Narrow/tablet-like | Single-column stacked cards, accessible tables with horizontal scroll where unavoidable, context panels hidden by shell rules. |

Responsive behavior must preserve single UI-001 shell and UI-002 navigation. No page-specific responsive nav may appear.

---

## 12. Phase decomposition

Implementation requires ITRGA acceptance of this plan and controlled Build Orders. No phase begins until authorized. No later phase begins until ITRGA accepts the prior phase unless ITRGA explicitly authorizes parallel work.

### UI-004-P01 — Research Workspace Frame and Data-Source Inventory

Objective: establish the Research & Intelligence workspace frame inside the existing shell and prove all surfaces map to existing governed data sources.

Scope:

- mount/enhance research workspace frame inside UI-001/UI-002;
- overview of intelligence, signals, analytics, validation, economic-usefulness, and artifacts as placeholders or thin read-only cards;
- complete data-source inventory visible in UI and tests;
- no saved view persistence yet unless ITRGA authorizes;
- no backend/API/schema/dependency change.

Named test anchors:

```text
test_ui004_research_workspace_mounts_inside_single_ui001_shell
test_ui004_research_workspace_registers_through_ui002_navigation_only
test_ui004_research_workspace_maps_every_surface_to_existing_sources
test_ui004_research_workspace_contains_no_recompute_inference_or_signal_generation
test_ui004_research_workspace_preserves_gate_closed_research_only_branding
```

### UI-004-P02 — Advisory Signals and Performance Analytics Integration

Objective: integrate existing advisory signals and advisory performance analytics into a continuous read-only research workflow.

Scope:

- read-only advisory signal cards/details;
- analytics metric/confidence-band panels using existing analytics API;
- signal-to-analytics context links;
- calibrated confidence and sample count display;
- no raw-score-as-confidence;
- no action controls.

Named test anchors:

```text
test_ui004_signals_render_existing_records_read_only_with_guardrails
test_ui004_analytics_render_existing_metrics_with_uncertainty_and_sample_counts
test_ui004_signals_and_analytics_do_not_recompute_or_cherry_pick
test_ui004_signal_surfaces_contain_no_execution_order_or_gate_path
test_ui004_signal_analytics_accessibility_and_brand_markers_hold
```

### UI-004-P03 — Intelligence Report Viewers and Drilldowns

Objective: create first-party institutional report viewers and drilldowns over existing W4/W7 report payloads.

Scope:

- report family navigation;
- report detail viewer;
- source ids, report hashes, method versions, limitations, uncertainty;
- progressive disclosure/drilldowns;
- no report generation or external renderer.

Named test anchors:

```text
test_ui004_report_viewers_render_existing_intelligence_reports_only
test_ui004_drilldowns_disclose_stored_fields_without_recomputation
test_ui004_report_viewers_preserve_lineage_uncertainty_limitations_and_hashes
test_ui004_report_viewers_use_first_party_components_no_new_dependency
test_ui004_report_viewers_are_keyboard_and_screen_reader_accessible
```

### UI-004-P04 — Validation and Economic-Usefulness Integrity Panels

Objective: provide dedicated validation/economic-usefulness panels that render stored verdicts verbatim and preserve no-cherry-picking discipline.

Scope:

- validation/economic-usefulness sections for selected signals/reports;
- stored statuses/verdicts visible;
- limitations/sample counts/scope visible;
- warning states remain warnings;
- no status reinterpretation.

Named test anchors:

```text
test_ui004_validation_statuses_are_rendered_verbatim_from_existing_artifacts
test_ui004_economic_usefulness_verdicts_are_not_rederived_or_upgraded
test_ui004_no_cherry_picking_sample_counts_scope_and_limitations_visible
test_ui004_validation_economic_panels_contain_no_client_side_analytics_engine
test_ui004_validation_economic_panels_preserve_research_only_disclaimers
```

### UI-004-P05 — Research Artifacts, Collections, and Saved View Preferences

Objective: integrate existing research artifacts/collections/tags and optionally save presentation-only view state through existing preferences.

Scope:

- research artifact context panels using existing research management APIs;
- collection/tag context links;
- optional saved UI view state under `operator_workspace_preferences`;
- artifact ids/filter ids only;
- no report payload copy;
- raw psql preference proof if persistence is implemented.

Named test anchors:

```text
test_ui004_artifact_context_uses_existing_research_management_sources
test_ui004_saved_views_use_operator_workspace_preferences_no_new_table
test_ui004_saved_views_store_ids_only_no_payloads_or_action_fields
test_ui004_artifact_context_preserves_operator_scope_and_no_secret_fields
test_ui004_artifact_saved_view_persistence_preserves_alembic_head
```

### UI-004-P06 — UI-004 Completion Checkpoint

Objective: final integration evidence and ITRGA completion review for UI-004.

Scope:

- route/browser integration evidence;
- whole-surface no-actuation and no-recompute grep;
- full regression;
- persistence proof if P05 saved views are implemented;
- constitutional and Doc 16 brand self-check;
- browser-served workflow proof.

Named test anchors:

```text
test_ui004_completion_research_intelligence_workflow_is_continuous_without_scope_expansion
test_ui004_completion_all_research_surfaces_are_existing_artifact_presentation_only
test_ui004_completion_no_recompute_inference_external_ai_live_data_or_execution_path
test_ui004_completion_validation_economic_usefulness_and_no_cherry_picking_hold
test_ui004_completion_accessibility_brand_and_ui001_ui002_integration_hold
```

---

## 13. Regression and evidence strategy

Each UI-004 Build Order shall provide a Level-I evidence bar:

- build identity proof;
- named tests displayed passing by verbose reporter;
- frontend full suite at/above baseline with no test loss;
- TypeScript clean;
- production build with bundle delta;
- npm audit;
- backend Ruff and backend full suite unless ITRGA narrows evidence;
- Alembic current = `20260717_0037` unless a separately authorized persistence migration occurs;
- package-manifest content proof showing no new dependency;
- no-new-endpoint/schema/provider grep;
- whole-surface no-actuation grep;
- **no-recompute/no-inference/no-signal-generation grep** for UI-004 source;
- no external AI/LLM grep;
- no-cherry-picking/uncertainty/sample-count tests where analytics/report surfaces are touched;
- served browser screenshots for route, responsive, keyboard, accessibility, and Doc 16 brand proof;
- networked Git-Bash CI with `LOCAL_CI_EXIT_CODE: 0`, or documented `TD-W6-CI-AUDIT` env-flake after substantive gates are green and operator/ITRGA waiver.

Standing no-drift method: git-diff phase isolation remains retired for this single-commit DA repository. UI-004 no-drift proof shall rely on per-phase tests, Alembic current, source greps, package manifest content, regression totals, and raw psql persistence-capture when applicable.

---

## 14. Risks and mitigations

| Risk | Severity | Mitigation |
|---|---:|---|
| UI appears to recompute intelligence or validation | Critical | Data-source inventory, source greps, named tests, verbatim status rendering. |
| Economic usefulness is over-interpreted | Critical | Stored verdicts shown verbatim; limitations and sample counts visible. |
| Analytics are cherry-picked | Critical | Included scope/sample count/source ids visible; tests reject misleading filtered full-scope claims. |
| Advisory signals become actionable | Critical | No action controls, disclaimers, no-actuation grep, read-only cards. |
| External AI/LLM temptation for summaries | Critical | Explicit prohibition; first-party stored-field viewers only. |
| New table creep for saved views | High | Reuse `operator_workspace_preferences`; raw psql capture if persistence used. |
| Duplicate workspace/navigation patterns | High | UI-001/UI-002 integration tests; registry-only navigation. |
| Report viewers become inaccessible dense JSON dumps | High | First-party semantic viewers, captions, keyboard drilldowns, summaries. |
| UI-009 component drift | Medium | Local first-party components flagged for later harvesting; no third-party dependencies. |
| Brand drift into retail dashboard style | High | Doc 16 B-1…B-7 browser proof every phase. |

---

## 15. Open questions for ITRGA

1. Does ITRGA accept enhancing the existing `/intelligence` route as the primary UI-004 Research & Intelligence workspace, while preserving `/signals` and `/analytics` as workflow destinations?
2. Does ITRGA accept the default no-new-table posture, with optional saved view state under `operator_workspace_preferences` using `research-intelligence-workspace-v1`?
3. Should UI-004-P02 integrate both advisory signals and performance analytics in one phase, or split advisory and analytics into separate phases for narrower review?
4. Should existing research collections/tags remain read-only in early UI-004 phases, deferring any collection/tag mutation UI changes to UI-006 Artifact Explorer?
5. Does ITRGA require raw psql read-back for UI-004 saved preferences if implemented, following the UI-003 watchlist precedent?
6. Should UI-002-P04b search adapters remain independent/non-blocking, or should UI-004 implementation include any adapter work only after a separate Build Order?

---

## 16. DA recommendation for first Build Order

If ITRGA accepts this plan, the DA recommends the first Build Order be:

```text
UI-004-P01 — Research Workspace Frame, Existing Data-Source Inventory, and No-Recompute Guardrail
```

Rationale:

- proves the continuous research workspace inside the completed shell/navigation/market foundations;
- establishes the brightest-line no-recompute/no-inference guardrail before report viewers or saved state;
- maps every UI-004 surface to existing governed sources;
- avoids persistence complexity until source/integration boundaries are accepted;
- creates baseline browser evidence for Doc 16 brand and accessibility.

---

## 17. Constitutional and Doc 16 attestation

The DA attests this design plan is:

- presentation-only;
- no new analysis/computation/live-data/capability;
- no client-side inference;
- no authoritative recompute;
- no validation/economic-usefulness re-derivation;
- no signal generation;
- no no-cherry-picking violation;
- no new backend/API/schema/dependency by default;
- no real market feed/broker/account/order path;
- no external AI/LLM;
- no dynamic plugin execution;
- no Governance Gate change;
- extends UI-001, UI-002, and UI-003 without duplication;
- proposes no new table by default;
- proposes no new dependency;
- applies Doc 16 brand gates B-1…B-7;
- does not certify production.

DA does not self-approve this design plan and does not begin UI-004 implementation. Implementation awaits ITRGA design acceptance and a controlled Build Order.

---

**End of UI-004_ENGINEERING_DESIGN_PLAN.md**
