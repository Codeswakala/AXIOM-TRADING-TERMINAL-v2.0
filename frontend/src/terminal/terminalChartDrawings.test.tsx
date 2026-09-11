/**
 * CHART-P03 fail-first frontend tests — drawing tools (M1/M2/M5/M6),
 * annotation surfacing (M3), legacy percentage honesty (M4), and the
 * Market-Structure naming guard (M10).
 *
 * Every test here MUST fail against the pre-CHART-P03 tree and pass once the
 * phase ships: the drawing palette, the overlay, the PATCH/DELETE client
 * functions, the geometry-typed persistence and the structure engine do not
 * exist yet.
 */
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { TerminalProvider } from "../components/terminal/TerminalContext";
import { TerminalChartStage } from "../components/terminal/TerminalChartStage";
import * as client from "../api/client";
import { INDICATOR_UI, engineOf } from "../api/indicatorRegistry";
import { DRAWING_TOOLS, drawingToolOf } from "../api/drawingTools";

vi.mock("../api/client", async () => {
  const actual = await vi.importActual<typeof client>("../api/client");
  return {
    ...actual,
    fetchCandles: vi.fn(),
    fetchIndicatorSeries: vi.fn(),
    fetchChartResearchAnnotations: vi.fn(),
    createChartResearchAnnotation: vi.fn(),
    updateChartResearchAnnotation: vi.fn(),
    deleteChartResearchAnnotation: vi.fn(),
    seedChartHistory: vi.fn(),
  };
});

/** The mock PriceChart exposes the coordinate bridge deterministically:
 * time(x) = BASE + x*60, price(y) = 1.1 + y*0.001 — so test clicks map to
 * known (price, time) handles. Drawings render as data attributes. */
vi.mock("../components/chart/PriceChart", () => ({
  PriceChart: ({
    bars,
    overlayLines,
    drawings,
    onCoordinateApiReady,
    selectedDrawingId,
  }: {
    bars: unknown[];
    overlayLines?: unknown[];
    drawings?: Array<{ id: string; kind: string; handles: Array<{ price: number; time: number }>; label?: string }>;
    onCoordinateApiReady?: (api: {
      coordinateToTime: (x: number) => number;
      coordinateToPrice: (y: number) => number;
      timeToCoordinate: (t: number) => number;
      priceToCoordinate: (p: number) => number;
    } | null) => void;
    selectedDrawingId?: string | null;
  }) => {
    const api = {
      coordinateToTime: (x: number) => 1_700_000_000 + x * 60,
      coordinateToPrice: (y: number) => 1.1 + y * 0.001,
      timeToCoordinate: (t: number) => (t - 1_700_000_000) / 60,
      priceToCoordinate: (p: number) => (p - 1.1) / 0.001,
    };
    const callApi = () => onCoordinateApiReady?.(api);
    return (
      <div>
        <button data-testid="mock-coordinate-bridge" onClick={callApi}>
          bridge
        </button>
        <div
          data-testid="mock-price-chart"
          data-bars-count={bars.length}
          data-overlay-lines={(overlayLines ?? []).length}
          data-drawings={(drawings ?? []).length}
          data-drawing-ids={(drawings ?? []).map((d) => d.id).join(",")}
          data-selected-drawing={selectedDrawingId ?? ""}
          data-drawing-handles={JSON.stringify((drawings ?? []).map((d) => d.handles))}
        />
      </div>
    );
  },
}));

vi.mock("../components/terminal/IndicatorPane", () => ({
  IndicatorPane: ({ testid }: { testid: string }) => <div data-testid={testid} />,
}));

const candle = (minute: number, close = "1.10000"): client.ApiCandle => ({
  id: `c${minute}`,
  market_class: "forex",
  symbol: "EURUSD",
  timeframe: "M1",
  open_time: new Date(Date.UTC(2026, 7, 17, 10, minute)).toISOString(),
  open: "1.10000",
  high: "1.10500",
  low: "1.09900",
  close,
  volume: "100",
  source: "seed:synthetic",
  created_at: new Date(Date.UTC(2026, 7, 17, 10, minute)).toISOString(),
});

const renderStage = () =>
  render(
    <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
      <TerminalChartStage />
    </TerminalProvider>,
  );

