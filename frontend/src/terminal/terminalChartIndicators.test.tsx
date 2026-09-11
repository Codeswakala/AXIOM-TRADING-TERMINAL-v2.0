/**
 * CHART-P01 fail-first frontend tests — indicator controls become real
 * (F-CHART-1 closure), typed insufficiency/provenance disclosure (M4/M5/M6),
 * single registry mirror (S1), no candle-series refetch on toggle (S3),
 * and the T-1 guard with non-vacuity anchors (M8).
 *
 * Every test here MUST fail against the pre-CHART-P01 tree and pass after
 * the implementation ships: the registry module and the typed client
 * function do not exist yet, the pills bind inert booleans, and the
 * disclosure anchors are absent from the chart stage source.
 */
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { TerminalProvider } from "../components/terminal/TerminalContext";
import { TerminalChartStage } from "../components/terminal/TerminalChartStage";
import * as client from "../api/client";
import { engineOf } from "../api/indicatorRegistry";
import { INDICATOR_UI, paneIndicators, overlayIndicators } from "../api/indicatorRegistry";

vi.mock("../api/client", async () => {
  const actual = await vi.importActual<typeof client>("../api/client");
  return {
    ...actual,
    fetchCandles: vi.fn(),
    fetchIndicatorSeries: vi.fn(),
    fetchChartResearchAnnotations: vi.fn().mockResolvedValue([]),
    createChartResearchAnnotation: vi.fn(),
    seedChartHistory: vi.fn(),
  };
});

