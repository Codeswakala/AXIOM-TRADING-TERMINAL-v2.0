# UI-002 Engineering Design Plan — Workflow Navigation Framework

| Field | Value |
|---|---|
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-002 — Workflow Navigation Framework |
| Document type | Engineering Design Plan; pre-Build-Order; no implementation authorization |
| Development Authority | AXIOM DA |
| ITRGA request | `docs/build-orders/ITRGA_REQUEST_UI-002_DESIGN_PLAN.md` |
| Predecessor milestone | `ITRGA_REVIEW_UI-001-P06_FINAL_AND_UI-001_COMPLETION.md` — UI-001 COMPLETE |
| Platform baseline | v0.62.0 |
| Alembic head | `20260717_0037` |
| Baseline validation | backend 414 passed · frontend 26 files / 97 tests |
| Governance Gate | CLOSED |
| Production status | Not certified; governed separately by `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md` |
| Governing UI docs | `12_INSTITUTIONAL_UI_TRANSFORMATION_PLAN.md` → `13_UI_TRANSFORMATION_MASTER_PLAN.md` → `14_UI-001_TECHNICAL_DESIGN_SPECIFICATION.md` → `15_UI-001_IMPLEMENTATION_SPECIFICATION.md` |

---

## 0. Executive Summary

UI-002 shall transform AXIOM navigation from page-oriented access into workflow-oriented operation while preserving UI-001 as the single workstation shell.

UI-001 is complete and remains the permanent application frame. UI-002 therefore **extends** the existing UI-001 Navigation Dock, Workspace Registry, Command Palette, Region-F overlay family, Shell Event Bus, Panel Infrastructure, Layout Manager, and shell preference seam. It shall not create a second navigation system, a second command palette, a second overlay framework, a competing layout, or any new business capability.

UI-002 scope, per Document 12 §4, includes:

```text
workflow navigation
global search
command palette
breadcrumbs
context-aware navigation
workspace switching
quick actions
```

The constitutional target is:

> Operators navigate according to institutional workflows rather than software modules.

This design plan recommends a frontend-first implementation. The default position is:

- no backend business-logic change;
- no new API endpoint;
- no new database table;
- no Alembic migration;
- no dependency addition;
- no server-side search index;
- no external AI/LLM;
- no dynamic plugin execution;
- no execution, order, broker, account, live, or Gate-opening surface.

Global search shall initially be a **read-only navigation index** over the UI-001 Workspace Registry and existing authenticated read/list APIs. Results shall only navigate to existing routes or existing artifact views where already supported. Search shall not create, mutate, execute, approve, open the Governance Gate, connect brokers, place orders, or trigger backend workflows.

This plan does **not** authorize implementation. It is submitted for ITRGA review. Only an accepted plan and a subsequent `BUILD_ORDER_UI-002-P01` may authorize implementation.

---

## 1. Constitutional Intake and Scope Confirmation

### 1.1 Intake facts recorded

| Item | Determination |
|---|---|
| UI-001-P06 final review | APPROVED by ITRGA |
| UI-001 milestone | COMPLETE — Institutional Workspace Shell complete |
| UI-002 request | Engineering Design Plan requested by ITRGA |
| Implementation authorization | Not yet authorized |
| Production deployment | Not certified |
| Governance Gate | CLOSED |

### 1.2 In scope for UI-002

| Scope item | Design intent |
|---|---|
| Workflow navigation | Present navigation according to institutional research lifecycle stages, not raw page/module structure. |
| Global search | Search workspaces and existing read-only artifacts, producing read-only jump-to results. |
| Command palette | Extend the existing UI-001 palette with registered navigation/UI-toggle commands only. |
| Breadcrumbs | Provide deterministic route/workflow/artifact orientation derived from registry and route context. |
| Context-aware navigation | Suggest related workflow destinations using static workflow maps and, where available, read-only artifact context. |
| Workspace switching | Provide keyboard-accessible switching between registered workspaces and recent workspace routes. |
| Quick actions | Provide enumerated navigation/UI-toggle shortcuts vetted item-by-item by ITRGA. |

### 1.3 Explicit non-scope

UI-002 shall not implement or alter:

- backend business logic;
- database schema;
- Alembic head;
- API contracts unless separately authorized by ITRGA;
- governance behavior;
- Governance Gate state;
- execution, order, broker, account, position, balance, margin, capital, live, real-money, or real P&L paths;
- external AI/LLM services;
- dynamic plugin execution;
- new analytical/research algorithms;
- new trading/research capability;
- production deployment or production certification;
- page-specific navigation, independent sidebars, duplicate headers, or competing layouts.

### 1.4 UI-001 inheritance rule

UI-002 shall inherit UI-001. It may add UI-002 presentation modules that consume UI-001 primitives, but it shall not change UI-001 architectural responsibilities without a separate constitutional amendment.

---

## 2. UI-001 Reconciliation Table

The table below maps each Document 12 §4 item to UI-001 reuse, extension, or net-new UI-002 responsibility.

| Doc 12 §4 item | UI-001 delivered primitive | UI-002 classification | UI-002 design decision |
|---|---|---|---|
| Workflow navigation | Navigation Dock generated from the 14-field Workspace Registry; workflow categories already exist (`Monitor`, `Research`, `Investigate`, `Compare`, `Plan`, `Review`, `Govern`, `Settings`). | Extends existing UI-001 primitive | Add a companion workflow metadata model keyed by `workspace.id` rather than forking the UI-001 registry. UI-001 remains the source of workspace identity, route, RBAC, layout, search-support, and no-actuation fields. |
| Global search | Workspace Registry has `search.enabled` and `search.scopes`; Region A provides header command entry; Region F hosts overlays. | Net-new UI-002 module hosted by UI-001 primitives | Implement `GlobalSearch` as a Region-F overlay/search mode using existing overlay infrastructure and read-only source adapters. No independent overlay/search framework. |
| Command palette | UI-001 Command Palette exists and type-enforces `commandType: "navigation" | "ui-toggle"`. | Extends existing UI-001 primitive | Add a typed `CommandRegistry` and vetted quick-action catalogue that feeds the existing palette. No second palette and no business/action command type. |
| Breadcrumbs | UI-001 header displays active workspace title derived from active route/registry. | Net-new presentation component | Add `BreadcrumbTrail` in Region A, deterministically derived from route + workspace + workflow metadata; optional artifact crumb only from read-only route/context data. |
| Context-aware navigation | UI-001 Context Panel, Panel Registry, Layout Manager, Shell Event Bus, and active workspace metadata. | Extends existing UI-001 primitive | Add a context-navigation model/panel that suggests read-only related routes. It may consume Shell Event Bus context but shall not own business state or mutate artifacts. |
| Workspace switching | UI-001 Navigation Dock, registry-driven palette navigation, shell preference last-route restoration. | Extends existing UI-001 primitive | Add a keyboard-accessible workspace switcher powered by visible registry entries and optional recent workspace ids stored through existing shell preferences. |
| Quick actions | UI-001 palette supports navigation/UI-toggle commands only. | Extends existing UI-001 primitive | Enumerate every quick action in this plan; generate command entries from the approved catalogue only. Every action is navigation or UI-toggle only. |

