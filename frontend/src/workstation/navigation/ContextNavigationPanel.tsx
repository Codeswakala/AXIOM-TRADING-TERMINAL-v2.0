import { Link } from "react-router-dom";
import type { WorkspaceDefinition } from "../registry/workspaceRegistry";
import { contextNavigationTargets } from "./contextNavigation";

export type ContextNavigationPanelProps = {
  activeWorkspace: WorkspaceDefinition;
};

export function ContextNavigationPanel({ activeWorkspace }: ContextNavigationPanelProps) {
  const targets = contextNavigationTargets(activeWorkspace);

  return (
    <div className="ix-panel-body ix-context-navigation" data-ui002-component="context-navigation">
      <p className="ix-metadata">
        Related workflow destinations are read-only navigation targets derived from the workflow map.
      </p>
      {targets.length > 0 ? (
        <ul aria-label="Related workflow navigation targets">
          {targets.map((target) => (
            <li key={target.workspaceId}>
              <Link
                to={target.route}
                data-workspace-id={target.workspaceId}
                data-result-action={target.resultAction}
                data-readonly={target.readonly}
              >
                <span>{target.label}</span>
                <small>
                  {target.stage} · Read-only route
                </small>
              </Link>
            </li>
          ))}
        </ul>
      ) : (
        <span className="ix-metadata">No related workflow destinations registered.</span>
      )}
    </div>
  );
}
