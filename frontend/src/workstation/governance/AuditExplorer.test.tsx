import { fireEvent, render, screen, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { GovernanceEvidenceWorkspace } from "../../components/terminal/governance/GovernanceOverlay";
import { reasonCodeFor } from "../../components/terminal/governance/governanceRecords";
import type { AuditEvent } from "../../api/client";
import { InstitutionalWorkspaceShell } from "../components/InstitutionalWorkspaceShell";

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

const refusedEvent: AuditEvent = {
  id: "audit-refused-1",
  category: "assistant",
  action: "assistant_refusal_recorded",
  actor: "operator",
  message: "Assistant request refused by policy",
  resource_type: "assistant_research_response",
  resource_id: "response-1",
  details: {
    reason_code: "ORDER_INSTRUCTION_REFUSED",
    policy_version: "w5-u01.non_actuating.v1",
  },
  created_at: "2026-07-27T06:00:00Z",
};

const pluginEvent: AuditEvent = {
  id: "audit-plugin-1",
  category: "plugin_contract",
  action: "plugin_contract_refused",
  actor: "operator",
  message: "Plugin contract request refused",
  resource_type: "plugin_contract",
  resource_id: "plugin-1",
  details: {
    reason_code: "PLUGIN_CONTRACT_NETWORK_REFUSED",
    method_version: "w7-u05.plugin_contract.v1",
  },
  created_at: "2026-07-27T05:00:00Z",
};

const informationalEvent: AuditEvent = {
  id: "audit-info-1",
  category: "system",
  action: "system_status_observed",
  actor: "system",
  message: "Read-only status observed",
  resource_type: null,
  resource_id: null,
  details: { status: "observed" },
  created_at: "2026-07-27T04:00:00Z",
};

function workspace(events: AuditEvent[] = [refusedEvent, pluginEvent, informationalEvent]) {
  return <GovernanceEvidenceWorkspace auditEvents={events} />;
}

function renderGovernanceShell() {
  return render(
    <MemoryRouter initialEntries={["/governance"]}>
      <Routes>
        <Route element={<InstitutionalWorkspaceShell />}>
          <Route path="/governance" element={workspace()} />
        </Route>
      </Routes>
    </MemoryRouter>,
  );
}

async function readP03ProductionSource(): Promise<string> {
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

describe("UI-007-P03 audit explorer", () => {
  it("test_ui007_audit_explorer_renders_existing_audit_events_read_only", () => {
    render(workspace());

    const list = screen.getByLabelText("Read-only audit event list");
    expect(list).toHaveTextContent("audit-refused-1");
    expect(list).toHaveTextContent("assistant_refusal_recorded");
    expect(list).toHaveTextContent("ORDER_INSTRUCTION_REFUSED");

    const detail = screen.getByLabelText("Read-only audit event detail");
    expect(detail).toHaveTextContent("audit-refused-1");
    expect(detail).toHaveTextContent("assistant_research_response");
    expect(detail).toHaveTextContent("response-1");
    expect(detail).toHaveTextContent("Assistant request refused by policy");
    expect(detail).toHaveTextContent("w5-u01.non_actuating.v1");
  });

  it("test_ui007_audit_reason_codes_and_refusals_render_verbatim_no_inference", () => {
    render(workspace());

    expect(reasonCodeFor(refusedEvent)).toBe("ORDER_INSTRUCTION_REFUSED");
    expect(reasonCodeFor(pluginEvent)).toBe("PLUGIN_CONTRACT_NETWORK_REFUSED");
    expect(reasonCodeFor(informationalEvent)).toBe("—");

    fireEvent.click(screen.getByText("plugin_contract_refused"));
    const detail = screen.getByLabelText("Read-only audit event detail");
    expect(detail).toHaveTextContent("PLUGIN_CONTRACT_NETWORK_REFUSED");
    expect(detail).toHaveTextContent("SCREAMING_SNAKE refusal reason-codes remain stored refusal text");
    expect(detail).toHaveTextContent("does not reinterpret them as an authorization path");
    expect(detail).not.toHaveTextContent("authorized");
    expect(detail).not.toHaveTextContent("success");
  });

  it("test_ui007_audit_explorer_filter_sort_are_in_memory_no_persistence_or_mutation", () => {
    render(workspace());

    const filterPanel = screen.getByLabelText("In-memory audit filters");
    fireEvent.change(within(filterPanel).getByRole("textbox"), { target: { value: "plugin" } });
    expect(screen.getByLabelText("Read-only audit event list")).toHaveTextContent("audit-plugin-1");
    expect(screen.getByLabelText("Read-only audit event list")).not.toHaveTextContent("audit-refused-1");
    expect(filterPanel).toHaveTextContent("showing 1 of 3 audit rows");
    expect(filterPanel).toHaveTextContent("In-memory only");

    fireEvent.change(within(filterPanel).getByRole("combobox"), { target: { value: "oldest" } });
    expect(screen.getByLabelText("Read-only audit event list")).toHaveTextContent("audit-plugin-1");
    expect(document.body.textContent).not.toContain("operator_workspace_preferences");
  });

  it("test_ui007_audit_explorer_contains_no_governance_mutation_gate_or_certification_control", async () => {
    render(workspace());

    const buttonText = screen
      .getAllByRole("button")
      .map((button) => button.textContent?.toLowerCase() ?? "")
      .join(" ");
    for (const marker of [
      "create audit",
      "edit audit",
      "delete audit",
      "redact",
      "replay",
      "mark reviewed",
      "acknowledge",
      "open gate",
      "approve production",
    ]) {
      expect(buttonText).not.toContain(marker);
    }

    const sourceText = await readP03ProductionSource();
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

  it("test_ui007_audit_explorer_accessibility_and_doc16_brand_hold", () => {
    renderGovernanceShell();

    expect(screen.getAllByTestId("institutional-workspace-shell")).toHaveLength(1);
    expect(screen.getByText(/AXIOM Institutional Workstation/i)).toBeInTheDocument();
    expect(screen.getAllByText("Gate CLOSED").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByLabelText("Read-only audit explorer")).toBeInTheDocument();
    expect(screen.getByLabelText("Read-only audit event list")).toBeInTheDocument();
    expect(screen.getByLabelText("Read-only audit event detail")).toBeInTheDocument();
    expect(screen.getByLabelText("Refusal reason-code viewer")).toBeInTheDocument();
    expect(document.body.querySelectorAll(".mono").length).toBeGreaterThan(10);
  });
});
