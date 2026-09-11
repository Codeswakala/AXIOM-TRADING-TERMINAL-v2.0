/**
 * BO-F-05 — Lineage & Evidence Visualization (traceability across the terminal)
 *
 * Pins:
 *  1. Intelligence reports, signals, and alerts surface their persisted
 *     lineage fields (audit correlation, source ids, hashes) where present.
 *  2. The read-only lineage/evidence view renders PERSISTED-ONLY nodes —
 *     the illustrative default chain (market→features→model→report) is
 *     never fabricated for real artifacts; sources are typed with the
 *     honest neutral `source_artifact` role.
 *  3. Absent lineage renders as "provenance not recorded" — never invented.
 *  4. Read-only: the only control is the expand toggle; no mutation.
 *  5. Scope discipline: presentation-only values (counts, tabs) carry no
 *     lineage labeling.
 */

import { describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import {
  buildPersistedLineageNodes,
  LineageEvidencePanel,
} from "../components/terminal/LineageEvidencePanel";
import { TerminalIntelligenceCards } from "../components/terminal/TerminalIntelligenceCards";
import { TerminalSignalStream } from "../components/terminal/TerminalSignalStream";
import { MonitoringAlertsPanel } from "../components/alerts/MonitoringAlertsPanel";
import { TerminalProvider } from "../components/terminal/TerminalContext";
import type {
  AdvisorySignal,
  CorrelationReport,
  MonitoringAlert,
} from "../api/client";
import * as client from "../api/client";

vi.mock("../api/client", async () => {
  const actual = await vi.importActual<typeof client>("../api/client");
  return {
    ...actual,
    fetchAdvisorySignals: vi.fn().mockResolvedValue([]),
    fetchSignalValidationReports: vi.fn().mockResolvedValue([]),
    fetchInstitutionalIntelligenceBundle: vi.fn().mockResolvedValue(null),
    fetchCorrelationReports: vi.fn().mockResolvedValue([]),
    fetchRegimeReports: vi.fn().mockResolvedValue([]),
    fetchScenarioReports: vi.fn().mockResolvedValue([]),
    fetchPortfolioRiskReports: vi.fn().mockResolvedValue([]),
    fetchCandles: vi.fn().mockResolvedValue({
      kind: "unavailable",
      timeframe: "M1",
      detail: "none",
      bars: [],
    }),
  };
});

vi.mock("../../hooks/useLiveMarket", () => ({
  useLiveMarket: () => ({ quotes: {}, stats: { running: false }, error: null }),
}));

const CORRELATION: CorrelationReport = {
  id: "corr-lineage-1",
  created_at: "2026-08-21T10:00:00Z",
  artifact_type: "correlation_report",
  method_version: "w4-u01.correlation.v1",
  left_market_class: "crypto",
  left_symbol: "BTCUSD",
  right_market_class: "crypto",
  right_symbol: "ETHUSD",
  timeframe: "H1",
  sample_count: 17520,
  correlation_value: 0.7321,
  uncertainty: { lower: 0.72, upper: 0.74 },
  significance: {},
  report_hash: "corr-real-hash-000000000000",
  research_status: "research_only",
  notes: "data-class: historical:real",
  source_artifact_ids: ["src-art-1", "src-art-2"],
  audit_correlation_id: "corr-audit-0001",
  created_by: "admin",
};

const CORRELATION_WITHOUT_LINEAGE: CorrelationReport = {
  ...CORRELATION,
  id: "corr-nolineage",
  source_artifact_ids: undefined,
  audit_correlation_id: undefined,
  created_by: undefined,
};

const SIGNAL: AdvisorySignal = {
  signal_id: "sig-lineage-1",
  created_at: "2026-08-21T09:00:00Z",
  as_of_time: "2026-08-21T08:55:00Z",
  market_class: "forex",
  provider: "internal",
  symbol: "EURUSD",
  timeframe: "M1",
  model_artifact_id: "model-art-1",
  model_version: "1.2.3",
  feature_set_version: "feature_set.v1",
  experiment_id: "exp-lineage-1",
  statistical_report_id: "stat-report-1",
  calibration_report_id: "calib-report-1",
  economic_report_id: "econ-report-1",
  generalization_report_id: "gen-report-1",
  inference_input_hash: "input-hash-abcdef0123456789",
  audit_correlation_id: "sig-audit-0001",
  calibrated_confidence: 0.51,
  raw_score: 0.5,
  input_staleness_seconds: 120,
  signal_validity_seconds: 3600,
  expires_at: null,
  freshness_status: "fresh",
  signal_direction: "neutral",
  signal_state: "emitted",
  state_reason: "reason",
  eligibility_reasons: [],
  operating_domain_status: "valid",
  calibration_status: "not_evaluated",
  economic_verdict: "not_evaluated",
  rationale: "research",
  explainability_summary: {},
  risk_notes: null,
  state_transition_history: [],
};

const ALERT: MonitoringAlert = {
  alert_id: "alert-lineage-1",
  created_at: "2026-08-21T08:00:00Z",
  alert_type: "DRIFT_DETECTED",
  severity: "warning",
  subject_type: "model_artifact",
  subject_id: "model-1",
  market_class: null,
  symbol: null,
  timeframe: null,
  model_artifact_id: "model-1",
  signal_id: null,
  summary: "drift",
  evidence: {},
  lineage: { source: "w2_u10_drift_monitoring_record" },
  acknowledged: false,
  acknowledged_at: null,
  acknowledged_by: null,
  audit_correlation_id: "alert-audit-0001",
};

describe("BO-F-05.2 — persisted-only lineage nodes (no fabricated chain)", () => {
  it("builds only the root artifact node plus real source nodes", () => {
    const nodes = buildPersistedLineageNodes({
      artifactId: "corr-1",
      artifactType: "correlation_report",
      reportHash: "hash-1",
      createdAt: "2026-08-21T10:00:00Z",
      researchStatus: "research_only",
      sourceArtifactIds: ["src-1", "src-2"],
    });
    expect(nodes).toHaveLength(3);
    expect(nodes[0]).toMatchObject({
      id: "corr-1",
      type: "report",
      hash: "hash-1",
      status: "research_only",
    });
    expect(nodes[1]).toMatchObject({ id: "src-1", type: "source_artifact" });
    expect(nodes[2]).toMatchObject({ id: "src-2", type: "source_artifact" });
    // The illustrative default chain nodes are NEVER built here.
    for (const node of nodes) {
      expect(["market_input", "feature_set", "model", "assistant_explanation"]).not.toContain(
        node.type,
      );
    }
  });

  it("renders the persisted-only tree: root + sources, real hash, no invented roles", () => {
    render(
      <LineageEvidencePanel
        artifactId="corr-1"
        artifactType="correlation_report"
        reportHash="corr-real-hash-000000000000"
        createdAt="2026-08-21T10:00:00Z"
        researchStatus="research_only"
        sourceArtifactIds={["src-1"]}
        auditCorrelationId="audit-1"
        createdBy="admin"
      />,
    );
    expect(screen.getByTestId("lineage-evidence-panel")).toBeInTheDocument();
    expect(screen.getByTestId("lineage-report-hash")).toHaveTextContent("corr-real-hash-0");
    expect(screen.getByTestId("lineage-audit-correlation")).toHaveTextContent("audit-1");
    expect(screen.getByText("Source artifact")).toBeInTheDocument();
    expect(screen.queryByText("Market Data Series")).not.toBeInTheDocument();
    expect(screen.queryByText("Feature Set Engine")).not.toBeInTheDocument();
    expect(screen.queryByText("Grounded Model Registry")).not.toBeInTheDocument();
    expect(screen.queryByText("Assistant Research Explanation")).not.toBeInTheDocument();
  });
});

describe("BO-F-05.2 — source render cap (honest, disclosed)", () => {
  it("caps rendered source nodes at the limit and discloses the count", () => {
    const manySources = Array.from({ length: 200 }, (_, i) => `bar-source-${i}`);
    render(
      <LineageEvidencePanel
        artifactId="capped-1"
        artifactType="correlation_report"
        reportHash="hash-capped"
        createdAt="2026-08-21T10:00:00Z"
        sourceArtifactIds={manySources}
      />,
    );
    expect(screen.getAllByText("Source artifact")).toHaveLength(12);
    expect(screen.getByTestId("lineage-source-cap-note")).toHaveTextContent(
      "200 source artifacts recorded; showing the first 12",
    );
  });
});

describe("BO-F-05.4 — honest absence", () => {
  it("renders 'provenance not recorded' for every absent lineage field", () => {
    render(
      <LineageEvidencePanel
        artifactId="bare-1"
        artifactType="regime_report"
        reportHash={null}
        createdAt={null}
        researchStatus={null}
        sourceArtifactIds={null}
        auditCorrelationId={null}
        createdBy={null}
      />,
    );
    expect(screen.getByTestId("lineage-report-hash")).toHaveTextContent(
      "provenance not recorded",
    );
    expect(screen.getByTestId("lineage-audit-correlation")).toHaveTextContent(
      "provenance not recorded",
    );
    expect(screen.getByTestId("lineage-not-recorded")).toBeInTheDocument();
  });
});

describe("BO-F-05.1/.2 — lineage on the intelligence cards", () => {
  beforeEach(() => {
    vi.mocked(client.fetchCorrelationReports).mockResolvedValue([CORRELATION] as never);
  });

  function renderCards() {
    return render(
      <TerminalProvider initialSymbol="BTC/USD" enableLiveMarket={false}>
        <TerminalIntelligenceCards />
      </TerminalProvider>,
    );
  }

  it("the per-report Lineage toggle opens the read-only evidence panel with persisted fields", async () => {
    renderCards();
    const tab = screen.getByTestId("intel-tab-correlation");
    fireEvent.click(tab);
    await new Promise((resolve) => setTimeout(resolve, 0));
    const toggle = screen.getByTestId("lineage-toggle-corr-lineage-1");
    expect(toggle).toBeInTheDocument();
    expect(toggle).toHaveAttribute("aria-expanded", "false");
    fireEvent.click(toggle);
    expect(screen.getByTestId("lineage-evidence-panel")).toBeInTheDocument();
    expect(screen.getByTestId("lineage-audit-correlation")).toHaveTextContent("corr-audit-0001");
    expect(screen.getByTestId("lineage-report-hash")).toHaveTextContent("corr-real-hash-0");
    // Both persisted sources appear as neutral source nodes.
    expect(screen.getAllByText("Source artifact")).toHaveLength(2);
    // Read-only: the ONLY control inside the panel surface is the toggle.
    const panelControls = screen
      .getByTestId("lineage-evidence-panel")
      .querySelectorAll("button, input, select, a");
    expect(panelControls).toHaveLength(0);
  });

  it("a report without persisted lineage shows the honest not-recorded state", async () => {
    vi.mocked(client.fetchCorrelationReports).mockResolvedValue([
      CORRELATION_WITHOUT_LINEAGE,
    ] as never);
    renderCards();
    fireEvent.click(screen.getByTestId("intel-tab-correlation"));
    await new Promise((resolve) => setTimeout(resolve, 0));
    fireEvent.click(screen.getByTestId("lineage-toggle-corr-nolineage"));
    expect(screen.getByTestId("lineage-audit-correlation")).toHaveTextContent(
      "provenance not recorded",
    );
    // The banner intentionally does NOT render: created_at is real evidence.
    expect(screen.queryByTestId("lineage-not-recorded")).not.toBeInTheDocument();
  });
});

describe("BO-F-05.1 — signal lineage completion", () => {
  beforeEach(() => {
    vi.mocked(client.fetchAdvisorySignals).mockResolvedValue([SIGNAL] as never);
  });

  function renderStream() {
    return render(
      <MemoryRouter>
        <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
          <TerminalSignalStream />
        </TerminalProvider>
      </MemoryRouter>,
    );
  }

  it("the expanded lineage section surfaces all three report ids + audit correlation; nothing fabricated", async () => {
    renderStream();
    const card = await screen.findByTestId("signal-card-sig-lineage-1");
    fireEvent.click(card);
    const lineage = screen.getByTestId("signal-detail-lineage-sig-lineage-1");
    expect(lineage).toHaveTextContent("stat-report-1");
    expect(lineage).toHaveTextContent("econ-report-1");
    expect(lineage).toHaveTextContent("gen-report-1");
    expect(lineage).toHaveTextContent("sig-audit-0001");
    expect(lineage).toHaveTextContent("exp-lineage-1");
    // The pre-F-05 fabricated fallback is gone.
    expect(lineage).not.toHaveTextContent("exp-001");
  });
});

describe("BO-F-05.1 — alert lineage completion", () => {
  it("the alert card and detail record surface the audit correlation", () => {
    render(
      <MonitoringAlertsPanel alerts={[ALERT]} detailAlert={ALERT} />,
    );
    expect(screen.getByTestId("alert-audit-alert-lineage-1")).toHaveTextContent(
      "Audit: alert-audit-0001",
    );
    expect(screen.getByTestId("alerts-detail-audit")).toHaveTextContent("alert-audit-0001");
  });

  it("absent audit correlation renders as provenance not recorded", () => {
    const bareAlert = { ...ALERT, alert_id: "bare-alert", audit_correlation_id: "" };
    render(<MonitoringAlertsPanel alerts={[bareAlert]} />);
    expect(screen.getByTestId("alert-audit-bare-alert")).toHaveTextContent(
      "provenance not recorded",
    );
  });
});

describe("BO-F-05.3 — scope discipline (presentation-only values not over-labeled)", () => {
  it("presentation-only elements carry no lineage controls", async () => {
    vi.mocked(client.fetchCorrelationReports).mockResolvedValue([CORRELATION] as never);
    render(
      <TerminalProvider initialSymbol="BTC/USD" enableLiveMarket={false}>
        <TerminalIntelligenceCards />
      </TerminalProvider>,
    );
    await new Promise((resolve) => setTimeout(resolve, 0));
    // The intelligence TAB BAR (presentation navigation) has no lineage
    // toggle inside it; the count badges are plain counters.
    const tabBar = screen
      .getByTestId("intel-tab-correlation")
      .closest('[role="tablist"]') as HTMLElement;
    expect(tabBar.querySelectorAll("[data-testid^='lineage-']")).toHaveLength(0);
    expect(tabBar.textContent).not.toContain("provenance not recorded");
  });
});
