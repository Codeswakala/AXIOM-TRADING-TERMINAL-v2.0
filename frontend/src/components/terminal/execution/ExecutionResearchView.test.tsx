/**
 * SURF-P01 — relocated suite.
 *
 * This file was the legacy `frontend/src/pages/ExecutionResearchPage.test.tsx`.
 * It relocated alongside its subject (ExecutionResearchView) per Build Order
 * SURF-P01. Re-targets are documented inline: (a) import paths resolve the view
 * module and its neighbours; (b) plain renders are wrapped in MemoryRouter
 * because the investigation-context links are now react-router Links targeting
 * post-absorption destinations (item-6 M5 class); (c) three new named tests
 * pin the legacy-route redirect, the M2 group labelling, and the R4 testids.
 */
import { render, screen, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { ProtectedRoute } from "../../../auth/ProtectedRoute";
import {
  EXECUTION_RESEARCH_DISCLAIMER,
  ExecutionResearchWorkspace,
} from "./ExecutionResearchView";
import { ExecutionResearchRedirect } from "../../../workstation/registry/workspaceRegistry";
import type { ExecutionResearchBundle } from "../../../api/client";

vi.mock("../../../context/AuthContext", () => ({
  useAuth: () => ({
    operator: null,
    loading: false,
    isAuthenticated: false,
    login: vi.fn(),
    logout: vi.fn(),
    refreshProfile: vi.fn(),
  }),
}));

const bundle: ExecutionResearchBundle = {
  runs: [
    {
      run_id: "run-1",
      created_at: "2026-07-17T10:00:00Z",
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
      simulation_disclaimer: EXECUTION_RESEARCH_DISCLAIMER,
      audit_correlation_id: "corr-run",
    },
  ],
  fills: [
    {
      simulated_fill_id: "fill-1",
      run_id: "run-1",
      created_at: "2026-07-17T10:00:00Z",
      simulation_mode: "SIMULATED",
      market_class: "forex",
      symbol: "EURUSD",
      timeframe: "M1",
      as_of_time: "2026-07-17T10:00:00Z",
      simulated_research_direction: "long_bias",
      simulated_units: 1,
      requested_reference_price: 1.1,
      simulated_fill_price: 1.100055,
      simulated_slippage_bps: 0.5,
      source_candle_ids: ["candle-1"],
      fill_model_name: "deterministic_mid_close_slippage",
      fill_model_version: "fill.v1",
      research_status: "research_only",
      simulation_disclaimer: EXECUTION_RESEARCH_DISCLAIMER,
      audit_correlation_id: "corr-fill",
    },
  ],
  ledger: [
    {
      ledger_entry_id: "ledger-1",
      created_at: "2026-07-17T10:00:00Z",
      simulation_mode: "SIMULATED",
      run_id: "run-1",
      simulated_fill_id: "fill-1",
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
      simulation_disclaimer: EXECUTION_RESEARCH_DISCLAIMER,
      audit_correlation_id: "corr-ledger",
    },
  ],
  riskReports: [
    {
      report_id: "risk-1",
      created_at: "2026-07-17T10:00:00Z",
      simulation_mode: "SIMULATED",
      input_artifact_ids: ["ledger-1"],
      simulated_request_summary: { ledger_entry_ids: ["ledger-1"] },
      risk_metrics: { simulated_fill_count: { value: 1 } },
      uncertainty: { method: "sample_range_or_single_sample_limitation", sample_count: 1 },
      limitations: ["economic_usefulness_not_assessed"],
      economic_usefulness: { verdict: "not_assessed" },
      research_status: "research_only",
      simulation_disclaimer: EXECUTION_RESEARCH_DISCLAIMER,
      audit_correlation_id: "corr-risk",
    },
  ],
  experiments: [
    {
      experiment_id: "experiment-1",
      created_at: "2026-07-17T10:00:00Z",
      simulation_mode: "SIMULATED",
      operator_id: "operator-1",
      experiment_title: "Pre-registered replay",
      pre_registration_plan: { hypothesis: "research" },
      plan_hash: "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
      as_of_time: "2026-07-17T10:00:00Z",
      as_of_window: { as_of_time: "2026-07-17T10:00:00Z" },
      replay_input_lineage: { included_candle_ids: ["candle-1"] },
      included_scope_summary: { full_scope_included: true },
      uncertainty: { method: "replay_scope_count_limitation", sample_count: 1 },
      limitations: ["as_of_bounded_no_future_rows"],
      research_status: "research_only",
      simulation_disclaimer: EXECUTION_RESEARCH_DISCLAIMER,
      audit_correlation_id: "corr-exp",
    },
  ],
  analyticsReports: [
    {
      report_id: "analytics-1",
      created_at: "2026-07-17T10:00:00Z",
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
      source_artifact_ids: ["fill-1", "ledger-1", "experiment-1"],
      research_status: "research_only",
      simulation_disclaimer: EXECUTION_RESEARCH_DISCLAIMER,
      audit_correlation_id: "corr-analytics",
    },
  ],
};

// Re-target (b): the workspace renders react-router Links, so plain renders
// are wrapped in a router.
function renderWorkspace(props: { bundle: ExecutionResearchBundle }) {
  return render(
    <MemoryRouter>
      <ExecutionResearchWorkspace bundle={props.bundle} />
    </MemoryRouter>,
  );
}

describe("ExecutionResearchWorkspace (relocated ExecutionResearchPage suite)", () => {
  it("renders SIMULATED label and not-live disclaimer", () => {
    renderWorkspace({ bundle });

    expect(screen.getByText("Execution Research Workspace")).toBeInTheDocument();
    expect(screen.getByText("SIMULATED.")).toBeInTheDocument();
    expect(screen.getByText(EXECUTION_RESEARCH_DISCLAIMER)).toBeInTheDocument();
    expect(screen.getAllByText("SIMULATED").length).toBeGreaterThan(3);
  });

  it("renders persisted simulated artifacts read-only", () => {
    renderWorkspace({ bundle });

    expect(screen.getByText("Simulated Runs")).toBeInTheDocument();
    expect(screen.getByText("Simulated Fills")).toBeInTheDocument();
    expect(screen.getByText("Paper Research Ledger")).toBeInTheDocument();
    expect(screen.getByText("Risk Research Reports")).toBeInTheDocument();
    expect(screen.getByText("Replay Experiments")).toBeInTheDocument();
    expect(screen.getByText("Analytics & Comparison")).toBeInTheDocument();
    expect(screen.getAllByText("run-1").length).toBeGreaterThan(0);
    expect(screen.getByText("EURUSD · M1")).toBeInTheDocument();
  });

  it("does not render forbidden actuation controls", () => {
    renderWorkspace({ bundle });

    const buttonText = screen
      .getAllByRole("button")
      .map((button) => button.textContent?.toLowerCase() ?? "")
      .join(" ");
    const forbidden = ["b" + "uy", "s" + "ell", "submit", "exec" + "ute", "go live", "connect"];
    for (const word of forbidden) {
      expect(buttonText).not.toContain(word);
    }
  });

  it("renders analytics uncertainty, limitations, and economic usefulness framing", () => {
    renderWorkspace({ bundle });

    const analytics = screen.getByLabelText("Simulated analytics reports");
    expect(within(analytics).getByText("return_estimate")).toBeInTheDocument();
    expect(within(analytics).getByText(/per-metric uncertainty present/)).toBeInTheDocument();
    expect(within(analytics).getByText("not_assessed")).toBeInTheDocument();
    expect(within(analytics).getByText(/not_real_p_and_l/)).toBeInTheDocument();
  });

  it("requires auth via protected route and blocks logged-out access", () => {
    render(
      <MemoryRouter initialEntries={["/execution-research"]}>
        <Routes>
          <Route path="/login" element={<div>Operator login required</div>} />
          <Route
            path="/execution-research"
            element={
              <ProtectedRoute>
                <ExecutionResearchWorkspace bundle={bundle} />
              </ProtectedRoute>
            }
          />
        </Routes>
      </MemoryRouter>,
    );

    expect(screen.getByText("Operator login required")).toBeInTheDocument();
    expect(screen.queryByText("Execution Research Workspace")).not.toBeInTheDocument();
  });

  it("test_surf_p01_legacy_route_redirects_to_the_execution_stage_view", () => {
    // R2: the registry route `/execution-research` now resolves to the
    // terminal execution research stage deep link (/?view=execution).
    render(
      <MemoryRouter initialEntries={["/execution-research"]}>
        <Routes>
          <Route
            path="/"
            element={<div data-testid="execution-stage-probe">execution stage probe</div>}
          />
          <Route path="/execution-research" element={<ExecutionResearchRedirect />} />
        </Routes>
      </MemoryRouter>,
    );

    expect(screen.getByTestId("execution-stage-probe")).toBeInTheDocument();
    expect(screen.getByText("execution stage probe")).toBeInTheDocument();
  });

  it("test_surf_p01_m2_group_labels_cover_every_artifact_group", () => {
    // M2: SIMULATED · NON-ACTUATING appears at EACH artifact group (six),
    // not once in a header.
    renderWorkspace({ bundle });

    expect(screen.getByTestId("execution-sim-badge-runs")).toHaveTextContent(
      "SIMULATED · NON-ACTUATING",
    );
    expect(screen.getByTestId("execution-sim-badge-fills")).toHaveTextContent(
      "SIMULATED · NON-ACTUATING",
    );
    expect(screen.getByTestId("execution-sim-badge-ledger")).toHaveTextContent(
      "SIMULATED · NON-ACTUATING",
    );
    expect(screen.getByTestId("execution-sim-badge-risk")).toHaveTextContent(
      "SIMULATED · NON-ACTUATING",
    );
    expect(screen.getByTestId("execution-sim-badge-experiments")).toHaveTextContent(
      "SIMULATED · NON-ACTUATING",
    );
    expect(screen.getByTestId("execution-sim-badge-analytics")).toHaveTextContent(
      "SIMULATED · NON-ACTUATING",
    );
  });

  it("test_surf_p01_r4_testid_hooks_cover_every_major_region", () => {
    // R4 / S4: data-testid across all regions.
    renderWorkspace({ bundle });

    expect(screen.getByTestId("execution-research-header")).toBeInTheDocument();
    expect(screen.getByTestId("execution-research-refresh")).toBeInTheDocument();
    expect(screen.getByTestId("execution-research-disclaimer")).toBeInTheDocument();
    expect(screen.getByTestId("execution-investigation-context")).toBeInTheDocument();
    expect(screen.getByTestId("execution-group-runs")).toBeInTheDocument();
    expect(screen.getByTestId("execution-group-fills")).toBeInTheDocument();
    expect(screen.getByTestId("execution-group-ledger")).toBeInTheDocument();
    expect(screen.getByTestId("execution-group-risk")).toBeInTheDocument();
    expect(screen.getByTestId("execution-group-experiments")).toBeInTheDocument();
    expect(screen.getByTestId("execution-group-analytics")).toBeInTheDocument();
    expect(screen.getByTestId("execution-run-card-run-1")).toBeInTheDocument();
    expect(screen.getByTestId("execution-fill-card-fill-1")).toBeInTheDocument();
    expect(screen.getByTestId("execution-ledger-card-ledger-1")).toBeInTheDocument();
    expect(screen.getByTestId("execution-risk-card-risk-1")).toBeInTheDocument();
    expect(screen.getByTestId("execution-experiment-card-experiment-1")).toBeInTheDocument();
    expect(screen.getByTestId("execution-analytics-card-analytics-1")).toBeInTheDocument();
  });
});
