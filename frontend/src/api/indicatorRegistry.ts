/**
 * CHART-P02 S1 — frontend mirror of the backend indicator registry, now
 * carrying the engine/category field so toolbar grouping is DATA-DRIVEN,
 * never a hardcoded UI list. Pinned to the backend golden table by tests on
 * both sides — a divergence cannot silently render.
 */

export type IndicatorPane = "overlay" | "pane";

export const ENGINES = [
  "Trend",
  "Momentum",
  "Volatility",
  "Levels",
  "Statistics",
  "MarketStructure",
] as const;
export type IndicatorEngine = (typeof ENGINES)[number];

export interface IndicatorUiDefinition {
  id: string;
  label: string;
  pane: IndicatorPane;
  engine: IndicatorEngine;
  testid: string;
}

export const INDICATOR_UI: readonly IndicatorUiDefinition[] = [
  { id: "SMA20", label: "SMA 20", pane: "overlay", engine: "Trend", testid: "overlay-sma20" },
  { id: "SMA50", label: "SMA 50", pane: "overlay", engine: "Trend", testid: "overlay-sma50" },
  { id: "EMA20", label: "EMA 20", pane: "overlay", engine: "Trend", testid: "overlay-ema20" },
  { id: "RSI14", label: "RSI 14", pane: "pane", engine: "Momentum", testid: "indicator-rsi14" },
  { id: "MACD12269", label: "MACD", pane: "pane", engine: "Momentum", testid: "indicator-macd12269" },
  { id: "BBANDS201", label: "Bollinger", pane: "overlay", engine: "Volatility", testid: "indicator-bbands201" },
  { id: "ATR14", label: "ATR 14", pane: "pane", engine: "Volatility", testid: "indicator-atr14" },
  // --- CHART-P02 breadth ---
  { id: "HMA20", label: "HMA 20", pane: "overlay", engine: "Trend", testid: "indicator-hma20" },
  { id: "SUPERTREND103", label: "Supertrend", pane: "overlay", engine: "Trend", testid: "indicator-supertrend103" },
  { id: "ICHIMOKU952652", label: "Ichimoku", pane: "overlay", engine: "Trend", testid: "indicator-ichimoku952652" },
  { id: "STOCH1433", label: "Stochastic", pane: "pane", engine: "Momentum", testid: "indicator-stoch1433" },
  { id: "CCI20", label: "CCI 20", pane: "pane", engine: "Momentum", testid: "indicator-cci20" },
  { id: "ROC12", label: "ROC 12", pane: "pane", engine: "Momentum", testid: "indicator-roc12" },
  { id: "ADX14", label: "ADX/DMI", pane: "pane", engine: "Momentum", testid: "indicator-adx14" },
  { id: "KELTNER20", label: "Keltner", pane: "overlay", engine: "Volatility", testid: "indicator-keltner20" },
  { id: "DONCHIAN20", label: "Donchian", pane: "overlay", engine: "Volatility", testid: "indicator-donchian20" },
  { id: "PIVOTCL", label: "Pivots", pane: "overlay", engine: "Levels", testid: "indicator-pivotcl" },
  { id: "CAMARILLA", label: "Camarilla", pane: "overlay", engine: "Levels", testid: "indicator-camarilla" },
  { id: "PREVHL", label: "Prev H/L", pane: "overlay", engine: "Levels", testid: "indicator-prevhl" },
  { id: "SESSLVL", label: "Session Lvls", pane: "overlay", engine: "Levels", testid: "indicator-sesslvl" },
  { id: "ZSCORE20", label: "Z-Score", pane: "overlay", engine: "Statistics", testid: "indicator-zscore20" },
  { id: "PCTRANK20", label: "Percentile", pane: "overlay", engine: "Statistics", testid: "indicator-pctrank20" },
  { id: "REGCHAN20", label: "Reg Chan", pane: "overlay", engine: "Statistics", testid: "indicator-regchan20" },
  // CHART-P03 — geometric pattern detections (M8: simulated-data disclosure
  // mandatory; never evidence of institutional activity).
  { id: "SWINGS55", label: "Swings", pane: "overlay", engine: "MarketStructure", testid: "indicator-swings55" },
  { id: "STRUCT55", label: "HH/HL/LH/LL", pane: "overlay", engine: "MarketStructure", testid: "indicator-struct55" },
  { id: "BOS55", label: "BOS", pane: "overlay", engine: "MarketStructure", testid: "indicator-bos55" },
  { id: "CHOCH55", label: "CHoCH", pane: "overlay", engine: "MarketStructure", testid: "indicator-choch55" },
  { id: "FVG3", label: "FVG", pane: "overlay", engine: "MarketStructure", testid: "indicator-fvg3" },
  { id: "OBPATTERN", label: "Order Blocks (Pattern)", pane: "overlay", engine: "MarketStructure", testid: "indicator-obpattern" },
] as const;

