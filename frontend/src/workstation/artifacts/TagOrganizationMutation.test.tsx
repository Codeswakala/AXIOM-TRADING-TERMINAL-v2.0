import { fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import {
  ResearchManagementWorkspace,
  assertTagOrganizationPayload,
} from "../../components/terminal/research/ResearchHubView";
import type { ResearchCollection, ResearchCollectionMember, ResearchTag, ResearchTagWrite, ScenarioReport } from "../../api/client";
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
  collection_id: "collection-ui006-p05-1",
  created_at: "2026-07-26T08:00:00Z",
  updated_at: "2026-07-26T08:00:00Z",
  operator_id: "operator-1",
  name: "P05 Tag Review",
  description: "Existing organization record.",
  research_status: "research_only",
  audit_correlation_id: "corr-collection-ui006-p05-1",
};

const member: ResearchCollectionMember = {
  member_id: "member-ui006-p05-1",
  created_at: "2026-07-26T08:00:00Z",
  operator_id: "operator-1",
  collection_id: "collection-ui006-p05-1",
  artifact_type: "scenario_report",
  artifact_id: "scenario-ui006-p05-1",
  audit_correlation_id: "corr-member-ui006-p05-1",
};

const tag: ResearchTag = {
  tag_id: "tag-ui006-p05-1",
  created_at: "2026-07-26T08:00:00Z",
  operator_id: "operator-1",
  artifact_type: "scenario_report",
  artifact_id: "scenario-ui006-p05-1",
  tag: "existing-review-tag",
  audit_correlation_id: "corr-tag-ui006-p05-1",
};

const scenario: ScenarioReport = {
  id: "scenario-ui006-p05-1",
  created_at: "2026-07-26T08:00:00Z",
  artifact_type: "scenario_report",
  method_version: "scenario.method.v1",
  market_class: "forex",
  symbol: "EURUSD",
  timeframe: "M1",
  as_of_start: "2026-07-26T07:00:00Z",
  as_of_end: "2026-07-26T08:00:00Z",
  sample_count: 6,
  scenario_name: "P05 tag scenario artifact",
  hypothetical_return: 0.01,
  scenario_result: { hypothetical_return: 0.01, counterfactual_index: 1.01 },
  assumptions: { horizon_bars: 4 },
  inputs: { baseline_returns: [0.01] },
  uncertainty: { method: "historical_band", lower: 0, upper: 0.02, sample_count: 6 },
  economic_usefulness: { verdict: "not_assessed" },
  config: { fixture: true },
  input_lineage: { input_policy: "as_of_bounded_hypothetical_research" },
  source_artifact_ids: ["source-ui006-p05-1"],
  market_scope: { symbol: "EURUSD", timeframe: "M1", sample_count: 6 },
  results: { stored: true },
  limitations: ["hypothetical_counterfactual_research_only", "not_a_prediction"],
  report_hash: "scenario-hash-ui006-p05-1",
  research_status: "research_only",
  created_by: "test",
  audit_correlation_id: "corr-scenario-ui006-p05-1",
  notes: "read only source artifact",
};

function workspace(onCreateTag?: (payload: ResearchTagWrite) => void) {
  return (
    <ResearchManagementWorkspace
      collections={[collection]}
      members={[member]}
      tags={[tag]}
      artifacts={[scenario]}
      onCreateTag={onCreateTag}
    />
  );
}

function renderExplorerShell(onCreateTag?: (payload: ResearchTagWrite) => void) {
  render(
    <MemoryRouter initialEntries={["/research-management"]}>
      <Routes>
        <Route element={<InstitutionalWorkspaceShell />}>
          <Route path="/research-management" element={workspace(onCreateTag)} />
        </Route>
      </Routes>
    </MemoryRouter>,
  );
}

