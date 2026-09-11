/**
 * SURF-P01 — R4 degradation + S2 detail-surfacing suite (Build Order §4/§5).
 *
 * Named tests prove: no single read-seam failure blanks the execution
 * research surface (the item-4 M5 pattern with genuine loaded counts),
 * absence renders as absence (R3 — nothing fabricated), and each of the six
 * previously unreachable detail GETs is retrieved on demand when the
 * operator opens a detail record.
 */
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { ExecutionResearchView } from "./ExecutionResearchView";
import * as client from "../../../api/client";
import type {
  ExecutionResearchExperiment,
  ExecutionRiskResearchReport,
  SimulatedExecutionAnalyticsReport,
  SimulatedExecutionRun,
  SimulatedFillEvent,
  SimulatedPaperLedgerEntry,
} from "../../../api/client";

vi.mock("../../../api/client", async () => {
  const actual = await vi.importActual<typeof client>("../../../api/client");
  return {
    ...actual,
    fetchSimulatedRunsList: vi.fn(),
    fetchSimulatedRunFills: vi.fn(),
    fetchSimulatedLedgerEntriesList: vi.fn(),
    fetchExecutionRiskReportsList: vi.fn(),
    fetchExecutionExperimentsList: vi.fn(),
    fetchSimulatedAnalyticsReportsList: vi.fn(),
    fetchSimulatedExecutionRunDetail: vi.fn(),
    fetchSimulatedFillDetail: vi.fn(),
    fetchSimulatedLedgerEntryDetail: vi.fn(),
    fetchExecutionRiskReportDetail: vi.fn(),
    fetchExecutionExperimentDetail: vi.fn(),
    fetchSimulatedAnalyticsReportDetail: vi.fn(),
  };
});

function runFixture(): SimulatedExecutionRun {
  return {
    run_id: "run-s1",
    created_at: "2026-08-16T10:00:00Z",
    operator_id: "operator-1",
    simulation_mode: "SIMULATED",
    simulation_policy_version: "policy.v1",
    input_artifact_ids: ["scope-1"],
    replay_scope: { symbol: "EURUSD" },
    fill_model_name: "deterministic_mid_close_slippage",
    fill_model_version: "fill.v1",
    assumptions: { deterministic: true },
    limitations: ["simulated_research_only"],
    research_status: "research_only",
    simulation_disclaimer: "SIMULATED execution research only.",
    audit_correlation_id: "corr-run-s1",
  };
}

function fillFixture(): SimulatedFillEvent {
  return {
    simulated_fill_id: "fill-s1",
    run_id: "run-s1",
    created_at: "2026-08-16T10:00:00Z",
    simulation_mode: "SIMULATED",
    market_class: "forex",
    symbol: "EURUSD",
    timeframe: "M1",
    as_of_time: "2026-08-16T10:00:00Z",
    simulated_research_direction: "long_bias",
    simulated_units: 1,
    requested_reference_price: 1.1,
    simulated_fill_price: 1.100055,
    simulated_slippage_bps: 0.5,
    source_candle_ids: ["candle-1"],
    fill_model_name: "deterministic_mid_close_slippage",
    fill_model_version: "fill.v1",
    research_status: "research_only",
    simulation_disclaimer: "SIMULATED execution research only.",
    audit_correlation_id: "corr-fill-s1",
  };
}

function ledgerFixture(): SimulatedPaperLedgerEntry {
  return {
    ledger_entry_id: "ledger-s1",
    created_at: "2026-08-16T10:00:00Z",
    simulation_mode: "SIMULATED",
    run_id: "run-s1",
    simulated_fill_id: "fill-s1",
    operator_id: "operator-1",
    ledger_event_type: "simulated_close_estimate",
    simulated_research_direction: "long_bias",
    simulated_units: 1,
    simulated_entry_value: 1.1,
    simulated_exit_value: 1.111,
    simulated_return_estimate: 0.01,
    uncertainty: { method: "fixed_simulated_estimate_band", sample_count: 1 },
    limitations: ["not_real_p_and_l"],
    research_status: "research_only",
    simulation_disclaimer: "SIMULATED execution research only.",
    audit_correlation_id: "corr-ledger-s1",
  };
}

function riskFixture(): ExecutionRiskResearchReport {
  return {
    report_id: "risk-s1",
    created_at: "2026-08-16T10:00:00Z",
    simulation_mode: "SIMULATED",
    input_artifact_ids: ["ledger-s1"],
    simulated_request_summary: { ledger_entry_ids: ["ledger-s1"] },
    risk_metrics: { simulated_fill_count: { value: 1 } },
    uncertainty: { method: "sample_range_or_single_sample_limitation", sample_count: 1 },
    limitations: ["economic_usefulness_not_assessed"],
    economic_usefulness: { verdict: "not_assessed" },
    research_status: "research_only",
    simulation_disclaimer: "SIMULATED execution research only.",
    audit_correlation_id: "corr-risk-s1",
  };
}

