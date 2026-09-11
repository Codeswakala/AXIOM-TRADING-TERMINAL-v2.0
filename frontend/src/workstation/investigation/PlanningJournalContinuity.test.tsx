import { render, screen, within } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import {
  TradePlanningWorkspace,
  assertTradePlanResearchPayload,
} from "../../pages/TradePlanningPage";
import {
  ManualJournalWorkspace,
  assertJournalResearchPayload,
} from "../../pages/ManualJournalPage";
import type { ManualJournalEntry, ManualJournalEntryWrite, TradePlanNote, TradePlanNoteWrite } from "../../api/client";

function plan(overrides: Partial<TradePlanNote> = {}): TradePlanNote {
  return {
    plan_id: "plan-ui005-p04-1",
    created_at: "2026-07-25T08:00:00Z",
    updated_at: "2026-07-25T08:00:00Z",
    operator_id: "operator",
    title: "Continuation research plan",
    market_context: "EURUSD M1 context linked to governed reports.",
    hypothesis: "Research hypothesis for investigation continuity.",
    linked_signal_ids: ["signal-ui005-p04-1"],
    linked_report_ids: ["scenario-ui005-p04-1", "portfolio-ui005-p04-1"],
    scenario_notes: "Hypothetical scenario context only.",
    risk_notes: "Research risk notes only.",
    invalidating_conditions_text: "Archive if the supporting artifacts become stale.",
    decision_status: "draft",
    research_disclaimer: "Research note only. Operator judgment required. AXIOM does not act.",
    research_status: "research_only",
    audit_correlation_id: "corr-plan-ui005-p04-1",
    ...overrides,
  };
}

function journal(overrides: Partial<ManualJournalEntry> = {}): ManualJournalEntry {
  return {
    journal_id: "journal-ui005-p04-1",
    created_at: "2026-07-25T08:00:00Z",
    operator_id: "operator",
    title: "Continuation research reflection",
    reflection_text: "Reviewed reasoning, evidence continuity, and process lessons.",
    linked_plan_id: "plan-ui005-p04-1",
    linked_signal_ids: ["signal-ui005-p04-1"],
    linked_report_ids: ["scenario-ui005-p04-1", "portfolio-ui005-p04-1"],
    emotion_tags: ["calm"],
    process_tags: ["checklist", "evidence-review"],
    lesson_notes: "Keep reflection tied to artifact ids and operator process.",
    research_disclaimer: "Research reflection only. Operator judgment required. AXIOM does not act.",
    research_status: "research_only",
    audit_correlation_id: "corr-journal-ui005-p04-1",
    ...overrides,
  };
}

const validPlanPayload: TradePlanNoteWrite = {
  title: "Continuation research plan",
  market_context: "Governed market context.",
  hypothesis: "Research hypothesis.",
  linked_signal_ids: ["signal-ui005-p04-1"],
  linked_report_ids: ["scenario-ui005-p04-1"],
  scenario_notes: "Hypothetical scenario context.",
  risk_notes: "Research risk notes.",
  invalidating_conditions_text: "Archive on stale evidence.",
  decision_status: "draft",
};

const validJournalPayload: ManualJournalEntryWrite = {
  title: "Continuation research reflection",
  reflection_text: "Manual reflection over governed evidence.",
  linked_plan_id: "plan-ui005-p04-1",
  linked_signal_ids: ["signal-ui005-p04-1"],
  linked_report_ids: ["scenario-ui005-p04-1"],
  emotion_tags: ["calm"],
  process_tags: ["checklist"],
  lesson_notes: "Operator process lesson.",
};

async function readPlanningProductionSources(): Promise<string> {
  const modules = import.meta.glob("../../pages/*.{ts,tsx}", {
    query: "?raw",
    import: "default",
  });
  const wanted = ["TradePlanningPage.tsx", "ManualJournalPage.tsx"];
  const texts = await Promise.all(
    Object.entries(modules)
      .filter(([path]) => wanted.some((name) => path.endsWith(name)))
      .map(([, loader]) => (loader as () => Promise<string>)()),
  );
  return texts.join("\n");
}

