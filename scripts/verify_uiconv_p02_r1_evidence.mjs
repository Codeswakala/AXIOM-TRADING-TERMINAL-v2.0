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
  await page.goto("http://localhost:5173/", { waitUntil: "networkidle" });
  await page.waitForTimeout(1500);

  // ---- Capture 1: palette top ----
  await page.keyboard.press("Control+k");
  await page.waitForTimeout(800);
  const items1 = await page.locator('.ix-command-item[role="menuitem"]').count();
  const groups1 = await page.locator(".ix-command-group").count();
  const listBox1 = await page.locator(".ix-command-list").first().evaluate((el) => ({
    scrollTop: el.scrollTop,
    scrollHeight: el.scrollHeight,
    clientHeight: el.clientHeight,
  }));
  const topLabels = await page.locator(".ix-command-item").allTextContents();
  const stale1 = await page.locator('.ix-command-item', { hasText: /Open Chart Workspace|Open Advisory Signals|Open Performance Analytics/ }).count();
  const newLabels1 = await page.locator('.ix-command-item', { hasText: /Open Chart Stage|Open Signals Dock|Open Intelligence Dock/ }).count();
  await page.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P02-R1_01_PALETTE_EMPTY_QUERY_TOP.png") });
  await record("01_PALETTE_TOP", {
    url: page.url(),
    menuItems: items1,
    groups: groups1,
    scroll: listBox1,
    staleLabels: stale1,
    relabeledEntries: newLabels1,
    firstSixLabels: topLabels.slice(0, 6),
  });

  // ---- Capture 2: palette scrolled to bottom ----
  await page.locator(".ix-command-list").first().evaluate((el) => { el.scrollTop = el.scrollHeight; });
  await page.waitForTimeout(600);
  const listBox2 = await page.locator(".ix-command-list").first().evaluate((el) => ({
    scrollTop: el.scrollTop,
    scrollHeight: el.scrollHeight,
    clientHeight: el.clientHeight,
  }));
  const items2 = await page.locator('.ix-command-item[role="menuitem"]').count();
  await page.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P02-R1_02_PALETTE_EMPTY_QUERY_SCROLLED_BOTTOM.png") });
  await record("02_PALETTE_SCROLLED", { url: page.url(), menuItems: items2, scroll: listBox2 });

  // ---- Capture 3: click Open Chart Stage ----
  await page.locator(".ix-command-list").first().evaluate((el) => { el.scrollTop = 0; });
  await page.waitForTimeout(300);
  await page.locator('button[data-command-id="qa.open.charts"]').first().click();
  await page.waitForTimeout(1500);
  const chartStageVisible = await page.locator('[data-testid="terminal-chart-stage"]').count();
  await page.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P02-R1_03_PALETTE_CHART_STAGE_NAVIGATION.png") });
  await record("03_CHART_STAGE_NAV", { url: page.url(), terminalChartStageCount: chartStageVisible });

  // ---- Capture 4: signals drill-down full interval ----
  await page.locator('[data-testid="right-dock-tab-signals"]').first().click();
  await page.waitForTimeout(1200);
  await page.locator(".signal-card").first().click();
  await page.waitForTimeout(900);
  const confTexts = await page.locator('[data-testid^="signal-confidence-"]').allTextContents();
  const expandedCount = await page.locator('[data-testid^="signal-expanded-"]').count();
  const clipped = await page.locator(".metric-value-uncertainty").allTextContents();
  // OBS-CONV2-1 width proof: the scroll container must not overflow horizontally
  // and the expanded body must fit within the dock width.
  const dockFit = await page.locator(".signals-cards-list").first().evaluate((el) => ({
    scrollWidth: el.scrollWidth,
    clientWidth: el.clientWidth,
    scrollHeight: el.scrollHeight,
    clientHeight: el.clientHeight,
    horizontalOverflow: el.scrollWidth > el.clientWidth + 1,
    verticalScrollable: el.scrollHeight > el.clientHeight + 1,
  }));
  const provenanceTexts = await page.locator(".provenance-id-row").first().allTextContents();
  const lineageTexts = await page.locator(".kv-grid").first().allTextContents();
  await page.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P02-R1_04_SIGNALS_DRILLDOWN_FULL_INTERVAL.png") });
  await record("04_SIGNALS_DRILLDOWN", {
    url: page.url(),
    confidenceTexts: confTexts,
    expandedSections: expandedCount,
    uncertaintyTexts: clipped,
    dockFit,
    provenanceRowText: provenanceTexts,
    lineageGridText: lineageTexts,
  });

  // ---- Capture 5: intelligence dock ----
  await page.locator('[data-testid="right-dock-tab-intelligence"]').first().click();
  await page.waitForTimeout(1500);
  const valTexts = await page.locator('[data-testid^="val-"]').allTextContents();
  const uncTexts = await page.locator(".box-unc").allTextContents();
  await page.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P02-R1_05_INTELLIGENCE_DOCK_HONEST_INTERVALS.png") });
  await record("05_INTELLIGENCE_DOCK", { url: page.url(), metricTexts: valTexts, uncertaintyTexts: uncTexts });

  // ---- Capture 6: withheld+expired verbatim state ----
  await page.locator('[data-testid="right-dock-tab-signals"]').first().click();
  await page.waitForTimeout(1200);
  const sig4 = page.locator('[data-testid="signal-card-sig-004"]').first();
  const sig4Exists = await sig4.count();
  if (sig4Exists) {
    await sig4.click();
    await page.waitForTimeout(700);
  }
  const stateBadge = sig4Exists ? await page.locator('[data-testid="signal-state-sig-004"]').allTextContents() : [];
  const freshness = sig4Exists ? await page.locator('[data-testid="signal-freshness-sig-004"]').allTextContents() : [];
  await page.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P02-R1_06_WITHHELD_EXPIRED_VERBATIM_STATE.png") });
  await record("06_MIXED_STATE", { url: page.url(), cardPresent: sig4Exists, stateBadge, freshnessTag: freshness });

  await browser.close();
  fs.writeFileSync(path.join(EVIDENCE_DIR, "UI-CONV-P02-R1_CAPTURE_VERIFICATION.json"), JSON.stringify(LOG, null, 2));
  console.log("VERIFICATION COMPLETE");
}

run().catch((err) => { console.error(err); process.exit(1); });
