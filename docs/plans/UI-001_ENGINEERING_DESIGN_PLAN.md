# UI-001 Engineering Design Plan — Institutional Workspace Shell

| Field | Value |
|---|---|
| Programme | Institutional UI Transformation |
| Workstream | UI-001 — Institutional Workspace Shell |
| Document type | Engineering Design Plan; pre-Build-Order; no implementation authorization |
| Development Authority | AXIOM DA |
| ITRGA request | `docs/build-orders/ITRGA_REQUEST_UI-001_DESIGN_PLAN.md` |
| Platform baseline | v0.62.0 |
| Alembic head | `20260717_0037` |
| Baseline validation | backend 413 passed · frontend 21 files / 67 tests |
| Governance Gate | CLOSED |
| Production status | Not certified; governed by `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md` |
| Governing UI docs | `12_INSTITUTIONAL_UI_TRANSFORMATION_PLAN.md` → `13_UI_TRANSFORMATION_MASTER_PLAN.md` → `14_UI-001_TECHNICAL_DESIGN_SPECIFICATION.md` → `15_UI-001_IMPLEMENTATION_SPECIFICATION.md` |

---

## 0. Executive Summary

This design plan defines how UI-001 shall establish the permanent AXIOM Institutional Workspace Shell without expanding backend capability, platform scope, trading functionality, research algorithms, governance behavior, API contracts, ML workflows, or database schema.

UI-001 is presentation infrastructure. It shall transform the current page-oriented terminal into a unified institutional workstation shell composed of:

```text
Region A — Global Header
Region B — Navigation Dock
Region C — Primary Workspace
Region D — Context Panel
Region E — Activity Dock
Region F — Overlay Layer
```

The shell shall host existing approved AXIOM workspaces through a shared Workspace Registry, Workspace Host, Panel Infrastructure, Layout Manager, Routing Infrastructure, Session Coordination, and Design Token foundation.

The first implementation Build Order after design acceptance should be the smallest safe slice: **shell skeleton + A–F region scaffolding + workspace registry + route/state seam + no-regression proof**. That first slice should prove one integrated environment before deeper page migration or visual refinement.

This plan does **not** authorize implementation. It is submitted for ITRGA design review and binding refinements before a `BUILD_ORDER_UI-001` or equivalent may be issued.

---

## 1. Scope and Non-Scope Confirmation

### 1.1 In scope for UI-001

Mapped to Document 15 §2 and Document 14:

| In-scope area | Design intent |
|---|---|
| Institutional Workspace Shell | Permanent application frame for AXIOM v1.x. |
| Global Header | Platform identity, workspace title, search/command entry, status, operator controls. |
| Navigation Dock | Task-oriented, persistent, keyboard-accessible workflow navigation. |
| Primary Workspace | Main host for existing workspace pages/content. |
| Context Panel | Context-sensitive supporting information and metadata host. |
| Activity Dock | Collapsible operational/activity/status area. |
| Overlay Layer | Command palette, dialogs, search results, toasts, menus. |
| Workspace Registry | Canonical metadata mapping workspaces to routes, workflow groups, labels, and context descriptors. |
| Routing Infrastructure | Stable route-to-workspace adapter preserving current routes where possible. |
| State Ownership | Clear Shell vs Workspace vs Component state boundaries. |
| Panel Infrastructure | Resize/collapse/persist behavior for context and activity docks. |
| Layout Persistence | Reuse existing W7-U02 `operator_workspace_preferences` for shell layout where applicable. |
| Design Token Foundation | Institutional tokens and CSS variables for shell and shared components. |
| Accessibility Foundation | Keyboard navigation, focus management, landmarks, ARIA, color contrast. |
| Responsive Infrastructure | Large desktop, standard desktop, laptop, and tablet/adaptive behavior. |
| Performance Foundation | Stable layout, minimal route transition overhead, no heavy new dependencies. |

### 1.2 Explicit non-scope

UI-001 shall not implement or alter:

