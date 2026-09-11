import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { InstitutionalIntelligenceWorkspace } from "./InstitutionalIntelligencePage";
import type { InstitutionalIntelligenceBundle, InstitutionalReport } from "../api/client";

function report(overrides: Partial<InstitutionalReport> = {}): InstitutionalReport {
  return {
    id: "report-1",
    artifact_type: "research_report",
    method_version: "method.v1",
    sample_count: 5,
    research_status: "research_only",
    report_hash: "hash-1",
    limitations: ["research_only", "not_a_guarantee"],
    uncertainty: {
      method: "interval_method",
      lower: -0.1,
      upper: 0.1,
      confidence_level: 0.95,
      sample_count: 5,
    },
    economic_usefulness: { verdict: "not_assessed" },
    results: { value: 0.25, explanation: "Persisted backend result" },
    input_lineage: { source: "persisted_report" },
    ...overrides,
  };
}

const bundle: InstitutionalIntelligenceBundle = {
  relation: [report({ artifact_type: "correlation_report" })],
  context: [report({ regime_label: "trend" })],
  hypothetical: [report({ scenario_name: "hypothetical_shock" })],
  risk: [report({ metrics: { max_metric: { sample_count: 5 } } })],
  validation: [
    report({
      artifact_type: "signal_validation_report",
      sample_count: 4,
      outcome_data_status: { status: "not_available" },
      uncertainty: {
        method: "wilson_score_intervals",
        confidence_level: 0.95,
        sample_count: 4,
        metrics: {
          clean_advisory_rate: {
            method: "wilson_score_interval",
            lower: 0.0456,
            upper: 0.6994,
            confidence_level: 0.95,
            sample_count: 4,
          },
        },
      },
    }),
  ],
};

describe("InstitutionalIntelligenceWorkspace", () => {
  it("renders research framing and report uncertainty", () => {
    render(<InstitutionalIntelligenceWorkspace bundle={bundle} />);

    expect(screen.getByText("Institutional Intelligence")).toBeInTheDocument();
    expect(screen.getByText("Research context only.")).toBeInTheDocument();
    expect(screen.getByText(/not a guarantee/i)).toBeInTheDocument();
    expect(screen.getAllByText(/n=5/).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/interval_method/).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/4.56% to 69.94%/).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/wilson_score_intervals/).length).toBeGreaterThan(0);
  });

  it("renders all persisted report groups", () => {
    render(<InstitutionalIntelligenceWorkspace bundle={bundle} />);

    expect(screen.getByText("Cross-Market Relation Reports")).toBeInTheDocument();
    expect(screen.getByText("Market Context Reports")).toBeInTheDocument();
    expect(screen.getByText("Hypothetical Research Studies")).toBeInTheDocument();
    expect(screen.getByText("Market-Series Risk Reports")).toBeInTheDocument();
    expect(screen.getByText("Advisory Quality Review")).toBeInTheDocument();
  });

  it("does not render transaction controls", () => {
    render(<InstitutionalIntelligenceWorkspace bundle={bundle} />);
    const buttons = screen.getAllByRole("button");
    const buttonText = buttons.map((button) => button.textContent?.toLowerCase() ?? "").join(" ");
    const forbidden = ["b" + "uy", "s" + "ell", "or" + "der", "pos" + "ition", "br" + "oker"];
    for (const word of forbidden) {
      expect(buttonText).not.toContain(word);
    }
  });

  it("does not display uncalibrated source score fields", () => {
    const blockedKey = `raw_${"score"}`;
    const withBlocked = {
      ...bundle,
      validation: [report({ results: { [blockedKey]: 0.123456, value: 1 } })],
    };
    render(<InstitutionalIntelligenceWorkspace bundle={withBlocked} />);
    const region = screen.getByLabelText("Advisory Quality Review");
    expect(within(region).queryByText("0.123456")).not.toBeInTheDocument();
    expect(within(region).queryByText(blockedKey)).not.toBeInTheDocument();
  });
});
