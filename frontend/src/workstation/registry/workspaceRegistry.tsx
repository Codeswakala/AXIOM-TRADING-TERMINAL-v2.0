import { lazy, Suspense, type ComponentType, type ReactNode } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { DashboardPage } from "../../pages/DashboardPage";

// POLISH-P01 M2 (OBS-5): route-level code splitting. The four heavyweight
// workspaces load as separate chunks; the terminal (dashboard + chart stage +
// docks) stays in the initial bundle. The RBAC gate below runs BEFORE a lazy
// component is rendered — rendering is what triggers the chunk fetch, so an
// unauthorized operator never causes the chunk to be requested.
const LiveMarketPage = lazy(() =>
  import("../../pages/LiveMarketPage").then((m) => ({ default: m.LiveMarketPage })),
);
const InstitutionalIntelligencePage = lazy(() =>
  import("../../pages/InstitutionalIntelligencePage").then((m) => ({
    default: m.InstitutionalIntelligencePage,
  })),
);
const TradePlanningPage = lazy(() =>
  import("../../pages/TradePlanningPage").then((m) => ({ default: m.TradePlanningPage })),
);
const ManualJournalPage = lazy(() =>
  import("../../pages/ManualJournalPage").then((m) => ({ default: m.ManualJournalPage })),
);


/**
 * Route Redirect Components (B-CONV2-2)
 *
 * Directs legacy duplicate routes to the unified terminal workstation with the appropriate dock activated:
 * - /charts, /chart -> /?view=chart (Primary Candlestick Chart Stage)
 * - /signals -> /?dock=signals (Advisory Signals Stream Dock)
 * - /analytics -> /?dock=intelligence (Intelligence & Calibration Dock)
 */
export function ChartWorkspaceRedirect() {
  return <Navigate to="/?view=chart" replace />;
}

export function AdvisorySignalsRedirect() {
  return <Navigate to="/?dock=signals" replace />;
}

export function PerformanceAnalyticsRedirect() {
  return <Navigate to="/?dock=intelligence" replace />;
}

/**
 * UI-CONV-P03 redirects (B-CONV-P03 / R2): legacy routes resolve to the
 * unified terminal with the re-homed capability's dock tab active.
 */
export function ScenarioComparisonRedirect() {
  return <Navigate to="/?panel=scenarios" replace />;
}

export function PortfolioResearchRedirect() {
  return <Navigate to="/?panel=portfolio" replace />;
}

/** UI-CONV-P03 item 3: /workspace resolves to the shell settings overlay. */
export function WorkspaceSettingsRedirect() {
  return <Navigate to="/?open=settings" replace />;
}

/** UI-CONV-P03 item 5: /governance resolves to the shell governance overlay. */
export function GovernanceRedirect() {
  return <Navigate to="/?open=governance" replace />;
}

/** UI-CONV-P03 item 6: /investigate resolves to the terminal signals dock
 * (the re-homed home of the signal investigation drill-down). */
export function SignalInvestigationRedirect() {
  return <Navigate to="/?dock=signals" replace />;
}

/** UI-CONV-P03 item 4: /research-management resolves to the terminal
 * research stage view (/?view=research) — the re-homed home of the UI-006
 * Unified Research Artifact Explorer (ResearchHubView). */
export function ResearchManagementRedirect() {
  return <Navigate to="/?view=research" replace />;
}

/** SURF-P01: /execution-research resolves to the terminal execution
 * research stage view (/?view=execution) — the re-homed home of the
 * ExecutionResearchWorkspace (ExecutionResearchView). */
export function ExecutionResearchRedirect() {
  return <Navigate to="/?view=execution" replace />;
}

export type NavigationCategory =
  | "Monitor"
  | "Research"
  | "Investigate"
  | "Compare"
  | "Plan"
  | "Review"
  | "Govern"
  | "Settings";

export type OperatorRole = "admin" | "operator" | "unprivileged" | string;

export type WorkspaceRbacRequirement = {
  allowedRoles: readonly OperatorRole[];
  permission?: string;
};

export type WorkspaceLayoutDefinition = {
  primaryRegion: "workspace";
  contextPanelDefault: "visible" | "collapsed" | "hidden";
  activityDockDefault: "visible" | "collapsed" | "hidden";
};

export type WorkspacePanelSupport = {
  supported: boolean;
  defaultVisible: boolean;
};