- new trading functionality;
- live execution capability;
- order, broker, account, position, balance, margin, capital, or real P&L capability;
- Governance Gate behavior;
- backend business logic;
- API contracts;
- database schema;
- ML workflows;
- market analysis algorithms;
- external LLM or external AI services;
- chart redesign beyond shell hosting;
- Institutional Intelligence redesign;
- research workspace redesign;
- governance workspace implementation;
- Navigator Assistant implementation;
- artifact explorer implementation;
- market workspace redesign;
- execution research redesign;
- visual refinement beyond foundational design-token integration;
- production deployment or production certification.

### 1.3 Constitutional bright line

UI-001 shall expose and organize existing capabilities. It shall not create new platform capability.

---

## 2. Region Architecture A–F

### 2.1 Shell hierarchy

Proposed component hierarchy:

```text
App
└── AuthProvider
    └── ProtectedRoute
        └── InstitutionalWorkspaceShell
            ├── GlobalHeader                 (Region A)
            ├── NavigationDock               (Region B)
            ├── WorkspaceHost                (Region C)
            ├── ContextPanelHost             (Region D)
            ├── ActivityDock                 (Region E)
            └── OverlayHost                  (Region F)
```

Supporting infrastructure:

```text
WorkspaceRegistry
WorkspaceRouteAdapter
WorkspaceLayoutProvider
WorkspaceSessionProvider
CommandPaletteProvider
NotificationProvider
DesignTokenProvider / CSS token layer
```

### 2.2 Region A — Global Header

Responsibilities:

- platform identity and version;
- active workspace title;
- high-level Governance Gate status (`CLOSED`);
- search/command palette entry point;
- system/connection status display;
- operator identity;
- sign-out/session controls.

Non-responsibilities:

- workspace-specific filters;
- trade/execution controls;
- backend business actions.

Evidence expectations:

- header visible on every protected route;
- no duplicate page headers replacing the global header;
- no execution/go-live/order controls;
- keyboard access to command palette.

### 2.3 Region B — Navigation Dock

Responsibilities:

- workflow-oriented navigation;
- persistent route access;
- group labels aligned to institutional workflow;
- collapsed/expanded states;
- keyboard navigation.

Initial workflow groups:

```text
Monitor
Research
Investigate
Compare
Plan
Review
Govern
Settings
```

Initial mapping of current routes:

| Workflow group | Existing route(s) |
|---|---|
| Monitor | `/`, `/live`, `/charts` |
| Research | `/signals`, `/analytics`, `/intelligence` |
| Investigate | `/investigate`, `/compare-scenarios` |
| Plan | `/trade-plans`, `/execution-research` |
| Review | `/portfolio-research`, `/journal`, `/research-management` |
| Govern | future UI-007; interim status in shell/context/activity only |
| Settings | `/workspace` |

### 2.4 Region C — Primary Workspace

Responsibilities:

- render existing workspace route content;
- provide a consistent workspace container;
- preserve existing page behavior;
- prevent independent page shell duplication.

Migration strategy:

- existing page components remain the primary content initially;
- route wrappers gradually provide standardized `WorkspaceHeader`, `WorkspaceToolbar`, and `WorkspaceContent` composition;
- no business logic migrates into the shell.

### 2.5 Region D — Context Panel

Responsibilities:

- display context-relevant metadata;
- display active workspace summary;
- display governance/research framing;
- reserve future hooks for lineage, related artifacts, validation, and audit references.

Initial UI-001 content should be conservative:

- workspace description from registry;
- current operator/session summary;
- platform/Gate status;
- active route metadata;
- placeholder empty state for future contextual panels.

It must not duplicate full workspace feature logic.

### 2.6 Region E — Activity Dock

Responsibilities:

- show activity/status stream placeholders;
- surface system health, recent alerts, or evidence status at shell level when available through existing APIs;
- support collapsed state, especially on laptop tier.

Initial UI-001 content:

- platform status summary;
- recent activity placeholder;
- no new backend telemetry path.

### 2.7 Region F — Overlay Layer

Responsibilities:

- command palette;
- global search overlay shell;
- dialogs and transient panels;
- toast/notification host.

Initial command palette may support only route/workspace navigation and shell commands:

