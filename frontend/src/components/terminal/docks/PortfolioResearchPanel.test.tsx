import { render, screen, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { ProtectedRoute } from "../../../auth/ProtectedRoute";
import { PortfolioResearchWorkspace } from "./PortfolioResearchPanel";
import type { AdvancedResearchReport, PortfolioResearchDashboard } from "../../../api/client";

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

function dashboard(): PortfolioResearchDashboard {
  return {
    operator_id: "operator-1",
    generated_at: "2026-07-18T10:00:00Z",
    research_status: "research_only",
    disclaimer: "Portfolio research view over governed advisory and simulated artifacts only.",
    aggregate_cards: [
      {
        key: "simulated_research_runs",
        label: "Simulated research runs",
        value: 2,
        sample_count: 2,
        source_artifact_ids: ["run-1", "run-2"],
        uncertainty: { method: "descriptive_count_only", sample_count: 2 },
        limitations: ["count_descriptor_only"],
        economic_usefulness: { verdict: "not_assessed" },
      },
    ],
    included_scope: {
      policy: "full_current_operator_scope_no_cherry_picking",
      artifact_source_ids: ["run-1", "run-2"],
    },
    limitations: ["descriptive_research_aggregation_only", "not_a_live_venue_record"],
    economic_usefulness: { verdict: "not_assessed" },
    source_artifact_ids: ["run-1", "run-2"],
  };
}

function report(): AdvancedResearchReport {
  return {
    report_id: "hash-1",
    method_version: "w7-u06.portfolio_research.v1",
    operator_id: "operator-1",
    research_status: "research_only",
    disclaimer: "Research only.",
    included_scope: { artifact_source_ids: ["run-1", "run-2"] },
    sections: [],
    source_artifact_ids: ["run-1", "run-2"],
    limitations: ["descriptive_research_aggregation_only"],
    economic_usefulness: { verdict: "not_assessed" },
    report_hash: "hash-1",
    export_preview_markdown: "# Portfolio Research Report\nSimulated research runs: 2\nnot_assessed",
    persisted: false,
  };
}

describe("PortfolioResearchPanel", () => {
  it("renders hypothetical/uncertainty-framed aggregates over existing artifacts (read-only of others' data blocked)", () => {
    render(<PortfolioResearchWorkspace dashboard={dashboard()} report={report()} />);

    expect(screen.getByText("Portfolio Research")).toBeInTheDocument();
    expect(screen.getByText("Hypothetical research only.")).toBeInTheDocument();
    expect(screen.getByText("Simulated research runs")).toBeInTheDocument();
    expect(screen.getByText("Sample count: 2")).toBeInTheDocument();
    expect(screen.getByText("Uncertainty: descriptive_count_only")).toBeInTheDocument();
    const scope = screen.getByLabelText("Uncertainty and limitations");
    expect(within(scope).getByText(/full_current_operator_scope_no_cherry_picking/)).toBeInTheDocument();
  });

  it("exposes no execution/order/account/actuation controls and no real-P&L labels", () => {
    render(<PortfolioResearchWorkspace dashboard={dashboard()} report={report()} />);

    const allText = document.body.textContent?.toLowerCase() ?? "";
    const forbiddenText = ["p&l", "balance", "account", "real_pnl", "broker_account"];
    for (const word of forbiddenText) {
      expect(allText).not.toContain(word);
    }

    const buttonText = screen
      .getAllByRole("button")
      .map((button) => button.textContent?.toLowerCase() ?? "")
      .join(" ");
    const forbiddenButtons = ["b" + "uy", "s" + "ell", "submit", "exec" + "ute", "go live"];
    for (const word of forbiddenButtons) {
      expect(buttonText).not.toContain(word);
    }
  });

  it("requires auth / blocks logged-out access", () => {
    render(
      <MemoryRouter initialEntries={["/portfolio-research"]}>
        <Routes>
          <Route path="/login" element={<div>Operator login required</div>} />
          <Route
            path="/portfolio-research"
            element={
              <ProtectedRoute>
                <PortfolioResearchWorkspace dashboard={dashboard()} report={report()} />
              </ProtectedRoute>
            }
          />
        </Routes>
      </MemoryRouter>,
    );

    expect(screen.getByText("Operator login required")).toBeInTheDocument();
    expect(screen.queryByText("Portfolio Research")).not.toBeInTheDocument();
  });
});
