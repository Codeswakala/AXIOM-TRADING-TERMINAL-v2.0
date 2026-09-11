import { render, screen, waitFor, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { TerminalProvider } from "../TerminalContext";
import { TerminalSignalStream } from "../TerminalSignalStream";
import type {
  AdvisorySignal,
  InstitutionalIntelligenceBundle,
  InstitutionalReport,
} from "../../../api/client";
import * as client from "../../../api/client";

// Re-located from pages/SignalInvestigationPage.test.tsx (deleted with the page
// under UI-CONV-P03 item 6). The workspace component was absorbed into the
// terminal signal drill-down; the same guarantees are asserted at the new home.
// Re-targets vs the original are documented inline where the old chrome no
// longer exists (dock headings carry colons; calibrated confidence renders
// through the single canonical CalibratedConfidenceBadge per B-CONV2-1).

vi.mock("../../../api/client", async () => {
  const actual = await vi.importActual<typeof client>("../../../api/client");
  return {
    ...actual,
    fetchAdvisorySignals: vi.fn(),
    fetchSignalValidationReports: vi.fn().mockResolvedValue([]),
    fetchInstitutionalIntelligenceBundle: vi.fn(),
  };
});

function signal(overrides: Partial<AdvisorySignal> = {}): AdvisorySignal {
  const blockedRawKey = `raw_${"score"}`;
  return {
    signal_id: "sig-1",
    created_at: "2026-07-17T10:00:00Z",
    as_of_time: "2026-07-17T09:59:00Z",
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
    inference_input_hash: "input-hash-1",
    raw_score: 0.987654,
    calibrated_confidence: 0.5,
    input_staleness_seconds: 60,
    signal_validity_seconds: 300,
    expires_at: "2026-07-17T10:05:00Z",
    freshness_status: "fresh",
    signal_direction: "positive_bias",
    signal_state: "emitted",
    state_reason: "ELIGIBLE",
    eligibility_reasons: [],
    operating_domain_status: "valid",
    calibration_status: "calibrated",
    economic_verdict: "not_assessed",
    risk_notes: "research only",
    rationale: "Governed rationale with complete lineage and calibrated confidence.",
    explainability_summary: {
      confidence_source: "calibration_report_bins_or_base_rate",
      [blockedRawKey]: 0.987654,
    },
    state_transition_history: ["candidate", "eligible_checked", "emitted"],
    audit_correlation_id: "corr-1",
    ...overrides,
  };
}

function report(overrides: Partial<InstitutionalReport> = {}): InstitutionalReport {
  return {
    id: "report-1",
    artifact_type: "signal_validation_report",
    sample_count: 4,
    research_status: "research_only",
    limitations: ["research_only"],
    ...overrides,
  };
}

const intelligence: InstitutionalIntelligenceBundle = {
  relation: [report({ id: "corr-1", artifact_type: "correlation_report" })],
  context: [report({ id: "regime-1", artifact_type: "regime_report" })],
  hypothetical: [report({ id: "scenario-1", artifact_type: "scenario_report" })],
  risk: [report({ id: "risk-1", artifact_type: "portfolio_risk_report" })],
  validation: [report({ id: "validation-1", artifact_type: "signal_validation_report" })],
};

function renderDrilldown() {
  return render(
    <MemoryRouter>
      <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
        <TerminalSignalStream />
      </TerminalProvider>
    </MemoryRouter>,
  );
}

beforeEach(() => {
  vi.clearAllMocks();
  vi.mocked(client.fetchAdvisorySignals).mockResolvedValue([signal()]);
  vi.mocked(client.fetchInstitutionalIntelligenceBundle).mockResolvedValue(intelligence);
});

describe("SignalInvestigationDrilldown (UI-CONV-P03 item 6 — absorbed investigation surface)", () => {
  it("renders rationale, guardrails, lineage, and linked intelligence reports", async () => {
    renderDrilldown();

    await waitFor(() => expect(screen.getByTestId("signal-card-sig-1")).toBeInTheDocument());
    screen.getByTestId("signal-card-sig-1").click();

    await waitFor(() => {
      expect(screen.getByTestId("signal-expanded-sig-1")).toBeInTheDocument();
    });

    expect(screen.getByText("Signal Investigation Workspace")).toBeInTheDocument();
    expect(screen.getByText(/Governed rationale/)).toBeInTheDocument();
    expect(screen.getByText("Guardrails & State Criteria:")).toBeInTheDocument();
    expect(screen.getByText("valid")).toBeInTheDocument();
    expect(screen.getAllByText("calibrated").length).toBeGreaterThan(0);
    expect(screen.getByText("Model Lineage & Audit:")).toBeInTheDocument();
    expect(screen.getByText("model-1")).toBeInTheDocument();
    expect(screen.getByText("exp-1")).toBeInTheDocument();
    expect(screen.getByText(/Linked intelligence reports/)).toBeInTheDocument();
    expect(screen.getByText(/correlation report · corr-1/)).toBeInTheDocument();
    expect(screen.getByText(/signal validation report · validation-1/)).toBeInTheDocument();
  });

  it("shows calibrated confidence through the canonical badge and never renders raw model score", async () => {
    renderDrilldown();

    await waitFor(() => expect(screen.getByTestId("signal-card-sig-1")).toBeInTheDocument());
    screen.getByTestId("signal-card-sig-1").click();

    await waitFor(() => {
      // B-CONV2-1: confidence renders via the single canonical component with
      // uncertainty or an explicit unavailable qualifier — never a bare number.
      const badge = screen.getByTestId("signal-confidence-sig-1");
      expect(badge).toHaveTextContent("50.0%");
      expect(badge).toHaveTextContent("Uncertainty");
    });
    expect(screen.queryByText("0.987654")).not.toBeInTheDocument();
    expect(screen.queryByText(/raw score/i)).not.toBeInTheDocument();
  });

  it("renders research framing and no action controls", async () => {
    renderDrilldown();

    await waitFor(() => expect(screen.getByTestId("signal-card-sig-1")).toBeInTheDocument());
    screen.getByTestId("signal-card-sig-1").click();

    await waitFor(() => {
      expect(screen.getByText("Research investigation only.")).toBeInTheDocument();
      expect(screen.getByText(/AXIOM does not act/)).toBeInTheDocument();
    });
    // Re-target: the dock's interactive controls are the state-filter tabs
    // (role="tab"); the card is an inert presentation surface.
    const controls = screen.getAllByRole("tab");
    const text = controls.map((control) => control.textContent?.toLowerCase() ?? "").join(" ");
    const forbidden = ["b" + "uy", "s" + "ell", "or" + "der", "br" + "oker", "exec" + "ute", "pos" + "ition"];
    for (const word of forbidden) {
      expect(text).not.toContain(word);
    }
  });

  it("states presentation-only behavior without authoritative recompute", async () => {
    renderDrilldown();

    await waitFor(() => expect(screen.getByTestId("signal-card-sig-1")).toBeInTheDocument());
    screen.getByTestId("signal-card-sig-1").click();

    await waitFor(() => {
      const header = screen.getByText(/Read-only investigation/);
      expect(header).not.toBeNull();
      expect(header.textContent).toContain("no client-side inference");
      expect(header.textContent).toContain("no signal mutation");
      expect(header.textContent).toContain("no browser-side analytics rerun");
    });
  });

  it("keeps signal selectors read-only and scoped to persisted records", async () => {
    vi.mocked(client.fetchAdvisorySignals).mockResolvedValue([
      signal(),
      signal({ signal_id: "sig-2", signal_state: "warning", state_reason: "POORLY_CALIBRATED" }),
    ]);
    renderDrilldown();

    await waitFor(() => expect(screen.getByTestId("signal-card-sig-2")).toBeInTheDocument());
    screen.getByTestId("signal-card-sig-2").click();

    await waitFor(() => {
      expect(screen.getByTestId("signal-expanded-sig-2")).toBeInTheDocument();
    });
    // The warning signal's state rationale renders from the persisted record.
    expect(screen.getByText("POORLY_CALIBRATED")).toBeInTheDocument();
    expect(screen.getByTestId("signal-state-sig-2")).toHaveTextContent("WARNING");
  });

  it("item 6: renders linked validation and report ids with verbatim absence markers", async () => {
    vi.mocked(client.fetchAdvisorySignals).mockResolvedValue([
      signal({
        statistical_report_id: null,
        calibration_report_id: null,
        economic_report_id: null,
        generalization_report_id: null,
      }),
    ]);
    renderDrilldown();

    await waitFor(() => expect(screen.getByTestId("signal-card-sig-1")).toBeInTheDocument());
    screen.getByTestId("signal-card-sig-1").click();

    await waitFor(() => {
      const ids = screen.getByTestId("signal-detail-report-ids-sig-1");
      // M2: honest absence markers — never plausible-looking ids.
      expect(ids).toHaveTextContent("Statistical: —");
      expect(ids).toHaveTextContent("Calibration: —");
      expect(ids).toHaveTextContent("Economic: —");
      expect(ids).toHaveTextContent("Generalization: —");
    });
  });

  it("item 6: renders linked intelligence reports with the verbatim empty state", async () => {
    vi.mocked(client.fetchInstitutionalIntelligenceBundle).mockResolvedValue(null as never);
    renderDrilldown();

    await waitFor(() => expect(screen.getByTestId("signal-card-sig-1")).toBeInTheDocument());
    screen.getByTestId("signal-card-sig-1").click();

    await waitFor(() => {
      const section = screen.getByTestId("signal-detail-intelligence-sig-1");
      // M2: honest absence — "No reports returned." per empty group.
      expect(section).toHaveTextContent("No reports returned.");
    });
  });

  it("item 6: evidence links navigate in-app to post-absorption destinations (OBS-CONV3-10)", async () => {
    renderDrilldown();

    await waitFor(() => expect(screen.getByTestId("signal-card-sig-1")).toBeInTheDocument());
    screen.getByTestId("signal-card-sig-1").click();

    await waitFor(() => {
      const links = screen.getByLabelText("Related investigation evidence links");
      expect(within(links).getByText("Open intelligence report viewer")).toHaveAttribute("href", "/?dock=intelligence");
      expect(within(links).getByText("Open advisory signal record")).toHaveAttribute("href", "/?dock=signals");
      expect(within(links).getByText("Open chart context")).toHaveAttribute("href", "/?view=chart");
    });
  });
});
