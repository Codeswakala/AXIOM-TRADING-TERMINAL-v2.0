import { QUICK_ACTION_CATALOGUE, QUICK_ACTION_CATALOGUE_IDS } from "./quickActionCatalogue";
import type {
  CommandRegistryContext,
  CommandType,
  QuickActionDefinition,
  RegisteredCommand,
  ShellCommandAction,
} from "./commandTypes";

const ALLOWED_COMMAND_TYPES: readonly CommandType[] = ["navigation", "ui-toggle"] as const;

export function assertVettedCommandDefinition(
  definition: QuickActionDefinition,
  vettedIds: readonly string[] = QUICK_ACTION_CATALOGUE_IDS,
): void {
  if (!vettedIds.includes(definition.id)) {
    throw new Error(`UNVETTED_COMMAND:${definition.id}`);
  }
  if (!ALLOWED_COMMAND_TYPES.includes(definition.commandType)) {
    throw new Error(`UNSUPPORTED_COMMAND_TYPE:${String(definition.commandType)}`);
  }
  if (definition.noActuation !== true) {
    throw new Error(`UNSAFE_COMMAND:${definition.id}`);
  }
}

export function validateQuickActionCatalogue(
  catalogue: readonly QuickActionDefinition[] = QUICK_ACTION_CATALOGUE,
): boolean {
  const ids = catalogue.map((item) => item.id);
  if (ids.length !== 33) throw new Error(`CATALOGUE_SIZE:${ids.length}`);
  if (new Set(ids).size !== ids.length) throw new Error("DUPLICATE_COMMAND_ID");
  for (const item of catalogue) assertVettedCommandDefinition(item, ids);
  return true;
}

export function createCommandRegistry(
  context: CommandRegistryContext,
  catalogue: readonly QuickActionDefinition[] = QUICK_ACTION_CATALOGUE,
): RegisteredCommand[] {
  validateQuickActionCatalogue(catalogue);
  return catalogue.map((definition) => registerCommand(definition, context));
}

function registerCommand(
  definition: QuickActionDefinition,
  context: CommandRegistryContext,
): RegisteredCommand {
  assertVettedCommandDefinition(definition);
  if (definition.target.kind === "route") {
    // CA-CONV2-1: An explicit catalogue route is the command's canonical post-absorption
    // destination (e.g. /?view=chart, /?dock=signals, /?dock=intelligence). The registry
    // lookup remains the RBAC-aware fallback when the catalogue omits an explicit route.
    const route = definition.target.route ?? context.routeForWorkspaceId(definition.target.workspaceId);
    const enabled = definition.enabled && context.visibleWorkspaceIds.has(definition.target.workspaceId);
    return {
      ...definition,
      enabled,
      onSelect: () => (enabled ? context.onNavigate(route) : context.onUnavailable(definition.label)),
    };
  }
  if (definition.target.kind === "previous-workspace" || definition.target.kind === "recent-workspace") {
    const recentWorkspaceId = context.recentWorkspaceIds[0] ?? null;
    const route = recentWorkspaceId ? context.routeForWorkspaceId(recentWorkspaceId) : null;
    const enabled = definition.enabled && Boolean(route);
    return {
      ...definition,
      enabled,
      onSelect: () => (enabled && route ? context.onNavigate(route) : context.onUnavailable(definition.label)),
    };
  }
  if (definition.target.kind === "shell") {
    const enabled = definition.enabled;
    const action = definition.target.action;
    return {
      ...definition,
      enabled,
      onSelect: () => (enabled ? runShellAction(action, context) : context.onUnavailable(definition.label)),
    };
  }
  throw new Error(`UNSUPPORTED_COMMAND_TARGET:${definition.id}`);
}

function runShellAction(action: ShellCommandAction, context: CommandRegistryContext): void {
  switch (action) {
    case "toggle-navigation":
      context.onToggleNavigation();
      return;
    case "toggle-context":
      context.onToggleContext();
      return;
    case "toggle-activity":
      context.onToggleActivity();
      return;
    case "toggle-theme":
      context.onToggleTheme();
      return;
    case "open-global-search":
      context.onOpenGlobalSearch();
      return;
    case "clear-search-query":
      context.onUnavailable("Clear search query");
      return;
    case "open-shell-status":
      context.onOpenShellStatus();
      return;
    case "show-governance-notification":
      context.onShowGovernanceNotification();
      return;
    case "open-assistant-surfaces":
      if (context.onOpenAssistantSurface) {
        context.onOpenAssistantSurface();
      } else {
        context.onUnavailable("Open Assistant Surfaces");
      }
      return;
    case "focus-navigation":
      context.onFocusRegion("B");
      return;
    case "focus-workspace":
      context.onFocusRegion("C");
      return;
    case "focus-context":
      context.onFocusRegion("D");
      return;
    case "focus-activity":
      context.onFocusRegion("E");
      return;
  }
}

export function commandMatches(command: RegisteredCommand, query: string): boolean {
  const normalized = query.trim().toLowerCase();
  if (!normalized) return true;
  return (
    command.label.toLowerCase().includes(normalized) ||
    command.group.toLowerCase().includes(normalized) ||
    command.keywords.some((keyword) => keyword.toLowerCase().includes(normalized))
  );
}
