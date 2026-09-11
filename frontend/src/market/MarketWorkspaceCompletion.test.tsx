import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import {
  ChartOverlayControls,
  ChartResearchMarkerList,
  ChartWorkspacePage,
  MarketStatusCards,
  MarketWorkspaceStateNotice,
} from "../components/chart/ChartWorkspaceSurface";
import {
  DEFAULT_MARKET_WORKSPACE_PREFERENCE,
  MarketWatchlistPanel,
  PROFESSIONAL_MARKET_WORKSPACE_KEY,
  toMarketWorkspacePreferenceWrite,
  WATCHLIST_FORBIDDEN_FIELDS,
} from "./marketWatchlists";
import type { AdvisorySignal } from "../api/client";
import { InstitutionalWorkspaceShell } from "../workstation/components/InstitutionalWorkspaceShell";
import { contextNavigationTargets } from "../workstation/navigation/contextNavigation";
import { generateNavigationSections } from "../workstation/navigation/navigationGenerator";
import { WORKSPACE_REGISTRY, workspaceForPath } from "../workstation/registry/workspaceRegistry";

const authState = vi.hoisted(() => ({
  value: {
    operator: { username: "operator", role: "admin" },
    loading: false,
    isAuthenticated: true,
    logout: vi.fn(),
    login: vi.fn(),
    refreshProfile: vi.fn(),
  },
}));

const chartDataState = vi.hoisted(() => ({
  value: {
    bars: [
      { time: 1_720_000_000, open: 1.1, high: 1.2, low: 1.05, close: 1.16, volume: 1000 },
      { time: 1_720_000_060, open: 1.16, high: 1.22, low: 1.1, close: 1.18, volume: 1004 },
    ],
    loadState: "ready" as const,
    error: null,
    connectionState: "connected" as const,
    feedRunning: false,
    lastLiveAt: null,
    reload: vi.fn().mockResolvedValue(undefined),
    startFeed: vi.fn().mockResolvedValue(undefined),
    stopFeed: vi.fn().mockResolvedValue(undefined),
  },
}));

vi.mock("../context/AuthContext", () => ({
  useAuth: () => authState.value,
}));

vi.mock("../workstation/persistence/shellPreferences", () => ({
  loadShellLayoutPreference: vi.fn().mockResolvedValue(null),
  persistShellLayoutPreference: vi.fn().mockResolvedValue({}),
}));

vi.mock("../hooks/useChartData", () => ({
  useChartData: () => chartDataState.value,
}));

vi.mock("../components/chart/PriceChart", () => ({
  PriceChart: ({ symbol, chartType }: { symbol: string; chartType: string }) => (
    <div className="chart-canvas" role="img" aria-label={`${symbol} price chart, ${chartType}`}>
      Mock governed price chart
    </div>
  ),
}));

vi.mock("../api/client", async (importOriginal) => {
  const actual = await importOriginal<typeof import("../api/client")>();
  const pendingRead = () => new Promise<never>(() => undefined);
  return {
    ...actual,
    fetchAdvisorySignals: vi.fn(pendingRead),
    fetchCandles: vi.fn().mockResolvedValue({ kind: "native", timeframe: "M1", bars: [] }),
    fetchChartResearchAnnotations: vi.fn(pendingRead),
    createChartResearchAnnotation: vi.fn().mockResolvedValue({}),
    seedChartHistory: vi.fn().mockResolvedValue({ status: "ok", seeded: {}, timeframe: "M1" }),
    fetchWorkspacePreferences: vi.fn(pendingRead),
    createWorkspacePreference: vi.fn().mockResolvedValue({}),
    updateWorkspacePreference: vi.fn().mockResolvedValue({}),
    fetchJournalEntries: vi.fn().mockResolvedValue([]),
    fetchResearchManagementBundle: vi.fn().mockResolvedValue({ collections: [], members: [], tags: [], supported_artifact_types: [], posture: "research_only" }),
  };
});

