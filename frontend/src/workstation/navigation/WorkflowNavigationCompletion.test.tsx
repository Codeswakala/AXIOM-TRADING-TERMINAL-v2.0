import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { QUICK_ACTION_CATALOGUE } from "../commands/quickActionCatalogue";
import { InstitutionalWorkspaceShell } from "../components/InstitutionalWorkspaceShell";
import { contextNavigationTargets } from "./contextNavigation";
import { generateNavigationSections } from "./navigationGenerator";
import { buildBreadcrumbTrail, workflowMetadataForWorkspace } from "../workflows/workflowModel";
import { createWorkspaceSearchSource } from "../search/globalSearchSources";
import { WORKSPACE_REGISTRY, CURRENT_PROTECTED_ROUTES, workspaceForPath } from "../registry/workspaceRegistry";

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
        <Route path="/login" element={<div>Operator login required</div>} />
      </Routes>
    </MemoryRouter>,
  );
}

async function readRawUi002Source(): Promise<string> {
  const modules = import.meta.glob("../**/*.{ts,tsx}", {
    query: "?raw",
    import: "default",
  });
  const texts = await Promise.all(
    Object.entries(modules)
      .filter(([path]) => !path.includes(".test."))
      .filter(
        ([path]) =>
          path.includes("/workflows/") ||
          path.includes("/navigation/") ||
          path.includes("/commands/") ||
          path.includes("/search/") ||
          path.includes("/overlays/"),
      )
      .map(([, loader]) => (loader as () => Promise<string>)()),
  );
  return texts.join("\n");
}

