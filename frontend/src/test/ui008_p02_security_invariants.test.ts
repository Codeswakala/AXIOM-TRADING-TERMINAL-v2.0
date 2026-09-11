import { describe, it, expect } from "vitest";
import { AI_DISCLAIMER_TEXT, SELF_DESCRIPTION_BANNER_TEXT } from "../workstation/ai/AssistantCommandSurface";
import { ASSISTANT_REFUSAL_REASON_CODES } from "./ui008_refusal_taxonomy.fixture";
import { ASSISTANT_DISCLOSURE_REGISTER } from "./ui008_disclosure_register.fixture";

describe("UI-008-P02 Security Invariants & Prohibitions (S-1, S-2, S-4)", () => {
  // S-1: Zero actuation controls invariant
  it("S-1: confirms zero order/buy/sell/execute/trade actuation controls in disclaimer and banner constants", () => {
    const combinedTexts = `${AI_DISCLAIMER_TEXT} ${SELF_DESCRIPTION_BANNER_TEXT}`;
    expect(combinedTexts).toContain("AXIOM does not act");
    expect(combinedTexts).toContain("no external LLM");
    expect(combinedTexts).not.toMatch(/execute trade|place order|submit order/i);
  });

  // S-2: Refusal taxonomy includes all 6 required constitutional reasons
  it("S-2: confirms refusal taxonomy covers all 6 refusal reasons including ASSISTANT_DISABLED", () => {
    expect(ASSISTANT_REFUSAL_REASON_CODES).toHaveLength(6);
    expect(ASSISTANT_REFUSAL_REASON_CODES).toContain("ORDER_INSTRUCTION_REFUSED");
    expect(ASSISTANT_REFUSAL_REASON_CODES).toContain("GATE_OPEN_INSTRUCTION_REFUSED");
    expect(ASSISTANT_REFUSAL_REASON_CODES).toContain("SECRET_EXFILTRATION_REFUSED");
    expect(ASSISTANT_REFUSAL_REASON_CODES).toContain("UNBOUNDED_TOOL_REQUEST_REFUSED");
    expect(ASSISTANT_REFUSAL_REASON_CODES).toContain("GROUNDING_REQUIRED");
    expect(ASSISTANT_REFUSAL_REASON_CODES).toContain("ASSISTANT_DISABLED");
  });

  // S-4: Disclosure register covers at least 18 items with honest severity
  it("S-4: confirms disclosure register fixtures provide full 18-item severity disclosures", () => {
    expect(ASSISTANT_DISCLOSURE_REGISTER.length).toBeGreaterThanOrEqual(18);
    for (const item of ASSISTANT_DISCLOSURE_REGISTER) {
      expect(item.id).toBeTruthy();
      expect(item.severityLabel).toBeTruthy();
      expect(item.sourcePin).toBeTruthy();
    }
  });
});
