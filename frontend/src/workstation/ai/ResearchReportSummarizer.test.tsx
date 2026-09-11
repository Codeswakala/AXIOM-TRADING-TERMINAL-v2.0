import { describe, it, expect } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import {
  ResearchReportSummarizer,
  summarizeRegimeReport,
  summarizeCorrelationReport,
  summarizeScenarioSimulation,
} from "./ResearchReportSummarizer";
import type { InstitutionalReport } from "../../api/client";

describe("UI-008-P04 ResearchReportSummarizer Component (T-1, T-4, T-5, T-6, U-3)", () => {
  const regimeReport: InstitutionalReport = {
    id: "rep-regime-501",
    artifact_type: "regime_report",
    method_version: "regime.v1",
    sample_count: 75,
    research_status: "verified",
    report_hash: "hash-regime-501",
    regime_label: "LOW_VOLATILITY_RANGING",
    limitations: ["Historical sample only"],
  };

  const correlationReport: InstitutionalReport = {
    id: "rep-corr-502",
    artifact_type: "correlation_report",
    method_version: "corr.v1",
    sample_count: 120,
    research_status: "verified",
    report_hash: "hash-corr-502",
    limitations: [],
  };

  const scenarioReport: InstitutionalReport = {
    id: "rep-scen-503",
    artifact_type: "scenario_report",
    method_version: "scen.v1",
    sample_count: 40,
    research_status: "research_only",
    report_hash: "hash-scen-503",
    scenario_name: "Interest Rate Shock",
    economic_usefulness: { verdict: "RESEARCH_VIABLE" },
    limitations: ["Simulation assumptions apply"],
  };

  // (T-1) Empty state rendering
  it("renders empty state message when no report is selected", () => {
    render(<ResearchReportSummarizer report={null} />);
    expect(screen.getByTestId("research-report-summarizer-empty")).toBeInTheDocument();
    expect(screen.getByTestId("summarizer-empty-message")).toHaveTextContent(
      "Select a research report to view its deterministic explainability summary",
    );
  });

  // (T-4) Regime report summarization
  it("renders deterministic regime report explanation and uncertainty badge (T-4)", () => {
    render(<ResearchReportSummarizer report={regimeReport} reportType="regime" />);

    expect(screen.getByTestId("research-report-summarizer")).toBeInTheDocument();
    expect(screen.getByTestId("summarizer-disclaimer")).toHaveTextContent(
      "Deterministic rule-based research summary only",
    );
    expect(screen.getByTestId("regime-summary-card")).toBeInTheDocument();
    expect(screen.getByTestId("regime-explanation")).toHaveTextContent("LOW VOLATILITY RANGING");
  });

  // (T-5) Correlation report summarization
  it("renders correlation report explanation and stability metrics (T-5)", () => {
    render(<ResearchReportSummarizer report={correlationReport} reportType="correlation" />);

    expect(screen.getByTestId("correlation-summary-card")).toBeInTheDocument();
    expect(screen.getByTestId("correlation-explanation")).toHaveTextContent("positive correlation");
  });

  // (T-6) Scenario simulation summarization
  it("renders scenario simulation explanation, assumptions, and impact (T-6)", () => {
    render(<ResearchReportSummarizer report={scenarioReport} reportType="scenario" />);

    expect(screen.getByTestId("scenario-summary-card")).toBeInTheDocument();
    expect(screen.getByTestId("scenario-explanation")).toHaveTextContent("Interest Rate Shock");
    expect(screen.getByText("Constant liquidity depth during simulated interval")).toBeInTheDocument();
  });

  // (U-3) Lineage tree toggle interaction
  it("toggles lineage tree visibility when toggle button is clicked (U-3)", () => {
    render(<ResearchReportSummarizer report={regimeReport} reportType="regime" />);

    const toggleBtn = screen.getByTestId("toggle-lineage-btn");
    expect(toggleBtn).toHaveTextContent("Hide Lineage Tree");
    expect(screen.getByTestId("summarizer-lineage-container")).toBeInTheDocument();

    fireEvent.click(toggleBtn);
    expect(toggleBtn).toHaveTextContent("Show Lineage Tree");
    expect(screen.queryByTestId("summarizer-lineage-container")).not.toBeInTheDocument();
  });

  // Summarizer helper functions
  describe("summarizer helpers", () => {
    it("summarizeRegimeReport produces structured output", () => {
      const summary = summarizeRegimeReport(regimeReport);
      expect(summary.regimeName).toBe("LOW_VOLATILITY_RANGING");
      expect(summary.sampleCount).toBe(75);
    });

    it("summarizeCorrelationReport produces structured output", () => {
      const summary = summarizeCorrelationReport(correlationReport);
      expect(summary.coefficient).toBe(0.72);
      expect(summary.stability).toBe("STABLE_POSITIVE");
    });

    it("summarizeScenarioSimulation produces structured output", () => {
      const summary = summarizeScenarioSimulation(scenarioReport);
      expect(summary.scenarioName).toBe("Interest Rate Shock");
      expect(summary.economicVerdict).toBe("RESEARCH_VIABLE");
      expect(summary.assumptions).toHaveLength(3);
    });
  });
});
