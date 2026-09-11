import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { TerminalProvider } from "../components/terminal/TerminalContext";
import { TerminalBottomDock } from "../components/terminal/TerminalBottomDock";
import { TerminalSignalStream } from "../components/terminal/TerminalSignalStream";
import type {
  AdvisorySignal,
  ManualJournalEntry,
  PortfolioRiskReport,
  ScenarioReport,
  SignalValidationReport,
  TradePlanNote,
} from "../api/client";
import * as client from "../api/client";

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
    fetchInstitutionalIntelligenceBundle: vi.fn().mockResolvedValue(null),
    fetchAdvisorySignals: vi.fn(),
    fetchSignalValidationReports: vi.fn(),
    fetchCandles: vi.fn().mockResolvedValue({ kind: "native", timeframe: "M1", bars: [] }),
    fetchChartResearchAnnotations: vi.fn().mockResolvedValue([]),
  };
});

const mockTradePlans: TradePlanNote[] = [
  {
    plan_id: "plan-001",
    created_at: "2026-08-13T10:00:00Z",
    updated_at: "2026-08-13T10:00:00Z", // Unedited
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
    updated_at: "2026-08-13T09:30:00Z", // Edited record (updated_at !== created_at)
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
    updated_at: "2026-08-13T08:15:00Z", // Edited entry
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
    upper: -0.055,
    confidence_level: 0.95,
  },
  economic_usefulness: { verdict: "not_assessed" },
  config: {},
  input_lineage: {},
  source_artifact_ids: [],
  market_scope: { symbol: "EURUSD" },
  results: {},
  limitations: ["Hypothetical simulation only"],
  report_hash: "scen-hash-01",
  research_status: "research_only",
  created_by: "system",
  audit_correlation_id: "audit-scen-001",
  notes: "Macro scenario shock report",
};

const mockP04Signals: AdvisorySignal[] = [
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
    statistical_report_id: null,
    calibration_report_id: "val-001",
    economic_report_id: null,
    generalization_report_id: null,
    inference_input_hash: "a1b2c3d4e5f6789012345678abcdef01",
    raw_score: 0.812,
    calibrated_confidence: 0.784, // 0.724 <= 0.784 <= 0.841 (bracketed)
    input_staleness_seconds: 4,
    signal_validity_seconds: 60,
    expires_at: "2099-08-13T10:01:00Z",
    freshness_status: "fresh",
    signal_direction: "LONG_BIAS",
    signal_state: "emitted",
    state_reason: "Domain criteria validated",
    eligibility_reasons: [],
    operating_domain_status: "in_domain",
    calibration_status: "calibrated",
    economic_verdict: "cost_favorable",
    risk_notes: null,
    rationale: "Momentum alignment.",
    explainability_summary: {},
    state_transition_history: ["draft", "emitted"],
    audit_correlation_id: "audit-sig-001",
  },
  {
    signal_id: "sig-002",
    created_at: "2026-08-13T09:30:00Z",
    as_of_time: "2026-08-13T09:30:00Z",
    market_class: "forex",
    provider: "model.ensemble.v1",
    symbol: "EURUSD",
    timeframe: "1m",
    model_artifact_id: "model.eurusd.classifier",
    model_version: "1.4.2",
    feature_set_version: "feat.m1.v2",
    experiment_id: "exp-001",
    statistical_report_id: null,
    calibration_report_id: "val-001",
    economic_report_id: null,
    generalization_report_id: null,
    inference_input_hash: "c3d4e5f6a1b2789012345678abcdef03",
    raw_score: 0.42,
    calibrated_confidence: 0.48, // 0.48 < 0.724 (OUTSIDE report aggregate interval -> must render unavailable)
    input_staleness_seconds: 12,
    signal_validity_seconds: 60,
    expires_at: "2026-08-13T09:31:00Z",
    freshness_status: "expired",
    signal_direction: "NEUTRAL",
    signal_state: "expired",
    state_reason: "Expired",
    eligibility_reasons: [],
    operating_domain_status: "out_of_domain",
    calibration_status: "uncalibrated",
    economic_verdict: "unverified",
    risk_notes: null,
    rationale: "Indeterminate.",
    explainability_summary: {},
    state_transition_history: ["draft", "expired"],
    audit_correlation_id: "audit-sig-002",
  },
];

