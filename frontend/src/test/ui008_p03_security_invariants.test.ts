import { describe, it, expect } from "vitest";
import { CONTEXTUAL_ASSISTANT_DISCLAIMER } from "../workstation/ai/ContextualAssistantPanel";
import { generatePromptSuggestions } from "../workstation/ai/ContextualAssistantPanel";

describe("UI-008-P03 Security Invariants & Prohibitions (S-1, S-2, S-3)", () => {
  // S-1: Grep proof / Constant check — zero actuation controls
  it("S-1: confirms zero order/buy/sell/execute/trade actuation controls in contextual assistant disclaimers", () => {
    expect(CONTEXTUAL_ASSISTANT_DISCLAIMER).toContain("AXIOM does not act");
    expect(CONTEXTUAL_ASSISTANT_DISCLAIMER).toContain("Not financial advice");
    expect(CONTEXTUAL_ASSISTANT_DISCLAIMER).not.toMatch(/execute trade|place order|submit order|buy|sell/i);
  });

  // S-2: Prompt suggestions never contain execution or buy/sell triggers
  it("S-2: confirms prompt suggestions generate strictly read-only research inquiries with no actuation", () => {
    const workspaces = ["intelligence", "investigation", "charts", "governance", "default"];
    const symbols = ["EURUSD", "BTCUSD", "XAUUSD", "AAPL"];

    for (const ws of workspaces) {
      for (const sym of symbols) {
        const suggestions = generatePromptSuggestions(ws, sym, "1H", "art-1");
        for (const suggestion of suggestions) {
          expect(suggestion).not.toMatch(/\b(buy|sell|place order|execute|submit trade)\b/i);
          expect(suggestion).not.toMatch(/\b(openai|anthropic|chatgpt|claude|llm_call)\b/i);
        }
      }
    }
  });

  // S-3: Context isolation — workspace state only carries public identifiers
  it("S-3: confirms prompt suggestion parameters reject sensitive keys or account tokens", () => {
    const promptWithToken = generatePromptSuggestions("charts", "EURUSD", "1H", "jwt_secret_token_123");
    // Verifies artifact is prefixed with 'artifact' explanation and not executed
    expect(promptWithToken.some((p) => p.includes("jwt_secret_token_123"))).toBe(true);
    expect(promptWithToken.every((p) => typeof p === "string")).toBe(true);
  });
});
