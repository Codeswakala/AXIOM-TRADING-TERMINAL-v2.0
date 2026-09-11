import { fireEvent, render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { IntelligenceReportViewer } from "../../pages/InstitutionalIntelligencePage";
import type { InstitutionalIntelligenceBundle, InstitutionalReport } from "../../api/client";

function report(overrides: Partial<InstitutionalReport> = {}): InstitutionalReport {
  return {
    id: "report-ui004-p03",
    artifact_type: "correlation_report",
    method_version: "w4.report.v1",
    sample_count: 18,
    research_status: "research_only",
    report_hash: "hash-ui004-p03",
    limitations: ["research_only", "sample_bound"],
    uncertainty: {
      method: "wilson_score_interval",
      lower: 0.2,
      upper: 0.7,
      confidence_level: 0.95,
      sample_count: 18,
    },
    economic_usefulness: { verdict: "not_assessed" },
    source_artifact_ids: ["signal-1", "report-source-2"],
    input_lineage: { source_artifact_ids: ["lineage-1"], source: "persisted_report" },
    results: { stored_metric: 0.25, interpretation: "Persisted backend result" },
    ...overrides,
  };
}

const bundle: InstitutionalIntelligenceBundle = {
  relation: [report({ id: "relation-1", artifact_type: "correlation_report" })],
  context: [report({ id: "context-1", artifact_type: "regime_report", regime_label: "trend" })],
  hypothetical: [report({ id: "scenario-1", artifact_type: "scenario_report", scenario_name: "stored_scenario" })],
  risk: [report({ id: "risk-1", artifact_type: "portfolio_risk_report" })],
  validation: [report({ id: "validation-1", artifact_type: "signal_validation_report" })],
};

async function readProductionSource(pathSuffix: string): Promise<string> {
  const modules = import.meta.glob("../../**/*.{ts,tsx}", {
    query: "?raw",
    import: "default",
  });
  const fileName = pathSuffix.split("/").pop() ?? pathSuffix;
  const entry = Object.entries(modules).find(
    ([path]) => path.endsWith(pathSuffix) || path.endsWith(fileName),
  );
  if (!entry) throw new Error(`Raw source not found: ${pathSuffix}`);
  return (entry[1] as () => Promise<string>)();
}

describe("UI-004-P03 intelligence report viewers and drilldowns", () => {
  it("test_ui004_report_viewers_render_existing_intelligence_reports_only", () => {
    render(<IntelligenceReportViewer bundle={bundle} />);

    const viewer = screen.getByLabelText("First-party intelligence report viewer");
    expect(viewer).toHaveTextContent("First-party viewer for existing W4/W7 report payloads");
    expect(screen.getByLabelText("Report family navigation")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: /Family: Market Context Reports/i }));
    expect(screen.getByLabelText("Stored report artifact list")).toHaveTextContent("context-1");
    expect(screen.getByLabelText("Stored report detail viewer")).toHaveTextContent("regime_report");
  });

  it("test_ui004_drilldowns_disclose_stored_fields_without_recomputation", async () => {
    render(<IntelligenceReportViewer bundle={bundle} />);

    const drilldowns = screen.getByLabelText("Progressive report drilldowns");
    expect(within(drilldowns).getByText("Stored artifact fields")).toBeInTheDocument();
    expect(within(drilldowns).getByText("Source lineage and report integrity")).toBeInTheDocument();
    expect(within(drilldowns).getByText("Limitations and stored payload")).toBeInTheDocument();
    expect(drilldowns).toHaveTextContent("correlation_report");
    expect(drilldowns).toHaveTextContent("wilson_score_interval");

    const sourceText = await readProductionSource("pages/InstitutionalIntelligencePage.tsx");
    const forbidden = [
      "inferSignal",
      "runInference",
      "authoritativeRecompute",
      "recompute",
      "recalculat",
      "deriveConfidence",
      "reclassif",
      "new AnalyticsEngine",
      "new IntelligenceEngine",
      "/api/v1/orders",
    ];
    for (const marker of forbidden) {
      expect(sourceText).not.toContain(marker);
    }
  });

  it("test_ui004_report_viewers_preserve_lineage_uncertainty_limitations_and_hashes", () => {
    render(<IntelligenceReportViewer bundle={bundle} />);

    const detail = screen.getByLabelText("Stored report detail viewer");
    expect(detail).toHaveTextContent("hash-ui004-p03");
    expect(detail).toHaveTextContent("w4.report.v1");
    expect(detail).toHaveTextContent("18");
    expect(detail).toHaveTextContent("20.00% to 70.00%");
    expect(detail).toHaveTextContent("signal-1, report-source-2");
    expect(detail).toHaveTextContent("research_only");
    expect(detail).toHaveTextContent("sample_bound");
    expect(detail).toHaveTextContent("Persisted backend result");
  });

  it("test_ui004_report_viewers_use_first_party_components_no_new_dependency", async () => {
    const sourceText = await readProductionSource("pages/InstitutionalIntelligencePage.tsx");
    expect(sourceText).toContain("IntelligenceReportViewer");
    expect(sourceText).toContain("report-family-nav");
    const forbiddenDependencies = ["react-markdown", "marked", "markdown-it", "d3", "lodash", "openai", "gpt"];
    for (const dependency of forbiddenDependencies) {
      expect(sourceText).not.toContain(dependency);
    }
  });

  it("test_ui004_report_viewers_are_keyboard_and_screen_reader_accessible", () => {
    render(<IntelligenceReportViewer bundle={bundle} />);

    const nav = screen.getByLabelText("Report family navigation");
    const buttons = within(nav).getAllByRole("button");
    expect(buttons.length).toBeGreaterThan(3);
    buttons[1].focus();
    expect(buttons[1]).toHaveFocus();
    expect(buttons[0]).toHaveAttribute("aria-pressed", "true");
    fireEvent.click(buttons[1]);
    expect(buttons[1]).toHaveAttribute("aria-pressed", "true");
    expect(screen.getByLabelText("Stored report artifact list")).toBeInTheDocument();
    expect(screen.getByLabelText("Stored report detail viewer")).toBeInTheDocument();
    expect(screen.getByLabelText("Progressive report drilldowns")).toBeInTheDocument();
  });
});
