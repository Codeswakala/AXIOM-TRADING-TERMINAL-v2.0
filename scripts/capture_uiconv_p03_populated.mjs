import { chromium } from "../frontend/node_modules/playwright/index.mjs";
import fs from "fs";
import path from "path";

const EVIDENCE_DIR = "/home/user/axiom/docs/evidence/uiconv";
const LOG = [];

async function record(label, data) {
  const entry = { label, ...data };
  LOG.push(entry);
  console.log(`[VERIFY] ${label}: ${JSON.stringify(data)}`);
}

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

  // 03: populated scenarios — dock cards + side-by-side comparison (two scenarios)
  await page.goto("http://localhost:5173/?panel=scenarios", { waitUntil: "networkidle" });
  await page.waitForTimeout(2200);
  const dockCards = await page.locator('[data-testid^="scenario-card-"]').count();
  const comparisonCards = await page.locator('[data-testid^="scenario-comparison-card-"]').count();
  const pickerCheckboxes = await page.locator('[data-testid^="scenario-picker-checkbox-"]').count();
  await page.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03_03_SCENARIOS_POPULATED_COMPARISON.png") });
  await record("03_SCENARIOS_POPULATED", {
    url: page.url(),
    dockCards,
    comparisonCards,
    pickerCheckboxes,
  });

  // 04: populated portfolio tab
  await page.goto("http://localhost:5173/?panel=portfolio", { waitUntil: "networkidle" });
  await page.waitForTimeout(2200);
  const aggCards = await page.locator('[data-testid^="portfolio-metric-"]').count();
  const reportPreview = await page.locator('[data-testid="portfolio-report-preview"]').count();
  const scope = await page.locator('[data-testid="portfolio-included-scope"]').count();
  await page.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03_04_PORTFOLIO_POPULATED.png") });
  await record("04_PORTFOLIO_POPULATED", {
    url: page.url(),
    aggregateCards: aggCards,
    reportPreviewPresent: reportPreview,
    includedScopePresent: scope,
  });

  // 05: /?view=chart deep link (OBS-CONV2-7 discharge, visual)
  await page.goto("http://localhost:5173/?view=chart", { waitUntil: "networkidle" });
  await page.waitForTimeout(1800);
  const stageView = await page.locator('[data-testid="trading-terminal-workspace"]').getAttribute("data-stage-view");
  const chartStage = await page.locator('[data-testid="terminal-chart-stage"]').count();
  await page.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03_05_VIEW_CHART_DEEP_LINK.png") });
  await record("05_VIEW_CHART", { url: page.url(), stageView, chartStagePresent: chartStage });

  // 06: legacy /portfolio-research redirect
  await page.goto("http://localhost:5173/portfolio-research", { waitUntil: "networkidle" });
  await page.waitForTimeout(2200);
  const redirTab = await page.locator('[data-testid="bottom-tab-portfolio"]').getAttribute("aria-selected");
  await page.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03_06_PORTFOLIO_ROUTE_REDIRECT.png") });
  await record("06_PORTFOLIO_REDIRECT", { url: page.url(), portfolioTabSelected: redirTab });

  // 07: legacy /compare-scenarios redirect
  await page.goto("http://localhost:5173/compare-scenarios", { waitUntil: "networkidle" });
  await page.waitForTimeout(2200);
  const redirScenTab = await page.locator('[data-testid="bottom-tab-scenarios"]').getAttribute("aria-selected");
  await page.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03_07_SCENARIOS_ROUTE_REDIRECT.png") });
  await record("07_SCENARIOS_REDIRECT", { url: page.url(), scenariosTabSelected: redirScenTab });

  await browser.close();
  fs.writeFileSync(path.join(EVIDENCE_DIR, "UI-CONV-P03_CAPTURE_VERIFICATION.json"), JSON.stringify(LOG, null, 2));
  console.log("POPULATED CAPTURE COMPLETE");
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
