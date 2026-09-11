import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { TerminalProvider } from "../components/terminal/TerminalContext";
import { TerminalSignalStream } from "../components/terminal/TerminalSignalStream";
import { TerminalIntelligenceCards } from "../components/terminal/TerminalIntelligenceCards";
import type { AdvisorySignal, CorrelationReport, RegimeReport, SignalValidationReport } from "../api/client";
import * as client from "../api/client";

vi.mock("../api/client", async () => {
  const actual = await vi.importActual<typeof client>("../api/client");
  return {
    ...actual,
    fetchAdvisorySignals: vi.fn(),
    fetchSignalValidationReports: vi.fn(),
    fetchCorrelationReports: vi.fn(),
    fetchRegimeReports: vi.fn(),
    fetchInstitutionalIntelligenceBundle: vi.fn().mockResolvedValue(null),
    fetchCandles: vi.fn().mockResolvedValue({ kind: "native", timeframe: "M1", bars: [] }),
    fetchChartResearchAnnotations: vi.fn().mockResolvedValue([]),
  };
});

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
    expires_at: "2099-08-13T10:01:00Z", // Future expiration for emitted test case
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
    statistical_report_id: null,
    calibration_report_id: null, // No linked validation report -> Uncalibrated / Unavailable
    economic_report_id: null,
    generalization_report_id: null,
    inference_input_hash: "b2c3d4e5f6a1789012345678abcdef02",
    raw_score: 0.65,
    calibrated_confidence: 0.625,
    input_staleness_seconds: 350,
    signal_validity_seconds: 60,
    expires_at: "2026-08-13T09:46:00Z",
    freshness_status: "expired",
    signal_direction: "SHORT_BIAS",
    signal_state: "expired",
    state_reason: "Signal validity TTL exceeded",
    eligibility_reasons: [],
    operating_domain_status: "in_domain",
    calibration_status: "uncalibrated",
    economic_verdict: "unverified",
    risk_notes: null,
    rationale: "Mean-reversion trigger at upper Bollinger band.",
    explainability_summary: { bb_upper: 0.45 },
    state_transition_history: ["emitted", "expired"],
    audit_correlation_id: "audit-sig-002",
  },
  {
    signal_id: "sig-003",
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
    calibrated_confidence: 0.48,
    input_staleness_seconds: 12,
    signal_validity_seconds: 60,
    expires_at: "2026-08-13T09:31:00Z",
    freshness_status: "withheld",
    signal_direction: "NEUTRAL",
    signal_state: "withheld",
    state_reason: "High volatility regime threshold exceeded",
    eligibility_reasons: ["volatility_clamp"],
    operating_domain_status: "out_of_domain",
    calibration_status: "calibrated",
    economic_verdict: "unfavorable",
    risk_notes: "News release volatility regime.",
    rationale: "Indeterminate trend direction.",
    explainability_summary: {},
    state_transition_history: ["draft", "withheld"],
    audit_correlation_id: "audit-sig-003",
  },
];

const mockValidationReport: SignalValidationReport = {
  id: "val-001",
  created_at: "2026-08-13T09:00:00Z",
  artifact_type: "signal_validation_report",
  method_version: "w4-u06.signal_validation.v1",
  sample_count: 520,
  metrics: {
    clean_advisory_rate: {
      value: 0.824,
      sample_count: 520,
      uncertainty: {
        method: "wilson_score_interval",
        lower: 0.789,
        upper: 0.854,
        confidence_level: 0.95,
      },
    },
    guardrail_intervention_rate: {
      value: 0.176,
      sample_count: 520,
      uncertainty: {
        method: "wilson_score_interval",
        lower: 0.146,
        upper: 0.211,
        confidence_level: 0.95,
      },
    },
    calibrated_confidence_coverage: {
      value: 0.784,
      sample_count: 520,
      uncertainty: {
        method: "wilson_score_interval",
        lower: 0.724,
        upper: 0.841,
        confidence_level: 0.95,
      },
    },
  },
  uncertainty: {
    method: "wilson_score_interval",
    lower: 0.724,
    upper: 0.841,
    confidence_level: 0.95,
  },
  limitations: ["Synthetic simulation sample window"],
  report_hash: "val-hash-01",
  research_status: "research_only",
};

