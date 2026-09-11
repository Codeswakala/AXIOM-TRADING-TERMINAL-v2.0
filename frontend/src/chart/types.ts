/** Chart presentation types — no analytical logic (Architecture §30). */

export type ChartType = "candlestick" | "line" | "area" | "bar";

export type ChartTimeframe = "M1" | "M5" | "H1" | "D1";

export type ChartState = {
  symbol: string;
  timeframe: ChartTimeframe;
  chartType: ChartType;
  /** Logical bar range hint for future viewport persistence (presentation only). */
  viewportFrom: number | null;
  viewportTo: number | null;
};

export type CandleBar = {
  time: number; // unix seconds UTC
  open: number;
  high: number;
  low: number;
  close: number;
  volume?: number | null;
  source?: string | null;
};

export type ChartLoadState = "idle" | "loading" | "ready" | "empty" | "error";

export const DEFAULT_CHART_STATE: ChartState = {
  symbol: "EURUSD",
  timeframe: "M1",
  chartType: "candlestick",
  viewportFrom: null,
  viewportTo: null,
};

export const AVAILABLE_SYMBOLS = ["EURUSD", "BTCUSD"] as const;
export const AVAILABLE_TIMEFRAMES: ChartTimeframe[] = ["M1", "M5", "H1", "D1"];

export function parseCandleTime(iso: string): number {
  const ms = Date.parse(iso);
  if (Number.isNaN(ms)) return 0;
  return Math.floor(ms / 1000);
}

export function apiCandleToBar(c: {
  open_time: string;
  open: string;
  high: string;
  low: string;
  close: string;
  volume?: string | null;
}): CandleBar {
  return {
    time: parseCandleTime(c.open_time),
    open: Number(c.open),
    high: Number(c.high),
    low: Number(c.low),
    close: Number(c.close),
    volume: c.volume != null ? Number(c.volume) : null,
  };
}

/** Merge live candle into series: update forming bar or append new bar. */
export function mergeLiveBar(series: CandleBar[], bar: CandleBar): CandleBar[] {
  if (series.length === 0) return [bar];
  const last = series[series.length - 1];
  if (bar.time === last.time) {
    const next = series.slice(0, -1);
    next.push(bar);
    return next;
  }
  if (bar.time > last.time) {
    return [...series, bar];
  }
  // Out-of-order older bar: ignore for live path (historical reload handles corrections)
  return series;
}
