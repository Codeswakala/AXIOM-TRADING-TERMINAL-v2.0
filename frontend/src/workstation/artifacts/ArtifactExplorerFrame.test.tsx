import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import {
  ResearchManagementWorkspace,
  UI006_ARTIFACT_EXPLORER_SOURCES,
} from "../../components/terminal/research/ResearchHubView";
import type {
  ResearchCollection,
  ResearchCollectionMember,
  ResearchTag,
  ScenarioReport,
} from "../../api/client";
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

function collection(overrides: Partial<ResearchCollection> = {}): ResearchCollection {
  return {
    collection_id: "collection-ui006-p01-1",
    created_at: "2026-07-26T08:00:00Z",
    updated_at: "2026-07-26T08:00:00Z",
    operator_id: "operator-1",
    name: "Read-only Artifact Review",
    description: "Existing organization record.",
    research_status: "research_only",
    audit_correlation_id: "corr-collection-ui006-p01-1",
    ...overrides,
  };
}

function member(overrides: Partial<ResearchCollectionMember> = {}): ResearchCollectionMember {
  return {
    member_id: "member-ui006-p01-1",
    created_at: "2026-07-26T08:00:00Z",
    operator_id: "operator-1",
    collection_id: "collection-ui006-p01-1",
    artifact_type: "scenario_report",
    artifact_id: "scenario-ui006-p01-1",
    audit_correlation_id: "corr-member-ui006-p01-1",
    ...overrides,
  };
}

function tag(overrides: Partial<ResearchTag> = {}): ResearchTag {
  return {
    tag_id: "tag-ui006-p01-1",
    created_at: "2026-07-26T08:00:00Z",
    operator_id: "operator-1",
    artifact_type: "scenario_report",
    artifact_id: "scenario-ui006-p01-1",
    tag: "read-only-review",
    audit_correlation_id: "corr-tag-ui006-p01-1",
    ...overrides,
  };
}

function scenario(overrides: Partial<ScenarioReport> = {}): ScenarioReport {
  return {
    id: "scenario-ui006-p01-1",
    created_at: "2026-07-26T08:00:00Z",
    artifact_type: "scenario_report",
    method_version: "scenario.method.v1",
    market_class: "forex",
    symbol: "EURUSD",
    timeframe: "M1",
    as_of_start: "2026-07-26T07:00:00Z",
    as_of_end: "2026-07-26T08:00:00Z",
    sample_count: 6,
    scenario_name: "Read-only hypothetical scenario",
    hypothetical_return: 0.01,
    scenario_result: { hypothetical_return: 0.01 },
    assumptions: { scenario_name: "Read-only hypothetical scenario" },
    inputs: { baseline_returns: [0.01] },
    uncertainty: { method: "historical_band", sample_count: 6 },
    economic_usefulness: { verdict: "not_assessed" },
    config: { fixture: true },
    input_lineage: { policy: "as_of_bounded" },
    source_artifact_ids: ["source-ui006-p01-1"],
    market_scope: { market_class: "forex" },
    results: { stored: true },
    limitations: ["research_only"],
    report_hash: "hash-ui006-p01-1",
    research_status: "research_only",
    created_by: "test",
    audit_correlation_id: "corr-scenario-ui006-p01-1",
    notes: "read only source artifact",
    ...overrides,
  };
}

function workspace() {
  return (
    <ResearchManagementWorkspace
      collections={[collection()]}
      members={[member()]}
      tags={[tag()]}
      artifacts={[scenario()]}
    />
  );
}

function renderExplorerShell() {
  render(
    <MemoryRouter initialEntries={["/research-management"]}>
      <Routes>
        <Route element={<InstitutionalWorkspaceShell />}>
          <Route path="/research-management" element={workspace()} />
        </Route>
      </Routes>
    </MemoryRouter>,
  );
}

async function readProductionSource(): Promise<string> {
  // UI-CONV-P03 item 4 re-target: the UI-006 explorer source relocated from
  // pages/ResearchManagementPage.tsx to the research stage view module.
  const modules = import.meta.glob("../../components/terminal/research/*.{ts,tsx}", {
    query: "?raw",
    import: "default",
  });
  const entry = Object.entries(modules).find(([path]) => path.endsWith("ResearchHubView.tsx"));
  if (!entry) throw new Error("ResearchHubView source not found");
  return (entry[1] as () => Promise<string>)();
}

