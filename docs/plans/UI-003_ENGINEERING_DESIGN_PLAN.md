# UI-003 Engineering Design Plan — Professional Market Workspace

| Field | Value |
|---|---|
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-003 — Professional Market Workspace |
| Document type | Engineering Design Plan; pre-Build-Order; no implementation authorization |
| Development Authority | AXIOM DA |
| ITRGA request | `docs/build-orders/ITRGA_REQUEST_UI-003_DESIGN_PLAN.md` |
| Predecessor milestones | UI-001 COMPLETE · UI-002 COMPLETE |
| Platform baseline | v0.62.0 |
| Alembic head | `20260717_0037` |
| Baseline validation | backend 414 passed · frontend 31 files / 127 tests |
| Governance Gate | CLOSED |
| Production status | Not certified; governed separately by `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md` |
| Governing UI docs | `12_INSTITUTIONAL_UI_TRANSFORMATION_PLAN.md` → `13_UI_TRANSFORMATION_MASTER_PLAN.md` → UI-001 shell and implementation specifications |

---

## 0. Executive Summary

UI-003 shall transform AXIOM market observation into a professional institutional market workspace while preserving the constitutional bright line that **professional presentation is not new analysis**.

Per Document 12 §5, UI-003 scope is:

```text
Professional chart workspace
Market overview
Watchlists
Chart overlays
Annotation integration
Research markers
Market status
Layout improvements
```

Expected outcome:

> Charts become the operational centre of AXIOM.

This plan proposes a presentation-only transformation over existing governed market/chart/annotation/signal/readiness data. It does **not** introduce live/real market data, a broker/feed, client-side inference, authoritative recomputation, new analytical algorithms, execution controls, order tickets, real account state, or Governance Gate changes.

Recommended persistence posture: **reuse existing `operator_workspace_preferences`** for watchlists as operator-scoped symbol preferences. No new table is proposed for UI-003. Watchlists shall store **symbol identifiers / market display preferences only** — no quantities, positions, orders, accounts, balances, margin, P&L, or broker metadata.

This plan does **not** authorize implementation. It is submitted for ITRGA design review. Only an accepted plan and subsequent controlled Build Orders may authorize UI-003 implementation.

---

## 1. Objective and Scope Mapping to Document 12 §5

### 1.1 Objective restatement

UI-003 shall make the existing chart and market-observation surfaces feel like a professional institutional analytical workstation by improving layout, information hierarchy, market-status visibility, watchlist usability, chart overlay organization, and annotation/research-marker presentation.

The workstream is an integration and presentation workstream. It shall not change what AXIOM knows, computes, stores as analytical fact, or is authorized to do.

### 1.2 Scope mapping

| Doc 12 §5 item | UI-003 design interpretation | Explicit boundary |
|---|---|---|
| Professional chart workspace | Recompose the existing `/charts` capability into a chart-centered institutional workspace using UI-001 panels and UI-002 workflow navigation. | No new chart analysis, inference, signal generation, or real-data claim. |
| Market overview | Present existing governed market status, available symbols/timeframes, simulated feed state, and source provenance. | No new market data pipeline, feed vendor, broker, or real-time market provider. |
| Watchlists | Operator presentation preference listing symbols/timeframes to monitor. | Symbol ids only; no orders, quantities, positions, accounts, or P&L. |
| Chart overlays | Toggle presentation of existing overlays/annotations/markers. | No overlay generation algorithm; no recommendation engine. |
| Annotation integration | Display existing W5-U03 inert chart research annotations and existing annotation creation affordance if already authorized. | Annotations are research notes only, not instructions/signals/orders. |
| Research markers | Present existing governed advisory/research artifacts as read-only context markers where available. | Markers are not generated in UI-003; no client-side inference or recompute. |
| Market status | Display existing readiness/connection/feed/source status. | Status is observational, non-actuating, and does not start real feeds. |
| Layout improvements | Chart-centered layout using UI-001 shell, panel infrastructure, and UI-002 navigation. | No competing layout, duplicate nav, or independent shell. |

