import { describe, expect, it } from "vitest";
import * as fs from "fs";
import * as path from "path";

describe("UI-NEW-P05 Security Invariants & Risk/Journal Boundary (T-1..T-7, B-P05-1..5, SAL-2)", () => {
  const terminalDir = path.resolve(__dirname, "../components/terminal");
  const terminalFiles = fs
    .readdirSync(terminalDir)
    .filter((f: string) => f.endsWith(".tsx") || f.endsWith(".ts"));

  // 1. T-1 / S-1: Zero buy/sell/execute/order/broker controls in Terminal Bottom Dock
  it("T-1 / S-1: confirms zero buy/sell/execute/order/broker controls in Bottom Dock", () => {
    const bottomDockSource = fs.readFileSync(
      path.join(terminalDir, "TerminalBottomDock.tsx"),
      "utf8",
    );

    const forbiddenFunctionalTerms = [
      /\bplace_order\b/i,
      /\bsubmit_order\b/i,
      /\border_ticket\b/i,
      /\bconnect-broker\b/i,
      /\baccount_id\b/i,
      /\bposition_size\b/i,
      /\bopen_gate\b/i,
      /\ballow_execution\b/i,
    ];

    for (const pattern of forbiddenFunctionalTerms) {
      expect(pattern.test(bottomDockSource)).toBe(false);
    }
  });

  // 2. B-P05-1: Trade Plan Form Exposes No Position / Order Fields
  it("B-P05-1: confirms trade plan forms and models carry zero position or execution semantics", () => {
    const bottomDockSource = fs.readFileSync(
      path.join(terminalDir, "TerminalBottomDock.tsx"),
      "utf8",
    );

    const forbiddenInputNames = [
      /name=["']price["']/i,
      /name=["']stop_loss["']/i,
      /name=["']take_profit["']/i,
      /name=["']lot["']/i,
      /name=["']size["']/i,
      /name=["']side["']/i,
      /name=["']account["']/i,
    ];

    for (const pattern of forbiddenInputNames) {
      expect(pattern.test(bottomDockSource)).toBe(false);
    }
  });

  // 3. T-4 / S-2: Zero External AI SDK Imports in Terminal Module
  it("T-4 / S-2: confirms Bottom Dock and terminal module contain zero external AI SDK dependencies", () => {
    const forbiddenAiTokens = [
      /openai/i,
      /anthropic/i,
      /langchain/i,
      /api\.openai/i,
      /remote_prompt/i,
    ];

    for (const file of terminalFiles) {
      const content = fs.readFileSync(path.join(terminalDir, file), "utf8");
      for (const token of forbiddenAiTokens) {
        expect(token.test(content)).toBe(false);
      }
    }
  });

  // 4. T-5: All Planning and Journaling outputs framed as non-actuating research notes
  it("T-5: confirms all planning and journal outputs are framed as non-actuating research notes", () => {
    const bottomDockSource = fs.readFileSync(
      path.join(terminalDir, "TerminalBottomDock.tsx"),
      "utf8",
    );

    expect(bottomDockSource).toContain("RESEARCH-ONLY · NON-ACTUATING");
    expect(bottomDockSource).toContain("research_disclaimer");
  });

  // 5. T-6 / B-P05-2: Every risk metric is bound to uncertainty or explicit unavailable
  it("T-6 / B-P05-2: confirms risk metrics render with uncertainty intervals and server assumptions", () => {
    const bottomDockSource = fs.readFileSync(
      path.join(terminalDir, "TerminalBottomDock.tsx"),
      "utf8",
    );

    expect(bottomDockSource).toContain("renderRiskMetric");
    expect(bottomDockSource).toContain("[Uncertainty: Unavailable]");
    expect(bottomDockSource).toContain("assumptions");
  });

  // 6. S-3: Zero Dynamic DOM Injection or eval in Bottom Dock
  it("S-3: confirms Bottom Dock contains zero dynamic DOM injection or runtime code execution", () => {
    for (const file of terminalFiles) {
      const content = fs.readFileSync(path.join(terminalDir, file), "utf8");
      expect(content).not.toContain("dangerouslySetInnerHTML");
      expect(content).not.toMatch(/\beval\(/);
      expect(content).not.toMatch(/\bnew Function\(/);
    }
  });

  // 7. S-4: Pure Token Consumption (0 ad-hoc hex in TerminalMultiPane.css)
  it("S-4: confirms terminal styling consumes design tokens exclusively without ad-hoc hex", () => {
    const cssPath = path.join(terminalDir, "TerminalMultiPane.css");
    const cssContent = fs.readFileSync(cssPath, "utf8");
    const hexMatches = cssContent.match(/#[0-9a-fA-F]{3,8}\b/g) || [];
    expect(hexMatches.length).toBe(0);
  });

  // 8. T-7 / S-5: Zero Hardcoded API Keys or Secrets
  it("T-7 / S-5: confirms zero hardcoded API keys, tokens, or credentials in terminal source", () => {
    for (const file of terminalFiles) {
      const content = fs.readFileSync(path.join(terminalDir, file), "utf8");
      expect(content).not.toMatch(/(password|secret|api_key|private_key|bearer)\s*[:=]\s*["'][^"']+["']/i);
    }
  });

  // 9. C-1: Zero Order Book / Depth Ladder Rendering in Bottom Dock
  it("C-1: confirms zero order book, depth ladder, bid size, or ask size rendering in Bottom Dock", () => {
    const bottomDockSource = fs.readFileSync(
      path.join(terminalDir, "TerminalBottomDock.tsx"),
      "utf8",
    );

    expect(bottomDockSource).not.toMatch(/depth.?ladder/i);
    expect(bottomDockSource).not.toMatch(/order.?book/i);
    expect(bottomDockSource).not.toMatch(/\bbid_size\b/i);
    expect(bottomDockSource).not.toMatch(/\bask_size\b/i);
  });

  // 10. B-P05-SAL: Confirms SAL-2 (Internal) classification for Bottom Dock
  it("B-P05-SAL: confirms SAL-2 (Internal) classification for Bottom Dock presentation surfaces", () => {
    const bottomDockSource = fs.readFileSync(
      path.join(terminalDir, "TerminalBottomDock.tsx"),
      "utf8",
    );

    expect(bottomDockSource).toContain("SAL-2 (Internal)");
  });
});