```text
Open workspace
Toggle context panel
Toggle activity dock
Focus navigation
Focus primary workspace
Open settings
```

It shall not trigger business actions or execute backend mutations.

---

## 3. Migration Strategy

### 3.1 Principle

UI-001 shall follow: **incremental migration before wholesale replacement**.

The first implementation shall preserve the current route behavior while replacing the legacy `TerminalLayout` frame with the new institutional shell.

### 3.2 Current state

Current frontend structure uses:

```text
AuthProvider
ProtectedRoute
TerminalLayout
NavLink sidebar
Outlet page rendering
```

UI-001 should evolve this into:

```text
AuthProvider
ProtectedRoute
InstitutionalWorkspaceShell
WorkspaceHost
Existing pages as workspace content
```

### 3.3 Migration stages within UI-001

| Stage | Description | Regression control |
|---|---|---|
| Stage 1 | Introduce shell skeleton and workspace registry behind existing routes. | Existing page tests remain green. |
| Stage 2 | Replace legacy top nav/sidebar with Global Header + Navigation Dock. | Route navigation tests and screenshots. |
| Stage 3 | Add Context Panel + Activity Dock with minimal registry/status content. | No business logic changes. |
| Stage 4 | Add layout state and persistence using existing workspace preferences. | Mocked persistence tests and browser restore evidence. |
| Stage 5 | Add overlay host + command palette route navigation. | Keyboard and focus tests. |
| Stage 6 | Retire duplicate legacy layout styles where safe. | Visual regression/browser screenshots. |

### 3.4 Existing page mounting

Existing pages to be mounted without business regression:

```text
Operations Dashboard
Live Market
Advisory Signals
Performance Analytics
Institutional Intelligence
Signal Investigation
Scenario Comparison
Trade Planning
Research Journal
Execution Research
Portfolio Research
Research Management
Workspace Customization
Chart Workspace
```

Each current route should continue to resolve. If route aliases are changed, redirects or compatibility routes must be documented and tested.

---

## 4. State Ownership and Routing Model

### 4.1 State ownership

| Owner | Owns | Must not own |
|---|---|---|
| Shell | navigation, layout, panel state, routing metadata, auth/session display, notifications, theme, command palette visibility | business/research data mutation, report computation, signal logic, ML state |
| Workspace | filters, selected artifact, local loading/error state, page-specific API calls, workspace-specific forms | global routing, auth, shared panel lifecycle, design tokens |
| Component | local visual state, hover/focus, temporary expansion, input presentation | global navigation, operator session, persistent shell layout |

### 4.2 Workspace Registry

Proposed shape:

```ts
type WorkspaceDefinition = {
  id: string;
  route: string;
  label: string;
  group: WorkflowGroup;
  description: string;
  component: React.ComponentType;
  context?: WorkspaceContextDefinition;
  activity?: WorkspaceActivityDefinition;
  requiresAuth: true;
  noActuation: true;
};
```

Registry rules:

- all protected workspaces must appear in the registry;
- no page-specific sidebar entries outside the registry;
- registry labels drive Navigation Dock and command palette;
- registry may include governance metadata but no business logic.

### 4.3 Routing model

Routes remain React Router based. The Shell hosts `Outlet` or a registry-driven workspace renderer.

Proposed approach for first Build Order:

- keep existing route paths;
- define registry metadata for each path;
- `WorkspaceHost` determines active workspace by route match;
- existing pages are wrapped in `WorkspaceFrame` where needed;
- not-found behavior remains safe and informative.

### 4.4 Layout persistence model

State to persist:

```text
active workspace id
navigation dock collapsed/expanded
context panel visible/hidden
context panel width
activity dock visible/hidden
activity dock height
theme mode
```

Initial non-persisted fallback:

```text
local default layout constants
```

Authenticated persistence:

- reuse `operator_workspace_preferences` table;
- use a dedicated workspace key such as `institutional-shell-v1`;
- store shell layout in `layout_config`;
- store theme in `theme_config`;
- store visible shell regions in `visible_modules` only if compatible with W7-U02 allowlist, otherwise in `layout_config.region_visibility`;
- store non-sensitive metadata only.

