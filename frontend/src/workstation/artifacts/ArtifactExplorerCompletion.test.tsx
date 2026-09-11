import { fireEvent, render, screen, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { ProtectedRoute } from "../../auth/ProtectedRoute";
import {
  ResearchManagementWorkspace,
  UI006_ARTIFACT_EXPLORER_SOURCES,
} from "../../components/terminal/research/ResearchHubView";
import type {
  ResearchArtifactReferenceWrite,
  ResearchCollection,
  ResearchCollectionMember,
  ResearchCollectionWrite,
  ResearchTag,
  ResearchTagWrite,
  ScenarioReport,
} from "../../api/client";
import { InstitutionalWorkspaceShell } from "../components/InstitutionalWorkspaceShell";
import { WORKSPACE_REGISTRY, workspaceForPath } from "../registry/workspaceRegistry";

const authenticatedAuth = () => ({
  operator: { username: "operator", role: "admin" },
  loading: false,
  isAuthenticated: true,
  logout: vi.fn(),
  login: vi.fn(),
  refreshProfile: vi.fn(),
});

const loggedOutAuth = () => ({
  operator: null,
  loading: false,
  isAuthenticated: false,
  logout: vi.fn(),
  login: vi.fn(),
  refreshProfile: vi.fn(),
});

const authState = vi.hoisted(() => ({
  value: {
    operator: { username: "operator", role: "admin" },
    loading: false,
    isAuthenticated: true,
    logout: vi.fn(),
    login: vi.fn(),
    refreshProfile: vi.fn(),
  } as ReturnType<typeof authenticatedAuth> | ReturnType<typeof loggedOutAuth>,
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
    collection_id: "collection-ui006-p06-1",
    created_at: "2026-07-26T08:00:00Z",
    updated_at: "2026-07-26T08:00:00Z",
    operator_id: "operator-1",
    name: "P06 Completion Review",
    description: "Existing W7 organization record.",
    research_status: "research_only",
    audit_correlation_id: "corr-collection-ui006-p06-1",
    ...overrides,
  };
}

function member(overrides: Partial<ResearchCollectionMember> = {}): ResearchCollectionMember {
  return {
    member_id: "member-ui006-p06-1",
    created_at: "2026-07-26T08:00:00Z",
    operator_id: "operator-1",
    collection_id: "collection-ui006-p06-1",
    artifact_type: "scenario_report",
    artifact_id: "scenario-ui006-p06-1",
    audit_correlation_id: "corr-member-ui006-p06-1",
    ...overrides,
  };
}

function tag(overrides: Partial<ResearchTag> = {}): ResearchTag {
  return {
    tag_id: "tag-ui006-p06-1",
    created_at: "2026-07-26T08:00:00Z",
    operator_id: "operator-1",
    artifact_type: "scenario_report",
    artifact_id: "scenario-ui006-p06-1",
    tag: "completion-review",
    audit_correlation_id: "corr-tag-ui006-p06-1",
    ...overrides,
  };
}

function scenario(overrides: Partial<ScenarioReport> = {}): ScenarioReport {
  return {
    id: "scenario-ui006-p06-1",
    created_at: "2026-07-26T08:00:00Z",
    artifact_type: "scenario_report",
    method_version: "scenario.method.v1",
    market_class: "forex",
    symbol: "EURUSD",
    timeframe: "M1",
    as_of_start: "2026-07-26T07:00:00Z",
    as_of_end: "2026-07-26T08:00:00Z",
    sample_count: 6,
    scenario_name: "P06 completion scenario artifact",
    hypothetical_return: 0.01,
    scenario_result: { hypothetical_return: 0.01, counterfactual_index: 1.01 },
    assumptions: { horizon_bars: 4 },
    inputs: { baseline_returns: [0.01] },
    uncertainty: { method: "historical_band", lower: 0, upper: 0.02, sample_count: 6 },
    economic_usefulness: { verdict: "not_assessed" },
    config: { fixture: true },
    input_lineage: { input_policy: "as_of_bounded_hypothetical_research" },
    source_artifact_ids: ["source-ui006-p06-1"],
    market_scope: { symbol: "EURUSD", timeframe: "M1", sample_count: 6 },
    results: { stored: true },
    limitations: ["hypothetical_counterfactual_research_only", "not_a_prediction"],
    report_hash: "scenario-hash-ui006-p06-1",
    research_status: "research_only",
    created_by: "test",
    audit_correlation_id: "corr-scenario-ui006-p06-1",
    notes: "read only source artifact",
    ...overrides,
  };
}

function workspace(
  handlers: Partial<{
    onCreateCollection: (payload: ResearchCollectionWrite) => void;
    onAddMember: (collectionId: string, payload: ResearchArtifactReferenceWrite) => void;
    onRemoveMember: (collectionId: string, memberId: string) => void;
    onCreateTag: (payload: ResearchTagWrite) => void;
  }> = {},
) {
  return (
    <ResearchManagementWorkspace
      collections={[collection()]}
      members={[member()]}
      tags={[tag()]}
      artifacts={[scenario()]}
      {...handlers}
    />
  );
}

function renderExplorerShell(
  handlers: Partial<{
    onCreateCollection: (payload: ResearchCollectionWrite) => void;
    onAddMember: (collectionId: string, payload: ResearchArtifactReferenceWrite) => void;
    onRemoveMember: (collectionId: string, memberId: string) => void;
    onCreateTag: (payload: ResearchTagWrite) => void;
  }> = {},
) {
  return render(
    <MemoryRouter initialEntries={["/research-management"]}>
      <Routes>
        <Route element={<InstitutionalWorkspaceShell />}>
          <Route path="/research-management" element={workspace(handlers)} />
        </Route>
      </Routes>
    </MemoryRouter>,
  );
}

async function readCompletionSurfaceSource(): Promise<string> {
  const modules = import.meta.glob(
    [
      // UI-CONV-P03 item 4 re-target: the UI-006 explorer source relocated from
      // pages/ResearchManagementPage.tsx to the research stage view module.
      "../../components/terminal/research/ResearchHubView.tsx",
      "../../api/client.ts",
      "../registry/workspaceRegistry.tsx",
      "../components/InstitutionalWorkspaceShell.tsx",
    ],
    {
      query: "?raw",
      import: "default",
    },
  );
  const values = await Promise.all(
    Object.values(modules).map((loader) => (loader as () => Promise<string>)()),
  );
  return values.join("\n").toLowerCase();
}

beforeEach(() => {
  authState.value = authenticatedAuth();
});

describe("UI-006-P06 completion checkpoint", () => {
  it("test_ui006_completion_artifact_explorer_discovery_organization_and_traceability_hold", () => {
    render(
      workspace({
        onCreateCollection: vi.fn(),
        onAddMember: vi.fn(),
        onRemoveMember: vi.fn(),
        onCreateTag: vi.fn(),
      }),
    );

    expect(screen.getAllByText("Unified Research Artifact Explorer").length).toBeGreaterThan(0);
    expect(screen.getByLabelText("UI-006 governed data-source inventory")).toHaveTextContent(
      "Current posture",
    );
    expect(UI006_ARTIFACT_EXPLORER_SOURCES).toHaveLength(11);
    for (const family of ["Scenario reports", "Collections", "Collection memberships", "Tags"]) {
      expect(screen.getByLabelText("UI-006 governed data-source inventory")).toHaveTextContent(family);
    }

    const catalog = screen.getByLabelText("Read-only unified artifact catalog");
    expect(catalog).toHaveTextContent("P06 completion scenario artifact");
    expect(catalog).toHaveTextContent("P06 Completion Review");
    expect(catalog).toHaveTextContent("completion-review");

    const detail = screen.getByLabelText("Read-only artifact metadata detail");
    expect(detail).toHaveTextContent("scenario-ui006-p06-1");
    expect(detail).toHaveTextContent("scenario-hash-ui006-p06-1");
    expect(detail).toHaveTextContent("collection:collection-ui006-p06-1");
    expect(detail).toHaveTextContent("tag:completion-review");
    expect(screen.getByLabelText("Collection membership organization controls")).toBeInTheDocument();
    expect(screen.getByLabelText("Tag organization controls")).toBeInTheDocument();
  });

  it("test_ui006_completion_mutations_are_organization_only_and_existing_store_bound", () => {
    const onCreateCollection = vi.fn();
    const onAddMember = vi.fn();
    const onRemoveMember = vi.fn();
    const onCreateTag = vi.fn();
    render(workspace({ onCreateCollection, onAddMember, onRemoveMember, onCreateTag }));

    const before = screen.getByLabelText("Read-only artifact metadata detail");
    expect(before).toHaveTextContent("scenario-ui006-p06-1");
    expect(before).toHaveTextContent("scenario-hash-ui006-p06-1");
    expect(before).toHaveTextContent("not_assessed");
    expect(before).toHaveTextContent("historical_band");

    fireEvent.click(screen.getByText("Save collection record"));
    expect(onCreateCollection).toHaveBeenCalledWith({
      name: "Artifact review set",
      description: "Reference-only grouping of governed research artifacts.",
    });

    fireEvent.click(screen.getByText("Add reference"));
    expect(onAddMember).toHaveBeenCalledWith("collection-ui006-p06-1", {
      artifact_type: "scenario_report",
      artifact_id: "scenario-ui006-p06-1",
    });

    fireEvent.click(screen.getByText("Remove reference"));
    expect(onRemoveMember).toHaveBeenCalledWith("collection-ui006-p06-1", "member-ui006-p06-1");

    fireEvent.click(screen.getByText("Save tag record"));
    const tagPayload = onCreateTag.mock.calls[0][0] as ResearchTagWrite;
    expect(Object.keys(tagPayload).sort()).toEqual(["artifact_id", "artifact_type", "tag"]);
    expect(tagPayload).toEqual({
      artifact_type: "scenario_report",
      artifact_id: "scenario-ui006-p06-1",
      tag: "artifact-review",
    });

    expect(screen.getByLabelText("Collection membership organization controls")).toHaveTextContent(
      "existing W7 research-management stores",
    );
    expect(screen.getByLabelText("Tag organization controls")).toHaveTextContent(
      "existing W7 research tag store",
    );
    const after = screen.getByLabelText("Read-only artifact metadata detail");
    expect(after).toHaveTextContent("scenario-ui006-p06-1");
    expect(after).toHaveTextContent("scenario-hash-ui006-p06-1");
    expect(after).toHaveTextContent("not_assessed");
    expect(after).toHaveTextContent("historical_band");
  });

  it("test_ui006_completion_no_actuation_recompute_external_ai_schema_or_route_drift", async () => {
    const workspaceDefinition = workspaceForPath("/research-management");
    const routes = new Set(WORKSPACE_REGISTRY.map((item) => item.route));
    expect(workspaceDefinition.id).toBe("review.research_management");
    expect(workspaceDefinition.noActuation).toBe(true);
    expect(routes.has("/research-management")).toBe(true);
    expect(routes.has("/artifacts")).toBe(false);
    expect(routes.has("/artifact-explorer")).toBe(false);

    const sourceText = await readCompletionSurfaceSource();
    for (const marker of [
      "place_" + "order",
      "exec" + "ute",
      "go-live",
      "connect-" + "broker",
      "br" + "oker",
      "account_" + "id",
      "order_" + "ticket",
      "pos" + "ition",
      "bal" + "ance",
      "mar" + "gin",
      "cap" + "ital",
      "alloc" + "ation",
      "real_" + "pnl",
      "open_" + "gate",
      "allow_exec" + "ution",
      "infersignal",
      "runinference",
      "authoritative" + "recompute",
      "emitsignal",
      "generatesignal",
      "generatescenario",
      "inferrelationship",
      "rec" + "ompute",
      "recalculat",
      "deriveconfidence",
      "reclassif",
      "open" + "ai",
      "external_" + "llm",
      "llm_" + "summary",
      "ai_" + "summary",
      "/api/v1/" + "orders",
      "/api/v1/artifacts",
      "/api/v1/artifact-explorer",
      "artifact-explorer-workspace-v1",
      "unified-artifact-explorer-workspace-v1",
    ]) {
      expect(sourceText).not.toContain(marker);
    }
  });

  it("test_ui006_completion_verbatim_no_cherry_picking_and_relationship_boundaries_hold", () => {
    render(workspace());

    const detail = screen.getByLabelText("Read-only artifact metadata detail");
    expect(within(detail).getByText("scenario-ui006-p06-1")).toBeInTheDocument();
    expect(within(detail).getByText("scenario-hash-ui006-p06-1")).toBeInTheDocument();
    expect(within(detail).getByText("6")).toBeInTheDocument();
    expect(within(detail).getByText("not_assessed")).toBeInTheDocument();
    expect(within(detail).getByText(/historical_band/)).toBeInTheDocument();
    expect(within(detail).getByText("source-ui006-p06-1")).toBeInTheDocument();
    expect(within(detail).getByText("hypothetical_counterfactual_research_only")).toBeInTheDocument();
    expect(within(detail).getByText("not_a_prediction")).toBeInTheDocument();

    const filterPanel = screen.getByLabelText("In-memory artifact filters");
    const familySelect = within(filterPanel).getAllByRole("combobox")[0];
    fireEvent.change(familySelect, { target: { value: "Tags" } });
    expect(screen.getByLabelText("Filtered view scope notice")).toHaveTextContent("Showing 1 of 4");
    expect(screen.getByLabelText("Filtered view scope notice")).toHaveTextContent("No cherry-picking");
    expect(filterPanel).toHaveTextContent("presentation subset");
    expect(filterPanel).toHaveTextContent("never a full-scope analytical claim");
  });

  it("test_ui006_completion_accessibility_doc16_brand_and_ui001_ui002_integration_hold", () => {
    const { unmount } = renderExplorerShell({
      onCreateCollection: vi.fn(),
      onAddMember: vi.fn(),
      onRemoveMember: vi.fn(),
      onCreateTag: vi.fn(),
    });

    expect(screen.getAllByTestId("institutional-workspace-shell")).toHaveLength(1);
    expect(screen.getByLabelText("Primary workspace")).toHaveAttribute(
      "data-active-telemetry-id",
      "workspace.review.research_management",
    );
    expect(screen.getByText(/AXIOM Institutional Workstation/i)).toBeInTheDocument();
    // SUPERSEDED BY CITATION (BO-FE-U02 §2.2/§2.9, PC-FEU02-1 C4/C9, ACC-1; adopted 2026-09-11): the asserted heritage chips are EXPELLED from the chrome boundary; the truthful cluster renders the locked-config mode badge + live health chip instead.
    // (pin scoped to the CHROME's status cluster — the GovernanceOverlay's 'Gate CLOSED' record entries are OUT-OF-BOUNDARY heritage, protected per PC-FEU02-1 C9 heritage clause, not chrome chips)
    const chromeCluster = screen.getByTestId("shell-governance-status");
    expect(chromeCluster.textContent).not.toContain("Gate CLOSED");
    expect(screen.getByTestId("chrome-mode-badge")).toHaveTextContent(/RESEARCH · NON-ACTUATING/);
    expect(screen.getAllByText("Research-only").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByLabelText("Unified artifact explorer frame")).toBeInTheDocument();
    expect(screen.getByLabelText("Artifact explorer completion guardrails")).toHaveTextContent(
      "Organization-only",
    );
    expect(screen.getByLabelText("Collection membership organization controls")).toBeInTheDocument();
    expect(screen.getByLabelText("Tag organization controls")).toBeInTheDocument();
    expect(document.body.querySelectorAll(".mono").length).toBeGreaterThan(10);

    unmount();
    authState.value = loggedOutAuth();
    render(
      <MemoryRouter initialEntries={["/research-management"]}>
        <Routes>
          <Route path="/login" element={<div>Operator login required</div>} />
          <Route
            path="/research-management"
            element={
              <ProtectedRoute>
                <ResearchManagementWorkspace
                  collections={[collection()]}
                  members={[member()]}
                  tags={[tag()]}
                  artifacts={[scenario()]}
                />
              </ProtectedRoute>
            }
          />
        </Routes>
      </MemoryRouter>,
    );

    expect(screen.getByText("Operator login required")).toBeInTheDocument();
    expect(screen.queryByText("P06 completion scenario artifact")).not.toBeInTheDocument();
  });
});
