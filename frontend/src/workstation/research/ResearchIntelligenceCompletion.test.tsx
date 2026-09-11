import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { InstitutionalIntelligenceWorkspace } from "../../pages/InstitutionalIntelligencePage";
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
    id: "completion-report-1",
    artifact_type: "signal_validation_report",
    method_version: "completion.method.v1",
    sample_count: 11,
    research_status: "research_only",
    report_hash: "hash-completion-1",
    limitations: ["research_only", "sample_bound"],
    uncertainty: {
      method: "wilson_score_interval",
      lower: 0.2,
      upper: 0.7,
      confidence_level: 0.95,
      sample_count: 11,
    },
    economic_usefulness: { verdict: "not_assessed" },
    outcome_data_status: { status: "not_available" },
    source_artifact_ids: ["source-completion-1"],
    market_scope: { symbol: "EURUSD", timeframe: "M1", sample_count: 11 },
    results: { stored_result: true },
    input_lineage: { source: "persisted_report" },
    ...overrides,
  };
}

function signal(overrides: Partial<AdvisorySignal> = {}): AdvisorySignal {
  return {
    signal_id: "completion-signal-1",
    created_at: "2026-07-24T08:00:00Z",
    as_of_time: "2026-07-24T07:59:00Z",
    market_class: "forex",
    provider: "internal",
    symbol: "EURUSD",
    timeframe: "M1",
    model_artifact_id: "completion-model-1",
    model_version: "completion.model.v1",
    feature_set_version: "completion.features.v1",
    experiment_id: "completion-exp-1",
    statistical_report_id: "completion-stat-1",
    calibration_report_id: "completion-cal-1",
    economic_report_id: "completion-econ-1",
    generalization_report_id: "completion-gen-1",
    inference_input_hash: "completion-hash-1",
    raw_score: 0.99,
    calibrated_confidence: 0.5,
    input_staleness_seconds: 60,
    signal_validity_seconds: 300,
    expires_at: "2026-07-24T08:05:00Z",
    freshness_status: "fresh",
    signal_direction: "positive_bias",
    signal_state: "warning",
    state_reason: "POORLY_CALIBRATED",
    eligibility_reasons: [],
    operating_domain_status: "valid",
    calibration_status: "warning:POORLY_CALIBRATED",
    economic_verdict: "not_assessed",
    risk_notes: null,
    rationale: "Stored advisory rationale for completion evidence.",
    explainability_summary: { stored: true },
    state_transition_history: ["candidate", "warning"],
    audit_correlation_id: "completion-corr-1",
    ...overrides,
  };
}

const bundle: InstitutionalIntelligenceBundle = {
  relation: [report({ id: "relation-completion", artifact_type: "correlation_report" })],
  context: [report({ id: "context-completion", artifact_type: "regime_report" })],
  hypothetical: [report({ id: "scenario-completion", artifact_type: "scenario_report" })],
  risk: [report({ id: "risk-completion", artifact_type: "portfolio_risk_report" })],
  validation: [report({ id: "validation-completion", artifact_type: "signal_validation_report" })],
};

const analytics = {
  generated_from: "existing-advisory-analytics-read-api",
  disclaimer: "Research analytics only.",
  metrics: [
    {
      key: "completion_metric",
      label: "Completion metric",
      value: 0.5,
      unit: "ratio",
      sample_count: 11,
      uncertainty: {
        method: "wilson_score_interval",
        lower: 0.2,
        upper: 0.7,
        confidence_level: 0.95,
        sample_count: 11,
      },
      interpretation: "Stored analytics interpretation.",
    },
  ],
  confidence_bands: [
    {
      label: "completion band",
      lower: 0.4,
      upper: 0.6,
      sample_count: 11,
      average_calibrated_confidence: 0.5,
      calibration_status: "warning:POORLY_CALIBRATED",
      uncertainty: {
        method: "wilson_score_interval",
        lower: 0.2,
        upper: 0.7,
        confidence_level: 0.95,
        sample_count: 11,
      },
      unreliable: true,
      economic_context: "not_assessed",
    },
  ],
  notes: ["Stored analytics note"],
  limitations: ["analytics_limit"],
  source_artifact_ids: ["analytics-source-completion"],
  included_scope: { symbol: "EURUSD", timeframe: "M1", sample_count: 11 },
} as AdvisoryAnalyticsResponse & {
  limitations: string[];
  source_artifact_ids: string[];
  included_scope: Record<string, unknown>;
};

