import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { ProtectedRoute } from "../../auth/ProtectedRoute";
import { InstitutionalWorkspaceShell } from "./InstitutionalWorkspaceShell";
import { CURRENT_PROTECTED_ROUTES, WORKSPACE_REGISTRY } from "../registry/workspaceRegistry";

type MockAuthState = {
  operator: { username: string; role: string } | null;
  loading: boolean;
  isAuthenticated: boolean;
  logout: ReturnType<typeof vi.fn>;
  login: ReturnType<typeof vi.fn>;
  refreshProfile: ReturnType<typeof vi.fn>;
};

const mockLogout = vi.fn();
const authState = vi.hoisted((): { value: MockAuthState } => ({
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

function renderShell(initialPath = "/", content = "Existing workspace content") {
  render(
    <MemoryRouter initialEntries={[initialPath]}>
      <Routes>
        <Route
          element={
            <ProtectedRoute>
              <InstitutionalWorkspaceShell />
            </ProtectedRoute>
          }
        >
          <Route path={initialPath} element={<h1>{content}</h1>} />
        </Route>
        <Route path="/login" element={<div>Operator login required</div>} />
      </Routes>
    </MemoryRouter>,
  );
}

beforeEach(() => {
  mockLogout.mockReset();
  authState.value = {
    operator: { username: "operator", role: "admin" },
    loading: false,
    isAuthenticated: true,
    logout: mockLogout,
    login: vi.fn(),
    refreshProfile: vi.fn(),
  };
});

describe("InstitutionalWorkspaceShell", () => {
  it("InstitutionalWorkspaceShell renders Regions A–F (header/nav/workspace/context/activity/overlay)", () => {
    renderShell("/", "Operations workspace mounted");

    expect(screen.getByLabelText("Global command bar")).toBeInTheDocument();
    expect(screen.getByLabelText("Institutional workflow navigation")).toBeInTheDocument();
    expect(screen.getByLabelText("Primary workspace")).toBeInTheDocument();
    expect(screen.getByLabelText("Context panel")).toBeInTheDocument();
    expect(screen.getByLabelText("Activity dock")).toBeInTheDocument();
    expect(screen.getByLabelText("Overlay layer")).toBeInTheDocument();
    expect(screen.getByText("Operations workspace mounted")).toBeInTheDocument();
  });

  it("WorkspaceRegistry contains every current protected route (canonical, noActuation)", () => {
    const expectedRoutes = [
      "/",
      "/live",
      "/charts",
      "/chart",
      "/signals",
      "/analytics",
      "/intelligence",
      "/investigate",
      "/compare-scenarios",
      "/trade-plans",
      "/execution-research",
      "/portfolio-research",
      "/journal",
      "/research-management",
      "/governance",
      "/workspace",
    ];
    expect(CURRENT_PROTECTED_ROUTES.sort()).toEqual(expectedRoutes.sort());
    expect(WORKSPACE_REGISTRY.every((workspace) => workspace.requiresAuth)).toBe(true);
    expect(WORKSPACE_REGISTRY.every((workspace) => workspace.noActuation)).toBe(true);
    for (const workspace of WORKSPACE_REGISTRY) {
      expect(workspace.displayName).toBeTruthy();
      expect(workspace.navigationCategory).toBeTruthy();
      expect(workspace.icon).toBeTruthy();
      expect(workspace.rbac.allowedRoles.length).toBeGreaterThan(0);
      expect(workspace.defaultLayout.primaryRegion).toBe("workspace");
      expect(typeof workspace.contextPanel.supported).toBe("boolean");
      expect(typeof workspace.activityDock.supported).toBe("boolean");
      expect(typeof workspace.search.enabled).toBe("boolean");
      expect(workspace.keyboardShortcut).toBeTruthy();
      expect(workspace.telemetryId).toBeTruthy();
      expect(workspace.workspaceVersion).toBeTruthy();
      expect("featureFlag" in workspace).toBe(true);
    }
    expect(new Set(WORKSPACE_REGISTRY.map((workspace) => workspace.id)).size).toBe(
      WORKSPACE_REGISTRY.length,
    );
  });

  it("WorkspaceHost mounts each existing page content by route (no page regression)", () => {
    for (const route of CURRENT_PROTECTED_ROUTES) {
      renderShell(route, `content for ${route}`);
      expect(screen.getByText(`content for ${route}`)).toBeInTheDocument();
      document.body.innerHTML = "";
    }
  }, 30000);

  it("test_shell_hosts_only_no_business_logic_in_shell", async () => {
    const modules = import.meta.glob("../**/*.{ts,tsx,css}", {
      query: "?raw",
      import: "default",
    });
    const productionLoaders = Object.entries(modules)
      .filter(([path]) => !path.includes(".test."))
      .filter(([path]) => !path.includes("/persistence/"))
      .map(([, loader]) => loader);
    const texts = await Promise.all(productionLoaders.map((loader) => loader()));
    const shellText = texts.join("\n");
    const forbidden = [
      "fetchWorkspacePreferences",
      "createWorkspacePreference",
      "updateWorkspacePreference",
      "createResearchCollection",
      "createResearchTag",
      "fetchPortfolioResearchDashboard",
      "/api/v1/",
      "place_order",
      "model_artifact",
    ];
    for (const marker of forbidden) {
      expect(shellText).not.toContain(marker);
    }
  });

  it("test_command_palette_navigation_only_no_business_actions", async () => {
    renderShell();
    fireEvent.keyDown(window, { key: "k", ctrlKey: true });
    const dialog = await screen.findByRole("dialog", { name: "Command palette" });
    expect(dialog).toBeInTheDocument();
    expect(screen.getAllByText("Navigate").length).toBeGreaterThan(0);
    const text = dialog.textContent?.toLowerCase() ?? "";
    for (const marker of ["save", "create", "update", "submit", "place", "connect"]) {
      expect(text).not.toContain(marker);
    }
  });

  it("shell exposes no execution/order/broker/account/go-live/actuation controls (any region)", () => {
    renderShell();
    const buttonText = screen
      .getAllByRole("button")
      .map((button) => button.textContent?.toLowerCase() ?? "")
      .join(" ");
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
      expect(buttonText).not.toContain(marker);
    }
  });

  it("shell displays Gate CLOSED / research-only framing", () => {
    renderShell();
    expect(screen.getAllByText(/Gate CLOSED/i).length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText(/Research-only/i).length).toBeGreaterThanOrEqual(1);
  });

  it("shell provides ARIA landmarks and keyboard focus-transition between regions", async () => {
    renderShell();
    const rail = screen.getByLabelText("Module Launcher Rail");
    const workspace = screen.getByLabelText("Primary workspace");

    fireEvent.keyDown(window, { key: "1", altKey: true });
    expect(document.activeElement).toBe(rail);
    fireEvent.keyDown(window, { key: "2", altKey: true });
    expect(document.activeElement).toBe(workspace);

    fireEvent.keyDown(window, { key: "k", ctrlKey: true });
    await waitFor(() => expect(screen.getByLabelText("Search workspaces and shell commands")).toHaveFocus());
  });

  it("protected shell route blocks logged-out access / redirects to login", () => {
    authState.value = {
      operator: null,
      loading: false,
      isAuthenticated: false,
      logout: mockLogout,
      login: vi.fn(),
      refreshProfile: vi.fn(),
    };
    renderShell("/signals", "Signals workspace mounted");
    expect(screen.getByText("Operator login required")).toBeInTheDocument();
    expect(screen.queryByTestId("institutional-workspace-shell")).not.toBeInTheDocument();
  });

  it("test_terminal_layout_retired_shell_is_sole_frame", async () => {
    const modules = import.meta.glob("../../**/*.{ts,tsx}", {
      query: "?raw",
      import: "default",
    });
    const productionEntries = Object.entries(modules).filter(
      ([path]) => !path.includes(".test."),
    );
    const loaded = await Promise.all(
      productionEntries.map(async ([path, loader]) => ({ path, text: await loader() })),
    );
    const offenders = loaded
      .filter(({ text }) => text.includes("TerminalLayout"))
      .map(({ path }) => path);
    expect(offenders).toEqual([]);
    expect(loaded.some(({ text }) => text.includes("InstitutionalWorkspaceShell"))).toBe(true);
  });

  it("test_all_routes_mount_only_through_workspace_shell_no_regression", () => {
    for (const route of CURRENT_PROTECTED_ROUTES) {
      renderShell(route, `shell content for ${route}`);
      expect(screen.getByTestId("institutional-workspace-shell")).toBeInTheDocument();
      expect(screen.getByText(`shell content for ${route}`)).toBeInTheDocument();
      expect(screen.getByLabelText("Primary workspace")).toBeInTheDocument();
      document.body.innerHTML = "";
    }
  });

  it("test_shell_contains_no_execution_or_actuation_after_retirement", async () => {
    const modules = import.meta.glob("../**/*.{ts,tsx,css}", {
      query: "?raw",
      import: "default",
    });
    const productionLoaders = Object.entries(modules)
      .filter(([path]) => !path.includes(".test."))
      .map(([, loader]) => loader);
    const sourceText = (await Promise.all(productionLoaders.map((loader) => loader()))).join("\n");
    const forbidden = [
      "place_order",
      "submit order",
      "go_live",
      "connect_broker",
      "account_id",
      "order_ticket",
    ];
    for (const marker of forbidden) {
      expect(sourceText).not.toContain(marker);
    }
  });
});
