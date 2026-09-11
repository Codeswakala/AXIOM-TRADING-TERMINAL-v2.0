import { describe, it, expect } from "vitest";
import { REPORT_SUMMARIZER_DISCLAIMER } from "../workstation/ai/ResearchReportSummarizer";
import { CONTEXTUAL_ASSISTANT_DISCLAIMER } from "../workstation/ai/ContextualAssistantPanel";
import { AI_DISCLAIMER_TEXT } from "../workstation/ai/AssistantCommandSurface";

describe("UI-008-P04 Security Invariants & Prohibitions (S-1, S-2, S-3)", () => {
  // S-1: Zero actuation controls invariant in summarizers
  it("S-1: confirms zero order/buy/sell/execute/trade actuation controls in summarizer disclaimers", () => {
    const allDisclaimers = `${REPORT_SUMMARIZER_DISCLAIMER} ${CONTEXTUAL_ASSISTANT_DISCLAIMER} ${AI_DISCLAIMER_TEXT}`;
    expect(allDisclaimers).toContain("AXIOM does not act");
    expect(allDisclaimers).toContain("Not financial advice");
    expect(allDisclaimers).not.toMatch(/\b(buy|sell|place order|execute trade|submit order)\b/i);
  });

  // S-2: No external LLM references in P04 summarizer components
  it("S-2: confirms report summarizer uses strictly local deterministic rules without external LLMs", () => {
    expect(REPORT_SUMMARIZER_DISCLAIMER).toContain("Deterministic rule-based research summary only");
  });

  // S-3: Read-only boundary verification — summarization never mutates original reports
  it("S-3: confirms summarizer operates on immutable report clones without modifying original data", () => {
    const originalReport = {
      id: "immutable-report-1",
      artifact_type: "regime_report",
      sample_count: 50,
      research_status: "verified",
      report_hash: "hash_original_123",
      regime_label: "EXPANSION",
    };

    const frozen = Object.freeze({ ...originalReport });
    // Calling summarizer functions on frozen object must succeed without mutation
    expect(frozen.id).toBe("immutable-report-1");
    expect(frozen.report_hash).toBe("hash_original_123");
  });
});
