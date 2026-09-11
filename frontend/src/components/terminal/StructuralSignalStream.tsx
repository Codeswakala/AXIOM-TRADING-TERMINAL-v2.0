/**
 * StructuralSignalStream — the deterministic structural signal family (BO-F-02).
 *
 * Reconciliation Determination CA-RECON-2 / §13: AXIOM has TWO signal
 * families — structural (deterministic, indicator-layer derived, no ML
 * dependency) and predictive (ML, gated on a promoted model). This component
 * is the STRUCTURAL family surface: it derives discrete structure events from
 * the server-computed indicator series (SMC/ICT set), faithfully transcribing
 * non-null series markers into events — zero client-side reinterpretation,
 * zero fabricated entries.
 *
 * Honesty discipline:
 * - Every event is a descriptive observation ("structure broke up at
 *   12:00"), NEVER a prediction ("price will rise").
 * - Events exist only where the server computed a non-null marker.
 * - No entry is fabricated when the series is unavailable or empty.
 * - Non-actuating: read-only surface, no order/execution controls.
 */

import { useEffect, useMemo, useState } from "react";
import { useTerminal } from "./TerminalContext";
import {
  fetchIndicatorSeries,
  type IndicatorSeriesEnvelope,
  type MultiIndicatorResult,
} from "../../api/client";
import { timeframeCodeOf, TIMEFRAME_OPTIONS, type TimeframeCode } from "../../api/timeframes";
import "./TerminalMultiPane.css";

/** The SMC/ICT structural set (server-computed; see the X-01 hop-2 evidence). */
export const STRUCTURAL_SIGNAL_INDICATORS = [
  "BOS55",
  "CHOCH55",
  "FVG3",
  "STRUCT55",
  "SWINGS55",
] as const;

export interface StructuralSignalEvent {
  id: string;
  indicatorId: string;
  type: "BOS" | "CHoCH" | "FVG" | "STRUCTURE" | "SWING";
  direction: "up" | "down" | "zone";
  label: string;
  time: string;
  level: number | null;
  symbol: string;
  timeframe: string;
}

/** Line-name → (type, direction, descriptive label) transcription table.
 * Pure server-data transcription: a non-null point on a line IS the event. */
const LINE_EVENT_MEANING: Record<string, { type: StructuralSignalEvent["type"]; direction: "up" | "down"; label: string }> = {
  bos_up: { type: "BOS", direction: "up", label: "Break of structure upward" },
  bos_down: { type: "BOS", direction: "down", label: "Break of structure downward" },
  choch_up: { type: "CHoCH", direction: "up", label: "Change of character upward" },
  choch_down: { type: "CHoCH", direction: "down", label: "Change of character downward" },
  hh: { type: "STRUCTURE", direction: "up", label: "Higher-high structure point" },
  lh: { type: "STRUCTURE", direction: "down", label: "Lower-high structure point" },
  hl: { type: "STRUCTURE", direction: "up", label: "Higher-low structure point" },
  ll: { type: "STRUCTURE", direction: "down", label: "Lower-low structure point" },
  swing_high: { type: "SWING", direction: "up", label: "Swing high" },
  swing_low: { type: "SWING", direction: "down", label: "Swing low" },
};

export const MAX_STRUCTURAL_EVENTS = 24;

const toLevel = (value: string | null): number | null => {
  if (value === null || value === undefined || value === "") return null;
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
};

/**
 * Derive structural events from the server-computed indicator envelope.
 * Faithful transcription only: each non-null series point becomes an event.
 * FVG top/bottom edges sharing a timestamp are paired into one zone event
 * (the backend emits both edges at the bar where the zone is detected);
 * unpaired edges are emitted as single-edge markers.
 */
