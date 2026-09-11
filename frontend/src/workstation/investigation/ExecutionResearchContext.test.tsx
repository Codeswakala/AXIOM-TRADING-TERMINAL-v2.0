import { render, screen, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";
import {
  EXECUTION_RESEARCH_DISCLAIMER,
  ExecutionResearchWorkspace,
} from "../../components/terminal/execution/ExecutionResearchView";
import type { ExecutionResearchBundle } from "../../api/client";

// SURF-P01 re-target (b): the workspace renders react-router Links, so plain
// renders are wrapped in a router.
function renderWorkspace(bundle: ExecutionResearchBundle) {
  return render(
    <MemoryRouter>
      <ExecutionResearchWorkspace bundle={bundle} />
    </MemoryRouter>,
  );
}

const simulatedBundle: ExecutionResearchBundle = {
  runs: [
    {
      run_id: "run-ui005-p05-1",
      created_at: "2026-07-25T08:00:00Z",
      operator_id: "operator-1",
      simulation_mode: "SIMULATED",
      simulation_policy_version: "simulation.policy.v1",
      input_artifact_ids: ["signal-ui005-p05-1", "plan-ui005-p05-1"],
      replay_scope: { symbol: "EURUSD", timeframe: "M1", as_of_policy: "bounded_replay" },
      fill_model_name: "deterministic_mid_close_slippage",
      fill_model_version: "fill.model.v1",
      assumptions: { deterministic: true, slippage_bps: 0.5 },
      limitations: ["simulated_research_only", "not_production_outcome"],
      research_status: "research_only",
      simulation_disclaimer: EXECUTION_RESEARCH_DISCLAIMER,
      audit_correlation_id: "corr-run-ui005-p05-1",
    },
  ],
  fills: [
    {
      simulated_fill_id: "fill-ui005-p05-1",
      run_id: "run-ui005-p05-1",
      created_at: "2026-07-25T08:00:00Z",
      simulation_mode: "SIMULATED",
      market_class: "forex",
      symbol: "EURUSD",
      timeframe: "M1",
      as_of_time: "2026-07-25T08:00:00Z",
      simulated_research_direction: "long_bias",
      simulated_units: 1,
      requested_reference_price: 1.1,
      simulated_fill_price: 1.100055,
      simulated_slippage_bps: 0.5,
      source_candle_ids: ["candle-ui005-p05-1"],
      fill_model_name: "deterministic_mid_close_slippage",
      fill_model_version: "fill.model.v1",
      research_status: "research_only",
      simulation_disclaimer: EXECUTION_RESEARCH_DISCLAIMER,
      audit_correlation_id: "corr-fill-ui005-p05-1",
    },
  ],
  ledger: [
    {
      ledger_entry_id: "ledger-ui005-p05-1",
      created_at: "2026-07-25T08:00:00Z",
      simulation_mode: "SIMULATED",
      run_id: "run-ui005-p05-1",
      simulated_fill_id: "fill-ui005-p05-1",
      operator_id: "operator-1",
      ledger_event_type: "simulated_close_estimate",
      simulated_research_direction: "long_bias",
      simulated_units: 1,
      simulated_entry_value: 1.1,
      simulated_exit_value: 1.111,
      simulated_return_estimate: 0.01,
      uncertainty: { method: "fixed_simulated_estimate_band", sample_count: 1 },
      limitations: ["simulated_return_estimate_only"],
      research_status: "research_only",
      simulation_disclaimer: EXECUTION_RESEARCH_DISCLAIMER,
      audit_correlation_id: "corr-ledger-ui005-p05-1",
    },
  ],
  riskReports: [
    {
      report_id: "risk-ui005-p05-1",
      created_at: "2026-07-25T08:00:00Z",
      simulation_mode: "SIMULATED",
      input_artifact_ids: ["ledger-ui005-p05-1"],
      simulated_request_summary: { ledger_entry_ids: ["ledger-ui005-p05-1"] },
      risk_metrics: { simulated_fill_count: { value: 1 } },
      uncertainty: { method: "sample_range_or_single_sample_limitation", sample_count: 1 },
      limitations: ["economic_usefulness_not_assessed"],
      economic_usefulness: { verdict: "not_assessed" },
      research_status: "research_only",
      simulation_disclaimer: EXECUTION_RESEARCH_DISCLAIMER,
      audit_correlation_id: "corr-risk-ui005-p05-1",
    },
  ],
  experiments: [
    {
      experiment_id: "experiment-ui005-p05-1",
      created_at: "2026-07-25T08:00:00Z",
      simulation_mode: "SIMULATED",
      operator_id: "operator-1",
      experiment_title: "Pre-registered replay context",
      pre_registration_plan: { hypothesis: "research_continuity", horizon_bars: 4 },
      plan_hash: "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
      as_of_time: "2026-07-25T08:00:00Z",
      as_of_window: { as_of_time: "2026-07-25T08:00:00Z", lookahead_rows: 0 },
      replay_input_lineage: { included_candle_ids: ["candle-ui005-p05-1"] },
      included_scope_summary: { full_scope_included: true },
      uncertainty: { method: "replay_scope_count_limitation", sample_count: 1 },
      limitations: ["as_of_bounded_no_future_rows"],
      research_status: "research_only",
      simulation_disclaimer: EXECUTION_RESEARCH_DISCLAIMER,
      audit_correlation_id: "corr-experiment-ui005-p05-1",
    },
  ],
  analyticsReports: [
    {
      report_id: "analytics-ui005-p05-1",
      created_at: "2026-07-25T08:00:00Z",
      simulation_mode: "SIMULATED",
      analytics_type: "return_estimate_review",
      included_scope: { full_scope_included: true, sample_count: 3 },
      sample_count: 3,
      metrics: { simulated_average_return_estimate: { value: 0.01 } },
      uncertainty: {
        method: "per_metric_interval_or_insufficient_sample_limitation",
        sample_count: 3,
        metrics: { simulated_average_return_estimate: { method: "insufficient_sample_limitation" } },
      },
      limitations: ["full_declared_scope_included", "simulated_research_only"],
      economic_usefulness: { verdict: "not_assessed" },
      report_hash: "abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcd",
      source_artifact_ids: ["fill-ui005-p05-1", "ledger-ui005-p05-1", "experiment-ui005-p05-1"],
      research_status: "research_only",
      simulation_disclaimer: EXECUTION_RESEARCH_DISCLAIMER,
      audit_correlation_id: "corr-analytics-ui005-p05-1",
    },
  ],
};

async function readExecutionResearchSource(): Promise<string> {
  // SURF-P01 re-target: the UI-005 execution research surface relocated from
  // pages/ExecutionResearchPage.tsx to the execution stage view module.
  const modules = import.meta.glob("../../components/terminal/execution/*.{ts,tsx}", {
    query: "?raw",
    import: "default",
  });
  const entry = Object.entries(modules).find(([path]) => path.endsWith("ExecutionResearchView.tsx"));
  if (!entry) throw new Error("ExecutionResearchView source not found");
  return (entry[1] as () => Promise<string>)();
}

describe("UI-005-P05 execution research SIMULATED evidence context", () => {
  it("test_ui005_execution_research_renders_existing_simulated_artifacts_only", async () => {
    renderWorkspace(simulatedBundle);

    expect(screen.getByText("Execution Research Workspace")).toBeInTheDocument();
    expect(screen.getByText("SIMULATED.")).toBeInTheDocument();
    expect(screen.getAllByText("SIMULATED").length).toBeGreaterThanOrEqual(6);
    expect(screen.getByLabelText("Execution research investigation context")).toHaveTextContent(
      "execution-research read seams",
    );
    expect(screen.getAllByText("run-ui005-p05-1").length).toBeGreaterThan(0);
    expect(screen.getByText("EURUSD · M1")).toBeInTheDocument();
    expect(screen.getByText("simulated_close_estimate")).toBeInTheDocument();
    expect(screen.getByText("Pre-registered replay context")).toBeInTheDocument();
    expect(screen.getByText("return_estimate_review")).toBeInTheDocument();

    const sourceText = await readExecutionResearchSource();
    expect(sourceText).toContain("fetchSimulatedRunsList");
  });

  it("test_ui005_execution_research_never_claims_live_execution_or_real_fills", () => {
    renderWorkspace(simulatedBundle);

    const allText = document.body.textContent?.toLowerCase() ?? "";
    for (const phrase of [
      "live execution",
      "live fill",
      "live fills",
      "real fill",
      "real fills",
      "real order",
      "real pnl",
      "real p&l",
      "production execution",
    ]) {
      expect(allText).not.toContain(phrase);
    }
    expect(allText).toContain("simulated execution research only");
    expect(allText).toContain("gate closed");
  });

  it("test_ui005_execution_research_preserves_assumptions_uncertainty_limitations", () => {
    renderWorkspace(simulatedBundle);

    const run = screen.getByLabelText("Simulated run run-ui005-p05-1");
    expect(within(run).getByText("Assumptions")).toBeInTheDocument();
    expect(within(run).getByText("deterministic")).toBeInTheDocument();
    expect(within(run).getByText("simulated_research_only")).toBeInTheDocument();
    expect(within(run).getByText("signal-ui005-p05-1, plan-ui005-p05-1")).toBeInTheDocument();

    const ledger = screen.getByLabelText("Simulated ledger ledger-ui005-p05-1");
    expect(within(ledger).getByText(/fixed_simulated_estimate_band/)).toBeInTheDocument();
    expect(within(ledger).getByText("simulated_return_estimate_only")).toBeInTheDocument();

    const risk = screen.getByLabelText("Execution risk report risk-ui005-p05-1");
    expect(within(risk).getByText(/sample_range_or_single_sample_limitation/)).toBeInTheDocument();
    expect(within(risk).getByText("economic_usefulness_not_assessed")).toBeInTheDocument();

    const experiment = screen.getByLabelText("Execution experiment experiment-ui005-p05-1");
    expect(within(experiment).getByText("as_of_bounded_no_future_rows")).toBeInTheDocument();
    expect(within(experiment).getByText("full_scope_included")).toBeInTheDocument();

    const analytics = screen.getByLabelText("Simulated analytics analytics-ui005-p05-1");
    expect(within(analytics).getByText(/per-metric uncertainty present/)).toBeInTheDocument();
    expect(within(analytics).getByText("full_declared_scope_included")).toBeInTheDocument();
    expect(within(analytics).getByText(/abcdefabcdef/)).toBeInTheDocument();
  });

  it("test_ui005_execution_research_contains_no_broker_order_account_or_gate_path", async () => {
    renderWorkspace(simulatedBundle);

    const buttonText = screen
      .getAllByRole("button")
      .map((button) => button.textContent?.toLowerCase() ?? "")
      .join(" ");
    for (const marker of ["b" + "uy", "s" + "ell", "exec" + "ute", "submit", "dispatch"]) {
      expect(buttonText).not.toContain(marker);
    }

    const sourceText = (await readExecutionResearchSource()).toLowerCase();
    for (const marker of [
      "place_order",
      "exec" + "ute",
      "go-live",
      "connect-" + "broker",
      "br" + "oker",
      "account_id",
      "order_" + "ticket",
      "pos" + "ition",
      "balance",
      "margin",
      "capital",
      "allocation",
      "real_pnl",
      "open_gate",
      "allow_exec" + "ution",
      "/api/v1/orders",
      "openai",
      "external_llm",
    ]) {
      expect(sourceText).not.toContain(marker);
    }
  });

  it("test_ui005_execution_research_accessibility_and_brand_markers_hold", () => {
    renderWorkspace(simulatedBundle);

    expect(screen.getByLabelText("Execution research disclaimer")).toHaveTextContent("SIMULATED");
    expect(screen.getByLabelText("Execution research investigation context")).toHaveTextContent(
      "Gate CLOSED",
    );
    expect(screen.getByLabelText("Read-only execution research context navigation")).toBeInTheDocument();
    expect(screen.getByText("Open signal investigation workspace")).toBeInTheDocument();
    expect(screen.getByText("Open trade planning workspace")).toBeInTheDocument();
    expect(screen.getByText("Open research journal workspace")).toBeInTheDocument();
    expect(screen.getByText("Open scenario comparison workspace")).toBeInTheDocument();
    expect(screen.getByText("Open portfolio research workspace")).toBeInTheDocument();
    expect(screen.getByLabelText("Execution research artifact counts")).toBeInTheDocument();
    expect(document.body.querySelectorAll(".mono").length).toBeGreaterThanOrEqual(8);
  });
});
