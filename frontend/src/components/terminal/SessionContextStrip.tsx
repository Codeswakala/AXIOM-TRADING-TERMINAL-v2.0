/**
 * DATA-P02 M7 — session context strip.
 *
 * Presentation and labelling over existing data only: shows the CURRENT UTC
 * session state (active sessions, overlap period, weekend closure) and the
 * session of the bar under the crosshair — or, without a hover, the session
 * span of the visible series. No generator, seeding or walk behaviour is
 * touched.
 */

import { useEffect, useState } from "react";
import type { CandleBar } from "../../chart/types";
import {
  overlapPeriodLabel,
  sessionLabelOfBar,
  sessionLabelOfTime,
  sessionsAtTime,
  utcClockLabel,
} from "../../terminal/sessions";

export interface SessionContextStripProps {
  bars: CandleBar[];
  hoveredBar: CandleBar | null;
}

export function SessionContextStrip({ bars, hoveredBar }: SessionContextStripProps) {
  const [now, setNow] = useState<Date>(() => new Date());

  useEffect(() => {
    const id = window.setInterval(() => setNow(new Date()), 30_000);
    return () => window.clearInterval(id);
  }, []);

  const active = sessionsAtTime(now);
  const firstSession = bars.length > 0 ? sessionLabelOfBar(bars[0].time) : null;
  const lastSession = bars.length > 0 ? sessionLabelOfBar(bars[bars.length - 1].time) : null;

  return (
    <div className="chart-session-strip" data-testid="chart-session-strip" role="status">
      <span className="session-strip-lbl mono">SESSION CONTEXT</span>
      <span className="session-clock mono" data-testid="session-clock">
        {utcClockLabel(now)} UTC
      </span>
      <span className="session-current" data-testid="session-current">
        {sessionLabelOfTime(now)}
      </span>
      {active.length === 2 ? (
        <span className="session-overlap mono" data-testid="session-overlap">
          overlap {overlapPeriodLabel(active[0].id, active[1].id)}
        </span>
      ) : null}
      {hoveredBar ? (
        <span className="session-bar mono" data-testid="session-hovered-bar">
          BAR {utcClockLabel(new Date(hoveredBar.time * 1000))} UTC — {sessionLabelOfBar(hoveredBar.time)}
        </span>
      ) : firstSession && lastSession ? (
        <span className="session-span mono" data-testid="session-series-span">
          series {firstSession} → {lastSession}
        </span>
      ) : null}
    </div>
  );
}
