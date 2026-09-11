import {
  WORKSPACE_REGISTRY,
  workspaceForPath,
  type WorkspaceDefinition,
} from "../registry/workspaceRegistry";
import { WORKFLOW_NAVIGATION_METADATA } from "./workflowNavigationMetadata";
import type {
  BreadcrumbBuildInput,
  BreadcrumbItem,
  WorkflowMetadataValidationResult,
  WorkflowNavigationMetadata,
  WorkflowStage,
} from "./workflowTypes";

export function workflowMetadataByWorkspaceId(
  metadata: readonly WorkflowNavigationMetadata[] = WORKFLOW_NAVIGATION_METADATA,
): Map<string, WorkflowNavigationMetadata> {
  return new Map(metadata.map((item) => [item.workspaceId, item]));
}

export function workflowMetadataForWorkspace(
  workspaceId: string,
  metadata: readonly WorkflowNavigationMetadata[] = WORKFLOW_NAVIGATION_METADATA,
): WorkflowNavigationMetadata | null {
  return workflowMetadataByWorkspaceId(metadata).get(workspaceId) ?? null;
}

export function validateWorkflowMetadata(
  metadata: readonly WorkflowNavigationMetadata[] = WORKFLOW_NAVIGATION_METADATA,
  workspaces: readonly WorkspaceDefinition[] = WORKSPACE_REGISTRY,
): WorkflowMetadataValidationResult {
  const registeredIds = new Set(workspaces.map((workspace) => workspace.id));
  const metadataIds = new Set(metadata.map((item) => item.workspaceId));
  const referencedIds = metadata.flatMap((item) => [
    ...item.relatedWorkspaceIds,
    ...item.defaultNextWorkspaceIds,
    ...item.defaultPreviousWorkspaceIds,
  ]);

  const orphanWorkspaceIds = [...metadataIds].filter((workspaceId) => !registeredIds.has(workspaceId));
  const missingWorkspaceIds = [...registeredIds].filter((workspaceId) => !metadataIds.has(workspaceId));
  const invalidReferences = referencedIds.filter((workspaceId) => !registeredIds.has(workspaceId));

  return {
    valid:
      orphanWorkspaceIds.length === 0 &&
      missingWorkspaceIds.length === 0 &&
      invalidReferences.length === 0,
    orphanWorkspaceIds,
    missingWorkspaceIds,
    invalidReferences,
  };
}

export function assertWorkflowMetadataValid(
  metadata: readonly WorkflowNavigationMetadata[] = WORKFLOW_NAVIGATION_METADATA,
  workspaces: readonly WorkspaceDefinition[] = WORKSPACE_REGISTRY,
): void {
  const result = validateWorkflowMetadata(metadata, workspaces);
  if (!result.valid) {
    throw new Error(
      `INVALID_WORKFLOW_METADATA orphan=${result.orphanWorkspaceIds.join(",")} missing=${result.missingWorkspaceIds.join(",")} invalidRefs=${result.invalidReferences.join(",")}`,
    );
  }
}

export function firstRouteForWorkflowStage(
  stage: WorkflowStage,
  metadata: readonly WorkflowNavigationMetadata[] = WORKFLOW_NAVIGATION_METADATA,
  workspaces: readonly WorkspaceDefinition[] = WORKSPACE_REGISTRY,
): string | undefined {
  const workspaceById = new Map(workspaces.map((workspace) => [workspace.id, workspace]));
  const firstMetadata = [...metadata]
    .filter((item) => item.primaryStage === stage)
    .sort((left, right) => left.workflowOrdinal - right.workflowOrdinal)[0];
  return firstMetadata ? workspaceById.get(firstMetadata.workspaceId)?.route : undefined;
}

export function buildBreadcrumbTrail(input: BreadcrumbBuildInput): BreadcrumbItem[] {
  const activeWorkspace = workspaceForPath(input.pathname);
  const metadata = workflowMetadataForWorkspace(activeWorkspace.id);
  const primaryStage = metadata?.primaryStage ?? activeWorkspace.navigationCategory;
  const workspaceLabel = metadata?.breadcrumbLabel ?? activeWorkspace.displayName;
  const stageRoute = firstRouteForWorkflowStage(primaryStage as WorkflowStage);

  const items: BreadcrumbItem[] = [
    {
      id: "axiom-root",
      label: "AXIOM",
      route: input.pathname === "/" ? undefined : "/",
      current: false,
    },
    {
      id: `workflow-stage.${primaryStage}`,
      label: primaryStage,
      route: stageRoute === input.pathname ? undefined : stageRoute,
      current: false,
    },
    {
      id: `workspace.${activeWorkspace.id}`,
      label: workspaceLabel,
      route: input.artifact ? activeWorkspace.route : undefined,
      current: !input.artifact,
    },
  ];

  if (input.artifact) {
    items.push({
      id: `artifact.${input.artifact.label}`,
      label: input.artifact.label,
      route: input.artifact.route,
      current: true,
    });
  }

  return items;
}
