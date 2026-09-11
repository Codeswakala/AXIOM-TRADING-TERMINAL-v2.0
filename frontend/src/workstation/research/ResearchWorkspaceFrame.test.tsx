import { render, screen, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import {
  InstitutionalIntelligenceWorkspace,
  UI004_RESEARCH_DATA_SOURCES,
} from "../../pages/InstitutionalIntelligencePage";
import type { InstitutionalIntelligenceBundle, InstitutionalReport } from "../../api/client";
import { InstitutionalWorkspaceShell } from "../components/InstitutionalWorkspaceShell";
import { generateNavigationSections } from "../navigation/navigationGenerator";
import { WORKSPACE_REGISTRY, workspaceForPath } from "../registry/workspaceRegistry";

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

function report(overrides: Partial<InstitutionalReport> = {}): InstitutionalReport {
  return {
    id: "report-ui004-p01",
    artifact_type: "signal_validation_report",
    method_version: "method.v1",
    sample_count: 12,
    research_status: "research_only",
    report_hash: "hash-ui004-p01",
    limitations: ["research_only", "low_sample_count"],
    uncertainty: {
      method: "wilson_score_intervals",
      lower: 0.1,
      upper: 0.4,
      confidence_level: 0.95,
      sample_count: 12,
    },
    economic_usefulness: { verdict: "not_assessed" },
    results: { persisted_value: 0.25 },
    input_lineage: { source: "persisted_report" },
    ...overrides,
  };
}

const bundle: InstitutionalIntelligenceBundle = {
  relation: [report({ artifact_type: "correlation_report" })],
  context: [report({ artifact_type: "regime_report" })],
  hypothetical: [report({ artifact_type: "scenario_report" })],
  risk: [report({ artifact_type: "portfolio_risk_report" })],
  validation: [report({ artifact_type: "signal_validation_report" })],
};

function renderShell() {
  render(
    <MemoryRouter initialEntries={["/intelligence"]}>
      <Routes>
        <Route element={<InstitutionalWorkspaceShell />}>
          <Route path="/intelligence" element={<InstitutionalIntelligenceWorkspace bundle={bundle} />} />
        </Route>
      </Routes>
    </MemoryRouter>,
  );
}

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

describe("UI-004-P01 research workspace frame", () => {
  it("test_ui004_research_workspace_mounts_inside_single_ui001_shell", () => {
    renderShell();

    expect(screen.getAllByTestId("institutional-workspace-shell")).toHaveLength(1);
    expect(screen.getAllByLabelText("Global command bar")).toHaveLength(1);
    expect(screen.getAllByLabelText("Institutional workflow navigation")).toHaveLength(1);
    expect(screen.getByLabelText("Research and intelligence workspace frame")).toBeInTheDocument();
    expect(screen.getByText("Research & Intelligence Workspace")).toBeInTheDocument();
    expect(screen.getByLabelText("UI-004 governed data-source inventory")).toBeInTheDocument();
    expect(screen.getByLabelText("Primary workspace")).toHaveAttribute(
      "data-active-telemetry-id",
      "workspace.research.intelligence",
    );
  });

  it("test_ui004_research_workspace_registers_through_ui002_navigation_only", () => {
    const workspace = workspaceForPath("/intelligence");
    const registeredRoutes = new Set(WORKSPACE_REGISTRY.map((item) => item.route));
    const visibleNavigationIds = generateNavigationSections({
      workspaces: WORKSPACE_REGISTRY,
      operator: { role: "admin" },
    }).flatMap((section) => section.workspaces.map((item) => item.id));

    expect(workspace.id).toBe("research.intelligence");
    expect(workspace.route).toBe("/intelligence");
    expect(workspace.requiresAuth).toBe(true);
    expect(workspace.noActuation).toBe(true);
    expect(visibleNavigationIds).toContain("research.intelligence");
    expect(registeredRoutes.has("/research-intelligence")).toBe(false);
    expect(registeredRoutes.has("/intelligence")).toBe(true);
  });

  it("test_ui004_research_workspace_maps_every_surface_to_existing_sources", () => {
    render(<InstitutionalIntelligenceWorkspace bundle={bundle} />);

    const inventory = screen.getByLabelText("UI-004 governed data-source inventory");
    const expectedSources = [
      "fetchInstitutionalIntelligenceBundle",
      "fetchAdvisorySignals",
      "fetchAdvisoryAnalytics",
      "fetchInstitutionalIntelligenceBundle.validation",
      "fetchResearchManagementBundle",
      "existing intelligence and portfolio report read APIs",
    ];
    for (const source of expectedSources) {
      expect(within(inventory).getByText(source)).toBeInTheDocument();
    }
    expect(UI004_RESEARCH_DATA_SOURCES.map((item) => item.surface)).toEqual([
      "Institutional Intelligence",
      "Advisory Signals",
      "Performance Analytics",
      "Validation",
      "Economic Usefulness",
      "Research Artifacts",
      "Report Viewers",
    ]);
    expect(screen.getByLabelText("Research workspace overview cards")).toHaveTextContent("registered");
    expect(screen.getByLabelText("Research workspace overview cards")).toHaveTextContent("fetchAdvisorySignals");
  });

  it("test_ui004_research_workspace_contains_no_recompute_inference_or_signal_generation", async () => {
    const sourceText = await readProductionSource("pages/InstitutionalIntelligencePage.tsx");
    const forbidden = [
      "inferSignal",
      "runInference",
      "authoritativeRecompute",
      "emitSignal",
      "generateSignal",
      "recompute",
      "recalculat",
      "deriveConfidence",
      "/api/v1/orders",
      "new AnalyticsEngine",
      "new IntelligenceEngine",
    ];
    for (const marker of forbidden) {
      expect(sourceText).not.toContain(marker);
    }
    expect(sourceText).toContain("UI004_RESEARCH_DATA_SOURCES");
    expect(sourceText).toContain("Stored-value guardrail");
  });

  it("test_ui004_research_workspace_preserves_gate_closed_research_only_branding", () => {
    renderShell();

    expect(screen.getByText(/AXIOM Institutional Workstation/i)).toBeInTheDocument();
    expect(screen.getAllByText("Gate CLOSED").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("Research-only").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByLabelText("Stored-value guardrail")).toHaveTextContent("Gate CLOSED");
    expect(screen.getByLabelText("Stored-value guardrail")).toHaveTextContent("Research-only");
    expect(screen.getByLabelText("UI-004 governed data-source inventory").querySelectorAll(".mono").length).toBeGreaterThan(5);

    const pageText = screen.getByLabelText("Research and intelligence workspace frame").textContent?.toLowerCase() ?? "";
    const forbiddenRetailOrAction = ["b" + "uy", "s" + "ell", "place_order", "connect-broker", "open_gate"];
    for (const marker of forbiddenRetailOrAction) {
      expect(pageText).not.toContain(marker);
    }
  });
});