const collection: ResearchCollection = {
  collection_id: "completion-collection-1",
  created_at: "2026-07-24T08:00:00Z",
  updated_at: "2026-07-24T08:01:00Z",
  operator_id: "operator-1",
  name: "Completion Review Set",
  description: "Read-only completion context.",
  research_status: "research_only",
  audit_correlation_id: "completion-collection-corr",
};

const member: ResearchCollectionMember = {
  member_id: "completion-member-1",
  created_at: "2026-07-24T08:00:00Z",
  operator_id: "operator-1",
  collection_id: "completion-collection-1",
  artifact_type: "signal_validation_report",
  artifact_id: "validation-completion",
  audit_correlation_id: "completion-member-corr",
};

const tag: ResearchTag = {
  tag_id: "completion-tag-1",
  created_at: "2026-07-24T08:00:00Z",
  operator_id: "operator-1",
  artifact_type: "advisory_signal",
  artifact_id: "completion-signal-1",
  tag: "completion-review",
  audit_correlation_id: "completion-tag-corr",
};

const researchManagement: ResearchManagementBundle = {
  collections: [collection],
  members: [member],
  tags: [tag],
  supported_artifact_types: ["signal_validation_report", "advisory_signal"],
  posture: "research_only",
};

const journalEntry: ManualJournalEntry = {
  journal_id: "completion-journal-1",
  created_at: "2026-07-24T08:00:00Z",
  operator_id: "operator-1",
  title: "Completion review journal",
  reflection_text: "Review stored completion evidence.",
  linked_plan_id: null,
  linked_signal_ids: ["completion-signal-1"],
  linked_report_ids: ["validation-completion"],
  emotion_tags: [],
  process_tags: ["review"],
  lesson_notes: null,
  research_disclaimer: "Research only.",
  research_status: "research_only",
  audit_correlation_id: "completion-journal-corr",
};

