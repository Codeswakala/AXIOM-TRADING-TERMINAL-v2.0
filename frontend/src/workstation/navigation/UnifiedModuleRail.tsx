import { useLocation, useNavigate } from "react-router-dom";
import { WORKSPACE_REGISTRY } from "../registry/workspaceRegistry";
import { useMonitoringAlerts } from "../../components/alerts/AlertsProvider";
import { railShortLabel, WorkspaceIcon } from "./icons";
import "./UnifiedModuleRail.css";

/**
 * UnifiedModuleRail
 *
 * Compact vertical launcher icon rail docked on the left edge of the unified application shell.
 * Replaces the legacy 232px NavigationDock accordion while maintaining instant reachability
 * to all 16 registered workspace routes and alerting affordances (B-CONV-1 / B-CONV-4).
 *
 * SURF-P02: the alerts launcher now shows a GENUINE unread count derived from
 * the monitoring-alerts API (acknowledged === false), via AlertsProvider —
 * never a placeholder. When the count cannot be determined (loading or
 * failure) the badge renders as absence. Clicking navigates to the terminal's
 * ALERTS right-dock tab (/?dock=alerts).
 *
 * Adheres to:
 * - T-1: Zero transaction or actuation triggers
 * - Doc 16 Brand Standards & Pure Token Consumption
 * - Presentation container: classification recital lives in the governance
 *   register, not in code comments (FE-U02 ACC-1 boundary law)
 */
export interface UnifiedModuleRailProps {
  /** PC-FEU02-1 C4: honestly persisted collapse (storage election
   *  axiom_chrome_rail_collapsed rides in the shell). */
  collapsed?: boolean;
  onToggleCollapsed?: () => void;
}

export function UnifiedModuleRail({ collapsed = false, onToggleCollapsed }: UnifiedModuleRailProps = {}) {
  const location = useLocation();
  const navigate = useNavigate();
  const { unreadCount } = useMonitoringAlerts();

  // Core navigation items from WORKSPACE_REGISTRY (excluding compatibility alias /chart)
  const primaryWorkspaces = WORKSPACE_REGISTRY.filter((w) => w.id !== "monitor.chart_alias");

  const alertsTitle =
    unreadCount !== null && unreadCount > 0
      ? `System Alerts (${unreadCount} Unread)`
      : "System Alerts";

  return (
    <nav
      className={`unified-module-rail${collapsed ? " rail-collapsed" : ""}`}
      role="navigation"
      aria-label="Module Launcher Rail"
      tabIndex={-1}
      data-region="B"
      data-testid="unified-module-rail"
    >
      {onToggleCollapsed ? (
        <button
          type="button"
          className="rail-collapse-btn"
          onClick={onToggleCollapsed}
          aria-expanded={!collapsed}
          aria-label={collapsed ? "Expand module rail" : "Collapse module rail"}
          data-testid="chrome-rail-collapse-btn"
        >
          <span aria-hidden="true">{collapsed ? "»" : "«"}</span>
        </button>
      ) : null}
      <div className="rail-section">
        {primaryWorkspaces.map((workspace) => {
          const isActive =
            location.pathname === workspace.route ||
            (workspace.route === "/charts" && location.pathname === "/chart");
          return (
            <button
              key={workspace.id}
              type="button"
              className={`rail-button ${isActive ? "active" : ""}`}
              onClick={() => navigate(workspace.route)}
              title={`${workspace.displayName} (${workspace.keyboardShortcut})`}
              aria-label={`Open ${workspace.displayName} (${workspace.keyboardShortcut})`}
              aria-current={isActive ? "page" : undefined}
              data-testid={`rail-btn-${workspace.id.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`}
            >
              <WorkspaceIcon icon={workspace.icon} />
              {/* BO-F-06.1: the visible label — the collapsed rail must be
                  legible at a glance (no icon-only-with-hidden-label). */}
              <span className="rail-label" aria-hidden="true">
                {railShortLabel(workspace.id, workspace.displayName)}
              </span>
            </button>
          );
        })}
      </div>

      <div className="rail-section">
        <div className="rail-divider" aria-hidden="true" />
        {/* Alerts launcher (SURF-P02): genuine unread count + ALERTS dock deep link */}
        <button
          type="button"
          className="rail-button rail-alerts-button"
          onClick={() => navigate("/?dock=alerts")}
          title={alertsTitle}
          aria-label={alertsTitle}
          data-testid="rail-btn-alerts"
        >
          <WorkspaceIcon icon="alerts" />
          {/* BO-F-06.1: the alerts launcher is labeled like every other item. */}
          <span className="rail-label" aria-hidden="true">
            Alerts
          </span>
          {unreadCount !== null && unreadCount > 0 ? (
            <span className="rail-badge-indicator" data-testid="rail-alerts-badge">
              {unreadCount}
            </span>
          ) : null}
        </button>
      </div>
    </nav>
  );
}
