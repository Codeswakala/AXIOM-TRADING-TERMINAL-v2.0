import { render, screen, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import {
  InstitutionalIntelligenceWorkspace,
  ResearchArtifactContextPanel,
} from "../../pages/InstitutionalIntelligencePage";
import type {
  AdvisoryAnalyticsResponse,
  AdvisorySignal,
  InstitutionalIntelligenceBundle,
  InstitutionalReport,
  ManualJournalEntry,
  ResearchCollection,
  ResearchCollectionMember,
  ResearchManagementBundle,
  ResearchTag,
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

function report(overrides: Partial<InstitutionalReport> = {}): InstitutionalReport {
  return {
    id: "report-artifact-1",
    artifact_type: "signal_validation_report",
    method_version: "method.v1",
    sample_count: 7,
    research_status: "research_only",
    report_hash: "hash-artifact-1",
    limitations: ["research_only"],
    uncertainty: { method: "declared", lower: 0.1, upper: 0.5, sample_count: 7 },
    source_artifact_ids: ["source-report-1"],
    results: { stored: true },
    ...overrides,
  };
}

function signal(overrides: Partial<AdvisorySignal> = {}): AdvisorySignal {
  return {
    signal_id: "signal-artifact-1",
    created_at: "2026-07-24T08:00:00Z",
    as_of_time: "2026-07-24T07:59:00Z",
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
    inference_input_hash: "hash-1",
    raw_score: null,
    calibrated_confidence: 0.5,
    input_staleness_seconds: 60,
    signal_validity_seconds: 300,
    expires_at: "2026-07-24T08:05:00Z",
    freshness_status: "fresh",
    signal_direction: "positive_bias",
    signal_state: "emitted",
    state_reason: "ELIGIBLE",
    eligibility_reasons: [],
    operating_domain_status: "valid",
    calibration_status: "calibrated",
    economic_verdict: "not_assessed",
    risk_notes: null,
    rationale: "Stored signal.",
    explainability_summary: {},
    state_transition_history: ["candidate", "emitted"],
    audit_correlation_id: "corr-1",
    ...overrides,
  };
}

const bundle: InstitutionalIntelligenceBundle = {
  relation: [report()],
  context: [],
  hypothetical: [],
  risk: [],
  validation: [],
};

const collection: ResearchCollection = {
  collection_id: "collection-1",
  created_at: "2026-07-24T08:00:00Z",
  updated_at: "2026-07-24T08:01:00Z",
  operator_id: "operator-1",
  name: "Validation Review Set",
  description: "Read-only collection context.",
  research_status: "research_only",
  audit_correlation_id: "corr-collection",
};

const member: ResearchCollectionMember = {
  member_id: "member-1",
  created_at: "2026-07-24T08:00:00Z",
  operator_id: "operator-1",
  collection_id: "collection-1",
  artifact_type: "signal_validation_report",
  artifact_id: "report-artifact-1",
  audit_correlation_id: "corr-member",
};

const tag: ResearchTag = {
  tag_id: "tag-1",
  created_at: "2026-07-24T08:00:00Z",
  operator_id: "operator-1",
  artifact_type: "advisory_signal",
  artifact_id: "signal-artifact-1",
  tag: "calibration-review",
  audit_correlation_id: "corr-tag",
};

const researchManagement: ResearchManagementBundle = {
  collections: [collection],
  members: [member],
  tags: [tag],
  supported_artifact_types: ["signal_validation_report", "advisory_signal"],
  posture: "research_only",
};

const journalEntry: ManualJournalEntry = {
  journal_id: "journal-1",
  created_at: "2026-07-24T08:00:00Z",
  operator_id: "operator-1",
  title: "Validation review journal",
  reflection_text: "Review stored validation evidence.",
  linked_plan_id: null,
  linked_signal_ids: ["signal-artifact-1"],
  linked_report_ids: ["report-artifact-1"],
  emotion_tags: [],
  process_tags: ["review"],
  lesson_notes: null,
  research_disclaimer: "Research only.",
  research_status: "research_only",
  audit_correlation_id: "corr-journal",
};

const analytics = {
  generated_from: "existing-read-api",
  disclaimer: "Research analytics only.",
  metrics: [],
  confidence_bands: [],
  notes: [],
  source_artifact_ids: ["analytics-source-1"],
} as AdvisoryAnalyticsResponse & { source_artifact_ids: string[] };

function renderPanel() {
  render(
    <ResearchArtifactContextPanel
      bundle={bundle}
      signals={[signal()]}
      analytics={analytics}
      researchManagement={researchManagement}
      journalEntries={[journalEntry]}
    />,
  );
}

function renderShell() {
  render(
    <MemoryRouter initialEntries={["/intelligence"]}>
      <Routes>
        <Route element={<InstitutionalWorkspaceShell />}>
          <Route
            path="/intelligence"
            element={
              <InstitutionalIntelligenceWorkspace
                bundle={bundle}
                signals={[signal()]}
                analytics={analytics}
                researchManagement={researchManagement}
                journalEntries={[journalEntry]}
              />
            }
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

describe("UI-004-P05 research artifacts and collections context", () => {
  it("test_ui004_research_artifacts_render_existing_collections_tags_and_ids_read_only", () => {
    renderPanel();

    const panel = screen.getByLabelText("Read-only research artifact context");
    expect(panel).toHaveTextContent("Validation Review Set");
    expect(panel).toHaveTextContent("collection-1");
    expect(panel).toHaveTextContent("signal_validation_report");
    expect(panel).toHaveTextContent("report-artifact-1");
    expect(panel).toHaveTextContent("calibration-review");
    expect(panel).toHaveTextContent("signal-artifact-1");
    expect(panel).toHaveTextContent("Validation review journal");
    expect(panel).toHaveTextContent("source-report-1");
    expect(panel).toHaveTextContent("analytics-source-1");
  });

  it("test_ui004_collections_and_tags_expose_no_create_update_or_delete_mutation", () => {
    renderPanel();

    const panel = screen.getByLabelText("Read-only research artifact context");
    expect(within(panel).queryAllByRole("button")).toHaveLength(0);
    expect(within(panel).queryAllByRole("textbox")).toHaveLength(0);
    expect(within(panel).queryByText(/^Create/i)).not.toBeInTheDocument();
    expect(within(panel).queryByText(/^Update/i)).not.toBeInTheDocument();
    expect(within(panel).queryByText(/^Delete/i)).not.toBeInTheDocument();
  });

  it("test_ui004_no_saved_view_persistence_is_implemented_this_phase", async () => {
    renderPanel();

    expect(screen.getByLabelText("Saved view persistence absence")).toHaveTextContent(
      "Saved view persistence is not implemented in UI-004-P05",
    );
    const sourceText = await readProductionSource("pages/InstitutionalIntelligencePage.tsx");
    expect(sourceText).not.toContain("operator_workspace_preferences");
    expect(sourceText).not.toContain("research-intelligence-workspace-v1");
    expect(sourceText).not.toContain("createWorkspacePreference");
    expect(sourceText).not.toContain("updateWorkspacePreference");
  });

  it("test_ui004_research_artifact_surface_contains_no_recompute_inference_or_signal_generation", async () => {
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
      "reclassif",
      "new AnalyticsEngine",
      "new IntelligenceEngine",
      "/api/v1/orders",
    ];
    for (const marker of forbidden) {
      expect(sourceText).not.toContain(marker);
    }
  });

  it("test_ui004_research_artifact_surface_contains_no_execution_order_broker_account_or_gate_path", async () => {
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

  it("test_ui004_research_artifacts_accessibility_and_brand_markers_hold", () => {
    renderShell();

    expect(screen.getByText(/AXIOM Institutional Workstation/i)).toBeInTheDocument();
    expect(screen.getAllByText("Gate CLOSED").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("Research-only").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByLabelText("Artifact context posture")).toHaveTextContent("Read-only context");
    expect(screen.getByLabelText("Existing research collections")).toBeInTheDocument();
    expect(screen.getByLabelText("Existing collection member references")).toBeInTheDocument();
    expect(screen.getByLabelText("Existing research tags")).toBeInTheDocument();
    expect(screen.getByLabelText("Journal references")).toBeInTheDocument();
    expect(screen.getByLabelText("Existing artifact id inventory").querySelectorAll(".mono").length).toBeGreaterThan(2);
  });
});