No new table is planned.

---

## 5. Persistence Plan

### 5.1 Preferred path

UI-001 shall reuse existing W7-U02 persistence:

```text
operator_workspace_preferences
```

No new Alembic migration is planned.

Alembic head should remain:

```text
20260717_0037
```

### 5.2 Persistence payload contract

Example shell preference payload:

```json
{
  "workspace_key": "institutional-shell-v1",
  "layout_config": {
    "active_workspace": "monitor.operations",
    "navigation": { "collapsed": false },
    "context_panel": { "visible": true, "width": 320 },
    "activity_dock": { "visible": true, "height": 220 },
    "last_route": "/"
  },
  "visible_modules": ["operations", "chart_workspace", "institutional_intelligence"],
  "theme_config": { "mode": "dark", "density": "standard" },
  "metadata": { "ui_workstream": "UI-001", "version": "shell-v1" }
}
```

Validation is already provided by W7-U02 for forbidden fields and secret markers.

### 5.3 If a new table is later proposed

A new table is **not recommended** for UI-001. If ITRGA or a later Build Order authorizes one, the plan must include:

- Alembic revision from `20260717_0037`;
- raw PostgreSQL SELECT evidence;
- no-orphan audit join;
- operator FK no-orphan join;
- forbidden column proof;
- no-secret/PII checks.

---

## 6. Design System and Token Plan

### 6.1 Token categories

UI-001 shall establish or normalize tokens for:

```text
colors
semantic colors
typography
spacing
sizing
borders
radius
elevation
focus rings
breakpoints
motion/reduced motion
```

### 6.2 Semantic color mapping

| Semantic role | Meaning |
|---|---|
| Green | positive/healthy/success state |
| Red | adverse/error state |
| Blue | information/primary focus |
| Amber | attention/warning |
| Purple | AI / institutional intelligence |
| Gray | neutral/system metadata |

Color shall not be the only state indicator. Badges, text, icons, and ARIA labels must provide meaning.

### 6.3 Typography hierarchy

| Level | Use |
|---|---|
| L1 | Workspace title |
| L2 | Section heading |
| L3 | Panel heading |
| L4 | Body text |
| L5 | Metadata/caption |

### 6.4 Proposed files

```text
frontend/src/workstation/design/tokens.css
frontend/src/workstation/design/theme.ts
frontend/src/workstation/components/*
```

If the first Build Order is intentionally minimal, tokens may initially extend `frontend/src/styles/global.css`, but the design should move toward a dedicated workstation token layer.

---

## 7. Accessibility and Keyboard Plan

### 7.1 Mandatory keyboard paths

UI-001 shall provide keyboard access for:

- navigation dock traversal;
- workspace route selection;
- command palette open/close;
- command search input;
- command selection with arrow keys and Enter;
- panel toggles;
- sign-out/menu controls;
- focus transition between shell regions.

Suggested shortcuts:

```text
Ctrl/Cmd + K -> command palette
Esc -> close overlay / command palette
Alt + 1..9 -> workspace shortcuts where safe
Alt + [ / ] -> focus navigation / context panel
```

Shortcuts must not conflict with browser-critical shortcuts where avoidable.

### 7.2 ARIA landmarks

Proposed landmarks:

```text
<header aria-label="Global command bar">
<nav aria-label="Institutional workflow navigation">
<main aria-label="Primary workspace">
<aside aria-label="Context panel">
<section aria-label="Activity dock">
<div role="dialog" aria-label="Command palette">
```

### 7.3 Focus management

- focus enters command palette input on open;
- focus returns to trigger on close;
- route changes move focus to workspace heading or main region;
- collapsed panels remain discoverable by keyboard;
- visible focus rings comply with contrast requirements.

### 7.4 Accessibility evidence

Evidence plan:

- Vitest/Testing Library checks for landmarks and labels;
- keyboard interaction tests for command palette and navigation;
- browser screenshots of focus states;
- contrast check based on token values;
- no mouse-only path for primary shell navigation.

---

## 8. Responsive and Performance Plan

### 8.1 Responsive tiers