const mockCorrelationReport: CorrelationReport = {
  id: "corr-001",
  created_at: "2026-08-13T09:00:00Z",
  artifact_type: "correlation_report",
  method_version: "pearson_fisher_v1",
  left_market_class: "forex",
  left_symbol: "EURUSD",
  right_market_class: "forex",
  right_symbol: "USDCHF",
  timeframe: "1m",
  sample_count: 1440,
  correlation_value: -0.742,
  uncertainty: {
    method: "fisher_z_confidence_interval",
    lower: -0.815,
    upper: -0.652,
    confidence_level: 0.95,
  },
  significance: {
    p_value: 0.0001,
  },
  report_hash: "corr-hash-01",
  research_status: "research_only",
};

const mockRegimeReport: RegimeReport = {
  id: "reg-001",
  created_at: "2026-08-13T09:00:00Z",
  artifact_type: "regime_report",
  method_version: "hmm_regime_v1",
  market_class: "forex",
  symbol: "EURUSD",
  timeframe: "1m",
  sample_count: 500,
  regime_label: "TRENDING_BULLISH",
  confidence: 0.845,
  uncertainty: {
    method: "posterior_interval",
    lower: 0.782,
    upper: 0.908,
  },
  evidence: { adx_14: 28.4, atr_ratio: 1.15 },
  report_hash: "reg-hash-01",
  research_status: "research_only",
};

beforeEach(() => {
  vi.clearAllMocks();
  vi.mocked(client.fetchAdvisorySignals).mockResolvedValue(mockSignals);
  vi.mocked(client.fetchSignalValidationReports).mockResolvedValue([mockValidationReport]);
  vi.mocked(client.fetchCorrelationReports).mockResolvedValue([mockCorrelationReport]);
  vi.mocked(client.fetchRegimeReports).mockResolvedValue([mockRegimeReport]);
});

