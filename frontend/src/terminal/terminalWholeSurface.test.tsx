import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { MemoryRouter } from "react-router-dom";
import { TradingTerminalWorkspace } from "../components/terminal/TradingTerminalWorkspace";
import type { SymbolQuote } from "../live/types";
import type {
  AdvisorySignal,
  ApiCandle,
  ManualJournalEntry,
  PortfolioRiskReport,
  ScenarioReport,
  SignalValidationReport,
  TradePlanNote,
} from "../api/client";
import * as client from "../api/client";

// Mock API Client
vi.mock("../api/client", async () => {
  const actual = await vi.importActual<typeof client>("../api/client");
  return {
    ...actual,
    fetchTradePlans: vi.fn(),
    createTradePlan: vi.fn(),
    updateTradePlan: vi.fn(),
    fetchJournalEntries: vi.fn(),
    createJournalEntry: vi.fn(),
    updateJournalEntry: vi.fn(),
    fetchPortfolioRiskReports: vi.fn(),
    fetchScenarioReports: vi.fn(),
    fetchAdvisorySignals: vi.fn(),
    fetchSignalValidationReports: vi.fn(),
    fetchCorrelationReports: vi.fn(),
    fetchRegimeReports: vi.fn(),
    fetchCandles: vi.fn(),
    fetchChartResearchAnnotations: vi.fn(),
  };
});

// Mock PriceChart to avoid Canvas2D rendering errors in JSDOM
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

// Mock Live Market WebSocket hook
const mockQuotes: Record<string, SymbolQuote> = {
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
  "GBP/USD": {
    symbol: "GBP/USD",
    marketClass: "forex",
    timeframe: "1m",
    open: "1.28800",
    high: "1.29500",
    low: "1.28700",
    close: "1.29150",
    volume: "9800000",
    openTime: "2026-08-13T12:00:00Z",
    source: "simulated",
    updatedAt: "2026-08-13T12:00:00Z",
  },
  "USD/JPY": {
    symbol: "USD/JPY",
    marketClass: "forex",
    timeframe: "1m",
    open: "145.900",
    high: "146.800",
    low: "145.750",
    close: "146.300",
    volume: "18500000",
    openTime: "2026-08-13T12:00:00Z",
    source: "simulated",
    updatedAt: "2026-08-13T12:00:00Z",
  },
};

