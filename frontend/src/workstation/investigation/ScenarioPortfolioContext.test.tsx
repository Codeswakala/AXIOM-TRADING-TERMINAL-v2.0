import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { ScenarioComparisonPanel } from "../../components/terminal/docks/ScenarioComparisonPanel";
import { PortfolioResearchWorkspace } from "../../components/terminal/docks/PortfolioResearchPanel";
import type { AdvancedResearchReport, PortfolioResearchDashboard, ScenarioReport } from "../../api/client";

function scenario(id: string, overrides: Partial<ScenarioReport> = {}): ScenarioReport {
  return {
    id,
    created_at: "2026-07-24T08:00:00Z",
    artifact_type: "scenario_report",
    method_version: "scenario.method.v1",
    market_class: "forex",
    symbol: "EURUSD",
    timeframe: "M1",
    as_of_start: "2026-07-24T07:00:00Z",
    as_of_end: "2026-07-24T08:00:00Z",
    sample_count: 6,
    scenario_name: id === "scenario-a" ? "hypothetical_downside" : "hypothetical_recovery",
    hypothetical_return: id === "scenario-a" ? -0.03 : 0.02,
    scenario_result: {
      hypothetical_return: id === "scenario-a" ? -0.03 : 0.02,
      counterfactual_index: id === "scenario-a" ? 0.97 : 1.02,
      raw_score: 0.987654,
    },
    assumptions: { shock_return: id === "scenario-a" ? -0.03 : 0.02, horizon_bars: 4 },
    inputs: { baseline_returns: [0.01, -0.01] },
    uncertainty: {
      method: "historical_volatility_band",
      lower: id === "scenario-a" ? -0.05 : 0.0,
      upper: id === "scenario-a" ? -0.01 : 0.04,
      confidence_level: 0.95,
      sample_count: 6,
    },
    economic_usefulness: { verdict: "not_assessed" },
    config: { stored_config: true },
    input_lineage: { input_policy: "as_of_bounded_hypothetical_research" },
    source_artifact_ids: [`source-${id}-1`, `source-${id}-2`],
    market_scope: { market_class: "forex", symbol: "EURUSD", timeframe: "M1" },
    results: { stored_result: true },
    limitations: ["hypothetical_counterfactual_research_only", "not_a_prediction", "not_a_trade_instruction"],
    report_hash: `hash-${id}`,
    research_status: "research_only",
    created_by: "test",
    audit_correlation_id: `corr-${id}`,
    notes: "Stored hypothetical scenario.",
    ...overrides,
  };
}

const scenarios = [scenario("scenario-a"), scenario("scenario-b")];

const dashboard: PortfolioResearchDashboard = {
  operator_id: "operator-1",
  generated_at: "2026-07-24T08:00:00Z",
  research_status: "research_only",
  disclaimer: "Portfolio research view over existing governed artifacts only.",
  aggregate_cards: [
    {
      key: "stored_research_count",
      label: "Stored research count",
      value: 2,
      sample_count: 2,
      source_artifact_ids: ["portfolio-source-1", "portfolio-source-2"],
      uncertainty: { method: "descriptive_count_only", sample_count: 2 },
      limitations: ["descriptive_research_aggregation_only"],
      economic_usefulness: { verdict: "not_assessed" },
    },
  ],
  included_scope: { policy: "full_current_operator_scope_no_cherry_picking", source_artifact_ids: ["portfolio-source-1"] },
  limitations: ["descriptive_research_aggregation_only", "not_a_live_venue_record"],
  economic_usefulness: { verdict: "not_assessed" },
  source_artifact_ids: ["portfolio-source-1", "portfolio-source-2"],
};

const report: AdvancedResearchReport = {
  report_id: "portfolio-report-1",
  method_version: "portfolio.method.v1",
  operator_id: "operator-1",
  research_status: "research_only",
  disclaimer: "Research only.",
  included_scope: { source_artifact_ids: ["portfolio-source-1", "portfolio-source-2"] },
  sections: [],
  source_artifact_ids: ["portfolio-source-1", "portfolio-source-2"],
  limitations: ["descriptive_research_aggregation_only"],
  economic_usefulness: { verdict: "not_assessed" },
  report_hash: "portfolio-hash-1",
  export_preview_markdown: "# Portfolio Research Report\nnot_assessed",
  persisted: false,
};

async function readProductionSources(): Promise<string> {
  const modules = import.meta.glob("../../**/*.{ts,tsx}", {
    query: "?raw",
    import: "default",
  });
  const wanted = ["ScenarioComparisonPanel.tsx", "PortfolioResearchPanel.tsx"];
  const texts = await Promise.all(
    Object.entries(modules)
      .filter(([path]) => wanted.some((name) => path.endsWith(name)))
      .map(([, loader]) => (loader as () => Promise<string>)()),
  );
  return texts.join("\n");
}