---

## 2. Constitutional Bright-Line Controls

UI-003 touches domain-facing market surfaces. Therefore the following are mandatory design constraints.

### 2.1 Presentation-only

UI-003 may:

- reorganize existing chart/market information;
- improve chart workspace layout;
- display existing candles/quotes/status/annotations/research artifacts;
- provide watchlist preference UI;
- add accessible toggles for existing overlay families;
- improve empty/loading/error states and responsiveness.

UI-003 shall not:

- add client-side inference;
- add authoritative recompute;
- add new analytical algorithms;
- add signal generation;
- add real market feed integration;
- add broker or account integration;
- add execution, order, position, balance, margin, capital, allocation, sizing, stop/target, or real P&L capability;
- open or weaken the Governance Gate;
- add external AI/LLM;
- add dynamic plugin execution.

### 2.2 Market-data posture

Existing market data labels must remain explicit:

```text
seed:synthetic = non-authoritative chart context
live:simulated = simulated/governed live-feed seam
CSV ingest labels = source-specific historical ingest provenance
```

No UI-003 surface may label simulated/governed data as real market data.

### 2.3 Chart overlays and markers

Chart overlays, research markers, and annotation integration shall be **read-only presentation of existing governed artifacts** unless a separately approved existing UI already supports inert operator-authored annotations. They shall not be interpreted or presented as orders, trading advice, live alerts, automated signals, or instructions.

---

## 3. UI-001 / UI-002 Reconciliation and No-Duplication Table

| UI-003 scope item | Existing UI-001/UI-002 primitive | Classification | UI-003 design decision |
|---|---|---|---|
| Professional chart workspace | UI-001 shell Region C primary workspace, PanelHost/PanelRegistry, LayoutManager; UI-002 breadcrumbs/switcher/search/palette. | Extends existing primitives | Recompose `/charts` inside the existing shell; no new application frame or page-level nav. |
| Market overview | Existing dashboard/live market surfaces; existing StatusPill and live components; UI-001 context/activity panels. | Extends / consolidates presentation | Use existing read/status data and present market summary in panels; no new data source. |
| Watchlists | Existing `operator_workspace_preferences`; UI-001 preference persistence seam. | Extends existing persistence | Store watchlists as operator-scoped presentation preferences under existing preferences. No new table. |
| Chart overlays | Existing chart component and annotation layer; UI-001 overlays only for temporary UI. | Extends presentation | Add overlay visibility model and controls, if authorized, using design tokens and local presentation state/preference. |
| Annotation integration | W5-U03 inert `chart_research_annotations` store/API and existing `ChartResearchAnnotationLayer`. | Reuse existing governed store | Display existing annotations/provenance; keep research-only disclaimer. |
| Research markers | Existing advisory signal/read APIs and research artifacts; UI-002 global search/navigation. | Extends read-only presentation | Read-only markers only; no generation, mutation, or inference. |
| Market status | Existing readiness/live-market stats/WebSocket state/status labels. | Reuse existing status | Present connection/feed/source status visibly and accessibly; no real feed. |
| Layout improvements | UI-001 shell layout + panels + tokens; UI-002 workflow navigation. | Extends UI-001/UI-002 | Chart-centered responsive layout, no duplicate nav/header/sidebar. |

### 3.1 No-duplication commitments

UI-003 shall not introduce:

- a second shell;
- a second global nav;
- a duplicate chart-specific sidebar competing with the UI-001 Navigation Dock;
- a second command palette;
- a second overlay family;
- page-specific global headers;
- workspace-owned route maps independent of UI-001 registry and UI-002 workflow metadata.

### 3.2 UI-009 dependency status

UI-003 depends on UI-009 core components conceptually, but the current approved UI foundation already provides:

