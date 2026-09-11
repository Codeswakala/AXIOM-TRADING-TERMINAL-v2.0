/**
 * CHART-P02 fail-first frontend tests — indicator surface at scale:
 * toolbar reachability (M5), pane budget refusal (M6), time-axis
 * synchronisation (M7), engine grouping (S1), directional-verdict guard (M9).
 *
 * Every test here MUST fail against the pre-CHART-P02 tree and pass once the
 * phase ships: the registry mirror has no engine field and only 7 entries,
 * the toolbar has no menus, the pane budget does not exist, the price pane
 * emits no visible-range events, and the guard's forbidden list does not
 * include the directional vocabulary.
 */
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { TerminalProvider } from "../components/terminal/TerminalContext";
import { TerminalChartStage } from "../components/terminal/TerminalChartStage";
import * as client from "../api/client";
import { ENGINES, INDICATOR_UI, engineOf, paneIndicators } from "../api/indicatorRegistry";

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
    onVisibleTimeRangeChange,
  }: {
    bars: unknown[];
    overlayLines?: unknown[];
    onVisibleTimeRangeChange?: (range: { from: number; to: number } | null) => void;
  }) => (
    <div
      data-testid="mock-price-chart"
      data-bars-count={bars.length}
      data-overlay-lines={(overlayLines ?? []).length}
      data-zoom-trigger="true"
      onClick={() => onVisibleTimeRangeChange?.({ from: 40, to: 80 })}
    />
  ),
}));

vi.mock("../components/terminal/IndicatorPane", () => ({
  IndicatorPane: ({
    testid,
    label,
    visibleRange,
  }: {
    testid: string;
    label: string;
    visibleRange?: { from: number; to: number } | null;
  }) => (
    <div
      data-testid={testid}
      data-visible-from={visibleRange ? String(visibleRange.from) : ""}
      data-visible-to={visibleRange ? String(visibleRange.to) : ""}
    >
      {label}
    </div>
  ),
}));