describe("UI-006-P05 tag organization mutation", () => {
  it("test_ui006_tags_mutate_existing_research_tag_store_only", () => {
    const onCreateTag = vi.fn();
    render(workspace(onCreateTag as unknown as (payload: ResearchTagWrite) => void));

    expect(screen.getByLabelText("Tag organization controls")).toHaveTextContent(
      "existing W7 research tag store",
    );
    fireEvent.click(screen.getByText("Save tag record"));
    expect(onCreateTag).toHaveBeenCalledTimes(1);
  });

  it("test_ui006_tags_write_labels_and_artifact_references_not_source_payloads", () => {
    const onCreateTag = vi.fn();
    render(workspace(onCreateTag as unknown as (payload: ResearchTagWrite) => void));

    fireEvent.click(screen.getByText("Save tag record"));
    const payload = onCreateTag.mock.calls[0][0] as ResearchTagWrite;
    expect(Object.keys(payload).sort()).toEqual(["artifact_id", "artifact_type", "tag"]);
    expect(payload).toEqual({
      artifact_type: "scenario_report",
      artifact_id: "scenario-ui006-p05-1",
      tag: "artifact-review",
    });
  });

  it("test_ui006_tags_reject_order_account_execution_and_verdict_fields", () => {
    const disallowedPayloadKey = ["economic", "_verdict"].join("");
    const disallowedReferenceKey = ["order", "_ticket"].join("");

    expect(
      assertTagOrganizationPayload({
        artifact_type: "scenario_report",
        artifact_id: "scenario-ui006-p05-1",
        tag: "allowed",
      }),
    ).toEqual({
      artifact_type: "scenario_report",
      artifact_id: "scenario-ui006-p05-1",
      tag: "allowed",
    });
    expect(() =>
      assertTagOrganizationPayload({
        artifact_type: "scenario_report",
        artifact_id: "scenario-ui006-p05-1",
        tag: "blocked",
        [disallowedPayloadKey]: "blocked",
      }),
    ).toThrow("TAG_ORGANIZATION_FIELD_NOT_ALLOWED");
    expect(() =>
      assertTagOrganizationPayload({
        artifact_type: "scenario_report",
        artifact_id: "scenario-ui006-p05-1",
        tag: "blocked",
        [disallowedReferenceKey]: "blocked",
      }),
    ).toThrow("TAG_ORGANIZATION_FIELD_NOT_ALLOWED");
  });

  it("test_ui006_tag_mutation_does_not_modify_underlying_artifact_values", () => {
    const onCreateTag = vi.fn();
    render(workspace(onCreateTag as unknown as (payload: ResearchTagWrite) => void));

    const before = screen.getByLabelText("Read-only artifact metadata detail");
    expect(before).toHaveTextContent("scenario-ui006-p05-1");
    expect(before).toHaveTextContent("scenario-hash-ui006-p05-1");
    expect(before).toHaveTextContent("not_assessed");
    expect(before).toHaveTextContent("historical_band");

    fireEvent.click(screen.getByText("Save tag record"));
    const after = screen.getByLabelText("Read-only artifact metadata detail");
    expect(after).toHaveTextContent("scenario-ui006-p05-1");
    expect(after).toHaveTextContent("scenario-hash-ui006-p05-1");
    expect(after).toHaveTextContent("not_assessed");
    expect(after).toHaveTextContent("historical_band");
  });

  it("test_ui006_tag_mutation_accessibility_brand_and_operator_scope_hold", () => {
    renderExplorerShell(vi.fn() as unknown as (payload: ResearchTagWrite) => void);

    expect(screen.getByText(/AXIOM Institutional Workstation/i)).toBeInTheDocument();
    expect(screen.getAllByText("Gate CLOSED").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("Research-only").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByLabelText("Unified artifact explorer frame")).toBeInTheDocument();
    expect(screen.getByLabelText("Tag organization controls")).toBeInTheDocument();
    expect(screen.getByLabelText("Create artifact tag organization record")).toBeInTheDocument();
    expect(document.body.querySelectorAll(".mono").length).toBeGreaterThan(8);
  });
});