- design tokens and semantic colors from UI-001;
- shell buttons/status chips/panels;
- panel/docking infrastructure;
- existing table/status/chart components;
- accessible overlay/dialog/notification primitives.

UI-003 shall avoid a separate UI-009 prerequisite for early phases by using existing primitives and small first-party components. If a reusable market component becomes broadly useful (for example `MarketStatusCard`, `WatchlistPanel`, or `ChartOverlayToggleGroup`), UI-003 shall implement it as a local first-party component first and flag it for later UI-009 component-library harvesting. No third-party component dependency is proposed.

---

## 4. Architecture

### 4.1 High-level workspace composition

```text
InstitutionalWorkspaceShell (UI-001)
├── Region A — Global Header / UI-002 breadcrumbs/search/palette/switcher
├── Region B — Navigation Dock (UI-002 workflow nav)
├── Region C — Professional Market Workspace (UI-003)
│   ├── Market Overview Strip
│   ├── Watchlist Panel / Symbol Focus
│   ├── Professional Chart Surface
│   ├── Overlay / Research Marker Controls
│   └── Annotation / Provenance Presentation
├── Region D — Context Panel
│   ├── Active symbol/source provenance
│   ├── Related research/annotation summary
│   └── Governance/research-only framing
├── Region E — Activity Dock
│   └── Feed/status/activity summary using existing events/status only
└── Region F — Existing overlay family
```

### 4.2 State ownership

| State | Owner | Persistence | Notes |
|---|---|---|---|
| Shell navigation/layout/session | UI-001 shell | Existing shell preferences | UI-003 consumes, does not own. |
| Workflow navigation/search/palette | UI-002 | Existing UI-002 modules | UI-003 registers/consumes route metadata only if authorized. |
| Active chart symbol/timeframe/type | Chart workspace presentation state | Existing state; optional preference persistence under existing table | No analytical state. |
| Watchlists | UI-003 presentation preference | Existing `operator_workspace_preferences` | Symbol/timeframe ids only. |
| Chart overlays visibility | UI-003 presentation state/preference | Existing preferences if persisted | Visibility only; no generation. |
| Candles/quotes/status data | Existing read APIs/hooks | Backend existing stores only | No new source. |
| Annotations/research markers | Existing governed stores/read APIs | Existing W5/W3 stores | Read-only presentation except already-authorized inert annotation creation. |

---

## 5. Data-Source Table

| Surface | Existing data origin | Existing frontend/API seam | UI-003 usage | New backend? |
|---|---|---|---|---|
| Candlestick/line/area chart | Existing candle persistence / synthetic seed / CSV ingest | `fetchCandles`, `useChartData`, `PriceChart`, `lightweight-charts` | Render professional chart surface | No |
| Simulated live status/quotes | Existing simulated WebSocket/live market seam | `useLiveMarket`, `LivePriceTable`, `/ws/market`, `fetchLiveMarketStats` where already present | Market overview/status display | No |
| Chart research annotations | Existing W5-U03 inert annotation store | `fetchChartResearchAnnotations`, `ChartResearchAnnotationLayer`, existing create API if retained | Display annotations/provenance; inert creation only where already authorized | No new backend |
| Advisory signal markers | Existing advisory signal records | `fetchAdvisorySignals` read API | Optional read-only marker badges/context | No |
| Research collections/journal links | Existing research management/journal stores | Existing read APIs and UI-002 search | Related research context only | No |
| Watchlists | Operator presentation preferences | Existing workspace preferences API | Store symbol/timeframe id lists | No new table |
| Market health/readiness | Existing health/readiness/status surfaces | Existing health/readiness/live status APIs/hooks | Non-actuating status display | No |

### 5.1 No new analysis statement

All UI-003 surfaces must display existing values. UI-003 shall not compute authoritative metrics, derive new signals, infer regimes, recompute analytics, generate overlays, or create recommendations.

---

## 6. Watchlist Persistence Design

### 6.1 Decision

UI-003 shall **reuse `operator_workspace_preferences`**.