export function overlayIndicators(): string[] {
  return INDICATOR_UI.filter((i) => i.pane === "overlay").map((i) => i.id);
}

export function paneIndicators(): string[] {
  return INDICATOR_UI.filter((i) => i.pane === "pane").map((i) => i.id);
}

export function indicatorUiOf(id: string): IndicatorUiDefinition | undefined {
  return INDICATOR_UI.find((i) => i.id === id);
}

export function engineOf(id: string): IndicatorEngine | undefined {
  return indicatorUiOf(id)?.engine;
}

/** M8 disclosure: rendered in the product whenever a structure indicator is
 * active. Geometric detections over simulated OHLC — NOT institutional. */
export const MARKET_STRUCTURE_DISCLOSURE =
  "Geometric pattern detection over simulated OHLC — not evidence of institutional activity or order placement.";

/** The three most-used indicators stay direct pills (M5: no more interactions
 * than today). */
export const DIRECT_PILL_IDS = ["SMA20", "SMA50", "EMA20"] as const;

/**
 * CHART-P02 S2 — overlay line palette: a fixed set of CSS tokens crossed with
 * line styles gives 24 distinguishable (colour, style) combinations; lines are
 * assigned deterministically from (indicator id, line name) so the same line
 * always renders identically. Full collision-avoidance at 20+ concurrent
 * lines is not achievable within the token palette — the deterministic
 * assignment plus the status strip labels are the stated mitigation.
 */
export const OVERLAY_LINE_PALETTE: ReadonlyArray<{ colorToken: string; style: 0 | 1 | 2 }> = [
  { colorToken: "--ix-color-electric-blue", style: 0 },
  { colorToken: "--ix-color-warning-amber", style: 0 },
  { colorToken: "--ix-color-accent", style: 0 },
  { colorToken: "--ix-color-success-green", style: 0 },
  { colorToken: "--ix-color-critical-red", style: 0 },
  { colorToken: "--ix-text-muted", style: 0 },
  { colorToken: "--ix-color-electric-blue", style: 2 },
  { colorToken: "--ix-color-warning-amber", style: 2 },
  { colorToken: "--ix-color-accent", style: 2 },
  { colorToken: "--ix-color-success-green", style: 2 },
  { colorToken: "--ix-color-critical-red", style: 2 },
  { colorToken: "--ix-text-muted", style: 2 },
  { colorToken: "--ix-color-electric-blue", style: 1 },
  { colorToken: "--ix-color-warning-amber", style: 1 },
  { colorToken: "--ix-color-accent", style: 1 },
  { colorToken: "--ix-color-success-green", style: 1 },
  { colorToken: "--ix-color-critical-red", style: 1 },
  { colorToken: "--ix-text-muted", style: 1 },
  { colorToken: "--ix-color-electric-blue", style: 1 },
  { colorToken: "--ix-color-warning-amber", style: 1 },
  { colorToken: "--ix-color-accent", style: 1 },
  { colorToken: "--ix-color-success-green", style: 1 },
  { colorToken: "--ix-color-critical-red", style: 1 },
  { colorToken: "--ix-text-muted", style: 1 },
];

export function paletteEntryFor(key: string): { colorToken: string; style: 0 | 1 | 2 } {
  let hash = 0;
  for (let i = 0; i < key.length; i++) {
    hash = (hash * 31 + key.charCodeAt(i)) >>> 0;
  }
  return OVERLAY_LINE_PALETTE[hash % OVERLAY_LINE_PALETTE.length];
}
