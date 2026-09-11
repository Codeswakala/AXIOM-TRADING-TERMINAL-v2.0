import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { AssistantCommandSurface } from "./AssistantCommandSurface";
import { ContextualAssistantPanel } from "./ContextualAssistantPanel";
import { ResearchReportSummarizer } from "./ResearchReportSummarizer";
import { DocumentationLookupSurface } from "./DocumentationLookupSurface";
import { AssistantAuditSubSection } from "../governance/AssistantAuditSubSection";
import { AssistantReviewSubPanel } from "../../pages/institutional/AssistantReviewSubPanel";
import { QUICK_ACTION_CATALOGUE } from "../commands/quickActionCatalogue";
import { ASSISTANT_REFUSAL_REASON_CODES } from "../../test/ui008_refusal_taxonomy.fixture";
import { WorkspaceContextProvider } from "./WorkspaceContext";

describe("UI-008-P06 Institutional AI Completion Checkpoint Suite", () => {
  // Test 1: All UI-008 surfaces render with mandatory disclaimers
  it("test_ui008_completion_all_surfaces_render_mandatory_disclaimers", () => {
    // 1. Command surface
    const { unmount: u1 } = render(<AssistantCommandSurface />);
    expect(screen.getByTestId("r5-6")).toHaveTextContent("AI-generated research assistance only");
    expect(screen.getByTestId("r5-6")).toHaveTextContent("AXIOM does not act");
    u1();

    // 2. Contextual panel
    const { unmount: u2 } = render(
      <WorkspaceContextProvider>
        <ContextualAssistantPanel />
      </WorkspaceContextProvider>,
    );
    expect(screen.getByTestId("contextual-disclaimer")).toHaveTextContent("AI-generated research assistance only");
    expect(screen.getByTestId("contextual-disclaimer")).toHaveTextContent("AXIOM does not act");
    u2();

    // 3. Report summarizer
    const { unmount: u3 } = render(
      <ResearchReportSummarizer
        report={{ id: "rep-test", artifact_type: "regime_report" }}
        reportType="regime"
      />,
    );
    expect(screen.getByTestId("summarizer-disclaimer")).toHaveTextContent("Deterministic rule-based research summary only");
    expect(screen.getByTestId("summarizer-disclaimer")).toHaveTextContent("AXIOM does not act");
    u3();

    // 4. Documentation lookup
    const { unmount: u4 } = render(<DocumentationLookupSurface />);
    expect(screen.getByTestId("doc-disclaimer")).toHaveTextContent("Platform documentation and knowledge lookup for research only");
    expect(screen.getByTestId("doc-disclaimer")).toHaveTextContent("AXIOM does not act");
    u4();

    // 5. Audit subsection
    const { unmount: u5 } = render(<AssistantAuditSubSection />);
    expect(screen.getByTestId("r5-6")).toHaveTextContent("AXIOM does not act");
    u5();

    // 6. Review sub-panel
    const { unmount: u6 } = render(<AssistantReviewSubPanel />);
    expect(screen.getByTestId("r5-6")).toHaveTextContent("AXIOM does not act");
    u6();
  });

  // Test 2: Zero functional actuation controls on any AI surface
  it("test_ui008_completion_zero_actuation_controls_on_all_surfaces", () => {
    const { container: c1, unmount: u1 } = render(<AssistantCommandSurface />);
    const { container: c2, unmount: u2 } = render(
      <WorkspaceContextProvider>
        <ContextualAssistantPanel />
      </WorkspaceContextProvider>,
    );
    const { container: c3, unmount: u3 } = render(<DocumentationLookupSurface />);

    const allButtons = [
      ...c1.querySelectorAll("button"),
      ...c2.querySelectorAll("button"),
      ...c3.querySelectorAll("button"),
    ];

    const buttonTexts = allButtons.map((b) => b.textContent?.toLowerCase() ?? "").join(" ");
    const forbiddenActuationTerms = ["buy", "sell", "place order", "execute trade", "submit order"];

    for (const term of forbiddenActuationTerms) {
      expect(buttonTexts).not.toContain(term);
    }

    u1();
    u2();
    u3();
  });

  // Test 3: Six-code refusal taxonomy completeness
  it("test_ui008_completion_six_code_refusal_taxonomy_completeness", () => {
    expect(ASSISTANT_REFUSAL_REASON_CODES).toHaveLength(6);
    expect(ASSISTANT_REFUSAL_REASON_CODES).toContain("ORDER_INSTRUCTION_REFUSED");
    expect(ASSISTANT_REFUSAL_REASON_CODES).toContain("GATE_OPEN_INSTRUCTION_REFUSED");
    expect(ASSISTANT_REFUSAL_REASON_CODES).toContain("SECRET_EXFILTRATION_REFUSED");
    expect(ASSISTANT_REFUSAL_REASON_CODES).toContain("UNBOUNDED_TOOL_REQUEST_REFUSED");
    expect(ASSISTANT_REFUSAL_REASON_CODES).toContain("GROUNDING_REQUIRED");
    expect(ASSISTANT_REFUSAL_REASON_CODES).toContain("ASSISTANT_DISABLED");
  });

  // Test 4: Quick action catalogue contains all 33 commands including 4 Assistant actions
  it("test_ui008_completion_quick_action_catalogue_contains_33_commands_with_assistant_group", () => {
    expect(QUICK_ACTION_CATALOGUE).toHaveLength(33);

    const assistantCommands = QUICK_ACTION_CATALOGUE.filter((cmd) => cmd.group === "Assistant");
    expect(assistantCommands).toHaveLength(4);

    const assistantIds = assistantCommands.map((cmd) => cmd.id);
    expect(assistantIds).toContain("qa.open.assistant-surfaces");
    expect(assistantIds).toContain("qa.open.recent-assistant-responses");
    expect(assistantIds).toContain("qa.open.assistant-refusals-audit");
    expect(assistantIds).toContain("qa.open.documentation-lookup");

    for (const cmd of assistantCommands) {
      expect(cmd.noActuation).toBe(true);
      expect(cmd.commandType).toBe("navigation");
    }
  });

  // Test 5: Governance Gate and Production Certification firewalls hold
  it("test_ui008_completion_governance_gate_and_production_certification_firewalls_hold", () => {
    render(<AssistantCommandSurface />);
    const banner = screen.getByTestId("td-078-self-description");
    expect(banner).toHaveTextContent("no external LLM");
    expect(banner).toHaveTextContent("external LLM requires a future gated Build Order");
  });
});