| Tier | Behavior |
|---|---|
| Large desktop | Navigation dock, primary workspace, context panel, and activity dock visible. |
| Standard desktop | Context panel remains visible but narrower; activity dock collapsible. |
| Laptop | Activity dock collapsed by default; context panel can collapse. |
| Tablet / narrow | Navigation collapses to icon/drawer; context panel becomes slide-over; activity dock hidden/collapsed. |

The shell must preserve workflow continuity during adaptation.

### 8.2 Performance budget

Initial budget proposal:

- no new UI/state/layout dependency in first Build Order;
- production build must remain successful;
- bundle size increase should be explicitly reported;
- route transitions should not remount global shell;
- shell state updates should not trigger full workspace data reload;
- context/activity panels should lazy-render heavy content in later workstreams.

### 8.3 Performance evidence

Evidence plan:

- `npm run build` output and bundle size comparison;
- smoke timing/observational evidence for route transitions;
- no infinite render loops in tests;
- no additional network requests for shell-only navigation except authorized preference persistence.

---

## 9. Unit Decomposition

UI-001 should be decomposed into controlled Build Orders. The exact Build Order naming remains for ITRGA/operator authorization, but the recommended decomposition is:

### UI-001-P01 — Shell Skeleton, Registry, and Region Scaffolding

Objective: prove the frame before migrating feature-specific presentation.

Scope:

- `InstitutionalWorkspaceShell` skeleton;
- Regions A–F rendered;
- `WorkspaceRegistry` for all current routes;
- `WorkspaceHost` mounting existing pages;
- initial design tokens;
- no duplicate header/sidebar after shell mount;
- no business/API/schema changes;
- no-regression frontend tests.

Evidence:

- shell region tests;
- route registry tests;
- protected-route/logged-out block;
- no actuation controls;
- browser screenshots of all six regions.

### UI-001-P02 — Navigation Dock and Workflow Routing

Scope:

- workflow navigation groups;
- active route highlighting;
- keyboard traversal;
- workspace titles/breadcrumb basics;
- command palette route navigation skeleton.

### UI-001-P03 — Panel Infrastructure and Layout Manager

Scope:

- context panel collapse/resize;
- activity dock collapse/resize;
- layout state model;
- responsive state behavior;
- local default state.

### UI-001-P04 — Workspace Persistence via Existing Preferences

Scope:

- use `operator_workspace_preferences` for shell layout;
- restore layout after login;
- safe fallback on missing preference;
- no new table.

### UI-001-P05 — Overlay, Notifications, and Shell Accessibility Hardening

Scope:

- command palette accessibility completion;
- overlay focus traps;
- toast/notification host;
- focus restoration;
- ARIA and keyboard hardening.

### UI-001-P06 — Legacy Layout Retirement and Migration Completion

Scope:

- remove/retire legacy `TerminalLayout` structure where replaced;
- ensure every current page is hosted by the institutional shell;
- final UI-001 browser/regression package;
- documentation and component registry snapshot.

### Dependency rule

No later phase should begin until ITRGA accepts the preceding foundational slice or explicitly authorizes parallel work.

---

## 10. Dependency Declaration

### 10.1 Planned dependencies

No new dependency is planned for the first UI-001 implementation slice.

Existing frontend dependencies remain:

```text
react
react-dom
react-router-dom
lightweight-charts
vite/vitest/testing-library/typescript
```

### 10.2 Barred dependencies

UI-001 shall not add:

- broker SDK;
- external AI/LLM package;
- dynamic plugin runtime;
- unspiked layout/docking library;
- unspiked command palette library;
- unspiked state-management library.

Any proposed dependency must include compatibility/security/no-leak review and ITRGA note before use.

### 10.3 Backend/schema/API declaration

No backend business logic change, API contract change, schema migration, governance behavior change, ML workflow change, or database table is planned for UI-001 design.

---

## 11. Regression and Evidence Plan

### 11.1 Regression baseline

Starting baseline:

```text
Backend: 413 passed
Frontend: 21 files / 67 tests
Alembic: 20260717_0037
Platform: v0.62.0
Gate: CLOSED
```

