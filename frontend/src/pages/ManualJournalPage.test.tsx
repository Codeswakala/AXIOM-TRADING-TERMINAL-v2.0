import { render, screen, within } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { ManualJournalWorkspace } from "./ManualJournalPage";
import type { ManualJournalEntry } from "../api/client";

function entry(overrides: Partial<ManualJournalEntry> = {}): ManualJournalEntry {
  return {
    journal_id: "journal-1",
    created_at: "2026-07-17T10:00:00Z",
    operator_id: "operator",
    title: "Manual research reflection",
    reflection_text: "Reviewed reasoning and process lessons only.",
    linked_plan_id: "plan-1",
    linked_signal_ids: ["signal-1"],
    linked_report_ids: ["report-1"],
    emotion_tags: ["calm"],
    process_tags: ["checklist"],
    lesson_notes: "Keep reflections separate from external records.",
    research_disclaimer:
      "Manual research journal entry only. Not financial advice, not a trade record, not a trade instruction. Operator judgment required. AXIOM does not act.",
    research_status: "research_only",
    audit_correlation_id: "corr-1",
    ...overrides,
  };
}

describe("ManualJournalWorkspace", () => {
  it("renders persisted reflection with disclaimer and linked ids", () => {
    render(<ManualJournalWorkspace entries={[entry()]} />);

    expect(screen.getByText("Manual Research Journal")).toBeInTheDocument();
    expect(screen.getByText("Manual research reflection only.")).toBeInTheDocument();
    expect(screen.getAllByText(/AXIOM does not act/).length).toBeGreaterThan(0);
    const detail = screen.getByLabelText("Manual research journal detail");
    expect(within(detail).getByText("Manual research reflection")).toBeInTheDocument();
    expect(within(detail).getByText("plan-1")).toBeInTheDocument();
    expect(within(detail).getByText("signal-1")).toBeInTheDocument();
    expect(within(detail).getByText("report-1")).toBeInTheDocument();
    expect(within(detail).getByText(/calm/)).toBeInTheDocument();
  });

  it("renders only research reflection fields and no forbidden record labels", () => {
    render(<ManualJournalWorkspace entries={[entry()]} />);

    expect(screen.getByLabelText("Create manual research journal entry")).toBeInTheDocument();
    expect(screen.getAllByText("Reflection text").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Linked plan id").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Lesson notes").length).toBeGreaterThan(0);
    const forbiddenLabels = [/broker/i, /account/i, /execution/i, /fill/i, /p&l/i, /profit/i, /quantity/i, /position/i];
    for (const label of forbiddenLabels) {
      expect(screen.queryByLabelText(label)).not.toBeInTheDocument();
    }
  });

  it("does not expose import or action controls", () => {
    render(<ManualJournalWorkspace entries={[entry()]} />);

    const buttonText = screen
      .getAllByRole("button")
      .map((button) => button.textContent?.toLowerCase() ?? "")
      .join(" ");
    const forbidden = ["import", "broker", "account", "execute", "submit", "order", "p&l"];
    for (const word of forbidden) {
      expect(buttonText).not.toContain(word);
    }
  });

  it("creates and updates reflections through journal-store callbacks only", async () => {
    const onCreateEntry = vi.fn();
    const onUpdateEntry = vi.fn();
    render(
      <ManualJournalWorkspace
        entries={[entry()]}
        onCreateEntry={onCreateEntry}
        onUpdateEntry={onUpdateEntry}
      />,
    );

    screen.getByText("Save reflection").click();
    expect(onCreateEntry).toHaveBeenCalledTimes(1);
    screen.getByText("Update selected reflection").click();
    expect(onUpdateEntry).toHaveBeenCalledTimes(1);
  });

  it("shows empty state without broker-record wording", () => {
    render(<ManualJournalWorkspace entries={[]} />);
    expect(screen.getByText(/No manual research journal entries/)).toBeInTheDocument();
    const text = screen.getByLabelText("Persisted manual journal entries").textContent?.toLowerCase() ?? "";
    expect(text).not.toContain("broker");
    expect(text).not.toContain("account");
    expect(text).not.toContain("p&l");
  });
});
