/**
 * UI-CONV-P03 item 4 — M5 degradation suite (directive §6).
 *
 * The research hub fans out to ten independent fetches. These named tests
 * prove the directive's M5 contract: no single failure blanks the hub, each
 * source degrades with its own error/loading state, row counts are genuine
 * loaded counts (R3 — nothing fabricated), and write-path failures render in
 * the mutation error banner without touching read-source state.
 */
import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { ResearchHubView } from "./ResearchHubView";
import * as client from "../../../api/client";
import type { AdvisorySignal, ScenarioReport } from "../../../api/client";

vi.mock("../../../api/client", async () => {
  const actual = await vi.importActual<typeof client>("../../../api/client");
  return {
    ...actual,
    fetchResearchManagementBundle: vi.fn(),
    fetchScenarioReports: vi.fn(),
    fetchAdvisorySignals: vi.fn(),
    fetchInstitutionalIntelligenceBundle: vi.fn(),
    fetchTradePlans: vi.fn(),
    fetchJournalEntries: vi.fn(),
    fetchExecutionResearchBundle: vi.fn(),
    fetchPortfolioResearchDashboard: vi.fn(),
    fetchAdvancedResearchReport: vi.fn(),
    fetchChartResearchAnnotations: vi.fn(),
    createResearchCollection: vi.fn(),
    createResearchTag: vi.fn(),
    addResearchCollectionMember: vi.fn(),
    removeResearchCollectionMember: vi.fn(),
  };
});

const EMPTY_BUNDLE = {
  collections: [],
  members: [],
  tags: [],
  supported_artifact_types: [],
  posture: "research_only",
};
const EMPTY_INTEL = { relation: [], context: [], hypothetical: [], risk: [], validation: [] };
const EMPTY_EXECUTION = {
  runs: [],
  fills: [],
  ledger: [],
  riskReports: [],
  experiments: [],
  analyticsReports: [],
};

function signalFixture(): AdvisorySignal {
  return {
    signal_id: "sig-m5-1",
    created_at: "2026-08-16T10:00:00Z",
    as_of_time: "2026-08-16T10:00:00Z",
    market_class: "forex",
    provider: "model.ensemble.v1",
    symbol: "EURUSD",
    timeframe: "1m",
    model_artifact_id: "model.eurusd.classifier",
    model_version: "1.4.2",
    feature_set_version: "feat.m1.v2",
    experiment_id: "exp-m5",
    statistical_report_id: "stat-m5",
    calibration_report_id: "val-m5",
    economic_report_id: "econ-m5",
    generalization_report_id: "gen-m5",
    inference_input_hash: "a1b2c3d4e5f6789012345678abcdef01",
    raw_score: 0.812,
    calibrated_confidence: 0.784,
    input_staleness_seconds: 4,
    signal_validity_seconds: 60,
    expires_at: "2099-08-16T10:01:00Z",
    freshness_status: "fresh",
    signal_direction: "LONG_BIAS",
    signal_state: "emitted",
    state_reason: "Domain criteria validated",
    eligibility_reasons: ["low_spread"],
    operating_domain_status: "in_domain",
    calibration_status: "calibrated",
    economic_verdict: "cost_favorable",
    risk_notes: "fixture",
    rationale: "fixture",
    explainability_summary: {},
    state_transition_history: ["emitted"],
    audit_correlation_id: "audit-m5",
  };
}

function scenarioFixture(): ScenarioReport {
  return {
    id: "scenario-m5-1",
    created_at: "2026-08-16T10:00:00Z",
    artifact_type: "scenario_report",
    method_version: "w4-u04.hypothetical_path.v1",
    market_class: "forex",
    symbol: "EURUSD",
    timeframe: "M1",
    as_of_start: "2026-08-16T09:00:00Z",
    as_of_end: "2026-08-16T10:00:00Z",
    sample_count: 4,
    scenario_name: "M5 stored hypothetical scenario",
    hypothetical_return: -0.02,
    scenario_result: { hypothetical_return: -0.02 },
    assumptions: { scenario_name: "M5 stored hypothetical scenario" },
    inputs: { baseline_returns: [0, 0.01] },
    uncertainty: { method: "fixture", sample_count: 4 },
    economic_usefulness: { verdict: "not_assessed" },
    config: { fixture: true },
    input_lineage: { policy: "as_of_bounded" },
    source_artifact_ids: ["source-m5"],
    market_scope: { market_class: "forex" },
    results: { scenario_result: { hypothetical_return: -0.02 } },
    limitations: ["research_only"],
    report_hash: "hash-m5",
    research_status: "research_only",
    created_by: "vitest",
    audit_correlation_id: "corr-m5",
    notes: "read only source artifact",
  };
}

beforeEach(() => {
  vi.clearAllMocks();
  vi.mocked(client.fetchResearchManagementBundle).mockResolvedValue(EMPTY_BUNDLE);
  vi.mocked(client.fetchScenarioReports).mockResolvedValue([]);
  vi.mocked(client.fetchAdvisorySignals).mockResolvedValue([]);
  vi.mocked(client.fetchInstitutionalIntelligenceBundle).mockResolvedValue(EMPTY_INTEL);
  vi.mocked(client.fetchTradePlans).mockResolvedValue([]);
  vi.mocked(client.fetchJournalEntries).mockResolvedValue([]);
  vi.mocked(client.fetchExecutionResearchBundle).mockResolvedValue(EMPTY_EXECUTION);
  vi.mocked(client.fetchPortfolioResearchDashboard).mockResolvedValue(
    null as unknown as import("../../../api/client").PortfolioResearchDashboard,
  );
  vi.mocked(client.fetchAdvancedResearchReport).mockResolvedValue(
    null as unknown as import("../../../api/client").AdvancedResearchReport,
  );
  vi.mocked(client.fetchChartResearchAnnotations).mockResolvedValue([]);
});

