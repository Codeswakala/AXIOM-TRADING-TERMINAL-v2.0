import { render, screen, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import {
  InstitutionalIntelligenceWorkspace,
  ResearchPerformanceAnalyticsPanel,
} from "../../pages/InstitutionalIntelligencePage";
import type { AdvisoryAnalyticsResponse, InstitutionalIntelligenceBundle } from "../../api/client";
import { InstitutionalWorkspaceShell } from "../components/InstitutionalWorkspaceShell";

const authState = vi.hoisted(() => ({
  value: {
    operator: { username: "operator", role: "admin" },
    loading: false,
    isAuthenticated: true,
    logout: vi.fn(),
    login: vi.fn(),
    refreshProfile: vi.fn(),
  },
}));

vi.mock("../../context/AuthContext", () => ({
  useAuth: () => authState.value,
}));

vi.mock("../persistence/shellPreferences", () => ({
  loadShellLayoutPreference: vi.fn().mockResolvedValue(null),
  persistShellLayoutPreference: vi.fn().mockResolvedValue({}),
}));

const analytics = {
  generated_from: "existing-advisory-analytics-read-api",
  disclaimer: "Research analytics only. Metrics are not financial advice.",
  metrics: [
    {
      key: "clean_advisory_rate",
      label: "Clean advisory rate",
      value: 0.625,
      unit: "ratio",
      sample_count: 24,
      uncertainty: {
        method: "wilson_score_interval",
        lower: 0.42,
        upper: 0.79,
        confidence_level: 0.95,
        sample_count: 24,
      },
      interpretation: "Stored advisory analytics interpretation.",
    },
    {
      key: "withheld_rate",
      label: "Withheld rate",
      value: 0.125,
      unit: "ratio",
      sample_count: 24,
      uncertainty: {
        method: "wilson_score_interval",
        lower: 0.04,
        upper: 0.31,
        confidence_level: 0.95,
        sample_count: 24,
      },
      interpretation: "Stored withheld-state context.",
    },
  ],
  confidence_bands: [
    {
      label: "0.40-0.60 confidence band",
      lower: 0.4,
      upper: 0.6,
      sample_count: 8,
      average_calibrated_confidence: 0.5,
      calibration_status: "warning:POORLY_CALIBRATED",
      uncertainty: {
        method: "wilson_score_interval",
        lower: 0.18,
        upper: 0.72,
        confidence_level: 0.95,
        sample_count: 8,
      },
      unreliable: true,
      economic_context: "not_assessed",
    },
  ],
  notes: ["Existing analytics response note", "Filtered UI views must not claim full-scope truth"],
  limitations: ["low sample count", "research_only"],
  source_artifact_ids: ["sig-1", "sig-2"],
  included_scope: { source: "advisory_signal_history", sample_count: 24 },
} as AdvisoryAnalyticsResponse & {
  limitations: string[];
  source_artifact_ids: string[];
  included_scope: Record<string, unknown>;
};

const emptyBundle: InstitutionalIntelligenceBundle = {
  relation: [],
  context: [],
  hypothetical: [],
  risk: [],
  validation: [],
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

function renderShell() {
  render(
    <MemoryRouter initialEntries={["/intelligence"]}>
      <Routes>
        <Route element={<InstitutionalWorkspaceShell />}>
          <Route
            path="/intelligence"
            element={<InstitutionalIntelligenceWorkspace bundle={emptyBundle} analytics={analytics} />}
          />
        </Route>
      </Routes>
    </MemoryRouter>,
  );
}

describe("UI-004-P02b performance analytics research integration", () => {
  it("test_ui004_analytics_render_existing_metrics_with_uncertainty_and_sample_counts", () => {
    render(<ResearchPerformanceAnalyticsPanel analytics={analytics} />);

    const surface = screen.getByLabelText("Read-only performance analytics research surface");
    expect(surface).toHaveTextContent("fetchAdvisoryAnalytics");
    expect(surface).toHaveTextContent("Clean advisory rate");
    expect(surface).toHaveTextContent("62.5%");
    expect(surface).toHaveTextContent("42.0% to 79.0%");
    expect(surface).toHaveTextContent("24");
    expect(surface).toHaveTextContent("wilson_score_interval");
    expect(surface).toHaveTextContent("0.40-0.60 confidence band");
    expect(surface).toHaveTextContent("50.0%");
    expect(surface).toHaveTextContent("warning:POORLY_CALIBRATED");
    expect(surface).toHaveTextContent("Unreliable calibration warning preserved.");
  });

  it("test_ui004_analytics_do_not_recompute_or_cherry_pick", async () => {
    render(<ResearchPerformanceAnalyticsPanel analytics={analytics} />);

    const sourcePanel = screen.getByLabelText("Analytics scope notes limitations and sources");
    expect(sourcePanel).toHaveTextContent("existing-advisory-analytics-read-api");
    expect(sourcePanel).toHaveTextContent("source");
    expect(sourcePanel).toHaveTextContent("advisory_signal_history");
    expect(sourcePanel).toHaveTextContent("sig-1, sig-2");
    expect(sourcePanel).toHaveTextContent("Existing analytics response note");
    expect(sourcePanel).toHaveTextContent("low sample count");
    expect(sourcePanel).toHaveTextContent("research_only");

    const sourceText = await readProductionSource("pages/InstitutionalIntelligencePage.tsx");
    expect(sourceText).toContain("fetchAdvisoryAnalytics");
    expect(sourceText).not.toContain("inferSignal");
    expect(sourceText).not.toContain("runInference");
    expect(sourceText).not.toContain("authoritativeRecompute");
    expect(sourceText).not.toContain("recompute");
    expect(sourceText).not.toContain("recalculat");
    expect(sourceText).not.toContain("reduce(");
    expect(sourceText).not.toContain("aggregate");
    expect(sourceText).not.toContain("deriveConfidence");
    expect(sourceText).not.toContain("new AnalyticsEngine");
  });

  it("test_ui004_analytics_surfaces_contain_no_execution_order_or_gate_path", async () => {
    const sourceText = (await readProductionSource("pages/InstitutionalIntelligencePage.tsx")).toLowerCase();
    const forbidden = [
      "b" + "uy",
      "s" + "ell",
      "place_order",
      "exec" + "ute",
      "go-live",
      "connect-broker",
      "account_id",
      "order_ticket",
      "open_gate",
      "allow_exec" + "ution",
    ];
    for (const marker of forbidden) {
      expect(sourceText).not.toContain(marker);
    }
  });

  it("test_ui004_analytics_accessibility_and_brand_markers_hold", () => {
    renderShell();

    expect(screen.getByText(/AXIOM Institutional Workstation/i)).toBeInTheDocument();
    expect(screen.getAllByText("Gate CLOSED").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("Research-only").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByLabelText("Analytics no cherry picking posture")).toHaveTextContent("Sample counts");
    expect(screen.getByLabelText("Stored analytics metrics with uncertainty")).toBeInTheDocument();
    expect(screen.getByLabelText("Stored calibrated confidence bands")).toBeInTheDocument();
    expect(screen.getByLabelText("Read-only analytics context navigation")).toBeInTheDocument();
    expect(screen.getByText("Open performance analytics workspace")).toBeInTheDocument();
    expect(screen.getByText("Open advisory signal workspace")).toBeInTheDocument();
    expect(within(screen.getByLabelText("Read-only performance analytics research surface")).getAllByText(/sample count/i).length).toBeGreaterThan(1);
    expect(screen.getByLabelText("Read-only performance analytics research surface").querySelectorAll(".mono").length).toBeGreaterThan(4);
  }, 30000);
});