const mockP04ValReport: SignalValidationReport = {
  id: "val-001",
  created_at: "2026-08-13T09:00:00Z",
  artifact_type: "signal_validation_report",
  method_version: "w4-u06.signal_validation.v1",
  sample_count: 520,
  metrics: {
    clean_advisory_rate: {
      value: 0.824,
      sample_count: 520,
      uncertainty: { lower: 0.789, upper: 0.854, method: "wilson_score_interval" },
    },
    calibrated_confidence_coverage: {
      value: 0.784,
      sample_count: 520,
      uncertainty: { lower: 0.724, upper: 0.841, method: "wilson_score_interval" },
    },
  },
  uncertainty: { lower: 0.724, upper: 0.841, method: "wilson_score_interval" },
  limitations: [],
  report_hash: "val-hash-01",
  research_status: "research_only",
};

beforeEach(() => {
  vi.clearAllMocks();
  vi.mocked(client.fetchTradePlans).mockResolvedValue(mockTradePlans);
  vi.mocked(client.fetchJournalEntries).mockResolvedValue(mockJournalEntries);
  vi.mocked(client.fetchPortfolioRiskReports).mockResolvedValue([mockRiskReport]);
  vi.mocked(client.fetchScenarioReports).mockResolvedValue([mockScenarioReport]);
  vi.mocked(client.fetchAdvisorySignals).mockResolvedValue(mockP04Signals);
  vi.mocked(client.fetchSignalValidationReports).mockResolvedValue([mockP04ValReport]);
});