### 2.1 Anti-duplication commitments

UI-002 shall not introduce:

- a second global nav;
- workspace-owned sidebars for global navigation;
- duplicated route maps outside the Workspace Registry and additive workflow metadata;
- a second command palette;
- a second overlay layer;
- page-specific breadcrumbs independent of the registry;
- a separate search application shell;
- command types beyond `navigation` and `ui-toggle`.

---

## 3. Proposed Architecture

### 3.1 High-level composition

```text
InstitutionalWorkspaceShell                (UI-001 permanent frame)
├── Region A — Global Header
│   ├── BreadcrumbTrail                    (UI-002)
│   ├── GlobalSearchTrigger                (UI-002)
│   └── WorkspaceSwitcher                  (UI-002)
├── Region B — Navigation Dock             (UI-001; UI-002 workflow metadata extension)
├── Region C — Primary Workspace           (UI-001 WorkspaceHost; unchanged ownership)
├── Region D — Context Panel
│   └── ContextNavigationPanel             (UI-002 through UI-001 PanelHost/registry)
├── Region E — Activity Dock               (UI-001; no UI-002 ownership change)
└── Region F — Overlay Layer
    ├── Existing CommandPalette            (UI-001; extended by UI-002 command registry)
    └── GlobalSearchOverlay/SearchMode     (UI-002 hosted in existing Region F)
```

### 3.2 Proposed module boundaries

Representative frontend-only module layout:

```text
frontend/src/workstation/workflows/
  workflowTypes.ts
  workflowNavigationMetadata.ts
  workflowModel.ts
  workflowModel.test.ts

frontend/src/workstation/navigation/
  BreadcrumbTrail.tsx
  WorkspaceSwitcher.tsx
  ContextNavigationPanel.tsx
  WorkflowNavigation.test.tsx

frontend/src/workstation/search/
  globalSearchTypes.ts
  globalSearchSources.ts
  globalSearchIndex.ts
  GlobalSearchOverlay.tsx
  GlobalSearch.test.tsx

frontend/src/workstation/commands/
  commandTypes.ts
  commandRegistry.ts
  quickActionCatalogue.ts
  CommandRegistry.test.ts
```

The exact file paths may be refined by Build Order, but the architecture shall preserve these boundaries:

| Boundary | Owner | Responsibility |
|---|---|---|
| UI-001 Workspace Registry | UI-001 shell infrastructure | Authoritative workspace identity, route, RBAC, no-actuation guard, layout/search flags. |
| UI-002 Workflow Metadata | UI-002 navigation presentation | Workflow stage, breadcrumb labels, related workflow route hints, search keywords. |
| UI-002 Search Sources | UI-002 search presentation | Read-only adapters over existing data sources; normalize into jump-to results. |
| UI-002 Command Registry | UI-002 command presentation | Register navigation/UI-toggle commands from workspace registry and approved quick actions. |
| Workspaces | Existing workspace modules | Own business/research presentation and existing API usage; no global navigation ownership. |

### 3.3 Data flow

```text
Workspace Registry
  ↓
Workflow Metadata Reconciliation
  ↓
Workflow Navigation Model
  ├── Navigation Dock sections
  ├── BreadcrumbTrail
  ├── WorkspaceSwitcher
  ├── CommandRegistry navigation commands
  └── GlobalSearch workspace results

Existing authenticated read APIs
  ↓
Read-only Search Source Adapters
  ↓
Ephemeral client-side search index
  ↓
GlobalSearch results
  ↓
Navigate to existing route / artifact view
```

### 3.4 State ownership

| State | Owner | Persistence | Notes |
|---|---|---|---|
| Current route | React Router / UI-001 shell | Browser history | UI-002 consumes but does not own route engine. |
| Workflow metadata | UI-002 static metadata module | Source code only | Keyed by `workspace.id`; no backend. |
| Breadcrumb state | Derived UI state | None | Derived from route + workflow metadata. |
| Search query | UI-002 overlay component | None | Query text shall not be persisted. |
| Search results | UI-002 search controller | Memory only | Derived from registry/existing read APIs. |
| Search source cache | UI-002 search controller | Memory only with short TTL | No localStorage/sessionStorage of artifact payloads unless separately approved. |
| Recent workspace ids | UI-001 shell preference seam, if implemented | Existing `operator_workspace_preferences.layout_config` | Store workspace ids/routes only; no search queries or artifact content. |
| Command palette open/closed | UI-001 OverlayProvider | React state | Existing palette provider remains owner. |
| Quick action catalogue | UI-002 static command module | Source code only | Requires ITRGA vetting. |

---

## 4. Workflow Navigation Model

### 4.1 Institutional lifecycle stages

UI-002 shall represent navigation using the institutional research lifecycle from Document 12 Part IV:

```text
Observe → Detect → Investigate → Analyze → Compare → Plan → Document → Review → Govern
```

Settings remains a supporting operator-configuration area and shall not be presented as a research lifecycle stage.

### 4.2 Current workspace-to-workflow mapping

