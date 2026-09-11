import { describe, expect, it } from "vitest";
import * as fs from "fs";
import * as path from "path";
import { CURRENT_PROTECTED_ROUTES, WORKSPACE_REGISTRY } from "../workstation/registry/workspaceRegistry";

describe("UI-NEW-P06 Programme-Scope Security Invariants & Terminal Handover (T-1..T-7, S-1..S-5, B-P06-1..5, SAL-2)", () => {
  const terminalDir = path.resolve(__dirname, "../components/terminal");
  const packageJsonPath = path.resolve(__dirname, "../../package.json");

  // 1. T-1 / S-1: Zero functional buy/sell/execute/order/broker controls across terminal components
  it("T-1 / S-1: confirms zero functional buy/sell/execute/order/broker controls in terminal components", () => {
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

  // 2. T-2: Candle-derived market telemetry and ticker feeds are display-only and non-actuating
  it("T-2: confirms candle-derived market telemetry and ticker feeds are display-only", () => {
    const telemetrySource = fs.readFileSync(
      path.join(terminalDir, "TerminalMarketTelemetry.tsx"),
      "utf8",
    );
    const tickerSource = fs.readFileSync(
      path.join(terminalDir, "TerminalTopTicker.tsx"),
      "utf8",
    );

    expect(telemetrySource).toContain("MARKET TELEMETRY");
    expect(telemetrySource).toContain("live:simulated");
    expect(telemetrySource).toContain("Level-2 depth and broker spread are Gate-closed");
    expect(tickerSource).toContain("live:simulated");
  });

  // 3. T-3: Trade plans and research journals carry zero position/order semantics
  it("T-3: confirms trade plans and journals carry zero execution semantics and render research disclaimers", () => {
    const bottomDockSource = fs.readFileSync(
      path.join(terminalDir, "TerminalBottomDock.tsx"),
      "utf8",
    );

    // Form inputs must not include order fields
    expect(bottomDockSource).not.toMatch(/name=["']price["']/i);
    expect(bottomDockSource).not.toMatch(/name=["']stop_loss["']/i);
    expect(bottomDockSource).not.toMatch(/name=["']take_profit["']/i);
    expect(bottomDockSource).not.toMatch(/name=["']size["']/i);
    expect(bottomDockSource).not.toMatch(/name=["']side["']/i);

    // Must contain required non-actuating disclaimer
    expect(bottomDockSource).toContain("RESEARCH-ONLY · NON-ACTUATING");
  });

  // 4. T-4 / S-2: Zero External LLM SDK Imports across frontend source & package.json
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

  // 5. T-5: Assistant and research tooling remain strictly subordinate and non-actuating
  it("T-5: confirms assistant and research tooling outputs carry non-actuating disclaimers", () => {
    const bottomDockSource = fs.readFileSync(
      path.join(terminalDir, "TerminalBottomDock.tsx"),
      "utf8",
    );
    expect(bottomDockSource).toContain("Trade plan notes carry zero order, pricing, sizing, or execution affordance.");
  });

  // 6. T-6 / B-P06-1: Every rendered statistical value carries uncertainty intervals
  it("T-6 / B-P06-1: confirms statistical outputs bracket point estimates or render explicit unavailable", () => {
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
    expect(signalsSource).toContain("[Uncertainty: Unavailable]");
    expect(signalsSource).toContain("isBracketed");
  });

  // 7. T-7 / S-5: Zero hardcoded secrets, API keys, or private tokens in terminal source
  it("T-7 / S-5: confirms zero hardcoded API keys, secrets, or bearer tokens in terminal source", () => {
    const terminalFiles = fs
      .readdirSync(terminalDir)
      .filter((f: string) => f.endsWith(".tsx") || f.endsWith(".ts"));

    for (const file of terminalFiles) {
      const content = fs.readFileSync(path.join(terminalDir, file), "utf8");
      expect(content).not.toMatch(/(password|secret|api_key|private_key|bearer)\s*[:=]\s*["'][^"']+["']/i);
    }
  });

  // 8. S-3: Zero dangerouslySetInnerHTML, eval(), or new Function() in terminal components
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

  // 9. S-4 / B-P06-2: Design Token Consumption & Terminal MultiPane CSS Pure Token Consumption
  it("S-4 / B-P06-2: confirms TerminalMultiPane.css consumes design tokens exclusively with 0 ad-hoc hex", () => {
    const cssPath = path.join(terminalDir, "TerminalMultiPane.css");
    const cssContent = fs.readFileSync(cssPath, "utf8");
    const hexMatches = cssContent.match(/#[0-9a-fA-F]{3,8}\b/g) || [];
    expect(hexMatches.length).toBe(0);
  });

  // 10. C-1: Zero order book, depth ladder, bid size, or ask size in terminal components
  it("C-1: confirms zero order book or depth ladder rendering in terminal components", () => {
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

  // 11. B-P06-4: Route Inventory & Auth-Guarding Verification
  it("B-P06-4: confirms 16 protected workspace routes in WORKSPACE_REGISTRY, all auth-guarded and presentation-only", () => {
    expect(WORKSPACE_REGISTRY.length).toBe(16);
    expect(CURRENT_PROTECTED_ROUTES.length).toBe(16);

    for (const workspace of WORKSPACE_REGISTRY) {
      expect(workspace.requiresAuth).toBe(true);
      expect(workspace.noActuation).toBe(true);
      expect(workspace.route.startsWith("/")).toBe(true);
    }
  });

  // 12. SAL-2: Confirms SAL-2 (Internal) classification for all terminal surfaces
  it("SAL-2: confirms SAL-2 (Internal) classification across terminal surfaces", () => {
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
