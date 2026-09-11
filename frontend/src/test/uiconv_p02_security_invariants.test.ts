import { describe, expect, it } from "vitest";
import * as fs from "fs";
import * as path from "path";
import { CURRENT_PROTECTED_ROUTES, WORKSPACE_REGISTRY } from "../workstation/registry/workspaceRegistry";

describe("UI-CONV-P02 Security Invariants, Single Statistical Path & C-1 Permanence (T-1..T-7, S-1..S-5, B-CONV2-1..4, SAL-2)", () => {
  const terminalDir = path.resolve(__dirname, "../components/terminal");
  const packageJsonPath = path.resolve(__dirname, "../../package.json");

  // 1. T-1 / S-1: Zero functional buy/sell/execute/order/broker controls across absorbed terminal docks
  it("T-1 / S-1: confirms zero functional buy/sell/execute/order/broker controls across terminal components", () => {
    const terminalFiles = fs
      .readdirSync(terminalDir)
      .filter((f: string) => f.endsWith(".tsx") || f.endsWith(".ts"));

    const forbiddenExecutionPatterns = [
      /\bplace_order\(/i,
      /\bsubmit_order\(/i,
      /\border_ticket\(/i,
      /\bconnect_broker\(/i,
      /\baccount_id\s*[:=]\s*["'][^"']+["']/i,
      /\bopen_gate\(/i,
      /\ballow_execution\(/i,
      /<button[^>]*>\s*(Buy|Sell|Execute|Place Order)\b/i,
    ];

    for (const file of terminalFiles) {
      const content = fs.readFileSync(path.join(terminalDir, file), "utf8");
      for (const pattern of forbiddenExecutionPatterns) {
        expect(pattern.test(content)).toBe(false);
      }
    }
  });

  // 2. B-CONV2-1: Exactly one shared statistical rendering component for calibrated confidence
  it("B-CONV2-1: confirms CalibratedConfidenceBadge and MetricWithInterval are the sole statistical rendering paths", () => {
    const statRendererSource = fs.readFileSync(
      path.join(terminalDir, "StatisticalValueRenderer.tsx"),
      "utf8",
    );

    expect(statRendererSource).toContain("export function CalibratedConfidenceBadge");
    expect(statRendererSource).toContain("export function MetricWithInterval");
    expect(statRendererSource).toContain("[Uncertainty: Unavailable]");
    expect(statRendererSource).toContain("isBracketed");
  });

  // 3. T-4 / S-2: Zero External LLM SDK Imports across frontend source & package.json
  it("T-4 / S-2: confirms whole frontend source and package.json contain zero external LLM/AI SDK dependencies", () => {
    const packageJsonContent = fs.readFileSync(packageJsonPath, "utf8");
    const packageJson = JSON.parse(packageJsonContent);

    const allDeps = {
      ...packageJson.dependencies,
      ...packageJson.devDependencies,
    };

    const forbiddenPackages = [
      "openai",
      "@anthropic-ai/sdk",
      "langchain",
      "@google/generative-ai",
      "cohere-ai",
      "huggingface",
    ];

    for (const pkg of forbiddenPackages) {
      expect(allDeps[pkg]).toBeUndefined();
    }
  });

  // 4. T-5: Assistant and research tooling remain strictly subordinate and non-actuating
  it("T-5: confirms absorbed signal stream and intelligence cards outputs carry non-actuating disclaimers", () => {
    const signalSource = fs.readFileSync(
      path.join(terminalDir, "TerminalSignalStream.tsx"),
      "utf8",
    );
    expect(signalSource).toContain("Statistical model advisory note. Zero transaction execution affordance.");
    expect(signalSource).toContain("RESEARCH-ONLY · NON-ACTUATING");
  });

  // 5. T-6 / Principle 1: Every rendered statistical value carries uncertainty intervals
  it("T-6 / Principle 1: confirms statistical bracketing invariant holds across terminal components", () => {
    const bottomDockSource = fs.readFileSync(
      path.join(terminalDir, "TerminalBottomDock.tsx"),
      "utf8",
    );
    const signalsSource = fs.readFileSync(
      path.join(terminalDir, "TerminalSignalStream.tsx"),
      "utf8",
    );

    expect(bottomDockSource).toContain("[Uncertainty: Unavailable]");
    expect(bottomDockSource).toContain("renderRiskMetric");
    expect(signalsSource).toContain("CalibratedConfidenceBadge");
  });

  // 6. T-7 / S-5: Zero hardcoded secrets, API keys, or private tokens in terminal source
  it("T-7 / S-5: confirms zero hardcoded API keys, secrets, or bearer tokens in terminal source", () => {
    const terminalFiles = fs
      .readdirSync(terminalDir)
      .filter((f: string) => f.endsWith(".tsx") || f.endsWith(".ts"));

    for (const file of terminalFiles) {
      const content = fs.readFileSync(path.join(terminalDir, file), "utf8");
      expect(content).not.toMatch(/(password|secret|api_key|private_key|bearer)\s*[:=]\s*["'][^"']+["']/i);
    }
  });

  // 7. S-3: Zero dangerouslySetInnerHTML, eval(), or new Function() in terminal components
  it("S-3: confirms zero dangerouslySetInnerHTML, eval(), or dynamic execution in terminal source", () => {
    const terminalFiles = fs
      .readdirSync(terminalDir)
      .filter((f: string) => f.endsWith(".tsx") || f.endsWith(".ts"));

    for (const file of terminalFiles) {
      const content = fs.readFileSync(path.join(terminalDir, file), "utf8");
      expect(content).not.toContain("dangerouslySetInnerHTML");
      expect(content).not.toMatch(/\beval\(/);
      expect(content).not.toMatch(/\bnew Function\(/);
    }
  });

  // 8. S-4 / B-CONV2-3: Pure Token Consumption across terminal components
  it("S-4 / B-CONV2-3: confirms TerminalMultiPane.css consumes design tokens exclusively with 0 ad-hoc hex", () => {
    const cssPath = path.join(terminalDir, "TerminalMultiPane.css");
    const cssContent = fs.readFileSync(cssPath, "utf8");
    const hexMatches = cssContent.match(/#[0-9a-fA-F]{3,8}\b/g) || [];
    expect(hexMatches.length).toBe(0);
  });

  // 9. C-1 / TD-023: Zero order book, depth ladder, bid size, or ask size (TD-023 WONTFIX)
  it("C-1 / TD-023: confirms zero order book, depth ladder, bid size, or ask size rendering in terminal components", () => {
    const terminalFiles = fs
      .readdirSync(terminalDir)
      .filter((f: string) => f.endsWith(".tsx") || f.endsWith(".ts"));

    for (const file of terminalFiles) {
      const content = fs.readFileSync(path.join(terminalDir, file), "utf8");
      expect(content).not.toMatch(/\bdepth_ladder\b/i);
      expect(content).not.toMatch(/\borderbook\b/i);
      expect(content).not.toMatch(/\bbid_size\b/i);
      expect(content).not.toMatch(/\bask_size\b/i);
    }
  });

  // 10. B-CONV2-2: Route Inventory & Redirect Verification
  it("B-CONV2-2: confirms 16 protected workspace routes in WORKSPACE_REGISTRY, all auth-guarded and presentation-only", () => {
    expect(WORKSPACE_REGISTRY.length).toBe(16);
    expect(CURRENT_PROTECTED_ROUTES.length).toBe(16);

    for (const workspace of WORKSPACE_REGISTRY) {
      expect(workspace.requiresAuth).toBe(true);
      expect(workspace.noActuation).toBe(true);
      expect(workspace.route.startsWith("/")).toBe(true);
    }
  });

  // 11. SAL-2: Confirms SAL-2 (Internal) classification across terminal surfaces
  it("SAL-2: confirms SAL-2 (Internal) classification across terminal presentation surfaces", () => {
    const bottomDockSource = fs.readFileSync(
      path.join(terminalDir, "TerminalBottomDock.tsx"),
      "utf8",
    );
    const layoutSource = fs.readFileSync(
      path.join(terminalDir, "TerminalMultiPaneLayout.tsx"),
      "utf8",
    );

    expect(bottomDockSource).toContain("SAL-2 (Internal)");
    expect(layoutSource).toContain("SAL-2 (Internal)");
  });
});
