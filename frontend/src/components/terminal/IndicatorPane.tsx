/**
 * CHART-P01 S2 — separate-pane indicator chart (RSI / MACD / ATR).
 *
 * A presentation-only lightweight-charts instance that RENDERS a precomputed
 * indicator series in its own pane, so the price pane's scale is never
 * distorted by oscillator values. Computes nothing (R7 discipline) — the
 * caller owns the math, the provenance, and the typed result handling.
 */

import { useEffect, useRef } from "react";
import {
  createChart,
  type IChartApi,
  type ISeriesApi,
  type LineData,
  type HistogramData,
  type UTCTimestamp,
  ColorType,
} from "lightweight-charts";
import type { LineIndicatorResult, MacdIndicatorResult, MultiIndicatorResult } from "../../api/client";
import { paletteEntryFor } from "../../api/indicatorRegistry";
import { getComputedToken } from "./tokenResolver";

export interface IndicatorPaneProps {
  testid: string;
  label: string;
  series: LineIndicatorResult | MacdIndicatorResult | MultiIndicatorResult;
  height?: number;
  /** CHART-P02 M7: the price pane's visible time range — applied so the
   * pane's axis tracks the price pane after zoom/pan. */
  visibleRange?: { from: number; to: number } | null;
}

export function IndicatorPane({
  testid,
  label,
  series,
  height = 110,
  visibleRange = null,
}: IndicatorPaneProps) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const seriesRef = useRef<Array<ISeriesApi<"Line"> | ISeriesApi<"Histogram">>>([]);
  const labelRef = useRef(label);
  labelRef.current = label;

  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    const bg = getComputedToken("--ix-bg-root", "rgb(11, 14, 20)");
    const text = getComputedToken("--ix-text-muted", "rgb(148, 163, 184)");
    const grid = getComputedToken("--ix-border-subtle", "rgb(38, 50, 68)");
    const chart = createChart(el, {
      height,
      layout: { background: { type: ColorType.Solid, color: bg }, textColor: text },
      grid: { vertLines: { color: grid }, horzLines: { color: grid } },
      rightPriceScale: { borderColor: grid },
      timeScale: { borderColor: grid, timeVisible: true, secondsVisible: false },
    });
    chartRef.current = chart;
    const ro = new ResizeObserver(() => {
      if (containerRef.current) chart.applyOptions({ width: containerRef.current.clientWidth });
    });
    ro.observe(el);
    chart.applyOptions({ width: el.clientWidth });
    return () => {
      ro.disconnect();
      chart.remove();
      chartRef.current = null;
      seriesRef.current = [];
    };
  }, [height]);

  useEffect(() => {
    const chart = chartRef.current;
    if (!chart) return;
    if (visibleRange && visibleRange.from < visibleRange.to) {
      chart
        .timeScale()
        .setVisibleLogicalRange({ from: visibleRange.from, to: visibleRange.to });
    }
  }, [visibleRange]);

  useEffect(() => {
    const chart = chartRef.current;
    if (!chart) return;
    for (const s of seriesRef.current) {
      try {
        chart.removeSeries(s);
      } catch {
        /* already removed */
      }
    }
    seriesRef.current = [];
    if (series.shape === "multi") {
      // CHART-P02: multi-line pane indicators (ADX/DMI, Stochastic) — one
      // line series per named line, deterministically styled.
      for (const [name, points] of Object.entries(series.lines)) {
        const palette = paletteEntryFor(`${labelRef.current}:${name}`);
        const line = chart.addLineSeries({
          color: getComputedToken(palette.colorToken, "rgb(148, 163, 184)"),
          lineWidth: 2,
          priceLineVisible: false,
          lastValueVisible: false,
        });
        line.setData(
          (points ?? [])
            .filter((p) => p.value !== null && Number.isFinite(Number(p.value)))
            .map(
              (p): LineData => ({
                time: (Date.parse(p.time) / 1000) as UTCTimestamp,
                value: Number(p.value),
              }),
            ),
        );
        seriesRef.current.push(line);
      }
    } else if (series.shape === "line") {
      const line = chart.addLineSeries({
        color: getComputedToken("--ix-color-electric-blue", "rgb(59, 130, 246)"),
        lineWidth: 2,
        priceLineVisible: false,
        lastValueVisible: false,
      });
      line.setData(
        series.points
          .filter((p) => p.value !== null && Number.isFinite(Number(p.value)))
          .map(
            (p): LineData => ({
              time: (Date.parse(p.time) / 1000) as UTCTimestamp,
              value: Number(p.value),
            }),
          ),
      );
      seriesRef.current = [line];
    } else {
      // MACD: signal line + histogram.
      const hist = chart.addHistogramSeries({ priceFormat: { type: "price", precision: 5, minMove: 0.00001 } });
      hist.setData(
        series.points
          .filter((p) => p.histogram !== null && Number.isFinite(Number(p.histogram)))
          .map((p): HistogramData => ({
            time: (Date.parse(p.time) / 1000) as UTCTimestamp,
            value: Number(p.histogram),
            color:
              Number(p.histogram) >= 0
                ? getComputedToken("--ix-color-success-green", "rgb(16, 185, 129)")
                : getComputedToken("--ix-color-critical-red", "rgb(239, 68, 68)"),
          })),
      );
      const line = chart.addLineSeries({
        color: getComputedToken("--ix-color-accent", "rgb(37, 99, 235)"),
        lineWidth: 1,
        priceLineVisible: false,
        lastValueVisible: false,
      });
      line.setData(
        series.points
          .filter((p) => p.signal !== null && Number.isFinite(Number(p.signal)))
          .map(
            (p): LineData => ({
              time: (Date.parse(p.time) / 1000) as UTCTimestamp,
              value: Number(p.signal),
            }),
          ),
      );
      seriesRef.current = [line];
    }
    chart.timeScale().fitContent();
  }, [series]);

  return (
    <div
      className="chart-indicator-pane"
      data-testid={testid}
      data-synced-range-from={visibleRange && visibleRange.from < visibleRange.to ? String(visibleRange.from) : ""}
      data-synced-range-to={visibleRange && visibleRange.from < visibleRange.to ? String(visibleRange.to) : ""}
      role="img"
      aria-label={`${label} indicator pane`}
    >
      <div className="chart-indicator-pane-label mono">
        <span>{label}</span>
        <span className="chart-indicator-pane-hint">derived · descriptive only</span>
      </div>
      <div className="chart-indicator-pane-canvas" ref={containerRef} />
    </div>
  );
}