No new watchlist table is proposed.

### 6.2 Preference key and payload sketch

Proposed workspace key:

```text
professional-market-workspace-v1
```

Payload sketch:

```json
{
  "workspace_key": "professional-market-workspace-v1",
  "layout_config": {
    "active_symbol": "EURUSD",
    "active_timeframe": "M1",
    "watchlists": [
      {
        "watchlist_id": "primary-market-watchlist",
        "name": "Primary market watchlist",
        "symbols": ["EURUSD", "BTCUSD"],
        "timeframes": ["M1", "H1"]
      }
    ],
    "overlay_visibility": {
      "annotations": true,
      "research_markers": true,
      "source_provenance": true
    }
  },
  "visible_modules": ["chart", "watchlist", "market_status", "annotations"],
  "theme_config": { "density": "institutional" },
  "metadata": { "ui_workstream": "UI-003", "version": "market-workspace-v1" }
}
```

### 6.3 Watchlist forbidden fields

Watchlist payloads shall not contain:

```text
quantity
position
order
side
buy
sell
broker
account
balance
margin
capital
allocation
stop_loss
take_profit
real_pnl
pnl
open_gate
allow_execution
```

### 6.4 Evidence expectation when implemented

Because this reuses an existing table/API and adds no schema, the evidence shall include:

- payload-shape tests proving symbol/timeframe ids only;
- operator-scoping tests via existing preference tests where relevant;
- no-secret/no-forbidden-field tests;
- Alembic head unchanged;
- package manifests unchanged;
- optional raw PostgreSQL read-back if ITRGA requests preference-row proof.

A new table is not proposed. If ITRGA later requires a dedicated table, a separate persistence/endpoint review and full persistence-capture control would be required.

---

## 7. Chart Overlays, Research Markers, and Annotation Integration

### 7.1 Existing governed annotation integration

UI-003 shall reuse existing W5-U03 chart research annotations:

```text
chart_research_annotations
fetchChartResearchAnnotations
ChartResearchAnnotationLayer
```

Annotations remain:

- operator-authored or existing governed artifacts;
- research-only;
- inert;
- source/provenance-bearing;
- non-instructional;
- non-executing.

### 7.2 Research markers

Research markers may present existing artifacts such as advisory signals or linked reports as read-only markers. They shall be labeled as research context and shall preserve uncertainty/provenance where available.

Prohibited:

- client-side marker generation by inference;
- signal re-emission;
- guardrail override;
- automatic alerting/action;
- trading instruction language.

### 7.3 Overlay controls

Overlay controls are presentation toggles only, such as:

```text
Show annotations
Show research markers
Show source provenance
Show simulated feed status
```

They shall not mutate source artifacts or trigger computations.

---

## 8. Accessibility Plan

Charts are intrinsically accessibility-sensitive. UI-003 shall treat accessibility as first-class.

### 8.1 Chart accessibility

Required:

- accessible chart title and description;
- textual summary of active symbol, timeframe, source provenance, bar count, and simulated status;
- keyboard-operable symbol/timeframe/chart-type controls;
- focus-visible chart container and overlay controls;
- non-color status labels for up/down/neutral states;
- reduced-motion compatible live-update indicators;
- screen-reader-readable empty/loading/error states;
- table/list alternative for watchlist and market overview values.

### 8.2 Watchlist accessibility

Required:

- keyboard-operable add/remove/reorder if authorized;
- explicit labels for symbol/timeframe selectors;
- no drag-only operations;
- clear validation errors;
- no color-only selected states.

### 8.3 Overlay/marker accessibility

Required:

- toggle buttons with `aria-pressed`;
- marker list alternative outside the chart canvas;
- annotation provenance and research-only labels in text;
- no reliance solely on position/color.

---

## 9. Responsive and Layout Plan

UI-003 shall use UI-001 layout regions and degrade gracefully:

