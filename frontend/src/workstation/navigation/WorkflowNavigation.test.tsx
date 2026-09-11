import { render, screen, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { InstitutionalWorkspaceShell } from "../components/InstitutionalWorkspaceShell";
import { WORKSPACE_REGISTRY, workspaceForPath } from "../registry/workspaceRegistry";
import { BreadcrumbTrail } from "./BreadcrumbTrail";
import { WORKFLOW_NAVIGATION_METADATA } from "../workflows/workflowNavigationMetadata";
import {
  assertWorkflowMetadataValid,
  buildBreadcrumbTrail,
  validateWorkflowMetadata,
  workflowMetadataForWorkspace,
} from "../workflows/workflowModel";

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

async function readRawSource(pathSuffix: string): Promise<string> {
  const modules = import.meta.glob("../**/*.{ts,tsx}", {
    query: "?raw",
    import: "default",
  });
  const entry = Object.entries(modules).find(([path]) => path.endsWith(pathSuffix));
  if (!entry) throw new Error(`Raw source not found: ${pathSuffix}`);
  const loader = entry[1] as () => Promise<string>;
  return loader();
}

function renderShell(path = "/signals") {
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

describe("UI-002-P01 workflow navigation foundation", () => {
  it("test_ui002_workflow_metadata_extends_ui001_registry_without_duplication", async () => {
    const registrySource = await readRawSource("registry/workspaceRegistry.tsx");
    const metadataSource = await readRawSource("workflows/workflowNavigationMetadata.ts");

    expect(metadataSource).toContain("workspaceId");
    expect(metadataSource).toContain("primaryStage");
    expect(registrySource).not.toContain("WorkflowNavigationMetadata");
    expect(registrySource).not.toContain("primaryStage");
    expect(registrySource).not.toContain("breadcrumbLabel");

    for (const item of WORKFLOW_NAVIGATION_METADATA) {
      const record = item as unknown as Record<string, unknown>;
      expect(record.route).toBeUndefined();
      expect(record.rbac).toBeUndefined();
      expect(record.defaultLayout).toBeUndefined();
      expect(record.requiresAuth).toBeUndefined();
      expect(record.noActuation).toBeUndefined();
    }
  });

  it("test_ui002_workflow_metadata_references_only_registered_workspaces", () => {
    const validation = validateWorkflowMetadata();
    expect(validation.valid).toBe(true);
    expect(validation.orphanWorkspaceIds).toEqual([]);
    expect(validation.missingWorkspaceIds).toEqual([]);
    expect(validation.invalidReferences).toEqual([]);
    expect(() => assertWorkflowMetadataValid()).not.toThrow();

    const registeredIds = new Set(WORKSPACE_REGISTRY.map((workspace) => workspace.id));
    for (const item of WORKFLOW_NAVIGATION_METADATA) {
      expect(registeredIds.has(item.workspaceId)).toBe(true);
      for (const relatedId of [
        ...item.relatedWorkspaceIds,
        ...item.defaultNextWorkspaceIds,
        ...item.defaultPreviousWorkspaceIds,
      ]) {
        expect(registeredIds.has(relatedId)).toBe(true);
      }
    }
  });

  it("test_ui002_breadcrumbs_are_route_registry_derived_and_deterministic", () => {
    const first = buildBreadcrumbTrail({ pathname: "/signals" });
    const second = buildBreadcrumbTrail({ pathname: "/signals" });
    const activeWorkspace = workspaceForPath("/signals");
    const metadata = workflowMetadataForWorkspace(activeWorkspace.id);

    expect(first).toEqual(second);
    expect(first.map((item) => item.label)).toEqual(["AXIOM", "Detect", "Advisory Signals"]);
    expect(first[2]).toMatchObject({
      id: `workspace.${activeWorkspace.id}`,
      label: metadata?.breadcrumbLabel,
      current: true,
    });

    const researchManagement = buildBreadcrumbTrail({ pathname: "/research-management" });
    expect(researchManagement.map((item) => item.label)).toEqual([
      "AXIOM",
      "Document",
      "Research Management",
    ]);
  });

  it("test_ui002_breadcrumbs_are_accessible_and_keyboard_navigable", () => {
    render(
      <MemoryRouter initialEntries={["/research-management"]}>
        <BreadcrumbTrail />
      </MemoryRouter>,
    );

    const breadcrumb = screen.getByLabelText("Breadcrumb");
    expect(breadcrumb).toHaveAttribute("data-region", "A");
    const current = within(breadcrumb).getByText("Research Management");
    expect(current).toHaveAttribute("aria-current", "page");

    const links = within(breadcrumb).getAllByRole("link");
    expect(links.length).toBeGreaterThan(0);
    expect(links[0]).toHaveAttribute("href", "/");
    links[0].focus();
    expect(links[0]).toHaveFocus();
  });

  it("test_ui002_no_independent_navigation_or_competing_layout", () => {
    renderShell("/signals");

    const shell = screen.getByTestId("institutional-workspace-shell");
    const header = screen.getByLabelText("Global command bar");
    const breadcrumb = screen.getByLabelText("Breadcrumb");

    expect(shell).toBeInTheDocument();
    expect(screen.getAllByLabelText("Global command bar")).toHaveLength(1);
    expect(screen.getAllByLabelText("Institutional workflow navigation")).toHaveLength(1);
    expect(screen.getAllByLabelText("Breadcrumb")).toHaveLength(1);
    expect(header.contains(breadcrumb)).toBe(true);
    expect(breadcrumb).toHaveAttribute("data-ui002-component", "breadcrumb-trail");
    expect(screen.getByLabelText("Primary workspace")).toBeInTheDocument();
    expect(screen.queryByText("TerminalLayout")).not.toBeInTheDocument();
  });

  it("test_ui002_workflow_navigation_contains_no_execution_or_actuation_controls", async () => {
    const modules = import.meta.glob("../**/*.{ts,tsx}", {
      query: "?raw",
      import: "default",
    });
    const productionLoaders = Object.entries(modules)
      .filter(([path]) => !path.includes(".test."))
      .filter(([path]) => path.includes("/workflows/") || path.endsWith("navigation/BreadcrumbTrail.tsx"))
      .map(([, loader]) => loader as () => Promise<string>);
    const sourceText = (await Promise.all(productionLoaders.map((loader) => loader()))).join("\n").toLowerCase();
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
});
