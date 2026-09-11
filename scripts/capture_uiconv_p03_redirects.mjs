import { chromium } from "../frontend/node_modules/playwright/index.mjs";
import fs from "fs";
import path from "path";
const EVIDENCE_DIR = "/home/user/axiom/docs/evidence/uiconv";
const LOG = [];

async function record(label, data) {
  LOG.push({ label, ...data });
  console.log(`[VERIFY] ${label}: ${JSON.stringify(data)}`);
}

const browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
const page = await context.newPage();
await page.goto("http://localhost:5173/login", { waitUntil: "networkidle" });
await page.waitForTimeout(800);
await page.locator('input[data-testid="login-username-input"], input#username-input').first().fill("admin");
await page.locator('input[data-testid="login-password-input"], input#password-input').first().fill("AxiomSecurePass2026!");
await page.click('button[type="submit"]');
await page.waitForTimeout(2500);

await page.goto("http://localhost:5173/portfolio-research", { waitUntil: "domcontentloaded" });
await page.waitForTimeout(3500);
const portTab = await page.locator('[data-testid="bottom-tab-portfolio"]').getAttribute("aria-selected");
const portPanel = await page.locator('[data-testid="portfolio-research-panel"]').count();
await page.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03_06_PORTFOLIO_ROUTE_REDIRECT.png") });
await record("06_PORTFOLIO_REDIRECT", { url: page.url(), portfolioTabSelected: portTab, panelPresent: portPanel });

await page.goto("http://localhost:5173/compare-scenarios", { waitUntil: "domcontentloaded" });
await page.waitForTimeout(3500);
const scenTab = await page.locator('[data-testid="bottom-tab-scenarios"]').getAttribute("aria-selected");
const cmpPanel = await page.locator('[data-testid="scenario-comparison-panel"]').count();
await page.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03_07_SCENARIOS_ROUTE_REDIRECT.png") });
await record("07_SCENARIOS_REDIRECT", { url: page.url(), scenariosTabSelected: scenTab, comparisonPanelPresent: cmpPanel });

await browser.close();

// Merge with existing verification record (03-05 from the populated run).
const existing = JSON.parse(fs.readFileSync(path.join(EVIDENCE_DIR, "UI-CONV-P03_CAPTURE_VERIFICATION.json"), "utf8"));
const merged = [...existing.filter((e) => !["06_PORTFOLIO_REDIRECT", "07_SCENARIOS_REDIRECT"].includes(e.label)), ...LOG];
fs.writeFileSync(path.join(EVIDENCE_DIR, "UI-CONV-P03_CAPTURE_VERIFICATION.json"), JSON.stringify(merged, null, 2));
console.log("REDIRECT CAPTURES COMPLETE");
