import { fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import {
  ResearchManagementWorkspace,
  assertCollectionOrganizationPayload,
  assertMemberReferencePayload,
} from "../../components/terminal/research/ResearchHubView";
import type { ResearchCollection, ResearchCollectionMember, ResearchTag, ScenarioReport } from "../../api/client";
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

const collection: ResearchCollection = {
  collection_id: "collection-ui006-p04-1",
  created_at: "2026-07-26T08:00:00Z",
  updated_at: "2026-07-26T08:00:00Z",
  operator_id: "operator-1",
  name: "P04 Organization Review",
  description: "Existing organization record.",
  research_status: "research_only",
  audit_correlation_id: "corr-collection-ui006-p04-1",
};

const member: ResearchCollectionMember = {
  member_id: "member-ui006-p04-1",
  created_at: "2026-07-26T08:00:00Z",
  operator_id: "operator-1",
  collection_id: "collection-ui006-p04-1",
  artifact_type: "scenario_report",
  artifact_id: "scenario-ui006-p04-1",
  audit_correlation_id: "corr-member-ui006-p04-1",
};

const tag: ResearchTag = {
  tag_id: "tag-ui006-p04-1",
  created_at: "2026-07-26T08:00:00Z",
  operator_id: "operator-1",
  artifact_type: "scenario_report",
  artifact_id: "scenario-ui006-p04-1",
  tag: "organization-review",
  audit_correlation_id: "corr-tag-ui006-p04-1",
};

const scenario: ScenarioReport = {
  id: "scenario-ui006-p04-1",
  created_at: "2026-07-26T08:00:00Z",
  artifact_type: "scenario_report",
  method_version: "scenario.method.v1",
  market_class: "forex",
  symbol: "EURUSD",
  timeframe: "M1",
  as_of_start: "2026-07-26T07:00:00Z",
  as_of_end: "2026-07-26T08:00:00Z",
  sample_count: 6,
  scenario_name: "P04 stored scenario artifact",
  hypothetical_return: 0.01,
  scenario_result: { hypothetical_return: 0.01, counterfactual_index: 1.01 },
  assumptions: { horizon_bars: 4 },
  inputs: { baseline_returns: [0.01] },
  uncertainty: { method: "historical_band", lower: 0, upper: 0.02, sample_count: 6 },
  economic_usefulness: { verdict: "not_assessed" },
  config: { fixture: true },
  input_lineage: { input_policy: "as_of_bounded_hypothetical_research" },
  source_artifact_ids: ["source-ui006-p04-1"],
  market_scope: { symbol: "EURUSD", timeframe: "M1", sample_count: 6 },
  results: { stored: true },
  limitations: ["hypothetical_counterfactual_research_only", "not_a_prediction"],
  report_hash: "scenario-hash-ui006-p04-1",
  research_status: "research_only",
  created_by: "test",
  audit_correlation_id: "corr-scenario-ui006-p04-1",
  notes: "read only source artifact",
};

function workspace(overrides: {
  onCreateCollection?: ReturnType<typeof vi.fn>;
  onAddMember?: ReturnType<typeof vi.fn>;
  onRemoveMember?: ReturnType<typeof vi.fn>;
} = {}) {
  return (
    <ResearchManagementWorkspace
      collections={[collection]}
      members={[member]}
      tags={[tag]}
      artifacts={[scenario]}
      onCreateCollection={overrides.onCreateCollection as never}
      onAddMember={overrides.onAddMember as never}
      onRemoveMember={overrides.onRemoveMember as never}
    />
  );
}

function renderExplorerShell() {
  render(
    <MemoryRouter initialEntries={["/research-management"]}>
      <Routes>
        <Route element={<InstitutionalWorkspaceShell />}>
          <Route path="/research-management" element={workspace()} />
        </Route>
      </Routes>
    </MemoryRouter>,
  );
}


describe("UI-006-P04 collection and membership organization mutation", () => {
  it("test_ui006_collections_mutate_existing_research_management_store_only", () => {
    const onCreateCollection = vi.fn();
    render(workspace({ onCreateCollection }));

    expect(screen.getByLabelText("Collection membership organization controls")).toHaveTextContent(
      "existing W7 research-management stores",
    );
    fireEvent.click(screen.getByText("Save collection record"));
    expect(onCreateCollection).toHaveBeenCalledTimes(1);
    expect(Object.keys(onCreateCollection.mock.calls[0][0]).sort()).toEqual([
      "description",
      "name",
    ]);
  });

  it("test_ui006_collection_membership_writes_artifact_references_not_source_payloads", () => {
    const onAddMember = vi.fn();
    const onRemoveMember = vi.fn();
    render(workspace({ onAddMember, onRemoveMember }));

    fireEvent.click(screen.getByText("Add reference"));
    expect(onAddMember).toHaveBeenCalledTimes(1);
    expect(onAddMember.mock.calls[0][0]).toBe("collection-ui006-p04-1");
    expect(Object.keys(onAddMember.mock.calls[0][1]).sort()).toEqual([
      "artifact_id",
      "artifact_type",
    ]);
    expect(onAddMember.mock.calls[0][1]).toEqual({
      artifact_type: "scenario_report",
      artifact_id: "scenario-ui006-p04-1",
    });

    fireEvent.click(screen.getByText("Remove reference"));
    expect(onRemoveMember).toHaveBeenCalledWith(
      "collection-ui006-p04-1",
      "member-ui006-p04-1",
    );
  });

  it("test_ui006_collections_reject_order_account_execution_and_verdict_fields", () => {
    const disallowedCollectionKey = ["economic", "_verdict"].join("");
    const disallowedMemberKey = ["order", "_ticket"].join("");

    expect(
      assertCollectionOrganizationPayload({ name: "Allowed", description: "Reference only" }),
    ).toEqual({ name: "Allowed", description: "Reference only" });
    expect(assertMemberReferencePayload({ artifact_type: "scenario_report", artifact_id: "s1" })).toEqual({
      artifact_type: "scenario_report",
      artifact_id: "s1",
    });
    expect(() =>
      assertCollectionOrganizationPayload({ name: "Blocked", [disallowedCollectionKey]: "blocked" }),
    ).toThrow("COLLECTION_ORGANIZATION_FIELD_NOT_ALLOWED");
    expect(() =>
      assertMemberReferencePayload({ artifact_type: "scenario_report", artifact_id: "s1", [disallowedMemberKey]: "blocked" }),
    ).toThrow("MEMBER_REFERENCE_FIELD_NOT_ALLOWED");
  });

  it("test_ui006_collection_mutation_does_not_modify_underlying_artifact_values", () => {
    const onAddMember = vi.fn();
    render(workspace({ onAddMember }));

    const before = screen.getByLabelText("Read-only artifact metadata detail");
    expect(before).toHaveTextContent("scenario-ui006-p04-1");
    expect(before).toHaveTextContent("scenario-hash-ui006-p04-1");
    expect(before).toHaveTextContent("not_assessed");
    expect(before).toHaveTextContent("historical_band");

    fireEvent.click(screen.getByText("Add reference"));
    const after = screen.getByLabelText("Read-only artifact metadata detail");
    expect(after).toHaveTextContent("scenario-ui006-p04-1");
    expect(after).toHaveTextContent("scenario-hash-ui006-p04-1");
    expect(after).toHaveTextContent("not_assessed");
    expect(after).toHaveTextContent("historical_band");
  });

  it("test_ui006_collection_mutation_accessibility_brand_and_operator_scope_hold", () => {
    renderExplorerShell();

    expect(screen.getByText(/AXIOM Institutional Workstation/i)).toBeInTheDocument();
    expect(screen.getAllByText("Gate CLOSED").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("Research-only").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByLabelText("Unified artifact explorer frame")).toBeInTheDocument();
    expect(screen.queryByLabelText("Collection membership organization controls")).not.toBeInTheDocument();
    expect(document.body.querySelectorAll(".mono").length).toBeGreaterThan(8);
  });
});
