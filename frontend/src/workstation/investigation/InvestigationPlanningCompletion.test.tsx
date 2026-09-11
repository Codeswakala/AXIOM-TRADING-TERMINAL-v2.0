import { render, screen } from "@testing-library/react";
import type {
  AdvancedResearchReport,
  ExecutionResearchBundle,
  ManualJournalEntry,
  PortfolioResearchDashboard,
  ScenarioReport,
  TradePlanNote,
} from "../../api/client";

import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { ExecutionResearchWorkspace } from "../../components/terminal/execution/ExecutionResearchView";
import { ManualJournalWorkspace } from "../../pages/ManualJournalPage";
import { PortfolioResearchWorkspace } from "../../components/terminal/docks/PortfolioResearchPanel";
import { ScenarioComparisonPanel } from "../../components/terminal/docks/ScenarioComparisonPanel";
import { SignalInvestigationFrame } from "../../components/terminal/signals/SignalInvestigationRecords";
import { TradePlanningWorkspace } from "../../pages/TradePlanningPage";

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

function scenario(id: string, name: string): ScenarioReport {
  return {
    id,
    created_at: "2026-07-25T08:00:00Z",
    artifact_type: "scenario_report",
    method_version: "scenario.method.v1",
    market_class: "forex",
    symbol: "EURUSD",
    timeframe: "M1",
    as_of_start: "2026-07-25T07:00:00Z",
    as_of_end: "2026-07-25T08:00:00Z",
    sample_count: 6,
    scenario_name: name,
    hypothetical_return: 0.01,
    scenario_result: { hypothetical_return: 0.01, counterfactual_index: 1.01 },
    assumptions: { shock_return: 0.01, horizon_bars: 4 },
    inputs: { baseline_returns: [0.01, -0.01] },
    uncertainty: {
      method: "historical_volatility_band",
      lower: 0.0,
      upper: 0.02,
      confidence_level: 0.95,
      sample_count: 6,
    },
    economic_usefulness: { verdict: "not_assessed" },
    config: { stored_config: true },
    input_lineage: { input_policy: "as_of_bounded_hypothetical_research" },
    source_artifact_ids: [`source-${id}`],
    market_scope: { market_class: "forex", symbol: "EURUSD", timeframe: "M1" },
    results: { stored_result: true },
    limitations: ["hypothetical_counterfactual_research_only", "not_a_prediction"],
    report_hash: `hash-${id}`,
    research_status: "research_only",
    created_by: "test",
    audit_correlation_id: `corr-${id}`,
    notes: "Stored hypothetical scenario.",
  };
}

const dashboard: PortfolioResearchDashboard = {
  operator_id: "operator-1",
  generated_at: "2026-07-25T08:00:00Z",
  research_status: "research_only",
  disclaimer: "Portfolio research view over existing governed artifacts only.",
  aggregate_cards: [
    {
      key: "stored_research_count",
      label: "Stored research count",
      value: 2,
      sample_count: 2,
      source_artifact_ids: ["portfolio-source-ui005"],
      uncertainty: { method: "descriptive_count_only", sample_count: 2 },
      limitations: ["descriptive_research_aggregation_only"],
      economic_usefulness: { verdict: "not_assessed" },
    },
  ],
  included_scope: { policy: "full_current_operator_scope_no_cherry_picking" },
  limitations: ["descriptive_research_aggregation_only", "not_a_live_venue_record"],
  economic_usefulness: { verdict: "not_assessed" },
  source_artifact_ids: ["portfolio-source-ui005"],
};

const advancedReport: AdvancedResearchReport = {
  report_id: "advanced-report-ui005",
  method_version: "portfolio.method.v1",
  operator_id: "operator-1",
  research_status: "research_only",
  disclaimer: "Research only.",
  included_scope: { source_artifact_ids: ["portfolio-source-ui005"] },
  sections: [],
  source_artifact_ids: ["portfolio-source-ui005"],
  limitations: ["descriptive_research_aggregation_only"],
  economic_usefulness: { verdict: "not_assessed" },
  report_hash: "portfolio-hash-ui005",
  export_preview_markdown: "# Portfolio Research Report\nnot_assessed",
  persisted: false,
};

const plan: TradePlanNote = {
  plan_id: "plan-ui005-completion",
  created_at: "2026-07-25T08:00:00Z",
  updated_at: "2026-07-25T08:00:00Z",
  operator_id: "operator-1",
  title: "Completion research plan",
  market_context: "Governed market context only.",
  hypothesis: "Research hypothesis for completion review.",
  linked_signal_ids: ["completion-signal-ui005"],
  linked_report_ids: ["completion-scenario-a"],
  scenario_notes: "Hypothetical scenario context only.",
  risk_notes: "Research risk notes only.",
  invalidating_conditions_text: "Archive if evidence changes.",
  decision_status: "draft",
  research_disclaimer: "Research note only. Operator judgment required. AXIOM does not act.",
  research_status: "research_only",
  audit_correlation_id: "corr-plan-ui005-completion",
};

