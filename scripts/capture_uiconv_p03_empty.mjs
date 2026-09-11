import { chromium } from "../frontend/node_modules/playwright/index.mjs";
import fs from "fs";
import path from "path";

const EVIDENCE_DIR = "/home/user/axiom/docs/evidence/uiconv";

async function run() {
  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox", "--disable-setuid-sandbox"] });
  const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const page = await context.newPage();

  await page.goto("http://localhost:5173/login", { waitUntil: "networkidle" });
  await page.waitForTimeout(1000);
  await page.locator('input[data-testid="login-username-input"], input#username-input').first().fill("admin");
  await page.locator('input[data-testid="login-password-input"], input#password-input').first().fill("AxiomSecurePass2026!");
  await page.click('button[type="submit"]');
  await page.waitForTimeout(2500);

  // Genuine empty path: artifact-free database.
  await page.goto("http://localhost:5173/?panel=portfolio", { waitUntil: "networkidle" });
  await page.waitForTimeout(2000);
  const emptyState = await page.locator('[data-testid="portfolio-empty"]').count();
  const noAggMsg = await page.locator('text=No aggregate figures returned.').count();
  await page.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03_01_PORTFOLIO_EMPTY_STATE.png") });
  console.log(`[VERIFY] 01_PORTFOLIO_EMPTY: ${JSON.stringify({ url: page.url(), emptyState, noAggregateFiguresMessage: noAggMsg })}`);

  await page.goto("http://localhost:5173/?panel=scenarios", { waitUntil: "networkidle" });
  await page.waitForTimeout(2000);
  const cmpEmpty = await page.locator('[data-testid="scenario-comparison-empty"]').count();
  const dockEmpty = await page.locator('[data-testid="scenarios-empty"]').count();
  await page.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03_02_SCENARIOS_EMPTY_STATE.png") });
  console.log(`[VERIFY] 02_SCENARIOS_EMPTY: ${JSON.stringify({ url: page.url(), comparisonEmpty: cmpEmpty, dockEmpty })}`);

  await browser.close();
  console.log("EMPTY CAPTURE COMPLETE");
}

run().catch((err) => { console.error(err); process.exit(1); });
