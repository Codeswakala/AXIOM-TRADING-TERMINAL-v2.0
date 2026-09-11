import { render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { OverlayProvider, useOverlayController } from "../../../workstation/overlays/OverlayProvider";
import { GovernanceOverlay } from "./GovernanceOverlay";
import type { AuditEvent, PlatformOperationsEvidence } from "../../../api/client";
import * as client from "../../../api/client";

vi.mock("../../../api/client", async () => {
  const actual = await vi.importActual<typeof client>("../../../api/client");
  return {
    ...actual,
    fetchAuditEvents: vi.fn(),
    fetchInstitutionalIntelligenceBundle: vi.fn(),
    fetchPlatformOperationsEvidence: vi.fn(),
    // SURF-P03: the overlay now fetches five platform-record sources.
    fetchRouteInventory: vi.fn(),
    fetchRbacPermissions: vi.fn(),
    fetchApiCatalogue: vi.fn(),
    fetchPluginContracts: vi.fn(),
    fetchOperatorScopeRecords: vi.fn(),
    fetchOperatorScopeRecord: vi.fn(),
  };
});

/** Harness: opens the overlay inside a real OverlayProvider. */
function GovernanceHarness() {
  return (
    <OverlayProvider>
      <HarnessInner />
    </OverlayProvider>
  );
}

function HarnessInner() {
  const overlay = useOverlayController();
  return (
    <div>
      <button type="button" onClick={overlay.openGovernance} data-testid="harness-open-btn">
        open
      </button>
      <GovernanceOverlay />
    </div>
  );
}

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

beforeEach(() => {
  vi.clearAllMocks();
});

describe("GovernanceOverlay (UI-CONV-P03 item 5)", () => {
  it("test_uiconv_p03_governance_overlay_opens_and_closes_via_controller", async () => {
    vi.mocked(client.fetchAuditEvents).mockResolvedValue([]);
    vi.mocked(client.fetchInstitutionalIntelligenceBundle).mockResolvedValue(null as never);
    vi.mocked(client.fetchPlatformOperationsEvidence).mockResolvedValue(platformOperations);

    render(<GovernanceHarness />);
    expect(screen.queryByTestId("governance-overlay")).not.toBeInTheDocument();

    screen.getByTestId("harness-open-btn").click();
    await waitFor(() => expect(screen.getByTestId("governance-overlay")).toBeInTheDocument());

    screen.getByTestId("governance-overlay-close-btn").click();
    await waitFor(() => expect(screen.queryByTestId("governance-overlay")).not.toBeInTheDocument());
  });

  it("test_uiconv_p03_governance_four_constitutional_declarations_visible_without_interaction", async () => {
    vi.mocked(client.fetchAuditEvents).mockResolvedValue([]);
    vi.mocked(client.fetchInstitutionalIntelligenceBundle).mockResolvedValue(null as never);
    vi.mocked(client.fetchPlatformOperationsEvidence).mockResolvedValue(platformOperations);

    render(<GovernanceHarness />);
    screen.getByTestId("harness-open-btn").click();
    await waitFor(() => expect(screen.getByTestId("governance-overlay")).toBeInTheDocument());

    // M3: all four constitutional declarations render as plain visible sections —
    // no accordion, tooltip, or secondary tab.
    expect(screen.getByTestId("governance-certification-status")).toBeInTheDocument();
    expect(screen.getByTestId("governance-standing-residuals")).toBeInTheDocument();
    expect(screen.getByTestId("governance-readonly-boundary")).toBeInTheDocument();
    expect(screen.getByTestId("governance-inert-display-rules")).toBeInTheDocument();
    // Production certification boundary (within the platform posture section).
    expect(screen.getByLabelText("Production certification remains separate")).toBeInTheDocument();
  });

  it("test_uiconv_p03_governance_audit_failure_degrades_independently_and_never_blanks_declarations", async () => {
    // M5: audit fetch fails; validation and platform sections still load; the
    // certification boundary remains visible.
    vi.mocked(client.fetchAuditEvents).mockRejectedValue(new Error("Audit read seam unavailable"));
    vi.mocked(client.fetchInstitutionalIntelligenceBundle).mockResolvedValue(null as never);
    vi.mocked(client.fetchPlatformOperationsEvidence).mockResolvedValue(platformOperations);

    render(<GovernanceHarness />);
    screen.getByTestId("harness-open-btn").click();
    await waitFor(() => expect(screen.getByTestId("governance-overlay")).toBeInTheDocument());

    // Audit section shows its own error; constitutional declarations unaffected.
    await waitFor(() => {
      expect(screen.getByText("Audit read seam unavailable")).toBeInTheDocument();
    });
    expect(screen.getByTestId("governance-certification-status")).toBeInTheDocument();
    expect(screen.getByTestId("governance-standing-residuals")).toBeInTheDocument();
    expect(screen.getByTestId("governance-platform-posture")).toBeInTheDocument();
  });

  it("test_uiconv_p03_governance_validation_failure_is_independent_of_audit", async () => {
    const auditEvents: AuditEvent[] = [
      {
        id: "audit-1",
        created_at: "2026-08-15T10:00:00Z",
        category: "SECURITY",
        action: "auth.login_success",
        actor: "admin",
        message: "Login success",
        resource_type: "operator",
        resource_id: "op-1",
        details: { reason_code: "EXTERNAL_LLM_REFUSED" },
      },
    ];
    vi.mocked(client.fetchAuditEvents).mockResolvedValue(auditEvents);
    vi.mocked(client.fetchInstitutionalIntelligenceBundle).mockRejectedValue(
      new Error("Validation read seam unavailable"),
    );
    vi.mocked(client.fetchPlatformOperationsEvidence).mockResolvedValue(platformOperations);

    render(<GovernanceHarness />);
    screen.getByTestId("harness-open-btn").click();
    await waitFor(() => expect(screen.getByTestId("governance-overlay")).toBeInTheDocument());

    // Audit renders its event + refusal reason-code viewer (M2: verbatim code).
    await waitFor(() => {
      expect(screen.getByTestId("governance-refusal-reason-viewer")).toBeInTheDocument();
      expect(screen.getByTestId("governance-refusal-reason-viewer")).toHaveTextContent("EXTERNAL_LLM_REFUSED");
    });
    // Validation section carries its own error.
    await waitFor(() => {
      expect(screen.getByText("Validation read seam unavailable")).toBeInTheDocument();
    });
  });

  it("test_uiconv_p03_governance_major_regions_carry_testids", async () => {
    vi.mocked(client.fetchAuditEvents).mockResolvedValue([]);
    vi.mocked(client.fetchInstitutionalIntelligenceBundle).mockResolvedValue(null as never);
    vi.mocked(client.fetchPlatformOperationsEvidence).mockResolvedValue(platformOperations);

    render(<GovernanceHarness />);
    screen.getByTestId("harness-open-btn").click();
    await waitFor(() => expect(screen.getByTestId("governance-overlay")).toBeInTheDocument());

    for (const testid of [
      "governance-frame",
      "governance-audit-explorer",
      "governance-evidence-viewer",
      "governance-validation-panels",
      "governance-platform-posture",
      "governance-sources-inventory",
      "governance-overlay-body",
    ]) {
      expect(screen.getByTestId(testid)).toBeInTheDocument();
    }
  });
});