async function readProductionMarketSource(): Promise<string> {
  const modules = import.meta.glob("../**/*.{ts,tsx}", {
    query: "?raw",
    import: "default",
  });
  const marketFiles = ["/components/chart/ChartWorkspaceSurface.tsx", "/marketWatchlists.tsx"];
  const texts = await Promise.all(
    Object.entries(modules)
      .filter(([path]) => !path.includes(".test."))
      .filter(([path]) => marketFiles.some((suffix) => path.endsWith(suffix)))
      .map(([, loader]) => (loader as () => Promise<string>)()),
  );
  return texts.join("\n");
}

function renderMarketWorkspaceShell(path = "/charts") {
  render(
    <MemoryRouter initialEntries={[path]}>
      <Routes>
        <Route element={<InstitutionalWorkspaceShell />}>
          <Route path="/charts" element={<ChartWorkspacePage />} />
          <Route path="/" element={<h1>Operations content</h1>} />
        </Route>
        <Route path="/login" element={<div>Operator login required</div>} />
      </Routes>
    </MemoryRouter>,
  );
}

const researchSignal: AdvisorySignal = {
  signal_id: "sig-ui003-p05",
  created_at: "2026-07-23T08:00:00Z",
  as_of_time: "2026-07-23T07:59:00Z",
  market_class: "forex",
  provider: "internal",
  symbol: "EURUSD",
  timeframe: "M1",
  model_artifact_id: "model-1",
  model_version: "1-42",
  feature_set_version: "features-v1",
  experiment_id: "exp-1",
  statistical_report_id: "stat-1",
  calibration_report_id: "cal-1",
  economic_report_id: "econ-1",
  generalization_report_id: "gen-1",
  inference_input_hash: "hash-1",
  raw_score: 0.1234,
  calibrated_confidence: 0.5,
  input_staleness_seconds: 60,
  signal_validity_seconds: 300,
  expires_at: "2026-07-23T08:05:00Z",
  freshness_status: "fresh",
  signal_direction: "positive_bias",
  signal_state: "warning",
  state_reason: "POORLY_CALIBRATED",
  eligibility_reasons: [],
  operating_domain_status: "valid",
  calibration_status: "warning:POORLY_CALIBRATED",
  economic_verdict: "research_only",
  risk_notes: null,
  rationale: "Existing advisory context for completion marker.",
  explainability_summary: {},
  state_transition_history: ["candidate", "warning"],
  audit_correlation_id: "corr-1",
};