const journal: ManualJournalEntry = {
  journal_id: "journal-ui005-completion",
  created_at: "2026-07-25T08:00:00Z",
  operator_id: "operator-1",
  title: "Completion research reflection",
  reflection_text: "Reviewed investigation and planning evidence.",
  linked_plan_id: "plan-ui005-completion",
  linked_signal_ids: ["completion-signal-ui005"],
  linked_report_ids: ["completion-scenario-a"],
  emotion_tags: ["calm"],
  process_tags: ["completion-review"],
  lesson_notes: "Keep workflow evidence tied to artifact ids.",
  research_disclaimer: "Research reflection only. Operator judgment required. AXIOM does not act.",
  research_status: "research_only",
  audit_correlation_id: "corr-journal-ui005-completion",
};

const executionBundle: ExecutionResearchBundle = {
  runs: [
    {
      run_id: "run-ui005-completion",
      created_at: "2026-07-25T08:00:00Z",
      operator_id: "operator-1",
      simulation_mode: "SIMULATED",
      simulation_policy_version: "simulation.policy.v1",
      input_artifact_ids: ["completion-signal-ui005"],
      replay_scope: { symbol: "EURUSD", timeframe: "M1" },
      fill_model_name: "deterministic_mid_close_slippage",
      fill_model_version: "fill.model.v1",
      assumptions: { deterministic: true },
      limitations: ["simulated_research_only"],
      research_status: "research_only",
      simulation_disclaimer: "SIMULATED execution research only.",
      audit_correlation_id: "corr-run-ui005-completion",
    },
  ],
  fills: [],
  ledger: [],
  riskReports: [],
  experiments: [],
  analyticsReports: [
    {
      report_id: "analytics-ui005-completion",
      created_at: "2026-07-25T08:00:00Z",
      simulation_mode: "SIMULATED",
      analytics_type: "return_estimate_review",
      included_scope: { full_scope_included: true, sample_count: 3 },
      sample_count: 3,
      metrics: { simulated_average_return_estimate: { value: 0.01 } },
      uncertainty: { method: "per_metric_interval_or_insufficient_sample_limitation", sample_count: 3 },
      limitations: ["full_declared_scope_included", "simulated_research_only"],
      economic_usefulness: { verdict: "not_assessed" },
      report_hash: "analytics-hash-ui005-completion",
      source_artifact_ids: ["completion-signal-ui005"],
      research_status: "research_only",
      simulation_disclaimer: "SIMULATED execution research only.",
      audit_correlation_id: "corr-analytics-ui005-completion",
    },
  ],
};

function CompletionHarness() {
  return (
    <>
      <SignalInvestigationFrame />
      <ScenarioComparisonPanel
        reports={[
          scenario("completion-scenario-a", "completion_hypothetical_a"),
          scenario("completion-scenario-b", "completion_hypothetical_b"),
        ]}
      />
      <PortfolioResearchWorkspace dashboard={dashboard} report={advancedReport} />
      <TradePlanningWorkspace plans={[plan]} />
      <ManualJournalWorkspace entries={[journal]} />
      <MemoryRouter>
        <ExecutionResearchWorkspace bundle={executionBundle} />
      </MemoryRouter>
    </>
  );
}