const clickChartAt = (container: HTMLElement, x: number, y: number) => {
  const canvas = container.querySelector('[data-testid="chart-canvas-container"]');
  fireEvent.click(canvas as HTMLElement, { clientX: x, clientY: y });
};

let savedAnnotations: client.ChartResearchAnnotation[] = [];

beforeEach(() => {
  vi.clearAllMocks();
  savedAnnotations = [];
  vi.mocked(client.fetchCandles).mockResolvedValue({
    kind: "native",
    timeframe: "M1",
    bars: Array.from({ length: 30 }, (_, i) => candle(i)),
  });
  vi.mocked(client.fetchChartResearchAnnotations).mockImplementation(async () => [
    ...savedAnnotations,
  ]);
  vi.mocked(client.fetchIndicatorSeries).mockResolvedValue({
    symbol: "EURUSD",
    timeframe: "M1",
    seriesKind: "native",
    sourceTimeframe: null,
    excludedPartialBuckets: null,
    detail: null,
    indicators: {},
  });
  vi.mocked(client.createChartResearchAnnotation).mockImplementation(async (payload) => {
    const created: client.ChartResearchAnnotation = {
      id: `d-${Math.random().toString(36).slice(2, 8)}`,
      created_at: new Date().toISOString(),
      operator_id: "admin",
      artifact_type: payload.artifact_type ?? "chart_research_annotation",
      chart_context: payload.chart_context,
      content: payload.content,
      source_artifact_ids: payload.source_artifact_ids,
      provenance: {},
      uncertainty: {},
      disclaimer: "Inert research markup",
      research_status: "research_only",
      audit_correlation_id: "audit-1",
    };
    savedAnnotations.push(created);
    return created;
  });
});

describe("CHART-P03 S1 — drawing palette", () => {
  it("test_chart_p03_drawing_tools_registry_and_palette", () => {
    expect(DRAWING_TOOLS.map((t) => t.id)).toEqual([
      "trendline",
      "hline",
      "ray",
      "rect",
      "fib",
      "text",
    ]);
    expect(drawingToolOf("fib")?.label).toBe("Fibonacci");
    renderStage();
    for (const tool of DRAWING_TOOLS) {
      expect(screen.getByTestId(`drawing-tool-${tool.id}`)).toBeInTheDocument();
    }
  });
});

describe("CHART-P03 M1/M2 — drawings anchor to price and time, not pixels", () => {
  it("test_chart_p03_drawing_anchors_persist_as_price_and_time_not_pixels", async () => {
    const { container } = renderStage();
    await waitFor(() => expect(screen.getByTestId("mock-price-chart")).toBeInTheDocument());
    // Activate the coordinate bridge (the mock PriceChart's API).
    fireEvent.click(screen.getByTestId("mock-coordinate-bridge"));
    fireEvent.click(screen.getByTestId("drawing-tool-trendline"));
    // Two clicks: (100, 200) and (160, 230) relative to the canvas — the
    // stage converts via the bridge; the mock bridge maps x->time, y->price.
    clickChartAt(container, 100, 200);
    clickChartAt(container, 160, 230);
    await waitFor(() =>
      expect(client.createChartResearchAnnotation).toHaveBeenCalledTimes(1),
    );
    const payload = vi.mocked(client.createChartResearchAnnotation).mock.calls[0][0];
    expect(payload.artifact_type).toBe("chart_research_drawing");
    const geometry = payload.content.geometry as {
      kind: string;
      handles: Array<{ price: number; time_iso: string }>;
    };
    expect(geometry.kind).toBe("trendline");
    expect(geometry.handles).toHaveLength(2);
    // price = 1.1 + y*0.001 ; time = 1_700_000_000 + x*60
    expect(geometry.handles[0].price).toBeCloseTo(1.1 + 200 * 0.001, 9);
    expect(geometry.handles[0].time_iso).toBe(new Date((1_700_000_000 + 100 * 60) * 1000).toISOString());
    expect(geometry.handles[1].price).toBeCloseTo(1.1 + 230 * 0.001, 9);
    // No pixel or percentage coordinates anywhere in the payload.
    expect(JSON.stringify(payload)).not.toContain("pixel");
    expect(JSON.stringify(payload)).not.toContain("x_percent");
    expect(JSON.stringify(payload)).not.toContain("y_percent");
  });

  it("test_chart_p03_drawing_returns_to_same_anchors_after_timeframe_change", async () => {
    const { container } = renderStage();
    await waitFor(() => expect(screen.getByTestId("mock-price-chart")).toBeInTheDocument());
    fireEvent.click(screen.getByTestId("mock-coordinate-bridge"));
    fireEvent.click(screen.getByTestId("drawing-tool-hline"));
    clickChartAt(container, 120, 200);
    await waitFor(() =>
      expect(screen.getByTestId("mock-price-chart")).toHaveAttribute("data-drawings", "1"),
    );
    const handlesBefore = screen
      .getByTestId("mock-price-chart")
      .getAttribute("data-drawing-handles");
    // Timeframe round-trip: 1m -> 1h -> 1m.
    fireEvent.click(screen.getByTestId("chart-tf-1h"));
    await waitFor(() => expect(client.fetchCandles).toHaveBeenCalledWith(
      expect.objectContaining({ timeframe: "H1" }),
    ));
    fireEvent.click(screen.getByTestId("chart-tf-1m"));
    await waitFor(() => expect(client.fetchCandles).toHaveBeenCalledWith(
      expect.objectContaining({ timeframe: "M1" }),
    ));
    const handlesAfter = screen
      .getByTestId("mock-price-chart")
      .getAttribute("data-drawing-handles");
    expect(handlesAfter).toBe(handlesBefore);
    expect(handlesAfter).toContain("1.3"); // price 1.1 + 200*0.001 = 1.3
  });
});