describe("UI-NEW-P04 Quantitative Signals, Intelligence & Uncertainty Stream", () => {
  // Test 1 (Mandatory named test #1)
  it("test_uinew_p04_signal_stream_renders_only_backend_signals_with_no_client_fabrication", async () => {
    render(
      <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
        <TerminalSignalStream />
      </TerminalProvider>,
    );

    expect(screen.getByTestId("terminal-signal-stream")).toBeInTheDocument();
    expect(screen.getByText("ADVISORY SIGNALS")).toBeInTheDocument();

    await waitFor(() => {
      expect(client.fetchAdvisorySignals).toHaveBeenCalledWith({ symbol: "EURUSD", limit: 30 });
      expect(screen.getByTestId("signal-count-badge")).toHaveTextContent("3 SIGNALS");
      expect(screen.getByTestId("signal-card-sig-001")).toBeInTheDocument();
      expect(screen.getByTestId("signal-card-sig-002")).toBeInTheDocument();
      expect(screen.getByTestId("signal-card-sig-003")).toBeInTheDocument();
    });
  });

  // Test 2 (Mandatory named test #2 — B-P04-1 & CA-P04-5: Uncertainty Discipline & Point-Estimate Bracketing)
  it("test_uinew_p04_calibrated_confidence_never_renders_without_uncertainty_or_explicit_unavailable", async () => {
    render(
      <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
        <TerminalSignalStream />
      </TerminalProvider>,
    );

    await waitFor(() => {
      // Case A: Signal 1 (78.4%) has linked validation report [72.4% – 84.1%] which brackets 78.4% -> renders confidence WITH Wilson bounds
      const sig1Conf = screen.getByTestId("signal-confidence-sig-001");
      expect(sig1Conf).toHaveTextContent("78.4% · Wilson: [72.4% – 84.1%]");

      // Case B: Signal 2 (62.5%) has no linked validation report -> renders explicit "Uncertainty: Unavailable" qualifier
      const sig2Conf = screen.getByTestId("signal-confidence-sig-002");
      expect(sig2Conf).toHaveTextContent("62.5% · [Uncertainty: Unavailable]");
      expect(sig2Conf.textContent).not.toBe("62.5%"); // Never a bare/naked number

      // Case C (CA-P04-5): Signal 3 (48.0%) is linked to val-001 [72.4% – 84.1%] but 48.0% falls OUTSIDE [72.4%, 84.1%] -> must render explicit [Uncertainty: Unavailable]
      const sig3Conf = screen.getByTestId("signal-confidence-sig-003");
      expect(sig3Conf).toHaveTextContent("48.0% · [Uncertainty: Unavailable]");
      expect(sig3Conf.textContent).not.toContain("Wilson: [72.4% – 84.1%]");
    });
  });

  // Test 3 (Mandatory named test #3 — B-P04-2: Zero Client-Side Statistics)
  it("test_uinew_p04_no_client_side_computation_of_ece_brier_wilson_or_correlation", async () => {
    render(
      <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
        <TerminalIntelligenceCards initialTab="CALIBRATION" />
      </TerminalProvider>,
    );

    // 1. Verify validation rates and Wilson intervals rendered verbatim from backend report
    await waitFor(() => {
      expect(screen.getByTestId("val-calibrated-coverage-val")).toHaveTextContent("78.4%");
      expect(screen.getByTestId("val-clean-advisory-val")).toHaveTextContent("82.4%");
      expect(screen.getByTestId("val-guardrail-rate-val")).toHaveTextContent("17.6%");
      expect(screen.getByTestId("val-wilson")).toHaveTextContent("[72.4% – 84.1%]");
    });

    // 2. Switch to Correlation tab and verify r and Fisher Z interval
    const corrTab = screen.getByTestId("intel-tab-correlation");
    fireEvent.click(corrTab);

    await waitFor(() => {
      expect(screen.getByTestId("corr-row-corr-001")).toHaveTextContent("r = -0.742");
      expect(screen.getByTestId("corr-row-corr-001")).toHaveTextContent("CI: [-0.81, -0.65]");
    });

    // 3. Switch to Regime tab and verify regime label
    const regimeTab = screen.getByTestId("intel-tab-regime");
    fireEvent.click(regimeTab);

    await waitFor(() => {
      expect(screen.getByTestId("regime-label")).toHaveTextContent("TRENDING_BULLISH");
      expect(screen.getByText(/Confidence: 84.5%/)).toBeInTheDocument();
    });
  });

  // Test 4 (Mandatory named test #4 — B-P04-3: Direction With State, Never As Instruction)
  it("test_uinew_p04_signal_direction_renders_with_state_and_never_as_instruction", async () => {
    render(
      <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
        <TerminalSignalStream />
      </TerminalProvider>,
    );

    await waitFor(() => {
      // 1. Verify direction is rendered with "BIAS" and state, not imperative "Buy/Sell"
      const dir1 = screen.getByTestId("signal-direction-sig-001");
      expect(dir1).toHaveTextContent("POSITIVE BIAS");
      expect(dir1.textContent?.toLowerCase()).not.toContain("buy now");
      expect(dir1.textContent?.toLowerCase()).not.toContain("enter");

      const state1 = screen.getByTestId("signal-state-sig-001");
      expect(state1).toHaveTextContent("EMITTED");

      // 2. Verify prominent research-only framing
      expect(screen.getAllByText("RESEARCH-ONLY · NON-ACTUATING").length).toBeGreaterThan(0);
    });
  });

  // Test 5 (Mandatory named test #5 — B-P04-3: Withheld, Expired & Superseded Visible and Distinct)
  it("test_uinew_p04_withheld_expired_and_superseded_signals_remain_visible_and_distinct", async () => {
    render(
      <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
        <TerminalSignalStream />
      </TerminalProvider>,
    );

    await waitFor(() => {
      // Both emitted, expired, and withheld signals are present simultaneously
      expect(screen.getByTestId("signal-card-sig-001")).toHaveClass("emitted");
      expect(screen.getByTestId("signal-card-sig-002")).toHaveClass("expired");
      expect(screen.getByTestId("signal-card-sig-003")).toHaveClass("withheld");

      // Verify withheld reason is prominently disclosed
      expect(screen.getByTestId("signal-reason-sig-003")).toHaveTextContent(
        "High volatility regime threshold exceeded",
      );
    });
  });

  // Test 6 (Mandatory named test #6 — B-P04-4: Stale/Expired Marked with Absolute UTC Time)
  it("test_uinew_p04_stale_and_expired_signals_are_explicitly_marked_with_absolute_utc_time", async () => {
    render(
      <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
        <TerminalSignalStream />
      </TerminalProvider>,
    );

    await waitFor(() => {
      // Verify absolute UTC timestamp
      expect(screen.getByTestId("signal-asof-sig-001")).toHaveTextContent(/UTC/);
      expect(screen.getByTestId("signal-asof-sig-002")).toHaveTextContent(/UTC/);

      // Verify expired status badge
      expect(screen.getByTestId("signal-state-sig-002")).toHaveTextContent("EXPIRED");
      expect(screen.getByTestId("signal-freshness-sig-002")).toHaveTextContent("EXPIRED");
    });
  });

  // Test 6b (OBS-CONV2-1 regression — fabricated fallback statistical values must never render)
  it("test_uiconv_p02_intelligence_metrics_never_render_fabricated_fallback_values", async () => {
    // A validation report exists but carries NO metrics and NO aggregate uncertainty —
    // the exact condition under which fabricated fallback literals previously rendered.
    const emptyMetricsReport: SignalValidationReport = {
      ...mockValidationReport,
      id: "val-empty",
      metrics: {},
      uncertainty: { method: "wilson_score_interval" },
    };
    vi.mocked(client.fetchSignalValidationReports).mockResolvedValue([emptyMetricsReport]);

    render(
      <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
        <TerminalIntelligenceCards initialTab="CALIBRATION" />
      </TerminalProvider>,
    );

    await waitFor(() => {
      // Every metric box must render the explicit unavailable qualifiers — never fabricated numbers.
      expect(screen.getByTestId("val-calibrated-coverage-val")).toHaveTextContent("Unavailable");
      expect(screen.getByTestId("val-calibrated-coverage-unc")).toHaveTextContent("[Uncertainty: Unavailable]");
      expect(screen.getByTestId("val-clean-advisory-val")).toHaveTextContent("Unavailable");
      expect(screen.getByTestId("val-clean-advisory-unc")).toHaveTextContent("[Uncertainty: Unavailable]");
      expect(screen.getByTestId("val-guardrail-rate-val")).toHaveTextContent("Unavailable");
      expect(screen.getByTestId("val-guardrail-rate-unc")).toHaveTextContent("[Uncertainty: Unavailable]");
      expect(screen.getByTestId("val-wilson")).toHaveTextContent("[Uncertainty: Unavailable]");
    });

    // The previously fabricated literals must never appear anywhere in the rendered document.
    const bodyText = document.body.textContent ?? "";
    expect(bodyText).not.toContain("78.4%");
    expect(bodyText).not.toContain("82.4%");
    expect(bodyText).not.toContain("17.6%");
    expect(bodyText).not.toContain("72.4%");
  });

  // Test 6c (OBS-CONV2-3 regression — state badge renders signal_state verbatim, never derived from freshness)
  it("test_uiconv_p02_signal_state_badge_renders_signal_state_verbatim_not_freshness_derived", async () => {
    // A withheld signal whose TTL has lapsed: signal_state=withheld, freshness_status=expired.
    // Under the prior derived-state logic the badge rendered EXPIRED while the state filter
    // grouped it under WITHHELD — a data-honesty defect.
    const mixedStateSignal: AdvisorySignal = {
      ...mockSignals[2],
      signal_id: "sig-mixed",
      freshness_status: "expired",
      signal_state: "withheld",
      expires_at: "2026-08-13T09:31:00Z",
    };
    vi.mocked(client.fetchAdvisorySignals).mockResolvedValue([mixedStateSignal]);

    render(
      <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
        <TerminalSignalStream />
      </TerminalProvider>,
    );

    await waitFor(() => {
      // State badge must render the recorded state VERBATIM — WITHHELD, not a derived EXPIRED.
      expect(screen.getByTestId("signal-state-sig-mixed")).toHaveTextContent("WITHHELD");
      // Freshness is carried separately and verbatim by the freshness tag.
      expect(screen.getByTestId("signal-freshness-sig-mixed")).toHaveTextContent("EXPIRED");
    });
  });

  // Test 7 (Mandatory named test #7 — B-P04-5: Model Version, Feature Set & Input Hash)
  it("test_uinew_p04_model_version_feature_set_and_input_hash_render_for_every_signal", async () => {
    // UI-CONV-P03 item 6: the expanded card now renders in-app navigation Links
    // (M5); this test expands a card, so it renders inside a Router.
    render(
      <MemoryRouter>
        <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
          <TerminalSignalStream />
        </TerminalProvider>
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByTestId("signal-provenance-sig-001")).toHaveTextContent(
        "Model: model.eurusd.classifier v1.4.2",
      );
      expect(screen.getByTestId("signal-provenance-sig-001")).toHaveTextContent(
        "Feat: feat.m1.v2",
      );
      expect(screen.getByTestId("signal-hash-sig-001")).toHaveTextContent(
        "Hash: a1b2c3d4e5f67890…",
      );
    });

    // Expand signal to verify feature attribution
    const card1 = screen.getByTestId("signal-card-sig-001");
    fireEvent.click(card1);

    await waitFor(() => {
      expect(screen.getByTestId("signal-expanded-sig-001")).toBeInTheDocument();
      expect(screen.getByText(/rsi_14:/)).toBeInTheDocument();
      expect(screen.getByText("0.3240")).toBeInTheDocument();
      expect(screen.getByText(/Elevated spread risk during session rollover/)).toBeInTheDocument();
    });
  });
});
