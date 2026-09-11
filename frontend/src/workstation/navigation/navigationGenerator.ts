import type { Operator } from "../../api/client";
import {
  NAVIGATION_CATEGORIES,
  type NavigationCategory,
  type WorkspaceDefinition,
} from "../registry/workspaceRegistry";

export type NavigationSection = {
  category: NavigationCategory;
  workspaces: WorkspaceDefinition[];
};

export type NavigationGenerationInput = {
  workspaces: WorkspaceDefinition[];
  operator: Pick<Operator, "role"> | null;
  enabledFeatureFlags?: ReadonlySet<string>;
};

export type WorkspaceActivationEvent = {
  type: "workspace.activation";
  workspaceId: string;
  route: string;
  telemetryId: string;
  timestamp: string;
};

export function canAccessWorkspace(
  workspace: WorkspaceDefinition,
  operator: Pick<Operator, "role"> | null,
): boolean {
  if (!workspace.requiresAuth || !operator) return false;
  return workspace.rbac.allowedRoles.includes(operator.role);
}

export function featureFlagEnabled(
  workspace: WorkspaceDefinition,
  enabledFeatureFlags: ReadonlySet<string> = new Set(),
): boolean {
  return workspace.featureFlag === null || enabledFeatureFlags.has(workspace.featureFlag);
}

export function visibleWorkspaces(input: NavigationGenerationInput): WorkspaceDefinition[] {
  return input.workspaces
    .filter((workspace) => !workspace.aliasFor)
    .filter((workspace) => canAccessWorkspace(workspace, input.operator))
    .filter((workspace) => featureFlagEnabled(workspace, input.enabledFeatureFlags))
    .sort((left, right) => left.order - right.order);
}

export function generateNavigationSections(input: NavigationGenerationInput): NavigationSection[] {
  const visible = visibleWorkspaces(input);
  return NAVIGATION_CATEGORIES.map((category) => ({
    category,
    workspaces: visible.filter((workspace) => workspace.navigationCategory === category),
  })).filter((section) => section.workspaces.length > 0);
}

export function createWorkspaceActivationEvent(
  workspace: WorkspaceDefinition,
): WorkspaceActivationEvent {
  return {
    type: "workspace.activation",
    workspaceId: workspace.id,
    route: workspace.route,
    telemetryId: workspace.telemetryId,
    timestamp: new Date().toISOString(),
  };
}