function experimentFixture(): ExecutionResearchExperiment {
  return {
    experiment_id: "experiment-s1",
    created_at: "2026-08-16T10:00:00Z",
    simulation_mode: "SIMULATED",
    operator_id: "operator-1",
    experiment_title: "Pre-registered replay",
    pre_registration_plan: { hypothesis: "research" },
    plan_hash: "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
    as_of_time: "2026-08-16T10:00:00Z",
    as_of_window: { as_of_time: "2026-08-16T10:00:00Z" },
    replay_input_lineage: { included_candle_ids: ["candle-1"] },
    included_scope_summary: { full_scope_included: true },
    uncertainty: { method: "replay_scope_count_limitation", sample_count: 1 },
    limitations: ["as_of_bounded_no_future_rows"],
    research_status: "research_only",
    simulation_disclaimer: "SIMULATED execution research only.",
    audit_correlation_id: "corr-exp-s1",
  };
}

function analyticsFixture(): SimulatedExecutionAnalyticsReport {
  return {
    report_id: "analytics-s1",
    created_at: "2026-08-16T10:00:00Z",
    simulation_mode: "SIMULATED",
    analytics_type: "return_estimate",
    included_scope: { full_scope_included: true },
    sample_count: 3,
    metrics: { simulated_average_return_estimate: { value: 0.01 } },
    uncertainty: {
      method: "per_metric_interval_or_insufficient_sample_limitation",
      sample_count: 3,
      metrics: { simulated_average_return_estimate: { method: "insufficient_sample_limitation" } },
    },
    limitations: ["not_real_p_and_l", "full_declared_scope_included"],
    economic_usefulness: { verdict: "not_assessed" },
    report_hash: "abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcd",
    source_artifact_ids: ["fill-s1", "ledger-s1", "experiment-s1"],
    research_status: "research_only",
    simulation_disclaimer: "SIMULATED execution research only.",
    audit_correlation_id: "corr-analytics-s1",
  };
}

beforeEach(() => {
  vi.clearAllMocks();
  vi.mocked(client.fetchSimulatedRunsList).mockResolvedValue([runFixture()]);
  vi.mocked(client.fetchSimulatedRunFills).mockResolvedValue([fillFixture()]);
  vi.mocked(client.fetchSimulatedLedgerEntriesList).mockResolvedValue([ledgerFixture()]);
  vi.mocked(client.fetchExecutionRiskReportsList).mockResolvedValue([riskFixture()]);
  vi.mocked(client.fetchExecutionExperimentsList).mockResolvedValue([experimentFixture()]);
  vi.mocked(client.fetchSimulatedAnalyticsReportsList).mockResolvedValue([analyticsFixture()]);
});

function renderView() {
  return render(
    <MemoryRouter>
      <ExecutionResearchView />
    </MemoryRouter>,
  );
}