function renderWorkspaceShell() {
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

describe("UI-004-P06 completion checkpoint", () => {
  it("test_ui004_completion_research_intelligence_workflow_is_continuous_without_scope_expansion", () => {
    renderWorkspaceShell();

    const workspace = workspaceForPath("/intelligence");
    expect(workspace.id).toBe("research.intelligence");
    expect(workspace.requiresAuth).toBe(true);
    expect(workspace.noActuation).toBe(true);
    expect(WORKSPACE_REGISTRY.some((item) => item.route === "/research-intelligence")).toBe(false);
    expect(screen.getAllByTestId("institutional-workspace-shell")).toHaveLength(1);
    expect(screen.getByLabelText("Research and intelligence workspace frame")).toBeInTheDocument();
    expect(screen.getByLabelText("Read-only advisory signal research surface")).toBeInTheDocument();
    expect(screen.getByLabelText("Read-only performance analytics research surface")).toBeInTheDocument();
    expect(screen.getByLabelText("First-party intelligence report viewer")).toBeInTheDocument();
    expect(screen.getByLabelText("Validation and economic-usefulness integrity panels")).toBeInTheDocument();
    expect(screen.getByLabelText("Read-only research artifact context")).toBeInTheDocument();
  });

  it("test_ui004_completion_all_research_surfaces_are_existing_artifact_presentation_only", async () => {
    renderWorkspaceShell();

    expect(screen.getByLabelText("UI-004 governed data-source inventory")).toHaveTextContent("fetchInstitutionalIntelligenceBundle");
    expect(screen.getByLabelText("Read-only advisory signal research surface")).toHaveTextContent("fetchAdvisorySignals");
    expect(screen.getByLabelText("Read-only performance analytics research surface")).toHaveTextContent("fetchAdvisoryAnalytics");
    expect(screen.getByLabelText("First-party intelligence report viewer")).toHaveTextContent("existing W4/W7 report payloads");
    expect(screen.getByLabelText("Validation and economic-usefulness integrity panels")).toHaveTextContent("Stored Validation Statuses");
    expect(screen.getByLabelText("Read-only research artifact context")).toHaveTextContent("Completion Review Set");
    expect(screen.getByLabelText("Saved view persistence absence")).toHaveTextContent("not implemented");

    const sourceText = await readProductionSource("pages/InstitutionalIntelligencePage.tsx");
    expect(sourceText).toContain("fetchResearchManagementBundle");
    expect(sourceText).toContain("fetchJournalEntries");
    expect(sourceText).not.toContain("operator_workspace_preferences");
    expect(sourceText).not.toContain("research-intelligence-workspace-v1");
  });

  it("test_ui004_completion_no_recompute_inference_external_ai_live_data_or_execution_path", async () => {
    const sourceText = (await readProductionSource("pages/InstitutionalIntelligencePage.tsx")).toLowerCase();
    const forbidden = [
      "infersignal",
      "runinference",
      "authoritativerecompute",
      "emitsignal",
      "generatesignal",
      "recompute",
      "recalculat",
      "deriveconfidence",
      "reclassif",
      "openai",
      "gpt",
      "external_llm",
      "new analyticsengine",
      "new intelligenceengine",
      "startlivemarket",
      "fetchlivemarketstats",
      "place_order",
      "open_gate",
      "/api/v1/orders",
    ];
    for (const marker of forbidden) {
      expect(sourceText).not.toContain(marker);
    }
  });

  it("test_ui004_completion_validation_economic_usefulness_and_no_cherry_picking_hold", () => {
    renderWorkspaceShell();

    const validation = screen.getByLabelText("Validation and economic-usefulness integrity panels");
    expect(validation).toHaveTextContent("research_only");
    expect(validation).toHaveTextContent("not_assessed");
    expect(validation).toHaveTextContent("warning:POORLY_CALIBRATED");
    expect(validation).toHaveTextContent("11");
    expect(validation).toHaveTextContent("20.00% to 70.00%");
    expect(validation).toHaveTextContent("sample_bound");

    const analyticsPanel = screen.getByLabelText("Read-only performance analytics research surface");
    expect(analyticsPanel).toHaveTextContent("No selective performance claim");
    expect(analyticsPanel).toHaveTextContent("Sample count");
    expect(analyticsPanel).toHaveTextContent("analytics_limit");
    expect(analyticsPanel).toHaveTextContent("analytics-source-completion");
  });

  it("test_ui004_completion_accessibility_brand_and_ui001_ui002_integration_hold", () => {
    renderWorkspaceShell();

    expect(screen.getByText(/AXIOM Institutional Workstation/i)).toBeInTheDocument();
    expect(screen.getAllByText("Gate CLOSED").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("Research-only").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByLabelText("Global command bar")).toBeInTheDocument();
    expect(screen.getByLabelText("Institutional workflow navigation")).toBeInTheDocument();
    expect(screen.getByLabelText("Breadcrumb")).toBeInTheDocument();
    expect(screen.getByLabelText("Context panel")).toBeInTheDocument();
    expect(screen.getByLabelText("Activity dock")).toBeInTheDocument();
    expect(screen.getByLabelText("Report family navigation")).toBeInTheDocument();
    expect(screen.getByLabelText("Progressive report drilldowns")).toBeInTheDocument();
    expect(screen.getByLabelText("Existing artifact id inventory").querySelectorAll(".mono").length).toBeGreaterThan(2);
  });
});