| Workspace id | Route | Current UI-001 category | UI-002 workflow stage | Role in workflow |
|---|---|---|---|---|
| `monitor.operations` | `/` | Monitor | Observe / Govern awareness | Platform operations, health, alerts, Gate status. |
| `monitor.live_market` | `/live` | Monitor | Observe | Market observation and status. |
| `monitor.chart_workspace` | `/charts` | Monitor | Observe / Investigate | Chart observation and governed annotations. |
| `research.advisory_signals` | `/signals` | Research | Detect | Advisory observations and signal state. |
| `research.analytics` | `/analytics` | Research | Analyze / Review | Performance and calibration analytics. |
| `research.intelligence` | `/intelligence` | Research | Analyze | Institutional intelligence reports. |
| `investigate.signal_investigation` | `/investigate` | Investigate | Investigate | Rationale, guardrail, and lineage review. |
| `compare.scenarios` | `/compare-scenarios` | Compare | Compare | Hypothetical scenario comparison. |
| `plan.trade_plans` | `/trade-plans` | Plan | Plan | Inert research planning notes. |
| `plan.execution_research` | `/execution-research` | Plan | Plan / Review | SIMULATED execution research review. |
| `review.portfolio_research` | `/portfolio-research` | Review | Review | Hypothetical portfolio research aggregation. |
| `review.journal` | `/journal` | Review | Document | Manual research journal. |
| `review.research_management` | `/research-management` | Review | Document / Review | Collections, tags, artifact organization. |
| `settings.workspace` | `/workspace` | Settings | Settings | Presentation preferences only. |

The `Govern` workflow stage remains represented through existing Gate/governance status until UI-007 authorizes a dedicated Governance & Evidence Workspace. UI-002 shall not create a new governance workspace route.

### 4.3 Companion workflow metadata contract

To avoid changing UI-001 architectural responsibilities, UI-002 should add a companion metadata contract keyed by the existing `workspace.id`:

```ts
type WorkflowStage =
  | "Observe"
  | "Detect"
  | "Investigate"
  | "Analyze"
  | "Compare"
  | "Plan"
  | "Document"
  | "Review"
  | "Govern"
  | "Settings";

type WorkflowNavigationMetadata = {
  workspaceId: string;
  primaryStage: WorkflowStage;
  secondaryStages?: readonly WorkflowStage[];
  breadcrumbLabel: string;
  workflowOrdinal: number;
  keywords: readonly string[];
  relatedWorkspaceIds: readonly string[];
  defaultNextWorkspaceIds: readonly string[];
  defaultPreviousWorkspaceIds: readonly string[];
  quickActionIds: readonly string[];
  searchEntityTypes: readonly SearchEntityType[];
};
```

Validation rules:

- every metadata entry must reference an existing UI-001 workspace id;
- every visible workspace should either have metadata or an explicit no-metadata exclusion;
- related/next/previous ids must reference existing registry entries;
- no metadata entry may contain business mutation descriptors;
- no route may be introduced solely by metadata.

### 4.4 Navigation Dock extension

UI-002 may adjust the presentation of the existing Navigation Dock to emphasize lifecycle progression, but it shall still consume visible workspaces generated from the Workspace Registry.

Allowed improvements:

- workflow stage labels;
- lifecycle ordering;
- current stage highlighting;
- keyboard shortcuts displayed consistently;
- accessible descriptions;
- optional compact view of workflow stages;
- deterministic related-workflow hints.

Prohibited changes:

- hardcoded workspace lists independent of registry;
- alternate sidebars;
- workspace-owned global navigation;
- mutation/action controls in navigation;
- RBAC bypass or independent permission logic.

---

## 5. Global Search Design

### 5.1 Design objective

Global search shall provide a read-only, workstation-wide way to find existing workspaces and existing artifacts. It shall return navigation targets only.

### 5.2 Result model

```ts
type SearchEntityType =
  | "workspace"
  | "signal"
  | "intelligence-report"
  | "scenario-report"
  | "journal-entry"
  | "research-collection"
  | "research-tag"
  | "portfolio-report"
  | "chart-annotation"
  | "trade-plan"
  | "execution-research-artifact"
  | "setting";

type GlobalSearchResult = {
  id: string;
  entityType: SearchEntityType;
  title: string;
  subtitle: string;
  sourceWorkspaceId: string;
  route: string;
  artifactId?: string;
  badges: readonly string[];
  snippet?: string;
  provenance: "workspace-registry" | "existing-read-api";
  resultAction: "navigate";
  readonly: true;
};
```

Mandatory invariants:

- `resultAction` is always `"navigate"`;
- `readonly` is always `true`;
- no result may contain an executable callback other than route navigation;
- no result may expose secret markers or privileged payloads;
- search result selection shall not POST, PUT, PATCH, DELETE, execute, approve, connect, place, size, allocate, or open the Gate.

### 5.3 Search sources

| Source | Data origin | Existing API / origin | Target route | UI-002 posture |
|---|---|---|---|---|
| Workspaces | UI-001 Workspace Registry | `WORKSPACE_REGISTRY` | workspace route | Always available; no API. |
| Advisory signals | Existing read API | `fetchAdvisorySignals(...)` / `/api/v1/signals/history` | `/signals` or `/investigate` | Read-only jump-to signal context. |
| Institutional intelligence reports | Existing read APIs | `fetchInstitutionalIntelligenceBundle(...)` and report list endpoints | `/intelligence` | Read-only report discovery. |
| Scenario reports | Existing read API | `fetchScenarioReports(...)` | `/compare-scenarios` | Read-only comparison target. |
| Journal entries | Existing read API | `fetchJournalEntries(...)` | `/journal` | Read-only navigation to journal workspace or item where supported. |
| Research collections/tags | Existing read API | `fetchResearchManagementBundle(...)` | `/research-management` | Read-only artifact organization discovery. |
| Portfolio research | Existing read APIs | `fetchPortfolioResearchDashboard(...)`; report search may be deferred if endpoint computes heavy output | `/portfolio-research` | Read-only summary/report navigation; no generation on every keystroke. |
| Chart annotations | Existing read API | `fetchChartResearchAnnotations(...)` | `/charts` | Read-only annotation discovery. |
| Trade plans | Existing read API | `fetchTradePlans(...)` | `/trade-plans` | Read-only plan navigation; no create/update action. |
| Execution research artifacts | Existing read API | `fetchExecutionResearchBundle(...)` | `/execution-research` | SIMULATED/research-only artifact discovery. |
| Settings | Workspace registry/settings metadata | `settings.workspace` | `/workspace` | Presentation-preference navigation only. |

