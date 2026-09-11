/**
 * Presentation-only chart component (TradingView Lightweight Charts).
 * Renders series data; does not compute indicators or analytics.
 *
 * CHART-P01 (R7): the contract above remains true — overlay lines are
 * PRECOMPUTED by the caller (server-side indicator service) and passed in;
 * this component only creates line series for them.
 */

import { useEffect, useRef, useState } from "react";
import {
  createChart,
  type IChartApi,
  type ISeriesApi,
  type CandlestickData,
  type LineData,
  type UTCTimestamp,
  ColorType,
  CrosshairMode,
  LineStyle,
} from "lightweight-charts";
import type { CandleBar, ChartType } from "../../chart/types";
import { getComputedToken } from "../terminal/tokenResolver";
import {
  ChartDrawingOverlay,
  type CoordinateConverters,
} from "../terminal/ChartDrawingOverlay";
import type { ChartDrawing } from "../../api/drawingTools";

export interface OverlayLine {
  id: string;
  label: string;
  colorToken: string;
  style?: 0 | 1 | 2;
  points: Array<{ time: number; value: number }>;
}

export interface VisibleRange {
  from: number;
  to: number;
}

type Props = {
  bars: CandleBar[];
  chartType: ChartType;
  symbol: string;
  height?: number;
  /** DATA-P02 M7: presentation-only hover callback — fires with the bar under
   * the crosshair (or null when the crosshair leaves the series). */
  onBarHover?: (bar: CandleBar | null) => void;
  /** CHART-P01: precomputed overlay line series (SMA/EMA/Bollinger). */
  overlayLines?: OverlayLine[];
  /** CHART-P02 M7: the price pane's visible time range after zoom/pan —
   * consumed by stacked indicator panes so their axes track it. */
  onVisibleTimeRangeChange?: (range: VisibleRange | null) => void;
  /** CHART-P03: persisted drawings, rendered as an overlay — this component
   * converts (price, time) to pixels at draw time and never computes. */
  drawings?: ChartDrawing[];
  selectedDrawingId?: string | null;
  onDrawingSelect?: (id: string | null) => void;
  onDrawingHandlesChanged?: (id: string, handles: ChartDrawing["handles"]) => void;
  /** CHART-P03: the coordinate bridge — exposed once the chart + series
   * exist, so the stage can convert placement clicks to (price, time). */
  onCoordinateApiReady?: (api: CoordinateConverters | null) => void;
};

function toCandle(b: CandleBar): CandlestickData {
  return {
    time: b.time as UTCTimestamp,
    open: b.open,
    high: b.high,
    low: b.low,
    close: b.close,
  };
}

function toLine(b: CandleBar): LineData {
  return { time: b.time as UTCTimestamp, value: b.close };
}

