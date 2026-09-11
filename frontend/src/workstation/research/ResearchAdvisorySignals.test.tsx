import { render, screen, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import {
  InstitutionalIntelligenceWorkspace,
  ResearchAdvisorySignalPanel,
} from "../../pages/InstitutionalIntelligencePage";
import type { AdvisorySignal, InstitutionalIntelligenceBundle } from "../../api/client";
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

function signal(overrides: Partial<AdvisorySignal> = {}): AdvisorySignal {
  const state = overrides.signal_state ?? "emitted";
  return {
    signal_id: `sig-ui004-${state}`,
    created_at: "2026-07-23T08:00:00Z",
    as_of_time: "2026-07-23T07:59:00Z",
    market_class: "forex",
    provider: "internal",
    symbol: "EURUSD",
    timeframe: "M1",
    model_artifact_id: "model-ui004",
    model_version: "model.v1",
    feature_set_version: "features.v1",
    experiment_id: "exp-ui004",
    statistical_report_id: "stat-ui004",
    calibration_report_id: "cal-ui004",
    economic_report_id: "econ-ui004",
    generalization_report_id: "gen-ui004",
    inference_input_hash: "hash-ui004",
    raw_score: 0.987654,
    calibrated_confidence: 0.42,
    input_staleness_seconds: 60,
    signal_validity_seconds: 300,
    expires_at: "2026-07-23T08:05:00Z",
    freshness_status: "fresh",
    signal_direction: "positive_bias",
    signal_state: state,
    state_reason: state === "emitted" ? "ELIGIBLE" : state.toUpperCase(),
    eligibility_reasons: [],
    operating_domain_status: "valid",
    calibration_status: "calibrated",
    economic_verdict: "not_assessed",
    risk_notes: null,
    rationale: "Persisted advisory rationale with governed guardrails and documented lineage.",
    explainability_summary: { persisted: true },
    state_transition_history: ["candidate", state],
    audit_correlation_id: "corr-ui004",
    ...overrides,
  };
}

const sampleSignals: AdvisorySignal[] = [
  signal({ signal_state: "emitted", signal_id: "sig-advisory" }),
  signal({
    signal_state: "warning",
    signal_id: "sig-warning",
    state_reason: "POORLY_CALIBRATED",
    calibration_status: "warning:POORLY_CALIBRATED",
  }),
  signal({
    signal_state: "withheld",
    signal_id: "sig-withheld",
    state_reason: "STALE_INPUT",
    freshness_status: "stale",
    calibrated_confidence: null,
  }),
  signal({
    signal_state: "expired",
    signal_id: "sig-expired",
    state_reason: "SIGNAL_EXPIRED",
    freshness_status: "expired",
  }),
];

const emptyBundle: InstitutionalIntelligenceBundle = {
  relation: [],
  context: [],
  hypothetical: [],
  risk: [],
  validation: [],
};

function renderShell() {
  render(
    <MemoryRouter initialEntries={["/intelligence"]}>
      <Routes>
        <Route element={<InstitutionalWorkspaceShell />}>
          <Route
            path="/intelligence"
            element={<InstitutionalIntelligenceWorkspace bundle={emptyBundle} signals={sampleSignals} />}
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

describe("UI-004-P02 advisory signal research integration", () => {
  it("test_ui004_signals_render_existing_records_read_only_with_guardrails", () => {
    render(<ResearchAdvisorySignalPanel signals={sampleSignals} />);

    const surface = screen.getByLabelText("Read-only advisory signal research surface");
    expect(surface).toHaveTextContent("fetchAdvisorySignals");
    expect(surface).toHaveTextContent("not financial advice");
    expect(surface).toHaveTextContent("not a trade instruction");
    expect(surface).toHaveTextContent("operator decides independently");
    expect(surface).toHaveTextContent("ELIGIBLE");
    expect(surface).toHaveTextContent("POORLY_CALIBRATED");
    expect(surface).toHaveTextContent("STALE_INPUT");
    expect(within(surface).getAllByText("Advisory").length).toBeGreaterThan(0);
    expect(within(surface).getAllByText("Warning").length).toBeGreaterThan(0);
    expect(within(surface).getAllByText("Withheld").length).toBeGreaterThan(0);
    expect(within(surface).getAllByText("Expired").length).toBeGreaterThan(0);
    expect(screen.getAllByText(/Read-only/).length).toBeGreaterThan(0);
  });

  it("test_ui004_signals_show_calibrated_confidence_not_raw_score", () => {
    render(<ResearchAdvisorySignalPanel signals={[signal({ calibrated_confidence: 0.42 })]} />);

    expect(screen.getAllByText("42.0% calibrated").length).toBeGreaterThan(0);
    expect(screen.getByLabelText("Stored calibrated confidence")).toHaveTextContent("calibrated");
    expect(screen.queryByText("0.987654")).not.toBeInTheDocument();
    expect(screen.queryByText(/raw score/i)).not.toBeInTheDocument();
  });

  it("test_ui004_signals_and_analytics_do_not_recompute_or_cherry_pick", async () => {
    render(<ResearchAdvisorySignalPanel signals={sampleSignals} />);

    const cards = screen.getByLabelText("Read-only advisory signal cards");
    expect(within(cards).getAllByText("Advisory").length).toBeGreaterThan(0);
    expect(within(cards).getAllByText("Warning").length).toBeGreaterThan(0);
    expect(within(cards).getAllByText("Withheld").length).toBeGreaterThan(0);
    expect(within(cards).getAllByText("Expired").length).toBeGreaterThan(0);
    expect(cards).toHaveTextContent("fresh");
    expect(cards).toHaveTextContent("stale");
    expect(cards).toHaveTextContent("expired");

    const sourceText = await readProductionSource("pages/InstitutionalIntelligencePage.tsx");
    expect(sourceText).toContain("fetchAdvisorySignals");
    expect(sourceText).not.toContain("inferSignal");
    expect(sourceText).not.toContain("emitSignal");
    expect(sourceText).not.toContain("deriveConfidence");
    expect(sourceText).toContain("fetchAdvisoryAnalytics");
  });

  it("test_ui004_signal_surfaces_contain_no_execution_order_or_gate_path", async () => {
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

  it("test_ui004_signal_analytics_accessibility_and_brand_markers_hold", () => {
    renderShell();

    expect(screen.getByText(/AXIOM Institutional Workstation/i)).toBeInTheDocument();
    expect(screen.getAllByText("Gate CLOSED").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("Research-only").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByLabelText("Advisory signal posture")).toHaveTextContent("Calibrated confidence");
    expect(screen.getByLabelText("Read-only advisory signal cards")).toBeInTheDocument();
    expect(screen.getByLabelText("Selected advisory signal stored detail")).toBeInTheDocument();
    expect(screen.getByLabelText("Read-only signal context navigation")).toBeInTheDocument();
    expect(screen.getAllByText("Open advisory signal workspace").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("Open investigation workspace")).toHaveLength(1);
    expect(screen.getByLabelText("Selected advisory signal stored detail").querySelectorAll(".mono").length).toBeGreaterThan(5);
  });
});