### 5.4 Indexing approach

Initial UI-002 global search shall use an ephemeral client-side index:

- normalize selected safe fields from registry entries and read/list responses;
- debounce query input, recommended 200–300 ms;
- require minimum query length of 2 characters for API-backed sources;
- cap results per source and globally;
- cache source results in memory only with a short TTL;
- avoid persisting search queries or artifact payloads;
- cancel obsolete requests with `AbortController` where practical;
- rank with first-party deterministic matching: exact prefix > word prefix > substring > keyword match;
- avoid a fuzzy-search dependency in the first implementation.

No server index, table, migration, or new search endpoint is proposed.

If ITRGA later requests a backend search index, that shall require a dedicated persistence/endpoint review with RBAC scoping, read-only semantics, no execution surface, persistence-capture evidence, and no dependency adoption without a spike.

### 5.5 Search user experience

Global search shall be accessible from Region A and rendered through Region F.

Expected behavior:

1. operator opens search from the Global Header or keyboard shortcut;
2. focus moves to the search input;
3. results are grouped by entity type and owning workflow stage;
4. each result displays title, type, owning workspace, and research/governance framing where applicable;
5. Enter or click navigates to the existing route;
6. Escape closes search and restores focus;
7. result count is announced to assistive technology;
8. no result presents an action verb such as execute, place order, connect broker, approve Gate, allocate, or size.

### 5.6 Deep-link policy

If an existing route supports a detail view or query parameter, the search result may navigate there. If not, the result shall navigate to the owning workspace and optionally provide non-persistent UI state for focus/highlight. Lack of a deep route shall not justify adding backend capability or new artifact mutations under UI-002.

---

## 6. Breadcrumbs and Context-Aware Navigation

### 6.1 Breadcrumb model

Breadcrumbs shall be deterministic and derived from route/registry/workflow metadata:

```text
AXIOM → Workflow Stage → Workspace → Optional Artifact Context
```

Examples:

```text
AXIOM → Observe → Chart Workspace
AXIOM → Detect → Advisory Signals
AXIOM → Investigate → Signal Investigation → Signal [id]
AXIOM → Document → Research Journal → Entry [id]
```

The optional artifact crumb may appear only when artifact identity is already available from route/query state or an existing read-only workspace context. Breadcrumbs shall not fetch privileged content solely to display a label unless an existing read endpoint already provides that label to the operator.

### 6.2 Breadcrumb component rules

`BreadcrumbTrail` shall:

- render within Region A;
- use `<nav aria-label="Breadcrumb">`;
- mark current item with `aria-current="page"`;
- avoid color-only hierarchy;
- provide keyboard-accessible links for navigable ancestors;
- never bypass `WorkspaceHost` or UI-001 routing.

### 6.3 Context-aware navigation model

Context-aware navigation shall suggest **where to go next**, not **what business action to perform**.

Representative static workflow transitions:

| Active workspace | Suggested read-only destinations | Rationale |
|---|---|---|
| Operations | Live Market, Chart Workspace, Advisory Signals | Move from platform status to observation/detection. |
| Live Market | Chart Workspace, Advisory Signals | Observe markets then inspect signal state. |
| Chart Workspace | Advisory Signals, Signal Investigation, Research Journal | Preserve chart context while moving to research evidence. |
| Advisory Signals | Signal Investigation, Performance Analytics, Institutional Intelligence | Move from detected signal to rationale/evidence. |
| Performance Analytics | Institutional Intelligence, Portfolio Research | Move from metrics to deeper intelligence/review. |
| Institutional Intelligence | Scenario Comparison, Signal Investigation, Research Management | Move from evidence to comparison or artifact organization. |
| Signal Investigation | Institutional Intelligence, Scenario Comparison, Trade Planning | Continue investigation into analysis/compare/plan. |
| Scenario Comparison | Trade Planning, Research Journal, Portfolio Research | Preserve comparison context through planning and review. |
| Trade Planning | Execution Research, Research Journal | Plan remains research-only, then simulation review/documentation. |
| Execution Research | Portfolio Research, Research Journal | Review SIMULATED research and document findings. |
| Research Journal | Research Management, Portfolio Research | Organize and review documented artifacts. |
| Research Management | Portfolio Research, Operations | Review portfolio research or return to platform status. |
| Portfolio Research | Research Management, Operations | Organize artifacts or return to status/governance visibility. |
| Workspace Settings | Previous workspace, Operations | Return to research flow after preference update. |

### 6.4 Shell Event Bus context

Where existing or future workspaces publish context through the UI-001 Shell Event Bus, UI-002 may consume a safe presentation contract:

```ts
type NavigationContext = {
  workspaceId: string;
  artifactType?: SearchEntityType;
  artifactId?: string;
  label?: string;
  relatedWorkspaceIds: readonly string[];
  source: "route" | "workspace-event" | "search-selection";
};
```

Rules:

- event payloads are presentation metadata only;
- no business calculations in the navigation layer;
- no backend mutation;
- no order/execution/broker/Gate commands;
- unknown artifact types are ignored safely.

---

## 7. Command Palette Extension

### 7.1 Existing UI-001 primitive

UI-001 already delivered a global command palette under Region F with command types restricted to:

```ts
"navigation" | "ui-toggle"
```

UI-002 shall preserve that type boundary.

### 7.2 UI-002 command registry

UI-002 should introduce a declarative command registry generated from:

1. visible UI-001 Workspace Registry entries;
2. approved quick-action catalogue entries;
3. UI-only shell toggles;
4. search/open/focus commands.

Representative contract:

