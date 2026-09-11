import { render, screen, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { GovernanceEvidenceWorkspace } from "../../components/terminal/governance/GovernanceOverlay";
import type { AuditEvent, InstitutionalIntelligenceBundle, PlatformOperationsEvidence } from "../../api/client";
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

const auditEvents: AuditEvent[] = [
  {
    id: "audit-ui007-completion-refused",
    category: "SECURITY",
    action: "plugin_contract_request.refused",
    actor: "w7-u05-evidence-operator",
    message: "Plugin contract request refused reason=PLUGIN_CONTRACT_IMPORT_REFUSED",
    resource_type: "plugin_contract_request",
    resource_id: "plugin-contract-001",
    details: { reason_code: "PLUGIN_CONTRACT_IMPORT_REFUSED" },
    created_at: "2026-07-28T12:00:00Z",
  },
];

const validationBundle: InstitutionalIntelligenceBundle = {
  relation: [],
  context: [],
  hypothetical: [],
  risk: [],
  validation: [
    {
      id: "validation-ui007-completion",
      artifact_type: "signal_validation_report",
      method_version: "validation.v1",
      research_status: "research_only",
      sample_count: 9,
      validation_scope: { market_class: "forex", symbol: "EURUSD", timeframe: "M1" },
      uncertainty: { method: "wilson", lower: 0.1, upper: 0.6, sample_count: 9 },
      limitations: ["research_only", "outcome_data_not_available"],
      source_signal_ids: ["signal-ui007-completion"],
      input_lineage: { snapshot: "snapshot-ui007" },
      audit_correlation_id: "audit-correlation-ui007",
      report_hash: "hash-ui007",
      created_at: "2026-07-28T12:00:01Z",
    },
  ],
};

const platformOperations: PlatformOperationsEvidence = {
  health: {
    status: "ok",
    service: "AXIOM",
    version: "0.62.0",
    environment: "development",
    timestamp: "2026-07-28T12:00:02Z",
    message: "AXIOM backend is alive",
    latency_ms: 0.1,
  },
  readiness: {
    status: "ready",
    service: "AXIOM",
    version: "0.62.0",
    environment: "development",
    timestamp: "2026-07-28T12:00:03Z",
    checks: [{ name: "database", status: "up", detail: "backend=postgresql", latency_ms: 1.1 }],
  },
  metrics: {
    service: "AXIOM",
    version: "0.62.0",
    environment: "development",
    observability: {
      process: { pid: 42, uptime_seconds: 12.5 },
      http: { requests_total: 1, errors_total: 0, latency_avg_ms: 1, latency_max_ms: 1 },
      governance: { gate_refusals_total: 1 },
    },
    database: { status: "up", latency_ms: 1.1, backend: "postgresql", pool: {} },
    live_market: {
      running: false,
      connected: false,
      messages_received: 0,
      persist_count: 0,
      persist_errors: 0,
      lag_ms: null,
      subscribers: 0,
    },
  },
  persistenceStats: {
    backend: "postgresql",
    database_url_scheme: "postgresql+asyncpg",
    pool: {},
    candle_count: 5132,
    audit_count: 632,
  },
  systemInfo: {
    name: "AXIOM",
    version: "0.62.0",
    environment: "development",
    wave: "7 — Institutional Platform",
    unit: "W7-U08",
    architecture_version: "2.0.0",
    description: "Existing platform identity",
    timestamp: "2026-07-28T12:00:04Z",
  },
  routeInventory: {
    service: "institutional_platform",
    version: "w7-u01.security_foundation.v1",
    routes: [],
    actuation_surface_present: false,
    governance_gate_capability_present: false,
  },
  rbac: { policy: "default_deny", roles: { admin: ["institutional.rbac.read"] }, forbidden_capabilities_present: false },
  apiCatalogue: {
    service: "institutional_platform_api_catalogue",
    catalogue_version: "w7-u04.research_api_catalogue.v1",
    api_version: "v1",
    routes: [],
    route_count: 4,
    actuation_surface_present: false,
    governance_gate_capability_present: false,
    abuse_guard: { status: "deferred", reason: "Existing disposition" },
    persistence: { catalogue_table_persisted: false, alembic_head_expected: "20260717_0037" },
  },
  pluginContracts: {
    service: "institutional_platform_plugin_contracts",
    contract_version: "w7-u05.plugin_contract.v1",
    contracts: [],
    capability_allowlist: [],
    dynamic_code_execution_enabled: false,
    third_party_plugin_execution_enabled: false,
    plugin_execution_audit_table_present: false,
    governance_gate_capability_present: false,
  },
};

function workspace() {
  return (
    <GovernanceEvidenceWorkspace
      auditEvents={auditEvents}
      validationBundle={validationBundle}
      platformOperations={platformOperations}
    />
  );
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

async function readP06ProductionSource(): Promise<string> {
  const modules = import.meta.glob(
    [
      "../../components/terminal/governance/GovernanceOverlay.tsx",
      "../../components/terminal/governance/governanceRecords.ts",
      "../registry/workspaceRegistry.tsx",
      "../commands/quickActionCatalogue.ts",
      "../commands/commandTypes.ts",
      "../workflows/workflowNavigationMetadata.ts",
    ],
    { query: "?raw", import: "default" },
  );
  const values = await Promise.all(
    Object.values(modules).map((loader) => (loader as () => Promise<string>)()),
  );
  return values.join("\n").toLowerCase();
}

describe("UI-007-P06 Governance & Evidence completion checkpoint", () => {
  it("test_ui007_completion_governance_audit_evidence_health_and_version_are_discoverable", () => {
    render(workspace());

    for (const heading of [
      "Governance Workspace Frame",
      "Governance Status",
      "Certification Status",
      "Standing Residuals",
      "Audit Explorer",
      "Evidence Viewer",
      "Validation Summary Panels",
      "Platform Health, Readiness & API Posture",
    ]) {
      expect(screen.getByRole("heading", { name: heading })).toBeInTheDocument();
    }
    expect(screen.getByLabelText("Read-only audit explorer")).toHaveTextContent(
      "PLUGIN_CONTRACT_IMPORT_REFUSED",
    );
    expect(screen.getByLabelText("Read-only evidence viewer")).toBeInTheDocument();
    expect(screen.getByLabelText("Read-only validation summary panels")).toHaveTextContent(
      "validation-ui007-completion",
    );
    expect(screen.getByLabelText("Platform health readiness version and API posture")).toHaveTextContent(
      "20260717_0037",
    );
  });

  it("test_ui007_completion_all_governance_surfaces_are_read_only_and_inert", () => {
    render(workspace());

    const pageText = document.body.textContent?.toLowerCase() ?? "";
    for (const marker of [
      "create governance",
      "update governance",
      "delete governance",
      "open gate",
      "approve production",
      "certification action",
      "restart platform",
      "clear cache",
    ]) {
      expect(pageText).not.toContain(marker);
    }

    const operationPanel = screen.getByLabelText("Platform health readiness version and API posture");
    expect(within(operationPanel).queryAllByRole("button")).toHaveLength(0);
    expect(within(operationPanel).queryAllByRole("textbox")).toHaveLength(0);
    expect(within(operationPanel).queryAllByRole("checkbox")).toHaveLength(0);
    expect(screen.getAllByText("Gate CLOSED").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("Production NOT CERTIFIED").length).toBeGreaterThanOrEqual(1);
  });

  it("test_ui007_completion_no_actuation_recompute_external_ai_gate_or_certification_control", async () => {
    const sourceText = await readP06ProductionSource();
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
      "rest" + "art",
      "re" + "deploy",
      "dr" + "ain",
      "fl" + "ush",
      "reset_" + "metrics",
      "clear_" + "cache",
      "rerun_" + "migration",
      "trigger_" + "health",
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

  it("test_ui007_completion_verbatim_no_cherry_picking_and_residual_disclosure_hold", () => {
    render(workspace());

    const audit = screen.getByLabelText("Read-only audit event detail");
    expect(audit).toHaveTextContent("PLUGIN_CONTRACT_IMPORT_REFUSED");
    expect(audit).toHaveTextContent("does not reinterpret them as an authorization path");

    const validation = screen.getByLabelText("Read-only validation summary panels");
    expect(validation).toHaveTextContent("9");
    expect(validation).toHaveTextContent("wilson");
    expect(validation).toHaveTextContent("research_only");
    expect(validation).toHaveTextContent("outcome_data_not_available");

    const operational = screen.getByLabelText("Platform health readiness version and API posture");
    expect(operational).toHaveTextContent("Runtime readiness is not production certification.");
    expect(operational).toHaveTextContent("TD-AXIOM-GIT-PROVENANCE");
    expect(operational).toHaveTextContent("PRE-CERTIFICATION BLOCKER");
    expect(operational).toHaveTextContent("TD-UI005-COMPLETION-TIMEOUT");
    expect(operational).toHaveTextContent("OPEN · LOW · CONTENTION-FRAGILE");
  });

  it("test_ui007_completion_accessibility_doc16_brand_and_ui001_ui002_integration_hold", () => {
    renderGovernanceShell();

    const workspaceDefinition = workspaceForPath("/governance");
    expect(workspaceDefinition.requiresAuth).toBe(true);
    expect(workspaceDefinition.noActuation).toBe(true);
    expect(screen.getAllByTestId("institutional-workspace-shell")).toHaveLength(1);
    expect(screen.getByLabelText("Primary workspace")).toHaveAttribute(
      "data-active-telemetry-id",
      "workspace.govern.governance_evidence",
    );
    expect(screen.getByText(/AXIOM Institutional Workstation/i)).toBeInTheDocument();
    expect(screen.getByLabelText("Runtime certification separation")).toHaveTextContent(
      "Production NOT CERTIFIED",
    );
    expect(screen.getByLabelText("Readiness posture records and residual honesty")).toBeInTheDocument();
    expect(document.body.querySelectorAll(".mono").length).toBeGreaterThan(24);
  });
});
