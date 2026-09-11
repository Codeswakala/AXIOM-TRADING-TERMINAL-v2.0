import { describe, it, expect } from "vitest";
import { DOC_LOOKUP_DISCLAIMER } from "../workstation/ai/DocumentationLookupSurface";
import { PLATFORM_DOCUMENTATION_INDEX } from "../workstation/ai/documentationIndex";

describe("UI-008-P05 Security Invariants & Prohibitions (S-1, S-2, S-3)", () => {
  // S-1: Zero actuation controls in documentation surface
  it("S-1: confirms zero order/buy/sell/execute/trade actuation controls in doc lookup disclaimers", () => {
    expect(DOC_LOOKUP_DISCLAIMER).toContain("AXIOM does not act");
    expect(DOC_LOOKUP_DISCLAIMER).toContain("Not financial advice");
    expect(DOC_LOOKUP_DISCLAIMER).not.toMatch(/\b(buy|sell|place order|execute trade|submit order)\b/i);
  });

  // S-2: No external LLM calls or web browsing in documentation index
  it("S-2: confirms documentation index contains strictly static text with zero external API endpoints", () => {
    for (const doc of PLATFORM_DOCUMENTATION_INDEX) {
      expect(doc.contentMarkdown).not.toMatch(/https?:\/\/api\.openai\.com/i);
      expect(doc.contentMarkdown).not.toMatch(/https?:\/\/api\.anthropic\.com/i);
      expect(doc.contentMarkdown).not.toMatch(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/i);
    }
  });

  // S-3: Sandboxed markdown safety — no raw HTML script tags
  it("S-3: confirms static index contains no raw executable script tags or eval statements", () => {
    const rawIndexString = JSON.stringify(PLATFORM_DOCUMENTATION_INDEX);
    expect(rawIndexString).not.toContain("<script>");
    expect(rawIndexString).not.toContain("javascript:");
    expect(rawIndexString).not.toContain("eval(");
  });
});