vi.mock("../hooks/useLiveMarket", () => ({
  useLiveMarket: () => ({
    quotes: mockQuotes,
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
    source: "simulated",
    created_at: "2026-08-13T12:00:00Z",
  },
  {
    id: "c2",
    market_class: "forex",
    symbol: "EURUSD",
    timeframe: "1m",
    open_time: "2026-08-13T12:00:00Z",
    open: "1.08450",
    high: "1.08600",
    low: "1.08400",
    close: "1.08550",
    volume: "1200",
    source: "simulated",
    created_at: "2026-08-13T12:01:00Z",
  },
];

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
];

const mockValidationReports: SignalValidationReport[] = [
  {
    id: "val-001",
    created_at: "2026-08-13T09:00:00Z",
    artifact_type: "signal_validation_report",
    method_version: "w3-u01.validation.v1",
    sample_count: 500,
    metrics: { win_rate: 0.612, sharpe: 1.45 },
    uncertainty: {
      lower: 0.568,
      upper: 0.654,
      confidence_level: 0.95,
      method: "wilson_score_interval",
    },
    limitations: ["Simulated backtest", "Zero execution warranty"],
    report_hash: "val-hash-01",
    research_status: "research_only",
  },
];

const mockTradePlans: TradePlanNote[] = [
  {
    plan_id: "plan-001",
    created_at: "2026-08-13T10:00:00Z",
    updated_at: "2026-08-13T10:00:00Z",
    operator_id: "operator_01",
    title: "London Open Momentum Thesis",
    market_context: "EUR/USD M1 London Open breakout",
    hypothesis: "Order flow imbalance creates short-term upward momentum.",
    linked_signal_ids: ["sig-001"],
    linked_report_ids: ["val-001"],
    scenario_notes: "Dependent on ECB rate pause stability.",
    risk_notes: "Rollover spread risk during Asian transition.",
    invalidating_conditions_text: "Spread widening above 1.5 pips or volume dry-up.",
    decision_status: "reviewed",
    research_disclaimer:
      "Trade plan research note only. Hypothetical research, not financial advice, not a trade instruction, not an order ticket. Operator judgment required. AXIOM does not act.",
    research_status: "research_only",
    audit_correlation_id: "audit-plan-001-abc",
  },
  {
    plan_id: "plan-002",
    created_at: "2026-08-13T08:00:00Z",
    updated_at: "2026-08-13T09:30:00Z", // Edited record
    operator_id: "operator_01",
    title: "Mean Reversion at Bollinger Band",
    market_context: "EUR/USD M1 Overextended Range",
    hypothesis: "Mean reversion expected following 2.5 sigma excursion.",
    linked_signal_ids: [],
    linked_report_ids: [],
    scenario_notes: null,
    risk_notes: "News release volatility.",
    invalidating_conditions_text: "Breakout beyond 3.0 sigma.",
    decision_status: "draft",
    research_disclaimer:
      "Trade plan research note only. Hypothetical research, not financial advice, not a trade instruction, not an order ticket. Operator judgment required. AXIOM does not act.",
    research_status: "research_only",
    audit_correlation_id: "audit-plan-002-def",
  },
];

const mockJournalEntries: ManualJournalEntry[] = [
  {
    journal_id: "journ-001",
    created_at: "2026-08-13T11:00:00Z",
    updated_at: "2026-08-13T11:00:00Z",
    operator_id: "operator_01",
    title: "Session Execution Reflection",
    reflection_text:
      "Maintained strict patience during high spread environment; respected invalidating condition.",
    linked_plan_id: "plan-001",
    linked_signal_ids: ["sig-001"],
    linked_report_ids: [],
    emotion_tags: ["disciplined", "patient"],
    process_tags: ["followed_checklist", "logged_hypothesis"],
    lesson_notes: "Avoid entering before London liquidity injection confirms.",
    research_disclaimer:
      "Manual research journal entry only. Not financial advice, not a trade record, not a trade instruction. Operator judgment required. AXIOM does not act.",
    research_status: "research_only",
    audit_correlation_id: "audit-journ-001-ghi",
  },
  {
    journal_id: "journ-002",
    created_at: "2026-08-13T07:00:00Z",
    updated_at: "2026-08-13T08:15:00Z", // Edited record
    operator_id: "operator_01",
    title: "Asian Range Boundary Review",
    reflection_text: "Observed tight compression prior to European crossover.",
    linked_plan_id: null,
    linked_signal_ids: [],
    linked_report_ids: [],
    emotion_tags: ["observant"],
    process_tags: ["spread_monitored"],
    lesson_notes: "Keep position size zero in presentation mode.",
    research_disclaimer:
      "Manual research journal entry only. Not financial advice, not a trade record, not a trade instruction. Operator judgment required. AXIOM does not act.",
    research_status: "research_only",
    audit_correlation_id: "audit-journ-002-jkl",
  },
];

const mockRiskReport: PortfolioRiskReport = {
  id: "risk-001",
  created_at: "2026-08-13T09:00:00Z",
  artifact_type: "portfolio_risk_report",
  method_version: "w4-u05.market_series_risk_pure_python.v1",
  market_class: "forex",
  symbol: "EURUSD",
  timeframe: "M1",
  as_of_start: "2026-08-06T00:00:00Z",
  as_of_end: "2026-08-13T00:00:00Z",
  sample_count: 500,
  max_drawdown: -0.142,
  realized_volatility: 0.118,
  stress_loss: -0.225,
  metrics: {
    max_drawdown: -0.142,
    realized_volatility: 0.118,
    stress_loss: -0.225,
  },
  uncertainty: {
    max_drawdown: {
      lower: -0.185,
      upper: -0.112,
      confidence_level: 0.95,
      method: "bootstrap_percentile",
    },
    realized_volatility: {
      lower: 0.095,
      upper: 0.138,
      confidence_level: 0.95,
      method: "chi_square_interval",
    },
    stress_loss: {
      lower: -0.285,
      upper: -0.182,
      confidence_level: 0.95,
      method: "historical_simulation",
    },
  },
  assumptions: {
    stress_multiplier: 2.0,
    tail_quantile: 0.05,
    scenario_horizon: "1-day",
  },
  economic_usefulness: { verdict: "not_assessed" },
  config: {},
  input_lineage: { source: "market_candles" },
  source_artifact_ids: [],
  market_scope: { symbol: "EURUSD" },
  results: {},
  limitations: ["Historical research only", "Zero execution guarantee"],
  report_hash: "risk-hash-01",
  research_status: "research_only",
  created_by: "system",
  audit_correlation_id: "audit-risk-001",
  notes: "Portfolio risk analytics report",
};

const mockScenarioReport: ScenarioReport = {
  id: "scen-001",
  created_at: "2026-08-13T09:00:00Z",
  artifact_type: "scenario_report",
  method_version: "w4-u04.scenario_shock.v1",
  market_class: "forex",
  symbol: "EURUSD",
  timeframe: "M1",
  as_of_start: "2026-08-06T00:00:00Z",
  as_of_end: "2026-08-13T00:00:00Z",
  sample_count: 500,
  scenario_name: "Hawkish Central Bank Rate Shock",
  hypothetical_return: -0.084,
  scenario_result: { shock_magnitude_bps: 75 },
  assumptions: { rate_hike_bps: 75, volatility_multiplier: 1.8 },
  inputs: {},
  uncertainty: {
    lower: -0.115,
    upper: -0.053,
    confidence_level: 0.95,
    method: "bootstrap_quantile",
  },
  economic_usefulness: { verdict: "not_assessed" },
  config: {},
  input_lineage: { source: "market_candles" },
  source_artifact_ids: [],
  market_scope: { symbol: "EURUSD" },
  results: {},
  limitations: ["Hypothetical model shock only", "No trading warranty"],
  report_hash: "scen-hash-01",
  research_status: "research_only",
  created_by: "system",
  audit_correlation_id: "audit-scen-001",
  notes: "Macro shock simulation",
};

beforeEach(() => {
  vi.clearAllMocks();
  vi.mocked(client.fetchCandles).mockResolvedValue({ kind: "native", timeframe: "M1", bars: mockCandles });
  vi.mocked(client.fetchChartResearchAnnotations).mockResolvedValue([]);
  vi.mocked(client.fetchAdvisorySignals).mockResolvedValue(mockSignals);
  vi.mocked(client.fetchSignalValidationReports).mockResolvedValue(mockValidationReports);
  vi.mocked(client.fetchCorrelationReports).mockResolvedValue([]);
  vi.mocked(client.fetchRegimeReports).mockResolvedValue([]);
  vi.mocked(client.fetchTradePlans).mockResolvedValue(mockTradePlans);
  vi.mocked(client.fetchJournalEntries).mockResolvedValue(mockJournalEntries);
  vi.mocked(client.fetchPortfolioRiskReports).mockResolvedValue([mockRiskReport]);
  vi.mocked(client.fetchScenarioReports).mockResolvedValue([mockScenarioReport]);
});

describe("UI-NEW-P06 Whole-Terminal Integration & Visual Audit (B-P06-1..5)", () => {
  // Test 1 (Mandatory named test #1 — B-P06-1 Whole-Surface Composition)
  it("test_uinew_p06_all_five_terminal_zones_mount_together_without_dom_collision", async () => {
    render(
      <MemoryRouter>
        <TradingTerminalWorkspace initialSymbol="EUR/USD" />
      </MemoryRouter>,
    );

    // Verify root workspace container
    expect(screen.getByTestId("trading-terminal-workspace")).toBeInTheDocument();
    expect(screen.getByTestId("terminal-multipane-layout")).toBeInTheDocument();

    // Verify all 5 terminal zones mount together cleanly with non-colliding ARIA landmark roles:
    // 1. Zone 1: Top Ticker Header (P01) -> role="banner"
    const banner = screen.getByRole("banner", { name: "Global Terminal Ticker Bar" });
    expect(banner).toBeInTheDocument();
    expect(screen.getByTestId("terminal-top-ticker")).toBeInTheDocument();

    // 2. Zone 2: Watchlist Dock (P02) -> role="complementary" (left slot)
    const watchlistSlot = screen.getByRole("complementary", { name: "Market Watchlist Dock" });
    expect(watchlistSlot).toBeInTheDocument();
    expect(screen.getByTestId("terminal-watchlist-dock")).toBeInTheDocument();

    // 3. Zone 3: Primary Candlestick Chart Stage (P03) -> role="main"
    const chartStage = screen.getByRole("main", { name: "Primary Candlestick Chart Stage" });
    expect(chartStage).toBeInTheDocument();
    expect(screen.getByTestId("terminal-chart-stage")).toBeInTheDocument();

    // 4. Zone 4: Right Dock (Signals / Telemetry / Intelligence) (P04) -> role="complementary" (right slot)
    const rightDock = screen.getByRole("complementary", { name: "Signals & Telemetry Dock" });
    expect(rightDock).toBeInTheDocument();
    expect(screen.getByTestId("right-dock-container")).toBeInTheDocument();

    // 5. Zone 5: Bottom Dock (Risk, Journal, Trade Plans, Scenarios) (P05) -> role="region"
    const bottomDock = screen.getByRole("region", { name: "Terminal Analytics Dock" });
    expect(bottomDock).toBeInTheDocument();
    expect(screen.getByTestId("terminal-bottom-dock")).toBeInTheDocument();

    // Assert zero DOM id collisions across all mounted zones
    const allElementsWithId = document.querySelectorAll("[id]");
    const idSet = new Set<string>();
    allElementsWithId.forEach((el) => {
      expect(idSet.has(el.id)).toBe(false);
      idSet.add(el.id);
    });
  });

  // Test 2 (Mandatory named test #2 — B-P06-1 Symbol Context Propagation)
  it("test_uinew_p06_symbol_selection_propagates_to_chart_telemetry_signals_and_risk", async () => {
    render(
      <MemoryRouter>
        <TradingTerminalWorkspace initialSymbol="EUR/USD" />
      </MemoryRouter>,
    );

    // Initial state: EUR/USD
    expect(screen.getByTestId("ticker-symbol-badge")).toHaveTextContent("EUR/USD");
    expect(screen.getByTestId("chart-symbol-badge")).toHaveTextContent("EUR/USD");

    // Select GBP/USD in Watchlist Dock
    const gbpItem = screen.getByTestId("watchlist-row-gbp-usd");
    expect(gbpItem).toBeInTheDocument();
    fireEvent.click(gbpItem);

    // Verify propagation across all terminal zones:
    // 1. Ticker Header updates
    await waitFor(() => {
      expect(screen.getByTestId("ticker-symbol-badge")).toHaveTextContent("GBP/USD");
    });

    // 2. Chart Stage updates
    expect(screen.getByTestId("chart-symbol-badge")).toHaveTextContent("GBP/USD");

    // 3. Switch Right Dock to TELEMETRY tab and verify GBP/USD telemetry
    const telemetryTab = screen.getByTestId("right-dock-tab-telemetry");
    fireEvent.click(telemetryTab);
    await waitFor(() => {
      expect(screen.getByTestId("terminal-market-telemetry")).toBeInTheDocument();
      expect(screen.getByTestId("telemetry-instrument-section")).toHaveTextContent("GBP/USD");
    });

    // 4. Switch Bottom Dock to RISK tab and verify active symbol context
    const riskTab = screen.getByTestId("bottom-tab-risk");
    fireEvent.click(riskTab);
    await waitFor(() => {
      expect(screen.getByTestId("terminal-risk-panel")).toBeInTheDocument();
    });
  });

  // Test 3 (Mandatory named test #3 — B-P06-1 Pane Stability on Dock Tab Switching)
  it("test_uinew_p06_dock_tab_switching_does_not_unmount_or_disturb_sibling_panes", async () => {
    render(
      <MemoryRouter>
        <TradingTerminalWorkspace initialSymbol="EUR/USD" />
      </MemoryRouter>,
    );

    // Verify baseline stage presence
    expect(screen.getByTestId("terminal-chart-stage")).toBeInTheDocument();
    expect(screen.getByTestId("terminal-watchlist-dock")).toBeInTheDocument();
    expect(screen.getByTestId("terminal-top-ticker")).toBeInTheDocument();

    // 1. Cycle Right Dock tabs: SIGNALS -> TELEMETRY -> INTELLIGENCE -> SIGNALS
    const rightSignalsTab = screen.getByTestId("right-dock-tab-signals");
    const rightTelemetryTab = screen.getByTestId("right-dock-tab-telemetry");
    const rightIntelligenceTab = screen.getByTestId("right-dock-tab-intelligence");

    fireEvent.click(rightTelemetryTab);
    expect(screen.getByTestId("terminal-market-telemetry")).toBeInTheDocument();
    expect(screen.getByTestId("terminal-chart-stage")).toBeInTheDocument();

    fireEvent.click(rightIntelligenceTab);
    expect(screen.getByTestId("terminal-intelligence-cards")).toBeInTheDocument();
    expect(screen.getByTestId("terminal-chart-stage")).toBeInTheDocument();

    fireEvent.click(rightSignalsTab);
    expect(screen.getByTestId("terminal-signal-stream")).toBeInTheDocument();
    expect(screen.getByTestId("terminal-chart-stage")).toBeInTheDocument();

    // 2. Cycle Bottom Dock tabs: TRADE_PLANS -> JOURNAL -> RISK -> SCENARIOS -> TRADE_PLANS
    const bottomPlansTab = screen.getByTestId("bottom-tab-trade-plans");
    const bottomJournalTab = screen.getByTestId("bottom-tab-journal");
    const bottomRiskTab = screen.getByTestId("bottom-tab-risk");
    const bottomScenariosTab = screen.getByTestId("bottom-tab-scenarios");

    fireEvent.click(bottomJournalTab);
    await waitFor(() => {
      expect(screen.getByTestId("journal-panel")).toBeInTheDocument();
    });
    expect(screen.getByTestId("terminal-chart-stage")).toBeInTheDocument();
    expect(screen.getByTestId("terminal-watchlist-dock")).toBeInTheDocument();

    fireEvent.click(bottomRiskTab);
    await waitFor(() => {
      expect(screen.getByTestId("terminal-risk-panel")).toBeInTheDocument();
    });
    expect(screen.getByTestId("terminal-chart-stage")).toBeInTheDocument();

    fireEvent.click(bottomScenariosTab);
    await waitFor(() => {
      expect(screen.getByTestId("terminal-scenarios-panel")).toBeInTheDocument();
    });
    expect(screen.getByTestId("terminal-chart-stage")).toBeInTheDocument();

    fireEvent.click(bottomPlansTab);
    await waitFor(() => {
      expect(screen.getByTestId("trade-plans-panel")).toBeInTheDocument();
    });
    expect(screen.getByTestId("terminal-chart-stage")).toBeInTheDocument();
  });

  // Test 4 (Mandatory named test #4 — B-P06-1 Governance Chips in Assembled Surface)
  it("test_uinew_p06_governance_chips_render_in_assembled_surface_not_only_in_units", async () => {
    render(
      <MemoryRouter>
        <TradingTerminalWorkspace initialSymbol="EUR/USD" />
      </MemoryRouter>,
    );

    // 1. Governance badge in Top Ticker
    const govBadge = screen.getByTestId("terminal-governance-badge");
    expect(govBadge).toBeInTheDocument();
    expect(screen.getByTestId("terminal-gov-gate")).toHaveTextContent("GATE: CLOSED");
    expect(screen.getByTestId("terminal-gov-posture")).toHaveTextContent(
      "RESEARCH-ONLY · NON-ACTUATING",
    );

    // 2. Data honesty posture tag in Top Ticker
    expect(screen.getByTestId("ticker-posture-badge")).toHaveTextContent("live:simulated");

    // 3. Bottom Dock Governance Header and SAL classification
    expect(screen.getByText("RESEARCH & ANALYTICS")).toBeInTheDocument();
    expect(screen.getAllByText("RESEARCH-ONLY · NON-ACTUATING").length).toBeGreaterThan(0);

    // 4. Disclaimers in Chart Stage and Watchlist Dock
    expect(screen.getAllByText(/live:simulated/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/NON-ACTUATING/i).length).toBeGreaterThan(0);
  });

  // Test 5 (Mandatory named test #5 — B-P06-3 Programme-Scope Zero Actuation/LLM/Orderbook/Secrets)
  it("test_uinew_p06_whole_frontend_contains_zero_actuation_llm_orderbook_or_secret_affordance", async () => {
    render(
      <MemoryRouter>
        <TradingTerminalWorkspace initialSymbol="EUR/USD" />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByTestId("trade-plans-panel")).toBeInTheDocument();
    });

    // Inspect all buttons across the assembled surface
    const allButtons = screen.getAllByRole("button");
    const buttonLabels = allButtons.map((b) => b.textContent?.trim().toLowerCase() ?? "");

    // Strict prohibition: zero buy/sell/execute/order controls
    const forbiddenButtonWords = [
      "buy",
      "sell",
      "place order",
      "submit order",
      "execute",
      "connect broker",
      "open gate",
      "allow execution",
      "trade now",
    ];

    for (const forbidden of forbiddenButtonWords) {
      for (const label of buttonLabels) {
        expect(label).not.toBe(forbidden);
      }
    }

    // Inspect all form fields: open create trade plan modal
    const createBtn = screen.getByTestId("add-trade-plan-btn");
    fireEvent.click(createBtn);

    const form = screen.getByTestId("trade-plan-modal");
    expect(form).toBeInTheDocument();

    // Verify zero order pricing, size, leverage, side, or broker inputs
    const forbiddenFieldNames = ["price", "stop_loss", "take_profit", "size", "lot", "side", "account"];
    forbiddenFieldNames.forEach((field) => {
      expect(form.querySelector(`[name="${field}"]`)).toBeNull();
    });

    // Verify no external LLM prompt inputs
    expect(document.querySelector("textarea[placeholder*='prompt']")).toBeNull();
    expect(document.querySelector("input[placeholder*='openai']")).toBeNull();

    // Verify no depth ladder or orderbook table
    expect(document.querySelector(".depth-ladder")).toBeNull();
    expect(document.querySelector(".orderbook-table")).toBeNull();
  });

  // Test 6 (Mandatory named test #6 — B-P06-1 Statistical Uncertainty Bracketing Generalisation)
  it("test_uinew_p06_every_rendered_statistical_value_carries_uncertainty_or_explicit_unavailable", async () => {
    render(
      <MemoryRouter>
        <TradingTerminalWorkspace initialSymbol="EUR/USD" />
      </MemoryRouter>,
    );

    // 1. Check Signal Stream uncertainty (P04)
    await waitFor(() => {
      expect(screen.getByTestId("signal-card-sig-001")).toBeInTheDocument();
    });
    expect(screen.getByTestId("signal-confidence-sig-001")).toHaveTextContent(/78\.4%/);

    // 2. Check Risk & Drawdown tab (P05)
    const riskTab = screen.getByTestId("bottom-tab-risk");
    fireEvent.click(riskTab);

    await waitFor(() => {
      expect(screen.getByTestId("terminal-risk-panel")).toBeInTheDocument();
    });

    // Check Max Historical Drawdown (-14.2% bracketed by [-18.5%, -11.2%])
    expect(screen.getByTestId("risk-max-drawdown-val")).toHaveTextContent(/-14\.2%/);
    expect(screen.getByTestId("risk-max-drawdown-unc")).toHaveTextContent(/-18\.5%/);
    expect(screen.getByTestId("risk-max-drawdown-unc")).toHaveTextContent(/-11\.2%/);

    // Check Realized Volatility (11.8% bracketed by [9.5%, 13.8%])
    expect(screen.getByTestId("risk-volatility-val")).toHaveTextContent(/11\.8%/);
    expect(screen.getByTestId("risk-volatility-unc")).toHaveTextContent(/9\.5%/);
    expect(screen.getByTestId("risk-volatility-unc")).toHaveTextContent(/13\.8%/);

    // Check Hypothetical Stress Loss (-22.5% bracketed by [-28.5%, -18.2%])
    expect(screen.getByTestId("risk-stress-loss-val")).toHaveTextContent(/-22\.5%/);
    expect(screen.getByTestId("risk-stress-loss-unc")).toHaveTextContent(/-28\.5%/);
    expect(screen.getByTestId("risk-stress-loss-unc")).toHaveTextContent(/-18\.2%/);

    // 3. Check Macro Scenarios tab (P05)
    const scenTab = screen.getByTestId("bottom-tab-scenarios");
    fireEvent.click(scenTab);

    await waitFor(() => {
      expect(screen.getByTestId("terminal-scenarios-panel")).toBeInTheDocument();
    });

    // Check scenario hypothetical return
    expect(screen.getByTestId("scenario-return-scen-001")).toHaveTextContent("Hypothetical: -8.40%");

    // Verify assumptions box is explicitly rendered
    expect(screen.getByTestId("scenario-assumptions-scen-001")).toHaveTextContent(/rate_hike_bps/i);
  });
});
