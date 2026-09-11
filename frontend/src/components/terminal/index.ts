export { TerminalGovernanceBadge } from "./TerminalGovernanceBadge";
export type { TerminalGovernanceBadgeProps } from "./TerminalGovernanceBadge";

export { TerminalTopTicker } from "./TerminalTopTicker";
export type {
  TerminalTopTickerProps,
  TickerMarketData,
  WebSocketFeedStatus,
} from "./TerminalTopTicker";

export {
  TerminalMultiPaneLayout,
  TerminalSlotPlaceholder,
} from "./TerminalMultiPaneLayout";
export type {
  TerminalMultiPaneLayoutProps,
  TerminalSlotPlaceholderProps,
} from "./TerminalMultiPaneLayout";

export {
  TerminalProvider,
  useTerminal,
  SUPPORTED_INSTRUMENTS,
} from "./TerminalContext";
export type {
  TerminalContextValue,
  TerminalProviderProps,
} from "./TerminalContext";

export { TerminalWatchlistDock } from "./TerminalWatchlistDock";
export type {
  TerminalWatchlistDockProps,
  AssetCategory,
} from "./TerminalWatchlistDock";

export { TerminalMarketTelemetry } from "./TerminalMarketTelemetry";
export type { TerminalMarketTelemetryProps } from "./TerminalMarketTelemetry";

export { TerminalSpreadTelemetry } from "./TerminalSpreadTelemetry";
export type { TerminalSpreadTelemetryProps } from "./TerminalSpreadTelemetry";

export { TerminalChartStage } from "./TerminalChartStage";
export type {
  TerminalChartStageProps,
  TimeframeOption,
} from "./TerminalChartStage";

export { TerminalSignalStream } from "./TerminalSignalStream";
export type { TerminalSignalStreamProps } from "./TerminalSignalStream";

export { TerminalIntelligenceCards } from "./TerminalIntelligenceCards";
export type {
  TerminalIntelligenceCardsProps,
  IntelligenceTab,
} from "./TerminalIntelligenceCards";

export { TerminalBottomDock } from "./TerminalBottomDock";
export { TerminalBottomDock as TerminalAnalyticsDock } from "./TerminalBottomDock";
export type {
  TerminalBottomDockProps,
  BottomDockTab,
} from "./TerminalBottomDock";

export { getComputedToken } from "./tokenResolver";

export { TradingTerminalWorkspace } from "./TradingTerminalWorkspace";
export type {
  TradingTerminalWorkspaceProps,
  RightDockView,
} from "./TradingTerminalWorkspace";
