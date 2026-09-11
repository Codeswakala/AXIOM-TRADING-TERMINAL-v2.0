/**
 * CHART-P03 drawing tools — types, tool registry, and the label-vocabulary
 * guards.
 *
 * M1: every drawing persists (price, time) handles — never pixels, never
 * percentages. Pixels exist only momentarily at conversion time.
 * M5/M10: drawing labels are inert research text; the actuation vocabulary
 * (shared with the annotation guard) and the institutional/directional
 * vocabulary live HERE, outside the chart stage source, so the stage's
 * source-residue guard checks remain meaningful.
 */

export type DrawingToolId = "trendline" | "hline" | "ray" | "rect" | "fib" | "text";

export interface DrawingToolDefinition {
  id: DrawingToolId;
  label: string;
  handles: 1 | 2;
  description: string;
}

export const DRAWING_TOOLS: readonly DrawingToolDefinition[] = [
  { id: "trendline", label: "Trendline", handles: 2, description: "Line between two price/time anchors" },
  { id: "hline", label: "H Line", handles: 1, description: "Horizontal line at one price level" },
  { id: "ray", label: "Ray", handles: 2, description: "Line extended beyond the second anchor" },
  { id: "rect", label: "Rectangle", handles: 2, description: "Zone between two price/time anchors" },
  { id: "fib", label: "Fibonacci", handles: 2, description: "Retracement levels between two anchors — geometry only, no trade semantics" },
  { id: "text", label: "Text Note", handles: 1, description: "Anchored research note" },
] as const;

export function drawingToolOf(id: string): DrawingToolDefinition | undefined {
  return DRAWING_TOOLS.find((t) => t.id === id);
}

export interface DrawingHandle {
  /** Instrument price at the anchor — the persisted, meaning-bearing value. */
  price: number;
  /** Epoch seconds UTC at the anchor. */
  time: number;
}

export interface ChartDrawing {
  id: string;
  kind: DrawingToolId;
  handles: DrawingHandle[];
  label?: string;
  /** true when the annotation row predates price/time anchoring. */
  legacy?: boolean;
}

/** Geometry persistence contract (M6): content.geometry on the existing
 * chart_research_annotation artifact. */
export interface DrawingGeometry {
  kind: DrawingToolId;
  handles: Array<{ price: number; time_iso: string }>;
  label?: string;
}

/** M5: actuation vocabulary — drawing labels inherit the annotation guard. */
export const DRAWING_FORBIDDEN_LABEL_TERMS = [
  "entry",
  "stop_loss",
  "take_profit",
  "position_size",
  "lot",
  "order",
  "risk_reward",
  "setup",
] as const;

/** M10: institutional-claim and directional-folk vocabulary. The geometry is
 * real; the narrative is refused. */
export const STRUCTURE_FORBIDDEN_TERMS = [
  "institutional order",
  "smart money",
  "accumulation zone",
  "distribution zone",
  "entry zone",
  "golden pocket",
  "buy signal",
  "sell signal",
  "golden cross",
  "death cross",
  "crossover signal",
  "bullish",
  "bearish",
  "oversold",
  "overbought",
  "trade recommendation",
  "eligibility",
  "setup quality",
  "risk/reward",
] as const;

export function drawingLabelRejection(label: string): string | null {
  const lower = label.toLowerCase();
  for (const term of DRAWING_FORBIDDEN_LABEL_TERMS) {
    if (lower.includes(term)) return term;
  }
  return null;
}