| Viewport | Behavior |
|---|---|
| Large desktop | Chart surface central; watchlist/market overview and context visible simultaneously. |
| Standard desktop | Chart central; watchlist may compact; context panel remains visible. |
| Laptop | Watchlist/overview collapsible; chart retains priority. |
| Narrow/tablet-like | Watchlist becomes stacked/accordion; chart remains usable; no duplicate shell/nav. |

No permanent floating windows or independent chart terminal layout shall be introduced.

---

## 10. Phase Decomposition

Implementation requires ITRGA-accepted plan and controlled Build Orders. No later phase begins until ITRGA accepts the prior phase or explicitly authorizes parallel work.

### UI-003-P01 — Market Workspace Frame and Data-Source Inventory

Objective: establish the professional market workspace frame inside UI-001/UI-002 without capability expansion.

Scope:

- chart-centered Region C composition;
- market overview/status placeholders using existing data;
- explicit source-provenance labels;
- no watchlist persistence yet;
- no new backend/API/schema/dependency.

Named test anchors:

```text
test_ui003_market_workspace_mounts_inside_single_ui001_shell
test_ui003_market_workspace_uses_existing_chart_and_market_sources_only
test_ui003_market_workspace_labels_synthetic_and_simulated_data_non_authoritative
test_ui003_market_workspace_contains_no_execution_or_actuation_controls
test_ui003_market_workspace_has_accessible_chart_summary_and_controls
```

### UI-003-P02 — Watchlists via Existing Preferences

Objective: implement operator watchlists as presentation preferences using existing `operator_workspace_preferences`.

Scope:

- watchlist model with symbol/timeframe ids only;
- preference read/write through existing preference API;
- forbidden-field validation;
- operator scoping inherited from existing endpoint;
- no new table.

Named test anchors:

```text
test_ui003_watchlists_use_operator_workspace_preferences_no_new_table
test_ui003_watchlists_store_symbol_ids_only_no_positions_orders_or_accounts
test_ui003_watchlists_reject_execution_broker_account_payload_fields
test_ui003_watchlists_are_keyboard_operable_and_accessible
test_ui003_watchlist_persistence_preserves_alembic_head
```

### UI-003-P03 — Chart Overlays, Research Markers, and Annotation Integration

Objective: integrate existing annotations and read-only research markers as professional overlays.

Scope:

- overlay visibility controls;
- existing W5-U03 annotation layer presentation hardening;
- optional read-only advisory signal marker display from existing read API;
- marker list alternative for accessibility;
- provenance and research-only labels.

Named test anchors:

```text
test_ui003_overlays_render_existing_annotations_read_only
test_ui003_research_markers_use_existing_read_artifacts_no_inference
test_ui003_overlay_controls_are_presentation_toggles_only
test_ui003_markers_preserve_provenance_uncertainty_and_research_only_labels
test_ui003_overlays_contain_no_signal_generation_or_actuation
```

### UI-003-P04 — Market Status, Overview, and Responsive Professional Layout

Objective: refine market overview/status panels and responsive chart-centered layout.

Scope:

- market overview cards over existing status/quote data;
- responsive layout hardening;
- loading/empty/error states;
- no new feed/provider.

Named test anchors:

```text
test_ui003_market_overview_uses_existing_simulated_status_sources_only
test_ui003_market_status_never_claims_real_feed_or_broker_connection
test_ui003_responsive_layout_preserves_single_shell_no_duplicate_nav
test_ui003_empty_loading_error_states_are_accessible_and_research_framed
```

### UI-003-P05 — UI-003 Completion Checkpoint

Objective: final integration evidence and ITRGA completion review.

Scope:

- route/browser evidence;
- no-actuation whole-surface grep;
- regression;
- watchlist persistence proof if implemented;
- final constitutional self-check.

Named test anchors:

```text
test_ui003_completion_chart_workspace_is_operational_center_without_scope_expansion
test_ui003_completion_all_market_surfaces_are_presentation_only
test_ui003_completion_no_live_real_data_broker_execution_or_gate_path
test_ui003_completion_accessibility_responsive_and_registry_integration_hold
test_ui003_completion_regression_preserves_backend_and_ui002_navigation
```

