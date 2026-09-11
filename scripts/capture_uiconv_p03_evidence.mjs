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
  const userField = page.locator('input[data-testid="login-username-input"], input#username-input').first();
  const passField = page.locator('input[data-testid="login-password-input"], input#password-input').first();
  await userField.fill("admin");
  await passField.fill("AxiomSecurePass2026!");
  await page.click('button[type="submit"]');
  await page.waitForTimeout(2500);

  // ============ PHASE A — EMPTY STATES (ITRGA A-4: the empty path is where honesty defects live) ============

  // A1: /?panel=portfolio with no dashboard data
  await page.goto("http://localhost:5173/?panel=portfolio", { waitUntil: "networkidle" });
  await page.waitForTimeout(1800);
  const portEmpty = await page.locator('[data-testid="portfolio-empty"]').count();
  const portPanel = await page.locator('[data-testid="portfolio-research-panel"]').count();
  const portTabSelected = await page.locator('[data-testid="bottom-tab-portfolio"]').getAttribute("aria-selected");
  await page.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03_01_PORTFOLIO_EMPTY_STATE.png") });
  await record("01_PORTFOLIO_EMPTY", {
    url: page.url(),
    portfolioPanel: portPanel,
    emptyStateVisible: portEmpty,
    tabSelected: portTabSelected,
  });

  // A2: /?panel=scenarios with zero persisted scenarios (comparison empty state)
  await page.goto("http://localhost:5173/?panel=scenarios", { waitUntil: "networkidle" });
  await page.waitForTimeout(1800);
  const scenEmpty = await page.locator('[data-testid="scenario-comparison-empty"]').count();
  const dockEmpty = await page.locator('[data-testid="scenarios-empty"]').count();
  await page.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03_02_SCENARIOS_EMPTY_STATE.png") });
  await record("02_SCENARIOS_EMPTY", {
    url: page.url(),
    comparisonEmptyVisible: scenEmpty,
    dockEmptyVisible: dockEmpty,
  });

  await browser.close();

  // ============ SEED (external process) ============
  console.log("Seeding P05 evidence data...");
  const { execSync } = await import("child_process");
  execSync(
    "cd /home/user/axiom/backend && .venv/bin/python ../scripts/seed_ui_p05_evidence.py",
    { stdio: "inherit" },
  );

  // ============ PHASE B — POPULATED STATES ============
  const browser2 = await chromium.launch({ headless: true, args: ["--no-sandbox", "--disable-setuid-sandbox"] });
  const context2 = await browser2.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const page2 = await context2.newPage();

  await page2.goto("http://localhost:5173/login", { waitUntil: "networkidle" });
  await page2.waitForTimeout(1000);
  await page2.locator('input[data-testid="login-username-input"], input#username-input').first().fill("admin");
  await page2.locator('input[data-testid="login-password-input"], input#password-input').first().fill("AxiomSecurePass2026!");
  await page2.click('button[type="submit"]');
  await page2.waitForTimeout(2500);

  // B1: /?panel=scenarios — populated dock + side-by-side comparison
  await page2.goto("http://localhost:5173/?panel=scenarios", { waitUntil: "networkidle" });
  await page2.waitForTimeout(2000);
  const scenarioCards = await page2.locator('[data-testid^="scenario-card-"]').count();
  const comparisonCards = await page2.locator('[data-testid^="scenario-comparison-card-"]').count();
  const pickerItems = await page2.locator('[data-testid^="scenario-picker-"]').count();
  await page2.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03_03_SCENARIOS_POPULATED_COMPARISON.png") });
  await record("03_SCENARIOS_POPULATED", {
    url: page2.url(),
    dockCards: scenarioCards,
    comparisonCards,
    pickerElements: pickerItems,
  });

  // B2: /?panel=portfolio — populated portfolio tab
  await page2.goto("http://localhost:5173/?panel=portfolio", { waitUntil: "networkidle" });
  await page2.waitForTimeout(2000);
  const aggCards = await page2.locator('[data-testid^="portfolio-metric-"]').count();
  const reportPreview = await page2.locator('[data-testid="portfolio-report-preview"]').count();
  const scope = await page2.locator('[data-testid="portfolio-included-scope"]').count();
  await page2.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03_04_PORTFOLIO_POPULATED.png") });
  await record("04_PORTFOLIO_POPULATED", {
    url: page2.url(),
    aggregateCards: aggCards,
    reportPreviewPresent: reportPreview,
    includedScopePresent: scope,
  });

  // B3: /?view=chart deep link (OBS-CONV2-7 discharge, visual)
  await page2.goto("http://localhost:5173/?view=chart", { waitUntil: "networkidle" });
  await page2.waitForTimeout(1800);
  const stageView = await page2.locator('[data-testid="trading-terminal-workspace"]').getAttribute("data-stage-view");
  const chartStage = await page2.locator('[data-testid="terminal-chart-stage"]').count();
  await page2.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03_05_VIEW_CHART_DEEP_LINK.png") });
  await record("05_VIEW_CHART", { url: page2.url(), stageView, chartStagePresent: chartStage });

  // B4: legacy /portfolio-research redirect → terminal PORTFOLIO tab
  await page2.goto("http://localhost:5173/portfolio-research", { waitUntil: "networkidle" });
  await page2.waitForTimeout(2000);
  const redirTab = await page2.locator('[data-testid="bottom-tab-portfolio"]').getAttribute("aria-selected");
  await page2.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03_06_PORTFOLIO_ROUTE_REDIRECT.png") });
  await record("06_PORTFOLIO_REDIRECT", { url: page2.url(), portfolioTabSelected: redirTab });

  // B5: legacy /compare-scenarios redirect → terminal SCENARIOS tab
  await page2.goto("http://localhost:5173/compare-scenarios", { waitUntil: "networkidle" });
  await page2.waitForTimeout(2000);
  const redirScenTab = await page2.locator('[data-testid="bottom-tab-scenarios"]').getAttribute("aria-selected");
  await page2.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03_07_SCENARIOS_ROUTE_REDIRECT.png") });
  await record("07_SCENARIOS_REDIRECT", { url: page2.url(), scenariosTabSelected: redirScenTab });

  await browser2.close();
  fs.writeFileSync(path.join(EVIDENCE_DIR, "UI-CONV-P03_CAPTURE_VERIFICATION.json"), JSON.stringify(LOG, null, 2));
  console.log("CAPTURE COMPLETE");
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
