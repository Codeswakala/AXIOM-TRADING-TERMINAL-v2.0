export type CommandType = "navigation" | "ui-toggle";

export type CommandSource = "quick-action-catalogue";

export type CommandGroup =
  | "Observe"
  | "Detect"
  | "Investigate"
  | "Analyze"
  | "Compare"
  | "Plan"
  | "Document"
  | "Review"
  | "Govern"
  | "Settings"
  | "Assistant"
  | "Shell Controls";

export type CommandTarget =
  | { kind: "route"; route: string; workspaceId: string }
  | { kind: "previous-workspace" }
  | { kind: "recent-workspace" }
  | { kind: "shell"; action: ShellCommandAction };

export type ShellCommandAction =
  | "toggle-navigation"
  | "toggle-context"
  | "toggle-activity"
  | "toggle-theme"
  | "open-global-search"
  | "clear-search-query"
  | "open-shell-status"
  | "show-governance-notification"
  | "open-assistant-surfaces"
  | "focus-navigation"
  | "focus-workspace"
  | "focus-context"
  | "focus-activity";

export type QuickActionDefinition = {
  id: `qa.${string}`;
  label: string;
  commandType: CommandType;
  group: CommandGroup;
  target: CommandTarget;
  keywords: readonly string[];
  enabled: boolean;
  source: CommandSource;
  noActuation: true;
};

export type CommandRegistryContext = {
  visibleWorkspaceIds: ReadonlySet<string>;
  routeForWorkspaceId: (workspaceId: string) => string | null;
  recentWorkspaceIds: readonly string[];
  onNavigate: (route: string) => void;
  onToggleNavigation: () => void;
  onToggleContext: () => void;
  onToggleActivity: () => void;
  onToggleTheme: () => void;
  onOpenGlobalSearch: () => void;
  onOpenShellStatus: () => void;
  onShowGovernanceNotification: () => void;
  onOpenAssistantSurface?: () => void;
  onFocusRegion: (region: "B" | "C" | "D" | "E") => void;
  onUnavailable: (label: string) => void;
};

export type RegisteredCommand = QuickActionDefinition & {
  onSelect: () => void;
};
