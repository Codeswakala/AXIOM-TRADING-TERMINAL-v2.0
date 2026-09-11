import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { InstitutionalWorkspaceShell } from "../components/InstitutionalWorkspaceShell";
import { WORKSPACE_REGISTRY } from "../registry/workspaceRegistry";
import {
  assertVettedCommandDefinition,
  createCommandRegistry,
  validateQuickActionCatalogue,
} from "./commandRegistry";
import type { CommandRegistryContext, QuickActionDefinition } from "./commandTypes";
import { QUICK_ACTION_CATALOGUE, QUICK_ACTION_CATALOGUE_IDS } from "./quickActionCatalogue";

const authState = vi.hoisted(() => ({
  value: {
    operator: { username: "operator", role: "admin" },
    loading: false,
    isAuthenticated: true,
    logout: vi.fn(),
    login: vi.fn(),
    refreshProfile: vi.fn(),
  },
}));

vi.mock("../../context/AuthContext", () => ({
  useAuth: () => authState.value,
}));

vi.mock("../persistence/shellPreferences", () => ({
  loadShellLayoutPreference: vi.fn().mockResolvedValue(null),
  persistShellLayoutPreference: vi.fn().mockResolvedValue({}),
}));

function commandContext(overrides: Partial<CommandRegistryContext> = {}): CommandRegistryContext {
  const visibleWorkspaces = WORKSPACE_REGISTRY.filter((workspace) => !workspace.aliasFor);
  const routeByWorkspaceId = new Map(WORKSPACE_REGISTRY.map((workspace) => [workspace.id, workspace.route]));
  return {
    visibleWorkspaceIds: new Set(visibleWorkspaces.map((workspace) => workspace.id)),
    routeForWorkspaceId: (workspaceId) => routeByWorkspaceId.get(workspaceId) ?? null,
    recentWorkspaceIds: ["monitor.operations"],
    onNavigate: vi.fn(),
    onToggleNavigation: vi.fn(),
    onToggleContext: vi.fn(),
    onToggleActivity: vi.fn(),
    onToggleTheme: vi.fn(),
    onOpenGlobalSearch: vi.fn(),
    onOpenShellStatus: vi.fn(),
    onShowGovernanceNotification: vi.fn(),
    onFocusRegion: vi.fn(),
    onUnavailable: vi.fn(),
    ...overrides,
  };
}

function renderShell(path = "/") {
  render(
    <MemoryRouter initialEntries={[path]}>
      <Routes>
        <Route element={<InstitutionalWorkspaceShell />}>
          {WORKSPACE_REGISTRY.map((workspace) => (
            <Route
              key={workspace.route}
              path={workspace.route}
              element={<h1>{workspace.displayName} content</h1>}
            />
          ))}
        </Route>
      </Routes>
    </MemoryRouter>,
  );
}

describe("UI-002-P03 command registry and palette", () => {
  it("test_ui002_command_palette_extends_existing_palette_not_second_palette", () => {
    renderShell("/");
    fireEvent.click(screen.getByRole("button", { name: /Command palette/i }));

    const palette = screen.getByRole("dialog", { name: "Command palette" });
    expect(palette).toHaveAttribute("data-ui002-component", "command-palette-registry");
    expect(screen.getAllByRole("dialog", { name: "Command palette" })).toHaveLength(1);
    expect(screen.getAllByLabelText("Overlay layer")).toHaveLength(1);
    expect(within(palette).getByText("Observe")).toBeInTheDocument();
    expect(within(palette).getByText("Shell Controls")).toBeInTheDocument();
    expect(within(palette).getAllByRole("menuitem")).toHaveLength(33);
  });

  it("test_ui002_command_registry_accepts_only_navigation_or_ui_toggle_commands", () => {
    expect(validateQuickActionCatalogue()).toBe(true);
    const registry = createCommandRegistry(commandContext());
    expect(registry).toHaveLength(33);
    expect(registry.every((command) => ["navigation", "ui-toggle"].includes(command.commandType))).toBe(
      true,
    );

    const unsupportedType = {
      ...QUICK_ACTION_CATALOGUE[0],
      commandType: "workflow-mutation",
    } as unknown as QuickActionDefinition;
    expect(() => assertVettedCommandDefinition(unsupportedType)).toThrow(/UNSUPPORTED_COMMAND_TYPE/);
  });

  it("test_ui002_quick_action_catalogue_is_itemized_and_registered", () => {
    const registry = createCommandRegistry(commandContext());
    const registeredIds = registry.map((command) => command.id);
    expect(QUICK_ACTION_CATALOGUE_IDS).toHaveLength(33);
    expect(new Set(QUICK_ACTION_CATALOGUE_IDS).size).toBe(33);
    expect(registeredIds).toEqual(QUICK_ACTION_CATALOGUE_IDS);
    expect(registeredIds.every((id) => id.startsWith("qa."))).toBe(true);
    expect(registry.every((command) => command.source === "quick-action-catalogue")).toBe(true);
  });

  it("test_ui002_quick_actions_are_navigation_or_ui_toggle_only", () => {
    const registry = createCommandRegistry(commandContext());
    expect(registry.filter((command) => command.commandType === "navigation")).toHaveLength(21);
    expect(registry.filter((command) => command.commandType === "ui-toggle")).toHaveLength(12);
    expect(registry.every((command) => command.noActuation)).toBe(true);
    expect(registry.every((command) => command.target.kind === "route" || command.target.kind === "shell" || command.target.kind.includes("workspace"))).toBe(true);
  });

  it("test_ui002_command_registry_rejects_business_trading_execution_broker_account_gate_actions", () => {
    const unvetted = {
      ...QUICK_ACTION_CATALOGUE[0],
      id: "qa.place-live-instruction",
      label: "Place live instruction",
    } as QuickActionDefinition;
    expect(() => assertVettedCommandDefinition(unvetted)).toThrow(/UNVETTED_COMMAND/);

    const unsafe = {
      ...QUICK_ACTION_CATALOGUE[0],
      noActuation: false,
    } as unknown as QuickActionDefinition;
    expect(() => assertVettedCommandDefinition(unsafe)).toThrow(/UNSAFE_COMMAND/);
  });

  it("test_ui002_command_palette_keyboard_focus_and_escape_restore", async () => {
    renderShell("/");
    const trigger = screen.getByRole("button", { name: /Command palette/i });
    trigger.focus();
    fireEvent.keyDown(window, { key: "k", ctrlKey: true });

    const input = await screen.findByLabelText("Search workspaces and shell commands");
    expect(input).toHaveFocus();
    fireEvent.change(input, { target: { value: "theme" } });
    expect(screen.getByRole("menuitem", { name: /Toggle Institutional Theme/i })).toBeInTheDocument();

    fireEvent.keyDown(screen.getByRole("dialog", { name: "Command palette" }), { key: "Escape" });
    await waitFor(() => expect(screen.queryByRole("dialog", { name: "Command palette" })).not.toBeInTheDocument());
    expect(trigger).toHaveFocus();
  });
});