```ts
type CommandType = "navigation" | "ui-toggle";

type CommandDefinition = {
  id: string;
  label: string;
  commandType: CommandType;
  target: {
    route?: string;
    region?: "A" | "B" | "C" | "D" | "E" | "F";
    overlay?: "command-palette" | "global-search" | "status-dialog";
  };
  keywords: readonly string[];
  source: "workspace-registry" | "quick-action-catalogue" | "shell-ui";
  enabled: boolean;
  noActuation: true;
};
```

Validation rules:

- every command must have `commandType` of `navigation` or `ui-toggle`;
- every navigation command must route to an existing authorized workspace route;
- every UI-toggle command must target shell UI state only;
- no command may invoke business writes, backend mutations, broker actions, execution actions, Gate actions, account actions, or order actions;
- command registry tests shall fail on disallowed words and disallowed command types.

### 7.3 Palette behavior

The existing `CommandPalette` may be refactored internally to consume the command registry, but it shall remain the single global palette.

Allowed extensions:

- grouping commands by workflow stage;
- showing quick actions;
- launching global search overlay/mode;
- displaying keyboard shortcuts;
- improved keyboard navigation and active result management;
- accessible command count announcements.

Prohibited extensions:

- business action commands;
- mutation commands;
- workspace-local command systems competing with the global palette;
- external plugin command execution;
- command execution over dynamically loaded code.

---

## 8. Quick-Action Catalogue for ITRGA Vetting

Every quick action below is explicitly proposed as navigation or UI-toggle only. Any action not listed here is out of scope until ITRGA approves a revised catalogue.

| ID | Name | What it does | Target | Command type | Constitutional assertion |
|---|---|---|---|---|---|
| `qa.open.operations` | Open Operations | Navigates to the Operations workspace. | Route `/` | navigation | Navigation/UI-toggle only; never business/trading/execution/order/broker/account/Gate mutation. |
| `qa.open.live-market` | Open Live Market | Navigates to the Live Market workspace. | Route `/live` | navigation | Navigation/UI-toggle only; never business/trading/execution/order/broker/account/Gate mutation. |
| `qa.open.charts` | Open Chart Workspace | Navigates to the Chart Workspace. | Route `/charts` | navigation | Navigation/UI-toggle only; never business/trading/execution/order/broker/account/Gate mutation. |
| `qa.open.signals` | Open Advisory Signals | Navigates to the Advisory Signals workspace. | Route `/signals` | navigation | Navigation/UI-toggle only; never business/trading/execution/order/broker/account/Gate mutation. |
| `qa.open.analytics` | Open Performance Analytics | Navigates to the Performance Analytics workspace. | Route `/analytics` | navigation | Navigation/UI-toggle only; never business/trading/execution/order/broker/account/Gate mutation. |
| `qa.open.intelligence` | Open Institutional Intelligence | Navigates to the Institutional Intelligence workspace. | Route `/intelligence` | navigation | Navigation/UI-toggle only; never business/trading/execution/order/broker/account/Gate mutation. |
| `qa.open.investigation` | Open Signal Investigation | Navigates to the Signal Investigation workspace. | Route `/investigate` | navigation | Navigation/UI-toggle only; never business/trading/execution/order/broker/account/Gate mutation. |
| `qa.open.scenario-comparison` | Open Scenario Comparison | Navigates to the Scenario Comparison workspace. | Route `/compare-scenarios` | navigation | Navigation/UI-toggle only; never business/trading/execution/order/broker/account/Gate mutation. |
| `qa.open.trade-planning` | Open Trade Planning | Navigates to the inert Trade Planning research workspace. | Route `/trade-plans` | navigation | Navigation/UI-toggle only; never business/trading/execution/order/broker/account/Gate mutation. |
| `qa.open.execution-research` | Open Execution Research | Navigates to the SIMULATED Execution Research workspace. | Route `/execution-research` | navigation | Navigation/UI-toggle only; never business/trading/execution/order/broker/account/Gate mutation. |
| `qa.open.portfolio-research` | Open Portfolio Research | Navigates to the Portfolio Research workspace. | Route `/portfolio-research` | navigation | Navigation/UI-toggle only; never business/trading/execution/order/broker/account/Gate mutation. |
| `qa.open.journal` | Open Research Journal | Navigates to the Research Journal workspace. | Route `/journal` | navigation | Navigation/UI-toggle only; never business/trading/execution/order/broker/account/Gate mutation. |
| `qa.open.research-management` | Open Research Management | Navigates to collections/tags workspace. | Route `/research-management` | navigation | Navigation/UI-toggle only; never business/trading/execution/order/broker/account/Gate mutation. |
| `qa.open.workspace-settings` | Open Workspace Settings | Navigates to presentation preferences. | Route `/workspace` | navigation | Navigation/UI-toggle only; never business/trading/execution/order/broker/account/Gate mutation. |
| `qa.open.previous-workspace` | Return to Previous Workspace | Navigates to the prior workspace route if stored as a route id. | Existing route from in-memory/history state | navigation | Navigation/UI-toggle only; never business/trading/execution/order/broker/account/Gate mutation. |
| `qa.open.recent-workspace` | Open Recent Workspace | Opens a recent registered workspace selected from route ids. | Existing registered route | navigation | Navigation/UI-toggle only; never business/trading/execution/order/broker/account/Gate mutation. |
| `qa.toggle.navigation-dock` | Toggle Navigation Dock | Collapses or expands Region B. | Region B shell state | ui-toggle | Navigation/UI-toggle only; never business/trading/execution/order/broker/account/Gate mutation. |
| `qa.toggle.context-panel` | Toggle Context Panel | Shows/collapses Region D through existing panel layout state. | Region D shell state | ui-toggle | Navigation/UI-toggle only; never business/trading/execution/order/broker/account/Gate mutation. |
| `qa.toggle.activity-dock` | Toggle Activity Dock | Shows/collapses Region E through existing panel layout state. | Region E shell state | ui-toggle | Navigation/UI-toggle only; never business/trading/execution/order/broker/account/Gate mutation. |
| `qa.toggle.theme` | Toggle Institutional Theme | Switches dark/light institutional theme mode. | Existing theme state | ui-toggle | Navigation/UI-toggle only; never business/trading/execution/order/broker/account/Gate mutation. |
| `qa.open.global-search` | Open Global Search | Opens the UI-002 global search overlay/mode. | Region F search overlay | ui-toggle | Navigation/UI-toggle only; never business/trading/execution/order/broker/account/Gate mutation. |
| `qa.clear.search-query` | Clear Search Query | Clears the local search input text. | Local search component state | ui-toggle | Navigation/UI-toggle only; never business/trading/execution/order/broker/account/Gate mutation. |
| `qa.open.shell-status` | Open Shell Status Dialog | Opens a shell status dialog showing Gate CLOSED / research-only framing. | Existing global dialog layer | ui-toggle | Navigation/UI-toggle only; never business/trading/execution/order/broker/account/Gate mutation. |
| `qa.show.governance-notification` | Show Governance Status | Displays a non-persistent notification that Gate remains CLOSED. | Existing notification layer | ui-toggle | Navigation/UI-toggle only; never business/trading/execution/order/broker/account/Gate mutation. |
| `qa.focus.navigation` | Focus Navigation Dock | Moves keyboard focus to Region B. | Region B | ui-toggle | Navigation/UI-toggle only; never business/trading/execution/order/broker/account/Gate mutation. |
| `qa.focus.workspace` | Focus Primary Workspace | Moves keyboard focus to Region C. | Region C | ui-toggle | Navigation/UI-toggle only; never business/trading/execution/order/broker/account/Gate mutation. |
| `qa.focus.context` | Focus Context Panel | Moves keyboard focus to Region D. | Region D | ui-toggle | Navigation/UI-toggle only; never business/trading/execution/order/broker/account/Gate mutation. |
| `qa.focus.activity` | Focus Activity Dock | Moves keyboard focus to Region E. | Region E | ui-toggle | Navigation/UI-toggle only; never business/trading/execution/order/broker/account/Gate mutation. |

