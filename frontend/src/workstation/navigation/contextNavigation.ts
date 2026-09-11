import { WORKSPACE_REGISTRY, type WorkspaceDefinition } from "../registry/workspaceRegistry";
import { workflowMetadataForWorkspace } from "../workflows/workflowModel";

export type ContextNavigationTarget = {
  workspaceId: string;
  label: string;
  route: string;
  stage: string;
  description: string;
  resultAction: "navigate";
  readonly: true;
};

export function contextNavigationTargets(
  activeWorkspace: WorkspaceDefinition,
  registry: readonly WorkspaceDefinition[] = WORKSPACE_REGISTRY,
): ContextNavigationTarget[] {
  const metadata = workflowMetadataForWorkspace(activeWorkspace.id);
  if (!metadata) return [];
  const workspaceById = new Map(registry.map((workspace) => [workspace.id, workspace]));
  return metadata.relatedWorkspaceIds
    .map((workspaceId) => workspaceById.get(workspaceId))
    .filter((workspace): workspace is WorkspaceDefinition => Boolean(workspace && !workspace.aliasFor))
    .map((workspace) => {
      const targetMetadata = workflowMetadataForWorkspace(workspace.id);
      return {
        workspaceId: workspace.id,
        label: workspace.displayName,
        route: workspace.route,
        stage: targetMetadata?.primaryStage ?? workspace.navigationCategory,
        description: workspace.description,
        resultAction: "navigate",
        readonly: true,
      };
    });
}

export function allContextNavigationTargetsAreRegistered(
  registry: readonly WorkspaceDefinition[] = WORKSPACE_REGISTRY,
): boolean {
  const registeredRoutes = new Set(registry.map((workspace) => workspace.route));
  return registry.every((workspace) =>
    contextNavigationTargets(workspace, registry).every((target) => registeredRoutes.has(target.route)),
  );
}
