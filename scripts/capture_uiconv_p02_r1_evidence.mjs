import { chromium } from "../frontend/node_modules/playwright/index.mjs";
import fs from "fs";
import path from "path";

const EVIDENCE_DIR = "/home/user/axiom/docs/evidence/uiconv";

if (!fs.existsSync(EVIDENCE_DIR)) {
  fs.mkdirSync(EVIDENCE_DIR, { recursive: true });
}

async function run() {
  const browser = await chromium.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1,
  });

  const page = await context.newPage();

  // Log in
  console.log("Logging in with operator credentials...");
  await page.goto("http://localhost:5173/login", { waitUntil: "networkidle" });
  await page.waitForTimeout(1000);

  const userField = page.locator('input[data-testid="login-username-input"], input#username-input').first();
  const passField = page.locator('input[data-testid="login-password-input"], input#password-input').first();
  await userField.fill("admin");
  await passField.fill("AxiomSecurePass2026!");
  await page.click('button[type="submit"]');
  await page.waitForTimeout(2500);

  // Terminal root
  await page.goto("http://localhost:5173/", { waitUntil: "networkidle" });
  await page.waitForTimeout(1500);

  // -------------------------------------------------------------
  // Capture 1: Command Palette empty query — TOP (CA-CONV2-1)
  // -------------------------------------------------------------
  console.log("Capture 1: Command Palette empty query (top)...");
  await page.keyboard.press("Control+k");
  await page.waitForTimeout(800);

  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-CONV-P02-R1_01_PALETTE_EMPTY_QUERY_TOP.png"),
    fullPage: false,
  });

  // -------------------------------------------------------------
  // Capture 2: Command Palette empty query — SCROLLED to bottom (CA-CONV2-1)
  // Proves the panel scrolls and every group enumerates.
  // -------------------------------------------------------------
  console.log("Capture 2: Command Palette empty query (scrolled to bottom)...");
  const list = page.locator(".ix-command-list").first();
  if (await list.isVisible()) {
    await list.evaluate((el) => {
      el.scrollTop = el.scrollHeight;
    });
    await page.waitForTimeout(600);
  }

  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-CONV-P02-R1_02_PALETTE_EMPTY_QUERY_SCROLLED_BOTTOM.png"),
    fullPage: false,
  });

  // -------------------------------------------------------------
  // Capture 3: Click "Open Chart Stage" -> terminal chart stage (CA-CONV2-1)
  // -------------------------------------------------------------
  console.log("Capture 3: Open Chart Stage palette navigation...");
  await list.evaluate((el) => {
    el.scrollTop = 0;
  });
  await page.waitForTimeout(300);
  const chartStageCmd = page.locator('button[data-command-id="qa.open.charts"]').first();
  if (await chartStageCmd.isVisible()) {
    await chartStageCmd.click();
    await page.waitForTimeout(1500);
  }

  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-CONV-P02-R1_03_PALETTE_CHART_STAGE_NAVIGATION.png"),
    fullPage: false,
  });

  // -------------------------------------------------------------
  // Capture 4: Signals dock drill-down — full Wilson interval (OBS-CONV2-1)
  // -------------------------------------------------------------
  console.log("Capture 4: Signals dock drill-down with full interval...");
  const signalsTab = page.locator('[data-testid="right-dock-tab-signals"]').first();
  if (await signalsTab.isVisible()) {
    await signalsTab.click();
    await page.waitForTimeout(1200);
  }
  const firstSignalCard = page.locator(".signal-card").first();
  if (await firstSignalCard.isVisible()) {
    await firstSignalCard.click();
    await page.waitForTimeout(900);
  }

  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-CONV-P02-R1_04_SIGNALS_DRILLDOWN_FULL_INTERVAL.png"),
    fullPage: false,
  });

  // -------------------------------------------------------------
  // Capture 5: Intelligence dock — canonical metrics, honest intervals (OBS-CONV2-1)
  // -------------------------------------------------------------
  console.log("Capture 5: Intelligence dock calibration metrics...");
  const intelTab = page.locator('[data-testid="right-dock-tab-intelligence"]').first();
  if (await intelTab.isVisible()) {
    await intelTab.click();
    await page.waitForTimeout(1200);
  }

  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-CONV-P02-R1_05_INTELLIGENCE_DOCK_HONEST_INTERVALS.png"),
    fullPage: false,
  });

  // -------------------------------------------------------------
  // Capture 6: Withheld signal with expired freshness — verbatim state (OBS-CONV2-3)
  // -------------------------------------------------------------
  console.log("Capture 6: Withheld+expired signal verbatim state...");
  if (await signalsTab.isVisible()) {
    await signalsTab.click();
    await page.waitForTimeout(1200);
  }
  const mixedCard = page.locator('[data-testid="signal-card-sig-004"]').first();
  if (await mixedCard.isVisible()) {
    await mixedCard.click();
    await page.waitForTimeout(700);
  }

  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-CONV-P02-R1_06_WITHHELD_EXPIRED_VERBATIM_STATE.png"),
    fullPage: false,
  });

  await browser.close();
  console.log("Capture complete.");
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
