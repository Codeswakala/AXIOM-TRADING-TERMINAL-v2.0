/**
 * SURF-P03 — platform records surfacing suite (Build Order S1, S2, S3, M2,
 * M3, M4, R1, R2). Named tests prove: the four record collections render
 * their record payloads (routes, roles, catalogue routes + abuse guard +
 * persistence, contracts + allowlist) with genuine counts; scope records
 * render list and detail; a 403 renders the explicit access-denied notice
 * distinct from both the empty result and a transport error; per-source
 * status rows report genuine loaded counts; and no governance-mutation
 * affordance exists anywhere in the rendered surface.
 */
import { fireEvent, render, screen, within } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { PlatformRecordsSection } from "./PlatformRecordsSection";
import type {
  ApiCatalogueResponse,
  OperatorScopeListResult,
  OperatorScopeRecordResult,
  PluginContractsResponse,
  RbacPermissionsResponse,
  RouteInventoryResponse,
} from "../../../api/client";

const routeInventory: RouteInventoryResponse = {
  service: "institutional_platform",
  version: "w7-u01.security_foundation.v1",
  routes: [
    {
      path: "/api/v1/institutional-platform/route-inventory",
      methods: ["GET"],
      permission: "institutional.route_inventory.read",
      description: "Read institutional platform route inventory.",
    },
    {
      path: "/api/v1/institutional-platform/operator-scope-records",
      methods: ["GET"],
      permission: "institutional.operator_scope.read",
      description: "List current operator scope records.",
    },
  ],
  actuation_surface_present: false,
  governance_gate_capability_present: false,
};

const rbac: RbacPermissionsResponse = {
  policy: "default_deny",
  roles: {
    admin: ["institutional.route_inventory.read", "institutional.rbac.read"],
    operator: ["institutional.operator_scope.read"],
  },
  forbidden_capabilities_present: false,
};

const apiCatalogue: ApiCatalogueResponse = {
  service: "institutional_platform",
  catalogue_version: "v1",
  api_version: "v1",
  routes: [
    { path: "/api/v1/alerts", methods: ["GET"], description: "List alerts." },
  ],
  route_count: 1,
  actuation_surface_present: false,
  governance_gate_capability_present: false,
  abuse_guard: { status: "engaged", reason: "default_deny_abuse_guard" },
  persistence: { catalogue_table_persisted: true, alembic_head_expected: "20260717_0037" },
};

const pluginContracts: PluginContractsResponse = {
  service: "institutional_platform_plugin_contracts",
  contract_version: "w7-u05.plugin_contracts.v1",
  contracts: [
    { name: "refusal_contract", version: "v1", capabilities: ["refuse_dynamic_plugin"] },
  ],
  capability_allowlist: ["refuse_dynamic_plugin"],
  dynamic_code_execution_enabled: false,
  third_party_plugin_execution_enabled: false,
  plugin_execution_audit_table_present: false,
  governance_gate_capability_present: false,
};

const scopeOk: OperatorScopeListResult = {
  kind: "ok",
  records: [
    {
      operator_id: "op-1",
      username: "lead_operator",
      role: "admin",
      record_type: "institutional_operator_scope",
      research_status: "research_only",
    },
  ],
};

const scopeDenied: OperatorScopeListResult = {
  kind: "denied",
  detail: "Institutional scope access denied",
};

const scopeError: OperatorScopeListResult = {
  kind: "error",
  detail: "Failed to fetch",
};

const scopeDetailOk: OperatorScopeRecordResult = {
  kind: "ok",
  record: {
    operator_id: "op-1",
    username: "lead_operator",
    role: "admin",
    record_type: "institutional_operator_scope",
    research_status: "research_only",
  },
};

function renderSection(overrides: Partial<Parameters<typeof PlatformRecordsSection>[0]> = {}) {
  const props: Parameters<typeof PlatformRecordsSection>[0] = {
    routeInventory,
    routeInventoryLoading: false,
    routeInventoryError: null,
    rbac,
    rbacLoading: false,
    rbacError: null,
    apiCatalogue,
    apiCatalogueLoading: false,
    apiCatalogueError: null,
    pluginContracts,
    pluginContractsLoading: false,
    pluginContractsError: null,
    scopeResult: scopeOk,
    scopeLoading: false,
    scopeRecordResult: null,
    scopeDetailLoading: false,
    onRefreshScope: vi.fn(),
    onSelectScopeDetail: vi.fn(),
    ...overrides,
  };
  return render(<PlatformRecordsSection {...props} />);
}

