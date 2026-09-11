import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { GovernanceEvidenceWorkspace } from "../../components/terminal/governance/GovernanceOverlay";
import { UI007_READINESS_POSTURE_RECORDS, UI007_STANDING_RESIDUALS } from "../../components/terminal/governance/governanceRecords";
import type { PlatformOperationsEvidence } from "../../api/client";

const platformOperations: PlatformOperationsEvidence = {
  health: {
    status: "ok",
    service: "AXIOM",
    version: "0.62.0",
    environment: "development",
    timestamp: "2026-07-28T12:00:00Z",
    message: "AXIOM backend is alive",
    latency_ms: 0.2,
  },
  readiness: {
    status: "ready",
    service: "AXIOM",
    version: "0.62.0",
    environment: "development",
    timestamp: "2026-07-28T12:00:01Z",
    checks: [
      { name: "configuration", status: "up", detail: "environment=development", latency_ms: 0 },
      { name: "database", status: "up", detail: "backend=postgresql; latency_ms=1.4", latency_ms: 1.4 },
    ],
  },
  metrics: {
    service: "AXIOM",
    version: "0.62.0",
    environment: "development",
    observability: {
      process: { pid: 42, uptime_seconds: 123.456 },
      http: { requests_total: 17, errors_total: 0, latency_avg_ms: 1.2, latency_max_ms: 3.4 },
      governance: { gate_refusals_total: 2 },
    },
    database: { status: "up", latency_ms: 1.4, backend: "postgresql", pool: { size: 5 } },
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
    pool: { size: 5 },
    candle_count: 12,
    audit_count: 33,
  },
  systemInfo: {
    name: "AXIOM",
    version: "0.62.0",
    environment: "development",
    wave: "7 — Institutional Platform",
    unit: "W7-U08",
    architecture_version: "2.0.0",
    description: "Existing system description",
    timestamp: "2026-07-28T12:00:02Z",
  },
  routeInventory: {
    service: "institutional_platform",
    version: "w7-u01.security_foundation.v1",
    routes: [{ path: "/api/v1/institutional-platform/route-inventory", methods: ["GET"] }],
    actuation_surface_present: false,
    governance_gate_capability_present: false,
  },
  rbac: {
    policy: "default_deny",
    roles: { admin: ["institutional.route_inventory.read"] },
    forbidden_capabilities_present: false,
  },
  apiCatalogue: {
    service: "institutional_platform_api_catalogue",
    catalogue_version: "w7-u04.research_api_catalogue.v1",
    api_version: "v1",
    routes: [{ path: "/api/v1/institutional-platform/api-catalogue", methods: ["GET"] }],
    route_count: 4,
    actuation_surface_present: false,
    governance_gate_capability_present: false,
    abuse_guard: { status: "deferred", reason: "No rate limiter added in W7-U04." },
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
  return <GovernanceEvidenceWorkspace platformOperations={platformOperations} />;
}

async function readP05ProductionSource(): Promise<string> {
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

describe("UI-007-P05 platform health, readiness, version and API posture", () => {
  it("test_ui007_platform_health_version_and_readiness_render_existing_read_api_values", () => {
    render(workspace());

    const panel = screen.getByLabelText("Platform health readiness version and API posture");
    expect(panel).toHaveTextContent("GET /health · as returned");
    expect(panel).toHaveTextContent("GET /ready · as returned");
    expect(panel).toHaveTextContent("GET /api/v1/metrics · safe direct fields");
    expect(panel).toHaveTextContent("GET /api/v1/persistence/stats · as returned");
    expect(panel).toHaveTextContent("GET /api/v1/system/info · as returned");
    expect(panel).toHaveTextContent("0.62.0");
    expect(panel).toHaveTextContent("20260717_0037");
    expect(panel).toHaveTextContent("123.456");
    expect(panel).toHaveTextContent("12");
    expect(panel).toHaveTextContent("33");
    expect(panel).toHaveTextContent("default_deny");
  });

  it("test_ui007_runtime_readiness_is_not_displayed_as_production_certification", () => {
    render(workspace());

    const separation = screen.getByLabelText("Runtime readiness is not production certification");
    expect(separation).toHaveTextContent("Runtime readiness is not production certification.");
    expect(separation).toHaveTextContent("Production remains NOT CERTIFIED");

    const certification = screen.getByLabelText("Production certification remains separate");
    expect(certification).toHaveTextContent("Production NOT CERTIFIED");
    expect(certification).toHaveTextContent("HELD");
    expect(certification).toHaveTextContent("not a certification outcome");
    expect(certification).not.toHaveTextContent(/all systems go/i);
    expect(certification).not.toHaveTextContent(/fully operational/i);
  });

  it("test_ui007_api_route_plugin_posture_discloses_no_gate_dynamic_plugin_or_actuation_capability", () => {
    render(workspace());

    const panel = screen.getByLabelText("Platform health readiness version and API posture");
    expect(panel).toHaveTextContent(/Route actuation surface present\s*false/);
    expect(panel).toHaveTextContent(/Route Gate capability present\s*false/);
    expect(panel).toHaveTextContent(/Dynamic plugin code enabled\s*false/);
    expect(panel).toHaveTextContent(/Third-party plugin enabled\s*false/);
    expect(panel).toHaveTextContent("TD-W7-U07-RATE-GUARD");
    expect(panel).toHaveTextContent("formally_deferred");
    expect(panel).toHaveTextContent("ADMIN_DEFAULT_CREDENTIAL_REJECTED_WITH_INSECURE_DEV_OFF");
    expect(panel).toHaveTextContent("TD-AXIOM-GIT-PROVENANCE");
    expect(panel).toHaveTextContent("PRE-CERTIFICATION BLOCKER");
    expect(UI007_READINESS_POSTURE_RECORDS).toHaveLength(2);
    expect(UI007_STANDING_RESIDUALS.some((item) => item.label === "TD-AXIOM-GIT-PROVENANCE")).toBe(true);
  });

  it("test_ui007_platform_health_contains_no_governance_mutation_gate_or_certification_control", async () => {
    render(workspace());

    const panel = screen.getByLabelText("Platform health readiness version and API posture");
    expect(within(panel).queryAllByRole("button")).toHaveLength(0);
    expect(within(panel).queryAllByRole("textbox")).toHaveLength(0);
    expect(within(panel).queryAllByRole("checkbox")).toHaveLength(0);

    const sourceText = await readP05ProductionSource();
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

  it("test_ui007_platform_health_accessibility_and_doc16_brand_hold", () => {
    render(workspace());

    const panel = screen.getByLabelText("Platform health readiness version and API posture");
    expect(screen.getByRole("heading", { name: "Platform Health, Readiness & API Posture" })).toBeInTheDocument();
    expect(screen.getByLabelText("Runtime certification separation")).toHaveTextContent("Production NOT CERTIFIED");
    expect(screen.getByLabelText("Readiness posture records and residual honesty")).toHaveTextContent(
      "TD-AXIOM-GIT-PROVENANCE",
    );
    expect(panel.querySelectorAll(".mono").length).toBeGreaterThan(14);
    expect(panel).toHaveTextContent(/Secret marker count\s*0/);
    expect(panel).not.toHaveTextContent("postgresql://");
    expect(panel).not.toHaveTextContent("Bearer ");
    expect(panel).not.toHaveTextContent("admin123");
  });
});
