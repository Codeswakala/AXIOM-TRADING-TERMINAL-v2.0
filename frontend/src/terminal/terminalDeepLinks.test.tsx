import { render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { ProtectedRoute } from "../auth/ProtectedRoute";
import { InstitutionalWorkspaceShell } from "../workstation/components/InstitutionalWorkspaceShell";
import { WORKSPACE_REGISTRY } from "../workstation/registry/workspaceRegistry";
import {
  getPanelFromSearch,
  getViewFromSearch,
} from "../components/terminal/TradingTerminalWorkspace";
import * as client from "../api/client";

// Mock API Client (dock + terminal fetches)
vi.mock("../api/client", async () => {
  const actual = await vi.importActual<typeof client>("../api/client");
  return {
    ...actual,
    fetchAdvisorySignals: vi.fn().mockResolvedValue([]),
    fetchSignalValidationReports: vi.fn().mockResolvedValue([]),
    fetchCorrelationReports: vi.fn().mockResolvedValue([]),
    fetchRegimeReports: vi.fn().mockResolvedValue([]),
    fetchCandles: vi.fn().mockResolvedValue({ kind: "native", timeframe: "M1", bars: [] }),
    fetchChartResearchAnnotations: vi.fn().mockResolvedValue([]),
    fetchTradePlans: vi.fn().mockResolvedValue([]),
    fetchJournalEntries: vi.fn().mockResolvedValue([]),
    fetchPortfolioRiskReports: vi.fn().mockResolvedValue([]),
    fetchScenarioReports: vi.fn().mockResolvedValue([]),
    fetchPortfolioResearchDashboard: vi.fn().mockResolvedValue(null),
    fetchAdvancedResearchReport: vi.fn().mockResolvedValue(null),
    fetchWorkspacePreferences: vi.fn().mockResolvedValue([]),
    createWorkspacePreference: vi.fn(),
    updateWorkspacePreference: vi.fn(),
    fetchAuditEvents: vi.fn().mockResolvedValue([]),
    fetchInstitutionalIntelligenceBundle: vi.fn().mockResolvedValue(null),
    fetchPlatformOperationsEvidence: vi.fn().mockResolvedValue(null),
    fetchResearchManagementBundle: vi
      .fn()
      .mockResolvedValue({ collections: [], members: [], tags: [] }),
    fetchExecutionResearchBundle: vi.fn().mockResolvedValue({
      runs: [],
      fills: [],
      ledger: [],
      riskReports: [],
      experiments: [],
      analyticsReports: [],
    }),
    // SURF-P01: the execution research stage view loads six independent seams.
    fetchSimulatedRunsList: vi.fn().mockResolvedValue([]),
    fetchSimulatedRunFills: vi.fn().mockResolvedValue([]),
    fetchSimulatedLedgerEntriesList: vi.fn().mockResolvedValue([]),
    fetchExecutionRiskReportsList: vi.fn().mockResolvedValue([]),
    fetchExecutionExperimentsList: vi.fn().mockResolvedValue([]),
    fetchSimulatedAnalyticsReportsList: vi.fn().mockResolvedValue([]),
    fetchSimulatedExecutionRunDetail: vi.fn(),
    fetchSimulatedFillDetail: vi.fn(),
    fetchSimulatedLedgerEntryDetail: vi.fn(),
    fetchExecutionRiskReportDetail: vi.fn(),
    fetchExecutionExperimentDetail: vi.fn(),
    fetchSimulatedAnalyticsReportDetail: vi.fn(),
    // SURF-P02: the ALERTS dock + rail badge consume the shared provider.
    fetchMonitoringAlerts: vi.fn().mockResolvedValue([
      {
        alert_id: "alert-dl-1",
        created_at: "2026-07-16T10:00:00Z",
        alert_type: "DRIFT_DETECTED",
        severity: "warning",
        subject_type: "model_artifact",
        subject_id: "model-1",
        market_class: null,
        symbol: null,
        timeframe: null,
        model_artifact_id: "model-1",
        signal_id: null,
        summary: "Deep-link alert fixture.",
        evidence: { drift_detected: true },
        lineage: { source: "deep-link-fixture" },
        acknowledged: false,
        acknowledged_at: null,
        acknowledged_by: null,
        audit_correlation_id: "corr-dl-1",
      },
    ]),
    acknowledgeMonitoringAlert: vi.fn(),
    fetchMonitoringAlertDetail: vi.fn(),
  };
});

// Mock PriceChart (JSDOM canvas)
vi.mock("../components/chart/PriceChart", () => ({
  PriceChart: () => <div data-testid="mock-price-chart">Mock Canvas</div>,
}));

// Mock Auth
const authState = vi.hoisted(() => ({
  value: {
    operator: { username: "lead_operator", role: "admin" },
    loading: false,
    isAuthenticated: true,
    logout: vi.fn(),
    login: vi.fn(),
    refreshProfile: vi.fn(),
  },
}));

vi.mock("../context/AuthContext", () => ({
  useAuth: () => authState.value,
}));

vi.mock("../workstation/persistence/shellPreferences", () => ({
  loadShellLayoutPreference: vi.fn().mockResolvedValue(null),
  persistShellLayoutPreference: vi.fn().mockResolvedValue({}),
}));

vi.mock("../hooks/useLiveMarket", () => ({
  useLiveMarket: () => ({
    quotes: {},
    connectionState: "idle",
    lastMessageTimestamp: Date.now(),
    subscribe: vi.fn(),
    unsubscribe: vi.fn(),
    reconnect: vi.fn(),
    messagesPerMinute: 0,
    messageCount: 0,
    lagHintMs: 0,
  }),
}));

function deepLinkSignal(overrides: Partial<import("../api/client").AdvisorySignal> = {}): import("../api/client").AdvisorySignal {
  return {
    signal_id: "sig-001",
    created_at: "2026-08-13T10:00:00Z",
    as_of_time: "2026-08-13T10:00:00Z",
    market_class: "forex",
    provider: "model.ensemble.v1",
    symbol: "EURUSD",
    timeframe: "1m",
    model_artifact_id: "model.eurusd.classifier",
    model_version: "1.4.2",
    feature_set_version: "feat.m1.v2",
    experiment_id: "exp-001",
    statistical_report_id: "stat-001",
    calibration_report_id: "val-001",
    economic_report_id: "econ-001",
    generalization_report_id: "gen-001",
    inference_input_hash: "a1b2c3d4e5f6789012345678abcdef01",
    raw_score: 0.812,
    calibrated_confidence: 0.784,
    input_staleness_seconds: 4,
    signal_validity_seconds: 60,
    expires_at: "2099-08-13T10:01:00Z",
    freshness_status: "fresh",
    signal_direction: "LONG_BIAS",
    signal_state: "emitted",
    state_reason: "Domain criteria validated",
    eligibility_reasons: ["low_spread", "high_liquidity"],
    operating_domain_status: "in_domain",
    calibration_status: "calibrated",
    economic_verdict: "cost_favorable",
    risk_notes: "Elevated spread risk during session rollover.",
    rationale: "Multi-timeframe momentum alignment with order flow imbalance.",
    explainability_summary: { rsi_14: 0.324 },
    state_transition_history: ["draft", "validated", "emitted"],
    audit_correlation_id: "audit-sig-001",
    ...overrides,
  };
}

beforeEach(() => {
  vi.clearAllMocks();
});

function renderTerminalAt(path: string) {
  return render(
    <MemoryRouter initialEntries={[path]}>
      <Routes>
        <Route
          element={
            <ProtectedRoute>
              <InstitutionalWorkspaceShell />
            </ProtectedRoute>
          }
        >
          {WORKSPACE_REGISTRY.map(({ route, Component }) => (
            <Route key={route} path={route} element={<Component />} />
          ))}
        </Route>
      </Routes>
    </MemoryRouter>,
  );
}

describe("UI-CONV-P03 Terminal Deep-Link Router (view / panel / dock)", () => {
  it("test_uiconv_p03_view_param_parser_resolves_chart_and_unknown_views", () => {
    // OBS-CONV2-7 discharge: the /?view=chart contract is honoured by the parser.
    expect(getViewFromSearch("?view=chart")).toBe("chart");
    expect(getViewFromSearch("?view=research")).toBe("research");
    expect(getViewFromSearch("?view=unknown")).toBe(null);
    expect(getViewFromSearch(undefined)).toBe(null);
    expect(getViewFromSearch("")).toBe(null);
  });

  it("test_uiconv_p03_panel_param_parser_resolves_bottom_dock_tabs", () => {
    expect(getPanelFromSearch("?panel=portfolio")).toBe("PORTFOLIO");
    expect(getPanelFromSearch("?panel=scenarios")).toBe("SCENARIOS");
    expect(getPanelFromSearch("?panel=TRADE_PLANS")).toBe("TRADE_PLANS");
    expect(getPanelFromSearch("?panel=journal")).toBe("JOURNAL");
    expect(getPanelFromSearch("?panel=unknown")).toBe(null);
    expect(getPanelFromSearch(undefined)).toBe(null);
  });

  it("test_uiconv_p03_view_chart_deep_link_renders_chart_stage", async () => {
    renderTerminalAt("/?view=chart");

    await waitFor(() => {
      expect(screen.getByTestId("trading-terminal-workspace")).toHaveAttribute(
        "data-stage-view",
        "chart",
      );
      expect(screen.getByTestId("terminal-chart-stage")).toBeInTheDocument();
    });
  });

  it("test_uiconv_p03_view_research_deep_link_renders_research_hub_stage_content", async () => {
    // OBS-CONV3-4 discharge (B-4 condition): `?view=research` must render the
    // Research Hub stage — real content, not an attribute-only seam. This
    // named test fails if the stage branch only sets `data-stage-view`.
    renderTerminalAt("/?view=research");

    await waitFor(() => {
      expect(screen.getByTestId("trading-terminal-workspace")).toHaveAttribute(
        "data-stage-view",
        "research",
      );
    });

    expect(screen.getByTestId("research-stage-scroll")).toBeInTheDocument();
    // POLISH-P01 M2: the research stage is lazy-loaded — await its chunk.
    await waitFor(() => {
      expect(screen.getByTestId("research-hub-view")).toBeInTheDocument();
    });
    // The centre slot is re-labelled for the research stage.
    expect(screen.getByRole("main", { name: "Research Hub Stage" })).toBeInTheDocument();
    // Real research hub content renders inside the primary stage.
    expect(screen.getAllByText("Unified Research Artifact Explorer").length).toBeGreaterThan(0);
    expect(screen.getByText("Governed Data-Source Inventory")).toBeInTheDocument();
    expect(screen.getByTestId("artifact-explorer-frame")).toBeInTheDocument();
    expect(screen.getByTestId("artifact-source-inventory")).toBeInTheDocument();
    expect(screen.getByTestId("artifact-catalog")).toBeInTheDocument();
    expect(screen.getByTestId("collection-organization-controls")).toBeInTheDocument();
    expect(screen.getByTestId("tag-organization-controls")).toBeInTheDocument();
    expect(screen.getByTestId("organization-records-preview")).toBeInTheDocument();
    // Empty fetch fixtures render the per-section absence markers.
    expect(screen.getByText("No collections returned for this operator.")).toBeInTheDocument();
    expect(screen.getByText("No membership references returned.")).toBeInTheDocument();
    expect(screen.getByText("No tags returned.")).toBeInTheDocument();
    // The chart stage is NOT mounted when the research stage is active.
    expect(screen.queryByTestId("terminal-chart-stage")).not.toBeInTheDocument();
  });

  it("test_surf_p01_view_execution_deep_link_renders_execution_research_stage_content", async () => {
    // SURF-P01 S1/M4-class: `?view=execution` must render the Execution
    // Research stage — real content, not an attribute-only seam.
    renderTerminalAt("/?view=execution");

    await waitFor(() => {
      expect(screen.getByTestId("trading-terminal-workspace")).toHaveAttribute(
        "data-stage-view",
        "execution",
      );
    });

    expect(screen.getByTestId("execution-stage-scroll")).toBeInTheDocument();
    // The centre slot is re-labelled for the execution research stage.
    expect(screen.getByRole("main", { name: "Execution Research Stage" })).toBeInTheDocument();
    // Real execution research content renders inside the primary stage.
    // POLISH-P01 M2: the execution stage is lazy-loaded — await its chunk.
    await waitFor(() => {
      expect(screen.getByText("Execution Research Workspace")).toBeInTheDocument();
    });
    expect(screen.getByText("SIMULATED.")).toBeInTheDocument();
    expect(screen.getByTestId("execution-group-runs")).toBeInTheDocument();
    expect(screen.getByTestId("execution-group-fills")).toBeInTheDocument();
    expect(screen.getByTestId("execution-group-ledger")).toBeInTheDocument();
    expect(screen.getByTestId("execution-group-risk")).toBeInTheDocument();
    expect(screen.getByTestId("execution-group-experiments")).toBeInTheDocument();
    expect(screen.getByTestId("execution-group-analytics")).toBeInTheDocument();
    // Empty fixtures render the per-group absence markers (R3).
    expect(screen.getByText("No simulated runs returned.")).toBeInTheDocument();
    expect(screen.getByText("No simulated ledger rows returned.")).toBeInTheDocument();
    expect(screen.getByText("No risk reports returned.")).toBeInTheDocument();
    expect(screen.getByText("No replay experiments returned.")).toBeInTheDocument();
    expect(screen.getByText("No analytics reports returned.")).toBeInTheDocument();
    // The chart stage is NOT mounted when the execution stage is active.
    expect(screen.queryByTestId("terminal-chart-stage")).not.toBeInTheDocument();
  });

  it("test_surf_p02_dock_alerts_deep_link_activates_the_alerts_tab", async () => {
    // SURF-P02 S1: the left-rail launcher targets /?dock=alerts; the deep link
    // must activate the ALERTS right-dock tab and render the alerts surface.
    renderTerminalAt("/?dock=alerts");

    // BO-F-04 churn (strengthening, D3): the two fixture assertions moved
    // INSIDE the waitFor — the provider populates the list asynchronously
    // after the panel mounts, and the immediate getByText raced that fetch
    // (this exact test was ITRGA's OBS-F03-1 custody failure and reproduced
    // as a full-suite flake on the DA's chain). The test's intent is
    // unchanged: the surfaced panel renders the genuine provider fixture.
    await waitFor(() => {
      expect(screen.getByTestId("right-dock-tab-alerts")).toHaveAttribute(
        "aria-selected",
        "true",
      );
      expect(screen.getByTestId("terminal-alerts-dock")).toBeInTheDocument();
      expect(screen.getByTestId("monitoring-alerts-panel")).toBeInTheDocument();
      expect(screen.getByText("DRIFT_DETECTED")).toBeInTheDocument();
      expect(screen.getByText("Monitoring Alerts")).toBeInTheDocument();
    });
  });

  it("test_uiconv_p03_unknown_view_degrades_to_default_multi_pane", async () => {
    renderTerminalAt("/?view=unknown");

    await waitFor(() => {
      expect(screen.getByTestId("trading-terminal-workspace")).toHaveAttribute(
        "data-stage-view",
        "default",
      );
      // The default multi-pane still renders — never a blank stage.
      expect(screen.getByTestId("terminal-chart-stage")).toBeInTheDocument();
    });
  });

  it("test_uiconv_p03_panel_portfolio_deep_link_activates_portfolio_tab", async () => {
    renderTerminalAt("/?panel=portfolio");

    await waitFor(() => {
      expect(screen.getByTestId("bottom-tab-portfolio")).toHaveAttribute("aria-selected", "true");
      expect(screen.getByTestId("terminal-portfolio-panel")).toBeInTheDocument();
      expect(screen.getByTestId("portfolio-research-panel")).toBeInTheDocument();
    });
  });

  it("test_uiconv_p03_panel_scenarios_deep_link_activates_scenarios_tab_with_comparison", async () => {
    renderTerminalAt("/?panel=scenarios");

    await waitFor(() => {
      expect(screen.getByTestId("bottom-tab-scenarios")).toHaveAttribute("aria-selected", "true");
      expect(screen.getByTestId("terminal-scenarios-panel")).toBeInTheDocument();
      // Item 2: the comparison surface (re-homed from ScenarioComparisonPage) is present.
      expect(screen.getByTestId("scenario-comparison-panel")).toBeInTheDocument();
    });
  });

  it("test_uiconv_p03_dock_param_regression_intelligence_still_activates", async () => {
    renderTerminalAt("/?dock=intelligence");

    await waitFor(() => {
      expect(screen.getByTestId("right-dock-tab-intelligence")).toHaveClass("active");
      expect(screen.getByTestId("terminal-intelligence-cards")).toBeInTheDocument();
    });
  });

  it("test_uiconv_p03_legacy_portfolio_route_redirects_to_portfolio_tab", async () => {
    renderTerminalAt("/portfolio-research");

    await waitFor(() => {
      expect(screen.getByTestId("bottom-tab-portfolio")).toHaveAttribute("aria-selected", "true");
      expect(screen.getByTestId("portfolio-research-panel")).toBeInTheDocument();
    });
  });

  it("test_uiconv_p03_legacy_scenarios_route_redirects_to_scenarios_tab", async () => {
    renderTerminalAt("/compare-scenarios");

    await waitFor(() => {
      expect(screen.getByTestId("bottom-tab-scenarios")).toHaveAttribute("aria-selected", "true");
      expect(screen.getByTestId("scenario-comparison-panel")).toBeInTheDocument();
    });
  });

  it("test_uiconv_p03_open_settings_deep_link_opens_settings_overlay", async () => {
    renderTerminalAt("/?open=settings");

    await waitFor(() => {
      expect(screen.getByTestId("workspace-settings-overlay")).toBeInTheDocument();
      expect(screen.getByTestId("workspace-settings-surface")).toBeInTheDocument();
    });
  });

  it("test_uiconv_p03_legacy_workspace_route_redirects_to_settings_overlay", async () => {
    renderTerminalAt("/workspace");

    await waitFor(() => {
      expect(screen.getByTestId("workspace-settings-overlay")).toBeInTheDocument();
    });
  });

  it("test_uiconv_p03_shell_settings_button_opens_overlay", async () => {
    renderTerminalAt("/");

    await waitFor(() => {
      expect(screen.getByTestId("shell-settings-btn")).toBeInTheDocument();
    });
    screen.getByTestId("shell-settings-btn").click();

    await waitFor(() => {
      expect(screen.getByTestId("workspace-settings-overlay")).toBeInTheDocument();
    });
  });

  it("test_uiconv_p03_open_governance_deep_link_opens_governance_overlay", async () => {
    renderTerminalAt("/?open=governance");

    await waitFor(() => {
      expect(screen.getByTestId("governance-overlay")).toBeInTheDocument();
      expect(screen.getByTestId("governance-frame")).toBeInTheDocument();
    });
  });

  it("test_uiconv_p03_legacy_governance_route_redirects_to_governance_overlay", async () => {
    renderTerminalAt("/governance");

    await waitFor(() => {
      expect(screen.getByTestId("governance-overlay")).toBeInTheDocument();
    });
  });

  it("test_uiconv_p03_legacy_investigate_route_redirects_to_signals_dock", async () => {
    renderTerminalAt("/investigate");

    await waitFor(() => {
      expect(screen.getByTestId("right-dock-tab-signals")).toHaveClass("active");
      expect(screen.getByTestId("terminal-signal-stream")).toBeInTheDocument();
    });
  });

  it("test_uiconv_p03_investigation_drilldown_renders_frame_and_new_sections", async () => {
    vi.mocked(client.fetchAdvisorySignals).mockResolvedValue([deepLinkSignal()]);
    renderTerminalAt("/?dock=signals");

    await waitFor(() => {
      expect(screen.getByTestId("signal-card-sig-001")).toBeInTheDocument();
    });
    // Expand the signal card: the absorbed investigation surface renders
    // its frame (group 1) and the three new capability sections (8/9/10).
    screen.getByTestId("signal-card-sig-001").click();

    await waitFor(() => {
      expect(screen.getByTestId("signal-investigation-frame")).toBeInTheDocument();
      expect(screen.getByTestId("signal-detail-report-ids-sig-001")).toBeInTheDocument();
      expect(screen.getByTestId("signal-detail-evidence-links-sig-001")).toBeInTheDocument();
      expect(screen.getByTestId("signal-detail-intelligence-sig-001")).toBeInTheDocument();
    });
  });
});
