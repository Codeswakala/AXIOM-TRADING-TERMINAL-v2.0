import { render, screen, within } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { TradePlanningWorkspace } from "./TradePlanningPage";
import type { TradePlanNote } from "../api/client";

function plan(overrides: Partial<TradePlanNote> = {}): TradePlanNote {
  return {
    plan_id: "plan-1",
    created_at: "2026-07-17T10:00:00Z",
    updated_at: "2026-07-17T10:00:00Z",
    operator_id: "operator",
    title: "Inert research plan",
    market_context: "EURUSD M1 governed context.",
    hypothesis: "Research hypothesis linked to governed evidence.",
    linked_signal_ids: ["signal-1"],
    linked_report_ids: ["report-1"],
    scenario_notes: "Hypothetical context only.",
    risk_notes: "Research risk notes only.",
    invalidating_conditions_text: "Archive if evidence changes.",
    decision_status: "draft",
    research_disclaimer:
      "Trade plan research note only. Hypothetical research, not financial advice, not a trade instruction, not an order ticket. Operator judgment required. AXIOM does not act.",
    research_status: "research_only",
    audit_correlation_id: "corr-1",
    ...overrides,
  };
}

describe("TradePlanningWorkspace", () => {
  it("renders persisted research plan note with disclaimer and linked ids", () => {
    render(<TradePlanningWorkspace plans={[plan()]} />);

    expect(screen.getByText("Trade Planning Workspace")).toBeInTheDocument();
    expect(screen.getByText("Research plan note only.")).toBeInTheDocument();
    expect(screen.getAllByText(/AXIOM does not act/).length).toBeGreaterThan(0);
    const detail = screen.getByLabelText("Trade plan research note detail");
    expect(within(detail).getByText("Inert research plan")).toBeInTheDocument();
    expect(within(detail).getByText("signal-1")).toBeInTheDocument();
    expect(within(detail).getByText("report-1")).toBeInTheDocument();
    expect(within(detail).getByText("research_only")).toBeInTheDocument();
  });

  it("renders only research-note fields and no order-ticket input labels", () => {
    render(<TradePlanningWorkspace plans={[plan()]} />);

    expect(screen.getByLabelText("Create inert trade plan note")).toBeInTheDocument();
    expect(screen.getAllByText("Market context").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Hypothesis").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Invalidating conditions").length).toBeGreaterThan(0);
    const forbiddenLabels = [
      /quantity/i,
      /lot/i,
      /size/i,
      /stop loss/i,
      /take profit/i,
      /broker/i,
      /account/i,
      /position/i,
    ];
    for (const label of forbiddenLabels) {
      expect(screen.queryByLabelText(label)).not.toBeInTheDocument();
    }
  });

  it("does not expose action controls", () => {
    render(<TradePlanningWorkspace plans={[plan()]} />);

    const buttonText = screen
      .getAllByRole("button")
      .map((button) => button.textContent?.toLowerCase() ?? "")
      .join(" ");
    const forbidden = ["b" + "uy", "s" + "ell", "exec" + "ute", "submit", "dispatch"];
    for (const word of forbidden) {
      expect(buttonText).not.toContain(word);
    }
  });

  it("creates and updates research notes through plan-store callbacks only", async () => {
    const onCreatePlan = vi.fn();
    const onUpdatePlan = vi.fn();
    render(
      <TradePlanningWorkspace
        plans={[plan()]}
        onCreatePlan={onCreatePlan}
        onUpdatePlan={onUpdatePlan}
      />,
    );

    screen.getByText("Save research note").click();
    expect(onCreatePlan).toHaveBeenCalledTimes(1);
    screen.getByText("Update selected note").click();
    expect(onUpdatePlan).toHaveBeenCalledTimes(1);
  });

  it("shows empty state without execution wording", () => {
    render(<TradePlanningWorkspace plans={[]} />);
    expect(screen.getByText(/No trade plan research notes/)).toBeInTheDocument();
    const text = screen.getByLabelText("Persisted trade plan notes").textContent?.toLowerCase() ?? "";
    expect(text).not.toContain("execute");
    expect(text).not.toContain("broker");
  });
});
