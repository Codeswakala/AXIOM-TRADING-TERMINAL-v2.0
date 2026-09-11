import { render, screen, waitFor, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { TerminalProvider } from "../../components/terminal/TerminalContext";
import { TerminalSignalStream } from "../../components/terminal/TerminalSignalStream";
import type { AdvisorySignal, InstitutionalIntelligenceBundle, InstitutionalReport } from "../../api/client";
import * as client from "../../api/client";

// UI-CONV-P03 item 6: re-pointed from SignalInvestigationPage (deleted). The
// investigation surface was absorbed into the terminal signal drill-down;
// renderInvestigation now expands the dock card at the new home. The three
// assertion re-targets below are documented inline:
//   (a) evidence links now navigate in-app to post-absorption destinations
//       (M5 / OBS-CONV3-10: /?view=chart, /?dock=signals, /?dock=intelligence);
//   (b) calibrated confidence renders through the canonical
//       CalibratedConfidenceBadge (B-CONV2-1) instead of the retired
//       formatConfidence string;
//   (c) raw-source greps read the new drill-down module.

vi.mock("../../api/client", async () => {
  const actual = await vi.importActual<typeof client>("../../api/client");
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
    signal_id: "sig-ui005-p02",
    created_at: "2026-07-24T08:00:00Z",
    as_of_time: "2026-07-24T07:59:00Z",
    market_class: "forex",
    provider: "internal",
    symbol: "EURUSD",
    timeframe: "M1",
    model_artifact_id: "model-ui005-p02",
    model_version: "model.v1",
    feature_set_version: "features.v1",
    experiment_id: "exp-ui005-p02",
    statistical_report_id: "stat-ui005-p02",
    calibration_report_id: "cal-ui005-p02",
    economic_report_id: "econ-ui005-p02",
    generalization_report_id: "gen-ui005-p02",
    inference_input_hash: "input-hash-ui005-p02",
    raw_score: 0.987654,
    calibrated_confidence: 0.5,
    input_staleness_seconds: 60,
    signal_validity_seconds: 300,
    expires_at: "2026-07-24T08:05:00Z",
    freshness_status: "fresh",
    signal_direction: "positive_bias",
    signal_state: "warning",
    state_reason: "POORLY_CALIBRATED",
    eligibility_reasons: ["stored_guardrail_warning"],
    operating_domain_status: "valid",
    calibration_status: "warning:POORLY_CALIBRATED",
    economic_verdict: "not_assessed",
    risk_notes: "research only",
    rationale: "Persisted signal rationale with stored lineage and guardrails.",
    explainability_summary: {
      confidence_source: "calibration_report_bins_or_base_rate",
      [blockedRawKey]: 0.987654,
    },
    state_transition_history: ["candidate", "eligible_checked", "warning"],
    audit_correlation_id: "corr-ui005-p02",
    ...overrides,
  };
}

function report(overrides: Partial<InstitutionalReport> = {}): InstitutionalReport {
  return {
    id: "report-ui005-p02",
    artifact_type: "signal_validation_report",
    method_version: "validation.v1",
    sample_count: 4,
    research_status: "research_only",
    report_hash: "hash-ui005-p02",
    limitations: ["research_only"],
    uncertainty: { method: "stored_interval", lower: 0.1, upper: 0.7, sample_count: 4 },
    ...overrides,
  };
}

const intelligence: InstitutionalIntelligenceBundle = {
  relation: [report({ id: "corr-ui005-p02", artifact_type: "correlation_report" })],
  context: [report({ id: "regime-ui005-p02", artifact_type: "regime_report" })],
  hypothetical: [report({ id: "scenario-ui005-p02", artifact_type: "scenario_report" })],
  risk: [report({ id: "risk-ui005-p02", artifact_type: "portfolio_risk_report" })],
  validation: [report({ id: "validation-ui005-p02", artifact_type: "signal_validation_report" })],
};

function renderInvestigation() {
  render(
    <MemoryRouter>
      <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
        <TerminalSignalStream />
      </TerminalProvider>
    </MemoryRouter>,
  );
}

async function renderInvestigationExpanded() {
  renderInvestigation();
  await waitFor(() => expect(screen.getByTestId("signal-card-sig-ui005-p02")).toBeInTheDocument());
  screen.getByTestId("signal-card-sig-ui005-p02").click();
  await waitFor(() => expect(screen.getByTestId("signal-expanded-sig-ui005-p02")).toBeInTheDocument());
}

beforeEach(() => {
  vi.clearAllMocks();
  vi.mocked(client.fetchAdvisorySignals).mockResolvedValue([signal()]);
  vi.mocked(client.fetchInstitutionalIntelligenceBundle).mockResolvedValue(intelligence);
});

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

describe("UI-005-P02 signal investigation lineage and related evidence", () => {
  it("test_ui005_signal_investigation_renders_existing_signal_lineage_read_only", async () => {
    await renderInvestigationExpanded();

    const detail = screen.getByLabelText("Signal investigation detail");
    expect(detail).toHaveTextContent("sig-ui005-p02");
    expect(detail).toHaveTextContent("model-ui005-p02");
    expect(detail).toHaveTextContent("model.v1");
    expect(detail).toHaveTextContent("exp-ui005-p02");
    expect(detail).toHaveTextContent("features.v1");
    expect(detail).toHaveTextContent("input-hash-ui005-p02");
    expect(detail).toHaveTextContent("Investigation reads persisted evidence only");
  });

  it("test_ui005_investigation_uses_stored_confidence_validation_and_economic_values_verbatim", async () => {
    await renderInvestigationExpanded();

    // Re-target (b): confidence renders through the canonical badge with an
    // uncertainty qualifier — never a bare number (B-CONV2-1, stronger invariant).
    const badge = screen.getByTestId("signal-confidence-sig-ui005-p02");
    expect(badge).toHaveTextContent("50.0%");
    expect(badge).toHaveTextContent("Uncertainty");
    expect(screen.queryByText("0.987654")).not.toBeInTheDocument();
    expect(screen.getAllByText("warning:POORLY_CALIBRATED").length).toBeGreaterThan(0);
    expect(screen.getAllByText("not_assessed").length).toBeGreaterThan(0);
    expect(screen.getAllByText("POORLY_CALIBRATED").length).toBeGreaterThan(0);
    expect(screen.queryByText(/economically usable/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/approved/i)).not.toBeInTheDocument();
  });

  it("test_ui005_investigation_links_related_reports_without_recompute", async () => {
    await renderInvestigationExpanded();

    const links = screen.getByLabelText("Related investigation evidence links");
    // Re-target (a): in-app navigation to post-absorption destinations (M5).
    expect(within(links).getByText("Open intelligence report viewer")).toHaveAttribute("href", "/?dock=intelligence");
    expect(within(links).getByText("Open advisory signal record")).toHaveAttribute("href", "/?dock=signals");
    expect(within(links).getByText("Open chart context")).toHaveAttribute("href", "/?view=chart");
    expect(screen.getByText(/correlation report · corr-ui005-p02/)).toBeInTheDocument();
    expect(screen.getByText(/signal validation report · validation-ui005-p02/)).toBeInTheDocument();

    const sourceText = await readProductionSource("components/terminal/signals/SignalInvestigationRecords.tsx");
    expect(sourceText).not.toContain("inferSignal");
    expect(sourceText).not.toContain("runInference");
    expect(sourceText).not.toContain("authoritativeRecompute");
    expect(sourceText).not.toContain("emitSignal");
    expect(sourceText).not.toContain("generateSignal");
  });

  it("test_ui005_investigation_contains_no_signal_generation_or_actuation", async () => {
    // Reads the investigation content module: the stream file legitimately
    // contains direction-normalization vocabulary (BUY/SHORT) and a defensive
    // "Zero transaction execution affordance" disclaimer, which the broad
    // marketing grep would false-positive on. The stream's constitutional
    // no-mutation guarantee is enforced separately by the backend guard
    // (backend/tests/test_signal_investigation_workspace.py, re-pointed M3).
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
      "infersignal",
      "runinference",
      "emitsignal",
      "generatesignal",
    ];
    for (const marker of forbidden) {
      expect(sourceText).not.toContain(marker);
    }
  });

  it("test_ui005_investigation_accessibility_and_brand_markers_hold", async () => {
    await renderInvestigationExpanded();

    expect(screen.getByLabelText("Investigation and planning workspace frame")).toBeInTheDocument();
    expect(screen.getByLabelText("Investigation planning guardrail")).toHaveTextContent("Gate CLOSED");
    expect(screen.getByLabelText("Investigation planning guardrail")).toHaveTextContent("Research-only");
    expect(screen.getByLabelText("Signal investigation detail")).toBeInTheDocument();
    expect(screen.getByLabelText("Related investigation evidence links")).toBeInTheDocument();
    expect(screen.getByLabelText("Signal investigation detail").querySelectorAll(".mono").length).toBeGreaterThan(5);
    expect(screen.getByText("Research investigation only.")).toBeInTheDocument();
  });
});
