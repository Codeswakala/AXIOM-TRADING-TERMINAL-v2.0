import { render, screen, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { ProtectedRoute } from "../auth/ProtectedRoute";
import { ResearchManagementWorkspace } from "./ResearchManagementPage";
import type {
  ResearchCollection,
  ResearchCollectionMember,
  ResearchTag,
  ScenarioReport,
} from "../api/client";

vi.mock("../context/AuthContext", () => ({
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

describe("ResearchManagementPage", () => {
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
    expect(screen.getByLabelText("Unified artifact explorer frame")).toHaveTextContent(
      "/research-management",
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
});