const candle = (minute: number): client.ApiCandle => ({
  id: `c${minute}`,
  market_class: "forex",
  symbol: "EURUSD",
  timeframe: "M1",
  open_time: new Date(Date.UTC(2026, 7, 17, 10, minute)).toISOString(),
  open: "1.10000",
  high: "1.10500",
  low: "1.09900",
  close: "1.10100",
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

const multiIndicator = (lines: Record<string, Array<number | null>>) => ({
  shape: "multi" as const,
  kind: "computed" as const,
  lines: Object.fromEntries(
    Object.entries(lines).map(([name, values]) => [
      name,
      values.map((v, i) => ({
        time: new Date(Date.UTC(2026, 7, 17, 10, i)).toISOString(),
        value: v === null ? null : String(v),
      })),
    ]),
  ),
});

const renderStage = () =>
  render(
    <TerminalProvider initialSymbol="EUR/USD" enableLiveMarket={false}>
      <TerminalChartStage />
    </TerminalProvider>,
  );

beforeEach(() => {
  vi.clearAllMocks();
  vi.mocked(client.fetchCandles).mockResolvedValue({
    kind: "native",
    timeframe: "M1",
    bars: Array.from({ length: 30 }, (_, i) => candle(i)),
  });
  vi.mocked(client.fetchIndicatorSeries).mockImplementation(
    (async (params) => {
      const ids = (params as { indicators: string[] }).indicators;
      const indicators: Record<string, unknown> = {};
      for (const id of ids) {
        const ui = INDICATOR_UI.find((i) => i.id === id);
        // Pane indicators render in IndicatorPane (line/macd shapes only);
        // overlay multi-line entries exercise the multi path.
        indicators[id] =
          ui && ui.pane === "pane" ? lineIndicator([1, 2, 3]) : multiIndicator({ a: [1, 2, 3], b: [1, 2, 3] });
      }
      return {
        symbol: "EURUSD",
        timeframe: "M1",
        seriesKind: "native",
        sourceTimeframe: null,
        excludedPartialBuckets: null,
        detail: null,
        indicators,
      };
    }) as typeof client.fetchIndicatorSeries,
  );
});

describe("CHART-P02 S1 — engine grouping is data-driven", () => {
  it("test_chart_p02_frontend_registry_mirrors_backend_engines_and_breadth", () => {
    expect(INDICATOR_UI.map((i) => i.id)).toEqual([
      "SMA20", "SMA50", "EMA20", "RSI14", "MACD12269", "BBANDS201", "ATR14",
      "HMA20", "SUPERTREND103", "ICHIMOKU952652",
      "STOCH1433", "CCI20", "ROC12", "ADX14",
      "KELTNER20", "DONCHIAN20",
      "PIVOTCL", "CAMARILLA", "PREVHL", "SESSLVL",
      "ZSCORE20", "PCTRANK20", "REGCHAN20",
      "SWINGS55", "STRUCT55", "BOS55", "CHOCH55", "FVG3", "OBPATTERN",
    ]);
    expect(INDICATOR_UI).toHaveLength(29);
    expect([...ENGINES]).toEqual([
      "Trend",
      "Momentum",
      "Volatility",
      "Levels",
      "Statistics",
      "MarketStructure",
    ]);
    expect(engineOf("HMA20")).toBe("Trend");
    expect(engineOf("STOCH1433")).toBe("Momentum");
    expect(engineOf("PIVOTCL")).toBe("Levels");
    expect(paneIndicators()).toEqual(["RSI14", "MACD12269", "ATR14", "STOCH1433", "CCI20", "ROC12", "ADX14"]);
  });
});

describe("CHART-P02 M5 — toolbar exposes every registry indicator", () => {
  it("test_chart_p02_toolbar_exposes_every_registry_indicator", () => {
    renderStage();
    // The three most-used remain direct pills (one interaction).
    expect(screen.getByTestId("overlay-sma20")).toBeInTheDocument();
    expect(screen.getByTestId("overlay-sma50")).toBeInTheDocument();
    expect(screen.getByTestId("overlay-ema20")).toBeInTheDocument();
    // Every other registry entry has an engine menu with an item control.
    for (const def of INDICATOR_UI) {
      if (["SMA20", "SMA50", "EMA20"].includes(def.id)) continue;
      const menuButton = screen.getByTestId(`engine-menu-button-${def.engine.toLowerCase()}`);
      fireEvent.click(menuButton);
      expect(screen.getByTestId(`indicator-item-${def.id}`)).toBeInTheDocument();
      fireEvent.click(menuButton); // close
    }
  });

  it("test_chart_p02_active_indicator_visible_in_tray_without_opening_menu", async () => {
    renderStage();
    await waitFor(() => expect(screen.getByTestId("mock-price-chart")).toBeInTheDocument());
    const menuButton = screen.getByTestId("engine-menu-button-trend");
    fireEvent.click(menuButton);
    fireEvent.click(screen.getByTestId("indicator-item-HMA20"));
    await waitFor(() => expect(screen.getByTestId("active-tray-HMA20")).toBeInTheDocument());
    // The tray shows the active indicator without opening any menu.
    expect(screen.getByTestId("active-tray-HMA20")).toHaveTextContent("HMA 20");
  });
});

describe("CHART-P02 M6 — pane budget refuses explicitly, never silently", () => {
  it("test_chart_p02_pane_budget_refuses_explicitly_not_silently", async () => {
    renderStage();
    await waitFor(() => expect(screen.getByTestId("mock-price-chart")).toBeInTheDocument());
    const clickMenuItem = (id: string) => {
      fireEvent.click(screen.getByTestId(`engine-menu-button-${(engineOf(id) ?? "").toLowerCase()}`));
      fireEvent.click(screen.getByTestId(`indicator-item-${id}`));
    };
    for (const id of ["RSI14", "MACD12269", "ATR14"]) {
      clickMenuItem(id);
      await waitFor(() =>
        expect(screen.getByTestId(`indicator-status-${id.toLowerCase()}`)).toBeInTheDocument(),
      );
    }
    expect(screen.getByTestId("pane-budget-indicator")).toHaveTextContent("3");
    clickMenuItem("STOCH1433");
    // The refusal is explicit, the item never activates, and the pane count is unchanged.
    await waitFor(() => expect(screen.getByTestId("pane-budget-refusal")).toBeInTheDocument());
    expect(screen.getByTestId("pane-budget-refusal")).toHaveTextContent("STOCH1433");
    expect(screen.getByTestId("pane-budget-indicator")).toHaveTextContent("3");
    fireEvent.click(screen.getByTestId("engine-menu-button-momentum"));
    expect(screen.getByTestId("indicator-item-STOCH1433")).not.toHaveClass("active");
  });
});

describe("CHART-P02 M7 — pane time axes track the price pane", () => {
  it("test_chart_p02_pane_time_axes_track_price_pane", async () => {
    renderStage();
    await waitFor(() => expect(screen.getByTestId("mock-price-chart")).toBeInTheDocument());
    fireEvent.click(screen.getByTestId("engine-menu-button-momentum"));
    fireEvent.click(screen.getByTestId("indicator-item-RSI14"));
    await waitFor(() =>
      expect(screen.getByTestId("indicator-pane-rsi14")).toBeInTheDocument(),
    );
    expect(screen.getByTestId("indicator-pane-rsi14")).toHaveAttribute("data-visible-from", "");
    // The mock price chart emits a visible-range change (a zoom/pan); the
    // pane must adopt it.
    fireEvent.click(screen.getByTestId("mock-price-chart"));
    await waitFor(() =>
      expect(screen.getByTestId("indicator-pane-rsi14")).toHaveAttribute("data-visible-from", "40"),
    );
    expect(screen.getByTestId("indicator-pane-rsi14")).toHaveAttribute("data-visible-to", "80");
  });
});

describe("CHART-P02 M9 — no directional verdict language", () => {
  it("test_chart_p02_no_directional_verdict_language", async () => {
    const source = readFileSync(
      join(process.cwd(), "src/components/terminal/TerminalChartStage.tsx"),
      "utf8",
    );
    const anchor = "describe data, they never advise a trade";
    expect(source).toContain(anchor);
    const residue = source.replace(anchor, "");
    // Advisory + directional folk vocabulary must be absent from the source.
    const forbidden = [
      "trade recommendation",
      "eligibility",
      "setup quality",
      "risk/reward",
      "buy signal",
      "sell signal",
      "golden cross",
      "death cross",
      "crossover signal",
      "bullish",
      "bearish",
      "oversold",
      "overbought",
    ];
    for (const term of forbidden) {
      expect(residue).not.toContain(term);
    }

    // And nothing of it may render with indicators active.
    renderStage();
    await waitFor(() => expect(screen.getByTestId("mock-price-chart")).toBeInTheDocument());
    fireEvent.click(screen.getByTestId("overlay-sma20")); // direct pill
    const clickMenuItem = (id: string) => {
      fireEvent.click(screen.getByTestId(`engine-menu-button-${(engineOf(id) ?? "").toLowerCase()}`));
      fireEvent.click(screen.getByTestId(`indicator-item-${id}`));
    };
    clickMenuItem("ADX14");
    clickMenuItem("STOCH1433");
    clickMenuItem("ICHIMOKU952652");
    await waitFor(() =>
      expect(screen.getByTestId("chart-indicator-status")).toBeInTheDocument(),
    );
    const rendered = (screen.getByTestId("terminal-chart-stage").textContent ?? "").toLowerCase();
    for (const term of forbidden) {
      expect(rendered).not.toContain(term);
    }
    expect(screen.getByTestId("indicator-status-anchor")).toHaveTextContent(anchor);
  });
});