export type WorkspaceSearchSupport = {
  enabled: boolean;
  scopes: readonly string[];
};

export type WorkspaceRegistrationContract = {
  /** Workspace Identifier */
  id: string;
  /** Workspace Display Name */
  displayName: string;
  /** Navigation Category */
  navigationCategory: NavigationCategory;
  /** Route */
  route: string;
  /** Icon */
  icon: string;
  /** RBAC Requirements */
  rbac: WorkspaceRbacRequirement;
  /** Default Layout */
  defaultLayout: WorkspaceLayoutDefinition;
  /** Context-Panel Support */
  contextPanel: WorkspacePanelSupport;
  /** Activity-Dock Support */
  activityDock: WorkspacePanelSupport;
  /** Search Support */
  search: WorkspaceSearchSupport;
  /** Keyboard Shortcut */
  keyboardShortcut: string;
  /** Telemetry Identifier */
  telemetryId: string;
  /** Workspace Version */
  workspaceVersion: string;
  /** Optional Feature Flag */
  featureFlag: string | null;
  /** ITRGA guard: protected route must require auth. */
  requiresAuth: true;
  /** ITRGA guard: workspace registry entries are presentation-only. */
  noActuation: true;
};

export type WorkspaceDefinition = WorkspaceRegistrationContract & {
  description: string;
  Component: ComponentType;
  order: number;
  aliasFor?: string;
};

const WORKSPACE_VERSION = "ui-001-p02.workspace-registration.v1";
const ALL_AUTHENTICATED_ROLES = ["admin", "operator"] as const;

const defaultLayout = (overrides: Partial<WorkspaceLayoutDefinition> = {}): WorkspaceLayoutDefinition => ({
  primaryRegion: "workspace",
  contextPanelDefault: "visible",
  activityDockDefault: "visible",
  ...overrides,
});

const panelSupport = (supported = true): WorkspacePanelSupport => ({
  supported,
  defaultVisible: supported,
});

const searchSupport = (...scopes: string[]): WorkspaceSearchSupport => ({
  enabled: scopes.length > 0,
  scopes,
});

const protectedWorkspace = (
  definition: Omit<
    WorkspaceDefinition,
    | "requiresAuth"
    | "noActuation"
    | "workspaceVersion"
    | "featureFlag"
    | "rbac"
    | "defaultLayout"
    | "contextPanel"
    | "activityDock"
  > &
    Partial<
      Pick<
        WorkspaceDefinition,
        "rbac" | "defaultLayout" | "contextPanel" | "activityDock" | "featureFlag"
      >
    >,
): WorkspaceDefinition => ({
  ...definition,
  rbac: definition.rbac ?? { allowedRoles: ALL_AUTHENTICATED_ROLES },
  defaultLayout: definition.defaultLayout ?? defaultLayout(),
  contextPanel: definition.contextPanel ?? panelSupport(true),
  activityDock: definition.activityDock ?? panelSupport(true),
  workspaceVersion: WORKSPACE_VERSION,
  featureFlag: definition.featureFlag ?? null,
  requiresAuth: true,
  noActuation: true,
});

/**
 * POLISH-P01 M2 — chunk-level RBAC gating (proven, not asserted).
 *
 * The gate checks the EXISTING registry RBAC metadata (allowedRoles) against
 * the operator BEFORE rendering the workspace component. For lazy components
 * the chunk is fetched by React only when the component first renders — so a
 * denied operator never triggers the chunk request (pinned by
 * test_polish_p01_lazy_route_chunk_not_fetched_when_unauthorized and by the
 * network-trace capture).
 */
export function GatedRouteElement({
  definition,
}: {
  definition: WorkspaceDefinition;
}): ReactNode {
  const { operator } = useAuth();
  if (!operator || !definition.rbac.allowedRoles.includes(operator.role)) {
    return (
      <div className="route-access-denied" data-testid="route-access-denied" role="alert">
        <span className="route-access-denied-title">ACCESS DENIED</span>
        <span className="route-access-denied-body">
          This workspace is not available to your operator role. This is an access
          restriction, not an empty result.
        </span>
      </div>
    );
  }
  return (
    <Suspense
      fallback={
        <div className="route-loading" data-testid="route-loading">
          Loading workspace…
        </div>
      }
    >
      <definition.Component />
    </Suspense>
  );
}

