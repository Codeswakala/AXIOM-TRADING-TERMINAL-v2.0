import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { TradingTerminalWorkspace } from "../components/terminal/TradingTerminalWorkspace";
import {
  CalibratedConfidenceBadge,
  MetricWithInterval,
} from "../components/terminal/StatisticalValueRenderer";
import { ProtectedRoute } from "../auth/ProtectedRoute";
import { InstitutionalWorkspaceShell } from "../workstation/components/InstitutionalWorkspaceShell";
import { WORKSPACE_REGISTRY } from "../workstation/registry/workspaceRegistry";
import { QUICK_ACTION_CATALOGUE } from "../workstation/commands/quickActionCatalogue";
import * as fs from "fs";
import * as path from "path";
import type {
  AdvisorySignal,
  ApiCandle,
  SignalValidationReport,
} from "../api/client";
import * as client from "../api/client";

// Mock API Client
vi.mock("../api/client", async () => {
  const actual = await vi.importActual<typeof client>("../api/client");
  return {
    ...actual,
    fetchAdvisorySignals: vi.fn(),
    fetchSignalValidationReports: vi.fn(),
    fetchCorrelationReports: vi.fn(),
    fetchRegimeReports: vi.fn(),
    fetchCandles: vi.fn(),
    fetchChartResearchAnnotations: vi.fn().mockResolvedValue([]),
    createChartResearchAnnotation: vi.fn(),
    seedChartHistory: vi.fn().mockResolvedValue({ status: "ok", seeded: { EURUSD: 80 } }),
    fetchTradePlans: vi.fn().mockResolvedValue([]),
    fetchJournalEntries: vi.fn().mockResolvedValue([]),
    fetchPortfolioRiskReports: vi.fn().mockResolvedValue([]),
    fetchScenarioReports: vi.fn().mockResolvedValue([]),
    fetchInstitutionalIntelligenceBundle: vi.fn().mockResolvedValue(null),
  };
});

// Mock PriceChart in tests to avoid JSDOM Canvas2D null measureText
vi.mock("../components/chart/PriceChart", () => ({
  PriceChart: ({ bars, chartType, symbol }: { bars: unknown[]; chartType: string; symbol: string }) => (
    <div
      data-testid="mock-price-chart"
      data-bars-count={bars?.length ?? 0}
      data-chart-type={chartType}
      data-symbol={symbol}
    >
      Mock Canvas ({bars?.length ?? 0} bars)
    </div>
  ),
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
    quotes: {
      "EUR/USD": {
        symbol: "EUR/USD",
        marketClass: "forex",
        timeframe: "1m",
        open: "1.08200",
        high: "1.08920",
        low: "1.08110",
        close: "1.08450",
        volume: "14200000",
        openTime: "2026-08-13T12:00:00Z",
        source: "simulated",
        updatedAt: "2026-08-13T12:00:00Z",
      },
    },
    connectionState: "connected",
    lastMessageTimestamp: Date.now(),
    subscribe: vi.fn(),
    unsubscribe: vi.fn(),
    reconnect: vi.fn(),
    messagesPerMinute: 45,
    messageCount: 120,
    lagHintMs: 8,
  }),
}));