Rejected action classes at plan stage:

```text
place order
execute trade
connect broker
open Governance Gate
approve certification
change account
allocate capital
size position
modify signal state
generate scenario
run simulation
create artifact
mutate journal/plan/tag/collection
call external AI/LLM
load plugin
```

The words `execution` and `trade` may appear only as approved research workspace names such as `Execution Research` and `Trade Planning`; they shall not appear as actuation verbs.

---

## 9. Accessibility Plan

Accessibility is a primary UI-002 requirement, not a final polish task.

### 9.1 Global search accessibility

Global search shall provide:

- keyboard-open path from Region A and command palette;
- focus moves to search input on open;
- Escape closes and restores focus;
- results navigable by ArrowUp/ArrowDown, Home/End, Enter, and Tab;
- `role="dialog"` or accessible combobox/listbox pattern as appropriate;
- accessible label for search input;
- result count announcement via `aria-live="polite"`;
- result type text labels, not color alone;
- clear no-results message;
- loading state announcement;
- error state with recovery guidance;
- reduced-motion behavior for overlay transitions.

### 9.2 Breadcrumb accessibility

Breadcrumbs shall provide:

- `<nav aria-label="Breadcrumb">`;
- ordered list semantics where practical;
- `aria-current="page"` on the current crumb;
- visible focus for navigable crumbs;
- meaningful labels for truncated artifact ids;
- screen-reader labels that include workflow stage and workspace.

### 9.3 Workspace switcher accessibility

Workspace switcher shall provide:

- keyboard activation from Region A;
- listbox/menu semantics;
- roving active item or native button list behavior;
- type-ahead where practical;
- visible focus;
- active workspace announcement;
- RBAC-filtered visible entries only;
- Escape closes and restores focus.

### 9.4 Command palette accessibility

Command palette extension shall provide:

- one global palette only;
- command count/group announcement;
- `navigation` versus `ui-toggle` text in result rows;
- disabled/rejected action classes never rendered;
- Escape and focus return;
- keyboard selection and scroll visibility;
- no mouse-only command path.

### 9.5 Context-aware navigation accessibility

Context navigation shall provide:

- accessible heading indicating suggestions are navigation only;
- clear relationship labels such as `Next workflow step`, `Related research workspace`, or `Return to previous workspace`;
- no color-only relationship encoding;
- keyboard-selectable links/buttons;
- no auto-navigation.

### 9.6 Accessibility evidence

Each implementation phase shall include named tests and browser evidence for:

- keyboard-only operation;
- focus management;
- ARIA labels/landmarks;
- screen-reader visible text for result types/statuses;
- reduced-motion compatibility;
- no color-only status meaning.

---

## 10. Phase Decomposition and Build-Order Strategy

Implementation shall proceed only after ITRGA accepts this design plan and issues a controlled Build Order. No later phase may begin until ITRGA accepts the prior slice or explicitly authorizes parallel work.

### UI-002-P01 — Workflow Metadata, Breadcrumb Foundation, and Registry Reconciliation

Objective: establish the workflow navigation model without altering UI-001 responsibilities.

Scope:

- companion workflow metadata keyed by UI-001 workspace ids;
- metadata validation utilities;
- deterministic breadcrumb model;
- `BreadcrumbTrail` rendered in Region A;
- no new routes;
- no backend/API/schema/dependency change.

Named test anchors:

```text
test_ui002_workflow_metadata_extends_ui001_registry_without_duplication
test_ui002_workflow_metadata_references_only_registered_workspaces
test_ui002_breadcrumbs_are_route_registry_derived_and_deterministic
test_ui002_breadcrumbs_are_accessible_and_keyboard_navigable
test_ui002_no_independent_navigation_or_competing_layout
test_ui002_workflow_navigation_contains_no_execution_or_actuation_controls
```

Evidence anchors:

- source diff limited to frontend/docs;
- browser shots for breadcrumbs on representative routes;
- no duplicate navigation/header proof;
- full frontend tests and no-actuation grep;
- backend regression unchanged/head unchanged.

### UI-002-P02 — Workspace Switcher and Context-Navigation Seam

Objective: allow operators to switch registered workspaces by workflow while preserving UI-001 shell ownership.

Scope:

