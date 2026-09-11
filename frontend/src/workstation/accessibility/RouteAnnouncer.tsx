/**
 * AXIOM Institutional Accessibility — RouteAnnouncer (UI-010-P05)
 *
 * Screen-reader live region announcing workspace route transitions (WCAG 4.1.3).
 * Uses role="status", aria-live="polite", and aria-atomic="true".
 *
 * Invariant: Announces navigation destination only; zero sensitive data exposure.
 */

import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { workspaceForPath } from "../registry/workspaceRegistry";
import "./RouteAnnouncer.css";

export interface RouteAnnouncerProps {
  routeTitle?: string;
}

export function RouteAnnouncer({ routeTitle }: RouteAnnouncerProps) {
  const location = useLocation();
  const [announcement, setAnnouncement] = useState("");

  useEffect(() => {
    const activeWorkspace = workspaceForPath(location.pathname);
    const title = routeTitle || activeWorkspace.displayName || "Workspace";
    setAnnouncement(`Navigated to ${title}`);
  }, [location.pathname, routeTitle]);

  return (
    <div
      role="status"
      aria-live="polite"
      aria-atomic="true"
      aria-label="Route announcements"
      className="ix-sr-only"
      data-testid="route-announcer"
      data-ui010-component="route-announcer"
    >
      {announcement}
    </div>
  );
}
