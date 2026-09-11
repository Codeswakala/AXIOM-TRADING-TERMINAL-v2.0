import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import {
  CHART_ANNOTATION_UI_DISCLAIMER,
  ChartResearchAnnotationLayer,
} from "./ChartWorkspaceSurface";
import type { ChartResearchAnnotation } from "../../api/client";

function annotation(overrides: Partial<ChartResearchAnnotation> = {}): ChartResearchAnnotation {
  return {
    id: "ann-1",
    created_at: "2026-07-17T10:00:00Z",
    operator_id: "operator",
    artifact_type: "chart_research_annotation",
    chart_context: { symbol: "EURUSD", timeframe: "M1" },
    content: {
      drawing_kind: "research_note",
      text: "Guardrail context note linked to governed advisory evidence.",
      visual: { x_percent: 20, y_percent: 25 },
      raw_score: 0.987654,
    },
    source_artifact_ids: ["signal-1", "report-1"],
    provenance: { presentation_only: true, ai_assisted: false },
    uncertainty: { method: "not_applicable_operator_markup" },
    disclaimer: CHART_ANNOTATION_UI_DISCLAIMER,
    research_status: "research_only",
    audit_correlation_id: "corr-1",
    ...overrides,
  };
}

describe("ChartResearchAnnotationLayer", () => {
  it("renders persisted annotations on the chart with sources and research status", () => {
    render(<ChartResearchAnnotationLayer annotations={[annotation()]} />);

    const layer = screen.getByLabelText("Chart research annotations layer");
    expect(within(layer).getByText("research note")).toBeInTheDocument();
    expect(within(layer).getByText(/Guardrail context note/)).toBeInTheDocument();
    expect(within(layer).getByText(/signal-1, report-1/)).toBeInTheDocument();
    expect(within(layer).getByText(/research_only/)).toBeInTheDocument();
  });

  it("does not render raw score or guaranteed-outcome fields from annotation content", () => {
    render(
      <ChartResearchAnnotationLayer
        annotations={[
          annotation({
            content: {
              drawing_kind: "research_zone",
              text: "Operator-marked research zone for later review only.",
              raw_score: 0.987654,
              guaranteed_outcome: "blocked",
            },
          }),
        ]}
      />,
    );

    const layer = screen.getByLabelText("Chart research annotations layer");
    expect(within(layer).queryByText("0.987654")).not.toBeInTheDocument();
    expect(within(layer).queryByText(/raw_score/i)).not.toBeInTheDocument();
    expect(within(layer).queryByText(/guaranteed/i)).not.toBeInTheDocument();
  });

  it("does not render execution, order, broker, account, or position controls", () => {
    render(<ChartResearchAnnotationLayer annotations={[annotation()]} />);
    expect(screen.queryAllByRole("button")).toHaveLength(0);
    const text = screen.getByLabelText("Chart research annotations layer").textContent?.toLowerCase() ?? "";
    const forbidden = ["b" + "uy", "s" + "ell", "or" + "der", "br" + "oker", "acc" + "ount", "pos" + "ition"];
    for (const word of forbidden) {
      expect(text).not.toContain(word);
    }
  });

  it("shows empty-state copy without client-side analytics or signal recompute", () => {
    render(<ChartResearchAnnotationLayer annotations={[]} />);
    expect(screen.getByText(/No chart research annotations yet/i)).toBeInTheDocument();
    const text = screen.getByLabelText("Chart research annotations layer").textContent?.toLowerCase() ?? "";
    expect(text).not.toContain("inference");
    expect(text).not.toContain("analytics recompute");
    expect(text).not.toContain("emit signal");
  });
});