vi.mock("../components/chart/PriceChart", () => ({
  PriceChart: ({
    bars,
    overlayLines,
  }: {
    bars: unknown[];
    overlayLines?: unknown[];
  }) => (
    <div
      data-testid="mock-price-chart"
      data-bars-count={bars.length}
      data-overlay-lines={(overlayLines ?? []).length}
      data-overlay-ids={(overlayLines ?? []).map((l) => (l as { id: string }).id).join(",")}
    />
  ),
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

const lineIndicator = (values: Array<number | null>) => ({
  shape: "line" as const,
  kind: "computed" as const,
  points: values.map((v, i) => ({
    time: new Date(Date.UTC(2026, 7, 17, 10, i)).toISOString(),
    value: v === null ? null : String(v),
  })),
});

const insufficient = (required: number, available: number) => ({
  shape: "insufficient" as const,
  required,
  available,
});

const nativeEnvelope = {
  symbol: "EURUSD",
  timeframe: "M1",
  seriesKind: "native" as const,
  sourceTimeframe: null,
  excludedPartialBuckets: null,
  detail: null,
  indicators: {},
};

const renderStage = () =>
  render(
    <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
      <TerminalChartStage />
    </TerminalProvider>,
  );

/** CHART-P02 toolbar contract: the three most-used indicators are direct
 * pills; everything else lives in its engine menu (one extra interaction). */
const clickIndicator = (id: string) => {
  const direct = screen.queryByTestId(`overlay-${id.toLowerCase()}`);
  if (direct) {
    fireEvent.click(direct);
    return;
  }
  const engine = engineOf(id) ?? "trend";
  fireEvent.click(screen.getByTestId(`engine-menu-button-${engine.toLowerCase()}`));
  fireEvent.click(screen.getByTestId(`indicator-item-${id}`));
};

beforeEach(() => {
  vi.clearAllMocks();
  vi.mocked(client.fetchCandles).mockResolvedValue({
    kind: "native",
    timeframe: "M1",
    bars: [candle(0), candle(1)],
  });
  vi.mocked(client.fetchIndicatorSeries).mockResolvedValue({
    ...nativeEnvelope,
    indicators: {},
  });
});

describe("CHART-P01 S1 — single registry mirror", () => {
  it("test_chart_p01_frontend_indicator_registry_matches_backend_golden", () => {
    // CHART-P02 extends the registry (23 entries with engines); the
    // CHART-P01 seven keep their exact positions — the contract is widened,
    // not weakened.
    expect(INDICATOR_UI.map((i) => i.id).slice(0, 7)).toEqual([
      "SMA20",
      "SMA50",
      "EMA20",
      "RSI14",
      "MACD12269",
      "BBANDS201",
      "ATR14",
    ]);
    expect(INDICATOR_UI).toHaveLength(29); // CHART-P03 adds 6 structure detections
    expect(overlayIndicators()).toHaveLength(22);
    expect(paneIndicators()).toEqual(["RSI14", "MACD12269", "ATR14", "STOCH1433", "CCI20", "ROC12", "ADX14"]);
    const macd = INDICATOR_UI.find((i) => i.id === "MACD12269");
    expect(macd?.label).toBe("MACD");
    expect(macd?.pane).toBe("pane");
  });
});

describe("CHART-P01 F-CHART-1 — the pills drive real series", () => {
  it("test_chart_p01_toggling_sma_fetches_indicator_series_and_renders_overlay", async () => {
    vi.mocked(client.fetchIndicatorSeries).mockResolvedValue({
      ...nativeEnvelope,
      indicators: { SMA20: lineIndicator([1, 2, 3]) },
    });
    renderStage();
    await waitFor(() => expect(screen.getByTestId("mock-price-chart")).toHaveAttribute("data-bars-count", "2"));

    const candleCallsBefore = vi.mocked(client.fetchCandles).mock.calls.length;
    fireEvent.click(screen.getByTestId("overlay-sma20"));

    await waitFor(() => {
      expect(client.fetchIndicatorSeries).toHaveBeenCalledWith({
        symbol: "EURUSD",
        timeframe: "M1",
        indicators: ["SMA20"],
      });
    });
    await waitFor(() => {
      expect(screen.getByTestId("mock-price-chart")).toHaveAttribute("data-overlay-lines", "1");
      expect(screen.getByTestId("mock-price-chart")).toHaveAttribute("data-overlay-ids", "SMA20");
    });
    expect(screen.getByTestId("overlay-sma20")).toHaveClass("active");
    // S3: the candle series was NOT refetched by the toggle.
    expect(vi.mocked(client.fetchCandles).mock.calls.length).toBe(candleCallsBefore);
  });

  it("test_chart_p01_toggling_off_removes_overlay_without_refetch", async () => {
    vi.mocked(client.fetchIndicatorSeries).mockResolvedValue({
      ...nativeEnvelope,
      indicators: { SMA20: lineIndicator([1, 2, 3]) },
    });
    renderStage();
    await waitFor(() => expect(screen.getByTestId("mock-price-chart")).toBeInTheDocument());
    fireEvent.click(screen.getByTestId("overlay-sma20"));
    await waitFor(() =>
      expect(screen.getByTestId("mock-price-chart")).toHaveAttribute("data-overlay-lines", "1"),
    );
    const fetchCount = vi.mocked(client.fetchIndicatorSeries).mock.calls.length;
    fireEvent.click(screen.getByTestId("overlay-sma20"));
    await waitFor(() =>
      expect(screen.getByTestId("mock-price-chart")).toHaveAttribute("data-overlay-lines", "0"),
    );
    expect(vi.mocked(client.fetchIndicatorSeries).mock.calls.length).toBe(fetchCount);
    expect(screen.getByTestId("overlay-sma20")).not.toHaveClass("active");
  });
});

describe("CHART-P01 M4/M5/M6 — typed insufficiency and provenance disclosure", () => {
  it("test_chart_p01_insufficient_history_renders_typed_disclosure_no_line", async () => {
    vi.mocked(client.fetchIndicatorSeries).mockResolvedValue({
      ...nativeEnvelope,
      indicators: { SMA50: insufficient(50, 6) },
    });
    renderStage();
    await waitFor(() => expect(screen.getByTestId("mock-price-chart")).toBeInTheDocument());
    fireEvent.click(screen.getByTestId("overlay-sma50"));
    await waitFor(() =>
      expect(screen.getByTestId("indicator-status-sma50")).toBeInTheDocument(),
    );
    const status = screen.getByTestId("indicator-status-sma50");
    expect(status).toHaveTextContent("50");
    expect(status).toHaveTextContent("6");
    expect(status).toHaveTextContent("insufficient");
    expect(status).toHaveTextContent("no series rendered");
    // No line may appear for an insufficient indicator.
    expect(screen.getByTestId("mock-price-chart")).toHaveAttribute("data-overlay-lines", "0");
  });

  it("test_chart_p01_indicator_provenance_discloses_derived_and_aggregated", async () => {
    vi.mocked(client.fetchIndicatorSeries).mockResolvedValue({
      symbol: "EURUSD",
      timeframe: "H1",
      seriesKind: "aggregated",
      sourceTimeframe: "M1",
      excludedPartialBuckets: 2,
      detail: null,
      indicators: { EMA20: lineIndicator([1, 2, 3]) },
    });
    renderStage();
    await waitFor(() => expect(screen.getByTestId("mock-price-chart")).toBeInTheDocument());
    fireEvent.click(screen.getByTestId("overlay-ema20"));
    await waitFor(() =>
      expect(screen.getByTestId("indicator-status-ema20")).toBeInTheDocument(),
    );
    const status = screen.getByTestId("indicator-status-ema20");
    expect(status).toHaveTextContent("derived from seed:synthetic OHLC");
    expect(status).toHaveTextContent("aggregated");
    expect(status).toHaveTextContent("2 partial bucket(s) excluded");
  });

  it("test_chart_p01_unavailable_series_renders_absence_not_indicator_lines", async () => {
    vi.mocked(client.fetchIndicatorSeries).mockResolvedValue({
      symbol: "EURUSD",
      timeframe: "H1",
      seriesKind: "unavailable",
      sourceTimeframe: null,
      excludedPartialBuckets: null,
      detail: "insufficient M1 coverage to form a complete H1 bucket",
      indicators: {},
    });
    renderStage();
    await waitFor(() => expect(screen.getByTestId("mock-price-chart")).toBeInTheDocument());
    fireEvent.click(screen.getByTestId("overlay-sma20"));
    await waitFor(() =>
      expect(screen.getByTestId("indicator-status-sma20")).toHaveTextContent(
        "insufficient M1 coverage",
      ),
    );
    expect(screen.getByTestId("mock-price-chart")).toHaveAttribute("data-overlay-lines", "0");
  });
});

describe("CHART-P01 M8 — T-1 guard with non-vacuity anchors", () => {
  it("test_chart_p01_indicators_never_render_actuation_language", () => {
    const source = readFileSync(
      join(process.cwd(), "src/components/terminal/TerminalChartStage.tsx"),
      "utf8",
    );
    // Anchor sentence: the indicator disclosure the guard protects. Its
    // removal must fail the build.
    const anchor = "describe data, they never advise a trade";
    expect(source).toContain(anchor);
    const residue = source.replace(anchor, "");

    // Advisory-drift vocabulary must be absent from the source residue: an
    // indicator surface must not drift into verdict language. (The actuation
    // vocabulary itself is asserted at RENDER below — the annotation guard
    // legitimately lists rejection tokens in source.)
    const forbiddenAdvisory = [
      "trade recommendation",
      "eligibility",
      "setup quality",
      "risk/reward",
    ];
    for (const term of forbiddenAdvisory) {
      expect(residue).not.toContain(term);
    }
  });

  it("test_chart_p01_actuation_vocabulary_absent_from_rendered_indicator_surface", async () => {
    vi.mocked(client.fetchIndicatorSeries).mockResolvedValue({
      ...nativeEnvelope,
      indicators: {
        SMA20: lineIndicator([1, 2, 3]),
        RSI14: lineIndicator([50, 55, 60]),
        MACD12269: {
          shape: "macd",
          kind: "computed",
          points: [
            { time: new Date().toISOString(), macd: "1", signal: "0.5", histogram: "0.5" },
          ],
        },
      },
    });
    renderStage();
    await waitFor(() => expect(screen.getByTestId("mock-price-chart")).toBeInTheDocument());
    fireEvent.click(screen.getByTestId("overlay-sma20"));
    clickIndicator("RSI14");
    clickIndicator("MACD12269");
    await waitFor(() =>
      expect(screen.getByTestId("chart-indicator-status")).toBeInTheDocument(),
    );

    // The actuation vocabulary enforced by the standing watchlist guard
    // (terminalWatchlistDepth.test.tsx) must be absent from EVERYTHING the
    // indicator surface renders — buttons, statuses, panes, anchors.
    const stage = screen.getByTestId("terminal-chart-stage");
    const rendered = (stage.textContent ?? "").toLowerCase();
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
      expect(rendered).not.toContain(term);
    }
    // And the honesty anchor is actually rendered while indicators are active.
    expect(screen.getByTestId("indicator-status-anchor")).toHaveTextContent(
      "describe data, they never advise a trade",
    );
  });

  it("test_chart_p01_all_indicators_off_renders_clean_chart_with_no_residue", async () => {
    renderStage();
    await waitFor(() => expect(screen.getByTestId("mock-price-chart")).toBeInTheDocument());
    expect(screen.getByTestId("mock-price-chart")).toHaveAttribute("data-overlay-lines", "0");
    expect(screen.queryByTestId("chart-indicator-status")).not.toBeInTheDocument();
    expect(screen.queryByTestId(/^indicator-pane-/)).not.toBeInTheDocument();
    expect(screen.getByTestId("terminal-chart-stage")).toBeInTheDocument();
  });
});