export function PriceChart({
  bars,
  chartType,
  symbol,
  height = 420,
  onBarHover,
  overlayLines = [],
  onVisibleTimeRangeChange,
  drawings = [],
  selectedDrawingId = null,
  onDrawingSelect,
  onDrawingHandlesChanged,
  onCoordinateApiReady,
}: Props) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const seriesRef = useRef<ISeriesApi<"Candlestick"> | ISeriesApi<"Line"> | ISeriesApi<"Area"> | null>(
    null,
  );
  const overlaySeriesRef = useRef<Map<string, ISeriesApi<"Line">>>(new Map());
  const typeRef = useRef<ChartType>(chartType);
  const lastLenRef = useRef(0);
  const lastTimeRef = useRef(0);
  const barsRef = useRef<CandleBar[]>(bars);
  const hoverRef = useRef(onBarHover);
  const rangeRef = useRef(onVisibleTimeRangeChange);
  const bridgeRef = useRef(onCoordinateApiReady);
  const selectRef = useRef(onDrawingSelect);
  const handlesRef = useRef(onDrawingHandlesChanged);
  const [converters, setConverters] = useState<CoordinateConverters | null>(null);
  const [containerSize, setContainerSize] = useState({ width: 0, height: 0 });
  barsRef.current = bars;
  hoverRef.current = onBarHover;
  rangeRef.current = onVisibleTimeRangeChange;
  bridgeRef.current = onCoordinateApiReady;
  selectRef.current = onDrawingSelect;
  handlesRef.current = onDrawingHandlesChanged;

  // Create chart once
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;

    const bg = getComputedToken("--ix-bg-root", "rgb(11, 14, 20)");
    const text = getComputedToken("--ix-text-muted", "rgb(148, 163, 184)");
    const grid = getComputedToken("--ix-border-subtle", "rgb(38, 50, 68)");

    const chart = createChart(el, {
      height,
      layout: {
        background: { type: ColorType.Solid, color: bg },
        textColor: text,
      },
      grid: {
        vertLines: { color: grid },
        horzLines: { color: grid },
      },
      crosshair: { mode: CrosshairMode.Normal },
      rightPriceScale: { borderColor: grid },
      timeScale: { borderColor: grid, timeVisible: true, secondsVisible: false },
    });
    chartRef.current = chart;

    // CHART-P02 M7: expose the price pane's visible time range so stacked
    // indicator panes can track it (zoom/pan sync).
    chart.timeScale().subscribeVisibleTimeRangeChange((range) => {
      const cb = rangeRef.current;
      if (!cb) return;
      if (!range) {
        cb(null);
        return;
      }
      cb({ from: range.from as number, to: range.to as number });
    });

    // DATA-P02 M7: report the bar under the crosshair for session labelling.
    chart.subscribeCrosshairMove((param) => {
      const cb = hoverRef.current;
      if (!cb) return;
      if (!param.time) {
        cb(null);
        return;
      }
      const target = param.time as number;
      const found = barsRef.current.find((b) => b.time === target);
      cb(found ?? null);
    });

    const ro = new ResizeObserver(() => {
      if (containerRef.current) {
        chart.applyOptions({ width: containerRef.current.clientWidth });
      }
    });
    ro.observe(el);
    chart.applyOptions({ width: el.clientWidth });

    return () => {
      ro.disconnect();
      chart.remove();
      chartRef.current = null;
      seriesRef.current = null;
    };
  }, [height]);

  // Recreate series when chart type changes
  useEffect(() => {
    const chart = chartRef.current;
    if (!chart) return;

    if (seriesRef.current) {
      chart.removeSeries(seriesRef.current);
      seriesRef.current = null;
    }
    typeRef.current = chartType;
    lastLenRef.current = 0;
    lastTimeRef.current = 0;

    const up = getComputedToken("--ix-color-success-green", "rgb(16, 185, 129)");
    const down = getComputedToken("--ix-color-critical-red", "rgb(239, 68, 68)");
    const accent = getComputedToken("--ix-color-accent", "rgb(37, 99, 235)");
    const selection = getComputedToken("--ix-color-selection", "rgb(28, 61, 102)");

    if (chartType === "candlestick") {
      seriesRef.current = chart.addCandlestickSeries({
        upColor: up,
        downColor: down,
        borderUpColor: up,
        borderDownColor: down,
        wickUpColor: up,
        wickDownColor: down,
      });
    } else if (chartType === "line") {
      seriesRef.current = chart.addLineSeries({
        color: accent,
        lineWidth: 2,
      });
    } else {
      seriesRef.current = chart.addAreaSeries({
        lineColor: accent,
        topColor: selection,
        bottomColor: "transparent",
        lineWidth: 2,
      });
    }
  }, [chartType, symbol]);

  // Push data efficiently
  useEffect(() => {
    const series = seriesRef.current;
    if (!series || !chartRef.current) return;
    if (bars.length === 0) {
      series.setData([]);
      lastLenRef.current = 0;
      lastTimeRef.current = 0;
      return;
    }

    const type = typeRef.current;
    // A full reset is required not only when the bar count shrinks or grows
    // sharply, but also when the series' LAST BAR TIME REGRESSES. Switching
    // to a longer timeframe always regresses: the M6 partial-bucket rule
    // excludes the still-forming bucket, so the aggregated series' last bar
    // is necessarily OLDER than the native series' last bar. The incremental
    // update() path rejects older times ("Cannot update oldest data"), which
    // previously crashed the whole chart stage on a plain 1m -> 1h switch
    // when no live bar had been merged (post-closure hotfix, disclosed).
    const lastTime = bars[bars.length - 1]?.time ?? 0;
    const fullReset =
      bars.length < lastLenRef.current ||
      (bars[0]?.time !== undefined && lastTimeRef.current === 0) ||
      (lastLenRef.current > 0 && bars.length > lastLenRef.current + 5) ||
      (lastLenRef.current > 0 &&
        lastTimeRef.current > 0 &&
        lastTime > 0 &&
        lastTime < lastTimeRef.current);

    // Default viewport: last N bars for legibility (ITRGA F-4 / R-1)
    const VISIBLE_BARS = 80;
    const visible =
      bars.length > VISIBLE_BARS ? bars.slice(bars.length - VISIBLE_BARS) : bars;

    if (fullReset || lastLenRef.current === 0) {
      if (type === "candlestick") {
        (series as ISeriesApi<"Candlestick">).setData(bars.map(toCandle));
      } else {
        (series as ISeriesApi<"Line">).setData(bars.map(toLine));
      }
      // Prefer a legible recent window over packing all bars edge-to-edge
      if (visible.length >= 2) {
        chartRef.current.timeScale().setVisibleLogicalRange({
          from: Math.max(0, bars.length - VISIBLE_BARS),
          to: bars.length - 1 + 2,
        });
      } else {
        chartRef.current.timeScale().fitContent();
      }
    } else {
      const last = bars[bars.length - 1];
      if (type === "candlestick") {
        (series as ISeriesApi<"Candlestick">).update(toCandle(last));
      } else {
        (series as ISeriesApi<"Line">).update(toLine(last));
      }
    }
    lastLenRef.current = bars.length;
    lastTimeRef.current = bars[bars.length - 1]?.time ?? 0;
  }, [bars, symbol]);

  // CHART-P03: publish the coordinate bridge whenever the chart + a series
  // exist (the stage uses it to convert placement clicks to (price, time)).
  useEffect(() => {
    const chart = chartRef.current;
    const series = seriesRef.current;
    const cb = bridgeRef.current;
    if (!chart || !series || !cb) return;
    const api: CoordinateConverters = {
      timeToCoordinate: (t: number) => chart.timeScale().timeToCoordinate(t as UTCTimestamp) ?? 0,
      priceToCoordinate: (price: number) => series.priceToCoordinate(price) ?? 0,
      coordinateToTime: (x: number) => (chart.timeScale().coordinateToTime(x) as number) ?? 0,
      coordinateToPrice: (y: number) => series.coordinateToPrice(y) ?? 0,
    };
    setConverters(api);
    setContainerSize({
      width: containerRef.current?.clientWidth ?? 0,
      height: containerRef.current?.clientHeight ?? height,
    });
    cb(api);
    return () => cb(null);
  }, [chartType, symbol, height]);

  // CHART-P01 overlay lines — render PRECOMPUTED series only (R7: no
  // computation here; the caller owns the math and its provenance).
  useEffect(() => {
    const chart = chartRef.current;
    if (!chart) return;
    const wanted = new Map(overlayLines.map((l) => [l.id, l]));

    for (const [id, series] of overlaySeriesRef.current) {
      if (!wanted.has(id)) {
        chart.removeSeries(series);
        overlaySeriesRef.current.delete(id);
      }
    }
    for (const line of overlayLines) {
      const existing = overlaySeriesRef.current.get(line.id);
      const points = line.points
        .filter((p) => Number.isFinite(p.value))
        .map((p) => ({ time: p.time as UTCTimestamp, value: p.value }));
      if (existing) {
        existing.setData(points);
        continue;
      }
      const color = getComputedToken(line.colorToken, "rgb(148, 163, 184)");
      const lineStyle =
        line.style === 2 ? LineStyle.Dashed : line.style === 1 ? LineStyle.Dotted : LineStyle.Solid;
      const created = chart.addLineSeries({
        color,
        lineWidth: 2,
        lineStyle,
        priceLineVisible: false,
        lastValueVisible: false,
      });
      created.setData(points);
      overlaySeriesRef.current.set(line.id, created);
    }
  }, [overlayLines]);

  return (
    <div
      className="chart-canvas"
      ref={containerRef}
      role="img"
      aria-label={`${symbol} price chart, ${chartType}`}
      style={{ position: "relative" }}
    >
      {converters ? (
        <ChartDrawingOverlay
          drawings={drawings}
          converters={converters}
          width={containerSize.width}
          height={containerSize.height}
          selectedId={selectedDrawingId}
          onSelect={(id) => selectRef.current?.(id)}
          onHandlesChanged={(id, handles) => handlesRef.current?.(id, handles)}
        />
      ) : null}
    </div>
  );
}
