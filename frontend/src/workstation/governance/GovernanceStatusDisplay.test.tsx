import { render, screen, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { GovernanceEvidenceWorkspace } from "../../components/terminal/governance/GovernanceOverlay";
import { UI007_CERTIFICATION_STATUS, UI007_GOVERNANCE_STATUS, UI007_STANDING_RESIDUALS } from "../../components/terminal/governance/governanceRecords";
import { InstitutionalWorkspaceShell } from "../components/InstitutionalWorkspaceShell";
import { workspaceForPath } from "../registry/workspaceRegistry";

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

async function readP02ProductionSource(): Promise<string> {
  const modules = import.meta.glob(
    [
      "../../components/terminal/governance/GovernanceOverlay.tsx",
      "../../components/terminal/governance/governanceRecords.ts",
      "../registry/workspaceRegistry.tsx",
      "../commands/quickActionCatalogue.ts",
      "../commands/commandTypes.ts",
      "../workflows/workflowNavigationMetadata.ts",
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

describe("UI-007-P02 governance status display", () => {
  it("test_ui007_governance_status_renders_existing_posture_read_only", () => {
    render(<GovernanceEvidenceWorkspace />);

    const panel = screen.getByLabelText("Governance status read-only panel");
    expect(panel).toHaveTextContent("Gate CLOSED");
    expect(panel).toHaveTextContent("/governance");
    expect(panel).toHaveTextContent("G-1…G-7 read-only");
    expect(panel).toHaveTextContent("display-only text");
    expect(UI007_GOVERNANCE_STATUS).toHaveLength(3);
    expect(within(panel).queryAllByRole("button")).toHaveLength(0);
    expect(within(panel).queryAllByRole("checkbox")).toHaveLength(0);
    expect(within(panel).queryAllByRole("textbox")).toHaveLength(0);
  });

  it("test_ui007_gate_closed_is_inert_no_toggle_or_control", async () => {
    render(<GovernanceEvidenceWorkspace />);

    const panel = screen.getByLabelText("Governance status read-only panel");
    expect(panel).toHaveTextContent("Gate CLOSED");
    expect(panel).toHaveTextContent("There is no UI affordance that changes this state.");
    expect(within(panel).queryAllByRole("button")).toHaveLength(0);
    expect(within(panel).queryAllByRole("switch")).toHaveLength(0);
    expect(within(panel).queryAllByRole("form")).toHaveLength(0);

    const sourceText = await readP02ProductionSource();
    for (const marker of ["open_gate", "allow_execution", "gate toggle", "toggle gate"]) {
      expect(sourceText).not.toContain(marker);
    }
  });

  it("test_ui007_certification_status_is_display_not_actuation", async () => {
    render(<GovernanceEvidenceWorkspace />);

    const panel = screen.getByLabelText("Certification status read-only panel");
    expect(panel).toHaveTextContent("Production NOT CERTIFIED");
    expect(panel).toHaveTextContent("HELD");
    expect(panel).toHaveTextContent("CERTIFIED · CERTIFIED WITH CONDITIONS · DEFERRED · NOT CERTIFIED");
    expect(panel).toHaveTextContent("TD-UI-POSTCSS-HIGH CLOSED / REMEDIATED");
    expect(UI007_CERTIFICATION_STATUS).toHaveLength(4);
    expect(within(panel).queryAllByRole("button")).toHaveLength(0);
    expect(within(panel).queryAllByRole("checkbox")).toHaveLength(0);

    const sourceText = await readP02ProductionSource();
    for (const marker of ["certify", "mark_ready", "approve_production", "waive", "risk_accept"]) {
      expect(sourceText).not.toContain(marker);
    }
  });

  it("test_ui007_governance_status_contains_no_governance_mutation_gate_or_certification_control", async () => {
    render(<GovernanceEvidenceWorkspace />);

    const pageText = document.body.textContent?.toLowerCase() ?? "";
    for (const marker of [
      "create governance",
      "update governance",
      "delete governance",
      "gate switch",
      "production approval action",
      "residual action",
      "audit editor",
      "verdict mutation",
    ]) {
      expect(pageText).not.toContain(marker);
    }

    const residualPanel = screen.getByLabelText("Residual status read-only panel");
    expect(residualPanel).toHaveTextContent("TD-UI-REACTROUTER-MODERATE");
    expect(residualPanel).toHaveTextContent("TD-W7-U07-RATE-GUARD");
    expect(residualPanel).toHaveTextContent("TD-W6-CI-AUDIT");
    expect(residualPanel).toHaveTextContent("UI-002-P04b");
    expect(residualPanel).toHaveTextContent("TD-UI005-COMPLETION-TIMEOUT");
    expect(residualPanel).toHaveTextContent("TD-AXIOM-GIT-PROVENANCE");
    expect(UI007_STANDING_RESIDUALS).toHaveLength(6);

    const sourceText = await readP02ProductionSource();
    for (const marker of [
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

  it("test_ui007_governance_status_accessibility_and_doc16_brand_hold", () => {
    renderGovernanceShell();

    const workspace = workspaceForPath("/governance");
    expect(workspace.noActuation).toBe(true);
    expect(workspace.requiresAuth).toBe(true);
    expect(screen.getAllByTestId("institutional-workspace-shell")).toHaveLength(1);
    expect(screen.getByLabelText("Primary workspace")).toHaveAttribute(
      "data-active-telemetry-id",
      "workspace.govern.governance_evidence",
    );
    expect(screen.getByText(/AXIOM Institutional Workstation/i)).toBeInTheDocument();
    expect(screen.getAllByText("Gate CLOSED").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("Production NOT CERTIFIED").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByLabelText("Certification status read-only panel")).toBeInTheDocument();
    expect(screen.getByLabelText("Residual status read-only panel")).toBeInTheDocument();
    expect(screen.getByLabelText("UI-007 governed data-source inventory").querySelectorAll(".mono").length).toBeGreaterThan(8);
  });
});
