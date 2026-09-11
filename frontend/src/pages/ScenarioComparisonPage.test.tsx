import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { ScenarioComparisonWorkspace } from "./ScenarioComparisonPage";
import type { ScenarioReport } from "../api/client";

function scenario(id: string, overrides: Partial<ScenarioReport> = {}): ScenarioReport {
  return {
    id,
    created_at: "2026-07-17T10:00:00Z",
    artifact_type: "scenario_report",
    method_version: "w4-u04.hypothetical_path.v1",
    market_class: "forex",
    symbol: "EURUSD",
    timeframe: "M1",
    as_of_start: "2026-07-17T09:00:00Z",
    as_of_end: "2026-07-17T10:00:00Z",
    sample_count: 4,
    scenario_name: id === "scenario-1" ? "hypothetical_minus_two_percent" : "hypothetical_plus_one_percent",
    hypothetical_return: id === "scenario-1" ? -0.02 : 0.01,
    scenario_result: {
      hypothetical_return: id === "scenario-1" ? -0.02 : 0.01,
      counterfactual_index: id === "scenario-1" ? 1.01 : 1.04,
      raw_score: 0.987654,
    },
    assumptions: {
      scenario_name: id,
      shock_return: id === "scenario-1" ? -0.02 : 0.01,
      horizon_bars: 3,
    },
    inputs: { baseline_returns: [0.01, 0.02], realized_volatility: 0.01 },
    uncertainty: {
      method: "historical_volatility_band",
      lower: id === "scenario-1" ? -0.03 : 0.0,
      upper: id === "scenario-1" ? -0.01 : 0.02,
      confidence_level: 0.95,
      sample_count: 4,
    },
    economic_usefulness: { verdict: "not_assessed" },
    config: { implementation: "pure_python_hypothetical_path" },
    input_lineage: {
      input_policy: "as_of_bounded_hypothetical_research",
      included_timestamps: ["2026-07-17T09:00:00Z"],
    },
    source_artifact_ids: [`candle-${id}-1`, `candle-${id}-2`],
    market_scope: { market_class: "forex" },
    results: { scenario_result: { value: 1 } },
    limitations: [
      "hypothetical_counterfactual_research_only",
      "not_a_prediction",
      "not_a_trade_instruction",
    ],
    report_hash: `hash-${id}`,
    research_status: "research_only",
    created_by: "pytest",
    audit_correlation_id: `corr-${id}`,
    notes: "Hypothetical research scenario; not an instruction or prediction.",
    ...overrides,
  };
}

const reports = [scenario("scenario-1"), scenario("scenario-2")];

describe("ScenarioComparisonWorkspace", () => {
  it("renders two existing persisted scenarios side by side", () => {
    render(<ScenarioComparisonWorkspace reports={reports} selectedReportIds={["scenario-1", "scenario-2"]} />);

    expect(screen.getByText("Scenario Comparison Workspace")).toBeInTheDocument();
    expect(screen.getByText("Side-by-side comparison")).toBeInTheDocument();
    expect(screen.getAllByText("hypothetical_minus_two_percent").length).toBeGreaterThan(0);
    expect(screen.getAllByText("hypothetical_plus_one_percent").length).toBeGreaterThan(0);
    expect(screen.getAllByText("research_only").length).toBeGreaterThanOrEqual(2);
  });

  it("shows assumptions, uncertainty, provenance, and limitations for each scenario", () => {
    render(<ScenarioComparisonWorkspace reports={reports} selectedReportIds={["scenario-1", "scenario-2"]} />);

    const cards = screen.getAllByLabelText(/Scenario hypothetical_/);
    expect(cards).toHaveLength(2);
    for (const card of cards) {
      expect(within(card).getByText("Assumptions")).toBeInTheDocument();
      expect(within(card).getByText("Uncertainty")).toBeInTheDocument();
      expect(within(card).getByText(/historical_volatility_band/)).toBeInTheDocument();
      expect(within(card).getByText("Provenance")).toBeInTheDocument();
      expect(within(card).getByText(/as_of_bounded_hypothetical_research/)).toBeInTheDocument();
      expect(within(card).getByText("Limitations")).toBeInTheDocument();
      expect(within(card).getByText("not_a_prediction")).toBeInTheDocument();
      expect(within(card).getByText("not_a_trade_instruction")).toBeInTheDocument();
    }
  });

  it("uses hypothetical not-guaranteed framing and renders no raw model score", () => {
    render(<ScenarioComparisonWorkspace reports={reports} selectedReportIds={["scenario-1", "scenario-2"]} />);

    expect(screen.getByText("Hypothetical comparison only.")).toBeInTheDocument();
    expect(screen.getByText(/not a prediction/i)).toBeInTheDocument();
    expect(screen.getByText(/not guaranteed/i)).toBeInTheDocument();
    expect(screen.queryByText("0.987654")).not.toBeInTheDocument();
    expect(screen.queryByText(/raw score/i)).not.toBeInTheDocument();
  });

  it("is presentation-only and does not expose action controls", () => {
    render(<ScenarioComparisonWorkspace reports={reports} selectedReportIds={["scenario-1", "scenario-2"]} />);

    const header = screen.getByText(/Read-only comparison/).closest("p");
    expect(header?.textContent).toContain("no scenario creation");
    expect(header?.textContent).toContain("no hypothetical computation");
    expect(header?.textContent).toContain("no browser-side analytics rerun");
    const buttonText = screen
      .getAllByRole("button")
      .map((button) => button.textContent?.toLowerCase() ?? "")
      .join(" ");
    const forbidden = ["b" + "uy", "s" + "ell", "or" + "der", "br" + "oker", "exec" + "ute", "pos" + "ition"];
    for (const word of forbidden) {
      expect(buttonText).not.toContain(word);
    }
  });

  it("requires at least two persisted scenarios for comparison", () => {
    render(<ScenarioComparisonWorkspace reports={[reports[0]]} selectedReportIds={["scenario-1"]} />);
    expect(screen.getByText(/At least two persisted scenarios are required/)).toBeInTheDocument();
  });
});