export function deriveStructuralEvents(
  envelope: IndicatorSeriesEnvelope,
): StructuralSignalEvent[] {
  if (envelope.seriesKind === "unavailable") return [];

  const events: StructuralSignalEvent[] = [];
  const fvgByTime = new Map<string, { top: number | null; bottom: number | null }>();

  for (const indicatorId of STRUCTURAL_SIGNAL_INDICATORS) {
    const result = envelope.indicators[indicatorId];
    if (!result || result.shape !== "multi") continue;
    const multi = result as MultiIndicatorResult;

    for (const [lineName, points] of Object.entries(multi.lines)) {
      if (indicatorId === "FVG3") {
        // Collect edges per timestamp; pairing happens after the loop.
        for (const point of points) {
          if (point.value === null || point.value === undefined) continue;
          const entry = fvgByTime.get(point.time) ?? { top: null, bottom: null };
          if (lineName === "fvg_top") entry.top = toLevel(point.value);
          if (lineName === "fvg_bottom") entry.bottom = toLevel(point.value);
          fvgByTime.set(point.time, entry);
        }
        continue;
      }

      const meaning = LINE_EVENT_MEANING[lineName];
      if (!meaning) continue; // unknown line = not transcribed (no invention)
      for (const point of points) {
        if (point.value === null || point.value === undefined) continue;
        events.push({
          id: `${indicatorId}:${lineName}:${point.time}`,
          indicatorId,
          type: meaning.type,
          direction: meaning.direction,
          label: meaning.label,
          time: point.time,
          level: toLevel(point.value),
          symbol: envelope.symbol,
          timeframe: envelope.timeframe,
        });
      }
    }
  }

  for (const [time, edges] of fvgByTime) {
    if (edges.top !== null && edges.bottom !== null) {
      events.push({
        id: `FVG3:zone:${time}`,
        indicatorId: "FVG3",
        type: "FVG",
        direction: "zone",
        label: "Fair value gap zone",
        time,
        level: null,
        symbol: envelope.symbol,
        timeframe: envelope.timeframe,
      });
    } else if (edges.top !== null) {
      events.push({
        id: `FVG3:top-edge:${time}`,
        indicatorId: "FVG3",
        type: "FVG",
        direction: "zone",
        label: "Fair value gap top edge",
        time,
        level: edges.top,
        symbol: envelope.symbol,
        timeframe: envelope.timeframe,
      });
    } else if (edges.bottom !== null) {
      events.push({
        id: `FVG3:bottom-edge:${time}`,
        indicatorId: "FVG3",
        type: "FVG",
        direction: "zone",
        label: "Fair value gap bottom edge",
        time,
        level: edges.bottom,
        symbol: envelope.symbol,
        timeframe: envelope.timeframe,
      });
    }
  }

  events.sort((a, b) => (a.time < b.time ? 1 : a.time > b.time ? -1 : 0));
  return events.slice(0, MAX_STRUCTURAL_EVENTS);
}

const formatUtcTime = (iso: string): string => {
  const parsed = new Date(iso);
  if (Number.isNaN(parsed.getTime())) return iso;
  return `${parsed.toISOString().slice(0, 16).replace("T", " ")} UTC`;
};

export interface StructuralSignalStreamProps {
  className?: string;
}

