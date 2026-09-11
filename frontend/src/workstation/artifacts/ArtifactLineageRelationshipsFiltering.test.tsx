import { fireEvent, render, screen, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { ResearchManagementWorkspace } from "../../components/terminal/research/ResearchHubView";
import type {
  AdvisorySignal,
  ResearchCollection,
  ResearchCollectionMember,
  ResearchTag,
  ScenarioReport,
} from "../../api/client";
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

const collection: ResearchCollection = {
  collection_id: "collection-ui006-p03-1",
  created_at: "2026-07-26T08:00:00Z",
  updated_at: "2026-07-26T08:00:00Z",
  operator_id: "operator-1",
  name: "P03 Relationship Review",
  description: "Existing collection metadata.",
  research_status: "research_only",
  audit_correlation_id: "corr-collection-ui006-p03-1",
};

const member: ResearchCollectionMember = {
  member_id: "member-ui006-p03-1",
  created_at: "2026-07-26T08:00:00Z",
  operator_id: "operator-1",
  collection_id: "collection-ui006-p03-1",
  artifact_type: "scenario_report",
  artifact_id: "scenario-ui006-p03-1",
  audit_correlation_id: "corr-member-ui006-p03-1",
};

const tag: ResearchTag = {
  tag_id: "tag-ui006-p03-1",
  created_at: "2026-07-26T08:00:00Z",
  operator_id: "operator-1",
  artifact_type: "scenario_report",
  artifact_id: "scenario-ui006-p03-1",
  tag: "relationship-review",
  audit_correlation_id: "corr-tag-ui006-p03-1",
};

const scenario: ScenarioReport = {
  id: "scenario-ui006-p03-1",
  created_at: "2026-07-26T08:00:00Z",
  artifact_type: "scenario_report",
  method_version: "scenario.method.v1",
  market_class: "forex",
  symbol: "EURUSD",
  timeframe: "M1",
  as_of_start: "2026-07-26T07:00:00Z",
  as_of_end: "2026-07-26T08:00:00Z",
  sample_count: 6,
  scenario_name: "P03 relationship scenario",
  hypothetical_return: 0.01,
  scenario_result: { hypothetical_return: 0.01, counterfactual_index: 1.01 },
  assumptions: { horizon_bars: 4 },
  inputs: { baseline_returns: [0.01] },
  uncertainty: { method: "historical_band", lower: 0, upper: 0.02, sample_count: 6 },
  economic_usefulness: { verdict: "not_assessed" },
  config: { fixture: true },
  input_lineage: { input_policy: "as_of_bounded_hypothetical_research" },
  source_artifact_ids: ["source-ui006-p03-1"],
  market_scope: { symbol: "EURUSD", timeframe: "M1", sample_count: 6 },
  results: { stored: true },
  limitations: ["hypothetical_counterfactual_research_only", "not_a_prediction"],
  report_hash: "scenario-hash-ui006-p03-1",
  research_status: "research_only",
  created_by: "test",
  audit_correlation_id: "corr-scenario-ui006-p03-1",
  notes: "read only source artifact",
};

const signal: AdvisorySignal = {
  signal_id: "signal-ui006-p03-1",
  created_at: "2026-07-26T08:00:00Z",
  as_of_time: "2026-07-26T07:59:00Z",
  market_class: "forex",
  provider: "internal",
  symbol: "EURUSD",
  timeframe: "M1",
  model_artifact_id: "model-ui006-p03-1",
  model_version: "model.v1",
  feature_set_version: "features.v1",
  experiment_id: "experiment-ui006-p03-1",
  statistical_report_id: "stat-ui006-p03-1",
  calibration_report_id: "cal-ui006-p03-1",
  economic_report_id: "econ-ui006-p03-1",
  generalization_report_id: "gen-ui006-p03-1",
  inference_input_hash: "input-hash-ui006-p03-1",
  raw_score: null,
  calibrated_confidence: 0.5,
  input_staleness_seconds: 60,
  signal_validity_seconds: 300,
  expires_at: "2026-07-26T08:05:00Z",
  freshness_status: "fresh",
  signal_direction: "positive_bias",
  signal_state: "warning",
  state_reason: "POORLY_CALIBRATED",
  eligibility_reasons: ["stored_warning"],
  operating_domain_status: "valid",
  calibration_status: "warning:POORLY_CALIBRATED",
  economic_verdict: "not_assessed",
  risk_notes: null,
  rationale: "Stored advisory rationale.",
  explainability_summary: { confidence_source: "stored_calibration" },
  state_transition_history: ["candidate", "warning"],
  audit_correlation_id: "corr-signal-ui006-p03-1",
};

function workspace() {
  return (
    <ResearchManagementWorkspace
      collections={[collection]}
      members={[member]}
      tags={[tag]}
      artifacts={[scenario]}
      signals={[signal]}
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

describe("UI-006-P03 lineage relationships and advanced filtering", () => {
  it("test_ui006_lineage_and_relationships_render_stored_links_read_only_no_inference", () => {
    render(workspace());

    fireEvent.click(screen.getAllByText("P03 relationship scenario")[0]);
    const detail = screen.getByLabelText("Read-only artifact metadata detail");
    expect(within(detail).getByText("Stored lineage")).toBeInTheDocument();
    expect(within(detail).getByText("Stored relationships")).toBeInTheDocument();
    expect(within(detail).getByText("source-ui006-p03-1")).toBeInTheDocument();
    expect(within(detail).getByText(/collection:collection-ui006-p03-1/)).toBeInTheDocument();
    expect(within(detail).getByText(/tag:relationship-review/)).toBeInTheDocument();
    expect(within(detail).getByText("scenario-hash-ui006-p03-1")).toBeInTheDocument();
  });

  it("test_ui006_advanced_filtering_is_in_memory_only_no_persistence", async () => {
    render(workspace());

    const filters = screen.getByLabelText("In-memory artifact filters");
    expect(filters).toHaveTextContent("In-memory only");
    fireEvent.change(screen.getByLabelText("Family"), { target: { value: "Scenario reports" } });
    fireEvent.change(screen.getByLabelText("Stored relationship"), {
      target: { value: "tag:relationship-review" },
    });
    expect(screen.getByLabelText("Filtered view scope notice")).toHaveTextContent("Showing 1 of");
    expect(screen.getByLabelText("Read-only unified artifact catalog")).toHaveTextContent(
      "P03 relationship scenario",
    );

    const sourceText = await readProductionSource();
    expect(sourceText).not.toContain("operator_workspace_preferences");
    expect(sourceText).not.toContain("artifact-explorer-workspace-v1");
    expect(sourceText).not.toContain("unified-artifact-explorer-workspace-v1");
  });

  it("test_ui006_filtered_views_preserve_no_cherry_picking_scope_and_limitations", () => {
    render(workspace());

    fireEvent.change(screen.getByLabelText("Family"), { target: { value: "Scenario reports" } });
    fireEvent.click(screen.getAllByText("P03 relationship scenario")[0]);
    const notice = screen.getByLabelText("Filtered view scope notice");
    expect(notice).toHaveTextContent("No cherry-picking");
    expect(notice).toHaveTextContent("scope, sample count, uncertainty, limitations, source ids, lineage, and hashes");
    const detail = screen.getByLabelText("Read-only artifact metadata detail");
    expect(detail).toHaveTextContent("Sample count");
    expect(detail).toHaveTextContent("6");
    expect(detail).toHaveTextContent("historical_band");
    expect(detail).toHaveTextContent("hypothetical_counterfactual_research_only");
    expect(detail).toHaveTextContent("not_a_prediction");
  });

  it("test_ui006_lineage_relationships_filtering_contain_no_mutation_actuation_or_gate_path", async () => {
    render(workspace());

    const buttonText = screen
      .getAllByRole("button")
      .map((button) => button.textContent?.toLowerCase() ?? "")
      .join(" ");
    for (const marker of ["create collection", "create tag", "add member", "delete", "remove", "update", "submit"]) {
      expect(buttonText).not.toContain(marker);
    }

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
      "inferrelationship",
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

  it("test_ui006_lineage_relationships_filtering_accessibility_and_doc16_brand_hold", () => {
    renderExplorerShell();

    expect(screen.getByText(/AXIOM Institutional Workstation/i)).toBeInTheDocument();
    expect(screen.getAllByText("Gate CLOSED").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("Research-only").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByLabelText("In-memory artifact filters")).toBeInTheDocument();
    expect(screen.getByLabelText("Filtered view scope notice")).toBeInTheDocument();
    expect(screen.getByLabelText("Read-only unified artifact catalog")).toBeInTheDocument();
    expect(screen.getByLabelText("Read-only artifact metadata detail")).toBeInTheDocument();
    expect(document.body.querySelectorAll(".mono").length).toBeGreaterThan(8);
  });
});