const mockSignals: AdvisorySignal[] = [
  {
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
    explainability_summary: { rsi_14: 0.324, macd_hist: 0.182, momentum_z: 0.441 },
    state_transition_history: ["draft", "validated", "emitted"],
    audit_correlation_id: "audit-sig-001",
  },
  {
    signal_id: "sig-002",
    created_at: "2026-08-13T09:45:00Z",
    as_of_time: "2026-08-13T09:45:00Z",
    market_class: "forex",
    provider: "model.ensemble.v1",
    symbol: "EURUSD",
    timeframe: "1m",
    model_artifact_id: "model.eurusd.classifier",
    model_version: "1.4.2",
    feature_set_version: "feat.m1.v2",
    experiment_id: "exp-001",
    statistical_report_id: "stat-002",
    calibration_report_id: "val-002", // Unbracketed / unsupplied interval
    economic_report_id: "econ-002",
    generalization_report_id: "gen-002",
    inference_input_hash: "b2c3d4e5f6a1b2789012345678abcdef02",
    raw_score: 0.520,
    calibrated_confidence: 0.480,
    input_staleness_seconds: 900,
    signal_validity_seconds: 60,
    expires_at: "2026-08-13T09:46:00Z",
    freshness_status: "expired",
    signal_direction: "NEUTRAL_BIAS",
    signal_state: "expired",
    state_reason: "High volatility regime threshold exceeded",
    eligibility_reasons: [],
    operating_domain_status: "out_of_domain",
    calibration_status: "warning:uncalibrated",
    economic_verdict: "cost_unfavorable",
    risk_notes: "Regime transition uncertainty.",
    rationale: "Uncertain regime; signal withheld from action.",
    explainability_summary: { rsi_14: 0.501, macd_hist: 0.002 },
    state_transition_history: ["draft", "expired"],
    audit_correlation_id: "audit-sig-002",
  },
];

const mockValidationReports: SignalValidationReport[] = [
  {
    id: "val-001",
    created_at: "2026-08-13T09:00:00Z",
    artifact_type: "signal_validation_report",
    method_version: "w3-u01.validation.v1",
    sample_count: 500,
    metrics: {
      win_rate: 0.612,
      calibrated_confidence_coverage: {
        value: 0.784,
        uncertainty: { lower: 0.724, upper: 0.841 },
      },
      clean_advisory_rate: {
        value: 0.824,
        uncertainty: { lower: 0.789, upper: 0.854 },
      },
      guardrail_intervention_rate: {
        value: 0.176,
        uncertainty: { lower: 0.146, upper: 0.211 },
      },
    },
    uncertainty: {
      lower: 0.724,
      upper: 0.841,
      confidence_level: 0.95,
      method: "wilson_score_interval",
    },
    limitations: ["Simulated backtest", "Zero execution warranty"],
    report_hash: "val-hash-01",
    research_status: "research_only",
  },
  {
    id: "val-002",
    created_at: "2026-08-13T09:00:00Z",
    artifact_type: "signal_validation_report",
    method_version: "w3-u01.validation.v1",
    sample_count: 500,
    metrics: {},
    uncertainty: {}, // Missing uncertainty bounds
    limitations: [],
    report_hash: "val-hash-02",
    research_status: "research_only",
  },
];

const mockCandles: ApiCandle[] = [
  {
    id: "c1",
    market_class: "forex",
    symbol: "EURUSD",
    timeframe: "1m",
    open_time: "2026-08-13T11:59:00Z",
    open: "1.08200",
    high: "1.08500",
    low: "1.08100",
    close: "1.08450",
    volume: "1000",
    source: "seed:synthetic",
    created_at: "2026-08-13T12:00:00Z",
  },
];

beforeEach(() => {
  vi.clearAllMocks();
  vi.mocked(client.fetchAdvisorySignals).mockResolvedValue(mockSignals);
  vi.mocked(client.fetchSignalValidationReports).mockResolvedValue(mockValidationReports);
  vi.mocked(client.fetchCandles).mockResolvedValue({ kind: "native", timeframe: "M1", bars: mockCandles });
  vi.mocked(client.fetchCorrelationReports).mockResolvedValue([]);
  vi.mocked(client.fetchRegimeReports).mockResolvedValue([]);
});

