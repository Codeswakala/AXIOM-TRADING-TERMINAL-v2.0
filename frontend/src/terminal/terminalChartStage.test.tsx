import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { TerminalProvider } from "../components/terminal/TerminalContext";
import { TerminalChartStage } from "../components/terminal/TerminalChartStage";
import { getComputedToken } from "../components/terminal/tokenResolver";
import type { ApiCandle, ChartResearchAnnotation } from "../api/client";
import * as client from "../api/client";

// Mock API client calls
vi.mock("../api/client", async () => {
  const actual = await vi.importActual<typeof client>("../api/client");
  return {
    ...actual,
    fetchCandles: vi.fn(),
    fetchIndicatorSeries: vi.fn(),
    fetchChartResearchAnnotations: vi.fn(),
    createChartResearchAnnotation: vi.fn(),
    seedChartHistory: vi.fn(),
    startLiveMarket: vi.fn(),
    stopLiveMarket: vi.fn(),
  };
});

// Mock PriceChart to avoid Canvas2D rendering in JSDOM
vi.mock("../components/chart/PriceChart", () => ({
  PriceChart: ({ bars, chartType, symbol }: { bars: unknown[]; chartType: string; symbol: string }) => (
    <div
      data-testid="mock-price-chart"
      data-bars-count={bars.length}
      data-chart-type={chartType}
      data-symbol={symbol}
    >
      Mock Canvas ({bars.length} bars)
    </div>
  ),
}));

const mockCandles: ApiCandle[] = [
  {
    id: "c1",
    market_class: "forex",
    symbol: "EURUSD",
    timeframe: "1m",
    open_time: "2026-08-12T15:00:00Z",
    open: "1.08410",
    high: "1.08490",
    low: "1.08390",
    close: "1.08450",
    volume: "14200000",
    source: "synthetic",
    created_at: "2026-08-12T15:01:00Z",
  },
  {
    id: "c2",
    market_class: "forex",
    symbol: "EURUSD",
    timeframe: "1m",
    open_time: "2026-08-12T15:01:00Z",
    open: "1.08450",
    high: "1.08510",
    low: "1.08440",
    close: "1.08490",
    volume: "11500000",
    source: "simulated",
    created_at: "2026-08-12T15:02:00Z",
  },
];

const mockAnnotation: ChartResearchAnnotation = {
  id: "ann-01",
  created_at: "2026-08-12T15:05:00Z",
  operator_id: "op-admin",
  artifact_type: "chart_research_annotation",
  chart_context: { symbol: "EUR/USD", timeframe: "1m" },
  content: { note: "Key resistance zone observed", price_level: 1.085 },
  source_artifact_ids: [],
  provenance: {},
  uncertainty: {},
  disclaimer: "Inert research markup",
  research_status: "research_only",
  audit_correlation_id: "audit-01",
};

beforeEach(() => {
  vi.clearAllMocks();
  vi.mocked(client.fetchCandles).mockResolvedValue({
      kind: "native",
      timeframe: "M1",
      bars: mockCandles,
    });
  vi.mocked(client.fetchChartResearchAnnotations).mockResolvedValue([mockAnnotation]);
  vi.mocked(client.createChartResearchAnnotation).mockImplementation(async (payload) => ({
    id: "ann-new",
    created_at: new Date().toISOString(),
    operator_id: "op-admin",
    artifact_type: "chart_research_annotation",
    chart_context: payload.chart_context,
    content: payload.content,
    source_artifact_ids: [],
    provenance: {},
    uncertainty: {},
    disclaimer: "Inert research markup",
    research_status: "research_only",
    audit_correlation_id: "audit-new",
  }));
  vi.mocked(client.seedChartHistory).mockResolvedValue({ status: "ok", seeded: { EURUSD: 80 }, timeframe: "1m" });
  vi.mocked(client.fetchIndicatorSeries).mockResolvedValue({
    symbol: "EURUSD",
    timeframe: "M1",
    seriesKind: "native",
    sourceTimeframe: null,
    excludedPartialBuckets: null,
    detail: null,
    indicators: {
      SMA20: {
        shape: "line",
        kind: "computed",
        points: [
          { time: "2026-08-12T15:00:00Z", value: "1.08410" },
          { time: "2026-08-12T15:01:00Z", value: "1.08450" },
        ],
      },
    },
  });
});

