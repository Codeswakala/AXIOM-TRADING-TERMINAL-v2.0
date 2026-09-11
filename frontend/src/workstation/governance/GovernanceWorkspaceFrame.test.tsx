import { render, screen, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { ProtectedRoute } from "../../auth/ProtectedRoute";
import { GovernanceEvidenceWorkspace } from "../../components/terminal/governance/GovernanceOverlay";
import { UI007_GOVERNANCE_SOURCES } from "../../components/terminal/governance/governanceRecords";
import { InstitutionalWorkspaceShell } from "../components/InstitutionalWorkspaceShell";
import {
  WORKSPACE_REGISTRY,
  workspaceForPath,
  type WorkspaceRegistrationContract,
} from "../registry/workspaceRegistry";

const authenticatedAuth = () => ({
  operator: { username: "operator", role: "admin" },
  loading: false,
  isAuthenticated: true,
  logout: vi.fn(),
  login: vi.fn(),
  refreshProfile: vi.fn(),
});

const loggedOutAuth = () => ({
  operator: null,
  loading: false,
  isAuthenticated: false,
  logout: vi.fn(),
  login: vi.fn(),
  refreshProfile: vi.fn(),
});

const authState = vi.hoisted(() => ({
  value: {
    operator: { username: "operator", role: "admin" },
    loading: false,
    isAuthenticated: true,
    logout: vi.fn(),
    login: vi.fn(),
    refreshProfile: vi.fn(),
  } as ReturnType<typeof authenticatedAuth> | ReturnType<typeof loggedOutAuth>,
}));

vi.mock("../../context/AuthContext", () => ({
  useAuth: () => authState.value,
}));

vi.mock("../persistence/shellPreferences", () => ({
  loadShellLayoutPreference: vi.fn().mockResolvedValue(null),
  persistShellLayoutPreference: vi.fn().mockResolvedValue({}),
}));

function renderGovernanceShell() {
  return render(
    <MemoryRouter initialEntries={["/governance"]}>
      <Routes>
        <Route element={<InstitutionalWorkspaceShell />}>
          <Route path="/governance" element={<GovernanceEvidenceWorkspace />} />
        </Route>
      </Routes>
    </MemoryRouter>,
  );
}

async function readP01ProductionSource(): Promise<string> {
  const modules = import.meta.glob(
    [
      "../../components/terminal/governance/GovernanceOverlay.tsx",
      "../../components/terminal/governance/governanceRecords.ts",
      "../registry/workspaceRegistry.tsx",
      "../commands/quickActionCatalogue.ts",
    ],
    {
      query: "?raw",
      import: "default",
    },
  );
  const values = await Promise.all(
    Object.values(modules).map((loader) => (loader as () => Promise<string>)()),
  );
  return values.join("\n").toLowerCase();
}

describe("UI-007-P01 governance workspace frame", () => {
  it("test_ui007_governance_workspace_mounts_inside_single_ui001_shell", () => {
    authState.value = authenticatedAuth();
    renderGovernanceShell();

    expect(screen.getAllByTestId("institutional-workspace-shell")).toHaveLength(1);
    expect(screen.getByLabelText("Primary workspace")).toHaveAttribute(
      "data-active-telemetry-id",
      "workspace.govern.governance_evidence",
    );
    expect(screen.getAllByText("Governance & Evidence").length).toBeGreaterThan(0);
    expect(screen.getByLabelText("Governance workspace frame")).toBeInTheDocument();
    expect(screen.getByLabelText("Governance inert status")).toHaveTextContent("Gate CLOSED");
  });

  it("test_ui007_governance_workspace_uses_single_governance_route_and_registry_contract", () => {
    const routeEntries = WORKSPACE_REGISTRY.filter((workspace) => workspace.route === "/governance");
    const workspace = workspaceForPath("/governance");
    const contractKeys: (keyof WorkspaceRegistrationContract)[] = [
      "id",
      "displayName",
      "navigationCategory",
      "route",
      "icon",
      "rbac",
      "defaultLayout",
      "contextPanel",
      "activityDock",
      "search",
      "keyboardShortcut",
      "telemetryId",
      "workspaceVersion",
      "featureFlag",
      "requiresAuth",
      "noActuation",
    ];

    expect(routeEntries).toHaveLength(1);
    expect(workspace.id).toBe("govern.governance_evidence");
    expect(workspace.displayName).toBe("Governance & Evidence");
    expect(workspace.navigationCategory).toBe("Govern");
    expect(workspace.requiresAuth).toBe(true);
    expect(workspace.noActuation).toBe(true);
    for (const key of contractKeys) {
      expect(workspace).toHaveProperty(key);
    }
    expect(WORKSPACE_REGISTRY.some((item) => item.route === "/admin")).toBe(false);
    expect(WORKSPACE_REGISTRY.some((item) => item.route === "/control")).toBe(false);
    expect(WORKSPACE_REGISTRY.some((item) => item.route === "/gate")).toBe(false);
  });

  it("test_ui007_governance_workspace_maps_every_section_to_existing_read_seams", () => {
    render(<GovernanceEvidenceWorkspace />);

    const inventory = screen.getByLabelText("UI-007 governed data-source inventory");
    for (const surface of [
      "Governance status",
      "Audit events",
      "Production status",
      "Platform health",
      "Runtime readiness",
      "Observability metrics",
      "Persistence stats",
      "System version",
      "RBAC vocabulary",
      "Operator scope",
      "Evidence records",
      "Validation summaries",
    ]) {
      expect(inventory).toHaveTextContent(surface);
    }
    for (const seam of [
      "GET /api/v1/persistence/audit-events",
      "GET /api/v1/health",
      "GET /api/v1/ready",
      "GET /api/v1/metrics",
      "GET /api/v1/persistence/stats",
      "GET /api/v1/system/info",
      "GET /api/v1/institutional-platform/route-inventory",
      "GET /api/v1/institutional-platform/rbac/permissions",
      "GET /api/v1/institutional-platform/api-catalogue",
      "GET /api/v1/institutional-platform/plugin-contracts",
      "GET /api/v1/institutional-platform/operator-scope-records",
      "Canonical governance records; no production-status API action",
    ]) {
      expect(inventory).toHaveTextContent(seam);
    }
    expect(UI007_GOVERNANCE_SOURCES).toHaveLength(12);
  });

  it("test_ui007_governance_workspace_contains_no_governance_mutation_gate_or_certification_control", async () => {
    render(<GovernanceEvidenceWorkspace />);

    const buttonText = screen
      .queryAllByRole("button")
      .map((button) => button.textContent?.toLowerCase() ?? "")
      .join(" ");
    const pageText = document.body.textContent?.toLowerCase() ?? "";
    for (const marker of [
      "create governance",
      "update governance",
      "delete governance",
      "gate switch",
      "gate form",
      "approve production",
      "residual disposition action",
      "audit editor",
      "audit mutation",
    ]) {
      expect(buttonText).not.toContain(marker);
      expect(pageText).not.toContain(marker);
    }

    const sourceText = await readP01ProductionSource();
    for (const marker of [
      "open_gate",
      "allow_execution",
      "gate toggle",
      "toggle gate",
      "certify",
      "mark_ready",
      "approve_production",
      "waive",
      "risk_accept",
      "place_order",
      "exec" + "ute",
      "go-live",
      "connect-" + "broker",
      "br" + "oker",
      "account_id",
      "order_ticket",
      "pos" + "ition",
      "bal" + "ance",
      "mar" + "gin",
      "cap" + "ital",
      "alloc" + "ation",
      "real_pnl",
      "infersignal",
      "runinference",
      "authoritativerecompute",
      "emitsignal",
      "generatesignal",
      "generatescenario",
      "inferrelationship",
      "rec" + "ompute",
      "recalculat",
      "deriveconfidence",
      "reclassif",
      "open" + "ai",
      "external_" + "llm",
      "llm_" + "summary",
      "ai_" + "summary",
      "/api/v1/" + "orders",
    ]) {
      expect(sourceText).not.toContain(marker);
    }
  });

  it("test_ui007_governance_workspace_preserves_gate_closed_not_certified_verbatim_and_doc16_branding", () => {
    authState.value = authenticatedAuth();
    const { unmount } = renderGovernanceShell();

    expect(screen.getByText(/AXIOM Institutional Workstation/i)).toBeInTheDocument();
    expect(screen.getAllByText("Gate CLOSED").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("Production NOT CERTIFIED").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText(/Doc 11 HELD/i).length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText(/TD-UI-POSTCSS-HIGH CLOSED/i).length).toBeGreaterThanOrEqual(1);
    expect(screen.getByLabelText("Read-only governance guardrails")).toHaveTextContent(
      "Read-only governance display",
    );
    expect(screen.getByLabelText("UI-007 governed data-source inventory").querySelectorAll(".mono").length).toBeGreaterThan(8);

    unmount();
    authState.value = loggedOutAuth();
    render(
      <MemoryRouter initialEntries={["/governance"]}>
        <Routes>
          <Route path="/login" element={<div>Operator login required</div>} />
          <Route
            path="/governance"
            element={
              <ProtectedRoute>
                <GovernanceEvidenceWorkspace />
              </ProtectedRoute>
            }
          />
        </Routes>
      </MemoryRouter>,
    );

    expect(screen.getByText("Operator login required")).toBeInTheDocument();
    expect(screen.queryByLabelText("Governance workspace frame")).not.toBeInTheDocument();
    expect(within(document.body).queryByText("Governance Workspace Frame")).not.toBeInTheDocument();
  });
});