describe("CHART-P03 M3/M4 — annotation surfacing and legacy honesty", () => {
  it("test_chart_p03_saved_annotations_render_on_chart", async () => {
    vi.mocked(client.fetchChartResearchAnnotations).mockResolvedValue([
      {
        id: "note-1",
        created_at: "2026-08-17T10:00:00Z",
        operator_id: "admin",
        artifact_type: "chart_research_annotation",
        chart_context: { symbol: "EURUSD", timeframe: "M1" },
        content: {
          note: "Key level",
          geometry: {
            kind: "text_note",
            handles: [{ price: 1.101, time_iso: "2026-08-17T10:05:00Z" }],
          },
        },
        source_artifact_ids: [],
        provenance: {},
        uncertainty: {},
        disclaimer: "Inert research markup",
        research_status: "research_only",
        audit_correlation_id: "a-1",
      },
    ]);
    renderStage();
    await waitFor(() =>
      expect(screen.getByTestId("mock-price-chart")).toHaveAttribute("data-drawings", "1"),
    );
    // The note's anchor is (price, time) — not a fabricated percentage.
    const handles = screen
      .getByTestId("mock-price-chart")
      .getAttribute("data-drawing-handles");
    expect(handles).toContain("1.101");
    expect(screen.getByTestId("chart-add-annotation-btn")).toHaveTextContent("(1)");
  });

  it("test_chart_p03_legacy_percentage_annotations_not_given_fabricated_anchors", async () => {
    vi.mocked(client.fetchChartResearchAnnotations).mockResolvedValue([
      {
        id: "legacy-1",
        created_at: "2026-08-17T10:00:00Z",
        operator_id: "admin",
        artifact_type: "chart_research_annotation",
        chart_context: { symbol: "EURUSD", timeframe: "M1" },
        content: {
          drawing_kind: "research_note",
          text: "legacy percent note",
          visual: { x_percent: 42, y_percent: 30 },
        },
        source_artifact_ids: [],
        provenance: {},
        uncertainty: {},
        disclaimer: "Inert research markup",
        research_status: "research_only",
        audit_correlation_id: "a-2",
      },
      {
        id: "legacy-2",
        created_at: "2026-08-17T10:00:00Z",
        operator_id: "admin",
        artifact_type: "chart_research_annotation",
        chart_context: { symbol: "EURUSD", timeframe: "M1" },
        content: { note: "price-only note", price_level: 1.085 },
        source_artifact_ids: [],
        provenance: {},
        uncertainty: {},
        disclaimer: "Inert research markup",
        research_status: "research_only",
        audit_correlation_id: "a-3",
      },
    ]);
    renderStage();
    await waitFor(() =>
      expect(screen.getByTestId("legacy-annotation-list")).toBeInTheDocument(),
    );
    // The percent note is listed as unanchored — never given chart position.
    expect(screen.getByTestId("legacy-annotation-list")).toHaveTextContent("legacy percent note");
    expect(screen.getByTestId("legacy-annotation-list")).toHaveTextContent(/unanchored/i);
    // The price-only note renders as a price-anchored marker (price is real;
    // time is unknown — stated, not invented).
    await waitFor(() =>
      expect(screen.getByTestId("mock-price-chart")).toHaveAttribute("data-drawings", "1"),
    );
    const handles = screen
      .getByTestId("mock-price-chart")
      .getAttribute("data-drawing-handles");
    expect(handles).toContain("1.085");
    expect(handles).not.toContain("42");
  });
});

