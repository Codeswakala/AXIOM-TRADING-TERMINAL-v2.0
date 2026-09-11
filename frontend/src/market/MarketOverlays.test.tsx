import { fireEvent, render, screen, within } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import {
  CHART_ANNOTATION_UI_DISCLAIMER,
  ChartOverlayControls,
  ChartResearchAnnotationLayer,
  ChartResearchMarkerLayer,
  ChartResearchMarkerList,
} from "../components/chart/ChartWorkspaceSurface";
import type { AdvisorySignal, ChartResearchAnnotation } from "../api/client";

function annotation(overrides: Partial<ChartResearchAnnotation> = {}): ChartResearchAnnotation {
  return {
    id: "ann-1",
    created_at: "2026-07-22T10:00:00Z",
    operator_id: "operator",
    artifact_type: "chart_research_annotation",
    chart_context: { symbol: "EURUSD", timeframe: "M1" },
    content: {
      drawing_kind: "research_note",
      text: "Existing governed chart annotation for market context.",
      visual: { x_percent: 22, y_percent: 28 },
      raw_score: 0.9876,
    },
    source_artifact_ids: ["signal-1", "report-1"],
    provenance: { presentation_only: true, ai_assisted: false },
    uncertainty: { method: "operator_markup" },
    disclaimer: CHART_ANNOTATION_UI_DISCLAIMER,
    research_status: "research_only",
    audit_correlation_id: "corr-1",
    ...overrides,
  };
}

function signal(overrides: Partial<AdvisorySignal> = {}): AdvisorySignal {
  return {
    signal_id: "sig-1",
    created_at: "2026-07-22T10:00:00Z",
    as_of_time: "2026-07-22T09:59:00Z",
    market_class: "forex",
    provider: "internal",
    symbol: "EURUSD",
    timeframe: "M1",
    model_artifact_id: "model-1",
    model_version: "1-42",
    feature_set_version: "features-v1",
    experiment_id: "exp-1",
    statistical_report_id: "stat-1",
    calibration_report_id: "cal-1",
    economic_report_id: "econ-1",
    generalization_report_id: "gen-1",
    inference_input_hash: "hash-1",
    raw_score: 0.1234,
    calibrated_confidence: 0.5,
    input_staleness_seconds: 60,
    signal_validity_seconds: 300,
    expires_at: "2026-07-22T10:05:00Z",
    freshness_status: "fresh",
    signal_direction: "positive_bias",
    signal_state: "warning",
    state_reason: "POORLY_CALIBRATED",
    eligibility_reasons: [],
    operating_domain_status: "valid",
    calibration_status: "warning:POORLY_CALIBRATED",
    economic_verdict: "research_only",
    risk_notes: null,
    rationale: "Existing advisory context for chart marker.",
    explainability_summary: {},
    state_transition_history: ["candidate", "warning"],
    audit_correlation_id: "corr-1",
    ...overrides,
  };
}

async function readRawSource(pathSuffix: string): Promise<string> {
  const modules = import.meta.glob("../**/*.{ts,tsx}", {
    query: "?raw",
    import: "default",
  });
  const parts = pathSuffix.split("/");
  const fileName = parts[parts.length - 1] ?? pathSuffix;
  const entry = Object.entries(modules).find(
    ([path]) => path.endsWith(pathSuffix) || path.endsWith(fileName),
  );
  if (!entry) throw new Error(`Raw source not found: ${pathSuffix}`);
  return (entry[1] as () => Promise<string>)();
}

describe("UI-003-P03 chart overlays and research markers", () => {
  it("test_ui003_overlays_render_existing_annotations_read_only", () => {
    render(<ChartResearchAnnotationLayer annotations={[annotation()]} />);
    const layer = screen.getByLabelText("Chart research annotations layer");
    expect(within(layer).getByText(/Existing governed chart annotation/)).toBeInTheDocument();
    expect(within(layer).getByText(/signal-1, report-1/)).toBeInTheDocument();
    expect(within(layer).getByText(/research_only/)).toBeInTheDocument();
    expect(within(layer).queryByText(/raw_score/i)).not.toBeInTheDocument();
    expect(within(layer).queryAllByRole("button")).toHaveLength(0);
  });

  it("test_ui003_research_markers_use_existing_read_artifacts_no_inference", async () => {
    render(<ChartResearchMarkerLayer signals={[signal()]} visible />);
    const layer = screen.getByLabelText("Read-only chart research markers layer");
    const marker = within(layer).getByLabelText("Read-only research marker 1");
    expect(marker).toHaveAttribute("data-readonly", "true");
    expect(marker).toHaveTextContent("Existing advisory record");
    expect(marker).toHaveTextContent("EURUSD");

    const sourceText = await readRawSource("components/chart/ChartWorkspaceSurface.tsx");
    expect(sourceText).toContain("fetchAdvisorySignals");
    expect(sourceText).not.toContain("inferSignal");
    expect(sourceText).not.toContain("runInference");
    expect(sourceText).not.toContain("authoritativeRecompute");
    expect(sourceText).not.toContain("emitSignal");
  });

  it("test_ui003_overlay_controls_are_presentation_toggles_only", () => {
    const onToggle = vi.fn();
    render(
      <ChartOverlayControls
        visibility={{ annotations: true, researchMarkers: true, sourceProvenance: true }}
        onToggle={onToggle}
      />,
    );
    const controls = screen.getByLabelText("Chart overlay presentation controls");
    expect(controls).toHaveTextContent("Presentation toggles only");
    fireEvent.click(screen.getByRole("button", { name: /Show annotations/i }));
    fireEvent.click(screen.getByRole("button", { name: /Show research markers/i }));
    fireEvent.click(screen.getByRole("button", { name: /Show source provenance/i }));
    expect(onToggle).toHaveBeenCalledWith("annotations");
    expect(onToggle).toHaveBeenCalledWith("researchMarkers");
    expect(onToggle).toHaveBeenCalledWith("sourceProvenance");
  });

  it("test_ui003_markers_preserve_provenance_uncertainty_and_research_only_labels", () => {
    render(<ChartResearchMarkerList signals={[signal()]} visible />);
    const list = screen.getByLabelText("Read-only research marker list");
    expect(list).toHaveTextContent("Existing advisory records shown as inert research context");
    expect(list).toHaveTextContent("Provenance: existing advisory record sig-1");
    expect(list).toHaveTextContent("Lineage: exp-1 · model-1");
    expect(list).toHaveTextContent("Uncertainty: 50.0% calibrated");
    expect(list).toHaveTextContent("Research-only marker");
    expect(within(list).queryAllByRole("button")).toHaveLength(0);
  });

  it("test_ui003_overlays_contain_no_signal_generation_or_actuation", async () => {
    const sourceText = (await readRawSource("components/chart/ChartWorkspaceSurface.tsx")).toLowerCase();
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
      "emitsignal",
      "infersignal",
      "runinference",
    ];
    for (const marker of forbidden) {
      expect(sourceText).not.toContain(marker);
    }
  });
});
