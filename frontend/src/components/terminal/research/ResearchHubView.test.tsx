/**
 * UI-CONV-P03 item 4 — relocated suite.
 *
 * This file was the legacy `frontend/src/pages/ResearchManagementPage.test.tsx`.
 * It relocated alongside its subject (ResearchHubView) per the approved re-home
 * plan. Re-targets are documented inline: (a) import paths resolve the view
 * module and its new neighbours; (b) the explorer frame route-posture assertion
 * now pins the post-absorption home `/?view=research` (the legacy
 * `/research-management` route remains registered and redirects); (c) two new
 * named tests pin the redirect behaviour and the R4 `data-testid` region hooks.
 */
import { render, screen, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { ProtectedRoute } from "../../../auth/ProtectedRoute";
import { ResearchManagementWorkspace } from "./ResearchHubView";
import { ResearchManagementRedirect } from "../../../workstation/registry/workspaceRegistry";
import type {
  ResearchCollection,
  ResearchCollectionMember,
  ResearchTag,
  ScenarioReport,
} from "../../../api/client";

vi.mock("../../../context/AuthContext", () => ({
  useAuth: () => ({
    operator: null,
    loading: false,
    isAuthenticated: false,
    login: vi.fn(),
    logout: vi.fn(),
    refreshProfile: vi.fn(),
  }),
}));

function collection(overrides: Partial<ResearchCollection> = {}): ResearchCollection {
  return {
    collection_id: "collection-1",
    created_at: "2026-07-18T10:00:00Z",
    updated_at: "2026-07-18T10:00:00Z",
    operator_id: "operator-1",
    name: "Macro Scenario Review",
    description: "Operator scoped collection",
    research_status: "research_only",
    audit_correlation_id: "corr-collection",
    ...overrides,
  };
}

function member(overrides: Partial<ResearchCollectionMember> = {}): ResearchCollectionMember {
  return {
    member_id: "member-1",
    created_at: "2026-07-18T10:00:00Z",
    operator_id: "operator-1",
    collection_id: "collection-1",
    artifact_type: "scenario_report",
    artifact_id: "scenario-1",
    audit_correlation_id: "corr-member",
    ...overrides,
  };
}

function tag(overrides: Partial<ResearchTag> = {}): ResearchTag {
  return {
    tag_id: "tag-1",
    created_at: "2026-07-18T10:00:00Z",
    operator_id: "operator-1",
    artifact_type: "scenario_report",
    artifact_id: "scenario-1",
    tag: "review-priority",
    audit_correlation_id: "corr-tag",
    ...overrides,
  };
}

function scenario(overrides: Partial<ScenarioReport> = {}): ScenarioReport {
  return {
    id: "scenario-1",
    created_at: "2026-07-18T10:00:00Z",
    artifact_type: "scenario_report",
    method_version: "w4-u04.hypothetical_path.v1",
    market_class: "forex",
    symbol: "EURUSD",
    timeframe: "M1",
    as_of_start: "2026-07-18T09:00:00Z",
    as_of_end: "2026-07-18T10:00:00Z",
    sample_count: 4,
    scenario_name: "Hypothetical Downside Shock",
    hypothetical_return: -0.02,
    scenario_result: { hypothetical_return: -0.02 },
    assumptions: { scenario_name: "Hypothetical Downside Shock" },
    inputs: { baseline_returns: [0, 0.01] },
    uncertainty: { method: "fixture", sample_count: 4 },
    economic_usefulness: { verdict: "not_assessed" },
    config: { fixture: true },
    input_lineage: { policy: "as_of_bounded" },
    source_artifact_ids: ["source-1"],
    market_scope: { market_class: "forex" },
    results: { scenario_result: { hypothetical_return: -0.02 } },
    limitations: ["research_only"],
    report_hash: "hash-1",
    research_status: "research_only",
    created_by: "pytest",
    audit_correlation_id: "corr-scenario",
    notes: "read only source artifact",
    ...overrides,
  };
}

describe("ResearchHubView (relocated ResearchManagementPage suite)", () => {
  it("renders read-only catalog, metadata detail, organization context, and governed artifacts", () => {
    render(
      <ResearchManagementWorkspace
        collections={[collection()]}
        members={[member()]}
        tags={[tag()]}
        artifacts={[scenario()]}
      />,
    );

    expect(screen.getAllByText("Unified Research Artifact Explorer").length).toBeGreaterThan(0);
    expect(screen.getByText("Research-only artifact discovery.")).toBeInTheDocument();
    // Re-target (b): the frame's route posture now pins the post-absorption home.
    expect(screen.getByLabelText("Unified artifact explorer frame")).toHaveTextContent(
      "/?view=research",
    );
    expect(screen.getByLabelText("Artifact explorer completion guardrails")).toHaveTextContent("Organization-only");
    expect(screen.getByLabelText("Read-only unified artifact catalog")).toHaveTextContent(
      "Hypothetical Downside Shock",
    );
    const detail = screen.getByLabelText("Read-only artifact metadata detail");
    expect(within(detail).getByText("scenario-1")).toBeInTheDocument();
    expect(within(detail).getByText("hash-1")).toBeInTheDocument();
    expect(within(detail).getAllByText("research_only").length).toBeGreaterThan(0);
    expect(within(detail).getByText("source-1")).toBeInTheDocument();
    expect(screen.getAllByText("Macro Scenario Review").length).toBeGreaterThan(0);
    expect(screen.getAllByText("review-priority").length).toBeGreaterThan(0);
  });

  it("exposes no organization mutation or execution/order/account controls", () => {
    render(
      <ResearchManagementWorkspace
        collections={[collection()]}
        members={[member()]}
        tags={[tag()]}
        artifacts={[scenario()]}
      />,
    );

    const buttonText = screen
      .getAllByRole("button")
      .map((button) => button.textContent?.toLowerCase() ?? "")
      .join(" ");
    for (const word of [
      "create collection",
      "add member",
      "create tag",
      "delete",
      "remove",
      "update",
      "submit",
      "b" + "uy",
      "s" + "ell",
      "exec" + "ute",
      "go live",
    ]) {
      expect(buttonText).not.toContain(word);
    }

    expect(screen.queryByLabelText("Research collection editor")).not.toBeInTheDocument();
    expect(screen.queryByText("Create collection")).not.toBeInTheDocument();
    expect(screen.queryByText("Add member reference")).not.toBeInTheDocument();
    expect(screen.queryByText("Create tag")).not.toBeInTheDocument();
  });

  it("requires auth / blocks logged-out access", () => {
    render(
      <MemoryRouter initialEntries={["/research-management"]}>
        <Routes>
          <Route path="/login" element={<div>Operator login required</div>} />
          <Route
            path="/research-management"
            element={
              <ProtectedRoute>
                <ResearchManagementWorkspace
                  collections={[collection()]}
                  members={[member()]}
                  tags={[tag()]}
                  artifacts={[scenario()]}
                />
              </ProtectedRoute>
            }
          />
        </Routes>
      </MemoryRouter>,
    );

    expect(screen.getByText("Operator login required")).toBeInTheDocument();
    expect(screen.queryByText("Unified Research Artifact Explorer")).not.toBeInTheDocument();
  });

  it("test_uiconv_p03_item4_legacy_route_redirects_to_the_research_stage_view", () => {
    // The registry route `/research-management` now resolves to the terminal
    // research stage deep link (/?view=research) via the P02 Navigate-replace
    // pattern — the explorer's post-absorption home.
    render(
      <MemoryRouter initialEntries={["/research-management"]}>
        <Routes>
          <Route
            path="/"
            element={<div data-testid="research-stage-probe">research stage probe</div>}
          />
          <Route path="/research-management" element={<ResearchManagementRedirect />} />
        </Routes>
      </MemoryRouter>,
    );

    expect(screen.getByTestId("research-stage-probe")).toBeInTheDocument();
    expect(screen.getByText("research stage probe")).toBeInTheDocument();
  });

  it("test_uiconv_p03_item4_r4_testid_hooks_cover_every_major_region", () => {
    // R4: every major region carries a data-testid hook.
    render(
      <ResearchManagementWorkspace
        collections={[collection()]}
        members={[member()]}
        tags={[tag()]}
        artifacts={[scenario()]}
        onCreateCollection={vi.fn()}
        onAddMember={vi.fn()}
        onRemoveMember={vi.fn()}
        onCreateTag={vi.fn()}
        onRefresh={vi.fn()}
        sourceStatus={[
          { family: "Scenario reports", state: "ready", detail: null, rowCount: 1 },
          { family: "Advisory signals", state: "error", detail: "seam down", rowCount: 0 },
          { family: "Trade plans", state: "loading", detail: null, rowCount: 0 },
        ]}
        mutationError="Failed to save tag record"
      />,
    );

    expect(screen.getByTestId("research-hub-header")).toBeInTheDocument();
    expect(screen.getByTestId("research-hub-refresh")).toBeInTheDocument();
    expect(screen.getByTestId("artifact-explorer-disclaimer")).toBeInTheDocument();
    expect(screen.getByTestId("artifact-explorer-frame")).toBeInTheDocument();
    expect(screen.getByTestId("artifact-explorer-guardrail")).toBeInTheDocument();
    expect(screen.getByTestId("artifact-explorer-completion-guardrails")).toBeInTheDocument();
    expect(screen.getByTestId("artifact-source-counts")).toBeInTheDocument();
    expect(screen.getByTestId("artifact-source-inventory")).toBeInTheDocument();
    expect(screen.getByTestId("artifact-catalog")).toBeInTheDocument();
    expect(screen.getByTestId("artifact-filter-panel")).toBeInTheDocument();
    expect(screen.getByTestId("artifact-catalog-list")).toBeInTheDocument();
    expect(screen.getByTestId("artifact-detail-card")).toBeInTheDocument();
    expect(screen.getByTestId("collection-organization-controls")).toBeInTheDocument();
    expect(screen.getByTestId("tag-organization-controls")).toBeInTheDocument();
    expect(screen.getByTestId("organization-records-preview")).toBeInTheDocument();
    // M5 regions: per-source status rows and the mutation error banner.
    expect(screen.getByTestId("artifact-source-status")).toBeInTheDocument();
    expect(screen.getAllByTestId("source-status-ready").length).toBeGreaterThan(0);
    expect(screen.getAllByTestId("source-status-error").length).toBeGreaterThan(0);
    expect(screen.getAllByTestId("source-status-loading").length).toBeGreaterThan(0);
    expect(screen.getByTestId("research-hub-mutation-error")).toBeInTheDocument();
  });
});