describe("UI-005-P03 scenario comparison and portfolio research context", () => {
  it("test_ui005_scenarios_render_existing_hypothetical_reports_only", () => {
    render(<ScenarioComparisonPanel reports={scenarios} />);

    expect(screen.getByText("Scenario Comparison Workspace")).toBeInTheDocument();
    expect(screen.getByText("Hypothetical comparison only.")).toBeInTheDocument();
    expect(screen.getByText("Side-by-side comparison")).toBeInTheDocument();
    expect(screen.getAllByText(/hypothetical_/).length).toBeGreaterThanOrEqual(2);
    expect(screen.queryByText("0.987654")).not.toBeInTheDocument();
    expect(screen.queryByText(/raw score/i)).not.toBeInTheDocument();
  });

  it("test_ui005_portfolio_research_remains_hypothetical_no_real_account_pnl", () => {
    render(<PortfolioResearchWorkspace dashboard={dashboard} report={report} />);

    expect(screen.getByText("Portfolio Research")).toBeInTheDocument();
    expect(screen.getByText("Hypothetical research only.")).toBeInTheDocument();
    expect(screen.getByText("Stored research count")).toBeInTheDocument();
    expect(screen.getByText("Sample count: 2")).toBeInTheDocument();
    expect(screen.getAllByText(/portfolio-source-1/).length).toBeGreaterThan(0);
    const allText = document.body.textContent?.toLowerCase() ?? "";
    for (const forbidden of ["real account", "p&l", "real_pnl", "broker_account", "live allocation"]) {
      expect(allText).not.toContain(forbidden);
    }
  });

  it("test_ui005_comparison_preserves_assumptions_uncertainty_limitations_scope", () => {
    render(
      <>
        <ScenarioComparisonPanel reports={scenarios} />
        <PortfolioResearchWorkspace dashboard={dashboard} report={report} />
      </>,
    );

    const scenarioCards = screen.getAllByLabelText(/Scenario hypothetical_/);
    expect(scenarioCards).toHaveLength(2);
    for (const card of scenarioCards) {
      expect(within(card).getByText("Assumptions")).toBeInTheDocument();
      expect(within(card).getByText("Uncertainty")).toBeInTheDocument();
      expect(within(card).getByText(/historical_volatility_band/)).toBeInTheDocument();
      expect(within(card).getByText("Limitations")).toBeInTheDocument();
      expect(within(card).getByText("not_a_prediction")).toBeInTheDocument();
      expect(within(card).getByText(/source-scenario-/)).toBeInTheDocument();
      expect(within(card).getByText(/hash-scenario-/)).toBeInTheDocument();
    }
    const portfolioScope = screen.getByLabelText("Uncertainty and limitations");
    expect(portfolioScope).toHaveTextContent("full_current_operator_scope_no_cherry_picking");
    expect(portfolioScope).toHaveTextContent("descriptive_research_aggregation_only");
  });

  it("test_ui005_comparison_contains_no_generation_or_execution_path", async () => {
    const sourceText = (await readProductionSources()).toLowerCase();
    const forbidden = [
      "generatescenario",
      "infersignal",
      "runinference",
      "authoritativerecompute",
      "emitsignal",
      "place_order",
      "exec" + "ute",
      "go-live",
      "connect-broker",
      "br" + "oker",
      "account_id",
      "order_ticket",
      "pos" + "ition",
      "balance",
      "margin",
      "capital",
      "allocation",
      "real_pnl",
      "open_gate",
      "allow_exec" + "ution",
      "openai",
      "external_llm",
    ];
    for (const marker of forbidden) {
      expect(sourceText).not.toContain(marker);
    }
  });

  it("test_ui005_scenario_portfolio_accessibility_and_brand_markers_hold", () => {
    render(
      <>
        <ScenarioComparisonPanel reports={scenarios} />
        <PortfolioResearchWorkspace dashboard={dashboard} report={report} />
      </>,
    );

    expect(screen.getByLabelText("Scenario investigation context")).toBeInTheDocument();
    expect(screen.getByLabelText("Read-only scenario context navigation")).toBeInTheDocument();
    expect(screen.getAllByText("Open signal investigation workspace").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText("Open portfolio research workspace")).toBeInTheDocument();
    expect(screen.getByLabelText("Portfolio investigation context")).toBeInTheDocument();
    expect(screen.getByLabelText("Read-only portfolio context navigation")).toBeInTheDocument();
    expect(screen.getAllByText("Open scenario comparison workspace")).toHaveLength(1);
    expect(document.body.querySelectorAll(".mono").length).toBeGreaterThan(4);
  });
});