---

## 11. Regression and Evidence Strategy

Each Build Order shall provide:

- build identity proof;
- named tests displayed passing by verbose reporter;
- frontend full suite;
- TypeScript clean;
- production build with bundle delta;
- npm audit;
- backend Ruff and full backend suite unless ITRGA narrows evidence;
- Alembic current = `20260717_0037` unless ITRGA authorizes persistence migration;
- no-new-endpoint/table/migration grep;
- package-manifest content proof showing no new dependency;
- whole-surface no-actuation grep;
- browser served-session screenshots;
- networked Git-Bash CI with `LOCAL_CI_EXIT_CODE: 0`.

Standing methodology from ITRGA UI-002 completion: git-diff phase isolation is retired for this single-commit DA repository. Future no-drift proof shall rely on per-phase tests, Alembic head, no-new-endpoint grep, package-manifest content, and regression.

---

## 12. Risks and Mitigations

| Risk | Severity | Mitigation |
|---|---:|---|
| Professional chart presentation is mistaken for trading execution | Critical | Strong research-only labels, no actuation controls, grep/tests. |
| Watchlists creep into portfolio/account concepts | Critical | Symbol/timeframe ids only; forbidden-field tests. |
| Chart overlays become generated signals | Critical | Existing artifacts only; no inference/recompute; marker provenance labels. |
| Simulated data is mistaken for real market data | High | Persistent `seed:synthetic` and `live:simulated` labels. |
| New chart dependency temptation | Medium | Reuse TradingView Lightweight Charts already present; no new dependency. |
| Accessibility gaps in chart canvas | High | Text summaries, marker lists, keyboard controls, no color-only meaning. |
| Duplicate chart-side navigation | Medium | UI-001/UI-002 single-shell tests and no duplicate nav proof. |
| Backend persistence creep | Medium | Reuse `operator_workspace_preferences`; no new table. |

---

## 13. Open Questions for ITRGA

1. Does ITRGA accept reuse of `operator_workspace_preferences` for watchlists as the approved P02 persistence approach, with symbol/timeframe ids only and no new table?
2. Should read-only advisory signal markers be included in UI-003-P03, or deferred until after the chart frame and watchlist persistence are accepted?
3. Should watchlist reorder be implemented in UI-003-P02 or deferred to P04 responsive/polish, given accessibility requirements?
4. Should P04b remaining global-search adapters from UI-002 be scheduled separately before or after UI-003 begins, or held until UI-006 artifact explorer?
5. Does ITRGA require raw PostgreSQL read-back for watchlist preferences even though no new table is proposed?

---

## 14. DA Recommendation for First Build Order

If ITRGA accepts this plan, the DA recommends the first Build Order be:

```text
UI-003-P01 — Professional Market Workspace Frame, Existing Data-Source Inventory, and Non-Authoritative Market Presentation
```

Rationale:

- proves chart-centered composition inside UI-001/UI-002 before persistence or overlays;
- validates the domain bright line early;
- avoids watchlist persistence until frame/source controls are accepted;
- minimizes regression risk;
- establishes browser evidence expectations for the market workspace.

---

## 15. Constitutional Attestation

The DA attests this design plan is:

- presentation-only;
- no new analysis/computation/live-data/capability;
- no client-side inference;
- no new backend analytical engine;
- no real market feed/broker/account/order path;
- no external AI/LLM;
- no dynamic plugin execution;
- no Governance Gate change;
- extends UI-001 and UI-002 without duplicating them;
- proposes no new table by default;
- proposes no new dependency;
- does not certify production.

DA does not self-approve this design plan and does not begin UI-003 implementation. Implementation awaits ITRGA design acceptance and a controlled Build Order.

---

**End of UI-003_ENGINEERING_DESIGN_PLAN.md**
