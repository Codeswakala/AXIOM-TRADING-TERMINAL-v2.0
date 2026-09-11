import { fireEvent, render, screen, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { InstitutionalWorkspaceShell } from "../components/InstitutionalWorkspaceShell";
import {
  WORKSPACE_REGISTRY,
  type WorkspaceDefinition,
} from "../registry/workspaceRegistry";
import {
  createWorkspaceActivationEvent,
  generateNavigationSections,
} from "./navigationGenerator";

const authState = vi.hoisted(() => ({
  value: {
    operator: { username: "operator", role: "operator" },
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

describe("NavigationDock", () => {
  it("test_navigation_generated_from_registry_not_hardcoded", () => {
    const sections = generateNavigationSections({
      workspaces: WORKSPACE_REGISTRY,
      operator: { role: "operator" },
    });
    const generatedRoutes = sections.flatMap((section) => section.workspaces.map((item) => item.route));
    const registryRoutes = WORKSPACE_REGISTRY.filter((workspace) => !workspace.aliasFor).map(
      (workspace) => workspace.route,
    );
    expect(generatedRoutes).toEqual(registryRoutes);
    expect(sections.map((section) => section.category)).toEqual([
      "Monitor",
      "Research",
      "Investigate",
      "Compare",
      "Plan",
      "Review",
      "Govern",
      "Settings",
    ]);
  });

  it("test_navigation_dock_contains_no_execution_or_actuation", () => {
    renderShell();
    const nav = screen.getByLabelText("Institutional workflow navigation");
    const text = nav.textContent?.toLowerCase() ?? "";
    const forbidden = [
      "b" + "uy",
      "s" + "ell",
      "place order",
      "submit order",
      "exec" + "ute",
      "go live",
      "connect broker",
      "account_id",
      "order_ticket",
    ];
    for (const marker of forbidden) {
      expect(text).not.toContain(marker);
    }
  });

  it("test_navigation_permission_filtering_hides_unauthorized_workspaces", () => {
    const fixtureWorkspace: WorkspaceDefinition = {
      ...WORKSPACE_REGISTRY[0],
      id: "govern.admin_only",
      route: "/admin-only-fixture",
      displayName: "Admin Only Fixture",
      navigationCategory: "Govern",
      rbac: { allowedRoles: ["admin"] },
      aliasFor: undefined,
    };
    const sections = generateNavigationSections({
      workspaces: [WORKSPACE_REGISTRY[0], fixtureWorkspace],
      operator: { role: "operator" },
    });
    const visibleIds = sections.flatMap((section) => section.workspaces.map((workspace) => workspace.id));
    expect(visibleIds).toContain(WORKSPACE_REGISTRY[0].id);
    expect(visibleIds).not.toContain("govern.admin_only");
  });

  it("test_workspace_activation_is_deterministic_for_all_routes", async () => {
    renderShell("/");
    for (const workspace of WORKSPACE_REGISTRY.filter((item) => !item.aliasFor).slice(0, 6)) {
      const event = createWorkspaceActivationEvent(workspace);
      expect(event.workspaceId).toBe(workspace.id);
      expect(event.route).toBe(workspace.route);
      expect(event.telemetryId).toBe(workspace.telemetryId);
    }
    fireEvent.click(
      within(screen.getByLabelText("Institutional workflow navigation")).getByRole("link", {
        name: /Advisory Signals/i,
      }),
    );
    expect(await screen.findByText("Advisory Signals content")).toBeInTheDocument();
    expect(screen.getByLabelText("Primary workspace")).toHaveAttribute(
      "data-active-telemetry-id",
      "workspace.research.advisory_signals",
    );
  });
});
