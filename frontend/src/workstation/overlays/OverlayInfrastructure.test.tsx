import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { createCommandRegistry } from "../commands/commandRegistry";
import { OverlayProvider, useOverlayController } from "./OverlayProvider";
import { OverlayLayer } from "./OverlayLayer";
import { NOTIFICATION_DEFINITIONS, NOTIFICATION_KINDS } from "./overlayTypes";
import { WORKSPACE_REGISTRY } from "../registry/workspaceRegistry";

function OverlayHarness() {
  const overlay = useOverlayController();
  const visibleWorkspaces = WORKSPACE_REGISTRY.filter((workspace) => !workspace.aliasFor);
  const routeByWorkspaceId = new Map(WORKSPACE_REGISTRY.map((workspace) => [workspace.id, workspace.route]));
  const commands = createCommandRegistry({
    visibleWorkspaceIds: new Set(visibleWorkspaces.map((workspace) => workspace.id)),
    routeForWorkspaceId: (workspaceId) => routeByWorkspaceId.get(workspaceId) ?? null,
    recentWorkspaceIds: [],
    onNavigate: () => undefined,
    onToggleNavigation: () => undefined,
    onToggleContext: () => undefined,
    onToggleActivity: () => undefined,
    onToggleTheme: overlay.toggleTheme,
    onOpenGlobalSearch: overlay.openGlobalSearch,
    onOpenShellStatus: () => overlay.openDialog({ title: "Shell status", body: "Status" }),
    onShowGovernanceNotification: () => overlay.notify("Governance", "Gate CLOSED", "Research-only"),
    onFocusRegion: () => undefined,
    onUnavailable: () => undefined,
  });
  return (
    <>
      <button type="button" onClick={overlay.openCommandPalette}>
        Open palette
      </button>
      <button
        type="button"
        onClick={() => overlay.openDialog({ title: "Test dialog", body: "Dialog body" })}
      >
        Open dialog
      </button>
      <button
        type="button"
        onClick={() => overlay.notify("Information", "Info notice", "Information message")}
      >
        Notify
      </button>
      <OverlayLayer commands={commands} onNavigate={() => undefined} />
    </>
  );
}

function renderOverlayHarness() {
  render(
    <OverlayProvider>
      <OverlayHarness />
    </OverlayProvider>,
  );
}

describe("OverlayInfrastructure", () => {
  it("test_region_f_overlay_dialog_notification_all_shell_owned", () => {
    renderOverlayHarness();
    fireEvent.click(screen.getByText("Open palette"));
    expect(screen.getByLabelText("Overlay layer")).toBeInTheDocument();
    expect(screen.getByRole("dialog", { name: "Command palette" })).toBeInTheDocument();
    fireEvent.keyDown(screen.getByRole("dialog", { name: "Command palette" }), { key: "Escape" });
    fireEvent.click(screen.getByText("Open dialog"));
    expect(screen.getByRole("dialog", { name: "Test dialog" })).toBeInTheDocument();
    fireEvent.click(screen.getByText("Notify"));
    expect(screen.getByLabelText("Notification layer")).toBeInTheDocument();
    expect(screen.getByRole("alert", { name: "Information: Info notice" })).toBeInTheDocument();
  });

  it("test_notification_service_centralized_six_types_never_color_alone", () => {
    expect(NOTIFICATION_KINDS).toEqual([
      "Information",
      "Success",
      "Warning",
      "Error",
      "Governance",
      "System",
    ]);
    for (const kind of NOTIFICATION_KINDS) {
      const definition = NOTIFICATION_DEFINITIONS[kind];
      expect(definition.icon).toBeTruthy();
      expect(definition.label).toBe(kind);
      expect(definition.semanticRole).toBeTruthy();
    }
  });

  it("test_command_palette_navigation_only_no_business_actions", () => {
    renderOverlayHarness();
    fireEvent.click(screen.getByText("Open palette"));
    const dialog = screen.getByRole("dialog", { name: "Command palette" });
    expect(dialog).toBeInTheDocument();
    const text = dialog.textContent?.toLowerCase() ?? "";
    expect(text).toContain("navigate");
    expect(text).toContain("ui toggle");
    for (const marker of ["buy", "sell", "order", "broker", "open gate", "account"]) {
      expect(text).not.toContain(marker);
    }
  });

  it("test_overlay_accessibility_focus_trap_esc_and_aria_roles", async () => {
    renderOverlayHarness();
    fireEvent.click(screen.getByText("Open dialog"));
    const dialog = screen.getByRole("dialog", { name: "Test dialog" });
    const close = screen.getByRole("button", { name: "Close dialog" });
    await waitFor(() => expect(close).toHaveFocus());
    fireEvent.keyDown(dialog, { key: "Tab" });
    expect(close).toHaveFocus();
    fireEvent.keyDown(dialog, { key: "Escape" });
    expect(screen.queryByRole("dialog", { name: "Test dialog" })).not.toBeInTheDocument();
  });

  it("test_no_hardcoded_color_all_visual_values_from_tokens", async () => {
    const modules = import.meta.glob("../**/*.{css,ts,tsx}", {
      query: "?raw",
      import: "default",
    });
    const productionLoaders = Object.entries(modules)
      .filter(([path]) => !path.includes(".test."))
      .filter(([path]) => !path.includes("design/tokens.css"))
      .map(([, loader]) => loader);
    const text = (await Promise.all(productionLoaders.map((loader) => loader()))).join("\n");
    expect(text).not.toMatch(/#[0-9a-fA-F]{3,8}/);
    expect(text).not.toMatch(/rgba?\(/);
  });
});
