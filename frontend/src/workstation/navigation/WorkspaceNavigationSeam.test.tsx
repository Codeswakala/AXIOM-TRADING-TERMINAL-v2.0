import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { toShellPreferenceWrite } from "../persistence/shellPreferences";
import { defaultLayoutForWorkspace } from "../panels/layoutManager";
import { InstitutionalWorkspaceShell } from "../components/InstitutionalWorkspaceShell";
import {
  WORKSPACE_REGISTRY,
  type WorkspaceDefinition,
} from "../registry/workspaceRegistry";
import { generateNavigationSections } from "./navigationGenerator";
import { WorkspaceSwitcher } from "./WorkspaceSwitcher";
import {
  allContextNavigationTargetsAreRegistered,
  contextNavigationTargets,
} from "./contextNavigation";
import { recordRecentWorkspace } from "./workspaceHistory";

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

vi.mock("../persistence/shellPreferences", async (importOriginal) => {
  const actual = await importOriginal<typeof import("../persistence/shellPreferences")>();
  return {
    ...actual,
    loadShellLayoutPreference: vi.fn().mockResolvedValue(null),
    persistShellLayoutPreference: vi.fn().mockResolvedValue({}),
  };
});

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

async function readRawSource(pathSuffix: string): Promise<string> {
  const modules = import.meta.glob("../**/*.{ts,tsx}", {
    query: "?raw",
    import: "default",
  });
  const parts = pathSuffix.split("/");
  const fileName = parts[parts.length - 1] ?? pathSuffix;
  const entry = Object.entries(modules).find(
    ([path]) => path.endsWith(pathSuffix) || path.endsWith(fileName),
  );
  if (!entry) throw new Error(`Raw source not found: ${pathSuffix}`);
  const loader = entry[1] as () => Promise<string>;
  return loader();
}

function objectText(value: unknown): string {
  return JSON.stringify(value).toLowerCase();
}