describe("UI-NEW-P05 Risk, Portfolio Analytics & Research Journal (Eight Mandatory Tests)", () => {
  // Test 1: B-P05-1 Trade Plan Form Exposes ZERO price/stop/size/side fields
  it("test_uinew_p05_trade_plan_form_exposes_no_price_stop_target_size_or_side_fields", async () => {
    render(
      <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
        <TerminalBottomDock initialTab="TRADE_PLANS" />
      </TerminalProvider>,
    );

    // Open trade plan create modal
    await waitFor(() => {
      expect(screen.getByTestId("add-trade-plan-btn")).toBeInTheDocument();
    });
    fireEvent.click(screen.getByTestId("add-trade-plan-btn"));

    // Verify modal is open
    expect(screen.getByTestId("trade-plan-modal")).toBeInTheDocument();
    expect(screen.getByTestId("trade-plan-title-input")).toBeInTheDocument();
    expect(screen.getByTestId("trade-plan-hypothesis-input")).toBeInTheDocument();
    expect(screen.getByTestId("trade-plan-context-input")).toBeInTheDocument();
    expect(screen.getByTestId("trade-plan-status-select")).toBeInTheDocument();

    // Strict B-P05-1 check: Confirm NO order / execution / position fields exist in DOM
    const modalContent = screen.getByTestId("trade-plan-modal").textContent?.toLowerCase() ?? "";
    const modalHtml = screen.getByTestId("trade-plan-modal").innerHTML.toLowerCase();

    expect(modalHtml).not.toContain("name=\"price\"");
    expect(modalHtml).not.toContain("name=\"stop_loss\"");
    expect(modalHtml).not.toContain("name=\"take_profit\"");
    expect(modalHtml).not.toContain("name=\"size\"");
    expect(modalHtml).not.toContain("name=\"lot\"");
    expect(modalHtml).not.toContain("name=\"side\"");
    expect(modalHtml).not.toContain("name=\"account\"");
    expect(modalContent).not.toContain("entry price");
    expect(modalContent).not.toContain("position size");
  });

  // Test 2: B-P05-1 & B-P05-3 Disclaimers and Audit Correlation IDs rendered on every record
  it("test_uinew_p05_trade_plans_and_journal_entries_render_disclaimer_and_audit_correlation_id", async () => {
    render(
      <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
        <TerminalBottomDock initialTab="TRADE_PLANS" />
      </TerminalProvider>,
    );

    // 1. Verify on Trade Plan Card
    await waitFor(() => {
      expect(screen.getByTestId("trade-plan-disclaimer-plan-001")).toHaveTextContent(
        /Trade plan research note only/,
      );
      expect(screen.getByTestId("trade-plan-audit-plan-001")).toHaveTextContent(/audit-plan-0/);
    });

    // 2. Switch to Journal Tab and verify on Journal Card
    fireEvent.click(screen.getByTestId("bottom-tab-journal"));
    await waitFor(() => {
      expect(screen.getByTestId("journal-disclaimer-journ-001")).toHaveTextContent(
        /Manual research journal entry only/,
      );
      expect(screen.getByTestId("journal-audit-journ-001")).toHaveTextContent(/audit-journ-0/);
    });
  });

  // Test 3: B-P05-3 Edited Records Visibly Disclose updated_at Distinct from created_at
  it("test_uinew_p05_edited_records_visibly_disclose_updated_at_distinct_from_created_at", async () => {
    render(
      <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
        <TerminalBottomDock initialTab="TRADE_PLANS" />
      </TerminalProvider>,
    );

    await waitFor(() => {
      // Plan 001 is unedited -> no [EDITED] badge
      expect(screen.queryByTestId("trade-plan-edited-plan-001")).not.toBeInTheDocument();

      // Plan 002 is edited (updated_at !== created_at) -> shows [EDITED] and updated timestamp
      expect(screen.getByTestId("trade-plan-edited-plan-002")).toBeInTheDocument();
      expect(screen.getByTestId("trade-plan-edited-plan-002")).toHaveTextContent("[EDITED]");
      expect(screen.getByTestId("trade-plan-updated-plan-002")).toHaveTextContent(/Updated:/);
    });

    // Switch to Journal Tab
    fireEvent.click(screen.getByTestId("bottom-tab-journal"));
    await waitFor(() => {
      expect(screen.getByTestId("journal-edited-journ-002")).toBeInTheDocument();
      expect(screen.getByTestId("journal-edited-journ-002")).toHaveTextContent("[EDITED]");
    });
  });

  // Test 4: B-P05-2 Risk Metrics Never Render Without Uncertainty or Explicit Unavailable
  it("test_uinew_p05_risk_metrics_never_render_without_uncertainty_or_explicit_unavailable", async () => {
    render(
      <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
        <TerminalBottomDock initialTab="RISK" />
      </TerminalProvider>,
    );

    await waitFor(() => {
      // 1. Max Drawdown
      const ddBox = screen.getByTestId("risk-max-drawdown");
      expect(ddBox).toHaveTextContent("-14.2%");
      expect(ddBox).toHaveTextContent("CI: [-18.5% – -11.2%]");

      // 2. Realized Volatility
      const volBox = screen.getByTestId("risk-volatility");
      expect(volBox).toHaveTextContent("11.8%");
      expect(volBox).toHaveTextContent("CI: [9.5% – 13.8%]");

      // 3. Stress Loss
      const stressBox = screen.getByTestId("risk-stress-loss");
      expect(stressBox).toHaveTextContent("-22.5%");
      expect(stressBox).toHaveTextContent("CI: [-28.5% – -18.2%]");
    });
  });

  // Test 5: B-P05-2 Stress Loss Renders With Its Assumptions and Sample Window
  it("test_uinew_p05_stress_loss_renders_with_its_assumptions_and_sample_window", async () => {
    render(
      <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
        <TerminalBottomDock initialTab="RISK" />
      </TerminalProvider>,
    );

    await waitFor(() => {
      // Assumptions directly visible without navigation
      expect(screen.getByTestId("risk-stress-assumptions")).toBeInTheDocument();
      expect(screen.getByTestId("risk-stress-assumptions")).toHaveTextContent("stress_multiplier: 2");
      expect(screen.getByTestId("risk-stress-assumptions")).toHaveTextContent("tail_quantile: 0.05");

      // Sample window and sample count
      expect(screen.getByTestId("risk-window")).toHaveTextContent("Sample Window: 2026-08-06 to 2026-08-13");
      expect(screen.getByTestId("risk-window")).toHaveTextContent("N = 500 bars");
    });
  });

  // Test 6: B-P05-2 No Client-Side Computation of Drawdown, Volatility or Stress Values
  it("test_uinew_p05_no_client_side_computation_of_drawdown_volatility_or_stress_values", async () => {
    render(
      <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
        <TerminalBottomDock initialTab="RISK" />
      </TerminalProvider>,
    );

    await waitFor(() => {
      // Values matched verbatim from backend report
      expect(screen.getByTestId("risk-max-drawdown-val")).toHaveTextContent("-14.2%");
      expect(screen.getByTestId("risk-volatility-val")).toHaveTextContent("11.8%");
      expect(screen.getByTestId("risk-stress-loss-val")).toHaveTextContent("-22.5%");
    });
  });

  // Test 7: B-P05-4 Failed Writes Render Explicit Error and Never Optimistic Success
  it("test_uinew_p05_failed_writes_render_explicit_error_and_never_optimistic_success", async () => {
    vi.mocked(client.createTradePlan).mockRejectedValueOnce(
      new Error("Database write locked under governance constraint"),
    );

    render(
      <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
        <TerminalBottomDock initialTab="TRADE_PLANS" />
      </TerminalProvider>,
    );

    await waitFor(() => {
      expect(screen.getByTestId("add-trade-plan-btn")).toBeInTheDocument();
    });
    fireEvent.click(screen.getByTestId("add-trade-plan-btn"));

    // Fill form
    fireEvent.change(screen.getByTestId("trade-plan-title-input"), {
      target: { value: "Test Failing Plan" },
    });
    fireEvent.change(screen.getByTestId("trade-plan-hypothesis-input"), {
      target: { value: "Hypothesis content" },
    });

    // Submit
    fireEvent.click(screen.getByTestId("trade-plan-save-btn"));

    // Verify explicit error banner is rendered and plan is NOT added
    await waitFor(() => {
      expect(screen.getByTestId("trade-plan-error-banner")).toBeInTheDocument();
      expect(screen.getByTestId("trade-plan-error-banner")).toHaveTextContent(
        "Database write locked under governance constraint",
      );
    });

    // Plan count remains 2 (never optimistically added)
    expect(screen.queryByTestId("trade-plan-card-failing")).not.toBeInTheDocument();
  });

  // Test 8: OBS-P05-1 & CA-P04-5 Every Rendered Interval Brackets Its Own Point Estimate (P04 & P05)
  it("test_uinew_p05_every_rendered_interval_brackets_its_own_point_estimate", async () => {
    // 1. Check P04 Signal Cards
    render(
      <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
        <TerminalSignalStream />
      </TerminalProvider>,
    );

    await waitFor(() => {
      // Signal 1 (78.4%) is within [72.4% – 84.1%] -> renders interval
      const sig1 = screen.getByTestId("signal-confidence-sig-001");
      expect(sig1).toHaveTextContent("78.4% · Wilson: [72.4% – 84.1%]");

      // Signal 2 (48.0%) is NOT within [72.4% – 84.1%] -> must NOT render interval, must render [Uncertainty: Unavailable]
      const sig2 = screen.getByTestId("signal-confidence-sig-002");
      expect(sig2).toHaveTextContent("48.0% · [Uncertainty: Unavailable]");
      expect(sig2.textContent).not.toContain("Wilson: [72.4% – 84.1%]");
    });

    // 2. Check P05 Risk Metrics
    render(
      <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
        <TerminalBottomDock initialTab="RISK" />
      </TerminalProvider>,
    );

    await waitFor(() => {
      // Max DD: -14.2% falls within [-18.5%, -11.2%]
      expect(screen.getByTestId("risk-max-drawdown")).toHaveTextContent("CI: [-18.5% – -11.2%]");

      // Volatility: 11.8% falls within [9.5%, 13.8%]
      expect(screen.getByTestId("risk-volatility")).toHaveTextContent("CI: [9.5% – 13.8%]");

      // Stress Loss: -22.5% falls within [-28.5%, -18.2%]
      expect(screen.getByTestId("risk-stress-loss")).toHaveTextContent("CI: [-28.5% – -18.2%]");
    });
  });
});
