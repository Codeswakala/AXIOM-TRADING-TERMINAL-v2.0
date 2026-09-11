import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import {
  SignalInvestigationFrame,
  UI005_INVESTIGATION_PLANNING_SOURCES,
} from "../../components/terminal/signals/SignalInvestigationRecords";

import { InstitutionalWorkspaceShell } from "../components/InstitutionalWorkspaceShell";
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

function renderInvestigationShell() {
  render(
    <MemoryRouter initialEntries={["/investigate"]}>
      <Routes>
        <Route element={<InstitutionalWorkspaceShell />}>
          <Route
            path="/investigate"
            element={<SignalInvestigationFrame />}
          />
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

describe("UI-005-P01 investigation and planning workspace frame", () => {
  it("test_ui005_workspace_mounts_inside_single_ui001_shell", () => {
    renderInvestigationShell();

    expect(screen.getAllByTestId("institutional-workspace-shell")).toHaveLength(1);
    expect(screen.getByLabelText("Primary workspace")).toHaveAttribute(
      "data-active-telemetry-id",
      "workspace.investigate.signal_investigation",
    );
    expect(screen.getByLabelText("Investigation and planning workspace frame")).toBeInTheDocument();
    expect(screen.getByText("Investigation & Planning Workspace")).toBeInTheDocument();
  });

  it("test_ui005_workspace_uses_existing_routes_and_registry_only", () => {
    const routes = new Set(WORKSPACE_REGISTRY.map((workspace) => workspace.route));
    expect(workspaceForPath("/investigate").id).toBe("investigate.signal_investigation");
    expect(routes.has("/investigate")).toBe(true);
    expect(routes.has("/compare-scenarios")).toBe(true);
    expect(routes.has("/trade-plans")).toBe(true);
    expect(routes.has("/execution-research")).toBe(true);
    expect(routes.has("/journal")).toBe(true);
    expect(routes.has("/portfolio-research")).toBe(true);
    expect(routes.has("/investigation-planning")).toBe(false);
    expect(WORKSPACE_REGISTRY.every((workspace) => workspace.requiresAuth && workspace.noActuation)).toBe(true);
  });

  it("test_ui005_workspace_maps_every_surface_to_existing_sources", () => {
    renderInvestigationShell();
    const inventory = screen.getByLabelText("UI-005 governed data-source inventory");
    const surfaces = [
      "Signal Investigation",
      "Scenario Comparison",
      "Trade Planning",
      "Execution Research",
      "Research Journal",
      "Portfolio Research",
    ];
    for (const surface of surfaces) {
      expect(inventory).toHaveTextContent(surface);
    }
    expect(inventory).toHaveTextContent("fetchAdvisorySignals + fetchInstitutionalIntelligenceBundle");
    expect(inventory).toHaveTextContent("fetchScenarioReports / fetchScenarioReport");
    expect(inventory).toHaveTextContent("existing trade plan read path");
    // SURF-P01 re-target: the execution research read-seam declaration now
    // names the surfaced list/detail seams.
    expect(inventory).toHaveTextContent("fetchSimulatedRunsList");
    expect(inventory).toHaveTextContent("fetchJournalEntries");
    expect(inventory).toHaveTextContent("fetchPortfolioResearchDashboard + fetchAdvancedResearchReport");
    expect(inventory).toHaveTextContent("SIMULATED display-only evidence");
    expect(UI005_INVESTIGATION_PLANNING_SOURCES).toHaveLength(6);
  });

  it("test_ui005_workspace_contains_no_actuation_or_gate_path", async () => {
    const sourceText = (await readProductionSource("components/terminal/signals/SignalInvestigationRecords.tsx")).toLowerCase();
    const forbidden = [
      "b" + "uy",
      "s" + "ell",
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
    ];
    for (const marker of forbidden) {
      expect(sourceText).not.toContain(marker);
    }

    const noRecomputeForbidden = [
      "inferSignal",
      "runInference",
      "authoritativeRecompute",
      "emitSignal",
      "generateSignal",
      "recompute",
      "recalculat",
      "deriveConfidence",
      "reclassif",
      "new AnalyticsEngine",
      "new IntelligenceEngine",
      "/api/v1/orders",
      "openai",
      "gpt",
      "external_llm",
      "llm_summary",
      "ai_summary",
    ];
    for (const marker of noRecomputeForbidden) {
      expect(sourceText).not.toContain(marker.toLowerCase());
    }
  });

  it("test_ui005_workspace_preserves_research_only_and_doc16_branding", () => {
    renderInvestigationShell();

    expect(screen.getByText(/AXIOM Institutional Workstation/i)).toBeInTheDocument();
    expect(screen.getAllByText("Gate CLOSED").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("Research-only").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByLabelText("Investigation planning guardrail")).toHaveTextContent("Gate CLOSED");
    expect(screen.getByLabelText("Investigation planning guardrail")).toHaveTextContent("SIMULATED evidence only");
    expect(screen.getByLabelText("UI-005 governed data-source inventory").querySelectorAll(".mono").length).toBeGreaterThan(5);
  });
});