describe("UI-CONV-P03 item 4 — M5 independent per-source degradation", () => {
  it("test_uiconv_p03_item4_m5_single_source_failure_does_not_blank_hub", async () => {
    vi.mocked(client.fetchScenarioReports).mockRejectedValue(new Error("scenario seam down"));
    vi.mocked(client.fetchAdvisorySignals).mockResolvedValue([signalFixture()]);

    render(<ResearchHubView />);

    await waitFor(() => {
      expect(screen.getAllByTestId("source-status-error").length).toBe(1);
    });

    // The hub is not blanked: header, catalog, and organization regions still render.
    expect(screen.getByTestId("research-hub-view")).toBeInTheDocument();
    expect(screen.getByTestId("artifact-catalog")).toBeInTheDocument();
    expect(screen.getByTestId("organization-records-preview")).toBeInTheDocument();

    // The failed family reports its own error inside the source status region.
    const status = screen.getByTestId("artifact-source-status");
    expect(within(status).getByText("Scenario reports")).toBeInTheDocument();
    expect(within(status).getByText("scenario seam down")).toBeInTheDocument();

    // The healthy family still contributed its row to the catalog.
    await waitFor(() => {
      const catalog = screen.getByTestId("artifact-catalog-list");
      expect(within(catalog).getByText("EURUSD · 1m · LONG_BIAS")).toBeInTheDocument();
      expect(screen.getAllByTestId("source-status-ready").length).toBe(9);
    });
  });

  it("test_uiconv_p03_item4_m5_two_source_failures_render_two_independent_errors", async () => {
    vi.mocked(client.fetchResearchManagementBundle).mockRejectedValue(
      new Error("organization seam down"),
    );
    vi.mocked(client.fetchTradePlans).mockRejectedValue(new Error("trade plan seam down"));
    vi.mocked(client.fetchScenarioReports).mockResolvedValue([scenarioFixture()]);

    render(<ResearchHubView />);

    await waitFor(() => {
      expect(screen.getAllByTestId("source-status-error").length).toBe(2);
    });

    const status = screen.getByTestId("artifact-source-status");
    expect(within(status).getByText("organization seam down")).toBeInTheDocument();
    expect(within(status).getByText("trade plan seam down")).toBeInTheDocument();

    // The unaffected scenario family still renders its catalog row, and the
    // organization preview renders its honest absence markers.
    await waitFor(() => {
      const catalog = screen.getByTestId("artifact-catalog-list");
      expect(within(catalog).getByText("M5 stored hypothetical scenario")).toBeInTheDocument();
    });
    expect(screen.getByText("No collections returned for this operator.")).toBeInTheDocument();
    expect(screen.getByText("No membership references returned.")).toBeInTheDocument();
    expect(screen.getByText("No tags returned.")).toBeInTheDocument();
  });

  it("test_uiconv_p03_item4_m5_all_sources_ready_reports_genuine_loaded_counts", async () => {
    vi.mocked(client.fetchScenarioReports).mockResolvedValue([scenarioFixture()]);
    vi.mocked(client.fetchAdvisorySignals).mockResolvedValue([signalFixture()]);

    render(<ResearchHubView />);

    await waitFor(() => {
      expect(screen.getAllByTestId("source-status-ready").length).toBe(10);
    });

    const status = screen.getByTestId("artifact-source-status");
    // Genuine loaded counts only — the two loaded families report exactly 1 row.
    expect(within(status).getAllByText("1 rows loaded").length).toBe(2);
    expect(within(status).getAllByText("0 rows loaded").length).toBe(8);
    expect(screen.queryAllByTestId("source-status-error").length).toBe(0);
  });

  it("test_uiconv_p03_item4_m5_absence_renders_as_absence_no_fabricated_counts", async () => {
    render(<ResearchHubView />);

    await waitFor(() => {
      expect(screen.getAllByTestId("source-status-ready").length).toBe(10);
    });

    // R3: nothing fabricated — every empty source states 0 rows.
    expect(screen.getAllByText("0 rows loaded").length).toBe(10);
    // The catalog honestly reports no matching rows; no stand-in numbers appear.
    expect(screen.getByText("No artifact metadata matches these filters.")).toBeInTheDocument();
    expect(screen.queryByTestId("source-status-error")).not.toBeInTheDocument();
  });

  it("test_uiconv_p03_item4_m5_mutation_failure_renders_mutation_error_banner", async () => {
    vi.mocked(client.createResearchCollection).mockRejectedValue(
      new Error("Failed to save collection record"),
    );

    render(<ResearchHubView />);

    await waitFor(() => {
      expect(screen.getAllByTestId("source-status-ready").length).toBe(10);
    });

    fireEvent.click(screen.getByText("Save collection record"));

    await waitFor(() => {
      expect(screen.getByTestId("research-hub-mutation-error")).toHaveTextContent(
        "Failed to save collection record",
      );
    });

    // A failed write never masquerades as a read-source failure.
    expect(screen.queryAllByTestId("source-status-error").length).toBe(0);
    expect(screen.getAllByTestId("source-status-ready").length).toBe(10);
  });
});