describe("UI-CONV-P02 Duplicate Surface Absorption & Single Statistical Code Path (B-CONV2-1..4)", () => {
  // Test 1 (Mandatory named test #1 — B-CONV2-1 Single Shared Calibrated Confidence Component)
  it("test_uiconv_p02_calibrated_confidence_renders_through_exactly_one_shared_component", () => {
    // 1. Valid bracketed confidence (78.4% in [72.4%, 84.1%])
    const { rerender } = render(
      <CalibratedConfidenceBadge
        confidence={0.784}
        uncertainty={{ lower: 0.724, upper: 0.841, method: "wilson_score_interval" }}
        testId="test-conf-1"
      />,
    );
    expect(screen.getByTestId("test-conf-1")).toHaveTextContent("78.4% · Wilson: [72.4% – 84.1%]");

    // 2. Unbracketed / missing uncertainty interval -> explicit qualifier
    rerender(
      <CalibratedConfidenceBadge
        confidence={0.480}
        uncertainty={null}
        testId="test-conf-2"
      />,
    );
    expect(screen.getByTestId("test-conf-2")).toHaveTextContent("48.0% · [Uncertainty: Unavailable]");

    // 3. Null / NaN confidence value -> Unavailable
    rerender(
      <CalibratedConfidenceBadge
        confidence={null}
        uncertainty={null}
        testId="test-conf-3"
      />,
    );
    expect(screen.getByTestId("test-conf-3")).toHaveTextContent("Unavailable · [Uncertainty: Unavailable]");
  });

  // Test 2 (Mandatory named test #2 — B-CONV2-1 Zero Bare Confidence Percentages)
  it("test_uiconv_p02_no_bare_confidence_percentage_renders_anywhere_in_frontend", async () => {
    render(
      <MemoryRouter>
        <TradingTerminalWorkspace initialSymbol="EUR/USD" />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByTestId("signal-card-sig-001")).toBeInTheDocument();
    });

    // Inspect all rendered confidence metrics in Signal Stream
    const conf1 = screen.getByTestId("signal-confidence-sig-001");
    expect(conf1.textContent).toMatch(/78\.4%\s*·\s*Wilson:\s*\[72\.4%\s*–\s*84\.1%\]/);

    const conf2 = screen.getByTestId("signal-confidence-sig-002");
    expect(conf2.textContent).toMatch(/48\.0%\s*·\s*\[Uncertainty:\s*Unavailable\]/);

    // Verify zero naked percentages exist in confidence badges
    const allBadges = screen.getAllByTestId(/^signal-confidence-/);
    for (const badge of allBadges) {
      expect(badge.textContent).toMatch(/(Wilson:|\[Uncertainty: Unavailable\])/);
      expect(badge.textContent).not.toMatch(/^\d+\.\d+%\s*$/); // Naked percentage prohibited
    }
  });

  // Test 3 (Mandatory named test #3 — B-CONV2-1 Strict Bracketing Invariant Across Metrics)
  it("test_uiconv_p02_every_rendered_interval_brackets_its_own_point_estimate", () => {
    // Test metric with interval component
    const { rerender } = render(
      <MetricWithInterval
        label="Historical Max Drawdown"
        value={-0.142}
        uncertainty={{ lower: -0.185, upper: -0.112 }}
        isPercentage={true}
        testId="metric-dd"
      />,
    );

    expect(screen.getByTestId("metric-dd-val")).toHaveTextContent("-14.2%");
    expect(screen.getByTestId("metric-dd-unc")).toHaveTextContent("CI: [-18.5% – -11.2%]");

    // Test invalid unbracketed interval -> surfaces [Uncertainty: Unavailable]
    rerender(
      <MetricWithInterval
        label="Corrupted Metric"
        value={0.95}
        uncertainty={{ lower: 0.10, upper: 0.50 }} // 0.95 outside [0.10, 0.50]
        isPercentage={true}
        testId="metric-bad"
      />,
    );

    expect(screen.getByTestId("metric-bad-val")).toHaveTextContent("95.0%");
    expect(screen.getByTestId("metric-bad-unc")).toHaveTextContent("[Uncertainty: Unavailable]");
  });

  // Test 4 (Mandatory named test #4 — B-CONV2-2 Retired Routes Redirect to Terminal with Correct Dock)
  it("test_uiconv_p02_retired_routes_redirect_to_terminal_with_correct_dock_active", async () => {
    // 1. /signals redirects to /?dock=signals (SIGNALS dock active)
    const { unmount: unmount1 } = render(
      <MemoryRouter initialEntries={["/signals"]}>
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

    await waitFor(() => {
      expect(screen.getByTestId("terminal-signal-stream")).toBeInTheDocument();
      expect(screen.getByTestId("right-dock-tab-signals")).toHaveClass("active");
    });
    unmount1();

    // 2. /analytics redirects to /?dock=intelligence (INTELLIGENCE dock active)
    const { unmount: unmount2 } = render(
      <MemoryRouter initialEntries={["/analytics"]}>
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

    await waitFor(() => {
      expect(screen.getByTestId("terminal-intelligence-cards")).toBeInTheDocument();
      expect(screen.getByTestId("right-dock-tab-intelligence")).toHaveClass("active");
    });
    unmount2();

    // 3. /charts redirects to / (Chart Stage active)
    const { unmount: unmount3 } = render(
      <MemoryRouter initialEntries={["/charts"]}>
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

    await waitFor(() => {
      expect(screen.getByTestId("terminal-chart-stage")).toBeInTheDocument();
    });
    unmount3();
  });

  // Test 5 (Mandatory named test #5 — B-CONV2-2 Signal Detail Drill-Down Exposes Full Lineage)
  it("test_uiconv_p02_signal_detail_exposes_rationale_guardrails_lineage_and_explainability", async () => {
    render(
      <MemoryRouter>
        <TradingTerminalWorkspace initialSymbol="EUR/USD" />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByTestId("signal-card-sig-001")).toBeInTheDocument();
    });

    // Click signal card to open detail drill-down
    const card = screen.getByTestId("signal-card-sig-001");
    fireEvent.click(card);

    // 1. Verbatim Rationale
    const rationale = screen.getByTestId("signal-detail-rationale-sig-001");
    expect(rationale).toHaveTextContent("Multi-timeframe momentum alignment with order flow imbalance.");

    // 2. Guardrails & State Criteria
    const guardrails = screen.getByTestId("signal-detail-guardrails-sig-001");
    expect(guardrails).toHaveTextContent("in_domain");
    expect(guardrails).toHaveTextContent("cost_favorable");
    expect(guardrails).toHaveTextContent("calibrated");

    // 3. Lineage & Model Identification
    const lineage = screen.getByTestId("signal-detail-lineage-sig-001");
    expect(lineage).toHaveTextContent("model.eurusd.classifier");
    expect(lineage).toHaveTextContent("feat.m1.v2");
    expect(lineage).toHaveTextContent("exp-001");
    expect(lineage).toHaveTextContent("val-001");

    // 4. Risk Disclosures
    const risk = screen.getByTestId("signal-detail-risk-sig-001");
    expect(risk).toHaveTextContent("Elevated spread risk during session rollover.");

    // 5. Explainability Feature Attribution
    const explainability = screen.getByTestId("signal-detail-explainability-sig-001");
    expect(explainability).toHaveTextContent("rsi_14:");
    expect(explainability).toHaveTextContent("0.3240");
    expect(explainability).toHaveTextContent("macd_hist:");
    expect(explainability).toHaveTextContent("0.1820");
  });

  // Test 6 (Mandatory named test #6 — B-CONV2-2 Every Retired Page Capability Has a Verified Home)
  it("test_uiconv_p02_every_retired_page_capability_has_a_verified_new_home", async () => {
    render(
      <MemoryRouter>
        <TradingTerminalWorkspace initialSymbol="EUR/USD" />
      </MemoryRouter>,
    );

    // 1. Chart history seeding & synthetic bar injection -> TerminalChartStage
    expect(screen.getByTestId("chart-seed-btn")).toBeInTheDocument();
    expect(screen.getByTestId("chart-provenance-badge")).toBeInTheDocument();

    // 2. Timeframe switching & TD-029 notice -> TerminalChartStage
    expect(screen.getByTestId("chart-tf-1m")).toBeInTheDocument();
    expect(screen.getByTestId("chart-tf-1h")).toBeInTheDocument();
    // DATA-P02: the notice now renders from the server series discriminant —
    // await the native series landing before asserting its label.
    await waitFor(() => {
      expect(screen.getByTestId("timeframe-native-notice")).toHaveTextContent("Native M1 Stream");
    });

    // 3. Presentation overlays -> TerminalChartStage
    expect(screen.getByTestId("overlay-sma20")).toBeInTheDocument();
    expect(screen.getByTestId("overlay-sma50")).toBeInTheDocument();
    expect(screen.getByTestId("overlay-ema20")).toBeInTheDocument();

    // 4. Research annotations write seam -> TerminalChartStage
    expect(screen.getByTestId("chart-add-annotation-btn")).toBeInTheDocument();

    // 5. Signal filters & detail drill-down -> TerminalSignalStream
    expect(screen.getByTestId("signal-filter-all")).toBeInTheDocument();
    expect(screen.getByTestId("signal-filter-emitted")).toBeInTheDocument();
    expect(screen.getByTestId("signal-filter-withheld")).toBeInTheDocument();

    // 6. Switch to Intelligence dock tab -> Model Calibration & Validation metrics
    const intelTab = screen.getByTestId("right-dock-tab-intelligence");
    fireEvent.click(intelTab);

    await waitFor(() => {
      expect(screen.getByTestId("intel-calibration-panel")).toBeInTheDocument();
      expect(screen.getByTestId("val-calibrated-coverage")).toBeInTheDocument();
      expect(screen.getByTestId("val-clean-advisory")).toBeInTheDocument();
      expect(screen.getByTestId("val-guardrail-rate")).toBeInTheDocument();
    });
  });

  // Test 7 (Mandatory named test #7 — B-CONV2-4 Seed and Live Provenance Labels Survive Absorption)
  it("test_uiconv_p02_seed_and_live_provenance_labels_survive_absorption", async () => {
    render(
      <MemoryRouter>
        <TradingTerminalWorkspace initialSymbol="EUR/USD" />
      </MemoryRouter>,
    );

    // 1. Ticker posture badge
    expect(screen.getByTestId("ticker-posture-badge")).toHaveTextContent("live:simulated");

    // 2. Chart provenance badge (awaited — bars land asynchronously)
    await waitFor(() => {
      expect(screen.getByTestId("chart-provenance-badge")).toHaveTextContent("live:simulated");
    });

    // 3. Telemetry posture badge (in telemetry dock)
    const telemetryTab = screen.getByTestId("right-dock-tab-telemetry");
    fireEvent.click(telemetryTab);

    await waitFor(() => {
      expect(screen.getByTestId("telemetry-posture-badge")).toHaveTextContent("live:simulated");
    });
  });

  // Test 7b (Mandatory named test — CA-CONV2-1 Command Palette Empty-Query Enumeration)
  it("test_uiconv_p02_command_palette_empty_query_enumerates_all_post_absorption_destinations", async () => {
    // 1. Route reconciliation: every registered workspace must be covered by a palette navigation command.
    const catalogueRouteTargets = QUICK_ACTION_CATALOGUE.filter((cmd) => cmd.target.kind === "route");
    const coveredWorkspaceIds = new Set(
      catalogueRouteTargets.map((cmd) => (cmd.target as { workspaceId?: string }).workspaceId),
    );
    for (const workspace of WORKSPACE_REGISTRY) {
      // monitor.chart_alias is the /chart compatibility alias of monitor.chart_workspace and
      // shares the same palette destination (Open Chart Stage). Every other registered
      // workspace must carry its own palette navigation command.
      if (workspace.id === "monitor.chart_alias") continue;
      expect(
        coveredWorkspaceIds.has(workspace.id),
        `workspace ${workspace.id} lacks palette coverage`,
      ).toBe(true);
    }

    // 2. Absorbed surfaces must be relabeled to — and target — their canonical post-absorption destinations.
    const chartsCmd = QUICK_ACTION_CATALOGUE.find((cmd) => cmd.id === "qa.open.charts");
    const signalsCmd = QUICK_ACTION_CATALOGUE.find((cmd) => cmd.id === "qa.open.signals");
    const analyticsCmd = QUICK_ACTION_CATALOGUE.find((cmd) => cmd.id === "qa.open.analytics");
    expect(chartsCmd?.label).toBe("Open Chart Stage");
    expect(chartsCmd?.target).toEqual({ kind: "route", route: "/?view=chart", workspaceId: "monitor.chart_workspace" });
    expect(signalsCmd?.label).toBe("Open Signals Dock");
    expect(signalsCmd?.target).toEqual({ kind: "route", route: "/?dock=signals", workspaceId: "research.advisory_signals" });
    expect(analyticsCmd?.label).toBe("Open Intelligence Dock");
    expect(analyticsCmd?.target).toEqual({ kind: "route", route: "/?dock=intelligence", workspaceId: "research.analytics" });

    // 3. Integration: empty-query palette renders the FULL catalogue (count asserted) — not a clipped subset.
    render(
      <MemoryRouter initialEntries={["/"]}>
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

    fireEvent.keyDown(window, { key: "k", ctrlKey: true });
    const dialog = await screen.findByRole("dialog", { name: "Command palette" });

    const items = within(dialog).getAllByRole("menuitem");
    expect(items.length).toBe(QUICK_ACTION_CATALOGUE.length);

    expect(within(dialog).getByText("Open Chart Stage")).toBeInTheDocument();
    expect(within(dialog).getByText("Open Signals Dock")).toBeInTheDocument();
    expect(within(dialog).getByText("Open Intelligence Dock")).toBeInTheDocument();
    expect(within(dialog).queryByText("Open Chart Workspace")).not.toBeInTheDocument();
    expect(within(dialog).queryByText("Open Advisory Signals")).not.toBeInTheDocument();
    expect(within(dialog).queryByText("Open Performance Analytics")).not.toBeInTheDocument();

    // 4. Selecting "Open Chart Stage" navigates to the terminal Chart Stage (post-absorption destination).
    fireEvent.click(within(dialog).getByText("Open Chart Stage"));
    await waitFor(() => {
      expect(screen.getByTestId("terminal-chart-stage")).toBeInTheDocument();
    });
  });

  // Test 8 (Mandatory named test #8 — B-CONV2-3 Zero Ad-Hoc Hex Across Whole Frontend)
  it("test_uiconv_p02_zero_adhoc_hex_across_whole_frontend_outside_tokens_css", () => {
    const srcDir = path.resolve(__dirname, "../");
    const allFiles: string[] = [];

    function collectFiles(dir: string) {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory()) {
          if (!["node_modules", "dist", "build", "coverage"].includes(entry.name)) {
            collectFiles(fullPath);
          }
        } else if (
          (entry.name.endsWith(".tsx") || entry.name.endsWith(".ts") || entry.name.endsWith(".css")) &&
          !entry.name.includes(".test.") &&
          entry.name !== "tokens.css"
        ) {
          allFiles.push(fullPath);
        }
      }
    }

    collectFiles(srcDir);

    for (const filePath of allFiles) {
      const content = fs.readFileSync(filePath, "utf8");
      const hexMatches = content.match(/#[0-9a-fA-F]{3,8}\b/g) || [];
      expect(
        hexMatches.length,
        `Found ad-hoc hex in ${path.relative(srcDir, filePath)}: ${hexMatches.join(", ")}`,
      ).toBe(0);
    }
  });
});