describe("UI-002-P02 workspace switcher and context-navigation seam", () => {
  it("test_ui002_workspace_switcher_uses_registry_and_rbac_visible_entries", () => {
    const adminOnlyWorkspace: WorkspaceDefinition = {
      ...WORKSPACE_REGISTRY[0],
      id: "govern.admin_only_fixture",
      route: "/admin-only-fixture",
      displayName: "Admin Only Fixture",
      navigationCategory: "Govern",
      rbac: { allowedRoles: ["admin"] },
      aliasFor: undefined,
    };
    const sections = generateNavigationSections({
      workspaces: [...WORKSPACE_REGISTRY, adminOnlyWorkspace],
      operator: { role: "operator" },
    });
    const visibleIds = sections.flatMap((section) => section.workspaces.map((workspace) => workspace.id));
    expect(visibleIds).toContain("monitor.operations");
    expect(visibleIds).not.toContain("govern.admin_only_fixture");
    expect(visibleIds).not.toContain("monitor.chart_alias");

    render(
      <WorkspaceSwitcher
        sections={sections}
        activeWorkspaceId="monitor.operations"
        recentWorkspaceIds={[]}
        onNavigate={() => undefined}
      />,
    );
    fireEvent.click(screen.getByRole("button", { name: "Workspace switcher" }));
    const menu = screen.getByRole("menu", { name: "Workspace switcher" });
    expect(within(menu).getByRole("menuitem", { name: /Operations/i })).toBeInTheDocument();
    expect(within(menu).queryByText("Admin Only Fixture")).not.toBeInTheDocument();
  });

  it("test_ui002_workspace_switcher_preserves_single_ui001_shell_frame", () => {
    renderShell("/signals");
    const header = screen.getByLabelText("Global command bar");
    const switcher = screen.getByRole("button", { name: "Workspace switcher" });

    expect(header.contains(switcher)).toBe(true);
    expect(screen.getAllByLabelText("Global command bar")).toHaveLength(1);
    expect(screen.getAllByLabelText("Institutional workflow navigation")).toHaveLength(1);
    expect(screen.getAllByTestId("institutional-workspace-shell")).toHaveLength(1);
    fireEvent.click(switcher);
    expect(screen.getAllByRole("menu", { name: "Workspace switcher" })).toHaveLength(1);
    expect(screen.queryByRole("dialog", { name: "Command palette" })).not.toBeInTheDocument();
  });

  it("test_ui002_context_navigation_suggests_read_only_registered_routes_only", () => {
    renderShell("/signals");
    const registeredRoutes = new Set(WORKSPACE_REGISTRY.map((workspace) => workspace.route));
    const panel = screen.getByLabelText("Related workflow navigation");
    const targets = contextNavigationTargets(WORKSPACE_REGISTRY.find((item) => item.route === "/signals")!);
    expect(targets.length).toBeGreaterThan(0);
    expect(allContextNavigationTargetsAreRegistered()).toBe(true);

    const links = within(panel).getAllByRole("link");
    expect(links.length).toBe(targets.length);
    for (const link of links) {
      const pathname = new URL(link.getAttribute("href") ?? "", "http://localhost").pathname;
      expect(registeredRoutes.has(pathname)).toBe(true);
      expect(link).toHaveAttribute("data-result-action", "navigate");
      expect(link).toHaveAttribute("data-readonly", "true");
    }
    expect(within(panel).getByText(/read-only navigation targets/i)).toBeInTheDocument();
  });

  it("test_ui002_workspace_switching_is_keyboard_operable", async () => {
    renderShell("/");
    const trigger = screen.getByRole("button", { name: "Workspace switcher" });
    trigger.focus();
    fireEvent.keyDown(trigger, { key: "Enter" });
    const menu = await screen.findByRole("menu", { name: "Workspace switcher" });
    const signalsItem = within(menu).getByRole("menuitem", { name: /Advisory Signals/i });
    signalsItem.focus();
    fireEvent.keyDown(signalsItem, { key: "Enter" });

    expect(await screen.findByText("Advisory Signals content")).toBeInTheDocument();
    await waitFor(() => expect(trigger).toHaveFocus());
  });

  it("test_ui002_navigation_recents_do_not_persist_search_queries_or_business_payloads", async () => {
    expect(recordRecentWorkspace([], "monitor.operations", "research.advisory_signals")).toEqual([
      "monitor.operations",
    ]);
    const payload = toShellPreferenceWrite({
      activeWorkspaceId: "research.advisory_signals",
      lastRoute: "/signals",
      navigationCollapsed: false,
      panelLayout: defaultLayoutForWorkspace("research.advisory_signals"),
      // BO-F-00 supersession: the pre-F-00 "dark"/"light" vocabulary is
      // replaced by the six-theme set; "dark" is now spelled "midnight".
      themeMode: "midnight",
      updatedAt: "2026-07-22T00:00:00.000Z",
    });
    const persistedText = objectText(payload);
    const forbiddenPersistedMarkers = [
      "recent_workspaces",
      "search_query",
      "searchqueries",
      "artifact_payload",
      "business_payload",
      "order_ticket",
      "account_id",
      "open_gate",
    ];
    for (const marker of forbiddenPersistedMarkers) {
      expect(persistedText).not.toContain(marker);
    }

    const historySource = await readRawSource("navigation/workspaceHistory.ts");
    expect(historySource).not.toContain("localStorage");
    expect(historySource).not.toContain("sessionStorage");
    expect(historySource).not.toContain("fetchWorkspacePreferences");
    expect(historySource).not.toContain("persistShellLayoutPreference");
    expect(historySource).not.toContain("recent_workspaces");
  });

  it("test_ui002_context_navigation_contains_no_business_actions", async () => {
    renderShell("/signals");
    const panelText = screen.getByLabelText("Related workflow navigation").textContent?.toLowerCase() ?? "";
    const productionSource = (
      await Promise.all(
        [
          "navigation/WorkspaceSwitcher.tsx",
          "navigation/ContextNavigationPanel.tsx",
          "navigation/contextNavigation.ts",
          "navigation/workspaceHistory.ts",
        ].map((path) => readRawSource(path)),
      )
    ).join("\n").toLowerCase();
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
      expect(panelText).not.toContain(marker);
      expect(productionSource).not.toContain(marker);
    }
  });
});
