/**
 * TerminalSpreadTelemetry (Alias to TerminalMarketTelemetry per C-1 and B-P02-1)
 *
 * Provides candle-derived market telemetry (tick rate, volume, intraperiod range, lag)
 * without synthetic depth or unbacked quote fabrication.
 */
export { TerminalMarketTelemetry as TerminalSpreadTelemetry } from "./TerminalMarketTelemetry";
export type { TerminalMarketTelemetryProps as TerminalSpreadTelemetryProps } from "./TerminalMarketTelemetry";
