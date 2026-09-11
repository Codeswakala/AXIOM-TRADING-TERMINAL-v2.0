/**
 * POLISH-P01 M5 — the confluence strip (evidence aggregation surface).
 *
 * Renders the score with its uncertainty band, the NON-ACTUATING label, and
 * the statement that this aggregates the operator's ACTIVE indicators over
 * SIMULATED data — it is not a market opinion. No eligibility, no risk/reward,
 * no verdict: the vocabulary is refused at source and at render (M7).
 */

import { useMemo } from "react";
import type { IndicatorResult } from "../../api/client";
import { computeConfluence, NON_ACTUATING_LABEL } from "../../terminal/confluence";

export interface ConfluenceStripProps {
  indicatorResults: Record<string, IndicatorResult>;
  closeSeries: number[];
}

export function ConfluenceStrip({ indicatorResults, closeSeries }: ConfluenceStripProps) {
  const confluence = useMemo(
    () => computeConfluence(indicatorResults, closeSeries),
    [indicatorResults, closeSeries],
  );

  if (confluence.directionalCount === 0) return null;

  const percent = confluence.score != null ? (confluence.score * 100).toFixed(0) : null;

  return (
    <div className="confluence-strip" data-testid="confluence-strip" role="status">
      <span className="confluence-lbl mono">EVIDENCE CONFLUENCE</span>
      <span className="confluence-score mono" data-testid="confluence-score">
        {confluence.alignedCount} of {confluence.directionalCount} active indicators aligned{" "}
        {confluence.direction !== "none" ? `(${confluence.direction.toUpperCase()})` : ""}
        {percent !== null ? ` · score ${percent}%` : ""}
      </span>
      <span className="confluence-uncertainty mono" data-testid="confluence-uncertainty">
        uncertainty ±{confluence.uncertaintyBand.toFixed(2)} (Wilson 95%)
      </span>
      <span className="confluence-nonactuating mono" data-testid="confluence-nonactuating">
        {NON_ACTUATING_LABEL}
      </span>
      <span className="confluence-statement mono" data-testid="confluence-statement">
        Aggregates the operator's currently active indicators over simulated data — not a market
        opinion.
      </span>
      {confluence.excluded.length > 0 ? (
        <span className="confluence-excluded mono" data-testid="confluence-excluded">
          excluded from direction: {confluence.excluded.join(", ")}
        </span>
      ) : null}
    </div>
  );
}