describe("UI-002-P05 workflow navigation completion checkpoint", () => {
  it("test_ui002_context_aware_navigation_preserves_workflow_without_business_logic", async () => {
    renderShell("/signals");
    const panel = screen.getByLabelText("Related workflow navigation");
    expect(within(panel).getByText(/read-only navigation targets/i)).toBeInTheDocument();
    expect(within(panel).getByRole("link", { name: /Signal Investigation/i })).toHaveAttribute(
      "href",
      "/investigate",
    );
    expect(within(panel).getByRole("link", { name: /Performance Analytics/i })).toHaveAttribute(
      "href",
      "/analytics",
    );

    const sourceText = (await readRawUi002Source()).toLowerCase();
    expect(sourceText).not.toContain("/api/v1/search");
    expect(sourceText).not.toContain("createorder");
    expect(sourceText).not.toContain("submit order");
    expect(sourceText).not.toContain("connect broker");
  });

  it("test_ui002_all_routes_keep_single_ui001_shell_navigation_system", () => {
    for (const route of CURRENT_PROTECTED_ROUTES) {
      renderShell(route);
      expect(screen.getAllByTestId("institutional-workspace-shell")).toHaveLength(1);
      expect(screen.getAllByLabelText("Global command bar")).toHaveLength(1);
      expect(screen.getAllByLabelText("Institutional workflow navigation")).toHaveLength(1);
      expect(screen.getAllByLabelText("Overlay layer")).toHaveLength(1);
      expect(screen.getAllByRole("button", { name: "Workspace switcher" })).toHaveLength(1);
      expect(screen.getAllByRole("button", { name: "Global search" })).toHaveLength(1);
      expect(screen.getAllByRole("button", { name: /Command palette/i })).toHaveLength(1);
      expect(screen.getByText(`${workspaceForPath(route).displayName} content`)).toBeInTheDocument();
      cleanup();
    }
  }, 30000);

  it("test_ui002_workflow_navigation_full_surface_contains_no_actuation_controls", async () => {
    const sourceText = (await readRawUi002Source()).toLowerCase();
    const forbidden = [
      "b" + "uy",
      "s" + "ell",
      "place_order",
      "exec" + "ute",
      "go-live",
      "connect-broker",
      "account_id",
      "order_ticket",
      "open_gate",
      "allow_exec" + "ution",
    ];
    for (const marker of forbidden) {
      expect(sourceText).not.toContain(marker);
    }
  });

  it("test_ui002_breadcrumbs_search_palette_and_switcher_remain_registry_consistent", async () => {
    const registeredWorkspaceIds = new Set(WORKSPACE_REGISTRY.map((workspace) => workspace.id));
    const registeredRoutes = new Set(WORKSPACE_REGISTRY.map((workspace) => workspace.route));
    const navigationIds = generateNavigationSections({
      workspaces: WORKSPACE_REGISTRY,
      operator: { role: "admin" },
    }).flatMap((section) => section.workspaces.map((workspace) => workspace.id));

    expect(navigationIds.every((workspaceId) => registeredWorkspaceIds.has(workspaceId))).toBe(true);

    for (const workspace of WORKSPACE_REGISTRY.filter((item) => !item.aliasFor)) {
      const breadcrumbTrail = buildBreadcrumbTrail({ pathname: workspace.route });
      const metadata = workflowMetadataForWorkspace(workspace.id);
      expect(breadcrumbTrail[breadcrumbTrail.length - 1]?.label).toBe(metadata?.breadcrumbLabel ?? workspace.displayName);
      expect(contextNavigationTargets(workspace).every((target) => registeredRoutes.has(target.route))).toBe(true);
    }

    const routeTargets = QUICK_ACTION_CATALOGUE.filter((command) => command.target.kind === "route").map(
      (command) => (command.target.kind === "route" ? command.target.route : ""),
    );
    // CA-CONV2-1 (post-absorption reconciliation): palette route targets may carry
    // dock-activation query parameters (/?view=chart, /?dock=signals, /?dock=intelligence).
    // The PATH component must still resolve to a registered route; the query parameter
    // selects the docked terminal view within it.
    expect(routeTargets.every((route) => registeredRoutes.has(route.split("?")[0]))).toBe(true);

    const workspaceResults = await createWorkspaceSearchSource(WORKSPACE_REGISTRY).fetchResults({
      query: "workspace",
    });
    expect(workspaceResults.every((result) => registeredRoutes.has(result.route))).toBe(true);
    expect(workspaceResults.every((result) => registeredWorkspaceIds.has(result.sourceWorkspaceId))).toBe(true);
  });

  it("test_ui002_completion_checkpoint_preserves_gate_closed_and_research_only_status", async () => {
    renderShell("/signals");
    // SUPERSEDED BY CITATION (BO-FE-U02 §2.2/§2.9, PC-FEU02-1 C4/C9, ACC-1; adopted 2026-09-11): the asserted heritage chips are EXPELLED from the chrome boundary; the truthful cluster renders the locked-config mode badge + live health chip instead.
    // (pin scoped to the CHROME's status cluster — the GovernanceOverlay's 'Gate CLOSED' record entries are OUT-OF-BOUNDARY heritage, protected per PC-FEU02-1 C9 heritage clause, not chrome chips)
    const chromeCluster = screen.getByTestId("shell-governance-status");
    expect(chromeCluster.textContent).not.toContain("Gate CLOSED");
    expect(screen.getByTestId("chrome-mode-badge")).toHaveTextContent(/RESEARCH · NON-ACTUATING/);
    // "Research-only" ×2 pinned the chip + a dock echo; the chip is expelled
    // (same citation) — the surviving out-of-boundary echo is heritage.
    expect(screen.getAllByText("Research-only").length).toBeGreaterThanOrEqual(1);
    expect(screen.queryByText("Presentation shell")).toBeNull();
    expect(screen.getByTestId("chrome-health-chip")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Global search" }));
    expect(await screen.findByRole("dialog", { name: "Global search" })).toBeInTheDocument();
    fireEvent.keyDown(screen.getByRole("dialog", { name: "Global search" }), { key: "Escape" });

    fireEvent.click(screen.getByRole("button", { name: /Command palette/i }));
    const palette = await screen.findByRole("dialog", { name: "Command palette" });
    expect(within(palette).queryByText(/open gate/i)).not.toBeInTheDocument();
    expect(within(palette).queryByText(/connect broker/i)).not.toBeInTheDocument();
  });

  it("test_ui002_completion_checkpoint_frontend_routes_mount_in_shell_without_regression", () => {
    for (const route of CURRENT_PROTECTED_ROUTES) {
      renderShell(route);
      const activeWorkspace = workspaceForPath(route);
      expect(screen.getByTestId("institutional-workspace-shell")).toBeInTheDocument();
      expect(screen.getByLabelText("Primary workspace")).toHaveAttribute(
        "data-active-telemetry-id",
        activeWorkspace.telemetryId,
      );
      expect(screen.getByLabelText("Breadcrumb")).toBeInTheDocument();
      expect(screen.getByLabelText("Context panel")).toBeInTheDocument();
      expect(screen.getByLabelText("Activity dock")).toBeInTheDocument();
      expect(screen.getByText(`${activeWorkspace.displayName} content`)).toBeInTheDocument();
      cleanup();
    }
  });
});