describe("SURF-P03 — platform records surfacing", () => {
  it("test_surf_p03_s1_four_record_collections_render_record_payloads", () => {
    renderSection();

    // Route inventory entries.
    const routes = screen.getByTestId("platform-route-inventory");
    expect(within(routes).getByText(/GET \/api\/v1\/institutional-platform\/route-inventory/)).toBeInTheDocument();
    expect(within(routes).getByText("institutional.route_inventory.read")).toBeInTheDocument();
    // RBAC per-role lists.
    const roles = screen.getByTestId("platform-rbac-records");
    expect(within(roles).getByText("admin")).toBeInTheDocument();
    expect(within(roles).getByText(/institutional.route_inventory.read, institutional.rbac.read/)).toBeInTheDocument();
    expect(within(roles).getByText("default_deny")).toBeInTheDocument();
    // API catalogue routes + abuse guard + persistence.
    const catalogue = screen.getByTestId("platform-api-catalogue");
    expect(within(catalogue).getByText(/GET \/api\/v1\/alerts/)).toBeInTheDocument();
    expect(within(catalogue).getByText(/engaged · default_deny_abuse_guard/)).toBeInTheDocument();
    expect(within(catalogue).getByText(/20260717_0037/)).toBeInTheDocument();
    // Plugin contracts + capability allowlist.
    const plugins = screen.getByTestId("platform-plugin-contracts");
    expect(within(plugins).getByText("refusal_contract")).toBeInTheDocument();
    expect(within(plugins).getByText("refuse_dynamic_plugin")).toBeInTheDocument();
  });

  it("test_surf_p03_s2_scope_records_list_and_detail_render", () => {
    const onSelectScopeDetail = vi.fn();
    renderSection({ scopeRecordResult: scopeDetailOk, onSelectScopeDetail });

    expect(screen.getByTestId("platform-scope-list")).toBeInTheDocument();
    expect(screen.getByText("lead_operator · admin")).toBeInTheDocument();
    expect(screen.getByText(/institutional_operator_scope · research_only/)).toBeInTheDocument();

    fireEvent.click(screen.getByTestId("platform-scope-detail-open-op-1"));
    expect(onSelectScopeDetail).toHaveBeenCalledWith("op-1");

    expect(screen.getByTestId("platform-scope-detail-record")).toHaveTextContent("op-1");
    expect(screen.getByTestId("platform-scope-detail-record")).toHaveTextContent("lead_operator");
  });

  it("test_surf_p03_m3_scope_403_renders_access_denied_notice_distinct_from_empty", () => {
    renderSection({ scopeResult: scopeDenied });

    const denied = screen.getByTestId("platform-scope-access-denied");
    expect(denied).toHaveTextContent("Access denied.");
    expect(denied).toHaveTextContent("access restriction, not an empty result");
    expect(denied).toHaveTextContent("Institutional scope access denied");
    // Distinct testids prove the three states are separate renderings.
    expect(screen.queryByTestId("platform-scope-empty")).not.toBeInTheDocument();
    expect(screen.queryByTestId("platform-scope-error")).not.toBeInTheDocument();
    expect(screen.queryByTestId("platform-scope-list")).not.toBeInTheDocument();
  });

  it("test_surf_p03_m3_scope_empty_result_is_distinct_from_denied", () => {
    renderSection({
      scopeResult: { kind: "ok", records: [] },
    });

    expect(screen.getByTestId("platform-scope-empty")).toHaveTextContent(
      "No scope records returned for this operator.",
    );
    expect(screen.queryByTestId("platform-scope-access-denied")).not.toBeInTheDocument();
  });

  it("test_surf_p03_m3_scope_transport_error_is_distinct_from_denied", () => {
    renderSection({ scopeResult: scopeError });

    expect(screen.getByTestId("platform-scope-error")).toHaveTextContent("Failed to fetch");
    expect(screen.queryByTestId("platform-scope-access-denied")).not.toBeInTheDocument();
  });

  it("test_surf_p03_r2_per_source_status_reports_genuine_counts_and_denial", () => {
    renderSection({ scopeResult: scopeDenied });

    expect(screen.getAllByTestId("platform-source-status-ready").length).toBe(4);
    expect(screen.getAllByTestId("platform-source-status-denied").length).toBe(1);
    // Genuine counts: 2 route entries, 2 roles, 1 catalogue route, 1 contract.
    expect(screen.getAllByText("2 records loaded").length).toBe(2);
    expect(screen.getAllByText("1 records loaded").length).toBe(2);
  });

  it("test_surf_p03_r2_single_source_failure_does_not_blank_the_section", () => {
    renderSection({
      apiCatalogue: null,
      apiCatalogueLoading: false,
      apiCatalogueError: "Institutional permission denied by default-deny policy",
    });

    const catalogue = screen.getByTestId("platform-api-catalogue");
    expect(within(catalogue).getByTestId("platform-api-catalogue-error")).toHaveTextContent(
      "Institutional permission denied by default-deny policy",
    );
    // The other three collections still render their records.
    expect(screen.getByTestId("platform-route-inventory")).toBeInTheDocument();
    expect(within(screen.getByTestId("platform-route-inventory")).getByText(/GET \/api\/v1\/institutional-platform\/route-inventory/)).toBeInTheDocument();
    expect(within(screen.getByTestId("platform-plugin-contracts")).getByText("refusal_contract")).toBeInTheDocument();
  });

  it("test_surf_p03_m2_no_governance_mutation_affordance", () => {
    renderSection();

    const buttonText = screen
      .getAllByRole("button")
      .map((button) => button.textContent?.toLowerCase() ?? "")
      .join(" ");
    for (const banned of [
      "edit",
      "grant",
      "revoke",
      "elevate",
      "register route",
      "enable plugin",
      "change scope",
      "create",
      "update",
      "delete",
      "submit",
    ]) {
      expect(buttonText).not.toContain(banned);
    }
    // The only controls are the scope refresh and the scope detail view.
    expect(screen.getAllByRole("button").map((b) => b.textContent?.trim())).toEqual([
      "Refresh scope",
      "View detail",
    ]);
  });

  it("test_surf_p03_m4_summary_agreement_disclaimer_present", () => {
    renderSection();

    expect(screen.getByLabelText("Platform records read-only notice")).toHaveTextContent(
      "Values that also appear in the posture summary above",
    );
    expect(screen.getByLabelText("Platform records inspection posture")).toHaveTextContent(
      "Inspection view",
    );
  });

  it("test_surf_p03_r1_absence_renders_as_absence_in_collections", () => {
    renderSection({
      routeInventory: { ...routeInventory, routes: [] },
      pluginContracts: { ...pluginContracts, contracts: [] },
    });

    expect(screen.getByTestId("platform-route-inventory-empty")).toHaveTextContent(
      "No route inventory records returned.",
    );
    expect(screen.getByTestId("platform-plugin-contracts-empty")).toHaveTextContent(
      "No plugin contract records returned.",
    );
  });
});