describe("UI-003-P05 professional market workspace completion checkpoint", () => {
  it("test_ui003_completion_chart_workspace_is_operational_center_without_scope_expansion", () => {
    renderMarketWorkspaceShell();

    expect(screen.getAllByTestId("institutional-workspace-shell")).toHaveLength(1);
    expect(screen.getByLabelText("Primary workspace")).toHaveAttribute(
      "data-active-telemetry-id",
      "workspace.monitor.chart_workspace",
    );
    expect(screen.getByLabelText("Professional market workspace overview")).toBeInTheDocument();
    expect(screen.getByLabelText("Market status overview cards")).toBeInTheDocument();
    expect(screen.getByLabelText("Professional market watchlist")).toBeInTheDocument();
    expect(screen.getByLabelText("Market overlay controls")).toBeInTheDocument();
    expect(screen.getByLabelText("Price chart with research annotations")).toBeInTheDocument();
    expect(screen.getByLabelText("Chart research annotation controls")).toBeInTheDocument();

    const workspace = workspaceForPath("/charts");
    expect(workspace.id).toBe("monitor.chart_workspace");
    expect(workspace.noActuation).toBe(true);
    expect(workspace.requiresAuth).toBe(true);
    expect(WORKSPACE_REGISTRY.filter((item) => item.route === "/charts")).toHaveLength(1);
  });

  it("test_ui003_completion_all_market_surfaces_are_presentation_only", async () => {
    const onToggle = vi.fn();
    const onAddSymbol = vi.fn();
    const onRemoveSymbol = vi.fn();
    const onSelectSymbol = vi.fn();

    render(
      <>
        <MarketStatusCards
          symbol="EURUSD"
          timeframe="M1"
          barCount={500}
          connectionState="connected"
          feedRunning={false}
          lastLiveAt={null}
          sourceSummary="seed:synthetic=500 · live:simulated=0"
        />
        <ChartOverlayControls
          visibility={{ annotations: true, researchMarkers: true, sourceProvenance: true }}
          onToggle={onToggle}
        />
        <ChartResearchMarkerList signals={[researchSignal]} visible />
        <MarketWatchlistPanel
          watchlist={DEFAULT_MARKET_WORKSPACE_PREFERENCE.watchlists[0]}
          availableSymbols={["EURUSD", "BTCUSD"]}
          availableTimeframes={["M1", "H1"]}
          selectedSymbol="EURUSD"
          selectedTimeframe="M1"
          onAddSymbol={onAddSymbol}
          onRemoveSymbol={onRemoveSymbol}
          onSelectSymbol={onSelectSymbol}
        />
      </>,
    );

    expect(screen.getByLabelText("Market status overview cards")).toHaveTextContent("live:simulated");
    expect(screen.getByLabelText("Chart overlay presentation controls")).toHaveTextContent(
      "Presentation toggles only",
    );
    expect(screen.getByLabelText("Read-only research marker list")).toHaveTextContent(
      "Existing advisory records shown as inert research context",
    );
    expect(screen.getByLabelText("Professional market watchlist")).toHaveTextContent(
      "Symbol and timeframe ids only",
    );

    fireEvent.click(screen.getByRole("button", { name: /Show annotations/i }));
    fireEvent.click(screen.getByRole("button", { name: "Add symbol to watchlist" }));
    expect(onToggle).toHaveBeenCalledWith("annotations");
    expect(onAddSymbol).toHaveBeenCalledWith("EURUSD", "M1");

    const payload = toMarketWorkspacePreferenceWrite(DEFAULT_MARKET_WORKSPACE_PREFERENCE);
    const payloadText = JSON.stringify(payload).toLowerCase();
    expect(payload.workspace_key).toBe(PROFESSIONAL_MARKET_WORKSPACE_KEY);
    for (const field of WATCHLIST_FORBIDDEN_FIELDS) {
      expect(payloadText).not.toContain(`\"${field}\"`);
    }

    const sourceText = (await readProductionMarketSource()).toLowerCase();
    expect(sourceText).not.toContain("runinference");
    expect(sourceText).not.toContain("authoritativerecompute");
    expect(sourceText).not.toContain("createorder");
  });

  it("test_ui003_completion_no_live_real_data_broker_execution_or_gate_path", async () => {
    const sourceText = (await readProductionMarketSource()).toLowerCase();
    expect(sourceText).toContain("live:simulated");
    expect(sourceText).toContain("not an external venue feed");
    expect(sourceText).not.toContain("real feed");
    expect(sourceText).not.toContain("broker connection");
    expect(sourceText).not.toContain("new marketdataprovider");
    expect(sourceText).not.toContain("brokerfeed");

    const forbidden = [
      "b" + "uy",
      "s" + "ell",
      "place_" + "order",
      "exec" + "ute",
      "go-live",
      "connect-broker",
      "account_id",
      "order_ticket",
      "open_gate",
      "allow_exec" + "ution",
      "emit" + "signal",
      "infer" + "signal",
    ];
    for (const marker of forbidden) {
      expect(sourceText).not.toContain(marker);
    }
  });

  it("test_ui003_completion_accessibility_responsive_and_registry_integration_hold", async () => {
    renderMarketWorkspaceShell();

    // SUPERSEDED BY CITATION (BO-FE-U02 §2.2/§2.9, PC-FEU02-1 C4/C9, ACC-1; adopted 2026-09-11): the asserted heritage chips are EXPELLED from the chrome boundary; the truthful cluster renders the locked-config mode badge + live health chip instead.
    // (pin scoped to the CHROME's status cluster — the GovernanceOverlay's 'Gate CLOSED' record entries are OUT-OF-BOUNDARY heritage, protected per PC-FEU02-1 C9 heritage clause, not chrome chips)
    const chromeCluster = screen.getByTestId("shell-governance-status");
    expect(chromeCluster.textContent).not.toContain("Gate CLOSED");
    expect(screen.getByTestId("chrome-mode-badge")).toHaveTextContent(/RESEARCH · NON-ACTUATING/);
    expect(screen.getAllByText("Research-only").length).toBeGreaterThanOrEqual(1);
    expect(screen.queryByText("Presentation shell")).toBeNull();
    expect(screen.getByLabelText("Breadcrumb")).toBeInTheDocument();
    expect(screen.getByLabelText("Institutional workflow navigation")).toBeInTheDocument();
    expect(screen.getByLabelText("Context panel")).toBeInTheDocument();
    expect(screen.getByLabelText("Activity dock")).toBeInTheDocument();

    const overview = screen.getByLabelText("Professional market workspace overview");
    expect(within(overview).getByText("EURUSD")).toHaveClass("mono");
    expect(within(overview).getByText("M1")).toHaveClass("mono");
    expect(within(overview).getByText("live:simulated")).toHaveClass("mono");

    const statusCards = screen.getByLabelText("Market status overview cards");
    expect(statusCards.querySelector(".market-status-card-grid")).not.toBeNull();
    expect(screen.getByLabelText("Professional market watchlist").querySelector(".watchlist-symbol-list")).not.toBeNull();
    expect(screen.getByLabelText("Price chart with research annotations")).toHaveClass("chart-annotation-stage");

    const overlayControls = screen.getByLabelText("Chart overlay presentation controls");
    expect(overlayControls.querySelector(".chart-overlay-toggle-row")).not.toBeNull();
    const annotationsToggle = within(overlayControls).getByRole("button", { name: /Show annotations/i });
    expect(annotationsToggle).toHaveAttribute("aria-pressed", "true");
    fireEvent.click(annotationsToggle);
    expect(annotationsToggle).toHaveAttribute("aria-pressed", "false");

    cleanup();
    render(
      <>
        <MarketWorkspaceStateNotice state="loading" message="Loading governed rows" />
        <MarketWorkspaceStateNotice state="empty" message="No governed rows" />
        <MarketWorkspaceStateNotice state="error" message="Unavailable" />
      </>,
    );
    expect(screen.getByLabelText("Market workspace loading state")).toHaveAttribute("role", "status");
    expect(screen.getByLabelText("Market workspace empty state")).toHaveAttribute("role", "status");
    expect(screen.getByLabelText("Market workspace error state")).toHaveAttribute("role", "alert");
    expect(screen.getAllByText(/Research-only presentation/i)).toHaveLength(3);

    const marketSource = await readProductionMarketSource();
    expect(marketSource).toContain("className=\"mono\"");
    expect(marketSource).toContain("market-status-card-grid");
    expect(marketSource).toContain("chart-overlay-toggle-row");
  });

  it("test_ui003_completion_regression_preserves_backend_and_ui002_navigation", async () => {
    const chartWorkspace = workspaceForPath("/charts");
    const registeredRoutes = new Set(WORKSPACE_REGISTRY.map((workspace) => workspace.route));
    const visibleNavigationIds = generateNavigationSections({
      workspaces: WORKSPACE_REGISTRY,
      operator: { role: "admin" },
    }).flatMap((section) => section.workspaces.map((workspace) => workspace.id));

    expect(visibleNavigationIds).toContain("monitor.chart_workspace");
    expect(contextNavigationTargets(chartWorkspace).every((target) => registeredRoutes.has(target.route))).toBe(true);
    expect(chartWorkspace.defaultLayout.primaryRegion).toBe("workspace");
    expect(chartWorkspace.contextPanel.supported).toBe(true);
    expect(chartWorkspace.activityDock.supported).toBe(true);

    const marketSource = await readProductionMarketSource();
    expect(marketSource).toContain("fetchWorkspacePreferences");
    expect(marketSource).toContain("fetchAdvisorySignals");
    expect(marketSource).not.toContain("CREATE TABLE");
    expect(marketSource).not.toContain("op.create_table");
    expect(marketSource).not.toContain("/api/v1/market-status");
    expect(marketSource).not.toContain("/api/v1/market-overview");
    expect(marketSource).not.toContain("new MarketDataProvider");

    renderMarketWorkspaceShell();
    expect(screen.getAllByTestId("institutional-workspace-shell")).toHaveLength(1);
    expect(screen.getAllByLabelText("Global command bar")).toHaveLength(1);
    expect(screen.getAllByLabelText("Institutional workflow navigation")).toHaveLength(1);
    expect(screen.getAllByRole("button", { name: "Workspace switcher" })).toHaveLength(1);
  });
});