function renderShellInvestigation() {
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

async function readUi005ProductionSources(): Promise<string> {
  const modules = import.meta.glob("../../**/*.{ts,tsx}", {
    query: "?raw",
    import: "default",
  });
  const wanted = [
    "SignalInvestigationRecords.tsx",
    "ScenarioComparisonPanel.tsx",
    "PortfolioResearchPanel.tsx",
    "TradePlanningPage.tsx",
    "ManualJournalPage.tsx",
    "ExecutionResearchView.tsx",
  ];
  const texts = await Promise.all(
    Object.entries(modules)
      .filter(([path]) => wanted.some((name) => path.endsWith(name)))
      .map(([, loader]) => (loader as () => Promise<string>)()),
  );
  return texts.join("\n");
}

describe("UI-005-P06 Investigation and Planning completion checkpoint", () => {
  it("test_ui005_completion_investigation_to_planning_workflow_is_continuous_without_scope_expansion", () => {
    render(<CompletionHarness />);

    const requiredRoutes = [
      "/investigate",
      "/compare-scenarios",
      "/portfolio-research",
      "/trade-plans",
      "/journal",
      "/execution-research",
    ];
    const routes = new Set(WORKSPACE_REGISTRY.map((workspace) => workspace.route));
    for (const route of requiredRoutes) {
      expect(routes.has(route)).toBe(true);
      expect(workspaceForPath(route).requiresAuth).toBe(true);
      expect(workspaceForPath(route).noActuation).toBe(true);
    }
    expect(routes.has("/investigation-planning")).toBe(false);
    expect(screen.getByText("Signal Investigation Workspace")).toBeInTheDocument();
    expect(screen.getByText("Scenario Comparison Workspace")).toBeInTheDocument();
    expect(screen.getAllByText("Portfolio Research").length).toBeGreaterThan(0);
    expect(screen.getByText("Trade Planning Workspace")).toBeInTheDocument();
    expect(screen.getByText("Manual Research Journal")).toBeInTheDocument();
    expect(screen.getByText("Execution Research Workspace")).toBeInTheDocument();
  });

  it("test_ui005_completion_all_surfaces_are_existing_artifact_presentation_or_existing_research_notes", () => {
    render(<CompletionHarness />);

    expect(screen.getByLabelText("UI-005 governed data-source inventory")).toHaveTextContent(
      "fetchAdvisorySignals + fetchInstitutionalIntelligenceBundle",
    );
    expect(screen.getByLabelText("Scenario investigation context")).toHaveTextContent(
      "stored scenario reports",
    );
    expect(screen.getByLabelText("Portfolio investigation context")).toHaveTextContent(
      "existing governed research artifacts",
    );
    expect(screen.getByLabelText("Trade planning investigation context")).toHaveTextContent(
      "existing W5 research-note store",
    );
    expect(screen.getByLabelText("Research journal investigation context")).toHaveTextContent(
      "existing W5 reflection store",
    );
    expect(screen.getByLabelText("Execution research investigation context")).toHaveTextContent(
      "execution-research read seams",
    );
    expect(screen.getAllByText("Completion research plan").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Completion research reflection").length).toBeGreaterThan(0);
  });

  it("test_ui005_completion_no_execution_broker_account_live_data_ai_or_gate_path", async () => {
    const sourceText = (await readUi005ProductionSources()).toLowerCase();
    const forbidden = [
      "b" + "uy",
      "s" + "ell",
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
      "llm_summary",
      "ai_summary",
      "/api/v1/orders",
    ];
    for (const marker of forbidden) {
      expect(sourceText).not.toContain(marker);
    }
  });

  it("test_ui005_completion_verbatim_values_no_cherry_picking_and_simulated_boundaries_hold", () => {
    render(<CompletionHarness />);

    expect(screen.getAllByText("completion_hypothetical_a").length).toBeGreaterThan(0);
    expect(screen.getAllByText(/historical_volatility_band/).length).toBeGreaterThan(0);
    expect(screen.getAllByText("not_assessed").length).toBeGreaterThanOrEqual(3);
    expect(screen.getByText(/hash-completion-scenario-a/)).toBeInTheDocument();
    expect(screen.getAllByText("portfolio-source-ui005").length).toBeGreaterThan(0);
    expect(screen.getByText(/full_current_operator_scope_no_cherry_picking/)).toBeInTheDocument();
    expect(screen.getAllByText("research_only").length).toBeGreaterThanOrEqual(4);
    expect(screen.getAllByText("SIMULATED").length).toBeGreaterThanOrEqual(2);
    expect(screen.getAllByText("simulated_research_only").length).toBeGreaterThan(0);
    expect(screen.getByText(/per_metric_interval_or_insufficient_sample_limitation/)).toBeInTheDocument();
  });

  it("test_ui005_completion_accessibility_brand_and_ui001_ui002_integration_hold", () => {
    renderShellInvestigation();

    expect(screen.getByText(/AXIOM Institutional Workstation/i)).toBeInTheDocument();
    expect(screen.getAllByText("Gate CLOSED").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("Research-only").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByLabelText("Global command bar")).toBeInTheDocument();
    expect(screen.getByLabelText("Institutional workflow navigation")).toBeInTheDocument();
    expect(screen.getByLabelText("Breadcrumb")).toBeInTheDocument();
    expect(screen.getByLabelText("Context panel")).toBeInTheDocument();
    expect(screen.getByLabelText("Activity dock")).toBeInTheDocument();
    expect(screen.getByLabelText("UI-005 governed data-source inventory").querySelectorAll(".mono").length).toBeGreaterThan(5);
  });
});
