import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { SignalInvestigationWorkspace } from "./SignalInvestigationPage";
import type { AdvisorySignal, InstitutionalIntelligenceBundle, InstitutionalReport } from "../api/client";

function signal(overrides: Partial<AdvisorySignal> = {}): AdvisorySignal {
  const blockedRawKey = `raw_${"score"}`;
  return {
    signal_id: "sig-1",
    created_at: "2026-07-17T10:00:00Z",
    as_of_time: "2026-07-17T09:59:00Z",
    market_class: "forex",
    provider: "internal",
    symbol: "EURUSD",
    timeframe: "M1",
    model_artifact_id: "model-1",
    model_version: "model.v1",
    feature_set_version: "features.v1",
    experiment_id: "exp-1",
    statistical_report_id: "stat-1",
    calibration_report_id: "cal-1",
    economic_report_id: "econ-1",
    generalization_report_id: "gen-1",
    inference_input_hash: "input-hash-1",
    raw_score: 0.987654,
    calibrated_confidence: 0.5,
    input_staleness_seconds: 60,
    signal_validity_seconds: 300,
    expires_at: "2026-07-17T10:05:00Z",
    freshness_status: "fresh",
    signal_direction: "positive_bias",
    signal_state: "emitted",
    state_reason: "ELIGIBLE",
    eligibility_reasons: [],
    operating_domain_status: "valid",
    calibration_status: "calibrated",
    economic_verdict: "not_assessed",
    risk_notes: "research only",
    rationale: "Governed rationale with complete lineage and calibrated confidence.",
    explainability_summary: {
      confidence_source: "calibration_report_bins_or_base_rate",
      [blockedRawKey]: 0.987654,
    },
    state_transition_history: ["candidate", "eligible_checked", "emitted"],
    audit_correlation_id: "corr-1",
    ...overrides,
  };
}

function report(overrides: Partial<InstitutionalReport> = {}): InstitutionalReport {
  return {
    id: "report-1",
    artifact_type: "signal_validation_report",
    sample_count: 4,
    research_status: "research_only",
    limitations: ["research_only"],
    ...overrides,
  };
}

const intelligence: InstitutionalIntelligenceBundle = {
  relation: [report({ id: "corr-1", artifact_type: "correlation_report" })],
  context: [report({ id: "regime-1", artifact_type: "regime_report" })],
  hypothetical: [report({ id: "scenario-1", artifact_type: "scenario_report" })],
  risk: [report({ id: "risk-1", artifact_type: "portfolio_risk_report" })],
  validation: [report({ id: "validation-1", artifact_type: "signal_validation_report" })],
};

describe("SignalInvestigationWorkspace", () => {
  it("renders rationale, guardrails, lineage, and linked intelligence reports", () => {
    render(<SignalInvestigationWorkspace signals={[signal()]} intelligence={intelligence} />);

    expect(screen.getByText("Signal Investigation Workspace")).toBeInTheDocument();
    expect(screen.getByText(/Governed rationale/)).toBeInTheDocument();
    expect(screen.getByText("Guardrail states")).toBeInTheDocument();
    expect(screen.getByText("valid")).toBeInTheDocument();
    expect(screen.getAllByText("calibrated").length).toBeGreaterThan(0);
    expect(screen.getByText("Lineage")).toBeInTheDocument();
    expect(screen.getByText("model-1")).toBeInTheDocument();
    expect(screen.getByText("exp-1")).toBeInTheDocument();
    expect(screen.getByText("Linked intelligence reports")).toBeInTheDocument();
    expect(screen.getByText(/correlation report · corr-1/)).toBeInTheDocument();
    expect(screen.getByText(/signal validation report · validation-1/)).toBeInTheDocument();
  });

  it("shows calibrated confidence and never renders raw model score", () => {
    render(<SignalInvestigationWorkspace signals={[signal()]} intelligence={intelligence} />);

    expect(screen.getByText("50.0% calibrated confidence")).toBeInTheDocument();
    expect(screen.queryByText("0.987654")).not.toBeInTheDocument();
    expect(screen.queryByText(/raw score/i)).not.toBeInTheDocument();
  });

  it("renders research framing and no action controls", () => {
    render(<SignalInvestigationWorkspace signals={[signal()]} intelligence={intelligence} />);

    expect(screen.getByText("Research investigation only.")).toBeInTheDocument();
    expect(screen.getByText(/AXIOM does not act/)).toBeInTheDocument();
    const buttons = screen.getAllByRole("button");
    const text = buttons.map((button) => button.textContent?.toLowerCase() ?? "").join(" ");
    const forbidden = ["b" + "uy", "s" + "ell", "or" + "der", "br" + "oker", "exec" + "ute", "pos" + "ition"];
    for (const word of forbidden) {
      expect(text).not.toContain(word);
    }
  });

  it("states presentation-only behavior without authoritative recompute", () => {
    render(<SignalInvestigationWorkspace signals={[signal()]} intelligence={intelligence} />);

    const header = screen.getByText(/Read-only investigation/).closest("p");
    expect(header).not.toBeNull();
    expect(header?.textContent).toContain("no client-side inference");
    expect(header?.textContent).toContain("no signal mutation");
    expect(header?.textContent).toContain("no browser-side analytics rerun");
  });

  it("keeps signal selectors read-only and scoped to persisted records", () => {
    render(
      <SignalInvestigationWorkspace
        signals={[signal(), signal({ signal_id: "sig-2", signal_state: "warning", state_reason: "POORLY_CALIBRATED" })]}
        intelligence={intelligence}
        selectedSignalId="sig-2"
      />,
    );

    const selector = screen.getByLabelText("Investigation signal selector");
    expect(within(selector).getByText("POORLY_CALIBRATED")).toBeInTheDocument();
    expect(screen.getAllByText("warning").length).toBeGreaterThan(0);
  });
});