describe("UI-NEW-P03 Primary Candlestick Chart Stage & Technical Overlays", () => {
  // Test 1 (Mandatory named test #1)
  it("test_uinew_p03_chart_stage_renders_candles_from_backend_series_only", async () => {
    render(
      <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
        <TerminalChartStage />
      </TerminalProvider>,
    );

    expect(screen.getByTestId("terminal-chart-stage")).toBeInTheDocument();
    expect(screen.getByTestId("chart-symbol-badge")).toHaveTextContent("EUR/USD");

    // Wait for candles to load from backend
    await waitFor(() => {
      expect(client.fetchCandles).toHaveBeenCalledWith({
        symbol: "EURUSD",
        timeframe: "M1",
        limit: 100,
        order: "asc",
      });
      expect(screen.getByTestId("mock-price-chart")).toHaveAttribute("data-bars-count", "2");
    });
  });

  // Test 2 (Mandatory named test #2 — B-P03-2 / TD-029 Timeframe Honesty)
  it("test_uinew_p03_timeframe_switching_discloses_resampled_or_incomplete_series", async () => {
    render(
      <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
        <TerminalChartStage />
      </TerminalProvider>,
    );

    // Initial 1m state shows Native M1 notice (once the native series lands)
    await waitFor(() => {
      expect(screen.getByTestId("timeframe-native-notice")).toHaveTextContent("Native M1 Stream");
    });

    // DATA-P02 M5: the notice renders from the SERVER discriminant — the
    // mock returns the aggregated envelope for H1, so the notice must state
    // the wall-clock-aligned aggregation, not a hardcoded TD-029 string.
    vi.mocked(client.fetchCandles).mockImplementation(
      (async (params) => {
        const tf = (params as { timeframe?: string }).timeframe;
        return tf === "H1"
          ? {
              kind: "aggregated",
              timeframe: "H1",
              sourceTimeframe: "M1",
              excludedPartialBuckets: 0,
              bars: mockCandles,
            }
          : { kind: "native", timeframe: "M1", bars: mockCandles };
      }) as typeof client.fetchCandles,
    );

    // Click 1H timeframe
    const tf1hBtn = screen.getByTestId("chart-tf-1h");
    fireEvent.click(tf1hBtn);

    // Verify timeframe switch triggers fetchCandles with H1
    await waitFor(() => {
      expect(client.fetchCandles).toHaveBeenCalledWith({
        symbol: "EURUSD",
        timeframe: "H1",
        limit: 100,
        order: "asc",
      });
    });

    await waitFor(() => {
      expect(screen.getByTestId("timeframe-resampled-notice")).toHaveTextContent(
        "Resampled from M1 stream · wall-clock aligned 60-minute buckets",
      );
    });
    expect(screen.queryByTestId("timeframe-native-notice")).not.toBeInTheDocument();
  });

  // Test 3 (Mandatory named test #3 — B-P03-1 Canvas Token Resolver)
  it("test_uinew_p03_chart_tokens_resolve_to_concrete_values_with_no_hardcoded_hex", () => {
    // 1. Verify getComputedToken resolves token names to RGB fallback when DOM is uncomputed
    const upColor = getComputedToken("--ix-color-success-green", "rgb(16, 185, 129)");
    const downColor = getComputedToken("--ix-color-critical-red", "rgb(239, 68, 68)");
    const bgColor = getComputedToken("--ix-bg-root", "rgb(11, 14, 20)");

    expect(upColor).toMatch(/^rgb\(\d+,\s*\d+,\s*\d+\)$/);
    expect(downColor).toMatch(/^rgb\(\d+,\s*\d+,\s*\d+\)$/);
    expect(bgColor).toMatch(/^rgb\(\d+,\s*\d+,\s*\d+\)$/);

    // 2. Verify resolved colors contain 0 hex values
    expect(upColor).not.toContain("#");
    expect(downColor).not.toContain("#");
    expect(bgColor).not.toContain("#");
  });

  // Test 4 (Mandatory named test #4 — B-P03-4 Research Annotation Integrity)
  it("test_uinew_p03_annotations_reject_order_entry_stop_target_and_size_fields", async () => {
    render(
      <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
        <TerminalChartStage />
      </TerminalProvider>,
    );

    // Open Annotation dialog
    const addNoteBtn = screen.getByTestId("chart-add-annotation-btn");
    fireEvent.click(addNoteBtn);

    expect(screen.getByTestId("annotation-dialog")).toBeInTheDocument();

    const textarea = screen.getByTestId("annotation-text-input");
    const saveBtn = screen.getByTestId("annotation-save-btn");

    // Case A: Forbidden order term "stop_loss" in text
    fireEvent.change(textarea, { target: { value: "Set stop_loss at 1.0820" } });
    fireEvent.click(saveBtn);

    expect(screen.getByTestId("annotation-error-banner")).toHaveTextContent(
      "Forbidden actuation term 'stop_loss' in research annotation.",
    );
    expect(client.createChartResearchAnnotation).not.toHaveBeenCalled();

    // Case B: Valid inert research note
    fireEvent.change(textarea, { target: { value: "Major liquidity pool identified at session high" } });
    fireEvent.click(saveBtn);

    await waitFor(() => {
      expect(client.createChartResearchAnnotation).toHaveBeenCalledWith(
        expect.objectContaining({
          artifact_type: "chart_research_annotation",
          content: expect.objectContaining({
            note: "Major liquidity pool identified at session high",
          }),
          research_status: "research_only",
        }),
      );
    });
  });

  // Test 5 (Mandatory named test #5 — B-P03-5 Seed vs Live Provenance Distinction)
  it("test_uinew_p03_seed_and_live_provenance_are_visually_distinguished", async () => {
    render(
      <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
        <TerminalChartStage />
      </TerminalProvider>,
    );

    await waitFor(() => {
      expect(screen.getByTestId("chart-provenance-badge")).toHaveTextContent("live:simulated");
      expect(screen.getByText(/1 live · 1 seed/i)).toBeInTheDocument();
    });

    // Test seed history button explicitly triggers seedChartHistory
    const seedBtn = screen.getByTestId("chart-seed-btn");
    fireEvent.click(seedBtn);

    await waitFor(() => {
      expect(client.seedChartHistory).toHaveBeenCalled();
      expect(screen.getByTestId("seed-alert-toast")).toHaveTextContent(
        "Seeded 80 synthetic historical bars. Marked as seed:synthetic.",
      );
    });
  });

  // Test 6 (Mandatory named test #6 — T-1 Zero Actuation)
  it("test_uinew_p03_chart_contains_no_execution_or_order_or_broker_or_account_control", () => {
    render(
      <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
        <TerminalChartStage />
      </TerminalProvider>,
    );

    const buttons = screen.queryAllByRole("button");
    const inputs = screen.queryAllByRole("textbox");

    const interactiveText = [
      ...buttons.map((b) => b.textContent?.toLowerCase() ?? ""),
      ...inputs.map((i) => i.getAttribute("placeholder")?.toLowerCase() ?? ""),
    ].join(" ");

    const forbiddenActuation = [
      "buy",
      "sell",
      "place_order",
      "submit_order",
      "order_ticket",
      "execute",
      "connect-broker",
      "account_id",
      "position",
      "balance",
      "margin",
      "open_gate",
      "allow_execution",
    ];

    for (const term of forbiddenActuation) {
      expect(interactiveText).not.toContain(term);
    }
  });

  // Test 7 (Mandatory named test #7 — B-P03-3 Overlays Presentation Only)
  it("test_uinew_p03_overlays_are_presentation_only_and_emit_no_signal_or_confidence", () => {
    render(
      <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
        <TerminalChartStage />
      </TerminalProvider>,
    );

    const sma20Btn = screen.getByTestId("overlay-sma20");
    const sma50Btn = screen.getByTestId("overlay-sma50");
    const ema20Btn = screen.getByTestId("overlay-ema20");

    // Toggle overlays on
    fireEvent.click(sma20Btn);
    fireEvent.click(sma50Btn);
    fireEvent.click(ema20Btn);

    expect(sma20Btn).toHaveClass("active");
    expect(sma50Btn).toHaveClass("active");
    expect(ema20Btn).toHaveClass("active");

    // Verify overlays contain zero signal generation text
    const toolbarText = screen.getByTestId("chart-toolbar").textContent?.toLowerCase() ?? "";
    expect(toolbarText).not.toContain("signal");
    expect(toolbarText).not.toContain("confidence");
    expect(toolbarText).not.toContain("probability");
    expect(toolbarText).not.toContain("buy_bias");
    expect(toolbarText).not.toContain("sell_bias");
  });
});
