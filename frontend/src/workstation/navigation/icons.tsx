/**
 * BO-F-06.1 — semantic workspace icon set (2026-08-22).
 *
 * The registry's pre-F-06 icons were cryptic Unicode glyphs
 * (● ◌ ⌁ ◇ ▦ ◆ …) — not self-explanatory (Blueprint §8 Addendum, Operator
 * binding). This module provides a curated inline-SVG set, one semantic key
 * per workspace, with:
 *
 *   - stroke="currentColor", no hardcoded colors → every SVG inherits the
 *     active F-00 theme's text/accent color automatically (six-theme
 *     consistent by construction);
 *   - no new runtime dependency (Doc 09 §12);
 *   - a raw-text fallback for unknown keys (never blanks);
 *   - `RAIL_SHORT_LABELS`: the visible under-icon label per workspace id —
 *     the collapsed rail's at-a-glance legibility (with the displayName as
 *     the fallback, so nothing is ever unlabeled).
 */

import type { ReactNode } from "react";

export interface WorkspaceIconProps {
  icon: string;
  className?: string;
}

const SVG_PATHS: Record<string, ReactNode> = {
  operations: (
    <>
      <path d="M2.5 4h3l1.2 8h6.1l1.1-5.5H7.5" />
      <rect x="2.5" y="2" width="4" height="1.6" rx="0.8" />
      <circle cx="12.2" cy="6" r="1.1" />
    </>
  ),
  "live-market": (
    <>
      <circle cx="8" cy="8" r="5.6" />
      <path d="M8 8h3.4" />
      <path d="M2.4 8h2M8 2.4v2" />
      <path d="M8 11.6v1.8M11.6 8h1.8" />
    </>
  ),
  charts: (
    <>
      <path d="M3 11v2.4M3 13.4h10" />
      <path d="M6.4 13.4V7.2M8 7.2v2.4h-1M9.6 13.4V4.6M11.2 4.6v2h-1" />
      <path d="M12.8 13.4V9.2" />
    </>
  ),
  signals: (
    <>
      <circle cx="8" cy="8" r="1.4" />
      <path d="M3.4 3.4a6.5 6.5 0 0 0 0 9.2M12.6 3.4a6.5 6.5 0 0 1 0 9.2" />
      <path d="M5.2 5.2a4 4 0 0 0 0 5.6M10.8 5.2a4 4 0 0 1 0 5.6" />
    </>
  ),
  analytics: (
    <>
      <path d="M2.5 13.4h11" />
      <rect x="3.6" y="9" width="2" height="4.4" />
      <rect x="7" y="5.6" width="2" height="7.8" />
      <rect x="10.4" y="7.6" width="2" height="5.8" />
    </>
  ),
  intelligence: (
    <>
      <path d="M8 2.4l2.6 2.2-1 3.1h-3.2l-1-3.1z" />
      <path d="M8 12.4l2.6-2.2 3.1 1v3.2h-11.4v-3.2l3.1-1z" />
    </>
  ),
  investigation: (
    <>
      <circle cx="7" cy="7" r="4.2" />
      <path d="M10.4 10.4L14 14" />
    </>
  ),
  scenarios: (
    <>
      <circle cx="4.6" cy="11.4" r="2" />
      <circle cx="11.4" cy="4.6" r="2" />
      <path d="M6 10.2l3.4-4.4" />
    </>
  ),
  plans: (
    <>
      <path d="M4 2.6h8v10.8H4z" />
      <path d="M6.2 5.2h3.6M6.2 8h3.6M6.2 10.8h2" />
    </>
  ),
  execution: (
    <>
      <path d="M4.6 2.8h6.8v3.4" />
      <path d="M7.6 6.2v5.8" />
      <path d="M3.4 10h8.4" />
    </>
  ),
  portfolio: (
    <>
      <circle cx="8" cy="8" r="5.6" />
      <path d="M8 2.4V8l3.4 3" />
    </>
  ),
  journal: (
    <>
      <path d="M3.4 2.6h7v10.8h-7z" />
      <path d="M10.4 4.4h2.2v9h-9" />
      <path d="M5.6 5.6h2.6M5.6 8h2.6" />
    </>
  ),
  artifacts: (
    <>
      <path d="M2.8 3h10.4v3.2H2.8z" />
      <path d="M3.8 6.2h8.4v7H3.8z" />
      <path d="M6 9h4" />
    </>
  ),
  governance: (
    <>
      <path d="M8 2.2l5 1.8v3.4c0 3-2.1 5.6-5 6.4-2.9-.8-5-3.4-5-6.4V4z" />
      <path d="M5.8 8l1.6 1.6 2.8-3" />
    </>
  ),
  alerts: (
    <>
      <path d="M4.2 12.6v-.9c0-1.7 1.1-3.1 2.7-3.6V7c0-.6.5-1.1 1.1-1.1S9.1 6.4 9.1 7v1.1c1.6.5 2.7 1.9 2.7 3.6v.9z" />
      <path d="M5.8 12.6h4.4" />
      <path d="M7 14h2" />
    </>
  ),
  settings: (
    <>
      <circle cx="8" cy="8" r="2" />
      <path d="M8 2.6v1.8M8 11.6v1.8M13.4 8h-1.8M4.4 8H2.6" />
      <path d="M11.8 4.2l-1.3 1.3M5.5 10.5l-1.3 1.3M11.8 11.8l-1.3-1.3M5.5 5.5L4.2 4.2" />
    </>
  ),
};

const FALLBACK_ICONS: Record<string, string> = {
  "": "▪",
};

/** BO-F-06.1 — the visible under-icon label per workspace id. */
export const RAIL_SHORT_LABELS: Record<string, string> = {
  "monitor.operations": "Operations",
  "monitor.live_market": "Live",
  "monitor.chart_workspace": "Charts",
  "monitor.chart_alias": "Charts",
  "research.advisory_signals": "Signals",
  "research.analytics": "Analytics",
  "research.intelligence": "Intel",
  "investigate.signal_investigation": "Investigate",
  "compare.scenarios": "Scenarios",
  "plan.trade_plans": "Plans",
  "plan.execution_research": "Execution",
  "review.portfolio_research": "Portfolio",
  "review.journal": "Journal",
  "review.research_management": "Artifacts",
  "govern.governance_evidence": "Governance",
  "settings.workspace": "Settings",
};

/** BO-F-06.1 — short label for a workspace id (displayName fallback). */
export function railShortLabel(workspaceId: string, displayName: string): string {
  return RAIL_SHORT_LABELS[workspaceId] ?? displayName;
}

/** BO-F-06.1 — the semantic icon renderer (inline SVG, currentColor stroke). */
export function WorkspaceIcon({ icon, className = "" }: WorkspaceIconProps) {
  const paths = SVG_PATHS[icon];
  if (!paths) {
    // Unknown key: render the raw value (fallback — never blank).
    return (
      <span className={`workspace-icon-fallback ${className}`} aria-hidden="true">
        {icon || FALLBACK_ICONS[""]}
      </span>
    );
  }
  return (
    <svg
      className={`workspace-icon ${className}`}
      viewBox="0 0 16 16"
      width={16}
      height={16}
      aria-hidden="true"
      focusable="false"
    >
      <g
        fill="none"
        stroke="currentColor"
        strokeWidth={1.5}
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        {paths}
      </g>
    </svg>
  );
}