- `WorkspaceSwitcher` in Region A;
- previous/recent workspace route ids, if implemented, stored through existing shell preference seam only;
- static context-navigation map rendered through existing Context Panel/PanelHost;
- keyboard support and focus restoration;
- no persisted search queries or artifact payloads.

Named test anchors:

```text
test_ui002_workspace_switcher_uses_registry_and_rbac_visible_entries
test_ui002_workspace_switcher_preserves_single_ui001_shell_frame
test_ui002_context_navigation_suggests_read_only_registered_routes_only
test_ui002_workspace_switching_is_keyboard_operable
test_ui002_navigation_recents_do_not_persist_search_queries_or_business_payloads
test_ui002_context_navigation_contains_no_business_actions
```

Evidence anchors:

- browser shots of workspace switcher;
- keyboard-only switching evidence;
- context panel related-workflow evidence;
- preference payload proof if recents are persisted;
- no backend/schema/dependency diff.

### UI-002-P03 — Command Palette Extension and Quick-Action Catalogue

Objective: extend the existing command palette with approved workflow navigation and UI-toggle quick actions only.

Scope:

- typed `CommandRegistry`;
- quick-action catalogue implementation using only ITRGA-vetted items;
- existing `CommandPalette` consumes registry;
- command grouping by workflow stage;
- no second command palette;
- rejection tests for prohibited command classes.

Named test anchors:

```text
test_ui002_command_palette_extends_existing_palette_not_second_palette
test_ui002_command_registry_accepts_only_navigation_or_ui_toggle_commands
test_ui002_quick_action_catalogue_is_itemized_and_registered
test_ui002_quick_actions_are_navigation_or_ui_toggle_only
test_ui002_command_registry_rejects_business_trading_execution_broker_account_gate_actions
test_ui002_command_palette_keyboard_focus_and_escape_restore
```

Evidence anchors:

- command palette browser shots with quick actions;
- source grep for second palette/overlay absence;
- no command action types beyond navigation/UI-toggle;
- no actuation phrase evidence;
- full frontend and backend regression.

### UI-002-P04 — Global Search Framework, Read-Only Source Adapters, and Search Overlay

Objective: provide global search over registered workspaces and existing read-only artifacts without backend expansion.

Scope:

- `GlobalSearchResult` model;
- first-party search ranking/index utility;
- search source adapters for registry and selected existing read APIs;
- Region-F global search overlay/search mode;
- keyboard and screen-reader behavior;
- read-only jump-to navigation results;
- no new search endpoint, table, dependency, or mutation.

Named test anchors:

```text
test_ui002_global_search_returns_read_only_navigation_results
test_ui002_global_search_uses_workspace_registry_and_existing_read_sources
test_ui002_global_search_never_registers_mutation_or_actuation_results
test_ui002_global_search_does_not_persist_query_text_or_artifact_payloads
test_ui002_global_search_accessibility_keyboard_and_result_announcement
test_ui002_global_search_adds_no_backend_schema_or_dependency_change
```

Evidence anchors:

- browser search proof for workspace + at least three artifact classes available in the target data;
- no result action except navigation;
- no network mutation proof for search interaction;
- TypeScript/build/full suite;
- backend head unchanged.

### UI-002-P05 — Context-Aware Workflow Integration and UI-002 Completion Checkpoint

Objective: integrate workflow navigation, breadcrumbs, switcher, command palette, context navigation, and search into a cohesive UI-002 completion package.

Scope:

- cross-route context-aware navigation consistency;
- search/palette/breadcrumb coordination;
- responsive behavior hardening;
- operator browser evidence across representative workflow progression;
- UI-002 documentation and evidence pack;
- completion regression.

Named test anchors:

```text
test_ui002_context_aware_navigation_preserves_workflow_without_business_logic
test_ui002_all_routes_keep_single_ui001_shell_navigation_system
test_ui002_workflow_navigation_full_surface_contains_no_actuation_controls
test_ui002_breadcrumbs_search_palette_and_switcher_remain_registry_consistent
test_ui002_completion_checkpoint_preserves_gate_closed_and_research_only_status
test_ui002_completion_checkpoint_frontend_routes_mount_in_shell_without_regression
```

Evidence anchors:

- route-by-route served browser screenshots;
- keyboard-only workflow walkthrough;
- responsive screenshots;
- full frontend suite;
- full backend suite;
- networked local CI;
- Alembic current proof;
- UI-only diff proof;
- no-actuation source and browser proof.

---

## 11. Regression and Evidence Strategy

### 11.1 Baseline to preserve

```text
Platform: v0.62.0
Alembic head: 20260717_0037
Backend baseline: 414 passed
Frontend baseline: 26 files / 97 tests
Governance Gate: CLOSED
Production deployment: NOT CERTIFIED
```

### 11.2 Mandatory validation categories per phase

Each UI-002 Build Order shall provide:

- named frontend tests displayed passing;
- relevant component/unit tests;
- full frontend suite;
- TypeScript check;
- production frontend build;
- npm audit result;
- backend Ruff;
- backend targeted regression where relevant;
- backend full suite unless ITRGA accepts a narrowed UI-only exception;
- `alembic current` showing `20260717_0037 (head)`;
- no backend/API/schema/dependency drift proof;
- no-actuation source grep;
- route/browser evidence from served app;
- Git Bash local CI with exit-code sentinel.

### 11.3 Operator evidence commands — Windows PowerShell pattern

Representative CI invocation:

```powershell
& "C:\Program Files\Git\bin\bash.exe" scripts/local_ci.sh | Tee-Object docs\evidence\UI-002-PXX_LOCAL_CI.txt
Write-Host "LOCAL_CI_EXIT_CODE:" $LASTEXITCODE
```

Representative head proof:

```powershell
cd backend
alembic current
cd ..
```

Representative UI-only diff proof:

```powershell
git diff -- backend\app backend\alembic backend\pyproject.toml backend\requirements.txt frontend\package.json frontend\package-lock.json
Write-Host "Expected: no backend/schema/package-manifest diff unless specifically authorized."
```

Representative no-actuation grep, with known research-label caution:

