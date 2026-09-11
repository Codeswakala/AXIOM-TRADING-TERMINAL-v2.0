export type WorkflowStage =
  | "Observe"
  | "Detect"
  | "Investigate"
  | "Analyze"
  | "Compare"
  | "Plan"
  | "Document"
  | "Review"
  | "Govern"
  | "Settings";

export type WorkflowNavigationMetadata = {
  workspaceId: string;
  primaryStage: WorkflowStage;
  secondaryStages?: readonly WorkflowStage[];
  breadcrumbLabel: string;
  workflowOrdinal: number;
  keywords: readonly string[];
  relatedWorkspaceIds: readonly string[];
  defaultNextWorkspaceIds: readonly string[];
  defaultPreviousWorkspaceIds: readonly string[];
};

export type WorkflowMetadataValidationResult = {
  valid: boolean;
  orphanWorkspaceIds: readonly string[];
  missingWorkspaceIds: readonly string[];
  invalidReferences: readonly string[];
};

export type BreadcrumbItem = {
  id: string;
  label: string;
  route?: string;
  current: boolean;
};

export type BreadcrumbArtifactContext = {
  label: string;
  route?: string;
};

export type BreadcrumbBuildInput = {
  pathname: string;
  artifact?: BreadcrumbArtifactContext;
};
