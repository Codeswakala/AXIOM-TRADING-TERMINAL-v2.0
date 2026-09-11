import { fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { ResearchManagementWorkspace } from "../../components/terminal/research/ResearchHubView";
import type {
  AdvisorySignal,
  AdvancedResearchReport,
  ChartResearchAnnotation,
  ExecutionResearchBundle,
  InstitutionalReport,
  ManualJournalEntry,
  PortfolioResearchDashboard,
  ResearchCollection,
  ResearchCollectionMember,
  ResearchTag,
  ScenarioReport,
  TradePlanNote,
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
  collection_id: "collection-ui006-p02-1",
  created_at: "2026-07-26T08:00:00Z",
  updated_at: "2026-07-26T08:00:00Z",
  operator_id: "operator-1",
  name: "P02 Artifact Review",
  description: "Existing collection metadata.",
  research_status: "research_only",
  audit_correlation_id: "corr-collection-ui006-p02-1",
};

const member: ResearchCollectionMember = {
  member_id: "member-ui006-p02-1",
  created_at: "2026-07-26T08:00:00Z",
  operator_id: "operator-1",
  collection_id: "collection-ui006-p02-1",
  artifact_type: "scenario_report",
  artifact_id: "scenario-ui006-p02-1",
  audit_correlation_id: "corr-member-ui006-p02-1",
};

const tag: ResearchTag = {
  tag_id: "tag-ui006-p02-1",
  created_at: "2026-07-26T08:00:00Z",
  operator_id: "operator-1",
  artifact_type: "scenario_report",
  artifact_id: "scenario-ui006-p02-1",
  tag: "catalog-review",
  audit_correlation_id: "corr-tag-ui006-p02-1",
};

const signal: AdvisorySignal = {
  signal_id: "signal-ui006-p02-1",
  created_at: "2026-07-26T08:00:00Z",
  as_of_time: "2026-07-26T07:59:00Z",
  market_class: "forex",
  provider: "internal",
  symbol: "EURUSD",
  timeframe: "M1",
  model_artifact_id: "model-ui006-p02-1",
  model_version: "model.v1",
  feature_set_version: "features.v1",
  experiment_id: "experiment-ui006-p02-1",
  statistical_report_id: "stat-ui006-p02-1",
  calibration_report_id: "cal-ui006-p02-1",
  economic_report_id: "econ-ui006-p02-1",
  generalization_report_id: "gen-ui006-p02-1",
  inference_input_hash: "input-hash-ui006-p02-1",
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
  audit_correlation_id: "corr-signal-ui006-p02-1",
};

const report: InstitutionalReport = {
  id: "report-ui006-p02-1",
  artifact_type: "signal_validation_report",
  method_version: "validation.method.v1",
  sample_count: 12,
  research_status: "research_only",
  report_hash: "report-hash-ui006-p02-1",
  limitations: ["sample_bound", "research_only"],
  uncertainty: {
    method: "wilson_score_interval",
    lower: 0.2,
    upper: 0.7,
    confidence_level: 0.95,
    sample_count: 12,
  },
  economic_usefulness: { verdict: "not_assessed" },
  source_artifact_ids: ["signal-ui006-p02-1"],
  input_lineage: { source: "persisted_report" },
  results: { stored_result: true },
};

const scenario: ScenarioReport = {
  id: "scenario-ui006-p02-1",
  created_at: "2026-07-26T08:00:00Z",
  artifact_type: "scenario_report",
  method_version: "scenario.method.v1",
  market_class: "forex",
  symbol: "EURUSD",
  timeframe: "M1",
  as_of_start: "2026-07-26T07:00:00Z",
  as_of_end: "2026-07-26T08:00:00Z",
  sample_count: 6,
  scenario_name: "P02 stored hypothetical scenario",
  hypothetical_return: 0.01,
  scenario_result: { hypothetical_return: 0.01, counterfactual_index: 1.01 },
  assumptions: { horizon_bars: 4 },
  inputs: { baseline_returns: [0.01] },
  uncertainty: { method: "historical_band", lower: 0, upper: 0.02, sample_count: 6 },
  economic_usefulness: { verdict: "not_assessed" },
  config: { fixture: true },
  input_lineage: { input_policy: "as_of_bounded_hypothetical_research" },
  source_artifact_ids: ["source-ui006-p02-1"],
  market_scope: { symbol: "EURUSD", timeframe: "M1", sample_count: 6 },
  results: { stored: true },
  limitations: ["hypothetical_counterfactual_research_only", "not_a_prediction"],
  report_hash: "scenario-hash-ui006-p02-1",
  research_status: "research_only",
  created_by: "test",
  audit_correlation_id: "corr-scenario-ui006-p02-1",
  notes: "read only source artifact",
};

const portfolioDashboard: PortfolioResearchDashboard = {
  operator_id: "operator-1",
  generated_at: "2026-07-26T08:00:00Z",
  research_status: "research_only",
  disclaimer: "Research only.",
  aggregate_cards: [
    {
      key: "stored_count",
      label: "Stored count",
      value: 2,
      sample_count: 2,
      source_artifact_ids: ["portfolio-source-ui006-p02-1"],
      uncertainty: { method: "descriptive_count_only", sample_count: 2 },
      limitations: ["descriptive_only"],
      economic_usefulness: { verdict: "not_assessed" },
    },
  ],
  included_scope: { policy: "full_current_operator_scope_no_cherry_picking" },
  limitations: ["descriptive_only"],
  economic_usefulness: { verdict: "not_assessed" },
  source_artifact_ids: ["portfolio-source-ui006-p02-1"],
};

const advancedReport: AdvancedResearchReport = {
  report_id: "advanced-ui006-p02-1",
  method_version: "advanced.method.v1",
  operator_id: "operator-1",
  research_status: "research_only",
  disclaimer: "Research only.",
  included_scope: { source_artifact_ids: ["portfolio-source-ui006-p02-1"] },
  sections: [],
  source_artifact_ids: ["portfolio-source-ui006-p02-1"],
  limitations: ["descriptive_only"],
  economic_usefulness: { verdict: "not_assessed" },
  report_hash: "advanced-hash-ui006-p02-1",
  export_preview_markdown: "# Report",
  persisted: false,
};

const tradePlan: TradePlanNote = {
  plan_id: "plan-ui006-p02-1",
  created_at: "2026-07-26T08:00:00Z",
  updated_at: "2026-07-26T08:00:00Z",
  operator_id: "operator-1",
  title: "P02 research plan note",
  market_context: "Stored market context.",
  hypothesis: "Stored hypothesis.",
  linked_signal_ids: ["signal-ui006-p02-1"],
  linked_report_ids: ["scenario-ui006-p02-1"],
  scenario_notes: "Scenario notes.",
  risk_notes: "Research risk notes.",
  invalidating_conditions_text: "Evidence changed.",
  decision_status: "draft",
  research_disclaimer: "Research only.",
  research_status: "research_only",
  audit_correlation_id: "corr-plan-ui006-p02-1",
};

const journalEntry: ManualJournalEntry = {
  journal_id: "journal-ui006-p02-1",
  created_at: "2026-07-26T08:00:00Z",
  operator_id: "operator-1",
  title: "P02 research reflection",
  reflection_text: "Stored reflection.",
  linked_plan_id: "plan-ui006-p02-1",
  linked_signal_ids: ["signal-ui006-p02-1"],
  linked_report_ids: ["scenario-ui006-p02-1"],
  emotion_tags: ["calm"],
  process_tags: ["review"],
  lesson_notes: "Stored lesson.",
  research_disclaimer: "Research only.",
  research_status: "research_only",
  audit_correlation_id: "corr-journal-ui006-p02-1",
};

const executionBundle: ExecutionResearchBundle = {
  runs: [
    {
      run_id: "run-ui006-p02-1",
      created_at: "2026-07-26T08:00:00Z",
      operator_id: "operator-1",
      simulation_mode: "SIMULATED",
      simulation_policy_version: "simulation.policy.v1",
      input_artifact_ids: ["signal-ui006-p02-1"],
      replay_scope: { symbol: "EURUSD" },
      fill_model_name: "deterministic_mid_close_slippage",
      fill_model_version: "fill.model.v1",
      assumptions: { deterministic: true },
      limitations: ["simulated_research_only"],
      research_status: "research_only",
      simulation_disclaimer: "SIMULATED research only.",
      audit_correlation_id: "corr-run-ui006-p02-1",
    },
  ],
  fills: [],
  ledger: [],
  riskReports: [],
  experiments: [],
  analyticsReports: [
    {
      report_id: "analytics-ui006-p02-1",
      created_at: "2026-07-26T08:00:00Z",
      simulation_mode: "SIMULATED",
      analytics_type: "simulated_return_review",
      included_scope: { full_scope_included: true },
      sample_count: 3,
      metrics: { simulated_average_return_estimate: { value: 0.01 } },
      uncertainty: { method: "per_metric_interval_or_insufficient_sample_limitation", sample_count: 3 },
      limitations: ["full_declared_scope_included"],
      economic_usefulness: { verdict: "not_assessed" },
      report_hash: "analytics-hash-ui006-p02-1",
      source_artifact_ids: ["run-ui006-p02-1"],
      research_status: "research_only",
      simulation_disclaimer: "SIMULATED research only.",
      audit_correlation_id: "corr-analytics-ui006-p02-1",
    },
  ],
};

const chartAnnotation: ChartResearchAnnotation = {
  id: "annotation-ui006-p02-1",
  created_at: "2026-07-26T08:00:00Z",
  operator_id: "operator-1",
  artifact_type: "chart_research_annotation",
  chart_context: { symbol: "EURUSD", timeframe: "M1" },
  content: { note: "Stored annotation" },
  source_artifact_ids: ["scenario-ui006-p02-1"],
  provenance: { source: "chart_workspace" },
  uncertainty: { method: "operator_annotation" },
  disclaimer: "Research only.",
  research_status: "research_only",
  audit_correlation_id: "corr-annotation-ui006-p02-1",
};

function workspace() {
  return (
    <ResearchManagementWorkspace
      collections={[collection]}
      members={[member]}
      tags={[tag]}
      artifacts={[scenario]}
      signals={[signal]}
      intelligenceReports={[report]}
      tradePlans={[tradePlan]}
      journalEntries={[journalEntry]}
      executionBundle={executionBundle}
      portfolioDashboard={portfolioDashboard}
      advancedReport={advancedReport}
      chartAnnotations={[chartAnnotation]}
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

describe("UI-006-P02 Unified artifact catalog and metadata detail", () => {
  it("test_ui006_catalog_lists_existing_artifacts_across_families_read_only", () => {
    render(workspace());

    const catalog = screen.getByLabelText("Read-only unified artifact catalog");
    for (const label of [
      "EURUSD · M1 · positive_bias",
      "signal_validation_report · report-ui006-p02-1",
      "P02 stored hypothetical scenario",
      "Portfolio research dashboard",
      "Advanced research report preview",
      "chart_research_annotation",
      "P02 research plan note",
      "P02 research reflection",
      "run-ui006-p02-1",
      "simulated_return_review",
      "P02 Artifact Review",
      "scenario_report · scenario-ui006-p02-1",
      "catalog-review",
    ]) {
      expect(catalog).toHaveTextContent(label);
    }
    expect(screen.queryByText("Create collection")).not.toBeInTheDocument();
    expect(screen.queryByText("Create tag")).not.toBeInTheDocument();
  });

  it("test_ui006_metadata_detail_renders_stored_fields_verbatim_without_recompute", () => {
    render(workspace());

    fireEvent.click(screen.getByText("P02 stored hypothetical scenario"));
    const detail = screen.getByLabelText("Read-only artifact metadata detail");
    expect(detail).toHaveTextContent("scenario-ui006-p02-1");
    expect(detail).toHaveTextContent("scenario_report");
    expect(detail).toHaveTextContent("research_only");
    expect(detail).toHaveTextContent("scenario.method.v1");
    expect(detail).toHaveTextContent("6");
    expect(detail).toHaveTextContent("not_assessed");
    expect(detail).toHaveTextContent("historical_band");
    expect(detail).toHaveTextContent("scenario-hash-ui006-p02-1");
    expect(detail).toHaveTextContent("source-ui006-p02-1");
  });

  it("test_ui006_catalog_preserves_no_cherry_picking_scope_sample_and_limitations", () => {
    render(workspace());

    fireEvent.click(screen.getByText("P02 stored hypothetical scenario"));
    const detail = screen.getByLabelText("Read-only artifact metadata detail");
    expect(detail).toHaveTextContent("Sample count");
    expect(detail).toHaveTextContent("Uncertainty");
    expect(detail).toHaveTextContent("hypothetical_counterfactual_research_only");
    expect(detail).toHaveTextContent("not_a_prediction");
    expect(detail).toHaveTextContent("Scope");
    expect(detail).toHaveTextContent("present");
  });

  it("test_ui006_catalog_contains_no_mutation_actuation_or_gate_path", async () => {
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

  it("test_ui006_catalog_accessibility_and_doc16_brand_markers_hold", () => {
    renderExplorerShell();

    expect(screen.getByText(/AXIOM Institutional Workstation/i)).toBeInTheDocument();
    expect(screen.getAllByText("Gate CLOSED").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("Research-only").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByLabelText("Unified artifact explorer frame")).toBeInTheDocument();
    expect(screen.getByLabelText("Read-only unified artifact catalog")).toBeInTheDocument();
    expect(screen.getByLabelText("Read-only artifact metadata detail")).toBeInTheDocument();
    expect(screen.getByLabelText("Artifact explorer guardrail")).toHaveTextContent("Gate CLOSED");
    expect(document.body.querySelectorAll(".mono").length).toBeGreaterThan(8);
  });
});
