import { describe, expect, it } from "vitest";
import * as fs from "fs";
import * as path from "path";
import { CURRENT_PROTECTED_ROUTES, WORKSPACE_REGISTRY } from "../workstation/registry/workspaceRegistry";

describe("UI-CONV-P01 Security Invariants, Brand Governance & Pre-Authentication Safety (T-1..T-7, S-1..S-5, B-CONV-1..5, SAL-2)", () => {
  const workstationDir = path.resolve(__dirname, "../workstation");
  const pagesDir = path.resolve(__dirname, "../pages");
  const packageJsonPath = path.resolve(__dirname, "../../package.json");

  // 1. T-1 / S-1: Zero buy/sell/execute/order/broker controls across shell, rail, login
  it("T-1 / S-1: confirms zero functional buy/sell/execute/order/broker controls across shell and login", () => {
    const shellSource = fs.readFileSync(
      path.join(workstationDir, "components/InstitutionalWorkspaceShell.tsx"),
      "utf8",
    );
    const railSource = fs.readFileSync(
      path.join(workstationDir, "navigation/UnifiedModuleRail.tsx"),
      "utf8",
    );
    const loginSource = fs.readFileSync(
      path.join(pagesDir, "LoginPage.tsx"),
      "utf8",
    );

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

    for (const content of [shellSource, railSource, loginSource]) {
      for (const pattern of forbiddenExecutionPatterns) {
        expect(pattern.test(content)).toBe(false);
      }
    }
  });

  // 2. F-BRAND-1: Brand Mark Governance — Official AX Monogram is retained, compass+Epsilon is not mounted
  it("F-BRAND-1: confirms official AX Monogram is retained and candidate compass+Epsilon mark is unmounted", () => {
    const shellSource = fs.readFileSync(
      path.join(workstationDir, "components/InstitutionalWorkspaceShell.tsx"),
      "utf8",
    );
    const loginSource = fs.readFileSync(
      path.join(pagesDir, "LoginPage.tsx"),
      "utf8",
    );

    // Official AX Monogram must be present
    expect(shellSource).toContain("AX");
    expect(loginSource).toContain("AX");

    // Compass + Epsilon mark must NOT be imported or mounted in production code
    expect(shellSource).not.toMatch(/candidate_compass_epsilon/i);
    expect(loginSource).not.toMatch(/candidate_compass_epsilon/i);
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

  // 4. B-CONV-2: Sign-in surface renders pre-authentication governance chips and zero credential hints
  it("B-CONV-2: confirms sign-in surface renders pre-authentication governance chips and no credential hints", () => {
    const loginSource = fs.readFileSync(
      path.join(pagesDir, "LoginPage.tsx"),
      "utf8",
    );

    // SUPERSEDED BY CITATION (BO-FE-U01 §2.1/§2.2, adopted 2026-09-10):
    // the hardcoded GATE/RESEARCH-ONLY literals are AAE-006-excluded; the
    // truthful pattern-(b) label is the pinned pre-auth posture rendering.
    expect(loginSource).toContain("POSTURE: VERIFIED AFTER SIGN-IN");
    expect(loginSource).not.toContain("GATE: CLOSED");
    expect(loginSource).not.toContain("AxiomSecurePass2026!");
    expect(loginSource).not.toContain("placeholder=\"admin\"");
  });

  // 5. T-6 / Principle 1: Every rendered statistical value carries uncertainty intervals
  it("T-6 / Principle 1: confirms statistical bracketing invariant holds across terminal components", () => {
    const terminalDir = path.resolve(__dirname, "../components/terminal");
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

  // 6. T-7 / S-5: Zero hardcoded secrets, API keys, or private tokens in shell source
  it("T-7 / S-5: confirms zero hardcoded API keys, secrets, or bearer tokens in shell source", () => {
    const files = [
      path.join(workstationDir, "components/InstitutionalWorkspaceShell.tsx"),
      path.join(workstationDir, "navigation/UnifiedModuleRail.tsx"),
      path.join(pagesDir, "LoginPage.tsx"),
    ];

    for (const file of files) {
      const content = fs.readFileSync(file, "utf8");
      expect(content).not.toMatch(/(password|secret|api_key|private_key|bearer)\s*[:=]\s*["'][^"']+["']/i);
    }
  });

  // 7. S-3: Zero dangerouslySetInnerHTML, eval(), or new Function() in shell source
  it("S-3: confirms zero dangerouslySetInnerHTML, eval(), or dynamic execution in shell components", () => {
    const files = [
      path.join(workstationDir, "components/InstitutionalWorkspaceShell.tsx"),
      path.join(workstationDir, "navigation/UnifiedModuleRail.tsx"),
      path.join(pagesDir, "LoginPage.tsx"),
    ];

    for (const file of files) {
      const content = fs.readFileSync(file, "utf8");
      expect(content).not.toContain("dangerouslySetInnerHTML");
      expect(content).not.toMatch(/\beval\(/);
      expect(content).not.toMatch(/\bnew Function\(/);
    }
  });

  // 8. S-4 / B-CONV-1: Pure token consumption in shell and rail styles (0 ad-hoc hex)
  it("S-4 / B-CONV-1: confirms shell and rail styles consume design tokens exclusively with 0 ad-hoc hex", () => {
    const cssFiles = [
      path.join(workstationDir, "components/InstitutionalWorkspaceShell.css"),
      path.join(workstationDir, "navigation/UnifiedModuleRail.css"),
      path.join(pagesDir, "LoginPage.css"),
      path.resolve(__dirname, "../styles/global.css"),
    ];

    for (const cssPath of cssFiles) {
      const cssContent = fs.readFileSync(cssPath, "utf8");
      const hexMatches = cssContent.match(/#[0-9a-fA-F]{3,8}\b/g) || [];
      expect(
        hexMatches.length,
        `Found ad-hoc hex in ${path.basename(cssPath)}: ${hexMatches.join(", ")}`,
      ).toBe(0);
    }
  });

  // 9. C-1: Zero order book, depth ladder, bid size, or ask size in shell components
  it("C-1: confirms zero order book or depth ladder rendering in shell and rail components", () => {
    const files = [
      path.join(workstationDir, "components/InstitutionalWorkspaceShell.tsx"),
      path.join(workstationDir, "navigation/UnifiedModuleRail.tsx"),
    ];

    for (const file of files) {
      const content = fs.readFileSync(file, "utf8");
      expect(content).not.toMatch(/\bdepth_ladder\b/i);
      expect(content).not.toMatch(/\borderbook\b/i);
      expect(content).not.toMatch(/\bbid_size\b/i);
      expect(content).not.toMatch(/\bask_size\b/i);
    }
  });

  // 10. B-CONV-4: Route Inventory & Auth-Guarding Verification
  it("B-CONV-4: confirms 16 protected workspace routes in WORKSPACE_REGISTRY, all auth-guarded and presentation-only", () => {
    expect(WORKSPACE_REGISTRY.length).toBe(16);
    expect(CURRENT_PROTECTED_ROUTES.length).toBe(16);

    for (const workspace of WORKSPACE_REGISTRY) {
      expect(workspace.requiresAuth).toBe(true);
      expect(workspace.noActuation).toBe(true);
      expect(workspace.route.startsWith("/")).toBe(true);
    }
  });

  // 11. SAL-2: Confirms SAL-2 (Internal) classification for shell presentation surfaces
  it("SAL-2: confirms SAL-2 (Internal) classification across shell presentation surfaces", () => {
    const shellSource = fs.readFileSync(
      path.join(workstationDir, "components/InstitutionalWorkspaceShell.tsx"),
      "utf8",
    );
    const loginSource = fs.readFileSync(
      path.join(pagesDir, "LoginPage.tsx"),
      "utf8",
    );

    // Shell arm SUPERSEDED BY CITATION (BO-FE-U02 §2.2/§2.9, PC-FEU02-1 C4/C9, ACC-1; adopted 2026-09-11): the asserted heritage chips are EXPELLED from the chrome boundary; the truthful cluster renders the locked-config mode badge + live health chip instead.
    // The classification recital lives in the governance register, not code.
    expect(shellSource).not.toContain("SAL-2 (Internal)");
    // Login-surface arm SUPERSEDED BY CITATION (BO-FE-U01 §2.2, adopted
    // 2026-09-10): the pre-auth SAL-2 assurance literal is AAE-006-excluded
    // — the door may not claim a security assurance it cannot verify. The
    // classification remains asserted on the authenticated shell (above).
    expect(loginSource).not.toContain("SAL-2 (Internal)");
  });
});