describe("UI-006-P01 Unified Research Artifact Explorer frame", () => {
  it("test_ui006_explorer_mounts_inside_single_ui001_shell", () => {
    renderExplorerShell();

    expect(screen.getAllByTestId("institutional-workspace-shell")).toHaveLength(1);
    expect(screen.getByLabelText("Primary workspace")).toHaveAttribute(
      "data-active-telemetry-id",
      "workspace.review.research_management",
    );
    expect(screen.getAllByText("Unified Research Artifact Explorer").length).toBeGreaterThan(0);
    expect(screen.getByLabelText("Unified artifact explorer frame")).toBeInTheDocument();
  });

  it("test_ui006_explorer_uses_existing_route_and_registry_only", () => {
    const routes = new Set(WORKSPACE_REGISTRY.map((item) => item.route));
    const workspace = workspaceForPath("/research-management");

    expect(workspace.id).toBe("review.research_management");
    expect(workspace.requiresAuth).toBe(true);
    expect(workspace.noActuation).toBe(true);
    expect(routes.has("/research-management")).toBe(true);
    expect(routes.has("/artifacts")).toBe(false);
    expect(routes.has("/artifact-explorer")).toBe(false);
    expect(new Set(WORKSPACE_REGISTRY.map((item) => item.id)).size).toBe(WORKSPACE_REGISTRY.length);
  });

  it("test_ui006_explorer_maps_every_artifact_family_to_existing_sources", () => {
    render(workspace());

    const inventory = screen.getByLabelText("UI-006 governed data-source inventory");
    for (const family of [
      "Advisory signals",
      "Intelligence reports",
      "Scenario reports",
      "Portfolio research",
      "Chart annotations",
      "Trade plans",
      "Research journal",
      "Execution research",
      "Collections",
      "Collection memberships",
      "Tags",
    ]) {
      expect(inventory).toHaveTextContent(family);
    }
    for (const seam of [
      "fetchAdvisorySignals / fetchAdvisorySignal",
      "fetchInstitutionalIntelligenceBundle",
      "fetchScenarioReports / fetchScenarioReport",
      "fetchPortfolioResearchDashboard / fetchAdvancedResearchReport",
      "fetchChartResearchAnnotations",
      "fetchTradePlans",
      "fetchJournalEntries",
      "fetchExecutionResearchBundle",
      "fetchResearchManagementBundle / fetchResearchCollections",
      "fetchResearchManagementBundle / fetchResearchTags",
    ]) {
      expect(inventory).toHaveTextContent(seam);
    }
    expect(UI006_ARTIFACT_EXPLORER_SOURCES).toHaveLength(11);
  });

  it("test_ui006_explorer_contains_no_mutation_actuation_or_gate_path", async () => {
    render(workspace());

    const buttonText = screen
      .getAllByRole("button")
      .map((button) => button.textContent?.toLowerCase() ?? "")
      .join(" ");
    for (const marker of ["create", "add member", "delete", "remove", "update", "submit"]) {
      expect(buttonText).not.toContain(marker);
    }
    expect(screen.queryByLabelText("Research collection editor")).not.toBeInTheDocument();
    expect(screen.getByLabelText("Artifact explorer completion guardrails")).toHaveTextContent("Organization-only");

    const sourceText = (await readProductionSource()).toLowerCase();
    for (const marker of [
      "place_order",
      "exec" + "ute",
      "go-live",
      "connect-" + "broker",
      "br" + "oker",
      "account_id",
      "order_" + "ticket",
      "pos" + "ition",
      "balance",
      "margin",
      "capital",
      "allocation",
      "real_pnl",
      "open_gate",
      "allow_exec" + "ution",
      "infersignal",
      "runinference",
      "authoritativerecompute",
      "emitsignal",
      "generatesignal",
      "generatescenario",
      "recompute",
      "recalculat",
      "deriveconfidence",
      "reclassif",
      "openai",
      "external_llm",
      "/api/v1/orders",
    ]) {
      expect(sourceText).not.toContain(marker);
    }
  });

  it("test_ui006_explorer_preserves_research_only_verbatim_and_doc16_branding", () => {
    renderExplorerShell();

    expect(screen.getByText(/AXIOM Institutional Workstation/i)).toBeInTheDocument();
    expect(screen.getAllByText("Gate CLOSED").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("Research-only").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByLabelText("Artifact explorer guardrail")).toHaveTextContent("Gate CLOSED");
    expect(screen.getAllByText("research_only").length).toBeGreaterThan(0);
    expect(screen.getByText("hash-ui006-p01-1")).toBeInTheDocument();
    expect(screen.getByLabelText("UI-006 governed data-source inventory").querySelectorAll(".mono").length).toBeGreaterThan(5);
  });
});
