/**
 * DATA-P02 S2 — single source of truth for the timeframe vocabulary.
 *
 * The backend owns the canonical vocabulary (app/services/timeframes.py) and
 * validates every request against it (an unknown code is a 422, failing
 * loudly, never silently). This module mirrors the identical golden table —
 * the same six (label, code, minutes) triples — and BOTH sides pin their
 * tables with tests. A divergence between the two maps cannot silently
 * render: it either fails a golden test or fails the API pattern check.
 */

export type TimeframeCode = "M1" | "M5" | "M15" | "H1" | "H4" | "D1";

export interface TimeframeOption {
  label: string;
  code: TimeframeCode;
  minutes: number;
}

export const TIMEFRAME_OPTIONS: readonly TimeframeOption[] = [
  { label: "1m", code: "M1", minutes: 1 },
  { label: "5m", code: "M5", minutes: 5 },
  { label: "15m", code: "M15", minutes: 15 },
  { label: "1h", code: "H1", minutes: 60 },
  { label: "4h", code: "H4", minutes: 240 },
  { label: "1d", code: "D1", minutes: 1440 },
] as const;

const LABEL_TO_CODE = new Map(TIMEFRAME_OPTIONS.map((t) => [t.label, t.code]));
const CODE_TO_MINUTES = new Map(TIMEFRAME_OPTIONS.map((t) => [t.code, t.minutes]));

export function timeframeCodeOf(label: string): TimeframeCode {
  const code = LABEL_TO_CODE.get(label);
  if (!code) {
    throw new Error(`Unknown timeframe label: ${label}`);
  }
  return code;
}

export function timeframeMinutesOf(code: TimeframeCode): number {
  const minutes = CODE_TO_MINUTES.get(code);
  if (minutes === undefined) {
    throw new Error(`Unknown timeframe code: ${code}`);
  }
  return minutes;
}

export function isAggregatedCode(code: string): boolean {
  return code === "M5" || code === "M15" || code === "H1" || code === "H4" || code === "D1";
}
