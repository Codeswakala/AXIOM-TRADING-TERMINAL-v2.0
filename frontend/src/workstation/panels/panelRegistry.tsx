import type { ComponentType } from "react";
import { ContextNavigationPanel } from "../navigation/ContextNavigationPanel";
import type { WorkspaceDefinition } from "../registry/workspaceRegistry";

export type PanelCategory = "context" | "activity" | "primary";
export type DockPosition = "left" | "right" | "top" | "bottom" | "center";

export type PanelDimensions = {
  width: number;
  height: number;
};

export type PanelRegistrationContract = {
  /** Panel Identifier */
  id: string;
  /** Display Name */
  displayName: string;
  /** Panel Category */
  panelCategory: PanelCategory;
  /** Supported Workspaces */
  supportedWorkspaces: readonly string[];
  /** Default Dimensions */
  defaultDimensions: PanelDimensions;
  /** Minimum Dimensions */
  minimumDimensions: PanelDimensions;
  /** Maximum Dimensions */
  maximumDimensions: PanelDimensions;
  /** Resizable */
  resizable: boolean;
  /** Dockable */
  dockable: boolean;
  /** Closable */
  closable: boolean;
  /** Persistence Support */
  persistenceSupport: "session" | "memory" | "none";
  /** Context Dependencies */
  contextDependencies: readonly string[];
  /** Telemetry Identifier */
  telemetryId: string;
  /** Panel Version */
  panelVersion: string;
  /** ITRGA guard: panel is presentation-only. */
  noActuation: true;
  Component: ComponentType<PanelComponentProps>;
};

export type PanelComponentProps = {
  activeWorkspace: WorkspaceDefinition;
};

const PANEL_VERSION = "ui-001-p03.panel-registration.v1";
const ALL_WORKSPACES = ["*"] as const;

function WorkspaceContextPanel({ activeWorkspace }: PanelComponentProps) {
  return (
    <div className="ix-panel-body">
      <strong>{activeWorkspace.displayName}</strong>
      <p className="ix-metadata">{activeWorkspace.description}</p>
      <dl className="ix-context-metadata">
        <dt>Category</dt>
        <dd>{activeWorkspace.navigationCategory}</dd>
        <dt>Shortcut</dt>
        <dd>{activeWorkspace.keyboardShortcut}</dd>
        <dt>Telemetry</dt>
        <dd>{activeWorkspace.telemetryId}</dd>
      </dl>
    </div>
  );
}

function GovernanceContextPanel() {
  return (
    <div className="ix-panel-body">
      <span className="ix-status-chip success">Gate CLOSED</span>
      <span className="ix-status-chip info">Research-only</span>
      <p className="ix-metadata">
        This workstation hosts approved AXIOM research workspaces and adds no platform capability.
      </p>
    </div>
  );
}

function ShellActivityPanel() {
  return (
    <div className="ix-panel-body">
      <span className="ix-metadata">
        Workstation panel infrastructure active. Detailed activity streams arrive in later UI phases.
      </span>
    </div>
  );
}

export const PANEL_REGISTRY: PanelRegistrationContract[] = [
  {
    id: "shell.context.workspace",
    displayName: "Workspace context",
    panelCategory: "context",
    supportedWorkspaces: ALL_WORKSPACES,
    defaultDimensions: { width: 320, height: 180 },
    minimumDimensions: { width: 240, height: 120 },
    maximumDimensions: { width: 520, height: 420 },
    resizable: true,
    dockable: true,
    closable: false,
    persistenceSupport: "session",
    contextDependencies: ["activeWorkspace"],
    telemetryId: "panel.shell.context.workspace",
    panelVersion: PANEL_VERSION,
    noActuation: true,
    Component: WorkspaceContextPanel,
  },
  {
    id: "shell.context.workflow_navigation",
    displayName: "Related workflow navigation",
    panelCategory: "context",
    supportedWorkspaces: ALL_WORKSPACES,
    defaultDimensions: { width: 320, height: 180 },
    minimumDimensions: { width: 240, height: 120 },
    maximumDimensions: { width: 520, height: 420 },
    resizable: true,
    dockable: true,
    closable: false,
    persistenceSupport: "session",
    contextDependencies: ["activeWorkspace", "workflowMetadata"],
    telemetryId: "panel.shell.context.workflow_navigation",
    panelVersion: PANEL_VERSION,
    noActuation: true,
    Component: ContextNavigationPanel,
  },
  {
    id: "shell.context.governance",
    displayName: "Governance context",
    panelCategory: "context",
    supportedWorkspaces: ALL_WORKSPACES,
    defaultDimensions: { width: 320, height: 160 },
    minimumDimensions: { width: 240, height: 120 },
    maximumDimensions: { width: 520, height: 360 },
    resizable: true,
    dockable: true,
    closable: false,
    persistenceSupport: "session",
    contextDependencies: ["governanceStatus"],
    telemetryId: "panel.shell.context.governance",
    panelVersion: PANEL_VERSION,
    noActuation: true,
    Component: GovernanceContextPanel,
  },
  {
    id: "shell.activity.status",
    displayName: "Workstation activity",
    panelCategory: "activity",
    supportedWorkspaces: ALL_WORKSPACES,
    defaultDimensions: { width: 640, height: 180 },
    minimumDimensions: { width: 320, height: 120 },
    maximumDimensions: { width: 1200, height: 360 },
    resizable: true,
    dockable: true,
    closable: false,
    persistenceSupport: "session",
    contextDependencies: ["shellEvents"],
    telemetryId: "panel.shell.activity.status",
    panelVersion: PANEL_VERSION,
    noActuation: true,
    Component: ShellActivityPanel,
  },
];

export function panelsForCategory(category: PanelCategory): PanelRegistrationContract[] {
  return PANEL_REGISTRY.filter((panel) => panel.panelCategory === category);
}