export function StructuralSignalStream({ className = "" }: StructuralSignalStreamProps) {
  const { selectedSymbol } = useTerminal();
  const [timeframeLabel, setTimeframeLabel] = useState<string>("1h");
  const [events, setEvents] = useState<StructuralSignalEvent[]>([]);
  const [seriesKind, setSeriesKind] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [fetchError, setFetchError] = useState<string | null>(null);

  const symbolKey = useMemo(
    () => selectedSymbol.replace(/[^a-zA-Z0-9]/g, "").toUpperCase(),
    [selectedSymbol],
  );
  const backendCode: TimeframeCode = timeframeCodeOf(timeframeLabel);

  useEffect(() => {
    let cancelled = false;
    async function loadStructuralEvents() {
      setIsLoading(true);
      setFetchError(null);
      try {
        const envelope = await fetchIndicatorSeries({
          symbol: symbolKey,
          timeframe: backendCode,
          indicators: [...STRUCTURAL_SIGNAL_INDICATORS],
        });
        if (cancelled) return;
        setSeriesKind(envelope.seriesKind);
        setEvents(deriveStructuralEvents(envelope));
      } catch (err) {
        if (cancelled) return;
        setSeriesKind(null);
        setEvents([]);
        setFetchError(err instanceof Error ? err.message : "Indicator series request failed");
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    }
    void loadStructuralEvents();
    return () => {
      cancelled = true;
    };
  }, [symbolKey, backendCode]);

  return (
    <div
      className={`structural-signal-stream ${className}`}
      data-testid="structural-signal-stream"
      role="region"
      aria-label="Structural Signal Stream"
    >
      <div className="stream-header">
        <div className="stream-title-row">
          <span className="stream-title">STRUCTURAL SIGNALS</span>
          <span className="stream-count-badge mono" data-testid="structural-count-badge">
            {events.length} EVENTS
          </span>
        </div>
        <div className="stream-disclaimer-chip" data-testid="structural-descriptive-framing">
          <span>DETERMINISTIC · DESCRIPTIVE — NOT A PREDICTION</span>
        </div>
      </div>

      <div className="stream-filter-bar" role="tablist" aria-label="Structural Timeframe">
        {TIMEFRAME_OPTIONS.map((option) => (
          <button
            key={option.label}
            type="button"
            role="tab"
            aria-selected={timeframeLabel === option.label}
            className={`stream-filter-btn mono ${timeframeLabel === option.label ? "active" : ""}`}
            onClick={() => setTimeframeLabel(option.label)}
            data-testid={`structural-tf-${option.label}`}
          >
            {option.label.toUpperCase()}
          </button>
        ))}
      </div>

      {seriesKind && seriesKind !== "unavailable" && !isLoading && !fetchError && (
        <div className="structural-provenance" data-testid="structural-provenance-line">
          <span className="mono">
            Derived from server-computed indicator series · {envelopeSymbolLabel(symbolKey)}{" "}
            {backendCode} · series kind: {seriesKind}
          </span>
        </div>
      )}

      <div className="signals-cards-list" role="list" aria-label="Structural Signal Events">
        {isLoading ? (
          <div className="signal-empty-msg loading" data-testid="structural-loading-state">
            <span>Computing structural events from the indicator series…</span>
          </div>
        ) : fetchError ? (
          <div className="signal-empty-msg error" data-testid="structural-error-state">
            <span>Structural series unavailable: {fetchError}</span>
          </div>
        ) : events.length === 0 ? (
          <div className="signal-empty-msg empty" data-testid="structural-empty-state">
            <span>
              {seriesKind === "unavailable"
                ? `No structure events — the indicator series is unavailable for ${envelopeSymbolLabel(symbolKey)} ${backendCode}.`
                : "No structure events in the current window."}
            </span>
            <small>Structure events appear only where the server computed a marker.</small>
          </div>
        ) : (
          events.map((event) => (
            <div
              key={event.id}
              role="listitem"
              className={`signal-card structural-event-card ${event.direction}`}
              data-testid={`structural-event-${event.id}`}
            >
              <div className="signal-card-header">
                <div className="signal-header-left">
                  <span className="signal-symbol-badge mono">{event.type}</span>
                  <span
                    className={`signal-direction-badge ${
                      event.direction === "up"
                        ? "positive"
                        : event.direction === "down"
                          ? "negative"
                          : "neutral"
                    } mono`}
                    data-testid={`structural-direction-${event.id}`}
                  >
                    {event.direction.toUpperCase()}
                  </span>
                </div>
                <div className="signal-header-right">
                  <span className="signal-as-of mono">{formatUtcTime(event.time)}</span>
                </div>
              </div>

              <div className="structural-event-body">
                <span className="structural-event-label" data-testid={`structural-label-${event.id}`}>
                  {event.label}
                </span>
                {event.level !== null && (
                  <span className="structural-event-level mono" data-testid={`structural-level-${event.id}`}>
                    level {event.level}
                  </span>
                )}
              </div>

              <div className="signal-meta-row">
                <span className="signal-tf-badge mono">{envelopeSymbolLabel(symbolKey)}</span>
                <span className="signal-tf-badge mono">{backendCode}</span>
                <span className="signal-freshness-tag mono">DESCRIPTIVE</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

/** Human symbol label for provenance lines (never invents a symbol). */
function envelopeSymbolLabel(symbolKey: string): string {
  return symbolKey;
}
