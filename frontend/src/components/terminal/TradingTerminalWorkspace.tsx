import { lazy, Suspense, useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { TerminalProvider, useTerminal } from "./TerminalContext";
import { TerminalMultiPaneLayout } from "./TerminalMultiPaneLayout";
import { TerminalTopTicker, type TickerMarketData, type WebSocketFeedStatus } from "./TerminalTopTicker";
import { TerminalWatchlistDock } from "./TerminalWatchlistDock";
import { TerminalChartStage } from "./TerminalChartStage";
import { TerminalMarketTelemetry } from "./TerminalMarketTelemetry";
import { TerminalSignalStream } from "./TerminalSignalStream";
import { TerminalIntelligenceCards } from "./TerminalIntelligenceCards";
import { TerminalBottomDock, type BottomDockTab } from "./TerminalBottomDock";
// POLISH-P01 M2: the research and execution stage views are lazy-loaded —
// they are the heaviest single contributors (ResearchHubView ~64 kB) and are
// reachable only via the stage-view query branches.
const ResearchHubView = lazy(() =>
  import("./research/ResearchHubView").then((m) => ({ default: m.ResearchHubView })),
);
const ExecutionResearchView = lazy(() =>
  import("./execution/ExecutionResearchView").then((m) => ({
    default: m.ExecutionResearchView,
  })),
);
import { TerminalAlertsDock } from "./TerminalAlertsDock";
import "./TerminalMultiPane.css";

export type RightDockView = "SIGNALS" | "TELEMETRY" | "INTELLIGENCE" | "ALERTS";

export interface TradingTerminalWorkspaceProps {
  initialSymbol?: string;
  className?: string;
  enableLiveMarket?: boolean;
  initialRightView?: RightDockView;
}

function useSafeLocation() {
  try {
    return useLocation();
  } catch {
    return null;
  }
}

function getDockFromSearch(search: string | undefined, fallback: RightDockView): RightDockView {
  if (!search) return fallback;
  try {
    const params = new URLSearchParams(search);
    const dock = params.get("dock")?.toUpperCase();
    if (
      dock === "SIGNALS" ||
      dock === "TELEMETRY" ||
      dock === "INTELLIGENCE" ||
      dock === "ALERTS"
    ) {
      return dock as RightDockView;
    }
  } catch {
    // Fallback
  }
  return fallback;
}

/**
 * UI-CONV-P03 / SURF-P01: `view` parameter parsing (discharges OBS-CONV2-7).
 *
 * CONV-P02 shipped ChartWorkspaceRedirect -> /?view=chart but nothing parsed
 * `view`, making the parameter decorative (tolerable only because the chart
 * stage is in the default layout). This parser makes the deep-link contract
 * real. `?view=research` mounts the Research Hub stage view (item 4);
 * `?view=execution` mounts the Execution Research stage view (SURF-P01);
 * unknown values resolve to the default multi-pane terminal — never a blank.
 */
export type StageViewName = "chart" | "research" | "execution";

export function getViewFromSearch(search: string | undefined): StageViewName | null {
  if (!search) return null;
  try {
    const params = new URLSearchParams(search);
    const view = params.get("view")?.toLowerCase();
    if (view === "chart") return "chart";
    if (view === "research") return "research";
    if (view === "execution") return "execution";
  } catch {
    // Fallback
  }
  return null;
}

/** UI-CONV-P03: `panel` parameter activates a bottom-dock tab from a deep link. */
export function getPanelFromSearch(search: string | undefined): BottomDockTab | null {
  if (!search) return null;
  try {
    const params = new URLSearchParams(search);
    const panel = params.get("panel")?.toUpperCase();
    const valid: BottomDockTab[] = ["TRADE_PLANS", "JOURNAL", "RISK", "SCENARIOS", "PORTFOLIO"];
    if (valid.includes(panel as BottomDockTab)) return panel as BottomDockTab;
  } catch {
    // Fallback
  }
  return null;
}

function TradingTerminalInner({
  className = "",
  initialRightView = "SIGNALS",
}: {
  className?: string;
  initialRightView?: RightDockView;
}) {
  const location = useSafeLocation();
  const searchStr = location?.search ?? (typeof window !== "undefined" ? window.location?.search : "");
  const { selectedSymbol, selectedQuote, liveMarket } = useTerminal();
  const [rightView, setRightView] = useState<RightDockView>(() => getDockFromSearch(searchStr, initialRightView));
  // UI-CONV-P03: `view` (primary stage) and `panel` (bottom dock) deep links.
  const [stageView] = useState<StageViewName | null>(() => getViewFromSearch(searchStr));
  const [requestedBottomTab, setRequestedBottomTab] = useState<BottomDockTab | null>(() =>
    getPanelFromSearch(searchStr),
  );

  useEffect(() => {
    if (searchStr) {
      setRightView(getDockFromSearch(searchStr, initialRightView));
      setRequestedBottomTab(getPanelFromSearch(searchStr));
    }
  }, [searchStr, initialRightView]);

  let wsStatus: WebSocketFeedStatus = "disconnected";
  if (liveMarket.connectionState === "connected") {
    wsStatus = "live";
  } else if (
    liveMarket.connectionState === "connecting" ||
    liveMarket.connectionState === "reconnecting"
  ) {
    wsStatus = "connecting";
  } else if (liveMarket.connectionState === "idle") {
    wsStatus = "empty";
  } else if (liveMarket.connectionState === "error") {
    wsStatus = "degraded";
  }

  // Derive honest market data from genuine quote (T-6 / B-P02-1)
  let marketData: TickerMarketData | null = null;
  if (selectedQuote) {
    const openNum = Number(selectedQuote.open);
    const closeNum = Number(selectedQuote.close);
    const highNum = Number(selectedQuote.high);
    const lowNum = Number(selectedQuote.low);
    const volNum = selectedQuote.volume != null ? Number(selectedQuote.volume) : null;

    const hasHighLow = !isNaN(highNum) && !isNaN(lowNum);
    const rangeVal = hasHighLow ? highNum - lowNum : null;

    marketData = {
      symbol: selectedSymbol,
      price: !isNaN(closeNum) ? closeNum : selectedQuote.close,
      change24h: !isNaN(closeNum) && !isNaN(openNum) ? closeNum - openNum : null,
      change24hPercent:
        !isNaN(closeNum) && !isNaN(openNum) && openNum !== 0
          ? ((closeNum - openNum) / openNum) * 100
          : 0,
      high24h: !isNaN(highNum) ? highNum : null,
      low24h: !isNaN(lowNum) ? lowNum : null,
      range: rangeVal !== null ? rangeVal.toFixed(5) : null,
      volume24h: volNum != null && !isNaN(volNum) ? `${(volNum / 1000000).toFixed(1)}M` : null,
      spread: null, // Gate-closed (B-P02-1)
      timestamp: selectedQuote.updatedAt ?? null,
      posture: "live:simulated",
    };
  }

  return (
    <div
      className={`trading-terminal-workspace ${className}`}
      data-testid="trading-terminal-workspace"
      data-stage-view={stageView ?? "default"}
    >
      {/* BO-F-00.3: landing heading outline (OBS-CAPASSESS-H1) — the "/"
          operations surface carries a visually-hidden h1 so the document
          outline is complete without changing the terminal density. */}
      <h1 className="ix-sr-only" data-testid="operations-landing-h1">
        AXIOM Institutional Trading Terminal — Operations
      </h1>
      <TerminalMultiPaneLayout
        topTicker={
          <TerminalTopTicker
            symbol={selectedSymbol}
            marketData={marketData}
            wsStatus={wsStatus}
            showGovernanceBadge={true}
          />
        }
        leftSlot={<TerminalWatchlistDock />}
        centreAriaLabel={
          stageView === "research"
            ? "Research Hub Stage"
            : stageView === "execution"
              ? "Execution Research Stage"
              : "Primary Candlestick Chart Stage"
        }
        centreSlot={
          // UI-CONV-P03 item 4 (OBS-CONV3-4 discharge) + SURF-P01: the stage
          // views are rendered branches, not attribute-only seams.
          // `?view=research` mounts the Research Hub stage view;
          // `?view=execution` mounts the Execution Research stage view
          // (SURF-P01); `chart` and the default multi-pane present the chart
          // stage (OBS-CONV2-7 discharge — the /?view=chart contract is
          // honoured by the parser above).
          stageView === "research" ? (
            <div className="research-stage-scroll" data-testid="research-stage-scroll">
              <Suspense fallback={<div className="stage-view-loading mono">Loading research stage…</div>}>
                <ResearchHubView />
              </Suspense>
            </div>
          ) : stageView === "execution" ? (
            <div className="stage-view-scroll" data-testid="execution-stage-scroll">
              <Suspense fallback={<div className="stage-view-loading mono">Loading execution research stage…</div>}>
                <ExecutionResearchView />
              </Suspense>
            </div>
          ) : (
            <TerminalChartStage />
          )
        }
        rightSlot={
          <div className="right-dock-container" data-testid="right-dock-container">
            <div className="right-dock-nav" role="tablist" aria-label="Right Dock Navigation">
              {(["SIGNALS", "TELEMETRY", "INTELLIGENCE", "ALERTS"] as const).map((view) => (
                <button
                  key={view}
                  type="button"
                  role="tab"
                  aria-selected={rightView === view}
                  className={`right-dock-tab-btn ${rightView === view ? "active" : ""}`}
                  onClick={() => setRightView(view)}
                  data-testid={`right-dock-tab-${view.toLowerCase()}`}
                >
                  {view}
                </button>
              ))}
            </div>
            <div className="right-dock-content">
              {rightView === "SIGNALS" ? (
                <TerminalSignalStream />
              ) : rightView === "TELEMETRY" ? (
                <TerminalMarketTelemetry />
              ) : rightView === "ALERTS" ? (
                <TerminalAlertsDock />
              ) : (
                <TerminalIntelligenceCards />
              )}
            </div>
          </div>
        }
        bottomSlot={<TerminalBottomDock requestedTab={requestedBottomTab ?? undefined} />}
      />
    </div>
  );
}

/**
 * TradingTerminalWorkspace
 *
 * Unified Trading Terminal Workstation mounted at route `/`.
 * Integrates TerminalProvider context, Watchlist Dock (P02), Primary Chart Stage (P03),
 * Signal Stream (P04), Market Telemetry (P02), Intelligence Cards (P04), and Analytics Dock (P05).
 */
export function TradingTerminalWorkspace({
  initialSymbol = "EUR/USD",
  className = "",
  enableLiveMarket = true,
  initialRightView = "SIGNALS",
}: TradingTerminalWorkspaceProps) {
  return (
    <TerminalProvider initialSymbol={initialSymbol} enableLiveMarket={enableLiveMarket}>
      <TradingTerminalInner className={className} initialRightView={initialRightView} />
    </TerminalProvider>
  );
}