```powershell
Get-ChildItem frontend\src\workstation -Recurse -File -Include *.ts,*.tsx |
  Select-String -Pattern 'place order|submit order|connect broker|open gate|gate open|real account|real pnl|real p&l|margin account|live execution|execute trade'

Write-Host "Expected: no output. Approved labels such as Execution Research are research workspace names, not actuation controls."
```

### 11.4 Browser evidence matrix

| Evidence item | Required proof |
|---|---|
| Workflow navigation | Operator can traverse Observe → Detect → Investigate → Analyze → Compare → Plan → Document/Review using registry-driven shell navigation. |
| Breadcrumbs | Representative routes show deterministic breadcrumbs inside UI-001 Region A. |
| Workspace switching | Switcher opens, lists RBAC-visible registered workspaces, keyboard selects route. |
| Context-aware navigation | Related workflow suggestions appear in existing context panel and navigate only to registered routes. |
| Command palette | Existing palette shows approved quick actions only; all commands are `navigation` or `ui-toggle`. |
| Global search | Search returns workspace and artifact results; selecting result navigates only. |
| Accessibility | Keyboard-only operation, focus return, labels, result counts, no color-only meaning. |
| No duplication | No second sidebar, second command palette, second overlay, or page-specific global header. |
| No actuation | No execution/order/broker/account/Gate controls or commands. |
| Gate and production status | Gate remains CLOSED; production remains not certified. |

### 11.5 CI and audit handling

If `npm audit` cannot reach the registry due offline network conditions, the result shall be disclosed under `TD-W6-CI-AUDIT`; the evidence package shall not relabel a red CI/audit result as green. Operator waiver may be requested only if the operator explicitly authorizes it.

---

## 12. Constitutional Attestation

UI-002, as designed here:

- is presentation/navigation integration only;
- extends UI-001 rather than duplicating it;
- keeps UI-001 as the sole application shell;
- keeps the Workspace Registry as the authoritative workspace catalogue;
- keeps the Navigation Dock as the single global navigation surface;
- keeps the existing Command Palette as the single global palette;
- keeps Region F as the single overlay family;
- uses existing read APIs for global search;
- does not add a backend search index by default;
- does not add a database table or migration;
- does not add a dependency by default;
- does not create business/trading/execution/order/broker/account/Gate actions;
- does not introduce external AI/LLM or dynamic plugin execution;
- does not open the Governance Gate;
- does not certify production deployment.

DA does not self-approve this plan and does not begin implementation. Implementation awaits ITRGA design acceptance and a controlled Build Order.

---

## 13. Risks, Mitigations, and Open Questions

### 13.1 Risks and mitigations

| Risk | Severity | Mitigation |
|---|---:|---|
| Workflow metadata drifts from UI-001 registry | High | Validate every metadata entry against `WORKSPACE_REGISTRY`; fail tests on orphan ids. |
| Global search becomes a hidden action surface | Critical | Result model is read-only navigation only; tests reject mutation/action commands and disallowed verbs. |
| Command palette becomes a business-command palette | Critical | Preserve `commandType: "navigation" | "ui-toggle"`; itemized quick-action catalogue; rejection tests. |
| Context-aware navigation reads as recommendation/advice | High | Label suggestions as workflow navigation only; no business ranking or advisory language. |
| Search data volume affects responsiveness | Medium | Debounce, cap results, memory TTL, source opt-in, no heavy report generation per keystroke. |
| Deep links are not available for some artifacts | Medium | Navigate to owning workspace and optionally focus/highlight using local UI state only. |
| Search queries leak sensitive operator intent | Medium | Do not persist search query text; avoid logging query text. |
| Visual duplication with UI-001 nav/palette | High | Extend existing components; source grep/tests for duplicate global palette/nav. |
| Accessibility regressions | High | Build accessibility tests into every phase; keyboard-first browser evidence. |
| Backend search-index temptation | Medium | Default frontend-only; any backend index requires separate ITRGA persistence/endpoint review. |

### 13.2 Assumptions

- UI-001 baseline remains the permanent application shell.
- Existing read APIs remain sufficient for first-pass global search source adapters.
- Search source scope may be phased according to data availability and performance constraints.
- UI-002 may add frontend-only metadata and presentation components after Build Order authorization.
- No dependency addition is necessary for initial deterministic matching/ranking.

### 13.3 Open questions for ITRGA

1. Does ITRGA accept the companion workflow metadata model keyed by `workspace.id` as the preferred way to extend UI-001 without modifying the 14-field Workspace Registration Contract?
2. Should UI-002-P04 include all listed artifact source adapters in the first global-search slice, or should ITRGA limit P04 to workspace + signals + journal + research collections first?
3. Are recent workspace ids acceptable for persistence in the existing `operator_workspace_preferences.layout_config`, provided search queries and artifact payloads are never persisted?
4. Should global search and command palette remain visually separate overlays inside Region F, or should the existing command palette become a tabbed command/search overlay? Either approach must preserve one overlay infrastructure and one command system.

---

## 14. Recommended First Build Order

If ITRGA accepts this plan, the DA recommends the first Build Order be limited to:

```text
UI-002-P01 — Workflow Metadata, Breadcrumb Foundation, and Registry Reconciliation
```

Rationale:

- it proves UI-002 can extend UI-001 without duplicating navigation;
- it introduces deterministic workflow orientation before search/palette complexity;
- it is frontend-only and low risk;
- it creates the metadata foundation needed for later switcher/search/context-aware navigation;
- it produces clear evidence for the “extend, do not modify UI-001 responsibilities” requirement.

P01 shall not implement global search, command quick actions, or workspace switching beyond what is necessary to prove breadcrumb/workflow metadata integrity.

---

## 15. DA Disposition

The DA submits this UI-002 Engineering Design Plan for ITRGA review.

DA does not self-approve the plan, does not authorize `BUILD_ORDER_UI-002-P01`, does not begin UI-002 implementation, does not modify backend/API/schema/governance/ML behavior, and does not expand platform capability.

The Governance Gate remains CLOSED. Production deployment remains NOT CERTIFIED.

---

**End of UI-002_ENGINEERING_DESIGN_PLAN.md**