Every UI-001 Build Order must report actual totals.

### 11.2 Test categories

Frontend tests:

- shell renders Regions A–F;
- all existing workspaces are present in registry;
- current routes mount existing content;
- navigation is workflow-oriented and active state works;
- command palette opens/closes and navigates by keyboard;
- context/activity panels toggle and preserve state;
- logged-out route redirects to login;
- no execution/order/broker/account controls in shell;
- accessibility landmarks exist.

Backend tests:

- full backend regression remains green;
- Gate CLOSED tests remain green;
- broker integration suite remains green.

Static checks:

- no backend/schema/API files changed unless explicitly authorized;
- no new dependency unless authorized;
- no forbidden UI control strings in shell.

### 11.3 Browser evidence matrix

Operator-run screenshots should include:

| Evidence | Required proof |
|---|---|
| Full shell desktop | Regions A–F visible. |
| Navigation dock | Workflow groups visible; active workspace highlighted. |
| Existing page hosted | At least Operations and one research workspace mounted inside shell. |
| Context panel | Context/metadata region visible and collapsible. |
| Activity dock | Dock visible/collapsible; laptop default collapsed evidence in responsive proof. |
| Command palette | Keyboard-opened overlay with workspace commands. |
| Responsive tiers | Large desktop, standard/laptop, narrow/tablet-like adaptation. |
| Layout persistence | Change panel state, reload/relogin, state restored. |
| No actuation | No execution/order/broker/account/go-live controls. |
| Logged-out block | Protected workspace redirects/blocks unauthenticated operator. |

### 11.4 CI evidence

Required:

```powershell
& "C:\Program Files\Git\bin\bash.exe" scripts/local_ci.sh
Write-Host "LOCAL_CI_EXIT_CODE:" $LASTEXITCODE
```

If offline `npm audit` recurs, disclose under `TD-W6-CI-AUDIT`; do not relabel red CI as green.

---

## 12. Risk Assessment

| Risk | Severity | Mitigation |
|---|---:|---|
| Shell becomes a new feature layer instead of presentation infrastructure | Critical | No business logic in shell; static/diff proof; route-host only. |
| Duplicate navigation/header patterns persist | High | Retire `TerminalLayout` frame once shell accepted; registry-only navigation. |
| Existing pages regress during migration | High | Mount existing pages first; full frontend regression and browser evidence. |
| Layout persistence introduces schema creep | Medium | Reuse `operator_workspace_preferences`; no new table. |
| Command palette becomes action surface | Critical | Navigation/shell commands only; no backend mutation commands. |
| Accessibility deferred | High | Keyboard/ARIA/focus tests in first slice. |
| Heavy layout dependency bloats bundle | Medium | No new dependency in first slice; dependency spike if proposed. |
| Responsive collapse hides critical content | Medium | Browser evidence at responsive tiers; explicit restore controls. |
| Governance/Gate status disappears from UX | High | Global Header/Context Panel display Gate CLOSED/research-only framing. |

---

## 13. Proposed Build Order Readiness

This design plan recommends the first implementation Build Order be limited to:

```text
UI-001-P01 — Institutional Workspace Shell Skeleton, Workspace Registry, Region Scaffolding, and Routing/State Seam
```

Acceptance goals for P01:

- shell renders Regions A–F;
- all existing pages mount inside Primary Workspace without regression;
- route registry is canonical;
- no duplicate global frame;
- no backend/API/schema/governance/ML change;
- no actuation controls;
- accessibility landmarks and keyboard basics present;
- browser evidence proves the frame.

The P01 Build Order should not yet attempt full layout persistence, full command palette, or full visual refinement beyond foundational tokens.

---

## 14. DA Disposition

The DA submits this UI-001 Engineering Design Plan for ITRGA review.

DA does not self-approve this plan, does not begin UI-001 implementation, does not authorize a Build Order, does not alter backend/API/schema/governance/ML behavior, and does not expand platform scope.

Implementation awaits ITRGA review and a subsequent operator-authorized Build Order.

---

**End of UI-001_ENGINEERING_DESIGN_PLAN.md**
