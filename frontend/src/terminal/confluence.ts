/**
 * POLISH-P01 M5 — Confluence as EVIDENCE AGGREGATION, evidence-only
 * (Operator decision).
 *
 * Counts how many of the operator's CURRENTLY ACTIVE indicators are
 * directionally aligned, presented as a score with an uncertainty band and
 * the NON-ACTUATING label — the Advisory Signals precedent exactly:
 * calibrated numbers, stated uncertainty, no instruction.
 *
 * EXPLICITLY NOT HERE (constitutionally refused): Trade Eligibility,
 * Risk/Reward, Setup Quality as a recommendation, entry/stop/target output,
 * and the folk directional vocabulary. The geometry is described; the
 * narrative is refused. The guard vocabulary for that refusal lives in
 * CONFLUENCE_FORBIDDEN_TERMS (asserted at source and at render).
 *
 * Direction classification (declared, one rule per indicator type):
 *   SMA20/SMA50/EMA20/HMA20 — last value vs value 5 bars earlier (slope).
 *   BBANDS201/KELTNER20/DONCHIAN20 — last close vs the middle line
 *                                   (requires the close series).
 *   RSI14 — last value vs 50.        MACD12269 — histogram sign.
 *   STOCH1433 — %K vs 50 (a momentum stance, NOT a crossover signal).
 *   CCI20 / ROC12 — sign of the last value.
 * EXCLUDED (declared, not silent): ADX14 and ATR14 (strength/volatility,
 * not direction); Supertrend (band-locking bands — no direction claim);
 * Ichimoku (multi-component; the folk tenkan/kijun signal is refused);
 * the four level families and the six structure detections (zones and
 * references, not directions); Z-Score/Percentile/Regression (not
 * directional).
 *
 * Uncertainty model (declared): Wilson 95% half-width on the aligned
 * proportion, z = 1.96, band = z * sqrt(p*(1-p)/n). Honest at small n;
 * never a fabricated precision.
 */

import type { IndicatorResult } from "../api/client";

export const NON_ACTUATING_LABEL = "NON-ACTUATING — evidence aggregation only";

export const CONFLUENCE_FORBIDDEN_TERMS = [
  "eligible",
  "eligibility",
  "risk/reward",
  "r:r",
  "setup quality",
  "take the trade",
  "high probability setup",
  "trade recommendation",
  "buy signal",
  "sell signal",
  "golden cross",
  "death cross",
  "crossover signal",
  "bullish",
  "bearish",
  "oversold",
  "overbought",
  "institutional order",
  "smart money",
  "accumulation zone",
  "distribution zone",
  "entry zone",
] as const;

export interface ConfluenceResult {
  direction: "up" | "down" | "none";
  alignedCount: number;
  directionalCount: number;
  /** aligned / directional, or null when nothing is directional. */
  score: number | null;
  /** Wilson 95% half-width on the aligned proportion (0 when n < 2). */
  uncertaintyBand: number;
  /** Registry ids present in the input but excluded from direction. */
  excluded: string[];
}

const SLOPE_LOOKBACK = 5;
const WILSON_Z = 1.96;

function lastLineValue(result: IndicatorResult, name?: string): number | null {
  if (result.shape === "line") {
    const pts = result.points.filter((p) => p.value !== null);
    return pts.length > 0 ? Number(pts[pts.length - 1].value) : null;
  }
  if (result.shape === "multi" && name) {
    const pts = (result.lines[name] ?? []).filter((p) => p.value !== null);
    return pts.length > 0 ? Number(pts[pts.length - 1].value) : null;
  }
  return null;
}

function slopeDirection(result: IndicatorResult): "up" | "down" | null {
  if (result.shape !== "line") return null;
  const pts = result.points.filter((p) => p.value !== null);
  if (pts.length < 2) return null;
  const last = Number(pts[pts.length - 1].value);
  const referenceIndex = Math.max(0, pts.length - 1 - SLOPE_LOOKBACK);
  const reference = Number(pts[referenceIndex].value);
  if (last > reference) return "up";
  if (last < reference) return "down";
  return null;
}

export function computeConfluence(
  results: Record<string, IndicatorResult>,
  closeSeries: number[] = [],
): ConfluenceResult {
  const directions: Array<{ id: string; direction: "up" | "down" }> = [];
  const excluded: string[] = [];

  for (const id of Object.keys(results)) {
    const result = results[id];
    if (!result || result.shape === "insufficient") continue;
    let direction: "up" | "down" | null = null;

    switch (id) {
      case "SMA20":
      case "SMA50":
      case "EMA20":
      case "HMA20":
        direction = slopeDirection(result);
        break;
      case "BBANDS201":
      case "KELTNER20":
      case "DONCHIAN20": {
        const middle = lastLineValue(result, "middle");
        const close = closeSeries.length > 0 ? closeSeries[closeSeries.length - 1] : null;
        if (middle === null || close === null) {
          excluded.push(id);
          continue;
        }
        direction = close > middle ? "up" : close < middle ? "down" : null;
        break;
      }
      case "RSI14": {
        const v = lastLineValue(result);
        direction = v === null ? null : v > 50 ? "up" : v < 50 ? "down" : null;
        break;
      }
      case "MACD12269": {
        if (result.shape !== "macd") continue;
        const pts = result.points.filter((p) => p.histogram !== null);
        if (pts.length === 0) {
          excluded.push(id);
          continue;
        }
        const h = Number(pts[pts.length - 1].histogram);
        direction = h > 0 ? "up" : h < 0 ? "down" : null;
        break;
      }
      case "STOCH1433": {
        const v = lastLineValue(result, "percent_k");
        direction = v === null ? null : v > 50 ? "up" : v < 50 ? "down" : null;
        break;
      }
      case "CCI20":
      case "ROC12": {
        const v = lastLineValue(result);
        direction = v === null ? null : v > 0 ? "up" : v < 0 ? "down" : null;
        break;
      }
      default:
        excluded.push(id);
        continue;
    }
    if (direction) directions.push({ id, direction });
  }

  const total = directions.length;
  const up = directions.filter((d) => d.direction === "up").length;
  const down = total - up;
  const aligned = Math.max(up, down);
  const score = total > 0 ? aligned / total : null;
  const p = score ?? 0.5;
  const band = total > 1 ? WILSON_Z * Math.sqrt((p * (1 - p)) / total) : 0;
  const direction: "up" | "down" | "none" =
    total === 0 ? "none" : up > down ? "up" : down > up ? "down" : "none";

  return {
    direction,
    alignedCount: total > 0 ? aligned : 0,
    directionalCount: total,
    score,
    uncertaintyBand: band,
    excluded,
  };
}