describe("CHART-P03 M5 — drawing labels reject actuation terms", () => {
  it("test_chart_p03_drawing_labels_reject_actuation_terms", async () => {
    const { container } = renderStage();
    await waitFor(() => expect(screen.getByTestId("mock-price-chart")).toBeInTheDocument());
    fireEvent.click(screen.getByTestId("mock-coordinate-bridge"));
    // Use the text tool: opens the annotation dialog with an anchored price.
    fireEvent.click(screen.getByTestId("drawing-tool-text"));
    clickChartAt(container, 100, 200);
    await waitFor(() =>
      expect(screen.getByTestId("annotation-dialog")).toBeInTheDocument(),
    );
    const textarea = screen.getByTestId("annotation-text-input");
    fireEvent.change(textarea, { target: { value: "stop_loss at 1.08" } });
    fireEvent.click(screen.getByTestId("annotation-save-btn"));
    expect(screen.getByTestId("annotation-error-banner")).toHaveTextContent(
      "Forbidden actuation term 'stop_loss'",
    );
    expect(client.createChartResearchAnnotation).not.toHaveBeenCalled();
  });
});

describe("CHART-P03 M8/M10 — no institutional or directional language", () => {
  it("test_chart_p03_no_institutional_behaviour_claims_in_source", () => {
    const stageSource = readFileSync(
      join(process.cwd(), "src/components/terminal/TerminalChartStage.tsx"),
      "utf8",
    );
    const anchor = "describe data, they never advise a trade";
    expect(stageSource).toContain(anchor);
    const residue = stageSource.replace(anchor, "");
    const forbidden = [
      "institutional order",
      "smart money",
      "accumulation zone",
      "distribution zone",
      "entry zone",
      "golden pocket",
      "buy signal",
      "sell signal",
      "bullish",
      "bearish",
      "oversold",
      "overbought",
      "trade recommendation",
      "eligibility",
    ];
    for (const term of forbidden) {
      expect(residue).not.toContain(term);
    }
  });

  it("test_chart_p03_market_structure_registry_mirror", () => {
    const ids = INDICATOR_UI.map((i) => i.id);
    expect(ids).toContain("SWINGS55");
    expect(ids).toContain("STRUCT55");
    expect(ids).toContain("BOS55");
    expect(ids).toContain("CHOCH55");
    expect(ids).toContain("FVG3");
    expect(ids).toContain("OBPATTERN");
    for (const id of ["SWINGS55", "STRUCT55", "BOS55", "CHOCH55", "FVG3", "OBPATTERN"]) {
      expect(engineOf(id)).toBe("MarketStructure");
    }
  });

  it("test_chart_p03_structure_disclosure_rendered_when_active", async () => {
    vi.mocked(client.fetchIndicatorSeries).mockResolvedValue({
      symbol: "EURUSD",
      timeframe: "M1",
      seriesKind: "native",
      sourceTimeframe: null,
      excludedPartialBuckets: null,
      detail: null,
      indicators: {
        SWINGS55: {
          shape: "multi",
          kind: "computed",
          lines: {
            swing_high: [{ time: new Date().toISOString(), value: "1.12" }],
            swing_low: [{ time: new Date().toISOString(), value: null }],
          },
        },
      },
    });
    renderStage();
    await waitFor(() => expect(screen.getByTestId("mock-price-chart")).toBeInTheDocument());
    fireEvent.click(screen.getByTestId("engine-menu-button-marketstructure"));
    fireEvent.click(screen.getByTestId("indicator-item-SWINGS55"));
    await waitFor(() =>
      expect(screen.getByTestId("indicator-status-swings55")).toBeInTheDocument(),
    );
    expect(screen.getByTestId("indicator-status-swings55")).toHaveTextContent(
      "not evidence of institutional activity",
    );
  });
});