export const WORKSPACE_REGISTRY: WorkspaceDefinition[] = [
  protectedWorkspace({
    id: "monitor.operations",
    route: "/",
    displayName: "Operations",
    navigationCategory: "Monitor",
    icon: "operations",
    keyboardShortcut: "Alt+O",
    telemetryId: "workspace.monitor.operations",
    order: 10,
    description: "Platform operations, health, alerts, and governance status overview.",
    search: searchSupport("workspace", "alerts", "health"),
    Component: DashboardPage,
  }),
  protectedWorkspace({
    id: "monitor.live_market",
    route: "/live",
    displayName: "Live Market",
    navigationCategory: "Monitor",
    icon: "live-market",
    keyboardShortcut: "Alt+M",
    telemetryId: "workspace.monitor.live_market",
    order: 20,
    description: "Simulated live market stream and market status for research observation.",
    search: searchSupport("workspace", "market"),
    Component: LiveMarketPage,
  }),
  protectedWorkspace({
    id: "monitor.chart_workspace",
    route: "/charts",
    displayName: "Chart Workspace",
    navigationCategory: "Monitor",
    icon: "charts",
    keyboardShortcut: "Alt+C",
    telemetryId: "workspace.monitor.chart_workspace",
    order: 30,
    description: "Chart workspace absorbed into unified terminal chart stage.",
    search: searchSupport("workspace", "charts", "annotations"),
    Component: ChartWorkspaceRedirect,
  }),
  protectedWorkspace({
    id: "monitor.chart_alias",
    route: "/chart",
    displayName: "Chart Workspace Alias",
    navigationCategory: "Monitor",
    icon: "charts",
    keyboardShortcut: "Alt+C",
    telemetryId: "workspace.monitor.chart_alias",
    order: 31,
    description: "Compatibility alias redirecting to unified terminal chart stage.",
    search: searchSupport("workspace", "charts"),
    Component: ChartWorkspaceRedirect,
    aliasFor: "monitor.chart_workspace",
  }),
  protectedWorkspace({
    id: "research.advisory_signals",
    route: "/signals",
    displayName: "Advisory Signals",
    navigationCategory: "Research",
    icon: "signals",
    keyboardShortcut: "Alt+S",
    telemetryId: "workspace.research.advisory_signals",
    order: 40,
    description: "Advisory signals absorbed into unified terminal SIGNALS dock.",
    search: searchSupport("workspace", "signals"),
    Component: AdvisorySignalsRedirect,
  }),
  protectedWorkspace({
    id: "research.analytics",
    route: "/analytics",
    displayName: "Performance Analytics",
    navigationCategory: "Research",
    icon: "analytics",
    keyboardShortcut: "Alt+A",
    telemetryId: "workspace.research.analytics",
    order: 50,
    description: "Advisory analytics absorbed into unified terminal INTELLIGENCE dock.",
    search: searchSupport("workspace", "analytics"),
    Component: PerformanceAnalyticsRedirect,
  }),
  protectedWorkspace({
    id: "research.intelligence",
    route: "/intelligence",
    displayName: "Institutional Intelligence",
    navigationCategory: "Research",
    icon: "intelligence",
    keyboardShortcut: "Alt+I",
    telemetryId: "workspace.research.intelligence",
    order: 60,
    description: "Institutional intelligence reports and uncertainty-bearing summaries.",
    search: searchSupport("workspace", "intelligence", "reports"),
    Component: InstitutionalIntelligencePage,
  }),
  protectedWorkspace({
    id: "investigate.signal_investigation",
    route: "/investigate",
    displayName: "Signal Investigation",
    navigationCategory: "Investigate",
    icon: "investigation",
    keyboardShortcut: "Alt+G",
    telemetryId: "workspace.investigate.signal_investigation",
    order: 70,
    description: "Read-only investigation of signal rationale, lineage, and guardrails.",
    search: searchSupport("workspace", "investigation", "signals"),
    Component: SignalInvestigationRedirect,
  }),
  protectedWorkspace({
    id: "compare.scenarios",
    route: "/compare-scenarios",
    displayName: "Scenario Comparison",
    navigationCategory: "Compare",
    icon: "scenarios",
    keyboardShortcut: "Alt+R",
    telemetryId: "workspace.compare.scenarios",
    order: 80,
    description:
      "Comparison of existing persisted hypothetical scenario reports — absorbed into the terminal SCENARIOS dock.",
    search: searchSupport("workspace", "scenarios"),
    Component: ScenarioComparisonRedirect,
  }),
  protectedWorkspace({
    id: "plan.trade_plans",
    route: "/trade-plans",
    displayName: "Trade Planning",
    navigationCategory: "Plan",
    icon: "plans",
    keyboardShortcut: "Alt+P",
    telemetryId: "workspace.plan.trade_plans",
    order: 90,
    description: "Inert research planning notes with no transaction controls.",
    search: searchSupport("workspace", "plans"),
    Component: TradePlanningPage,
  }),
  protectedWorkspace({
    id: "plan.execution_research",
    route: "/execution-research",
    displayName: "Execution Research",
    navigationCategory: "Plan",
    icon: "execution",
    keyboardShortcut: "Alt+E",
    telemetryId: "workspace.plan.execution_research",
    order: 100,
    description:
      "SIMULATED execution research artifacts and analytics — re-homed into the terminal EXECUTION RESEARCH stage view (/?view=execution).",
    search: searchSupport("workspace", "simulated", "execution_research"),
    Component: ExecutionResearchRedirect,
  }),
  protectedWorkspace({
    id: "review.portfolio_research",
    route: "/portfolio-research",
    displayName: "Portfolio Research",
    navigationCategory: "Review",
    icon: "portfolio",
    keyboardShortcut: "Alt+V",
    telemetryId: "workspace.review.portfolio_research",
    order: 110,
    description:
      "Hypothetical research aggregation and generated reporting preview — absorbed into the terminal PORTFOLIO dock.",
    search: searchSupport("workspace", "portfolio_research"),
    Component: PortfolioResearchRedirect,
  }),
  protectedWorkspace({
    id: "review.journal",
    route: "/journal",
    displayName: "Research Journal",
    navigationCategory: "Review",
    icon: "journal",
    keyboardShortcut: "Alt+J",
    telemetryId: "workspace.review.journal",
    order: 120,
    description: "Manual research journal entries and documented operator reflections.",
    search: searchSupport("workspace", "journal"),
    Component: ManualJournalPage,
  }),
  protectedWorkspace({
    id: "review.research_management",
    route: "/research-management",
    displayName: "Research Management",
    navigationCategory: "Review",
    icon: "artifacts",
    keyboardShortcut: "Alt+T",
    telemetryId: "workspace.review.research_management",
    order: 130,
    description:
      "Reference-only collections and tags over governed research artifacts — re-homed into the terminal RESEARCH stage view (/?view=research).",
    search: searchSupport("workspace", "collections", "tags"),
    Component: ResearchManagementRedirect,
  }),
  protectedWorkspace({
    id: "govern.governance_evidence",
    route: "/governance",
    displayName: "Governance & Evidence",
    navigationCategory: "Govern",
    icon: "governance",
    keyboardShortcut: "Alt+Y",
    telemetryId: "workspace.govern.governance_evidence",
    order: 135,
    description: "Read-only governance, evidence, audit, health, readiness, and version posture.",
    search: searchSupport("workspace", "governance", "evidence", "audit", "readiness"),
    Component: GovernanceRedirect,
  }),
  protectedWorkspace({
    id: "settings.workspace",
    route: "/workspace",
    displayName: "Workspace Settings",
    navigationCategory: "Settings",
    icon: "settings",
    keyboardShortcut: "Alt+W",
    telemetryId: "workspace.settings.workspace",
    order: 140,
    description:
      "Per-operator presentation preferences — re-homed into the shell-owned settings overlay.",
    search: searchSupport("workspace", "settings", "preferences"),
    Component: WorkspaceSettingsRedirect,
  }),
];

export const NAVIGATION_CATEGORIES: NavigationCategory[] = [
  "Monitor",
  "Research",
  "Investigate",
  "Compare",
  "Plan",
  "Review",
  "Govern",
  "Settings",
];

export const CURRENT_PROTECTED_ROUTES = WORKSPACE_REGISTRY.map((workspace) => workspace.route);

export function workspaceForPath(pathname: string): WorkspaceDefinition {
  return (
    WORKSPACE_REGISTRY.find((workspace) => workspace.route === pathname) ?? WORKSPACE_REGISTRY[0]
  );
}
