import { Outlet, useLocation } from "react-router-dom";
import { workspaceForPath } from "../registry/workspaceRegistry";

export function WorkspaceHost() {
  const location = useLocation();
  const workspace = workspaceForPath(location.pathname);
  return (
    <section
      className="ix-workspace-host"
      aria-label={`Primary workspace: ${workspace.displayName}`}
      data-workspace-id={workspace.id}
    >
      <Outlet />
    </section>
  );
}