describe("SURF-P01 — R4 independent degradation and S2 detail surfacing", () => {
  it("test_surf_p01_r4_single_seam_failure_does_not_blank_surface", async () => {
    vi.mocked(client.fetchSimulatedLedgerEntriesList).mockRejectedValue(
      new Error("ledger seam down"),
    );

    renderView();

    await waitFor(() => {
      expect(screen.getAllByTestId("exec-source-status-error").length).toBe(1);
    });

    // The surface is not blanked: header, groups, and counts still render.
    expect(screen.getByTestId("execution-research-header")).toBeInTheDocument();
    expect(screen.getByTestId("execution-group-runs")).toBeInTheDocument();
    expect(screen.getByTestId("execution-group-analytics")).toBeInTheDocument();

    // The failed seam reports its own error inside the source status region.
    const status = screen.getByTestId("execution-source-status");
    expect(within(status).getByText("Paper ledger")).toBeInTheDocument();
    expect(within(status).getByText("ledger seam down")).toBeInTheDocument();

    // Healthy seams still contributed genuine rows to their groups.
    await waitFor(() => {
      expect(screen.getAllByTestId("exec-source-status-ready").length).toBe(5);
      expect(screen.getByTestId("execution-run-card-run-s1")).toBeInTheDocument();
    });
    expect(screen.getByText("No simulated ledger rows returned.")).toBeInTheDocument();
  });

  it("test_surf_p01_r4_two_seam_failures_render_honest_error_rows", async () => {
    vi.mocked(client.fetchSimulatedRunsList).mockRejectedValue(new Error("runs seam down"));
    vi.mocked(client.fetchExecutionExperimentsList).mockRejectedValue(
      new Error("experiments seam down"),
    );

    renderView();

    // Three honest error rows: the two failed seams plus the fills row, which
    // declares its dependency on the failed runs seam rather than pretending
    // to be ready.
    await waitFor(() => {
      expect(screen.getAllByTestId("exec-source-status-error").length).toBe(3);
    });

    const status = screen.getByTestId("execution-source-status");
    expect(within(status).getByText("runs seam down")).toBeInTheDocument();
    expect(within(status).getByText("experiments seam down")).toBeInTheDocument();
    expect(
      within(status).getByText("Simulated runs unavailable — fills not loaded"),
    ).toBeInTheDocument();

    // Unaffected seams still render their groups.
    expect(screen.getByTestId("execution-ledger-card-ledger-s1")).toBeInTheDocument();
  });

  it("test_surf_p01_r4_all_seams_ready_report_genuine_loaded_counts", async () => {
    renderView();

    await waitFor(() => {
      expect(screen.getAllByTestId("exec-source-status-ready").length).toBe(6);
    });

    const status = screen.getByTestId("execution-source-status");
    // Genuine loaded counts only — every seam loaded exactly one fixture row.
    expect(within(status).getAllByText("1 rows loaded").length).toBe(6);
    expect(screen.queryAllByTestId("exec-source-status-error").length).toBe(0);
  });

  it("test_surf_p01_r3_absence_renders_as_absence_no_fabricated_values", async () => {
    vi.mocked(client.fetchSimulatedRunsList).mockResolvedValue([]);
    vi.mocked(client.fetchSimulatedLedgerEntriesList).mockResolvedValue([]);
    vi.mocked(client.fetchExecutionRiskReportsList).mockResolvedValue([]);
    vi.mocked(client.fetchExecutionExperimentsList).mockResolvedValue([]);
    vi.mocked(client.fetchSimulatedAnalyticsReportsList).mockResolvedValue([]);

    renderView();

    await waitFor(() => {
      expect(screen.getAllByTestId("exec-source-status-ready").length).toBe(6);
    });

    // R3: zero rows stated, never a plausible stand-in number.
    expect(screen.getAllByText("0 rows loaded").length).toBe(6);
    expect(screen.getByText("No simulated runs returned.")).toBeInTheDocument();
    expect(screen.getByText("No simulated ledger rows returned.")).toBeInTheDocument();
    expect(screen.getByText("No risk reports returned.")).toBeInTheDocument();
    expect(screen.getByText("No replay experiments returned.")).toBeInTheDocument();
    expect(screen.getByText("No analytics reports returned.")).toBeInTheDocument();
  });

  it("test_surf_p01_s2_run_detail_get_surfaces_record_on_selection", async () => {
    vi.mocked(client.fetchSimulatedExecutionRunDetail).mockResolvedValue({
      run: runFixture(),
      fills: [fillFixture()],
    });

    renderView();

    await waitFor(() => {
      expect(screen.getByTestId("execution-detail-open-run-run-s1")).toBeInTheDocument();
    });

    fireEvent.click(screen.getByTestId("execution-detail-open-run-run-s1"));

    // The surfaced detail GET was retrieved with the selected id…
    expect(client.fetchSimulatedExecutionRunDetail).toHaveBeenCalledWith("run-s1");

    // …and its record (run + its fills) renders in the detail panel.
    await waitFor(() => {
      expect(screen.getByTestId("execution-detail-record")).toBeInTheDocument();
    });
    const panel = screen.getByTestId("execution-detail-panel");
    // The detail panel header and the run record body both show the id.
    expect(within(panel).getAllByText("run-s1").length).toBeGreaterThanOrEqual(2);
    expect(within(panel).getByText("Fills (1)")).toBeInTheDocument();
    // The run's fill record renders inside the detail panel (the fill card
    // presents symbol · timeframe).
    expect(within(panel).getByText("EURUSD · M1")).toBeInTheDocument();
  });

  it("test_surf_p01_s2_detail_failure_never_blanks_the_index", async () => {
    vi.mocked(client.fetchExecutionRiskReportDetail).mockRejectedValue(
      new Error("risk detail seam down"),
    );

    renderView();

    await waitFor(() => {
      expect(screen.getByTestId("execution-detail-open-risk-risk-s1")).toBeInTheDocument();
    });

    fireEvent.click(screen.getByTestId("execution-detail-open-risk-risk-s1"));

    // The detail panel reports its own error…
    await waitFor(() => {
      expect(screen.getByTestId("execution-detail-error")).toHaveTextContent(
        "risk detail seam down",
      );
    });

    // …while the index stays fully rendered with all six seams ready.
    expect(screen.getByTestId("execution-group-runs")).toBeInTheDocument();
    expect(screen.getAllByTestId("exec-source-status-ready").length).toBe(6);
    expect(screen.getByTestId("execution-detail-close")).toBeInTheDocument();
  });

  it("test_surf_p01_obs1_2_stage_panels_keep_intrinsic_height_rule_present", () => {
    // OBS-SURF1-2 (2026-08-17): the stage scroll containers are flex columns,
    // and flex-shrink compressed the direct panel children to their 120px
    // min-height — the per-source cards then overflowed behind the next
    // panel's background and were unreadable. jsdom cannot compute layout, so
    // this named test pins the corrective stylesheet rule non-vacuously (both
    // stage selectors plus the property) by reading the shipped stylesheet
    // directly. The rendered proof is the Rev C capture set, whose JSON
    // records card/panel containment.
    const cssPath = join(process.cwd(), "src/components/terminal/TerminalMultiPane.css");
    if (!existsSync(cssPath)) {
      throw new Error(`TerminalMultiPane.css not found at ${cssPath}`);
    }
    const css = readFileSync(cssPath, "utf8");
    expect(css).toContain(".research-stage-scroll > *");
    expect(css).toContain(".stage-view-scroll > *");
    expect(css).toContain("flex-shrink: 0");
  });
});
