import { TradingTerminalWorkspace } from "../components/terminal/TradingTerminalWorkspace";

/**
 * DashboardPage (Root Route `/`)
 *
 * Institutional Trading Terminal root workstation mount.
 * Replaces the legacy Operations card dashboard per UI-NEW Master Engineering Design Plan §D.
 */
export function DashboardPage() {
  return <TradingTerminalWorkspace />;
}