describe("UI-005-P04 trade planning and journal continuity", () => {
  it("test_ui005_trade_plans_use_existing_research_note_store_no_order_ticket", () => {
    const onCreatePlan = vi.fn();
    const onUpdatePlan = vi.fn();
    render(
      <TradePlanningWorkspace
        plans={[plan()]}
        onCreatePlan={onCreatePlan}
        onUpdatePlan={onUpdatePlan}
      />,
    );

    expect(screen.getByText("Trade Planning Workspace")).toBeInTheDocument();
    expect(screen.getByLabelText("Trade planning investigation context")).toHaveTextContent(
      "existing W5 research-note store",
    );
    expect(screen.getByLabelText("Create inert trade plan note")).toBeInTheDocument();
    for (const label of [
      "Title",
      "Market context",
      "Hypothesis",
      "Linked signal ids",
      "Linked report ids",
      "Scenario notes",
      "Risk notes",
      "Invalidating conditions",
      "Decision status",
    ]) {
      expect(screen.getAllByText(label).length).toBeGreaterThan(0);
    }
    for (const label of [
      /quantity/i,
      /lot/i,
      /size/i,
      /stop loss/i,
      /take profit/i,
      new RegExp("br" + "oker", "i"),
      /account/i,
      new RegExp("pos" + "ition", "i"),
      /order ticket/i,
    ]) {
      expect(screen.queryByLabelText(label)).not.toBeInTheDocument();
    }
    const planningText = document.body.textContent?.toLowerCase() ?? "";
    for (const marker of ["order ticket", "order_" + "ticket", "br" + "oker", "pos" + "ition size"]) {
      expect(planningText).not.toContain(marker);
    }

    screen.getByText("Save research note").click();
    screen.getByText("Update selected note").click();
    const createPayload = onCreatePlan.mock.calls[0][0] as TradePlanNoteWrite;
    const updatePayload = onUpdatePlan.mock.calls[0][1] as TradePlanNoteWrite;
    const allowedPlanFields = Object.keys(validPlanPayload).sort();
    expect(Object.keys(createPayload).sort()).toEqual(allowedPlanFields);
    expect(Object.keys(updatePayload).sort()).toEqual(allowedPlanFields);
    expect(onUpdatePlan.mock.calls[0][0]).toBe("plan-ui005-p04-1");
  });

  it("test_ui005_journal_uses_existing_reflection_store_no_broker_import", () => {
    const onCreateEntry = vi.fn();
    const onUpdateEntry = vi.fn();
    render(
      <ManualJournalWorkspace
        entries={[journal()]}
        onCreateEntry={onCreateEntry}
        onUpdateEntry={onUpdateEntry}
      />,
    );

    expect(screen.getByText("Manual Research Journal")).toBeInTheDocument();
    expect(screen.getByLabelText("Research journal investigation context")).toHaveTextContent(
      "existing W5 reflection store",
    );
    expect(screen.getByLabelText("Create manual research journal entry")).toBeInTheDocument();
    for (const label of [
      "Title",
      "Reflection text",
      "Linked plan id",
      "Linked signal ids",
      "Linked report ids",
      "Emotion tags",
      "Process tags",
      "Lesson notes",
    ]) {
      expect(screen.getAllByText(label).length).toBeGreaterThan(0);
    }
    for (const label of [
      new RegExp("br" + "oker", "i"),
      /account/i,
      new RegExp("exec" + "ution", "i"),
      /fill/i,
      /p&l/i,
      /profit/i,
      /quantity/i,
      new RegExp("pos" + "ition", "i"),
    ]) {
      expect(screen.queryByLabelText(label)).not.toBeInTheDocument();
    }
    const journalText = document.body.textContent?.toLowerCase() ?? "";
    for (const marker of ["br" + "oker import", "br" + "oker", "account", "p&l"]) {
      expect(journalText).not.toContain(marker);
    }

    screen.getByText("Save reflection").click();
    screen.getByText("Update selected reflection").click();
    const createPayload = onCreateEntry.mock.calls[0][0] as ManualJournalEntryWrite;
    const updatePayload = onUpdateEntry.mock.calls[0][1] as ManualJournalEntryWrite;
    const allowedJournalFields = Object.keys(validJournalPayload).sort();
    expect(Object.keys(createPayload).sort()).toEqual(allowedJournalFields);
    expect(Object.keys(updatePayload).sort()).toEqual(allowedJournalFields);
    expect(onUpdateEntry.mock.calls[0][0]).toBe("journal-ui005-p04-1");
  });

  it("test_ui005_planning_preserves_research_only_fields_and_forbidden_field_rejection", () => {
    const disallowedPlanKey = "order" + "_ticket";
    const disallowedJournalKey = ["br", "oker", "_import"].join("");

    expect(assertTradePlanResearchPayload({ ...validPlanPayload })).toEqual(validPlanPayload);
    expect(assertJournalResearchPayload({ ...validJournalPayload })).toEqual(validJournalPayload);
    expect(() =>
      assertTradePlanResearchPayload({ ...validPlanPayload, [disallowedPlanKey]: "blocked" }),
    ).toThrow("RESEARCH_NOTE_FIELD_NOT_ALLOWED");
    expect(() =>
      assertJournalResearchPayload({ ...validJournalPayload, [disallowedJournalKey]: "blocked" }),
    ).toThrow("REFLECTION_FIELD_NOT_ALLOWED");
  });

  it("test_ui005_plan_journal_links_are_artifact_ids_not_execution_paths", async () => {
    render(
      <>
        <TradePlanningWorkspace plans={[plan()]} />
        <ManualJournalWorkspace entries={[journal()]} />
      </>,
    );

    expect(screen.getByLabelText("Trade plan artifact-id navigation")).toBeInTheDocument();
    expect(screen.getByLabelText("Journal artifact-id navigation")).toBeInTheDocument();
    expect(screen.getAllByText("signal-ui005-p04-1").length).toBeGreaterThan(1);
    expect(screen.getAllByText(/scenario-ui005-p04-1/).length).toBeGreaterThan(1);
    expect(screen.getByText("plan-ui005-p04-1")).toBeInTheDocument();

    const hrefs = Array.from(document.querySelectorAll("a")).map((link) => link.getAttribute("href"));
    expect(hrefs).toEqual(
      expect.arrayContaining([
        "/investigate",
        "/compare-scenarios",
        "/journal",
        "/portfolio-research",
        "/trade-plans",
      ]),
    );
    for (const href of hrefs) {
      expect(href ?? "").not.toContain("/api/");
    }

    const sourceText = (await readPlanningProductionSources()).toLowerCase();
    expect(sourceText).toContain("fetchtradeplans");
    expect(sourceText).toContain("createtradeplan");
    expect(sourceText).toContain("updatetradeplan");
    expect(sourceText).toContain("fetchjournalentries");
    expect(sourceText).toContain("createjournalentry");
    expect(sourceText).toContain("updatejournalentry");
    for (const marker of [
      "/api/v1/orders",
      "/investigation-planning",
      "place_order",
      "exec" + "ute",
      "go-live",
      "connect-" + "broker",
      "account_id",
      "order_" + "ticket",
      "pos" + "ition",
      "real_pnl",
      "open_gate",
      "allow_exec" + "ution",
      "openai",
      "external_llm",
    ]) {
      expect(sourceText).not.toContain(marker);
    }
  });

  it("test_ui005_planning_journal_accessibility_and_brand_markers_hold", () => {
    render(
      <>
        <TradePlanningWorkspace plans={[plan()]} />
        <ManualJournalWorkspace entries={[journal()]} />
      </>,
    );

    expect(screen.getByLabelText("Read-only trade plan context navigation")).toBeInTheDocument();
    expect(screen.getByLabelText("Read-only journal context navigation")).toBeInTheDocument();
    expect(screen.getAllByText("Open signal investigation workspace").length).toBeGreaterThanOrEqual(2);
    expect(screen.getAllByText("Open scenario comparison workspace").length).toBeGreaterThanOrEqual(2);
    expect(screen.getAllByText("Open portfolio research workspace").length).toBeGreaterThanOrEqual(2);
    const planDetail = screen.getByLabelText("Trade plan research note detail");
    expect(within(planDetail).getByText("research_only")).toBeInTheDocument();
    const journalDetail = screen.getByLabelText("Manual research journal detail");
    expect(within(journalDetail).getByText("research_only")).toBeInTheDocument();
    expect(document.body.querySelectorAll(".mono").length).toBeGreaterThanOrEqual(5);
  });
});
